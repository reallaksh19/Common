#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import VALID_DEFINITIONS,VALID_EXECUTION_STATUS,VALID_NODE_STATES,index_roadmap,iter_work_packages,load_yaml,print_result,require

def validate_roadmap_data(r):
    e=[]; w=[]; e+=require(r,["schema_version","roadmap","objectives"],"ROADMAP")
    if r.get("schema_version")!="relay-v2.5": e.append("ROADMAP: schema_version must be relay-v2.5")
    e+=require(r.get("roadmap") or {},["id","revision","title"],"ROADMAP.roadmap")
    ids=set()
    for obj in r.get("objectives",[]) or []:
        for node,label in ((obj,"objective"),):
            nid=node.get("id")
            if not nid: e.append(f"ROADMAP: {label} missing id"); continue
            if nid in ids: e.append(f"ROADMAP: duplicate id {nid}")
            ids.add(nid)
            if node.get("state") not in VALID_NODE_STATES: e.append(f"{nid}: invalid state {node.get('state')}")
            if node.get("definition") not in VALID_DEFINITIONS: e.append(f"{nid}: invalid definition {node.get('definition')}")
        for ph in obj.get("phases",[]) or []:
            pid=ph.get("id")
            if not pid: e.append(f"{obj.get('id')}: phase missing id"); continue
            if pid in ids: e.append(f"ROADMAP: duplicate id {pid}")
            ids.add(pid)
            if ph.get("state") not in VALID_NODE_STATES: e.append(f"{pid}: invalid state {ph.get('state')}")
            if ph.get("definition") not in VALID_DEFINITIONS: e.append(f"{pid}: invalid definition {ph.get('definition')}")
            for wp in ph.get("work_packages",[]) or []:
                wid=wp.get("id")
                if not wid: e.append(f"{pid}: work package missing id"); continue
                if wid in ids: e.append(f"ROADMAP: duplicate id {wid}")
                ids.add(wid)
                if wp.get("state") not in VALID_NODE_STATES: e.append(f"{wid}: invalid state {wp.get('state')}")
                if wp.get("definition") not in VALID_DEFINITIONS: e.append(f"{wid}: invalid definition {wp.get('definition')}")
                if wp.get("execution_status") not in VALID_EXECUTION_STATUS: e.append(f"{wid}: invalid execution_status {wp.get('execution_status')}")
    _,_,idx=index_roadmap(r)
    for _,_,wp in iter_work_packages(r):
        wid=wp.get("id","?")
        for dep in wp.get("depends_on",[]) or []:
            if dep not in idx: e.append(f"{wid}: dependency does not exist: {dep}")
            if dep==wid: e.append(f"{wid}: work package cannot depend on itself")
        if wp.get("state") in {"COMPLETE","SUPERSEDED","CANCELLED"} and wp.get("execution_status") in {"EXECUTABLE","ACTIVE"}: e.append(f"{wid}: terminal/superseded state cannot be executable/active")
        if wp.get("execution_status")=="EXECUTABLE" and wp.get("definition")!="DETAILED": e.append(f"{wid}: executable work package must be DETAILED")
    visiting=set(); visited=set()
    def dfs(wid):
        if wid in visiting: e.append(f"ROADMAP: dependency cycle includes {wid}"); return
        if wid in visited or wid not in idx: return
        visiting.add(wid)
        for dep in idx[wid][2].get("depends_on",[]) or []: dfs(dep)
        visiting.remove(wid); visited.add(wid)
    for wid in idx: dfs(wid)
    return e,w

def validate(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml"); return validate_roadmap_data(load_yaml(root/s["roadmap"]["path"]))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("repo_root",nargs="?",default="."); a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__": main()
