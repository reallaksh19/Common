"""Intrinsic-measurement layout for Grade 4 staged visual hints.

This component fixes a class of learner-page failures rather than one page:

* H1/H2/H3 cards are measured before drawing;
* compact support may use a three-column row;
* dense support uses H1 full-width above H2/H3 side by side when readable;
* narrow or very dense support stacks vertically;
* all text stays inside its own measured card;
* thinking-path chips wrap as a 4-up row or 2x2 grid instead of loose arrows;
* visual primitives are rendered only inside their allocated visual boxes.

The component never shrinks learner text to force a fit. Callers paginate when
the measured unit does not fit the remaining page space.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from Grade4.V2.Mathematics.Publication.engine.layout_measure import paragraph_height
from Grade4.V2.Mathematics.Representation.engine.base import BoundingBox, PrimaryPalette, VectorRenderBackend
from Grade4.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive


class StagedHintLayoutError(ValueError):
    pass


def _require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise StagedHintLayoutError(f"{code}: {detail}")


@dataclass(frozen=True)
class StagePlacement:
    level: str
    card: BoundingBox
    visual: BoundingBox
    cue_top: float
    action_top: float


@dataclass(frozen=True)
class SupportLayoutPlan:
    mode: str
    height: float
    stages: tuple[StagePlacement, ...]
    path_boxes: tuple[BoundingBox, ...]


class StagedHintComponent:
    """Measure and draw H1/H2/H3 + optional thinking path as one atomic unit."""

    GAP = 10.0
    CARD_PAD = 10.0
    LABEL_H = 18.0
    VISUAL_H = 72.0
    CUE_FONT = 10.5
    CUE_LINE = 14.0
    ACTION_FONT = 10.0
    ACTION_LINE = 13.0
    MIN_COLUMN_W = 148.0
    MAX_ROW_CARD_H = 192.0
    MAX_ROW_COPY_CHARS = 76
    MIN_TWO_COL_W = 210.0
    MAX_TWO_COL_CARD_H = 220.0
    PATH_GAP = 8.0
    PATH_MIN_W = 104.0
    PATH_PAD = 8.0
    PATH_FONT = 9.5
    PATH_LINE = 12.0

    STAGE_ACCENTS = (PrimaryPalette.TEAL, PrimaryPalette.SOFT_GREEN, PrimaryPalette.ACCENT_BLUE)

    @classmethod
    def _stage_height(cls, stage: Mapping[str, Any], width: float) -> float:
        inner = max(width - 2 * cls.CARD_PAD, 40.0)
        cue = str(stage.get("verbal_cue") or "")
        action = str(stage.get("learner_action") or "")
        cue_h = paragraph_height(cue, inner, font_size=cls.CUE_FONT, line_height=cls.CUE_LINE) if cue else 0.0
        action_h = paragraph_height(action, inner, font_size=cls.ACTION_FONT, line_height=cls.ACTION_LINE) if action else 0.0
        text_gap = 6.0 if cue and action else 0.0
        return cls.CARD_PAD + cls.LABEL_H + 6.0 + cls.VISUAL_H + 8.0 + cue_h + text_gap + action_h + cls.CARD_PAD

    @classmethod
    def _placement(cls, stage: Mapping[str, Any], level: str, x: float, top_y: float, width: float, height: float) -> StagePlacement:
        sy = top_y - height
        visual_y = top_y - cls.CARD_PAD - cls.LABEL_H - 6.0 - cls.VISUAL_H
        visual = BoundingBox(x + cls.CARD_PAD, visual_y, width - 2 * cls.CARD_PAD, cls.VISUAL_H)
        cue_top = visual_y - 8.0
        cue = str(stage.get("verbal_cue") or "")
        cue_h = paragraph_height(cue, visual.width, font_size=cls.CUE_FONT, line_height=cls.CUE_LINE) if cue else 0.0
        action_top = cue_top - cue_h - (6.0 if cue and str(stage.get("learner_action") or "") else 0.0)
        return StagePlacement(level, BoundingBox(x, sy, width, height), visual, cue_top, action_top)

    @classmethod
    def _path_box_height(cls, step: Mapping[str, Any], width: float) -> float:
        inner = max(width - 2 * cls.PATH_PAD, 30.0)
        label = str(step.get("child_label") or "")
        action = str(step.get("one_line_action") or "")
        text = f"{label}: {action}" if label else action
        return max(34.0, cls.PATH_PAD * 2 + paragraph_height(text, inner, font_size=cls.PATH_FONT, line_height=cls.PATH_LINE))

    @classmethod
    def _row_is_readable(cls, stages: Sequence[Mapping[str, Any]], width: float) -> bool:
        card_w = (width - 2 * cls.GAP) / 3.0
        if card_w < cls.MIN_COLUMN_W:
            return False
        if max(cls._stage_height(stage, card_w) for stage in stages) > cls.MAX_ROW_CARD_H:
            return False
        return all(
            len(str(stage.get("verbal_cue") or "")) + len(str(stage.get("learner_action") or "")) <= cls.MAX_ROW_COPY_CHARS
            for stage in stages
        )

    @classmethod
    def _two_row_is_readable(cls, stages: Sequence[Mapping[str, Any]], width: float) -> bool:
        half = (width - cls.GAP) / 2.0
        if half < cls.MIN_TWO_COL_W:
            return False
        return max(cls._stage_height(stages[1], half), cls._stage_height(stages[2], half)) <= cls.MAX_TWO_COL_CARD_H

    @classmethod
    def plan(
        cls,
        stages: Sequence[Mapping[str, Any]],
        *,
        x: float,
        top_y: float,
        width: float,
        thinking_path: Sequence[Mapping[str, Any]] = (),
    ) -> SupportLayoutPlan:
        _require(len(stages) == 3, "STAGED_HINT_EXACTLY_THREE_REQUIRED", str(len(stages)))
        _require(width > 0, "STAGED_HINT_WIDTH_INVALID", str(width))
        stage_boxes: list[StagePlacement] = []

        if cls._row_is_readable(stages, width):
            card_w = (width - 2 * cls.GAP) / 3.0
            row_h = max(cls._stage_height(stage, card_w) for stage in stages)
            for i, stage in enumerate(stages):
                sx = x + i * (card_w + cls.GAP)
                stage_boxes.append(cls._placement(stage, str(stage.get("level") or f"H{i+1}"), sx, top_y, card_w, row_h))
            used_h = row_h
            mode = "ROW"
        elif cls._two_row_is_readable(stages, width):
            h1 = cls._stage_height(stages[0], width)
            stage_boxes.append(cls._placement(stages[0], str(stages[0].get("level") or "H1"), x, top_y, width, h1))
            second_top = top_y - h1 - cls.GAP
            half = (width - cls.GAP) / 2.0
            lower_h = max(cls._stage_height(stages[1], half), cls._stage_height(stages[2], half))
            stage_boxes.append(cls._placement(stages[1], str(stages[1].get("level") or "H2"), x, second_top, half, lower_h))
            stage_boxes.append(cls._placement(stages[2], str(stages[2].get("level") or "H3"), x + half + cls.GAP, second_top, half, lower_h))
            used_h = h1 + cls.GAP + lower_h
            mode = "H1_TOP_H2H3_ROW"
        else:
            cur_top = top_y
            used_h = 0.0
            for i, stage in enumerate(stages):
                h = cls._stage_height(stage, width)
                stage_boxes.append(cls._placement(stage, str(stage.get("level") or f"H{i+1}"), x, cur_top, width, h))
                cur_top -= h + cls.GAP
                used_h += h + (cls.GAP if i < len(stages) - 1 else 0.0)
            mode = "STACK"

        path_boxes: list[BoundingBox] = []
        if thinking_path:
            path_top = top_y - used_h - 12.0
            n = len(thinking_path)
            cols = 4 if n <= 4 and (width - 3 * cls.PATH_GAP) / 4.0 >= cls.PATH_MIN_W else 2
            box_w = (width - (cols - 1) * cls.PATH_GAP) / cols
            rows = (n + cols - 1) // cols
            row_heights: list[float] = []
            for row in range(rows):
                row_steps = thinking_path[row * cols:(row + 1) * cols]
                row_heights.append(max(cls._path_box_height(step, box_w) for step in row_steps))
            cur_top = path_top
            for row in range(rows):
                rh = row_heights[row]
                for col, _step in enumerate(thinking_path[row * cols:(row + 1) * cols]):
                    bx = x + col * (box_w + cls.PATH_GAP)
                    path_boxes.append(BoundingBox(bx, cur_top - rh, box_w, rh))
                cur_top -= rh + (cls.PATH_GAP if row < rows - 1 else 0.0)
            used_h += 12.0 + sum(row_heights) + cls.PATH_GAP * max(rows - 1, 0)

        result = SupportLayoutPlan(mode=mode, height=used_h, stages=tuple(stage_boxes), path_boxes=tuple(path_boxes))
        cls.assert_plan(result, x=x, top_y=top_y, width=width)
        return result

    @staticmethod
    def _overlap(a: BoundingBox, b: BoundingBox) -> bool:
        return not (a.x_max <= b.x or b.x_max <= a.x or a.y_max <= b.y or b.y_max <= a.y)

    @classmethod
    def assert_plan(cls, plan: SupportLayoutPlan, *, x: float, top_y: float, width: float) -> None:
        left, right = x, x + width
        bottom = top_y - plan.height
        boxes = [p.card for p in plan.stages] + list(plan.path_boxes)
        for box in boxes:
            _require(box.x >= left - 0.01 and box.x_max <= right + 0.01, "STAGED_HINT_LAYOUT_HORIZONTAL_OVERFLOW", repr(box))
            _require(box.y >= bottom - 0.01 and box.y_max <= top_y + 0.01, "STAGED_HINT_LAYOUT_VERTICAL_OVERFLOW", repr(box))
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                _require(not cls._overlap(a, b), "STAGED_HINT_LAYOUT_COLLISION", f"{a} vs {b}")

    @classmethod
    def measure(cls, stages: Sequence[Mapping[str, Any]], width: float, thinking_path: Sequence[Mapping[str, Any]] = ()) -> float:
        return cls.plan(stages, x=0.0, top_y=10000.0, width=width, thinking_path=thinking_path).height

    @classmethod
    def render(
        cls,
        backend: VectorRenderBackend,
        stages: Sequence[Mapping[str, Any]],
        *,
        x: float,
        top_y: float,
        width: float,
        thinking_path: Sequence[Mapping[str, Any]] = (),
    ) -> dict[str, Any]:
        plan = cls.plan(stages, x=x, top_y=top_y, width=width, thinking_path=thinking_path)
        for i, (stage, placement) in enumerate(zip(stages, plan.stages)):
            accent = cls.STAGE_ACCENTS[min(i, len(cls.STAGE_ACCENTS) - 1)]
            backend.draw_rect(placement.card.x, placement.card.y, placement.card.width, placement.card.height, fill=PrimaryPalette.WHITE, stroke=accent, corner_radius=6.0)
            label = str(stage.get("child_label") or stage.get("level") or f"H{i+1}")
            backend.draw_text(f"{stage.get('level', f'H{i+1}')}  {label}", placement.card.x + cls.CARD_PAD, placement.card.y_max - cls.CARD_PAD - 10.0, font_size=9.5, color=accent)
            primitive_kind = str(stage.get("primitive_kind") or "")
            params = stage.get("semantic_params")
            _require(bool(primitive_kind), "STAGED_HINT_PRIMITIVE_MISSING", placement.level)
            _require(isinstance(params, Mapping), "STAGED_HINT_PARAMS_MISSING", placement.level)
            render_primitive(primitive_kind, dict(params), backend, placement.visual)
            cue = str(stage.get("verbal_cue") or "")
            action = str(stage.get("learner_action") or "")
            if cue:
                backend.draw_paragraph(cue, placement.card.x + cls.CARD_PAD, placement.cue_top, width=placement.card.width - 2 * cls.CARD_PAD, font_size=cls.CUE_FONT, color=PrimaryPalette.NAVY, line_height=cls.CUE_LINE)
            if action:
                backend.draw_paragraph(action, placement.card.x + cls.CARD_PAD, placement.action_top, width=placement.card.width - 2 * cls.CARD_PAD, font_size=cls.ACTION_FONT, color=PrimaryPalette.SLATE, line_height=cls.ACTION_LINE)

        if thinking_path:
            for i, (step, box) in enumerate(zip(thinking_path, plan.path_boxes), start=1):
                accent = cls.STAGE_ACCENTS[(i - 1) % len(cls.STAGE_ACCENTS)]
                backend.draw_rect(box.x, box.y, box.width, box.height, fill=PrimaryPalette.LIGHT_BG, stroke=accent, corner_radius=6.0)
                backend.draw_circle(box.x + 14.0, box.y + box.height / 2.0, 8.0, fill=accent, stroke=accent)
                backend.draw_text(str(i), box.x + 14.0, box.y + box.height / 2.0 - 3.0, font_size=8.0, color=PrimaryPalette.WHITE, align="center")
                text = f"{step.get('child_label', '')}: {step.get('one_line_action', '')}".strip(": ")
                backend.draw_paragraph(text, box.x + 27.0, box.y_max - cls.PATH_PAD - 4.0, width=box.width - 34.0, font_size=cls.PATH_FONT, color=PrimaryPalette.NAVY, line_height=cls.PATH_LINE)

        return {
            "mode": plan.mode,
            "height": plan.height,
            "stage_boxes": [p.card for p in plan.stages],
            "path_boxes": list(plan.path_boxes),
        }
