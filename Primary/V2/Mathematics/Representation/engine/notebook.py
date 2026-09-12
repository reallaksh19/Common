"""
Authentic Notebook Engine for Primary Mathematics V2.
Preserves 4-tier work provenance, column alignment, borrow/carry markings,
long division brackets with internal quotient-zero slots, and teacher/student provenance.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend
)


class ProvenanceTier(str, Enum):
    ORIGINAL_SOURCE_IMAGE = "ORIGINAL_SOURCE_IMAGE"
    FAITHFUL_TRANSCRIPTION = "FAITHFUL_TRANSCRIPTION"
    STRUCTURED_REPLAY = "STRUCTURED_REPLAY"
    AUTHORED_NOTEBOOK_EXAMPLE = "AUTHORED_NOTEBOOK_EXAMPLE"


LEARNER_PROVENANCE_LABEL = {
    ProvenanceTier.ORIGINAL_SOURCE_IMAGE: "Original learner work",
    ProvenanceTier.FAITHFUL_TRANSCRIPTION: "Faithful transcription",
    ProvenanceTier.STRUCTURED_REPLAY: "Replay of learner work",
    ProvenanceTier.AUTHORED_NOTEBOOK_EXAMPLE: "Worked example",
}


@dataclass
class NotebookStep:
    step_number: int
    text: str
    is_ambiguous: bool = False
    self_corrected: bool = False
    teacher_annotation: Optional[str] = None
    is_correct: bool = True


@dataclass
class LongDivisionWorkoutSpec:
    dividend: int
    divisor: int
    quotient: int
    remainder: int
    quotient_digits: List[str]
    steps: List[Dict[str, Any]]
    multiples_table: Optional[List[int]] = None
    provenance_tier: ProvenanceTier = ProvenanceTier.STRUCTURED_REPLAY
    actor: str = "CHILD"
    claims_original_handwriting: bool = False
    notes: Optional[str] = None


class AuthenticNotebookEngine:
    """Renders authentic student notebook workouts and pedagogical exemplars."""

    def __init__(self, backend: VectorRenderBackend) -> None:
        self.backend = backend

    def render_notebook_grid(self, bbox: BoundingBox, grid_size: float = 24.0) -> None:
        """Draw a light, authentic notebook squared ruling."""
        self.backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, stroke_width=1.0, corner_radius=4.0
        )
        curr_x = bbox.x + grid_size
        while curr_x < bbox.x_max:
            self.backend.draw_line(curr_x, bbox.y, curr_x, bbox.y_max, stroke=PrimaryPalette.GRID_LINE, stroke_width=0.5)
            curr_x += grid_size
        curr_y = bbox.y + grid_size
        while curr_y < bbox.y_max:
            self.backend.draw_line(bbox.x, curr_y, bbox.x_max, curr_y, stroke=PrimaryPalette.GRID_LINE, stroke_width=0.5)
            curr_y += grid_size

    def render_vertical_multiplication(
        self,
        bbox: BoundingBox,
        factors: List[int],
        carry_rows: List[List[Tuple[int, int]]],
        partial_products: List[int],
        total_product: int,
        tier: ProvenanceTier = ProvenanceTier.STRUCTURED_REPLAY
    ) -> Dict[str, Any]:
        """Render aligned vertical multiplication."""
        self.render_notebook_grid(bbox)
        col_width = 24.0
        row_height = 24.0
        origin_x = bbox.x + bbox.width - 40.0
        origin_y = bbox.y_max - 30.0
        labels: List[str] = []

        f1_str = str(factors[0])
        labels.append(f1_str)
        for i, char in enumerate(reversed(f1_str)):
            self.backend.draw_text(char, origin_x - i * col_width, origin_y, font_size=14.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")

        origin_y -= row_height
        f2_str = str(factors[1])
        labels.append(f2_str)
        for i, char in enumerate(reversed(f2_str)):
            self.backend.draw_text(char, origin_x - i * col_width, origin_y, font_size=14.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")
        sym_x = origin_x - (max(len(f1_str), len(f2_str)) * col_width)
        self.backend.draw_text("x", sym_x, origin_y, font_size=14.0, color=PrimaryPalette.NAVY, align="center")
        labels.append("x")

        origin_y -= 8.0
        line_left = sym_x - 12.0
        self.backend.draw_line(line_left, origin_y, origin_x + 12.0, origin_y, stroke=PrimaryPalette.NAVY, stroke_width=1.5)

        for pp in partial_products:
            origin_y -= (row_height - 4.0)
            pp_str = str(pp)
            labels.append(pp_str)
            for i, char in enumerate(reversed(pp_str)):
                self.backend.draw_text(char, origin_x - i * col_width, origin_y, font_size=14.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")

        origin_y -= 8.0
        self.backend.draw_line(line_left, origin_y, origin_x + 12.0, origin_y, stroke=PrimaryPalette.NAVY, stroke_width=1.5)
        origin_y -= (row_height - 4.0)
        tot_str = str(total_product)
        labels.append(tot_str)
        for i, char in enumerate(reversed(tot_str)):
            self.backend.draw_text(char, origin_x - i * col_width, origin_y, font_size=14.0, color=PrimaryPalette.NAVY, align="center")

        # Keep exact provenance in machine evidence, but show a learner-safe label.
        learner_badge = LEARNER_PROVENANCE_LABEL[tier]
        self.backend.draw_text(learner_badge, bbox.x + 8.0, bbox.y + 8.0, font_size=9.0, color=PrimaryPalette.SLATE)
        labels.append(learner_badge)

        self.backend.record_evidence(
            kind="VERTICAL_MULTIPLICATION",
            params={"factors": factors, "partial_products": partial_products, "total": total_product, "tier": tier.value},
            element_count=len(labels) + 2,
            labels=labels
        )
        return {"tier": tier.value, "labels": labels, "col_aligned": True}

    def render_long_division_bracket(self, bbox: BoundingBox, spec: LongDivisionWorkoutSpec) -> Dict[str, Any]:
        """Render long division with strict place-value alignment and quotient-zero preservation."""
        self.render_notebook_grid(bbox)
        col_width = 22.0
        row_height = 22.0
        labels: List[str] = []

        table_width = 0.0
        if spec.multiples_table:
            table_x = bbox.x + 12.0
            table_y = bbox.y_max - 28.0
            self.backend.draw_text("Multiples of " + str(spec.divisor) + ":", table_x, table_y, font_size=11.0, color=PrimaryPalette.TEAL)
            labels.append(str(spec.divisor))
            for idx, m_val in enumerate(spec.multiples_table):
                table_y -= 18.0
                if table_y < bbox.y + 20:
                    break
                m_txt = f"{idx + 1} x {spec.divisor} = {m_val}"
                self.backend.draw_text(m_txt, table_x, table_y, font_size=10.0, color=PrimaryPalette.STUDENT_PENCIL)
                labels.append(str(m_val))
            table_width = 110.0

        division_origin_x = bbox.x + table_width + 45.0
        divisor_str = str(spec.divisor)
        dividend_str = str(spec.dividend)
        labels.extend([divisor_str, dividend_str])
        start_y = bbox.y_max - 40.0

        self.backend.draw_text(divisor_str, division_origin_x - 10.0, start_y, font_size=14.0, color=PrimaryPalette.NAVY, align="right")
        bracket_x = division_origin_x - 4.0
        dividend_width = len(dividend_str) * col_width + 12.0
        self.backend.draw_line(bracket_x, start_y - 4.0, bracket_x, start_y + 16.0, stroke=PrimaryPalette.NAVY, stroke_width=1.5)
        self.backend.draw_line(bracket_x, start_y + 16.0, bracket_x + dividend_width, start_y + 16.0, stroke=PrimaryPalette.NAVY, stroke_width=1.5)

        for idx, char in enumerate(dividend_str):
            cx = division_origin_x + idx * col_width + 8.0
            self.backend.draw_text(char, cx, start_y, font_size=14.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")

        quotient_y = start_y + 20.0
        offset = len(dividend_str) - len(spec.quotient_digits)
        for idx, q_digit_raw in enumerate(spec.quotient_digits):
            q_digit = str(q_digit_raw)
            target_col = offset + idx
            cx = division_origin_x + target_col * col_width + 8.0
            color = PrimaryPalette.AMBER if (q_digit == "0" and 0 < idx < len(spec.quotient_digits) - 1) else PrimaryPalette.NAVY
            self.backend.draw_text(q_digit, cx, quotient_y, font_size=14.0, color=color, align="center")
            labels.append(q_digit)

        current_y = start_y
        for step in spec.steps:
            current_y -= row_height
            if current_y < bbox.y + 25.0:
                break
            step_type = step.get("type", "SUBTRACTION")
            val_str = str(step.get("value", ""))
            col_pos = step.get("col", 0)
            cx = division_origin_x + col_pos * col_width + 8.0
            if step_type == "SUBTRACTION":
                self.backend.draw_text("-" + val_str, cx, current_y, font_size=13.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")
                labels.append(val_str)
                self.backend.draw_line(cx - (len(val_str) * col_width / 2.0) - 10.0, current_y - 2.0, cx + (col_width / 2.0) + 4.0, current_y - 2.0, stroke=PrimaryPalette.SLATE, stroke_width=1.0)
            elif step_type == "BRING_DOWN":
                self.backend.draw_text(val_str, cx, current_y, font_size=13.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")
                labels.append(val_str)
            elif step_type == "REMAINDER":
                rem_txt = f"R {val_str}"
                self.backend.draw_text(rem_txt, cx + 16.0, current_y, font_size=13.0, color=PrimaryPalette.TEAL, align="center")
                labels.append(rem_txt)

        learner_badge = LEARNER_PROVENANCE_LABEL[spec.provenance_tier]
        if spec.provenance_tier == ProvenanceTier.STRUCTURED_REPLAY and spec.actor == "CHILD":
            learner_badge = "Replay of learner work"
        self.backend.draw_text(learner_badge, bbox.x + 8.0, bbox.y + 8.0, font_size=9.0, color=PrimaryPalette.SLATE)
        labels.append(learner_badge)

        self.backend.record_evidence(
            kind="LONG_DIVISION_WORKOUT",
            params={
                "dividend": spec.dividend,
                "divisor": spec.divisor,
                "quotient": spec.quotient,
                "remainder": spec.remainder,
                "quotient_digits": spec.quotient_digits,
                "tier": spec.provenance_tier.value,
                "actor": spec.actor
            },
            element_count=len(labels) + 5,
            labels=labels
        )

        digit_strings = [str(x) for x in spec.quotient_digits]
        return {
            "dividend": spec.dividend,
            "divisor": spec.divisor,
            "quotient": spec.quotient,
            "remainder": spec.remainder,
            "internal_zero_preserved": ("0" in digit_strings[1:-1] if len(digit_strings) > 2 else (digit_strings[-1:] == ["0"])),
            "labels": labels
        }
