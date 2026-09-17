#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
ALLOWED_STATES={"SECURE","PARTIAL","FRAGILE","UNKNOWN"}; ALLOWED_EVIDENCE_KINDS={"LEARNER_RESPONSE","DIAGNOSTIC","TEACHER_OBSERVATION"}; ALLOWED_PRIORS={20,50,80}
def canonical(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(v:Any)->str:return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()
def resolve_control_state(spec,purpose_policy):
    prior=spec.get("learner_prior_pct")
    if prior not in ALLOWED_PRIORS: raise AssertionError("LEARNER_PRIOR_MUST_BE_20_50_OR_80")
    purpose=spec.get("purpose"); purposes=purpose_policy.get("purposes") or {}
    if purpose not in purposes: raise AssertionError("PURPOSE_UNRESOLVED_OR_INVALID")
    if purpose_policy.get("invariant")!="PURPOSE_CANNOT_BYPASS_REQUIRED_PREREQUISITES": raise AssertionError("PURPOSE_PREREQUISITE_INVARIANT_MISSING")
    prior_by_ref={}
    for row in list(spec.get("capability_prior_model") or []):
        ref=str(row.get("capability_ref","")).strip()
        if not ref: raise AssertionError("CAPABILITY_REF_REQUIRED")
        if ref in prior_by_ref: raise AssertionError("CAPABILITY_PRIOR_DUPLICATE:"+ref)
        states=row.get("state_by_prior") or {}
        for key in ("20","50","80"):
            if states.get(key) not in ALLOWED_STATES: raise AssertionError("CAPABILITY_PRIOR_STATE_INVALID:"+ref+":"+key)
        prior_by_ref[ref]=row
    if not prior_by_ref: raise AssertionError("CAPABILITY_PRIOR_MODEL_REQUIRED")
    evidence_by_ref={}
    for row in list(spec.get("learner_evidence") or []):
        ref=str(row.get("capability_ref","")).strip()
        if ref not in prior_by_ref: raise AssertionError("LEARNER_EVIDENCE_UNKNOWN_CAPABILITY:"+ref)
        if ref in evidence_by_ref: raise AssertionError("LEARNER_EVIDENCE_DUPLICATE_CAPABILITY:"+ref)
        kind=row.get("evidence_kind")
        if kind=="TEACHING_RECEIPT": raise AssertionError("TEACHING_RECEIPT_CANNOT_PROVE_LEARNER_STATE:"+ref)
        if kind not in ALLOWED_EVIDENCE_KINDS: raise AssertionError("LEARNER_EVIDENCE_KIND_INVALID:"+ref)
        state=row.get("state")
        if state not in ALLOWED_STATES: raise AssertionError("LEARNER_EVIDENCE_STATE_INVALID:"+ref)
        refs=sorted(set(str(x).strip() for x in (row.get("evidence_refs") or []) if str(x).strip()))
        if not refs: raise AssertionError("LEARNER_EVIDENCE_REF_REQUIRED:"+ref)
        evidence_by_ref[ref]={"state":state,"basis":kind,"evidence_refs":refs}
    capability_states=[]
    for ref in sorted(prior_by_ref):
        resolved=evidence_by_ref.get(ref) or {"state":prior_by_ref[ref]["state_by_prior"][str(prior)],"basis":"PRIOR_HEURISTIC","evidence_refs":[]}
        capability_states.append({"capability_ref":ref,**resolved})
    src=purposes[purpose]
    purpose_contract={"contract_id":src["contract_id"],"priorities":list(src["priorities"]),"support_bias":src["support_bias"],"transfer_focus":src["transfer_focus"],"purpose_cannot_bypass_required_prerequisites":True}
    out={"schema_version":"1.0.0","control_state_id":spec["control_state_id"],"topic_id":spec["topic_id"],"learner_prior_pct":prior,"purpose":purpose,"capability_states":capability_states,"purpose_contract":purpose_contract,"publication_teaching_receipts_used_as_learner_evidence":False}
    out["control_digest"]=digest(out); return out
def main():
    import argparse
    from jsonschema import Draft202012Validator
    ap=argparse.ArgumentParser(); ap.add_argument("spec",type=Path); ap.add_argument("--out",type=Path); ap.add_argument("--purpose-policy",type=Path,default=ROOT/"policy"/"purpose-contracts.v1.json"); a=ap.parse_args()
    spec=json.loads(a.spec.read_text(encoding="utf-8")); policy=json.loads(a.purpose_policy.read_text(encoding="utf-8")); out=resolve_control_state(spec,policy)
    schema=json.loads((ROOT/"contracts"/"learner-purpose-control-state.schema.json").read_text(encoding="utf-8")); Draft202012Validator(schema).validate(out)
    text=json.dumps(out,indent=2,ensure_ascii=False)+"\n"
    if a.out: a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(text,encoding="utf-8")
    else: print(text,end="")
if __name__=="__main__": main()
