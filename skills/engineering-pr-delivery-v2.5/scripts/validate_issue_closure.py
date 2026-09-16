#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import index_roadmap,load_yaml,print_result

def validate(root:Path):
    e=[];w=[];g=load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml");s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);_,_,wps=index_roadmap(r)
    for n in g.get("nodes",[]) or []:
        if n.get("state")!="CLOSED":continue
        label=str(n.get("id",n.get("issue","?")));rn=n.get("roadmap_node");receipt=n.get("closure_receipt") or {}
        if rn in wps and wps[rn][2].get("state") not in {"COMPLETE","SUPERSEDED","CANCELLED"}:e.append(f"closed issue {label} maps to non-terminal roadmap node {rn}")
        for k in ("acceptance_terminal","evidence_terminal","pr_disposition","remaining_work_disposition","checkpoint"):
            if k not in receipt:e.append(f"closed issue {label} missing closure_receipt.{k}")
        if receipt.get("acceptance_terminal") is not True:e.append(f"closed issue {label} acceptance is not terminal")
        if receipt.get("evidence_terminal") is not True:e.append(f"closed issue {label} evidence is not terminal")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
