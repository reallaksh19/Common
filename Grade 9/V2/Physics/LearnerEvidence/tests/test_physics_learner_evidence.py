#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D=Path(__file__).resolve().parents[1]
PHYSICS=D.parent
sys.path[:0]=[str(D/"engine"),str(PHYSICS/"ProblemSemantics"/"engine"),str(PHYSICS/"AssessmentIntake"/"engine")]
from infer_physics_learner_evidence import build_snapshot, load, digest_without_field, reduce_normalized_records
from build_physics_problem_semantics import build_package
from build_physics_assessment_intake import digest_without_field as intake_digest_without_field

Q=load(PHYSICS/"AssessmentIntake/fixtures/motion-question-set.fixture.json")
S=load(PHYSICS/"AssessmentIntake/fixtures/motion-topic-scope.fixture.json")
R=load(PHYSICS/"AssessmentReview/registry/physics-item-validity-registry.json")
P=load(PHYSICS/"AssessmentReview/policies/diagnostic-use-policy.json")
C=load(PHYSICS/"Canonical/registry/capabilities.json")
A=load(PHYSICS/"AssessmentScope/authority/physics-assessment-scope-authority.json")
B=load(PHYSICS/"AssessmentScope/registry/motion-question-scope-bindings.json")
PD=PHYSICS/"ProblemSemantics"
ROLE=load(PD/"registry/physics-reasoning-role-registry.json")
FAM=load(PD/"registry/physics-problem-family-registry.json")
VER=load(PD/"registry/physics-verification-route-registry.json")
ITEM=load(PD/"registry/motion-item-semantics.json")
BADGE=load(PD/"registry/guide-demand-badge-policy.json")
PKG=build_package(Q,S,R,P,C,A,B,ROLE,FAM,VER,ITEM,BADGE)
REG=load(D/"registry/physics-observation-code-registry.json")
POL=load(D/"registry/physics-diagnostic-policy.json")
ATT=load(PHYSICS/"AssessmentIntake/fixtures/motion-attempt-set.fixture.json")
LED=load(D/"fixtures/physics-learner-evidence-ledger.fixture.json")

def by_item(ref):
    return next(x for x in PKG["items"] if x["item_ref"]==ref)

def route_step(item_ref, role):
    item=by_item(item_ref)
    return next(x for x in item["reasoning_route"]["steps"] if x["role"]==role)

def allowed_caps(item_ref):
    return {c for s in by_item(item_ref)["reasoning_route"]["steps"] for c in s["capability_refs"]}

def cap(snapshot, ref):
    return next(x for x in snapshot["capability_states"] if x["capability_ref"]==ref)

def case(snapshot, code):
    return next(x for x in snapshot["diagnostic_cases"] if x["hypothesis_code"]==code)

def disp(bundle, obs_ref):
    return next(x for x in bundle["processed_evidence"] if x["observation_ref"]==obs_ref)["disposition"]

def obs(oid, attempt_ref, item_ref, role, code, polarity, caps, confidence=0.99, rep=None):
    step=route_step(item_ref,role)
    return {
        "observation_id":oid,
        "attempt_ref":attempt_ref,
        "item_ref":item_ref,
        "route_step_ref":step["step_id"],
        "route_role":role,
        "representation_ref":rep,
        "observation_code":code,
        "polarity":polarity,
        "capability_refs":caps,
        "evidence_fragment":f"Synthetic acceptance evidence for {code}.",
        "observation_confidence":confidence,
        "extraction_confidence":confidence,
        "transcription_confidence":confidence,
    }

def redigest_ledger(ledger):
    ledger["ledger_digest"]=""
    ledger["ledger_digest"]=digest_without_field(ledger,"ledger_digest","observations","observation_id")
    return ledger

def redigest_attempts(attempts):
    attempts["attempt_set_digest"]=""
    attempts["attempt_set_digest"]=intake_digest_without_field(attempts,"attempt_set_digest")
    return attempts

def add_attempt(attempts, aid, qref, part=None, reps=None, confidence=0.99):
    attempts["attempts"].append({
        "attempt_id":aid,
        "binding_method":"EXPLICIT_ID",
        "extraction_confidence":confidence,
        "part_ref":part,
        "question_ref":qref,
        "representation_refs":reps or [],
        "response":{"final_answer":None,"raw_transcription":"synthetic diagnostic evidence","work_steps":[]},
        "source_locator":{"artifact_ref":"PUBLIC_SYNTHETIC_ATTEMPT_P_E","page":1,"region":aid},
    })
    return redigest_attempts(attempts)

# Branch A — AttemptSet absent.
no_attempt=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(REG),copy.deepcopy(POL))
ns=no_attempt["snapshot"]
assert ns["attempt_mode"]=="ABSENT"
assert ns["support_policy"]=="NEUTRAL_CONSERVATIVE"
assert ns["diagnostic_cases"]==[]
assert all(x["state"]=="UNKNOWN" and not x["negative_evidence_refs"] for x in ns["capability_states"])

