#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import compute_frontier,index_roadmap,iter_work_packages,load_yaml,print_result
from validate_roadmap_continuity import validate as validate_continuity

def validate(root:Path):
    e=[];w=[]
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    r=load_yaml(root/s["roadmap"]["path"])
    f=compute_frontier(r)
    mode=(s.get("execution_policy") or {}).get("mode")
    relay_state=s.get("relay_state")
    active=s.get("active_ep") or {}

    if relay_state=="ACTIVE":
        if mode!="SERIAL":e.append("ACTIVE relay requires SERIAL execution mode")
        if len(f)!=1:e.append(f"ACTIVE SERIAL relay requires exactly one executable frontier node; found {f}")
        cur=(s.get("current_position") or {}).get("work_package")
        if len(f)==1 and cur!=f[0]:e.append(f"REPO_STATE current work package {cur} != computed frontier {f[0]}")
    elif relay_state=="PARALLEL":
        if mode!="OWNER_APPROVED_PARALLEL":e.append("PARALLEL relay requires OWNER_APPROVED_PARALLEL mode")
        if len(f)<2:e.append(f"PARALLEL relay requires at least two computed frontier nodes; found {f}")
        declared=set((s.get("current_position") or {}).get("work_packages") or [])
        if declared!=set(f):e.append(f"parallel current_position.work_packages {sorted(declared)} != computed frontier {sorted(f)}")
    elif relay_state in {"INITIALIZING","IDLE","TERMINAL"}:
        if f:e.append(f"{relay_state} relay requires empty executable frontier; found {f}")
    else:
        e.append(f"unknown relay_state {relay_state}")

    objectives,phases,idx=index_roadmap(r)
    for _,_,wp in iter_work_packages(r):
        wid=wp.get("id")
        declared=wp.get("execution_status")
        if wid in f and declared not in {"EXECUTABLE","ACTIVE"}:
            e.append(f"{wid}: computed frontier node must declare EXECUTABLE or ACTIVE, found {declared}")
        if relay_state=="ACTIVE" and wid not in f and declared in {"EXECUTABLE","ACTIVE"}:
            e.append(f"{wid}: non-frontier node cannot declare {declared} under ACTIVE SERIAL relay")

    if relay_state=="ACTIVE":
        ep=load_yaml(root/active["path"])
        identity=ep.get("identity") or {};source=ep.get("roadmap_source") or {}
        if identity.get("ep_id")!=active.get("id"):e.append("active EP id does not match EP.identity.ep_id")
        if source.get("roadmap_id")!=(s.get("roadmap") or {}).get("id"):e.append("active EP roadmap_id does not match REPO_STATE")
        if source.get("roadmap_revision")!=(s.get("roadmap") or {}).get("revision"):
            ce,cw=validate_continuity(root);e.extend(ce);w.extend(cw)
        swp=source.get("work_package")
        if swp not in idx:e.append(f"active EP references missing roadmap work package {swp}")
        else:
            obj,phase,_=idx[swp]
            if source.get("objective")!=obj.get("id") or source.get("phase")!=phase.get("id"):e.append("active EP roadmap hierarchy does not match work package parentage")
        current=s.get("current_position") or {}
        for key in ("objective","phase","work_package"):
            if source.get(key)!=current.get(key):e.append(f"active EP roadmap_source.{key} does not match REPO_STATE current_position")
        if source.get("generated_from_frontier") is not True:e.append("active EP must declare generated_from_frontier: true")
        if f and swp!=f[0]:e.append(f"active EP work package {swp} is not current frontier {f[0]}")
    elif active.get("state") not in {"NONE","ROUTER"}:
        e.append(f"relay_state {relay_state} cannot expose singular active EP state {active.get('state')}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
