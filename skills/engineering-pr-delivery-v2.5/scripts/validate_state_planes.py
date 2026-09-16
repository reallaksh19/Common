#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require

EXECUTION={"IDLE","READY","ACTIVE","WAITING","COMPLETE"}
MATERIAL_AUTHORITY={"WRITE","READ_ONLY","NONE"}
QUALITY={"CLEAR","NEEDS_ATTENTION","OWNER_REVIEW_REQUIRED"}
EVIDENCE={"COMPLETE","PARTIAL","NOT_RUN","FAILED","NA"}
HARD_STOPS={"OWNER_DECISION_REQUIRED","ESSENTIAL_INPUT_MISSING","AUTHORITY_VIOLATION","PROTECTED_INVARIANT_FAILURE","WRITE_COLLISION","SUPERSEDED_EP","ROADMAP_CONFLICT","REPOSITORY_STATE_CONFLICT","UNSAFE_ENGINEERING_RESULT"}
NOT_RUN_CAUSES={"INFRASTRUCTURE","UNAVAILABLE_TOOL","NOT_SCHEDULED","DEPENDENCY_WAIT","OTHER"}

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");planes=s.get("status_planes") or {};relay_state=s.get("relay_state")
    e+=require(planes,["execution","quality","evidence","stop"],"REPO_STATE.status_planes")
    execution=planes.get("execution") or {};quality=planes.get("quality") or {};evidence=planes.get("evidence") or {};stop=planes.get("stop") or {}
    e+=require(execution,["state","can_continue","material_authority","next_action"],"status_planes.execution")
    if execution.get("state") not in EXECUTION:e.append(f"status_planes.execution.state invalid: {execution.get('state')}")
    if not isinstance(execution.get("can_continue"),bool):e.append("status_planes.execution.can_continue must be boolean")
    authority=execution.get("material_authority")
    if authority not in MATERIAL_AUTHORITY:e.append(f"status_planes.execution.material_authority invalid: {authority}")
    if not str(execution.get("next_action","")).strip():e.append("status_planes.execution.next_action must be explicit")
    e+=require(quality,["state","findings"],"status_planes.quality")
    if quality.get("state") not in QUALITY:e.append(f"status_planes.quality.state invalid: {quality.get('state')}")
    if not isinstance(quality.get("findings"),list):e.append("status_planes.quality.findings must be a list")
    e+=require(evidence,["state","summary","not_run"],"status_planes.evidence")
    if evidence.get("state") not in EVIDENCE:e.append(f"status_planes.evidence.state invalid: {evidence.get('state')}")
    if not isinstance(evidence.get("not_run"),list):e.append("status_planes.evidence.not_run must be a list")
    for i,item in enumerate(evidence.get("not_run",[]) or []):
        if not isinstance(item,dict):e.append(f"status_planes.evidence.not_run[{i}] must be a mapping");continue
        e+=require(item,["id","reason","cause"],f"status_planes.evidence.not_run[{i}]")
        if item.get("cause") not in NOT_RUN_CAUSES:e.append(f"status_planes.evidence.not_run[{i}].cause invalid: {item.get('cause')}")
    if evidence.get("state")=="NOT_RUN" and not evidence.get("not_run"):e.append("evidence state NOT_RUN requires at least one explicit not_run item")
    e+=require(stop,["active","category","reason","basis"],"status_planes.stop")
    if not isinstance(stop.get("active"),bool):e.append("status_planes.stop.active must be boolean")
    if stop.get("active"):
        if stop.get("category") not in HARD_STOPS:e.append(f"active hard stop requires valid category, got {stop.get('category')}")
        if not str(stop.get("reason","")).strip():e.append("active hard stop requires plain-language reason")
        if not isinstance(stop.get("basis"),list) or not stop.get("basis"):e.append("active hard stop requires durable basis")
        if execution.get("can_continue") is not False:e.append("active hard stop requires execution.can_continue=false")
        if authority=="WRITE":e.append("active hard stop cannot retain material_authority WRITE")
    else:
        if stop.get("category") not in {None,"NONE"}:e.append("inactive stop must use category NONE")

    ex_state=execution.get("state");can=execution.get("can_continue")
    if relay_state=="INITIALIZING":
        if ex_state!="WAITING" or can is not False:e.append("INITIALIZING relay requires execution WAITING and can_continue=false")
        if authority!="NONE":e.append("INITIALIZING relay requires material_authority NONE")
    elif relay_state=="ACTIVE":
        if ex_state not in {"READY","ACTIVE","WAITING"}:e.append("ACTIVE relay execution must be READY, ACTIVE, or WAITING")
        if authority not in {"WRITE","READ_ONLY"}:e.append("ACTIVE relay requires material_authority WRITE or READ_ONLY")
    elif relay_state=="PARALLEL":
        if ex_state not in {"ACTIVE","WAITING"}:e.append("PARALLEL relay execution must be ACTIVE or WAITING")
        if authority not in {"WRITE","READ_ONLY"}:e.append("PARALLEL relay requires material_authority WRITE or READ_ONLY")
    elif relay_state=="IDLE":
        if ex_state not in {"IDLE","WAITING"} or can is not False:e.append("IDLE relay requires execution IDLE/WAITING and can_continue=false")
        if authority!="NONE":e.append("IDLE relay requires material_authority NONE")
    elif relay_state=="TERMINAL":
        if ex_state!="COMPLETE" or can is not False:e.append("TERMINAL relay requires execution COMPLETE and can_continue=false")
        if authority!="NONE":e.append("TERMINAL relay requires material_authority NONE")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
