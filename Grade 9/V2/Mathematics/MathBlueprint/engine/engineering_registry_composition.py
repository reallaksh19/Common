#!/usr/bin/env python3
"""Compose the canonical Mathematics Engineering gate graph from exact source files.

The large generated v1 registry remains the base artifact. Small, digest-bound
extensions may add new gates only when they explicitly bind to the exact base blob
and expected base gate count. The composed object retains the canonical registry ID
and is what runtime Engineering/Blueprint consumers validate and digest.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_REGISTRY_REL = "policies/mathematics-technical-engineering-gates.v1.json"
EUCLID_EXTENSION_REL = "policies/mathematics-technical-engineering-gates.v1.euclid-extension.json"
CANONICAL_EXTENSION_RELS = [EUCLID_EXTENSION_REL]


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


def _validate_extension_shape(extension: dict, rel: str, base: dict) -> None:
    required = {
        "schema_version", "subject", "extension_id", "base_registry_id",
        "base_registry_git_blob_sha", "expected_base_gate_count",
        "expected_composed_gate_count", "subtopic_gates",
    }
    missing = sorted(required - set(extension))
    if missing:
        raise EngineeringRegistryCompositionError(
            "MATH_ENG_EXTENSION_SCHEMA",
            f"{rel}: missing={missing}",
        )
    if extension["schema_version"] != "1.0.0" or extension["subject"] != "MATHEMATICS":
        raise EngineeringRegistryCompositionError("MATH_ENG_EXTENSION_SCHEMA", rel)
    if extension["base_registry_id"] != base.get("registry_id"):
        raise EngineeringRegistryCompositionError(
            "MATH_ENG_EXTENSION_BASE_REGISTRY_ID_DRIFT",
            f"{rel}:{extension['base_registry_id']}!={base.get('registry_id')}",
        )
    if not isinstance(extension["subtopic_gates"], list) or not extension["subtopic_gates"]:
        raise EngineeringRegistryCompositionError("MATH_ENG_EXTENSION_EMPTY", rel)


def load_canonical_engineering_registry(
    base_registry: str | Path = BASE_REGISTRY_REL,
    extension_rels: list[str] | None = None,
) -> dict:
    base_path = _path(base_registry)
    base = _load_raw(base_path)
    extensions = list(CANONICAL_EXTENSION_RELS if extension_rels is None else extension_rels)

    if Path(base_path).resolve() != _path(BASE_REGISTRY_REL).resolve():
        if extensions:
            raise EngineeringRegistryCompositionError(
                "MATH_ENG_NONCANONICAL_BASE_WITH_EXTENSION",
                str(base_path),
            )

    actual_base_blob = git_blob_sha(base_path)
    composed = copy.deepcopy(base)
    existing_ids = {row["subtopic_id"] for row in composed.get("subtopic_gates", [])}
    expected_count = len(existing_ids)

    for rel in extensions:
        extension = _load_raw(rel)
        _validate_extension_shape(extension, rel, base)
        if extension["base_registry_git_blob_sha"] != actual_base_blob:
            raise EngineeringRegistryCompositionError(
                "MATH_ENG_EXTENSION_BASE_BLOB_STALE",
                f"{rel}: expected={extension['base_registry_git_blob_sha']}, actual={actual_base_blob}",
            )
        if extension["expected_base_gate_count"] != expected_count:
            raise EngineeringRegistryCompositionError(
                "MATH_ENG_EXTENSION_BASE_GATE_COUNT_DRIFT",
                f"{rel}: expected={extension['expected_base_gate_count']}, actual={expected_count}",
            )

        extension_ids = [row["subtopic_id"] for row in extension["subtopic_gates"]]
        duplicates = sorted(set(extension_ids) & existing_ids)
        if duplicates:
            raise EngineeringRegistryCompositionError(
                "MATH_ENG_EXTENSION_DUPLICATE_GATE_ID",
                f"{rel}:{duplicates}",
            )
        if len(extension_ids) != len(set(extension_ids)):
            raise EngineeringRegistryCompositionError(
                "MATH_ENG_EXTENSION_DUPLICATE_GATE_ID",
                f"{rel}: duplicate inside extension",
            )

        composed["subtopic_gates"].extend(copy.deepcopy(extension["subtopic_gates"]))
        existing_ids.update(extension_ids)
        expected_count = len(existing_ids)
        if extension["expected_composed_gate_count"] != expected_count:
            raise EngineeringRegistryCompositionError(
                "MATH_ENG_EXTENSION_COMPOSED_GATE_COUNT_DRIFT",
                f"{rel}: expected={extension['expected_composed_gate_count']}, actual={expected_count}",
            )

    return composed


def canonical_source_custody() -> dict:
    return {
        "base_registry_ref": BASE_REGISTRY_REL,
        "base_registry_git_blob_sha": git_blob_sha(BASE_REGISTRY_REL),
        "extensions": [
            {
                "extension_ref": rel,
                "extension_git_blob_sha": git_blob_sha(rel),
                "extension_file_sha256": file_sha256(rel),
            }
            for rel in CANONICAL_EXTENSION_RELS
        ],
    }
