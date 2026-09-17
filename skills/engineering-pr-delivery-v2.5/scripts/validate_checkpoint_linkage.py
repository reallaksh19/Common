#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml, print_result
from validate_checkpoint import validate_file

NONE_IDS={None,"","NONE"}

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");last=s.get("last_checkpoint")
    if not isinstance(last,dict):return ["REPO_STATE.last_checkpoint must be a mapping"],w
    relay_state=s.get("relay_state");active=s.get("active_ep") or {};checkpoint_id=last.get("id");checkpoint_path=last.get("path");join=s.get("predecessor_join") or {};join_active=bool(join.get("id") or join.get("path"));replan=s.get("predecessor_replan") or {};replan_active=bool(replan.get("id") or replan.get("path"))

    if checkpoint_id in NONE_IDS:
        if checkpoint_path not in {None,""}:e.append("last_checkpoint.path must be null/empty when last_checkpoint.id is NONE")
        if join_active or replan_active:return e,w
        if relay_state=="ACTIVE":
            ep=load_yaml(root/active["path"]);previous=(ep.get("identity") or {}).get("previous_checkpoint")
            if previous not in NONE_IDS:e.append("active EP previous_checkpoint must be NONE when repository has no last checkpoint")
        return e,w

    if join_active:e.append("singular last_checkpoint cannot be active at the same time as predecessor_join")
    if replan_active:e.append("singular last_checkpoint cannot be active at the same time as predecessor_replan")
    if not checkpoint_path:return ["last_checkpoint.path is required when last_checkpoint.id is set"],w
    path=root/checkpoint_path
    if not path.exists():return [f"last checkpoint file does not exist: {checkpoint_path}"],w
    ce,cw=validate_file(path);e.extend(f"checkpoint: {x}" for x in ce);w.extend(f"checkpoint: {x}" for x in cw);cp=load_yaml(path)
    if str(cp.get("checkpoint_id"))!=str(checkpoint_id):e.append("last_checkpoint.id does not match checkpoint file")
    successor=cp.get("successor") or {};mode=successor.get("mode")

    if relay_state=="ACTIVE":
        if mode!="SERIAL":e.append("ACTIVE relay requires last checkpoint successor.mode SERIAL unless a non-checkpoint predecessor baton is active")
        ep=load_yaml(root/active["path"]);previous=(ep.get("identity") or {}).get("previous_checkpoint")
        if str(previous)!=str(checkpoint_id):e.append("active EP identity.previous_checkpoint does not match REPO_STATE.last_checkpoint.id")
        if str(successor.get("ep_id"))!=str(active.get("id")):e.append("last checkpoint successor.ep_id does not match active EP")
        if str(successor.get("frontier_work_package"))!=str((s.get("current_position") or {}).get("work_package")):e.append("last checkpoint successor.frontier_work_package does not match current roadmap position")
    elif relay_state=="PARALLEL":
        if mode!="PARALLEL":e.append("PARALLEL relay requires last checkpoint successor.mode PARALLEL")
        plan_ref=(s.get("execution_policy") or {}).get("parallel_plan")
        if plan_ref and (root/plan_ref).exists():
            plan=load_yaml(root/plan_ref);pid=plan.get("id")
            if str(successor.get("parallel_plan"))!=str(pid):e.append("last checkpoint successor.parallel_plan does not match active parallel plan")
            expected={(str(x.get("work_package")),str(x.get("ep_id"))) for x in plan.get("lanes",[]) or []}
            actual={(str(x.get("work_package")),str(x.get("ep_id"))) for x in successor.get("lanes",[]) or [] if isinstance(x,dict)}
            if actual!=expected:e.append("last checkpoint parallel lane receipts do not match active parallel plan")
            for lane in plan.get("lanes",[]) or []:
                ep_path=lane.get("ep_path")
                if ep_path and (root/ep_path).exists():
                    ep=load_yaml(root/ep_path);previous=(ep.get("identity") or {}).get("previous_checkpoint")
                    if str(previous)!=str(checkpoint_id):e.append(f"parallel lane {lane.get('id')} previous_checkpoint does not match last checkpoint")
    elif relay_state in {"INITIALIZING","IDLE","TERMINAL"}:
        if mode!="NONE":e.append(f"{relay_state} relay requires last checkpoint successor.mode NONE")
    else:e.append(f"unknown relay_state {relay_state}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
