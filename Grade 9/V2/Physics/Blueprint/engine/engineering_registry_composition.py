#!/usr/bin/env python3
"""Compose the canonical Physics Engineering gate graph from governed sources.

The large generated v1 registry remains the base artifact. Canonical extensions
are discovered from a digest-bound catalog, not from topic-specific Python
constants. Each extension must bind to the exact base blob and expected gate
counts. The composed object retains the canonical registry ID and is what runtime
Engineering/Blueprint consumers validate and digest.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_REGISTRY_REL = "policies/physics-technical-engineering-gates.v1.json"
EXTENSION_CATALOG_REL = "policies/physics-engineering-extension-catalog.v1.json"


class EngineeringRegistryCompositionError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def _path(rel_or_path: str | Path) -> Path:
    p = Path(rel_or_path)
    return p if p.is_absolute() else ROOT / p


def _load_raw(rel_or_path: str | Path) -> dict:
    return json.loads(_path(rel_or_path).read_text(encoding="utf-8"))


def git_blob_sha(path: str | Path) -> str:
    data = _path(path).read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def file_sha256(path: str | Path) -> str:
    return "sha256:" + hashlib.sha256(_path(path).read_bytes()).hexdigest()


def _validate_catalog_shape(catalog: dict) -> None:
    required = {
        "schema_version",
        "subject",
        "catalog_id",
        "base_registry_ref",
        "base_registry_git_blob_sha",
        "extensions",
    }
    missing = sorted(required - set(catalog))
    if missing:
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_EXTENSION_CATALOG_SCHEMA",
            f"missing={missing}",
        )
    if catalog["schema_version"] != "1.0.0" or catalog["subject"] != "PHYSICS":
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_EXTENSION_CATALOG_SCHEMA",
            "invalid schema_version or subject",
        )
    if catalog["base_registry_ref"] != BASE_REGISTRY_REL:
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_EXTENSION_CATALOG_BASE_REF_DRIFT",
            str(catalog["base_registry_ref"]),
        )
    entries = catalog["extensions"]
    if not isinstance(entries, list):
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_EXTENSION_CATALOG_SCHEMA",
            "extensions must be a list",
        )
    refs = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"extension_ref", "extension_git_blob_sha"}:
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_CATALOG_SCHEMA",
                f"invalid extension entry: {entry!r}",
            )
        ref = entry["extension_ref"]
        blob = entry["extension_git_blob_sha"]
        if not isinstance(ref, str) or not ref:
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_CATALOG_SCHEMA",
                "extension_ref must be a non-empty string",
            )
        if not isinstance(blob, str) or len(blob) != 40:
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_CATALOG_SCHEMA",
                f"invalid extension_git_blob_sha for {ref}",
            )
        refs.append(ref)
    if len(refs) != len(set(refs)):
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_EXTENSION_CATALOG_DUPLICATE_REF",
            str(refs),
        )


def load_extension_catalog() -> dict:
    catalog = _load_raw(EXTENSION_CATALOG_REL)
    _validate_catalog_shape(catalog)
    actual_base_blob = git_blob_sha(BASE_REGISTRY_REL)
    if catalog["base_registry_git_blob_sha"] != actual_base_blob:
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_EXTENSION_CATALOG_BASE_BLOB_STALE",
            f"expected={catalog['base_registry_git_blob_sha']}, actual={actual_base_blob}",
        )
    for entry in catalog["extensions"]:
        actual = git_blob_sha(entry["extension_ref"])
        if entry["extension_git_blob_sha"] != actual:
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_CATALOG_ENTRY_STALE",
                f"{entry['extension_ref']}: expected={entry['extension_git_blob_sha']}, actual={actual}",
            )
    return catalog


def canonical_extension_rels() -> list[str]:
    return [entry["extension_ref"] for entry in load_extension_catalog()["extensions"]]


# Compatibility surface for consumers that need the current ordered canonical
# extension set. The value is data-derived and contains no topic-specific path.
CANONICAL_EXTENSION_RELS = canonical_extension_rels()


def _validate_extension_shape(extension: dict, rel: str, base: dict) -> None:
    required = {
        "schema_version",
        "subject",
        "extension_id",
        "base_registry_id",
        "base_registry_git_blob_sha",
        "expected_base_gate_count",
        "expected_composed_gate_count",
        "subtopic_gates",
    }
    missing = sorted(required - set(extension))
    if missing:
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_EXTENSION_SCHEMA",
            f"{rel}: missing={missing}",
        )
    if extension["schema_version"] != "1.0.0" or extension["subject"] != "PHYSICS":
        raise EngineeringRegistryCompositionError("PHY_ENG_EXTENSION_SCHEMA", rel)
    if extension["base_registry_id"] != base.get("registry_id"):
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_EXTENSION_BASE_REGISTRY_ID_DRIFT",
            f"{rel}:{extension['base_registry_id']}!={base.get('registry_id')}",
        )
    if not isinstance(extension["subtopic_gates"], list) or not extension["subtopic_gates"]:
        raise EngineeringRegistryCompositionError("PHY_ENG_EXTENSION_EMPTY", rel)


def load_canonical_engineering_registry(
    base_registry: str | Path = BASE_REGISTRY_REL,
    extension_rels: list[str] | None = None,
) -> dict:
    base_path = _path(base_registry)
    base = _load_raw(base_path)

    canonical_base = _path(BASE_REGISTRY_REL).resolve()
    if base_path.resolve() != canonical_base and extension_rels:
        raise EngineeringRegistryCompositionError(
            "PHY_ENG_NONCANONICAL_BASE_WITH_EXTENSION",
            str(base_path),
        )

    if extension_rels is None:
        if base_path.resolve() != canonical_base:
            extensions: list[str] = []
        else:
            extensions = canonical_extension_rels()
    else:
        extensions = list(extension_rels)

    actual_base_blob = git_blob_sha(base_path)
    composed = copy.deepcopy(base)
    existing_ids = {row["subtopic_id"] for row in composed.get("subtopic_gates", [])}
    expected_count = len(existing_ids)

    for rel in extensions:
        extension = _load_raw(rel)
        _validate_extension_shape(extension, rel, base)
        if extension["base_registry_git_blob_sha"] != actual_base_blob:
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_BASE_BLOB_STALE",
                f"{rel}: expected={extension['base_registry_git_blob_sha']}, actual={actual_base_blob}",
            )
        if extension["expected_base_gate_count"] != expected_count:
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_BASE_GATE_COUNT_DRIFT",
                f"{rel}: expected={extension['expected_base_gate_count']}, actual={expected_count}",
            )

        extension_ids = [row["subtopic_id"] for row in extension["subtopic_gates"]]
        duplicates = sorted(set(extension_ids) & existing_ids)
        if duplicates:
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_DUPLICATE_GATE_ID",
                f"{rel}:{duplicates}",
            )
        if len(extension_ids) != len(set(extension_ids)):
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_DUPLICATE_GATE_ID",
                f"{rel}: duplicate inside extension",
            )

        composed["subtopic_gates"].extend(copy.deepcopy(extension["subtopic_gates"]))
        existing_ids.update(extension_ids)
        expected_count = len(existing_ids)
        if extension["expected_composed_gate_count"] != expected_count:
            raise EngineeringRegistryCompositionError(
                "PHY_ENG_EXTENSION_COMPOSED_GATE_COUNT_DRIFT",
                f"{rel}: expected={extension['expected_composed_gate_count']}, actual={expected_count}",
            )

    return composed


def canonical_source_custody() -> dict:
    catalog = load_extension_catalog()
    return {
        "base_registry_ref": BASE_REGISTRY_REL,
        "base_registry_git_blob_sha": git_blob_sha(BASE_REGISTRY_REL),
        "extension_catalog_ref": EXTENSION_CATALOG_REL,
        "extension_catalog_git_blob_sha": git_blob_sha(EXTENSION_CATALOG_REL),
        "extensions": [
            {
                "extension_ref": entry["extension_ref"],
                "extension_git_blob_sha": entry["extension_git_blob_sha"],
                "extension_file_sha256": file_sha256(entry["extension_ref"]),
            }
            for entry in catalog["extensions"]
        ],
    }
