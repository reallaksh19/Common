"""Render and smoke-check the English Worksheet 09 StudyJourney candidate.

This is a publication integrity check, not the instructional-completeness proof.
Instructional completeness is established by validate_english_worksheet_09_study_journey.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pypdfium2 as pdfium

HERE = Path(__file__).resolve().parent
ENGLISH_ROOT = HERE.parents[1]
SOURCE_SET = ENGLISH_ROOT / "Benchmarks" / "source_sets" / "english_worksheet_09"
PUB_ENGINE = ENGLISH_ROOT / "Publication" / "engine"
for path in (SOURCE_SET, PUB_ENGINE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from study_journey_fixture import build_study_journey  # type: ignore  # noqa: E402
from study_journey_composer import render_study_journey  # type: ignore  # noqa: E402

OUT = Path("build/grade4_english_v2")
PDF = OUT / "Grade4_English_WS09_StudyJourney.pdf"
RENDERS = OUT / "renders_study_journey"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    journey = build_study_journey()
    expected_student_blocks = sum(
        1
        for obj in journey["learning_objects"]
        for block in obj["blocks"]
        if block["audience"] in {"STUDENT", "BOTH"}
    )

    _, meta = render_study_journey(journey, PDF, audience="STUDENT")
    assert meta["publisher_invention_allowed"] is False
    assert meta["rendered_block_count"] == expected_student_blocks
    assert meta["validation"]["teaching_block_count"] >= 55
    assert PDF.exists() and PDF.stat().st_size > 10000

    doc = pdfium.PdfDocument(str(PDF))
    assert len(doc) == meta["page_count"]
    assert len(doc) > 0
    RENDERS.mkdir(parents=True, exist_ok=True)
    for index in range(len(doc)):
        page = doc[index]
        bitmap = page.render(scale=1.25)
        image = bitmap.to_pil()
        assert image.width > 500 and image.height > 700
        image.save(RENDERS / f"page_{index + 1:02d}.png")

    print(
        f"English Worksheet 09 StudyJourney publication PASS: "
        f"{meta['rendered_block_count']} authored blocks across {len(doc)} rendered pages."
    )


if __name__ == "__main__":
    main()
