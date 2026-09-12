"""Learning-support primitives consumed from Primary Math V2 representation plans.

These primitives realize semantic support states; they never infer pedagogy or
mathematical values from prose. All data-bearing content comes from ``params``.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Iterable

from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend,
)


class LearningSupportPrimitives:
    @staticmethod
    def _draw_tokens(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        count: int,
        stroke: str = PrimaryPalette.ACCENT_BLUE,
    ) -> None:
        if count <= 0:
            return
        cols = max(1, int(math.ceil(math.sqrt(count))))
        rows = int(math.ceil(count / cols))
        cell_w = bbox.width / cols
        cell_h = bbox.height / rows
        radius = max(1.5, min(cell_w, cell_h) * 0.18)
        for idx in range(count):
            row = idx // cols
            col = idx % cols
            cx = bbox.x + (col + 0.5) * cell_w
            cy = bbox.y_max - (row + 0.5) * cell_h
            backend.draw_circle(cx, cy, radius, fill=PrimaryPalette.WHITE, stroke=stroke, stroke_width=1.2)

    @staticmethod
    def draw_rate_compare(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        base = params["base_amount"]
        target = params["target_amount"]
        backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)
        cy = bbox.y + bbox.height * 0.45
        lx = bbox.x + bbox.width * 0.22
        rx = bbox.x + bbox.width * 0.78
        backend.draw_text(str(base), lx, cy + 12.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")
        backend.draw_text(str(target), rx, cy + 12.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")
        backend.draw_arrow(lx + 18.0, cy, rx - 18.0, cy, stroke=PrimaryPalette.TEAL, stroke_width=1.8)
        backend.record_evidence("RATE_COMPARE", params, 4, [str(base), str(target)])

    @staticmethod
    def draw_scale_factor(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        factor = params["scale_factor"]
        backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)
        cy = bbox.y + bbox.height * 0.5
        backend.draw_arrow(bbox.x + 24.0, cy, bbox.x_max - 24.0, cy, stroke=PrimaryPalette.TEAL, stroke_width=2.0)
        label = f"x {factor}"
        backend.draw_text(label, bbox.x + bbox.width / 2.0, cy + 12.0, font_size=13.0, color=PrimaryPalette.TEAL, align="center")
        backend.record_evidence("SCALE_FACTOR_VIEW", params, 3, [str(factor), label])

    @staticmethod
    def draw_rate_scale_model(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        base_amount = params.get("base_amount")
        target_amount = params.get("target_amount")
        base_count = int(params["base_count"])
        target_count = params.get("target_count")
        factor = params["scale_factor"]

        backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)
        left = BoundingBox(bbox.x + 12.0, bbox.y + 18.0, bbox.width * 0.34, bbox.height - 48.0)
        right = BoundingBox(bbox.x + bbox.width * 0.62, bbox.y + 18.0, bbox.width * 0.32, bbox.height - 48.0)
        LearningSupportPrimitives._draw_tokens(backend, left, base_count)
        if target_count is not None:
            LearningSupportPrimitives._draw_tokens(backend, right, int(target_count), stroke=PrimaryPalette.TEAL)
        else:
            backend.draw_text("?", right.x + right.width / 2.0, right.y + right.height / 2.0, font_size=18.0, color=PrimaryPalette.TEAL, align="center")

        if base_amount is not None:
            backend.draw_text(str(base_amount), left.x + left.width / 2.0, bbox.y_max - 20.0, font_size=11.0, color=PrimaryPalette.NAVY, align="center")
        if target_amount is not None:
            backend.draw_text(str(target_amount), right.x + right.width / 2.0, bbox.y_max - 20.0, font_size=11.0, color=PrimaryPalette.NAVY, align="center")
        backend.draw_arrow(left.x_max + 8.0, bbox.y + bbox.height / 2.0, right.x - 8.0, bbox.y + bbox.height / 2.0, stroke=PrimaryPalette.TEAL, stroke_width=1.8)
        backend.draw_text(f"x {factor}", bbox.x + bbox.width / 2.0, bbox.y + bbox.height / 2.0 + 12.0, font_size=11.0, color=PrimaryPalette.TEAL, align="center")
        labels = [str(base_count), str(factor)]
        if target_count is not None:
            labels.append(str(target_count))
        if base_amount is not None:
            labels.append(str(base_amount))
        if target_amount is not None:
            labels.append(str(target_amount))
        backend.record_evidence("RATE_SCALE_MODEL", params, base_count + (int(target_count) if target_count is not None else 1) + 5, labels)

    @staticmethod
    def _draw_division_table(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        columns: Iterable[int],
        rows: Iterable[int],
        cells: Dict[tuple[int, int], Any] | None = None,
        highlight: tuple[int, int] | None = None,
    ) -> None:
        columns = [int(x) for x in columns]
        rows = [int(x) for x in rows]
        cells = cells or {}
        ncols = len(columns) + 1
        nrows = len(rows) + 1
        cell_w = bbox.width / ncols
        cell_h = bbox.height / nrows
        for r in range(nrows):
            for col in range(ncols):
                x = bbox.x + col * cell_w
                y = bbox.y_max - (r + 1) * cell_h
                fill = PrimaryPalette.WHITE
                if r == 0 or col == 0:
                    fill = PrimaryPalette.LIGHT_BG
                if highlight and r > 0 and col > 0 and (columns[col - 1], rows[r - 1]) == highlight:
                    fill = PrimaryPalette.HIGHLIGHT_YELLOW
                backend.draw_rect(x, y, cell_w, cell_h, fill=fill, stroke=PrimaryPalette.CARD_BORDER, stroke_width=1.0)
        for idx, value in enumerate(columns, start=1):
            backend.draw_text(str(value), bbox.x + (idx + 0.5) * cell_w, bbox.y_max - 0.62 * cell_h, font_size=10.5, color=PrimaryPalette.NAVY, align="center")
        for idx, value in enumerate(rows, start=1):
            backend.draw_text(str(value), bbox.x + 0.5 * cell_w, bbox.y_max - (idx + 0.62) * cell_h, font_size=10.5, color=PrimaryPalette.TEAL, align="center")
        for (column, row), value in cells.items():
            ci = columns.index(int(column)) + 1
            ri = rows.index(int(row)) + 1
            backend.draw_text(str(value), bbox.x + (ci + 0.5) * cell_w, bbox.y_max - (ri + 0.62) * cell_h, font_size=11.0, color=PrimaryPalette.NAVY, align="center")

    @staticmethod
    def draw_division_table_model(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        columns = params["columns"]
        rows = params["rows"]
        values = {}
        for cell in params.get("cells", []):
            values[(int(cell["column"]), int(cell["row"]))] = cell["quotient"]
        LearningSupportPrimitives._draw_division_table(backend, bbox, columns, rows, values)
        labels = [str(x) for x in columns] + [str(x) for x in rows] + [str(v) for v in values.values()]
        backend.record_evidence("DIVISION_TABLE_MODEL", params, (len(columns) + 1) * (len(rows) + 1) + len(labels), labels)

    @staticmethod
    def draw_division_table_roles(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        columns = params.get("columns", [])
        rows = params.get("rows", [])
        table_box = BoundingBox(bbox.x + bbox.width * 0.24, bbox.y + 8.0, bbox.width * 0.72, bbox.height - 16.0)
        LearningSupportPrimitives._draw_division_table(backend, table_box, columns, rows)
        backend.draw_text("TOP = dividend", bbox.x + 4.0, bbox.y_max - 24.0, font_size=9.5, color=PrimaryPalette.ACCENT_BLUE)
        backend.draw_text("SIDE = divisor", bbox.x + 4.0, bbox.y_max - 44.0, font_size=9.5, color=PrimaryPalette.TEAL)
        labels = [str(x) for x in columns] + [str(x) for x in rows] + ["TOP = dividend", "SIDE = divisor"]
        backend.record_evidence("DIVISION_TABLE_ROLE_HIGHLIGHT", params, (len(columns) + 1) * (len(rows) + 1) + 2, labels)

    @staticmethod
    def draw_division_table_cell(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        """Render either an abstract table rule or one grounded table cell.

        Abstract form is deliberately number-free and is used before a learner is
        shown a specific cell: ``{"operation": "column/row"}``.

        Exact form is used once a cell is selected:
        ``{"column": 720, "row": 60, "quotient": 12?}``.
        """
        backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)
        cx = bbox.x + bbox.width * 0.52
        cy = bbox.y + bbox.height * 0.48

        if "column" not in params or "row" not in params:
            operation = str(params.get("operation") or "").strip()
            if not operation:
                raise ValueError("DIVISION_TABLE_CELL_MODEL requires either column+row or operation")
            normalized = operation.replace("/", " ÷ ")
            backend.draw_rect(cx - 92.0, cy + 16.0, 76.0, 34.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.ACCENT_BLUE, corner_radius=4.0)
            backend.draw_rect(cx - 92.0, cy - 42.0, 76.0, 34.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, corner_radius=4.0)
            backend.draw_text("TOP", cx - 54.0, cy + 27.0, font_size=10.5, color=PrimaryPalette.ACCENT_BLUE, align="center")
            backend.draw_text("SIDE", cx - 54.0, cy - 31.0, font_size=10.5, color=PrimaryPalette.TEAL, align="center")
            backend.draw_arrow(cx - 8.0, cy + 32.0, cx + 26.0, cy + 10.0, stroke=PrimaryPalette.ACCENT_BLUE)
            backend.draw_arrow(cx - 8.0, cy - 25.0, cx + 26.0, cy - 3.0, stroke=PrimaryPalette.TEAL)
            backend.draw_text("÷", cx + 48.0, cy + 1.0, font_size=18.0, color=PrimaryPalette.NAVY, align="center")
            backend.draw_text("?", cx + 86.0, cy + 1.0, font_size=17.0, color=PrimaryPalette.NAVY, align="center")
            backend.draw_text(normalized, cx, bbox.y + 14.0, font_size=9.5, color=PrimaryPalette.SLATE, align="center")
            labels = ["TOP", "SIDE", normalized, "?"]
            backend.record_evidence("DIVISION_TABLE_CELL_MODEL", params, 10, labels)
            return

        column = int(params["column"])
        row = int(params["row"])
        quotient = params.get("quotient")
        backend.draw_text(str(column), cx, cy + 28.0, font_size=11.0, color=PrimaryPalette.ACCENT_BLUE, align="center")
        backend.draw_text(str(row), cx - 52.0, cy, font_size=11.0, color=PrimaryPalette.TEAL, align="center")
        backend.draw_arrow(cx, cy + 18.0, cx, cy + 4.0, stroke=PrimaryPalette.ACCENT_BLUE)
        backend.draw_arrow(cx - 38.0, cy, cx - 10.0, cy, stroke=PrimaryPalette.TEAL)
        result = "?" if quotient is None else str(quotient)
        backend.draw_text(result, cx, cy - 4.0, font_size=13.0, color=PrimaryPalette.NAVY, align="center")
        labels = [str(column), str(row), result]
        backend.record_evidence("DIVISION_TABLE_CELL_MODEL", params, 7, labels)
