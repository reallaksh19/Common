#!/usr/bin/env python3
"""Prove source refs in module metadata cannot substitute for actual source questions."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.StudyDesign.engine.study_journey import StudyJourneyError, validate_study_journey
from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.study_journey_fixture import build_study_journey


def main() -> None:
    plan = copy.deepcopy(build_study_journey())
    generated_index = 0
    for module in plan["modules"]:
        for block in module["blocks"]:
            for question in block.get("questions") or []:
                if question.get("origin") != "SOURCE":
                    continue
                generated_index += 1
                question["origin"] = "GENERATED_PRACTICE"
                question["display_ref"] = f"Practice Coverage {generated_index}"
                question["source_identity"] = None

    # The plan still declares all source refs in module/source_coverage metadata.
    # That must not count as learner-facing source-question coverage.
    try:
        validate_study_journey(plan)
    except StudyJourneyError as exc:
        if str(exc).startswith("SOURCE_QUESTION_COVERAGE_GAP:"):
            print({"status": "PASS", "falsifier": "SOURCE_QUESTION_COVERAGE_GAP"})
            return
        raise AssertionError(f"expected SOURCE_QUESTION_COVERAGE_GAP, got {exc}") from exc
    raise AssertionError("metadata-only source coverage unexpectedly passed")


if __name__ == "__main__":
    main()
