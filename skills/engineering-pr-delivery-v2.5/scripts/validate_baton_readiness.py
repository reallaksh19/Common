#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from validate_repo_state import validate as repo_state
from validate_repo_profile import validate as repo_profile
from validate_roadmap import validate as roadmap
from validate_execution_frontier import validate as frontier
from validate_serial_execution import validate as execution_policy
from validate_checkpoint_linkage import validate as checkpoint_linkage
from validate_state_planes import validate as state_planes
from validate_roadmap_continuity import validate as continuity
from validate_ep_self_contained import validate as ep_self_contained
from validate_ep_semantics import validate as ep_semantics
from validate_ep_acceptance_mapping import validate as ep_acceptance
from validate_ep_staleness import validate as ep_staleness
from validate_report_contract import validate as report_contract
from validate_parallel_plan import validate as parallel_plan
from validate_question_set import validate as question_sets
from takeoverlib import current_routes


def baton_prerequisite_errors(root:Path)->list[str]:
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");relay_state=state.get("relay_state")
    if relay_state=="INITIALIZING":return ["relay is still INITIALIZING"]
    checks=[("repo_state",repo_state),("repo_profile",repo_profile),("roadmap",roadmap),("frontier",frontier),("execution_policy",execution_policy),("checkpoint_linkage",checkpoint_linkage),("state_planes",state_planes),("roadmap_continuity",continuity),("question_sets",question_sets)]
    if relay_state=="ACTIVE":checks.extend([("ep_self_contained",ep_self_contained),("ep_semantics",ep_semantics),("ep_acceptance",ep_acceptance),("ep_staleness",ep_staleness),("report_contract",report_contract)])
    elif relay_state=="PARALLEL":checks.append(("parallel_plan",parallel_plan))
    errors=[]
    for name,check in checks:
        try:ce,_=check(root)
        except Exception as exc:ce=[str(exc)]
        errors.extend(f"{name}: {x}" for x in ce)
    for route in current_routes(root,state):
        ep=load_yaml(root/str(route.get("ep_path")))
        qb=ep.get("qualification_boundary") or {}
        if qb.get("required") is True and (qb.get("question_policy") or "DEFAULT")=="SUPPRESSED_BY_OWNER":
            errors.append(f"qualification questions suppressed by Owner for {route.get('ep_id')}; baton/takeover readiness remains false until qualification is satisfied or becomes not applicable")
    if state.get("chat_context_required") is not False:errors.append("chat context is required")
    return errors


def expected_baton_ready(root:Path)->tuple[bool,list[str]]:
    errors=baton_prerequisite_errors(root);return not errors,errors


def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml");ready=state.get("relay_readiness") or {}
    for key in ("baton_ready","projection_ready","handover_ready","reasons"):
        if key not in ready:e.append(f"REPO_STATE.relay_readiness missing {key}")
    expected,why=expected_baton_ready(root)
    if ready.get("baton_ready") is not expected:e.append(f"relay_readiness.baton_ready disagrees with semantic baton proof; expected {expected}")
    projection_ready=ready.get("projection_ready")
    if not isinstance(projection_ready,bool):e.append("relay_readiness.projection_ready must be boolean")
    expected_handover=expected and projection_ready is True
    if ready.get("handover_ready") is not expected_handover:e.append("relay_readiness.handover_ready must equal baton_ready AND projection_ready")
    reasons=ready.get("reasons")
    if not isinstance(reasons,list):e.append("relay_readiness.reasons must be a list")
    elif not expected and not reasons:e.append("relay_readiness.reasons must explain why baton_ready is false")
    if not expected:w.extend(f"baton not ready: {x}" for x in why[:10])
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
