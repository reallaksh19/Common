#!/usr/bin/env python3
"""Owner-authorized same-principal Local stage transitions.

This contract preserves stage identity even when principal identity collapses. A
same principal may execute successive roles only with scoped ROLE_EXECUTION
authority and a fresh stage boundary/replay. Principal independence is then
truthfully DEGRADED; pinned-oracle independence is not fabricated from the actor.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from acceptance_basis import require_grant

ORDER = ["CODER", "REVIEWER", "COORDINATOR"]
REVIEW_ROLES = {"REVIEWER", "COORDINATOR"}


class RoleTransitionError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RoleTransitionError(message)


def transition_contract(
    *,
    task: dict[str, Any],
    previous_stage: str,
    previous_executor: str,
    next_stage: str,
    next_executor: str,
    grants: list[dict[str, Any]],
    at: datetime,
    previous_end_published: bool,
    previous_timer_stopped: bool,
    fresh_start_published: bool,
    fresh_timer_armed: bool,
    fresh_reconstruction: bool,
    fresh_role_replay: bool,
) -> dict[str, Any]:
    require(task.get("kind") == "RESPONSIBILITY", "Role-collapse contract applies to native RESPONSIBILITY tasks")
    require(previous_stage in ORDER and next_stage in ORDER, "Unknown production stage")
    require(ORDER.index(next_stage) == ORDER.index(previous_stage) + 1, "Role transition must remain forward-only and adjacent")
    require(next_executor in task["role_principals"][next_stage], "Next executor is not authorized for target role")
    require(previous_end_published, "Previous role END evidence must be published before transition")
    require(previous_timer_stopped, "Previous role timer accounting must stop at stage boundary")
    require(fresh_start_published, "Next role requires fresh START evidence")
    require(fresh_timer_armed, "Next role requires a fresh role timer")
    require(fresh_reconstruction, "Next role requires fresh reconstruction at the stage boundary")
    require(fresh_role_replay, "Next role must execute its own role-required replay; prior verdict is not proof")

    same_principal = previous_executor == next_executor
    grant_ref = None
    if same_principal:
        scope = {
            "parent_task_id": task["parent_owner"],
            "responsibility_task_id": task["task_id"],
            "acceptance_epoch_id": task.get("acceptance_epoch_id"),
        }
        # parent_task_id is replaced below when native TASK supplies the explicit parent identity.
        if task.get("parent_task_id"):
            scope["parent_task_id"] = task["parent_task_id"]
        try:
            grant = require_grant(
                grants,
                principal=next_executor,
                capability="ROLE_EXECUTION",
                scope=scope,
                at=at,
            )
        except Exception as error:
            raise RoleTransitionError(str(error)) from error
        grant_ref = grant["grant_id"]

    return {
        "mode": "OWNER_AUTHORIZED_COLLAPSE" if same_principal else "DISTINCT_PRINCIPAL",
        "previous_stage": previous_stage,
        "next_stage": next_stage,
        "previous_executor": previous_executor,
        "next_executor": next_executor,
        "role_execution_grant_ref": grant_ref,
        "principal_independence": "DEGRADED" if same_principal else "DISTINCT",
        "oracle_independence_required": "PINNED_ORACLE_INDEPENDENT" if next_stage in REVIEW_ROLES else "AUTHOR_EVIDENCE_ALLOWED",
        "stage_identity_preserved": True,
        "fresh_reconstruction": True,
        "fresh_role_replay": True,
    }
