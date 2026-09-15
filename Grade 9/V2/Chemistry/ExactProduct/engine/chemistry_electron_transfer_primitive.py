#!/usr/bin/env python3
"""Topic-neutral C-H electron-transfer ledger runtime extension.

This module adds one semantic primitive to the existing Chemistry visual runtime without
selecting it. Selection remains upstream in the C-H registry/page-intent authority and
four-Core representation plan. The renderer only realizes explicit, source-authorized
before/after states and electron counts and fails closed when exchange is unbalanced.
"""
from __future__ import annotations

from typing import Any

PRIMITIVE_ID = "ELECTRON_TRANSFER_LEDGER"
MIN_LEARNER_FONT_PT = 9.0
_INSTALLED = False


def _state_text(value: int) -> str:
    return f"{value:+d}" if value else "0"


def electron_transfer_rows(params: dict[str, Any], conservation_error: type[Exception]) -> tuple[list[dict[str, Any]], int, int]:
    rows: list[dict[str, Any]] = []
    total_lost = 0
    total_gained = 0
    for entry in params.get("oxidation_states") or []:
        element = str(entry.get("element", "")).strip()
        before_species = str(entry.get("before_species", "")).strip()
        after_species = str(entry.get("after_species", "")).strip()
        before = entry.get("before")
        after = entry.get("after")
        count = entry.get("electron_count")
        if not element or not before_species or not after_species or before is None or after is None or count is None:
            raise ValueError("CHEM_ELECTRON_TRANSFER_EXPLICIT_STATE_AND_COUNT_REQUIRED")
        before_i, after_i, count_i = int(before), int(after), int(count)
        delta = after_i - before_i
        if delta == 0 or count_i < 1:
            raise ValueError("CHEM_ELECTRON_TRANSFER_STATE_CHANGE_REQUIRED")
        magnitude = abs(delta)
        if count_i < magnitude or count_i % magnitude != 0:
            raise ValueError("CHEM_ELECTRON_TRANSFER_COUNT_STATE_MISMATCH")
        direction = "LOSS" if delta > 0 else "GAIN"
        row = {
            "element": element,
            "before_species": before_species,
            "after_species": after_species,
            "before": before_i,
            "after": after_i,
            "electron_count": count_i,
            "direction": direction,
        }
        rows.append(row)
        if direction == "LOSS":
            total_lost += count_i
        else:
            total_gained += count_i
    if not rows or total_lost < 1 or total_gained < 1:
        raise ValueError("CHEM_ELECTRON_TRANSFER_LOSS_AND_GAIN_REQUIRED")
    if total_lost != total_gained:
        raise conservation_error(
            "[GATE-02 FAIL: ELECTRON_EXCHANGE] electrons lost %d != electrons gained %d"
            % (total_lost, total_gained)
        )
    return rows, total_lost, total_gained


def _renderer(VP, canvas, x: float, y: float, w: float, h: float, params: dict[str, Any]) -> None:
    # Compute and validate the entire ledger before the first draw operation.
    rows, total_lost, total_gained = electron_transfer_rows(params, VP.ConservationError)

    # The shared card helper uses an 8 pt optional title. This primitive is used
    # inside products governed by a 9 pt engineering floor, so draw only the
    # shared frame and supply a compliant semantic title ourselves.
    VP.panel(canvas, x, y, w, h, None)
    title = params.get("title") or "Electron-transfer ledger: loss, gain, balance"
    VP.label(canvas, x + 12, y + h - 18, title, size=10.0, color="teal", font=VP.BOLD, width=w - 24)
    VP.label(
        canvas,
        x + 12,
        y + h - 34,
        params.get("attention_target") or "Track state change, electron direction and exchange balance.",
        size=MIN_LEARNER_FONT_PT,
        color="muted",
        width=w - 24,
    )

    body_top = y + h - 48
    footer_h = 32.0
    available = max(72.0, body_top - (y + footer_h + 8))
    row_h = min(38.0, available / len(rows))
    for index, row in enumerate(rows):
        ry = body_top - (index + 1) * row_h
        accent = "amber" if row["direction"] == "LOSS" else "teal"
        fill = "amber_fill" if row["direction"] == "LOSS" else "teal_fill"
        VP.box(canvas, x + 12, ry + 2, w - 24, row_h - 4, fill=fill, stroke=accent, radius=4, width=0.9)
        left = "%s  %s" % (row["before_species"], _state_text(row["before"]))
        right = "%s  %s" % (row["after_species"], _state_text(row["after"]))
        baseline = ry + row_h / 2 - 3.2
        VP.label(canvas, x + 20, baseline, left, size=9.4, color="ink", font=VP.BOLD, width=120)
        VP.arrow(canvas, x + 150, ry + row_h / 2, x + 194, ry + row_h / 2, color=accent, width=1.2, head=4.6)
        VP.label(canvas, x + 202, baseline, right, size=9.4, color="ink", font=VP.BOLD, width=120)
        action = "%s %d e⁻" % ("LOSES" if row["direction"] == "LOSS" else "GAINS", row["electron_count"])
        VP.label(canvas, x + w - 20, baseline, action, size=9.2, color=accent, font=VP.BOLD, align="right", width=112)

    balance_y = y + 10
    VP.box(canvas, x + 12, balance_y, w - 24, 24, fill="green_fill", stroke="green", radius=4, width=1.0)
    VP.label(
        canvas,
        x + w / 2,
        balance_y + 7.5,
        "electron check: lost = gained = %d e⁻" % total_lost,
        size=9.2,
        color="green",
        font=VP.BOLD,
        align="center",
        width=w - 40,
    )
    if total_gained != total_lost:  # defensive; electron_transfer_rows already fails closed.
        raise VP.ConservationError("CHEM_ELECTRON_TRANSFER_BALANCE_DRIFT")


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    import chemistry_visual_primitives as VP

    def draw(canvas, x, y, w, h, params):
        return _renderer(VP, canvas, x, y, w, h, params)

    original_height = VP.primitive_height

    def extended_height(kind, params, width=None):
        if kind != PRIMITIVE_ID:
            return original_height(kind, params, width)
        try:
            rows, _, _ = electron_transfer_rows(params, VP.ConservationError)
            return max(164.0, 88.0 + 38.0 * len(rows))
        except (ValueError, VP.ConservationError):
            return 164.0

    if PRIMITIVE_ID not in VP.PRIMITIVE_KINDS:
        VP.PRIMITIVE_KINDS = tuple(VP.PRIMITIVE_KINDS) + (PRIMITIVE_ID,)
    VP.PRIMITIVE_TITLES[PRIMITIVE_ID] = "Electron-transfer ledger: loss, gain, balance"
    VP.RENDERERS[PRIMITIVE_ID] = draw
    VP.BASE_HEIGHTS[PRIMITIVE_ID] = 164
    VP.REDOX_GATED.add(PRIMITIVE_ID)
    VP.primitive_height = extended_height
    _INSTALLED = True


__all__ = ["MIN_LEARNER_FONT_PT", "PRIMITIVE_ID", "electron_transfer_rows", "install"]
