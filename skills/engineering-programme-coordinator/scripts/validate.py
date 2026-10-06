#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from coordlib import load_yaml, validate
from evidence_gate import review_context_semantic_errors
from execution_kernel import semantic_errors as execution_state_semantic_errors
from production_readiness import semantic_errors as production_readiness_semantic_errors
from proof_obligations import (
    ledger_semantic_errors,
    manifest_semantic_errors,
)
from shadow_rollout import (
    semantic_errors as shadow_observation_semantic_errors,
    validate_summary as validate_shadow_summary,
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
    "proof-obligation-manifest",
    "evidence-ledger",
    "review-context",
    "evidence-gate-result",
    "shadow-observation",
    "shadow-summary",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate engineering programme coordinator objects.")
    parser.add_argument("schema", choices=sorted(SCHEMAS))
    parser.add_argument("path")
    args = parser.parse_args()

    path = Path(args.path)
    value = load_yaml(path)
    errors = validate(args.schema, value, path.name)

    if not errors and args.schema == "production-readiness":
        errors.extend(
            f"{path.name}: {error}"
            for error in production_readiness_semantic_errors(value)
        )
    if not errors and args.schema == "execution-state":
        errors.extend(
            f"{path.name}: {error}"
            for error in execution_state_semantic_errors(value)
        )
    if not errors and args.schema == "proof-obligation-manifest":
        errors.extend(
            f"{path.name}: {error}"
            for error in manifest_semantic_errors(value)
        )
    if not errors and args.schema == "evidence-ledger":
        errors.extend(
            f"{path.name}: {error}"
            for error in ledger_semantic_errors(value)
        )
    if not errors and args.schema == "review-context":
        errors.extend(
            f"{path.name}: {error}"
            for error in review_context_semantic_errors(value)
        )
    if not errors and args.schema == "shadow-observation":
        errors.extend(
            f"{path.name}: {error}"
            for error in shadow_observation_semantic_errors(value)
        )
    if not errors and args.schema == "shadow-summary":
        errors.extend(validate_shadow_summary(value, path.name))

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(f"OK: {args.schema}: {args.path}")


if __name__ == "__main__":
    main()
