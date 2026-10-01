#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


HERE = Path(__file__).resolve().parents[1]
SCHEMAS = HERE / "schemas"
_SAFE_ID_SUFFIX = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def require_identifier(value: str, prefix: str, label: str) -> str:
    text = str(value or "")
    legacy_prefix = str(prefix)
    canonical_prefix = legacy_prefix[:-1] + "." if legacy_prefix.endswith("-") else None
    if text.startswith(legacy_prefix):
        suffix = text[len(legacy_prefix):]
    elif canonical_prefix and text.startswith(canonical_prefix):
        suffix = text[len(canonical_prefix):]
    else:
        accepted = f"{legacy_prefix}* or {canonical_prefix}*" if canonical_prefix else f"{legacy_prefix}*"
        raise ValueError(f"{label} must use {accepted} namespace")
    if not _SAFE_ID_SUFFIX.fullmatch(suffix):
        raise ValueError(f"{label} contains unsafe characters")
    return text


def repo_path(root: Path, relative: str, label: str) -> Path:
    raw = Path(str(relative))
    if raw.is_absolute():
        raise ValueError(f"{label} must be repository-relative")
    root_resolved = root.resolve()
    candidate = (root_resolved / raw).resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root") from exc
    return candidate



def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def schema(name: str) -> dict[str, Any]:
    return load_yaml(SCHEMAS / f"{name}.schema.yaml")


def _native_v3_compat(value: Any, name: str) -> Any:
    """Return an in-memory V3->V3.1 compatibility view without rewriting repository truth."""
    if not isinstance(value, dict):
        return value
    version = str(value.get("schema_version") or "")
    if version == "relay-v3":
        compatible_version = "relay-v3.1"
    elif version.startswith("relay-v3-"):
        compatible_version = "relay-v3.1-" + version[len("relay-v3-"):]
    else:
        return value

    compatible = copy.deepcopy(value)
    compatible["schema_version"] = compatible_version
    if name == "protocol-selection" and compatible.get("selected_protocol") == "V3":
        compatible["selected_protocol"] = "V3_1"
    return compatible


def validate_schema(name: str, value: Any, label: str) -> list[str]:
    validator = Draft202012Validator(schema(name), format_checker=FormatChecker())
    candidate = _native_v3_compat(value, name)
    errors = []
    for error in sorted(validator.iter_errors(candidate), key=lambda item: list(item.path)):
        where = ".".join(str(part) for part in error.path)
        errors.append(f"{label}{'.' + where if where else ''}: {error.message}")
    return errors


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_events(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], []
    events = []
    errors = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{lineno}: invalid JSON: {exc.msg}")
            continue
        events.append(item)
        errors.extend(validate_schema("event", item, f"{path}:{lineno}"))
    return events, errors
