#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import compute_frontier,load_yaml,print_result,require
from validate_checkpoint import validate_file as validate_checkpoint

EVIDENCE_STATUS={"PASS","FAIL","NOT_RUN","NA"}

def _validate_transfer(item,label,e):
    for field in ("unresolved_acceptance","evidence","transfer_to_work_package"):
        if field not in item:e.append(f"{label} missing {field}")
    acc=item.get("unresolved_acceptance") or []
    if not isinstance(acc,list):e.append(f"{label}.unresolved_acceptance must be a list")
    else:
        for i,a in enumerate(acc):
            p=f"{label}.unresolved_acceptance[{i}]"
            if not isinstance(a,dict):e.append(f"{p} must be a mapping");continue
            for f in ("id","state","basis"):
                if f not in a:e.append(f"{p} missing {f}")
            if not isinstance(a.get("basis"),list) or not a.get("basis"):e.append(f"{p}.basis must contain durable references")
    ev=item.get("evidence") or []
    if not isinstance(ev,list):e.append(f"{label}.evidence must be a list")
    else:
        for i,x in enumerate(ev):
            p=f"{label}.evidence[{i}]"
            if not isinstance(x,dict):e.append(f"{p} must be a mapping");continue
            for f in ("id","status","basis_ref"):
                if f not in x:e.append(f"{p} missing {f}")
            if x.get("status") not in EVIDENCE_STATUS:e.append(f"{p}.status invalid: {x.get('status')}")
            if x.get("status") in {"PASS","FAIL","NOT_RUN"} and not str(x.get("basis_ref","")).strip():e.append(f"{p}.basis_ref must be explicit")
            if x.get("status")=="NOT_RUN" and not str(x.get("reason","")).strip():e.append(f"{p} NOT_RUN requires reason")

def _check_inheritance(ep,replan_id,item,label,e):
    ident=ep.get("identity") or {}
    if str(ident.get("previous_replan"))!=str(replan_id):e.append(f"{label}: identity.previous_replan must match {replan_id}")
    inh=ep.get("replan_inheritance") or {}
    if str(inh.get("from_replan"))!=str(replan_id):e.append(f"{label}: replan_inheritance.from_replan must match {replan_id}")
    if inh.get("unresolved_acceptance")!=(item.get("unresolved_acceptance") or []):e.append(f"{label}: replan inheritance mismatch for unresolved_acceptance")
    if inh.get("evidence")!=(item.get("evidence") or []):e.append(f"{label}: replan inheritance mismatch for evidence")

