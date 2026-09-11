#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
fixture = json.loads((ROOT / "cross_subject_answer_sheet_acceptance.json").read_text(encoding="utf-8"))
cases = {row["case_id"]: row for row in fixture["cases"]}

assert "MATH-COORD-GEOMETRIC-MODELLING" in cases["MATH-COORD-ALG-01"]["must_preserve"]
assert "MATHEMATICS_COORDINATE_GEOMETRY_GLOBALLY_WEAK" in cases["MATH-COORD-ALG-01"]["must_not_conclude"]

assert "MATH-WORD-MODELLING" in cases["MATH-WORD-EQUATION-01"]["must_preserve"]
assert "SHARED-SYMBOLIC-PRESERVE-MEANING" in cases["MATH-WORD-EQUATION-01"]["candidate_failure_capabilities"]

assert "PHY-KIN-SELECT-EQUATION" in cases["PHYSICS-MULTIPHASE-01"]["must_preserve"]
assert "PHY-KIN-PROPAGATE-STATE" in cases["PHYSICS-MULTIPHASE-01"]["candidate_failure_capabilities"]

assert cases["PHYSICS-PROJECTILE-01"]["required_action"] == "DIAGNOSTIC_PROBE_REQUIRED"

assert "CHEM-GAS-RELATIONSHIP" in cases["CHEM-GAS-PROP-01"]["must_preserve"]
assert "SHARED-PROPORTIONAL-REASONING" in cases["CHEM-GAS-PROP-01"]["candidate_failure_capabilities"]

for forbidden in [
    "ONE_WRONG_RESPONSE_CONFIRMS_MISCONCEPTION",
    "FAILED_FINAL_ANSWER_ERASES_UPSTREAM_SUCCESS",
    "ANSWER_SHEET_ALONE_PROVES_WORKING_MEMORY_OR_ATTENTION_CAUSE",
]:
    assert forbidden in fixture["global_falsifiers"]

print("LEARNER_INTELLIGENCE_CROSS_SUBJECT_ANSWER_SHEET_FALSIFIERS = PASS")
