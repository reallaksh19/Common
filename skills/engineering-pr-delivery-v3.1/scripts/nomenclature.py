from __future__ import annotations

import re
from pathlib import Path
from typing import Any


# Durable Relay namespaces. PGM is one-per-governing-issue. WP is normally
# one-per-governing-issue but may use a serial when one provider issue
# intentionally governs multiple durable work-package identities. All remaining
# namespaces are repeatable and therefore require a serial.
SINGLETON_TYPES = {"PGM"}
OPTIONALLY_SERIALIZED_TYPES = {"WP"}
SERIALIZED_TYPES = {
    "EP",
    "LEASE",
    "CP",
    "AC",
    "KI",
    "PEND",
    "CTRL",
    "CONT",
    "CHANGE",
    "OFFLOAD",
    "LOCAL",
    "EVID",
    "HO",
    "REC",
    "ODR",
    "TX",
    "EVT",
}
DURABLE_TYPES = SINGLETON_TYPES | OPTIONALLY_SERIALIZED_TYPES | SERIALIZED_TYPES
NON_ISSUE_ROOTS = {"REPO", "INTERNAL"}

_CANONICAL = re.compile(
    r"^(?P<kind>[A-Z]+)\.(?P<root>[1-9][0-9]*|REPO|INTERNAL)"
    r"(?:\.(?P<serial>[1-9][0-9]*))?$"
)
_LEGACY = re.compile(r"^(?P<kind>[A-Z]+)-[A-Za-z0-9][A-Za-z0-9._-]*$")
_CANONICAL_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_.-])(?:"
    + "|".join(sorted(DURABLE_TYPES, key=len, reverse=True))
    + r")\.(?:[1-9][0-9]*|REPO|INTERNAL)(?:\.[1-9][0-9]*)?"
)


def _normalize_kind(kind: str) -> str:
    value = str(kind or "").upper()
    if value not in DURABLE_TYPES:
        raise ValueError(f"unsupported Relay identifier type: {value}")
    return value


def _normalize_root(root: int | str) -> tuple[str, int | None, str]:
    if isinstance(root, bool):
        raise ValueError("identifier root must be a positive issue number, REPO, or INTERNAL")
    if isinstance(root, int):
        if root < 1:
            raise ValueError("issue number must be positive")
        return str(root), root, "ISSUE"

    text = str(root or "").upper()
    if text in NON_ISSUE_ROOTS:
        return text, None, "REPOSITORY" if text == "REPO" else "INTERNAL"
    if re.fullmatch(r"[1-9][0-9]*", text):
        number = int(text)
        return text, number, "ISSUE"
    raise ValueError("identifier root must be a positive issue number, REPO, or INTERNAL")


def canonical_id(
    kind: str,
    root: int | str,
    serial: int | None = None,
) -> str:
    """Render one canonical durable Relay display identifier.

    Durable identity is rooted in governing scope, not hierarchy. PGM is
    singleton per issue; WP may be singleton or serialised; repeatable object
    namespaces require a positive serial.
    """

    kind = _normalize_kind(kind)
    root_text, issue_number, _scope_kind = _normalize_root(root)

    if kind == "PGM":
        if issue_number is None:
            raise ValueError("PGM identifiers must be rooted in a governing issue")
        if serial is not None:
            raise ValueError("PGM identifiers do not use a serial")
        return f"{kind}.{root_text}"

    if kind == "WP":
        if issue_number is None:
            raise ValueError("WP identifiers must be rooted in a governing issue")
        if serial is None:
            return f"{kind}.{root_text}"

    if serial is None:
        raise ValueError(f"{kind} identifiers require a serial")
    sequence = int(serial)
    if sequence < 1:
        raise ValueError("serial must be positive")
    return f"{kind}.{root_text}.{sequence}"


def parse_canonical_id(value: str) -> dict[str, Any] | None:
    match = _CANONICAL.fullmatch(str(value or ""))
    if not match:
        return None

    kind = match.group("kind")
    if kind not in DURABLE_TYPES:
        return None

    root = match.group("root")
    serial_text = match.group("serial")
    serial = int(serial_text) if serial_text is not None else None

    if kind == "PGM" and (root in NON_ISSUE_ROOTS or serial is not None):
        return None
    if kind == "WP" and root in NON_ISSUE_ROOTS:
        return None
    if kind in SERIALIZED_TYPES and serial is None:
        return None

    issue_number = int(root) if root not in NON_ISSUE_ROOTS else None
    scope_kind = (
        "ISSUE"
        if issue_number is not None
        else "REPOSITORY"
        if root == "REPO"
        else "INTERNAL"
    )
    return {
        "kind": kind,
        "root": root,
        "scope_kind": scope_kind,
        "issue_number": issue_number,
        "serial": serial,
    }


