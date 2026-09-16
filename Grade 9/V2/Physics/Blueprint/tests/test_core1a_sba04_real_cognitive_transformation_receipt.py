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
SPEC = load_blueprint(SPEC_REF)


def stage_state(audit: dict, stage: str) -> str:
    return next(row for row in audit["stage_audit"] if row["stage"] == stage)["evidence_state"]


# Canonical binding is active; this probe overwrites it to prove the real 1A2 -> 1A3 chain independently.
assert len(SPEC["stage_evidence_refs"]) == 9
assert JUMP_RECEIPT in SPEC["stage_evidence_refs"]
assert TRANSFORMATION_RECEIPT in SPEC["stage_evidence_refs"]
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [JUMP_RECEIPT, TRANSFORMATION_RECEIPT]
audit = compile_audit(probe, spec_ref=SPEC_REF)

assert stage_state(audit, "1A2_INFERENTIAL_JUMPS") == "PRESENT"
assert stage_state(audit, "1A3_COGNITIVE_TRANSFORMATION") == "PRESENT"
assert stage_state(audit, "1A4_REPRESENTATION_REQUIREMENTS") == "PARTIAL"
assert stage_state(audit, "1A11_UNRESOLVED_JUMP_AUDIT") == "PARTIAL"
assert audit["release_authorized"] is False
assert JUMP_RECEIPT in audit["source_refs"]
assert TRANSFORMATION_RECEIPT in audit["source_refs"]

print("Core1A SBA04 real cognitive-transformation receipt: PASS (1A2/1A3 admissible in isolation; later stages remain fail-closed)")
