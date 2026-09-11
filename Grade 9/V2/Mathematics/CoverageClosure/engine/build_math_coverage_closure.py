#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path

DIMS=["acquisition","independent_reconstruction","delayed_retention","near_transfer","far_transfer","mixed_discrimination","fluency","timed_performance"]
FUTURE_DIMS={"delayed_retention","near_transfer","far_transfer","mixed_discrimination","fluency","timed_performance"}

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(x,omit=None):
    y=copy.deepcopy(x)
    if omit and isinstance(y,dict): y.pop(omit,None)
    return hashlib.sha256(canon(y).encode("utf-8")).hexdigest()
def fail(code,detail=""): raise ValueError(f"{code}:{detail}" if detail else code)
def unique(xs): return list(dict.fromkeys(xs))

def qmap(question_set): return {q["question_id"]:q for q in question_set["questions"]}
def page_map(core2): return {p["question_ref"]:p for p in core2["pages"]}
def plan_map(study_model): return {p["capability_ref"]:p for p in study_model["capability_plans"]}
def state_map(snapshot): return {s["capability_ref"]:s for s in snapshot["capability_states"]}

def problem_obligation_ref(cap,family):
    return "MATH-C1-PROBLEM-OBL-"+digest([cap,family])[:12].upper()

def build_coverage_matrix(question_set,scope_bindings,study_model,core2_plan):
    questions=qmap(question_set); pages=page_map(core2_plan); treatments=plan_map(study_model)
    rows=[]
    for b in scope_bindings["bindings"]:
        qid=b["question_ref"]
        if qid not in questions: fail("EVIDENCE_EVENT_WITHOUT_SOURCE_QUESTION",qid)
        if qid not in pages: fail("QUESTION_WITHOUT_CORE2_TRANSFER",qid)
        q=questions[qid]; page=pages[qid]
        if page["source_ref"]!=q["source_provenance"]["source_digest"]: fail("CORE2_PAGE_WITHOUT_SOURCE_QUESTION_CUSTODY",qid)
        if page["problem_family_ref"] not in b["problem_family_refs"]: fail("REASONING_ROUTE_WITHOUT_PROBLEM_FAMILY_AUTHORITY",b["item_ref"])
        rr=page["reasoning_route"]
        if rr.get("primary_family_ref")!=page["problem_family_ref"] or not rr.get("route_id"): fail("REASONING_ROUTE_WITHOUT_PROBLEM_FAMILY_AUTHORITY",b["item_ref"])
        direct_caps=b["canonical_capability_refs"]
        all_caps=unique(direct_caps+b["prerequisite_capability_refs"])
        missing_treatment=[c for c in all_caps if c not in treatments]
        if missing_treatment: fail("CAPABILITY_WITHOUT_INSTRUCTIONAL_TREATMENT",",".join(missing_treatment))
        links=[x for x in page["core1_lesson_refs"] if x["capability_ref"] in direct_caps]
        missing_core=[c for c in direct_caps if c not in {x["capability_ref"] for x in links}]
        if missing_core: fail("QUESTION_WITHOUT_CORE1_COVERAGE",f"{b['item_ref']}:{','.join(missing_core)}")
        if any(not x.get("learner_title") for x in links): fail("QUESTION_WITHOUT_CORE1_COVERAGE",b["item_ref"])
        treatment_rows=[{"capability_ref":c,"treatment":treatments[c]["treatment"]} for c in all_caps]
        problem_refs=[]
        for c in all_caps:
            fams=b["problem_family_refs"] or treatments[c].get("problem_family_refs",[])
            for fam in fams[:1] or ["MATH-PF-UNSPECIFIED"]:
                problem_refs.append(problem_obligation_ref(c,fam))
        row={
          "item_ref":b["item_ref"],"question_ref":qid,"part_ref":b["part_ref"],"mapping_state":b["mapping_state"],
          "topic_refs":copy.deepcopy(b["declared_topic_refs"]),"concept_refs":copy.deepcopy(b["canonical_concept_refs"]),
          "capability_refs":copy.deepcopy(direct_caps),"prerequisite_refs":copy.deepcopy(b["prerequisite_capability_refs"]),
          "problem_family_refs":copy.deepcopy(b["problem_family_refs"]),"core1_links":copy.deepcopy(links),
          "core1_problem_authoring_obligation_refs":sorted(set(problem_refs)),
          "core2_page_ref":qid,"core2_page_digest":page["page_digest"],"source_question_digest":q["source_provenance"]["source_digest"],
          "hint_levels":["H1","H2","H3"],"reasoning_route_ref":rr["route_id"],
          "verification_obligation_refs":copy.deepcopy(b["verification_obligations"]),"treatment_decisions":treatment_rows,
          "evidence_contract_ref":"MATH-TRANSFER-EVIDENCE-v1","longitudinal_owner_refs":copy.deepcopy(all_caps)
        }
        rows.append(row)
    matrix={"matrix_id":"","schema_version":"1.0.0","subject":"MATHEMATICS","question_set_ref":question_set["question_set_id"],
            "scope_binding_registry_ref":scope_bindings["binding_registry_id"],"core2_plan_ref":core2_plan["plan_id"],"rows":rows,"matrix_digest":""}
    matrix["matrix_id"]="MATH-COV-"+digest(rows)[:16]
    matrix["matrix_digest"]=digest(matrix,"matrix_digest")
    return matrix

