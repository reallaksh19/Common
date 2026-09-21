#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml, print_result
from zero_context_reconstruction import build


def _nonempty(value):
    if isinstance(value, str): return bool(value.strip())
    if isinstance(value, (list, dict)): return bool(value)
    return value is not None


def validate(root: Path):
    e=[]; w=[]; state=load_yaml(root/"agents/relay/REPO_STATE.yaml"); d=build(root)
    if d.get("conversation_context_required") is not False:
        e.append("zero-context reconstruction requires chat_context_required=false")
    lifecycle=d.get("relay_state")
    routes=d.get("routes") or []
    if d.get("control_obligations")!=(state.get("control_obligations") or []):
        e.append("zero-context reconstruction drops or changes control_obligations")
    if d.get("execution_custody")!=(state.get("execution_custody") or {"enforced":False,"leases":[]}):
        e.append("zero-context reconstruction drops or changes execution_custody")
    if lifecycle in {"ACTIVE","PARALLEL"}:
        if not routes:e.append(f"{lifecycle} repository must expose at least one reconstructable execution route")
        for route in routes:
            label=f"route {route.get('route_key')}"
            required=("roadmap_position","why_task_exists","current_task","input_authority_editability","benchmarks_oracles","scope","quality_obligations","evidence","tests_required","acceptance","first_implementation_action","stale_conditions","next_work","control_obligations","execution_custody")
            for key in required:
                if key=="control_obligations":
                    if not isinstance(route.get(key),list):e.append(f"{label}: control_obligations is not reconstructable from repository state")
                elif key=="execution_custody":
                    if not isinstance(route.get(key),dict):e.append(f"{label}: execution_custody is not reconstructable from repository state")
                elif not _nonempty(route.get(key)):e.append(f"{label}: {key} is not reconstructable from repository state")
            for item in route.get("control_obligations") or []:
                if item.get("kind")=="DEFERRED_VALIDATION":
                    if not item.get("must_resolve_before") or not item.get("allowed_before_resolution"):
                        e.append(f"{label}: OPEN pending control {item.get('id')} lacks continuation/resolution boundary")
                if item.get("kind")=="DELEGATION" and item.get("monitor_role")!="READ_ONLY":
                    e.append(f"{label}: OPEN delegation {item.get('id')} must reconstruct as READ_ONLY")
            scope=route.get("scope") or {}
            for key in ("allowed","protected","prohibited"):
                if not _nonempty(scope.get(key)):e.append(f"{label}: scope.{key} must be explicit for zero-context takeover")
            first=route.get("first_implementation_action") or {}
            if first and not first.get("action"):e.append(f"{label}: first implementation action must be explicit")
    elif lifecycle in {"INITIALIZING","IDLE","TERMINAL"}:
        if routes:e.append(f"{lifecycle} repository must not expose a material execution route")
        if not _nonempty(d.get("no_active_work")):e.append(f"{lifecycle} repository must explain why no material route exists")
    else:
        e.append(f"zero-context reconstruction: unsupported relay_state {lifecycle}")
    if lifecycle=="ACTIVE" and str(d.get("active_ep_state"))=="RECONCILING":
        execution=d.get("execution") or {}
        if execution.get("material_authority")!="READ_ONLY":e.append("RECONCILING active EP must reconstruct as READ_ONLY")
    projection=d.get("projection") or {}; readiness=d.get("relay_readiness") or {}
    if projection.get("state")=="STALE":
        if readiness.get("projection_ready") is not False:e.append("stale projection must reconstruct projection_ready=false")
        if readiness.get("handover_ready") is not False:e.append("stale projection must reconstruct handover_ready=false")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
