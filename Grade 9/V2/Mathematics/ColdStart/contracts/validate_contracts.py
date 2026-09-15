#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
MATH=D.parent
REPO=MATH.parents[2]
sys.path.insert(0,str(D/"engine"))
from math_cold_start_runner import digest, load

REQUIRED_DECISIONS={
    "CONCEPT_INCLUSION","ITEM_VALIDITY","SCOPE_RECONCILIATION","TREATMENT_DEPTH",
    "EXPLANATION_REPRESENTATION","WORKED_EXAMPLE","CORE1_PCK_LEGALITY",
    "ORIGINAL_QUESTION_CORE2","HINTS","REASONING_STEP","VERIFICATION","LONGITUDINAL_REVISIT",
}
REQUIRED_RUNTIME={"QuestionSet","DeclaredTopicScope"}
OPTIONAL_RUNTIME={"AttemptSet"}
FORBIDDEN_MANUAL={
    "MANUAL_LEARNER_STUDY_MODEL","MANUAL_SCOPE_PACKAGE","MANUAL_PROBLEM_FAMILY_MAP","MANUAL_ASSESSMENT_REVIEW"
}


def fail(code, detail=""):
    raise ValueError(f"{code}:{detail}" if detail else code)


def schema(name):
    return load(D/"contracts"/name)


def validate_manifest(manifest):
    if manifest.get("manifest_digest") != digest(manifest,"manifest_digest"):
        fail("GENERATION_AUTHORITY_MANIFEST_DIGEST_MISMATCH")
    if set(manifest["runtime_input_contract"]["required"]) != REQUIRED_RUNTIME:
        fail("COLD_START_INPUT_CONTRACT_DRIFT","required")
    if set(manifest["runtime_input_contract"]["optional"]) != OPTIONAL_RUNTIME:
        fail("COLD_START_INPUT_CONTRACT_DRIFT","optional")
    forbidden=set(manifest["runtime_input_contract"]["forbidden"])
    required_forbidden={"ISSUE_HISTORY","CHAT_HISTORY","ARCHITECT_HINTS","RAW_PR156","RAW_PR157","RAW_MATURE_REFERENCE"}|FORBIDDEN_MANUAL
    if not required_forbidden <= forbidden:
        fail("COLD_START_FORBIDDEN_INPUT_POLICY_GAP",",".join(sorted(required_forbidden-forbidden)))
    if set(manifest["required_authority_trace_decisions"]) != REQUIRED_DECISIONS:
        fail("AUTHORITY_TRACE_DECISION_COVERAGE_DRIFT")
    if manifest.get("entrypoint") != "Grade 9/V2/Mathematics/V2_GENERATION_ENTRYPOINT.md":
        fail("COLD_START_ENTRYPOINT_DRIFT")
    if not (REPO/manifest["entrypoint"]).exists():
        fail("COLD_START_ENTRYPOINT_MISSING")
    if "LearnerStudyModel" not in manifest["derived_not_runtime_inputs"] or "MathAssessmentScopeModel" not in manifest["derived_not_runtime_inputs"]:
        fail("GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_RESOLVED")
    forbidden_fragments=[x.lower() for x in manifest["forbidden_runtime_path_fragments"]]
    for name,binding in manifest["authority_bindings"].items():
        path=binding["path"]
        if not (REPO/path).exists():
            fail("AUTHORITY_BINDING_PATH_MISSING",f"{name}:{path}")
        low=path.lower()
        if any(fragment in low for fragment in forbidden_fragments):
            fail("COLD_START_AUTHORITY_PATH_FORBIDDEN",path)
    for binding in manifest.get("test_only_bindings",[]):
        if binding.get("producer_legal") is not False:
            fail("TEST_ONLY_AUTHORITY_PROMOTED_TO_PRODUCER",binding.get("path","?"))
        if not (REPO/binding["path"]).exists():
            fail("TEST_ONLY_BINDING_PATH_MISSING",binding["path"])
    production=load(MATH/"InstructionalKnowledge/registry/math-pck-promotion-registry.json")
    if production.get("registry_class")!="PRODUCTION":
        fail("PRODUCTION_PCK_REGISTRY_CLASS_INVALID")
    return True


