#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from coordlib import load_yaml, validate
from authority_resolver import validate_authority_resolution
from current_state import validate_current_state
from evidence_freshness import validate_evidence_freshness
from execution_kernel import semantic_errors as execution_state_semantic_errors
from production_readiness import semantic_errors as production_readiness_semantic_errors
from provider_mutation import semantic_errors as provider_mutation_semantic_errors
from review_basis import (
    review_context_semantic_errors,
    self_check_context_semantic_errors,
)


SCHEMAS = {
    "issue-contract",
    "work-order",
    "local-coordinator-return",
    "coordination-observation",
    "owner-coordination-report",
    "programme-record",
    "relay-handover",
    "production-readiness",
    "execution-state",
    "provider-mutation",
    "current-state",
    "authority-resolution",
    "evidence-freshness",
    "review-context",
    "self-check-context",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate engineering programme coordinator objects.")
    parser.add_argument("schema", choices=sorted(SCHEMAS))
    parser.add_argument("path")
    parser.add_argument("--execution-state")
    parser.add_argument("--local-bundle")
    parser.add_argument("--observed-at")
    parser.add_argument("--freshness-request")
    args = parser.parse_args()

    value = load_yaml(Path(args.path))
    if args.schema == "current-state":
        execution_state = (
            load_yaml(Path(args.execution_state))
            if args.execution_state
            else None
        )
        errors = validate_current_state(
            value,
            execution_state,
            Path(args.path).name,
        )
    elif args.schema == "authority-resolution":
        local_bundle = (
            load_yaml(Path(args.local_bundle))
            if args.local_bundle
            else None
        )
        errors = validate_authority_resolution(
            value,
            local_bundle,
            args.observed_at,
            Path(args.path).name,
        )
    elif args.schema == "evidence-freshness":
        freshness_request = (
            load_yaml(Path(args.freshness_request))
            if args.freshness_request
            else None
        )
        errors = validate_evidence_freshness(
            value,
            freshness_request,
            Path(args.path).name,
        )
    else:
        errors = validate(args.schema, value, Path(args.path).name)
    if not errors and args.schema == "production-readiness":
        errors.extend(
            f"{Path(args.path).name}: {error}"
            for error in production_readiness_semantic_errors(value)
        )
    if not errors and args.schema == "execution-state":
        errors.extend(
            f"{Path(args.path).name}: {error}"
            for error in execution_state_semantic_errors(value)
        )
    if not errors and args.schema == "provider-mutation":
        errors.extend(
            f"{Path(args.path).name}: {error}"
            for error in provider_mutation_semantic_errors(value)
        )
    if not errors and args.schema == "review-context":
        errors.extend(
            f"{Path(args.path).name}: {error}"
            for error in review_context_semantic_errors(value)
        )
    if not errors and args.schema == "self-check-context":
        errors.extend(
            f"{Path(args.path).name}: {error}"
            for error in self_check_context_semantic_errors(value)
        )
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(f"OK: {args.schema}: {args.path}")


if __name__ == "__main__":
    main()
