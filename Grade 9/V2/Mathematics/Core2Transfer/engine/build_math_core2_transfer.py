#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from pathlib import Path

D=Path(__file__).resolve().parents[1]
MATH=D.parent
sys.path.insert(0,str(MATH/"RepresentationSemantics"/"engine"))
from build_math_representation_plan import build as build_representation_plan

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(x,omit=None):
    y=copy.deepcopy(x)
    if omit and isinstance(y,dict): y.pop(omit,None)
    return hashlib.sha256(canon(y).encode("utf-8")).hexdigest()
def fail(code,detail=""): raise ValueError(f"{code}:{detail}" if detail else code)
def norm(s): return " ".join(str(s).lower().split())

PRIMITIVE_BY_REQUIREMENT={
 "NATURAL_LANGUAGE_STATEMENT":"MATH-TP-INVARIANT_HIGHLIGHT-v1",
 "ORDERED_PAIR":"MATH-TP-COORDINATE_PLANE-v1",
 "GEOMETRIC_DISTANCE_RELATION":"MATH-TP-ANNOTATED_DERIVATION-v1",
 "SYMBOLIC_LINEAR_EQUATION":"MATH-TP-ALIGNED_TRANSFORMATION_STACK-v1",
 "UNORDERED_PAIR_MODEL":"MATH-TP-INVARIANT_HIGHLIGHT-v1",
 "SLOPE_RATIO":"MATH-TP-COORDINATE_PLANE-v1",
 "ANGLE_RELATION":"MATH-TP-PARALLEL_MEET_CONTRAST-v1",
 "PARAMETER_CONDITION":"MATH-TP-ANNOTATED_DERIVATION-v1",
 "SYSTEM_OF_LINEAR_EQUATIONS":"MATH-TP-ALIGNED_TRANSFORMATION_STACK-v1",
 "CARTESIAN_AXIS_CONSTRAINT":"MATH-TP-COORDINATE_PLANE-v1",
 "UNIT_RATE":"MATH-TP-ANNOTATED_DERIVATION-v1",
 "RATE_CONTEXT_MODEL":"MATH-TP-SIDE_BY_SIDE_METHOD_VIEW-v1"
}

JOB_BY_PRIMITIVE={
 "MATH-TP-INVARIANT_HIGHLIGHT-v1":"SHOW_STRUCTURE",
 "MATH-TP-COORDINATE_PLANE-v1":"CONNECT_REPRESENTATIONS",
 "MATH-TP-ANNOTATED_DERIVATION-v1":"CONNECT_REPRESENTATIONS",
 "MATH-TP-ALIGNED_TRANSFORMATION_STACK-v1":"EXPOSE_TRANSFORMATION",
 "MATH-TP-PARALLEL_MEET_CONTRAST-v1":"DISCRIMINATE_CASES",
 "MATH-TP-SIDE_BY_SIDE_METHOD_VIEW-v1":"COMPARE_METHODS",
}

def primitive_payload(pid,q,sem,review):
    stem=q["stem"]
    transitions=[x["mathematical_transition"] for x in sem["reasoning_route"]["steps"]]
    roles=[x["role"] for x in sem["reasoning_route"]["steps"]]
    if pid=="MATH-TP-INVARIANT_HIGHLIGHT-v1":
        return {"mathematical_object":stem,"invariant":"Preserve the mathematical meaning of the stated condition.","changing_features":["surface wording","numeric data"]}
    if pid=="MATH-TP-COORDINATE_PLANE-v1":
        pts=[x["text"] for x in q.get("givens",[])] or [stem]
        return {"points":pts,"axes":["x-axis","y-axis"],"relations":list(dict.fromkeys(sem["reasoning_route"]["steps"][0].get("representation_refs",[]) + [sem["primary_family_ref"]]))}
    if pid=="MATH-TP-ANNOTATED_DERIVATION-v1":
        return {"steps":transitions,"annotations":roles,"conclusion":review["review_rationale"]}
    if pid=="MATH-TP-ALIGNED_TRANSFORMATION_STACK-v1":
        return {"states":[stem]+transitions,"operations":["apply one declared legal mathematical transformation at each step"],"invariant":"preserve equivalence and variable meaning"}
    if pid=="MATH-TP-PARALLEL_MEET_CONTRAST-v1":
        return {"angle_sum_cases":["same-side sum < 180 degrees","same-side sum = 180 degrees"],"boundary":"180 degrees","outcomes":["lines meet on that side","parallel boundary"]}
    if pid=="MATH-TP-SIDE_BY_SIDE_METHOD_VIEW-v1":
        return {"left_method":"downstream: effective speed x+y and speed=distance/time","right_method":"upstream: effective speed x-y and speed=distance/time","comparison_invariant":"each effective speed must reproduce its stated journey time"}
    fail("UNSUPPORTED_REPRESENTATION_PRIMITIVE",pid)

