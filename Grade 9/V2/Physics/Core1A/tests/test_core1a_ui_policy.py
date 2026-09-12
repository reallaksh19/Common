#!/usr/bin/env python3
"""Regression checks for the Core (1A) learner UI policy."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "registry" / "physics-core1a-publication-policy.json"
SPEC = ROOT / "CORE1A_UI_SPEC.md"


def main() -> None:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    page = policy["page"]
    ui = policy["learner_ui"]
    difficulty = policy["difficulty"]
    codes = set(policy["quality_codes"])

    assert page["body_font_target_pt"] >= 10.5
    assert page["body_font_minimum_pt"] >= 10.0
    assert page["diagram_label_font_minimum_pt"] >= 8.0
    assert page["badge_font_minimum_pt"] >= 7.0
    assert page["badge_must_remain_single_line"] is True
    assert page["heading_badge_collision_forbidden"] is True
    assert page["text_outside_page_bounds_forbidden"] is True

    assert ui["illustration_is_support_not_replacement"] is True
    assert ui["concept_gateway"] == ["CHECK", "APPLY", "TRANSFER"]
    assert ui["core2_forward_link_required_when_mapped"] is True
    assert ui["core2_exact_repair_target_required"] is True
    assert ui["d2_d3_illustration_without_explanation_forbidden"] is True

    assert difficulty["D1_FOUNDATION"]["minimum_visual_stages"] >= 1
    assert difficulty["D2_THINK_CAREFULLY"]["minimum_visual_stages"] >= 2
    assert difficulty["D3_CHALLENGING"]["minimum_visual_stages"] >= 3
    assert difficulty["D3_CHALLENGING"]["requires_worked_reasoning"] is True
    assert difficulty["D4_EXTENSION"]["must_be_marked_optional_extension"] is True

    required_codes = {
        "CORE1A_BADGE_TEXT_CLIPPED_OR_WRAPPED",
        "CORE1A_HEADING_BADGE_COLLISION",
        "CORE1A_TEXT_OUT_OF_PAGE_BOUNDS",
        "CORE1A_RAW_MATH_STRING",
        "CORE1A_D2_D3_VISUAL_WITHOUT_TEACHING",
        "CORE1A_DIFFICULTY_SUPPORT_MISSING",
        "CORE1A_NO_CORE2_MASTERY_LINK",
        "CORE1A_CORE2_REPAIR_TARGET_MISMATCH",
    }
    assert required_codes <= codes

    spec = SPEC.read_text(encoding="utf-8")
    for phrase in (
        "illustration is support",
        "D2 THINK CAREFULLY",
        "D3 CHALLENGING",
        "CHECK → APPLY → CORE (2) TRANSFER",
        "exact repair target",
    ):
        assert phrase.lower() in spec.lower(), phrase

    print("Core1A UI policy checks: PASS")


if __name__ == "__main__":
    main()
