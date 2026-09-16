#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from validate_repo_state import validate as repo_state
from validate_repo_profile import validate as repo_profile
from validate_roadmap import validate as roadmap
from validate_execution_frontier import validate as frontier
from validate_ep_self_contained import validate as ep
from validate_ep_semantics import validate as ep_semantics
from validate_ep_acceptance_mapping import validate as acceptance
from validate_ep_staleness import validate as staleness
from validate_report_contract import validate as report_contract
from validate_report_projection import validate as report_projection
from validate_human_communication import validate as human_communication
from validate_progress import validate as progress
from validate_serial_execution import validate as execution
from validate_parallel_plan import validate as parallel_plan
from validate_parallel_join import validate as parallel_join
from validate_parallel_replan import validate as parallel_replan
from validate_roadmap_continuity import validate as roadmap_continuity
from validate_phase_transition_questions import validate as questions
from validate_question_set import validate as question_sets
from validate_qualification_receipt import validate as qualifications
from validate_issue_graph import validate as issue_graph
from validate_issue_projection_tree import validate as issue_projection_tree
from validate_issue_closure import validate as issue_closure
from validate_supersession import validate as supersession
from validate_roadmap_transaction import validate as roadmap_transaction
from validate_owner_decision import validate as owner_decisions
from validate_state_planes import validate as state_planes
from validate_checkpoint_linkage import validate as checkpoint_linkage
from validate_projection_convergence import validate as projection
from validate_github_projection import validate as github_projection
from validate_github_generation_history import validate as github_generation_history
from validate_drift_receipt import validate as drift
from validate_takeover_certification import validate as takeover
from validate_baton_readiness import validate as baton_readiness
from validate_blueprints import validate as blueprints
from validate_quality_router import validate as quality_router
from validate_quality_review import validate as quality_review

ALWAYS=[("repo_state",repo_state),("repo_profile",repo_profile),("roadmap",roadmap),("frontier",frontier),("progress",progress),("report_projection",report_projection),("human_communication",human_communication),("execution_policy",execution),("parallel_plan",parallel_plan),("parallel_join",parallel_join),("parallel_replan",parallel_replan),("roadmap_continuity",roadmap_continuity),("state_planes",state_planes),("projection",projection),("github_projection",github_projection),("github_generation_history",github_generation_history),("drift",drift),("checkpoint_linkage",checkpoint_linkage),("owner_decisions",owner_decisions),("issue_graph",issue_graph),("issue_projection_tree",issue_projection_tree),("issue_closure",issue_closure),("supersession",supersession),("roadmap_transaction",roadmap_transaction),("question_sets",question_sets),("qualifications",qualifications),("takeover",takeover),("quality_blueprints",blueprints),("quality_router",quality_router),("quality_review",quality_review)]
ACTIVE_EP_ONLY=[("ep_self_contained",ep),("ep_semantics",ep_semantics),("ep_acceptance",acceptance),("ep_staleness",staleness),("report_contract",report_contract),("phase_questions_compat",questions)]

def validate(root:Path):
    e=[];w=[]
    try:s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    except Exception as exc:return [f"repo_state: {exc}"],w
    checks=list(ALWAYS)
    if s.get("relay_state")=="ACTIVE":checks.extend(ACTIVE_EP_ONLY)
    checks.append(("baton_readiness",baton_readiness))
    for name,check in checks:
        try:ce,cw=check(root)
        except Exception as exc:ce,cw=[str(exc)],[]
        e.extend(f"{name}: {x}" for x in ce);w.extend(f"{name}: {x}" for x in cw)
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();e,w=validate(Path(a.repo_root).resolve());raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
