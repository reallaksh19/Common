#!/usr/bin/env python3
"""V3.5 embedded-Coder identity and completion guardrails.

This module deliberately does not import Local v1.1 runtime code. It validates the
boundary contract handed to Relay by Local; Local remains the authority for role
lifecycle, timers, acceptance adoption and merge.
"""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any

SCHEMA = "relay-v3.5-embedded-coder-context"
AUTHORITY = "NESTED_ENGINEERING_EXECUTION_ONLY"
RESULT_SCOPE = "CODER_ENGINEERING_EXECUTION"
PROHIBITED_LOCAL_AUTHORITIES = {
    "LOCAL_ROLE_TRANSITION",
    "LOCAL_TIMER_CONTROL",
    "LOCAL_MERGE",
    "ACCEPTANCE_POLICY_ADOPTION",
    "RISK_RELAXATION",
}
PRD_RE = re.compile(r"^PRD-[A-Za-z0-9._-]+$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
LOCAL_REF_RE = re.compile(
    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}:skills/Local_PR_Deliverty_v1[.]1$"
)
RELAY_REF_RE = re.compile(
    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}:skills/engineering-pr-delivery-v3[.]5$"
)


class EmbeddedCoderError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EmbeddedCoderError(message)


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def engineering_responsibility(local_responsibility_task_id: str) -> str:
    require(bool(PRD_RE.fullmatch(local_responsibility_task_id)), "Local responsibility must use PRD-* identity")
    return "ENG-" + local_responsibility_task_id + "-CODER"


def validate_context(context: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(context, dict), "Embedded Coder context must be an object")
    required = {
        "schema",
        "authority",
        "local_parent_task_id",
        "local_responsibility_task_id",
        "engineering_responsibility",
        "role",
        "local_protocol_ref",
        "local_protocol_digest",
        "relay_protocol_ref",
        "relay_protocol_digest",
        "acceptance_epoch_ref",
        "acceptance_profile_ref",
        "acceptance_profile_digest",
        "prohibited_local_authorities",
    }
    require(set(context) == required, "Embedded Coder context has unknown or missing fields")
    require(context["schema"] == SCHEMA, "Wrong V3.5 embedded Coder schema")
    require(context["authority"] == AUTHORITY, "V3.5 authority must remain nested engineering execution only")
    require(isinstance(context["local_parent_task_id"], str) and context["local_parent_task_id"], "Missing Local parent task identity")

    local_id = context["local_responsibility_task_id"]
    require(isinstance(local_id, str) and PRD_RE.fullmatch(local_id), "Local responsibility must use PRD-* identity")
    require(
        context["engineering_responsibility"] == engineering_responsibility(local_id),
        "Nested engineering responsibility must be ENG-<PRD>-CODER",
    )
    require(context["role"] == "CODER", "V3.5 embedded mode is Coder-only")
    require(bool(LOCAL_REF_RE.fullmatch(context["local_protocol_ref"])), "Local protocol ref must pin Local_PR_Deliverty_v1.1 at exact SHA")
    require(bool(RELAY_REF_RE.fullmatch(context["relay_protocol_ref"])), "Relay protocol ref must pin engineering-pr-delivery-v3.5 at exact SHA")
    for field in ["local_protocol_digest", "relay_protocol_digest", "acceptance_profile_digest"]:
        require(bool(DIGEST_RE.fullmatch(context[field])), field + " must be a canonical sha256 hex digest")
    require(isinstance(context["acceptance_epoch_ref"], str) and context["acceptance_epoch_ref"], "Missing Local acceptance epoch ref")
    require(isinstance(context["acceptance_profile_ref"], str) and context["acceptance_profile_ref"], "Missing Local acceptance profile ref")

    denied = context["prohibited_local_authorities"]
    require(isinstance(denied, list) and set(denied) == PROHIBITED_LOCAL_AUTHORITIES, "V3.5 must explicitly deny every Local control-plane authority")
    require(len(denied) == len(set(denied)), "Duplicate prohibited Local authority")
    return deepcopy(context)


