#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path

D=Path(__file__).resolve().parents[1]; CHEM=D.parent
sys.path[:0]=[str(CHEM/"AssessmentIntake"/"engine"),str(CHEM/"AssessmentReview"/"engine")]
from build_chemistry_assessment_intake import verify_source_set,verify_questions,verify_corpus,verify_scope  # noqa:E402
from review_chemistry_assessment import build_review,load_registry as load_review_registry  # noqa:E402

ELIGIBLE="ELIGIBLE_IN_SCOPE"; PARTIAL="PARTIAL_SCOPE"; OUT="OUT_OF_SCOPE"; UNRESOLVED="SOURCE_UNRESOLVED"; REVIEW="REVIEW_REQUIRED"
QST={ELIGIBLE,PARTIAL,OUT,UNRESOLVED,REVIEW}; EST={ELIGIBLE,PARTIAL,OUT,UNRESOLVED}; LOW=0.90

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def digest(x): return hashlib.sha256(canon(x)).hexdigest()
def digest_without_field(x,f):
    y=copy.deepcopy(x); y.pop(f,None); return digest(y)
def fail(c,d=""): raise ValueError(f"{c}: {d}" if d else c)

def items(qs):
    out={}
    for q in qs["questions"]:
        out[q["question_id"]]=(q,None)
        for s in q["subparts"]: out[f"{q['question_id']}.{s['part_id']}"]=(q,s)
    return out

def rep_req(r):
    m={"formulas":"FORMULA","charges":"IONIC_CHARGE","states":"PHYSICAL_STATE","conditions":"CONDITION","structures":"STRUCTURE","figures":"FIGURE","observations":"OBSERVATION","units":"UNIT"}
    return {v for k,v in m.items() if r[k]}

def no_counters(x,label):
    bad=sorted(set(x)&{"summary","counters","counts","eligible_total","candidate_total","placed_total"})
    if bad: fail("COUNTERS_ACCEPTED_WITHOUT_RECORD_DERIVATION",f"{label}:{bad}")

def authority_maps(a,scope):
    if a["subject"]!="CHEMISTRY": fail("CANONICAL_AUTHORITY_SUBJECT_MISMATCH")
    topics={t["topic_id"] for t in scope["topics"]}
    if set(a["declared_topic_bindings"])!=topics: fail("DECLARED_SCOPE_SILENTLY_OVERRIDES_SOURCE")
    concepts={x["concept_id"]:x for x in a["concepts"]}; caps={x["capability_id"]:x for x in a["capabilities"]}
    if len(concepts)!=len(a["concepts"]) or len(caps)!=len(a["capabilities"]): fail("CANONICAL_AUTHORITY_DUPLICATE_ID")
    for t,b in a["declared_topic_bindings"].items():
        if set(b["allowed_concept_refs"])-set(concepts) or set(b["allowed_capability_refs"])-set(caps):
            fail("CANONICAL_CHEMISTRY_SILENTLY_ADDS_UNDECLARED_TOPIC",t)
    return topics,caps

def need_pre(refs,caps):
    out=set()
    for r in refs:
        if r not in caps: fail("CANONICAL_CHEMISTRY_SILENTLY_ADDS_UNDECLARED_TOPIC",r)
        out.update(caps[r]["prerequisite_capability_refs"])
    return out

def allowed(rec,a):
    ts=rec["declared_topic_refs"]
    if not ts:return False
    for c in rec["canonical_concept_refs"]:
        if not any(c in a["declared_topic_bindings"][t]["allowed_concept_refs"] for t in ts): return False
    for c in rec["canonical_capability_refs"]:
        if not any(c in a["declared_topic_bindings"][t]["allowed_capability_refs"] for t in ts): return False
    return True

