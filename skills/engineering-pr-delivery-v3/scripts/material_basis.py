#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from v3lib import canonical_digest, load_yaml, validate_schema


def _git(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git command failed")
    return result.stdout.strip()


def _matches(path: str, pattern: str) -> bool:
    path = path.replace("\\", "/").lstrip("./")
    pattern = pattern.replace("\\", "/").lstrip("./")
    if fnmatch.fnmatchcase(path, pattern):
        return True
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return False


def sensitivity(ep: dict[str, Any]) -> tuple[list[str], list[str]]:
    scope = ep.get("scope") or {}
    dependencies = [
        str(item.get("path"))
        for item in ((ep.get("basis") or {}).get("semantic_dependencies") or [])
        if isinstance(item, dict) and str(item.get("path") or "").strip()
    ]
    patterns: list[str] = []
    for key in ("write", "read", "protect"):
        patterns.extend(str(item) for item in (scope.get(key) or []) if str(item).strip())
    patterns.extend(dependencies)

    # A path-shaped acceptance test/oracle is also material-sensitive. Complex
    # command dependencies should be declared explicitly in semantic_dependencies.
    for acceptance in ep.get("acceptance") or []:
        for requirement in (acceptance.get("evidence_requirements") or []) if isinstance(acceptance, dict) else []:
            if not isinstance(requirement, dict):
                continue
            for value in requirement.values():
                text = str(value or "").strip()
                if "/" in text and not any(ch.isspace() for ch in text):
                    patterns.append(text)

    return list(dict.fromkeys(patterns)), list(dict.fromkeys(dependencies))


def _changed_paths(root: Path, rev: str) -> list[str]:
    out = _git(root, "diff-tree", "--no-commit-id", "--name-only", "-r", "--root", rev)
    return [line.strip() for line in out.splitlines() if line.strip()]


def _material_head(root: Path, material_base: str, coordination_head: str, patterns: list[str]) -> str:
    if subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", material_base, coordination_head],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode:
        return material_base
    commits = _git(root, "rev-list", "--reverse", f"{material_base}..{coordination_head}")
    material_head = material_base
    for commit in [line.strip() for line in commits.splitlines() if line.strip()]:
        paths = _changed_paths(root, commit)
        if any(any(_matches(path, pattern) for pattern in patterns) for path in paths):
            material_head = commit
    return material_head


def _tree_records(root: Path, commit: str, patterns: list[str] | None = None) -> list[dict[str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(root), "ls-tree", "-r", "-z", commit],
        stderr=subprocess.STDOUT,
    )
    records = []
    for entry in raw.decode("utf-8", errors="strict").split("\0"):
        if not entry:
            continue
        meta, path = entry.split("\t", 1)
        mode, obj_type, obj_sha = meta.split(" ", 2)
        if obj_type != "blob":
            continue
        if patterns is not None and not any(_matches(path, pattern) for pattern in patterns):
            continue
        records.append({"path": path, "mode": mode, "blob": obj_sha})
    return sorted(records, key=lambda item: item["path"])


def _digest_records(records: list[dict[str, str]]) -> str:
    return canonical_digest(records)


def classify_drift(root: Path, material_base: str, base_ref: str | None, patterns: list[str]) -> dict[str, Any]:
    if not base_ref:
        return {
            "classification": "UNKNOWN",
            "from_base": material_base,
            "to_base": None,
            "changed_paths": [],
            "sensitive_matches": [],
            "reason": "current base ref was not supplied",
        }
    try:
        to_base = _git(root, "rev-parse", base_ref)
    except Exception as exc:
        return {
            "classification": "UNKNOWN",
            "from_base": material_base,
            "to_base": None,
            "changed_paths": [],
            "sensitive_matches": [],
            "reason": f"cannot resolve current base ref: {exc}",
        }
    ancestor = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", material_base, to_base],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0
    if not ancestor:
        return {
            "classification": "UNKNOWN",
            "from_base": material_base,
            "to_base": to_base,
            "changed_paths": [],
            "sensitive_matches": [],
            "reason": "EP material base is not an ancestor of current base ref",
        }
    try:
        out = _git(root, "diff", "--name-only", f"{material_base}..{to_base}")
        changed = sorted(set(line.strip() for line in out.splitlines() if line.strip()))
    except Exception as exc:
        return {
            "classification": "UNKNOWN",
            "from_base": material_base,
            "to_base": to_base,
            "changed_paths": [],
            "sensitive_matches": [],
            "reason": f"cannot inspect base delta: {exc}",
        }
    matches = sorted(
        path for path in changed if any(_matches(path, pattern) for pattern in patterns)
    )
    if matches:
        return {
            "classification": "RELEVANT",
            "from_base": material_base,
            "to_base": to_base,
            "changed_paths": changed,
            "sensitive_matches": matches,
            "reason": "base delta intersects EP material sensitivity",
        }
    return {
        "classification": "DISJOINT",
        "from_base": material_base,
        "to_base": to_base,
        "changed_paths": changed,
        "sensitive_matches": [],
        "reason": "base delta has no intersection with EP material sensitivity",
    }


def inspect(root: Path, ep: dict[str, Any], base_ref: str | None) -> dict[str, Any]:
    material_base = str((ep.get("basis") or {}).get("material_base") or "")
    patterns, dependency_patterns = sensitivity(ep)
    coordination_head = _git(root, "rev-parse", "HEAD")
    ancestry_valid = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", material_base, coordination_head],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0

    material_head = _material_head(root, material_base, coordination_head, patterns)
    tree_records = _tree_records(root, material_head)
    relevant_records = _tree_records(root, material_head, patterns)
    dependency_records = _tree_records(root, material_head, dependency_patterns)

    result = {
        "schema_version": "relay-v3-material-basis",
        "material_basis": {
            "base": material_base,
            "head": material_head,
            "tree_digest": _digest_records(tree_records),
            "relevant_paths_digest": _digest_records(relevant_records),
            "dependency_digest": _digest_records(dependency_records),
            "ancestry_valid": ancestry_valid,
        },
        "coordination_basis": {"head": coordination_head},
        "sensitivity": {
            "patterns": patterns,
            "dependency_patterns": dependency_patterns,
        },
        "drift": classify_drift(root, material_base, base_ref, patterns),
    }
    errors = validate_schema("material-basis-result", result, "MATERIAL_BASIS")
    if errors:
        raise RuntimeError("; ".join(errors))
    return result


def load_current_ep(root: Path) -> dict[str, Any]:
    state = load_yaml(root / "relay/STATE.yaml")
    ep_id = ((state.get("execution") or {}).get("ep"))
    if not ep_id:
        raise RuntimeError("current STATE has no active EP")
    return load_yaml(root / "relay/WORK" / f"{ep_id}.yaml")


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive V3 material/coordination basis and classify base drift mechanically.")
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--base-ref", required=True, help="Current base branch/ref to compare against EP material_base.")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    result = inspect(root, load_current_ep(root), args.base_ref)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["material_basis"]["ancestry_valid"] and result["drift"]["classification"] != "UNKNOWN" else 1)


if __name__ == "__main__":
    main()
