#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from physical_page_custody import reconciliation_errors


def good_map() -> dict:
    return {
        "physical_page_count": 2,
        "page_intents": [
            {
                "page_intent_id": "PI-01",
                "physical_pages": [1, 2],
                "content_refs": ["CL-1", "Q-1"],
                "pagination_policy": "ALLOW_SPLIT",
                "max_physical_pages": 2,
                "minimum_final_page_fill": 0.25,
                "split": True,
                "continuation_pages": [2],
                "whitespace_role": "LEARNER_WORKSPACE",
            }
        ],
        "content_placements": [
            {
                "content_ref": "CL-1",
                "page_intent_id": "PI-01",
                "physical_pages": [1],
                "fragments": [{"page": 1, "x0": 50, "y0": 80, "x1": 500, "y1": 180}],
            },
            {
                "content_ref": "Q-1",
                "page_intent_id": "PI-01",
                "physical_pages": [2],
                "fragments": [{"page": 2, "x0": 50, "y0": 80, "x1": 500, "y1": 160}],
            },
        ],
        "page_metrics": [
            {
                "page": 1,
                "semantic_fill_ratio": 0.65,
                "starts_page_intent_ids": ["PI-01"],
                "continues_page_intent_ids": [],
                "semantic_content_refs": ["CL-1"],
                "orphan_continuation": False,
                "underfill_disposition": "ACCEPTABLE",
            },
            {
                "page": 2,
                "semantic_fill_ratio": 0.35,
                "starts_page_intent_ids": [],
                "continues_page_intent_ids": ["PI-01"],
                "semantic_content_refs": ["Q-1"],
                "orphan_continuation": False,
                "underfill_disposition": "LEARNER_WORKSPACE",
            },
        ],
    }


def main() -> int:
    good = good_map()
    assert reconciliation_errors(good) == [], reconciliation_errors(good)

    orphan = copy.deepcopy(good)
    orphan["page_metrics"][1]["orphan_continuation"] = True
    assert any("orphan continuation" in e for e in reconciliation_errors(orphan))

    missing = copy.deepcopy(good)
    missing["content_placements"] = missing["content_placements"][:1]
    assert any("declared page-intent content has no physical placement" in e for e in reconciliation_errors(missing))

    escaped = copy.deepcopy(good)
    escaped["physical_page_count"] = 3
    escaped["content_placements"][0]["physical_pages"] = [3]
    escaped["content_placements"][0]["fragments"][0]["page"] = 3
    escaped["page_metrics"].append({
        "page": 3,
        "semantic_fill_ratio": 0.1,
        "starts_page_intent_ids": [],
        "continues_page_intent_ids": [],
        "semantic_content_refs": [],
        "orphan_continuation": False,
        "underfill_disposition": "PATHOLOGICAL",
    })
    errors = reconciliation_errors(escaped)
    assert any("escapes page-intent physical range" in e for e in errors), errors
    assert any("pathological underfill" in e for e in errors), errors

    print("PHYSICAL_PAGE_GOOD_SPLIT = PASS")
    print("PHYSICAL_PAGE_ORPHAN_FALSIFIER = PASS")
    print("PHYSICAL_PAGE_CONTENT_PLACEMENT_CUSTODY = PASS")
    print("PHYSICAL_PAGE_RANGE_ESCAPE_FALSIFIER = PASS")
    print("PHYSICAL_PAGE_UNDERFILL_FALSIFIER = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