def source_check(src,reviews,ledger,a,topics,caps):
    no_counters(ledger,"source_ledger")
    if ledger["source_set_ref"]!=src["source_set_id"]: fail("SOURCE_OBLIGATION_SET_MISMATCH")
    exp={u["source_unit_id"]:u for u in src["units"]}; rs=ledger["obligations"]; refs=[r["source_ref"] for r in rs]
    if len(refs)!=len(set(refs)) or set(refs)!=set(exp): fail("SOURCE_OBLIGATION_DROPPED_DURING_SCOPE_DERIVATION")
    rv={r["source_unit_ref"]:r for r in reviews}; findings=[]
    for r in rs:
        ref=r["source_ref"]; u=exp[ref]
        if r["source_page"]!=u["source_page"] or r["source_locator"]!=u["source_provenance"]["source_locator"]: fail("SOURCE_OBLIGATION_DROPPED_DURING_SCOPE_DERIVATION",ref)
        if r["scope_status"] not in QST: fail("UNMAPPED_SOURCE_OBLIGATION",ref)
        if any(t not in topics for t in r["declared_topic_refs"]): fail("CANONICAL_CHEMISTRY_SILENTLY_ADDS_UNDECLARED_TOPIC",ref)
        missing=rep_req(u["representation"])-set(r["representation_requirements"])
        if missing: fail("REPRESENTATION_DEPENDENCY_DROPPED",f"{ref}:{sorted(missing)}")
        if u["representation"]["conditions"] and not set(u["representation"]["conditions"])<=set(r["condition_model_refs"]): fail("CONDITION_EXCEPTION_INFERRED_BUT_NOT_RECORDED",ref)
        if u["exceptions"] and not set(u["exceptions"])<=set(r["required_exceptions"]): fail("CONDITION_EXCEPTION_INFERRED_BUT_NOT_RECORDED",ref)
        missing=need_pre(r["canonical_capability_refs"],caps)-set(r["prerequisite_refs"])
        if missing: fail("PREREQUISITE_INFERRED_BUT_NOT_RECORDED",f"{ref}:{sorted(missing)}")
        if rv[ref]["source_integrity_state"]=="REVIEW_REQUIRED" and r["scope_status"] not in {UNRESOLVED,REVIEW}: fail("DECLARED_SCOPE_SILENTLY_OVERRIDES_SOURCE",ref)
        if r["scope_status"]==ELIGIBLE:
            if not r["declared_topic_refs"]: fail("DECLARED_SCOPE_SILENTLY_OVERRIDES_SOURCE",ref)
            if not allowed(r,a): fail("CANONICAL_CHEMISTRY_SILENTLY_ADDS_UNDECLARED_TOPIC",ref)
        elif r["scope_status"]==OUT: findings.append({"finding_type":"SOURCE_OBLIGATION_OUTSIDE_DECLARED_SCOPE","subject_ref":ref,"detail":r["scope_reason"]})
        elif r["scope_status"] in {UNRESOLVED,REVIEW}: findings.append({"finding_type":"REPRESENTATION_DEPENDENCY_UNRESOLVED","subject_ref":ref,"detail":r["scope_reason"]})
        elif r["scope_status"]==PARTIAL: findings.append({"finding_type":"PARTIAL_SCOPE_MATCH","subject_ref":ref,"detail":r["scope_reason"]})
    return findings

