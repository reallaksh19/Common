#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path
from relaylib import compute_frontier,load_yaml,print_result,require
from validate_checkpoint import validate_file as validate_checkpoint

EVIDENCE_STATUS={"PASS","FAIL","NOT_RUN","NA"}
NONE_IDS={None,"","NONE"}


def _sig(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False)


def _same_items(a,b):
    return Counter(_sig(x) for x in (a or []))==Counter(_sig(x) for x in (b or []))


def _unique_ids(items,label,e):
    seen=set()
    for item in items or []:
        if not isinstance(item,dict):continue
        ident=str(item.get("id","")).strip()
        if ident and ident in seen:e.append(f"{label} contains duplicate id {ident}")
        seen.add(ident)


def _validate_acceptance(items,label,e):
    if not isinstance(items,list):e.append(f"{label} must be a list");return
    _unique_ids(items,label,e)
    for i,a in enumerate(items):
        p=f"{label}[{i}]"
        if not isinstance(a,dict):e.append(f"{p} must be a mapping");continue
        for f in ("id","state","basis"):
            if f not in a:e.append(f"{p} missing {f}")
        if not isinstance(a.get("basis"),list) or not a.get("basis"):e.append(f"{p}.basis must contain durable references")


def _validate_evidence(items,label,e):
    if not isinstance(items,list):e.append(f"{label} must be a list");return
    _unique_ids(items,label,e)
    for i,x in enumerate(items):
        p=f"{label}[{i}]"
        if not isinstance(x,dict):e.append(f"{p} must be a mapping");continue
        for f in ("id","status","basis_ref"):
            if f not in x:e.append(f"{p} missing {f}")
        if x.get("status") not in EVIDENCE_STATUS:e.append(f"{p}.status invalid: {x.get('status')}")
        if x.get("status") in {"PASS","FAIL","NOT_RUN"} and not str(x.get("basis_ref","")).strip():e.append(f"{p}.basis_ref must be explicit")
        if x.get("status")=="NOT_RUN" and not str(x.get("reason","")).strip():e.append(f"{p} NOT_RUN requires reason")


def _validate_transfer_partition(item,label,frontier,e):
    for field in ("unresolved_acceptance","evidence","transfers"):
        if field not in item:e.append(f"{label} missing {field}")
    source_acc=item.get("unresolved_acceptance") or [];source_ev=item.get("evidence") or []
    _validate_acceptance(source_acc,f"{label}.unresolved_acceptance",e);_validate_evidence(source_ev,f"{label}.evidence",e)
    transfers=item.get("transfers") or []
    if not isinstance(transfers,list) or not transfers:
        e.append(f"{label}.transfers must contain at least one successor work package");return []
    targets=set();flat_acc=[];flat_ev=[];normalized=[]
    for i,t in enumerate(transfers):
        p=f"{label}.transfers[{i}]"
        if not isinstance(t,dict):e.append(f"{p} must be a mapping");continue
        for field in ("work_package","unresolved_acceptance","evidence"):
            if field not in t:e.append(f"{p} missing {field}")
        target=str(t.get("work_package","")).strip()
        if not target:e.append(f"{p}.work_package must be non-empty")
        elif target in targets:e.append(f"{label}.transfers contains duplicate target {target}")
        targets.add(target)
        if target and target not in frontier:e.append(f"{p} target {target} is not in recomputed frontier")
        ta=t.get("unresolved_acceptance") or [];te=t.get("evidence") or []
        _validate_acceptance(ta,f"{p}.unresolved_acceptance",e);_validate_evidence(te,f"{p}.evidence",e)
        flat_acc.extend(ta);flat_ev.extend(te);normalized.append(t)
    if not _same_items(source_acc,flat_acc):e.append(f"{label} acceptance transfer partition must preserve every unresolved item exactly once")
    if not _same_items(source_ev,flat_ev):e.append(f"{label} evidence transfer partition must preserve every item/status/basis exactly once")
    return normalized


def _aggregate_target(transfers,target):
    acc=[];ev=[]
    for _,_,t in transfers:
        if str(t.get("work_package"))!=str(target):continue
        acc.extend(t.get("unresolved_acceptance") or []);ev.extend(t.get("evidence") or [])
    return acc,ev


