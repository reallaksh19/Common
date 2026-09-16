#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml, print_result, require

PROJECTION_STATES={"NOT_REQUIRED","PENDING","PUBLISHED_UNCONFIRMED","IN_SYNC","STALE"}
NONE_VALUES={None,""}


def expected_execution_ref(root:Path,state:dict):
    relay_state=state.get("relay_state")
    if relay_state=="ACTIVE":return str((state.get("active_ep") or {}).get("id") or "NONE")
    if relay_state=="PARALLEL":
        ref=(state.get("execution_policy") or {}).get("parallel_plan")
        if not ref:return "NONE"
        plan=load_yaml(root/ref)
        return str(plan.get("id") or "NONE")
    return "NONE"


def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    projection=s.get("projection") or {};ready=s.get("relay_readiness") or {}
    e+=require(projection,["required","state","operation_id","target","roadmap_revision","execution_ref","receipt","basis"],"REPO_STATE.projection")
    e+=require(ready,["repository_ready","projection_ready","handover_ready","reasons"],"REPO_STATE.relay_readiness")
    required=projection.get("required")
    if not isinstance(required,bool):e.append("projection.required must be boolean")
    pstate=projection.get("state")
    if pstate not in PROJECTION_STATES:e.append(f"projection.state invalid: {pstate}")
    operation_id=projection.get("operation_id");target=projection.get("target");receipt=projection.get("receipt")

    if required is False:
        if pstate!="NOT_REQUIRED":e.append("projection.required=false requires state NOT_REQUIRED")
        if operation_id not in NONE_VALUES or target not in NONE_VALUES or receipt not in NONE_VALUES:e.append("NOT_REQUIRED projection must not declare operation_id, target, or receipt")
    elif required is True:
        if pstate=="NOT_REQUIRED":e.append("projection.required=true cannot use state NOT_REQUIRED")
        if not str(operation_id or "").strip():e.append("required projection needs stable operation_id before publication")
        if not str(target or "").strip():e.append("required projection needs durable target")

    expected_projection_ready=(required is False) or pstate=="IN_SYNC"
    if ready.get("projection_ready") is not expected_projection_ready:e.append("relay_readiness.projection_ready disagrees with projection state")
    expected_repository_ready=s.get("relay_state")!="INITIALIZING"
    if ready.get("repository_ready") is not expected_repository_ready:e.append("relay_readiness.repository_ready disagrees with relay lifecycle")
    expected_handover=expected_repository_ready and expected_projection_ready
    if ready.get("handover_ready") is not expected_handover:e.append("relay_readiness.handover_ready must equal repository_ready AND projection_ready")
    if not isinstance(ready.get("reasons"),list):e.append("relay_readiness.reasons must be a list")

    if required and pstate in {"PENDING","PUBLISHED_UNCONFIRMED","IN_SYNC"}:
        if projection.get("roadmap_revision")!=(s.get("roadmap") or {}).get("revision"):e.append(f"{pstate.lower()} projection roadmap_revision does not match current roadmap")
        exp=expected_execution_ref(root,s)
        if str(projection.get("execution_ref"))!=exp:e.append(f"{pstate.lower()} projection execution_ref {projection.get('execution_ref')} != current execution ref {exp}")

    if required and pstate=="PENDING":
        if receipt not in NONE_VALUES:e.append("PENDING projection must not claim a publication receipt")
    elif required and pstate=="PUBLISHED_UNCONFIRMED":
        if not str(receipt or "").strip():e.append("PUBLISHED_UNCONFIRMED projection requires observed publication receipt")
        if ready.get("projection_ready") is True:e.append("PUBLISHED_UNCONFIRMED projection cannot be projection_ready")
        w.append("projection publication has a receipt but is not yet confirmed against current desired state; reconcile by operation_id before republishing")
    elif required and pstate=="IN_SYNC":
        if not str(receipt or "").strip():e.append("IN_SYNC required projection requires verified publication receipt")
        if not isinstance(projection.get("basis"),list) or not projection.get("basis"):e.append("IN_SYNC required projection needs durable verification basis")
    elif required and pstate=="STALE":
        if ready.get("projection_ready") is True:e.append("STALE projection cannot be projection_ready")
        w.append("projection is stale; reconcile the stable operation/target against current repository state before claiming handover readiness")

    if required and pstate in {"PENDING","PUBLISHED_UNCONFIRMED","STALE"} and ready.get("handover_ready") is True:e.append(f"{pstate.lower()} projection cannot be handover ready")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
