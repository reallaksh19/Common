from __future__ import annotations

from typing import Any

from v3lib import validate_schema


LINEAGE_RELATIONSHIPS = {"SUPERSEDED_BY", "TRANSFERS_TO", "SPLIT_INTO"}
SELECTED_FRONTIER_BOUNDARIES = {"ADMIT_TASK", "RECOVERY_TAKEOVER"}
SWITCHABLE_BOUNDARIES = {"HANDOVER", "NEXT_WORK"}


def _ref(observation: dict[str, Any]) -> str:
    return f"{observation.get('repository')}#{observation.get('issue_number')}"


def _acceptance_summary(observation: dict[str, Any]) -> dict[str, int]:
    counts = {
        "complete": 0,
        "partial": 0,
        "pending": 0,
        "blocked": 0,
        "deferred": 0,
        "not_applicable": 0,
        "unknown": 0,
    }
    mapping = {
        "COMPLETE": "complete",
        "PARTIAL": "partial",
        "PENDING": "pending",
        "BLOCKED": "blocked",
        "DEFERRED": "deferred",
        "NOT_APPLICABLE": "not_applicable",
        "UNKNOWN": "unknown",
    }
    rows = ((observation.get("current_contract") or {}).get("acceptance_items") or [])
    for row in rows:
        state = str((row or {}).get("state") or "UNKNOWN")
        counts[mapping.get(state, "unknown")] += 1
    counts["total"] = len(rows)
    return counts


def _ownership(observation: dict[str, Any], summary: dict[str, int]) -> str:
    disposition = str(observation.get("disposition") or "UNKNOWN")
    state = str(observation.get("state") or "UNKNOWN")

    if disposition == "SUPERSEDE":
        return "SUPERSEDED"
    if disposition == "TRANSFER":
        return "TRANSFERRED"
    if disposition == "SPLIT":
        return "SPLIT"
    if disposition == "CLOSE" or state == "CLOSED":
        unresolved = (
            summary["partial"]
            + summary["pending"]
            + summary["blocked"]
            + summary["deferred"]
            + summary["unknown"]
        )
        return "CLOSED_WITH_DEBT" if unresolved else "LANDED"
    if state == "UNKNOWN" or disposition == "UNKNOWN":
        return "UNKNOWN"
    if summary["blocked"]:
        return "BLOCKED"
    if summary["deferred"] and not (summary["partial"] or summary["pending"] or summary["unknown"]):
        return "DEFERRED"
    if summary["partial"] or summary["pending"] or summary["unknown"]:
        return "STILL_REAL"
    if summary["total"] and summary["complete"] + summary["not_applicable"] == summary["total"]:
        return "READY_TO_CLOSE"
    return "STILL_REAL"


