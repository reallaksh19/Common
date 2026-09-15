#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D=Path(__file__).resolve().parents[1]
MATH=D.parent
REPO=MATH.parents[2]
sys.path.insert(0,str(D/"engine"))
sys.path.insert(0,str(D/"contracts"))
from math_cold_start_runner import run_cold_start, compare_runs, digest, load
from validate_contracts import validate_manifest, validate_report, validate_comparison


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e))
        return
    raise AssertionError("expected "+code)


def redigest_report(report):
    report["report_digest"]=""
    report["report_digest"]=digest(report,"report_digest")
    return report


def redigest_comp(comp):
    comp["comparison_digest"]=""
    comp["comparison_digest"]=digest(comp,"comparison_digest")
    return comp


A=MATH/"AssessmentIntake"/"fixtures"
questions=load(A/"mixed-grade9-question-set.fixture.json")
topic=load(A/"mixed-grade9-topic-scope.fixture.json")
attempts=load(A/"mixed-grade9-attempt-set.fixture.json")
manifest=load(MATH/"GENERATION_AUTHORITY_MANIFEST.json")
validate_manifest(manifest)

run_a,ia=run_cold_start(copy.deepcopy(questions),copy.deepcopy(topic),repo_root=REPO,run_id="MATH-M-K-RUN-A")
run_b,ib=run_cold_start(copy.deepcopy(questions),copy.deepcopy(topic),copy.deepcopy(attempts),repo_root=REPO,run_id="MATH-M-K-RUN-B",fixture_observation_oracle=True)
validate_report(run_a,manifest,ia)
validate_report(run_b,manifest,ib)
comparison=compare_runs(run_a,run_b)
validate_comparison(comparison,run_a,run_b)

# Exact external front door and complete downstream custody.
assert run_a["runtime_input_contract"]["question_set_ref"]==questions["question_set_id"]
assert run_a["runtime_input_contract"]["declared_topic_scope_ref"]==topic["declared_topic_scope_id"]
assert run_a["runtime_input_contract"]["attempt_set_ref"] is None
assert run_b["runtime_input_contract"]["attempt_set_ref"]==attempts["attempt_set_id"]
assert run_a["core2"]["question_count"]==14 and run_b["core2"]["question_count"]==14
assert run_a["coverage_closure"]["assessment_row_count"]==17
assert run_a["coverage_closure"]["semantic_gap_count"]==0
assert run_b["coverage_closure"]["semantic_gap_count"]==0
assert run_a["core1_authoring"]["scope_complete"] and run_b["core1_authoring"]["scope_complete"]

# No-attempt run must remain UNKNOWN and assessment-complete rather than inventing weakness.
sa={x["capability_ref"]:x for x in ia["learner_intelligence"]["learner_state_snapshot"]["capability_states"]}
assert sa and all(x["readiness"]=="UNKNOWN" for x in sa.values())
assert all(x["treatment"]=="ACTIVE_STUDY" for x in ia["study_model"]["capability_plans"])
assert ia["learner_intelligence"]["observations"]==[]
assert ia["learner_intelligence"]["learner_state_snapshot"]["diagnostic_cases"]==[]

# Attempt-present run preserves upstream mathematical success and localizes later execution failure.
sb={x["capability_ref"]:x for x in ib["learner_intelligence"]["learner_state_snapshot"]["capability_states"]}
assert sb["MATH-GEOMETRIC-MODELLING"]["readiness"]=="READY"
assert sb["MATH-EQUIDISTANCE-COORDINATE-MODEL"]["readiness"]=="READY"
assert sb["MATH-BINOMIAL-SQUARE-EXPANSION"]["readiness"]=="DEVELOPING"
assert sb["MATH-RIVER-CURRENT-MODEL"]["readiness"]=="READY"
assert sb["MATH-ARITHMETIC-DIVISION"]["readiness"]=="DEVELOPING"
assert sb["MATH-LINEAR-PARAMETER-CONDITION"]["readiness"]=="READY"  # Q9 gives positive evidence only.
assert sb["MATH-SLOPE-COMPUTATION"]["readiness"]=="UNKNOWN"  # Q7 copy error does not become a slope diagnosis.

