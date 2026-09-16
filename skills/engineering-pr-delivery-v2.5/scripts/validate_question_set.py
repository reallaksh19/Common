#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from relaylib import load_yaml,print_result,require
from takeoverlib import current_routes,route_key,yaml_digest

FOCUS={"Q1":"PRODUCTION_PATH","Q2":"ENGINEERING_PROBLEM","Q3":"BOUNDARIES_INVARIANTS","Q4":"VERIFICATION","Q5":"FIRST_SAFE_SLICE"}
DIMENSIONS={"PRODUCTION_PATH","ENGINEERING_AUTHORITY","NUMERICAL_METHOD","PROTECTED_INVARIANT","INPUT_AUTHORITY","VERIFICATION_ORACLE"}
RECONSTRUCTION={"QUANTITATIVE","LOGIC_RECONSTRUCTION","DESIGN_REASONING"}
REQUIRED_KEYS={
    "Q1":{"production_entrypoint","state_owner","authority_source","downstream_consumer"},
    "Q2":{"reconstruction_steps","intermediate_result","expected_result"},
    "Q3":{"mutation_effect","protected_invariant","falsifier"},
    "Q4":{"independent_method","predicted_result","tolerance_or_exactness"},
    "Q5":{"first_change","predicted_before","predicted_after","verification"},
}


def _text(v:Any)->bool:return isinstance(v,str) and bool(v.strip()) and not (v.strip().startswith("<") and v.strip().endswith(">"))
def _text_list(v:Any)->bool:return isinstance(v,list) and bool(v) and all(_text(x) for x in v)

def _route_fields(route:dict)->dict:
    return {"route_key":route_key(route),"mode":route.get("mode"),"execution_ref":route.get("execution_ref"),"ep_id":route.get("ep_id"),"ep_path":route.get("ep_path"),"plan_id":route.get("plan_id"),"plan_path":route.get("plan_path"),"lane_id":route.get("lane_id")}

def _current_route(root:Path,state:dict,rkey:str)->dict|None:
    for route in current_routes(root,state):
        if route_key(route)==rkey:return route
    return None

