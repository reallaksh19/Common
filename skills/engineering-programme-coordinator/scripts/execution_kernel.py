#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from coordlib import load_yaml, validate as schema_validate


def _decision(action: str, reason_code: str, *basis_refs: str) -> dict[str, Any]:
    refs = [ref for ref in basis_refs if ref]
    if not refs:
        refs = [f"derived://{reason_code.lower()}"]
    return {
        "type": action,
        "reason_code": reason_code,
        "basis_refs": refs,
    }


def derive_next_action(state: dict[str, Any]) -> dict[str, Any]:
    lifecycle = state["lifecycle"]
    capability = state["capability"]
    repository = state["repository"]
    dependencies = state["dependencies"]
    verification = state["verification"]
    contradictions = state["contradictions"]

    if lifecycle["stage"] == "STOPPED":
        return _decision(
            "STOPPED",
            "LIFECYCLE_STOPPED",
            lifecycle.get("last_completed_checkpoint") or "state://lifecycle",
        )

    if contradictions:
        return _decision(
            "RECONCILE",
            "STATE_CONTRADICTION",
            *(f"contradiction://{index + 1}" for index, _ in enumerate(contradictions)),
        )

    blocked = dependencies["blocked"]
    if blocked:
        return _decision(
            "WAIT_DEPENDENCY",
            "BLOCKED_DEPENDENCY",
            *(f"dependency://{row['id']}" for row in blocked),
        )

    active_role = capability["active_role"]
    allowed = set(capability["allowed_actions"])
    if active_role == "NONE":
        return _decision(
            "RECONCILE",
            "ACTIVE_ROLE_MISSING",
            *(capability.get("capability_basis") or ["state://capability"]),
        )

    candidate_sha = repository["candidate_sha"]
    if candidate_sha is None:
        if "WRITE_CANDIDATE" in allowed:
            return _decision(
                "IMPLEMENT",
                "IMPLEMENTATION_REQUIRED",
                repository["target_sha"],
            )
        return _decision(
            "RECONCILE",
            "CAPABILITY_MISSING",
            "capability://WRITE_CANDIDATE",
        )

    evidence_state = verification["evidence_state"]
    evidence_candidate_sha = verification["evidence_candidate_sha"]
    if evidence_state != "CURRENT" or evidence_candidate_sha != candidate_sha:
        if "RUN_VERIFICATION" in allowed:
            return _decision(
                "VERIFY_CANDIDATE",
                "VERIFICATION_REQUIRED",
                candidate_sha,
                verification.get("expectation_manifest_ref") or "state://expectation-manifest",
            )
        return _decision(
            "RECONCILE",
            "CAPABILITY_MISSING",
            "capability://RUN_VERIFICATION",
        )

    unresolved = verification["unresolved_critical"]
    refuted = [row for row in unresolved if row["state"] == "REFUTED"]
    if refuted:
        if "REPAIR_CANDIDATE" in allowed:
            return _decision(
                "REPAIR_CANDIDATE",
                "REPAIR_REQUIRED",
                *(f"obligation://{row['id']}" for row in refuted),
            )
        return _decision(
            "RECONCILE",
            "CAPABILITY_MISSING",
            "capability://REPAIR_CANDIDATE",
        )

    unknown = [row for row in unresolved if row["state"] == "UNKNOWN"]
    if unknown:
        if "RUN_VERIFICATION" in allowed:
            return _decision(
                "VERIFY_CANDIDATE",
                "CRITICAL_UNKNOWN",
                *(f"obligation://{row['id']}" for row in unknown),
            )
        return _decision(
            "RECONCILE",
            "CAPABILITY_MISSING",
            "capability://RUN_VERIFICATION",
        )

    if "ADVANCE_STAGE" in allowed:
        return _decision(
            "ADVANCE_STAGE",
            "ADVANCEMENT_READY",
            verification.get("evidence_ledger_ref") or candidate_sha,
        )

    return _decision(
        "RECONCILE",
        "CAPABILITY_MISSING",
        "capability://ADVANCE_STAGE",
    )


def semantic_errors(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    capability = state["capability"]
    repository = state["repository"]
    verification = state["verification"]

    allowed = set(capability["allowed_actions"])
    forbidden = set(capability["forbidden_actions"])
    overlap = sorted(allowed & forbidden)
    if overlap:
        errors.append(
            "capability actions cannot be both allowed and forbidden: "
            + ", ".join(overlap)
        )

    if capability["active_role"] == "NONE" and allowed:
        errors.append("active_role NONE requires allowed_actions to be empty")

    candidate_sha = repository["candidate_sha"]
    evidence_state = verification["evidence_state"]
    evidence_sha = verification["evidence_candidate_sha"]
    ledger_ref = verification["evidence_ledger_ref"]
    unresolved = verification["unresolved_critical"]

    if candidate_sha is None:
        if evidence_state != "MISSING":
            errors.append("missing candidate requires evidence_state MISSING")
        if evidence_sha is not None:
            errors.append("missing candidate cannot have evidence_candidate_sha")
        if unresolved:
            errors.append("missing candidate cannot have unresolved critical obligations")

    if evidence_state == "CURRENT":
        if candidate_sha is None:
            errors.append("CURRENT evidence requires candidate_sha")
        if evidence_sha != candidate_sha:
            errors.append("CURRENT evidence must bind the exact candidate_sha")
        if not ledger_ref:
            errors.append("CURRENT evidence requires evidence_ledger_ref")

    if evidence_state == "MISSING":
        if evidence_sha is not None:
            errors.append("MISSING evidence cannot have evidence_candidate_sha")
        if ledger_ref is not None:
            errors.append("MISSING evidence cannot have evidence_ledger_ref")

    derived = derive_next_action(state)
    stored = state["next_action"]
    if stored["type"] != derived["type"]:
        errors.append(
            f"next_action.type {stored['type']} does not match derived {derived['type']}"
        )
    if stored["reason_code"] != derived["reason_code"]:
        errors.append(
            "next_action.reason_code "
            f"{stored['reason_code']} does not match derived {derived['reason_code']}"
        )

    return errors


def validate_execution_state(value: Any, label: str = "execution-state") -> list[str]:
    errors = schema_validate("execution-state", value, label)
    if errors:
        return errors
    if not isinstance(value, dict):
        return [f"{label}: execution state must be an object"]
    return [f"{label}: {error}" for error in semantic_errors(value)]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate EXECUTION_STATE_V1 and its deterministic next action."
    )
    parser.add_argument("path")
    args = parser.parse_args()

    path = Path(args.path)
    value = load_yaml(path)
    errors = validate_execution_state(value, path.name)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(f"OK: execution-state: {path}")


if __name__ == "__main__":
    main()
