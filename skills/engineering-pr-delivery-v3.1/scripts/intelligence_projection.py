#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from protocol_default import resolve as resolve_protocol
from snapshot_projection import build as build_project_snapshot
from v25_migration import MIGRATION_REPORT, PROTOCOL_SELECTION, V25_ROOT, legacy_inventory
from v3lib import canonical_digest, load_yaml, validate_schema


V25_STATE = "agents/relay/REPO_STATE.yaml"
V25_PROGRESS = "agents/relay/roadmap/PROGRESS.yaml"
V25_EVENTS = "agents/relay/roadmap/ROADMAP_EVENTS.yaml"


class ProjectionError(RuntimeError):
    pass


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args,], text=True).strip()


def _load(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    value = load_yaml(path)
    return value if isinstance(value, dict) else None


def _strings(values: Any) -> list[str]:
    out: list[str] = []
    for value in values or []:
        if isinstance(value, str):
            text = value
        elif isinstance(value, dict):
            text = str(value.get("statement") or value.get("summary") or value.get("id") or json.dumps(value, sort_keys=True))
        else:
            text = str(value)
        if text and text not in out:
            out.append(text)
    return out


def _scope(rows: Any, *keys: str) -> list[str]:
    out: list[str] = []
    for row in rows or []:
        if isinstance(row, str):
            text = row
        elif isinstance(row, dict):
            text = next((str(row.get(key)) for key in keys if row.get(key)), json.dumps(row, sort_keys=True))
        else:
            text = str(row)
        if text and text not in out:
            out.append(text)
    return out


def _load_parent_issue_observation(value: dict[str, Any] | None) -> dict[str, Any] | None:
    if value is None:
        return None
    errors = validate_schema("parent-issue-observation", value, "PARENT_ISSUE_OBSERVATION")
    if errors:
        raise ProjectionError("; ".join(errors))
    return value


def _progress_summary(rows: list[dict[str, Any]], parent: bool) -> dict[str, int]:
    keys = (
        ("complete", "partial", "pending", "blocked", "deferred", "not_applicable", "unknown")
        if parent else ("complete", "partial", "pending", "blocked")
    )
    result = {key: 0 for key in keys}
    mapping = {
        "COMPLETE": "complete", "PASS": "complete",
        "PARTIAL": "partial",
        "PENDING": "pending", "NOT_PROVED": "pending",
        "BLOCKED": "blocked", "FAIL": "blocked",
        "DEFERRED": "deferred",
        "NOT_APPLICABLE": "not_applicable", "NA": "not_applicable",
        "UNKNOWN": "unknown",
    }
    for row in rows:
        bucket = mapping.get(str(row.get("state") or "UNKNOWN"), "unknown" if parent else "pending")
        if bucket in result:
            result[bucket] += 1
    result["total"] = len(rows)
    return result


PROGRESS_STATES = {
    "PASS": "PASS",
    "COMPLETE": "PASS",
    "PARTIAL": "PARTIAL",
    "FAIL": "FAIL",
    "BLOCKED": "FAIL",
    "NOT_RUN": "NOT_RUN",
    "PENDING": "PENDING",
    "NOT_PROVED": "PENDING",
    "DEFERRED": "DEFERRED",
    "NOT_APPLICABLE": "NOT_APPLICABLE",
    "NA": "NOT_APPLICABLE",
    "UNKNOWN": "UNKNOWN",
}


def _normalise_progress_state(value: Any) -> str:
    return PROGRESS_STATES.get(str(value or "UNKNOWN").upper(), "UNKNOWN")


def _progress_item(row: dict[str, Any], *, default_reason: str = "UNKNOWN") -> dict[str, Any]:
    return {
        "id": str(row.get("id") or "UNKNOWN"),
        "statement": str(row.get("statement") or row.get("description") or row.get("id") or "Unknown criterion"),
        "state": _normalise_progress_state(row.get("state") or row.get("result") or row.get("status")),
        "reason_class": str(row.get("reason_class") or default_reason),
        "evidence": _strings(row.get("evidence")),
        "trace_refs": _strings(row.get("provider_refs") or row.get("trace_refs")),
        "remaining": _strings(row.get("remaining")),
        "owner": row.get("owner"),
        "weight": row.get("weight") if isinstance(row.get("weight"), (int, float)) else None,
        "parent_mappings": _strings(row.get("parent_mappings") or row.get("acceptance_refs")),
    }


def _progress_model(rows: Any, *, default_reason: str = "UNKNOWN") -> dict[str, Any]:
    criteria = [
        _progress_item(row, default_reason=default_reason)
        for row in (rows or [])
        if isinstance(row, dict)
    ]
    summary = {key: 0 for key in ("pass", "partial", "fail", "not_run", "pending", "deferred", "not_applicable", "unknown")}
    key_map = {
        "PASS": "pass",
        "PARTIAL": "partial",
        "FAIL": "fail",
        "NOT_RUN": "not_run",
        "PENDING": "pending",
        "DEFERRED": "deferred",
        "NOT_APPLICABLE": "not_applicable",
        "UNKNOWN": "unknown",
    }
    for row in criteria:
        summary[key_map[row["state"]]] += 1
    summary["total"] = len(criteria)

    applicable = [row for row in criteria if row["state"] != "NOT_APPLICABLE"]
    if not applicable:
        coverage = {"satisfied": 0, "applicable_total": 0, "percent": None, "basis": "NO_DENOMINATOR"}
    elif all(isinstance(row.get("weight"), (int, float)) for row in applicable) and sum(float(row["weight"]) for row in applicable) > 0:
        total = sum(float(row["weight"]) for row in applicable)
        satisfied = sum(float(row["weight"]) for row in applicable if row["state"] == "PASS")
        coverage = {
            "satisfied": satisfied,
            "applicable_total": total,
            "percent": round(100.0 * satisfied / total, 1),
            "basis": "DECLARED_WEIGHTS",
        }
    else:
        total = len(applicable)
        satisfied = sum(1 for row in applicable if row["state"] == "PASS")
        coverage = {
            "satisfied": satisfied,
            "applicable_total": total,
            "percent": round(100.0 * satisfied / total, 1),
            "basis": "UNWEIGHTED_CRITERIA",
        }
    return {"criteria": criteria, "summary": summary, "coverage": coverage}


def _issue_progress(observation: dict[str, Any] | None) -> dict[str, Any]:
    current = (observation or {}).get("current_contract") or {}
    baseline = (observation or {}).get("baseline") or {}
    rows = current.get("acceptance_items") or baseline.get("acceptance_items") or []
    return _progress_model(rows)


def _plan_progress(observation: dict[str, Any] | None) -> dict[str, Any]:
    plan = (observation or {}).get("implementation_plan") or {}
    return _progress_model(plan.get("steps") or [], default_reason="CURRENT_TASK")


def _verification(observation: dict[str, Any] | None, task_progress: dict[str, Any]) -> dict[str, Any]:
    raw = (observation or {}).get("verification")
    observations = _progress_model(
        raw if isinstance(raw, list) else (task_progress or {}).get("criteria") or [],
        default_reason="CURRENT_TASK",
    )["criteria"]
    origins: dict[str, int] = {}
    for row in observations:
        if row["state"] in {"FAIL", "NOT_RUN", "PARTIAL", "PENDING"}:
            origin = str(row.get("reason_class") or "UNKNOWN")
            origins[origin] = origins.get(origin, 0) + 1

    states = [row["state"] for row in observations if row["state"] != "NOT_APPLICABLE"]
    current_fail = any(
        row["state"] == "FAIL" and row.get("reason_class") == "CURRENT_TASK"
        for row in observations
    )
    if not states:
        state = "UNKNOWN"
    elif current_fail:
        state = "FAIL"
    elif all(value == "PASS" for value in states):
        state = "PASS"
    elif all(value == "NOT_RUN" for value in states):
        state = "NOT_RUN"
    elif any(value in {"PASS", "PARTIAL", "FAIL", "NOT_RUN"} for value in states):
        state = "PARTIAL"
    elif any(value == "PENDING" for value in states):
        state = "PENDING"
    else:
        state = "UNKNOWN"
    return {"state": state, "observations": observations, "failure_origins": origins}


def _acceptance_state(progress: dict[str, Any] | None) -> str:
    coverage = (progress or {}).get("coverage") or {}
    total = coverage.get("applicable_total")
    percent = coverage.get("percent")
    summary = (progress or {}).get("summary") or {}
    if not total:
        return "UNKNOWN"
    if percent == 100:
        return "SATISFIED"
    if (coverage.get("satisfied") or 0) > 0 or summary.get("partial", 0) > 0:
        return "PARTIAL"
    return "OPEN"


def _implementation_state(plan_progress: dict[str, Any] | None, planning: dict[str, Any]) -> str:
    coverage = (plan_progress or {}).get("coverage") or {}
    percent = coverage.get("percent")
    if percent == 100:
        return "COMPLETE"
    if percent is not None and percent > 0:
        return "PARTIAL"
    if planning.get("state") == "PRESENT":
        return "OPEN"
    return "UNKNOWN"


def _completion_model(
    *,
    work_progress: dict[str, Any],
    plan_progress: dict[str, Any],
    task_progress: dict[str, Any],
    programme_progress: dict[str, Any] | None,
    planning: dict[str, Any],
    verification: dict[str, Any],
    delivery: dict[str, Any],
    issue_state: str | None,
    issue_number: Any,
) -> dict[str, Any]:
    work_state = _acceptance_state(work_progress)
    programme_state = _acceptance_state(programme_progress)
    implementation = _implementation_state(plan_progress, planning)
    verification_state = str(verification.get("state") or "UNKNOWN")
    delivery_state = str(delivery.get("lifecycle") or "UNKNOWN")
    provider_state = str(issue_state or "UNKNOWN").upper()
    if provider_state not in {"OPEN", "CLOSED"}:
        provider_state = "UNKNOWN"

    if work_state == "SATISFIED" and verification_state == "PASS":
        overall = "COMPLETE"
    elif work_state in {"PARTIAL", "SATISFIED"} or implementation in {"PARTIAL", "COMPLETE"} or verification_state in {"PARTIAL", "FAIL", "NOT_RUN"}:
        overall = "PARTIAL"
    elif work_state == "OPEN":
        overall = "OPEN"
    else:
        overall = "UNKNOWN"

    done = [
        row["statement"]
        for row in (work_progress.get("criteria") or [])
        if row.get("state") == "PASS"
    ]
    remains = [
        row["statement"]
        for row in (work_progress.get("criteria") or [])
        if row.get("state") not in {"PASS", "NOT_APPLICABLE"}
    ]
    if not remains:
        remains = [
            row["statement"]
            for row in (task_progress.get("criteria") or [])
            if row.get("state") not in {"PASS", "NOT_APPLICABLE"}
        ]

    dependency_reasons = {"UPSTREAM_DEPENDENCY", "SIBLING_WORKSTREAM", "INFRASTRUCTURE", "PROVIDER"}
    dependencies = []
    owner_decisions = []
    for progress in (work_progress, task_progress):
        for row in progress.get("criteria") or []:
            reason = row.get("reason_class")
            if row.get("state") in {"PASS", "NOT_APPLICABLE"}:
                continue
            if reason in dependency_reasons:
                dependencies.append(f"{row['id']}: {row['statement']} [{reason}]")
            if reason == "OWNER_DECISION":
                owner_decisions.append(f"{row['id']}: {row['statement']}")
    for row in verification.get("observations") or []:
        if row.get("state") in {"PASS", "NOT_APPLICABLE"}:
            continue
        reason = row.get("reason_class")
        if reason in dependency_reasons:
            dependencies.append(f"{row['id']}: {row['statement']} [{reason}]")
        if reason == "OWNER_DECISION":
            owner_decisions.append(f"{row['id']}: {row['statement']}")

    headline = (
        f"#{issue_number} {overall} — "
        f"child acceptance {work_state.lower()}; verification {verification_state.lower()}; "
        f"delivery {delivery_state.lower()}."
    )
    return {
        "overall_state": overall,
        "headline": headline,
        "implementation": implementation,
        "verification": verification_state,
        "delivery": delivery_state,
        "work_issue_acceptance": work_state,
        "programme_contribution": programme_state,
        "provider_issue": provider_state,
        "what_done": list(dict.fromkeys(done)),
        "what_remains": list(dict.fromkeys(remains)),
        "dependencies": list(dict.fromkeys(dependencies)),
        "owner_decisions": list(dict.fromkeys(owner_decisions)),
    }


def _tracked_items(controls: dict[str, Any] | None, kind: str) -> list[dict[str, Any]]:
    result = []
    for row in (controls or {}).get("controls") or []:
        if not isinstance(row, dict) or row.get("state") != "OPEN":
            continue
        tracking = row.get("tracking") or {}
        if tracking.get("kind") != kind:
            continue
        result.append({
            "id": tracking.get("id"),
            "control_ref": row.get("id"),
            "status": "OPEN",
            "statement": row.get("condition"),
            "trace_refs": [str((row.get("source") or {}).get("ref"))],
            "affects": list(row.get("blocks") or []),
            "resolve_when": (row.get("resolution") or {}).get("condition"),
        })
    return result


def _programme_ref(ep: dict[str, Any] | None, parent: dict[str, Any]) -> dict[str, Any] | None:
    source = (ep or {}).get("programme_parent") or (ep or {}).get("parent_issue") or parent
    if not isinstance(source, dict):
        return None
    return {
        "repository": source.get("repository"),
        "number": source.get("number"),
        "title": source.get("title"),
        "url": source.get("url"),
    }


def _planning_sections(
    observation: dict[str, Any] | None,
    ep: dict[str, Any] | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    observed = (observation or {}).get("implementation_plan")
    basis = (ep or {}).get("implementation_plan_basis") or {}
    if isinstance(observed, dict):
        planning = {
            "state": observed.get("state") or "UNKNOWN",
            "provider_ref": observed.get("provider_ref"),
            "revision": observed.get("revision"),
            "digest": observed.get("digest"),
            "observed_at": observed.get("observed_at"),
            "responsibility_basis_ref": observed.get("responsibility_basis_ref"),
            "responsibility_basis_digest": observed.get("responsibility_basis_digest"),
        }
    elif basis:
        planning = {
            "state": "PRESENT",
            "provider_ref": basis.get("provider_ref"),
            "revision": basis.get("revision"),
            "digest": basis.get("digest"),
            "observed_at": basis.get("observed_at"),
            "responsibility_basis_ref": basis.get("responsibility_basis_ref"),
            "responsibility_basis_digest": basis.get("responsibility_basis_digest"),
        }
    else:
        planning = {
            "state": "MISSING",
            "provider_ref": None,
            "revision": None,
            "digest": None,
            "observed_at": None,
            "responsibility_basis_ref": None,
            "responsibility_basis_digest": None,
        }

    current_responsibility_digest = (
        ((observation or {}).get("current_contract") or {}).get("body_digest")
    )
    planned_responsibility_digest = planning.get("responsibility_basis_digest")
    if (
        planning.get("state") == "PRESENT"
        and planned_responsibility_digest
        and current_responsibility_digest
        and planned_responsibility_digest != current_responsibility_digest
    ):
        planning["state"] = "STALE"

    expected = (observation or {}).get("expected_next_observable")
    if not isinstance(expected, dict):
        expected = (ep or {}).get("expected_next_observable")
    if not isinstance(expected, dict):
        first_action = ((ep or {}).get("next") or {}).get("first_action")
        expected = (
            {"statement": str(first_action), "evidence": []}
            if first_action
            else None
        )
    planning["expected_next_observable"] = expected
    publications = [
        dict(row)
        for row in ((observation or {}).get("task_publications") or [])
        if isinstance(row, dict)
    ]
    return planning, publications


def _issue_sections(
    observation: dict[str, Any] | None,
    programme_observation: dict[str, Any] | None,
    ep: dict[str, Any] | None,
    acceptance: list[dict[str, Any]],
    checkpoint: dict[str, Any] | None,
    controls: dict[str, Any] | None,
) -> dict[str, Any]:
    obs = _load_parent_issue_observation(observation)
    programme_obs = _load_parent_issue_observation(programme_observation)
    ep_issue = (ep or {}).get("parent_issue") or {}
    ep_programme = (ep or {}).get("programme_parent") or {}
    if obs and ep_issue:
        if (
            obs.get("repository") != ep_issue.get("repository")
            or obs.get("issue_number") != ep_issue.get("number")
        ):
            raise ProjectionError("parent issue observation does not match the current EP parent_issue")
    if programme_obs and ep_programme:
        if (
            programme_obs.get("repository") != ep_programme.get("repository")
            or programme_obs.get("issue_number") != ep_programme.get("number")
        ):
            raise ProjectionError("programme issue observation does not match the current EP programme_parent")
    baseline = (obs or {}).get("baseline") or ep_issue.get("baseline")
    current = (obs or {}).get("current_contract")
    parent = {
        "repository": (obs or {}).get("repository") or ep_issue.get("repository"),
        "number": (obs or {}).get("issue_number") or ep_issue.get("number"),
        "title": (obs or {}).get("title") or ep_issue.get("title"),
        "state": (obs or {}).get("state"),
        "url": (obs or {}).get("url") or ep_issue.get("url"),
        "baseline": baseline,
        "current": current,
        "updates": list((obs or {}).get("updates") or []),
        "disposition": (obs or {}).get("disposition") or "UNKNOWN",
        "relationships": list((obs or {}).get("relationships") or []),
        "handover_ledger": (obs or {}).get("handover_ledger"),
    }
    parent_rows = []
    for row in ((current or {}).get("acceptance_items") or (baseline or {}).get("acceptance_items") or []):
        parent_rows.append({
            "id": row.get("id"),
            "statement": row.get("statement"),
            "state": row.get("state") or "UNKNOWN",
            "evidence": list(row.get("evidence") or []),
            "trace_refs": list(row.get("provider_refs") or []),
        })
    task_rows = [{
        "id": row.get("id"),
        "statement": row.get("statement"),
        "state": "COMPLETE" if row.get("state") == "PASS" else "BLOCKED" if row.get("state") == "FAIL" else "PENDING",
        "evidence": list(row.get("evidence") or []),
    } for row in acceptance]

    cp_id = (checkpoint or {}).get("id") or (checkpoint or {}).get("checkpoint_id")
    handoff = (checkpoint or {}).get("handoff") or {}
    baseline_digest = (baseline or {}).get("body_digest")
    changes = list(handoff.get("what_changed") or [])
    legacy_summary = ((checkpoint or {}).get("implementation_result") or {}).get("summary")
    if legacy_summary and not changes:
        changes = [legacy_summary]
    improvements = []
    if cp_id and baseline_digest:
        for index, change in enumerate(changes, 1):
            improvements.append({
                "id": f"IMP-{cp_id}-{index:03d}",
                "status": "ACCEPTED",
                "type": "EVIDENCE_BOUND_VALUE_ADD",
                "original_expectation": f"Parent issue baseline {baseline_digest}",
                "improvement": str(change),
                "evidence": [str(cp_id)],
                "project_value": str(change),
            })
    planning, publications = _planning_sections(obs, ep)
    programme_parent = _programme_ref(ep, parent)
    if programme_obs:
        programme_parent = {
            "repository": programme_obs.get("repository"),
            "number": programme_obs.get("issue_number"),
            "title": programme_obs.get("title"),
            "url": programme_obs.get("url"),
        }

    work_progress = _issue_progress(obs)
    task_progress = _progress_model(acceptance, default_reason="CURRENT_TASK")
    plan_progress = _plan_progress(obs)
    programme_progress = _issue_progress(programme_obs) if programme_obs else None
    verification = _verification(obs, task_progress)
    delivery = dict((obs or {}).get("delivery") or {"lifecycle": "UNKNOWN"})
    completion = _completion_model(
        work_progress=work_progress,
        plan_progress=plan_progress,
        task_progress=task_progress,
        programme_progress=programme_progress,
        planning=planning,
        verification=verification,
        delivery=delivery,
        issue_state=parent.get("state"),
        issue_number=parent.get("number"),
    )
    return {
        "parent_issue": parent,
        "programme_parent": programme_parent,
        "planning": planning,
        "task_publications": publications,
        "programme_progress": programme_progress,
        "work_issue_progress": work_progress,
        "plan_progress": plan_progress,
        "task_acceptance_progress": task_progress,
        "verification": verification,
        "delivery": delivery,
        "completion": completion,
        "parent_issue_progress": {"checklist": parent_rows, "summary": _progress_summary(parent_rows, True)},
        "current_task_progress": {"checklist": task_rows, "summary": _progress_summary(task_rows, False)},
        "offloads": list((ep or {}).get("offloads") or []),
        "pending_items": _tracked_items(controls, "PENDING"),
        "known_issues": _tracked_items(controls, "KNOWN_ISSUE"),
        "improvement_vs_original_issue": {"baseline_digest": baseline_digest, "items": improvements},
    }


def _v25_checkpoint(root: Path, state: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None, str | None]:
    ref = state.get("last_checkpoint") or {}
    cid, path = ref.get("id"), ref.get("path")
    if cid in {None, "", "NONE"} or not path:
        return None, None, None
    return _load(root / str(path)), str(cid), str(path)


def _v25_ep(root: Path, state: dict[str, Any], checkpoint: dict[str, Any] | None) -> tuple[dict[str, Any] | None, str | None, str | None]:
    active = state.get("active_ep") or {}
    eid, path = active.get("id"), active.get("path")
    if eid in {None, "", "NONE"}:
        eid = (checkpoint or {}).get("ep_id")
        path = f"agents/relay/execution-packages/{eid}.yaml" if eid else None
    if not path:
        return None, None, None
    return _load(root / str(path)), str(eid), str(path)


def _v25_wp(roadmap: dict[str, Any], wp_id: str | None):
    for objective in roadmap.get("objectives") or []:
        for phase in (objective or {}).get("phases") or []:
            for wp in (phase or {}).get("work_packages") or []:
                if str((wp or {}).get("id")) == str(wp_id):
                    return objective, phase, wp
    return None, None, None


def _v25_events(root: Path, refs: set[str]) -> list[dict[str, Any]]:
    ledger = _load(root / V25_EVENTS) or {}
    rows = []
    for event in ledger.get("events") or []:
        if not isinstance(event, dict):
            continue
        concepts = {str(x) for x in event.get("concept_refs") or []}
        execution = {str(x) for x in (event.get("execution_refs") or {}).values() if x not in {None, ""}}
        if refs & (concepts | execution):
            rows.append(event)
    rows.sort(key=lambda x: int(x.get("sequence") or 0), reverse=True)
    return [{
        "id": str(x.get("id")),
        "event_class": str(x.get("event_class")),
        "summary": str(x.get("summary")),
        "concept_change": x.get("concept_change"),
        "basis": _strings(x.get("basis")),
    } for x in rows[:12]]


def _v25_controls(state: dict[str, Any]) -> dict[str, list[str]]:
    result = {k: [] for k in ("material_write", "checkpoint", "handover", "pr_ready", "merge", "release")}
    for row in state.get("control_obligations") or []:
        if not isinstance(row, dict) or row.get("state") != "OPEN":
            continue
        cid = str(row.get("id"))
        blocks = set(row.get("must_resolve_before") or [])
        allowed = set(row.get("allowed_before_resolution") or [])
        if "BOUNDED_PRODUCT_WRITES" not in allowed:
            result["material_write"].append(cid)
        for action, key in (("CHECKPOINT", "checkpoint"), ("PR_READY", "pr_ready"), ("MERGE", "merge"), ("RELEASE", "release")):
            if action in blocks:
                result[key].append(cid)
    stop = ((state.get("status_planes") or {}).get("stop") or {})
    if stop.get("active"):
        token = f"STOP:{stop.get('category')}"
        for values in result.values():
            values.append(token)
    return result


def _v3_controls(root: Path, state: dict[str, Any]) -> dict[str, list[str]]:
    result = {k: [] for k in ("material_write", "checkpoint", "handover", "pr_ready", "merge", "release")}
    controls = load_yaml(root / str((state.get("controls") or {}).get("path")))
    mapping = {
        "material_write": "MATERIAL_WRITE",
        "checkpoint": "CHECKPOINT",
        "handover": "HANDOVER",
        "pr_ready": "PR_READY",
        "merge": "MERGE",
        "release": "RELEASE",
    }
    for row in controls.get("controls") or []:
        if not isinstance(row, dict) or row.get("state") != "OPEN":
            continue
        blocked = set(row.get("blocks") or [])
        for key, action in mapping.items():
            if action in blocked:
                result[key].append(str(row.get("id")))
    return result


def _v25_task(
    root: Path,
    parent_issue_observation: dict[str, Any] | None = None,
    programme_issue_observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state = load_yaml(root / V25_STATE)
    roadmap = load_yaml(root / str((state.get("roadmap") or {}).get("path")))
    progress = _load(root / V25_PROGRESS) or {}
    checkpoint, checkpoint_id, checkpoint_path = _v25_checkpoint(root, state)
    ep, ep_id, ep_path = _v25_ep(root, state, checkpoint)

    current = state.get("current_position") or {}
    source = (ep or {}).get("roadmap_source") or {}
    wp_id = source.get("work_package") or current.get("work_package")
    objective_id = source.get("objective") or current.get("objective")
    phase_id = source.get("phase") or current.get("phase")
    objective, phase, wp = _v25_wp(roadmap, str(wp_id) if wp_id else None)

    pidx = {str(x.get("id")): x for x in progress.get("acceptance_criteria") or [] if isinstance(x, dict)}
    acceptance = []
    for row in (ep or {}).get("acceptance") or []:
        aid = str(row.get("id"))
        p = pidx.get(aid) or {}
        raw = str(p.get("status") or "")
        status = "PASS" if raw in {"PASS", "COMPLETE"} else "FAIL" if raw in {"FAIL", "FAILED"} else "NA" if raw == "NA" else "NOT_PROVED"
        acceptance.append({"id": aid, "state": status, "statement": row.get("description") or row.get("statement"), "evidence": _strings(p.get("basis"))})

    inputs = []
    for row in (ep or {}).get("inputs") or []:
        if not isinstance(row, dict):
            continue
        resolution = str(row.get("resolution") or "")
        freshness = "STALE" if "STALE" in resolution else "CURRENT" if resolution in {"READY", "RESOLVED", "PASS"} else "UNKNOWN"
        inputs.append({"id": row.get("id"), "role": row.get("name"), "authority": row.get("authority"), "source_ref": row.get("source"), "freshness": freshness})

    benchmarks = []
    for row in (ep or {}).get("benchmarks") or []:
        if not isinstance(row, dict):
            continue
        required = str(row.get("applicability") or "") != "OPTIONAL"
        benchmarks.append({
            "id": row.get("id"),
            "purpose": row.get("purpose"),
            "role": row.get("name"),
            "source_ref": row.get("source"),
            "oracle": row.get("oracle_class") or row.get("independence"),
            "expected": row.get("expected"),
            "required": required,
            "current_result": "UNKNOWN",
            "evidence_basis": {"material_ref": ((checkpoint or {}).get("execution_basis") or {}).get("material_ref"), "checkpoint": checkpoint_id},
        })

    refs = {str(x) for x in (objective_id, phase_id, wp_id, ep_id) if x}
    events = _v25_events(root, refs)
    negative = []
    for event in events:
        low = event["summary"].lower()
        result = "SUPERSEDED" if "supersed" in low else "REJECTED" if "reject" in low else "FAILED" if ("fail" in low or "invalid" in low) else None
        if result:
            negative.append({
                "attempt": event["summary"],
                "result": result,
                "reason": event["summary"],
                "evidence": event["basis"],
                "retry_when": ["The cited failure or dependency basis materially changes."],
            })

    admission = source.get("task_admission") or {}
    disposition = str(admission.get("disposition") or "UNKNOWN")
    allowed_dispositions = {"MAPPED_EXISTING_WP", "REVISED_EXISTING_WP", "ADDED_EXECUTION_WP", "CREATED_ROADMAP"}
    if disposition not in allowed_dispositions:
        disposition = "UNKNOWN"

    scope = (ep or {}).get("scope") or {}
    next_steps = ((ep or {}).get("next_work") or {}).get("steps") or []
    immediate = next_steps[0].get("action") if next_steps and isinstance(next_steps[0], dict) else None
    immediate = immediate or (((state.get("status_planes") or {}).get("execution") or {}).get("next_action"))
    outcome = (ep or {}).get("outcome") or {}
    engineering = outcome.get("engineering") if isinstance(outcome, dict) else []
    task_outcome = "; ".join(str(x) for x in engineering or []) or None
    context = (ep or {}).get("context_capsule") or {}

    cp_summary = ((checkpoint or {}).get("implementation_result") or {}).get("summary")
    cp_acceptance = [x for x in (checkpoint or {}).get("acceptance_results") or [] if isinstance(x, dict)]
    cp_pass = bool(cp_acceptance) and all(str(x.get("status")) in {"PASS", "NA"} for x in cp_acceptance)
    known_true = ([str(cp_summary)] if cp_summary and cp_pass else []) + _strings((checkpoint or {}).get("discoveries"))
    unknown = _strings((checkpoint or {}).get("known_limitations")) + _strings((checkpoint or {}).get("remaining_work"))

    preserve = []
    if checkpoint_id and cp_pass:
        for row in cp_acceptance:
            if row.get("status") in {"PASS", "NA"}:
                preserve.append({
                    "claim": f"{row.get('id')} accepted at {checkpoint_id}",
                    "checkpoint": checkpoint_id,
                    "evidence": [f"{checkpoint_id}:{row.get('id')}"],
                    "reopen_if": ["Required evidence becomes stale or fails.", "A dependency, counterexample, or Owner requirement changes the accepted basis."],
                })

    route = f"SERIAL:{ep_id}" if ep_id else None
    executor = None
    custody = None
    for lease in (state.get("execution_custody") or {}).get("leases") or []:
        if isinstance(lease, dict) and lease.get("state") == "ACTIVE" and str(lease.get("route_key")) == str(route):
            custody = str(lease.get("source") or lease.get("route_key"))
            executor = ((lease.get("candidate") or {}).get("agent_instance_id"))
            break

    required_missing = [str(x.get("id")) for x in benchmarks if x.get("required") and x.get("current_result") in {"UNKNOWN", "NOT_RUN"}]
    sources = [V25_STATE, str((state.get("roadmap") or {}).get("path")), V25_PROGRESS, V25_EVENTS]
    if ep_path:
        sources.append(ep_path)
    if checkpoint_path:
        sources.append(checkpoint_path)

    issue_sections = _issue_sections(
        parent_issue_observation,
        programme_issue_observation,
        None,
        acceptance,
        checkpoint,
        None,
    )
    task = {
        "schema_version": "relay-v3.1-task-snapshot",
        "authority": "DERIVED_READ_MODEL",
        "source_protocol": "V2_5",
        "identity": {"work_package": wp_id, "ep": ep_id, "issue": None, "delivery_vehicle": None},
        "purpose": {
            "programme_outcome": (objective or {}).get("title") or ((roadmap.get("roadmap") or {}).get("title")),
            "current_goal": (phase or {}).get("title") or (wp or {}).get("title"),
            "task_outcome": task_outcome,
            "why_this_task_exists": context.get("why_this_work_exists"),
        },
        "lineage": {
            "predecessor_checkpoint": ((ep or {}).get("identity") or {}).get("previous_checkpoint") or checkpoint_id,
            "upstream_dependencies": _strings((wp or {}).get("depends_on")),
            "roadmap_admission": {"disposition": disposition, "revision": source.get("roadmap_revision") or (state.get("roadmap") or {}).get("revision"), "basis": _strings(admission.get("basis"))},
        },
        **issue_sections,
        "scope": {
            "write": _scope(scope.get("allowed"), "path"),
            "read": _scope(scope.get("allowed_reads"), "path"),
            "protected": _scope(scope.get("protected"), "path", "invariant"),
            "prohibited": _scope(scope.get("prohibited"), "domain", "decision"),
        },
        "inputs": inputs,
        "benchmarks": benchmarks,
        "benchmark_debt": {"required_missing": required_missing, "stale": [], "optional": [str(x.get("id")) for x in benchmarks if not x.get("required")]},
        "execution": {"lifecycle": state.get("relay_state"), "lease_or_custody": custody, "executor": executor, "route": route, "branch": _git(root, "rev-parse", "--abbrev-ref", "HEAD")},
        "material": {"base": ((ep or {}).get("git_basis") or {}).get("material_ref"), "current_head": _git(root, "rev-parse", "HEAD")},
        "acceptance": acceptance,
        "controls": _v25_controls(state),
        "knowledge_state": {"known_true": known_true, "known_false": [], "unknown": unknown, "assumptions": []},
        "negative_knowledge": negative,
        "preserve": {"accepted_do_not_reopen": preserve},
        "history": {"recent_events": events},
        "next": {
            "immediate_action": immediate,
            "next_value_frontier": (wp or {}).get("title") or wp_id,
            "stop_conditions": _strings(((ep or {}).get("failure_and_stop_conditions") or {}).get("hard_stop_categories")),
        },
        "reconstruction_sources": list(dict.fromkeys(x for x in sources if x)),
    }
    errors = validate_schema("task-snapshot", task, "TASK_SNAPSHOT")
    if errors:
        raise ProjectionError("; ".join(errors))
    return task


def _v3_task(
    root: Path,
    base_ref: str | None,
    parent_issue_observation: dict[str, Any] | None = None,
    programme_issue_observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state = load_yaml(root / "relay/STATE.yaml")
    project = build_project_snapshot(root, base_ref)
    roadmap = load_yaml(root / str((state.get("roadmap") or {}).get("path")))
    execution = state.get("execution") or {}
    cp_id = (state.get("accepted") or {}).get("checkpoint")
    checkpoint = _load(root / "relay/CHECKPOINTS" / f"{cp_id}.yaml") if cp_id else None
    ep_id = execution.get("ep") or ((checkpoint or {}).get("ep"))
    ep = _load(root / "relay/WORK" / f"{ep_id}.yaml") if ep_id else None
    wp_id = (ep or {}).get("work_package")
    wp = next((x for x in roadmap.get("work_packages") or [] if str((x or {}).get("id")) == str(wp_id)), None)
    lease_id = execution.get("lease")
    lease = _load(root / "relay/LEASES" / f"{lease_id}.yaml") if lease_id else None
    cp_accept = {str(x.get("id")): x for x in (checkpoint or {}).get("acceptance") or [] if isinstance(x, dict)}
    acceptance = [{
        "id": row.get("id"),
        "state": (cp_accept.get(str(row.get("id"))) or {}).get("result") or "NOT_PROVED",
        "statement": row.get("statement"),
        "evidence": _strings((cp_accept.get(str(row.get("id"))) or {}).get("evidence")),
    } for row in (ep or {}).get("acceptance") or [] if isinstance(row, dict)]
    handoff = (checkpoint or {}).get("handoff") or {}
    native_controls = load_yaml(root / str((state.get("controls") or {}).get("path")))
    issue_sections = _issue_sections(
        parent_issue_observation,
        programme_issue_observation,
        ep,
        acceptance,
        checkpoint,
        native_controls,
    )
    task = {
        "schema_version": "relay-v3.1-task-snapshot",
        "authority": "DERIVED_READ_MODEL",
        "source_protocol": "V3_1",
        "identity": {"work_package": wp_id, "ep": ep_id, "issue": (project.get("delivery") or {}).get("issue"), "delivery_vehicle": (project.get("delivery") or {}).get("pr") or (project.get("delivery") or {}).get("issue")},
        "purpose": {
            "programme_outcome": (roadmap.get("owner") or {}).get("outcome"),
            "current_goal": (roadmap.get("owner") or {}).get("current_goal"),
            "task_outcome": ((ep or {}).get("outcome") or {}).get("statement"),
            "why_this_task_exists": (wp or {}).get("title"),
        },
        "lineage": {
            "predecessor_checkpoint": ((ep or {}).get("basis") or {}).get("predecessor_checkpoint"),
            "upstream_dependencies": _strings((wp or {}).get("depends_on")),
            "roadmap_admission": {"disposition": "MIGRATED_EXISTING_WP" if (root / MIGRATION_REPORT).exists() else "MAPPED_EXISTING_WP", "revision": (state.get("roadmap") or {}).get("revision"), "basis": ["relay/ROADMAP/ROADMAP.yaml"]},
        },
        **issue_sections,
        "scope": {"write": _strings(((ep or {}).get("scope") or {}).get("write")), "read": _strings(((ep or {}).get("scope") or {}).get("read")), "protected": _strings(((ep or {}).get("scope") or {}).get("protect")), "prohibited": _strings(((ep or {}).get("scope") or {}).get("prohibit"))},
        "inputs": [],
        "benchmarks": [],
        "benchmark_debt": {"required_missing": [], "stale": [], "optional": []},
        "execution": {"lifecycle": execution.get("lifecycle"), "lease_or_custody": lease_id, "executor": ((lease or {}).get("executor") or {}).get("id") if lease else None, "route": execution.get("route"), "branch": _git(root, "rev-parse", "--abbrev-ref", "HEAD")},
        "material": {"base": (project.get("material") or {}).get("base"), "current_head": (project.get("material") or {}).get("head")},
        "acceptance": acceptance,
        "controls": _v3_controls(root, state),
        "knowledge_state": {"known_true": _strings(handoff.get("what_is_true_now")), "known_false": [], "unknown": _strings(handoff.get("what_remains_uncertain")), "assumptions": []},
        "negative_knowledge": [{"attempt": str(x), "result": "REJECTED", "reason": str(x), "evidence": [cp_id] if cp_id else [], "retry_when": ["New evidence invalidates the rejection basis."]} for x in handoff.get("attempted_and_rejected") or []],
        "preserve": {"accepted_do_not_reopen": [{"claim": str(x), "checkpoint": cp_id, "evidence": [cp_id] if cp_id else [], "reopen_if": ["A benchmark fails or becomes stale.", "A dependency, counterexample, or Owner requirement changes."]} for x in handoff.get("what_is_true_now") or []]},
        "history": {"recent_events": []},
        "next": {"immediate_action": ((ep or {}).get("next") or {}).get("first_action"), "next_value_frontier": (wp or {}).get("title"), "stop_conditions": _strings(((ep or {}).get("next") or {}).get("stop_conditions"))},
        "reconstruction_sources": ["relay/ROADMAP/ROADMAP.yaml", "relay/STATE.yaml", "relay/CONTROLS/controls.yaml"] + ([f"relay/WORK/{ep_id}.yaml"] if ep_id else []) + ([f"relay/CHECKPOINTS/{cp_id}.yaml"] if cp_id else []),
    }
    errors = validate_schema("task-snapshot", task, "TASK_SNAPSHOT")
    if errors:
        raise ProjectionError("; ".join(errors))
    return task


def _use_v3_source(root: Path) -> bool:
    resolved = resolve_protocol(root)
    if resolved.get("status") == "INVALID":
        raise ProjectionError(resolved.get("warning") or "Relay protocol authority is ambiguous")
    if resolved.get("authority_mode") == "NATIVE" and resolved.get("status") == "ACTIVE":
        return True
    if resolved.get("authority_mode") == "LEGACY":
        return False
    raise ProjectionError("Relay authority mode is not deterministically resolved")


def build_task(
    root: Path,
    base_ref: str | None = None,
    parent_issue_observation: dict[str, Any] | None = None,
    programme_issue_observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return (
        _v3_task(root, base_ref, parent_issue_observation, programme_issue_observation)
        if _use_v3_source(root)
        else _v25_task(root, parent_issue_observation, programme_issue_observation)
    )


def _v25_improvement(root: Path) -> dict[str, Any]:
    state = load_yaml(root / V25_STATE)
    checkpoint, cp_id, cp_path = _v25_checkpoint(root, state)
    ep_id = (checkpoint or {}).get("ep_id")
    ep = _load(root / f"agents/relay/execution-packages/{ep_id}.yaml") if ep_id else None
    acceptance = [x for x in (checkpoint or {}).get("acceptance_results") or [] if isinstance(x, dict)]
    validations = [x for x in (checkpoint or {}).get("validation_results") or [] if isinstance(x, dict)]
    accepted = bool(acceptance) and all(str(x.get("status")) in {"PASS", "NA"} for x in acceptance)
    implementation = (checkpoint or {}).get("implementation_result") or {}
    changed = _strings(implementation.get("files_changed"))
    summary = implementation.get("summary")
    successor = (checkpoint or {}).get("successor") or {}
    recon = (checkpoint or {}).get("roadmap_reconciliation") or {}
    disposition = {"NO_ROADMAP_CHANGE": "PRESERVE", "STATUS_UPDATE": "CLOSE_WP", "ROADMAP_PROPOSAL": "REVISE_WP", "OWNER_DECISION_REQUIRED": "OTHER"}.get(str(recon.get("result") or ""), "OTHER")
    capability = [str(summary)] if accepted and changed and summary else []
    view = {
        "schema_version": "relay-v3.1-improvement-view",
        "authority": "DERIVED_READ_MODEL",
        "source_protocol": "V2_5",
        "task": ep_id,
        "checkpoint": cp_id,
        "from": {"predecessor_checkpoint": ((ep or {}).get("identity") or {}).get("previous_checkpoint"), "material_basis": ((ep or {}).get("git_basis") or {}).get("material_ref")},
        "to": {"accepted_checkpoint": cp_id if accepted else None, "material_basis": ((checkpoint or {}).get("execution_basis") or {}).get("material_ref")},
        "improvement": {
            "capability_added": [],
            "capability_strengthened": capability,
            "evidence_added": [f"{x.get('id')}={x.get('status')}" for x in validations + acceptance if x.get("status") in {"PASS", "NA"}],
            "understanding_improved": _strings((checkpoint or {}).get("discoveries")),
            "downstream_unlocked": [str(x) for x in (successor.get("frontier_work_package"), successor.get("ep_id")) if x],
            "controls_resolved": [],
            "controls_created": [],
        },
        "roadmap_effect": {"concept_change": "NO_CONCEPT_CHANGE", "execution_disposition": disposition, "roadmap_revision": (state.get("roadmap") or {}).get("revision")},
        "not_improved": [] if capability else ["No accepted capability improvement is inferred from this checkpoint."],
        "still_not_proved": _strings((checkpoint or {}).get("known_limitations")) + _strings((checkpoint or {}).get("remaining_work")) + [str(x.get("id")) for x in validations if x.get("status") in {"FAIL", "NOT_RUN"}],
        "new_questions": _strings(recon.get("owner_decisions_required")),
        "reconstruction_sources": [V25_STATE, cp_path or "agents/relay/checkpoints/", f"agents/relay/execution-packages/{ep_id}.yaml" if ep_id else "agents/relay/execution-packages/", V25_PROGRESS, V25_EVENTS],
    }
    errors = validate_schema("improvement-view", view, "IMPROVEMENT_VIEW")
    if errors:
        raise ProjectionError("; ".join(errors))
    return view


def _v31_roadmap_effect(
    root: Path,
    state: dict[str, Any],
    ep_id: str | None,
    checkpoint_id: str | None,
) -> dict[str, Any]:
    events_path = root / "relay/EVENTS.jsonl"
    rows: list[dict[str, Any]] = []
    if events_path.exists():
        for raw in events_path.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if row.get("type") == "ROADMAP_RECONCILED":
                details = row.get("details") or {}
                if details.get("ep") == ep_id and details.get("checkpoint") == checkpoint_id:
                    rows.append(row)
    if not rows:
        return {
            "concept_change": "UNKNOWN",
            "execution_disposition": "PRESERVE",
            "roadmap_revision": (state.get("roadmap") or {}).get("revision"),
        }
    latest = rows[-1]
    disposition = str((latest.get("details") or {}).get("disposition") or "UNKNOWN")
    return {
        "concept_change": "NO_CONCEPT_CHANGE" if disposition == "NO_CHANGE" else "RECONCILED",
        "execution_disposition": disposition,
        "roadmap_revision": (state.get("roadmap") or {}).get("revision"),
    }


def _v3_improvement(root: Path) -> dict[str, Any]:
    state = load_yaml(root / "relay/STATE.yaml")
    cp_id = (state.get("accepted") or {}).get("checkpoint")
    checkpoint = _load(root / "relay/CHECKPOINTS" / f"{cp_id}.yaml") if cp_id else None
    ep_id = (checkpoint or {}).get("ep")
    ep = _load(root / "relay/WORK" / f"{ep_id}.yaml") if ep_id else None
    acceptance = [x for x in (checkpoint or {}).get("acceptance") or [] if isinstance(x, dict)]
    accepted = bool(acceptance) and all(x.get("result") == "PASS" for x in acceptance)
    handoff = (checkpoint or {}).get("handoff") or {}
    view = {
        "schema_version": "relay-v3.1-improvement-view",
        "authority": "DERIVED_READ_MODEL",
        "source_protocol": "V3_1",
        "task": ep_id,
        "checkpoint": cp_id,
        "from": {"predecessor_checkpoint": ((ep or {}).get("basis") or {}).get("predecessor_checkpoint"), "material_basis": ((ep or {}).get("basis") or {}).get("material_base")},
        "to": {"accepted_checkpoint": cp_id if accepted else None, "material_basis": ((checkpoint or {}).get("material_result") or {}).get("head")},
        "improvement": {
            "capability_added": [],
            "capability_strengthened": _strings(handoff.get("what_changed")) if accepted else [],
            "evidence_added": [f"{k}={v}" for k, v in ((checkpoint or {}).get("validation") or {}).items() if v in {"PASS", "NOT_APPLICABLE"}],
            "understanding_improved": _strings((checkpoint or {}).get("discoveries")),
            "downstream_unlocked": _strings(handoff.get("resume_from")),
            "controls_resolved": [],
            "controls_created": [],
        },
        "roadmap_effect": _v31_roadmap_effect(root, state, ep_id, cp_id),
        "not_improved": [] if accepted and handoff.get("what_changed") else ["No capability improvement is inferred without accepted checkpoint evidence."],
        "still_not_proved": _strings((checkpoint or {}).get("known_limitations")) + _strings(handoff.get("what_remains_uncertain")),
        "new_questions": [],
        "reconstruction_sources": ["relay/STATE.yaml", f"relay/CHECKPOINTS/{cp_id}.yaml" if cp_id else "relay/CHECKPOINTS/", f"relay/WORK/{ep_id}.yaml" if ep_id else "relay/WORK/", "relay/EVENTS.jsonl"],
    }
    errors = validate_schema("improvement-view", view, "IMPROVEMENT_VIEW")
    if errors:
        raise ProjectionError("; ".join(errors))
    return view


def build_improvement(root: Path) -> dict[str, Any]:
    return _v3_improvement(root) if _use_v3_source(root) else _v25_improvement(root)


def _run_v25(root: Path, script: str) -> tuple[bool, str]:
    path = V25_ROOT / "scripts" / script
    proc = subprocess.run([sys.executable, str(path), str(root)], cwd=V25_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tail = " | ".join(x.strip() for x in proc.stdout.splitlines()[-4:] if x.strip())
    return proc.returncode == 0, f"{script} exit={proc.returncode}" + (f": {tail}" if tail else "")


def assess_continuity(root: Path, base_ref: str | None = None) -> dict[str, Any]:
    migration = _load(root / MIGRATION_REPORT)
    if not migration:
        raise ProjectionError("V3.1 migration report is required before continuity assessment")
    state = load_yaml(root / V25_STATE)
    before_entries, before = legacy_inventory(root)
    selection = _load(root / PROTOCOL_SELECTION) or {}
    freeze_digest = str(((selection.get("cutover") or {}).get("legacy_freeze_digest")) or "")
    expected = freeze_digest or str((migration.get("source") or {}).get("legacy_tree_digest") or "")
    task = build_task(root, base_ref)
    improvement = build_improvement(root)
    _, after = legacy_inventory(root)

    checks = {}
    evidence = []
    checks["legacy_history_preserved"] = "PASS" if before == after == expected else "FAIL"
    evidence.append(f"legacy digest expected={expected} before={before} after={after} files={len(before_entries)}")

    admission = (task.get("lineage") or {}).get("roadmap_admission") or {}
    checks["roadmap_admission"] = "PASS" if (not (task.get("identity") or {}).get("ep") or admission.get("disposition") != "UNKNOWN") else "FAIL"
    evidence.append(f"roadmap admission={admission.get('disposition')} revision={admission.get('revision')}")

    event_ok, event_basis = _run_v25(root, "validate_roadmap_events.py")
    checks["roadmap_events"] = "PASS" if event_ok else "FAIL"
    evidence.append(event_basis)

    progress_ok, progress_basis = _run_v25(root, "validate_progress.py")
    cp = state.get("last_checkpoint") or {}
    cp_id = cp.get("id")
    cp_path = cp.get("path")
    cp_exists = cp_id in {None, "", "NONE"} or bool(cp_path and (root / str(cp_path)).exists())
    checkpoint_ok = True
    checkpoint_basis = "checkpoint=NONE"
    if cp_id not in {None, "", "NONE"}:
        if not cp_exists:
            checkpoint_ok = False
            checkpoint_basis = f"checkpoint={cp_id} missing"
        else:
            validator = V25_ROOT / "scripts" / "validate_checkpoint.py"
            proc = subprocess.run(
                [sys.executable, str(validator), str((root / str(cp_path)).resolve())],
                cwd=V25_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            checkpoint_ok = proc.returncode == 0
            tail = " | ".join(x.strip() for x in proc.stdout.splitlines()[-4:] if x.strip())
            checkpoint_basis = f"validate_checkpoint.py exit={proc.returncode}" + (f": {tail}" if tail else "")
    checks["checkpoint_progress"] = "PASS" if progress_ok and cp_exists and checkpoint_ok else "FAIL"
    evidence.append(f"{progress_basis}; {checkpoint_basis}; checkpoint={cp_id} exists={cp_exists}")

    ep = _load(root / str((state.get("active_ep") or {}).get("path"))) if (state.get("active_ep") or {}).get("path") else None
    history_discovery = int(((migration.get("legacy_inventory") or {}).get("category_counts") or {}).get("DISCOVERY", 0))
    discovery_count = len((ep or {}).get("repository_discovery") or [])
    checks["discovery"] = "PASS" if discovery_count or history_discovery else "FAIL"
    evidence.append(f"discovery active_steps={discovery_count} historical_receipts={history_discovery}")

    owner_mechanisms = [V25_ROOT / "scripts/owner_publication.py", V25_ROOT / "scripts/render_owner_status.py", V25_ROOT / "scripts/owner_change_projection.py"]
    checks["owner_delta"] = "PASS" if all(x.exists() for x in owner_mechanisms) else "FAIL"
    evidence.append("owner delta mechanisms=" + ",".join(x.name for x in owner_mechanisms if x.exists()))

    handover_mechanism = V25_ROOT / "scripts/handover_planning.py"
    task_identity = task.get("identity") or {}
    task_present = bool(task_identity.get("ep"))
    intelligence = bool(task.get("inputs") or task.get("benchmarks") or (task.get("history") or {}).get("recent_events") or (task.get("acceptance") or []))
    # An idle repository may legitimately have no current task-local intelligence.
    # Continuity means the handover mechanism remains available and, when a task
    # exists, the task projection actually carries durable intelligence.
    handover_preserved = handover_mechanism.exists() and (not task_present or intelligence)
    checks["handover_intelligence"] = "PASS" if handover_preserved else "FAIL"
    evidence.append(
        f"handover planner={handover_mechanism.exists()} task_present={task_present} task_intelligence={intelligence}"
    )

    derived = task.get("authority") == "DERIVED_READ_MODEL" and improvement.get("authority") == "DERIVED_READ_MODEL" and before == after
    checks["generated_projection_non_authority"] = "PASS" if derived else "FAIL"
    evidence.append(f"derived views task={task.get('authority')} improvement={improvement.get('authority')} legacy_unchanged={before == after}")

    report = {
        "schema_version": "relay-v3.1-intelligence-continuity",
        "authority": "DERIVED_CONTINUITY_ASSESSMENT",
        "ready": all(x == "PASS" for x in checks.values()),
        "source": {"protocol": "V2_5", "legacy_tree_digest": before, "roadmap_revision": (state.get("roadmap") or {}).get("revision")},
        "projections": {"task_snapshot_digest": canonical_digest(task), "improvement_view_digest": canonical_digest(improvement)},
        "checks": checks,
        "evidence": evidence,
    }
    errors = validate_schema("intelligence-continuity", report, "INTELLIGENCE_CONTINUITY")
    if errors:
        raise ProjectionError("; ".join(errors))
    return report


def _write(root: Path, path: str | None, value: dict[str, Any]) -> None:
    payload = yaml.safe_dump(value, sort_keys=False)
    if path:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Relay V3 task/improvement read models or prove V2.5 intelligence continuity.")
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("kind", choices=["task", "improvement", "continuity"])
    parser.add_argument("--base-ref")
    parser.add_argument("--output")
    parser.add_argument("--task-output")
    parser.add_argument("--improvement-output")
    parser.add_argument("--parent-issue-observation", help="Owned child/work-issue provider observation")
    parser.add_argument("--programme-issue-observation", help="Optional governing programme-parent provider observation")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    parent_issue_observation = load_yaml(Path(args.parent_issue_observation)) if args.parent_issue_observation else None
    programme_issue_observation = load_yaml(Path(args.programme_issue_observation)) if args.programme_issue_observation else None
    if args.kind == "task":
        _write(
            root,
            args.output,
            build_task(root, args.base_ref, parent_issue_observation, programme_issue_observation),
        )
        return
    if args.kind == "improvement":
        _write(root, args.output, build_improvement(root))
        return
    report = assess_continuity(root, args.base_ref)
    if args.task_output:
        _write(
            root,
            args.task_output,
            build_task(root, args.base_ref, parent_issue_observation, programme_issue_observation),
        )
    if args.improvement_output:
        _write(root, args.improvement_output, build_improvement(root))
    _write(root, args.output, report)
    raise SystemExit(0 if report["ready"] else 1)


if __name__ == "__main__":
    main()
