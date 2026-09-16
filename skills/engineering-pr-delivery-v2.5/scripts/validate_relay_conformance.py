#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from validate_repo_state import validate as repo_state
from validate_roadmap import validate as roadmap
from validate_execution_frontier import validate as frontier
from validate_ep_self_contained import validate as ep
from validate_ep_acceptance_mapping import validate as acceptance
from validate_ep_staleness import validate as staleness
from validate_report_contract import validate as report_contract
from validate_progress import validate as progress
from validate_serial_execution import validate as execution
from validate_parallel_plan import validate as parallel_plan
from validate_parallel_join import validate as parallel_join
from validate_parallel_replan import validate as parallel_replan
from validate_roadmap_continuity import validate as roadmap_continuity
from validate_phase_transition_questions import validate as questions
from validate_issue_graph import validate as issue_graph
from validate_issue_closure import validate as issue_closure
from validate_supersession import validate as supersession
from validate_roadmap_transaction import validate as roadmap_transaction
from validate_owner_decision import validate as owner_decisions
from validate_state_planes import validate as state_planes
from validate_checkpoint_linkage import validate as checkpoint_linkage
from validate_projection_convergence import validate as projection
from validate_drift_receipt import validate as drift

ALWAYS=[("repo_state",repo_state),("roadmap",roadmap),("frontier",frontier),("progress",progress),("execution_policy",execution),("parallel_plan",parallel_plan),("parallel_join",parallel_join),("parallel_replan",parallel_replan),("roadmap_continuity",roadmap_continuity),("state_planes",state_planes),("projection",projection),("drift",drift),("checkpoint_linkage",checkpoint_linkage),("owner_decisions",owner_decisions),("issue_graph",issue_graph),("issue_closure",issue_closure),("supersession",supersession),("roadmap_transaction",roadmap_transaction)]
ACTIVE_EP_ONLY=[("ep_self_contained",ep),("ep_acceptance",acceptance),("ep_staleness",staleness),("report_contract",report_contract),("phase_questions",questions)]

def validate(root:Path):
    e=[];w=[]
    try:s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    except Exception as exc:return [f"repo_state: {exc}"],w
    checks=list(ALWAYS)
    if s.get("relay_state")=="ACTIVE":checks[3:3]=ACTIVE_EP_ONLY
    for name,check in checks:
        try:ce,cw=check(root)
        except Exception as exc:ce,cw=[str(exc)],[]
        e.extend(f"{name}: {x}" for x in ce);w.extend(f"{name}: {x}" for x in cw)
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();e,w=validate(Path(a.repo_root).resolve());raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