def _check_inheritance(ep,replan_id,expected_acc,expected_ev,label,e):
    ident=ep.get("identity") or {}
    if str(ident.get("previous_replan"))!=str(replan_id):e.append(f"{label}: identity.previous_replan must match {replan_id}")
    inh=ep.get("replan_inheritance") or {}
    if str(inh.get("from_replan"))!=str(replan_id):e.append(f"{label}: replan_inheritance.from_replan must match {replan_id}")
    if not _same_items(inh.get("unresolved_acceptance") or [],expected_acc):e.append(f"{label}: replan inheritance mismatch for unresolved_acceptance")
    if not _same_items(inh.get("evidence") or [],expected_ev):e.append(f"{label}: replan inheritance mismatch for evidence")


def _validate_history_chain(root:Path,current_replan:dict,e):
    seen_replans=set();seen_plans=set();replan=current_replan
    while True:
        rid=str(replan.get("id","")).strip()
        if not rid:e.append("parallel replan history contains receipt without id");return
        if rid in seen_replans:e.append(f"parallel replan history cycle detected at {rid}");return
        seen_replans.add(rid)
        pred=replan.get("predecessor_plan") or {};pid=str(pred.get("id","")).strip();ppath=str(pred.get("path","")).strip()
        if not pid or not ppath:e.append(f"parallel replan history {rid} missing predecessor plan id/path");return
        if ppath in seen_plans:e.append(f"parallel replan history plan cycle detected at {ppath}");return
        seen_plans.add(ppath)
        plan_path=root/ppath
        if not plan_path.exists():e.append(f"parallel replan history missing predecessor plan: {ppath}");return
        plan=load_yaml(plan_path)
        if str(plan.get("id"))!=pid:e.append(f"parallel replan history predecessor plan id mismatch for {rid}")
        prev_id=plan.get("previous_replan");prev_path=plan.get("previous_replan_path")
        if prev_id in NONE_IDS and prev_path in {None,""}:return
        if prev_id in NONE_IDS or prev_path in {None,""}:
            e.append(f"parallel plan {pid} must retain both previous_replan and previous_replan_path or neither");return
        hist_path=root/str(prev_path)
        if not hist_path.exists():e.append(f"parallel replan history missing receipt: {prev_path}");return
        prior=load_yaml(hist_path)
        if str(prior.get("id"))!=str(prev_id):e.append(f"parallel plan {pid} previous_replan id/path mismatch")
        route=prior.get("successor_route") or {}
        if route.get("mode")!="PARALLEL":e.append(f"historical replan {prev_id} must have PARALLEL successor to plan {pid}")
        if str(route.get("parallel_plan_id"))!=pid or str(route.get("parallel_plan_path"))!=ppath:e.append(f"historical replan {prev_id} successor route does not point to plan {pid}")
        replan=prior