def build_context(
    *,
    local_parent_task_id: str,
    local_responsibility_task_id: str,
    local_protocol_ref: str,
    local_protocol_digest: str,
    relay_protocol_ref: str,
    relay_protocol_digest: str,
    acceptance_epoch_ref: str,
    acceptance_profile_ref: str,
    acceptance_profile_digest: str,
) -> dict[str, Any]:
    context = {
        "schema": SCHEMA,
        "authority": AUTHORITY,
        "local_parent_task_id": local_parent_task_id,
        "local_responsibility_task_id": local_responsibility_task_id,
        "engineering_responsibility": engineering_responsibility(local_responsibility_task_id),
        "role": "CODER",
        "local_protocol_ref": local_protocol_ref,
        "local_protocol_digest": local_protocol_digest,
        "relay_protocol_ref": relay_protocol_ref,
        "relay_protocol_digest": relay_protocol_digest,
        "acceptance_epoch_ref": acceptance_epoch_ref,
        "acceptance_profile_ref": acceptance_profile_ref,
        "acceptance_profile_digest": acceptance_profile_digest,
        "prohibited_local_authorities": sorted(PROHIBITED_LOCAL_AUTHORITIES),
    }
    return validate_context(context)


def build_task_result(
    context: dict[str, Any],
    *,
    engineering_responsibility_complete: bool,
    coverage: str,
    evidence_refs: list[str],
) -> dict[str, Any]:
    context = validate_context(context)
    require(isinstance(coverage, str) and coverage.strip(), "Coder engineering result requires coverage")
    require(isinstance(evidence_refs, list) and all(isinstance(ref, str) and ref for ref in evidence_refs), "Invalid evidence refs")
    require(len(evidence_refs) == len(set(evidence_refs)), "Duplicate evidence ref")
    result = {
        "result_scope": RESULT_SCOPE,
        "engineering_responsibility": context["engineering_responsibility"],
        "engineering_responsibility_complete": bool(engineering_responsibility_complete),
        "local_responsibility_task_id": context["local_responsibility_task_id"],
        "local_responsibility_complete": False,
        "coverage": coverage.strip(),
        "evidence_refs": list(evidence_refs),
        "acceptance_epoch_ref": context["acceptance_epoch_ref"],
        "acceptance_profile_ref": context["acceptance_profile_ref"],
        "acceptance_profile_digest": context["acceptance_profile_digest"],
    }
    result["digest"] = canonical_digest(result)
    return result


def validate_task_result(context: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    context = validate_context(context)
    required = {
        "result_scope",
        "engineering_responsibility",
        "engineering_responsibility_complete",
        "local_responsibility_task_id",
        "local_responsibility_complete",
        "coverage",
        "evidence_refs",
        "acceptance_epoch_ref",
        "acceptance_profile_ref",
        "acceptance_profile_digest",
        "digest",
    }
    require(set(result) == required, "V3.5 TASK_RESULT has unknown or missing fields")
    require(result["result_scope"] == RESULT_SCOPE, "V3.5 TASK_RESULT scope must be Coder engineering execution")
    require(result["engineering_responsibility"] == context["engineering_responsibility"], "TASK_RESULT nested responsibility mismatch")
    require(result["local_responsibility_task_id"] == context["local_responsibility_task_id"], "TASK_RESULT Local responsibility mismatch")
    require(result["local_responsibility_complete"] is False, "V3.5 can never declare the Local responsibility complete")
    require(result["acceptance_epoch_ref"] == context["acceptance_epoch_ref"], "TASK_RESULT acceptance epoch drift")
    require(result["acceptance_profile_ref"] == context["acceptance_profile_ref"], "TASK_RESULT acceptance profile drift")
    require(result["acceptance_profile_digest"] == context["acceptance_profile_digest"], "TASK_RESULT acceptance profile digest drift")
    require(result["digest"] == canonical_digest({k: v for k, v in result.items() if k != "digest"}), "TASK_RESULT digest mismatch")
    return deepcopy(result)


def reject_local_authority_claim(claim: str) -> None:
    require(claim not in PROHIBITED_LOCAL_AUTHORITIES, "V3.5 cannot exercise Local control-plane authority: " + claim)
