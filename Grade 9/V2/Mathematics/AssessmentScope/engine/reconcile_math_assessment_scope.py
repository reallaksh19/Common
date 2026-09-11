#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import Counter
from pathlib import Path

D=Path(__file__).resolve().parents[1]; MATH=D.parent
sys.path[:0]=[str(MATH/"AssessmentIntake"/"engine"),str(MATH/"AssessmentReview"/"engine")]
from build_math_assessment_intake import validate_question_set, validate_topic_scope
from review_math_assessment import build_review

STATES={"MAPPED","PARTIAL_SCOPE_MATCH","OUTSIDE_DECLARED_SCOPE","UNMAPPED"}
BAD={"attempt","attempts","attempt_set","attempt_interpretation","learner_state","learner_diagnosis","diagnosis","misconception","learner_evidence","observed_answer","hint_level","support_state"}

def cb(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def dg(x): return hashlib.sha256(cb(x)).hexdigest()
def dwo(x,k):
    y=copy.deepcopy(x); y.pop(k,None); return dg(y)
digest_without_field=dwo
def fail(c,d=""): raise ValueError(f"{c}: {d}" if d else c)
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

def nolearner(x,path="root"):
    if isinstance(x,dict):
        for k,v in x.items():
            if k.lower() in BAD: fail("SCOPE_RESOLUTION_CONSUMES_LEARNER_DATA",f"{path}.{k}")
            nolearner(v,f"{path}.{k}")
    elif isinstance(x,list):
        for i,v in enumerate(x): nolearner(v,f"{path}[{i}]")

def idx(rows,key,code):
    out={}
    for r in rows:
        if r[key] in out: fail(code,r[key])
        out[r[key]]=r
    return out

def authority_maps(a):
    nolearner(a)
    if a["authority_digest"]!=dwo(a,"authority_digest"): fail("MATH_SCOPE_AUTHORITY_DIGEST_MISMATCH")
    if a["subject"]!="MATHEMATICS" or a["authority_class"]!="MATH_ASSESSMENT_SCOPE_AUTHORITY": fail("MATH_SCOPE_AUTHORITY_CLASS_MISMATCH")
    need={"LEARNER_STATE","DIAGNOSIS","REASONING_ROUTE_SEMANTICS","DEMAND_DIFFICULTY","TEACHING_CHOREOGRAPHY","HINTS","SOLUTIONS"}
    if not need<=set(a["does_not_own"]): fail("MATH_SCOPE_AUTHORITY_BOUNDARY_MISSING")
    cs=idx(a["concepts"],"concept_id","DUPLICATE_SCOPE_CONCEPT_ID"); caps=idx(a["capabilities"],"capability_id","DUPLICATE_SCOPE_CAPABILITY_ID"); fam=idx(a["problem_families"],"problem_family_id","DUPLICATE_SCOPE_PROBLEM_FAMILY_ID")
    for c in caps.values():
        if any(x not in cs for x in c["concept_refs"]): fail("UNKNOWN_SCOPE_CONCEPT_REF",c["capability_id"])
        if any(x not in caps for x in c["prerequisite_capability_refs"]): fail("UNKNOWN_PREREQUISITE_CAPABILITY_REF",c["capability_id"])
    seen={}
    def visit(x):
        if seen.get(x)==1: fail("PREREQUISITE_CYCLE",x)
        if seen.get(x)==2:return
        seen[x]=1
        for p in caps[x]["prerequisite_capability_refs"]: visit(p)
        seen[x]=2
    for x in caps: visit(x)
    if any(f["semantic_owner_phase"]!="M-D" or f["identity_status"]!="BOUND_IDENTITY" for f in fam.values()): fail("PROBLEM_FAMILY_SEMANTICS_PREMATURELY_OWNED")
    return cs,caps,fam,set(a["representation_identities"]),set(a["verification_obligation_identities"]),set(a["reasoning_role_expectations"])

def topic_ids(s):
    allids=set(); subs=set()
    for t in s["topics"]:
        allids.add(t["topic_id"])
        for u in t["subtopics"]: allids.add(u["subtopic_id"]); subs.add(u["subtopic_id"])
    return allids,subs

def closure(direct,caps):
    direct=set(direct); out=set(); stack=[p for x in direct for p in caps[x]["prerequisite_capability_refs"]]
    while stack:
        x=stack.pop()
        if x in direct or x in out: continue
        out.add(x); stack+=caps[x]["prerequisite_capability_refs"]
    return sorted(out)

def relation(direct,caps,declared):
    refs={t for x in direct for t in caps[x]["declared_topic_refs"]}
    return "CROSS_CUTTING" if not refs else ("WITHIN_DECLARED_SCOPE" if refs&declared else "OUTSIDE_DECLARED_SCOPE")

def validate_bindings(b,q,s,a,maps,review):
    cs,caps,fam,reps,ver,roles=maps; declared,_=topic_ids(s)
    if b["binding_registry_digest"]!=dwo(b,"binding_registry_digest"): fail("QUESTION_SCOPE_BINDING_REGISTRY_DIGEST_MISMATCH")
    if (b["question_set_ref"],b["declared_topic_scope_ref"],b["authority_ref"],b["authority_digest"])!=(q["question_set_id"],s["declared_topic_scope_id"],a["authority_id"],a["authority_digest"]): fail("QUESTION_SCOPE_BINDING_AUTHORITY_MISMATCH")
    nolearner(b)
    rv={x["item_ref"]:x for x in review["item_reviews"]}; rows=b["bindings"]; refs=[x["item_ref"] for x in rows]
    if len(refs)!=len(set(refs)): fail("QUESTION_WITHOUT_EXPLICIT_MAPPING_STATE","duplicate")
    if set(refs)!=set(rv): fail("QUESTION_DROPPED_DURING_SCOPE_DERIVATION",f"missing={sorted(set(rv)-set(refs))}, extra={sorted(set(refs)-set(rv))}")
    for r in rows:
        it=r["item_ref"]; z=rv[it]
        if (r["question_ref"],r["part_ref"])!=(z["question_ref"],z["part_ref"]): fail("QUESTION_SCOPE_BINDING_SOURCE_DRIFT",it)
        st=r.get("mapping_state")
        if st not in STATES: fail("QUESTION_WITHOUT_EXPLICIT_MAPPING_STATE",it)
        checks=[(r["declared_topic_refs"],declared,"QUESTION_EVIDENCE_SILENTLY_OVERRIDES_DECLARED_BOUNDARY"),(r["canonical_concept_refs"],set(cs),"UNKNOWN_SCOPE_CONCEPT_REF"),(r["canonical_capability_refs"],set(caps),"UNKNOWN_SCOPE_CAPABILITY_REF"),(r["prerequisite_capability_refs"],set(caps),"UNKNOWN_PREREQUISITE_CAPABILITY_REF"),(r["problem_family_refs"],set(fam),"UNKNOWN_SCOPE_PROBLEM_FAMILY_REF"),(r["representation_demands"],reps,"UNKNOWN_REPRESENTATION_REF"),(r["verification_obligations"],ver,"UNKNOWN_VERIFICATION_OBLIGATION_REF"),(r["reasoning_role_expectations"],roles,"UNKNOWN_REASONING_ROLE_EXPECTATION")]
        for values,allowed,code in checks:
            if any(x not in allowed for x in values): fail(code,it)
        if st=="UNMAPPED":
            if any(r[k] for k in ["canonical_concept_refs","canonical_capability_refs","prerequisite_capability_refs","problem_family_refs"]): fail("UNMAPPED_QUESTION_HAS_INVENTED_SEMANTICS",it)
            continue
        if not all(r[k] for k in ["canonical_concept_refs","canonical_capability_refs","problem_family_refs","verification_obligations","reasoning_role_expectations"]): fail("QUESTION_WITHOUT_EXPLICIT_MAPPING_STATE",f"{it}:incomplete")
        if closure(r["canonical_capability_refs"],caps)!=sorted(r["prerequisite_capability_refs"]): fail("PREREQUISITE_INFERRED_BUT_NOT_RECORDED",it)
        rel=relation(r["canonical_capability_refs"],caps,declared)
        if rel=="OUTSIDE_DECLARED_SCOPE" and st in {"MAPPED","PARTIAL_SCOPE_MATCH"}: fail("TOPIC_LIST_SILENTLY_OVERRIDES_QUESTION_EVIDENCE",it)
        if st=="OUTSIDE_DECLARED_SCOPE" and (r["declared_topic_refs"] or rel!="OUTSIDE_DECLARED_SCOPE"): fail("QUESTION_EVIDENCE_SILENTLY_OVERRIDES_DECLARED_BOUNDARY",it)
    return rows

def finding(code,item=None,topic=None,cap=None,detail="",severity="WARNING"):
    return {"code":code,"severity":severity,"item_ref":item,"declared_topic_ref":topic,"capability_ref":cap,"detail":detail}

def reconcile(q,s,reg,policy,a,b):
    validate_question_set(q); validate_topic_scope(s)
    if q["subject"]!="MATHEMATICS" or s["subject"]!="MATHEMATICS" or q["grade"]!=s["grade"]: fail("ASSESSMENT_SCOPE_IDENTITY_MISMATCH")
    maps=authority_maps(a); cs,caps,fam,reps,ver,roles=maps; declared,subs=topic_ids(s)
    review=build_review(q,reg,policy,"MATH-ASSESSMENT-REVIEW-FOR-MC"); rv={x["item_ref"]:x for x in review["item_reviews"]}
    rows=validate_bindings(b,q,s,a,maps,review); findings=[]; undeclared={}; used=set()
    for r in rows:
        it=r["item_ref"]; st=r["mapping_state"]; used|=set(r["declared_topic_refs"])&subs
        if st=="OUTSIDE_DECLARED_SCOPE": findings.append(finding("QUESTION_OUTSIDE_DECLARED_SCOPE",it,detail="Question mathematics is preserved but lies outside the supplied declared-topic boundary."))
        elif st=="PARTIAL_SCOPE_MATCH": findings.append(finding("PARTIAL_SCOPE_MATCH",it,detail="Only a broader/partial declared-topic match is available."))
        elif st=="UNMAPPED": findings.append(finding("UNMAPPED_QUESTION",it,detail="Repository authority is insufficient; no semantics were invented.",severity="BLOCKING"))
        u=[]
        for p in r["prerequisite_capability_refs"]:
            tr=set(caps[p]["declared_topic_refs"])
            if tr and not tr&declared:
                u.append(p); findings.append(finding("QUESTION_MAPS_TO_UNDECLARED_PREREQUISITE",it,cap=p,detail=f"Prerequisite {p} is outside DeclaredTopicScope."))
        undeclared[it]=sorted(u)
    for t in sorted(subs-used): findings.append(finding("DECLARED_TOPIC_NOT_ASSESSED",topic=t,detail="Declared subtopic is not directly assessed by any mapped source item.",severity="INFO"))
    findings.sort(key=lambda x:(x["code"],x["item_ref"] or "",x["declared_topic_ref"] or "",x["capability_ref"] or ""))
    for i,f in enumerate(findings,1): f["finding_id"]=f"MC-F{i:03d}"
    frefs={}
    for f in findings:
        if f["item_ref"]: frefs.setdefault(f["item_ref"],[]).append(f["finding_id"])
    cov=[]; pre=[]
    for r in rows:
        z=rv[r["item_ref"]]
        cov.append({"item_ref":r["item_ref"],"question_ref":r["question_ref"],"part_ref":r["part_ref"],"source_question_digest":z["source_question_digest"],"validity_state":z["validity_state"],"diagnostic_use":z["diagnostic_use"],"mapping_state":r["mapping_state"],"declared_topic_refs":sorted(r["declared_topic_refs"]),"canonical_concept_refs":sorted(r["canonical_concept_refs"]),"canonical_capability_refs":sorted(r["canonical_capability_refs"]),"prerequisite_capability_refs":sorted(r["prerequisite_capability_refs"]),"problem_family_refs":sorted(r["problem_family_refs"]),"representation_demands":sorted(r["representation_demands"]),"verification_obligations":sorted(r["verification_obligations"]),"reasoning_role_expectations":r["reasoning_role_expectations"],"finding_refs":sorted(frefs.get(r["item_ref"],[]))})
        pre.append({"item_ref":r["item_ref"],"direct_capability_refs":sorted(r["canonical_capability_refs"]),"prerequisite_capability_refs":sorted(r["prerequisite_capability_refs"]),"undeclared_prerequisite_refs":undeclared[r["item_ref"]]})
    counts=dict(sorted(Counter(x["mapping_state"] for x in cov).items()))
    def union(k): return sorted({v for r in cov for v in r[k]})
    model={"scope_model_id":"MATH-G9-MIXED-PT2-ASSESSMENT-SCOPE-v1","schema_version":"1.0.0","subject":"MATHEMATICS","question_set_ref":q["question_set_id"],"declared_topic_scope_ref":s["declared_topic_scope_id"],"authority_ref":a["authority_id"],"assessment_review_bundle_ref":review["review_bundle_id"],"binding_registry_ref":b["binding_registry_id"],"attempt_data_consumed":False,"assessed_declared_topic_refs":union("declared_topic_refs"),"assessed_concept_refs":union("canonical_concept_refs"),"assessed_capability_refs":union("canonical_capability_refs"),"required_prerequisite_capability_refs":union("prerequisite_capability_refs"),"problem_family_refs":union("problem_family_refs"),"representation_demands":union("representation_demands"),"verification_obligations":union("verification_obligations"),"reasoning_role_expectations":union("reasoning_role_expectations"),"mapping_state_counts":counts,"scope_model_digest":""}; model["scope_model_digest"]=dwo(model,"scope_model_digest")
    coverage={"coverage_matrix_id":"MATH-G9-MIXED-PT2-COVERAGE-v1","schema_version":"1.0.0","subject":"MATHEMATICS","question_set_ref":q["question_set_id"],"scope_model_ref":model["scope_model_id"],"rows":cov,"coverage_complete":len(cov)==len(review["item_reviews"]),"matrix_digest":""}
    if not coverage["coverage_complete"]: fail("QUESTION_DROPPED_DURING_SCOPE_DERIVATION")
    coverage["matrix_digest"]=dwo(coverage,"matrix_digest")
    prereq={"prerequisite_closure_id":"MATH-G9-MIXED-PT2-PREREQUISITES-v1","schema_version":"1.0.0","subject":"MATHEMATICS","authority_ref":a["authority_id"],"items":pre,"closure_digest":""}; prereq["closure_digest"]=dwo(prereq,"closure_digest")
    report={"reconciliation_id":"MATH-G9-MIXED-PT2-RECONCILIATION-v1","schema_version":"1.0.0","subject":"MATHEMATICS","question_set_ref":q["question_set_id"],"question_set_digest":q["question_set_digest"],"declared_topic_scope_ref":s["declared_topic_scope_id"],"declared_topic_scope_digest":s["scope_digest"],"assessment_review_bundle_digest":review["bundle_digest"],"authority_ref":a["authority_id"],"authority_digest":a["authority_digest"],"binding_registry_ref":b["binding_registry_id"],"binding_registry_digest":b["binding_registry_digest"],"attempt_data_consumed":False,"findings":findings,"summary":{"item_count":len(cov),"mapping_state_counts":counts,"finding_code_counts":dict(sorted(Counter(x["code"] for x in findings).items()))},"report_digest":""}; report["report_digest"]=dwo(report,"report_digest")
    return model,coverage,report,prereq

def main():
    p=argparse.ArgumentParser()
    for x in ["questions","topic-scope","review-registry","review-policy","authority","bindings","scope-model-out","coverage-out","reconciliation-out","prerequisite-out"]: p.add_argument("--"+x,required=True)
    x=p.parse_args()
    vals=reconcile(load(x.questions),load(x.topic_scope),load(x.review_registry),load(x.review_policy),load(x.authority),load(x.bindings))
    for path,val in zip([x.scope_model_out,x.coverage_out,x.reconciliation_out,x.prerequisite_out],vals): write(path,val)
if __name__=="__main__": main()
