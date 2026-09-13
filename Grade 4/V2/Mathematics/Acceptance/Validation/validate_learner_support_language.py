#!/usr/bin/env python3
"""Acceptance gate: source forensics stay out of Grade 4 learner support copy."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.build_fixture import build_primary_input
from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.study_journey_fixture import build_study_journey
from Grade4.V2.Mathematics.StudyDesign.engine.learner_support_language import (
    LearnerSupportLanguageError,
    assert_child_support_copy,
)
from Grade4.V2.Mathematics.StudyDesign.engine.source_visual_hints import (
    attach_source_visual_hints,
    build_source_visual_catalog,
)


def _source_questions(plan: dict) -> list[dict]:
    return [
        q
        for module in plan.get("modules") or []
        for block in module.get("blocks") or []
        for q in block.get("questions") or []
        if str(q.get("origin") or "") == "SOURCE"
    ]


def _must_fail(question: dict, code: str) -> None:
    try:
        assert_child_support_copy(question)
    except LearnerSupportLanguageError as exc:
        if not str(exc).startswith(code + ":"):
            raise AssertionError(f"expected {code}, got {exc}") from exc
        return
    raise AssertionError(f"expected {code}, question passed")


def main() -> None:
    primary = build_primary_input()
    plan = attach_source_visual_hints(build_study_journey(), build_source_visual_catalog(primary))
    questions = _source_questions(plan)
    assert len(questions) == 18
    for question in questions:
        assert_child_support_copy(question)

    issue_question = next(q for q in questions if (q.get("source_identity") or {}).get("source_issue"))
    raw_leak = copy.deepcopy(issue_question)
    raw_leak["hint_contract"]["stages"][0]["verbal_cue"] = str(raw_leak["source_identity"]["source_issue"])
    _must_fail(raw_leak, "SOURCE_FORENSIC_LANGUAGE_ON_LEARNER_SURFACE")

    long_copy = copy.deepcopy(questions[0])
    long_copy["hint_contract"]["stages"][0]["verbal_cue"] = "Read every possible detail before deciding what matters. " * 6
    _must_fail(long_copy, "LEARNER_HINT_COPY_TOO_LONG")

    phrase_leak = copy.deepcopy(questions[0])
    phrase_leak["hint_contract"]["stages"][0]["verbal_cue"] = "WHY THIS IS FLAGGED: inspect the worksheet."
    _must_fail(phrase_leak, "SOURCE_FORENSIC_LANGUAGE_ON_LEARNER_SURFACE")

    print({"status": "PASS", "source_questions_checked": len(questions)})


if __name__ == "__main__":
    main()
