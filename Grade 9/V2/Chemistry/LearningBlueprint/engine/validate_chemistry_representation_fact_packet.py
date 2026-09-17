#!/usr/bin/env python3
"""Topic-neutral scientific validation for governed Chemistry representation facts."""
from __future__ import annotations

from typing import Any


class ChemistryRepresentationFactPacketError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryRepresentationFactPacketError(code, message)


def _validate_electron_transfer_state_ledger(parameters: dict[str, Any], packet_id: str) -> None:
    rows = parameters.get("oxidation_states")
    if not isinstance(rows, list) or len(rows) < 2:
        fail("CHEM_REP_FACT_ELECTRON_STATES_REQUIRED", packet_id)
    total_lost = 0
    total_gained = 0
    for row in rows:
        if not isinstance(row, dict):
            fail("CHEM_REP_FACT_ELECTRON_STATE_INVALID", packet_id)
        before = row.get("before")
        after = row.get("after")
        count = row.get("electron_count")
        if not isinstance(before, int) or not isinstance(after, int) or not isinstance(count, int):
            fail("CHEM_REP_FACT_ELECTRON_STATE_INVALID", packet_id)
        delta = after - before
        magnitude = abs(delta)
        if magnitude < 1 or count < magnitude or count % magnitude != 0:
            fail("CHEM_REP_FACT_ELECTRON_COUNT_STATE_MISMATCH", packet_id)
        if not str(row.get("element", "")).strip():
            fail("CHEM_REP_FACT_ELECTRON_STATE_INVALID", packet_id)
        if not str(row.get("before_species", "")).strip() or not str(row.get("after_species", "")).strip():
            fail("CHEM_REP_FACT_ELECTRON_STATE_INVALID", packet_id)
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


def validate_fact_packet(packet: dict[str, Any]) -> None:
    if not isinstance(packet, dict):
        fail("CHEM_REP_FACT_PACKET_INVALID")
    packet_id = str(packet.get("fact_packet_id", "")).strip() or "unnamed"
    kind = packet.get("fact_kind")
    parameters = packet.get("parameters")
    if not isinstance(parameters, dict):
        fail("CHEM_REP_FACT_PARAMETERS_INVALID", packet_id)
    if kind == "ELECTRON_TRANSFER_STATE_LEDGER_V1":
        _validate_electron_transfer_state_ledger(parameters, packet_id)
        return
    fail("CHEM_REP_FACT_KIND_UNSUPPORTED", str(kind))


__all__ = ["ChemistryRepresentationFactPacketError", "validate_fact_packet"]
