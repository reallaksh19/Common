#!/usr/bin/env python3
"""Acceptance falsifiers for source anchoring, answer coverage and hint modality."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.StudyDesign.engine.study_journey import (
    StudyJourneyError,
    validate_study_journey,
)
from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.study_journey_fixture import (
    build_study_journey,
)


def _source_question() -> dict:
    return {
        "question_id": "Q-SRC-1",
        "origin": "SOURCE",
        "display_ref": "I(a)",
        "prompt": "40 / 5 + 12 = ____",
        "source_identity": {
            "source_ref": "SRC-Q1",
            "source_display_ref": "I(a)",
            "source_text": "40 / 5 + 12 = ____",
            "source_numeric_tokens": ["40", "5", "12"],
            "source_asset_ref": "SCAN-001",
            "source_page_or_image_index": 1,
            "source_section_label": "I",
            "source_item_label": "a",
            "source_issue": None,
        },
        "task_support_policy": "NUMERIC_FIRST",
        "answer_contract": {
            "answer_kind": "EXACT",
            "answer_text": "20",
            "check_route": "CHECK_AFTER_TRY",
            "answer_ref": "ANS-SRC-Q1",
        },
        "hint_contract": {
            "modality": "NUMERIC",
            "hint_text": "40 / 5 = 8. Now use 8 + 12.",
            "visual_ref": None,
            "may_reveal_final_answer": False,
        },
    }


def _base_plan() -> dict:
    q = _source_question()
    worked = copy.deepcopy(q)
    worked["question_id"] = "Q-SRC-WORKED"
    worked["answer_contract"]["answer_ref"] = "ANS-SRC-WORKED"
    worked["answer_contract"]["check_route"] = "INLINE"
    worked["task_support_policy"] = "NO_HINT"
    worked["hint_contract"] = {"modality": "NONE", "hint_text": None, "visual_ref": None, "may_reveal_final_answer": False}

    independent = {
        "question_id": "Q-PRACTICE-A",
        "origin": "GENERATED_PRACTICE",
        "display_ref": "Practice A",
        "prompt": "48 / 6 + 10 = ____",
        "source_identity": None,
        "task_support_policy": "NO_HINT",
        "answer_contract": {
            "answer_kind": "EXACT",
            "answer_text": "18",
            "check_route": "ANSWER_MAP",
            "answer_ref": "ANS-PRACTICE-A",
        },
        "hint_contract": {"modality": "NONE", "hint_text": None, "visual_ref": None, "may_reveal_final_answer": False},
    }

    return {
        "schema_version": "1.0.0",
        "journey_id": "SOURCE-ANCHOR-TEST",
        "title": "Source anchor test",
        "grade_level": 4,
        "modules": [
            {
                "module_id": "M1",
                "title": "DMAS",
                "learning_goal": "Use operation order.",
                "source_refs": ["SRC-Q1"],
                "concept_refs": ["ORDER_OF_OPERATIONS"],
                "prerequisite_bridges": [],
                "misconception_targets": [],
                "blocks": [
                    {
                        "block_id": "M1-SEE",
                        "block_type": "SEE_DISCOVER",
                        "title": "See",
                        "body": "Division and multiplication come before addition and subtraction.",
                        "answer_visibility": "HIDDEN",
                        "source_refs": ["SRC-Q1"],
                    },
                    {
                        "block_id": "M1-WORKED",
                        "block_type": "WORKED_EXAMPLE",
                        "title": "Worked",
                        "body": "Watch one.",
                        "answer_visibility": "WORKED_EXAMPLE",
                        "solution_text": "40 / 5 = 8; 8 + 12 = 20.",
                        "source_refs": ["SRC-Q1"],
                        "questions": [worked],
                    },
                    {
                        "block_id": "M1-GUIDED",
                        "block_type": "GUIDED_TRY",
                        "title": "With help",
                        "body": "Try the source question.",
                        "answer_visibility": "PARTIAL",
                        "source_refs": ["SRC-Q1"],
                        "questions": [q],
                    },
                    {
                        "block_id": "M1-INDEPENDENT",
                        "block_type": "INDEPENDENT_TRY",
                        "title": "Your turn",
                        "body": "Fresh practice.",
                        "answer_visibility": "HIDDEN",
                        "source_refs": ["SRC-Q1"],
                        "questions": [independent],
                    },
                ],
                "mastery_evidence": ["solves source item and fresh item"],
            }
        ],
        "source_coverage": {"required_source_refs": ["SRC-Q1"], "covered_source_refs": ["SRC-Q1"]},
    }


def _must_fail(plan: dict, code: str) -> None:
    try:
        validate_study_journey(plan)
    except StudyJourneyError as exc:
        if not str(exc).startswith(code + ":"):
            raise AssertionError(f"expected {code}, got {exc}") from exc
        return
    raise AssertionError(f"expected {code}, plan passed")


def main() -> None:
    base = _base_plan()
    result = validate_study_journey(base)
    assert result["learner_question_count"] == 3
    assert result["answer_contract_count"] == 3

    p = copy.deepcopy(base)
    p["modules"][0]["blocks"][2]["questions"][0]["source_identity"]["source_display_ref"] = ""
    _must_fail(p, "SOURCE_DISPLAY_REF_MISSING")

    p = copy.deepcopy(base)
    p["modules"][0]["blocks"][2]["questions"][0]["prompt"] = "Use DMAS."
    _must_fail(p, "SOURCE_QUESTION_TEXT_MISSING")

    p = copy.deepcopy(base)
    q = p["modules"][0]["blocks"][2]["questions"][0]
    q["source_identity"]["source_text"] = "40 / 5 + ____"
    q["source_identity"]["source_numeric_tokens"] = ["40", "5", "12"]
    q["prompt"] = "40 / 5 + ____"
    _must_fail(p, "SOURCE_NUMERIC_VALUE_DROPPED")

    p = copy.deepcopy(base)
    p["modules"][0]["blocks"][2]["questions"][0]["display_ref"] = "1"
    _must_fail(p, "SOURCE_ITEM_RENUMBERED")

    p = copy.deepcopy(base)
    del p["modules"][0]["blocks"][2]["questions"][0]["answer_contract"]
    _must_fail(p, "QUESTION_WITHOUT_ANSWER_CONTRACT")

    p = copy.deepcopy(base)
    p["modules"][0]["blocks"][2]["questions"][0]["answer_contract"]["check_route"] = ""
    _must_fail(p, "ANSWER_CHECK_ROUTE_MISSING")

    p = copy.deepcopy(base)
    p["modules"][0]["blocks"][3]["questions"][0]["display_ref"] = "II(b)"
    _must_fail(p, "GENERATED_ITEM_USES_SOURCE_NUMBERING")

    p = copy.deepcopy(base)
    p["modules"][0]["blocks"][2]["questions"][0]["task_support_policy"] = ""
    _must_fail(p, "HINT_MODALITY_MISSING")

    p = copy.deepcopy(base)
    q = p["modules"][0]["blocks"][2]["questions"][0]
    q["hint_contract"]["modality"] = "VISUAL"
    q["hint_contract"]["visual_ref"] = "SOME-VISUAL"
    _must_fail(p, "NUMERIC_TASK_WITH_GENERIC_TEXT_ONLY_HINT")

    p = copy.deepcopy(base)
    p["modules"][0]["blocks"][2]["questions"] = []
    _must_fail(p, "LEARNER_QUESTION_REQUIRED")

    real = build_study_journey()
    real_result = validate_study_journey(real)
    assert real_result["learner_question_count"] == real_result["answer_contract_count"]
    assert real_result["learner_question_count"] >= 20

    print({"status": "PASS", "synthetic_questions": 3, "p97_p99_questions": real_result["learner_question_count"]})


if __name__ == "__main__":
    main()
