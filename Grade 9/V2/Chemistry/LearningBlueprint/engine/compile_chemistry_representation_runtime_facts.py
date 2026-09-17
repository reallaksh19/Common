#!/usr/bin/env python3
"""Resolve governed Chemistry representation facts into primitive runtime parameters.

Engineering-owned scientific facts are compiled from Engineering authority. C-H runtime
extensions may add only Blueprint-local semantic instances. Adapters may nominate opaque
authority/instance refs, but they never supply scientific runtime parameters.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

from compile_chemistry_engineering_representation_facts import (
    ChemistryEngineeringRepresentationFactsError,
    compile_engineering_representation_facts,
)
from validate_chemistry_representation_fact_packet import (
    ChemistryRepresentationFactPacketError,
    validate_fact_packet,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_REL = "contracts/chemistry-representation-runtime-facts.schema.json"
DEFAULT_RUNTIME_FACT_EXTENSION_RELS = (
    "../Representation/registry/chemistry-electron-transfer-runtime-facts.v1.json",
)


class ChemistryRepresentationRuntimeFactsError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryRepresentationRuntimeFactsError(code, message)


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def _load(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).resolve().read_text(encoding="utf-8"))


def compile_runtime_fact_authority(
    extensions: list[dict[str, Any]] | None = None,
    *,
    engineering_fact_authority: dict[str, Any] | None = None,
    engineering_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        engineering = compile_engineering_representation_facts(
            engineering_fact_authority,
            registry=engineering_registry,
        )
    except ChemistryEngineeringRepresentationFactsError as exc:
        fail(exc.code, exc.message)

    rows = list(extensions) if extensions is not None else [_load(rel) for rel in DEFAULT_RUNTIME_FACT_EXTENSION_RELS]
    schema = _load(SCHEMA_REL)
    extension_refs: list[str] = []
    by_representation: dict[str, list[dict[str, Any]]] = {}
    packet_ids: set[str] = set()
    semantic_instance_refs: set[str] = set()

    def add_packet(packet: dict[str, Any]) -> None:
        packet_id = packet["fact_packet_id"]
        semantic_ref = packet["semantic_instance_ref"]
        rep_ref = packet["source_representation_ref"]
        if packet_id in packet_ids:
            fail("CHEM_REP_FACT_PACKET_DUPLICATE", packet_id)
        if semantic_ref in semantic_instance_refs:
            fail("CHEM_REP_FACT_SEMANTIC_INSTANCE_DUPLICATE", semantic_ref)
        try:
            validate_fact_packet(packet)
        except ChemistryRepresentationFactPacketError as exc:
            fail(exc.code, exc.message)
        packet_ids.add(packet_id)
        semantic_instance_refs.add(semantic_ref)
        by_representation.setdefault(rep_ref, []).append(copy.deepcopy(packet))

    for packet in engineering["fact_packets"]:
        if packet.get("source_authority_kind") != "ENGINEERING_OBLIGATION":
            fail("CHEM_REP_FACT_ENGINEERING_AUTHORITY_KIND_DRIFT", packet["fact_packet_id"])
        if packet.get("source_authority_ref") != engineering["authority_id"]:
            fail("CHEM_REP_FACT_ENGINEERING_AUTHORITY_REF_DRIFT", packet["fact_packet_id"])
        add_packet(packet)

    for extension in rows:
        try:
            jsonschema.validate(extension, schema)
        except jsonschema.ValidationError as exc:
            fail("CHEM_REP_FACT_EXTENSION_SCHEMA", exc.message)
        extension_id = extension["extension_id"]
        if extension_id in extension_refs:
            fail("CHEM_REP_FACT_EXTENSION_DUPLICATE", extension_id)
        extension_refs.append(extension_id)
        for packet in extension["fact_packets"]:
            if packet.get("source_authority_kind") != "BLUEPRINT_CONTENT_AUTHORITY":
                fail("CHEM_REP_FACT_ENGINEERING_AUTHORITY_MISPLACED", packet["fact_packet_id"])
            add_packet(packet)

    for rep_ref in by_representation:
        by_representation[rep_ref].sort(key=lambda row: row["semantic_instance_ref"])
    return {
        "engineering_authority_ref": engineering["authority_id"],
        "engineering_authority_digest": engineering["authority_digest"],
        "engineering_registry_digest": engineering["registry_digest"],
        "extension_refs": extension_refs,
        "fact_packets_by_representation": by_representation,
        "semantic_instance_refs": sorted(semantic_instance_refs),
    }


def _matching_representation_obligation(
    intent: dict[str, Any], obligation_packet: dict[str, Any], rep_ref: str
) -> dict[str, Any]:
    rows = [
        row for row in obligation_packet.get("obligations", [])
        if row.get("kind") == "REPRESENTATION"
        and row.get("gate_id") == intent.get("source_gate_id")
        and row.get("asset_ref") == rep_ref
    ]
    if len(rows) != 1:
        fail("CHEM_REP_RUNTIME_FACT_REPRESENTATION_UNAUTHORIZED", rep_ref)
    rep_payload = rows[0].get("payload") or {}
    if rep_payload.get("representation_type") != intent.get("representation_type"):
        fail("CHEM_REP_RUNTIME_FACT_REPRESENTATION_TYPE_DRIFT", rep_ref)
    return rows[0]


def _validate_engineering_source(
    packet: dict[str, Any], intent: dict[str, Any], obligation_packet: dict[str, Any]
) -> None:
    equation_rows = {
        str(row.get("asset_ref")): row
        for row in obligation_packet.get("obligations", [])
        if row.get("kind") == "EQUATION" and row.get("gate_id") == intent.get("source_gate_id")
    }
    source_equations = packet.get("source_equation_refs") or []
    missing = sorted(set(source_equations) - set(equation_rows))
    if missing:
        fail("CHEM_REP_RUNTIME_FACT_EQUATION_UNAUTHORIZED", ",".join(missing))
    entities = (packet.get("parameters") or {}).get("chemical_entities")
    if entities is not None:
        governed_formulas = {
            str((equation_rows[ref].get("payload") or {}).get("formula", "")).strip()
            for ref in source_equations
        }
        governed_formulas.discard("")
        if set(entities) != governed_formulas:
            fail("CHEM_REP_RUNTIME_FACT_CHEMICAL_ENTITY_DRIFT", packet["source_representation_ref"])


def _validate_blueprint_source(
    packet: dict[str, Any],
    semantic_instance_authorities: dict[str, dict[str, Any]],
) -> None:
    authority_ref = str(packet.get("source_authority_ref", "")).strip()
    authority = semantic_instance_authorities.get(authority_ref)
    if authority is None:
        fail("CHEM_REP_RUNTIME_FACT_BLUEPRINT_AUTHORITY_REQUIRED", authority_ref or "missing")
    if str(authority.get("authority_id", "")).strip() != authority_ref:
        fail("CHEM_REP_RUNTIME_FACT_BLUEPRINT_AUTHORITY_DRIFT", authority_ref)
    objects = authority.get("content_objects")
    if not isinstance(objects, list):
        fail("CHEM_REP_RUNTIME_FACT_BLUEPRINT_OBJECTS_REQUIRED", authority_ref)
    by_id = {
        str(row.get("object_id")): row
        for row in objects
        if isinstance(row, dict) and str(row.get("object_id", "")).strip()
    }
    source_refs = [str(value) for value in packet.get("source_content_object_refs") or []]
    missing = sorted(set(source_refs) - set(by_id))
    if missing:
        fail("CHEM_REP_RUNTIME_FACT_BLUEPRINT_OBJECT_UNAUTHORIZED", ",".join(missing))
    meaningful_classes = {
        str(by_id[ref].get("object_class", "")) for ref in source_refs
    }
    if not meaningful_classes & {"EQUATION", "REPRESENTATION", "REASONING_CHAIN", "VERIFICATION", "WORKED_EXAMPLE"}:
        fail("CHEM_REP_RUNTIME_FACT_BLUEPRINT_SEMANTIC_SOURCE_WEAK", authority_ref)


def _select_fact_packet(
    candidates: list[dict[str, Any]],
    *,
    semantic_instance_authority_refs: list[str] | None,
    semantic_instance_refs: list[str] | None,
) -> dict[str, Any]:
    selected = list(candidates)
    if semantic_instance_refs is not None:
        requested = {str(value).strip() for value in semantic_instance_refs if str(value).strip()}
        selected = [row for row in selected if row.get("semantic_instance_ref") in requested]
    elif semantic_instance_authority_refs is not None:
        requested = {str(value).strip() for value in semantic_instance_authority_refs if str(value).strip()}
        selected = [
            row for row in selected
            if row.get("source_authority_kind") == "BLUEPRINT_CONTENT_AUTHORITY"
            and row.get("source_authority_ref") in requested
        ]
    else:
        selected = [row for row in selected if row.get("source_authority_kind") == "ENGINEERING_OBLIGATION"]
    if not selected:
        fail("CHEM_REP_RUNTIME_FACT_SEMANTIC_INSTANCE_UNRESOLVED")
    if len(selected) != 1:
        refs = ",".join(sorted(str(row.get("semantic_instance_ref")) for row in selected))
        fail("CHEM_REP_RUNTIME_FACT_SEMANTIC_INSTANCE_AMBIGUOUS", refs)
    return selected[0]


def resolve_runtime_fact_parameters(
    intent: dict[str, Any],
    obligation_packet: dict[str, Any],
    primitive: dict[str, Any],
    authority: dict[str, Any],
    *,
    semantic_instance_authorities: dict[str, dict[str, Any]] | None = None,
    semantic_instance_authority_refs: list[str] | None = None,
    semantic_instance_refs: list[str] | None = None,
) -> dict[str, Any] | None:
    required_kind = primitive.get("runtime_fact_kind")
    if not required_kind:
        return None
    rep_ref = str(intent.get("source_representation_ref", "")).strip()
    _matching_representation_obligation(intent, obligation_packet, rep_ref)
    candidates = [
        row for row in authority["fact_packets_by_representation"].get(rep_ref, [])
        if row.get("fact_kind") == required_kind
    ]
    if not candidates:
        fail("CHEM_REP_RUNTIME_FACTS_REQUIRED", f"{rep_ref}:{required_kind}")
    packet = _select_fact_packet(
        candidates,
        semantic_instance_authority_refs=semantic_instance_authority_refs,
        semantic_instance_refs=semantic_instance_refs,
    )
    if packet["source_gate_id"] != intent.get("source_gate_id"):
        fail("CHEM_REP_RUNTIME_FACT_GATE_MISMATCH", rep_ref)

    source_kind = packet["source_authority_kind"]
    authorities = semantic_instance_authorities or {}
    if source_kind == "ENGINEERING_OBLIGATION":
        if packet.get("source_authority_ref") != authority.get("engineering_authority_ref"):
            fail("CHEM_REP_RUNTIME_FACT_ENGINEERING_AUTHORITY_DRIFT", rep_ref)
        _validate_engineering_source(packet, intent, obligation_packet)
    elif source_kind == "BLUEPRINT_CONTENT_AUTHORITY":
        _validate_blueprint_source(packet, authorities)
    else:
        fail("CHEM_REP_RUNTIME_FACT_SOURCE_AUTHORITY_KIND_UNSUPPORTED", str(source_kind))

    return {
        "fact_packet_ref": packet["fact_packet_id"],
        "fact_packet_digest": digest(packet),
        "fact_kind": packet["fact_kind"],
        "semantic_instance_ref": packet["semantic_instance_ref"],
        "source_authority_kind": source_kind,
        "source_authority_ref": packet.get("source_authority_ref"),
        "source_equation_refs": list(packet.get("source_equation_refs") or []),
        "source_content_object_refs": list(packet.get("source_content_object_refs") or []),
        "parameters": copy.deepcopy(packet["parameters"]),
    }


__all__ = [
    "ChemistryRepresentationRuntimeFactsError",
    "compile_runtime_fact_authority",
    "resolve_runtime_fact_parameters",
]
