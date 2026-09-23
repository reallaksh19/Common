#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from protocol_cutover import validate_selection
from v25_migration import PROTOCOL_SELECTION
from v3lib import load_yaml


V25_SKILL = "skills/engineering-pr-delivery-v2.5/SKILL.md"
V31_SKILL = "skills/engineering-pr-delivery-v3.1/SKILL.md"
LEGACY_STATE = "agents/relay/REPO_STATE.yaml"
NATIVE_STATE = "relay/STATE.yaml"


def _result(
    *,
    authority_mode: str,
    selected_protocol: str | None,
    repository_protocol: str | None,
    status: str,
    source: str,
    warning: str,
) -> dict:
    return {
        "authority_mode": authority_mode,
        # Compatibility metadata only. Consumers deciding authority should use
        # authority_mode/status instead of version-string comparisons.
        "selected_protocol": selected_protocol,
        "repository_protocol": repository_protocol,
        "tool_protocol": "V3_1" if authority_mode == "NATIVE" else "V2_5" if authority_mode == "LEGACY" else None,
        "skill": V31_SKILL if authority_mode == "NATIVE" else V25_SKILL if authority_mode == "LEGACY" else None,
        "status": status,
        "source": source,
        "warning": warning,
    }


def resolve(root: Path) -> dict:
    """Resolve repository Relay authority deterministically.

    Authority identity is LEGACY vs NATIVE. V2.5/V3/V3.1 remain compatibility
    and tooling metadata, not programme state.

    Selectorless repositories are resolved from durable authority presence:
    exactly one authority tree -> that mode; both trees -> fail closed.
    """

    selection_path = root / PROTOCOL_SELECTION
    legacy_exists = (root / LEGACY_STATE).exists()
    native_exists = (root / NATIVE_STATE).exists()

    if not selection_path.exists():
        if legacy_exists and native_exists:
            return _result(
                authority_mode="AMBIGUOUS",
                selected_protocol=None,
                repository_protocol=None,
                status="INVALID",
                source="TREE_PRESENCE",
                warning=(
                    "No protocol selector exists and both LEGACY and NATIVE authority trees are present; "
                    "fail closed rather than guessing which tree is live."
                ),
            )
        if native_exists:
            return _result(
                authority_mode="NATIVE",
                selected_protocol="V3_1",
                repository_protocol="NATIVE_NO_SELECTOR",
                status="ACTIVE",
                source="NATIVE_TREE",
                warning=(
                    "Selectorless repository has native relay/STATE.yaml and no legacy REPO_STATE. "
                    "Use the compatible native core; no version migration is required merely to run current tooling."
                ),
            )
        if legacy_exists:
            return _result(
                authority_mode="LEGACY",
                selected_protocol="V2_5",
                repository_protocol="V2_5",
                status="LEGACY_DEFAULT",
                source="LEGACY_TREE",
                warning=(
                    "Selectorless repository has only legacy V2.5 authority; keep V2.5 live. "
                    "Native authority must not be inferred without a native tree or active selector."
                ),
            )
        return _result(
            authority_mode="LEGACY",
            selected_protocol="V2_5",
            repository_protocol="UNINITIALIZED",
            status="LEGACY_DEFAULT",
            source="NO_AUTHORITY_TREE",
            warning="No Relay authority tree or selector exists; retain legacy-default compatibility until Relay is initialized.",
        )

    errors = validate_selection(root)
    if errors:
        return _result(
            authority_mode="AMBIGUOUS",
            selected_protocol=None,
            repository_protocol=None,
            status="INVALID",
            source="SELECTOR",
            warning="Protocol selection is invalid: " + "; ".join(errors[:5]),
        )

    selection = load_yaml(selection_path)
    selected = str(selection.get("selected_protocol") or "")
    status = str(selection.get("status") or "")

    if selected in {"V3", "V3_1"} and status == "ACTIVE":
        return _result(
            authority_mode="NATIVE",
            selected_protocol="V3_1",
            repository_protocol=selected,
            status="ACTIVE",
            source="SELECTOR",
            warning=(
                "Repository authority is native. Current V3.1 tooling may operate on the compatible native core "
                "without rewriting accepted history or treating tooling version as programme state."
            ),
        )

    # Every non-active native selection and every V2.5 selection leaves legacy
    # authority live until an explicit successful cutover activates NATIVE.
    return _result(
        authority_mode="LEGACY",
        selected_protocol="V2_5",
        repository_protocol=selected or "V2_5",
        status=status or "PREPARED",
        source="SELECTOR",
        warning="Native Relay is not active; legacy authority remains live until explicit cutover.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve the repository's Engineering Relay authority mode.")
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    value = resolve(Path(args.repo_root).resolve())
    for key in (
        "authority_mode",
        "selected_protocol",
        "repository_protocol",
        "tool_protocol",
        "skill",
        "status",
        "source",
        "warning",
    ):
        print(f"{key}: {value.get(key)}")
    # Recorder-first V3.1 reports protocol-selection ambiguity as diagnostics.
    # It must not become an execution/CI permission gate.
    raise SystemExit(0)


if __name__ == "__main__":
    main()