pb={x["capability_ref"]:x for x in ib["study_model"]["capability_plans"]}
assert pb["MATH-GEOMETRIC-MODELLING"]["treatment"]=="VERIFY_ONLY"
assert pb["MATH-RIVER-CURRENT-MODEL"]["treatment"]=="VERIFY_ONLY"
assert pb["MATH-BINOMIAL-SQUARE-EXPANSION"]["treatment"] in {"REPAIR_BEFORE","REPAIR_IN_UNIT"}
assert pb["MATH-ARITHMETIC-DIVISION"]["treatment"] in {"REPAIR_BEFORE","REPAIR_IN_UNIT"}

# M-G promotion has run for real, so Core1 materializes. It rests on AI-assisted
# reference review only, so the run is PROVISIONAL and never release-legal.
# M-K may expose the materialized candidate but may not fabricate human PCK promotion.
for run in (run_a,run_b):
    c1=run["core1_authoring"]
    assert c1["status"]=="PROVISIONAL_PLAN_READY", c1["status"]
    assert c1["production_plan_ref"] is not None
    assert c1["missing_pck_candidate_capability_refs"]==[]
    assert c1["unpromoted_pck_capability_refs"]==[]
    assert c1["provisional_only_pck_capability_refs"]
    assert c1["pck_expert_review_state"]=="PENDING"
    assert c1["release_legal"] is False
    assert run["release_status"]=="PROVISIONAL_PENDING_PCK_EXPERT_REVIEW"
    assert "M-G/#242:PCK_EXPERT_REVIEW_PENDING" in run["blockers"]
    assert run["core2"]["publication_ready"] is True
    assert run["core2"]["core1_linkage_mode"]=="MATERIALIZED_PROVISIONAL"

# Run A/B invariants and intended learner-conditioned differences.
assert all(comparison["invariants"].values())
assert all(comparison["expected_differences"].values())

# Attempt mode cannot silently skip the governed semantic-review stage.
expect("ATTEMPT_SEMANTIC_REVIEW_STAGE_REQUIRED",lambda:run_cold_start(copy.deepcopy(questions),copy.deepcopy(topic),copy.deepcopy(attempts),repo_root=REPO,run_id="MATH-M-K-RUN-NO-REVIEW"))

