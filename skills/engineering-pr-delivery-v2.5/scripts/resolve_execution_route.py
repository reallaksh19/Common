#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
from relaylib import load_yaml


def _git(root:Path,*args):
    return subprocess.check_output(["git","-C",str(root),*args],text=True,stderr=subprocess.DEVNULL).strip()


def detect_branch(root:Path):
    try:return _git(root,"branch","--show-current") or None
    except Exception:return None


def detect_worktree(root:Path):
    try:return _git(root,"rev-parse","--show-toplevel")
    except Exception:return None


def resolve(root:Path,branch:str|None=None,worktree:str|None=None):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");state=s.get("relay_state")
    branch=branch or detect_branch(root);worktree=worktree or detect_worktree(root)
    if state in {"INITIALIZING","IDLE","TERMINAL"}:
        return {"relay_state":state,"route":"NONE","ep_id":None,"ep_path":None,"branch":branch,"worktree":worktree}
    if state=="ACTIVE":
        active=s.get("active_ep") or {};ep=load_yaml(root/active["path"]);expected=(ep.get("identity") or {}).get("branch")
        if branch and expected and branch!=expected:raise ValueError(f"checked-out branch {branch} does not match active EP branch {expected}")
        return {"relay_state":state,"route":"SERIAL","ep_id":active.get("id"),"ep_path":active.get("path"),"branch":branch,"worktree":worktree}
    if state!="PARALLEL":raise ValueError(f"unsupported relay state {state}")
    pref=(s.get("execution_policy") or {}).get("parallel_plan");plan=load_yaml(root/pref);matches=[]
    for lane in plan.get("lanes",[]) or []:
        branch_match=bool(branch and lane.get("branch")==branch)
        wt=lane.get("worktree");worktree_match=bool(worktree and wt and (worktree==wt or Path(worktree).name==Path(str(wt)).name))
        if branch_match or worktree_match:matches.append(lane)
    if len(matches)!=1:
        raise ValueError(f"parallel route must resolve exactly one lane from branch/worktree; matched {[x.get('id') for x in matches]}")
    lane=matches[0]
    return {"relay_state":state,"route":"PARALLEL_LANE","plan_id":plan.get("id"),"lane_id":lane.get("id"),"work_package":lane.get("work_package"),"ep_id":lane.get("ep_id"),"ep_path":lane.get("ep_path"),"branch":branch,"worktree":worktree}


def main():
    ap=argparse.ArgumentParser(description="Resolve the executable V2.5 EP from repository state and current branch/worktree.")
    ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--branch");ap.add_argument("--worktree");a=ap.parse_args()
    try:result=resolve(Path(a.repo_root).resolve(),a.branch,a.worktree)
    except Exception as exc:print(json.dumps({"status":"FAIL","error":str(exc)},indent=2));raise SystemExit(1)
    print(json.dumps({"status":"PASS",**result},indent=2))
if __name__=="__main__":main()