def derive_evidence_state(raw,policy):
    support=raw["support_consumed"]; correct=raw["response_correctness"]; reasoning=raw["reasoning_validity"]
    if correct=="NO_RESPONSE": return "NO_ATTEMPT"
    if support=="SOLUTION": return "SOLUTION_EXPOSED"
    if correct=="CORRECT" and reasoning=="VALID": return policy["support_semantics"][support]["success_state"]
    if correct=="CORRECT": return "CORRECT_ANSWER_INVALID_REASONING"
    return "INCORRECT_AFTER_SUPPORT"

def verification_state(raw):
    return {"SUCCESS":"VERIFICATION_SUCCESS","FAILURE":"VERIFICATION_FAILURE","NOT_ATTEMPTED":"VERIFICATION_NOT_ATTEMPTED","NOT_APPLICABLE":"VERIFICATION_NOT_APPLICABLE"}[raw["verification"]]

def build_evidence_events(outcomes,core2_plan,policy):
    pages=page_map(core2_plan); events=[]
    for raw in outcomes.get("outcomes",[]):
        qid=raw["question_ref"]
        if qid not in pages: fail("EVIDENCE_EVENT_WITHOUT_SOURCE_QUESTION",qid)
        p=pages[qid]; state=derive_evidence_state(raw,policy)
        mastery=(state=="INDEPENDENT_SUCCESS" and p["assessment_safety"]["validity_state"] not in {"UNDERDETERMINED","AMBIGUOUS","DATA_ERROR","REVIEW_REQUIRED"})
        event={
          "event_id":"","schema_version":"1.0.0","subject":"MATHEMATICS","question_ref":qid,"core2_page_digest":p["page_digest"],
          "source_question_digest":p["source_ref"],"support_consumed":raw["support_consumed"],"evidence_state":state,
          "verification_state":verification_state(raw),"response_correctness":raw["response_correctness"],"reasoning_validity":raw["reasoning_validity"],
          "capability_refs":copy.deepcopy(p["capability_refs"]),"assessment_validity_state":p["assessment_safety"]["validity_state"],
          "diagnostic_use":p["assessment_safety"]["diagnostic_use"],"negative_inference_allowed":p["assessment_safety"]["negative_inference_allowed"],
          "mastery_evidence_allowed":mastery,"event_digest":""
        }
        event["event_id"]="MATH-TEV-"+digest([outcomes.get("fixture_id"),raw])[:16]
        event["event_digest"]=digest(event,"event_digest")
        events.append(event)
    return events

def update_semantics(event,prior):
    ev=event["evidence_state"]
    if ev=="INDEPENDENT_SUCCESS": return "READY","POSITIVE_INDEPENDENT",1,0,0,"Independent correct reasoning creates current independent positive evidence."
    if ev=="H1_SUCCESS": return ("READY" if prior=="READY" else "DEVELOPING"),"POSITIVE_ASSISTED_H1",0,1,0,"Success after H1 is assisted positive evidence, not independent mastery evidence."
    if ev=="H2_SUCCESS": return ("READY" if prior=="READY" else "DEVELOPING"),"POSITIVE_ASSISTED_H2",0,1,0,"Success after H2 is assisted positive evidence and preserves the support depth."
    if ev=="H3_SUCCESS": return ("READY" if prior=="READY" else "DEVELOPING"),"POSITIVE_ASSISTED_H3",0,1,0,"Success after H3 is assisted execution evidence and cannot be counted as independent success."
    if ev=="CORRECT_ANSWER_INVALID_REASONING": return ("READY" if prior=="READY" else "DEVELOPING"),"LIMITED_POSITIVE_INVALID_REASONING",0,1,0,"A correct final answer with invalid reasoning is limited evidence and cannot establish full capability success."
    if ev=="INCORRECT_AFTER_SUPPORT":
        if event["negative_inference_allowed"]: return "DEVELOPING","NEGATIVE_ASSISTED",0,0,1,"Incorrect supported work creates negative evidence only because this source item permits negative inference."
        return prior,"NON_DIAGNOSTIC",0,0,0,"Assessment-safety policy forbids negative inference from this item; learner readiness is unchanged."
    if ev=="SOLUTION_EXPOSED": return prior,"NON_DIAGNOSTIC",0,0,0,"Solution exposure is not learner mastery evidence and does not promote readiness."
    return prior,"NO_EVIDENCE",0,0,0,"No attempt creates no learner readiness claim."

