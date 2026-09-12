from pathlib import Path

import pytest

from Primary.V2.Mathematics.Publication.engine.production_composer import (
    ProductionPrimaryPageComposer,
    ProductionPublicationError,
    render_core2_from_authoring_handoff,
)
from Primary.V2.Mathematics.Publication.tests.test_authoring_handoff_adapter import _handoff


def test_production_composer_rejects_legacy_text_only_ladder(tmp_path: Path):
    legacy = {
        "companion_id": "C2-LEGACY",
        "linked_core1_id": "C1-LEGACY",
        "appendix_a": {"batches": []},
        "appendix_b": {
            "ladders": [
                {
                    "item_id": "LEGACY-Q1",
                    "H1_notice": "Look at the groups.",
                    "H2_remember": "Remember equal groups.",
                    "H3_represent": "Draw the groups.",
                    "fresh_independent_retry_H0": "Try a fresh question."
                }
            ]
        },
        "appendix_c": {},
    }
    with pytest.raises(ProductionPublicationError) as exc:
        ProductionPrimaryPageComposer().render_core2_companion(legacy, tmp_path / "legacy.pdf")
    assert exc.value.code == "LEGACY_TEXT_ONLY_HINT_LADDER_FORBIDDEN"


def test_canonical_handoff_route_renders_without_legacy_fallback(tmp_path: Path):
    output = tmp_path / "production-from-handoff.pdf"
    pdf_sha, custody = render_core2_from_authoring_handoff(
        _handoff(),
        output,
        companion_id="C2-PRODUCTION",
        linked_core1_id="C1-PRODUCTION",
    )
    assert output.exists() and output.stat().st_size > 0
    assert len(pdf_sha) == 64
    semantic_ids = [sid for page in custody["page_map"] for sid in page["semantic_ids"]]
    assert "C2-RATE-BUILD:H1" in semantic_ids
    assert "C2-RATE-BUILD:H2" in semantic_ids
    assert "C2-RATE-BUILD:H3" in semantic_ids
    assert "C2-DIV-PROBE" not in semantic_ids
