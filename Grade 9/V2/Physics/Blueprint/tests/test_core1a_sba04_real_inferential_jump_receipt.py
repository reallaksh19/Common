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
RECEIPT_REF = "topics/m2d-sba04-stage-evidence/1a2-inferential-jump-closure.v1.json"
SPEC = load_blueprint(SPEC_REF)
EXPECTED_HIGH_FRAGILITY_JUMPS = {
    "PHY-M2D-VELOCITY-EVOLUTION:RS-M2D-VE-APEX",
    "PHY-M2D-VELOCITY-DIRECTION:RS-M2D-VD-ANGLE",
    "PHY-M2D-SPEED-MAGNITUDE:RS-M2D-SM-APEX",
    "PHY-M2D-SAME-HEIGHT-VELOCITY:RS-M2D-SH-COMPARE",
    "PHY-M2D-PERPENDICULAR-VELOCITY:RS-M2D-PV-IDENTIFY",
    "PHY-M2D-PERPENDICULAR-VELOCITY:RS-M2D-PV-DOT",
    "PHY-M2D-SPEED-AT-HEIGHT:RS-M2D-SHGT-ORIGIN",
    "PHY-M2D-SPEED-AT-HEIGHT:RS-M2D-SHGT-SPEED",
}


def stage_row(audit: dict, stage: str) -> dict:
    return next(row for row in audit["stage_audit"] if row["stage"] == stage)


# Canonical authority now binds the complete real receipt chain; this probe overwrites it to test 1A2 isolation.
assert len(SPEC["stage_evidence_refs"]) == 9
assert RECEIPT_REF in SPEC["stage_evidence_refs"]

# Real-data probe: the governed SBA04 receipt closes exactly the eight live HIGH_FRAGILITY jumps.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [RECEIPT_REF]
audit = compile_audit(probe, spec_ref=SPEC_REF)

jump_stage = stage_row(audit, "1A2_INFERENTIAL_JUMPS")
unresolved_stage = stage_row(audit, "1A11_UNRESOLVED_JUMP_AUDIT")
assert jump_stage["evidence_state"] == "PRESENT"
assert set(jump_stage["artifact_refs"]) == EXPECTED_HIGH_FRAGILITY_JUMPS
assert len(jump_stage["artifact_refs"]) == 8
assert jump_stage["notes"] == [
    "Promoted by governed migration evidence receipt M2D-SBA04-1A2-INFERENTIAL-JUMP-CLOSURE-V1."
]
assert RECEIPT_REF in audit["source_refs"]

# Closing the atom-by-atom jump evidence is not permission to infer the independent unresolved-jump audit.
assert unresolved_stage["evidence_state"] == "PARTIAL"
assert audit["release_authorized"] is False
assert any(reason.startswith("PARTIAL_STAGE_EVIDENCE:") for reason in audit["block_reasons"])

print("Core1A SBA04 real inferential-jump receipt: PASS (8/8 high-fragility jumps; 1A11 and release remain closed in isolation)")
