from __future__ import annotations

from typing import Any

from v3lib import validate_schema


LINEAGE_RELATIONSHIPS = {"SUPERSEDED_BY", "TRANSFERS_TO", "SPLIT_INTO"}


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


def require_ready(reconciliation: dict[str, Any]) -> None:
    if reconciliation.get("status") in {"READY", "NOT_REQUIRED"}:
        return
    reasons = ", ".join(reconciliation.get("reason_codes") or [])
    raise RuntimeError(f"PROGRAMME_RECONCILIATION_REQUIRED: {reasons}")