def validate_report(report, manifest, internals=None):
    Draft202012Validator(schema("math-cold-start-run-report.schema.json")).validate(report)
    if report["report_digest"] != digest(report,"report_digest"):
        fail("COLD_START_REPORT_DIGEST_MISMATCH")
    audit=report["runtime_dependency_audit"]
    if audit["chat_or_issue_history_used"]:
        fail("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY")
    if audit["raw_mature_reference_used"]:
        fail("RAW_MATURE_REFERENCE_READ_DURING_PRODUCTION")
    if audit["raw_pr156_or_pr157_used"]:
        fail("RAW_PR156_OR_PR157_READ_DURING_PRODUCTION")
    if audit["forbidden_reads"]:
        fail("COLD_START_FORBIDDEN_RUNTIME_READ",audit["forbidden_reads"][0])
    manual=set(audit["manual_precomputed_inputs_used"])
    if manual:
        upper={x.upper() for x in manual}
        if any("STUDYMODEL" in x.replace("_","") or "LEARNERSTUDYMODEL" in x.replace("_","") for x in upper):
            fail("MANUAL_STUDYMODEL_REQUIRED")
        if any("PROBLEMFAMILY" in x.replace("_","") for x in upper):
            fail("MANUAL_PROBLEM_FAMILY_MAP_REQUIRED")
        if any("SCOPE" in x for x in upper):
            fail("GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_RESOLVED")
        fail("MANUAL_PRECOMPUTED_RUNTIME_INPUT_USED",",".join(sorted(manual)))
    if audit["test_oracle_used"]:
        if report["attempt_mode"]!="PRESENT":
            fail("TEST_ORACLE_USED_WITHOUT_ATTEMPT")
        if audit["test_oracle_producer_legal"] is not False:
            fail("TEST_ORACLE_PROMOTED_TO_PRODUCER")
    elif audit["test_oracle_producer_legal"]:
        fail("TEST_ORACLE_PROMOTED_TO_PRODUCER")
    input_contract=report["runtime_input_contract"]
    if report["attempt_mode"]=="ABSENT" and input_contract["attempt_set_ref"] is not None:
        fail("NO_ATTEMPT_RUN_HAS_ATTEMPT_REF")
    if report["attempt_mode"]=="PRESENT" and not input_contract["attempt_set_ref"]:
        fail("ATTEMPT_RUN_MISSING_ATTEMPT_REF")
    trace={x["decision_class"]:x for x in report["authority_trace"]}
    if set(trace)!=REQUIRED_DECISIONS:
        missing=sorted(REQUIRED_DECISIONS-set(trace))
        fail("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE",",".join(missing))
    forbidden_fragments=[x.lower() for x in manifest["forbidden_runtime_path_fragments"]]
    for decision,row in trace.items():
        if not row["authority_refs"] or not row["output_refs"]:
            fail("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE",decision)
        for ref in row["authority_refs"]:
            low=ref.lower()
            if any(fragment in low for fragment in forbidden_fragments):
                fail("COLD_START_AUTHORITY_TRACE_FORBIDDEN_SOURCE",ref)
    c1=report["core1_authoring"]
    if not c1["scope_complete"]:
        fail("CORE1_AUTHORING_OBLIGATION_SCOPE_INCOMPLETE")
    if c1["status"]=="BLOCKED_PCK_CANDIDATE_COVERAGE":
        if not c1["missing_pck_candidate_capability_refs"] or c1["production_plan_ref"] is not None:
            fail("PCK_CANDIDATE_BLOCKER_BYPASSED")
        if "M-G/#242:PCK_CANDIDATE_COVERAGE" not in report["blockers"]:
            fail("PCK_CANDIDATE_BLOCKER_NOT_REPORTED")
    elif c1["status"]=="BLOCKED_PCK_PROMOTION":
        if c1["missing_pck_candidate_capability_refs"] or not c1["unpromoted_pck_capability_refs"] or c1["production_plan_ref"] is not None:
            fail("PCK_PROMOTION_BLOCKER_BYPASSED")
        if "M-G/#242:PCK_HUMAN_PROMOTION" not in report["blockers"]:
            fail("PCK_PROMOTION_BLOCKER_NOT_REPORTED")
    elif c1["status"]=="PRODUCTION_PLAN_READY":
        if c1["missing_pck_candidate_capability_refs"] or c1["unpromoted_pck_capability_refs"] or not c1["production_plan_ref"]:
            fail("PRODUCTION_CORE1_WITHOUT_PCK_LEGALITY")
        if c1["provisional_only_pck_capability_refs"] or not c1["release_legal"] or c1["pck_expert_review_state"]!="PASS":
            fail("PRODUCTION_CORE1_WITHOUT_EXPERT_PCK_REVIEW")
    elif c1["status"]=="PROVISIONAL_PLAN_READY":
        if c1["missing_pck_candidate_capability_refs"] or c1["unpromoted_pck_capability_refs"] or not c1["production_plan_ref"]:
            fail("PROVISIONAL_CORE1_WITHOUT_PCK_AUTHORING_LEGALITY")
        if not c1["provisional_only_pck_capability_refs"]:
            fail("PROVISIONAL_CORE1_WITHOUT_PROVISIONAL_PCK")
        if c1["release_legal"] or c1["pck_expert_review_state"]!="PENDING":
            fail("PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL")
        if "M-G/#242:PCK_EXPERT_REVIEW_PENDING" not in report["blockers"]:
            fail("PCK_EXPERT_REVIEW_BLOCKER_NOT_REPORTED")
    else:
        fail("UNKNOWN_CORE1_AUTHORING_STATUS",c1["status"])
    expected_release={
        "PRODUCTION_PLAN_READY":"M_K_SEMANTIC_CANDIDATE_ONLY",
        "PROVISIONAL_PLAN_READY":"PROVISIONAL_PENDING_PCK_EXPERT_REVIEW",
    }.get(c1["status"],"BLOCKED_UPSTREAM_PCK")
    if report["release_status"]!=expected_release:
        fail("UPSTREAM_PCK_BLOCKER_RELEASE_BYPASS")
    if report["core2"]["question_count"]!=14 or report["core2"]["source_fidelity"] is not True:
        fail("CORE2_SOURCE_CUSTODY_LOST")
    if c1["status"] not in {"PRODUCTION_PLAN_READY","PROVISIONAL_PLAN_READY"} and report["core2"]["publication_ready"]:
        fail("CORE2_PUBLISHED_WITH_UNMATERIALIZED_CORE1")
    if c1["status"]=="PROVISIONAL_PLAN_READY" and report["core2"]["core1_linkage_mode"]!="MATERIALIZED_PROVISIONAL":
        fail("PROVISIONAL_CORE1_LINKAGE_STATE_DRIFT")
    if report["coverage_closure"]["assessment_row_count"]!=17:
        fail("ASSESSMENT_COVERAGE_ROW_GAP")
    if report["coverage_closure"]["semantic_gap_count"]!=0:
        fail("PUBLICATION_COVERAGE_GAP")
    if bool(report["blockers"]) != (report["cold_start_status"]=="PASS_WITH_UPSTREAM_RELEASE_BLOCKERS"):
        fail("COLD_START_STATUS_BLOCKER_MISMATCH")
    if internals is not None:
        snapshot=internals["learner_intelligence"]["learner_state_snapshot"]
        if report["stage_outputs"]["learner_state_digest"]!=snapshot["snapshot_digest"]:
            fail("COLD_START_STAGE_OUTPUT_DRIFT","learner_state")
        core2=internals["core2"]
        if report["stage_outputs"]["core2_plan_ref"]!=core2["plan_id"] or report["stage_outputs"]["core2_plan_digest"]!=core2["plan_digest"]:
            fail("COLD_START_STAGE_OUTPUT_DRIFT","core2")
        closure=internals["closure"]
        if report["stage_outputs"]["coverage_package_digest"]!=closure["package_digest"]:
            fail("COLD_START_STAGE_OUTPUT_DRIFT","closure")
        if report["attempt_mode"]=="ABSENT":
            if internals["learner_intelligence"]["observations"] or snapshot["diagnostic_cases"]:
                fail("NO_ATTEMPT_RUN_INVENTS_WEAKNESS")
            if any(x["readiness"]!="UNKNOWN" for x in snapshot["capability_states"]):
                fail("NO_ATTEMPT_RUN_INVENTS_WEAKNESS")
    return True


