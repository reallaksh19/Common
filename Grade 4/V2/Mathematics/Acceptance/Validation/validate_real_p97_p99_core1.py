#!/usr/bin/env python3
"""Real-source Core1 production gate for The Pupil pages 97-99.

This gate proves the canonical route:
source transcription -> explicit Grade-4 evidence -> authoring handoff ->
LearningRepresentationPlan -> measured direct Core1 PDF.

It also asserts the three source-quality caveats and the typed work surfaces that
were previously lost by renderer-local publication.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.build_fixture import build_primary_input
from Grade4.V2.Mathematics.LearningDesign.engine.authoring_handoff import build_authoring_handoff
from Grade4.V2.Mathematics.Publication.engine.production_composer import render_core1_from_authoring_handoff


OUTPUT_DIR = REPO_ROOT / "build" / "grade4_math_v2"
PDF_PATH = OUTPUT_DIR / "Primary_V2_P97_P99_Core1_Candidate.pdf"
RECORD_PATH = OUTPUT_DIR / "Primary_V2_P97_P99_Core1_Candidate.custody.json"


def fail(message: str) -> None:
    raise SystemExit(f"Real p97-p99 Core1 acceptance failed: {message}")


def _core1_row_by_source(handoff, qref: str):
    modules = list((handoff["authoring_result"].get("core1_plan") or {}).get("modules") or [])
    matches = [module for module in modules if qref in set(map(str, module.get("source_refs") or []))]
    if len(matches) != 1:
        fail(f"{qref}: expected one Core1 module, found {len(matches)}")
    module = matches[0]
    rows = [row for row in handoff["module_support"] if row.get("product") == "CORE1" and row.get("module_id") == module["module_id"]]
    if len(rows) != 1:
        fail(f"{qref}: support row missing for {module['module_id']}")
    return module, rows[0]


def _assert_surface(handoff, qref: str, expected_kind: str) -> None:
    _, row = _core1_row_by_source(handoff, qref)
    plan = row.get("learning_representation_plan") or {}
    surface = plan.get("work_surface")
    if not surface or surface.get("kind") != expected_kind:
        fail(f"{qref}: expected {expected_kind}, got {surface and surface.get('kind')}")


def main() -> None:
    primary_input = build_primary_input()
    questions = list(primary_input["question_set"]["questions"])
    if len(questions) != 18:
        fail(f"source-set coverage expected 18 questions, got {len(questions)}")
    refs = {q["question_ref"] for q in questions}
    if len(refs) != 18:
        fail("duplicate question_ref in source set")

    handoff = build_authoring_handoff(primary_input)
    core1_modules = list((handoff["authoring_result"].get("core1_plan") or {}).get("modules") or [])
    if len(core1_modules) != 18:
        fail(f"expected one Core1 module per source task, got {len(core1_modules)}")
    if handoff.get("publisher_invention_allowed") is not False:
        fail("publisher invention must remain false")
    if handoff["coverage"].get("unaccounted_modules") != 0:
        fail(f"unaccounted modules: {handoff['coverage']}")

    # Procedural learner work must survive the semantic boundary.
    for qref in ("P98-Q1", "P98-Q2", "P98-Q3"):
        _assert_surface(handoff, qref, "LONG_DIVISION_WORK")
    for qref in ("P98-Q4", "P98-Q5"):
        _assert_surface(handoff, qref, "ANGLE_DRAWING_WORKSPACE")
    _assert_surface(handoff, "P99-Q4", "DIVISION_TABLE_WORKSPACE")

    # The three source-quality caveats must survive into the learning plan.
    expected_note_fragments = {
        "P97-Q4": "DEFECTIVE_PRINTED_ITEM",
        "P97-Q6": "SEMANTICALLY_INVALID_STORY",
        "P97-Q9": "PHOTO_MAPPING_UNCERTAIN",
    }
    for qref, fragment in expected_note_fragments.items():
        _, row = _core1_row_by_source(handoff, qref)
        note = str((row.get("learning_representation_plan") or {}).get("source_note") or "")
        if fragment not in note:
            fail(f"{qref}: source caveat lost")

    # The notorious 7048 / 24 item must preserve exact validated semantics while
    # publishing an answer-free work surface.
    _, div_row = _core1_row_by_source(handoff, "P98-Q2")
    div_plan = div_row["learning_representation_plan"]
    params = div_plan["work_surface"]["semantic_params"]
    if (params.get("quotient"), params.get("remainder"), params.get("quotient_places")) != (293, 16, [2, 9, 3]):
        fail(f"P98-Q2 long-division semantics changed: {params}")
    if (div_plan.get("solution_guard") or {}).get("solution_tokens") != ["293", "16"]:
        fail("P98-Q2 solution guard missing quotient/remainder tokens")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_sha, custody = render_core1_from_authoring_handoff(
        handoff,
        PDF_PATH,
        title="Grade 4 Mathematics - Pages 97-99 Study Guide",
        topic="Workbook Revision",
        grade_level=4,
    )
    if not PDF_PATH.exists() or PDF_PATH.stat().st_size < 5000:
        fail("candidate PDF was not produced or is unexpectedly small")
    if len(pdf_sha) != 64:
        fail("candidate PDF SHA-256 missing")
    if custody.get("core1_handoff", {}).get("legacy_sections_used") is not False:
        fail("candidate used legacy Core1 sections")
    if custody.get("core1_handoff", {}).get("planned_module_count") != 18:
        fail(f"candidate planned module count mismatch: {custody.get('core1_handoff')}")
    notes = custody.get("core1_handoff", {}).get("source_notes") or []
    joined_notes = "\n".join(str(x.get("note") or "") for x in notes)
    for fragment in expected_note_fragments.values():
        if fragment not in joined_notes:
            fail(f"custody lost source caveat {fragment}")

    record = {
        "schema_version": "1.0.0",
        "candidate_kind": "REAL_SOURCE_CORE1",
        "source_set_id": "THE-PUPIL-P97-P99",
        "question_count": 18,
        "core1_module_count": 18,
        "pdf_path": str(PDF_PATH.relative_to(REPO_ROOT)),
        "pdf_sha256": pdf_sha,
        "legacy_sections_used": False,
        "typed_surface_requirements": {
            "long_division": ["P98-Q1", "P98-Q2", "P98-Q3"],
            "angle_drawing": ["P98-Q4", "P98-Q5"],
            "division_table": ["P99-Q4"],
        },
        "source_caveats": expected_note_fragments,
        "custody": custody,
    }
    RECORD_PATH.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "questions": 18,
        "core1_modules": 18,
        "pages": custody.get("page_count"),
        "pdf_sha256": pdf_sha,
        "pdf": str(PDF_PATH.relative_to(REPO_ROOT)),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
