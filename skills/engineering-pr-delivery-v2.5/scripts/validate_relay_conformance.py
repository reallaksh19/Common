#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from validate_repo_state import validate as repo_state
from validate_roadmap import validate as roadmap
from validate_execution_frontier import validate as frontier
from validate_ep_self_contained import validate as ep
from validate_ep_acceptance_mapping import validate as acceptance
from validate_ep_staleness import validate as staleness
from validate_report_contract import validate as report_contract
from validate_progress import validate as progress
from validate_serial_execution import validate as execution
from validate_phase_transition_questions import validate as questions
from validate_issue_graph import validate as issue_graph
from validate_issue_closure import validate as issue_closure
from validate_supersession import validate as supersession
from validate_roadmap_transaction import validate as roadmap_transaction
from relaylib import print_result
CHECKS=[("repo_state",repo_state),("roadmap",roadmap),("frontier",frontier),("ep_self_contained",ep),("ep_acceptance",acceptance),("ep_staleness",staleness),("report_contract",report_contract),("progress",progress),("execution_policy",execution),("phase_questions",questions),("issue_graph",issue_graph),("issue_closure",issue_closure),("supersession",supersession),("roadmap_transaction",roadmap_transaction)]

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
