from __future__ import annotations
from pathlib import Path
from relaylib import load_yaml
from report_projection import build as report_projection
from takeoverlib import current_routes, route_key


def _maybe(root: Path, path):
    if not path:
        return None
    p = root / str(path)
    return load_yaml(p) if p.exists() else None


def _checkpoint(root: Path, state: dict) -> dict | None:
    ref = state.get("last_checkpoint") or {}
    return _maybe(root, ref.get("path"))


def _quality_from_checkpoint(root: Path, cp: dict | None) -> dict | None:
    if not cp:
        return None
    return _maybe(root, (cp.get("quality_review") or {}).get("path"))


def _route_summary(root: Path, state: dict, route: dict, report: dict) -> dict:
    ep = load_yaml(root / route["ep_path"])
    context = ep.get("context_capsule") or {}
    cp = _checkpoint(root, state)
    qrv = _quality_from_checkpoint(root, cp)
    next_work = ep.get("next_work") or {}
    steps = next_work.get("steps") or []
    first = steps[0] if steps else None
    uncertainties = []
    uncertainties.extend(context.get("known_problems") or [])
    if cp:
        uncertainties.extend(cp.get("known_limitations") or [])
        uncertainties.extend(cp.get("remaining_work") or [])
    if qrv:
        for finding in qrv.get("findings") or []:
            if finding.get("disposition") != "REMEDIATED":
                uncertainties.append(finding.get("statement") or finding.get("id"))
    stale = list((ep.get("anti_drift") or {}).get("stale_if") or [])
    for item in ep.get("inputs") or []:
        stale.extend(item.get("stale_if") or [])
    for item in ep.get("benchmarks") or []:
        stale.extend(item.get("stale_if") or [])
    predecessor = None
    if cp:
        predecessor = {
            "checkpoint_id": cp.get("checkpoint_id"),
            "implementation_result": cp.get("implementation_result") or {},
            "acceptance_results": cp.get("acceptance_results") or [],
            "validation_results": cp.get("validation_results") or [],
            "known_limitations": cp.get("known_limitations") or [],
            "remaining_work": cp.get("remaining_work") or [],
            "roadmap_reconciliation": cp.get("roadmap_reconciliation") or {},
        }
    return {
        "route_key": route_key(route),
        "route": {
            "mode": route.get("mode"),
            "execution_ref": route.get("execution_ref"),
            "ep_id": route.get("ep_id"),
            "ep_path": route.get("ep_path"),
            "plan_id": route.get("plan_id"),
            "lane_id": route.get("lane_id"),
        },
        "roadmap_position": {
            "repository_position": state.get("current_position") or {},
            "ep_position": ep.get("roadmap_source") or {},
            "description": context.get("roadmap_position"),
        },
        "why_task_exists": context.get("why_this_work_exists"),
        "current_task": {
            "outcome": ep.get("outcome") or {},
            "implementation_plan": ep.get("implementation_plan") or [],
        },
        "owner_decisions": report.get("owner_decisions") or [],
        "predecessor_established": predecessor,
        "remaining_uncertain": uncertainties,
        "input_authority_editability": [
            {
                "id": x.get("id"), "name": x.get("name"), "authority": x.get("authority"),
                "source": x.get("source"), "editable": x.get("editable"),
                "applicability": x.get("applicability"), "resolution": x.get("resolution"),
            }
            for x in ep.get("inputs") or []
        ],
        "benchmarks_oracles": [
            {
                "id": x.get("id"), "name": x.get("name"), "oracle_class": x.get("oracle_class"),
                "source": x.get("source"), "expected": x.get("expected"), "tolerance": x.get("tolerance"),
                "independence": x.get("independence"), "applicability": x.get("applicability"),
                "resolution": x.get("resolution"),
            }
            for x in ep.get("benchmarks") or []
        ],
        "scope": ep.get("scope") or {},
        "quality_obligations": {
            "router": ep.get("quality") or {},
            "latest_review": qrv,
        },
        "evidence": {
            "state_plane": (state.get("status_planes") or {}).get("evidence") or {},
            "checkpoint_validation": (cp or {}).get("validation_results") or [],
            "quality_review": qrv,
        },
        "tests_required": ep.get("validation") or [],
        "acceptance": ep.get("acceptance") or [],
        "first_implementation_action": first,
        "stale_conditions": stale,
        "next_work": next_work,
        "projection_state": state.get("projection") or {},
        "control_obligations": [
            x for x in (state.get("control_obligations") or [])
            if isinstance(x,dict) and x.get("state")=="OPEN"
            and (
                not ((x.get("scope") or {}).get("route_key"))
                or str((x.get("scope") or {}).get("route_key"))==route_key(route)
            )
        ],
        "execution_custody": {
            "enforced": bool((state.get("execution_custody") or {}).get("enforced")),
            "active_lease": next((
                x for x in ((state.get("execution_custody") or {}).get("leases") or [])
                if isinstance(x,dict) and x.get("state")=="ACTIVE" and str(x.get("route_key"))==route_key(route)
            ), None),
        },
    }


def build(root: Path) -> dict:
    state = load_yaml(root / "agents/relay/REPO_STATE.yaml")
    report = report_projection(root)
    routes = []
    try:
        current = current_routes(root, state)
    except Exception:
        current = []
    for route in current:
        if route.get("ep_path") and (root / route["ep_path"]).exists():
            routes.append(_route_summary(root, state, route, report))
    lifecycle = state.get("relay_state")
    inactive_reason = None
    if not routes:
        inactive_reason = {
            "INITIALIZING": "Repository relay is initializing; no material execution route is authorized yet.",
            "IDLE": "Repository has no currently executable material frontier.",
            "TERMINAL": "Roadmap material work is complete; no successor execution route exists.",
        }.get(lifecycle)
    return {
        "schema_version": "relay-v2.5-zero-context-reconstruction",
        "conversation_context_required": state.get("chat_context_required"),
        "relay_state": lifecycle,
        "active_ep_state": (state.get("active_ep") or {}).get("state"),
        "roadmap": report.get("roadmap_summary") or {},
        "progress": report.get("progress") or {},
        "execution": report.get("execution") or {},
        "evidence": report.get("evidence") or {},
        "quality": report.get("quality") or {},
        "stop": report.get("stop") or {},
        "projection": report.get("projection") or {},
        "relay_readiness": report.get("relay_readiness") or {},
        "owner_decisions": report.get("owner_decisions") or [],
        "control_obligations": state.get("control_obligations") or [],
        "execution_custody": state.get("execution_custody") or {"enforced": False, "leases": []},
        "routes": routes,
        "no_active_work": inactive_reason,
    }
