#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");policy=s.get("execution_policy") or {};mode=policy.get("mode")
    if mode=="SERIAL":
        if policy.get("parallel_plan"):e.append("SERIAL execution must not declare parallel_plan")
    elif mode=="OWNER_APPROVED_PARALLEL":
        ref=policy.get("parallel_plan")
        if not ref:e.append("parallel mode requires parallel_plan")
        else:
            path=root/ref
            if not path.exists():e.append(f"parallel plan does not exist: {ref}")
            else:
                plan=load_yaml(path);approval=plan.get("owner_approval") or {}
                if approval.get("approved") is not True or approval.get("authority")!="OWNER":e.append("parallel plan lacks explicit OWNER approval")
                if len(plan.get("lanes",[]) or [])<2:e.append("parallel plan requires at least two lanes")
                if not str(plan.get("ascii_topology","")).strip():e.append("parallel plan requires ascii_topology")
    else:e.append(f"unknown execution mode {mode}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