def build_state_updates(events,prior_snapshot):
    sm=state_map(prior_snapshot); out=[]
    for e in events:
        rows=[]
        for cap in e["capability_refs"]:
            prior=sm.get(cap,{"readiness":"UNKNOWN"})["readiness"]
            result,klass,ind,assist,neg,rationale=update_semantics(e,prior)
            rows.append({"capability_ref":cap,"prior_readiness":prior,"resulting_readiness":result,"evidence_class":klass,
                         "independent_success_increment":ind,"assisted_success_increment":assist,"negative_evidence_increment":neg,
                         "state_changed":result!=prior,"rationale":rationale})
        vs=e["verification_state"]
        if vs=="VERIFICATION_SUCCESS": ve={"state":vs,"evidence_class":"POSITIVE","independent":e["support_consumed"]=="NONE"}
        elif vs=="VERIFICATION_FAILURE" and e["negative_inference_allowed"]: ve={"state":vs,"evidence_class":"NEGATIVE","independent":e["support_consumed"]=="NONE"}
        else: ve={"state":vs,"evidence_class":"NONE","independent":False}
        u={"update_id":"","schema_version":"1.0.0","subject":"MATHEMATICS","event_ref":e["event_id"],"prior_snapshot_ref":prior_snapshot["snapshot_id"],
           "capability_updates":rows,"verification_evidence":ve,"update_digest":""}
        u["update_id"]="MATH-LSU-"+digest([e["event_digest"],prior_snapshot["snapshot_digest"]])[:16]
        u["update_digest"]=digest(u,"update_digest"); out.append(u)
    return out

def longitudinal_result(event,dim,prior):
    ev=event["evidence_state"]
    if dim in FUTURE_DIMS: return "OPEN_FUTURE_EVIDENCE",False
    if dim=="acquisition":
        if ev=="INDEPENDENT_SUCCESS": return "CURRENT_EVIDENCE",True
        if ev in {"H1_SUCCESS","H2_SUCCESS","H3_SUCCESS","CORRECT_ANSWER_INVALID_REASONING"}: return "PARTIAL_CURRENT_EVIDENCE",False
        return prior,False
    if dim=="independent_reconstruction":
        if ev=="INDEPENDENT_SUCCESS": return "CURRENT_EVIDENCE",True
        if ev in {"H1_SUCCESS","H2_SUCCESS","H3_SUCCESS"}: return "PARTIAL_CURRENT_EVIDENCE",False
        return prior,False
    return prior,False

def build_longitudinal_updates(events,study_model):
    pm=plan_map(study_model); out=[]
    for e in events:
        caps=[]
        for cap in e["capability_refs"]:
            if cap not in pm: fail("LONGITUDINAL_OBLIGATION_DISAPPEARS",cap)
            prior=pm[cap]["future_evidence_obligations"]
            if {x["dimension"] for x in prior}!=set(DIMS): fail("LONGITUDINAL_OBLIGATION_DISAPPEARS",cap)
            dims=[]
            for x in prior:
                result,closed=longitudinal_result(e,x["dimension"],x["status"])
                dims.append({"dimension":x["dimension"],"prior_status":x["status"],"resulting_status":result,"evidence_needed":x["evidence_needed"],
                             "owner_capability_ref":cap,"closed_by_event":closed})
            caps.append({"capability_ref":cap,"dimensions":dims})
        u={"longitudinal_update_id":"","schema_version":"1.0.0","subject":"MATHEMATICS","event_ref":e["event_id"],"capability_obligations":caps,
           "invariant":"CURRENT_SUCCESS_DOES_NOT_CLOSE_DELAYED_OR_TRANSFER_OBLIGATIONS","update_digest":""}
        u["longitudinal_update_id"]="MATH-LONG-"+digest([e["event_digest"],study_model["study_model_digest"]])[:16]
        u["update_digest"]=digest(u,"update_digest"); out.append(u)
    return out

