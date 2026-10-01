#!/usr/bin/env python3
"""Test-only changed-file summary utility for Relay V3.2 recovery drill #486.

Commit-A scope established the parser and extension aggregation. This branch is
intentionally allowed to advance beyond that durable evidence checkpoint so a
later successor has a real material delta to reconstruct.
"""

from __future__ import annotations

import json
from collections import Counter
from typing import Iterable


class InputContractError(ValueError):
    """Raised when the changed-file JSON does not match the declared contract."""


def parse_changed_paths(raw_text: str) -> list[str]:
    """Parse a JSON array of non-empty file-path strings."""
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise InputContractError(f"invalid JSON: {exc.msg}") from exc

    if not isinstance(payload, list):
        raise InputContractError("input must be a JSON array")

    paths: list[str] = []
    for index, value in enumerate(payload):
        if not isinstance(value, str):
            raise InputContractError(f"item {index} must be a string path")
        path = value.strip()
        if not path:
            raise InputContractError(f"item {index} must not be empty")
        paths.append(path.replace("\\", "/"))
    return paths


def extension_counts(paths: Iterable[str]) -> dict[str, int]:
    """Return deterministic counts keyed by lowercase final file extension."""
    counts: Counter[str] = Counter()
    for path in paths:
        name = path.rsplit("/", 1)[-1]
        if "." in name and not name.startswith("."):
            extension = "." + name.rsplit(".", 1)[-1].lower()
        else:
            extension = "<no_extension>"
        counts[extension] += 1
    return dict(sorted(counts.items()))


def _parent_directory(path: str) -> str:
    """Return one normalized parent candidate for later directory aggregation."""
    normalized = path.replace("\\", "/").strip("/")
    if "/" not in normalized:
        return "."
    return normalized.rsplit("/", 1)[0] or "."


def summary_seed(paths: Iterable[str]) -> dict[str, object]:
    """Assemble the already-proved summary fields for later CLI composition."""
    path_list = list(paths)
    return {
        "total_file_count": len(path_list),
        "extensions": extension_counts(path_list),
    }
