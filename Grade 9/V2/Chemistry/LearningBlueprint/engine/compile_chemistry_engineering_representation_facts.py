#!/usr/bin/env python3
"""Compile typed scientific representation facts owned by Chemistry Engineering authority.

This compiler binds structured scientific facts to exact Engineering gate,
representation, and equation assets. It is topic-neutral and does not select teaching
primitives, renderers, page intents, or learner-product behavior.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

from validate_chemistry_engineering_registry_runtime import (
    ChemistryEngineeringRegistryError,
    validate as validate_registry,
)
from validate_chemistry_representation_fact_packet import (
    ChemistryRepresentationFactPacketError,
    validate_fact_packet,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_REL = "contracts/chemistry-engineering-representation-facts.schema.json"
DEFAULT_AUTHORITY_REL = "policies/chemistry-engineering-representation-facts.v1.json"


class ChemistryEngineeringRepresentationFactsError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryEngineeringRepresentationFactsError(code, message)


def load(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def _validate_source_binding(
    packet: dict[str, Any],
    gate_map: dict[str, dict[str, Any]],
) -> None:
    gate_id = packet["source_gate_id"]
    gate = gate_map.get(gate_id)
    if gate is None:
        fail("CHEM_ENG_REP_FACT_GATE_MISSING", gate_id)

    rep_ref = packet["source_representation_ref"]
    representation_rows = [
        row for row in gate.get("representations", [])
        if row.get("representation_id") == rep_ref
    ]
    if len(representation_rows) != 1:
        fail("CHEM_ENG_REP_FACT_REPRESENTATION_UNAUTHORIZED", f"{gate_id}:{rep_ref}")

    equation_rows = {
        str(row.get("equation_id")): row
        for row in gate.get("mandatory_equations", [])
        if str(row.get("equation_id", "")).strip()
    }
    source_equations = list(packet.get("source_equation_refs") or [])
    missing = sorted(set(source_equations) - set(equation_rows))
    if missing:
        fail("CHEM_ENG_REP_FACT_EQUATION_UNAUTHORIZED", f"{gate_id}:{','.join(missing)}")

    entities = (packet.get("parameters") or {}).get("chemical_entities")
    if entities is not None:
        governed_formulas = {
            str(equation_rows[ref].get("formula", "")).strip()
            for ref in source_equations
        }
        governed_formulas.discard("")
        if set(entities) != governed_formulas:
            fail("CHEM_ENG_REP_FACT_CHEMICAL_ENTITY_DRIFT", rep_ref)


def compile_engineering_representation_facts(
    authority: dict[str, Any] | None = None,
    *,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source = copy.deepcopy(authority) if authority is not None else load(DEFAULT_AUTHORITY_REL)
    try:
        jsonschema.validate(source, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_ENG_REP_FACT_AUTHORITY_SCHEMA", exc.message)

    current_registry = copy.deepcopy(registry) if registry is not None else load(source["registry_ref"])
    try:
        validate_registry(current_registry)
    except ChemistryEngineeringRegistryError as exc:
        fail("CHEM_ENG_REP_FACT_REGISTRY_INVALID", f"{exc.code}:{exc.message}")
    if current_registry.get("registry_id") != source["registry_id"]:
        fail(
            "CHEM_ENG_REP_FACT_REGISTRY_ID_DRIFT",
            f"authority={source['registry_id']}:registry={current_registry.get('registry_id')}",
        )

    gate_map = {row["subtopic_id"]: row for row in current_registry["subtopic_gates"]}
    packet_ids: set[str] = set()
    semantic_instance_refs: set[str] = set()
    representation_fact_keys: set[tuple[str, str]] = set()
    compiled_packets: list[dict[str, Any]] = []

    for packet in source["fact_packets"]:
        packet_id = packet["fact_packet_id"]
        semantic_ref = packet["semantic_instance_ref"]
        if packet_id in packet_ids:
            fail("CHEM_ENG_REP_FACT_PACKET_DUPLICATE", packet_id)
        if semantic_ref in semantic_instance_refs:
            fail("CHEM_ENG_REP_FACT_SEMANTIC_INSTANCE_DUPLICATE", semantic_ref)
        key = (packet["source_representation_ref"], packet["fact_kind"])
        if key in representation_fact_keys:
            fail("CHEM_ENG_REP_FACT_REPRESENTATION_AMBIGUOUS", "|".join(key))
        _validate_source_binding(packet, gate_map)
        try:
            validate_fact_packet(packet)
        except ChemistryRepresentationFactPacketError as exc:
            fail(exc.code, exc.message)

        row = copy.deepcopy(packet)
        row["source_authority_kind"] = "ENGINEERING_OBLIGATION"
        row["source_authority_ref"] = source["authority_id"]
        compiled_packets.append(row)
        packet_ids.add(packet_id)
        semantic_instance_refs.add(semantic_ref)
        representation_fact_keys.add(key)

    registry_digest = digest(current_registry)
    authority_digest = digest({
        "authority": source,
        "registry_digest": registry_digest,
    })
    return {
        "authority_id": source["authority_id"],
        "authority_digest": authority_digest,
        "registry_ref": source["registry_ref"],
        "registry_id": source["registry_id"],
        "registry_digest": registry_digest,
        "fact_packets": compiled_packets,
        "semantic_instance_refs": sorted(semantic_instance_refs),
        "status": "ENGINEERING_REPRESENTATION_FACTS_READY",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority", default=DEFAULT_AUTHORITY_REL)
    parser.add_argument("--out")
    args = parser.parse_args()
    compiled = compile_engineering_representation_facts(load(args.authority))
    text = json.dumps(compiled, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()


__all__ = [
    "ChemistryEngineeringRepresentationFactsError",
    "compile_engineering_representation_facts",
]
