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
CANDIDATE_RECEIPT = "topics/m2d-sba04-stage-evidence/1a5-representation-candidates.v1.json"
DECISION_RECEIPT = "topics/m2d-sba04-stage-evidence/1a6-representation-decision.v1.json"
DESIGN_STUDY = "topics/m2d-sba04-design/representation-design-study.v1.json"
SPEC = load_blueprint(SPEC_REF)


def stage_state(audit: dict, stage: str) -> str:
    return next(row for row in audit["stage_audit"] if row["stage"] == stage)["evidence_state"]


study = load_blueprint(DESIGN_STUDY)
assert len(study["candidates"]) == 3
assert study["decision"]["primary_candidate_id"] == "CAND-SBA04-STAGED-TRAJECTORY-FIRST"
assert study["decision"]["rejected_candidate_ids"] == ["CAND-SBA04-STATE-TABLE-FIRST"]

base_chain = [JUMP_RECEIPT, TRANSFORMATION_RECEIPT, REP_REQUIREMENTS_RECEIPT]
assert len(SPEC["stage_evidence_refs"]) == 9
assert set(base_chain + [CANDIDATE_RECEIPT, DECISION_RECEIPT]).issubset(SPEC["stage_evidence_refs"])

# Candidate comparison is independent evidence; it must not manufacture a selection decision.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = base_chain + [CANDIDATE_RECEIPT]
audit = compile_audit(probe, spec_ref=SPEC_REF)
assert stage_state(audit, "1A5_REPRESENTATION_CANDIDATES") == "PRESENT"
assert stage_state(audit, "1A6_REPRESENTATION_DECISIONS") == "MISSING"
assert audit["release_authorized"] is False

# The explicit decision receipt promotes 1A6 only after the candidate set is supplied.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = base_chain + [CANDIDATE_RECEIPT, DECISION_RECEIPT]
audit = compile_audit(probe, spec_ref=SPEC_REF)
assert stage_state(audit, "1A5_REPRESENTATION_CANDIDATES") == "PRESENT"
assert stage_state(audit, "1A6_REPRESENTATION_DECISIONS") == "PRESENT"
assert stage_state(audit, "1A7_PICTURE_WORD_SYMBOL_EQUATION_BRIDGE") == "PARTIAL"
assert stage_state(audit, "1A11_UNRESOLVED_JUMP_AUDIT") == "PARTIAL"
assert audit["release_authorized"] is False
assert DESIGN_STUDY in audit["source_refs"]
assert CANDIDATE_RECEIPT in audit["source_refs"]
assert DECISION_RECEIPT in audit["source_refs"]

print("Core1A SBA04 real representation design: PASS (candidate comparison and decision separated; PWSE/release remain closed in isolation)")
