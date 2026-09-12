"""Real-source publication acceptance for Grade-4 English Worksheet 09."""
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

from production_fixture import build_production_handoff  # type: ignore  # noqa: E402
from production_composer import (  # type: ignore  # noqa: E402
    render_practice_workbook,
    render_study_guide,
    render_teacher_diagnostic_key,
)
from publication_model import build_study_guide_model, build_teacher_key_model  # type: ignore  # noqa: E402

OUT = Path("build/grade4_english_v2")
EXPECTED_REFS = {
    "ENG-G4-WS09-I",
    "ENG-G4-WS09-II",
    "ENG-G4-WS09-III",
    "ENG-G4-WS09-IV",
    "ENG-G4-WS09-V-Q1",
    "ENG-G4-WS09-V-Q2",
    "ENG-G4-WS09-V-Q3",
    "ENG-G4-WS09-V-Q4",
}


def _render_check(path: Path, render_dir: Path) -> int:
    doc = pdfium.PdfDocument(str(path))
    assert len(doc) == 9, f"{path.name}: expected 9 pages, got {len(doc)}"
    render_dir.mkdir(parents=True, exist_ok=True)
    for index in range(len(doc)):
        page = doc[index]
        bitmap = page.render(scale=1.35)
        image = bitmap.to_pil()
        assert image.width > 500 and image.height > 700
        image.save(render_dir / f"page_{index + 1:02d}.png")
    return len(doc)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    handoff = build_production_handoff()
    refs = {p["question_ref"] for p in handoff["learning_representation_plans"]}
    assert refs == EXPECTED_REFS

    for plan in handoff["learning_representation_plans"]:
        assert plan.get("publication_provenance") == "VISUAL_QA_REFINEMENT_WITHOUT_SEMANTIC_CHANGE"
        assert plan.get("source_prompt")
        assert plan.get("learner_prompt")
        assert plan["representation_specs"]

    study_model = build_study_guide_model(handoff)
    teacher_model = build_teacher_key_model(handoff)
    for page in study_model["pages"]:
        if page.get("question_ref"):
            assert page["fresh_retry"]["conceptual_support"] == "H0"
    boundary = next(p for p in study_model["pages"] if p.get("question_ref") == "ENG-G4-WS09-III")
    assert boundary["source_boundary_required"] is True
    assert boundary["source_model"]["ordering"] == ["OPINION", "SIZE", "AGE", "SHAPE", "COLOUR", "ORIGIN", "MATERIAL"]
    assert "traditional" in " ".join(boundary["ambiguity"])

    for page in teacher_model["pages"]:
        if page.get("judgement_required"):
            assert "model_answer" not in page and "exact_answer" not in page

    artifacts = [
        (render_study_guide, OUT / "Grade4_English_WS09_Study_Guide.pdf", OUT / "renders_study"),
        (render_practice_workbook, OUT / "Grade4_English_WS09_Practice_Workbook.pdf", OUT / "renders_workbook"),
        (render_teacher_diagnostic_key, OUT / "Grade4_English_WS09_Teacher_Diagnostic_Key.pdf", OUT / "renders_teacher"),
    ]
    total = 0
    for renderer, path, render_dir in artifacts:
        _, meta = renderer(handoff, path)
        assert set(meta["question_refs"]) == EXPECTED_REFS
        assert path.exists() and path.stat().st_size > 5000
        total += _render_check(path, render_dir)

    print(f"Grade 4 English V2 publication acceptance passed: 3 PDFs / {total} rendered pages.")


if __name__ == "__main__":
    main()
