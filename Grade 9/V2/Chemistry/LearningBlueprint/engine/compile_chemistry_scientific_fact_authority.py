#!/usr/bin/env python3
"""Compile governed Chemistry scientific facts before representation realization.

This module owns scientific fact validation and authority lineage. Representation/C-H
code may request a supported fact kind and project a selected packet into runtime
parameters, but it does not author or infer the scientific facts.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_REL = "contracts/chemistry-scientific-fact-authority.schema.json"
DEFAULT_AUTHORITY_RELS = ("policies/chemistry-scientific-facts.v1.json",)


class ChemistryScientificFactAuthorityError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryScientificFactAuthorityError(code, message)


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def load(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).resolve().read_text(encoding="utf-8"))


def _validate_electron_transfer_state_ledger(parameters: dict[str, Any], packet_id: str) -> None:
    rows = parameters.get("oxidation_states")
    if not isinstance(rows, list) or len(rows) < 2:
        fail("CHEM_SCI_FACT_ELECTRON_STATES_REQUIRED", packet_id)
    total_lost = 0
    total_gained = 0
    for row in rows:
        before = row.get("before")
        after = row.get("after")
        count = row.get("electron_count")
        if not isinstance(before, int) or not isinstance(after, int) or not isinstance(count, int):
            fail("CHEM_SCI_FACT_ELECTRON_STATE_INVALID", packet_id)
        delta = after - before
        magnitude = abs(delta)
        if magnitude < 1 or count < magnitude or count % magnitude != 0:
            fail("CHEM_SCI_FACT_ELECTRON_COUNT_STATE_MISMATCH", packet_id)
        if delta > 0:
            total_lost += count
        else:
            total_gained += count
    if total_lost < 1 or total_gained < 1:
        fail("CHEM_SCI_FACT_ELECTRON_LOSS_AND_GAIN_REQUIRED", packet_id)
    if total_lost != total_gained:
        fail(
            "CHEM_SCI_FACT_ELECTRON_EXCHANGE_UNBALANCED",
            f"{packet_id}:lost={total_lost}:gained={total_gained}",
        )


def _validate_packet(packet: dict[str, Any]) -> None:
    kind = packet["fact_kind"]
    if kind == "ELECTRON_TRANSFER_STATE_LEDGER_V1":
        _validate_electron_transfer_state_ledger(packet["parameters"], packet["fact_packet_id"])
        return
    fail("CHEM_SCI_FACT_KIND_UNSUPPORTED", str(kind))


def compile_scientific_fact_authority(
    authorities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    rows = list(authorities) if authorities is not None else [load(rel) for rel in DEFAULT_AUTHORITY_RELS]
    schema = load(SCHEMA_REL)
    authority_refs: list[str] = []
    authority_digests: dict[str, str] = {}
    packet_authority: dict[str, dict[str, str]] = {}
    by_representation: dict[str, list[dict[str, Any]]] = {}
    packet_ids: set[str] = set()
    semantic_instance_refs: set[str] = set()

    for authority in rows:
        try:
            jsonschema.validate(authority, schema)
        except jsonschema.ValidationError as exc:
            fail("CHEM_SCI_FACT_AUTHORITY_SCHEMA", exc.message)
        authority_id = authority["authority_id"]
        if authority_id in authority_refs:
            fail("CHEM_SCI_FACT_AUTHORITY_DUPLICATE", authority_id)
        authority_refs.append(authority_id)
        authority_digest = digest(authority)
        authority_digests[authority_id] = authority_digest
        for packet in authority["fact_packets"]:
            packet_id = packet["fact_packet_id"]
            semantic_ref = packet["semantic_instance_ref"]
            rep_ref = packet["source_representation_ref"]
            if packet_id in packet_ids:
                fail("CHEM_SCI_FACT_PACKET_DUPLICATE", packet_id)
            if semantic_ref in semantic_instance_refs:
                fail("CHEM_SCI_FACT_SEMANTIC_INSTANCE_DUPLICATE", semantic_ref)
            _validate_packet(packet)
            packet_ids.add(packet_id)
            semantic_instance_refs.add(semantic_ref)
            packet_authority[packet_id] = {
                "authority_ref": authority_id,
                "authority_digest": authority_digest,
            }
            by_representation.setdefault(rep_ref, []).append(copy.deepcopy(packet))

    for rep_ref in by_representation:
        by_representation[rep_ref].sort(key=lambda row: row["semantic_instance_ref"])
    return {
        "authority_refs": authority_refs,
        "authority_digests": authority_digests,
        "packet_authority": packet_authority,
        "fact_packets_by_representation": by_representation,
        "semantic_instance_refs": sorted(semantic_instance_refs),
    }


__all__ = [
    "ChemistryScientificFactAuthorityError",
    "DEFAULT_AUTHORITY_RELS",
    "compile_scientific_fact_authority",
    "digest",
]
