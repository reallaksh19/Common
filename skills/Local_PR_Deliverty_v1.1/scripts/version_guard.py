#!/usr/bin/env python3
"""No-silent-migration guards for Local v1.1 + nested Relay v3.5."""
from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

DIGEST = re.compile(r"^[0-9a-f]{64}$")
EXACT_REF = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}:(.+)$")
ACTIVE_LOCAL = "skills/Local_PR_Deliverty_v1.1"
ACTIVE_RELAY = "skills/engineering-pr-delivery-v3.5"
FORBIDDEN_ACTIVE_RELAY = {
    "skills/engineering-pr-delivery-v2",
    "skills/engineering-pr-delivery-v2.5",
    "skills/engineering-pr-delivery-v3",
    "skills/engineering-pr-delivery-v3.1",
    "skills/engineering-pr-delivery-v3.2",
}
LEGACY_CLASSES = {"HISTORICAL", "MIGRATION", "COMPATIBILITY"}


class VersionGuardError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VersionGuardError(message)


def parse_exact_ref(ref: str) -> str:
    match = EXACT_REF.fullmatch(str(ref or ""))
    require(bool(match), "Protocol ref must be exact owner/repo@<40-sha>:path")
    return match.group(1)


def revision_notice(*, pinned_ref: str, pinned_digest: str, observed_ref: str, observed_digest: str, discovered_version: str | None = None) -> dict[str, Any]:
    parse_exact_ref(pinned_ref)
    parse_exact_ref(observed_ref)
    require(bool(DIGEST.fullmatch(pinned_digest)), "Invalid pinned digest")
    require(bool(DIGEST.fullmatch(observed_digest)), "Invalid observed digest")
    ref_changed = observed_ref != pinned_ref
    digest_changed = observed_digest != pinned_digest
    change = "NONE"
    if discovered_version:
        change = "SUCCESSOR_AVAILABLE"
    elif ref_changed:
        change = "EXACT_REF_CHANGED"
    elif digest_changed:
        change = "SAME_VERSION_DIGEST_CHANGED"
    return {
        "change": change,
        "notify_owner": change != "NONE",
        "automatic_migration": False,
        "pinned_ref": pinned_ref,
        "pinned_digest": pinned_digest,
        "observed_ref": observed_ref,
        "observed_digest": observed_digest,
        "discovered_version": discovered_version,
        "effective_ref": pinned_ref,
        "effective_digest": pinned_digest,
    }


def classify_protocol_reference(*, ref: str, usage: str) -> dict[str, Any]:
    path = parse_exact_ref(ref)
    usage = str(usage or "").strip().upper()
    if path in FORBIDDEN_ACTIVE_RELAY:
        allowed = usage in LEGACY_CLASSES
        return {
            "path": path,
            "usage": usage,
            "allowed": allowed,
            "severity": "HISTORICAL_OK" if allowed else "ACTIVE_VERSION_CONFLICT",
        }
    if path in {ACTIVE_LOCAL, ACTIVE_RELAY}:
        return {"path": path, "usage": usage, "allowed": True, "severity": "ACTIVE_ALLOWED"}
    return {"path": path, "usage": usage, "allowed": False, "severity": "UNKNOWN_PROTOCOL_PATH"}


def scan_references(references: list[dict[str, str]]) -> dict[str, Any]:
    findings = []
    for item in references:
        result = classify_protocol_reference(ref=item["ref"], usage=item.get("usage", "ACTIVE"))
        if not result["allowed"]:
            findings.append({**deepcopy(item), **result})
    return {
        "result": "PASS" if not findings else "CONFLICT",
        "findings": findings,
    }


def effective_stack(*, local_ref: str, relay_ref: str, selector_refs: list[dict[str, str]]) -> dict[str, Any]:
    require(parse_exact_ref(local_ref) == ACTIVE_LOCAL, "Outer protocol must be Local v1.1")
    require(parse_exact_ref(relay_ref) == ACTIVE_RELAY, "Nested Coder protocol must be v3.5")
    scan = scan_references(selector_refs)
    return {
        "local_ref": local_ref,
        "nested_coder_ref": relay_ref,
        "legacy_scan": scan,
        "usable": scan["result"] == "PASS",
    }
