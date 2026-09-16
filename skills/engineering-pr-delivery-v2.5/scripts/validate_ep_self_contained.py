#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require,scan_context_phrases
REQ=["schema_version","identity","roadmap_source","outcome","context_capsule","repository_discovery","inputs","benchmarks","scope","anti_drift","implementation_plan","quality","acceptance","validation","failure_and_stop_conditions","report_contract","checkpoint_contract","successor_relay"]

def validate(root:Path):
    e=[]; w=[]; s=load_yaml(root/"agents/relay/REPO_STATE.yaml"); ep=load_yaml(root/s["active_ep"]["path"]); e+=require(ep,REQ,"EP")
    if ep.get("schema_version")!="relay-v2.5":e.append("EP: schema_version must be relay-v2.5")
    e+=scan_context_phrases(ep); e+=require(ep.get("identity") or {},["ep_id","branch","execution_state"],"EP.identity"); e+=require(ep.get("roadmap_source") or {},["roadmap_id","roadmap_revision","objective","phase","work_package"],"EP.roadmap_source"); e+=require(ep.get("scope") or {},["allowed","prohibited"],"EP.scope")
    if not ep.get("repository_discovery"):e.append("EP.repository_discovery must contain at least one concrete step")
    if not ep.get("acceptance"):e.append("EP.acceptance must contain at least one criterion")
    suc=ep.get("successor_relay") or {}
    if suc.get("required") is not True:e.append("EP.successor_relay.required must be true")
    duties=suc.get("duties") or []
    for expected in ("compute next executable frontier","run cold-start check","update REPO_STATE"):
        if not any(expected.lower() in str(d).lower() for d in duties):e.append(f"EP.successor_relay missing duty: {expected}")
    for step in ep.get("repository_discovery",[]) or []:
        targets=([step["target"]] if step.get("target") else [])+(step.get("targets",[]) or [])
        for target in targets:
            if isinstance(target,str) and target.startswith("agents/relay/") and not any(c in target for c in "*?[") and not (root/target).exists():e.append(f"EP discovery target does not exist: {target}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
