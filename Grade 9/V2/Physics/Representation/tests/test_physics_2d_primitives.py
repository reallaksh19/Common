#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from reportlab.pdfgen import canvas as rl_canvas

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from physics_2d_primitive_renderer import (  # noqa: E402
    Unknown2DPrimitive,
    render_primitive_2d,
    supported_kinds_2d,
)

REGISTRY = json.loads((ROOT / "registry" / "physics-2d-teaching-primitive-registry-v1.json").read_text())


def main():
    declared = {row["primitive_id"] for row in REGISTRY["primitives"]}
    assert declared == set(supported_kinds_2d()), (declared, supported_kinds_2d())
    assert REGISTRY["scope"] == "SUBJECT_WIDE_2D"
    assert all(not row["topic_scope_refs"] for row in REGISTRY["primitives"])
    assert all(row["decorative"] is False and row["realized_as_vector_graphics"] is True for row in REGISTRY["primitives"])

    floors = {row["primitive_id"]: row["minimum_vector_ops"] for row in REGISTRY["primitives"]}
    with tempfile.TemporaryDirectory() as td:
        pdf = Path(td) / "physics-2d-primitives.pdf"
        c = rl_canvas.Canvas(str(pdf), pagesize=(595.2756, 841.8898), invariant=1)
        y = 650
        for kind in supported_kinds_2d():
            ev = render_primitive_2d(kind, {}, c, (40, y, 515, 130))
            assert ev["realized"] is True, kind
            assert ev["vector_ops"] >= floors[kind], (kind, ev["vector_ops"], floors[kind])
            assert ev["ink_bbox"] is not None, kind
            assert ev["quantitative_grounding"] == "SCHEMATIC_STRUCTURE_ONLY"
            c.showPage()
        c.save()
        assert pdf.stat().st_size > 1000

    try:
        render_primitive_2d("PROJECTILE_MAGIC_PICTURE", {}, None, (0, 0, 10, 10))
        raise AssertionError("unknown 2D primitive accepted")
    except Unknown2DPrimitive:
        pass

    print("Physics 2D primitive extension: PASS (%d primitives)" % len(declared))


if __name__ == "__main__":
    main()
