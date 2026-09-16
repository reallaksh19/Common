#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,pct,print_result

def bucket(name,b,e):
    earned,total,percent=b.get("earned_weight"),b.get("total_weight"),b.get("percent")
    if not all(isinstance(x,(int,float)) for x in (earned,total,percent)):e.append(f"{name}: earned_weight, total_weight and percent must be numeric");return
    if earned<0 or total<0 or earned>total:e.append(f"{name}: invalid weights {earned}/{total}");return
    expected=pct(earned,total)
    if abs(float(percent)-expected)>.01:e.append(f"{name}: percent {percent} != calculated {expected}")

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");p=load_yaml(root/"agents/relay/roadmap/PROGRESS.yaml")
    if (p.get("progress_basis") or {}).get("roadmap_revision")!=s["roadmap"]["revision"]:e.append("PROGRESS basis roadmap_revision does not match REPO_STATE")
    bucket("overall",p.get("overall") or {},e)
    for group in ("objectives","phases","work_packages","execution_packages"):
        for item in p.get(group,[]) or []:bucket(f"{group}:{item.get('id','?')}",item,e)
    if isinstance((p.get("overall") or {}).get("percent"),(int,float)) and abs(float(s["progress"]["overall_percent"])-float(p["overall"]["percent"]))>.01:e.append("REPO_STATE overall_percent does not match PROGRESS")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
