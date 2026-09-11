#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from material_custody import reconciliation_errors


def model() -> dict:
    return {
        "main_sections": [
            {
                "section_id": "SEC-01",
                "items": [
                    {"item_id": "CL-1", "traceability_class": "MATERIAL"},
                    {"item_id": "COND-1", "traceability_class": "MATERIAL"},
                    {"item_id": "PED-1", "traceability_class": "PEDAGOGICAL_CONNECTIVE"},
                ],
            }
        ]
    }


def structure(*, include_condition: bool, disposition: dict | None = None) -> dict:
    refs = ["CL-1"] + (["COND-1"] if include_condition else [])
    sg = {
        "learning_units": [
            {
                "unit_id": "SEC-01",
                "arc_steps": [
                    {"step_id": "S-1", "role": "SAY_IN_WORDS", "content_refs": refs}
                ],
            }
        ]
    }
    if disposition is not None:
        sg["content_dispositions"] = [disposition]
    return {"study_guide": sg}


def main() -> int:
    missing = reconciliation_errors(model(), structure(include_condition=False))
    assert any("COND-1: MATERIAL item disappears" in e for e in missing), missing

    rendered = reconciliation_errors(model(), structure(include_condition=True))
    assert rendered == [], rendered

    omitted = reconciliation_errors(
        model(),
        structure(
            include_condition=False,
            disposition={
                "content_ref": "COND-1",
                "disposition": "OMITTED_FOR_LEARNER",
                "reason": "Explicitly outside the declared learner depth for this publication target.",
            },
        ),
    )
    assert omitted == [], omitted

    bad_omission = reconciliation_errors(
        model(),
        structure(
            include_condition=False,
            disposition={"content_ref": "COND-1", "disposition": "OMITTED_FOR_LEARNER"},
        ),
    )
    assert any("requires a reason" in e for e in bad_omission), bad_omission

    print("MATERIAL_CUSTODY_MISSING_ITEM_FALSIFIER = PASS")
    print("MATERIAL_CUSTODY_RENDERED_PATH = PASS")
    print("MATERIAL_CUSTODY_EXPLICIT_OMISSION_PATH = PASS")
    print("MATERIAL_CUSTODY_REASON_REQUIRED = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
