#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_core1a_real_bucket_migration import compile_audit  # noqa: E402
from validate_core1a_real_bucket_migration import load_blueprint  # noqa: E402

SPEC_REF = "topics/m2d-sba04-core1a-migration-spec.v1.json"
INTRINSIC_STATE = "topics/m2d-sba04-design/intrinsic-design-state.v1.json"
CONTROL_STATE = "topics/m2d-sba04-design/learner-purpose-control-state.v1.json"
LEARNER_GAP_RECEIPT = "topics/m2d-sba04-stage-evidence/1a0-learner-state-gap.v1.json"
CHAIN = [
    LEARNER_GAP_RECEIPT,
    "topics/m2d-sba04-stage-evidence/1a2-inferential-jump-closure.v1.json",
    "topics/m2d-sba04-stage-evidence/1a3-cognitive-transformation.v1.json",
    "topics/m2d-sba04-stage-evidence/1a4-representation-requirements.v1.json",
    "topics/m2d-sba04-stage-evidence/1a5-representation-candidates.v1.json",
    "topics/m2d-sba04-stage-evidence/1a6-representation-decision.v1.json",
    "topics/m2d-sba04-stage-evidence/1a7-pwse-bridge.v1.json",
    "topics/m2d-sba04-stage-evidence/1a9-worked-faded-independent.v1.json",
    "topics/m2d-sba04-stage-evidence/1a11-unresolved-jump-closure.v1.json",
]
SPEC = load_blueprint(SPEC_REF)


def digest_without_field(doc: dict, field: str) -> str:
    body = {k: v for k, v in doc.items() if k != field}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


assert SPEC["stage_evidence_refs"] == CHAIN
intrinsic = load_blueprint(INTRINSIC_STATE)
control = load_blueprint(CONTROL_STATE)
control_schema = load_blueprint("contracts/learner-purpose-control-state.schema.json")
Draft202012Validator(control_schema).validate(control)

assert intrinsic["intrinsic_difficulty"] == "D3"
assert intrinsic["student_knowledge_pct_used_for_authored_depth"] is False
assert [row["capability_ref"] for row in intrinsic["requirements"]] == [f"M2D-SBA-04{x}" for x in "ABCDEFG"]
assert control["learner_prior_pct"] == 20
assert control["publication_teaching_receipts_used_as_learner_evidence"] is False
assert all(row["state"] == "UNKNOWN" for row in control["capability_states"])
assert all(row["basis"] == "PRIOR_HEURISTIC" for row in control["capability_states"])
assert control["control_digest"] == digest_without_field(control, "control_digest")

gap_receipt = load_blueprint(LEARNER_GAP_RECEIPT)
assert all(row["learner_state"] == "UNKNOWN" for row in gap_receipt["proof"]["capability_gap_rows"])
assert all(row["gap_assessment"] == "UNKNOWN_GAP" for row in gap_receipt["proof"]["capability_gap_rows"])
assert gap_receipt["proof"]["publication_teaching_receipts_used_as_learner_evidence"] is False

probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = CHAIN
audit = compile_audit(probe, spec_ref=SPEC_REF)

assert all(row["evidence_state"] == "PRESENT" for row in audit["stage_audit"])
assert audit["technical_gate_audit"]["status"] == "READY"
assert audit["release_authorized"] is True
assert audit["block_reasons"] == []

print("Core1A SBA04 learner-state gap: PASS (explicit UNKNOWN prior-heuristic state; all-stage evidence and satisfied SBA05 dependency authorize release)")
