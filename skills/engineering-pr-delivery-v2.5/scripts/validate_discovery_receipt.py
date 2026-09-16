#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from relaylib import load_yaml,print_result,require
from takeoverlib import expected_basis,find_route,required_discovery_steps,route_key


def _text(value:Any)->bool:return isinstance(value,str) and bool(value.strip())


def _compare_basis(receipt:dict,expected:dict,label:str)->list[str]:
    e=[];basis=receipt.get("basis") or {};route=receipt.get("route") or {}
    for key in ("roadmap_id","roadmap_revision","relay_protocol_basis_ref","material_ref","ep_contract_digest","repo_profile_digest"):
        if str(basis.get(key))!=str(expected.get(key)):e.append(f"{label}.basis.{key} does not match current route basis")
    for key in ("route_key","mode","execution_ref","ep_id","ep_path","plan_id","plan_path","lane_id"):
        if str(route.get(key))!=str(expected.get(key) if key!="mode" else receipt.get("route",{}).get("mode")):
            pass
    exp_baton=expected.get("predecessor_baton") or {};got_baton=basis.get("predecessor_baton") or {}
    for key in ("type","id","path","digest"):
        if str(got_baton.get(key))!=str(exp_baton.get(key)):e.append(f"{label}.basis.predecessor_baton.{key} does not match current predecessor baton")
    return e


def validate_file(root:Path,path:Path,state:dict|None=None,expected_route:dict|None=None,expected_candidate:str|None=None):
    e=[];w=[]
    try:receipt=load_yaml(path)
    except Exception as exc:return [f"DISCOVERY_RECEIPT: {exc}"],w
    label=f"DISCOVERY_RECEIPT {receipt.get('id','?')}"
    e+=require(receipt,["schema_version","id","candidate","route","basis","steps","result","conversation_context_used"],label)
    if receipt.get("schema_version")!="relay-v2.5-discovery":e.append(f"{label}.schema_version must be relay-v2.5-discovery")
    rid=str(receipt.get("id") or "")
    if not rid.startswith("DISC-"):e.append(f"{label}.id must use DISC-* namespace")
    candidate=str((receipt.get("candidate") or {}).get("agent_instance_id") or "")
    if not candidate:e.append(f"{label}.candidate.agent_instance_id must be explicit")
    if expected_candidate is not None and candidate!=str(expected_candidate):e.append(f"{label}.candidate does not match takeover admission")
    if receipt.get("conversation_context_used") is not False:e.append(f"{label}.conversation_context_used must be false")
    state=state or load_yaml(root/"agents/relay/REPO_STATE.yaml")
    rdata=receipt.get("route") or {};rkey=str(rdata.get("route_key") or "")
    route=expected_route or find_route(root,state,rkey)
    if route is None:return e+[f"{label}.route_key does not resolve to a current execution route: {rkey}"],w
    expected=expected_basis(root,state,route)
    expected_route_fields={"route_key":route_key(route),"mode":route.get("mode"),"execution_ref":route.get("execution_ref"),"ep_id":route.get("ep_id"),"ep_path":route.get("ep_path"),"plan_id":route.get("plan_id"),"plan_path":route.get("plan_path"),"lane_id":route.get("lane_id")}
    for key,val in expected_route_fields.items():
        if str(rdata.get(key))!=str(val):e.append(f"{label}.route.{key} does not match current route")
    e+=_compare_basis(receipt,expected,label)
    ep=load_yaml(root/str(route.get("ep_path")));all_ids={str(x.get("id")) for x in ep.get("repository_discovery",[]) or [] if isinstance(x,dict) and x.get("id")};required=set(required_discovery_steps(ep))
    steps=receipt.get("steps")
    if not isinstance(steps,list):e.append(f"{label}.steps must be a list");steps=[]
    seen=set();passed=set()
    for i,item in enumerate(steps):
        sl=f"{label}.steps[{i}]"
        if not isinstance(item,dict):e.append(f"{sl} must be a mapping");continue
        sid=str(item.get("id") or "")
        if not sid.startswith("DSTEP-"):e.append(f"{sl}.id must reference a DSTEP-* instruction")
        if sid not in all_ids:e.append(f"{sl}.id references unknown discovery instruction {sid}")
        if sid in seen:e.append(f"{sl}.id duplicates {sid}")
        seen.add(sid)
        status=item.get("status")
        if status not in {"PASS","FAIL"}:e.append(f"{sl}.status must be PASS or FAIL")
        if status=="PASS":passed.add(sid)
        basis=item.get("basis")
        if not isinstance(basis,list) or not basis or not all(_text(x) for x in basis):e.append(f"{sl}.basis must contain durable non-empty basis entries")
        outputs=item.get("outputs")
        if not isinstance(outputs,list) or not outputs:e.append(f"{sl}.outputs must contain observed outputs")
        else:
            for j,out in enumerate(outputs):
                ol=f"{sl}.outputs[{j}]"
                if not isinstance(out,dict):e.append(f"{ol} must be a mapping");continue
                if not _text(out.get("name")):e.append(f"{ol}.name must be explicit")
                if "value" not in out or out.get("value") in (None,""):e.append(f"{ol}.value must record the observed result")
                ob=out.get("basis")
                if not isinstance(ob,list) or not ob or not all(_text(x) for x in ob):e.append(f"{ol}.basis must contain durable evidence")
    missing=sorted(required-passed)
    if missing:e.append(f"{label} missing PASS results for required discovery steps: {missing}")
    result=receipt.get("result")
    if result not in {"PASS","FAIL"}:e.append(f"{label}.result must be PASS or FAIL")
    if result=="PASS" and (missing or any(isinstance(x,dict) and x.get("status")!="PASS" for x in steps)):e.append(f"{label}.result PASS requires every recorded and required discovery step to PASS")
    return e,w


def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    for admission in state.get("takeover_admissions",[]) or []:
        if not isinstance(admission,dict):continue
        pointer=admission.get("discovery_receipt") or {};path=pointer.get("path")
        if not path:continue
        route=find_route(root,state,str(admission.get("route_key") or ""));candidate=str((admission.get("candidate") or {}).get("agent_instance_id") or "")
        ce,cw=validate_file(root,root/str(path),state,route,candidate);e.extend(ce);w.extend(cw)
        if route:
            receipt=load_yaml(root/str(path))
            if str(pointer.get("id"))!=str(receipt.get("id")):e.append(f"takeover admission discovery_receipt.id does not match receipt at {path}")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
