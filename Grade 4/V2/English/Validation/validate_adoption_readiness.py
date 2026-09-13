#!/usr/bin/env python3
"""Block canonical adoption until source, render, and learner evidence are complete."""

from __future__ import annotations

import json
import sys
from pathlib import Path


class ReadinessError(Exception):
    pass


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise ReadinessError(f"{code}: {detail}")


def validate(root: Path) -> None:
    golden = load(root / "Golden" / "adjective-golden-lesson.v1.draft.json")
    qa = load(root / "Golden" / "adjective-golden-lesson.qa.v1.draft.json")
    trial = load(root / "Validation" / "adjective-learner-trial-template.v1.draft.json")

    require(
        golden["school_model"].get("verification_status") == "VERIFIED_PRIMARY_SOURCE",
        "PRIMARY_SOURCE_NOT_VERIFIED",
        golden["school_model"].get("verification_status", "missing"),
    )

    require(
        qa.get("visual_page_review", {}).get("status") == "PASS_FOR_DRAFT_GOLDEN_FIXTURE",
        "GOLDEN_RENDER_QA_NOT_PASS",
        qa.get("visual_page_review", {}).get("status", "missing"),
    )

    require(trial.get("status") == "PASS", "LEARNER_TRIAL_NOT_PASS", trial.get("status", "missing"))
    require(trial.get("decision") == "READY_FOR_ADOPTION_REVIEW", "LEARNER_TRIAL_DECISION_NOT_READY", trial.get("decision", "missing"))

    conditions = trial.get("conditions", {})
    require(conditions.get("adult_grammar_paraphrase_used") is False, "ADULT_GRAMMAR_TRANSLATION_USED", "trial required adult grammar paraphrase")
    require(conditions.get("answer_revealing_prompt_used") is False, "ANSWER_REVEALING_PROMPT_USED", "trial used an answer-revealing prompt")

    observations = trial.get("observations", {})
    required_true = [
        "states_page_task_without_grammar_translation",
        "classifies_before_ordering",
        "boundary_word_does_not_create_new_box",
        "explains_star_as_describing_word_without_book_box",
        "explains_starred_word_placement_from_model_or_example",
        "fresh_retry_uses_full_routine",
    ]
    for key in required_true:
        require(observations.get(key) is True, "LEARNER_OBSERVATION_NOT_MET", key)
    require(observations.get("needs_internal_or_adult_metadata") is False, "CHILD_SURFACE_NOT_INDEPENDENT", "learner needed adult/internal metadata")

    for task_id, status in trial.get("regression_tasks", {}).items():
        require(status == "PASS", "LEARNER_REGRESSION_NOT_PASS", f"{task_id}={status}")


def main() -> int:
    root = Path(__file__).parents[1]
    validate(root)
    print("PASS: Grade 4 English adjective adoption readiness")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ReadinessError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(1)
