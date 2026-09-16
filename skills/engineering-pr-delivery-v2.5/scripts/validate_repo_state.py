#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require

def validate(repo_root:Path):
    errors=[]; warnings=[]
    try: state=load_yaml(repo_root/"agents/relay/REPO_STATE.yaml")
    except Exception as exc: return [f"REPO_STATE: {exc}"],warnings
    errors+=require(state,["schema_version","repository","roadmap","current_position","execution_policy","active_ep","last_checkpoint","progress","status_planes","chat_context_required"],"REPO_STATE")
    if state.get("schema_version")!="relay-v2.5": errors.append("REPO_STATE: schema_version must be relay-v2.5")
    if state.get("chat_context_required") is not False: errors.append("REPO_STATE: chat_context_required must be false")
    roadmap=state.get("roadmap") or {}; errors+=require(roadmap,["id","revision","path"],"REPO_STATE.roadmap")
    if roadmap.get("path") and not (repo_root/roadmap["path"]).exists(): errors.append(f"REPO_STATE.roadmap.path does not exist: {roadmap['path']}")
    active=state.get("active_ep") or {}; errors+=require(active,["id","path","state"],"REPO_STATE.active_ep")
    if active.get("path") and active.get("state")!="NONE" and not (repo_root/active["path"]).exists(): errors.append(f"REPO_STATE.active_ep.path does not exist: {active['path']}")
    last=state.get("last_checkpoint") or {}; errors+=require(last,["id","path"],"REPO_STATE.last_checkpoint")
    mode=(state.get("execution_policy") or {}).get("mode")
    if mode not in {"SERIAL","OWNER_APPROVED_PARALLEL"}: errors.append("REPO_STATE.execution_policy.mode must be SERIAL or OWNER_APPROVED_PARALLEL")
    if mode=="OWNER_APPROVED_PARALLEL" and not (state.get("execution_policy") or {}).get("parallel_plan"): errors.append("REPO_STATE: parallel execution requires parallel_plan")
    return errors,warnings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("repo_root",nargs="?",default="."); a=ap.parse_args(); e,w=validate(Path(a.repo_root).resolve()); raise SystemExit(print_result(e,w))
if __name__=="__main__": main()
