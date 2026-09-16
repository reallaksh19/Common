#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result

FOCUS={
    "Q1":"PRODUCTION_PATH",
    "Q2":"ENGINEERING_PROBLEM",
    "Q3":"BOUNDARIES_INVARIANTS",
    "Q4":"VERIFICATION",
    "Q5":"FIRST_SAFE_SLICE",
}

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/s["active_ep"]["path"]);tr=ep.get("phase_transition")
    if not tr or tr.get("required") is not True:return e,w
    src=ep.get("roadmap_source") or {}
    if not tr.get("from_phase") or not tr.get("to_phase"):e.append("phase transition requires from_phase and to_phase")
    if tr.get("from_phase")==tr.get("to_phase"):e.append("phase transition from_phase and to_phase must differ")
    if tr.get("to_phase")!=src.get("phase"):e.append("phase transition to_phase must equal incoming EP roadmap_source.phase")

    qs=tr.get("questions") or []
    if len(qs)!=5:return [*e,f"phase transition requires exactly 5 questions; found {len(qs)}"],w

    valid_anchors={str(x) for x in (src.get("phase"),src.get("work_package")) if x}
    for group in ("acceptance","validation","inputs","implementation_plan"):
        valid_anchors|={str(x.get("id")) for x in ep.get(group,[]) or [] if isinstance(x,dict) and x.get("id")}

    for i,q in enumerate(qs,1):
        qid=f"Q{i}"
        if not isinstance(q,dict):
            e.append(f"phase-transition question {i} must be a mapping")
            continue
        if q.get("id")!=qid:e.append(f"phase-transition question {i} must have id {qid}")
        if q.get("focus")!=FOCUS[qid]:e.append(f"{qid} focus must be {FOCUS[qid]}")
        if not str(q.get("question","")).strip():e.append(f"{qid} question text must be explicit")
        anchors=q.get("anchors")
        if not isinstance(anchors,list) or not anchors:
            e.append(f"{qid} must declare at least one incoming-EP anchor")
            continue
        unknown=[str(a) for a in anchors if str(a) not in valid_anchors]
        if unknown:e.append(f"{qid} contains anchors not present in incoming EP: {', '.join(unknown)}")

    q4=qs[3] if len(qs)>3 and isinstance(qs[3],dict) else {}
    if not any(str(a).startswith(("TEST-","AC-")) for a in q4.get("anchors",[]) or []):
        e.append("Q4 must anchor to incoming verification or acceptance IDs")
    q5=qs[4] if len(qs)>4 and isinstance(qs[4],dict) else {}
    if not any(str(a).startswith(("STEP-","AC-")) for a in q5.get("anchors",[]) or []):
        e.append("Q5 must anchor to an incoming implementation step or acceptance ID")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
