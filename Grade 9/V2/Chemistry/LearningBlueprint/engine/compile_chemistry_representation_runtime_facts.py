#!/usr/bin/env python3
"""Project upstream Chemistry scientific facts into representation runtime parameters.

Scientific fact content and fact-kind validation are owned by governed Engineering/
Blueprint scientific authority. This module only binds an already-validated fact packet
to the exact authorized representation/semantic instance and projects its parameters.
Adapters never supply scientific facts or primitive runtime parameters.
"""
from __future__ import annotations

import copy
from typing import Any

from compile_chemistry_scientific_fact_authority import (
    ChemistryScientificFactAuthorityError,
    compile_scientific_fact_authority,
    digest,
)


class ChemistryRepresentationRuntimeFactsError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryRepresentationRuntimeFactsError(code, message)


def compile_runtime_fact_authority(
    authorities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compatibility entrypoint returning a compiled upstream scientific authority.

    The historical function name is retained so representation compilation remains API
    stable, but the data source is no longer a C-H runtime-fact extension.
    """
    try:
        compiled = compile_scientific_fact_authority(authorities)
    except ChemistryScientificFactAuthorityError as exc:
        fail(exc.code, exc.message)
    return {
        **compiled,
        # Retained as a compatibility alias for bundle consumers while authority
        # ownership migrates. Values are upstream scientific-authority IDs.
        "extension_refs": list(compiled["authority_refs"]),
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
    meaningful_classes = {str(by_id[ref].get("object_class", "")) for ref in source_refs}
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
        _validate_engineering_source(packet, intent, obligation_packet)
    elif source_kind == "BLUEPRINT_CONTENT_AUTHORITY":
        _validate_blueprint_source(packet, authorities)
    else:
        fail("CHEM_REP_RUNTIME_FACT_SOURCE_AUTHORITY_KIND_UNSUPPORTED", str(source_kind))

    packet_id = packet["fact_packet_id"]
    lineage = authority.get("packet_authority", {}).get(packet_id)
    if not lineage:
        fail("CHEM_REP_RUNTIME_FACT_SCIENTIFIC_AUTHORITY_LINEAGE_MISSING", packet_id)
    return {
        "fact_packet_ref": packet_id,
        "fact_packet_digest": digest(packet),
        "fact_kind": packet["fact_kind"],
        "semantic_instance_ref": packet["semantic_instance_ref"],
        "scientific_fact_authority_ref": lineage["authority_ref"],
        "scientific_fact_authority_digest": lineage["authority_digest"],
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
