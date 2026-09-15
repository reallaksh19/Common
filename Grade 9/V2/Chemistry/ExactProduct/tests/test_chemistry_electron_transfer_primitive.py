#!/usr/bin/env python3
"""Physical falsifiers for the topic-neutral C-H electron-transfer ledger."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas

D = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(D / "engine"))

import chemistry_visual_primitives as VP  # noqa: E402
from chemistry_electron_transfer_primitive import install  # noqa: E402
from realize_chemistry_exact_product import register_fonts  # noqa: E402

install()
register_fonts()


def expect(exc, fn, label):
    try:
        fn()
    except exc:
        return
    raise AssertionError("expected " + label)


assert "ELECTRON_TRANSFER_LEDGER" in VP.PRIMITIVE_KINDS
assert "ELECTRON_TRANSFER_LEDGER" in VP.RENDERERS

with tempfile.TemporaryDirectory() as td:
    path = Path(td) / "electron-transfer-ledger-probe.pdf"
    c = rl_canvas.Canvas(str(path), pagesize=A4, invariant=1)

    # Context 1: neutral atoms becoming oppositely charged ions.
    ionic = VP.build_params(
        primitive_id="ELECTRON_TRANSFER_LEDGER",
        tokens=["Na", "Na⁺", "Cl", "Cl⁻"],
        declared_entities=["Na", "Na⁺", "Cl", "Cl⁻"],
        oxidation_states=[
            {"element": "Na", "before": 0, "after": 1, "before_species": "Na", "after_species": "Na⁺", "electron_count": 1},
            {"element": "Cl", "before": 0, "after": -1, "before_species": "Cl", "after_species": "Cl⁻", "electron_count": 1},
        ],
        checks=["electrons lost equals electrons gained"],
    )
    evidence = VP.render_primitive("ELECTRON_TRANSFER_LEDGER", ionic, c, (42, 560, 500, VP.primitive_height("ELECTRON_TRANSFER_LEDGER", ionic)))
    assert evidence["primitive"] == "ELECTRON_TRANSFER_LEDGER"

    # Context 2: one ion is oxidized while another ion is reduced.
    ion_exchange = VP.build_params(
        primitive_id="ELECTRON_TRANSFER_LEDGER",
        tokens=["Fe²⁺", "Fe³⁺", "Cu²⁺", "Cu⁺"],
        declared_entities=["Fe²⁺", "Fe³⁺", "Cu²⁺", "Cu⁺"],
        oxidation_states=[
            {"element": "Fe", "before": 2, "after": 3, "before_species": "Fe²⁺", "after_species": "Fe³⁺", "electron_count": 1},
            {"element": "Cu", "before": 2, "after": 1, "before_species": "Cu²⁺", "after_species": "Cu⁺", "electron_count": 1},
        ],
    )
    evidence2 = VP.render_primitive("ELECTRON_TRANSFER_LEDGER", ion_exchange, c, (42, 340, 500, VP.primitive_height("ELECTRON_TRANSFER_LEDGER", ion_exchange)))
    assert evidence2["primitive"] == "ELECTRON_TRANSFER_LEDGER"

    # Unequal electron exchange must fail before the ledger can be drawn.
    broken = VP.build_params(
        primitive_id="ELECTRON_TRANSFER_LEDGER",
        tokens=["Na", "Na⁺", "Cl", "Cl⁻"],
        declared_entities=["Na", "Na⁺", "Cl", "Cl⁻"],
        oxidation_states=[
            {"element": "Na", "before": 0, "after": 1, "before_species": "Na", "after_species": "Na⁺", "electron_count": 1},
            {"element": "Cl", "before": 0, "after": -1, "before_species": "Cl", "after_species": "Cl⁻", "electron_count": 2},
        ],
    )
    expect(
        VP.ConservationError,
        lambda: VP.render_primitive("ELECTRON_TRANSFER_LEDGER", broken, c, (42, 120, 500, 126)),
        "unequal electron exchange rejected",
    )
    c.save()
    assert path.exists() and path.stat().st_size > 0

print("CHEMISTRY C-H electron-transfer primitive physical falsifiers = PASS")
print("Same renderer exercised across multiple chemical contexts; no topic branch used.")
