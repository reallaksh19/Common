#!/usr/bin/env python3
from __future__ import annotations
import copy, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"engine"))
from compile_chemistry_engineering_closure import ChemistryEngineeringClosureError, compile_closure, load
from compile_chemistry_engineering_passport import ChemistryEngineeringPassportError, compile_passport
from validate_cdau_engineering_ready import ChemistryCDAUEngineeringError, validate_engineered_cdau
from validate_chemistry_engineering_gates_v2 import ChemistryEngineeringGateV2Error, validate as validate_registry

REQUEST=load("fixtures/engineering-workbench/redox-request.v1.json"); MANIFEST=load("fixtures/engineering-workbench/redox-manifest.v1.json"); REGISTRY=load("policies/chemistry-technical-engineering-gates.v1.json"); CDAU=load("golden/v6/cdau-redox.json")
EXPECTED={"CHEM-SYM-LITERACY","CHEM-ION-VALENCY","CHEM-FORMULA-CONSTRUCTION","CHEM-EQ-BALANCING","CHEM-REDOX-OXIDATION"}
def gate(doc,gid): return next(g for g in doc["subtopic_gates"] if g["subtopic_id"]==gid)
def must_closure_fail(req,man,code,**kw):
    try: compile_closure(req,man,**kw)
    except ChemistryEngineeringClosureError as e: assert e.code==code,(code,e.code,str(e)); return
    raise AssertionError(code)
def must_passport_fail(req,receipt,code):
    try: compile_passport(req,receipt)
    except ChemistryEngineeringPassportError as e: assert e.code==code,(code,e.code,str(e)); return
    raise AssertionError(code)
def must_cdau_fail(req,man,cdau,code):
    try: validate_engineered_cdau(req,man,cdau)
    except ChemistryCDAUEngineeringError as e: assert e.code==code,(code,e.code,str(e)); return
    raise AssertionError(code)

for s in ["chemistry-engineering-request.schema.json","chemistry-engineering-topic-manifest.schema.json","chemistry-engineering-research-dossier.schema.json","chemistry-engineering-claim-ledger.schema.json","chemistry-engineering-closure-receipt.schema.json","chemistry-engineering-passport.schema.json","chemistry-engineering-authorization-binding.schema.json"]: Draft202012Validator.check_schema(load("contracts/"+s))
assert len(validate_registry(REGISTRY))==10
receipt=compile_closure(REQUEST,MANIFEST); assert receipt["closure_status"]=="READY"; assert set(receipt["closure_gate_ids"])==EXPECTED; assert receipt["counts"]["closure_gate_count"]==5; assert receipt["counts"]["external_dependency_count"]==1; assert receipt["external_dependency_states"][0]["dependency_id"]=="MATH-BASIC-ARITHMETIC"; assert receipt["external_dependency_states"][0]["status"]=="RESOLVED_BY_OWNER_SCOPE"; assert receipt["source_item_status"]=="SOURCE_HELD"
passport=compile_passport(REQUEST,receipt); assert passport["technical_state"]=="ENGINEERING_READY"; assert passport["cdau_technical_authorization"]=="ALLOWED"
result=validate_engineered_cdau(REQUEST,MANIFEST,CDAU); assert result["status"]=="PASS"; assert result["engineering_binding_id"]=="CHEM-ENG-BIND-REDOX-001"; assert result["engineering_binding_digest"].startswith("sha256:"); assert result["engineering_closure_digest"]==receipt["closure_digest"]

bad=copy.deepcopy(MANIFEST); bad["required_gate_ids"]=["CHEM-REDOX-NOT-REAL"]; r=compile_closure(REQUEST,bad); assert r["closure_status"]=="BLOCKED" and r["blockers"][0]["code"]=="CHEM_ENG_GATE_MISSING"
badreg=copy.deepcopy(REGISTRY); gate(badreg,"CHEM-REDOX-OXIDATION")["technical_readiness"]="ENGINEERING_GATE_INCOMPLETE"; r=compile_closure(REQUEST,MANIFEST,registry=badreg); assert r["closure_status"]=="BLOCKED"
badreg=copy.deepcopy(REGISTRY); gate(badreg,"CHEM-SYM-LITERACY")["prerequisite_ids"].append("CHEM-REDOX-OXIDATION"); must_closure_fail(REQUEST,MANIFEST,"CHEM_ENG_DEPENDENCY_CYCLE",registry=badreg)
bad=copy.deepcopy(MANIFEST); bad["external_prerequisite_resolutions"]=[]; r=compile_closure(REQUEST,bad); assert r["closure_status"]=="BLOCKED"; assert any(b["code"]=="CHEM_ENG_EXTERNAL_PREREQ_UNRESOLVED" for b in r["blockers"])
research=copy.deepcopy(REQUEST); research["engineering_depth"]="RESEARCH"; r=compile_closure(research,MANIFEST); assert r["closure_status"]=="BLOCKED"; assert {b["code"] for b in r["blockers"]}>={"CHEM_ENG_RESEARCH_DOSSIER_REQUIRED","CHEM_ENG_CLAIM_LEDGER_REQUIRED"}
badreq=copy.deepcopy(REQUEST); badreq["engineering_ready"]=True; must_closure_fail(badreq,MANIFEST,"CHEM_ENG_REQUEST_SCHEMA")
tampered=copy.deepcopy(r); tampered["closure_status"]="READY"; must_passport_fail(research,tampered,"CHEM_PASS_RECEIPT_INCONSISTENT")
badman=copy.deepcopy(MANIFEST); badman["scope_ref"]="REDOX-OTHER"; must_cdau_fail(REQUEST,badman,CDAU,"CHEM_CDAU_ENGINEERING_SCOPE_MISMATCH")
badreg=copy.deepcopy(REGISTRY); badreg["maturity"]="EMPIRICAL_VALIDATED"
try: validate_registry(badreg)
except ChemistryEngineeringGateV2Error as e: assert e.code in {"CHEM_ENG_REGISTRY_V1_INVALID","CHEM_ENG_MATURITY_OVERREACH"}
else: raise AssertionError("empirical maturity must fail")
print("Chemistry Engineering Workbench v1: PASS")