def question_check(qs,reviews,reg,a,topics,caps):
    no_counters(reg,"question_bindings")
    if reg["question_set_ref"]!=qs["question_set_id"]: fail("QUESTION_BINDING_SET_MISMATCH")
    exp=items(qs); rs=reg["bindings"]; refs=[r["item_ref"] for r in rs]
    if len(refs)!=len(set(refs)) or set(refs)!=set(exp): fail("UNMAPPED_QUESTION")
    rv={r["item_ref"]:r for r in reviews}; findings=[]; closure=[]
    for r in rs:
        ref=r["item_ref"]; q,s=exp[ref]
        if r["question_ref"]!=q["question_id"] or r["part_ref"]!=(s["part_id"] if s else None): fail("UNMAPPED_QUESTION",ref)
        if r["scope_status"] not in QST: fail("QUESTION_WITHOUT_EXPLICIT_SCOPE_STATE",ref)
        if any(t not in topics for t in r["declared_topic_refs"]): fail("QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE",ref)
        missing=rep_req(q["representation"])-set(r["representation_demands"])
        if missing: fail("REPRESENTATION_DEPENDENCY_DROPPED",f"{ref}:{sorted(missing)}")
        if q["representation"]["conditions"] and not set(q["representation"]["conditions"])<=set(r["conditions_exceptions"]): fail("CONDITION_EXCEPTION_INFERRED_BUT_NOT_RECORDED",ref)
        req=need_pre(r["canonical_capability_refs"],caps); got=set(r["prerequisite_capability_refs"]); ok=req<=got
        closure.append({"item_ref":ref,"required_prerequisites":sorted(req),"recorded_prerequisites":sorted(got),"closed":ok})
        if not ok: fail("PREREQUISITE_INFERRED_BUT_NOT_RECORDED",f"{ref}:{sorted(req-got)}")
        blocked=rv[ref]["validity_state"]=="REVIEW_REQUIRED" or rv[ref]["source_integrity_state"]=="REVIEW_REQUIRED"
        if blocked and r["scope_status"] not in {UNRESOLVED,REVIEW}: fail("QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE",f"{ref}:C-B blocked")
        if r["scope_status"]==ELIGIBLE:
            if not r["declared_topic_refs"] or not allowed(r,a): fail("QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE",ref)
            if r["primary_learner_unit"] not in r["declared_topic_refs"]: fail("ELIGIBLE_ITEM_WITHOUT_UNIQUE_PRIMARY_HOME",ref)
        elif r["scope_status"]==OUT: findings.append({"finding_type":"QUESTION_OUTSIDE_DECLARED_SCOPE","subject_ref":ref,"detail":r["scope_reason"]})
        elif r["scope_status"] in {UNRESOLVED,REVIEW}: findings.append({"finding_type":"REPRESENTATION_DEPENDENCY_UNRESOLVED","subject_ref":ref,"detail":r["scope_reason"]})
        elif r["scope_status"]==PARTIAL: findings.append({"finding_type":"PARTIAL_SCOPE_MATCH","subject_ref":ref,"detail":r["scope_reason"]})
    return findings,closure

def external_check(corpus,reg,a,topics,caps):
    no_counters(reg,"external_classification")
    if reg["corpus_ref"]!=corpus["corpus_id"]: fail("EXTERNAL_CORPUS_CLASSIFICATION_SET_MISMATCH")
    exp={x["candidate_id"]:x for x in corpus["candidates"]}; rs=reg["classifications"]; refs=[r["candidate_id"] for r in rs]
    if len(refs)!=len(set(refs)) or set(refs)!=set(exp): fail("QUESTION_WITHOUT_EXPLICIT_SCOPE_STATE","external coverage")
    findings=[]
    for r in rs:
        cid=r["candidate_id"]; c=exp[cid]
        if r["scope_status"] not in EST: fail("QUESTION_WITHOUT_EXPLICIT_SCOPE_STATE",cid)
        if r["eligibility_basis"]=="TOPIC_LABEL": fail("EXAMSIDE_TOPIC_LABEL_TREATED_AS_ELIGIBILITY",cid)
        if any(t not in topics for t in r["declared_topic_refs"]): fail("QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE",cid)
        if not need_pre(r["canonical_capability_refs"],caps)<=set(r["prerequisite_capability_refs"]): fail("PREREQUISITE_INFERRED_BUT_NOT_RECORDED",cid)
        if c["extraction_confidence"]<LOW and r["scope_status"]==ELIGIBLE: fail("QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE",f"{cid}:low-confidence source")
        if r["scope_status"]==ELIGIBLE:
            if not r["declared_topic_refs"] or not allowed(r,a): fail("QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE",cid)
            if r["primary_learner_unit"] not in r["declared_topic_refs"]: fail("ELIGIBLE_ITEM_WITHOUT_UNIQUE_PRIMARY_HOME",cid)
        elif r["scope_status"]==PARTIAL: findings.append({"finding_type":"PARTIAL_SCOPE_MATCH","subject_ref":cid,"detail":r["scope_reason"]})
        elif r["scope_status"]==OUT: findings.append({"finding_type":"QUESTION_OUTSIDE_DECLARED_SCOPE","subject_ref":cid,"detail":r["scope_reason"]})
        elif r["scope_status"]==UNRESOLVED: findings.append({"finding_type":"REPRESENTATION_DEPENDENCY_UNRESOLVED","subject_ref":cid,"detail":r["scope_reason"]})
    return findings

