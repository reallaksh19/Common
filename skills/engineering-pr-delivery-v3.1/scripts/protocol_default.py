#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from protocol_cutover import validate_selection
from v25_migration import PROTOCOL_SELECTION
from v3lib import load_yaml


V25_SKILL = "skills/engineering-pr-delivery-v2.5/SKILL.md"
V31_SKILL = "skills/engineering-pr-delivery-v3.1/SKILL.md"


def resolve(root: Path) -> dict:
    selection_path = root / PROTOCOL_SELECTION
    if not selection_path.exists():
        return {
            "selected_protocol": "V2_5",
            "skill": V25_SKILL,
            "status": "LEGACY_DEFAULT",
            "warning": "No protocol selection exists; use V2.5 compatibility behavior. V3.1 must not be inferred.",
        }
    errors = validate_selection(root)
    if errors:
        return {
            "selected_protocol": None,
            "skill": None,
            "status": "INVALID",
            "warning": "Protocol selection is invalid: " + "; ".join(errors[:5]),
        }
    selection = load_yaml(selection_path)
    if selection.get("selected_protocol") == "V3_1" and selection.get("status") == "ACTIVE":
        return {
            "selected_protocol": "V3_1",
            "skill": V31_SKILL,
            "status": "ACTIVE",
            "warning": "V2.5 is read-only migration history; do not create new V2.5 relay authority.",
        }
    return {
        "selected_protocol": "V2_5",
        "skill": V25_SKILL,
        "status": "PREPARED",
        "warning": "V3.1 is staged but not activated. Continue using V2.5 authority until explicit cutover.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve the repository's selected Engineering Relay protocol.")
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    value = resolve(Path(args.repo_root).resolve())
    for key in ("selected_protocol", "skill", "status", "warning"):
        print(f"{key}: {value.get(key)}")
    raise SystemExit(0 if value["status"] != "INVALID" else 1)


if __name__ == "__main__":
    main()
