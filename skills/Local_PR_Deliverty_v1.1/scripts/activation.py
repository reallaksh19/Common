#!/usr/bin/env python3
"""Deterministic Local v1.1 activation and pre-material-work handshake.

This module does not authenticate a human from text. Authentication/source truth is
supplied by the provider/session boundary. It resolves whether an authenticated
Owner instruction semantically activates the Local stack and then enforces the
required protocol/timer/evidence handshake before material work is authorized.
"""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

STACK_ID = "LOCAL_V1_1_V35"
LOCAL_PATH = "skills/Local_PR_Deliverty_v1.1"
V35_PATH = "skills/engineering-pr-delivery-v3.5"
VALID_ROLES = {"CODER", "REVIEWER", "COORDINATOR", "PARENT_CHECK"}
DEFAULT_BUDGETS = {"CODER": 15, "REVIEWER": 15, "COORDINATOR": 45, "PARENT_CHECK": 45}
TRUSTED_OWNER_SOURCES = {"DIRECT_OWNER_SESSION", "GITHUB_OWNER_INSTRUCTION", "OTHER_AUTHENTICATED_PROVIDER"}
DIRECT_CONTEXTS = {"DIRECT_INSTRUCTION", "OWNER_COMMAND"}
NEGATIVE_INTENTS = {"EXPLAIN", "REVIEW", "COMPARE", "AUDIT", "QUOTE", "FIXTURE", "DOCUMENTATION_EXAMPLE"}
ACTIVATION_VERBS = re.compile(r"\b(follow|use|apply|adhere(?:\s+to)?|execute|run|work\s+(?:under|as\s+per))\b", re.I)
LOCAL_REFERENCE = re.compile(
    r"(?:Local[_\s-]*PR[_\s-]*Deliverty[_\s-]*v?1[.]1|skills/Local_PR_Deliverty_v1[.]1|github\.com/[^\s]+/Common/(?:tree|blob)/[^\s]+/skills/Local_PR_Deliverty_v1[.]1)",
    re.I,
)
NEGATIVE_PREFIX = re.compile(r"^\s*(?:please\s+)?(?:explain|review|compare|audit|summarize|analyse|analyze)\b", re.I)
EXACT_REF = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}:.+$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")


class ActivationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ActivationError(message)


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_role(role: str) -> str:
    value = str(role or "").strip().upper().replace("SUPER_REVIEWER", "COORDINATOR")
    require(value in VALID_ROLES, "Unknown Local role")
    return value


