#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_core1a_real_bucket_migration import compile_audit  # noqa: E402
from validate_core1a_real_bucket_migration import load_blueprint  # noqa: E402

SPEC_REF = "topics/m2d-sba04-core1a-migration-spec.v1.json"
LINEAGE_PLAN = "topics/m2d-sba04-design/worked-faded-independent-lineages.v1.json"
LINEAGE_RECEIPT = "topics/m2d-sba04-stage-evidence/1a9-worked-faded-independent.v1.json"
CHAIN = [
    "topics/m2d-sba04-stage-evidence/1a2-inferential-jump-closure.v1.json",
    "topics/m2d-sba04-stage-evidence/1a3-cognitive-transformation.v1.json",
    "topics/m2d-sba04-stage-evidence/1a4-representation-requirements.v1.json",
    "topics/m2d-sba04-stage-evidence/1a5-representation-candidates.v1.json",
    "topics/m2d-sba04-stage-evidence/1a6-representation-decision.v1.json",
    "topics/m2d-sba04-stage-evidence/1a7-pwse-bridge.v1.json",
]
SPEC = load_blueprint(SPEC_REF)


def stage_state(audit: dict, stage: str) -> str:
    return next(row for row in audit["stage_audit"] if row["stage"] == stage)["evidence_state"]


def invariant_digest(value: dict) -> str:
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


assert len(SPEC["stage_evidence_refs"]) == 9
assert set(CHAIN + [LINEAGE_RECEIPT]).issubset(SPEC["stage_evidence_refs"])
plan = load_blueprint(LINEAGE_PLAN)
assert [row["routine_id"] for row in plan["lineages"]] == [f"M2D-SBA-04-R{x}" for x in range(1, 5)]
for row in plan["lineages"]:
    assert row["invariant_fingerprint"] == invariant_digest(row["structural_invariant"]), row["lineage_id"]
    assert row["worked"]["artifact_id"]
    assert row["faded"]["artifact_id"]
    assert row["independent"]["registry_ref"].endswith(".independent_practice")

probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = CHAIN + [LINEAGE_RECEIPT]
audit = compile_audit(probe, spec_ref=SPEC_REF)

assert stage_state(audit, "1A9_WORKED_FADED_INDEPENDENT_PLAN") == "PRESENT"
assert stage_state(audit, "1A10_CORE2_TRANSFER_BRIDGE") == "PRESENT"
assert stage_state(audit, "1A11_UNRESOLVED_JUMP_AUDIT") == "PARTIAL"
assert audit["release_authorized"] is False
assert LINEAGE_PLAN in audit["source_refs"]
assert LINEAGE_RECEIPT in audit["source_refs"]

print("Core1A SBA04 worked/faded/independent lineage: PASS (4/4 structural fingerprints verified; unresolved-jump/release remain closed in isolation)")
