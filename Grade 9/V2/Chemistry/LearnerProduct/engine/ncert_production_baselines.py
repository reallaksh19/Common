#!/usr/bin/env python3
"""Bind LearnerProduct runs to the real NCERT authoring baselines from PR #346.

PR #346 contains two independently-authored denominator statements:

* ``HANDOFF_MANIFEST.json`` records each topic's retained question count and
  answer-path obligations;
* ``tools/validate_handoff.py`` freezes the same counts in ``TOPICS``.

This module treats agreement between those two artifacts as a real
``FROZEN_ELIGIBLE_ONLY`` baseline. It deliberately does *not* invent
``TOTAL_SCANNED`` or exclusion counts because the handoff did not preserve
those counters. A production LearnerProduct run may bind to one of these
baselines, but its live C-J coverage closure must reproduce the retained
question denominator exactly before Core1A/Core2A synthesis proceeds.

The legacy source bundle's reconstructability is reported separately. Bundle
failure is archival evidence debt, not permission to weaken the denominator.
"""
from __future__ import annotations

import ast
import base64
import copy
import hashlib
import io
import json
import tarfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
CHEM_ROOT = HERE.parents[2]
REPO_ROOT = CHEM_ROOT.parents[2]
WORKBENCH = CHEM_ROOT / "AuthoringHandoff" / "NCERT-Core-Workbench"
MANIFEST_PATH = WORKBENCH / "HANDOFF_MANIFEST.json"
VALIDATOR_PATH = WORKBENCH / "tools" / "validate_handoff.py"

EXPECTED_TOPICS = {
    "some-basic-concepts": 68,
    "behaviour-of-gases": 27,
    "chemical-bonding": 38,
    "redox-reactions": 11,
}


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _validator_topics(path: Path = VALIDATOR_PATH) -> dict[str, int]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "TOPICS" for t in node.targets):
            value = ast.literal_eval(node.value)
            return {str(k): int(v) for k, v in value.items()}
    fail("CHEM_LP_PRODUCTION_BASELINE_VALIDATOR_TOPICS_MISSING", str(path))


def validate_topic_tables(manifest: dict[str, Any], validator_topics: dict[str, int]) -> dict[str, dict[str, Any]]:
    topics = {row["id"]: row for row in manifest.get("topics", [])}
    if set(topics) != set(EXPECTED_TOPICS):
        fail("CHEM_LP_PRODUCTION_BASELINE_TOPIC_SET_DRIFT", canonical(sorted(topics)))
    if validator_topics != EXPECTED_TOPICS:
        fail("CHEM_LP_PRODUCTION_BASELINE_VALIDATOR_DRIFT", canonical(validator_topics))

    out: dict[str, dict[str, Any]] = {}
    for topic_id, expected in EXPECTED_TOPICS.items():
        row = topics[topic_id]
        retained = int(row["retained_questions"])
        quick = int(row["required_immediate_answer_checks"])
        full = int(row["required_full_solutions"])
        if retained != expected or validator_topics[topic_id] != retained:
            fail("CHEM_LP_PRODUCTION_BASELINE_DENOMINATOR_DISAGREEMENT", topic_id)
        if quick != retained or full != retained:
            fail("CHEM_LP_PRODUCTION_BASELINE_ANSWER_CLOSURE_DRIFT", topic_id)
        out[topic_id] = {
            "topic_id": topic_id,
            "title": row["title"],
            "retained_questions": retained,
            "required_immediate_answer_checks": quick,
            "required_full_solutions": full,
            "freeze_state": "FROZEN_ELIGIBLE_ONLY",
            "unresolved_counters": ["TOTAL_SCANNED", "EXCLUDED_WITH_REASON", "UNRESOLVED_WITH_REASON"],
        }
    return out


def validate_all_baselines(workbench: Path = WORKBENCH) -> dict[str, Any]:
    manifest_path = workbench / "HANDOFF_MANIFEST.json"
    validator_path = workbench / "tools" / "validate_handoff.py"
    manifest = load_json(manifest_path)
    topics = validate_topic_tables(manifest, _validator_topics(validator_path))
    evidence = {
        "manifest_path": str(manifest_path.relative_to(REPO_ROOT)),
        "manifest_sha256": sha_file(manifest_path),
        "validator_path": str(validator_path.relative_to(REPO_ROOT)),
        "validator_sha256": sha_file(validator_path),
    }
    for topic_id, row in topics.items():
        row["baseline_ref"] = f"CHEM-NCERT-BASELINE:{topic_id}"
        row["baseline_digest"] = digest({
            "topic_id": topic_id,
            "retained_questions": row["retained_questions"],
            "freeze_state": row["freeze_state"],
            "evidence": evidence,
        })
    return {
        "status": "PASS",
        "authority": "PR346_DUAL_EVIDENCE_RETAINED_DENOMINATOR",
        "evidence": evidence,
        "topics": topics,
    }


