#!/usr/bin/env python3
import copy, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"engine"))
from build_math_exact_candidate import build_fixture_binding, bind_rendered_artifacts, seal
from evaluate_math_mature_gate import load, digest, evaluate, validate_candidate, validate_decision

POLICY=load(ROOT/"registry"/"math-mature-quality-policy.json")


def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError("expected "+code)


def receipt(candidate,dim,status="PASS",candidate_digest=None,artifact_digest=None):
    r={
      "receipt_id":f"TEST-REVIEW-{dim}","schema_version":"1.0.0","subject":"MATHEMATICS","review_dimension":dim,
      "candidate_digest":candidate_digest or candidate["binding_digest"],"artifact_set_digest":artifact_digest or candidate["artifact_set_digest"],
      "review_status":status,"review_mode":"TEST_ONLY","fixture_class":"TEST_ONLY_SYNTHETIC",
      "source_system":"MATH_ASSESSMENT_REVIEW_INTAKE" if dim=="ASSESSMENT" else "SHARED_HUMAN_REVIEW_INTAKE",
      "source_ref":f"test://human-review/{dim.lower()}","source_result_digest":digest(["source",dim,status]),
      "authorized":True,"release_evidence_eligible":False,"receipt_digest":"",
    }
    r["receipt_digest"]=digest(r,"receipt_digest"); return r


def machine(candidate,failed=None,claim="PASS"):
    return {"evidence_id":"TEST-MACHINE","candidate_digest":candidate["binding_digest"],"artifact_set_digest":candidate["artifact_set_digest"],
            "machine_falsifiers":claim,"publication_engineering":"PASS","exact_artifact_custody":"PASS","failed_falsifiers":failed or []}


def ai(candidate,status="PASS",majors=0):
    return {"pre_review_id":"TEST-AI-PRE-REVIEW","candidate_digest":candidate["binding_digest"],"artifact_set_digest":candidate["artifact_set_digest"],"status":status,"unresolved_major_count":majors}


def reference(candidate,status="PASS",raw_runtime=False):
    return {"validation_id":"TEST-REFERENCE-COMPARISON","candidate_digest":candidate["binding_digest"],"artifact_set_digest":candidate["artifact_set_digest"],"status":status,
            "mode":"TEST_ONLY","fixture_class":"TEST_ONLY_SYNTHETIC","reference_access_phase":"FINAL_COMPARATIVE_VALIDATION",
            "raw_reference_used_as_runtime_template":raw_runtime,"release_evidence_eligible":False}


def rendered_test_candidate():
    c=build_fixture_binding("A")
    # Positive-path gate logic is tested only with a synthetic rendered binding. It is never release evidence.
    c=copy.deepcopy(c)
    c["fixture_class"]="TEST_ONLY_SYNTHETIC"
    c["core1_authoring_status"]="PRODUCTION_PLAN_READY"
    c["materialization_state"]="SEMANTIC_READY_RENDER_NOT_BOUND"
    c["upstream_blockers"]=["M-L:RENDERED_EXACT_TWO_PRODUCT_NOT_BOUND"]
    c["artifacts"]=[]; c["artifact_set_digest"]=None
    c=seal(c)
    artifacts=[
      {"artifact_role":"CORE1_STUDY_GUIDE","media_type":"application/pdf","artifact_sha256":"1"*64,"manifest_digest":"a"*64},
      {"artifact_role":"CORE2_TRANSFER_BOOK","media_type":"application/pdf","artifact_sha256":"2"*64,"manifest_digest":"b"*64},
    ]
    return bind_rendered_artifacts(c,artifacts,fixture_class="TEST_ONLY_SYNTHETIC")


# Current real architecture state: exact semantic custody closes, but product release is blocked upstream.
current=build_fixture_binding("A")
validate_candidate(current)
blocked=evaluate(current,POLICY,gate_mode="REAL_RELEASE")
assert current["candidate_class"]=="SEMANTIC_COLD_START_EXACT_PACKAGE"
assert current["core1_authoring_status"] in {"BLOCKED_PCK_CANDIDATE_COVERAGE","BLOCKED_PCK_PROMOTION"}
assert current["artifact_set_digest"] is None
assert blocked["quality_states"]["PUBLICATION_ENGINEERING"]=="BLOCKED"
assert blocked["quality_states"]["SUBJECT_CORRECTNESS"]=="NOT_RUN"
assert blocked["quality_states"]["PEDAGOGICAL_DESIGN"]=="NOT_RUN"
assert blocked["quality_states"]["ASSESSMENT_DESIGN"]=="NOT_RUN"
assert blocked["quality_states"]["VISUAL_USABILITY"]=="NOT_RUN"
assert blocked["quality_states"]["MATURE_DESIGN_QUALITY"]=="BLOCKED"
assert blocked["quality_states"]["REFERENCE_COMPARABILITY"]=="NOT_RUN"
assert blocked["learning_effectiveness_validation"]=="NOT_RUN"
assert blocked["mature_product_class"]=="NOT_ELIGIBLE"
assert not blocked["release_evidence_eligible"]

# Positive-path state-machine proof is TEST_ONLY and can never become release evidence.
candidate=rendered_test_candidate()
reviews=[receipt(candidate,d) for d in ["SUBJECT","PEDAGOGY","ASSESSMENT","VISUAL"]]
full=evaluate(candidate,POLICY,machine(candidate),ai(candidate),reviews,reference(candidate),gate_mode="TEST_ONLY")
assert all(v=="PASS" for v in full["quality_states"].values())
assert full["mature_product_class"]=="TEST_ONLY_MATURE_GATE_LOGIC_PASS"
assert not full["release_evidence_eligible"]
assert full["learning_effectiveness_validation"]=="NOT_RUN"
assert full["reference_read_authorized"]

# MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS
bad=copy.deepcopy(full); bad["human_review_receipt_refs"]=[x for x in bad["human_review_receipt_refs"] if "PEDAGOGY" not in x]; bad["decision_digest"]=digest(bad,"decision_digest")
expect("MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS",lambda:validate_decision(bad,candidate,[r for r in reviews if r["review_dimension"]!="PEDAGOGY"],POLICY))

# HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT
bad_reviews=copy.deepcopy(reviews); bad_reviews[0]["candidate_digest"]="f"*64; bad_reviews[0]["receipt_digest"]=digest(bad_reviews[0],"receipt_digest")
expect("HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT",lambda:evaluate(candidate,POLICY,machine(candidate),ai(candidate),bad_reviews,None,gate_mode="TEST_ONLY"))

# SUBJECT_ERROR_SURVIVES_TO_MATURE_STATE: a subject FAIL must force mature-design FAIL / no mature class.
subject_fail=[receipt(candidate,d,"FAIL" if d=="SUBJECT" else "PASS") for d in ["SUBJECT","PEDAGOGY","ASSESSMENT","VISUAL"]]
result=evaluate(candidate,POLICY,machine(candidate),ai(candidate),subject_fail,None,gate_mode="TEST_ONLY")
assert result["quality_states"]["SUBJECT_CORRECTNESS"]=="FAIL"
assert result["quality_states"]["MATURE_DESIGN_QUALITY"]=="FAIL"
assert result["mature_product_class"]=="NOT_ELIGIBLE"

# CORE1_SUMMARY_LEVEL_BUT_MARKED_MATURE
bad_candidate=copy.deepcopy(candidate); bad_candidate["core1_authoring_status"]="BLOCKED_PCK_PROMOTION"; bad_candidate=seal(bad_candidate)
expect("CORE1_SUMMARY_LEVEL_BUT_MARKED_MATURE",lambda:validate_candidate(bad_candidate))

# HINTS_DUPLICATE_SOLUTION_BUT_MARKED_MATURE: any failed machine falsifier makes the candidate non-green.
expect("MACHINE_GREEN_WITH_FAILED_FALSIFIER",lambda:evaluate(candidate,POLICY,machine(candidate,["HINTS_DUPLICATE_SOLUTION"]),ai(candidate),reviews,None,gate_mode="TEST_ONLY"))

# VISUAL_UNUSABLE_AT_ACTUAL_OUTPUT_SIZE: authorized visual FAIL cannot yield mature state.
visual_fail=[receipt(candidate,d,"FAIL" if d=="VISUAL" else "PASS") for d in ["SUBJECT","PEDAGOGY","ASSESSMENT","VISUAL"]]
result=evaluate(candidate,POLICY,machine(candidate),ai(candidate),visual_fail,None,gate_mode="TEST_ONLY")
assert result["quality_states"]["VISUAL_USABILITY"]=="FAIL"
assert result["quality_states"]["MATURE_DESIGN_QUALITY"]=="FAIL"
assert result["mature_product_class"]=="NOT_ELIGIBLE"

# RAW_MATURE_REFERENCE_USED_AS_RUNTIME_TEMPLATE
expect("RAW_MATURE_REFERENCE_USED_AS_RUNTIME_TEMPLATE",lambda:evaluate(candidate,POLICY,machine(candidate),ai(candidate),reviews,reference(candidate,raw_runtime=True),gate_mode="TEST_ONLY"))

# LEARNING_EFFECTIVENESS_CLAIMED_WITHOUT_STUDY
bad_efficacy={"state":"VALIDATED","evidence_ref":None,"evidence_class":"NONE"}
expect("LEARNING_EFFECTIVENESS_CLAIMED_WITHOUT_STUDY",lambda:evaluate(current,POLICY,learning_effectiveness=bad_efficacy,gate_mode="REAL_RELEASE"))

# Frozen mature reference cannot be touched before the human gates are complete.
partial=[receipt(candidate,"SUBJECT"),receipt(candidate,"PEDAGOGY")]
expect("REFERENCE_READ_BEFORE_HUMAN_GATES",lambda:evaluate(candidate,POLICY,machine(candidate),ai(candidate),partial,reference(candidate),gate_mode="TEST_ONLY"))

# Test-only evidence is never accepted for real release.
expect("TEST_ONLY_REVIEW_USED_FOR_REAL_RELEASE",lambda:evaluate(candidate,POLICY,machine(candidate),ai(candidate),reviews,None,gate_mode="REAL_RELEASE"))

# Regeneration invalidates prior review evidence through exact digest binding.
changed=copy.deepcopy(candidate); changed["artifacts"][0]["artifact_sha256"]="3"*64; changed["artifact_set_digest"]=digest(changed["artifacts"]); changed=seal(changed)
expect("HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT",lambda:evaluate(changed,POLICY,machine(changed),ai(changed),reviews,None,gate_mode="TEST_ONLY"))

# Deterministic exact semantic binding from the same M-K run.
current2=build_fixture_binding("A")
assert current==current2
print("MATH M-L current semantic candidate remains correctly BLOCKED, not mature")
print("MATH M-L exact candidate/hash custody PASS")
print("MATH M-L machine vs human authority separation PASS")
print("MATH M-L subject/pedagogy/assessment/visual gate separation PASS")
print("MATH M-L final-reference ordering firewall PASS")
print("MATH M-L learning-effectiveness separation PASS")
print("MATH M-L test-only positive state-machine proof PASS")
