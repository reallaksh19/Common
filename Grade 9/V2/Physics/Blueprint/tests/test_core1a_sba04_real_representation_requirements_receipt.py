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
JUMP_RECEIPT = "topics/m2d-sba04-stage-evidence/1a2-inferential-jump-closure.v1.json"
TRANSFORMATION_RECEIPT = "topics/m2d-sba04-stage-evidence/1a3-cognitive-transformation.v1.json"
REP_REQUIREMENTS_RECEIPT = "topics/m2d-sba04-stage-evidence/1a4-representation-requirements.v1.json"
SPEC = load_blueprint(SPEC_REF)
EXPECTED_REPRESENTATIONS = {
    "REP-M2D-VELOCITY-STAGE-TIMELINE",
    "REP-M2D-VELOCITY-DIRECTION-TRIANGLE",
    "REP-M2D-SPEED-TRIANGLE",
    "REP-M2D-SAME-HEIGHT-PAIR",
    "REP-M2D-PERP-VELOCITY-PAIR",
    "REP-M2D-SPEED-AT-HEIGHT",
}


def stage_row(audit: dict, stage: str) -> dict:
    return next(row for row in audit["stage_audit"] if row["stage"] == stage)


# Canonical binding is active; overwrite it here to preserve the 1A4 isolation boundary.
assert len(SPEC["stage_evidence_refs"]) == 9
assert {JUMP_RECEIPT, TRANSFORMATION_RECEIPT, REP_REQUIREMENTS_RECEIPT}.issubset(SPEC["stage_evidence_refs"])
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [JUMP_RECEIPT, TRANSFORMATION_RECEIPT, REP_REQUIREMENTS_RECEIPT]
audit = compile_audit(probe, spec_ref=SPEC_REF)

assert stage_row(audit, "1A2_INFERENTIAL_JUMPS")["evidence_state"] == "PRESENT"
assert stage_row(audit, "1A3_COGNITIVE_TRANSFORMATION")["evidence_state"] == "PRESENT"
rep_stage = stage_row(audit, "1A4_REPRESENTATION_REQUIREMENTS")
assert rep_stage["evidence_state"] == "PRESENT"
assert set(rep_stage["artifact_refs"]) == EXPECTED_REPRESENTATIONS
assert len(rep_stage["artifact_refs"]) == 6

# Requirements do not manufacture candidate comparison, selection, or a complete PWSE bridge.
assert stage_row(audit, "1A5_REPRESENTATION_CANDIDATES")["evidence_state"] == "MISSING"
assert stage_row(audit, "1A6_REPRESENTATION_DECISIONS")["evidence_state"] == "MISSING"
assert stage_row(audit, "1A7_PICTURE_WORD_SYMBOL_EQUATION_BRIDGE")["evidence_state"] == "PARTIAL"
assert stage_row(audit, "1A11_UNRESOLVED_JUMP_AUDIT")["evidence_state"] == "PARTIAL"
assert audit["release_authorized"] is False
assert REP_REQUIREMENTS_RECEIPT in audit["source_refs"]

print("Core1A SBA04 real representation-requirements receipt: PASS (6/6 direct-gate representations; later authority remains closed in isolation)")
