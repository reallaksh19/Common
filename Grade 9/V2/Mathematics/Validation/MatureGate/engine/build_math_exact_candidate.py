#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from pathlib import Path

D=Path(__file__).resolve().parents[1]
MG=D.parent
MATH=MG.parents[1]
REPO=MATH.parents[2]
sys.path.insert(0,str(MATH/"ColdStart"/"engine"))
from math_cold_start_runner import run_cold_start, compare_runs, load


def canon(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False)


def digest(value, omit=None):
    x=copy.deepcopy(value)
    if omit and isinstance(x,dict): x.pop(omit,None)
    return hashlib.sha256(canon(x).encode("utf-8")).hexdigest()


def fail(code,detail=""):
    raise ValueError(f"{code}:{detail}" if detail else code)


def seal(binding):
    x=copy.deepcopy(binding)
    x.pop("candidate_id",None); x.pop("binding_digest",None)
    binding["candidate_id"]="MATH-ML-CAND-"+digest(x)[:16]
    binding["binding_digest"]=""
    binding["binding_digest"]=digest(binding,"binding_digest")
    return binding


def build_fixture_binding(selected_run="A"):
    if selected_run not in {"A","B"}: fail("UNKNOWN_SELECTED_RUN",selected_run)
    A=MATH/"AssessmentIntake"/"fixtures"
    questions=load(A/"mixed-grade9-question-set.fixture.json")
    topic=load(A/"mixed-grade9-topic-scope.fixture.json")
    attempts=load(A/"mixed-grade9-attempt-set.fixture.json")
    run_a,_=run_cold_start(copy.deepcopy(questions),copy.deepcopy(topic),repo_root=REPO,run_id="MATH-M-K-RUN-A")
    run_b,_=run_cold_start(copy.deepcopy(questions),copy.deepcopy(topic),copy.deepcopy(attempts),repo_root=REPO,run_id="MATH-M-K-RUN-B",fixture_observation_oracle=True)
    comparison=compare_runs(run_a,run_b)
    if not all(comparison["invariants"].values()): fail("M_K_REPRODUCIBILITY_PROOF_NOT_CLOSED")
    selected=run_a if selected_run=="A" else run_b
    blockers=sorted(set(selected["blockers"]+["M-L:RENDERED_EXACT_TWO_PRODUCT_NOT_BOUND"]))
    material="BLOCKED_UPSTREAM_PCK" if selected["core1_authoring"]["status"]!="PRODUCTION_PLAN_READY" else "SEMANTIC_READY_RENDER_NOT_BOUND"
    binding={
      "candidate_id":"",
      "schema_version":"1.0.0",
      "subject":"MATHEMATICS",
      "fixture_class":"PUBLIC_SYNTHETIC_COLD_START",
      "candidate_class":"SEMANTIC_COLD_START_EXACT_PACKAGE",
      "question_set_ref":selected["runtime_input_contract"]["question_set_ref"],
      "declared_topic_scope_ref":selected["runtime_input_contract"]["declared_topic_scope_ref"],
      "attempt_set_ref":selected["runtime_input_contract"]["attempt_set_ref"],
      "selected_run_ref":selected["run_id"],
      "generation_report_digest":selected["report_digest"],
      "reproducibility_proof":{
        "run_a_ref":run_a["run_id"],"run_a_digest":run_a["report_digest"],
        "run_b_ref":run_b["run_id"],"run_b_digest":run_b["report_digest"],
        "comparison_ref":comparison["comparison_id"],"comparison_digest":comparison["comparison_digest"],
        "scope_invariant":comparison["invariants"]["assessment_scope_identical"],
        "canonical_math_invariant":comparison["invariants"]["canonical_math_truth_identical"],
        "core2_semantics_invariant":comparison["invariants"]["core2_semantics_identical"],
      },
      "core1_authoring_status":selected["core1_authoring"]["status"],
      "core2_plan_ref":selected["stage_outputs"]["core2_plan_ref"],
      "core2_plan_digest":selected["stage_outputs"]["core2_plan_digest"],
      "coverage_package_ref":selected["stage_outputs"]["coverage_package_ref"],
      "coverage_package_digest":selected["stage_outputs"]["coverage_package_digest"],
      "materialization_state":material,
      "artifacts":[],
      "artifact_set_digest":None,
      "raw_mature_reference_runtime_used":False,
      "upstream_blockers":blockers,
      "binding_digest":"",
    }
    return seal(binding)


def bind_rendered_artifacts(binding, artifacts, fixture_class=None):
    out=copy.deepcopy(binding)
    if out["core1_authoring_status"]!="PRODUCTION_PLAN_READY":
        fail("RENDERED_CANDIDATE_WITHOUT_PRODUCTION_CORE1")
    blocking=[x for x in out["upstream_blockers"] if x!="M-L:RENDERED_EXACT_TWO_PRODUCT_NOT_BOUND"]
    if blocking: fail("RENDERED_CANDIDATE_WITH_UPSTREAM_BLOCKER",blocking[0])
    roles=[x.get("artifact_role") for x in artifacts]
    if sorted(roles)!=["CORE1_STUDY_GUIDE","CORE2_TRANSFER_BOOK"] or len(set(roles))!=2:
        fail("EXACT_TWO_PRODUCT_TOPOLOGY_REQUIRED")
    for row in artifacts:
        if row.get("media_type")!="application/pdf": fail("EXACT_PRODUCT_MEDIA_TYPE_INVALID",row.get("artifact_role","?"))
        for key in ("artifact_sha256","manifest_digest"):
            value=row.get(key,"")
            if len(value)!=64 or any(c not in "0123456789abcdef" for c in value): fail("EXACT_PRODUCT_DIGEST_INVALID",f"{row.get('artifact_role')}:{key}")
    out["fixture_class"]=fixture_class or out["fixture_class"]
    out["candidate_class"]="RENDERED_TWO_PRODUCT_EXACT_CANDIDATE"
    out["materialization_state"]="RENDERED_EXACT"
    out["artifacts"]=sorted(copy.deepcopy(artifacts),key=lambda x:x["artifact_role"])
    out["artifact_set_digest"]=digest(out["artifacts"])
    out["upstream_blockers"]=[]
    return seal(out)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--selected-run",choices=["A","B"],default="A")
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    result=build_fixture_binding(args.selected_run)
    Path(args.out).write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")


if __name__=="__main__": main()