def build_publication_closure(matrix,core2_plan,events,state_updates,long_updates):
    gaps={
      "question_without_core1_coverage":[],"question_without_core2_transfer":[],"capability_without_instructional_treatment":[],
      "core2_page_without_source_custody":[],"reasoning_route_without_problem_family_authority":[],
      "transfer_event_without_learner_state_update_semantics":[],"future_obligation_without_longitudinal_owner":[]
    }
    update_events={u["event_ref"] for u in state_updates}; long_events={u["event_ref"] for u in long_updates}
    for e in events:
        if e["event_id"] not in update_events: gaps["transfer_event_without_learner_state_update_semantics"].append(e["event_id"])
        if e["event_id"] not in long_events: gaps["future_obligation_without_longitudinal_owner"].append(e["event_id"])
    planned=any(l["linkage_state"]!="MATERIALIZED" for r in matrix["rows"] for l in r["core1_links"])
    blocked=planned or not core2_plan["summary"]["publication_ready"]
    closure={"closure_id":"","schema_version":"1.0.0","subject":"MATHEMATICS","matrix_ref":matrix["matrix_id"],"matrix_digest":matrix["matrix_digest"],
             "semantic_closure_status":"PASS","publication_closure_status":"BLOCKED_UPSTREAM_PCK_PROMOTION" if blocked else "PASS",
             "publication_blockers":["M-G/#242 real human PCK promotion is required before Core1 materialization"] if blocked else [],
             "gap_report":gaps,"closure_digest":""}
    closure["closure_id"]="MATH-PUBC-"+digest([matrix["matrix_digest"],blocked])[:16]
    closure["closure_digest"]=digest(closure,"closure_digest")
    return closure

