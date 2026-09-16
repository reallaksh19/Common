#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from validate_repo_state import validate as repo_state
from validate_roadmap import validate as roadmap
from validate_execution_frontier import validate as frontier
from validate_ep_self_contained import validate as ep
from validate_ep_acceptance_mapping import validate as acceptance
from validate_progress import validate as progress
from validate_serial_execution import validate as execution
from validate_phase_transition_questions import validate as questions
from relaylib import print_result
CHECKS=[("repo_state",repo_state),("roadmap",roadmap),("frontier",frontier),("ep_self_contained",ep),("ep_acceptance",acceptance),("progress",progress),("execution_policy",execution),("phase_questions",questions)]

def validate(root:Path):
    e=[];w=[]
    for name,check in CHECKS:
        try:ce,cw=check(root)
        except Exception as exc:ce,cw=[str(exc)],[]
        e.extend(f"{name}: {x}" for x in ce);w.extend(f"{name}: {x}" for x in cw)
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();e,w=validate(Path(a.repo_root).resolve());raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