def build(
    observations: list[dict[str, Any]] | None,
    *,
    current_parent_ref: str | None = None,
) -> dict[str, Any]:
    """Build an ordered programme-parent reconciliation read model.

    Input order is preserved as the caller's reconciled programme order. The
    result is derived only: it does not mutate ROADMAP, issue state, or EP state.
    """

    observations = list(observations or [])
    if not observations:
        return {
            "authority": "DERIVED_PROGRAMME_RECONCILIATION",
            "status": "NOT_REQUIRED",
            "current_parent": current_parent_ref,
            "parents": [],
            "ordered_roadmap": [],
            "programme_frontier": [],
            "execution_blocked": [],
            "acceptance_debt": [],
            "delivery_governance_debt": [],
            "deferred_or_future": [],
            "graph": [],
            "reason_codes": [],
        }

    parents: list[dict[str, Any]] = []
    graph: list[dict[str, Any]] = []
    reason_codes: list[str] = []
    seen: set[str] = set()

    for index, observation in enumerate(observations):
        errors = validate_schema("parent-issue-observation", observation, f"PROGRAMME_PARENT[{index}]")
        if errors:
            raise ValueError("; ".join(errors))
        ref = _ref(observation)
        if ref in seen:
            reason_codes.append(f"DUPLICATE_PARENT:{ref}")
            continue
        seen.add(ref)
        summary = _acceptance_summary(observation)
        ownership = _ownership(observation, summary)
        if ownership == "UNKNOWN":
            reason_codes.append(f"UNRESOLVED_PARENT:{ref}")

        row = {
            "order": index + 1,
            "ref": ref,
            "repository": observation.get("repository"),
            "issue_number": observation.get("issue_number"),
            "title": observation.get("title"),
            "state": observation.get("state"),
            "disposition": observation.get("disposition"),
            "ownership": ownership,
            "acceptance": summary,
        }
        parents.append(row)

        for relationship in observation.get("relationships") or []:
            target = relationship.get("target") or {}
            target_ref = f"{target.get('repository')}#{target.get('issue_number')}"
            graph.append({
                "from": ref,
                "type": relationship.get("type"),
                "to": target_ref,
                "scope": list(relationship.get("scope") or []),
                "acceptance_items": list(relationship.get("acceptance_items") or []),
                "provider_refs": list(relationship.get("provider_refs") or []),
            })

    if current_parent_ref and current_parent_ref not in seen:
        reason_codes.append(f"CURRENT_PARENT_MISSING:{current_parent_ref}")

    for edge in graph:
        if edge["type"] in LINEAGE_RELATIONSHIPS and edge["to"] not in seen:
            reason_codes.append(f"LINEAGE_TARGET_UNOBSERVED:{edge['to']}")

    programme_frontier = [
        row["ref"] for row in parents if row["ownership"] == "STILL_REAL"
    ]
    execution_blocked = [
        row["ref"] for row in parents if row["ownership"] == "BLOCKED"
    ]
    acceptance_debt = [
        row["ref"] for row in parents if row["ownership"] == "CLOSED_WITH_DEBT"
    ]
    delivery_governance_debt = [
        row["ref"] for row in parents if row["ownership"] == "READY_TO_CLOSE"
    ]
    deferred_or_future = [
        row["ref"] for row in parents if row["ownership"] in {"DEFERRED", "TRANSFERRED", "SPLIT"}
    ]

    ordered_roadmap = [
        {
            "order": row["order"],
            "ref": row["ref"],
            "ownership": row["ownership"],
        }
        for row in parents
    ]

    return {
        "authority": "DERIVED_PROGRAMME_RECONCILIATION",
        "status": "RECONCILIATION_REQUIRED" if reason_codes else "READY",
        "current_parent": current_parent_ref,
        "parents": parents,
        "ordered_roadmap": ordered_roadmap,
        "programme_frontier": programme_frontier,
        "execution_blocked": execution_blocked,
        "acceptance_debt": acceptance_debt,
        "delivery_governance_debt": delivery_governance_debt,
        "deferred_or_future": deferred_or_future,
        "graph": graph,
        "reason_codes": reason_codes,
    }


def parent_ref(parent: dict[str, Any] | None) -> str | None:
    value = parent or {}
    repository = value.get("repository")
    number = value.get("number")
    return f"{repository}#{number}" if repository and number else None


def observation_ref(observation: dict[str, Any] | None) -> str | None:
    value = observation or {}
    repository = value.get("repository")
    number = value.get("issue_number")
    return f"{repository}#{number}" if repository and number else None


