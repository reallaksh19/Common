#!/usr/bin/env python3
"""Build the layout probe object map.

Three pages that between them carry every shape the stress test broke:

* page 1 — a `PROOF` item (Euclid class): stem, two proof obligations, a proof-sized
  workspace, and a diagram with its label;
* page 2 — a `MULTIPART` item (Polynomials class): stem, three subparts and the multipart
  workspace whose measured content must fit the rectangle it was given;
* page 3 — two solution blocks packed two-up, which is the shape that collided in the
  Euclid run and is only legal here because it was measured first.

Objects declare `container_id`, so a child inside its panel is legal containment while two
siblings overlapping is a collision. They declare `content_height_pt`, so measured height
can be compared with allocated height. Workspace objects declare `response_mode`, so the
workspace can be checked against the response the question actually demands.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PHASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PHASE / "engine"))

from validate_layout_safety import load, measure_then_pack  # noqa: E402

OUT = PHASE / "fixtures" / "math-layout-probe.fixture.json"
REGISTRY = load(PHASE / "registry" / "math-typography-role-registry.json")

PAGE_W, PAGE_H = 595.28, 841.89
MARGIN = 42.0
CONTENT_W = PAGE_W - 2 * MARGIN
PRINTABLE_H = PAGE_H - 2 * MARGIN


def obj(object_id, kind, question_ref, page, order, box, text, role, size, *,
        atomic_ask_ref=None, opaque=False, container_id=None, content_height_pt=None,
        response_mode=None) -> dict:
    return {
        "object_id": object_id,
        "kind": kind,
        "question_ref": question_ref,
        "atomic_ask_ref": atomic_ask_ref,
        "page": page,
        "paint_order": order,
        "opaque": opaque,
        "box": box,
        "text": text,
        "typography_role": role,
        "font_size_pt": size,
        "container_id": container_id,
        "content_height_pt": content_height_pt,
        "response_mode": response_mode,
    }


def box(x, y, w, h) -> dict:
    return {"x": round(x, 2), "y": round(y, 2), "w": round(w, 2), "h": round(h, 2)}


def page_one() -> list[dict]:
    """Euclid class: a proof item with a diagram."""
    top = PAGE_H - MARGIN
    panel_h = 132.0
    panel_y = top - panel_h
    out = [
        obj("Q2/panel", "PANEL", "Q2", 1, 0,
            box(MARGIN, panel_y, CONTENT_W, panel_h), "", "PAGE_FURNITURE", 8.0),
        obj("Q2/stem", "STEM", "Q2", 1, 1,
            box(MARGIN + 6, panel_y + panel_h - 34, CONTENT_W - 12, 26),
            "Two distinct lines cannot have more than one point in common.",
            "QUESTION_BODY", 11.5, container_id="Q2/panel", content_height_pt=26.0),
        obj("Q2/proof-1", "SUBPART", "Q2", 1, 2,
            box(MARGIN + 18, panel_y + panel_h - 74, CONTENT_W - 36, 30),
            "Prove the statement using Euclid's axioms.",
            "QUESTION_BODY", 11.0, atomic_ask_ref="Q2#PROOF-1",
            container_id="Q2/panel", content_height_pt=30.0),
        obj("Q2/proof-2", "SUBPART", "Q2", 1, 3,
            box(MARGIN + 18, panel_y + panel_h - 118, CONTENT_W - 36, 36),
            "Hence deduce that two distinct lines cannot both pass through two distinct "
            "given points.",
            "QUESTION_BODY", 11.0, atomic_ask_ref="Q2#PROOF-2",
            container_id="Q2/panel", content_height_pt=36.0),
    ]
    figure_h = 190.0
    figure_y = panel_y - 16 - figure_h
    out += [
        obj("Q2/figure", "FIGURE", "Q2", 1, 4,
            box(MARGIN, figure_y, 240.0, figure_h), "", "PAGE_FURNITURE", 8.0),
        obj("Q2/figure/label-A", "FIGURE", "Q2", 1, 5,
            box(MARGIN + 14, figure_y + figure_h - 28, 40.0, 12.0), "A",
            "DIAGRAM_LABEL", 9.0, container_id="Q2/figure", content_height_pt=12.0),
        obj("Q2/figure/label-B", "FIGURE", "Q2", 1, 6,
            box(MARGIN + 186, figure_y + 22, 40.0, 12.0), "B",
            "DIAGRAM_LABEL", 9.0, container_id="Q2/figure", content_height_pt=12.0),
    ]
    workspace_h = 220.0
    workspace_y = figure_y - 16 - workspace_h
    out.append(obj("Q2/workspace", "WORKSPACE", "Q2", 1, 7,
                   box(MARGIN + 254, figure_y - 16 - workspace_h + 16,
                       CONTENT_W - 254, workspace_h + figure_h - 16),
                   "Write your proof here", "WORKSPACE", 9.5,
                   opaque=False, content_height_pt=workspace_h + figure_h - 16,
                   response_mode="PROOF"))
    _ = workspace_y
    return out


def page_two() -> list[dict]:
    """Polynomials class: a multipart item whose workspace must fit its content."""
    top = PAGE_H - MARGIN
    panel_h = 150.0
    panel_y = top - panel_h
    out = [
        obj("Q3/panel", "PANEL", "Q3", 2, 0,
            box(MARGIN, panel_y, CONTENT_W, panel_h), "", "PAGE_FURNITURE", 8.0),
        obj("Q3/stem", "STEM", "Q3", 2, 1,
            box(MARGIN + 6, panel_y + panel_h - 32, CONTENT_W - 12, 24),
            "For the polynomial p(x) = x³ + ax² − 5x + 6:",
            "MATH_INLINE", 11.5, container_id="Q3/panel", content_height_pt=24.0),
        obj("Q3/sub-a", "SUBPART", "Q3", 2, 2,
            box(MARGIN + 18, panel_y + panel_h - 68, CONTENT_W - 36, 28),
            "(a) Find the value of a for which (x − 1) is a factor of p(x).",
            "QUESTION_BODY", 11.0, atomic_ask_ref="Q3#SUB-a",
            container_id="Q3/panel", content_height_pt=28.0),
        obj("Q3/sub-b", "SUBPART", "Q3", 2, 3,
            box(MARGIN + 18, panel_y + panel_h - 102, CONTENT_W - 36, 28),
            "(b) Using that value of a, factorise p(x) completely.",
            "QUESTION_BODY", 11.0, atomic_ask_ref="Q3#SUB-b",
            container_id="Q3/panel", content_height_pt=28.0),
        obj("Q3/cond", "SUBPART", "Q3", 2, 4,
            box(MARGIN + 18, panel_y + panel_h - 140, CONTENT_W - 36, 32),
            "State the values of a for which p(x) has no linear factor with integer root.",
            "QUESTION_BODY", 11.0, atomic_ask_ref="Q3#COND",
            container_id="Q3/panel", content_height_pt=32.0),
    ]
    workspace_h = 330.0
    workspace_y = panel_y - 18 - workspace_h
    out.append(obj("Q3/workspace", "WORKSPACE", "Q3", 2, 5,
                   box(MARGIN, workspace_y, CONTENT_W, workspace_h),
                   "Working space", "WORKSPACE", 9.5,
                   content_height_pt=318.0, response_mode="MULTIPART"))
    out.append(obj("Q3/source-note", "PAGE_FURNITURE", "Q3", 2, 6,
                   box(MARGIN, workspace_y - 22, CONTENT_W, 12.0),
                   "WHERE THIS QUESTION CAME FROM", "SOURCE_META", 8.0,
                   content_height_pt=12.0))
    return out


def page_three() -> list[dict]:
    """Two measured solution blocks, packed only because they were measured first."""
    blocks = [{"block_id": "Q2/solution", "height_pt": 322.0},
              {"block_id": "Q3/solution", "height_pt": 358.0}]
    gap = float(REGISTRY["solution_packing_policy"]["inter_block_gap_pt"])
    pages = measure_then_pack(blocks, PRINTABLE_H, gap)
    assert pages == [["Q2/solution", "Q3/solution"]], pages

    out: list[dict] = []
    cursor = PAGE_H - MARGIN
    for order, block in enumerate(blocks):
        height = block["height_pt"]
        cursor -= height
        question = block["block_id"].split("/")[0]
        out.append(obj(block["block_id"], "SOLUTION", question, 3, order * 2,
                       box(MARGIN, cursor, CONTENT_W, height),
                       "FULL WORKING", "SOLUTION_BODY", 10.5,
                       content_height_pt=height))
        out.append(obj(f"{block['block_id']}/check", "VERIFICATION", question, 3,
                       order * 2 + 1,
                       box(MARGIN + 8, cursor + 8, CONTENT_W - 16, 34.0),
                       "QUICK CHECK", "SOLUTION_BODY", 10.0,
                       container_id=block["block_id"], content_height_pt=34.0))
        cursor -= gap
    return out


def build() -> dict:
    objects = page_one() + page_two() + page_three()
    return {
        "map_id": "MATH-ROM-LAYOUT-PROBE",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "page_count": 3,
        "page_width_pt": PAGE_W,
        "page_height_pt": PAGE_H,
        "printable_margin_pt": MARGIN,
        "objects": objects,
    }


def main() -> None:
    payload = build()
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"wrote {OUT.name}: {len(payload['objects'])} objects over "
          f"{payload['page_count']} pages")


if __name__ == "__main__":
    main()
