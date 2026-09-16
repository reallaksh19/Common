#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import compute_frontier,index_roadmap,load_yaml,print_result,require
from validate_checkpoint import validate_file as validate_checkpoint_file


def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml");join_ref=state.get("predecessor_join") or {}
    join_id=join_ref.get("id");join_path=join_ref.get("path")
    if not join_id and not join_path:return e,w
    if state.get("relay_state")!="ACTIVE":e.append("predecessor_join is valid only while integration executes as ACTIVE serial work")
    if (state.get("execution_policy") or {}).get("mode")!="SERIAL":e.append("parallel join convergence requires SERIAL execution policy")
    if not join_id or not join_path:return e+["predecessor_join requires id and path"],w
    path=root/join_path
    if not path.exists():return e+[f"parallel join receipt does not exist: {join_path}"],w
    join=load_yaml(path);e+=require(join,["schema_version","id","parallel_plan","roadmap_revision","lane_checkpoints","integration","state"],"PARALLEL_JOIN")
    if join.get("schema_version")!="relay-v2.5":e.append("PARALLEL_JOIN.schema_version must be relay-v2.5")
    if str(join.get("id"))!=str(join_id):e.append("predecessor_join.id does not match join receipt")
    if join.get("state")!="READY":e.append("active integration requires parallel join state READY")
    roadmap_ref=state.get("roadmap") or {}
    if str(join.get("roadmap_revision"))!=str(roadmap_ref.get("revision")):e.append("parallel join roadmap_revision must match current roadmap")

    plan_ref=join.get("parallel_plan") or {};e+=require(plan_ref,["id","path"],"PARALLEL_JOIN.parallel_plan")
    plan_path=plan_ref.get("path")
    if not plan_path or not (root/plan_path).exists():return e+[f"parallel join plan does not exist: {plan_path}"],w
    plan=load_yaml(root/plan_path)
    if str(plan.get("id"))!=str(plan_ref.get("id")):e.append("parallel join plan id does not match referenced plan")
    lanes=plan.get("lanes") or []
    lane_by_id={str(x.get("id")):x for x in lanes if isinstance(x,dict)}
    receipts=join.get("lane_checkpoints") or []
    if len(receipts)<2:e.append("parallel join requires at least two lane checkpoints")
    seen=set();actual=set()
    for i,item in enumerate(receipts):
        label=f"lane_checkpoints[{i}]";e+=require(item,["lane_id","work_package","checkpoint_id","checkpoint_path"],label)
        lid=str(item.get("lane_id"));actual.add(lid)
        if lid in seen:e.append(f"duplicate lane checkpoint receipt: {lid}")
        seen.add(lid)
        lane=lane_by_id.get(lid)
        if not lane:e.append(f"parallel join references unknown lane {lid}");continue
        if str(item.get("work_package"))!=str(lane.get("work_package")):e.append(f"{lid}: join work_package does not match parallel plan")
        cp_path=item.get("checkpoint_path")
        if not cp_path or not (root/cp_path).exists():e.append(f"{lid}: lane checkpoint missing: {cp_path}");continue
        ce,cw=validate_checkpoint_file(root/cp_path);e.extend(f"{lid}: {x}" for x in ce);w.extend(f"{lid}: {x}" for x in cw)
        cp=load_yaml(root/cp_path)
        if str(cp.get("checkpoint_id"))!=str(item.get("checkpoint_id")):e.append(f"{lid}: checkpoint_id does not match checkpoint file")
        if str(cp.get("ep_id"))!=str(lane.get("ep_id")):e.append(f"{lid}: checkpoint ep_id does not match lane EP")
        successor=cp.get("successor") or {}
        if successor.get("mode")!="JOIN":e.append(f"{lid}: lane checkpoint successor.mode must be JOIN")
        if str(successor.get("parallel_plan"))!=str(plan.get("id")):e.append(f"{lid}: lane checkpoint JOIN must reference parallel plan")
        if str(successor.get("lane_id"))!=lid:e.append(f"{lid}: lane checkpoint JOIN lane_id mismatch")
    if actual!=set(lane_by_id):e.append("parallel join lane checkpoint set must exactly cover the approved parallel lanes")

    roadmap=load_yaml(root/roadmap_ref["path"]);frontier=compute_frontier(roadmap);_,_,wps=index_roadmap(roadmap)
    integration=join.get("integration") or {};e+=require(integration,["work_package","ep_id","ep_path"],"PARALLEL_JOIN.integration")
    iwp=str(integration.get("work_package"));iep=str(integration.get("ep_id"));iep_path=integration.get("ep_path")
    plan_integration=plan.get("integration") or {}
    if iwp!=str(plan_integration.get("work_package")):e.append("parallel join integration work_package does not match plan")
    if iep!=str(plan_integration.get("planned_ep_id")):e.append("parallel join integration ep_id does not match plan")
    if frontier!=[iwp]:e.append(f"parallel join requires integration work package to be the sole computed frontier; got {frontier}")
    for lane in lanes:
        wp=str(lane.get("work_package"));node=wps.get(wp)
        if not node or (node[2].get("state"))!="COMPLETE":e.append(f"parallel join requires lane work package COMPLETE: {wp}")
    active=state.get("active_ep") or {};current=state.get("current_position") or {}
    if str(active.get("id"))!=iep:e.append("parallel join integration ep_id does not match REPO_STATE.active_ep")
    if str(current.get("work_package"))!=iwp:e.append("parallel join integration work_package does not match REPO_STATE.current_position")
    if not iep_path or not (root/iep_path).exists():return e+[f"parallel join integration EP does not exist: {iep_path}"],w
    ep=load_yaml(root/iep_path);identity=ep.get("identity") or {};src=ep.get("roadmap_source") or {}
    if str(identity.get("ep_id"))!=iep:e.append("integration EP identity does not match join")
    if str(src.get("work_package"))!=iwp:e.append("integration EP roadmap source does not match join")
    if str(identity.get("previous_join"))!=str(join_id):e.append("integration EP identity.previous_join must reference parallel join receipt")
    if identity.get("previous_checkpoint") not in {None,"","NONE"}:e.append("integration EP uses previous_join; identity.previous_checkpoint must be NONE")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