def baseline_for_topic(topic_id: str, workbench: Path = WORKBENCH) -> dict[str, Any]:
    report = validate_all_baselines(workbench)
    if topic_id not in report["topics"]:
        fail("CHEM_LP_PRODUCTION_BASELINE_UNKNOWN_TOPIC", topic_id)
    return copy.deepcopy(report["topics"][topic_id])


def inspect_legacy_source_bundle(workbench: Path = WORKBENCH) -> dict[str, Any]:
    """Report, but do not conceal, the archival bundle's current integrity state."""
    manifest = load_json(workbench / "HANDOFF_MANIFEST.json")
    spec = manifest["source_bundle"]
    parts = sorted((workbench / spec["directory"]).glob(spec["part_glob"]))
    names = [p.name for p in parts]
    if len(parts) != int(spec["part_count"]):
        return {"status": "FAIL", "reason": "PART_COUNT", "part_names": names}
    try:
        encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        return {"status": "FAIL", "reason": "BASE64", "detail": str(exc), "part_names": names}
    actual_bytes = len(payload)
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    expected_bytes = int(spec["decoded_archive_bytes"])
    expected_sha256 = str(spec["decoded_archive_sha256"])
    archive_ok = False
    members: list[str] = []
    try:
        with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tf:
            members = sorted(m.name for m in tf.getmembers())
            archive_ok = True
    except Exception:
        archive_ok = False
    status = "PASS" if actual_bytes == expected_bytes and actual_sha256 == expected_sha256 and archive_ok else "FAIL"
    return {
        "status": status,
        "actual_bytes": actual_bytes,
        "expected_bytes": expected_bytes,
        "actual_sha256": actual_sha256,
        "expected_sha256": expected_sha256,
        "archive_readable": archive_ok,
        "member_count": len(members),
    }


def _production_fields(run: dict[str, Any]) -> tuple[Any, Any, Any]:
    inputs = run.get("inputs", {})
    return (
        inputs.get("production_topic_id"),
        inputs.get("production_baseline_ref"),
        inputs.get("production_baseline_digest"),
    )


def validate_optional_run_binding_shape(run: dict[str, Any]) -> bool:
    topic_id, ref, bound_digest = _production_fields(run)
    populated = [value not in (None, "") for value in (topic_id, ref, bound_digest)]
    if any(populated) and not all(populated):
        fail("CHEM_LP_PRODUCTION_BASELINE_BINDING_INCOMPLETE")
    return all(populated)


def assert_run_binding(run: dict[str, Any], closure: dict[str, Any], workbench: Path = WORKBENCH) -> dict[str, Any] | None:
    """Bind a live C-LP run to a PR #346 retained denominator before synthesis."""
    if not validate_optional_run_binding_shape(run):
        return None
    topic_id, ref, bound_digest = _production_fields(run)
    baseline = baseline_for_topic(str(topic_id), workbench)
    if ref != baseline["baseline_ref"]:
        fail("CHEM_LP_PRODUCTION_BASELINE_REF_MISMATCH", str(topic_id))
    if bound_digest != baseline["baseline_digest"]:
        fail("CHEM_LP_PRODUCTION_BASELINE_DIGEST_MISMATCH", str(topic_id))

    summary = closure.get("external_matrix", {}).get("summary", {})
    retained = baseline["retained_questions"]
    actual = {
        "eligible": int(summary.get("eligible_total", -1)),
        "placed": int(summary.get("placed_unique_total", -1)),
        "missing": int(summary.get("missing_total", -1)),
        "duplicate": int(summary.get("duplicate_primary_total", -1)),
    }
    expected = {"eligible": retained, "placed": retained, "missing": 0, "duplicate": 0}
    if actual != expected:
        fail(
            "CHEM_LP_PRODUCTION_DENOMINATOR_DRIFT",
            f"{topic_id}:expected={canonical(expected)}:actual={canonical(actual)}",
        )
    return baseline


def main() -> None:
    report = validate_all_baselines()
    report["legacy_source_bundle"] = inspect_legacy_source_bundle()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