def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml");replan_ref=state.get("predecessor_replan") or {};ref=replan_ref.get("path")
    if not ref:return e,w
    path=root/ref
    if not path.exists():return [f"parallel replan receipt does not exist: {ref}"],w
    replan=load_yaml(path);e+=require(replan,["schema_version","id","predecessor_plan","trigger","lane_dispositions","roadmap_reconciliation","successor_route"],"PARALLEL_REPLAN")
    if replan.get("schema_version")!="relay-v2.5-parallel-replan":e.append("PARALLEL_REPLAN.schema_version must be relay-v2.5-parallel-replan")
    if str(replan_ref.get("id"))!=str(replan.get("id")):e.append("REPO_STATE.predecessor_replan.id does not match receipt")
    pred=replan.get("predecessor_plan") or {};e+=require(pred,["id","path"],"PARALLEL_REPLAN.predecessor_plan")
    pred_path=root/str(pred.get("path",""))
    if not pred_path.exists():return e+[f"predecessor parallel plan does not exist: {pred.get('path')}"],w
    plan=load_yaml(pred_path)
    if str(plan.get("id"))!=str(pred.get("id")):e.append("predecessor plan id does not match receipt")
    _validate_history_chain(root,replan,e)
    old_lanes={str(x.get("id")):x for x in plan.get("lanes",[]) or []}
    dispositions=replan.get("lane_dispositions") or []
    if {str(x.get("lane_id")) for x in dispositions}!={*old_lanes}:e.append("parallel replan lane_dispositions must cover every predecessor lane exactly once")
    trigger=replan.get("trigger") or {};e+=require(trigger,["type","lane_id","reason","basis"],"PARALLEL_REPLAN.trigger")
    if not str(trigger.get("reason","")).strip():e.append("parallel replan trigger reason is required")
    if not isinstance(trigger.get("basis"),list) or not trigger.get("basis"):e.append("parallel replan trigger basis must contain durable references")

    roadmap=load_yaml(root/state["roadmap"]["path"]);frontier=compute_frontier(roadmap);wp_state={}
    for obj in roadmap.get("objectives",[]) or []:
        for ph in obj.get("phases",[]) or []:
            for wp in ph.get("work_packages",[]) or []:wp_state[str(wp.get("id"))]=wp.get("state")
    all_transfers=[]
    for i,item in enumerate(dispositions):
        lid=str(item.get("lane_id",""));label=f"lane_dispositions[{i}]";old=old_lanes.get(lid) or {};source_wp=str(item.get("work_package",""))
        if source_wp!=str(old.get("work_package")):e.append(f"{label} work_package does not match predecessor lane")
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
            if wp_state.get(source_wp)!="COMPLETE":e.append(f"{label} COMPLETE lane work package must be COMPLETE in current roadmap")
        else:
            if disp=="INVALIDATED" and (not isinstance(item.get("basis"),list) or not item.get("basis")):e.append(f"{label} INVALIDATED requires durable basis")
            for t in _validate_transfer_partition(item,label,set(frontier),e):all_transfers.append((lid,source_wp,t))

    recon=replan.get("roadmap_reconciliation") or {};e+=require(recon,["roadmap_revision","frontier_after"],"PARALLEL_REPLAN.roadmap_reconciliation")
    if str(recon.get("roadmap_revision"))!=str((state.get("roadmap") or {}).get("revision")):e.append("parallel replan roadmap_revision != current REPO_STATE roadmap revision")
    if sorted(str(x) for x in (recon.get("frontier_after") or []))!=sorted(str(x) for x in frontier):e.append("parallel replan frontier_after != computed current frontier")

    route=replan.get("successor_route") or {};e+=require(route,["mode","work_package","ep_id","ep_path","parallel_plan_id","parallel_plan_path"],"PARALLEL_REPLAN.successor_route")
    mode=route.get("mode");count=len(frontier);rid=str(replan.get("id"))
    if count==0 and mode!="NONE":e.append("empty recomputed frontier requires successor_route.mode NONE")
    if count==1 and mode!="SERIAL":e.append("single-node recomputed frontier requires successor_route.mode SERIAL")
    if count>=2 and mode!="PARALLEL":e.append("multi-node recomputed frontier requires successor_route.mode PARALLEL")
    if mode=="SERIAL":
        if state.get("relay_state")!="ACTIVE" or (state.get("execution_policy") or {}).get("mode")!="SERIAL":e.append("SERIAL replan successor requires ACTIVE/SERIAL REPO_STATE")
        wp=frontier[0] if frontier else ""
        if str(route.get("work_package"))!=str(wp):e.append("SERIAL replan successor work_package != computed frontier")
        active=state.get("active_ep") or {}
        if str(route.get("ep_id"))!=str(active.get("id")) or str(route.get("ep_path"))!=str(active.get("path")):e.append("SERIAL replan successor route != REPO_STATE active EP")
        if active.get("path") and (root/active["path"]).exists():
            acc,ev=_aggregate_target(all_transfers,wp);_check_inheritance(load_yaml(root/active["path"]),rid,acc,ev,"SERIAL successor EP",e)
    elif mode=="PARALLEL":
        if state.get("relay_state")!="PARALLEL":e.append("PARALLEL replan successor requires relay_state PARALLEL")
        current_ref=(state.get("execution_policy") or {}).get("parallel_plan")
        if str(route.get("parallel_plan_path"))!=str(current_ref):e.append("PARALLEL replan successor plan path != REPO_STATE")
        if current_ref and (root/current_ref).exists():
            current=load_yaml(root/current_ref)
            if str(current.get("id"))!=str(route.get("parallel_plan_id")):e.append("PARALLEL replan successor plan id mismatch")
            if str(current.get("previous_replan"))!=rid:e.append("successor parallel plan must reference previous_replan")
            if str(current.get("previous_replan_path"))!=str(ref):e.append("successor parallel plan must reference previous_replan_path")
            lane_by_wp={str(x.get("work_package")):x for x in current.get("lanes",[]) or []}
            for target in frontier:
                lane=lane_by_wp.get(str(target))
                if not lane:continue
                ep_path=root/str(lane.get("ep_path", ""))
                if ep_path.exists():
                    acc,ev=_aggregate_target(all_transfers,target);_check_inheritance(load_yaml(ep_path),rid,acc,ev,f"successor lane {lane.get('id')}",e)
    elif mode=="NONE":
        if state.get("relay_state") not in {"IDLE","TERMINAL"}:e.append("NONE replan successor requires IDLE or TERMINAL relay state")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