# Branch B — supplied synthetic P-A AttemptSet + P-E ledger.
with_attempt=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(REG),copy.deepcopy(POL),copy.deepcopy(ATT),copy.deepcopy(LED))
ws=with_attempt["snapshot"]
assert ws["attempt_mode"]=="PRESENT" and ws["support_policy"]=="EVIDENCE_CONDITIONED"
assert ns["assessment_scope_ref"]==ws["assessment_scope_ref"]
assert ns["assessment_scope_digest"]==ws["assessment_scope_digest"]
assert ns["scope_unchanged"] is True and ws["scope_unchanged"] is True

# 1 CORRECT_MODEL_SELECTION + BAD_ARITHMETIC != MODEL_FAILURE
assert cap(ws,"PHY-CAP-UNIFORM-ACCELERATION")["state"]=="DEMONSTRATED"
assert "PHE-O01" in cap(ws,"PHY-CAP-UNIFORM-ACCELERATION")["positive_evidence_refs"]
assert disp(with_attempt,"PHE-O03")=="SHARED_EXECUTION_ERROR_LOCALIZED"
assert case(ws,"ARITHMETIC_EXECUTION_ERROR")["status"]=="HYPOTHESIS"

# 2 CORRECT_PROJECTILE_COMPONENTS + APEX_AMBIGUITY != PROJECTILE_FAILURE
projectile_records=[
    {"observation_ref":"PJ-POS","attempt_ref":"SYN-PJ-1","item_ref":"SYN-PJ","observation_code":"CORRECT_STATE_EXTRACTION",
     "capability_refs":["PHY-CAP-PROJECTILE-COMPONENTS"],"effective_confidence":0.99,"state_effect":"POSITIVE","probe_family":None,"disposition":"CREDITED"},
    {"observation_ref":"PJ-AMB","attempt_ref":"SYN-PJ-1","item_ref":"SYN-PJ","observation_code":"APEX_COMPONENT_AMBIGUITY",
     "capability_refs":["PHY-CAP-PROJECTILE-COMPONENTS"],"effective_confidence":0.96,"state_effect":"AMBIGUITY_ONLY","probe_family":"PHY-PROBE-APEX-COMPONENTS","disposition":"AMBIGUITY_PROBE_REQUIRED"},
]
pst,pcases,pprobes=reduce_normalized_records(["PHY-CAP-PROJECTILE-COMPONENTS"],projectile_records,POL)
assert pst[0]["state"]=="DEMONSTRATED" and pst[0]["negative_evidence_refs"]==[]
assert "PHY-PROBE-APEX-COMPONENTS" in pprobes
assert next(x for x in pcases if x["hypothesis_code"]=="APEX_COMPONENT_AMBIGUITY")["status"]=="PROBE_REQUIRED"

# 3 CORRECT_PHASE1_REASONING + INVALID_HANDOFF != PHASE1_FAILURE
assert "PHY-CAP-MULTIPHASE-KINEMATICS" in allowed_caps("Q10")
att=copy.deepcopy(ATT)
led=copy.deepcopy(LED)
led["observations"] += [
    obs("PHE-PHASE-POS","A10","Q10","SELECT_MODEL","CORRECT_MODEL_SELECTION","POSITIVE",["PHY-CAP-MULTIPHASE-KINEMATICS"]),
    obs("PHE-PHASE-NEG","A10","Q10","PROPAGATE_STATE","OMITTED_PHASE_HANDOFF","NEGATIVE",["PHY-CAP-MULTIPHASE-KINEMATICS"]),
]
redigest_ledger(led)
phase=build_snapshot(PKG,Q,REG,POL,att,led); ps=phase["snapshot"]
assert "PHE-PHASE-POS" in cap(ps,"PHY-CAP-MULTIPHASE-KINEMATICS")["positive_evidence_refs"]
# Q10 is positive-evidence-only upstream, so the handoff failure cannot punish the learner.
assert disp(phase,"PHE-PHASE-NEG")=="IGNORED_INVALID_ITEM"
assert cap(ps,"PHY-CAP-MULTIPHASE-KINEMATICS")["state"]!="EVIDENCE_OF_DIFFICULTY"

# 4 CORRECT_GRAPH_REGION_IDENTIFICATION + SIGN_SUM_ERROR != GRAPH_CONCEPT_FAILURE
assert "PHY-CAP-VT-SIGNED-AREA" in allowed_caps("Q8")
led=copy.deepcopy(LED)
led["observations"] += [
    obs("PHE-GRAPH-POS","A8","Q8","REPRESENT","CORRECT_REPRESENTATION_TRANSLATION","POSITIVE",["PHY-CAP-VT-SIGNED-AREA"],rep="FIG-Q8-VT"),
    obs("PHE-GRAPH-NEG","A8","Q8","CHOOSE_FRAME","SIGN_DIRECTION_MISMATCH","NEGATIVE",["PHY-CAP-VT-SIGNED-AREA"]),
]
redigest_ledger(led)
graph=build_snapshot(PKG,Q,REG,POL,ATT,led); gs=graph["snapshot"]
assert cap(gs,"PHY-CAP-VT-SIGNED-AREA")["state"]=="MIXED"
assert "PHE-GRAPH-POS" in cap(gs,"PHY-CAP-VT-SIGNED-AREA")["positive_evidence_refs"]
assert case(gs,"SIGN_DIRECTION_MISMATCH")["status"]=="PROBE_REQUIRED"

