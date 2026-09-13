#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(path:Path): return json.loads(path.read_text(encoding="utf-8"))
def validate():
    schema_dir=ROOT/"contracts"; names=["architecture-blueprint.schema.json","packet-envelope.schema.json","evidence-state.schema.json","routing-decision.schema.json","independent-validation-session.schema.json","join-packet.schema.json","role-bindings.schema.json","learner-purpose-control-state.schema.json"]
    schemas={n:load(schema_dir/n) for n in names}
    for s in schemas.values(): Draft202012Validator.check_schema(s)
    Draft202012Validator(schemas["architecture-blueprint.schema.json"]).validate(load(ROOT/"policy"/"architecture.v1.json"))
    bindings=load(ROOT/"policy"/"role-bindings.v1.json"); Draft202012Validator(schemas["role-bindings.schema.json"]).validate(bindings)
    ev=Draft202012Validator(schemas["evidence-state.schema.json"])
    for f in sorted((ROOT/"fixtures"/"golden").glob("*.json")): ev.validate(load(f)["evidence"])
    a=load(ROOT/"policy"/"architecture.v1.json")
    if a["role_lifecycle"]["CORE2A"]!="ACTIVE": raise AssertionError("CORE2A_MUST_BE_ACTIVE_AFTER_SEMANTIC_CONTRACT")
    if not a["invariants"]["core2a_requires_taught_state_receipts"]: raise AssertionError("CORE2A_TAUGHT_STATE_GATE_DISABLED")
    if not a["invariants"]["core2a_may_not_infer_learner_mastery"]: raise AssertionError("CORE2A_MASTERY_INFERENCE_GUARD_DISABLED")
    if a["invariants"]["max_subtopics_per_handoff"]!=3: raise AssertionError("HANDOFF_BOUND_DRIFT")
    if not a["invariants"]["learning_atoms_unbounded"]: raise AssertionError("TRANSPORT_BOUND_LEAKED_INTO_PEDAGOGY")
    if bindings["canonical_root"]!="Grade 9/V2/Physics/Blueprint": raise AssertionError("PHYSICS_BLUEPRINT_ROOT_DRIFT")
    if bindings["roles"]["JOIN"]["ownership"]!="BLUEPRINT_NATIVE": raise AssertionError("JOIN_MUST_BE_BLUEPRINT_NATIVE")
    independent=load(ROOT/"policy"/"independent-validation.v1.json")
    if not independent["self_validation_forbidden"] or not independent["fresh_validator_instance_required"]: raise AssertionError("INDEPENDENT_VALIDATION_POLICY_DISABLED")
    join=load(ROOT/"policy"/"join-policy.v1.json")
    if join["coverage_rule"]!="EVERY_CORE2_DEMAND_CLAIM_EXACTLY_ONCE" or not join["critical_conflict_blocks_core1a"]: raise AssertionError("JOIN_POLICY_DRIFT")
    purpose=load(ROOT/"policy"/"purpose-contracts.v1.json")
    if purpose["invariant"]!="PURPOSE_CANNOT_BYPASS_REQUIRED_PREREQUISITES": raise AssertionError("PURPOSE_PREREQUISITE_INVARIANT_MISSING")
    if set(purpose["purposes"])!={"FIRST_STUDY","PRACTICE","REVISION","COMPETITIVE_EXAM"}: raise AssertionError("PURPOSE_VOCABULARY_DRIFT")
    print("Blueprint contracts: PASS")
if __name__=="__main__":validate()
