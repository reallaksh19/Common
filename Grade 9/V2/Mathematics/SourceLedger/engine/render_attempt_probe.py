#!/usr/bin/env python3
"""A deterministic attempt-page probe renderer.

This exists so the rendered-coverage witness is exercised against a **real rendered page**
rather than a hand-written object map. It draws exactly what the Linear Equations case
study exposed — a stem, its option set, and the panel that followed it — and emits both the
PDF and the ``math-rendered-object-map`` describing what was placed, in paint order.

Two deliberate defect modes are available so the falsifiers have something to catch:

    ``occlude_after_option``  paint an opaque panel over the tail of the option set
    ``drop_atomic_ask``       omit one required atomic ask entirely
    ``clip_atomic_ask``       place one object outside the printable area
"""
from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
sys.path.insert(0, str(MATH / "MathTypesetting" / "engine"))

from math_expression import GlyphRegistry  # noqa: E402

PAGE_W, PAGE_H = A4
MARGIN = 42.0
BODY_PT = 11.0
STEM_PT = 11.5
OPTION_PT = 10.5


def _wrap(canvas, text: str, font_name: str, size: float, max_width: float) -> list[str]:
    """Greedy word wrap so no placed object can run past the printable width."""
    words, lines, current = str(text).split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if canvas.stringWidth(trial, font_name, size) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _draw_block(canvas, text: str, font_name: str, size: float, x: float, y: float,
                max_width: float) -> tuple[float, float, float]:
    """Draw a wrapped block from baseline ``y`` downwards; return (width, height, next_y)."""
    lines = _wrap(canvas, text, font_name, size, max_width)
    leading = size * 1.34
    canvas.setFont(font_name, size)
    width = 0.0
    for i, line in enumerate(lines):
        canvas.drawString(x, y - i * leading, line)
        width = max(width, canvas.stringWidth(line, font_name, size))
    height = leading * (len(lines) - 1) + size + 4.0
    return width, height, y - leading * (len(lines) - 1)


def render(manifest: dict, out_path: Path | str, *,
           occlude_after_option: str | None = None,
           drop_atomic_ask: str | None = None,
           clip_atomic_ask: str | None = None) -> tuple[Path, dict]:
    """Render the manifest's questions as an attempt page and return (pdf, object_map)."""
    reg = GlyphRegistry()
    font = reg.bind_font("√ ² ₁ × − ≤ ⊂")
    out_path = Path(out_path)
    c = rl_canvas.Canvas(str(out_path), pagesize=A4)
    objects: list[dict] = []
    paint = 0
    y = PAGE_H - MARGIN - 18.0
    page = 1

    def place(object_id, kind, question_ref, atomic_ask_ref, box, text, role, size):
        nonlocal paint
        objects.append({
            "object_id": object_id,
            "kind": kind,
            "question_ref": question_ref,
            "atomic_ask_ref": atomic_ask_ref,
            "page": page,
            "paint_order": paint,
            "opaque": False,
            "box": box,
            "text": text,
            "typography_role": role,
            "font_size_pt": size,
        })
        paint += 1

    for question in manifest["questions"]:
        qref = question["question_ref"]
        # -- stem ---------------------------------------------------------
        c.setFillColor(colors.black)
        stem = f"{question['source_order']}. {question['stem']}"
        content_w = PAGE_W - 2 * MARGIN
        width, height, last_y = _draw_block(c, stem, font.regular_name, STEM_PT,
                                            MARGIN, y, content_w)
        place(f"{qref}/stem", "STEM", qref, None,
              {"x": MARGIN, "y": last_y - 3.0, "w": width, "h": height},
              stem, "QUESTION_BODY", STEM_PT)
        y = last_y - STEM_PT * 1.8

        options = [a for a in question["atomic_asks"] if a["kind"] == "OPTION"]
        others = [a for a in question["atomic_asks"] if a["kind"] != "OPTION"]

        # -- non-option atomic asks, one per line -------------------------
        for ask in others:
            if ask["atomic_ask_ref"] == drop_atomic_ask:
                continue
            label = f"{ask['label']} {ask['text']}"
            width, height, last_y = _draw_block(c, label, font.regular_name, BODY_PT,
                                                MARGIN + 12.0, y, content_w - 12.0)
            box_y = last_y - 3.0
            if ask["atomic_ask_ref"] == clip_atomic_ask:
                box_y = -20.0            # deliberately outside the printable area
            place(f"{qref}/{ask['atomic_ask_ref']}", "SUBPART", qref, ask["atomic_ask_ref"],
                  {"x": MARGIN + 12.0, "y": box_y, "w": width, "h": height},
                  ask["text"], "QUESTION_BODY", BODY_PT)
            y = last_y - BODY_PT * 1.6

        # -- option set, one per line so occlusion is unambiguous ---------
        occlude_from_y = None
        for ask in options:
            if ask["atomic_ask_ref"] == drop_atomic_ask:
                continue
            label = f"{ask['label']}  {ask['text']}"
            c.setFont(font.regular_name, OPTION_PT)
            c.drawString(MARGIN + 20.0, y, label)
            box = {"x": MARGIN + 20.0, "y": y - 3.0,
                   "w": c.stringWidth(label, font.regular_name, OPTION_PT),
                   "h": OPTION_PT + 4.0}
            place(f"{qref}/{ask['atomic_ask_ref']}", "OPTION", qref, ask["atomic_ask_ref"],
                  box, ask["text"], "QUESTION_BODY", OPTION_PT)
            if occlude_after_option and ask["label"].startswith(occlude_after_option):
                occlude_from_y = box["y"] - OPTION_PT * 1.7
            y -= OPTION_PT * 1.7

        # -- the following panel: this is the object that covered C and D --
        panel_top = occlude_from_y if occlude_from_y is not None else y - 6.0
        panel_h = 56.0
        panel_y = panel_top - panel_h + (OPTION_PT + 4.0 if occlude_from_y else 0.0)
        c.setFillColor(colors.HexColor("#EEF3F8"))
        c.rect(MARGIN, panel_y, PAGE_W - 2 * MARGIN, panel_h, stroke=0, fill=1)
        c.setFillColor(colors.black)
        c.setFont(font.regular_name, BODY_PT)
        c.drawString(MARGIN + 8.0, panel_y + panel_h - BODY_PT - 6.0, "Working space")
        objects.append({
            "object_id": f"{qref}/workspace",
            "kind": "WORKSPACE",
            "question_ref": qref,
            "atomic_ask_ref": None,
            "page": page,
            "paint_order": paint,
            "opaque": True,
            "box": {"x": MARGIN, "y": panel_y, "w": PAGE_W - 2 * MARGIN, "h": panel_h},
            "text": "Working space",
            "typography_role": "WORKSPACE",
            "font_size_pt": BODY_PT,
        })
        paint += 1
        y = panel_y - 22.0

        if y < MARGIN + 140.0:
            c.showPage()
            page += 1
            y = PAGE_H - MARGIN - 18.0

    c.showPage()
    c.save()

    object_map = {
        "map_id": f"MATH-ROM-{manifest['topic_ref']}",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "page_count": page,
        "page_width_pt": float(PAGE_W),
        "page_height_pt": float(PAGE_H),
        "printable_margin_pt": MARGIN,
        "objects": objects,
    }
    return out_path, object_map


def page_texts(pdf_path: Path | str) -> list[str]:
    """Extract per-page text so the witness can check what a learner can actually read."""
    import fitz  # type: ignore

    return [p.get_text() for p in fitz.open(str(pdf_path))]
