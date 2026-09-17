#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,pct,print_result

GROUPS=("objectives","phases","work_packages","execution_packages","implementation_steps","acceptance_criteria")

def bucket(name,b,e):
    earned,total,percent=b.get("earned_weight"),b.get("total_weight"),b.get("percent")
    if not all(isinstance(x,(int,float)) for x in (earned,total,percent)):e.append(f"{name}: earned_weight, total_weight and percent must be numeric");return
    if earned<0 or total<0 or earned>total:e.append(f"{name}: invalid weights {earned}/{total}");return
    expected=pct(earned,total)
    if abs(float(percent)-expected)>.01:e.append(f"{name}: percent {percent} != calculated {expected}")

def index(items):return {str(x.get("id")):x for x in (items or []) if isinstance(x,dict) and x.get("id")}

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");p=load_yaml(root/"agents/relay/roadmap/PROGRESS.yaml");r=load_yaml(root/s["roadmap"]["path"])
    if (p.get("progress_basis") or {}).get("roadmap_revision")!=s["roadmap"]["revision"]:e.append("PROGRESS basis roadmap_revision does not match REPO_STATE")
    bucket("overall",p.get("overall") or {},e)
    idx={}
    for group in GROUPS:
        items=p.get(group)
        if not isinstance(items,list):e.append(f"PROGRESS.{group} must be a list");items=[]
        idx[group]=index(items)
        for item in items:bucket(f"{group}:{item.get('id','?')}",item,e)
    roadmap_ids={"objectives":set(),"phases":set(),"work_packages":set()}
    for obj in r.get("objectives",[]) or []:
        roadmap_ids["objectives"].add(str(obj.get("id")))
        for ph in obj.get("phases",[]) or []:
            roadmap_ids["phases"].add(str(ph.get("id")))
            for wp in ph.get("work_packages",[]) or []:roadmap_ids["work_packages"].add(str(wp.get("id")))
    for group in ("objectives","phases","work_packages"):
        missing=roadmap_ids[group]-set(idx[group]);extra=set(idx[group])-roadmap_ids[group]
        if missing:e.append(f"PROGRESS.{group} missing roadmap ids: {', '.join(sorted(missing))}")
        if extra:e.append(f"PROGRESS.{group} contains unknown roadmap ids: {', '.join(sorted(extra))}")
    active=s.get("active_ep") or {}
    if s.get("relay_state")=="ACTIVE" and active.get("path"):
        ep=load_yaml(root/active["path"]);epid=str((ep.get("identity") or {}).get("ep_id"))
        if epid not in idx["execution_packages"]:e.append(f"PROGRESS.execution_packages missing active EP {epid}")
        step_ids={str(x.get("id")) for x in ep.get("implementation_plan",[]) or [] if isinstance(x,dict) and x.get("id")}
        ac_ids={str(x.get("id")) for x in ep.get("acceptance",[]) or [] if isinstance(x,dict) and x.get("id")}
        missing_steps=step_ids-set(idx["implementation_steps"]);missing_ac=ac_ids-set(idx["acceptance_criteria"])
        if missing_steps:e.append(f"PROGRESS.implementation_steps missing active EP steps: {', '.join(sorted(missing_steps))}")
        if missing_ac:e.append(f"PROGRESS.acceptance_criteria missing active EP acceptance ids: {', '.join(sorted(missing_ac))}")
        for aid in ac_ids:
            row=idx["acceptance_criteria"].get(aid) or {};status=row.get("status")
            if status not in {"NOT_STARTED","IN_PROGRESS","COMPLETE","NOT_RUN","FAILED","NA"}:e.append(f"acceptance_criteria:{aid}: invalid status {status}")
            basis=row.get("basis")
            if not isinstance(basis,list):e.append(f"acceptance_criteria:{aid}.basis must be a list")
    mirrors=s.get("progress") or {}
    mirror_map=(("overall_percent",p.get("overall") or {}),("phase_percent",idx["phases"].get(str((s.get("current_position") or {}).get("phase"))) or {}),("ep_percent",idx["execution_packages"].get(str(active.get("id"))) or {}))
    for key,row in mirror_map:
        authoritative=row.get("percent")
        if isinstance(authoritative,(int,float)) and isinstance(mirrors.get(key),(int,float)) and abs(float(mirrors[key])-float(authoritative))>.01:e.append(f"REPO_STATE {key} mirror does not match authoritative PROGRESS")
    if mirrors.get("basis_revision")!=(p.get("progress_basis") or {}).get("id"):e.append("REPO_STATE progress.basis_revision does not match PROGRESS progress_basis.id")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
