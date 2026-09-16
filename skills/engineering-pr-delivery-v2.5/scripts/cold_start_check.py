#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from validate_relay_conformance import validate as relay

def _check_ep(ep:dict,label:str,e:list[str]):
    c=ep.get("context_capsule") or {}
    for key in ("product_goal","roadmap_position","why_this_work_exists","current_architecture","current_implementation_state"):
        if not str(c.get(key,"")).strip():e.append(f"cold start {label}: context_capsule.{key} must be non-empty")
    out=ep.get("outcome") or {}
    if not any(out.get(k) for k in ("user_visible","engineering")):e.append(f"cold start {label}: EP outcome is empty")
    if not (ep.get("scope") or {}).get("allowed"):e.append(f"cold start {label}: scope.allowed is empty; executable change domain is unclear")
    if not ep.get("implementation_plan"):e.append(f"cold start {label}: implementation_plan is empty")
    if not (ep.get("report_contract") or {}).get("sections"):e.append(f"cold start {label}: exact report sections are missing")

def validate(root:Path):
    e,w=relay(root)
    if e:return e,w
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    if s.get("chat_context_required") is not False:e.append("cold start: repository declares chat context required")
    relay_state=s.get("relay_state")
    if relay_state=="ACTIVE":
        ep=load_yaml(root/s["active_ep"]["path"]);_check_ep(ep,"active EP",e)
    elif relay_state=="PARALLEL":
        plan=load_yaml(root/(s.get("execution_policy") or {})["parallel_plan"])
        for lane in plan.get("lanes",[]) or []:
            ep_path=lane.get("ep_path")
            if ep_path and (root/ep_path).exists():_check_ep(load_yaml(root/ep_path),f"lane {lane.get('id')}",e)
    elif relay_state not in {"INITIALIZING","IDLE","TERMINAL"}:
        e.append(f"cold start: unknown relay_state {relay_state}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();e,w=validate(Path(a.repo_root).resolve());raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
