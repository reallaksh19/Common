#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import compute_frontier,index_roadmap,load_yaml,print_result
from validate_roadmap_continuity import validate as validate_continuity

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);ep=load_yaml(root/s["active_ep"]["path"]);src=ep.get("roadmap_source") or {};identity=ep.get("identity") or {};_,_,idx=index_roadmap(r)
    if identity.get("execution_state") in {"STALE","SUPERSEDED"}:e.append("active EP is explicitly stale/superseded")
    revision_changed=src.get("roadmap_revision")!=s["roadmap"]["revision"]
    if revision_changed:
        ce,cw=validate_continuity(root);e.extend(ce);w.extend(cw)
    wid=src.get("work_package")
    if wid not in idx:e.append(f"active EP work package missing from roadmap: {wid}")
    else:
        wp=idx[wid][2]
        if wp.get("state") in {"COMPLETE","SUPERSEDED","CANCELLED"}:e.append(f"active EP points to terminal roadmap node {wid}:{wp.get('state')}")
    active_state=(s.get("active_ep") or {}).get("state")
    if wid not in compute_frontier(r) and active_state!="RECONCILING":e.append(f"active EP work package {wid} is no longer on computed frontier")
    anti=ep.get("anti_drift") or {}
    if not anti.get("stale_if"):e.append("EP anti_drift.stale_if must define invalidation conditions")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
