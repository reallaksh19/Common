#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/s["active_ep"]["path"]);tr=ep.get("phase_transition")
    if not tr or tr.get("required") is not True:return e,w
    qs=tr.get("questions") or []
    if len(qs)!=5:return [f"phase transition requires exactly 5 questions; found {len(qs)}"],w
    src=ep.get("roadmap_source") or {};anchors={src.get("phase"),src.get("work_package")};anchors|={str(x.get("id")) for x in ep.get("acceptance",[]) or [] if x.get("id")};anchors|={str(x.get("id")) for x in ep.get("validation",[]) or [] if x.get("id")};anchors|={str(x.get("id")) for x in ep.get("inputs",[]) or [] if isinstance(x,dict) and x.get("id")}
    text=" ".join(str(q.get("question",q)) for q in qs);hits=sum(1 for a in anchors if a and a in text)
    if hits<3:e.append("phase-transition Q1-Q5 insufficiently grounded in incoming EP anchors")
    for i,q in enumerate(qs,1):
        if not isinstance(q,dict) or q.get("id")!=f"Q{i}":e.append(f"phase-transition question {i} must have id Q{i}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
