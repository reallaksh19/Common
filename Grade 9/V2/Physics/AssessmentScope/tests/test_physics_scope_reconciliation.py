#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
PHYSICS = D.parent
sys.path.insert(0, str(D / "engine"))
from reconcile_physics_assessment_scope import reconcile, digest_without_field  # noqa: E402

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def redigest(x, field):
    x[field] = ""
    x[field] = digest_without_field(x, field)

def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        if str(e).split(":",1)[0] != code:
            raise AssertionError(f"expected {code}, got {e}") from e
        return
    raise AssertionError(f"expected {code}")

Q = load(PHYSICS / "AssessmentIntake" / "fixtures" / "motion-question-set.fixture.json")
S = load(PHYSICS / "AssessmentIntake" / "fixtures" / "motion-topic-scope.fixture.json")
R = load(PHYSICS / "AssessmentReview" / "registry" / "physics-item-validity-registry.json")
P = load(PHYSICS / "AssessmentReview" / "policies" / "diagnostic-use-policy.json")
C = load(PHYSICS / "Canonical" / "registry" / "capabilities.json")
A = load(D / "authority" / "physics-assessment-scope-authority.json")
B = load(D / "registry" / "motion-question-scope-bindings.json")

def run(bindings=B, authority=A): return reconcile(Q,S,R,P,C,authority,bindings)
def row(b, ref): return next(x for x in b["bindings"] if x["item_ref"] == ref)

model, coverage, report, prereq = run()
assert len(coverage["rows"]) == 17 and coverage["coverage_complete"]
by = {x["item_ref"]: x for x in coverage["rows"]}
assert by["Q9"]["mapping_state"] == "PARTIAL_SCOPE_MATCH"
assert by["Q10"]["mapping_state"] == "PARTIAL_SCOPE_MATCH"
assert by["Q13"]["resolution_status"] == "BLOCKED"
assert "REPRESENTATION" in by["Q13"]["unresolved_requirements"]
assert by["Q14"]["source_integrity_state"] == "TYPOGRAPHIC_OR_OCR_AMBIGUITY"
assert by["Q14"]["validity_state"] == "REVIEW_REQUIRED"
assert by["Q14"]["resolution_status"] == "BLOCKED"
assert model["attempt_data_consumed"] is False and report["attempt_data_consumed"] is False
assert any(f["code"] == "REPRESENTATION_DEPENDENCY_UNRESOLVED" and f["item_ref"] == "Q13" for f in report["findings"])

b=copy.deepcopy(B); b["bindings"]=[x for x in b["bindings"] if x["item_ref"]!="Q2"]; redigest(b,"binding_registry_digest")
expect("QUESTION_DROPPED_DURING_SCOPE_DERIVATION",lambda:run(b))

b=copy.deepcopy(B); row(b,"Q1")["mapping_state"]="MAGIC"; redigest(b,"binding_registry_digest")
expect("QUESTION_WITHOUT_EXPLICIT_MAPPING_STATE",lambda:run(b))

b=copy.deepcopy(B); row(b,"Q1")["declared_topic_refs"].append("PHY-NOT-DECLARED"); redigest(b,"binding_registry_digest")
expect("QUESTION_EVIDENCE_SILENTLY_EXPANDS_DECLARED_BOUNDARY",lambda:run(b))

b=copy.deepcopy(B); q1=row(b,"Q1"); q1["canonical_concept_refs"]=["PHY-PROJECTILE-COMPONENTS"]; q1["canonical_capability_refs"]=["PHY-CAP-PROJECTILE-COMPONENTS"]; q1["prerequisite_capability_refs"]=["PHY-CAP-FRAME-SIGN-SETUP","PHY-CAP-REPRESENTATION-TRANSLATE"]; q1["physical_model_refs"]=["PHY-MODEL-PROJECTILE-IDEAL"]; q1["law_refs"]=["PHY-LAW-COMPONENT-INDEPENDENCE"]; q1["model_validity_conditions"]=["air resistance neglected","constant gravitational field"]; q1["problem_family_refs"]=["PHY-PF-PROJECTILE-COMPONENTS"]; q1["reference_frame"]={"required":True,"frame_text":"ground frame"}; q1["sign_convention"]={"positive_direction":"right/up as defined","status":"EXPLICIT"}; q1["state_variable_refs"]=["POSITION","VELOCITY","ACCELERATION","TIME"]; q1["representation_demands"]=["COMPONENT_VECTOR_VIEW"]; q1["verification_obligations"]=["VERIFY_COMPONENT_CONSISTENCY"]; q1["reasoning_role_expectations"]=["INTERPRET","REPRESENT","MODEL","VERIFY"]; redigest(b,"binding_registry_digest")
expect("TOPIC_LIST_SILENTLY_OVERRIDES_QUESTION_EVIDENCE",lambda:run(b))

b=copy.deepcopy(B); row(b,"Q7")["prerequisite_capability_refs"]=[]; redigest(b,"binding_registry_digest")
expect("PREREQUISITE_INFERRED_BUT_NOT_RECORDED",lambda:run(b))

b=copy.deepcopy(B); row(b,"Q6")["model_validity_conditions"]=[]; redigest(b,"binding_registry_digest")
expect("MODEL_VALIDITY_INFERRED_BUT_NOT_RECORDED",lambda:run(b))

b=copy.deepcopy(B); row(b,"Q6")["reference_frame"]["frame_text"]=""; redigest(b,"binding_registry_digest")
expect("REFERENCE_FRAME_REQUIRED_BUT_UNBOUND",lambda:run(b))

b=copy.deepcopy(B); row(b,"Q8")["source_representation_refs"]=[]; redigest(b,"binding_registry_digest")
expect("REPRESENTATION_DEPENDENCY_DROPPED",lambda:run(b))

b=copy.deepcopy(B); r=row(b,"Q10"); r["phase_structure"]={"kind":"SINGLE_PHASE","phases":["phase"],"boundary_state_variables":[],"justification":""}; redigest(b,"binding_registry_digest")
expect("MULTIPHASE_ITEM_MAPPED_AS_SINGLE_PHASE_WITHOUT_JUSTIFICATION",lambda:run(b))

b=copy.deepcopy(B); b["learner_state"]="WEAK"; redigest(b,"binding_registry_digest")
expect("SCOPE_RESOLUTION_CONSUMES_LEARNER_DATA",lambda:run(b))

m2,c2,r2,p2=run()
assert (model,coverage,report,prereq)==(m2,c2,r2,p2)
print("PHYSICS P-C scope-reconciliation falsifiers = 10 PASS + deterministic replay PASS")