def assess_boundary(
    parent: dict[str, Any] | None,
    observations: list[dict[str, Any]] | None,
    *,
    boundary: str,
    current_observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Canonical programme decision for actor-change / next-work boundaries.

    The result is a derived decision only. It never mutates ROADMAP, provider
    state, EP state, or action authority.
    """

    boundary = str(boundary).upper()
    if boundary not in SELECTED_FRONTIER_BOUNDARIES | SWITCHABLE_BOUNDARIES:
        raise ValueError(f"unsupported programme boundary: {boundary}")

    selected_ref = parent_ref(parent)
    explicit = list(observations or [])
    selected_observation = None

    if not selected_ref:
        reconciliation = build([], current_parent_ref=None)
        return {
            "status": "READY",
            "boundary": boundary,
            "mode": "NOT_PROVIDER_BACKED",
            "selected_parent": None,
            "selected_ownership": None,
            "selected_observation": None,
            "next_frontier": None,
            "continuation": "NOT_APPLICABLE",
            "reason_codes": [],
            "reconciliation": reconciliation,
        }

    if explicit:
        supplied = explicit
        selected_observation = next(
            (row for row in explicit if observation_ref(row) == selected_ref),
            None,
        )
    elif current_observation is not None:
        supplied = [current_observation]
        selected_observation = current_observation if observation_ref(current_observation) == selected_ref else None
    else:
        status = (
            "PROGRAMME_CURRENTNESS_REQUIRED"
            if boundary == "HANDOVER"
            else "PROGRAMME_RECONCILIATION_REQUIRED"
        )
        return {
            "status": status,
            "boundary": boundary,
            "mode": "MISSING_PROVIDER_OBSERVATION",
            "selected_parent": selected_ref,
            "selected_ownership": None,
            "selected_observation": None,
            "next_frontier": None,
            "continuation": "BLOCK",
            "reason_codes": ["PARENT_PROVIDER_STATE_REQUIRED"],
            "reconciliation": build([], current_parent_ref=selected_ref),
        }

    # Handover may use a single live current-parent readback as a cheap
    # continuation proof. Unknown provider state/disposition is currentness debt,
    # not a fully reconciled programme decision.
    if boundary == "HANDOVER" and not explicit and selected_observation is not None:
        state = str(selected_observation.get("state") or "UNKNOWN")
        disposition = str(selected_observation.get("disposition") or "UNKNOWN")
        missing = []
        if state == "UNKNOWN":
            missing.append("PARENT_PROVIDER_STATE_REQUIRED")
        if disposition == "UNKNOWN":
            missing.append("PARENT_DISPOSITION_REQUIRED")
        if missing:
            return {
                "status": "PROGRAMME_CURRENTNESS_REQUIRED",
                "boundary": boundary,
                "mode": "SINGLE_PARENT_CURRENTNESS",
                "selected_parent": selected_ref,
                "selected_ownership": None,
                "selected_observation": selected_observation,
                "next_frontier": None,
                "continuation": "BLOCK",
                "reason_codes": missing,
                "reconciliation": build([], current_parent_ref=selected_ref),
            }

    reconciliation = build(supplied, current_parent_ref=selected_ref)
    if reconciliation.get("status") != "READY":
        return {
            "status": "PROGRAMME_RECONCILIATION_REQUIRED",
            "boundary": boundary,
            "mode": "ORDERED_PARENT_SET" if explicit else "SINGLE_PARENT_CURRENTNESS",
            "selected_parent": selected_ref,
            "selected_ownership": None,
            "selected_observation": selected_observation,
            "next_frontier": (reconciliation.get("programme_frontier") or [None])[0],
            "continuation": "BLOCK",
            "reason_codes": list(reconciliation.get("reason_codes") or []),
            "reconciliation": reconciliation,
        }

    selected_row = next(
        (row for row in reconciliation.get("parents") or [] if row.get("ref") == selected_ref),
        {},
    )
    selected_ownership = selected_row.get("ownership") or "UNKNOWN"
    frontier = list(reconciliation.get("programme_frontier") or [])
    next_frontier = frontier[0] if frontier else None

    if boundary in SELECTED_FRONTIER_BOUNDARIES and selected_ref not in frontier:
        return {
            "status": "PROGRAMME_FRONTIER_MISMATCH",
            "boundary": boundary,
            "mode": "ORDERED_PARENT_SET",
            "selected_parent": selected_ref,
            "selected_ownership": selected_ownership,
            "selected_observation": selected_observation,
            "next_frontier": next_frontier,
            "continuation": "BLOCK",
            "reason_codes": [f"SELECTED_PARENT_{selected_ownership}"],
            "reconciliation": reconciliation,
        }

    if boundary == "HANDOVER" and not explicit and selected_ref not in frontier:
        return {
            "status": "PROGRAMME_RECONCILIATION_REQUIRED",
            "boundary": boundary,
            "mode": "SINGLE_PARENT_CURRENTNESS",
            "selected_parent": selected_ref,
            "selected_ownership": selected_ownership,
            "selected_observation": selected_observation,
            "next_frontier": next_frontier,
            "continuation": "BLOCK",
            "reason_codes": [f"SELECTED_PARENT_{selected_ownership}"],
            "reconciliation": reconciliation,
        }

    continuation = (
        "CONTINUE_CURRENT"
        if selected_ref in frontier
        else "SWITCH_FRONTIER"
        if next_frontier
        else "NO_IMPLEMENTATION_FRONTIER"
    )
    return {
        "status": "READY",
        "boundary": boundary,
        "mode": "ORDERED_PARENT_SET" if explicit else "SINGLE_PARENT_CURRENTNESS",
        "selected_parent": selected_ref,
        "selected_ownership": selected_ownership,
        "selected_observation": selected_observation,
        "next_frontier": next_frontier,
        "continuation": continuation,
        "reason_codes": [],
        "reconciliation": reconciliation,
    }


def require_boundary_ready(assessment: dict[str, Any]) -> dict[str, Any]:
    if assessment.get("status") == "READY":
        return assessment

    status = str(assessment.get("status") or "PROGRAMME_RECONCILIATION_REQUIRED")
    selected = assessment.get("selected_parent")
    ownership = assessment.get("selected_ownership")
    reasons = ", ".join(assessment.get("reason_codes") or [])
    if status == "PROGRAMME_FRONTIER_MISMATCH":
        raise RuntimeError(
            f"{status} before {assessment.get('boundary')}: "
            f"{selected} is {ownership}, not STILL_REAL"
        )
    raise RuntimeError(
        f"{status} before {assessment.get('boundary')}: "
        f"parent {selected} cannot determine the programme frontier"
        + (f" ({reasons})" if reasons else "")
    )
