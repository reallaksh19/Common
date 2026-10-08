#!/usr/bin/env python3
"""Changed-file summary CLI for the Relay V3.2 recovery drill #486."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence


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
    """Return the normalized direct parent directory for one changed file path."""
    normalized = path.replace("\\", "/").strip("/")
    if "/" not in normalized:
        return "."
    return normalized.rsplit("/", 1)[0] or "."


def unique_directories(paths: Iterable[str]) -> list[str]:
    """Return sorted unique direct parent directories for changed file paths."""
    return sorted({_parent_directory(path) for path in paths})


def summarize(paths: Iterable[str]) -> dict[str, object]:
    """Build the deterministic changed-file summary."""
    path_list = list(paths)
    return {
        "total_file_count": len(path_list),
        "extensions": extension_counts(path_list),
        "directories": unique_directories(path_list),
    }


def _read_input(source: str) -> str:
    """Read JSON from stdin (`-`) or a UTF-8 file path."""
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarize a JSON array of changed file paths."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="JSON input file, or '-' / omitted to read stdin",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    args = _build_parser().parse_args(argv)
    try:
        raw_text = _read_input(args.input)
        paths = parse_changed_paths(raw_text)
    except (OSError, InputContractError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    json.dump(summarize(paths), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
