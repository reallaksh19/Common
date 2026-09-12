"""Measured publication components for LearningRepresentationPlan support.

Components own local layout only. They receive bounded rectangles, reserve separate
visual/text lanes, and return placement evidence. They never choose pedagogy.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping

from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PageMetricsA4,
    PrimaryPalette,
    VectorRenderBackend,
)
from Primary.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive


@dataclass(frozen=True)
class ComponentPlacement:
    kind: str
    ref: str
    bbox: BoundingBox
    font_min_used: float | None = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "ref": self.ref,
            "bbox": {"x": self.bbox.x, "y": self.bbox.y, "width": self.bbox.width, "height": self.bbox.height},
            "font_min_used": self.font_min_used,
        }


def _line_count(text: str, width: float, font_size: float) -> int:
    if not text:
        return 0
    char_width = max(font_size * 0.55, 1.0)
    chars_per_line = max(int(width / char_width), 1)
    return max(1, int(math.ceil(len(str(text)) / chars_per_line)))


def _contains(parent: BoundingBox, child: BoundingBox) -> bool:
    return (
        child.x >= parent.x
        and child.y >= parent.y
        and child.x_max <= parent.x_max
        and child.y_max <= parent.y_max
    )


class HintCardComponent:
    HEADER_H = 26.0
    PAD = 10.0
    GAP = 10.0
    VISUAL_RATIO = 0.36
    BODY_FONT = 12.0
    LINE_H = 15.0
    MIN_VISUAL_H = 72.0

    @classmethod
    def measure(cls, card: Mapping[str, Any], width: float) -> float:
        inner_w = max(width - 2 * cls.PAD, 1.0)
        visual_w = inner_w * cls.VISUAL_RATIO
        text_w = inner_w - visual_w - cls.GAP
        text = " ".join(filter(None, [str(card.get("verbal_cue", "")), str(card.get("learner_action", ""))]))
        text_h = _line_count(text, text_w, cls.BODY_FONT) * cls.LINE_H + 10.0
        content_h = max(cls.MIN_VISUAL_H, text_h)
        return cls.HEADER_H + cls.PAD + content_h + cls.PAD

    @classmethod
    def render(
        cls,
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        card: Mapping[str, Any],
    ) -> List[ComponentPlacement]:
        required = cls.measure(card, bbox.width)
        if bbox.height + 0.001 < required:
            raise ValueError(f"HINT_CARD_BBOX_TOO_SMALL: need {required:.1f}, got {bbox.height:.1f}")

        backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill="#FFF9EA", stroke="#E4B250", corner_radius=6.0)
        label = str(card["child_label"])
        level = str(card["level"])
        backend.draw_text(f"{level}  {label}", bbox.x + cls.PAD, bbox.y_max - 18.0, font_size=12.0, color=PrimaryPalette.NAVY)

        content_y = bbox.y + cls.PAD
        content_h = bbox.height - cls.HEADER_H - 2 * cls.PAD
        inner_w = bbox.width - 2 * cls.PAD
        visual_w = inner_w * cls.VISUAL_RATIO
        text_w = inner_w - visual_w - cls.GAP
        visual_bbox = BoundingBox(bbox.x + cls.PAD, content_y, visual_w, content_h)
        text_bbox = BoundingBox(visual_bbox.x_max + cls.GAP, content_y, text_w, content_h)

        if not _contains(bbox, visual_bbox) or not _contains(bbox, text_bbox):
            raise ValueError("NESTED_VISUAL_ESCAPE: hint-card child slot is outside parent bbox")
        if visual_bbox.x_max > text_bbox.x:
            raise ValueError("TEXT_AND_VISUAL_SHARE_UNMEASURED_SLOT: visual/text lanes overlap")

        call = card["primitive_call"]
        render_primitive(call["kind"], dict(call.get("params") or {}), backend, visual_bbox)
        cue = str(card.get("verbal_cue", ""))
        action = str(card.get("learner_action", ""))
        text_top = text_bbox.y_max - 14.0
        used = backend.draw_paragraph(cue, text_bbox.x, text_top, width=text_bbox.width, font_size=cls.BODY_FONT, color=PrimaryPalette.NAVY, line_height=cls.LINE_H)
        action_y = text_top - max(used, cls.LINE_H) - 8.0
        backend.draw_paragraph(action, text_bbox.x, action_y, width=text_bbox.width, font_size=cls.BODY_FONT, color=PrimaryPalette.STUDENT_PENCIL, line_height=cls.LINE_H)

        return [
            ComponentPlacement("HINT_CARD", f"{level}:{label}", bbox, cls.BODY_FONT),
            ComponentPlacement("HINT_VISUAL", str(card.get("visual_state_id", level)), visual_bbox, None),
            ComponentPlacement("HINT_TEXT", level, text_bbox, cls.BODY_FONT),
        ]


class HintLadderComponent:
    GAP = 10.0

    @classmethod
    def measure(cls, cards: List[Mapping[str, Any]], width: float) -> float:
        return sum(HintCardComponent.measure(card, width) for card in cards) + cls.GAP * max(len(cards) - 1, 0)

    @classmethod
    def render(
        cls,
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        cards: List[Mapping[str, Any]],
    ) -> List[ComponentPlacement]:
        required = cls.measure(cards, bbox.width)
        if bbox.height + 0.001 < required:
            raise ValueError(f"HINT_LADDER_BBOX_TOO_SMALL: need {required:.1f}, got {bbox.height:.1f}")
        placements: List[ComponentPlacement] = []
        cursor_top = bbox.y_max
        for idx, card in enumerate(cards):
            card_h = HintCardComponent.measure(card, bbox.width)
            card_box = BoundingBox(bbox.x, cursor_top - card_h, bbox.width, card_h)
            placements.extend(HintCardComponent.render(backend, card_box, card))
            cursor_top = card_box.y - (cls.GAP if idx < len(cards) - 1 else 0.0)
        return placements


class ThinkingPathComponent:
    GAP = 8.0
    CARD_H = 126.0
    BODY_FONT = 12.0

    @classmethod
    def measure(cls, steps: List[Mapping[str, Any]], width: float) -> float:
        if not steps:
            return 0.0
        return cls.CARD_H

    @classmethod
    def render(
        cls,
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        steps: List[Mapping[str, Any]],
    ) -> List[ComponentPlacement]:
        if not steps:
            return []
        if bbox.height + 0.001 < cls.CARD_H:
            raise ValueError("THINKING_PATH_BBOX_TOO_SMALL")
        card_w = (bbox.width - cls.GAP * (len(steps) - 1)) / len(steps)
        if card_w < 90.0:
            raise ValueError("THINKING_PATH_CARD_TOO_NARROW")
        placements: List[ComponentPlacement] = []
        for idx, step in enumerate(steps):
            x = bbox.x + idx * (card_w + cls.GAP)
            card_box = BoundingBox(x, bbox.y, card_w, cls.CARD_H)
            backend.draw_rect(card_box.x, card_box.y, card_box.width, card_box.height, fill="#F3F9FF", stroke="#9EC4EE", corner_radius=5.0)
            backend.draw_text(f"{idx + 1}  {step.get('child_label', '')}", card_box.x + 8.0, card_box.y_max - 18.0, font_size=11.0, color=PrimaryPalette.NAVY)
            visual = step.get("resolved_visual")
            if not visual:
                raise ValueError(f"THINKING_PATH_MICRO_VISUAL_MISSING: {step.get('micro_visual_ref')}")
            visual_box = BoundingBox(card_box.x + 8.0, card_box.y + 44.0, card_box.width - 16.0, 52.0)
            render_primitive(visual["primitive_kind"], dict(visual.get("semantic_params") or {}), backend, visual_box)
            backend.draw_paragraph(str(step.get("one_line_action", "")), card_box.x + 8.0, card_box.y + 30.0, width=card_box.width - 16.0, font_size=cls.BODY_FONT, color=PrimaryPalette.STUDENT_PENCIL, line_height=14.0)
            placements.append(ComponentPlacement("THINKING_PATH_CARD", str(step.get("step_id", idx + 1)), card_box, 11.0))
            placements.append(ComponentPlacement("THINKING_PATH_VISUAL", str(step.get("micro_visual_ref", "")), visual_box, None))
        return placements
