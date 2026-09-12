from pathlib import Path

from Grade4.V2.Mathematics.LearningDesign.engine.authoring_handoff import build_authoring_handoff
from Grade4.V2.Mathematics.LearningDesign.validation.validate_authoring_handoff import (
    attach_blueprint,
    load_case,
)
from Grade4.V2.Mathematics.Publication.engine.production_composer import (
    render_core1_from_authoring_handoff,
)


def test_real_authoring_fixture_reaches_core1_pdf_without_legacy_sections(tmp_path: Path):
    primary_input = attach_blueprint(load_case("QUESTION_ONLY"))
    handoff = build_authoring_handoff(primary_input)

    output = tmp_path / "core1-real-authoring-handoff.pdf"
    pdf_sha, custody = render_core1_from_authoring_handoff(
        handoff,
        output,
        title="Multiplication Bridge",
        topic="Multiplication",
        grade_level=4,
    )

    assert output.exists() and output.stat().st_size > 0
    assert len(pdf_sha) == 64
    assert custody["core1_handoff"]["planned_module_count"] == 1
    assert custody["core1_handoff"]["publisher_invention_allowed"] is False

    semantic_ids = [sid for page in custody["page_map"] for sid in page["semantic_ids"]]
    assert any(sid.endswith("-PRIMARY") for sid in semantic_ids)
    assert any(sid == "C1-MULTIPLICATION-BRIDGE" for sid in semantic_ids)
