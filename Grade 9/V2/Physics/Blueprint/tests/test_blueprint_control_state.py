#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from copy import deepcopy
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"engine")); from resolve_control_state import resolve_control_state

def fixture(): return json.loads((ROOT/"fixtures"/"control-state"/"m2d-p20-first-study.json").read_text(encoding="utf-8"))
def policy(): return json.loads((ROOT/"policy"/"purpose-contracts.v1.json").read_text(encoding="utf-8"))
def assert_fails(spec,code):
    try: resolve_control_state(spec,policy())
    except AssertionError as exc: assert str(exc).startswith(code),str(exc)
    else: raise AssertionError("EXPECTED_FAILURE:"+code)
def by_ref(out): return {r["capability_ref"]:r for r in out["capability_states"]}
def test_p20_prior_resolves_capabilities():
    s=by_ref(resolve_control_state(fixture(),policy())); assert s["PHY-CAP-VECTOR-MEANING"]["state"]=="PARTIAL"; assert s["PHY-CAP-SIGN-CONVENTION"]["state"]=="FRAGILE"; assert s["PHY-CAP-PROJECTILE-COMPONENTS"]["state"]=="UNKNOWN"
def test_real_learner_evidence_overrides_prior_heuristic():
    r=by_ref(resolve_control_state(fixture(),policy()))["PHY-CAP-LINEAR-EQUATION"]; assert r["state"]=="SECURE" and r["basis"]=="DIAGNOSTIC"
def test_teaching_receipt_cannot_be_used_as_learner_state_evidence():
    s=fixture(); s["learner_evidence"][0]["evidence_kind"]="TEACHING_RECEIPT"; assert_fails(s,"TEACHING_RECEIPT_CANNOT_PROVE_LEARNER_STATE")
def test_purpose_is_explicit_and_governed():
    s=fixture(); s["purpose"]=None; assert_fails(s,"PURPOSE_UNRESOLVED_OR_INVALID")
def test_purpose_cannot_bypass_prerequisites():
    s=fixture(); s["purpose"]="COMPETITIVE_EXAM"; o=resolve_control_state(s,policy()); assert o["purpose_contract"]["purpose_cannot_bypass_required_prerequisites"] is True and "HIDDEN_CONSTRAINTS" in o["purpose_contract"]["priorities"]
def test_invalid_prior_fails():
    s=fixture(); s["learner_prior_pct"]=30; assert_fails(s,"LEARNER_PRIOR_MUST_BE_20_50_OR_80")
def test_unknown_evidence_capability_fails():
    s=fixture(); s["learner_evidence"][0]["capability_ref"]="PHY-CAP-NOT-IN-MODEL"; assert_fails(s,"LEARNER_EVIDENCE_UNKNOWN_CAPABILITY")
def test_evidence_requires_provenance():
    s=fixture(); s["learner_evidence"][0]["evidence_refs"]=[]; assert_fails(s,"LEARNER_EVIDENCE_REF_REQUIRED")
def test_duplicate_capability_prior_fails():
    s=fixture(); s["capability_prior_model"].append(deepcopy(s["capability_prior_model"][0])); assert_fails(s,"CAPABILITY_PRIOR_DUPLICATE")
def test_output_schema_and_mastery_guard():
    o=resolve_control_state(fixture(),policy()); schema=json.loads((ROOT/"contracts"/"learner-purpose-control-state.schema.json").read_text(encoding="utf-8")); Draft202012Validator(schema).validate(o); assert o["publication_teaching_receipts_used_as_learner_evidence"] is False
def test_digest_deterministic_under_input_order():
    a=fixture(); b=fixture(); b["capability_prior_model"]=list(reversed(b["capability_prior_model"])); assert resolve_control_state(a,policy())["control_digest"]==resolve_control_state(b,policy())["control_digest"]
def main():
    tests=[v for k,v in globals().items() if k.startswith("test_") and callable(v)]
    for t in tests:t()
    print(f"Blueprint control-state tests: PASS ({len(tests)} tests)")
if __name__=="__main__":main()