def representation_spec(req,pid,q,sem,review,cap,primitive):
    payload=primitive_payload(pid,q,sem,review)
    contrast_ref="MEET_VS_PARALLEL_BOUNDARY" if pid=="MATH-TP-PARALLEL_MEET_CONTRAST-v1" else None
    spec={
      "representation_id":"MATH-RSPEC-"+digest({"q":q["question_id"],"req":req})[:12].upper(),
      "schema_version":"1.0.0","subject":"MATHEMATICS","surface_role":"CORE2_TRANSFER","semantic_role":"INSTRUCTIONAL",
      "semantic_requirement_ref":req,"primitive_id":pid,"capability_ref":cap,"problem_family_ref":sem["primary_family_ref"],
      "instructional_job":JOB_BY_PRIMITIVE[pid],
      "attention_target":f"Notice the mathematical structure required by {req} before executing the solution.",
      "translation_obligation":f"Translate the {req} representation back into the formal mathematics used in the reasoning route.",
      "source_semantic_data":{"declared_claims":[review["review_rationale"]],"payload":payload},
      "learner_action_expected":"Use the representation to name the next mathematical relation or check, not merely inspect the picture.",
      "misconception_or_contrast_ref":contrast_ref,
      "accessibility_text":f"Instructional mathematics representation for {q['question_id']} showing {req} from declared source data.",
      "renderer_constraints":{"must_not_infer_mathematical_content":True,"must_render_from_source_semantic_data":True,
                              "layout_constraints":list(primitive["renderer_constraints"])},
      "spec_digest":""
    }
    spec["spec_digest"]=digest(spec,"spec_digest")
    return spec

def build_representation(q,binding,sem,review,primitive_registry,page_intent_profile):
    cap=binding["canonical_capability_refs"][0]
    prim={x["primitive_id"]:x for x in primitive_registry["primitives"]}
    specs=[]
    for req in binding["representation_demands"]:
        pid=PRIMITIVE_BY_REQUIREMENT.get(req)
        if not pid or pid not in prim: fail("REPRESENTATION_REQUIREMENT_UNCOVERED",f"{q['question_id']}:{req}")
        specs.append(representation_spec(req,pid,q,sem,review,cap,prim[pid]))
    context={"surface_role":"CORE2_TRANSFER","lesson_or_transfer_ref":q["question_id"],"capability_ref":cap,
             "problem_family_refs":[sem["primary_family_ref"]],"representation_requirements":binding["representation_demands"],
             "required_pck_jobs":[]}
    return build_representation_plan(context,specs,primitive_registry,page_intent_profile)

def planned_core1_link(cap,authority,core1_plan=None):
    titles={x["capability_id"]:x["title"] for x in authority["capabilities"]}
    title=titles.get(cap,cap.removeprefix("MATH-").replace("-"," ").title())
    lesson=None
    if core1_plan and core1_plan.get("release_class")=="PRODUCTION":
        lesson=next((x for x in core1_plan.get("lessons",[]) if x["capability_ref"]==cap),None)
    if lesson:
        return {"stable_id":lesson["lesson_id"],"learner_title":lesson["learner_title"],"capability_ref":cap,
                "linkage_state":"MATERIALIZED","materialized_lesson_id":lesson["lesson_id"],"source_question_reuse":False}
    return {"stable_id":"MATH-C1-PLANNED-"+digest(cap)[:8],"learner_title":title,"capability_ref":cap,
            "linkage_state":"PLANNED_UNTIL_PCK_PROMOTED","materialized_lesson_id":None,"source_question_reuse":False}

def make_hints(fam):
    h=fam["hints"]
    return {"support_revealed_initially":False,
            "H1":{"level":"H1","job":"NOTICE_STRUCTURE","text":h["H1_NOTICE"]},
            "H2":{"level":"H2","job":"CHOOSE_METHOD_OR_REPRESENTATION","text":h["H2_METHOD"]},
            "H3":{"level":"H3","job":"FIRST_EXECUTABLE_STEP","text":h["H3_START"]}}

