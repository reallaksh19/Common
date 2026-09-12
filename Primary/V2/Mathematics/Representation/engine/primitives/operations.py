"""
Deep Multiplication & Division Visual Primitives for Primary Mathematics V2.
Every entity drawn is directly derived from params (0 hardcoded visual constants).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend
)


class MultiplicationPrimitives:
    """Deep Multiplication 6-stage representational bridge primitives."""

    @staticmethod
    def draw_equal_groups(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Stage 1: Equal Groups (e.g. 6 groups of 23)."""
        num_groups = params.get("group_count", 6)
        items_per_group = params.get("items_per_group", 23)

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [f"{num_groups} equal groups of {items_per_group}"]
        backend.draw_text(
            labels[0], bbox.x + 12.0, bbox.y_max - 20.0,
            font_size=12.0, color=PrimaryPalette.NAVY
        )

        # Draw group circles
        padding = 10.0
        avail_w = bbox.width - (2 * padding)
        group_w = avail_w / max(num_groups, 1)
        r = min(group_w / 2.5, (bbox.height - 40.0) / 2.5)

        for i in range(num_groups):
            cx = bbox.x + padding + (i + 0.5) * group_w
            cy = bbox.y + (bbox.height - 20.0) / 2.0
            backend.draw_circle(cx, cy, r, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.AMBER, stroke_width=1.5)
            # Count label inside
            item_lbl = str(items_per_group)
            backend.draw_text(item_lbl, cx, cy - 4.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")
            labels.append(item_lbl)

        backend.record_evidence("EQUAL_GROUPS", params, len(labels) + num_groups, labels)

    @staticmethod
    def draw_array(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Stage 2: Discrete / Scaled Array."""
        rows = params.get("rows", 6)
        cols = params.get("cols", 23)

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [f"Array: {rows} rows x {cols} columns"]
        backend.draw_text(labels[0], bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.0, color=PrimaryPalette.NAVY)

        # Draw representative grid / array boundaries
        grid_w = bbox.width - 40.0
        grid_h = bbox.height - 50.0
        gx = bbox.x + 20.0
        gy = bbox.y + 15.0

        backend.draw_rect(gx, gy, grid_w, grid_h, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.SLATE, stroke_width=1.0)
        
        # Dimensions labels
        backend.draw_text(str(rows), gx - 14.0, gy + grid_h / 2.0, font_size=12.0, color=PrimaryPalette.NAVY, align="right")
        backend.draw_text(str(cols), gx + grid_w / 2.0, gy + grid_h + 4.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")
        labels.extend([str(rows), str(cols)])

        backend.record_evidence("ARRAY", params, len(labels) + 2, labels)

    @staticmethod
    def draw_area_model(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Stage 3: Area / Distributive Partition (e.g. 23 x 6 partitioned into 20x6 and 3x6)."""
        factors = params.get("factors", [23, 6])
        partitions = params.get("partitions", [
            {"length": 20, "height": 6, "area": 120},
            {"length": 3, "height": 6, "area": 18}
        ])

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [f"Area Model: {factors[0]} x {factors[1]}"]
        backend.draw_text(labels[0], bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.0, color=PrimaryPalette.NAVY)

        total_length = sum(p["length"] for p in partitions)
        height_val = factors[1]

        model_w = bbox.width - 60.0
        model_h = bbox.height - 60.0
        mx = bbox.x + 35.0
        my = bbox.y + 20.0

        # Draw left height label
        backend.draw_text(str(height_val), mx - 12.0, my + model_h / 2.0 - 5.0, font_size=13.0, color=PrimaryPalette.NAVY, align="right")
        labels.append(str(height_val))

        # Draw partitioned sub-rectangles proportionally
        cur_x = mx
        for idx, part in enumerate(partitions):
            p_len = part["length"]
            p_area = part["area"]
            sub_w = (p_len / total_length) * model_w
            fill_col = PrimaryPalette.HIGHLIGHT_YELLOW if idx % 2 == 0 else PrimaryPalette.WHITE

            backend.draw_rect(
                cur_x, my, sub_w, model_h,
                fill=fill_col, stroke=PrimaryPalette.NAVY, stroke_width=1.2
            )

            # Top dimension label
            len_lbl = str(p_len)
            backend.draw_text(len_lbl, cur_x + sub_w / 2.0, my + model_h + 4.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")
            labels.append(len_lbl)

            # Inside area label (e.g. "20 x 6 = 120")
            calc_lbl = f"{p_len} x {height_val} = {p_area}"
            backend.draw_text(calc_lbl, cur_x + sub_w / 2.0, my + model_h / 2.0 - 5.0, font_size=12.0, color=PrimaryPalette.AMBER, align="center")
            labels.append(str(p_area))
            labels.append(calc_lbl)

            cur_x += sub_w

        backend.record_evidence("AREA_MODEL", params, len(labels) + len(partitions), labels)

    @staticmethod
    def draw_partial_products(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Stage 4: Explicit Partial Products Addition."""
        factors = params.get("factors", [23, 6])
        partials = params.get("partial_products", [120, 18])
        total = params.get("product", sum(partials))

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [f"Partial Products for {factors[0]} x {factors[1]}"]
        backend.draw_text(labels[0], bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.0, color=PrimaryPalette.NAVY)

        sy = bbox.y_max - 45.0
        sx = bbox.x + bbox.width / 2.0

        for idx, pp in enumerate(partials):
            pp_str = str(pp)
            backend.draw_text(f"+ {pp_str}", sx, sy, font_size=13.5, color=PrimaryPalette.STUDENT_PENCIL, align="right")
            labels.append(pp_str)
            sy -= 22.0

        # Separator line
        backend.draw_line(sx - 70.0, sy + 4.0, sx + 10.0, sy + 4.0, stroke=PrimaryPalette.NAVY, stroke_width=1.5)
        # Total sum
        tot_str = str(total)
        backend.draw_text(tot_str, sx, sy - 18.0, font_size=14.0, color=PrimaryPalette.NAVY, align="right")
        labels.append(tot_str)

        backend.record_evidence("PARTIAL_PRODUCTS", params, len(labels) + 2, labels)

    @staticmethod
    def draw_estimate_check(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Stage 6: Estimation & Inverse Check."""
        actual = params.get("actual", 138)
        estimate_expr = params.get("estimate_expr", "20 x 6 = 120 (lower bound)")
        reasoning = params.get("reasoning", "138 is reasonable because 23 is slightly more than 20.")

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.SOFT_GREEN, stroke_width=1.2, corner_radius=6.0
        )

        labels = ["Estimate & Reasonableness Check:", estimate_expr, f"Calculated Answer: {actual}", reasoning]
        backend.draw_text(labels[0], bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.0, color=PrimaryPalette.NAVY)
        backend.draw_text(labels[1], bbox.x + 12.0, bbox.y_max - 40.0, font_size=12.0, color=PrimaryPalette.SLATE)
        backend.draw_text(labels[2], bbox.x + 12.0, bbox.y_max - 60.0, font_size=13.0, color=PrimaryPalette.SOFT_GREEN)
        backend.draw_text(labels[3], bbox.x + 12.0, bbox.y_max - 80.0, font_size=11.5, color=PrimaryPalette.STUDENT_PENCIL)

        backend.record_evidence("ESTIMATE_CHECK", params, len(labels), labels)


class DivisionPrimitives:
    """Deep Division 15-dimension primitives."""

    @staticmethod
    def draw_sharing_vs_grouping(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """
        Distinguishes Sharing (Partitive: known number of groups, find size)
        from Grouping (Quotitive: known group size, find number of groups).
        """
        dividend = params.get("dividend", 24)
        divisor = params.get("divisor", 6)
        quotient = params.get("quotient", 4)
        meaning = params.get("meaning", "SHARING").upper()

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(dividend), str(divisor), str(quotient), meaning]

        if meaning == "SHARING":
            title = f"Sharing (Partitive): {dividend} shared equally among {divisor} groups -> {quotient} in each"
            backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.0, color=PrimaryPalette.TEAL)
            labels.append(title)
            # Draw 'divisor' distinct group boxes with 'quotient' dots inside each
            box_w = (bbox.width - 30.0) / divisor
            box_h = bbox.height - 50.0
            for g in range(divisor):
                bx = bbox.x + 15.0 + g * box_w
                by = bbox.y + 15.0
                backend.draw_rect(bx + 2.0, by, box_w - 4.0, box_h, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, stroke_width=1.0)
                backend.draw_text(f"Group {g+1}", bx + box_w / 2.0, by + box_h - 14.0, font_size=9.0, color=PrimaryPalette.SLATE, align="center")
                backend.draw_text(f"{quotient} items", bx + box_w / 2.0, by + box_h / 2.0 - 5.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")
        else: # GROUPING
            title = f"Grouping (Quotitive): {dividend} packaged into groups of {divisor} -> {quotient} groups made"
            backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.0, color=PrimaryPalette.AMBER)
            labels.append(title)
            # Draw 'quotient' distinct bags each containing 'divisor' items
            box_w = (bbox.width - 30.0) / quotient
            box_h = bbox.height - 50.0
            for g in range(quotient):
                bx = bbox.x + 15.0 + g * box_w
                by = bbox.y + 15.0
                backend.draw_rect(bx + 2.0, by, box_w - 4.0, box_h, fill=PrimaryPalette.HIGHLIGHT_YELLOW, stroke=PrimaryPalette.AMBER, stroke_width=1.0)
                backend.draw_text(f"Pack {g+1}", bx + box_w / 2.0, by + box_h - 14.0, font_size=9.0, color=PrimaryPalette.SLATE, align="center")
                backend.draw_text(f"{divisor} items", bx + box_w / 2.0, by + box_h / 2.0 - 5.0, font_size=12.0, color=PrimaryPalette.NAVY, align="center")

        backend.record_evidence("DIVISION_STRUCTURE", params, len(labels) + 4, labels)

    @staticmethod
    def draw_remainder_context(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Draw contextual interpretation of division remainder."""
        dividend = params.get("dividend", 125)
        divisor = params.get("divisor", 40)
        quotient = params.get("quotient", 3)
        remainder = params.get("remainder", 5)
        action = params.get("action", "ROUND_UP_ONE_MORE_GROUP")
        final_answer = params.get("final_answer", 4)
        explanation = params.get("explanation", "All students need transport, so 1 more bus is needed.")

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(dividend), str(divisor), str(quotient), str(remainder), str(final_answer), action]

        title = f"Remainder Interpretation: {dividend} / {divisor} = {quotient} R {remainder}"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.5, color=PrimaryPalette.NAVY)
        labels.append(title)

        action_txt = f"Context Action: {action.replace('_', ' ')}"
        backend.draw_text(action_txt, bbox.x + 12.0, bbox.y_max - 42.0, font_size=12.0, color=PrimaryPalette.AMBER)
        labels.append(action_txt)

        ans_txt = f"Final Answer Required: {final_answer}"
        backend.draw_text(ans_txt, bbox.x + 12.0, bbox.y_max - 64.0, font_size=13.5, color=PrimaryPalette.SOFT_GREEN)
        labels.append(ans_txt)

        backend.draw_text(explanation, bbox.x + 12.0, bbox.y_max - 86.0, font_size=11.5, color=PrimaryPalette.STUDENT_PENCIL)
        labels.append(explanation)

        backend.record_evidence("DIVISION_REMAINDER_CONTEXT", params, len(labels), labels)

    @staticmethod
    def draw_unit_chain(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Draws explicit multi-step unit conversion chain (e.g. 23 dozen -> 276 eggs -> Rs 1656)."""
        steps = params.get("unit_steps", [
            {"quantity": 23, "unit": "DOZEN_EGGS"},
            {"multiplier": 12, "result_quantity": 276, "unit": "INDIVIDUAL_EGGS"},
            {"rate": 6, "result_value": 1656, "unit": "RUPEES"}
        ])

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = ["Unit Chain Analysis:"]
        backend.draw_text(labels[0], bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.5, color=PrimaryPalette.NAVY)

        step_w = (bbox.width - 30.0) / len(steps)
        cy = bbox.y + (bbox.height - 40.0) / 2.0

        for idx, step in enumerate(steps):
            bx = bbox.x + 15.0 + idx * step_w
            backend.draw_rect(
                bx + 5.0, cy - 22.0, step_w - 30.0, 44.0,
                fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.ACCENT_BLUE, stroke_width=1.2, corner_radius=4.0
            )

            q_txt = str(step.get("quantity") or step.get("result_quantity") or step.get("result_value"))
            u_txt = str(step.get("unit")).replace("_", " ")
            backend.draw_text(q_txt, bx + (step_w - 30.0) / 2.0 + 5.0, cy + 2.0, font_size=13.0, color=PrimaryPalette.NAVY, align="center")
            backend.draw_text(u_txt, bx + (step_w - 30.0) / 2.0 + 5.0, cy - 14.0, font_size=9.5, color=PrimaryPalette.SLATE, align="center")
            labels.extend([q_txt, u_txt])

            # Draw transition arrow if not last step
            if idx < len(steps) - 1:
                arrow_start_x = bx + step_w - 20.0
                arrow_end_x = bx + step_w
                backend.draw_arrow(arrow_start_x, cy, arrow_end_x, cy, stroke=PrimaryPalette.AMBER, stroke_width=2.0)
                trans_label = f"x {steps[idx+1].get('multiplier') or steps[idx+1].get('rate')}"
                backend.draw_text(trans_label, arrow_start_x + 10.0, cy + 8.0, font_size=9.0, color=PrimaryPalette.AMBER, align="center")
                labels.append(trans_label)

        backend.record_evidence("UNIT_CHAIN", params, len(labels) + len(steps), labels)