def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml");ref=(state.get("predecessor_replan") or {}).get("path")
    if not ref:return e,w
    path=root/ref
    if not path.exists():return [f"parallel replan receipt does not exist: {ref}"],w
    replan=load_yaml(path);e+=require(replan,["schema_version","id","predecessor_plan","trigger","lane_dispositions","roadmap_reconciliation","successor_route"],"PARALLEL_REPLAN")
    if replan.get("schema_version")!="relay-v2.5-parallel-replan":e.append("PARALLEL_REPLAN.schema_version must be relay-v2.5-parallel-replan")
    if str((state.get("predecessor_replan") or {}).get("id"))!=str(replan.get("id")):e.append("REPO_STATE.predecessor_replan.id does not match receipt")
    pred=replan.get("predecessor_plan") or {};e+=require(pred,["id","path"],"PARALLEL_REPLAN.predecessor_plan")
    pred_path=root/str(pred.get("path",""))
    if not pred_path.exists():return e+[f"predecessor parallel plan does not exist: {pred.get('path')}"],w
    plan=load_yaml(pred_path)
    if str(plan.get("id"))!=str(pred.get("id")):e.append("predecessor plan id does not match receipt")
    old_lanes={str(x.get("id")):x for x in plan.get("lanes",[]) or []}
    dispositions=replan.get("lane_dispositions") or []
    if {str(x.get("lane_id")) for x in dispositions}!={*old_lanes}:e.append("parallel replan lane_dispositions must cover every predecessor lane exactly once")
    trigger=replan.get("trigger") or {};e+=require(trigger,["type","lane_id","reason","basis"],"PARALLEL_REPLAN.trigger")
    if not str(trigger.get("reason","")).strip():e.append("parallel replan trigger reason is required")
    if not isinstance(trigger.get("basis"),list) or not trigger.get("basis"):e.append("parallel replan trigger basis must contain durable references")

    transfers=[]
    roadmap=load_yaml(root/state["roadmap"]["path"]);frontier=compute_frontier(roadmap);wp_state={}
    for obj in roadmap.get("objectives",[]) or []:
        for ph in obj.get("phases",[]) or []:
            for wp in ph.get("work_packages",[]) or []:wp_state[str(wp.get("id"))]=wp.get("state")
    for i,item in enumerate(dispositions):
        lid=str(item.get("lane_id",""));label=f"lane_dispositions[{i}]";old=old_lanes.get(lid) or {}
        if str(item.get("work_package"))!=str(old.get("work_package")):e.append(f"{label} work_package does not match predecessor lane")
        disp=item.get("disposition")
        if disp not in {"COMPLETE","CARRIED","INVALIDATED"}:e.append(f"{label} invalid disposition {disp}");continue
        if trigger.get("type")=="LANE_INVALIDATED" and lid==str(trigger.get("lane_id")) and disp!="INVALIDATED":e.append("trigger lane must have INVALIDATED disposition")
        if disp=="COMPLETE":
            cp=item.get("checkpoint") or {};e+=require(cp,["id","path"],f"{label}.checkpoint")
            cp_path=root/str(cp.get("path",""))
            if not cp_path.exists():e.append(f"{label} checkpoint does not exist")
            else:
                ce,cw=validate_checkpoint(cp_path);e.extend(f"{label}: {x}" for x in ce);w.extend(f"{label}: {x}" for x in cw);data=load_yaml(cp_path)
                if str(data.get("checkpoint_id"))!=str(cp.get("id")):e.append(f"{label} checkpoint id mismatch")
                if str(data.get("ep_id"))!=str(old.get("ep_id")):e.append(f"{label} checkpoint ep_id does not match predecessor lane")
            if wp_state.get(str(item.get("work_package")))!="COMPLETE":e.append(f"{label} COMPLETE lane work package must be COMPLETE in current roadmap")
        else:
            if disp=="INVALIDATED" and (not isinstance(item.get("basis"),list) or not item.get("basis")):e.append(f"{label} INVALIDATED requires durable basis")
            _validate_transfer(item,label,e);target=str(item.get("transfer_to_work_package") or "")
            if target not in frontier:e.append(f"{label} transfer target {target} is not in recomputed frontier")
            transfers.append(item)

    recon=replan.get("roadmap_reconciliation") or {};e+=require(recon,["roadmap_revision","frontier_after"],"PARALLEL_REPLAN.roadmap_reconciliation")
    if str(recon.get("roadmap_revision"))!=str((state.get("roadmap") or {}).get("revision")):e.append("parallel replan roadmap_revision != current REPO_STATE roadmap revision")
    if sorted(str(x) for x in (recon.get("frontier_after") or []))!=sorted(str(x) for x in frontier):e.append("parallel replan frontier_after != computed current frontier")

    route=replan.get("successor_route") or {};e+=require(route,["mode","work_package","ep_id","ep_path","parallel_plan_id","parallel_plan_path"],"PARALLEL_REPLAN.successor_route")
    mode=route.get("mode");count=len(frontier)
    if count==0 and mode!="NONE":e.append("empty recomputed frontier requires successor_route.mode NONE")
    if count==1 and mode!="SERIAL":e.append("single-node recomputed frontier requires successor_route.mode SERIAL")
    if count>=2 and mode!="PARALLEL":e.append("multi-node recomputed frontier requires successor_route.mode PARALLEL")
    rid=str(replan.get("id"))
    if mode=="SERIAL":
        if state.get("relay_state")!="ACTIVE" or (state.get("execution_policy") or {}).get("mode")!="SERIAL":e.append("SERIAL replan successor requires ACTIVE/SERIAL REPO_STATE")
        wp=frontier[0] if frontier else ""
        if str(route.get("work_package"))!=str(wp):e.append("SERIAL replan successor work_package != computed frontier")
        active=state.get("active_ep") or {}
        if str(route.get("ep_id"))!=str(active.get("id")) or str(route.get("ep_path"))!=str(active.get("path")):e.append("SERIAL replan successor route != REPO_STATE active EP")
        if active.get("path") and (root/active["path"]).exists():
            ep=load_yaml(root/active["path"])
            if str((ep.get("identity") or {}).get("previous_replan"))!=rid:e.append("SERIAL successor EP must reference identity.previous_replan")
            for item in transfers:
                if str(item.get("transfer_to_work_package"))==str(wp):_check_inheritance(ep,rid,item,"SERIAL successor EP",e)
    elif mode=="PARALLEL":
        if state.get("relay_state")!="PARALLEL":e.append("PARALLEL replan successor requires relay_state PARALLEL")
        current_ref=(state.get("execution_policy") or {}).get("parallel_plan")
        if str(route.get("parallel_plan_path"))!=str(current_ref):e.append("PARALLEL replan successor plan path != REPO_STATE")
        if current_ref and (root/current_ref).exists():
            current=load_yaml(root/current_ref)
            if str(current.get("id"))!=str(route.get("parallel_plan_id")):e.append("PARALLEL replan successor plan id mismatch")
            if str(current.get("previous_replan"))!=rid:e.append("successor parallel plan must reference previous_replan")
            lane_by_wp={str(x.get("work_package")):x for x in current.get("lanes",[]) or []}
            for item in transfers:
                target=str(item.get("transfer_to_work_package"));lane=lane_by_wp.get(target)
                if lane and (root/lane.get("ep_path","")).exists():_check_inheritance(load_yaml(root/lane["ep_path"]),rid,item,f"successor lane {lane.get('id')}",e)
    elif mode=="NONE":
        if state.get("relay_state") not in {"IDLE","TERMINAL"}:e.append("NONE replan successor requires IDLE or TERMINAL relay state")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
