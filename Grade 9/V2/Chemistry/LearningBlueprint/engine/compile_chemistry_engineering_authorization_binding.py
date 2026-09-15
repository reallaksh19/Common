#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"engine"))
from compile_chemistry_engineering_closure import compile_closure, load

class ChemistryEngineeringBindingError(Exception):
    def __init__(self,code,message): super().__init__(f"{code}: {message}"); self.code=code; self.message=message
def fail(c,m): raise ChemistryEngineeringBindingError(c,m)
def compile_binding(request,manifest):
    receipt=compile_closure(request,manifest)
    if receipt["closure_status"]!="READY": fail("CHEM_BIND_ENGINEERING_BLOCKED",f"closure blocked: {[b['code'] for b in receipt['blockers']]}")
    binding={"schema_version":"1.0.0","binding_id":manifest["manifest_id"].replace("CHEM-ENG-MAN-","CHEM-ENG-BIND-",1),"request_id":request["request_id"],"manifest_id":manifest["manifest_id"],"scope_ref":manifest["scope_ref"],"registry_ref":receipt["registry_ref"],"registry_digest":receipt["registry_digest"],"closure_receipt_id":receipt["receipt_id"],"closure_digest":receipt["closure_digest"],"authorized_consumers":manifest["downstream_consumers"],"source_item_status":receipt["source_item_status"],"status":"ENGINEERING_AUTHORIZED"}
    try: jsonschema.validate(binding,load("contracts/chemistry-engineering-authorization-binding.schema.json"))
    except jsonschema.ValidationError as exc: fail("CHEM_BIND_SCHEMA",exc.message)
    return binding
def main():
    p=argparse.ArgumentParser(); p.add_argument("request"); p.add_argument("manifest"); p.add_argument("--out"); a=p.parse_args(); b=compile_binding(load(a.request),load(a.manifest)); text=json.dumps(b,indent=2)+"\n"; Path(a.out).write_text(text,encoding="utf-8") if a.out else print(text,end="")
if __name__=="__main__": main()
