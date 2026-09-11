#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path
LOW_CONFIDENCE=0.90
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def digest(o,field=None,array=None,key=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    if array and key: x[array]=sorted(x[array],key=lambda r:r[key])
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def unit_payload(u): return {k:u[k] for k in ["source_unit_id","source_order","source_page","heading","statement","examples","exceptions","footnotes","representation"]}
def q_payload(q): return {k:q[k] for k in ["question_id","source_order","section","marks","stem","subparts","options","givens","representation","answer_key","source_shape"]}
def c_payload(c): return {k:c[k] for k in ["candidate_id","source_order","source_url","source_locator","source_title"]}
def verify_source_set(s):
    seen=set()
    for u in s["units"]:
        if u["source_unit_id"] in seen: raise ValueError("DUPLICATE_SOURCE_UNIT_ID")
        seen.add(u["source_unit_id"])
        if u["source_provenance"]["source_digest"]!=hashlib.sha256(canonical(unit_payload(u)).encode()).hexdigest(): raise ValueError("SOURCE_UNIT_DIGEST_MISMATCH")
    if s["source_set_digest"]!=digest(s,"source_set_digest","units","source_unit_id"): raise ValueError("SOURCE_SET_DIGEST_MISMATCH")
def verify_questions(qs):
    qids=set(); parts=set()
    for q in qs["questions"]:
        if q["question_id"] in qids: raise ValueError("DUPLICATE_QUESTION_ID")
        qids.add(q["question_id"])
        sh=q["source_shape"]
        if sh["option_count"]!=len(q["options"]): raise ValueError("MCQ_OPTION_LOST")
        if sh["subpart_count"]!=len(q["subparts"]): raise ValueError("QUESTION_PART_MERGED")
        if sh["figure_count"]!=len(q["representation"]["figures"]): raise ValueError("FIGURE_DEPENDENCY_DROPPED")
        for p in q["subparts"]: parts.add((q["question_id"],p["part_id"]))
        if q["source_provenance"]["source_digest"]!=hashlib.sha256(canonical(q_payload(q)).encode()).hexdigest(): raise ValueError("QUESTION_SOURCE_DIGEST_MISMATCH")
    if qs["question_set_digest"]!=digest(qs,"question_set_digest","questions","question_id"): raise ValueError("QUESTION_SET_DIGEST_MISMATCH")
    return qids,parts
def verify_corpus(c):
    if c["candidate_count_declared"]!=len(c["candidates"]): raise ValueError("EXTERNAL_CORPUS_DENOMINATOR_MISMATCH")
    seen=set()
    for x in c["candidates"]:
        if x["candidate_id"] in seen: raise ValueError("DUPLICATE_CORPUS_ID")
        seen.add(x["candidate_id"])
        if x["source_digest"]!=hashlib.sha256(canonical(c_payload(x)).encode()).hexdigest(): raise ValueError("CORPUS_SOURCE_DIGEST_MISMATCH")
    if c["corpus_digest"]!=digest(c,"corpus_digest","candidates","candidate_id"): raise ValueError("CORPUS_DIGEST_MISMATCH")
def verify_scope(s):
    if s["scope_digest"]!=digest(s,"scope_digest","topics","topic_id"): raise ValueError("TOPIC_SCOPE_DIGEST_MISMATCH")
def verify_attempts(a,qids,parts):
    if a["attempt_set_digest"]!=digest(a,"attempt_set_digest","attempts","attempt_id"): raise ValueError("ATTEMPT_SET_DIGEST_MISMATCH")
    for r in a["attempts"]:
        if r["binding_method"]!="EXPLICIT_ID": raise ValueError("ATTEMPT_NOT_EXPLICITLY_BOUND")
        if r["question_ref"] not in qids: raise ValueError("ATTEMPT_BOUND_TO_WRONG_ITEM")
        if r["part_ref"] is not None and (r["question_ref"],r["part_ref"]) not in parts: raise ValueError("ATTEMPT_BOUND_TO_WRONG_PART")
def build(S,Q,C,T,A,intake_id):
    verify_source_set(S); qids,parts=verify_questions(Q); verify_corpus(C); verify_scope(T)
    if A is not None: verify_attempts(A,qids,parts)
    conf=[]; low=[]; corrections=0
    for u in S["units"]:
        p=u["source_provenance"]; conf.append(p["extraction_confidence"]); corrections+=len(p["human_correction_events"])
        if p["extraction_confidence"]<LOW_CONFIDENCE: low.append("SOURCE:"+u["source_unit_id"])
    for q in Q["questions"]:
        p=q["source_provenance"]; conf.append(p["extraction_confidence"]); corrections+=len(p["human_correction_events"])
        if p["extraction_confidence"]<LOW_CONFIDENCE: low.append("QUESTION:"+q["question_id"])
    for c in C["candidates"]:
        conf.append(c["extraction_confidence"])
        if c["extraction_confidence"]<LOW_CONFIDENCE: low.append("CORPUS:"+c["candidate_id"])
    out={"intake_id":intake_id,"schema_version":"1.0.0","subject":"CHEMISTRY","source_set_ref":S["source_set_id"],"source_set_digest":S["source_set_digest"],
      "question_set_ref":Q["question_set_id"],"question_set_digest":Q["question_set_digest"],"corpus_ref":C["corpus_id"],"corpus_digest":C["corpus_digest"],
      "declared_topic_scope_ref":T["scope_id"],"declared_topic_scope_digest":T["scope_digest"],"attempt_mode":"PRESENT" if A else "ABSENT",
      "attempt_set_ref":A["attempt_set_id"] if A else None,"attempt_set_digest":A["attempt_set_digest"] if A else None,
      "binding_summary":{"source_unit_count":len(S["units"]),"question_count":len(Q["questions"]),"subpart_count":sum(len(q["subparts"]) for q in Q["questions"]),"corpus_candidate_count":len(C["candidates"]),"attempt_count":len(A["attempts"]) if A else 0,"explicit_binding_count":len(A["attempts"]) if A else 0},
      "source_quality_summary":{"minimum_extraction_confidence":min(conf),"low_confidence_refs":sorted(low),"human_correction_event_count":corrections}}
    out["intake_digest"]=digest(out)
    return out
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--sources",required=True); ap.add_argument("--questions",required=True); ap.add_argument("--corpus",required=True); ap.add_argument("--topic-scope",required=True); ap.add_argument("--attempts"); ap.add_argument("--out",required=True); ap.add_argument("--intake-id",required=True); a=ap.parse_args()
    out=build(load(a.sources),load(a.questions),load(a.corpus),load(a.topic_scope),load(a.attempts) if a.attempts else None,a.intake_id)
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
