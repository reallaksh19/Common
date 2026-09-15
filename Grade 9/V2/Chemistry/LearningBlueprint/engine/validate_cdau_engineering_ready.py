#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"engine"))
from compile_chemistry_engineering_closure import compile_closure, load

class ChemistryCDAUEngineeringError(Exception):
    def __init__(self,code,message): super().__init__(f"{code}: {message}"); self.code=code; self.message=message
def fail(c,m): raise ChemistryCDAUEngineeringError(c,m)
def validate_engineered_cdau(request,manifest,cdau):
    if manifest.get("scope_kind")!="SUBTOPIC": fail("CHEM_CDAU_ENGINEERING_SCOPE_KIND","CDAU manifest must use SUBTOPIC")
    if manifest.get("scope_ref")!=cdau.get("subtopic_id"): fail("CHEM_CDAU_ENGINEERING_SCOPE_MISMATCH",f"manifest scope_ref {manifest.get('scope_ref')} != CDAU {cdau.get('subtopic_id')}")
    if "CDAU" not in manifest.get("downstream_consumers",[]): fail("CHEM_CDAU_ENGINEERING_NOT_AUTHORIZED","manifest does not authorize CDAU")
    receipt=compile_closure(request,manifest)
    if receipt["closure_status"]!="READY": fail("CHEM_CDAU_ENGINEERING_BLOCKED",f"engineering closure blocked: {[b['code'] for b in receipt['blockers']]}")
    try: jsonschema.validate(cdau,load("contracts/cdau-governance-v6.schema.json"))
    except jsonschema.ValidationError as exc: fail("CHEM_CDAU_SCHEMA",exc.message)
    return {"status":"PASS","subtopic_id":cdau["subtopic_id"],"engineering_closure_receipt_id":receipt["receipt_id"],"engineering_closure_digest":receipt["closure_digest"],"engineering_gate_count":receipt["counts"]["closure_gate_count"],"external_dependency_count":receipt["counts"]["external_dependency_count"],"source_item_status":receipt["source_item_status"]}
def main():
    p=argparse.ArgumentParser(); p.add_argument("request"); p.add_argument("manifest"); p.add_argument("cdau"); a=p.parse_args(); print(json.dumps(validate_engineered_cdau(load(a.request),load(a.manifest),load(a.cdau)),indent=2))
if __name__=="__main__": main()
