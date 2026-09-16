from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from validate_assessment_engineering_crosswalk import (
    DEFAULT_CROSSWALK,
    MathematicsAssessmentEngineeringCrosswalkError,
    load,
    resolve_bucket_gate_map,
    resolve_capability_gates,
    validate,
)


def canonical():
    return load(DEFAULT_CROSSWALK)


class AssessmentEngineeringCrosswalkTests(unittest.TestCase):
    def test_canonical_crosswalk_covers_all_mixed_grade9_capabilities(self):
        result = validate(canonical())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["capability_count"], 30)
        self.assertEqual(result["covered_capability_count"], 30)
        self.assertEqual(result["engineering_gap_count"], 0)
        self.assertEqual(result["engineering_gaps"], [])

    def test_euclid_classification_resolves_to_exact_foundations_gate(self):
        result = resolve_capability_gates(canonical(), ["MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE"])
        self.assertEqual(result["required_status"], "COVERED")
        self.assertEqual(
            result["capability_gate_map"]["MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE"],
            ["MATH-GEO-EUCLID-FOUNDATIONS"],
        )

    def test_exact_capability_resolution_has_no_title_or_fuzzy_fallback(self):
        with self.assertRaises(MathematicsAssessmentEngineeringCrosswalkError) as ctx:
            resolve_capability_gates(canonical(), ["Euclid Classify Axiom Postulate"])
        self.assertEqual(ctx.exception.code, "MATH_ENG_CROSSWALK_REQUIRED_CAPABILITY_OUTSIDE_SCOPE")

    def test_covered_capability_resolves_only_to_declared_exact_gate(self):
        result = resolve_capability_gates(canonical(), ["MATH-COORDINATE-DISTANCE"])
        self.assertEqual(result["required_status"], "COVERED")
        self.assertEqual(result["capability_gate_map"]["MATH-COORDINATE-DISTANCE"], ["MATH-GEO-COORDINATES"])

    def test_unknown_engineering_gate_fails(self):
        doc = canonical()
        row = next(x for x in doc["rows"] if x["capability_ref"] == "MATH-COORDINATE-DISTANCE")
        row["engineering_gate_ids"] = ["MATH-GEO-NOT-A-GATE"]
        with self.assertRaises(MathematicsAssessmentEngineeringCrosswalkError) as ctx:
            validate(doc)
        self.assertEqual(ctx.exception.code, "MATH_ENG_CROSSWALK_UNKNOWN_ENGINEERING_GATE")

    def test_unknown_assessment_capability_fails(self):
        doc = canonical()
        old = doc["rows"][0]["capability_ref"]
        doc["rows"][0]["capability_ref"] = "MATH-NOT-IN-ASSESSMENT-AUTHORITY"
        doc["coverage_scope_capability_refs"] = [
            "MATH-NOT-IN-ASSESSMENT-AUTHORITY" if x == old else x
            for x in doc["coverage_scope_capability_refs"]
        ]
        with self.assertRaises(MathematicsAssessmentEngineeringCrosswalkError) as ctx:
            validate(doc)
        self.assertEqual(ctx.exception.code, "MATH_ENG_CROSSWALK_UNKNOWN_ASSESSMENT_CAPABILITY")

    def test_engineering_registry_digest_drift_fails(self):
        doc = canonical()
        doc["engineering_registry_digest"] = "sha256:" + "0" * 64
        with self.assertRaises(MathematicsAssessmentEngineeringCrosswalkError) as ctx:
            validate(doc)
        self.assertEqual(ctx.exception.code, "MATH_ENG_CROSSWALK_ENGINEERING_REGISTRY_DIGEST_DRIFT")

    def test_bucket_resolution_is_exact_union_of_member_capabilities(self):
        plan = {"buckets": [{
            "bucket_id": "B1",
            "member_capability_refs": ["MATH-BINOMIAL-SQUARE-EXPANSION", "MATH-EQUIDISTANT-POINT-ON-AXIS"],
        }]}
        result = resolve_bucket_gate_map(canonical(), plan)
        self.assertEqual(
            result["bucket_gate_map"][0]["engineering_gate_ids"],
            ["MATH-ALG-POLYNOMIALS", "MATH-GEO-COORDINATES"],
        )
        self.assertEqual(result["bucket_gate_map"][0]["engineering_gap_capability_refs"], [])

    def test_euclid_bucket_is_release_covered(self):
        plan = {"buckets": [{
            "bucket_id": "B-EUCLID",
            "member_capability_refs": ["MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE"],
        }]}
        result = resolve_bucket_gate_map(canonical(), plan)
        self.assertEqual(result["required_status"], "COVERED")
        self.assertEqual(
            result["bucket_gate_map"][0]["engineering_gate_ids"],
            ["MATH-GEO-EUCLID-FOUNDATIONS"],
        )
        self.assertEqual(result["bucket_gate_map"][0]["engineering_gap_capability_refs"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
