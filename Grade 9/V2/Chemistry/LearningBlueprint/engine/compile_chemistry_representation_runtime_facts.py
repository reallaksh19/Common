#!/usr/bin/env python3
"""Resolve source-bound Chemistry representation facts into primitive runtime parameters.

This bridge is intentionally asset-level. A representation type may be broad, but a
primitive that requires structured runtime facts may only realize an exact Engineering
representation asset for which governed facts exist. Product adapters never supply
scientific fact payloads to this compiler.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

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


def _validate_electron_transfer_state_ledger(parameters: dict[str, Any], packet_id: str) -> None:
    rows = parameters.get("oxidation_states")
    if not isinstance(rows, list) or len(rows) < 2:
        fail("CHEM_REP_FACT_ELECTRON_STATES_REQUIRED", packet_id)
    total_lost = 0
    total_gained = 0
    for row in rows:
        before = row.get("before")
        after = row.get("after")
        count = row.get("electron_count")
        if not isinstance(before, int) or not isinstance(after, int) or not isinstance(count, int):
            fail("CHEM_REP_FACT_ELECTRON_STATE_INVALID", packet_id)
        delta = after - before
        magnitude = abs(delta)
        if magnitude < 1 or count < magnitude or count % magnitude != 0:
            fail("CHEM_REP_FACT_ELECTRON_COUNT_STATE_MISMATCH", packet_id)
        if delta > 0:
            total_lost += count
        else:
            total_gained += count
    if total_lost < 1 or total_gained < 1:
        fail("CHEM_REP_FACT_ELECTRON_LOSS_AND_GAIN_REQUIRED", packet_id)
    if total_lost != total_gained:
        fail(
            "CHEM_REP_FACT_ELECTRON_EXCHANGE_UNBALANCED",
            f"{packet_id}:lost={total_lost}:gained={total_gained}",
        )


def _validate_fact_packet(packet: dict[str, Any]) -> None:
    kind = packet["fact_kind"]
    if kind == "ELECTRON_TRANSFER_STATE_LEDGER_V1":
        _validate_electron_transfer_state_ledger(packet["parameters"], packet["fact_packet_id"])
        return
    fail("CHEM_REP_FACT_KIND_UNSUPPORTED", str(kind))


def compile_runtime_fact_authority(
    extensions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    rows = list(extensions) if extensions is not None else [_load(rel) for rel in DEFAULT_RUNTIME_FACT_EXTENSION_RELS]
    schema = _load(SCHEMA_REL)
    extension_refs: list[str] = []
    by_representation: dict[str, dict[str, Any]] = {}
    packet_ids: set[str] = set()
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
            packet_id = packet["fact_packet_id"]
            rep_ref = packet["source_representation_ref"]
            if packet_id in packet_ids:
                fail("CHEM_REP_FACT_PACKET_DUPLICATE", packet_id)
            if rep_ref in by_representation:
                fail("CHEM_REP_FACT_REPRESENTATION_OVERRIDE_FORBIDDEN", rep_ref)
            _validate_fact_packet(packet)
            packet_ids.add(packet_id)
            by_representation[rep_ref] = copy.deepcopy(packet)
    return {
        "extension_refs": extension_refs,
        "fact_packets_by_representation": by_representation,
    }


def resolve_runtime_fact_parameters(
    intent: dict[str, Any],
    obligation_packet: dict[str, Any],
    primitive: dict[str, Any],
    authority: dict[str, Any],
) -> dict[str, Any] | None:
    required_kind = primitive.get("runtime_fact_kind")
    if not required_kind:
        return None
    rep_ref = str(intent.get("source_representation_ref", "")).strip()
    packet = authority["fact_packets_by_representation"].get(rep_ref)
    if packet is None:
        fail("CHEM_REP_RUNTIME_FACTS_REQUIRED", f"{rep_ref}:{required_kind}")
    if packet["fact_kind"] != required_kind:
        fail(
            "CHEM_REP_RUNTIME_FACT_KIND_MISMATCH",
            f"{rep_ref}:{packet['fact_kind']}!={required_kind}",
        )
    if packet["source_gate_id"] != intent.get("source_gate_id"):
        fail("CHEM_REP_RUNTIME_FACT_GATE_MISMATCH", rep_ref)

    matching_rep_obligations = [
        row for row in obligation_packet.get("obligations", [])
        if row.get("kind") == "REPRESENTATION"
        and row.get("gate_id") == intent.get("source_gate_id")
        and row.get("asset_ref") == rep_ref
    ]
    if len(matching_rep_obligations) != 1:
        fail("CHEM_REP_RUNTIME_FACT_REPRESENTATION_UNAUTHORIZED", rep_ref)
    rep_payload = matching_rep_obligations[0].get("payload") or {}
    if rep_payload.get("representation_type") != intent.get("representation_type"):
        fail("CHEM_REP_RUNTIME_FACT_REPRESENTATION_TYPE_DRIFT", rep_ref)

    equation_rows = {
        str(row.get("asset_ref")): row
        for row in obligation_packet.get("obligations", [])
        if row.get("kind") == "EQUATION" and row.get("gate_id") == intent.get("source_gate_id")
    }
    source_equations = packet["source_equation_refs"]
    missing = sorted(set(source_equations) - set(equation_rows))
    if missing:
        fail("CHEM_REP_RUNTIME_FACT_EQUATION_UNAUTHORIZED", ",".join(missing))

    parameters = copy.deepcopy(packet["parameters"])
    entities = parameters.get("chemical_entities")
    if entities is not None:
        governed_formulas = {
            str((equation_rows[ref].get("payload") or {}).get("formula", "")).strip()
            for ref in source_equations
        }
        governed_formulas.discard("")
        if set(entities) != governed_formulas:
            fail("CHEM_REP_RUNTIME_FACT_CHEMICAL_ENTITY_DRIFT", rep_ref)

    return {
        "fact_packet_ref": packet["fact_packet_id"],
        "fact_packet_digest": digest(packet),
        "fact_kind": packet["fact_kind"],
        "source_equation_refs": list(source_equations),
        "parameters": parameters,
    }


__all__ = [
    "ChemistryRepresentationRuntimeFactsError",
    "compile_runtime_fact_authority",
    "resolve_runtime_fact_parameters",
]
