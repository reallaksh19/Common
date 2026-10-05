"""Canonical Production Responsibility helpers for Local PR Delivery v1.1.

Native responsibilities use TASK.task_id as the durable engineering identity. Legacy
CHILD tasks remain historical records; this module exposes a deterministic read view
without rewriting their stored identity.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any


class ResponsibilityError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ResponsibilityError(message)


def responsibility_view(task: dict[str, Any]) -> dict[str, Any]:
    """Return a normalized read view without mutating the persisted TASK."""
    kind = task["kind"]
    if kind == "RESPONSIBILITY":
        representation = deepcopy(task["representation"])
        return {
            "identity": task["task_id"],
            "identity_mode": "NATIVE_TASK_ID",
            "task_id": task["task_id"],
            "representation": representation,
            "active_pr": task.get("pr"),
            "acceptance_epoch_id": task["acceptance_epoch_id"],
            "acceptance_profile_ref": task["acceptance_profile_ref"],
            "acceptance_profile_digest": task["acceptance_profile_digest"],
        }
    if kind == "CHILD":
        return {
            "identity": task["task_id"],
            "identity_mode": "LEGACY_TASK_ID",
            "task_id": task["task_id"],
            "representation": {
                "kind": "SINGLE_ISSUE",
                "primary_issue": task["issue"],
                "member_issues": [task["issue"]],
                "predecessor_attempt_refs": [],
                "delivery_pr_history": [task["pr"]] if task.get("pr") else [],
            },
            "active_pr": task.get("pr"),
            "acceptance_epoch_id": None,
            "acceptance_profile_ref": None,
            "acceptance_profile_digest": None,
        }
    raise ResponsibilityError("Only RESPONSIBILITY/legacy CHILD tasks have a Production Responsibility view")


def validate_material_candidate(task: dict[str, Any]) -> None:
    view = responsibility_view(task)
    history = view["representation"]["delivery_pr_history"]
    active = view["active_pr"]
    if active is None:
        return
    require(active in history, "Active PR must appear in delivery_pr_history")
    require(history[-1] == active, "Active PR must be the latest sequential delivery PR")


def permission_targets_task(permission: dict[str, Any], task: dict[str, Any]) -> bool:
    """Native permissions target TASK identity; legacy permissions may target issue."""
    responsibility_target = permission.get("responsibility_task_id")
    if responsibility_target is not None:
        return responsibility_target == task["task_id"]
    child_issue = permission.get("child_issue")
    return task["kind"] == "CHILD" and child_issue == task["issue"]


def command_targets_task(command: dict[str, Any], task: dict[str, Any]) -> bool:
    responsibility_target = command.get("responsibility_task_id")
    if responsibility_target is not None:
        return responsibility_target == task["task_id"]
    child_issue = command.get("child_issue")
    return child_issue is None or child_issue == task["issue"]


def release_entry(parent_task: dict[str, Any], responsibility_task: dict[str, Any]) -> dict[str, Any] | None:
    control = parent_task.get("control_plane")
    if not control:
        return None
    matches = [
        entry
        for entry in control["responsibility_registry"]
        if entry["task_id"] == responsibility_task["task_id"]
    ]
    require(len(matches) <= 1, "Duplicate Parent control-plane responsibility registry entry")
    return matches[0] if matches else None


def validate_native_release(parent_task: dict[str, Any], responsibility_task: dict[str, Any]) -> None:
    require(responsibility_task["kind"] == "RESPONSIBILITY", "Native release applies only to RESPONSIBILITY tasks")
    control = parent_task.get("control_plane")
    require(control, "Native responsibility requires Parent TASK control_plane")
    require(control["bootstrap_state"] == "ESTABLISHED", "Parent bootstrap is not established")
    entry = release_entry(parent_task, responsibility_task)
    require(entry is not None, "Responsibility is absent from Parent control-plane registry")
    require(entry["acceptance_profile_ref"] == responsibility_task["acceptance_profile_ref"], "Parent registry Acceptance Profile ref differs from TASK")
    require(entry["acceptance_profile_digest"] == responsibility_task["acceptance_profile_digest"], "Parent registry Acceptance Profile digest differs from TASK")
    require(entry["release_state"] == "READY", f"Responsibility release is {entry['release_state']}")


def task_provider_issues(task: dict[str, Any]) -> list[int]:
    view = responsibility_view(task)
    return list(view["representation"]["member_issues"])
