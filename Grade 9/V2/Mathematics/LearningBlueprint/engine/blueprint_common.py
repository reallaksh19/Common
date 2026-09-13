#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTRACTS = ROOT / "contracts"

EVIDENCE_STATES = {"PRESENT", "ABSENT", "PARTIAL", "UNRESOLVED", "CONFLICTED"}
GROUND_TRUTH_AUTHORITIES = {"ORIGINAL_EVIDENCE", "AUTHORITATIVE_SOURCE"}
RUN_STATES = {
    "GT_READY", "ROUTED", "FIRST_CORE_COMPLETE", "SECOND_CORE_COMPLETE",
    "CROSS_VALIDATED", "JOIN_READY", "ASSIMILATION_COMPILED", "CORE1A_REALIZED",
    "EXPOSURE_RECORDED", "CORE2A_ELIGIBLE", "CORE2A_REALIZED", "FINAL_AUDIT_PASS",
    "BLOCKED_EVIDENCE", "BLOCKED_CONFLICT", "BLOCKED_PREREQUISITE",
    "BLOCKED_REPRESENTATION", "BLOCKED_EXPOSURE", "BLOCKED_OWNER_REVIEW",
}
RUN_ID_RE = re.compile(r"^MATH-MLR-[0-9a-f]{16}$")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def file_digest(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_schema(instance: dict, schema_name: str) -> None:
    schema = load(CONTRACTS / schema_name)
    jsonschema.validate(instance, schema)


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def validate_ground_truth_manifest(manifest: dict) -> None:
    validate_schema(manifest, "math-ground-truth-manifest.schema.json")
    if manifest.get("manifest_digest") != digest(manifest, "manifest_digest"):
        fail("GROUND_TRUTH_MANIFEST_DIGEST_MISMATCH")
    seen = set()
    for item in manifest.get("evidence_items", []):
        eid = item["evidence_id"]
        if eid in seen:
            fail("GROUND_TRUTH_EVIDENCE_ID_DUPLICATE", eid)
        seen.add(eid)
        if item["authority_class"] not in GROUND_TRUTH_AUTHORITIES:
            fail("GROUND_TRUTH_AUTHORITY_CLASS_FORBIDDEN", item["authority_class"])
        if item["availability"] == "ABSENT":
            if item["ref"] is not None or item["digest"] is not None:
                fail("ABSENT_EVIDENCE_HAS_SOURCE_BINDING", eid)
        else:
            if not item["ref"] or not item["digest"]:
                fail("AVAILABLE_EVIDENCE_BINDING_MISSING", eid)
        if item["availability"] == "CONFLICTED" and not item["conflict_refs"]:
            fail("CONFLICTED_EVIDENCE_WITHOUT_CONFLICT_REFS", eid)


def validate_learning_run(run: dict) -> None:
    validate_schema(run, "math-learning-run-blueprint.schema.json")
    if run.get("run_digest") != digest(run, "run_digest"):
        fail("LEARNING_RUN_DIGEST_MISMATCH")
    if not run.get("state_history"):
        fail("LEARNING_RUN_STATE_HISTORY_EMPTY")
    seq = [x["sequence"] for x in run["state_history"]]
    if seq != list(range(len(seq))):
        fail("LEARNING_RUN_STATE_HISTORY_SEQUENCE_INVALID")
    if run["state_history"][-1]["state"] != run["current_state"]:
        fail("LEARNING_RUN_CURRENT_STATE_MISMATCH")
    bundle_ids = set()
    for bundle in run.get("bundles", []):
        if bundle["bundle_id"] in bundle_ids:
            fail("HANDOFF_BUNDLE_ID_DUPLICATE", bundle["bundle_id"])
        bundle_ids.add(bundle["bundle_id"])
        if not 1 <= len(bundle["subtopic_refs"]) <= 3:
            fail("HANDOFF_BUNDLE_TOO_LARGE", bundle["bundle_id"])


def seal_ground_truth(manifest: dict) -> dict:
    out = copy.deepcopy(manifest)
    out["manifest_id"] = "MATH-GT-" + digest({k: v for k, v in out.items() if k not in {"manifest_id", "manifest_digest"}})[:16]
    out["manifest_digest"] = digest(out, "manifest_digest")
    validate_ground_truth_manifest(out)
    return out


def seal_learning_run(run: dict) -> dict:
    out = copy.deepcopy(run)
    # A run is one evolving orchestration record. Assign identity once from the
    # initial ground-truth/control-plane binding, then preserve it across state
    # transitions while run_digest changes with state.
    if not RUN_ID_RE.fullmatch(str(out.get("run_id") or "")):
        identity = {
            "ground_truth_ref": out.get("ground_truth_ref"),
            "ground_truth_digest": out.get("ground_truth_digest"),
            "initial_control_plane": copy.deepcopy(out.get("control_plane") or {}),
        }
        out["run_id"] = "MATH-MLR-" + digest(identity)[:16]
    out["run_digest"] = digest(out, "run_digest")
    validate_learning_run(out)
    return out
