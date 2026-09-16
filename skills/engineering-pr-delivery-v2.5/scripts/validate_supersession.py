#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result

TRANSFER_FIELDS=("unresolved_acceptance","inputs","risks","decisions","evidence")

def key(node):return str(node.get("id",node.get("issue","")))

def validate(root:Path):
    e=[];w=[];g=load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml");nodes={key(n):n for n in g.get("nodes",[]) or []}
    for rel in g.get("relationships",[]) or []:
        if rel.get("relation")!="SUPERSEDES":continue
        new,old=str(rel.get("from","")),str(rel.get("to",""));on=nodes.get(old) or {};nn=nodes.get(new) or {}
        if not on or not nn:continue
        if on.get("state")!="SUPERSEDED":e.append(f"superseded predecessor {old} must have state SUPERSEDED")
        if nn.get("state")=="SUPERSEDED":e.append(f"supersession successor {new} cannot itself be SUPERSEDED by the same transfer")
        transfer=on.get("supersession_receipt") or {}
        if str(transfer.get("successor",""))!=new:e.append(f"superseded predecessor {old} missing successor receipt to {new}")
        for field in TRANSFER_FIELDS:
            if field not in transfer:e.append(f"supersession {old}->{new} missing transfer field {field}")

        inherited=nn.get("supersession_inheritance") or {}
        if str(inherited.get("predecessor",""))!=old:e.append(f"supersession successor {new} missing predecessor inheritance from {old}")
        for field in TRANSFER_FIELDS:
            if field not in inherited:
                e.append(f"supersession successor {new} missing inherited field {field}")
            elif field in transfer and inherited.get(field)!=transfer.get(field):
                e.append(f"supersession {old}->{new} transfer mismatch for {field}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
