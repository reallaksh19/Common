#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import compute_frontier,index_roadmap,load_yaml,print_result

def validate(root:Path):
    e=[]; w=[]; s=load_yaml(root/"agents/relay/REPO_STATE.yaml"); r=load_yaml(root/s["roadmap"]["path"]); f=compute_frontier(r); mode=s["execution_policy"]["mode"]
    if mode=="SERIAL":
        if len(f)!=1: e.append(f"SERIAL execution requires exactly one executable frontier node; found {f}")
        cur=(s.get("current_position") or {}).get("work_package")
        if len(f)==1 and cur!=f[0]: e.append(f"REPO_STATE current work package {cur} != computed frontier {f[0]}")
    elif mode=="OWNER_APPROVED_PARALLEL" and len(f)<2: w.append(f"parallel mode has fewer than two executable frontier nodes: {f}")
    _,_,idx=index_roadmap(r); active=s.get("active_ep") or {}
    if active.get("state")!="NONE":
        ep=load_yaml(root/active["path"]); swp=(ep.get("roadmap_source") or {}).get("work_package")
        if swp not in idx: e.append(f"active EP references missing roadmap work package {swp}")
        if mode=="SERIAL" and f and swp!=f[0]: e.append(f"active EP work package {swp} is not current frontier {f[0]}")
        if (ep.get("roadmap_source") or {}).get("roadmap_revision")!=(s.get("roadmap") or {}).get("revision"): e.append("active EP roadmap revision does not match REPO_STATE roadmap revision")
    return e,w

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("repo_root",nargs="?",default="."); a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
