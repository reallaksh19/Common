#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_core1a_real_bucket_migration import compile_audit  # noqa: E402
from validate_core1a_real_bucket_migration import load_blueprint  # noqa: E402

SPEC_REF = "topics/m2d-sba04-core1a-migration-spec.v1.json"
CHAIN = [
    "topics/m2d-sba04-stage-evidence/1a2-inferential-jump-closure.v1.json",
    "topics/m2d-sba04-stage-evidence/1a3-cognitive-transformation.v1.json",
    "topics/m2d-sba04-stage-evidence/1a4-representation-requirements.v1.json",
    "topics/m2d-sba04-stage-evidence/1a5-representation-candidates.v1.json",
    "topics/m2d-sba04-stage-evidence/1a6-representation-decision.v1.json",
    "topics/m2d-sba04-stage-evidence/1a7-pwse-bridge.v1.json",
]
PLAN_REF = "topics/m2d-sba04-design/pwse-bridge-plan.v1.json"
SPEC = load_blueprint(SPEC_REF)


def stage_row(audit: dict, stage: str) -> dict:
    return next(row for row in audit["stage_audit"] if row["stage"] == stage)


assert len(SPEC["stage_evidence_refs"]) == 9
assert set(CHAIN).issubset(SPEC["stage_evidence_refs"])
plan = load_blueprint(PLAN_REF)
assert [row["learning_atom_ref"] for row in plan["bridges"]] == [f"M2D-SBA-04{x}" for x in "ABCDEFG"]

probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = CHAIN
audit = compile_audit(probe, spec_ref=SPEC_REF)

for stage in (
    "1A2_INFERENTIAL_JUMPS",
    "1A3_COGNITIVE_TRANSFORMATION",
    "1A4_REPRESENTATION_REQUIREMENTS",
    "1A5_REPRESENTATION_CANDIDATES",
    "1A6_REPRESENTATION_DECISIONS",
    "1A7_PICTURE_WORD_SYMBOL_EQUATION_BRIDGE",
):
    assert stage_row(audit, stage)["evidence_state"] == "PRESENT", stage

bridge_stage = stage_row(audit, "1A7_PICTURE_WORD_SYMBOL_EQUATION_BRIDGE")
assert bridge_stage["artifact_refs"] == [f"M2D-SBA-04{x}" for x in "ABCDEFG"]
assert stage_row(audit, "1A9_WORKED_FADED_INDEPENDENT_PLAN")["evidence_state"] == "PARTIAL"
assert stage_row(audit, "1A11_UNRESOLVED_JUMP_AUDIT")["evidence_state"] == "PARTIAL"
assert audit["release_authorized"] is False
assert PLAN_REF in audit["source_refs"]

print("Core1A SBA04 PWSE bridge: PASS (7/7 atoms bridged; worked/faded and unresolved-jump authority remain closed in isolation)")
