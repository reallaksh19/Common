#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"engine"))
from compile_chemistry_engineering_closure import digest, load

class ChemistryEngineeringPassportError(Exception):
    def __init__(self,code,message): super().__init__(f"{code}: {message}"); self.code=code; self.message=message
def fail(c,m): raise ChemistryEngineeringPassportError(c,m)
def schema(obj,rel,code):
    try: jsonschema.validate(obj,load(rel))
    except jsonschema.ValidationError as exc: fail(code,exc.message)
def validate_receipt(r):
    s=r["gate_states"]; e=r["external_dependency_states"]; c=r["counts"]; ready=sum(x["status"]=="ENGINEERING_GATE_READY" for x in s); blocked=len(s)-ready; ext_blocked=sum(x["status"] in {"BLOCKED","UNRESOLVED"} for x in e)
    if c != {"direct_gate_count":len(r["direct_gate_ids"]),"closure_gate_count":len(r["closure_gate_ids"]),"ready_gate_count":ready,"blocked_gate_count":blocked,"external_dependency_count":len(e),"external_blocked_count":ext_blocked}: fail("CHEM_PASS_RECEIPT_INCONSISTENT","receipt counts inconsistent")
    should=bool(r["blockers"]) or blocked>0 or ext_blocked>0
    if (r["closure_status"]=="BLOCKED") != should: fail("CHEM_PASS_RECEIPT_INCONSISTENT","closure_status contradicts blockers/states")
def compile_passport(request,receipt):
    schema(request,"contracts/chemistry-engineering-request.schema.json","CHEM_PASS_REQUEST_SCHEMA"); schema(receipt,"contracts/chemistry-engineering-closure-receipt.schema.json","CHEM_PASS_RECEIPT_SCHEMA"); validate_receipt(receipt)
    if request["request_id"]!=receipt["request_id"]: fail("CHEM_PASS_REQUEST_RECEIPT_MISMATCH","request mismatch")
    ready=receipt["closure_status"]=="READY"; next_action="Proceed to CDAU technical boundary; source custody, pedagogy, learner fit and publication remain separate." if ready else (receipt["blockers"][0]["message"] if receipt["blockers"] else "Resolve engineering blockers.")
    p={"schema_version":"1.0.0","passport_id":receipt["receipt_id"].replace("CHEM-ENG-CLOSURE-","CHEM-ENG-PASS-",1),"request_id":request["request_id"],"manifest_id":receipt["manifest_id"],"closure_receipt_id":receipt["receipt_id"],"closure_receipt_digest":digest(receipt),"requested_topic":request["requested_topic"],"requested_scope":request["requested_scope"],"engineering_depth":request["engineering_depth"],"technical_state":"ENGINEERING_READY" if ready else "BLOCKED_PENDING_ENGINEERING","counts":receipt["counts"],"gate_states":receipt["gate_states"],"external_dependency_states":receipt["external_dependency_states"],"source_item_status":receipt["source_item_status"],"cdau_technical_authorization":"ALLOWED" if ready else "BLOCKED","next_action":next_action}; schema(p,"contracts/chemistry-engineering-passport.schema.json","CHEM_PASS_SCHEMA"); return p
def render(p):
    lines=["# Chemistry Engineering Passport","",f"- **Request:** {p['requested_topic']} — {p['requested_scope']}",f"- **Engineering depth:** {p['engineering_depth']}",f"- **Technical state:** {p['technical_state']}",f"- **Internal closure:** {p['counts']['ready_gate_count']}/{p['counts']['closure_gate_count']} gates READY",f"- **External dependencies:** {p['counts']['external_dependency_count']-p['counts']['external_blocked_count']}/{p['counts']['external_dependency_count']} resolved",f"- **Source state:** {p['source_item_status']}",f"- **CDAU technical authorization:** {p['cdau_technical_authorization']}","","## Gate closure",""]
    for x in p["gate_states"]: lines.append(f"- {'✓' if x['status']=='ENGINEERING_GATE_READY' else '✕'} `{x['gate_id']}` — {x['status']}{' (direct)' if x['direct'] else ''}")
    lines += ["","## External prerequisites",""]
    for x in p["external_dependency_states"]: lines.append(f"- `{x['dependency_id']}` — {x['status']} — `{x['evidence_ref']}`")
    lines += ["","## Next action","",p["next_action"],""]; return "\n".join(lines)
def main():
    a=argparse.ArgumentParser(); a.add_argument("request"); a.add_argument("receipt"); a.add_argument("--out"); a.add_argument("--markdown-out"); x=a.parse_args(); p=compile_passport(load(x.request),load(x.receipt)); text=json.dumps(p,indent=2)+"\n"; Path(x.out).write_text(text,encoding="utf-8") if x.out else print(text,end=""); Path(x.markdown_out).write_text(render(p),encoding="utf-8") if x.markdown_out else None
if __name__=="__main__": main()
