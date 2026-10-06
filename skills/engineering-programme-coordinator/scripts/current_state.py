#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from coordlib import load_yaml, validate as schema_validate


def canonical_document_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def semantic_errors(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    candidate = value["candidate"]
    production = value["production"]
    merge = value["merge_authority"]
    next_action = value["next_action"]
    source_refs = set(value["source_refs"])

    if candidate["state"] == "NONE":
        if any(
            item is not None
            for item in (
                candidate["pr"],
                candidate["branch"],
                candidate["base_sha"],
                candidate["head_sha"],
            )
        ):
            errors.append("candidate NONE requires null pr/branch/base_sha/head_sha")
        if candidate["changed_files"]:
            errors.append("candidate NONE requires changed_files to be empty")
    else:
        if not candidate["branch"]:
            errors.append("candidate ACTIVE requires branch")
        if not candidate["base_sha"]:
            errors.append("candidate ACTIVE requires base_sha")
        if not candidate["head_sha"]:
            errors.append("candidate ACTIVE requires head_sha")

    for dependency in value["dependencies"]:
        observed = dependency["observed_state"]
        if observed in {"VERIFIED", "REFUTED"}:
            if not dependency["evidence_ref"] or not dependency["exact_result_ref"]:
                errors.append(
                    f"dependency {dependency['producer']} {observed} requires "
                    "evidence_ref and exact_result_ref"
                )

    if production["mode"] == "OFF":
        if production["authority_ref"] is not None:
            errors.append("production mode OFF cannot carry authority_ref")
    elif not production["authority_ref"]:
        errors.append("non-OFF production mode requires authority_ref")

    if merge["state"] == "NOT_GRANTED":
        if merge["authority_ref"] is not None:
            errors.append("merge authority NOT_GRANTED cannot carry authority_ref")
    elif not merge["authority_ref"]:
        errors.append("OWNER_GRANTED merge authority requires authority_ref")

    if next_action["type"] in set(value["forbidden_next_actions"]):
        errors.append("next_action.type cannot also appear in forbidden_next_actions")

    required_sources = {
        value["parent"]["parent_ref"],
        value["active"]["issue_ref"],
        next_action["execution_state_ref"],
    }
    missing_sources = sorted(required_sources - source_refs)
    if missing_sources:
        errors.append(
            "source_refs must include parent, active issue, and execution-state refs: "
            + ", ".join(missing_sources)
        )

    return errors


def execution_binding_errors(
    value: dict[str, Any],
    execution_state: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    if execution_state.get("schema_version") != "EXECUTION_STATE_V1":
        errors.append("bound execution state must be EXECUTION_STATE_V1")
        return errors

    expected_digest = canonical_document_digest(execution_state)
    next_action = value["next_action"]
    if next_action["execution_state_digest"] != expected_digest:
        errors.append("execution_state_digest does not match bound execution state")

    execution_next = execution_state.get("next_action")
    if not isinstance(execution_next, dict):
        errors.append("bound execution state is missing next_action")
        return errors

    mirrored = {
        "type": next_action["type"],
        "reason_code": next_action["reason_code"],
        "basis_refs": next_action["basis_refs"],
    }
    if mirrored != execution_next:
        errors.append(
            "CURRENT_STATE next_action must exactly mirror EXECUTION_STATE_V1 next_action"
        )

    candidate = value["candidate"]
    execution_repo = execution_state.get("repository") or {}
    if candidate["state"] == "ACTIVE":
        if candidate["head_sha"] != execution_repo.get("candidate_sha"):
            errors.append(
                "ACTIVE CURRENT_STATE candidate head_sha must equal execution-state candidate_sha"
            )
    elif execution_repo.get("candidate_sha") is not None:
        errors.append(
            "CURRENT_STATE candidate NONE conflicts with execution-state candidate_sha"
        )

    if value["active"]["prd_id"] != (
        (execution_state.get("identity") or {}).get("responsibility")
    ):
        errors.append(
            "CURRENT_STATE active.prd_id must equal execution-state responsibility"
        )

    return errors


def validate_current_state(
    value: Any,
    execution_state: Any | None = None,
    label: str = "current-state",
) -> list[str]:
    errors = schema_validate("current-state", value, label)
    if errors:
        return errors
    if not isinstance(value, dict):
        return [f"{label}: current state must be an object"]

    errors = [f"{label}: {error}" for error in semantic_errors(value)]

    if execution_state is not None:
        if not isinstance(execution_state, dict):
            errors.append(f"{label}: bound execution state must be an object")
        else:
            errors.extend(
                f"{label}: {error}"
                for error in execution_binding_errors(value, execution_state)
            )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate CURRENT_STATE_V1 and optional exact EXECUTION_STATE_V1 binding."
    )
    parser.add_argument("path")
    parser.add_argument("--execution-state")
    args = parser.parse_args()

    path = Path(args.path)
    value = load_yaml(path)
    execution_state = (
        load_yaml(Path(args.execution_state))
        if args.execution_state
        else None
    )
    errors = validate_current_state(value, execution_state, path.name)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(f"OK: current-state projection: {path}")


if __name__ == "__main__":
    main()
