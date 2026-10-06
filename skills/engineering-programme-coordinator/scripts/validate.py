#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from coordlib import load_yaml, validate
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