def build_scope(src,qs,corpus,scope,review,ledger,qreg,ereg,a,bundle_id="CHEM-C-C-SCOPE-BUNDLE-v1"):
    verify_source_set(src); verify_questions(qs); verify_corpus(corpus); verify_scope(scope)
    if any(x.get("subject")!="CHEMISTRY" for x in [src,qs,scope]): fail("ASSESSMENT_SCOPE_SUBJECT_MISMATCH")
    if review["source_set_ref"]!=src["source_set_id"] or review["question_set_ref"]!=qs["question_set_id"]: fail("ASSESSMENT_REVIEW_BINDING_MISMATCH")
    topics,caps=authority_maps(a,scope)
    findings=source_check(src,review["source_reviews"],ledger,a,topics,caps)
    f,closure=question_check(qs,review["question_reviews"],qreg,a,topics,caps); findings+=f
    findings+=external_check(corpus,ereg,a,topics,caps)

    supported=defaultdict(list); assessed=defaultdict(list)
    for r in ledger["obligations"]:
        if r["scope_status"]==ELIGIBLE:
            for t in r["declared_topic_refs"]: supported[t].append(r["obligation_id"])
    for r in qreg["bindings"]:
        if r["scope_status"]==ELIGIBLE:
            for t in r["declared_topic_refs"]: assessed[t].append(r["item_ref"])
    for r in ereg["classifications"]:
        if r["scope_status"]==ELIGIBLE:
            for t in r["declared_topic_refs"]: assessed[t].append(r["candidate_id"])
    for t in sorted(topics):
        if not supported[t]: findings.append({"finding_type":"DECLARED_TOPIC_NOT_SUPPORTED_BY_SOURCE","subject_ref":t,"detail":"No eligible source obligation supports this declared topic."})
        if not assessed[t]: findings.append({"finding_type":"DECLARED_TOPIC_NOT_ASSESSED","subject_ref":t,"detail":"No eligible question or external candidate assesses this declared topic."})

    def row(kind,ref,status,primary,concepts,caps_,levels):
        return {"record_type":kind,"record_ref":ref,"scope_status":status,"primary_learner_unit":primary,"canonical_concept_refs":concepts,"canonical_capability_refs":caps_,"representation_levels":levels}
    sr=[row("SOURCE_OBLIGATION",r["obligation_id"],r["scope_status"],r["declared_topic_refs"][0] if len(r["declared_topic_refs"])==1 and r["scope_status"]==ELIGIBLE else None,r["canonical_concept_refs"],r["canonical_capability_refs"],r["representation_levels"]) for r in ledger["obligations"]]
    qr=[row("QUESTION",r["item_ref"],r["scope_status"],r["primary_learner_unit"],r["canonical_concept_refs"],r["canonical_capability_refs"],r["representation_levels"]) for r in qreg["bindings"]]
    er=[row("EXTERNAL_CANDIDATE",r["candidate_id"],r["scope_status"],r["primary_learner_unit"],r["canonical_concept_refs"],r["canonical_capability_refs"],r["representation_levels"]) for r in ereg["classifications"]]
    sc=Counter(r["scope_status"] for r in ledger["obligations"]); qc=Counter(r["scope_status"] for r in qreg["bindings"]); ec=Counter(r["scope_status"] for r in ereg["classifications"])
    homes=defaultdict(list)
    for rs,key in [(qreg["bindings"],"item_ref"),(ereg["classifications"],"candidate_id")]:
        for r in rs:
            if r["scope_status"]==ELIGIBLE: homes[r["primary_learner_unit"]].append(r[key])
    edges=[{"capability_ref":c["capability_id"],"prerequisite_capability_ref":p} for c in a["capabilities"] for p in c["prerequisite_capability_refs"]]
    status="PASS_NO_MISMATCHES" if not findings else "CLOSED_WITH_EXPLICIT_MISMATCHES"

    out={"bundle_id":bundle_id,"schema_version":"1.0.0","subject":"CHEMISTRY",
      "source_set_ref":src["source_set_id"],"source_set_digest":src["source_set_digest"],"question_set_ref":qs["question_set_id"],"question_set_digest":qs["question_set_digest"],
      "corpus_ref":corpus["corpus_id"],"corpus_digest":corpus["corpus_digest"],"declared_scope_ref":scope["scope_id"],"declared_scope_digest":scope["scope_digest"],
      "assessment_review_ref":review["review_bundle_id"],"assessment_review_digest":review["bundle_digest"],
      "source_obligation_ledger":{"ledger_id":ledger["ledger_id"],"source_set_ref":ledger["source_set_ref"],"obligation_refs":[r["obligation_id"] for r in ledger["obligations"]],"scope_status_counts":dict(sorted(sc.items()))},
      "scope_reconciliation":{"reconciliation_id":"CHEM-C-C-RECON-v1","declared_scope_ref":scope["scope_id"],"findings":findings,"status":status},
      "assessment_scope_model":{"model_id":"CHEM-C-C-ASSESSMENT-SCOPE-v1","source_set_ref":src["source_set_id"],"question_set_ref":qs["question_set_id"],"corpus_ref":corpus["corpus_id"],"declared_scope_ref":scope["scope_id"],"source_obligation_refs":[r["obligation_id"] for r in ledger["obligations"]],"question_binding_refs":[r["item_ref"] for r in qreg["bindings"]],"external_candidate_refs":[r["candidate_id"] for r in ereg["classifications"]],"eligible_primary_units":{k:sorted(v) for k,v in sorted(homes.items())},"model_status":"CLOSED"},
      "prerequisite_closure":{"closure_id":"CHEM-C-C-PREREQ-v1","capability_edges":edges,"question_prerequisite_closure":closure,"status":"CLOSED" if all(x["closed"] for x in closure) else "BLOCKED"},
      "external_corpus_classification":{"classification_id":ereg["classification_id"],"corpus_ref":ereg["corpus_ref"],"candidate_count":len(er),"scope_status_counts":dict(sorted(ec.items())),"eligible_primary_homes":{r["candidate_id"]:r["primary_learner_unit"] for r in ereg["classifications"] if r["scope_status"]==ELIGIBLE}},
      "assessment_coverage_matrix":{"matrix_id":"CHEM-C-C-COVERAGE-v1","rows":sr+qr+er,"summary":{"source_obligation_total":len(sr),"question_item_total":len(qr),"external_candidate_total":len(er),"external_eligible_total":ec[ELIGIBLE],"external_partial_total":ec[PARTIAL],"external_out_of_scope_total":ec[OUT],"external_source_unresolved_total":ec[UNRESOLVED],"question_scope_status_counts":dict(sorted(qc.items())),"source_scope_status_counts":dict(sorted(sc.items()))}},
      "summary":{"source_obligation_total":len(sr),"question_item_total":len(qr),"external_candidate_total":len(er),"external_eligible_total":ec[ELIGIBLE],"external_source_unresolved_total":ec[UNRESOLVED],"finding_count":len(findings),"finding_type_counts":dict(sorted(Counter(x["finding_type"] for x in findings).items())),"blocking_review_refs":review["summary"]["blocking_review_refs"],"counters_derived_from_records":True,"status":"CLOSED_WITH_EXPLICIT_MISMATCHES" if findings else "PASS"},"bundle_digest":""}
    out["bundle_digest"]=digest_without_field(out,"bundle_digest"); return out

def main():
    ap=argparse.ArgumentParser()
    for x in ["sources","questions","corpus","topic-scope","review-registry","review-policy","qc-events","source-obligations","question-bindings","external-classifications","authority","out"]: ap.add_argument("--"+x,required=True)
    a=ap.parse_args(); src=load(a.sources); qs=load(a.questions); rr,md=load_review_registry(a.review_registry)
    review=build_review(src,qs,rr,load(a.review_policy),load(a.qc_events),registry_manifest_digest=md)
    out=build_scope(src,qs,load(a.corpus),load(a.topic_scope),review,load(a.source_obligations),load(a.question_bindings),load(a.external_classifications),load(a.authority))
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__": main()
