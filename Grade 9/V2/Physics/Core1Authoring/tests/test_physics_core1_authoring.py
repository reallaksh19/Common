#!/usr/bin/env python3
import copy, importlib.util, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PHYS=ROOT.parent
sys.path[:0]=[
    str(ROOT/"engine"),
    str(PHYS/"StudySynthesis"/"engine"),
    str(PHYS/"LearnerEvidence"/"engine"),
    str(PHYS/"ProblemSemantics"/"engine"),
]
from author_physics_core1 import build_core1, validate_core1, load, digest
from study_scope import derive_study_scope
from study_treatment import build_model
from infer_physics_learner_evidence import build_snapshot
from build_physics_problem_semantics import build_package

Q=load(PHYS/"AssessmentIntake/fixtures/motion-question-set.fixture.json")
TOPIC=load(PHYS/"AssessmentIntake/fixtures/motion-topic-scope.fixture.json")
REVIEW=load(PHYS/"AssessmentReview/registry/physics-item-validity-registry.json")
REVIEW_POLICY=load(PHYS/"AssessmentReview/policies/diagnostic-use-policy.json")
CANON=load(PHYS/"Canonical/registry/capabilities.json")
AUTH=load(PHYS/"AssessmentScope/authority/physics-assessment-scope-authority.json")
BIND=load(PHYS/"AssessmentScope/registry/motion-question-scope-bindings.json")
PD=PHYS/"ProblemSemantics"
PKG=build_package(
    Q,TOPIC,REVIEW,REVIEW_POLICY,CANON,AUTH,BIND,
    load(PD/"registry/physics-reasoning-role-registry.json"),
    load(PD/"registry/physics-problem-family-registry.json"),
    load(PD/"registry/physics-verification-route-registry.json"),
    load(PD/"registry/motion-item-semantics.json"),
    load(PD/"registry/guide-demand-badge-policy.json"),
)
PE=PHYS/"LearnerEvidence"
PE_REG=load(PE/"registry/physics-observation-code-registry.json")
PE_POLICY=load(PE/"registry/physics-diagnostic-policy.json")
ATT=load(PHYS/"AssessmentIntake/fixtures/motion-attempt-set.fixture.json")
LED=load(PE/"fixtures/physics-learner-evidence-ledger.fixture.json")
PF_POLICY=load(PHYS/"StudySynthesis/policies/physics-treatment-policy.json")

scope=derive_study_scope(copy.deepcopy(BIND),copy.deepcopy(AUTH),copy.deepcopy(PKG))
no_bundle=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(PE_REG),copy.deepcopy(PE_POLICY))
att_bundle=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(PE_REG),copy.deepcopy(PE_POLICY),copy.deepcopy(ATT),copy.deepcopy(LED))
no_model=build_model(copy.deepcopy(scope),copy.deepcopy(no_bundle),copy.deepcopy(PF_POLICY))
att_model=build_model(copy.deepcopy(scope),copy.deepcopy(att_bundle),copy.deepcopy(PF_POLICY))

IK=PHYS/"InstructionalKnowledge"
spec=importlib.util.spec_from_file_location("physics_pck_candidates",IK/"registry/physics_pck_candidates.py")
pckmod=importlib.util.module_from_spec(spec); spec.loader.exec_module(pckmod)
CAND=pckmod.get_registry()
PROM=load(IK/"registry/physics-pck-promotion-registry.json")
AUTHOR=load(ROOT/"policies/physics-instructional-authoring-profile.json")
SCOPE_POLICY=load(ROOT/"policies/physics-core1-scope-completeness-policy.json")
PROBLEM=load(ROOT/"policies/physics-problem-authoring-profile.json")

pre=build_core1(copy.deepcopy(no_model),copy.deepcopy(CAND),copy.deepcopy(PROM),copy.deepcopy(AUTHOR),copy.deepcopy(SCOPE_POLICY),copy.deepcopy(PROBLEM),"PRE_REVIEW")
att_pre=build_core1(copy.deepcopy(att_model),copy.deepcopy(CAND),copy.deepcopy(PROM),copy.deepcopy(AUTHOR),copy.deepcopy(SCOPE_POLICY),copy.deepcopy(PROBLEM),"PRE_REVIEW")

