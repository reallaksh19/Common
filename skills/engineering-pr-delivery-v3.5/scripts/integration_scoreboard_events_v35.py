"""R4 event selection only; event payload NEVER supplies authority or progress.

GitHub event data filters whether a preapproved graph/leaf/PR should be read
again; the publisher must always fetch current graph-bound GitHub truth itself.
This does not install a workflow or create a background scheduler.
"""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any

import delp_projection_v35 as DELP


class EventError(ValueError):
    pass


def _number(data: Any) -> int | None:
    try:
        n = int(data)
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def event_scope(
    graph: Mapping[str, Any],
    responsibility_ref: str,
    pr_number: int,
    event_name: str,
    event: Mapping[str, Any],
    actor: str | None = None,
) -> dict[str, Any]:
    """SELECT or SKIP a pull/issue/check event; never authorize source mutation."""
    if not isinstance(event, Mapping):
        raise EventError("GitHub event payload must be an object")
    indexed = DELP.validate_graph(graph)
    node = indexed["nodes"].get(responsibility_ref)
    if not node or node["kind"] != "LEAF" or (
        not node.get("primary_pr") or
        DELP.ref_number(node["primary_pr"]) != pr_number
    ):
        raise EventError("event requested a foreign leaf or PR")
    leaf_n, root_n = DELP.ref_number(responsibility_ref), DELP.ref_number(indexed["root"])
    selected = False
    why = "UNRELATED_OR_UNSUPPORTED_EVENT"
    # A human workflow_dispatch is only a request to *re-fetch* trusted GitHub
    # graph and scored facts. Event inputs grant no graph, role or write authority;
    # the production apply path still validates both distinct Owner receipts.
    if event_name == "workflow_dispatch":
        selected = True
        why = "EXPLICIT_MANUAL_PROVIDER_RECONCILIATION_ONLY"
    # Avoid a managed LIVE_STATUS comment recursively triggering itself.
    elif event_name in ("issue_comment", "issues"):
        observed = _number((event.get("issue") or {}).get("number"))
        selected = observed in (leaf_n, root_n, pr_number)
        why = "DECLARED_RELATED_ISSUE" if selected else "UNRELATED_ISSUE"
        if selected and event_name == "issue_comment" and str(actor or "").lower().endswith("[bot]"):
            selected = False
            why = "BOT_MANAGED_COMMENT_NO_LOOP"
    elif event_name in ("pull_request", "pull_request_target", "pull_request_review", "pull_request_review_comment"):
        selected = _number((event.get("pull_request") or {}).get("number") or event.get("number")) == pr_number
        why = "DECLARED_PRIMARY_PR" if selected else "UNRELATED_PR"
    elif event_name in ("check_run", "check_suite", "workflow_run"):
        payload = event.get(event_name) or {}
        pulls = payload.get("pull_requests") or []
        selected = any(_number(p.get("number")) == pr_number for p in pulls if isinstance(p, Mapping))
        why = "DECLARED_PR_CHECK_EVENT" if selected else "CHECK_HAS_NO_DECLARED_PR"
    # We do not make any read/write decision based on event-authored percentages
    # or PR head: those are fetched afresh from the GitHub API by R2/R4.
    return {"decision": "SELECT" if selected else "SKIP", "reason": why,
            "repository": indexed["programme"].get("repository"),
            "responsibility_ref": responsibility_ref, "pr_number": pr_number}