def resolve_activation_trigger(
    text: str,
    *,
    source_kind: str,
    context_kind: str,
    intent: str = "EXECUTE",
    quoted: bool = False,
) -> dict[str, Any]:
    """Resolve activation only from authenticated direct Owner instruction semantics."""
    text = str(text or "").strip()
    intent = str(intent or "").strip().upper()
    source_kind = str(source_kind or "").strip().upper()
    context_kind = str(context_kind or "").strip().upper()

    trusted_source = source_kind in TRUSTED_OWNER_SOURCES
    direct_context = context_kind in DIRECT_CONTEXTS
    references_local = bool(LOCAL_REFERENCE.search(text))
    activation_verb = bool(ACTIVATION_VERBS.search(text))
    negative = quoted or intent in NEGATIVE_INTENTS or bool(NEGATIVE_PREFIX.search(text))
    activated = bool(text and trusted_source and direct_context and references_local and activation_verb and not negative)

    reason = "ACTIVATE_LOCAL_PR_DELIVERY_STACK" if activated else "NO_ACTIVATION"
    if negative:
        detail = "NEGATIVE_CONTROL"
    elif not trusted_source:
        detail = "UNTRUSTED_OR_NON_OWNER_SOURCE"
    elif not direct_context:
        detail = "NON_DIRECT_CONTEXT"
    elif not references_local:
        detail = "LOCAL_PROTOCOL_NOT_REFERENCED"
    elif not activation_verb:
        detail = "NO_EXECUTION_VERB"
    else:
        detail = "MATCH"
    return {
        "activated": activated,
        "normalized_event": reason,
        "detail": detail,
        "source_kind": source_kind,
        "context_kind": context_kind,
        "intent": intent,
        "quoted": bool(quoted),
        "instruction_digest": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def validate_exact_pin(pin: dict[str, Any], expected_path: str) -> dict[str, Any]:
    require(isinstance(pin, dict), "Protocol pin must be an object")
    require(set(pin) == {"ref", "digest"}, "Protocol pin has unknown/missing fields")
    require(bool(EXACT_REF.fullmatch(pin["ref"])), "Protocol pin must use owner/repo@<40-sha>:path")
    require(pin["ref"].endswith(":" + expected_path), "Protocol pin points at wrong protocol path")
    require(bool(DIGEST.fullmatch(pin["digest"])), "Protocol pin digest must be sha256 hex")
    return deepcopy(pin)


def arm_timer_accounting(role: str, *, budget_minutes: int | None = None, watchdog_available: bool = False, started_at: str | None = None) -> dict[str, Any]:
    role = normalize_role(role)
    budget = DEFAULT_BUDGETS[role] if budget_minutes is None else int(budget_minutes)
    require(budget > 0, "Timer budget must be positive")
    return {
        "accounting": "ARMED",
        "role": role,
        "budget_minutes": budget,
        "started_at": started_at or now_iso(),
        "watchdog": "ACTIVE" if watchdog_available else "NOT_AVAILABLE",
        "paused": False,
        "stopped_at": None,
    }


def publish_start_evidence(*, publication_ref: str, published_at: str, read_back: bool, evidence_digest: str) -> dict[str, Any]:
    require(isinstance(publication_ref, str) and publication_ref, "START evidence needs durable publication ref")
    require(isinstance(published_at, str) and published_at, "START evidence needs publication timestamp")
    require(bool(DIGEST.fullmatch(evidence_digest)), "START evidence digest must be sha256 hex")
    return {
        "publication_ref": publication_ref,
        "published_at": published_at,
        "read_back": bool(read_back),
        "evidence_digest": evidence_digest,
    }


def build_activation_record(
    *,
    trigger: dict[str, Any],
    owner_instruction_ref: str,
    local_pin: dict[str, Any],
    v35_pin: dict[str, Any] | None,
    role: str,
    responsibility_task_id: str,
    acceptance_epoch_ref: str,
    acceptance_profile_ref: str,
    acceptance_profile_digest: str,
    timer: dict[str, Any],
    start_evidence: dict[str, Any],
    legacy_scan: str,
) -> dict[str, Any]:
    require(trigger.get("activated") is True, "Activation trigger did not authorize production stack")
    require(isinstance(owner_instruction_ref, str) and owner_instruction_ref, "Activation needs Owner instruction reference")
    role = normalize_role(role)
    local_pin = validate_exact_pin(local_pin, LOCAL_PATH)
    if role == "CODER":
        require(v35_pin is not None, "Coder activation requires exact V3.5 nested protocol pin")
        v35_pin = validate_exact_pin(v35_pin, V35_PATH)
    else:
        require(v35_pin is None, "Non-Coder Local role must not activate V3.5 execution")
    require(str(responsibility_task_id).startswith("PRD-"), "Native activation requires PRD-* responsibility identity")
    require(acceptance_epoch_ref and acceptance_profile_ref, "Activation requires adopted acceptance epoch/profile")
    require(bool(DIGEST.fullmatch(acceptance_profile_digest)), "Acceptance profile digest is invalid")
    require(timer.get("accounting") == "ARMED" and timer.get("role") == role, "Role timer accounting must be armed before material work")
    require(start_evidence.get("read_back") is True, "TASK_EVIDENCE START must be durably published and read back")
    require(legacy_scan in {"PASS", "CONFLICT"}, "Legacy scan must report PASS or CONFLICT")

    record = {
        "schema": "local-pr-deliverty-activation/v1",
        "stack_id": STACK_ID,
        "trigger": deepcopy(trigger),
        "owner_instruction_ref": owner_instruction_ref,
        "responsibility_task_id": responsibility_task_id,
        "role": role,
        "local_protocol": local_pin,
        "nested_coder_protocol": v35_pin,
        "acceptance_epoch_ref": acceptance_epoch_ref,
        "acceptance_profile_ref": acceptance_profile_ref,
        "acceptance_profile_digest": acceptance_profile_digest,
        "timer": deepcopy(timer),
        "start_evidence": deepcopy(start_evidence),
        "legacy_scan": legacy_scan,
        "material_work_authorized": legacy_scan == "PASS",
    }
    record["stack_profile_digest"] = canonical_digest({
        "stack_id": STACK_ID,
        "local_protocol": local_pin,
        "nested_coder_protocol": v35_pin,
        "acceptance_epoch_ref": acceptance_epoch_ref,
        "acceptance_profile_ref": acceptance_profile_ref,
        "acceptance_profile_digest": acceptance_profile_digest,
    })
    record["activation_digest"] = canonical_digest(record)
    return record


def activation_acknowledgement(record: dict[str, Any]) -> str:
    require(record.get("schema") == "local-pr-deliverty-activation/v1", "Invalid activation record")
    nested = record["nested_coder_protocol"]["ref"] if record.get("nested_coder_protocol") else "NOT_APPLICABLE"
    timer = record["timer"]
    evidence = record["start_evidence"]
    return "\n".join([
        "PROTOCOL ACTIVE",
        "LOCAL: " + record["local_protocol"]["ref"],
        "NESTED_CODER: " + nested,
        "ROLE: " + record["role"],
        f"TIMER_ACCOUNTING: {timer['accounting']} — {timer['budget_minutes']} min",
        "WATCHDOG: " + timer["watchdog"],
        "START_EVIDENCE: " + evidence["publication_ref"],
        "ACCEPTANCE_PROFILE: " + record["acceptance_profile_ref"],
        "LEGACY_SCAN: " + record["legacy_scan"],
        "MATERIAL_WORK: " + ("AUTHORIZED" if record["material_work_authorized"] else "BLOCKED"),
    ])
