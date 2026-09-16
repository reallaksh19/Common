#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");policy=s.get("execution_policy") or {};mode=policy.get("mode");relay_state=s.get("relay_state")
    if mode=="SERIAL":
        if relay_state=="PARALLEL":e.append("SERIAL execution cannot use relay_state PARALLEL")
        if policy.get("parallel_plan"):e.append("SERIAL execution must not declare parallel_plan")
    elif mode=="OWNER_APPROVED_PARALLEL":
        if relay_state!="PARALLEL":e.append("OWNER_APPROVED_PARALLEL requires relay_state PARALLEL")
        ref=policy.get("parallel_plan")
        if not ref:e.append("parallel mode requires parallel_plan")
        elif not (root/ref).exists():e.append(f"parallel plan does not exist: {ref}")
    else:e.append(f"unknown execution mode {mode}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