assert pre["release_status"]=="PRE_REVIEW_ONLY"
assert pre["scope_complete"] is True and pre["original_assessment_unspoiled"] is True
assert {x["capability_ref"] for x in pre["lessons"]}=={x["capability_ref"] for x in no_model["capability_records"]}
assert len(pre["lessons"])==len(no_model["capability_records"])
assert all(x["treatment"]=="ACTIVE_STUDY" for x in no_model["capability_records"])
assert all(len(x["instructional_stages"])==len(AUTHOR["full_learning_stages"]) for x in pre["lessons"])

# Production is deliberately fail-closed until human SUBJECT+PEDAGOGY promotion exists.
try:
    build_core1(copy.deepcopy(no_model),copy.deepcopy(CAND),copy.deepcopy(PROM),copy.deepcopy(AUTHOR),copy.deepcopy(SCOPE_POLICY),copy.deepcopy(PROBLEM),"PRODUCTION")
    raise AssertionError("PCK_PROMOTION_REQUIRED not raised")
except ValueError as e:
    assert "PCK_PROMOTION_REQUIRED" in str(e)

def lesson(plan,cap):
    return next(x for x in plan["lessons"] if x["capability_ref"]==cap)

def redigest(plan):
    for le in plan["lessons"]:
        for pp in le["problem_authoring_plans"]:
            pp["plan_digest"]=digest(pp,"plan_digest")
        le["lesson_digest"]=digest(le,"lesson_digest")
    plan["plan_digest"]=digest(plan,"plan_digest")
    return plan

def assert_fails(code,plan,model):
    p=redigest(copy.deepcopy(plan))
    try:
        validate_core1(p,model,CAND,PROM,AUTHOR,SCOPE_POLICY,PROBLEM)
        raise AssertionError(code+" not rejected")
    except ValueError as e:
        assert code in str(e),(code,str(e))

# 1 CORE1_IS_ONLY_A_REPAIR_MEMO
bad=copy.deepcopy(pre); bad["lessons"]=bad["lessons"][:-1]
assert_fails("CORE1_IS_ONLY_A_REPAIR_MEMO",bad,no_model)

# 2 CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE
bad=copy.deepcopy(pre)
pp=next(x for x in bad["lessons"][0]["problem_authoring_plans"] if x["role"]=="WORKED")
pp["source_question_reuse"]=True; pp["source_question_refs"]=["Q1"]
assert_fails("CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE",bad,no_model)

# 3 PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY
bad=copy.deepcopy(pre); bad["generation_mode"]="PRODUCTION"; bad["release_status"]="PRODUCER_LEGAL"
assert_fails("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY",bad,no_model)

# 4 PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY
bad=copy.deepcopy(pre)
bad["lessons"][0]["problem_authoring_plans"][0]["problem_family_ref"]=""
assert_fails("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",bad,no_model)

# 5 FULL_LEARNING_TREATMENT_WITHOUT_PHYSICAL_RECONSTRUCTION
bad=copy.deepcopy(pre)
bad["lessons"][0]["instructional_stages"]=[s for s in bad["lessons"][0]["instructional_stages"] if s["stage"]!="RECONSTRUCT"]
assert_fails("FULL_LEARNING_TREATMENT_WITHOUT_PHYSICAL_RECONSTRUCTION",bad,no_model)

# 6 NAKED_EQUATION_COUNTS_AS_CONCEPT_TEACHING
eq_cap=next(x["capability_ref"] for x in pre["lessons"] if x["equation_contract"]["applies"])
bad=copy.deepcopy(pre); lesson(bad,eq_cap)["equation_contract"]["understand_origin"]=[]
assert_fails("NAKED_EQUATION_COUNTS_AS_CONCEPT_TEACHING",bad,no_model)

