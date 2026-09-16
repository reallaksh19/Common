#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from validate_relay_conformance import validate as relay

def validate(root:Path):
    e,w=relay(root)
    if e:return e,w
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/s["active_ep"]["path"]);c=ep.get("context_capsule") or {}
    for key in ("product_goal","roadmap_position","why_this_work_exists","current_architecture","current_implementation_state"):
        if not str(c.get(key,"")).strip():e.append(f"cold start: context_capsule.{key} must be non-empty")
    out=ep.get("outcome") or {}
    if not any(out.get(k) for k in ("user_visible","engineering")):e.append("cold start: EP outcome is empty")
    if not (ep.get("scope") or {}).get("allowed"):e.append("cold start: scope.allowed is empty; executable change domain is unclear")
    if not ep.get("implementation_plan"):e.append("cold start: implementation_plan is empty")
    if not (ep.get("report_contract") or {}).get("sections"):e.append("cold start: exact report sections are missing")
    if s.get("chat_context_required") is not False:e.append("cold start: repository declares chat context required")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();e,w=validate(Path(a.repo_root).resolve());raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
