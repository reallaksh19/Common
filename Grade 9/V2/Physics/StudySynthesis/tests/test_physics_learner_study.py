#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PHYS=ROOT.parent
sys.path[:0]=[
    str(ROOT/"engine"),
    str(PHYS/"LearnerEvidence"/"engine"),
    str(PHYS/"ProblemSemantics"/"engine"),
]
from build_physics_learner_study_model import derive_study_scope, build_model, validate_model, load, digest
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
POLICY=load(ROOT/"policies/physics-treatment-policy.json")

scope=derive_study_scope(copy.deepcopy(BIND),copy.deepcopy(AUTH),copy.deepcopy(PKG))
scope2=derive_study_scope(copy.deepcopy(BIND),copy.deepcopy(AUTH),copy.deepcopy(PKG))
assert scope["study_scope_digest"]==scope2["study_scope_digest"]

no_bundle=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(PE_REG),copy.deepcopy(PE_POLICY))
attempt_bundle=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(PE_REG),copy.deepcopy(PE_POLICY),copy.deepcopy(ATT),copy.deepcopy(LED))
assert no_bundle["snapshot"]["assessment_scope_digest"]==attempt_bundle["snapshot"]["assessment_scope_digest"]==scope["learner_evidence_scope_digest"]

no_model=build_model(copy.deepcopy(scope),copy.deepcopy(no_bundle),copy.deepcopy(POLICY))
attempt_model=build_model(copy.deepcopy(scope),copy.deepcopy(attempt_bundle),copy.deepcopy(POLICY))

def rec(model,cap):
    return next(x for x in model["capability_records"] if x["capability_ref"]==cap)
def lng(model,cap):
    return next(x for x in model["longitudinal_initializations"] if x["capability_ref"]==cap)
def assert_fails(code, model):
    bad=copy.deepcopy(model)
    bad["study_model_digest"]=digest(bad,"study_model_digest")
    try:
        validate_model(bad,scope,POLICY)
        raise AssertionError(code+" not rejected")
    except ValueError as e:
        assert code in str(e), (code,str(e))

# Governing invariant: learner state never changes required scope.
assert no_model["study_scope_digest"]==attempt_model["study_scope_digest"]==scope["study_scope_digest"]
assert {x["capability_ref"] for x in no_model["capability_records"]}=={x["capability_ref"] for x in attempt_model["capability_records"]}==set(scope["direct_assessed_capability_refs"])|set(scope["prerequisite_support_capability_refs"])
assert set(scope["required_item_refs"])=={b["item_ref"] for b in BIND["bindings"]}

# Attempt-absent UNKNOWN is complete neutral teaching, not repair.
assert no_model["learner_attempt_mode"]=="ABSENT"
assert all(x["learner_state"]=="UNKNOWN" for x in no_model["capability_records"])
assert all(x["treatment"]=="ACTIVE_STUDY" for x in no_model["capability_records"])

# Real P-E positive evidence legitimately changes treatment without changing scope.
ua=rec(attempt_model,"PHY-CAP-UNIFORM-ACCELERATION")
assert ua["learner_state"]=="DEMONSTRATED"
assert ua["treatment"]=="READY_VERIFY_ONLY"
assert not (set(ua["required_pck_jobs"]) & set(POLICY["ready_forbidden_full_reteach_jobs"]))
assert rec(no_model,"PHY-CAP-UNIFORM-ACCELERATION")["treatment"]=="ACTIVE_STUDY"

# Frame/sign and model-validity obligations survive even for READY/other treatments.
frame=next(x for x in scope["capability_scope_records"] if x["capability_ref"]=="PHY-CAP-FRAME-SIGN-SETUP")
assert any(x["reference_frame"]["required"] or x["sign_convention"]["required"] for x in frame["system_frame_obligations"])
assert any(x["required"] for x in next(x for x in scope["capability_scope_records"] if x["capability_ref"]=="PHY-CAP-UNIFORM-ACCELERATION")["model_validity_obligations"])
assert POLICY["mandatory_jobs"]["model_validity"] in ua["required_pck_jobs"]

# Future evidence stays open after current success.
assert lng(attempt_model,"PHY-CAP-UNIFORM-ACCELERATION")["dimensions"]["delayed_retention"]=="OPEN"
assert lng(attempt_model,"PHY-CAP-UNIFORM-ACCELERATION")["dimensions"]["far_transfer"]=="OPEN"

# Synthetic accepted-shape learner state: prerequisite difficulty -> REPAIR_BEFORE.
difficulty=copy.deepcopy(attempt_bundle)
snap=difficulty["snapshot"]
state_by={x["capability_ref"]:x for x in snap["capability_states"]}
frame_state=state_by.get("PHY-CAP-FRAME-SIGN-SETUP")
if frame_state is None:
    frame_state={"capability_ref":"PHY-CAP-FRAME-SIGN-SETUP","state":"EVIDENCE_OF_DIFFICULTY","confidence":0.97,"positive_evidence_refs":[],"negative_evidence_refs":["SYN-FRAME-NEG"]}
    snap["capability_states"].append(frame_state)
else:
    frame_state.update({"state":"EVIDENCE_OF_DIFFICULTY","confidence":0.97,"positive_evidence_refs":[],"negative_evidence_refs":["SYN-FRAME-NEG"]})
