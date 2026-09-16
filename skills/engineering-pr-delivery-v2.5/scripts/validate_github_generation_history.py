#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result

NO_RETRY={"VERIFIED","SUPERSEDED","FAILED"}

def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml");projection=state.get("projection") or {}
    if projection.get("adapter")!="GITHUB_ISSUES":return e,w
    current_rel=projection.get("plan")
    if not current_rel:return ["GITHUB_ISSUES projection missing current plan"],w
    current_path=root/current_rel;current=load_yaml(current_path);seen=[];plan=current;path=current_path
    first_prev=str((plan.get("generation") or {}).get("supersedes_generation") or "")
    while True:
        gen=plan.get("generation") or {};gid=str(gen.get("id") or "")
        if gid in seen:e.append("GitHub generation history cycle: "+" -> ".join(seen+[gid]));break
        seen.append(gid)
        prev=str(gen.get("supersedes_generation") or "")
        if not prev:break
        prev_path=path.parent/f"{prev}.yaml"
        if not prev_path.exists():e.append(f"GitHub generation {gid} references missing predecessor generation {prev}");break
        previous=load_yaml(prev_path);pgen=previous.get("generation") or {}
        if str(pgen.get("id") or "")!=prev:e.append(f"historical generation path {prev_path} id mismatch")
        if pgen.get("state")!="SUPERSEDED":e.append(f"historical generation {prev} must be SUPERSEDED")
        for op in previous.get("operations",[]) or []:
            if op.get("state") not in NO_RETRY:e.append(f"historical generation {prev} retains retryable operation {op.get('id')} state {op.get('state')}")
            if op.get("state")=="SUPERSEDED" and not str(op.get("superseded_by") or "").strip():e.append(f"historical superseded operation {op.get('id')} requires superseded_by")
        plan=previous;path=prev_path
    if first_prev:
        observed=(projection.get("observed") or {}).get("operation_id")
        history={str(x.get("operation_id")) for x in (projection.get("superseded_operations") or []) if isinstance(x,dict)}
        if str(observed or "")!=first_prev and first_prev not in history:e.append(f"immediate predecessor generation {first_prev} must be preserved as observed external generation or superseded projection history")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
