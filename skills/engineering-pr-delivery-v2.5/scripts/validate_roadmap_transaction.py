#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import compute_frontier,load_yaml,print_result
from validate_owner_decision import validate_file as validate_owner_decision_file
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
            else:
                oe,ow=validate_owner_decision_file(p);e.extend(f"referenced ODR: {x}" for x in oe);w.extend(f"referenced ODR: {x}" for x in ow)
                odr=load_yaml(p)
                if odr.get("status")!="APPLIED":e.append(f"referenced ODR is not APPLIED: {ref}")
                if ((odr.get("decision") or {}).get("kind"))!="INTENT_MUTATION":e.append("OWNER_INTENT_MUTATION revision requires ODR decision.kind INTENT_MUTATION")
    change=rev.get("progress_basis_change")
    if not isinstance(change,dict):
        e.append("roadmap revision missing progress_basis_change")
    else:
        progress=load_yaml(root/"agents/relay/roadmap/PROGRESS.yaml");basis=progress.get("progress_basis") or {}
        if str(change.get("new_basis"))!=str(basis.get("id")):e.append("roadmap revision progress_basis_change.new_basis != current PROGRESS basis id")
        if str(basis.get("roadmap_revision"))!=str(meta.get("revision")):e.append("current PROGRESS basis is not bound to current roadmap revision")
        old_total,new_total=change.get("old_total_weight"),change.get("new_total_weight")
        if isinstance(old_total,(int,float)) and isinstance(new_total,(int,float)) and old_total!=new_total and change.get("old_basis")==change.get("new_basis"):
            e.append("changed progress denominator requires a new progress basis id")
    if "frontier_after" not in rev:
        e.append("roadmap revision missing frontier_after")
    elif sorted(str(x) for x in (rev.get("frontier_after") or []))!=sorted(compute_frontier(r)):
        e.append("roadmap revision frontier_after does not match computed current frontier")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