def make_solution(fam,review,verification_routes):
    checks=[]
    for r in verification_routes: checks.extend(copy.deepcopy(r["checks"]))
    return {"steps":copy.deepcopy(fam["solution_steps"]),"final_answer":copy.deepcopy(review["canonical_answer"]),"verification_checks":checks}

def item_notice(review):
    s=review["validity_state"]
    if s=="UNDERDETERMINED": return "This source item does not determine one unique answer. Attempt the algebra, then judge information sufficiency."
    if s=="VALID_MULTIPLE_SOLUTIONS": return "More than one mathematically valid answer exists; retain and verify every valid branch."
    if s in {"AMBIGUOUS","DATA_ERROR","REVIEW_REQUIRED"}: return f"Assessment-safety status: {s}. Do not use a miss here as ordinary negative learner evidence."
    return None

def build_plan(question_set,review_registry,review_policy,scope_bindings,authority,problem_semantics,
               verification_registry,primitive_registry,page_intent_profile,authoring_profile,core1_plan=None):
    if question_set["subject"]!="MATHEMATICS" or problem_semantics["subject"]!="MATHEMATICS": fail("SUBJECT_MISMATCH")
    reviews={x["item_ref"]:x for x in review_registry["reviews"]}
    rules={x["validity_state"]:x for x in review_policy["rules"]}
    bindings={x["item_ref"]:x for x in scope_bindings["bindings"]}
    sems={x["item_ref"]:x for x in problem_semantics["assessment_item_semantics"]}
    vrs={x["verification_route_id"]:x for x in verification_registry["routes"]}
    families=authoring_profile["families"]
    pages=[]
    for q in sorted(question_set["questions"],key=lambda x:x["source_order"]):
        qid=q["question_id"]
        if qid not in reviews or qid not in bindings or qid not in sems: fail("TRANSFER_AUTHORITY_COVERAGE_GAP",qid)
        review,bind,sem=reviews[qid],bindings[qid],sems[qid]
        if sem["primary_family_ref"] not in families: fail("GENERIC_WORKSPACE_IGNORES_RESPONSE_SHAPE",qid)
        fam=families[sem["primary_family_ref"]]
        routes=[]
        for ref in sem["verification_route_refs"]:
            if ref not in vrs: fail("VERIFICATION_ROUTE_MISSING",ref)
            routes.append(vrs[ref])
        hints=make_hints(fam)
        links=[planned_core1_link(c,authority,core1_plan) for c in bind["canonical_capability_refs"]]
        page={
          "question_ref":qid,"source_ref":q["source_provenance"]["source_digest"],"source_order":q["source_order"],
          "source_stem":q["stem"],"source_subparts":copy.deepcopy(q["subparts"]),"source_options":copy.deepcopy(q["options"]),
          "source_givens":copy.deepcopy(q["givens"]),"source_units":copy.deepcopy(q["units"]),
          "assessment_safety":{"validity_state":review["validity_state"],"diagnostic_use":review["diagnostic_use"],
                               "negative_inference_allowed":rules[review["validity_state"]]["negative_inference_allowed"],
                               "canonical_answer":copy.deepcopy(review["canonical_answer"])},
          "concept_refs":copy.deepcopy(bind["canonical_concept_refs"]),
          "capability_refs":copy.deepcopy(bind["canonical_capability_refs"]),
          "problem_family_ref":sem["primary_family_ref"],"demand_vector_ref":sem["demand_vector"]["vector_id"],
          "guide_demand_badge":copy.deepcopy(sem["guide_demand_badge"]),
          "core1_lesson_refs":links,
          "workspace_spec":{"workspace_type":sem["primary_family_ref"],"fields":copy.deepcopy(fam["workspace_fields"])},
          "hint_ladder":hints,
          "reasoning_route":copy.deepcopy(sem["reasoning_route"]),
          "solution_route":make_solution(fam,review,routes),
          "representation_plan":build_representation(q,bind,sem,review,primitive_registry,page_intent_profile),
          "attempt_policy":{"attempt_original_first":True,"support_hidden_initially":True,"item_validity_notice":item_notice(review)},
          "page_digest":""
        }
        page["page_digest"]=digest(page,"page_digest")
        pages.append(page)
    materialized=all(l["linkage_state"]=="MATERIALIZED" for p in pages for l in p["core1_lesson_refs"])
    out={"plan_id":"","schema_version":"1.0.0","subject":"MATHEMATICS",
         "release_class":"PRODUCTION_READY" if materialized else "SEMANTIC_TEST",
         "question_set_ref":question_set["question_set_id"],"question_set_digest":question_set["question_set_digest"],
         "problem_semantics_ref":problem_semantics["package_id"],"problem_semantics_digest":problem_semantics["package_digest"],
         "representation_authority_ref":primitive_registry["registry_id"],
         "core1_linkage_mode":"MATERIALIZED" if materialized else "PLANNED_UNTIL_PCK_PROMOTED",
         "pages":pages,
         "summary":{"question_count":len(pages),"attempt_first":True,"source_fidelity":True,"psychometric_claims":False,
                    "publication_ready":bool(materialized)},
         "plan_digest":""}
    out["plan_id"]="MATH-C2TP-"+digest({"q":out["question_set_digest"],"ps":out["problem_semantics_digest"],
                                       "profile":digest(authoring_profile),"core1":out["core1_linkage_mode"]})[:16]
    out["plan_digest"]=digest(out,"plan_digest")
    validate_plan(out,question_set,review_registry,review_policy,scope_bindings,authority,problem_semantics,
                  verification_registry,primitive_registry,page_intent_profile,authoring_profile,core1_plan)
    return out

