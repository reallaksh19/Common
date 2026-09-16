#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_core1a_real_bucket_migration import compile_audit_with_facts  # noqa: E402
from validate_core1a_real_bucket_migration import load_blueprint  # noqa: E402

SPEC_REF = "topics/m2d-sba04-core1a-migration-spec.v1.json"
JUMP_RECEIPT = "topics/m2d-sba04-stage-evidence/1a2-inferential-jump-closure.v1.json"
AUDIT_REF = "topics/m2d-sba04-design/unresolved-jump-audit.v1.json"
CLOSURE_RECEIPT = "topics/m2d-sba04-stage-evidence/1a11-unresolved-jump-closure.v1.json"
CHAIN = [
    JUMP_RECEIPT,
    "topics/m2d-sba04-stage-evidence/1a3-cognitive-transformation.v1.json",
    "topics/m2d-sba04-stage-evidence/1a4-representation-requirements.v1.json",
    "topics/m2d-sba04-stage-evidence/1a5-representation-candidates.v1.json",
    "topics/m2d-sba04-stage-evidence/1a6-representation-decision.v1.json",
    "topics/m2d-sba04-stage-evidence/1a7-pwse-bridge.v1.json",
    "topics/m2d-sba04-stage-evidence/1a9-worked-faded-independent.v1.json",
    CLOSURE_RECEIPT,
]
SPEC = load_blueprint(SPEC_REF)


def stage_state(audit: dict, stage: str) -> str:
    return next(row for row in audit["stage_audit"] if row["stage"] == stage)["evidence_state"]


assert len(SPEC["stage_evidence_refs"]) == 9
assert set(CHAIN).issubset(SPEC["stage_evidence_refs"])
closure_audit = load_blueprint(AUDIT_REF)
jump_receipt = load_blueprint(JUMP_RECEIPT)
closure_receipt = load_blueprint(CLOSURE_RECEIPT)

probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = CHAIN
audit, facts = compile_audit_with_facts(probe, spec_ref=SPEC_REF)

live_required = set(facts["high_fragility_step_refs"])
receipt_closed = {row["jump_ref"] for row in jump_receipt["proof"]["jump_rows"]}
audited_required = set(closure_audit["required_jump_refs"])
audited_closed = set(closure_audit["closed_jump_refs"])
proof_required = set(closure_receipt["proof"]["required_jump_refs"])

assert len(live_required) == 8
assert live_required == receipt_closed == audited_required == audited_closed == proof_required
assert closure_audit["unresolved_jump_refs"] == []
assert closure_audit["unresolved_required_jump_count"] == 0
assert closure_receipt["proof"]["unresolved_jump_refs"] == []
assert closure_receipt["proof"]["unresolved_required_jump_count"] == 0
assert stage_state(audit, "1A11_UNRESOLVED_JUMP_AUDIT") == "PRESENT"

# In this isolation probe 1A0 is deliberately omitted; Q14/Q27 are already operationally released by the completed SBA05 bridge.
assert stage_state(audit, "1A0_LEARNER_STATE_GAP") == "LEGACY_ONLY"
assert audit["release_authorized"] is False
assert audit["block_reasons"] == ["LEGACY_ONLY_STAGE_EVIDENCE:1A0_LEARNER_STATE_GAP"]
assert facts["held_questions"] == []

print("Core1A SBA04 unresolved-jump audit: PASS (live 8/8 closure exact; isolation remains closed only because 1A0 is omitted)")
