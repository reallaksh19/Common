#!/usr/bin/env python3
"""Report the exact live Engineering Relay V3.1 basis of this Common checkout."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/engineering-pr-delivery-v3.1/SKILL.md"
TWO_PASS_SCHEMA = ROOT / "skills/two-pass-prompt-generator/schema.md"
REVISION_RE = re.compile(r"TPG-2P-[0-9A-Za-z._-]+")


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def resolve() -> dict[str, Any]:
    skill = SKILL.read_text(encoding="utf-8")
    if "CURRENT LIVE PROTOCOL" not in skill or "\nV3.1\n" not in skill:
        raise RuntimeError("Common checkout does not declare V3.1 as current live protocol")

    schema = TWO_PASS_SCHEMA.read_text(encoding="utf-8")
    match = REVISION_RE.search(schema)
    if not match:
        raise RuntimeError("cannot resolve live Two-Pass protocol revision")

    sha = _git("rev-parse", "HEAD")
    branch = _git("branch", "--show-current") or None
    return {
        "schema_version": "relay-v3.1-live-protocol-basis",
        "protocol": "V3.1",
        "common_repository": "reallaksh19/Common",
        "common_sha": sha,
        "common_branch": branch,
        "two_pass_revision": match.group(0),
        "skill_path": "skills/engineering-pr-delivery-v3.1/SKILL.md",
        "two_pass_schema_path": "skills/two-pass-prompt-generator/schema.md",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve the exact Common checkout used as live V3.1 protocol basis.")
    parser.add_argument("--expect-sha")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    basis = resolve()
    if args.expect_sha and basis["common_sha"] != args.expect_sha:
        print(
            f"REFRESH_REQUIRED expected={args.expect_sha} live={basis['common_sha']}"
        )
        raise SystemExit(2)

    if args.json:
        print(json.dumps(basis, sort_keys=True))
    else:
        for key, value in basis.items():
            print(f"{key}={value}")


if __name__ == "__main__":
    main()
