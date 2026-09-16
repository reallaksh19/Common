#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
VALID={"MUST_PASS","SHOULD_RUN","INFORMATIONAL"}

def validate_ep_data(ep:dict,label="EP"):
    e=[];w=[];acs=ep.get("acceptance",[]) or [];tests=ep.get("validation",[]) or [];aids=set();tids=set()
    for ac in acs:
        aid=ac.get("id")
        if not aid:e.append(f"{label}: acceptance criterion missing id");continue
        if aid in aids:e.append(f"{label}: duplicate acceptance id {aid}")
        aids.add(aid);weight=ac.get("weight")
        if not isinstance(weight,(int,float)) or weight<0:e.append(f"{label} {aid}: weight must be non-negative number")
        if not ac.get("verification"):e.append(f"{label} {aid}: no verification mapping")
    for t in tests:
        tid=t.get("id")
        if not tid:e.append(f"{label}: validation item missing id");continue
        if tid in tids:e.append(f"{label}: duplicate validation id {tid}")
        tids.add(tid)
        if t.get("class") not in VALID:e.append(f"{label} {tid}: invalid class {t.get('class')}")
        for aid in t.get("proves",[]) or []:
            if aid not in aids:e.append(f"{label} {tid}: proves unknown acceptance id {aid}")
    for ac in acs:
        for tid in ac.get("verification",[]) or []:
            if tid not in tids and not str(tid).startswith(("BENCH-","REVIEW-","ORACLE-")):e.append(f"{label} {ac.get('id')}: verification target not found: {tid}")
    return e,w

def validate(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/s["active_ep"]["path"]);return validate_ep_data(ep)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