def validate_plan(plan,question_set,review_registry,review_policy,scope_bindings,authority,problem_semantics,
                  verification_registry,primitive_registry,page_intent_profile,authoring_profile,core1_plan=None):
    if plan["plan_digest"]!=digest(plan,"plan_digest"): fail("TRANSFER_PLAN_DIGEST_MISMATCH")
    qby={x["question_id"]:x for x in question_set["questions"]}
    expected=[x["question_id"] for x in sorted(question_set["questions"],key=lambda x:x["source_order"])]
    refs=[x["question_ref"] for x in plan["pages"]]
    if refs!=expected: fail("MISSING_TRANSFER_QUESTION")
    reviews={x["item_ref"]:x for x in review_registry["reviews"]}
    rules={x["validity_state"]:x for x in review_policy["rules"]}
    bindings={x["item_ref"]:x for x in scope_bindings["bindings"]}
    sems={x["item_ref"]:x for x in problem_semantics["assessment_item_semantics"]}
    vr={x["verification_route_id"]:x for x in verification_registry["routes"]}
    prim_by={x["primitive_id"]:x for x in primitive_registry["primitives"]}
    for p in plan["pages"]:
        qid=p["question_ref"]; q=qby[qid]; review=reviews[qid]; bind=bindings[qid]; sem=sems[qid]
        if p["page_digest"]!=digest(p,"page_digest"): fail("TRANSFER_PAGE_DIGEST_MISMATCH",qid)
        if (p["source_ref"]!=q["source_provenance"]["source_digest"] or p["source_stem"]!=q["stem"] or
            p["source_subparts"]!=q["subparts"] or p["source_givens"]!=q["givens"] or p["source_units"]!=q["units"]):
            fail("SOURCE_SHAPE_DRIFT",qid)
        if p["source_options"]!=q["options"]: fail("SOURCE_MC_OPTIONS_MISSING",qid)
        if not p["attempt_policy"]["attempt_original_first"] or not p["attempt_policy"]["support_hidden_initially"] or p["hint_ladder"]["support_revealed_initially"]:
            fail("ATTEMPT_FIRST_BYPASSED",qid)
        hs=[p["hint_ladder"][k]["text"] for k in ("H1","H2","H3")]
        if len({norm(x) for x in hs})<3: fail("H1_DISCLOSES_H3",qid)
        sol=[norm(x) for x in p["solution_route"]["steps"]]
        if any(norm(x) in sol for x in hs): fail("HINT_EQUALS_SOLUTION",qid)
        route_text=[norm(x["mathematical_transition"]) for x in p["reasoning_route"]["steps"]]
        if set(route_text) and set(route_text).issubset(set(norm(x) for x in hs)): fail("REASONING_ROUTE_EQUALS_HINT_COPY",qid)
        if p["reasoning_route"]!=sem["reasoning_route"]: fail("REASONING_ROUTE_AUTHORITY_DRIFT",qid)
        if p["guide_demand_badge"]!=sem["guide_demand_badge"]: fail("GUIDE_BADGE_AUTHORITY_DRIFT",qid)
        if p["guide_demand_badge"].get("psychometric_claim") is not False: fail("GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC",qid)
        if p["guide_demand_badge"]["label"]=="HARD":
            steps=p["reasoning_route"]["steps"]; roles={x["role"] for x in steps}
            if len(steps)<5 or len(roles)<4: fail("HARD_BADGE_WITHOUT_DEEP_REASONING_STRUCTURE",qid)
        fam=authoring_profile["families"][sem["primary_family_ref"]]
        if p["workspace_spec"]!={"workspace_type":sem["primary_family_ref"],"fields":fam["workspace_fields"]}:
            fail("GENERIC_WORKSPACE_IGNORES_RESPONSE_SHAPE",qid)
        if not p["solution_route"]["steps"] or len(p["solution_route"]["steps"])<2: fail("SOLUTION_IS_ANSWER_ONLY",qid)
        expected_checks=[]
        for r in sem["verification_route_refs"]: expected_checks.extend(vr[r]["checks"])
        if p["solution_route"]["verification_checks"]!=expected_checks: fail("VERIFICATION_ROUTE_DRIFT",qid)
        safety=p["assessment_safety"]
        if safety["validity_state"]!=review["validity_state"] or safety["diagnostic_use"]!=review["diagnostic_use"]:
            fail("ASSESSMENT_SAFETY_POLICY_LOST",qid)
        if safety["negative_inference_allowed"]!=rules[review["validity_state"]]["negative_inference_allowed"]:
            fail("ASSESSMENT_SAFETY_POLICY_LOST",qid)
        if review["validity_state"]=="UNDERDETERMINED" and safety["negative_inference_allowed"]:
            fail("UNDERDETERMINED_POLICY_LOST",qid)
        if review["validity_state"]=="VALID_MULTIPLE_SOLUTIONS":
            ca=p["solution_route"]["final_answer"]
            if ca.get("uniqueness_status")!="MULTIPLE" or len(ca.get("accepted_answers",[]))+len(ca.get("accepted_option_labels",[]))<2:
                fail("MULTI_SOLUTION_COLLAPSED",qid)
        for link in p["core1_lesson_refs"]:
            if not link["learner_title"] or link["learner_title"]==link["stable_id"]: fail("OPAQUE_CORE1_LINK_ONLY",qid)
            if link["source_question_reuse"]: fail("ORIGINAL_TRANSFER_LEAKED_INTO_CORE1_WORKED_EXAMPLE",qid)
        rp=p["representation_plan"]
        if rp["surface_role"]!="CORE2_TRANSFER" or rp["lesson_or_transfer_ref"]!=qid: fail("REPRESENTATION_PLAN_DRIFT",qid)
        if sorted(rp["required_representation_refs"])!=sorted(bind["representation_demands"]): fail("REPRESENTATION_PLAN_DRIFT",qid)
        for s in rp["representations"]:
            if s["primitive_id"] not in prim_by: fail("REPRESENTATION_PLAN_DRIFT",qid)
    if plan["summary"]["psychometric_claims"] is not False: fail("GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC")
    any_planned=any(l["linkage_state"]!="MATERIALIZED" for p in plan["pages"] for l in p["core1_lesson_refs"])
    if any_planned and (plan["release_class"]!="SEMANTIC_TEST" or plan["summary"]["publication_ready"]):
        fail("UNPROMOTED_CORE1_LINK_PUBLISHED")
    return True

def main():
    ap=argparse.ArgumentParser()
    for k in ["questions","review-registry","review-policy","scope-bindings","authority","problem-semantics",
              "verification-registry","primitive-registry","page-intent-profile","authoring-profile","out"]:
        ap.add_argument("--"+k,required=True)
    args=ap.parse_args()
    out=build_plan(load(args.questions),load(args.review_registry),load(args.review_policy),load(args.scope_bindings),
                   load(args.authority),load(args.problem_semantics),load(args.verification_registry),
                   load(args.primitive_registry),load(args.page_intent_profile),load(args.authoring_profile))
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
if __name__=="__main__": main()
