#!/usr/bin/env python3
"""Acceptance gate: every source-derived learner question has a realized visual hint."""
from __future__ import annotations

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

    # Every resolved visual must be a real supported primitive with vector output.
    for source_ref, visual in catalog.items():
        backend = MockVectorBackend()
        render_primitive(
            visual["primitive_kind"],
            dict(visual["semantic_params"]),
            backend,
            BoundingBox(40.0, 40.0, 500.0, 150.0),
        )
        assert backend.operations, f"SOURCE_VISUAL_HINT_NOT_REALIZED: {source_ref}"
        assert backend.get_evidence(), f"SOURCE_VISUAL_HINT_EVIDENCE_MISSING: {source_ref}"

    # One mutation proves this is an acceptance requirement, not documentation.
    broken_catalog = dict(catalog)
    missing_ref = sorted(broken_catalog)[0]
    broken_catalog.pop(missing_ref)
    _must_fail(lambda: attach_source_visual_hints(plan, broken_catalog), "SOURCE_VISUAL_HINT_REQUIRED")

    # Real publication path: source question -> visual representation custody.
    out = REPO_ROOT / "build" / "grade4_math_v2" / "Source_Visual_Hint_Probe.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    _, custody = render_source_anchored_study_journey(plan, catalog, out)
    assert out.exists() and out.stat().st_size > 0
    assert custody["study_journey"]["source_visual_hint_required"] is True
    assert custody["study_journey"]["source_visual_hint_coverage"]["source_question_count"] == coverage["source_question_count"]

    print({"status": "PASS", **coverage, "catalog_count": len(catalog), "pdf": str(out)})


if __name__ == "__main__":
    main()
