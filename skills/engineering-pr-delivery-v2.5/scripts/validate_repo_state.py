#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require
from takeoverlib import current_routes,route_key

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

    # Execution custody is distinct from candidate certification. Certification says a
    # candidate is qualified; an ACTIVE custody lease says who currently owns writes.
    custody=state.get("execution_custody")
    if custody is not None:
        if not isinstance(custody,dict):errors.append("REPO_STATE.execution_custody must be a mapping")
        else:
            leases=custody.get("leases")
            if not isinstance(leases,list):errors.append("REPO_STATE.execution_custody.leases must be a list")
            else:
                active_by_route={}
                live_routes={route_key(r):r for r in current_routes(repo_root,state)}
                for i,lease in enumerate(leases):
                    label=f"REPO_STATE.execution_custody.leases[{i}]"
                    if not isinstance(lease,dict):errors.append(f"{label} must be a mapping");continue
                    errors+=require(lease,["route_key","candidate","state","branch","source"],label)
                    rkey=str(lease.get("route_key") or "")
                    candidate=lease.get("candidate") or {};cid=str(candidate.get("agent_instance_id") or "")
                    if not rkey:errors.append(f"{label}.route_key must be explicit")
                    if not cid:errors.append(f"{label}.candidate.agent_instance_id must be explicit")
                    if lease.get("state") not in {"ACTIVE","RELEASED","SUPERSEDED"}:errors.append(f"{label}.state invalid")
                    if not _explicit(lease.get("branch")):errors.append(f"{label}.branch must be explicit")
                    if not _explicit(lease.get("source")):errors.append(f"{label}.source must be explicit")
                    if lease.get("state")=="ACTIVE":
                        active_by_route.setdefault(rkey,[]).append(lease)
                        route=live_routes.get(rkey)
                        if route is None:errors.append(f"{label} ACTIVE route is not a current execution route: {rkey}")
                        elif str(route.get("branch"))!=str(lease.get("branch")):errors.append(f"{label}.branch does not match current route branch")
                for rkey,items in active_by_route.items():
                    if len(items)>1:errors.append(f"REPO_STATE.execution_custody has multiple ACTIVE executors for {rkey}")

    obligations=state.get("control_obligations")
    if obligations is not None:
        if not isinstance(obligations,list):errors.append("REPO_STATE.control_obligations must be a list")
        else:
            seen_ids=set();all_ids=set()
            for item in obligations:
                if isinstance(item,dict) and item.get("id"):all_ids.add(str(item.get("id")))
            for i,item in enumerate(obligations):
                label=f"REPO_STATE.control_obligations[{i}]"
                if not isinstance(item,dict):errors.append(f"{label} must be a mapping");continue
                errors+=require(item,["id","kind","state","summary","source","scope","evidence"],label)
                oid=str(item.get("id") or "");kind=item.get("kind");ostate=item.get("state")
                if oid in seen_ids:errors.append(f"duplicate control obligation id: {oid}")
                seen_ids.add(oid)
                if not str(item.get("summary") or "").strip():errors.append(f"{label}.summary must be explicit")
                if not str(item.get("source") or "").strip():errors.append(f"{label}.source must be explicit")
                if not isinstance(item.get("scope"),dict):errors.append(f"{label}.scope must be a mapping")
                if not isinstance(item.get("evidence"),list):errors.append(f"{label}.evidence must be a list")
                if ostate not in {"OPEN","SATISFIED","SUPERSEDED","CANCELLED","EXPIRED"}:errors.append(f"{label}.state invalid")
                supersedes=item.get("supersedes")
                if supersedes not in {None,""} and str(supersedes) not in all_ids:errors.append(f"{label}.supersedes references unknown control obligation: {supersedes}")
                if kind=="DEFERRED_VALIDATION":
                    if not oid.startswith("PEND-"):errors.append(f"{label}.id must use PEND-* for DEFERRED_VALIDATION")
                    boundaries=item.get("must_resolve_before")
                    allowed=item.get("allowed_before_resolution")
                    if not isinstance(boundaries,list) or not boundaries:errors.append(f"{label}.must_resolve_before must be non-empty")
                    if not isinstance(allowed,list) or not allowed:errors.append(f"{label}.allowed_before_resolution must be non-empty")
                    if not str(item.get("resolution_condition") or "").strip():errors.append(f"{label}.resolution_condition is required")
                    if ostate=="EXPIRED":errors.append(f"{label} DEFERRED_VALIDATION cannot use EXPIRED; use OPEN/SATISFIED/SUPERSEDED/CANCELLED")
                elif kind=="KNOWN_ISSUE":
                    if not oid.startswith("KI-"):errors.append(f"{label}.id must use KI-* for KNOWN_ISSUE")
                    if ostate=="OPEN" and not str(item.get("revisit_when") or "").strip():errors.append(f"{label}.revisit_when is required while known issue is OPEN")
                    if ostate=="EXPIRED":errors.append(f"{label} KNOWN_ISSUE cannot use EXPIRED")
                elif kind=="DELEGATION":
                    if not oid.startswith("DLG-"):errors.append(f"{label}.id must use DLG-* for DELEGATION")
                    if item.get("monitor_role")!="READ_ONLY":errors.append(f"{label}.monitor_role must be READ_ONLY")
                    if not str(item.get("success_condition") or "").strip():errors.append(f"{label}.success_condition is required")
                else:
                    errors.append(f"{label}.kind invalid: {kind}")
                if ostate=="SATISFIED" and not item.get("evidence"):errors.append(f"{label} SATISFIED requires resolution evidence")

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
    adapter=projection.get("adapter");plan=projection.get("plan")
    if bool(adapter)!=bool(plan):errors.append("REPO_STATE.projection adapter and plan must be declared together")
    if adapter not in {None,"", "GITHUB_ISSUES"}:errors.append(f"REPO_STATE.projection.adapter unsupported: {adapter}")
    if adapter=="GITHUB_ISSUES":
        if projection.get("required") is not True:errors.append("GITHUB_ISSUES adapter requires projection.required=true")
        if not str(projection.get("operation_id") or "").startswith("GHGEN-"):errors.append("GITHUB_ISSUES projection.operation_id must use GHGEN-* namespace")
        if not str(projection.get("target") or "").startswith("github:"):errors.append("GITHUB_ISSUES projection.target must use github:<owner/repo>:... form")
        if not _explicit(plan):errors.append("GITHUB_ISSUES projection.plan must identify current immutable generation")
        elif not (repo_root/plan).exists():errors.append(f"REPO_STATE.projection.plan does not exist: {plan}")
    elif plan not in {None,""}:errors.append("projection.plan is only valid with projection.adapter")
    delivery=state.get("delivery")
    if delivery is not None:
        if not isinstance(delivery,dict):errors.append("REPO_STATE.delivery must be mapping")
        else:
            drequired=delivery.get("required");provider=delivery.get("provider");observation=delivery.get("observation") or {};observations=delivery.get("observations") or []
            if not isinstance(drequired,bool):errors.append("REPO_STATE.delivery.required must be boolean")
            if not isinstance(observations,list):errors.append("REPO_STATE.delivery.observations must be a list")
            else:
                seen_paths=set()
                for i,item in enumerate(observations):
                    if not isinstance(item,dict):errors.append(f"REPO_STATE.delivery.observations[{i}] must be mapping");continue
                    oid=item.get("id");opath=item.get("path")
                    if not str(oid or "").startswith("DOBS-"):errors.append(f"REPO_STATE.delivery.observations[{i}].id must use DOBS-* namespace")
                    if not _explicit(opath):errors.append(f"REPO_STATE.delivery.observations[{i}].path must be explicit")
                    elif not (repo_root/str(opath)).exists():errors.append(f"REPO_STATE.delivery.observations[{i}].path does not exist: {opath}")
                    if opath in seen_paths:errors.append(f"duplicate REPO_STATE.delivery observation path: {opath}")
                    seen_paths.add(opath)
            if drequired is True:
                if provider!="GITHUB":errors.append("required REPO_STATE.delivery currently supports provider GITHUB")
                if not str(observation.get("id") or "").startswith("DOBS-"):errors.append("required REPO_STATE.delivery observation.id must use DOBS-* namespace")
                opath=observation.get("path")
                if not _explicit(opath):errors.append("required REPO_STATE.delivery observation.path must be explicit")
                elif not (repo_root/str(opath)).exists():errors.append(f"REPO_STATE.delivery observation.path does not exist: {opath}")
                if observations and not any(str(x.get("path"))==str(opath) for x in observations if isinstance(x,dict)):
                    errors.append("REPO_STATE.delivery primary observation must also appear in observations[] when observations[] is used")
            elif drequired is False:
                if provider not in {None,""}:errors.append("delivery.required=false must not name a provider")
                if observation.get("id") not in {None,""} or observation.get("path") not in {None,""}:errors.append("delivery.required=false must not point at an observation")
                if observations:errors.append("delivery.required=false must not retain observations[]")
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
        if isinstance(custody,dict) and any(isinstance(x,dict) and x.get("state")=="ACTIVE" for x in (custody.get("leases") or [])):
            errors.append(f"relay_state {relay_state} must not retain ACTIVE execution custody")
    return errors,warnings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("repo_root",nargs="?",default="."); a=ap.parse_args(); e,w=validate(Path(a.repo_root).resolve()); raise SystemExit(print_result(e,w))
if __name__=="__main__": main()