def validate_comparison(comp, run_a, run_b):
    Draft202012Validator(schema("math-cold-start-comparison.schema.json")).validate(comp)
    if comp["comparison_digest"] != digest(comp,"comparison_digest"):
        fail("COLD_START_COMPARISON_DIGEST_MISMATCH")
    if comp["run_a_ref"]!=run_a["run_id"] or comp["run_b_ref"]!=run_b["run_id"]:
        fail("COLD_START_COMPARISON_RUN_BINDING_MISMATCH")
    if run_a["attempt_mode"]!="ABSENT" or run_b["attempt_mode"]!="PRESENT":
        fail("COLD_START_COMPARISON_MODE_MISMATCH")
    if run_a["runtime_input_contract"]["question_set_ref"]!=run_b["runtime_input_contract"]["question_set_ref"] or run_a["runtime_input_contract"]["declared_topic_scope_ref"]!=run_b["runtime_input_contract"]["declared_topic_scope_ref"]:
        fail("ATTEMPT_RUN_CHANGES_REQUIRED_INPUT_SCOPE")
    inv=comp["invariants"]
    if not inv["assessment_scope_identical"]:
        fail("ATTEMPT_RUN_CHANGES_ASSESSMENT_SCOPE")
    if not inv["canonical_math_truth_identical"]:
        fail("ATTEMPT_RUN_CHANGES_CANONICAL_MATH_TRUTH")
    if not inv["core2_semantics_identical"]:
        fail("ATTEMPT_RUN_CHANGES_CORE2_SEMANTICS")
    diff=comp["expected_differences"]
    if not diff["learner_state_changed"]:
        fail("ATTEMPT_RUN_DOES_NOT_CHANGE_LEARNER_STATE")
    if not diff["treatment_changed"]:
        fail("ATTEMPT_RUN_DOES_NOT_CHANGE_TREATMENT")
    if not diff["support_changed"]:
        fail("ATTEMPT_RUN_DOES_NOT_CHANGE_SUPPORT")
    return True


def main():
    manifest=load(MATH/"GENERATION_AUTHORITY_MANIFEST.json")
    validate_manifest(manifest)
    Draft202012Validator.check_schema(schema("math-cold-start-run-report.schema.json"))
    Draft202012Validator.check_schema(schema("math-cold-start-comparison.schema.json"))
    print("MATH M-K manifest + cold-start contracts PASS")


if __name__=="__main__":
    main()
