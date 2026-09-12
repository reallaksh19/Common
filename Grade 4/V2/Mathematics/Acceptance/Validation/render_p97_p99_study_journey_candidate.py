#!/usr/bin/env python3
"""Render the document-level p97-99 StudyJourney candidate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.study_journey_fixture import build_study_journey
from Grade4.V2.Mathematics.Publication.engine.study_journey_composer import render_study_journey

OUT_DIR = REPO_ROOT / "build" / "grade4_math_v2"
PDF = OUT_DIR / "Grade4_P97_P99_StudyJourney_Candidate.pdf"
CUSTODY = OUT_DIR / "Grade4_P97_P99_StudyJourney_Candidate.custody.json"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plan = build_study_journey()
    sha, custody = render_study_journey(plan, PDF)
    if not PDF.exists() or PDF.stat().st_size < 5000:
        raise SystemExit("StudyJourney PDF missing or unexpectedly small")
    study = custody.get("study_journey") or {}
    if study.get("publisher_invention_allowed") is not False:
        raise SystemExit("StudyJourney publisher invention must remain false")
    if (study.get("validation") or {}).get("source_coverage_count") != 18:
        raise SystemExit(f"source coverage lost: {study}")
    if int(study.get("page_count") or 0) < 8:
        raise SystemExit(f"unexpectedly short study journey: {study}")
    CUSTODY.write_text(json.dumps(custody, indent=2), encoding="utf-8")
    print({"status": "PASS", "pdf": str(PDF.relative_to(REPO_ROOT)), "sha256": sha, "pages": study.get("page_count")})


if __name__ == "__main__":
    main()
