#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_chemistry_engineering_gates_v2 import ChemistryEngineeringGateV2Error, validate as validate_registry


class ChemistryEngineeringClosureError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}"); self.code=code; self.message=message


def fail(code, message): raise ChemistryEngineeringClosureError(code, message)
def load(rel): return json.loads((ROOT / rel).read_text(encoding="utf-8"))
def digest(obj): return "sha256:" + hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def validate_schema(obj, rel, code):
    try: jsonschema.validate(obj, load(rel))
    except jsonschema.ValidationError as exc: fail(code, exc.message)

def research_artifact(request, manifest, ref_key, schema, ready, supplied, missing_code, invalid_code, blockers):
    rel=manifest.get(ref_key)
    if not rel:
        blockers.append({"code":missing_code,"message":f"RESEARCH request requires {ref_key}"}); return
    try:
        art=supplied if supplied is not None else load(rel)
        jsonschema.validate(art, load(schema))
        if art["request_id"] != request["request_id"] or art["status"] != ready: raise ValueError("request/status mismatch")
    except Exception as exc:
        blockers.append({"code":invalid_code,"message":f"{ref_key} not ready: {exc}"})

def compile_closure(request, manifest, *, registry=None, research_dossier=None, claim_ledger=None):
    validate_schema(request,"contracts/chemistry-engineering-request.schema.json","CHEM_ENG_REQUEST_SCHEMA")
    validate_schema(manifest,"contracts/chemistry-engineering-topic-manifest.schema.json","CHEM_ENG_MANIFEST_SCHEMA")
    if request["request_id"] != manifest["request_id"]: fail("CHEM_ENG_REQUEST_MANIFEST_MISMATCH","request_id mismatch")
    registry = registry if registry is not None else load(manifest["registry_ref"])
    try: validate_registry(registry)
    except ChemistryEngineeringGateV2Error as exc: fail("CHEM_ENG_REGISTRY_INVALID",f"{exc.code}: {exc.message}")

    gate_map={g["subtopic_id"]:g for g in registry["subtopic_gates"]}; direct=list(manifest["required_gate_ids"]); direct_set=set(direct)
    seen=set(); visiting=[]; ordered=[]; external=set()
    def walk(gid):
        if gid in seen:return
        if gid in visiting:
            i=visiting.index(gid); fail("CHEM_ENG_DEPENDENCY_CYCLE"," -> ".join(visiting[i:]+[gid]))
        gate=gate_map.get(gid)
        if gate is None:
            seen.add(gid); ordered.append(gid); return
        visiting.append(gid)
        for p in gate.get("prerequisite_ids",[]):
            if p.startswith("CHEM-"): walk(p)
            else: external.add(p)
        visiting.pop(); seen.add(gid); ordered.append(gid)
    for gid in direct: walk(gid)

    blockers=[]; gate_states=[]
    for gid in ordered:
        gate=gate_map.get(gid)
        if gate is None:
            gate_states.append({"gate_id":gid,"status":"MISSING","direct":gid in direct_set}); blockers.append({"code":"CHEM_ENG_GATE_MISSING","gate_id":gid,"message":f"required gate {gid} missing"}); continue
        status=gate["technical_readiness"]; gate_states.append({"gate_id":gid,"status":status,"direct":gid in direct_set})
        if status != "ENGINEERING_GATE_READY": blockers.append({"code":"CHEM_ENG_GATE_NOT_READY","gate_id":gid,"message":f"{gid} status is {status}"})

    resolution_map={r["dependency_id"]:r for r in manifest["external_prerequisite_resolutions"]}; ext_states=[]
    for dep in sorted(external):
        r=resolution_map.get(dep)
        if not r:
            ext_states.append({"dependency_id":dep,"status":"UNRESOLVED","evidence_ref":"NONE"}); blockers.append({"code":"CHEM_ENG_EXTERNAL_PREREQ_UNRESOLVED","dependency_id":dep,"message":f"external prerequisite {dep} unresolved"}); continue
        ext_states.append({"dependency_id":dep,"status":r["status"],"evidence_ref":r["evidence_ref"]})
        if r["status"] == "BLOCKED": blockers.append({"code":"CHEM_ENG_EXTERNAL_PREREQ_UNRESOLVED","dependency_id":dep,"message":f"external prerequisite {dep} blocked"})

    if request["engineering_depth"] == "RESEARCH":
        research_artifact(request,manifest,"research_dossier_ref","contracts/chemistry-engineering-research-dossier.schema.json","RESEARCH_DOSSIER_READY",research_dossier,"CHEM_ENG_RESEARCH_DOSSIER_REQUIRED","CHEM_ENG_RESEARCH_DOSSIER_INVALID",blockers)
        research_artifact(request,manifest,"claim_ledger_ref","contracts/chemistry-engineering-claim-ledger.schema.json","CLAIM_LEDGER_READY",claim_ledger,"CHEM_ENG_CLAIM_LEDGER_REQUIRED","CHEM_ENG_CLAIM_LEDGER_INVALID",blockers)

    ready=sum(s["status"]=="ENGINEERING_GATE_READY" for s in gate_states); blocked=len(gate_states)-ready; ext_blocked=sum(s["status"] in {"BLOCKED","UNRESOLVED"} for s in ext_states); status="BLOCKED" if blockers else "READY"
    registry_digest=digest(registry)
    payload={"request_id":request["request_id"],"manifest_id":manifest["manifest_id"],"registry_digest":registry_digest,"direct_gate_ids":direct,"closure_gate_ids":ordered,"gate_states":gate_states,"external_dependency_states":ext_states,"blockers":blockers,"closure_status":status,"source_item_status":manifest["source_item_status"]}
    note="technical engineering closure READY; source, pedagogy, learner-state and publication authority remain independent" if status=="READY" else "technical engineering closure BLOCKED; downstream engineering consumption forbidden"
    receipt={"schema_version":"1.0.0","receipt_id":manifest["manifest_id"].replace("CHEM-ENG-MAN-","CHEM-ENG-CLOSURE-",1),"request_id":request["request_id"],"manifest_id":manifest["manifest_id"],"registry_ref":manifest["registry_ref"],"registry_digest":registry_digest,"closure_digest":digest(payload),"direct_gate_ids":direct,"closure_gate_ids":ordered,"gate_states":gate_states,"external_dependency_states":ext_states,"blockers":blockers,"counts":{"direct_gate_count":len(direct),"closure_gate_count":len(ordered),"ready_gate_count":ready,"blocked_gate_count":blocked,"external_dependency_count":len(ext_states),"external_blocked_count":ext_blocked},"closure_status":status,"source_item_status":manifest["source_item_status"],"authority_note":note}
    validate_schema(receipt,"contracts/chemistry-engineering-closure-receipt.schema.json","CHEM_ENG_RECEIPT_SCHEMA"); return receipt

def main():
    p=argparse.ArgumentParser(); p.add_argument("request"); p.add_argument("manifest"); p.add_argument("--out"); a=p.parse_args(); r=compile_closure(load(a.request),load(a.manifest)); text=json.dumps(r,indent=2)+"\n"; Path(a.out).write_text(text,encoding="utf-8") if a.out else print(text,end="")
if __name__=="__main__": main()
