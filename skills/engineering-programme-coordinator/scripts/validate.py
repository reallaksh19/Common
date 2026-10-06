#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from coordlib import load_yaml, validate
from current_state import semantic_errors as current_state_semantic_errors
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
    "review-context",
    "self-check-context",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate engineering programme coordinator objects.")
    parser.add_argument("schema", choices=sorted(SCHEMAS))
    parser.add_argument("path")
    args = parser.parse_args()

    value = load_yaml(Path(args.path))
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
    if not errors and args.schema == "current-state":
        errors.extend(
            f"{Path(args.path).name}: {error}"
            for error in current_state_semantic_errors(value)
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
