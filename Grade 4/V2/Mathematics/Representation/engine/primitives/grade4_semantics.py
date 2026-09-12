"""Grade-4 semantic visual primitives.

These are the typed visual meanings emitted by Grade-4 LearningDesign. They are
not layout fallbacks: every renderer derives only from semantic params supplied by
the validated LearningRepresentationPlan.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List

from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend,
)
from Primary.V2.Mathematics.Representation.engine.primitives.geometry import GeometryPrimitives


class Grade4SemanticPrimitives:
    @staticmethod
    def _frame(backend: VectorRenderBackend, bbox: BoundingBox) -> None:
        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE,
            stroke=PrimaryPalette.CARD_BORDER,
            stroke_width=1.0,
            corner_radius=6.0,
        )

    @staticmethod
    def _tokens(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        count: int,
        *,
        stroke: str = PrimaryPalette.ACCENT_BLUE,
        max_draw: int = 24,
    ) -> int:
        draw_count = max(0, min(int(count), max_draw))
        if draw_count == 0:
            return 0
        cols = max(1, int(math.ceil(math.sqrt(draw_count))))
        rows = int(math.ceil(draw_count / cols))
        cw = bbox.width / cols
        ch = bbox.height / rows
        radius = max(2.0, min(cw, ch) * 0.17)
        for idx in range(draw_count):
            row = idx // cols
            col = idx % cols
            cx = bbox.x + (col + 0.5) * cw
            cy = bbox.y_max - (row + 0.5) * ch
            backend.draw_circle(cx, cy, radius, fill=PrimaryPalette.WHITE, stroke=stroke, stroke_width=1.1)
        return draw_count

    @staticmethod
    def draw_object_groups(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        groups = list(params.get("groups") or [])
        labels: List[str] = []
        element_count = 1
        if groups:
            gap = 12.0
            panel_w = (bbox.width - gap * (len(groups) + 1)) / len(groups)
            for idx, group in enumerate(groups):
                x = bbox.x + gap + idx * (panel_w + gap)
                panel = BoundingBox(x, bbox.y + 14.0, panel_w, bbox.height - 38.0)
                backend.draw_rect(panel.x, panel.y, panel.width, panel.height, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=5.0)
                kind = str(group.get("kind", "group")).replace("_", " ").title()
                count = int(group.get("count", 0))
                backend.draw_text(f"{count} {kind}", panel.x + panel.width / 2.0, panel.y_max - 16.0, font_size=10.5, color=PrimaryPalette.NAVY, align="center")
                token_box = BoundingBox(panel.x + 8.0, panel.y + 8.0, panel.width - 16.0, max(20.0, panel.height - 34.0))
                element_count += Grade4SemanticPrimitives._tokens(backend, token_box, count) + 2
                labels.extend([str(count), kind])
        else:
            count = int(params.get("rendered_quantity", params.get("declared_quantity", params.get("count", 0))))
            token_box = BoundingBox(bbox.x + 16.0, bbox.y + 16.0, bbox.width - 32.0, bbox.height - 32.0)
            element_count += Grade4SemanticPrimitives._tokens(backend, token_box, count)
            labels.append(str(count))
        backend.record_evidence("OBJECT_GROUPS", params, element_count, labels)

    @staticmethod
    def draw_money_model(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        groups = list(params.get("groups") or [])
        subtotals = list(params.get("subtotals") or [])
        labels: List[str] = []
        count = 1
        if groups:
            gap = 14.0
            panel_w = (bbox.width - gap * (len(groups) + 1)) / len(groups)
            for idx, group in enumerate(groups):
                x = bbox.x + gap + idx * (panel_w + gap)
                panel = BoundingBox(x, bbox.y + 16.0, panel_w, bbox.height - 32.0)
                backend.draw_rect(panel.x, panel.y, panel.width, panel.height, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=5.0)
                n = int(group.get("count", 0))
                price = group.get("unit_price")
                kind = str(group.get("kind", "item")).replace("_", " ").title()
                backend.draw_text(f"{n} {kind}", panel.x + panel.width / 2.0, panel.y_max - 18.0, font_size=11.0, color=PrimaryPalette.NAVY, align="center")
                if price is not None:
                    backend.draw_text(f"Rs {price} each", panel.x + panel.width / 2.0, panel.y_max - 36.0, font_size=10.5, color=PrimaryPalette.TEAL, align="center")
                token_box = BoundingBox(panel.x + 10.0, panel.y + 10.0, panel.width - 20.0, max(20.0, panel.height - 58.0))
                count += Grade4SemanticPrimitives._tokens(backend, token_box, n, stroke=PrimaryPalette.ACCENT_BLUE if idx == 0 else PrimaryPalette.AMBER) + 3
                labels.extend([str(n), kind, str(price)])
        elif subtotals:
            gap = 16.0
            card_w = min(120.0, (bbox.width - gap * (len(subtotals) + 1)) / len(subtotals))
            total_w = len(subtotals) * card_w + (len(subtotals) - 1) * gap
            start_x = bbox.x + (bbox.width - total_w) / 2.0
            cy = bbox.y + bbox.height / 2.0
            for idx, value in enumerate(subtotals):
                x = start_x + idx * (card_w + gap)
                backend.draw_rect(x, cy - 28.0, card_w, 56.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, corner_radius=5.0)
                backend.draw_text(f"Rs {value}", x + card_w / 2.0, cy - 4.0, font_size=13.0, color=PrimaryPalette.NAVY, align="center")
                if idx < len(subtotals) - 1:
                    backend.draw_text("+", x + card_w + gap / 2.0, cy - 4.0, font_size=16.0, color=PrimaryPalette.AMBER, align="center")
                labels.append(str(value))
                count += 2
        else:
            backend.draw_text("Money", bbox.x + bbox.width / 2.0, bbox.y + bbox.height / 2.0, font_size=13.0, color=PrimaryPalette.TEAL, align="center")
            labels.append("Money")
            count += 1
        backend.record_evidence("MONEY_MODEL", params, count, labels)

    @staticmethod
    def draw_quantity_structure_map(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        branches = [str(x) for x in (params.get("branches") or [])]
        if not branches:
            branches = ["part", "part"]
        gap = 14.0
        card_w = (bbox.width - gap * (len(branches) + 1)) / len(branches)
        cy = bbox.y + bbox.height * 0.58
        for idx, text in enumerate(branches):
            x = bbox.x + gap + idx * (card_w + gap)
            backend.draw_rect(x, cy - 22.0, card_w, 44.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.ACCENT_BLUE, corner_radius=4.0)
            backend.draw_text(text, x + card_w / 2.0, cy - 4.0, font_size=11.0, color=PrimaryPalette.NAVY, align="center")
            backend.draw_arrow(x + card_w / 2.0, cy - 28.0, bbox.x + bbox.width / 2.0, bbox.y + 28.0, stroke=PrimaryPalette.TEAL, stroke_width=1.3)
        backend.draw_text("put together", bbox.x + bbox.width / 2.0, bbox.y + 12.0, font_size=10.0, color=PrimaryPalette.TEAL, align="center")
        backend.record_evidence("QUANTITY_STRUCTURE_MAP", params, len(branches) * 3 + 2, branches + ["put together"])

    @staticmethod
    def draw_inverse_check(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        expression = params.get("expression")
        unit_rate = params.get("unit_rate")
        if expression:
            text = f"Check: {expression}"
        elif unit_rate is not None:
            text = f"Check the same rate: {unit_rate} each"
        else:
            text = "Check the relationship"
        backend.draw_text("✓", bbox.x + 24.0, bbox.y + bbox.height / 2.0 - 7.0, font_size=18.0, color=PrimaryPalette.SOFT_GREEN, align="center")
        backend.draw_text(text, bbox.x + 48.0, bbox.y + bbox.height / 2.0 - 4.0, font_size=11.0, color=PrimaryPalette.NAVY)
        backend.record_evidence("INVERSE_CHECK", params, 3, [text])

    @staticmethod
    def draw_div_equal_group(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        group_size = int(params.get("group_size", params.get("divisor", 0)))
        inner = BoundingBox(bbox.x + 18.0, bbox.y + 18.0, bbox.width - 36.0, bbox.height - 46.0)
        drawn = Grade4SemanticPrimitives._tokens(backend, inner, group_size, stroke=PrimaryPalette.TEAL)
        backend.draw_text(f"{group_size} in each group", bbox.x + bbox.width / 2.0, bbox.y_max - 18.0, font_size=11.0, color=PrimaryPalette.TEAL, align="center")
        backend.record_evidence("DIV_EQUAL_GROUP", params, drawn + 2, [str(group_size)])

    @staticmethod
    def draw_div_multiples_strip(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        comparisons = [str(x).replace("x", "×") for x in (params.get("comparisons") or [])]
        labels: List[str] = []
        if comparisons:
            values = comparisons
        else:
            divisor = int(params.get("divisor", 0))
            if divisor <= 0:
                values = ["multiple", "multiple", "multiple"]
            else:
                values = [f"{i} × {divisor} = {i * divisor}" for i in range(1, 6)]
        gap = 8.0
        card_w = (bbox.width - gap * (len(values) + 1)) / len(values)
        card_w = max(54.0, card_w)
        if card_w * len(values) + gap * (len(values) + 1) > bbox.width:
            card_w = (bbox.width - gap * (len(values) + 1)) / len(values)
        cy = bbox.y + bbox.height / 2.0
        for idx, text in enumerate(values):
            x = bbox.x + gap + idx * (card_w + gap)
            backend.draw_rect(x, cy - 24.0, card_w, 48.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, corner_radius=4.0)
            backend.draw_text(text, x + card_w / 2.0, cy - 4.0, font_size=9.5, color=PrimaryPalette.NAVY, align="center")
            labels.append(text)
        backend.record_evidence("DIV_MULTIPLES_STRIP", params, len(values) * 2 + 1, labels)

    @staticmethod
    def draw_div_remainder_context(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        group_size = params.get("group_size")
        rendered_groups = int(params.get("rendered_quantity", 0)) if group_size is not None else 0
        declared_groups = params.get("declared_quantity")
        leftover = int(params.get("leftover", params.get("remainder", 0)))
        continuation = params.get("continuation_marker")
        labels: List[str] = []

        if group_size is not None and rendered_groups > 0:
            sample_n = min(rendered_groups, 4)
            gap = 8.0
            box_w = min(82.0, (bbox.width * 0.70 - gap * (sample_n - 1)) / sample_n)
            for idx in range(sample_n):
                x = bbox.x + 14.0 + idx * (box_w + gap)
                box = BoundingBox(x, bbox.y + 30.0, box_w, bbox.height - 56.0)
                backend.draw_rect(box.x, box.y, box.width, box.height, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, corner_radius=4.0)
                backend.draw_text(str(group_size), box.x + box.width / 2.0, box.y + box.height / 2.0 - 4.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")
            labels.extend([str(group_size), str(rendered_groups)])
            marker = str(continuation or (f"… × {declared_groups}" if declared_groups is not None else "…"))
            backend.draw_text(marker, bbox.x + bbox.width * 0.72, bbox.y + bbox.height * 0.62, font_size=11.0, color=PrimaryPalette.SLATE, align="center")
            labels.append(marker)

        if leftover > 0:
            left_box = BoundingBox(bbox.x + bbox.width * 0.76, bbox.y + 22.0, bbox.width * 0.20, bbox.height * 0.42)
            drawn = Grade4SemanticPrimitives._tokens(backend, left_box, leftover, stroke=PrimaryPalette.AMBER)
            backend.draw_text(f"{leftover} left", left_box.x + left_box.width / 2.0, left_box.y_max + 5.0, font_size=10.5, color=PrimaryPalette.AMBER, align="center")
            labels.append(str(leftover))
        else:
            drawn = 0
        backend.record_evidence("DIV_REMAINDER_CONTEXT", params, rendered_groups + drawn + 3, labels)

    @staticmethod
    def draw_estimate_bound(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        estimate = params.get("estimate")
        if estimate is None:
            text = "Estimate first"
        else:
            text = f"about {estimate}"
        backend.draw_text("≈", bbox.x + bbox.width * 0.30, bbox.y + bbox.height / 2.0 - 8.0, font_size=22.0, color=PrimaryPalette.AMBER, align="center")
        backend.draw_text(text, bbox.x + bbox.width * 0.58, bbox.y + bbox.height / 2.0 - 4.0, font_size=13.0, color=PrimaryPalette.NAVY, align="center")
        backend.record_evidence("ESTIMATE_BOUND", params, 3, [text])

    @staticmethod
    def draw_div_long_algorithm(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        if "dividend" in params and "divisor" in params:
            dividend = int(params["dividend"])
            divisor = int(params["divisor"])
            quotient = params.get("quotient")
            remainder = params.get("remainder")
            dividend_s = str(dividend)
            ox = bbox.x + bbox.width * 0.30
            oy = bbox.y + bbox.height * 0.48
            col_w = 24.0
            backend.draw_text(str(divisor), ox - 14.0, oy, font_size=15.0, color=PrimaryPalette.NAVY, align="right")
            backend.draw_line(ox - 5.0, oy - 4.0, ox - 5.0, oy + 20.0, stroke=PrimaryPalette.NAVY, stroke_width=1.6)
            backend.draw_line(ox - 5.0, oy + 20.0, ox + len(dividend_s) * col_w + 12.0, oy + 20.0, stroke=PrimaryPalette.NAVY, stroke_width=1.6)
            for idx, char in enumerate(dividend_s):
                backend.draw_text(char, ox + idx * col_w + 8.0, oy, font_size=15.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")
            labels = [str(dividend), str(divisor)]
            if quotient is not None:
                q_s = str(quotient)
                offset = len(dividend_s) - len(q_s)
                for idx, char in enumerate(q_s):
                    backend.draw_text(char, ox + (offset + idx) * col_w + 8.0, oy + 26.0, font_size=15.0, color=PrimaryPalette.TEAL, align="center")
                labels.append(q_s)
            if remainder is not None:
                backend.draw_text(f"R {remainder}", ox + len(dividend_s) * col_w + 34.0, oy - 3.0, font_size=12.0, color=PrimaryPalette.AMBER)
                labels.append(str(remainder))
            backend.record_evidence("DIV_LONG_ALGORITHM", params, 6 + len(dividend_s), labels)
            return

        partial = params.get("partial_dividend")
        q_digit = params.get("quotient_digit")
        product = params.get("product")
        if partial is not None and q_digit is not None and product is not None:
            partial = int(partial)
            q_digit = int(q_digit)
            product = int(product)
            remainder = partial - product
            cx = bbox.x + bbox.width / 2.0
            cy = bbox.y + bbox.height * 0.62
            backend.draw_text(f"{partial} ÷ ?  →  quotient digit {q_digit}", cx, cy, font_size=11.5, color=PrimaryPalette.NAVY, align="center")
            backend.draw_text(str(partial), cx + 20.0, cy - 28.0, font_size=13.0, color=PrimaryPalette.STUDENT_PENCIL, align="right")
            backend.draw_text(f"− {product}", cx + 20.0, cy - 48.0, font_size=13.0, color=PrimaryPalette.STUDENT_PENCIL, align="right")
            backend.draw_line(cx - 20.0, cy - 52.0, cx + 26.0, cy - 52.0, stroke=PrimaryPalette.SLATE, stroke_width=1.0)
            backend.draw_text(str(remainder), cx + 20.0, cy - 70.0, font_size=13.0, color=PrimaryPalette.TEAL, align="right")
            backend.record_evidence("DIV_LONG_ALGORITHM", params, 6, [str(partial), str(q_digit), str(product), str(remainder)])
            return

        backend.draw_text("Long division", bbox.x + bbox.width / 2.0, bbox.y + bbox.height / 2.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")
        backend.record_evidence("DIV_LONG_ALGORITHM", params, 2, ["Long division"])

    @staticmethod
    def draw_angle_rays_arc(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        degrees = int(params.get("degrees", params.get("declared_quantity", 60)))
        if degrees < 90:
            classification = "ACUTE"
        elif degrees == 90:
            classification = "RIGHT"
        elif degrees < 180:
            classification = "OBTUSE"
        elif degrees == 180:
            classification = "STRAIGHT"
        else:
            classification = "REFLEX"
        GeometryPrimitives.draw_angle(
            backend,
            bbox,
            {"angle_degrees": degrees, "classification": classification},
        )

    @staticmethod
    def draw_angle_benchmark_compare(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        degrees = int(params.get("degrees", 90))
        Grade4SemanticPrimitives._frame(backend, bbox)
        left = BoundingBox(bbox.x + 10.0, bbox.y + 12.0, bbox.width * 0.44, bbox.height - 24.0)
        right = BoundingBox(bbox.x + bbox.width * 0.54, bbox.y + 12.0, bbox.width * 0.44, bbox.height - 24.0)
        Grade4SemanticPrimitives._draw_simple_angle(backend, left, degrees, PrimaryPalette.ACCENT_BLUE)
        Grade4SemanticPrimitives._draw_simple_angle(backend, right, 90, PrimaryPalette.TEAL)
        backend.draw_text(f"{degrees}°", left.x + left.width / 2.0, left.y_max - 16.0, font_size=11.0, color=PrimaryPalette.ACCENT_BLUE, align="center")
        backend.draw_text("90° benchmark", right.x + right.width / 2.0, right.y_max - 16.0, font_size=11.0, color=PrimaryPalette.TEAL, align="center")
        backend.record_evidence("ANGLE_BENCHMARK_COMPARE", params, 10, [str(degrees), "90"])

    @staticmethod
    def _draw_simple_angle(backend: VectorRenderBackend, bbox: BoundingBox, degrees: float, stroke: str) -> None:
        vx = bbox.x + bbox.width * 0.28
        vy = bbox.y + bbox.height * 0.30
        length = min(bbox.width * 0.55, bbox.height * 0.48)
        backend.draw_arrow(vx, vy, vx + length, vy, stroke=stroke, stroke_width=1.8)
        rad = math.radians(degrees)
        backend.draw_arrow(vx, vy, vx + length * math.cos(rad), vy + length * math.sin(rad), stroke=stroke, stroke_width=1.8)
        backend.draw_circle(vx, vy, 2.6, fill=stroke, stroke=stroke)

    @staticmethod
    def draw_angle_object_example(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        Grade4SemanticPrimitives._frame(backend, bbox)
        examples = [str(x).lower() for x in (params.get("examples") or [])]
        mark_vertex = bool(params.get("mark_vertex"))
        if not examples:
            examples = ["angle"]
        gap = 10.0
        panel_w = (bbox.width - gap * (len(examples) + 1)) / len(examples)
        labels: List[str] = []
        for idx, example in enumerate(examples):
            x = bbox.x + gap + idx * (panel_w + gap)
            panel = BoundingBox(x, bbox.y + 12.0, panel_w, bbox.height - 24.0)
            cx = panel.x + panel.width / 2.0
            cy = panel.y + panel.height * 0.44
            length = min(panel.width * 0.30, panel.height * 0.28)
            if example == "clock":
                backend.draw_circle(cx, cy, max(18.0, length), fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, stroke_width=1.0)
                backend.draw_line(cx, cy, cx, cy + length * 0.85, stroke=PrimaryPalette.NAVY, stroke_width=1.8)
                backend.draw_line(cx, cy, cx + length * 0.72, cy + length * 0.35, stroke=PrimaryPalette.NAVY, stroke_width=1.8)
            elif example == "triangle":
                backend.draw_polygon([(cx - length, cy - length * 0.6), (cx + length, cy - length * 0.6), (cx, cy + length)], fill=None, stroke=PrimaryPalette.NAVY, stroke_width=1.6)
                cx, cy = cx - length, cy - length * 0.6
            elif example == "scissors":
                backend.draw_line(cx, cy, cx - length, cy - length * 0.6, stroke=PrimaryPalette.NAVY, stroke_width=2.0)
                backend.draw_line(cx, cy, cx + length, cy + length * 0.55, stroke=PrimaryPalette.NAVY, stroke_width=2.0)
                backend.draw_circle(cx - length * 0.85, cy - length * 0.55, 5.0, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.TEAL)
                backend.draw_circle(cx + length * 0.85, cy + length * 0.48, 5.0, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.TEAL)
            else:
                backend.draw_arrow(cx, cy, cx + length, cy, stroke=PrimaryPalette.NAVY, stroke_width=1.8)
                backend.draw_arrow(cx, cy, cx + length * 0.55, cy + length * 0.75, stroke=PrimaryPalette.NAVY, stroke_width=1.8)
            if mark_vertex:
                backend.draw_circle(cx, cy, 3.0, fill=PrimaryPalette.AMBER, stroke=PrimaryPalette.AMBER)
            label = example.title() if example != "angle" else "vertex + rays"
            backend.draw_text(label, panel.x + panel.width / 2.0, panel.y_max - 15.0, font_size=9.5, color=PrimaryPalette.SLATE, align="center")
            labels.append(label)
        backend.record_evidence("ANGLE_OBJECT_EXAMPLE", params, len(examples) * 5 + 1, labels)
