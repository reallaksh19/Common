#!/usr/bin/env python3
"""Validate a Grade 9 Chemistry publication package.

This validator is intentionally chapter-agnostic. It derives topic/artifact and
external-corpus counters from records and enforces the Chemistry two-file topic
contract:

- Core Study Guide with Appendix A Core Practice, Appendix B Core Solutions,
  Appendix C Printable Handout;
- ExamSIDE Solution & Transfer with concept segregation, badges, H0/hints,
  Core/source links and complete solutions.

Exit codes:
  0 technical PASS
  1 validation mismatch/failure
  2 blocking state (for example exact learner artifact bytes unavailable)
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - explicit blocking dependency state
    PdfReader = None


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(root: Path, value: str | None) -> Path | None:
    if not value:
        return None
    p = Path(value)
    return p if p.is_absolute() else root / p


def validate_topic_delivery(root: Path, delivery: dict, failures: list[str]) -> tuple[str, set[str]]:
    topic_id = str(delivery.get("topic_id") or "<missing-topic>")
    core = delivery.get("core_study_guide") or {}
    exam = delivery.get("examside_solution_transfer") or {}

    if not core or not exam:
        failures.append(f"{topic_id}: topic must define both Core Study Guide and ExamSIDE Solution & Transfer")
        return topic_id, set()

    roles = {core.get("artifact_role"), exam.get("artifact_role")}
    if roles != {"CORE_STUDY_GUIDE", "EXAMSIDE_SOLUTION_TRANSFER"}:
        failures.append(f"{topic_id}: topic artifact roles must be exactly CORE_STUDY_GUIDE + EXAMSIDE_SOLUTION_TRANSFER")

    app = core.get("appendices") or {}
    required_appendices = {
        "A": ("CORE_PRACTICE", False),
        "B": ("CORE_SOLUTIONS", False),
        "C": ("PRINTABLE_HANDOUT", True),
    }
    for key, (role, handout) in required_appendices.items():
        item = app.get(key)
        if not isinstance(item, dict):
            failures.append(f"{topic_id}: missing Appendix {key}")
            continue
        if item.get("role") != role or item.get("present") is not True:
            failures.append(f"{topic_id}: Appendix {key} must be present with role {role}")
        if handout:
            if item.get("printable_handout") is not True:
                failures.append(f"{topic_id}: Appendix C must be explicitly marked printable_handout=true")
            if item.get("introduces_new_chemistry") is not False:
                failures.append(f"{topic_id}: Appendix C must declare introduces_new_chemistry=false")

    qc = exam.get("question_contract") or {}
    mandatory = [
        "source_badge",
        "difficulty_badge",
        "transfer_badge",
        "primary_concept_label",
        "concept_segregation_label",
        "core_cross_link",
        "h0_attempt_first",
        "progressive_hints",
        "complete_solution",
        "source_link",
    ]
    for field in mandatory:
        if qc.get(field) is not True:
            failures.append(f"{topic_id}: ExamSIDE question_contract.{field} must be true")

    return topic_id, {str(core.get("artifact_id")), str(exam.get("artifact_id"))}


def validate_external_corpus(root: Path, path: Path, failures: list[str]) -> dict:
    ledger = load_json(path)
    records = ledger.get("records")
    if records is None:
        # Sharded corpora remain valid only if a package-specific reconciler has
        # materialised record shards before this generic gate.
        failures.append(f"external corpus {path.name}: records array missing; derive/materialise records before validation")
        return {}

    if not isinstance(records, list):
        failures.append(f"external corpus {path.name}: records must be an array")
        return {}

    ids = [r.get("candidate_id") for r in records]
    if any(not x for x in ids):
        failures.append(f"external corpus {path.name}: every record needs candidate_id")
    if len(ids) != len(set(ids)):
        failures.append(f"external corpus {path.name}: duplicate candidate_id")

    scope = Counter(r.get("scope_status") for r in records)
    declared = (ledger.get("snapshot") or {}).get("candidate_count_declared")
    if declared is not None and int(declared) != len(records):
        failures.append(f"external corpus {path.name}: declared candidate count {declared} != derived {len(records)}")

    by_unit = Counter()
    for r in records:
        if r.get("scope_status") != "ELIGIBLE_IN_SCOPE":
            continue
        if not r.get("stem") or r.get("answer") is None:
            failures.append(f"{r.get('candidate_id')}: eligible record needs verified stem and answer")
        src = r.get("source_identity") or {}
        if not src.get("source_url_or_locator"):
            failures.append(f"{r.get('candidate_id')}: eligible record missing source URL/locator")
        support = r.get("publication_support") or {}
        required = [
            "primary_unit_id",
            "primary_concept_id",
            "concept_segregation_label",
            "difficulty_badge",
            "transfer_badge",
            "source_badge",
            "transfer_book_id",
            "question_id",
            "required_hint_depth",
            "core_cross_link_status",
            "full_solution_status",
            "source_link_status",
            "placement_status",
        ]
        for field in required:
            if support.get(field) in (None, ""):
                failures.append(f"{r.get('candidate_id')}: eligible publication_support missing {field}")
        if support.get("h0_attempt_first") is not True:
            failures.append(f"{r.get('candidate_id')}: H0 attempt-first state is required")
        if support.get("full_solution_status") != "PASS":
            failures.append(f"{r.get('candidate_id')}: complete solution status must PASS")
        if support.get("core_cross_link_status") != "PASS":
            failures.append(f"{r.get('candidate_id')}: Core cross-link status must PASS")
        if support.get("source_link_status") != "PASS":
            failures.append(f"{r.get('candidate_id')}: source link status must PASS")
        if support.get("placement_status") != "PLACED":
            failures.append(f"{r.get('candidate_id')}: final eligible placement must be PLACED")
        if support.get("primary_unit_id"):
            by_unit[support["primary_unit_id"]] += 1

    return {
        "candidate_total": len(records),
        "scope_counts": dict(scope),
        "eligible_by_primary_unit": dict(by_unit),
    }


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    package_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("Chemistry_Publication_Package.json")
    package_path = package_path if package_path.is_absolute() else root / package_path

    failures: list[str] = []
    blockers: list[str] = []
    observations: dict = {"topics": {}, "artifacts": {}, "external_corpus": {}}

    if not package_path.is_file():
        print(json.dumps({"status": "BLOCKED", "blockers": [f"missing package model: {package_path}"]}, indent=2))
        return 2

    package = load_json(package_path)
    if package.get("subject") != "Chemistry":
        failures.append("package subject must be Chemistry")

    deliveries = package.get("topic_deliveries") or []
    if not deliveries:
        failures.append("package must contain at least one topic_delivery")

    expected_topic_artifact_ids: dict[str, set[str]] = {}
    for item in deliveries:
        if isinstance(item, str):
            p = resolve(root, item)
            if not p or not p.is_file():
                blockers.append(f"missing topic delivery record: {item}")
                continue
            delivery = load_json(p)
        elif isinstance(item, dict):
            delivery = item
        else:
            failures.append("topic_deliveries entries must be paths or objects")
            continue
        topic_id, ids = validate_topic_delivery(root, delivery, failures)
        expected_topic_artifact_ids[topic_id] = ids
        observations["topics"][topic_id] = {"artifact_ids": sorted(ids)}

    artifacts = package.get("artifacts") or []
    by_topic: dict[str, list[dict]] = defaultdict(list)
    by_id: dict[str, dict] = {}
    for art in artifacts:
        aid = str(art.get("artifact_id") or "")
        if not aid:
            failures.append("artifact missing artifact_id")
            continue
        if aid in by_id:
            failures.append(f"duplicate artifact_id: {aid}")
        by_id[aid] = art
        if art.get("topic_id"):
            by_topic[str(art["topic_id"])].append(art)

        p = resolve(root, art.get("filename"))
        if not p or not p.is_file():
            blockers.append(f"exact learner artifact unavailable: {art.get('filename') or aid}")
            continue
        if art.get("sha256") and sha256(p) != art.get("sha256"):
            failures.append(f"{aid}: sha256 mismatch")
        if PdfReader is None:
            blockers.append("pypdf dependency unavailable; cannot verify PDF page identity")
            continue
        try:
            reader = PdfReader(str(p))
            pages = len(reader.pages)
            if art.get("pages") and pages != int(art["pages"]):
                failures.append(f"{aid}: page count {pages} != declared {art['pages']}")
            observations["artifacts"][aid] = {"pages": pages, "sha256": sha256(p)}
        except Exception as exc:
            failures.append(f"{aid}: PDF parse failed: {exc}")

    for topic_id, expected_ids in expected_topic_artifact_ids.items():
        actual = {str(a.get("artifact_id")) for a in by_topic.get(topic_id, []) if a.get("artifact_role") in {"CORE_STUDY_GUIDE", "EXAMSIDE_SOLUTION_TRANSFER"}}
        if actual != expected_ids or len(actual) != 2:
            failures.append(f"{topic_id}: exactly two topic artifacts required; expected {sorted(expected_ids)}, got {sorted(actual)}")

    external_path = resolve(root, package.get("external_corpus_path"))
    if external_path:
        if not external_path.is_file():
            blockers.append(f"missing external corpus ledger: {external_path}")
        else:
            observations["external_corpus"] = validate_external_corpus(root, external_path, failures)

    manifest_path = resolve(root, package.get("file_manifest_path") or "FILE_MANIFEST.json")
    if manifest_path and manifest_path.is_file():
        manifest = load_json(manifest_path)
        for rel, meta in (manifest.get("files") or {}).items():
            p = resolve(root, rel)
            if not p or not p.is_file():
                failures.append(f"manifest path missing: {rel}")
            elif meta.get("sha256") and sha256(p) != meta["sha256"]:
                failures.append(f"manifest hash mismatch: {rel}")

    if failures:
        status, code = "FAIL", 1
    elif blockers:
        status, code = "BLOCKED", 2
    else:
        status, code = "PASS", 0

    print(json.dumps({
        "status": status,
        "failures": failures,
        "blockers": sorted(set(blockers)),
        "observations": observations,
    }, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
