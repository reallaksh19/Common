#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from coordlib import load_yaml, validate as schema_validate


POSITIVE_EVIDENCE_STATES = {
    "VERIFIED",
    "REFUTED",
    "SHADOW_ONLY",
    "CONDITIONALLY_QUALIFIED",
}

SHADOW_REQUIRED = {
    "canonical_local_projection",
    "active_authority_resolution",
    "activation_state_derivation",
    "execution_kernel",
    "proof_obligation_runtime",
    "evidence_gate",
}

ADVISORY_REQUIRED = SHADOW_REQUIRED | {
    "reviewer_definition",
    "real_artifact_horizontal_integration",
}

CRITICAL_REQUIRED = ADVISORY_REQUIRED | {
    "role_succession_semantics",
    "acceptance_denominator_closure",
    "rollback",
}

DEFAULT_REQUIRED = CRITICAL_REQUIRED | {
    "shadow_rollout",
}


def semantic_errors(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    components = value.get("components") or {}
    mode = value.get("production_mode")

    for name, component in components.items():
        state = component.get("state")
        evidence_refs = component.get("evidence_refs") or []
        note = component.get("note")
        if state in POSITIVE_EVIDENCE_STATES and not evidence_refs:
            errors.append(
                f"components.{name}: state {state} requires at least one evidence_ref"
            )
        if state == "NOT_APPLICABLE" and not evidence_refs and not note:
            errors.append(
                f"components.{name}: NOT_APPLICABLE requires evidence_ref or explanatory note"
            )

    def require_states(names: set[str], allowed: set[str], label: str) -> None:
        for name in sorted(names):
            state = (components.get(name) or {}).get("state")
            if state not in allowed:
                errors.append(
                    f"production_mode {label} requires components.{name} in "
                    f"{sorted(allowed)}, got {state!r}"
                )

    if mode == "SHADOW":
        require_states(
            SHADOW_REQUIRED,
            {"VERIFIED", "SHADOW_ONLY", "CONDITIONALLY_QUALIFIED"},
            mode,
        )
    elif mode == "ADVISORY":
        require_states(
            ADVISORY_REQUIRED,
            {"VERIFIED", "SHADOW_ONLY", "CONDITIONALLY_QUALIFIED"},
            mode,
        )
    elif mode == "CRITICAL_GATE":
        require_states(CRITICAL_REQUIRED, {"VERIFIED"}, mode)
    elif mode == "DEFAULT_GATE":
        require_states(DEFAULT_REQUIRED, {"VERIFIED"}, mode)

    authorization = value.get("cutover_authorization") or {}
    authorized = authorization.get("authorized") is True
    if authorized:
        if not authorization.get("authority_ref"):
            errors.append(
                "cutover_authorization.authority_ref is required when authorized=true"
            )
        if not authorization.get("authorized_at"):
            errors.append(
                "cutover_authorization.authorized_at is required when authorized=true"
            )

    if mode in {"CRITICAL_GATE", "DEFAULT_GATE"} and not authorized:
        errors.append(
            f"production_mode {mode} requires explicit cutover_authorization"
        )

    blockers = value.get("cutover_blockers") or []
    open_hard = [
        blocker for blocker in blockers
        if blocker.get("state") == "OPEN" and blocker.get("severity") == "HARD"
    ]
    open_any = [blocker for blocker in blockers if blocker.get("state") == "OPEN"]

    if mode == "CRITICAL_GATE" and open_hard:
        ids = ", ".join(blocker.get("id", "<unknown>") for blocker in open_hard)
        errors.append(
            f"production_mode CRITICAL_GATE is forbidden with open HARD blockers: {ids}"
        )

    if mode == "DEFAULT_GATE" and open_any:
        ids = ", ".join(blocker.get("id", "<unknown>") for blocker in open_any)
        errors.append(
            f"production_mode DEFAULT_GATE is forbidden with open blockers: {ids}"
        )

    if mode == "DEFAULT_GATE":
        shadow_state = (components.get("shadow_rollout") or {}).get("state")
        if shadow_state != "VERIFIED":
            errors.append(
                "production_mode DEFAULT_GATE requires verified shadow_rollout"
            )

    return errors


def validate_readiness(value: Any, label: str = "production-readiness") -> list[str]:
    errors = schema_validate("production-readiness", value, label)
    if errors:
        return errors
    if not isinstance(value, dict):
        return [f"{label}: readiness value must be an object"]
    return [f"{label}: {error}" for error in semantic_errors(value)]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate PRODUCTION_READINESS_V1 state."
    )
    parser.add_argument("path")
    args = parser.parse_args()

    path = Path(args.path)
    value = load_yaml(path)
    errors = validate_readiness(value, path.name)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(f"OK: production-readiness: {path}")


if __name__ == "__main__":
    main()
