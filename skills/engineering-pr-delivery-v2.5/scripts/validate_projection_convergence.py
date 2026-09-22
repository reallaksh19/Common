#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml, print_result, require

PROJECTION_STATES={"NOT_REQUIRED","PENDING","PUBLISHED_UNCONFIRMED","IN_SYNC","STALE"}
SUPERSEDED_DISPOSITIONS={"SUPERSEDED_BEFORE_PUBLICATION","SUPERSEDED_AFTER_ATTEMPT_UNCONFIRMED","SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED","SUPERSEDED_AFTER_VERIFIED_PUBLICATION"}
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


def _validate_superseded(projection,e):
    history=projection.get("superseded_operations",[]) or []
    if not isinstance(history,list):e.append("projection.superseded_operations must be a list");return
    current=str(projection.get("operation_id") or "");target=str(projection.get("target") or "")
    ids=set();entries={}
    for i,item in enumerate(history):
        p=f"projection.superseded_operations[{i}]"
        if not isinstance(item,dict):e.append(f"{p} must be a mapping");continue
        for field in ("operation_id","target","roadmap_revision","execution_ref","disposition","superseded_by","receipt","basis"):
            if field not in item:e.append(f"{p} missing {field}")
        oid=str(item.get("operation_id") or "")
        if not oid:e.append(f"{p}.operation_id must be non-empty");continue
        if oid==current:e.append(f"{p}.operation_id reuses current operation_id")
        if oid in ids:e.append(f"projection.superseded_operations duplicate operation_id {oid}")
        ids.add(oid);entries[oid]=item
        if str(item.get("target") or "")!=target:e.append(f"{p}.target must match current projection target")
        disposition=item.get("disposition")
        if disposition not in SUPERSEDED_DISPOSITIONS:e.append(f"{p}.disposition invalid: {disposition}")
        if disposition in {"SUPERSEDED_BEFORE_PUBLICATION","SUPERSEDED_AFTER_ATTEMPT_UNCONFIRMED"} and item.get("receipt") not in NONE_VALUES:e.append(f"{p} {disposition} cannot invent a publication receipt")
        if disposition in {"SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED","SUPERSEDED_AFTER_VERIFIED_PUBLICATION"} and not str(item.get("receipt") or "").strip():e.append(f"{p} published supersession requires receipt")
        if not isinstance(item.get("basis"),list) or not item.get("basis"):e.append(f"{p}.basis must contain durable supersession evidence")
    valid_targets=ids|({current} if current else set())
    for oid,item in entries.items():
        nxt=str(item.get("superseded_by") or "")
        if not nxt:e.append(f"superseded projection operation {oid} requires superseded_by")
        elif nxt not in valid_targets:e.append(f"superseded projection operation {oid} points to unknown superseded_by {nxt}")
        elif nxt==oid:e.append(f"superseded projection operation {oid} cannot supersede itself")
    for start in entries:
        seen=[];cur=start
        while cur in entries:
            if cur in seen:e.append("projection supersession cycle: "+" -> ".join(seen+[cur]));break
            seen.append(cur);cur=str(entries[cur].get("superseded_by") or "")
        if cur and current and cur!=current:e.append(f"superseded projection chain from {start} does not terminate at current operation {current}")


def _validate_observed(projection,e):
    observed=projection.get("observed")
    if not isinstance(observed,dict):e.append("STALE projection requires observed external generation");return
    for field in ("operation_id","target","roadmap_revision","execution_ref","receipt","basis"):
        if field not in observed:e.append(f"projection.observed missing {field}")
    if str(observed.get("target") or "")!=str(projection.get("target") or ""):e.append("projection.observed.target must match current projection target")
    if not str(observed.get("operation_id") or "").strip():e.append("projection.observed.operation_id must be explicit")
    if not str(observed.get("receipt") or "").strip():e.append("projection.observed.receipt must identify external observed publication")
    if not isinstance(observed.get("basis"),list) or not observed.get("basis"):e.append("projection.observed.basis must contain durable observation basis")
    same=(str(observed.get("roadmap_revision"))==str(projection.get("roadmap_revision")) and str(observed.get("execution_ref"))==str(projection.get("execution_ref")))
    if same:e.append("STALE projection observed generation must differ from newest desired roadmap/execution basis")


def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    projection=s.get("projection") or {};ready=s.get("relay_readiness") or {}
    e+=require(projection,["required","state","operation_id","target","roadmap_revision","execution_ref","receipt","basis"],"REPO_STATE.projection")
    e+=require(ready,["baton_ready","projection_ready","handover_ready","reasons"],"REPO_STATE.relay_readiness")
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
        _validate_superseded(projection,e)

    expected_projection_ready=(required is False) or pstate=="IN_SYNC"
    if ready.get("projection_ready") is not expected_projection_ready:e.append("relay_readiness.projection_ready disagrees with projection state")
    if not isinstance(ready.get("baton_ready"),bool):e.append("relay_readiness.baton_ready must be boolean")
    expected_handover=ready.get("baton_ready") is True and expected_projection_ready
    if ready.get("handover_ready") is not expected_handover:e.append("relay_readiness.handover_ready must equal baton_ready AND projection_ready")
    if not isinstance(ready.get("reasons"),list):e.append("relay_readiness.reasons must be a list")

    if required and pstate in {"PENDING","PUBLISHED_UNCONFIRMED","IN_SYNC","STALE"}:
        if projection.get("roadmap_revision")!=(s.get("roadmap") or {}).get("revision"):e.append(f"{pstate.lower()} projection newest desired roadmap_revision does not match current roadmap")
        exp=expected_execution_ref(root,s)
        if str(projection.get("execution_ref"))!=exp:e.append(f"{pstate.lower()} projection newest desired execution_ref {projection.get('execution_ref')} != current execution ref {exp}")

    if required and pstate=="PENDING":
        if receipt not in NONE_VALUES:e.append("PENDING projection must not claim a publication receipt")
    elif required and pstate=="PUBLISHED_UNCONFIRMED":
        if not str(receipt or "").strip():e.append("PUBLISHED_UNCONFIRMED projection requires observed publication receipt")
        if ready.get("projection_ready") is True:e.append("PUBLISHED_UNCONFIRMED projection cannot be projection_ready")
        w.append("projection publication has a receipt but is not yet confirmed against current desired state; reconcile by operation_id before republishing")
    elif required and pstate=="IN_SYNC":
        if not str(receipt or "").strip():e.append("IN_SYNC required projection requires verified publication receipt")
        if not isinstance(projection.get("basis"),list) or not projection.get("basis"):e.append("IN_SYNC required projection needs durable verification basis")
        observed=projection.get("observed")
        if observed:
            if str(observed.get("operation_id"))!=str(operation_id) or str(observed.get("roadmap_revision"))!=str(projection.get("roadmap_revision")) or str(observed.get("execution_ref"))!=str(projection.get("execution_ref")):e.append("IN_SYNC projection cannot retain stale observed generation")
    elif required and pstate=="STALE":
        if receipt not in NONE_VALUES:e.append("STALE projection top-level receipt belongs to newest desired operation and must be empty until that operation is published")
        if ready.get("projection_ready") is True:e.append("STALE projection cannot be projection_ready")
        _validate_observed(projection,e)
        w.append("projection is stale; publish/reconcile only the newest desired operation. Superseded operations are historical and have no retry authority")

    if required and pstate in {"PENDING","PUBLISHED_UNCONFIRMED","STALE"} and ready.get("handover_ready") is True:e.append(f"{pstate.lower()} projection cannot be handover ready")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
