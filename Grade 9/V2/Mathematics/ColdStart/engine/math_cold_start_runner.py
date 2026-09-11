#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from pathlib import Path

D=Path(__file__).resolve().parents[1]
MATH=D.parent
REPO=MATH.parents[2]
for p in [
    MATH/"AssessmentIntake"/"engine",
    MATH/"AssessmentReview"/"engine",
    MATH/"AssessmentScope"/"engine",
    MATH/"ProblemSemantics"/"engine",
    MATH/"LearnerIntelligence"/"engine",
    MATH/"StudySynthesis"/"engine",
    MATH/"Core1Authoring"/"engine",
    MATH/"Core2Transfer"/"engine",
    MATH/"CoverageClosure"/"engine",
]:
    sys.path.insert(0,str(p))

from build_math_assessment_intake import build_intake
from review_math_assessment import build_review
from reconcile_math_assessment_scope import reconcile
from build_math_problem_semantics import build_package as build_problem_semantics, load_family_registry
from derive_math_learner_state import derive as derive_learner_state
from synthesize_math_study_model import build_study_scope, synthesize
from author_math_core1 import author as author_core1, load_candidate_bundle
from build_math_core2_transfer import build_plan as build_core2
from build_math_coverage_closure import build_package as build_closure

FULL_TREATMENTS={"ACTIVE_STUDY","REPAIR_BEFORE","REPAIR_IN_UNIT"}

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def canon(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def digest(value, omit=None):
    x=copy.deepcopy(value)
    if omit and isinstance(x,dict):
        x.pop(omit,None)
    return hashlib.sha256(canon(x).encode("utf-8")).hexdigest()

def authority(path):
    return load(MATH/path)

def candidate_assets():
    reg, assets=load_candidate_bundle(MATH/"InstructionalKnowledge"/"registry"/"math-pck-candidates.json")
    return reg, assets

def pck_legality(study_model):
    reg,assets=candidate_assets()
    production=authority("InstructionalKnowledge/registry/math-pck-promotion-registry.json")
    coverage={}
    for asset in assets:
        for cap in asset["capability_refs"]:
            coverage.setdefault(cap,[]).append(asset["asset_id"])
    promoted={}
    for rec in production["promotions"]:
        if rec["promotion_status"]=="PROMOTED" and rec.get("producer_legal") is True:
            asset=next((a for a in assets if a["asset_id"]==rec["asset_id"]),None)
            if asset and asset["asset_digest"]==rec["asset_digest"]:
                for cap in asset["capability_refs"]:
                    promoted.setdefault(cap,[]).append(asset["asset_id"])
    full=sorted(x["capability_ref"] for x in study_model["capability_plans"] if x["treatment"] in FULL_TREATMENTS)
    missing=sorted(cap for cap in full if not coverage.get(cap))
    unpromoted=sorted(cap for cap in full if coverage.get(cap) and not promoted.get(cap))
    return reg,assets,production,full,missing,unpromoted

def treatment_signature(study_model):
    return digest([{"capability_ref":x["capability_ref"],"treatment":x["treatment"],"readiness":x["learner_state_readiness"]} for x in study_model["capability_plans"]])

def support_overlay(core2, study_model):
    by_cap={x["capability_ref"]:x["treatment"] for x in study_model["capability_plans"]}
    rows=[]
    for page in core2["pages"]:
        treatments=sorted({by_cap[c] for c in page["capability_refs"] if c in by_cap})
        if "REPAIR_BEFORE" in treatments:
            mode="REPAIR_BEFORE_TRANSFER"
        elif "PROBE_FIRST" in treatments:
            mode="PROBE_FIRST"
        elif "REPAIR_IN_UNIT" in treatments:
            mode="TARGETED_REPAIR"
        elif treatments and all(x=="VERIFY_ONLY" for x in treatments):
            mode="ATTEMPT_AND_VERIFY"
        else:
            mode="STUDY_THEN_ATTEMPT"
        rows.append({"question_ref":page["question_ref"],"support_mode":mode,"treatment_refs":treatments})
    return rows

def core2_truth_signature(core2):
    rows=[]
    for p in core2["pages"]:
        rows.append({
            "question_ref":p["question_ref"],
            "source_ref":p["source_ref"],
            "assessment_safety":p["assessment_safety"],
            "problem_family_ref":p["problem_family_ref"],
            "reasoning_route":p["reasoning_route"],
            "guide_demand_badge":p["guide_demand_badge"],
            "solution_route":p["solution_route"],
            "representation_plan":p["representation_plan"],
        })
    return digest(rows)

def build_authority_trace(intake, review, scope_model, problem, study_model, core1_info, core2, closure):
    A="Grade 9/V2/Mathematics/"
    refs={
      "CONCEPT_INCLUSION":[A+"AssessmentScope/authority/math-assessment-scope-authority.json"],
      "ITEM_VALIDITY":[A+"AssessmentReview/registry/assessment-item-validity-registry.json",A+"AssessmentReview/policies/diagnostic-use-policy.json"],
      "SCOPE_RECONCILIATION":[A+"AssessmentScope/registry/mixed-grade9-question-scope-bindings.json"],
      "TREATMENT_DEPTH":[A+"StudySynthesis/policies/math-treatment-policy.json"],
      "EXPLANATION_REPRESENTATION":[A+"RepresentationSemantics/registry/math-teaching-primitive-registry.json",A+"RepresentationSemantics/policies/math-page-intent-profile.json"],
      "WORKED_EXAMPLE":[A+"Core1Authoring/policies/math-instructional-authoring-profile.json",A+"Core1Authoring/contracts/math-problem-authoring-plan.schema.json"],
      "CORE1_PCK_LEGALITY":[A+"InstructionalKnowledge/registry/math-pck-candidates.json",A+"InstructionalKnowledge/registry/math-pck-promotion-registry.json"],
      "ORIGINAL_QUESTION_CORE2":[A+"Core2Transfer/registry/math-core2-authoring-profile.json"],
      "HINTS":[A+"Core2Transfer/registry/math-core2-authoring-profile.json"],
      "REASONING_STEP":[A+"ProblemSemantics/registry/math-reasoning-role-registry.json",A+"ProblemSemantics/registry/math-problem-family-registry.json"],
      "VERIFICATION":[A+"ProblemSemantics/registry/math-verification-route-registry.json"],
      "LONGITUDINAL_REVISIT":[A+"CoverageClosure/registry/math-transfer-evidence-policy.json",A+"StudySynthesis/policies/math-treatment-policy.json"],
    }
    outputs={
      "CONCEPT_INCLUSION":[scope_model["scope_model_id"]],
      "ITEM_VALIDITY":[review["review_bundle_id"]],
      "SCOPE_RECONCILIATION":[scope_model["scope_model_id"]],
      "TREATMENT_DEPTH":[study_model["study_model_id"]],
      "EXPLANATION_REPRESENTATION":[core2["plan_id"]],
      "WORKED_EXAMPLE":[core1_info["candidate_class"]],
      "CORE1_PCK_LEGALITY":[core1_info["status"]],
      "ORIGINAL_QUESTION_CORE2":[core2["plan_id"]],
      "HINTS":[core2["plan_id"]],
      "REASONING_STEP":[problem["package_id"]],
      "VERIFICATION":[problem["package_id"]],
      "LONGITUDINAL_REVISIT":[closure["publication_coverage_closure"]["closure_id"]],
    }
    return [{"decision_class":k,"authority_refs":refs[k],"output_refs":outputs[k]} for k in refs]

def fixture_reviewed_observations(attempt_set, fixture_oracle):
    if attempt_set is None:
        return None,False
    if not fixture_oracle:
        raise ValueError("ATTEMPT_SEMANTIC_REVIEW_STAGE_REQUIRED")
    fixture=authority("LearnerIntelligence/fixtures/reviewed-observations.fixture.json")
    if fixture["attempt_set_ref"]!=attempt_set["attempt_set_id"]:
        raise ValueError("TEST_ORACLE_ATTEMPT_SET_MISMATCH")
    return fixture,True

def run_cold_start(question_set, topic_scope, attempt_set=None, repo_root=None, run_id="MATH-M-K-RUN", fixture_observation_oracle=False):
    if repo_root is not None and Path(repo_root).resolve()!=REPO.resolve():
        raise ValueError("COLD_START_NON_REPOSITORY_AUTHORITY_ROOT")
    intake=build_intake(copy.deepcopy(question_set),copy.deepcopy(topic_scope),copy.deepcopy(attempt_set) if attempt_set else None,run_id+"-INTAKE")
    review_reg=authority("AssessmentReview/registry/assessment-item-validity-registry.json")
    review_policy=authority("AssessmentReview/policies/diagnostic-use-policy.json")
    scope_authority=authority("AssessmentScope/authority/math-assessment-scope-authority.json")
    scope_bindings=authority("AssessmentScope/registry/mixed-grade9-question-scope-bindings.json")
    review=build_review(copy.deepcopy(question_set),review_reg,review_policy,run_id+"-REVIEW")
    scope_model,scope_coverage,reconciliation,prereq=reconcile(question_set,topic_scope,review_reg,review_policy,scope_authority,scope_bindings)

    role_reg=authority("ProblemSemantics/registry/math-reasoning-role-registry.json")
    family_reg=load_family_registry(MATH/"ProblemSemantics"/"registry"/"math-problem-family-registry.json")
    verification_reg=authority("ProblemSemantics/registry/math-verification-route-registry.json")
    item_semantics_reg=authority("ProblemSemantics/registry/mixed-grade9-item-semantics.json")
    badge_policy=authority("ProblemSemantics/registry/guide-demand-badge-policy.json")
    problem=build_problem_semantics(question_set,topic_scope,review_reg,review_policy,scope_authority,scope_bindings,role_reg,family_reg,verification_reg,item_semantics_reg,badge_policy)

    reviewed_fixture,oracle_used=fixture_reviewed_observations(attempt_set,fixture_observation_oracle)
    obs_registry=authority("LearnerIntelligence/registry/math-observation-type-registry.json")
    li=derive_learner_state(question_set,review_reg,scope_authority,item_semantics_reg,obs_registry,attempt_set,reviewed_fixture)
    snapshot=li["learner_state_snapshot"]
    treatment_policy=authority("StudySynthesis/policies/math-treatment-policy.json")
    study_scope=build_study_scope(scope_bindings,scope_authority)
    study_model=synthesize(study_scope,snapshot,treatment_policy)

    cand_reg,cand_assets,prod_promos,full,missing,unpromoted=pck_legality(study_model)
    core1_plan=None
    if missing:
        c1status="BLOCKED_PCK_CANDIDATE_COVERAGE"
    elif unpromoted:
        c1status="BLOCKED_PCK_PROMOTION"
    else:
        core1_plan=author_core1(
            {"learner_study_model":study_model},cand_reg,cand_assets,prod_promos,
            authority("Core1Authoring/policies/math-instructional-authoring-profile.json"),
            authority("Core1Authoring/policies/math-core1-scope-completeness-policy.json"),
            test_mode=False,
        )
        c1status="PRODUCTION_PLAN_READY"
    core1_info={
      "candidate_class":"SCOPE_COMPLETE_AUTHORING_OBLIGATION_PLAN",
      "scope_complete":set(study_scope["direct_assessed_capability_refs"]+study_scope["prerequisite_support_capability_refs"])=={x["capability_ref"] for x in study_model["capability_plans"]},
      "required_capability_count":len(study_model["capability_plans"]),
      "full_teaching_capability_count":len(full),
      "missing_pck_candidate_capability_refs":missing,
      "unpromoted_pck_capability_refs":unpromoted,
      "production_plan_ref":core1_plan["core1_study_plan_id"] if core1_plan else None,
      "status":c1status,
    }

    primitives=authority("RepresentationSemantics/registry/math-teaching-primitive-registry.json")
    page_intent=authority("RepresentationSemantics/policies/math-page-intent-profile.json")
    core2_profile=authority("Core2Transfer/registry/math-core2-authoring-profile.json")
    core2=build_core2(question_set,review_reg,review_policy,scope_bindings,scope_authority,problem,verification_reg,primitives,page_intent,core2_profile,core1_plan)
    overlay=support_overlay(core2,study_model)
    outcomes={"fixture_id":run_id+"-NO-POST-TRANSFER-EVIDENCE","subject":"MATHEMATICS","question_set_ref":question_set["question_set_id"],"outcomes":[]}
    closure=build_closure(question_set,scope_bindings,study_model,snapshot,core2,outcomes,authority("CoverageClosure/registry/math-transfer-evidence-policy.json"))

    blockers=[]
    if missing:
        blockers.append("M-G/#242:PCK_CANDIDATE_COVERAGE")
    if unpromoted:
        blockers.append("M-G/#242:PCK_HUMAN_PROMOTION")
    if not core2["summary"]["publication_ready"]:
        blockers.append("M-I/M-J:PUBLICATION_NOT_READY")
    blockers=sorted(set(blockers))

    signatures={
      "assessment_scope":digest({"scope_model":scope_model["scope_model_digest"],"coverage":scope_coverage["matrix_digest"],"reconciliation":reconciliation["report_digest"],"prereq":prereq["closure_digest"]}),
      "canonical_math_truth":digest({"authority":scope_authority["authority_digest"],"problem":problem["package_digest"],"review":review_reg["registry_digest"]}),
      "core2_semantics":core2_truth_signature(core2),
      "learner_state":snapshot["snapshot_digest"],
      "treatment":treatment_signature(study_model),
      "support":digest(overlay),
    }
    gap_report=closure["publication_coverage_closure"]["gap_report"]
    report={
      "run_id":run_id,"schema_version":"1.0.0","subject":"MATHEMATICS","attempt_mode":"PRESENT" if attempt_set else "ABSENT",
      "runtime_input_contract":{"question_set_ref":question_set["question_set_id"],"declared_topic_scope_ref":topic_scope["declared_topic_scope_id"],"attempt_set_ref":attempt_set["attempt_set_id"] if attempt_set else None},
      "runtime_dependency_audit":{
        "chat_or_issue_history_used":False,"raw_mature_reference_used":False,"raw_pr156_or_pr157_used":False,
        "manual_precomputed_inputs_used":[],"test_oracle_used":oracle_used,"test_oracle_producer_legal":False,"forbidden_reads":[]
      },
      "stage_outputs":{
        "intake_ref":intake["intake_id"],"review_ref":review["review_bundle_id"],
        "scope_model_ref":scope_model["scope_model_id"],"scope_model_digest":scope_model["scope_model_digest"],"scope_coverage_digest":scope_coverage["matrix_digest"],
        "problem_semantics_digest":problem["package_digest"],"learner_state_ref":snapshot["snapshot_id"],"learner_state_digest":snapshot["snapshot_digest"],
        "study_scope_ref":study_scope["study_scope_id"],"study_scope_digest":study_scope["scope_digest"],"study_model_ref":study_model["study_model_id"],"study_model_digest":study_model["study_model_digest"],
        "core2_plan_ref":core2["plan_id"],"core2_plan_digest":core2["plan_digest"],
        "coverage_package_ref":closure["package_id"],"coverage_package_digest":closure["package_digest"],
      },
      "signatures":signatures,
      "core1_authoring":core1_info,
      "core2":{"question_count":core2["summary"]["question_count"],"source_fidelity":core2["summary"]["source_fidelity"],"publication_ready":core2["summary"]["publication_ready"],"core1_linkage_mode":core2["core1_linkage_mode"],"support_overlay":overlay},
      "coverage_closure":{"assessment_row_count":len(closure["assessment_coverage_matrix"]["rows"]),"semantic_gap_count":sum(len(v) for v in gap_report.values()),"publication_closure_status":closure["publication_coverage_closure"]["publication_closure_status"]},
      "authority_trace":[],
      "cold_start_status":"PASS_WITH_UPSTREAM_RELEASE_BLOCKERS" if blockers else "PASS_PRODUCTION_SEMANTICS",
      "release_status":"BLOCKED_UPSTREAM_PCK" if c1status!="PRODUCTION_PLAN_READY" else "M_K_SEMANTIC_CANDIDATE_ONLY",
      "blockers":blockers,
      "report_digest":"",
    }
    report["authority_trace"]=build_authority_trace(intake,review,scope_model,problem,study_model,core1_info,core2,closure)
    report["report_digest"]=digest(report,"report_digest")
    internals={"intake":intake,"review":review,"scope_model":scope_model,"scope_coverage":scope_coverage,"problem_semantics":problem,"learner_intelligence":li,"study_scope":study_scope,"study_model":study_model,"core1_plan":core1_plan,"core2":core2,"closure":closure}
    return report,internals

def compare_runs(run_a,run_b):
    comp={
      "comparison_id":"MATH-M-K-COMP-"+digest([run_a["report_digest"],run_b["report_digest"]])[:16],
      "schema_version":"1.0.0","subject":"MATHEMATICS","run_a_ref":run_a["run_id"],"run_b_ref":run_b["run_id"],
      "invariants":{
        "assessment_scope_identical":run_a["signatures"]["assessment_scope"]==run_b["signatures"]["assessment_scope"],
        "canonical_math_truth_identical":run_a["signatures"]["canonical_math_truth"]==run_b["signatures"]["canonical_math_truth"],
        "core2_semantics_identical":run_a["signatures"]["core2_semantics"]==run_b["signatures"]["core2_semantics"],
      },
      "expected_differences":{
        "learner_state_changed":run_a["signatures"]["learner_state"]!=run_b["signatures"]["learner_state"],
        "treatment_changed":run_a["signatures"]["treatment"]!=run_b["signatures"]["treatment"],
        "support_changed":run_a["signatures"]["support"]!=run_b["signatures"]["support"],
      },
      "comparison_digest":"",
    }
    comp["comparison_digest"]=digest(comp,"comparison_digest")
    return comp

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--questions",required=True); ap.add_argument("--topic-scope",required=True); ap.add_argument("--attempts")
    ap.add_argument("--fixture-observation-oracle",action="store_true"); ap.add_argument("--out",required=True); ap.add_argument("--run-id",default="MATH-M-K-RUN")
    a=ap.parse_args()
    report,_=run_cold_start(load(a.questions),load(a.topic_scope),load(a.attempts) if a.attempts else None,REPO,a.run_id,a.fixture_observation_oracle)
    Path(a.out).write_text(json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

if __name__=="__main__": main()
