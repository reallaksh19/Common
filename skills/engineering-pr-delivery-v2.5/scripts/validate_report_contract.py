#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
MANDATORY=("Executive state","Overall / phase / EP progress","Work completed","Files changed","Acceptance matrix","Tests and evidence","Quality findings","Known limitations","Owner decisions required","GitHub issue changes","Roadmap changes","Exact next actions","Successor EP")

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/s["active_ep"]["path"]);sections=[str(x) for x in (ep.get("report_contract") or {}).get("sections",[]) or []]
    for item in MANDATORY:
        if item not in sections:e.append(f"EP report_contract missing mandatory section: {item}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
