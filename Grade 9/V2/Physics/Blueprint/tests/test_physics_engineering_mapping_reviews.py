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


grav_review = load("provenance/pr383/mapping-reviews/PHY-GRAV-UNIVERSAL-LAW.v1.json")
grav_result = validate(grav_review)
assert grav_result["status"] == "PASS"
assert grav_result["decision"] == "APPROVED"
assert grav_result["discovery_gate_id"] == "PHY-GRAV-UNIVERSAL-LAW"
assert grav_result["target_gate_ids"] == ["PHY-GRAV-FORCE", "PHY-GRAV-FIELD"]
assert grav_result["source_obligation_count"] == 11
assert grav_result["covered_obligation_count"] == 11
assert grav_result["uncovered_obligation_count"] == 0
assert grav_result["readiness_authorized"] is False
assert grav_result["source_custody_promoted"] is False
assert "Q15" not in json.dumps(grav_review, sort_keys=True)

free_fall_review = load("provenance/pr383/mapping-reviews/PHY-GRAV-FREE-FALL.v1.json")
free_fall_result = validate(free_fall_review)
assert free_fall_result["status"] == "PASS"
assert free_fall_result["decision"] == "APPROVED"
assert free_fall_result["discovery_gate_id"] == "PHY-GRAV-FREE-FALL"
assert free_fall_result["target_gate_ids"] == [
    "PHY-GRAV-FORCE",
    "PHY-GRAV-FIELD",
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-VELOCITY-EVOLUTION",
    "PHY-M2D-SAME-HEIGHT-VELOCITY",
]
assert free_fall_result["source_obligation_count"] == 14
assert free_fall_result["covered_obligation_count"] == 14
assert free_fall_result["uncovered_obligation_count"] == 0
assert free_fall_result["readiness_authorized"] is False
assert free_fall_result["source_custody_promoted"] is False
assert "Q15" not in json.dumps(free_fall_review, sort_keys=True)

newton_review = load("provenance/pr383/mapping-reviews/PHY-FORCE-NEWTON-LAWS.v1.json")
newton_result = validate(newton_review)
assert newton_result["status"] == "PASS"
assert newton_result["decision"] == "APPROVED"
assert newton_result["discovery_gate_id"] == "PHY-FORCE-NEWTON-LAWS"
assert newton_result["target_gate_ids"] == [
    "PHY-NLM-INTERACTION",
    "PHY-NLM-FBD",
    "PHY-NLM-FIRST-LAW",
    "PHY-NLM-SECOND-LAW",
    "PHY-NLM-THIRD-LAW",
]
assert newton_result["source_obligation_count"] == 12
assert newton_result["covered_obligation_count"] == 12
assert newton_result["uncovered_obligation_count"] == 0
assert newton_result["readiness_authorized"] is False
assert newton_result["source_custody_promoted"] is False
assert "Q15" not in json.dumps(newton_review, sort_keys=True)

projectile_review = load("provenance/pr383/mapping-reviews/PHY-KIN-2D-PROJECTILE.v1.json")
projectile_result = validate(projectile_review)
assert projectile_result["status"] == "PASS"
assert projectile_result["decision"] == "APPROVED"
assert projectile_result["discovery_gate_id"] == "PHY-KIN-2D-PROJECTILE"
assert projectile_result["target_gate_ids"] == [
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-VELOCITY-EVOLUTION",
]
assert projectile_result["source_obligation_count"] == 14
assert projectile_result["covered_obligation_count"] == 14
assert projectile_result["uncovered_obligation_count"] == 0
assert projectile_result["readiness_authorized"] is False
assert projectile_result["source_custody_promoted"] is False
assert "Q15" not in json.dumps(projectile_review, sort_keys=True)

relative_review = load("provenance/pr383/mapping-reviews/PHY-KIN-RELATIVE-2D.v1.json")
relative_result = validate(relative_review)
assert relative_result["status"] == "PASS"
assert relative_result["decision"] == "APPROVED"
assert relative_result["discovery_gate_id"] == "PHY-KIN-RELATIVE-2D"
assert relative_result["target_gate_ids"] == ["PHY-M2D-RELATIVE-VELOCITY"]
assert relative_result["source_obligation_count"] == 14
assert relative_result["covered_obligation_count"] == 14
assert relative_result["uncovered_obligation_count"] == 0
assert relative_result["readiness_authorized"] is False
assert relative_result["source_custody_promoted"] is False
assert "Q15" not in json.dumps(relative_review, sort_keys=True)

bad = copy.deepcopy(grav_review)
bad["target_snapshot"][0]["gate_git_blob_sha"] = "0" * 40
expect_code(lambda: validate(bad), "E_ENG_MAPPING_TARGET_BLOB_DRIFT")

bad = copy.deepcopy(grav_review)
bad["coverage"].pop()
expect_code(lambda: validate(bad), "E_ENG_MAPPING_SOURCE_COVERAGE_MISMATCH")

bad = copy.deepcopy(grav_review)
pointer = bad["coverage"][0]["source_pointer"]
bad["coverage"][0]["status"] = "UNCOVERED"
bad["coverage"][0]["target_refs"] = []
bad["decision"]["uncovered_source_pointers"] = [pointer]
expect_code(lambda: validate(bad), "E_ENG_MAPPING_APPROVAL_HAS_GAPS")

bad = copy.deepcopy(free_fall_review)
bad["target_snapshot"][5]["gate_git_blob_sha"] = "0" * 40
expect_code(lambda: validate(bad), "E_ENG_MAPPING_TARGET_BLOB_DRIFT")

bad = copy.deepcopy(free_fall_review)
bad["coverage"][3]["status"] = "UNCOVERED"
bad["coverage"][3]["target_refs"] = []
bad["decision"]["uncovered_source_pointers"] = [bad["coverage"][3]["source_pointer"]]
expect_code(lambda: validate(bad), "E_ENG_MAPPING_APPROVAL_HAS_GAPS")

bad = copy.deepcopy(newton_review)
bad["coverage"][0]["target_refs"][0]["target_pointer"] = "/concepts/999"
expect_code(lambda: validate(bad), "E_ENG_MAPPING_POINTER_INVALID")

bad = copy.deepcopy(projectile_review)
bad["target_snapshot"][1]["gate_git_blob_sha"] = "0" * 40
expect_code(lambda: validate(bad), "E_ENG_MAPPING_TARGET_BLOB_DRIFT")

bad = copy.deepcopy(relative_review)
bad["coverage"][1]["target_refs"] = []
bad["coverage"][1]["status"] = "UNCOVERED"
bad["decision"]["uncovered_source_pointers"] = [bad["coverage"][1]["source_pointer"]]
expect_code(lambda: validate(bad), "E_ENG_MAPPING_APPROVAL_HAS_GAPS")

bad = copy.deepcopy(free_fall_review)
bad["question_id"] = "Q15"
expect_code(lambda: validate(bad), "E_ENG_MAPPING_REVIEW_SCHEMA")

print("Physics engineering discovery mapping reviews: PASS")
print({
    "gravitation": grav_result,
    "free_fall": free_fall_result,
    "newton_laws": newton_result,
    "projectile": projectile_result,
    "relative_velocity": relative_result,
})
