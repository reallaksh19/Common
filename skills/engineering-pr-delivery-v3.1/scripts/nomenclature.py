from __future__ import annotations

import re
from typing import Any


ISSUE_ROOTED_TYPES = {
    "EP",
    "KI",
    "PEND",
    "LOCAL",
    "OFFLOAD",
    "CP",
    "LEASE",
}

_CANONICAL = re.compile(
    r"^(?P<kind>EP|KI|PEND|LOCAL|OFFLOAD|CP|LEASE)\.(?P<issue>[1-9][0-9]*)\.(?P<serial>[1-9][0-9]*)$"
)


def canonical_id(kind: str, issue_number: int, serial: int) -> str:
    kind = str(kind or "").upper()
    if kind not in ISSUE_ROOTED_TYPES:
        raise ValueError(f"unsupported issue-rooted identifier type: {kind}")
    issue = int(issue_number)
    sequence = int(serial)
    if issue < 1 or sequence < 1:
        raise ValueError("issue number and serial must be positive")
    return f"{kind}.{issue}.{sequence}"


def parse_canonical_id(value: str) -> dict[str, Any] | None:
    match = _CANONICAL.fullmatch(str(value or ""))
    if not match:
        return None
    return {
        "kind": match.group("kind"),
        "issue_number": int(match.group("issue")),
        "serial": int(match.group("serial")),
    }


def require_issue_rooted_id(
    value: str,
    *,
    kind: str,
    issue_number: int,
    label: str,
) -> str:
    parsed = parse_canonical_id(value)
    if parsed is None:
        raise ValueError(
            f"{label} must use {kind}.{int(issue_number)}.<serial> nomenclature"
        )
    if parsed["kind"] != kind:
        raise ValueError(f"{label} must use {kind}.* namespace")
    if parsed["issue_number"] != int(issue_number):
        raise ValueError(
            f"{label} issue root {parsed['issue_number']} does not match "
            f"governing GitHub issue {int(issue_number)}"
        )
    return value


def issue_number_from_ep(ep: dict[str, Any] | None) -> int | None:
    parent = (ep or {}).get("parent_issue") or {}
    number = parent.get("number")
    return int(number) if number is not None else None


def next_serial(existing_ids: list[str], *, kind: str, issue_number: int) -> int:
    maximum = 0
    for value in existing_ids:
        parsed = parse_canonical_id(value)
        if (
            parsed
            and parsed["kind"] == kind
            and parsed["issue_number"] == int(issue_number)
        ):
            maximum = max(maximum, int(parsed["serial"]))
    return maximum + 1
