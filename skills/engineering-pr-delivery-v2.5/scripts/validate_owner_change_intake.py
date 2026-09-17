#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from owner_change_projection import build,_find_revision_for_odr,_current_odr_path

REQ_INTAKE=("previous_concept","requested_concept","retained_behavior","invalidated_behavior","new_scope")

def _validate_intake(path:Path,odr:dict):
    e=[];intake=odr.get("change_intake")
    if not isinstance(intake,dict):return ["INTENT_MUTATION ODR requires change_intake for Owner-facing change projection"]
    for key in REQ_INTAKE:
        if key not in intake:e.append(f"change_intake.{key} is required")
    for key in ("previous_concept","requested_concept"):
        if not str(intake.get(key,"")).strip():e.append(f"change_intake.{key} must be concrete")
    for key in ("retained_behavior","invalidated_behavior","new_scope"):
        if not isinstance(intake.get(key),list):e.append(f"change_intake.{key} must be a list")
        elif any(not str(x).strip() for x in intake.get(key) or []):e.append(f"change_intake.{key} entries must be concrete")
    if not any(intake.get(k) for k in ("retained_behavior","invalidated_behavior","new_scope")):
        e.append("change_intake must state at least one retained, invalidated, or new-scope item")
    return e


def validate(root:Path):
    e=[];w=[];root=root.resolve();base=root/"agents/relay/roadmap/owner-decisions"
    if base.exists():
        for path in sorted(list(base.glob("*.yaml"))+list(base.glob("*.yml"))):
            odr=load_yaml(path);kind=((odr.get("decision") or {}).get("kind"))
            if kind=="INTENT_MUTATION" and odr.get("change_intake") is not None:
                e.extend(f"{path.name}: {x}" for x in _validate_intake(path,odr))
                if odr.get("status")=="APPLIED":
                    matches=_find_revision_for_odr(root,path)
                    if len(matches)!=1:e.append(f"{path.name}: APPLIED change_intake ODR must bind exactly one roadmap revision; found {len(matches)}")
                    elif ((matches[0][1].get("revision") or {}).get("classification"))!="OWNER_INTENT_MUTATION":e.append(f"{path.name}: bound revision must be OWNER_INTENT_MUTATION")
    current=_current_odr_path(root)
    if current:
        odr=load_yaml(current);e.extend(f"current Owner change: {x}" for x in _validate_intake(current,odr))
        p=build(root,current)
        d=p.get("decision") or {}
        if not d.get("applied"):e.append("current Owner-intent roadmap revision requires APPLIED ODR")
        if not d.get("applied_to_current_roadmap"):e.append("Owner change projection is not bound to current roadmap revision")
        if p.get("new_frontier")!=p.get("current_frontier"):e.append("Owner change projection new_frontier does not equal computed current frontier")
        pb=p.get("progress_basis_effect") or {}
        if str(pb.get("new_basis"))!=str(pb.get("current_basis")):e.append("Owner change projection progress basis is stale")
        disp=p.get("current_ep_disposition") or {}
        if disp.get("disposition")=="UNCLASSIFIED":e.append("Owner change must explicitly classify the active EP/work package as changed, removed, unaffected, or invalidated")
        impact=p.get("issue_impact") or {};affected=impact.get("affected") or []
        if affected and impact.get("issue_graph_reconciled") is not True:e.append("Owner change affecting issues requires issue_graph_reconciled: true")
        if impact.get("issue_graph_reconciled") not in {True,False}:e.append("Owner change revision must declare boolean issue_graph_reconciled")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
