#!/usr/bin/env python3
"""Acceptance gate: every source question has three realized staged visual hints."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.build_fixture import build_primary_input
from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.study_journey_fixture import build_study_journey
from Grade4.V2.Mathematics.Publication.engine.source_anchored_study_journey_composer import render_source_anchored_study_journey
from Grade4.V2.Mathematics.Representation.engine.base import BoundingBox, MockVectorBackend
from Grade4.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive
from Grade4.V2.Mathematics.StudyDesign.engine.source_visual_hints import (
    SourceVisualHintError,
    assert_source_visual_hint_coverage,
    attach_source_visual_hints,
    build_source_visual_catalog,
)


def _must_fail(fn, code: str) -> None:
    try:
        fn()
    except SourceVisualHintError as exc:
        if not str(exc).startswith(code + ":"):
            raise AssertionError(f"expected {code}, got {exc}") from exc
        return
    raise AssertionError(f"expected {code}, operation passed")


def main() -> None:
    primary_input = build_primary_input()
    catalog = build_source_visual_catalog(primary_input)
    plan = build_study_journey()
    enriched = attach_source_visual_hints(plan, catalog)
    coverage = assert_source_visual_hint_coverage(enriched)

    if coverage["source_visual_stage_count"] != coverage["source_question_count"] * 3:
        raise SystemExit(f"SOURCE_STAGED_HINT_COVERAGE_INCOMPLETE: {coverage}")

    # Every H1/H2/H3 visual must be a supported vector primitive, not a label.
    for source_ref, support in catalog.items():
        stages = list(support.get("stages") or [])
        assert [stage["level"] for stage in stages] == ["H1", "H2", "H3"]
        for stage in stages:
            backend = MockVectorBackend()
            render_primitive(
                stage["primitive_kind"],
                dict(stage["semantic_params"]),
                backend,
                BoundingBox(40.0, 40.0, 500.0, 150.0),
            )
            assert backend.operations, f"SOURCE_VISUAL_HINT_NOT_REALIZED: {source_ref}/{stage['level']}"
            assert backend.get_evidence(), f"SOURCE_VISUAL_HINT_EVIDENCE_MISSING: {source_ref}/{stage['level']}"

    # Missing one whole source binding must fail.
    broken_catalog = dict(catalog)
    missing_ref = sorted(broken_catalog)[0]
    broken_catalog.pop(missing_ref)
    _must_fail(lambda: attach_source_visual_hints(plan, broken_catalog), "SOURCE_VISUAL_HINT_REQUIRED")

    # Missing one stage must fail too; coverage is stage-level, not only question-level.
    one_stage_missing = copy.deepcopy(catalog)
    target_ref = sorted(one_stage_missing)[0]
    one_stage_missing[target_ref]["stages"] = one_stage_missing[target_ref]["stages"][:2]
    _must_fail(lambda: attach_source_visual_hints(plan, one_stage_missing), "SOURCE_STAGED_HINT_REQUIRED")

    # Real publication path must carry staged hint custody.
    out = REPO_ROOT / "build" / "grade4_math_v2" / "Source_Visual_Hint_Probe.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    _, custody = render_source_anchored_study_journey(plan, catalog, out)
    assert out.exists() and out.stat().st_size > 0
    sj = custody["study_journey"]
    assert sj["source_visual_hint_required"] is True
    assert sj["intrinsic_staged_hint_layout"] is True
    assert sj["source_visual_hint_coverage"]["source_question_count"] == coverage["source_question_count"]
    assert sj["source_visual_hint_coverage"]["source_visual_stage_count"] == coverage["source_visual_stage_count"]

    print({"status": "PASS", **coverage, "catalog_count": len(catalog), "pdf": str(out)})


if __name__ == "__main__":
    main()
