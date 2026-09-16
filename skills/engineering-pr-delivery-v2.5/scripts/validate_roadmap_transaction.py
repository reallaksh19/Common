#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
CLASSES={"EXECUTION_DERIVED_STATUS","ENGINEERING_DISCOVERY_PROPOSAL","OWNER_INTENT_MUTATION"}

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);meta=r.get("roadmap") or {};record=meta.get("revision_record")
    if not record:return e,["current roadmap does not declare revision_record; transaction audit is not available"]
    path=root/record
    if not path.exists():return [f"roadmap revision_record missing: {record}"],w
    rev=load_yaml(path);info=rev.get("revision") or {}
    if info.get("to_revision")!=meta.get("revision"):e.append("roadmap revision record to_revision != current roadmap revision")
    if info.get("classification") not in CLASSES:e.append(f"invalid roadmap revision classification {info.get('classification')}")
    changes=rev.get("changes") or {}
    for k in ("added","removed","changed","unaffected"):
        if k not in changes:e.append(f"roadmap revision missing changes.{k}")
    if info.get("classification")=="OWNER_INTENT_MUTATION":
        trigger=info.get("trigger") or {}
        if trigger.get("type")!="OWNER_DECISION":e.append("OWNER_INTENT_MUTATION revision must be triggered by OWNER_DECISION")
        ref=trigger.get("path") or trigger.get("ref")
        if not ref:e.append("OWNER_INTENT_MUTATION revision requires ODR reference")
        elif isinstance(ref,str) and ref.endswith((".yaml",".yml")):
            p=root/ref
            if not p.exists():e.append(f"referenced ODR does not exist: {ref}")
            elif (load_yaml(p).get("status"))!="APPLIED":e.append(f"referenced ODR is not APPLIED: {ref}")
    if "progress_basis_change" not in rev:e.append("roadmap revision missing progress_basis_change")
    if "frontier_after" not in rev:e.append("roadmap revision missing frontier_after")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
