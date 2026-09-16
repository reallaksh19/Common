#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require,scan_context_phrases
REQ=["schema_version","identity","roadmap_source","outcome","context_capsule","repository_discovery","inputs","benchmarks","scope","anti_drift","implementation_plan","quality","acceptance","validation","failure_and_stop_conditions","report_contract","checkpoint_contract","successor_relay"]

def validate_ep_data(root:Path,ep:dict,label="EP"):
    e=[];w=[];e+=require(ep,REQ,label)
    if ep.get("schema_version")!="relay-v2.5":e.append(f"{label}: schema_version must be relay-v2.5")
    e+=[f"{label}{x[1:]}" if x.startswith("$") else f"{label}: {x}" for x in scan_context_phrases(ep)]
    e+=require(ep.get("identity") or {},["ep_id","branch","execution_state","previous_checkpoint"],f"{label}.identity")
    e+=require(ep.get("roadmap_source") or {},["roadmap_id","roadmap_revision","objective","phase","work_package"],f"{label}.roadmap_source")
    e+=require(ep.get("scope") or {},["allowed","prohibited"],f"{label}.scope")
    if not ep.get("repository_discovery"):e.append(f"{label}.repository_discovery must contain at least one concrete step")
    if not ep.get("acceptance"):e.append(f"{label}.acceptance must contain at least one criterion")
    suc=ep.get("successor_relay") or {}
    if suc.get("required") is not True:e.append(f"{label}.successor_relay.required must be true")
    duties=suc.get("duties") or []
    for expected in ("compute next executable frontier","run cold-start check","update REPO_STATE"):
        if not any(expected.lower() in str(d).lower() for d in duties):e.append(f"{label}.successor_relay missing duty: {expected}")
    for step in ep.get("repository_discovery",[]) or []:
        targets=([step["target"]] if step.get("target") else [])+(step.get("targets",[]) or [])
        for target in targets:
            if isinstance(target,str) and target.startswith("agents/relay/") and not any(c in target for c in "*?[") and not (root/target).exists():e.append(f"{label} discovery target does not exist: {target}")
    return e,w

def validate(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/s["active_ep"]["path"]);return validate_ep_data(root,ep)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