def parse_legacy_id(value: str) -> dict[str, str] | None:
    """Recognize historical hyphenated Relay IDs without pretending lineage.

    Legacy IDs remain readable, but their governing issue cannot be inferred
    from their string form. Migration code must use structured/provider lineage
    rather than guessing from a legacy suffix.
    """

    match = _LEGACY.fullmatch(str(value or ""))
    if not match or match.group("kind") not in DURABLE_TYPES:
        return None
    return {"kind": match.group("kind"), "value": str(value)}


def require_rooted_id(
    value: str,
    *,
    kind: str,
    root: int | str,
    label: str,
) -> str:
    kind = _normalize_kind(kind)
    root_text, _issue_number, _scope_kind = _normalize_root(root)
    parsed = parse_canonical_id(value)
    if parsed is None:
        suffix = "" if kind in SINGLETON_TYPES | OPTIONALLY_SERIALIZED_TYPES else ".<serial>"
        raise ValueError(
            f"{label} must use {kind}.{root_text}{suffix} nomenclature"
        )
    if parsed["kind"] != kind:
        raise ValueError(f"{label} must use {kind}.* namespace")
    if parsed["root"] != root_text:
        raise ValueError(
            f"{label} root {parsed.get('root')} does not match governing scope {root_text}"
        )
    return value


def require_issue_rooted_id(
    value: str,
    *,
    kind: str,
    issue_number: int,
    label: str,
) -> str:
    return require_rooted_id(
        value,
        kind=kind,
        root=issue_number,
        label=label,
    )


def issue_number_from_ep(ep: dict[str, Any] | None) -> int | None:
    parent = (ep or {}).get("parent_issue") or {}
    number = parent.get("number")
    return int(number) if number is not None else None


def canonical_ids_in_text(text: str) -> list[str]:
    found: set[str] = set()
    for match in _CANONICAL_TOKEN.finditer(str(text or "")):
        value = match.group(0)
        if parse_canonical_id(value) is not None:
            found.add(value)
    return sorted(found)


def canonical_ids_in_repository(repo_root: Path) -> list[str]:
    """Collect canonical IDs already consumed by durable Relay state/history."""
    relay = repo_root / "relay"
    if not relay.exists():
        return []
    found: set[str] = set()
    for path in relay.rglob("*"):
        if not path.is_file() or "GENERATED" in path.parts:
            continue
        if path.suffix.lower() not in {".yaml", ".yml", ".jsonl"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        found.update(canonical_ids_in_text(text))
        if parse_canonical_id(path.stem) is not None:
            found.add(path.stem)
    return sorted(found)


def allocate_next_id(repo_root: Path, *, kind: str, root: int | str) -> str:
    """Choose the next ID from durable state/history.

    The caller must create the object and append its creation event in one Relay
    transaction. Shared EVENTS.jsonl preconditions then make concurrent
    allocation conflicts fail closed; the loser retries from fresh state.
    """
    kind = _normalize_kind(kind)
    if kind in SINGLETON_TYPES:
        return canonical_id(kind, root)
    serial = next_serial(canonical_ids_in_repository(repo_root), kind=kind, root=root)
    return canonical_id(kind, root, serial)


def allocate_next_ids(
    repo_root: Path,
    *,
    kind: str,
    root: int | str,
    count: int,
) -> list[str]:
    if count < 1:
        raise ValueError("allocation count must be positive")
    kind = _normalize_kind(kind)
    if kind in SINGLETON_TYPES:
        if count != 1:
            raise ValueError(f"{kind} supports only one identifier per governing issue")
        return [canonical_id(kind, root)]
    start = next_serial(canonical_ids_in_repository(repo_root), kind=kind, root=root)
    return [canonical_id(kind, root, start + offset) for offset in range(count)]


def next_serial(
    existing_ids: list[str],
    *,
    kind: str,
    root: int | str | None = None,
    issue_number: int | None = None,
) -> int:
    """Return the next monotonic serial for one namespace + governing root.

    Gaps are allowed and never filled. Legacy IDs are intentionally ignored:
    they pre-date canonical issue-rooted serials and are not guessed into a
    sequence.
    """

    kind = _normalize_kind(kind)
    if kind in SINGLETON_TYPES:
        raise ValueError(f"{kind} does not use serial allocation")
    if root is None:
        if issue_number is None:
            raise ValueError("root or issue_number is required")
        root = issue_number
    root_text, _issue, _scope_kind = _normalize_root(root)

    maximum = 0
    for value in existing_ids:
        parsed = parse_canonical_id(value)
        if (
            parsed
            and parsed["kind"] == kind
            and parsed["root"] == root_text
            and parsed["serial"] is not None
        ):
            maximum = max(maximum, int(parsed["serial"]))
    return maximum + 1