def validate_package(pkg,question_set,scope_bindings,study_model,prior_snapshot,core2_plan,policy):
    if pkg["package_digest"]!=digest(pkg,"package_digest"): fail("COVERAGE_PACKAGE_DIGEST_MISMATCH")
    matrix=pkg["assessment_coverage_matrix"]
    if matrix["matrix_digest"]!=digest(matrix,"matrix_digest"): fail("COVERAGE_MATRIX_DIGEST_MISMATCH")
    expected={b["item_ref"] for b in scope_bindings["bindings"]}; actual={r["item_ref"] for r in matrix["rows"]}
    if expected!=actual: fail("ASSESSMENT_COVERAGE_ROW_GAP")
    pages=page_map(core2_plan); qs=qmap(question_set); treatments=plan_map(study_model)
    for r in matrix["rows"]:
        if not r["core1_links"]: fail("QUESTION_WITHOUT_CORE1_COVERAGE",r["item_ref"])
        if r["question_ref"] not in pages: fail("QUESTION_WITHOUT_CORE2_TRANSFER",r["question_ref"])
        if r["core2_page_digest"]!=pages[r["question_ref"]]["page_digest"]: fail("QUESTION_WITHOUT_CORE2_TRANSFER",r["question_ref"])
        if r["source_question_digest"]!=qs[r["question_ref"]]["source_provenance"]["source_digest"]: fail("CORE2_PAGE_WITHOUT_SOURCE_QUESTION_CUSTODY",r["question_ref"])
        if any(c not in treatments for c in r["capability_refs"]+r["prerequisite_refs"]): fail("CAPABILITY_WITHOUT_INSTRUCTIONAL_TREATMENT",r["item_ref"])
        if not r["reasoning_route_ref"] or not r["problem_family_refs"]: fail("REASONING_ROUTE_WITHOUT_PROBLEM_FAMILY_AUTHORITY",r["item_ref"])
        if not r["core1_problem_authoring_obligation_refs"]: fail("QUESTION_WITHOUT_CORE1_COVERAGE",r["item_ref"])
        if not r["longitudinal_owner_refs"]: fail("LONGITUDINAL_OBLIGATION_DISAPPEARS",r["item_ref"])
    closure=pkg["publication_coverage_closure"]
    if closure["closure_digest"]!=digest(closure,"closure_digest"): fail("PUBLICATION_CLOSURE_DIGEST_MISMATCH")
    for e in pkg["transfer_evidence_events"]:
        if e["event_digest"]!=digest(e,"event_digest"): fail("TRANSFER_EVIDENCE_DIGEST_MISMATCH",e["event_id"])
    for u in pkg["learner_state_updates"]:
        if u["update_digest"]!=digest(u,"update_digest"): fail("LEARNER_STATE_UPDATE_DIGEST_MISMATCH",u["event_ref"])
    for u in pkg["longitudinal_updates"]:
        if u["update_digest"]!=digest(u,"update_digest"): fail("LONGITUDINAL_UPDATE_DIGEST_MISMATCH",u["event_ref"])
    events={e["event_id"]:e for e in pkg["transfer_evidence_events"]}; updates={u["event_ref"]:u for u in pkg["learner_state_updates"]}; longs={u["event_ref"]:u for u in pkg["longitudinal_updates"]}
    for e in events.values():
        q=e["question_ref"]
        if q not in pages or e["core2_page_digest"]!=pages[q]["page_digest"] or e["source_question_digest"]!=pages[q]["source_ref"]: fail("EVIDENCE_EVENT_WITHOUT_SOURCE_QUESTION",e["event_id"])
        if e["event_id"] not in updates: fail("TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS",e["event_id"])
        if e["event_id"] not in longs: fail("LONGITUDINAL_OBLIGATION_DISAPPEARS",e["event_id"])
        u=updates[e["event_id"]]
        if e["evidence_state"]=="H3_SUCCESS" and any(x["independent_success_increment"] for x in u["capability_updates"]): fail("H3_SUCCESS_RECORDED_AS_INDEPENDENT_SUCCESS",e["event_id"])
        if e["evidence_state"]=="SOLUTION_EXPOSED":
            if e["mastery_evidence_allowed"] or any(x["resulting_readiness"]!=x["prior_readiness"] for x in u["capability_updates"]): fail("SOLUTION_EXPOSED_RECORDED_AS_MASTERY",e["event_id"])
        if e["assessment_validity_state"]=="UNDERDETERMINED" and not e["negative_inference_allowed"]:
            if any(x["negative_evidence_increment"] for x in u["capability_updates"]): fail("ASSESSMENT_SAFETY_POLICY_LOST",e["event_id"])
        l=longs[e["event_id"]]
        for cap in l["capability_obligations"]:
            dims={x["dimension"]:x for x in cap["dimensions"]}
            if set(dims)!=set(DIMS): fail("LONGITUDINAL_OBLIGATION_DISAPPEARS",cap["capability_ref"])
            for d in FUTURE_DIMS:
                if dims[d]["resulting_status"]!="OPEN_FUTURE_EVIDENCE" or dims[d]["closed_by_event"]: fail("CURRENT_SUCCESS_ERASES_FUTURE_RETRIEVAL",f"{e['event_id']}:{d}")
            if any(not x["owner_capability_ref"] for x in cap["dimensions"]): fail("LONGITUDINAL_OBLIGATION_DISAPPEARS",cap["capability_ref"])
    if any(closure["gap_report"][k] for k in closure["gap_report"]): fail("PUBLICATION_COVERAGE_GAP")
    planned=any(l["linkage_state"]!="MATERIALIZED" for r in matrix["rows"] for l in r["core1_links"])
    if planned and closure["publication_closure_status"]!="BLOCKED_UPSTREAM_PCK_PROMOTION": fail("UNPROMOTED_CORE1_LINK_PUBLISHED")
    return True

def build_package(question_set,scope_bindings,study_model,prior_snapshot,core2_plan,outcomes,policy):
    matrix=build_coverage_matrix(question_set,scope_bindings,study_model,core2_plan)
    events=build_evidence_events(outcomes,core2_plan,policy)
    state_updates=build_state_updates(events,prior_snapshot)
    long_updates=build_longitudinal_updates(events,study_model)
    closure=build_publication_closure(matrix,core2_plan,events,state_updates,long_updates)
    pkg={"package_id":"","schema_version":"1.0.0","subject":"MATHEMATICS","assessment_coverage_matrix":matrix,
         "publication_coverage_closure":closure,"transfer_evidence_events":events,"learner_state_updates":state_updates,
         "longitudinal_updates":long_updates,"package_digest":""}
    pkg["package_id"]="MATH-MJ-"+digest([matrix["matrix_digest"],[e["event_digest"] for e in events]])[:16]
    pkg["package_digest"]=digest(pkg,"package_digest")
    validate_package(pkg,question_set,scope_bindings,study_model,prior_snapshot,core2_plan,policy)
    return pkg

def main():
    ap=argparse.ArgumentParser()
    for x in ["questions","scope-bindings","study-model","prior-snapshot","core2-plan","outcomes","policy","out"]: ap.add_argument("--"+x,required=True)
    a=ap.parse_args(); result=build_package(load(a.questions),load(a.scope_bindings),load(a.study_model),load(a.prior_snapshot),load(a.core2_plan),load(a.outcomes),load(a.policy))
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
if __name__=="__main__": main()
