#!/usr/bin/env python3
from __future__ import annotations
import copy, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"engine"))
from compile_chemistry_engineering_closure import load
from compile_chemistry_engineering_authorization_binding import ChemistryEngineeringBindingError, compile_binding
from validate_cdau_engineering_ready import validate_engineered_cdau

REQUEST=load("fixtures/engineering-workbench/redox-request.v1.json"); MANIFEST=load("fixtures/engineering-workbench/redox-manifest.v1.json"); CDAU=load("golden/v6/cdau-redox.json")
Draft202012Validator.check_schema(load("contracts/chemistry-engineering-authorization-binding.schema.json"))
b=compile_binding(REQUEST,MANIFEST)
assert b["status"]=="ENGINEERING_AUTHORIZED"
assert b["scope_ref"]=="REDOX-SPECIES-STATE-AGENT"
assert {"CDAU","PAL"}.issubset(set(b["authorized_consumers"]))
assert b["registry_digest"].startswith("sha256:") and b["closure_digest"].startswith("sha256:")
assert len(b["source_audit_states"])==1
sa=b["source_audit_states"][0]
assert sa["gate_id"]=="CHEM-REDOX-OXIDATION"
assert sa["status"]=="SOURCE_HARDENED"
assert sa["scope_policy"]=="GRADE_BANDED"
assert sa["audit_digest"].startswith("sha256:")

r=validate_engineered_cdau(REQUEST,MANIFEST,CDAU)
assert r["status"]=="PASS"
assert r["engineering_binding_id"]==b["binding_id"]
assert r["engineering_binding_digest"].startswith("sha256:")
assert r["source_audit_states"]==b["source_audit_states"]

bad=copy.deepcopy(MANIFEST); bad["external_prerequisite_resolutions"]=[]
try: compile_binding(REQUEST,bad)
except ChemistryEngineeringBindingError as e: assert e.code=="CHEM_BIND_ENGINEERING_BLOCKED"
else: raise AssertionError("blocked closure must not issue authorization binding")
print("Chemistry Engineering authorization binding: PASS")