# 1 COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY
bad=copy.deepcopy(run_a); bad["runtime_dependency_audit"]["chat_or_issue_history_used"]=True; redigest_report(bad)
expect("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY",lambda:validate_report(bad,manifest))
# 2 GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_RESOLVED
bad=copy.deepcopy(run_a); bad["runtime_dependency_audit"]["manual_precomputed_inputs_used"]=["MANUAL_SCOPE_PACKAGE"]; redigest_report(bad)
expect("GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_RESOLVED",lambda:validate_report(bad,manifest))
# 3 RAW_MATURE_REFERENCE_READ_DURING_PRODUCTION
bad=copy.deepcopy(run_a); bad["runtime_dependency_audit"]["raw_mature_reference_used"]=True; redigest_report(bad)
expect("RAW_MATURE_REFERENCE_READ_DURING_PRODUCTION",lambda:validate_report(bad,manifest))
# 4 MANUAL_STUDYMODEL_REQUIRED
bad=copy.deepcopy(run_a); bad["runtime_dependency_audit"]["manual_precomputed_inputs_used"]=["LearnerStudyModel"]; redigest_report(bad)
expect("MANUAL_STUDYMODEL_REQUIRED",lambda:validate_report(bad,manifest))
# 5 NO_ATTEMPT_RUN_INVENTS_WEAKNESS
bad_internal=copy.deepcopy(ia); bad_internal["learner_intelligence"]["learner_state_snapshot"]["capability_states"][0]["readiness"]="DEVELOPING"
expect("NO_ATTEMPT_RUN_INVENTS_WEAKNESS",lambda:validate_report(run_a,manifest,bad_internal))
# 6 ATTEMPT_RUN_CHANGES_ASSESSMENT_SCOPE
bad=copy.deepcopy(comparison); bad["invariants"]["assessment_scope_identical"]=False; redigest_comp(bad)
expect("ATTEMPT_RUN_CHANGES_ASSESSMENT_SCOPE",lambda:validate_comparison(bad,run_a,run_b))
# 7 FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE
bad=copy.deepcopy(run_a); bad["authority_trace"][0]["decision_class"]="UNAUTHORIZED_DECISION"; redigest_report(bad)
expect("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE",lambda:validate_report(bad,manifest))
# 8 RAW_PR156_OR_PR157_READ_DURING_PRODUCTION
bad=copy.deepcopy(run_a); bad["runtime_dependency_audit"]["raw_pr156_or_pr157_used"]=True; redigest_report(bad)
expect("RAW_PR156_OR_PR157_READ_DURING_PRODUCTION",lambda:validate_report(bad,manifest))
# 9 MANUAL_PROBLEM_FAMILY_MAP_REQUIRED
bad=copy.deepcopy(run_a); bad["runtime_dependency_audit"]["manual_precomputed_inputs_used"]=["ProblemFamilyMap"]; redigest_report(bad)
expect("MANUAL_PROBLEM_FAMILY_MAP_REQUIRED",lambda:validate_report(bad,manifest))
# 10 TEST_ORACLE_PROMOTED_TO_PRODUCER
bad=copy.deepcopy(run_b); bad["runtime_dependency_audit"]["test_oracle_producer_legal"]=True; redigest_report(bad)
expect("TEST_ORACLE_PROMOTED_TO_PRODUCER",lambda:validate_report(bad,manifest))
# 11 UPSTREAM_PCK_BLOCKER_RELEASE_BYPASS
bad=copy.deepcopy(run_a); bad["release_status"]="M_K_SEMANTIC_CANDIDATE_ONLY"; redigest_report(bad)
expect("UPSTREAM_PCK_BLOCKER_RELEASE_BYPASS",lambda:validate_report(bad,manifest))
# 11b PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL
bad=copy.deepcopy(run_a); bad["core1_authoring"]["release_legal"]=True; redigest_report(bad)
expect("PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL",lambda:validate_report(bad,manifest))
# 11c a provisional run may not silently claim the expert-reviewed production status
bad=copy.deepcopy(run_a)
bad["core1_authoring"]["status"]="PRODUCTION_PLAN_READY"
bad["release_status"]="M_K_SEMANTIC_CANDIDATE_ONLY"
redigest_report(bad)
expect("PRODUCTION_CORE1_WITHOUT_EXPERT_PCK_REVIEW",lambda:validate_report(bad,manifest))
# 11d COLD_START_STILL_BLOCKED_AFTER_PCK_FIX: with candidate coverage and a
# populated promotion registry the run must not report the pre-fix blocked state.
assert run_a["release_status"]!="BLOCKED_UPSTREAM_PCK"
assert run_b["release_status"]!="BLOCKED_UPSTREAM_PCK"
# 12 ATTEMPT_RUN_CHANGES_CANONICAL_MATH_TRUTH
bad=copy.deepcopy(comparison); bad["invariants"]["canonical_math_truth_identical"]=False; redigest_comp(bad)
expect("ATTEMPT_RUN_CHANGES_CANONICAL_MATH_TRUTH",lambda:validate_comparison(bad,run_a,run_b))
# 13 ATTEMPT_RUN_CHANGES_CORE2_SEMANTICS
bad=copy.deepcopy(comparison); bad["invariants"]["core2_semantics_identical"]=False; redigest_comp(bad)
expect("ATTEMPT_RUN_CHANGES_CORE2_SEMANTICS",lambda:validate_comparison(bad,run_a,run_b))

# Deterministic replay from repository authority only.
run_a2,ia2=run_cold_start(copy.deepcopy(questions),copy.deepcopy(topic),repo_root=REPO,run_id="MATH-M-K-RUN-A")
run_b2,ib2=run_cold_start(copy.deepcopy(questions),copy.deepcopy(topic),copy.deepcopy(attempts),repo_root=REPO,run_id="MATH-M-K-RUN-B",fixture_observation_oracle=True)
assert json.dumps(run_a,sort_keys=True,separators=(",",":"),ensure_ascii=False)==json.dumps(run_a2,sort_keys=True,separators=(",",":"),ensure_ascii=False)
assert json.dumps(run_b,sort_keys=True,separators=(",",":"),ensure_ascii=False)==json.dumps(run_b2,sort_keys=True,separators=(",",":"),ensure_ascii=False)

print("MATH M-K required issue falsifiers PASS")
print("MATH M-K Run A no-attempt repository-only cold start PASS")
print("MATH M-K Run B attempt-present repository-only cold start PASS")
print("MATH M-K upstream success / downstream failure localization PASS")
print("MATH M-K PCK fail-closed release boundary PASS")
print("MATH M-K Run A/B invariant comparison PASS")
print("MATH M-K deterministic replay PASS")
