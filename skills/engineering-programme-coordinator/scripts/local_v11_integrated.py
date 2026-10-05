#!/usr/bin/env python3
"""Observation-only adapter for Local PR Delivery v1.1 + Relay V3.5.

The programme coordinator consumes authoritative Local/V3.5 records but does not
create engineering acceptance truth or exercise Local control-plane authority.
"""
from __future__ import annotations

import copy
import re
from typing import Any

MODE = "LOCAL_V1_1_INTEGRATED"
AUTHORITY = "OBSERVATION_ONLY"
LEGACY_V31 = "READABLE_COMPATIBILITY_ONLY"
NON_AUTHORITIES = {
    "ENGINEERING_PASS",
    "LOCAL_ROLE_TRANSITION",
    "PRODUCT_WRITE",
    "ACCEPTANCE_POLICY_WRITE",
    "RISK_RELAXATION",
    "MERGE",
}
PRD_RE = re.compile(r"^PRD-[A-Za-z0-9._-]+$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
LOCAL_REF_RE = re.compile(
    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}:skills/Local_PR_Deliverty_v1[.]1$"
)
V35_REF_RE = re.compile(
    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}:skills/engineering-pr-delivery-v3[.]5$"
)


class IntegratedModeError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IntegratedModeError(message)


def expected_nested_identity(task_id: str) -> str:
    require(bool(PRD_RE.fullmatch(task_id)), "Integrated responsibility must use PRD-* identity")
    return "ENG-" + task_id + "-CODER"


def observe_responsibility(local_task: dict[str, Any], v35_result: dict[str, Any] | None = None) -> dict[str, Any]:
    """Project Local truth and optional V3.5 Coder result into observation-only state."""
    task_id = local_task.get("task_id")
    require(local_task.get("kind") == "RESPONSIBILITY", "Integrated observation requires Local RESPONSIBILITY TASK")
    require(isinstance(task_id, str) and PRD_RE.fullmatch(task_id), "Integrated responsibility must use PRD-* identity")
    require(local_task.get("acceptance_epoch_ref"), "Local responsibility lacks acceptance epoch")
    require(local_task.get("acceptance_profile_ref"), "Local responsibility lacks acceptance profile")
    require(bool(DIGEST_RE.fullmatch(local_task.get("acceptance_profile_digest", ""))), "Local responsibility has invalid acceptance profile digest")

    nested = expected_nested_identity(task_id)
    coder_complete = False
    if v35_result is not None:
        require(v35_result.get("result_scope") == "CODER_ENGINEERING_EXECUTION", "Coordinator can consume only Coder-scoped V3.5 result")
        require(v35_result.get("engineering_responsibility") == nested, "V3.5 nested responsibility does not match Local responsibility")
        require(v35_result.get("local_responsibility_task_id") == task_id, "V3.5 result points at another Local responsibility")
        require(v35_result.get("local_responsibility_complete") is False, "V3.5 result illegally claims Local responsibility completion")
        require(v35_result.get("acceptance_epoch_ref") == local_task["acceptance_epoch_ref"], "V3.5 result acceptance epoch is stale")
        require(v35_result.get("acceptance_profile_ref") == local_task["acceptance_profile_ref"], "V3.5 result acceptance profile is stale")
        require(v35_result.get("acceptance_profile_digest") == local_task["acceptance_profile_digest"], "V3.5 result acceptance profile digest is stale")
        coder_complete = bool(v35_result.get("engineering_responsibility_complete"))

    return {
        "task_id": task_id,
        "release_state": local_task.get("release_state", "READY"),
        "acceptance_epoch_ref": local_task["acceptance_epoch_ref"],
        "acceptance_profile_ref": local_task["acceptance_profile_ref"],
        "acceptance_profile_digest": local_task["acceptance_profile_digest"],
        "nested_engineering_responsibility": nested,
        "coder_engineering_complete": coder_complete,
        "local_responsibility_complete": bool(local_task.get("responsibility_complete", False)),
    }


def build_integrated_context(
    *,
    parent_task_id: str,
    local_protocol_ref: str,
    local_protocol_digest: str,
    engineering_evidence_provider_ref: str,
    engineering_evidence_provider_digest: str,
    responsibility_observations: list[dict[str, Any]],
) -> dict[str, Any]:
    require(isinstance(parent_task_id, str) and parent_task_id, "Missing Local parent TASK identity")
    require(bool(LOCAL_REF_RE.fullmatch(local_protocol_ref)), "Integrated mode requires exact Local v1.1 protocol ref")
    require(bool(DIGEST_RE.fullmatch(local_protocol_digest)), "Invalid Local protocol digest")
    require(bool(V35_REF_RE.fullmatch(engineering_evidence_provider_ref)), "Integrated mode requires exact V3.5 evidence-provider ref")
    require(bool(DIGEST_RE.fullmatch(engineering_evidence_provider_digest)), "Invalid V3.5 provider digest")
    require(isinstance(responsibility_observations, list), "Responsibility observations must be an array")
    ids = [row.get("task_id") for row in responsibility_observations]
    require(len(ids) == len(set(ids)), "Duplicate responsibility observation")
    for row in responsibility_observations:
        require(row.get("nested_engineering_responsibility") == expected_nested_identity(row.get("task_id", "")), "Nested engineering identity mismatch")
        require(row.get("release_state") in {"READY", "BLOCKED_DEPENDENCY", "HELD", "COMPLETE"}, "Invalid Local release state")
        require(isinstance(row.get("coder_engineering_complete"), bool), "Missing Coder engineering completion observation")
        require(isinstance(row.get("local_responsibility_complete"), bool), "Missing Local responsibility completion observation")

    return {
        "mode": MODE,
        "authority": AUTHORITY,
        "parent_task_id": parent_task_id,
        "local_protocol_ref": local_protocol_ref,
        "local_protocol_digest": local_protocol_digest,
        "engineering_evidence_provider_ref": engineering_evidence_provider_ref,
        "engineering_evidence_provider_digest": engineering_evidence_provider_digest,
        "responsibilities": copy.deepcopy(responsibility_observations),
        "non_authorities": sorted(NON_AUTHORITIES),
        "legacy_v31_interpretation": LEGACY_V31,
    }


def assert_observation_only_action(action: str) -> None:
    require(action not in NON_AUTHORITIES, "Programme coordinator integrated mode cannot exercise authority: " + action)


def derive_programme_status(context: dict[str, Any]) -> dict[str, Any]:
    """Return a coordination status projection without inventing engineering PASS."""
    require(context.get("mode") == MODE and context.get("authority") == AUTHORITY, "Not a valid integrated coordinator context")
    require(set(context.get("non_authorities", [])) == NON_AUTHORITIES, "Integrated context weakened its non-authority boundary")
    rows = context.get("responsibilities", [])
    return {
        "mode": MODE,
        "observed_responsibilities": len(rows),
        "coder_engineering_complete": sum(bool(row["coder_engineering_complete"]) for row in rows),
        "local_responsibilities_complete": sum(bool(row["local_responsibility_complete"]) for row in rows),
        "blocked_or_held": [row["task_id"] for row in rows if row["release_state"] in {"BLOCKED_DEPENDENCY", "HELD"}],
        "engineering_acceptance_verdict": "NOT_AUTHORIZED",
        "merge_authority": "NOT_AUTHORIZED",
    }
