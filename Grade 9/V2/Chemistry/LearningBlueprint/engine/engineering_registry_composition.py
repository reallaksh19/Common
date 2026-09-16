#!/usr/bin/env python3
"""Canonical composition layer for Chemistry Engineering Gate registries."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_REGISTRY_REL = "policies/chemistry-technical-engineering-gates.v1.json"
EXTENSION_CATALOG_REL = "policies/chemistry-engineering-extension-catalog.v1.json"


class EngineeringRegistryCompositionError(Exception):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def _path(rel_or_path: str | Path) -> Path:
    p = Path(rel_or_path)
    return p if p.is_absolute() else ROOT / p


def _load_raw(rel_or_path: str | Path) -> dict:
    p = _path(rel_or_path)
    if not p.exists():
        raise EngineeringRegistryCompositionError("CHEM_ENG_EXTENSION_FILE_NOT_FOUND", str(p))
    return json.loads(p.read_text(encoding="utf-8"))


def git_blob_sha(rel_or_path: str | Path) -> str:
    path = _path(rel_or_path)
    proc = subprocess.run(
        ["git", "hash-object", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        return proc.stdout.strip()
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def file_sha256(rel_or_path: str | Path) -> str:
    return hashlib.sha256(_path(rel_or_path).read_bytes()).hexdigest()


def load_extension_catalog() -> dict:
    catalog = _load_raw(EXTENSION_CATALOG_REL)
    actual_base_blob = git_blob_sha(BASE_REGISTRY_REL)
    if catalog["base_registry_git_blob_sha"] != actual_base_blob:
        raise EngineeringRegistryCompositionError(
            "CHEM_ENG_EXTENSION_CATALOG_BASE_BLOB_STALE",
            f"expected={catalog['base_registry_git_blob_sha']}, actual={actual_base_blob}",
        )
    return catalog


def canonical_extension_rels() -> list[str]:
    return [entry["extension_ref"] for entry in load_extension_catalog()["extensions"]]


CANONICAL_EXTENSION_RELS = canonical_extension_rels()


def load_canonical_engineering_registry(
    base_registry: str | Path = BASE_REGISTRY_REL,
    extension_rels: list[str] | None = None,
) -> dict:
    base_path = _path(base_registry)
    base = _load_raw(base_path)
    return base


def canonical_source_custody() -> dict:
    catalog = load_extension_catalog()
    return {
        "base_registry_ref": BASE_REGISTRY_REL,
        "base_registry_git_blob_sha": git_blob_sha(BASE_REGISTRY_REL),
        "extension_catalog_ref": EXTENSION_CATALOG_REL,
        "extension_catalog_git_blob_sha": git_blob_sha(EXTENSION_CATALOG_REL),
        "extensions": [],
    }
