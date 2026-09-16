#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from relaylib import load_yaml,print_result,require
from takeoverlib import expected_basis,find_route,route_key
from validate_discovery_receipt import validate_file as validate_discovery
from validate_ep_self_contained import validate_ep_data as validate_ep_self_contained
from validate_ep_semantics import validate_ep_data as validate_ep_semantics
from validate_ep_acceptance_mapping import validate_ep_data as validate_ep_acceptance

CHECKS=("baton_semantics","repository_discovery","route_grounding","input_oracle_readiness","scope_understood","report_successor_contract")
EVALUATORS={"DETERMINISTIC_VALIDATOR","INDEPENDENT_AGENT","OWNER"}


def _text(value:Any)->bool:return isinstance(value,str) and bool(value.strip())


def _route_fields(route:dict)->dict:
    return {"route_key":route_key(route),"mode":route.get("mode"),"execution_ref":route.get("execution_ref"),"ep_id":route.get("ep_id"),"ep_path":route.get("ep_path"),"plan_id":route.get("plan_id"),"plan_path":route.get("plan_path"),"lane_id":route.get("lane_id")}


def _basis_errors(tc:dict,expected:dict,label:str)->list[str]:
    e=[];basis=tc.get("basis") or {}
    for key in ("roadmap_id","roadmap_revision","relay_protocol_basis_ref","material_ref","ep_contract_digest","repo_profile_digest"):
        if str(basis.get(key))!=str(expected.get(key)):e.append(f"{label}.basis.{key} does not match current repository/EP basis")
    got=basis.get("predecessor_baton") or {};exp=expected.get("predecessor_baton") or {}
    for key in ("type","id","path","digest"):
        if str(got.get(key))!=str(exp.get(key)):e.append(f"{label}.basis.predecessor_baton.{key} does not match current predecessor baton")
    return e


def validate_file(root:Path,path:Path,state:dict|None=None,expected_route:dict|None=None,expected_candidate:str|None=None):
    e=[];w=[]
    try:tc=load_yaml(path)
    except Exception as exc:return [f"TAKEOVER_CERTIFICATION: {exc}"],w
    label=f"TAKEOVER_CERTIFICATION {tc.get('id','?')}"
    e+=require(tc,["schema_version","id","candidate","prepared_by","evaluated_by","self_certification","route","basis","discovery_receipt","qualification","checks","result","conversation_context_used"],label)
    if tc.get("schema_version")!="relay-v2.5-takeover-certification":e.append(f"{label}.schema_version must be relay-v2.5-takeover-certification")
    if not str(tc.get("id") or "").startswith("TC-"):e.append(f"{label}.id must use TC-* namespace")
    candidate=str((tc.get("candidate") or {}).get("agent_instance_id") or "")
    preparer=str((tc.get("prepared_by") or {}).get("agent_instance_id") or "")
    if not candidate:e.append(f"{label}.candidate.agent_instance_id must be explicit")
    if not preparer:e.append(f"{label}.prepared_by.agent_instance_id must be explicit")
    if candidate and preparer and candidate==preparer:e.append(f"{label}: candidate must not prepare its own takeover criteria/certification")
    if expected_candidate is not None and candidate!=str(expected_candidate):e.append(f"{label}.candidate does not match takeover admission")
    evaluator=tc.get("evaluated_by") or {};etype=evaluator.get("type");eid=str(evaluator.get("identity") or "")
    if etype not in EVALUATORS:e.append(f"{label}.evaluated_by.type invalid: {etype}")
    if not eid:e.append(f"{label}.evaluated_by.identity must be explicit")
    ebasis=evaluator.get("basis")
    if not isinstance(ebasis,list) or not ebasis or not all(_text(x) for x in ebasis):e.append(f"{label}.evaluated_by.basis must contain durable evaluation basis")
    if etype=="INDEPENDENT_AGENT" and eid==candidate:e.append(f"{label}: independent evaluator cannot be the candidate")
    if etype=="DETERMINISTIC_VALIDATOR" and eid!="validate_takeover_certification.py":e.append(f"{label}: deterministic evaluation identity must be validate_takeover_certification.py")
    if (tc.get("self_certification") or {}).get("allowed") is not False:e.append(f"{label}.self_certification.allowed must be false")
    if tc.get("conversation_context_used") is not False:e.append(f"{label}.conversation_context_used must be false")

    state=state or load_yaml(root/"agents/relay/REPO_STATE.yaml")
    rdata=tc.get("route") or {};rkey=str(rdata.get("route_key") or "")
    route=expected_route or find_route(root,state,rkey)
    if route is None:return e+[f"{label}.route_key does not resolve to a current execution route: {rkey}"],w
    for key,val in _route_fields(route).items():
        if str(rdata.get(key))!=str(val):e.append(f"{label}.route.{key} does not match current route")
    expected=expected_basis(root,state,route);e+=_basis_errors(tc,expected,label)

    ep=load_yaml(root/str(route.get("ep_path")))
    se,sw=validate_ep_self_contained(root,ep,label+" EP");e.extend(se);w.extend(sw)
    se,sw=validate_ep_semantics(root,ep,label+" EP");e.extend(se);w.extend(sw)
    se,sw=validate_ep_acceptance(ep,label+" EP");e.extend(se);w.extend(sw)

    dp=tc.get("discovery_receipt") or {};dpath=dp.get("path")
    if not str(dp.get("id") or "").startswith("DISC-"):e.append(f"{label}.discovery_receipt.id must use DISC-* namespace")
    if not _text(dpath):e.append(f"{label}.discovery_receipt.path must be explicit")
    elif not (root/str(dpath)).exists():e.append(f"{label}.discovery_receipt.path does not exist: {dpath}")
    else:
        de,dw=validate_discovery(root,root/str(dpath),state,route,candidate);e.extend(de);w.extend(dw)
        disc=load_yaml(root/str(dpath))
        if str(disc.get("id"))!=str(dp.get("id")):e.append(f"{label}.discovery_receipt.id does not match receipt file")
        if disc.get("result")!="PASS":e.append(f"{label} requires discovery receipt PASS")

    phase_required=bool((ep.get("phase_transition") or {}).get("required"))
    qual=tc.get("qualification") or {}
    if phase_required:
        if qual.get("required") is not True:e.append(f"{label}: incoming EP requires qualification but TC does not")
        if tc.get("result")=="PASS":e.append(f"{label}: TC cannot PASS while qualification is required until WP-03 QUAL validation is available")
    else:
        if qual.get("required") is not False:e.append(f"{label}.qualification.required must be false when EP has no qualification boundary")
        if qual.get("status")!="NOT_REQUIRED":e.append(f"{label}.qualification.status must be NOT_REQUIRED")
        if qual.get("receipt_id") not in {None,""} or qual.get("receipt_path") not in {None,""}:e.append(f"{label}: NOT_REQUIRED qualification cannot cite a receipt")

    checks=tc.get("checks") or {}
    for check in CHECKS:
        if checks.get(check) not in {"PASS","FAIL"}:e.append(f"{label}.checks.{check} must be PASS or FAIL")
    result=tc.get("result")
    if result not in {"PASS","FAIL"}:e.append(f"{label}.result must be PASS or FAIL")
    if result=="PASS" and any(checks.get(x)!="PASS" for x in CHECKS):e.append(f"{label}.result PASS requires every takeover check PASS")
    return e,w


