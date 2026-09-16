#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result

def key(node):return str(node.get("id",node.get("issue","")))
def validate(root:Path):
    e=[];w=[];g=load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml");nodes={key(n):n for n in g.get("nodes",[]) or []}
    for rel in g.get("relationships",[]) or []:
        if rel.get("relation")!="SUPERSEDES":continue
        new,old=str(rel.get("from","")),str(rel.get("to",""));on=nodes.get(old) or {};nn=nodes.get(new) or {}
        if not on or not nn:continue
        if on.get("state")!="SUPERSEDED":e.append(f"superseded predecessor {old} must have state SUPERSEDED")
        transfer=on.get("supersession_receipt") or {}
        if str(transfer.get("successor",""))!=new:e.append(f"superseded predecessor {old} missing successor receipt to {new}")
        for k in ("unresolved_acceptance","inputs","risks","decisions","evidence"):
            if k not in transfer:e.append(f"supersession {old}->{new} missing transfer field {k}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
