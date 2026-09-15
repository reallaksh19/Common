#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from validate_engineering_mapping_review import MappingReviewError, load, validate  # noqa: E402


def expect_code(fn, code: str) -> None:
    try:
        fn()
    except MappingReviewError as exc:
        assert exc.code == code, (exc.code, exc.message)
        return
    raise AssertionError(f"expected {code}")


review = load("provenance/pr383/mapping-reviews/PHY-GRAV-UNIVERSAL-LAW.v1.json")
result = validate(review)
assert result["status"] == "PASS"
assert result["decision"] == "APPROVED"
assert result["discovery_gate_id"] == "PHY-GRAV-UNIVERSAL-LAW"
assert result["target_gate_ids"] == ["PHY-GRAV-FORCE", "PHY-GRAV-FIELD"]
assert result["source_obligation_count"] == 11
assert result["covered_obligation_count"] == 11
assert result["uncovered_obligation_count"] == 0
assert result["readiness_authorized"] is False
assert result["source_custody_promoted"] is False
assert "Q15" not in json.dumps(review, sort_keys=True)

bad = copy.deepcopy(review)
bad["target_snapshot"][0]["gate_git_blob_sha"] = "0" * 40
expect_code(lambda: validate(bad), "E_ENG_MAPPING_TARGET_BLOB_DRIFT")

bad = copy.deepcopy(review)
bad["coverage"].pop()
expect_code(lambda: validate(bad), "E_ENG_MAPPING_SOURCE_COVERAGE_MISMATCH")

bad = copy.deepcopy(review)
pointer = bad["coverage"][0]["source_pointer"]
bad["coverage"][0]["status"] = "UNCOVERED"
bad["coverage"][0]["target_refs"] = []
bad["decision"]["uncovered_source_pointers"] = [pointer]
expect_code(lambda: validate(bad), "E_ENG_MAPPING_APPROVAL_HAS_GAPS")

bad = copy.deepcopy(review)
bad["coverage"][0]["target_refs"][0]["target_pointer"] = "/concepts/999"
expect_code(lambda: validate(bad), "E_ENG_MAPPING_POINTER_INVALID")

bad = copy.deepcopy(review)
bad["question_id"] = "Q15"
expect_code(lambda: validate(bad), "E_ENG_MAPPING_REVIEW_SCHEMA")

print("Physics engineering discovery mapping reviews: PASS")
print(result)