repair=build_model(scope,difficulty,POLICY)
assert rec(repair,"PHY-CAP-FRAME-SIGN-SETUP")["treatment"]=="REPAIR_BEFORE"
# A demonstrated downstream strength stays READY; it is not relabelled weak to justify the repair.
assert rec(repair,"PHY-CAP-UNIFORM-ACCELERATION")["treatment"]=="READY_VERIFY_ONLY"

# Mixed/unresolved evidence -> PROBE_FIRST and keeps the exact probe requirement.
probe_bundle=copy.deepcopy(attempt_bundle)
ps=probe_bundle["snapshot"]
state_by={x["capability_ref"]:x for x in ps["capability_states"]}
target="PHY-CAP-VT-SIGNED-AREA"
if target not in state_by:
    ps["capability_states"].append({"capability_ref":target,"state":"MIXED","confidence":0.95,"positive_evidence_refs":["SYN-GRAPH-POS"],"negative_evidence_refs":["SYN-GRAPH-NEG"]})
else:
    state_by[target].update({"state":"MIXED","confidence":0.95,"positive_evidence_refs":["SYN-GRAPH-POS"],"negative_evidence_refs":["SYN-GRAPH-NEG"]})
ps["diagnostic_cases"].append({
    "case_id":"SYN-PF-GRAPH-CASE","subject":"PHYSICS","hypothesis_code":"GRAPH_HEIGHT_SLOPE_AREA_CONFUSION",
    "capability_refs":[target],"evidence_refs":["SYN-GRAPH-NEG"],"status":"PROBE_REQUIRED","confidence":0.95,
    "probe_requirement":"PROBE_GRAPH_HEIGHT_SLOPE_AREA","rationale":"Synthetic P-F treatment-routing proof."
})
probe_model=build_model(scope,probe_bundle,POLICY)
pr=rec(probe_model,target)
assert pr["treatment"]=="PROBE_FIRST" and pr["probe_requirements"]==["PROBE_GRAPH_HEIGHT_SLOPE_AREA"]

# Release-blocking falsifiers.
bad=copy.deepcopy(attempt_model)
bad["capability_records"]=bad["capability_records"][:-1]
bad["longitudinal_initializations"]=bad["longitudinal_initializations"][:-1]
assert_fails("LEARNER_WEAKNESS_SHRINKS_ASSESSMENT_SCOPE",bad)

bad=copy.deepcopy(attempt_model)
r=rec(bad,"PHY-CAP-UNIFORM-ACCELERATION")
r["required_pck_jobs"].append("WORKED_REASONING_SEQUENCE")
assert_fails("READY_CAPABILITY_FULLY_RETAUGHT_FOR_PAGE_DENSITY",bad)

bad=copy.deepcopy(no_model)
r=next(x for x in bad["capability_records"] if x["learner_state"]=="UNKNOWN")
r["treatment"]="REPAIR_IN_UNIT"; r["priority"]="EMBEDDED_REPAIR"
assert_fails("NO_ATTEMPT_FORCES_REPAIR",bad)

bad=copy.deepcopy(attempt_model)
lng(bad,"PHY-CAP-UNIFORM-ACCELERATION")["dimensions"]["delayed_retention"]="CURRENT_EVIDENCE"
assert_fails("ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL",bad)

bad=copy.deepcopy(attempt_model)
rec(bad,"PHY-CAP-UNIFORM-ACCELERATION")["source_scope_trace_item_refs"]=[]
assert_fails("STUDYMODEL_WITHOUT_SOURCE_SCOPE_TRACE",bad)

bad=copy.deepcopy(attempt_model)
rec(bad,"PHY-CAP-UNIFORM-ACCELERATION")["model_validity_obligations"]=[]
assert_fails("MODEL_VALIDITY_DROPPED_FROM_STUDYMODEL",bad)

bad=copy.deepcopy(attempt_model)
rec(bad,"PHY-CAP-FRAME-SIGN-SETUP")["system_frame_obligations"]=[]
assert_fails("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_STUDYMODEL",bad)

bad=copy.deepcopy(attempt_model)
r=rec(bad,"PHY-CAP-UNIFORM-ACCELERATION")
r["treatment"]="ACTIVE_STUDY"; r["priority"]="CORE_STUDY"
assert_fails("UPSTREAM_PHYSICS_STRENGTH_RELABELLED_WEAK_TO_SUPPORT_REPAIR",bad)

# Deterministic replay.
again_scope=derive_study_scope(copy.deepcopy(BIND),copy.deepcopy(AUTH),copy.deepcopy(PKG))
again_model=build_model(again_scope,copy.deepcopy(attempt_bundle),copy.deepcopy(POLICY))
assert json.dumps(scope,sort_keys=True,separators=(",",":"))==json.dumps(again_scope,sort_keys=True,separators=(",",":"))
assert json.dumps(attempt_model,sort_keys=True,separators=(",",":"))==json.dumps(again_model,sort_keys=True,separators=(",",":"))

print("PHYSICS P-F required falsifiers = 8 PASS")
print("PHYSICS P-F assessment-scope invariant = PASS")
print("PHYSICS P-F no-attempt neutral teaching = PASS")
print("PHYSICS P-F evidence-conditioned treatment = PASS")
print("PHYSICS P-F longitudinal initialization = PASS")
print("PHYSICS P-F deterministic replay = PASS")