# 5 NO_ATTEMPT != PHYSICS_WEAK
assert all(x["state"]!="EVIDENCE_OF_DIFFICULTY" for x in ns["capability_states"])
assert "PHYSICS_WEAK" not in json.dumps(ns)

# 6 ONE_ERROR != CONFIRMED_MISCONCEPTION
att1=add_attempt(copy.deepcopy(ATT),"A1","Q1")
led1=copy.deepcopy(LED)
led1["attempt_set_ref"]=att1["attempt_set_id"]
led1["observations"].append(obs("PHE-DIST-1","A1","Q1","CHOOSE_RELATION","DISTANCE_DISPLACEMENT_CONFUSION","NEGATIVE",["PHY-CAP-DISTANCE-DISPLACEMENT"]))
redigest_ledger(led1)
one=build_snapshot(PKG,Q,REG,POL,att1,led1); os=one["snapshot"]
assert case(os,"DISTANCE_DISPLACEMENT_CONFUSION")["status"]=="PROBE_REQUIRED"

# 7 INVALID_ITEM_PUNISHES_LEARNER
led_bad=copy.deepcopy(LED)
led_bad["observations"].append(obs("PHE-BLOCKED","A14B","Q14.b","PROPAGATE_STATE","OMITTED_PHASE_HANDOFF","NEGATIVE",["PHY-CAP-MULTIPHASE-KINEMATICS"]))
redigest_ledger(led_bad)
blocked=build_snapshot(PKG,Q,REG,POL,ATT,led_bad)
assert disp(blocked,"PHE-BLOCKED")=="IGNORED_INVALID_ITEM"
assert "PHE-BLOCKED" not in cap(blocked["snapshot"],"PHY-CAP-MULTIPHASE-KINEMATICS")["negative_evidence_refs"]

# 8 LOW_CONFIDENCE_OBSERVATION_BECOMES_CONFIDENT_STATE
led_low=copy.deepcopy(LED)
led_low["observations"].append(obs("PHE-LOW","A3","Q3","CHECK_MODEL_VALIDITY","MODEL_VALIDITY_IGNORED","NEGATIVE",["PHY-CAP-UNIFORM-ACCELERATION"],confidence=0.60))
redigest_ledger(led_low)
low=build_snapshot(PKG,Q,REG,POL,ATT,led_low)
assert disp(low,"PHE-LOW")=="LOW_CONFIDENCE_PROBE_REQUIRED"
assert cap(low["snapshot"],"PHY-CAP-UNIFORM-ACCELERATION")["state"]=="DEMONSTRATED"
assert "PHE-LOW" not in cap(low["snapshot"],"PHY-CAP-UNIFORM-ACCELERATION")["negative_evidence_refs"]

# 9 SHARED_ARITHMETIC_FAILURE_ERASES_PHYSICS_REASONING
assert cap(ws,"PHY-CAP-UNIFORM-ACCELERATION")["state"]=="DEMONSTRATED"
assert not cap(ws,"PHY-CAP-UNIFORM-ACCELERATION")["negative_evidence_refs"]

# Confirmation requires two independent high-confidence negative observations.
att2=add_attempt(copy.deepcopy(att1),"A1B","Q1")
led2=copy.deepcopy(led1)
led2["attempt_set_ref"]=att2["attempt_set_id"]
led2["observations"].append(obs("PHE-DIST-2","A1B","Q1","CHOOSE_RELATION","DISTANCE_DISPLACEMENT_CONFUSION","NEGATIVE",["PHY-CAP-DISTANCE-DISPLACEMENT"]))
redigest_ledger(led2)
two=build_snapshot(PKG,Q,REG,POL,att2,led2)
assert case(two["snapshot"],"DISTANCE_DISPLACEMENT_CONFUSION")["status"]=="CONFIRMED"

# Deterministic replay.
again=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(REG),copy.deepcopy(POL),copy.deepcopy(ATT),copy.deepcopy(LED))
canonical=json.dumps(with_attempt,sort_keys=True,separators=(",",":"),ensure_ascii=False)
assert canonical==json.dumps(again,sort_keys=True,separators=(",",":"),ensure_ascii=False)

print("PHYSICS P-E required falsifiers = 9 PASS")
print("PHYSICS P-E no-attempt branch = UNKNOWN / no negative diagnosis PASS")
print("PHYSICS P-E attempt branch = localized evidence PASS")
print("PHYSICS P-E assessment scope invariant = PASS")
print("PHYSICS P-E two-evidence confirmation threshold = PASS")
print("PHYSICS P-E deterministic replay = PASS")