def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    admissions=state.get("takeover_admissions",[]) or []
    if not isinstance(admissions,list):return ["REPO_STATE.takeover_admissions must be a list"],w
    seen=set();current={route_key(r):r for r in __import__('takeoverlib').current_routes(root,state)}
    for i,admission in enumerate(admissions):
        label=f"takeover_admissions[{i}]"
        if not isinstance(admission,dict):e.append(f"{label} must be a mapping");continue
        rkey=str(admission.get("route_key") or "")
        if not rkey:e.append(f"{label}.route_key must be explicit");continue
        if rkey in seen:e.append(f"takeover_admissions duplicate route_key {rkey}")
        seen.add(rkey)
        route=current.get(rkey)
        if route is None:e.append(f"{label}.route_key is not a current execution route: {rkey}");continue
        candidate=str((admission.get("candidate") or {}).get("agent_instance_id") or "")
        if not candidate:e.append(f"{label}.candidate.agent_instance_id must be explicit")
        dp=admission.get("discovery_receipt") or {};cp=admission.get("certification") or {}
        for name,prefix,pointer in (("discovery_receipt","DISC-",dp),("certification","TC-",cp)):
            if not str(pointer.get("id") or "").startswith(prefix):e.append(f"{label}.{name}.id must use {prefix}* namespace")
            if not _text(pointer.get("path")):e.append(f"{label}.{name}.path must be explicit")
        if _text(cp.get("path")) and (root/str(cp.get("path"))).exists():
            ce,cw=validate_file(root,root/str(cp.get("path")),state,route,candidate);e.extend(ce);w.extend(cw)
            tc=load_yaml(root/str(cp.get("path")))
            if str(tc.get("id"))!=str(cp.get("id")):e.append(f"{label}.certification.id does not match certification file")
            if tc.get("result")!="PASS":e.append(f"{label} points to non-PASS Takeover Certification")
        elif _text(cp.get("path")):e.append(f"{label}.certification.path does not exist: {cp.get('path')}")
    return e,w


def is_takeover_certified(root:Path,route:dict,candidate_id:str)->tuple[bool,list[str]]:
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");rkey=route_key(route)
    matches=[x for x in state.get("takeover_admissions",[]) or [] if isinstance(x,dict) and str(x.get("route_key"))==rkey and str((x.get("candidate") or {}).get("agent_instance_id") or "")==str(candidate_id)]
    if len(matches)!=1:return False,[f"no unique takeover admission for {candidate_id} on {rkey}"]
    pointer=matches[0].get("certification") or {};path=pointer.get("path")
    if not path:return False,["takeover admission has no certification path"]
    e,_=validate_file(root,root/str(path),state,route,candidate_id)
    if e:return False,e
    tc=load_yaml(root/str(path));return tc.get("result")=="PASS",([] if tc.get("result")=="PASS" else ["takeover certification result is not PASS"])


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
