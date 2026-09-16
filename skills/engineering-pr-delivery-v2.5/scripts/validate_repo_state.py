#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require

RELAY_STATES={"INITIALIZING","ACTIVE","PARALLEL","IDLE","TERMINAL"}
NONE_IDS={None,"","NONE"}

def _explicit(value)->bool:
    if not isinstance(value,str):return False
    value=value.strip()
    return bool(value) and not (value.startswith("<") and value.endswith(">"))

def validate(repo_root:Path):
    errors=[]; warnings=[]
    try: state=load_yaml(repo_root/"agents/relay/REPO_STATE.yaml")
    except Exception as exc: return [f"REPO_STATE: {exc}"],warnings
    errors+=require(state,["schema_version","relay_state","repository","relay_protocol","roadmap","current_position","execution_policy","active_ep","last_checkpoint","takeover_admissions","progress","status_planes","projection","relay_readiness","chat_context_required"],"REPO_STATE")
    if state.get("schema_version")!="relay-v2.5": errors.append("REPO_STATE: schema_version must be relay-v2.5")
    protocol=state.get("relay_protocol") or {};errors+=require(protocol,["version","basis_ref"],"REPO_STATE.relay_protocol")
    if str(protocol.get("version"))!="2.5":errors.append("REPO_STATE.relay_protocol.version must be 2.5")
    if not _explicit(protocol.get("basis_ref")):errors.append("REPO_STATE.relay_protocol.basis_ref must be an explicit pinned Common ref")
    relay_state=state.get("relay_state")
    if relay_state not in RELAY_STATES:errors.append(f"REPO_STATE.relay_state invalid: {relay_state}")
    if state.get("chat_context_required") is not False: errors.append("REPO_STATE: chat_context_required must be false")
    roadmap=state.get("roadmap") or {}; errors+=require(roadmap,["id","revision","path"],"REPO_STATE.roadmap")
    if roadmap.get("path") and not (repo_root/roadmap["path"]).exists(): errors.append(f"REPO_STATE.roadmap.path does not exist: {roadmap['path']}")
    current=state.get("current_position") or {};errors+=require(current,["objective","phase","work_package"],"REPO_STATE.current_position")
    active=state.get("active_ep") or {}; errors+=require(active,["id","path","state"],"REPO_STATE.active_ep")
    last=state.get("last_checkpoint") or {}; errors+=require(last,["id","path"],"REPO_STATE.last_checkpoint")
    admissions=state.get("takeover_admissions")
    if not isinstance(admissions,list):errors.append("REPO_STATE.takeover_admissions must be a list")

    join=state.get("predecessor_join") or {};join_id=join.get("id");join_path=join.get("path")
    if bool(join_id)!=bool(join_path):errors.append("REPO_STATE.predecessor_join requires both id and path or neither")
    replan=state.get("predecessor_replan") or {};replan_id=replan.get("id");replan_path=replan.get("path")
    if bool(replan_id)!=bool(replan_path):errors.append("REPO_STATE.predecessor_replan requires both id and path or neither")
    if join_id and replan_id:errors.append("predecessor_join and predecessor_replan are mutually exclusive")
    if join_id:
        if relay_state!="ACTIVE":errors.append("predecessor_join is valid only for ACTIVE integration work")
        if last.get("id") not in NONE_IDS or last.get("path") not in {None,""}:errors.append("predecessor_join and singular last_checkpoint cannot both be active")
        if not (repo_root/join_path).exists():errors.append(f"REPO_STATE.predecessor_join.path does not exist: {join_path}")
    if replan_id:
        if relay_state=="INITIALIZING":errors.append("predecessor_replan is invalid during INITIALIZING")
        if last.get("id") not in NONE_IDS or last.get("path") not in {None,""}:errors.append("predecessor_replan and singular last_checkpoint cannot both be active")
        if not (repo_root/replan_path).exists():errors.append(f"REPO_STATE.predecessor_replan.path does not exist: {replan_path}")

    projection=state.get("projection") or {};errors+=require(projection,["required","state","operation_id","target","roadmap_revision","execution_ref","receipt","basis"],"REPO_STATE.projection")
    readiness=state.get("relay_readiness") or {};errors+=require(readiness,["baton_ready","projection_ready","handover_ready","reasons"],"REPO_STATE.relay_readiness")
    if "repository_ready" in readiness:errors.append("REPO_STATE.relay_readiness.repository_ready is retired; use baton_ready for candidate-independent repository custody")
    policy=state.get("execution_policy") or {};mode=policy.get("mode")
    if mode not in {"SERIAL","OWNER_APPROVED_PARALLEL"}: errors.append("REPO_STATE.execution_policy.mode must be SERIAL or OWNER_APPROVED_PARALLEL")

    if relay_state=="PARALLEL":
        if mode!="OWNER_APPROVED_PARALLEL":errors.append("relay_state PARALLEL requires execution_policy.mode OWNER_APPROVED_PARALLEL")
        if not policy.get("parallel_plan"):errors.append("relay_state PARALLEL requires execution_policy.parallel_plan")
        if active.get("state")!="ROUTER":errors.append("relay_state PARALLEL requires active_ep.state ROUTER")
        if active.get("path") not in {None,""}:errors.append("parallel router active_ep.path must be null/empty; lane EPs come from parallel plan")
        if active.get("continuity_receipt") not in NONE_IDS:errors.append("parallel router does not use singular active_ep.continuity_receipt")
        wps=current.get("work_packages") or []
        if not isinstance(wps,list) or len(wps)<2:errors.append("relay_state PARALLEL requires current_position.work_packages with at least two lanes")
        if current.get("work_package")!="PARALLEL":errors.append("relay_state PARALLEL requires current_position.work_package: PARALLEL")
    else:
        if mode=="OWNER_APPROVED_PARALLEL":errors.append("OWNER_APPROVED_PARALLEL mode requires relay_state PARALLEL")
        if policy.get("parallel_plan"):errors.append("non-parallel relay state must not declare parallel_plan")
        if current.get("work_packages"):errors.append("non-parallel relay state must not declare current_position.work_packages")

    if relay_state=="ACTIVE":
        if active.get("state") in {None,"NONE","ROUTER"}:errors.append("relay_state ACTIVE requires one active EP or reconciliation route")
        elif active.get("path") and not (repo_root/active["path"]).exists():errors.append(f"REPO_STATE.active_ep.path does not exist: {active['path']}")
        if active.get("state")=="RECONCILING" and active.get("continuity_receipt") in NONE_IDS:errors.append("active_ep.state RECONCILING requires continuity_receipt")
    elif relay_state in {"INITIALIZING","IDLE","TERMINAL"}:
        if active.get("state")!="NONE":errors.append(f"relay_state {relay_state} requires active_ep.state NONE")
        if active.get("path") not in {None,""}:errors.append(f"relay_state {relay_state} requires active_ep.path null/empty")
        if active.get("continuity_receipt") not in NONE_IDS:errors.append(f"relay_state {relay_state} must not expose active_ep.continuity_receipt")
        if isinstance(admissions,list) and admissions:errors.append(f"relay_state {relay_state} must not retain active takeover_admissions")
    return errors,warnings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("repo_root",nargs="?",default="."); a=ap.parse_args(); e,w=validate(Path(a.repo_root).resolve()); raise SystemExit(print_result(e,w))
if __name__=="__main__": main()
