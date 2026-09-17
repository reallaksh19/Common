#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from validate_question_set import validate as validate_question_sets


def validate(root:Path):
    """Compatibility entrypoint for the pre-WP-03 validator name.

    WP-03 replaces inline phase_transition.questions with an EP
    qualification_boundary that references a durable QSET-* object. This
    wrapper rejects the old inline contract and delegates to the strong
    question-set validator.
    """
    e=[];w=[]
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    if state.get("relay_state")=="ACTIVE":
        ep=load_yaml(root/(state.get("active_ep") or {})["path"])
        legacy=ep.get("phase_transition")
        if legacy and legacy.get("required") is True:
            e.append("inline phase_transition questions are retired; use qualification_boundary -> QSET-* -> QUAL-*")
    ce,cw=validate_question_sets(root);e.extend(ce);w.extend(cw)
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