def validate_file(root:Path,path:Path,state:dict|None=None,expected_route:dict|None=None):
    e=[];w=[]
    try:qset=load_yaml(path)
    except Exception as exc:return [f"QUESTION_SET: {exc}"],w
    label=f"QUESTION_SET {qset.get('id','?')}"
    e+=require(qset,["schema_version","id","route","boundary","questions","prepared_by"],label)
    if qset.get("schema_version")!="relay-v2.5-question-set":e.append(f"{label}.schema_version must be relay-v2.5-question-set")
    if not str(qset.get("id") or "").startswith("QSET-"):e.append(f"{label}.id must use QSET-* namespace")
    preparer=str((qset.get("prepared_by") or {}).get("agent_instance_id") or "")
    if not _text(preparer):e.append(f"{label}.prepared_by.agent_instance_id must be explicit")

    state=state or load_yaml(root/"agents/relay/REPO_STATE.yaml");rdata=qset.get("route") or {};rkey=str(rdata.get("route_key") or "")
    route=expected_route or _current_route(root,state,rkey)
    if route is None:return e+[f"{label}.route_key does not resolve to a current execution route: {rkey}"],w
    for key,val in _route_fields(route).items():
        if str(rdata.get(key))!=str(val):e.append(f"{label}.route.{key} does not match current execution route")
    ep_path=root/str(route.get("ep_path"));ep=load_yaml(ep_path);src=ep.get("roadmap_source") or {}
    if str(rdata.get("roadmap_revision"))!=str(src.get("roadmap_revision")):e.append(f"{label}.route.roadmap_revision must match EP roadmap revision")
    if str(rdata.get("work_package"))!=str(src.get("work_package")):e.append(f"{label}.route.work_package must match EP work package")
    if str(rdata.get("ep_contract_digest"))!=str(yaml_digest(ep_path)):e.append(f"{label}.route.ep_contract_digest does not match current EP contract")

    qb=ep.get("qualification_boundary") or {}
    if qb.get("required") is not True:e.append(f"{label}: current EP does not declare qualification_boundary.required=true")
    qref=qb.get("question_set") or {}
    if str(qref.get("id"))!=str(qset.get("id")):e.append(f"{label}: EP qualification_boundary.question_set.id mismatch")
    try:rel=str(path.relative_to(root))
    except Exception:rel=str(path)
    if str(qref.get("path"))!=rel:e.append(f"{label}: EP qualification_boundary.question_set.path mismatch")

    boundary=qset.get("boundary") or {};e+=require(boundary,["trigger","from_phase","to_phase","changed_dimensions","basis"],f"{label}.boundary")
    trigger=boundary.get("trigger");dims=boundary.get("changed_dimensions")
    if trigger not in {"PHASE_CHANGED","MATERIAL_QUALIFICATION_BOUNDARY_CHANGED"}:e.append(f"{label}.boundary.trigger invalid: {trigger}")
    if not isinstance(dims,list) or not dims:e.append(f"{label}.boundary.changed_dimensions must be non-empty")
    else:
        unknown=[x for x in dims if x not in DIMENSIONS]
        if unknown:e.append(f"{label}.boundary.changed_dimensions invalid: {unknown}")
    if not _text_list(boundary.get("basis")):e.append(f"{label}.boundary.basis must contain durable reasons")
    if str(boundary.get("to_phase"))!=str(src.get("phase")):e.append(f"{label}.boundary.to_phase must equal incoming EP phase")
    if trigger=="PHASE_CHANGED" and str(boundary.get("from_phase"))==str(boundary.get("to_phase")):e.append(f"{label}: PHASE_CHANGED requires different from_phase/to_phase")
    if trigger=="MATERIAL_QUALIFICATION_BOUNDARY_CHANGED" and str(boundary.get("from_phase"))!=str(boundary.get("to_phase")):e.append(f"{label}: same-phase material-boundary trigger requires from_phase == to_phase")
    for key in ("trigger","from_phase","to_phase","changed_dimensions"):
        if key in qb and qb.get(key)!=boundary.get(key):e.append(f"{label}: EP qualification_boundary.{key} disagrees with question set")

    valid={str(x) for x in (src.get("phase"),src.get("work_package")) if x}
    groups={}
    for group in ("inputs","benchmarks","acceptance","validation","implementation_plan"):
        ids={str(x.get("id")) for x in ep.get(group,[]) or [] if isinstance(x,dict) and x.get("id")}
        groups[group]=ids;valid|=ids

    qs=qset.get("questions")
    if not isinstance(qs,list) or len(qs)!=5:return [*e,f"{label} requires exactly five Q1-Q5 questions"],w
    seen=set()
    for idx,q in enumerate(qs,1):
        qid=f"Q{idx}";ql=f"{label}.{qid}"
        if not isinstance(q,dict):e.append(f"{ql} must be a mapping");continue
        if q.get("id")!=qid:e.append(f"{ql}.id must be {qid}")
        if qid in seen:e.append(f"{label} duplicate question {qid}")
        seen.add(qid)
        if q.get("focus")!=FOCUS[qid]:e.append(f"{ql}.focus must be {FOCUS[qid]}")
        if not _text(q.get("prompt")):e.append(f"{ql}.prompt must be explicit")
        anchors=q.get("anchors")
        if not _text_list(anchors):e.append(f"{ql}.anchors must contain incoming-EP ids")
        else:
            unknown=[a for a in anchors if str(a) not in valid]
            if unknown:e.append(f"{ql}.anchors not present in incoming EP: {unknown}")
        keys=q.get("required_output_keys")
        if not _text_list(keys):e.append(f"{ql}.required_output_keys must be explicit")
        elif not REQUIRED_KEYS[qid].issubset(set(keys)):e.append(f"{ql}.required_output_keys missing {sorted(REQUIRED_KEYS[qid]-set(keys))}")
        if q.get("evidence_required") is not True:e.append(f"{ql}.evidence_required must be true")

        if qid=="Q1" and not any(str(a).startswith(("INPUT-","WP-")) for a in anchors or []):e.append(f"{ql} must anchor the actual incoming path/input authority")
        elif qid=="Q2":
            mode=q.get("reconstruction_mode")
            if mode not in RECONSTRUCTION:e.append(f"{ql}.reconstruction_mode invalid: {mode}")
            payload=q.get("payload")
            if not isinstance(payload,dict) or not _text(payload.get("source")):e.append(f"{ql}.payload must identify a durable source")
            elif mode=="QUANTITATIVE" and (not isinstance(payload.get("values"),dict) or not payload.get("values")):e.append(f"{ql}: QUANTITATIVE reconstruction requires concrete payload.values")
        elif qid=="Q3":
            mut=q.get("mutation") or {}
            for k in ("condition","protected_invariant","falsifier"):
                if not _text(mut.get(k)):e.append(f"{ql}.mutation.{k} must be explicit")
        elif qid=="Q4":
            refs=q.get("oracle_refs")
            if not _text_list(refs):e.append(f"{ql}.oracle_refs must identify incoming benchmark/oracle ids")
            else:
                unknown=[x for x in refs if x not in groups["benchmarks"]]
                if unknown:e.append(f"{ql}.oracle_refs unknown: {unknown}")
            if not _text(q.get("independence_requirement")):e.append(f"{ql}.independence_requirement must be explicit")
            if not any(str(a).startswith(("TEST-","AC-","BENCH-")) for a in anchors or []):e.append(f"{ql} must anchor verification/acceptance/oracle ids")
        elif qid=="Q5":
            refs=q.get("step_refs")
            if not _text_list(refs):e.append(f"{ql}.step_refs must identify incoming STEP ids")
            else:
                unknown=[x for x in refs if x not in groups["implementation_plan"]]
                if unknown:e.append(f"{ql}.step_refs unknown: {unknown}")
            if not any(str(a).startswith(("STEP-","AC-")) for a in anchors or []):e.append(f"{ql} must anchor the first implementation slice")
    return e,w

def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    for route in current_routes(root,state):
        ep=load_yaml(root/str(route.get("ep_path")));qb=ep.get("qualification_boundary") or {}
        if qb.get("required") is not True:continue
        ref=qb.get("question_set") or {};path=ref.get("path")
        if not path:e.append(f"EP {route.get('ep_id')} qualification boundary requires question_set.path");continue
        qp=root/str(path)
        if not qp.exists():e.append(f"EP {route.get('ep_id')} question set does not exist: {path}");continue
        ce,cw=validate_file(root,qp,state,route);e.extend(ce);w.extend(cw)
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
