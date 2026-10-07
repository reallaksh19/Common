#!/usr/bin/env python3
"""Frozen V3.2 tree guard with explicit, base-pinned Owner amendments.

Default posture is unchanged: any change under `skills/engineering-pr-delivery-v3.2/` fails.

A change passes only for exact repository paths listed by an `owner_authorized` amendment in
`skills/Local_PR_Deliverty_v1.1/integration/frozen-v32-amendments.yaml` **as it exists at the PR base**,
never at the PR head. A pull request therefore cannot authorise its own edits to the frozen tree: the
amendment manifest has to be merged first (an Owner-controlled governance change), and only then may a
later change touch the listed paths. Anything not listed — including deletions and renames — still fails.

An unreadable or malformed base manifest honours nothing (fail closed).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

FROZEN_PREFIX = "skills/engineering-pr-delivery-v3.2/"
MANIFEST_PATH = "skills/Local_PR_Deliverty_v1.1/integration/frozen-v32-amendments.yaml"
SCHEMA = "frozen-v32-amendments"


class AmendmentError(ValueError):
    """The amendment manifest is malformed; no amendment is honoured."""


def _clean_path(value: Any, where: str) -> str:
    text = str(value or "")
    pure = PurePosixPath(text)
    if (
        not text
        or text.startswith("/")
        or "\\" in text
        or ".." in pure.parts
        or any(ch in text for ch in "*?[]")
        or not text.startswith(FROZEN_PREFIX)
        or text == MANIFEST_PATH
    ):
        raise AmendmentError(f"{where}: must be an exact path under {FROZEN_PREFIX} (no globs, no traversal): {text!r}")
    return text


def allowed_paths(manifest: Any) -> set[str]:
    """Exact paths authorised by the manifest. Raises AmendmentError when it is malformed."""
    if manifest is None:
        return set()
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        raise AmendmentError(f"manifest must be a mapping with schema: {SCHEMA}")
    allowed: set[str] = set()
    seen: set[str] = set()
    for index, amendment in enumerate(manifest.get("amendments") or []):
        where = f"amendments[{index}]"
        if not isinstance(amendment, dict) or not str(amendment.get("id") or "").strip():
            raise AmendmentError(f"{where}.id: required")
        aid = str(amendment["id"])
        if aid in seen:
            raise AmendmentError(f"{where}.id: duplicate amendment {aid}")
        seen.add(aid)
        if amendment.get("owner_authorized") is not True:
            continue  # recorded but not honoured
        if not str(amendment.get("owner_basis") or "").strip():
            raise AmendmentError(f"{where}.owner_basis: an authorised amendment must cite its Owner basis")
        paths = amendment.get("allowed_paths")
        if not isinstance(paths, list) or not paths:
            raise AmendmentError(f"{where}.allowed_paths: required list of exact paths")
        allowed.update(_clean_path(p, f"{where}.allowed_paths") for p in paths)
    return allowed


def violations(changed_paths: list[str], allowed: set[str]) -> list[str]:
    return sorted(p for p in changed_paths if p.startswith(FROZEN_PREFIX) and p not in allowed)


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args], text=True, capture_output=True, encoding="utf-8", check=check
    )


def changed_frozen_paths(root: Path, base: str, head: str) -> list[str]:
    out = _git(root, "diff", "--name-only", "--no-renames", "-z", base, head, "--", FROZEN_PREFIX).stdout
    return [p for p in out.split("\0") if p]


def base_manifest(root: Path, base: str) -> Any:
    shown = _git(root, "show", f"{base}:{MANIFEST_PATH}", check=False)
    if shown.returncode:
        return None  # no manifest at base: nothing is amended
    import yaml  # type: ignore

    return yaml.safe_load(shown.stdout)


def check(root: Path, base: str, head: str = "HEAD") -> tuple[int, list[str]]:
    changed = changed_frozen_paths(root, base, head)
    if not changed:
        return 0, []
    try:
        allowed = allowed_paths(base_manifest(root, base))
    except AmendmentError as exc:
        return 1, [f"base amendment manifest rejected (fail closed): {exc}", *violations(changed, set())]
    bad = violations(changed, allowed)
    return (1 if bad else 0), bad


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail on changes to the frozen V3.2 tree that no base-pinned Owner amendment authorises.")
    parser.add_argument("--base", required=True, help="PR base / comparison commit (the manifest is read from here)")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    code, bad = check(args.repo_root, args.base, args.head)
    if code:
        print("Frozen V3.2 tree changed without a base-pinned Owner amendment:", file=sys.stderr)
        for item in bad:
            print(f"  - {item}", file=sys.stderr)
        print(
            f"Merge an owner_authorized amendment listing these exact paths in {MANIFEST_PATH} first; "
            "a pull request cannot authorise its own edits to the frozen tree.",
            file=sys.stderr,
        )
    else:
        print("frozen V3.2 tree: no unauthorised change")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
