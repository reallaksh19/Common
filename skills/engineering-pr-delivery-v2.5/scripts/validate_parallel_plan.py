#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import compute_frontier,index_roadmap,load_yaml,print_result,require
from validate_ep_self_contained import validate_ep_data as validate_ep_self_contained_data
from validate_ep_semantics import validate_ep_data as validate_ep_semantics_data
from validate_ep_acceptance_mapping import validate_ep_data as validate_ep_acceptance_data

NONE_IDS={None,"","NONE"}

def _norm_domain(value:str)->str:
    value=str(value).strip().replace("\\","/")
    while "//" in value:value=value.replace("//","/")
    return value.rstrip("/")

def _overlap(a:str,b:str)->bool:
    a=_norm_domain(a);b=_norm_domain(b)
    if not a or not b:return True
    return a==b or a.startswith(b+"/") or b.startswith(a+"/") or a in {"*","."} or b in {"*","."}

def _exception_covers(exceptions:list,lane_a:str,lane_b:str,domain_a:str,domain_b:str)->bool:
    pair={lane_a,lane_b}
    for item in exceptions or []:
        if not isinstance(item,dict):continue
        if set(item.get("lanes") or [])!=pair:continue
        if item.get("owner_approved") is not True:continue
        if not str(item.get("reason","")).strip():continue
        declared=str(item.get("domain","")).strip()
        if declared and (_overlap(declared,domain_a) or _overlap(declared,domain_b)):return True
    return False

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    if s.get("relay_state")!="PARALLEL":return e,w
    policy=s.get("execution_policy") or {};ref=policy.get("parallel_plan")
    if not ref:return ["PARALLEL relay requires execution_policy.parallel_plan"],w
    path=root/ref
    if not path.exists():return [f"parallel plan does not exist: {ref}"],w
    plan=load_yaml(path);e+=require(plan,["schema_version","id","owner_approval","ascii_topology","lanes","shared_write_exceptions","integration","risks","stop_conditions"],"PARALLEL_PLAN")
    if plan.get("schema_version")!="relay-v2.5":e.append("PARALLEL_PLAN.schema_version must be relay-v2.5")
    replan_ref=s.get("predecessor_replan") or {};replan_id=replan_ref.get("id");replan_path=replan_ref.get("path")
    if replan_id not in NONE_IDS:
        if str(plan.get("previous_replan"))!=str(replan_id):e.append("parallel plan previous_replan must match REPO_STATE.predecessor_replan.id")
        if str(plan.get("previous_replan_path"))!=str(replan_path):e.append("parallel plan previous_replan_path must match REPO_STATE.predecessor_replan.path")
    elif plan.get("previous_replan") not in NONE_IDS or plan.get("previous_replan_path") not in {None,""}:
        e.append("parallel plan previous_replan/previous_replan_path require REPO_STATE.predecessor_replan")
    approval=plan.get("owner_approval") or {}
    if approval.get("approved") is not True or approval.get("authority")!="OWNER":e.append("parallel plan lacks explicit OWNER approval")
    if not str(approval.get("source","")).strip():e.append("parallel plan owner approval requires durable source")
    if str(approval.get("approval_token","")).strip()!=f"APPROVE PARALLEL {plan.get('id')}":e.append("parallel plan approval_token must exactly approve its plan id")
    if not str(plan.get("ascii_topology","")).strip():e.append("parallel plan requires ascii_topology")
    if not plan.get("risks"):e.append("parallel plan must disclose at least one integration/collision risk")
    if not plan.get("stop_conditions"):e.append("parallel plan must define at least one stop condition")

    roadmap=load_yaml(root/s["roadmap"]["path"]);frontier=set(compute_frontier(roadmap));_,_,wps=index_roadmap(roadmap)
    lanes=plan.get("lanes") or []
    if len(lanes)<2:e.append("parallel plan requires at least two lanes")
    seen={"id":set(),"work_package":set(),"ep_id":set(),"ep_path":set(),"branch":set(),"worktree":set()}
    lane_ids=[];lane_wps=[];lane_domains=[];last=(s.get("last_checkpoint") or {}).get("id")
    for i,lane in enumerate(lanes):
        label=f"lane[{i}]";e+=require(lane,["id","state","work_package","ep_id","ep_path","branch","write_domains","shared_read_domains"],label)
        lid=str(lane.get("id",f"?{i}"));lane_ids.append(lid);wp=str(lane.get("work_package",""));lane_wps.append(wp)
        if lane.get("state")!="ACTIVE":e.append(f"{lid}: current parallel lane must have state ACTIVE")
        for key in ("id","work_package","ep_id","ep_path","branch"):
            val=str(lane.get(key,"")).strip()
            if not val:e.append(f"{lid}: {key} must be non-empty")
            elif val in seen[key]:e.append(f"parallel lanes must have unique {key}: {val}")
            else:seen[key].add(val)
        wt=str(lane.get("worktree","")).strip()
        if wt:
            if wt in seen["worktree"]:e.append(f"parallel lanes must have unique worktree: {wt}")
            seen["worktree"].add(wt)
        domains=lane.get("write_domains") or []
        if not domains:e.append(f"{lid}: write_domains must contain at least one exclusive domain")
        for d in domains:lane_domains.append((lid,str(d)))
        ep_path=str(lane.get("ep_path","")).strip()
        if ep_path:
            p=root/ep_path
            if not p.exists():e.append(f"{lid}: lane EP does not exist: {ep_path}")
            else:
                ep=load_yaml(p)
                ee,ew=validate_ep_self_contained_data(root,ep,lid);e.extend(ee);w.extend(ew)
                ee,ew=validate_ep_semantics_data(root,ep,lid);e.extend(ee);w.extend(ew)
                ee,ew=validate_ep_acceptance_data(ep,lid);e.extend(ee);w.extend(ew)
                ident=ep.get("identity") or {};src=ep.get("roadmap_source") or {}
                if str(ident.get("ep_id"))!=str(lane.get("ep_id")):e.append(f"{lid}: ep_id does not match lane EP identity")
                if str(ident.get("branch"))!=str(lane.get("branch")):e.append(f"{lid}: branch does not match lane EP identity")
                if ident.get("execution_state") not in {"EXECUTABLE","ACTIVE"}:e.append(f"{lid}: lane EP must be executable/active")
                if str(src.get("work_package"))!=wp:e.append(f"{lid}: lane EP work package does not match plan")
                if str(src.get("roadmap_id"))!=str((s.get("roadmap") or {}).get("id")):e.append(f"{lid}: lane EP roadmap id does not match REPO_STATE")
                if str(src.get("roadmap_revision"))!=str((s.get("roadmap") or {}).get("revision")):e.append(f"{lid}: lane EP roadmap revision does not match REPO_STATE")
                if src.get("generated_from_frontier") is not True:e.append(f"{lid}: lane EP must declare generated_from_frontier: true")
                if replan_id not in NONE_IDS:
                    if ident.get("previous_checkpoint") not in NONE_IDS:e.append(f"{lid}: replanned lane previous_checkpoint must be NONE")
                    if str(ident.get("previous_replan"))!=str(replan_id):e.append(f"{lid}: previous_replan must match REPO_STATE.predecessor_replan.id")
                elif last in NONE_IDS:
                    if ident.get("previous_checkpoint") not in NONE_IDS:e.append(f"{lid}: previous_checkpoint must be NONE when repository has no last checkpoint")
                elif str(ident.get("previous_checkpoint"))!=str(last):e.append(f"{lid}: previous_checkpoint must match REPO_STATE.last_checkpoint.id")

    if set(lane_wps)!=frontier:e.append(f"parallel plan lane work packages {sorted(set(lane_wps))} != computed frontier {sorted(frontier)}")
    declared=set((s.get("current_position") or {}).get("work_packages") or [])
    if set(lane_wps)!=declared:e.append("parallel plan lane work packages != REPO_STATE current_position.work_packages")
    for wp in lane_wps:
        if wp not in wps:e.append(f"parallel lane references missing roadmap work package {wp}")

    exceptions=plan.get("shared_write_exceptions") or []
    for i,(la,da) in enumerate(lane_domains):
        for lb,db in lane_domains[i+1:]:
            if la==lb:continue
            if _overlap(da,db) and not _exception_covers(exceptions,la,lb,da,db):e.append(f"write-domain overlap without approved exception: {la}:{da} <-> {lb}:{db}")

    integration=plan.get("integration") or {};e+=require(integration,["owner","work_package","planned_ep_id","creation_policy","depends_on_lanes"],"PARALLEL_PLAN.integration")
    if integration.get("creation_policy")!="WHEN_FRONTIER":e.append("integration.creation_policy must be WHEN_FRONTIER")
    if set(integration.get("depends_on_lanes") or [])!=set(lane_ids):e.append("integration.depends_on_lanes must contain every current lane exactly once")
    iwp=str(integration.get("work_package",""))
    if iwp in frontier:e.append("integration work package must not be executable while parallel lanes are active")
    if iwp not in wps:e.append(f"integration work package missing from roadmap: {iwp}")
    else:
        deps=set(wps[iwp][2].get("depends_on") or [])
        if not set(lane_wps).issubset(deps):e.append("integration work package must depend on every parallel lane work package")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
