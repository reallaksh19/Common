#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"engine"))
from compile_chemistry_engineering_closure import digest, load
from compile_chemistry_engineering_authorization_binding import ChemistryEngineeringBindingError, compile_binding

class ChemistryCDAUEngineeringError(Exception):
    def __init__(self,code,message): super().__init__(f"{code}: {message}"); self.code=code; self.message=message
def fail(c,m): raise ChemistryCDAUEngineeringError(c,m)
def validate_engineered_cdau(request,manifest,cdau):
    if manifest.get("scope_kind")!="SUBTOPIC": fail("CHEM_CDAU_ENGINEERING_SCOPE_KIND","CDAU manifest must use SUBTOPIC")
    if manifest.get("scope_ref")!=cdau.get("subtopic_id"): fail("CHEM_CDAU_ENGINEERING_SCOPE_MISMATCH",f"manifest scope_ref {manifest.get('scope_ref')} != CDAU {cdau.get('subtopic_id')}")
    if "CDAU" not in manifest.get("downstream_consumers",[]): fail("CHEM_CDAU_ENGINEERING_NOT_AUTHORIZED","manifest does not authorize CDAU")
    try: binding=compile_binding(request,manifest)
    except ChemistryEngineeringBindingError as exc: fail("CHEM_CDAU_ENGINEERING_BLOCKED",f"{exc.code}: {exc.message}")
    if "CDAU" not in binding["authorized_consumers"]: fail("CHEM_CDAU_ENGINEERING_NOT_AUTHORIZED","binding does not authorize CDAU")
    if "CHEM-REDOX-OXIDATION" in manifest.get("required_gate_ids",[]):
        audits=[x for x in binding["source_audit_states"] if x["gate_id"]=="CHEM-REDOX-OXIDATION"]
        if len(audits)!=1 or audits[0]["status"]!="SOURCE_HARDENED": fail("CHEM_CDAU_SOURCE_AUDIT_MISSING","Redox CDAU requires SOURCE_HARDENED audit custody")
    try: jsonschema.validate(cdau,load("contracts/cdau-governance-v6.schema.json"))
    except jsonschema.ValidationError as exc: fail("CHEM_CDAU_SCHEMA",exc.message)
    return {"status":"PASS","subtopic_id":cdau["subtopic_id"],"engineering_binding_id":binding["binding_id"],"engineering_binding_digest":digest(binding),"engineering_closure_receipt_id":binding["closure_receipt_id"],"engineering_closure_digest":binding["closure_digest"],"source_audit_states":binding["source_audit_states"],"source_item_status":binding["source_item_status"]}
def main():
    p=argparse.ArgumentParser(); p.add_argument("request"); p.add_argument("manifest"); p.add_argument("cdau"); a=p.parse_args(); print(json.dumps(validate_engineered_cdau(load(a.request),load(a.manifest),load(a.cdau)),indent=2))
if __name__=="__main__": main()