# 7 MODEL_VALIDITY_CONDITION_DROPPED
mv_cap=next(x["capability_ref"] for x in pre["lessons"] if any(o["required"] for o in x["model_validity_obligations"]))
bad=copy.deepcopy(pre); lesson(bad,mv_cap)["model_validity_obligations"]=[]
assert_fails("MODEL_VALIDITY_CONDITION_DROPPED",bad,no_model)

# 8 MULTIPHASE_TEACHING_WITHOUT_STATE_HANDOFF
hand_cap=next(x["capability_ref"] for x in pre["lessons"] if x["state_handoff"]["required"])
bad=copy.deepcopy(pre); lesson(bad,hand_cap)["state_handoff"]["visible_terminal_to_next_initial"]=False
assert_fails("MULTIPHASE_TEACHING_WITHOUT_STATE_HANDOFF",bad,no_model)

# 9 GRAPH_TEACHING_WITHOUT_HEIGHT_SLOPE_AREA_SEMANTICS
graph_cap=next(x["capability_ref"] for x in pre["lessons"] if x["graph_semantics"]["required"])
bad=copy.deepcopy(pre); lesson(bad,graph_cap)["graph_semantics"]["operations"]=["SLOPE"]
assert_fails("GRAPH_TEACHING_WITHOUT_HEIGHT_SLOPE_AREA_SEMANTICS",bad,no_model)

# 10 READY_CONTENT_PADDED_INTO_FULL_RETEACH
ready_cap=next(x["capability_ref"] for x in att_pre["lessons"] if x["treatment"]=="READY_VERIFY_ONLY")
bad=copy.deepcopy(att_pre); lesson(bad,ready_cap)["instructional_stages"].insert(1,{"stage":"PHENOMENON","payload":{"padding":True}})
assert_fails("READY_CONTENT_PADDED_INTO_FULL_RETEACH",bad,att_model)

# 11 PHYSICAL_CHECK_REDUCED_TO_NUMBER_ONLY
bad=copy.deepcopy(pre); bad["lessons"][0]["physical_verification"]["checks"]=["NUMBER_ONLY"]
assert_fails("PHYSICAL_CHECK_REDUCED_TO_NUMBER_ONLY",bad,no_model)

# Strong positive checks.
for le in pre["lessons"]:
    assert le["pck_asset_refs"], le["capability_ref"]
    assert [x["stage"] for x in le["instructional_stages"]]==AUTHOR["full_learning_stages"]
    for pp in le["problem_authoring_plans"]:
        assert pp["must_be_new_instance"] is True
        assert pp["source_question_reuse"] is False and pp["source_question_refs"]==[]
        assert pp["problem_family_ref"] in le["problem_family_refs"]
        assert len(pp["surface_changes"])>=2

ua=lesson(att_pre,"PHY-CAP-UNIFORM-ACCELERATION")
assert ua["treatment"]=="READY_VERIFY_ONLY"
assert [x["stage"] for x in ua["instructional_stages"]]==["ACTIVATE","VERIFY"]
assert ua["pck_asset_refs"]==[] and ua["problem_authoring_plans"]==[]

# Deterministic replay.
again=build_core1(copy.deepcopy(no_model),copy.deepcopy(CAND),copy.deepcopy(PROM),copy.deepcopy(AUTHOR),copy.deepcopy(SCOPE_POLICY),copy.deepcopy(PROBLEM),"PRE_REVIEW")
assert json.dumps(pre,sort_keys=True,separators=(",",":"))==json.dumps(again,sort_keys=True,separators=(",",":"))

print("PHYSICS P-G required falsifiers = 11 PASS")
print("PHYSICS P-G full-learning semantic sequence = PASS")
print("PHYSICS P-G original-assessment firewall = PASS")
print("PHYSICS P-G READY concise treatment = PASS")
print("PHYSICS P-G production human-promotion gate = FAIL-CLOSED PASS")
print("PHYSICS P-G deterministic replay = PASS")
