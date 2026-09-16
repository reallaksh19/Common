#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
LE = HERE.parents[1]
PILOT = LE / "pilots" / "physics-thermodynamics.research.prototype.json"
REVIEW = LE / "pilots" / "physics-thermodynamics.first-law-validity.review.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ThermodynamicsFirstLawSemanticReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = load(PILOT)
        cls.review = load(REVIEW)

    def test_review_targets_exact_prototype_relation_and_is_non_authorizing(self):
        p = self.pilot
        r = self.review
        self.assertEqual(r["target_pilot_ref"], p["pilot_id"])
        relation_ids = {row["relation_id"] for row in p["relations"]}
        self.assertIn(r["target_relation_ref"], relation_ids)
        self.assertEqual(r["review_state"], "BLOCKING_SEMANTIC_REVIEW")
        self.assertFalse(r["runtime_authority"])
        self.assertFalse(r["publication_authority"])
        self.assertEqual(p["promotion_state"], "HELD")
        self.assertFalse(p["runtime_authority"])

    def test_internal_energy_form_cannot_be_promoted_without_macroscopic_energy_condition(self):
        relation = next(row for row in self.pilot["relations"] if row["relation_id"] == self.review["target_relation_ref"])
        self.assertEqual(relation["formal_expression"], "Delta U = Q_in - W_by")
        condition_text = " ".join(row["statement"] for row in relation["applicability_conditions"]).lower()
        has_macro_energy_condition = (
            ("kinetic" in condition_text and "potential" in condition_text)
            or "macroscopic energy" in condition_text
        )
        self.assertFalse(
            has_macro_energy_condition,
            "Once the governed relation carries the required condition, close/update the blocking semantic review instead of leaving stale review state.",
        )
        required = self.review["required_applicability_condition_before_promotion"].lower()
        self.assertIn("kinetic", required)
        self.assertIn("potential", required)
        self.assertIn("separately accounted", required)
        self.assertIn("must remain prototype held", self.review["promotion_effect"].lower().replace("_", " "))

    def test_general_energy_scope_and_sign_convention_are_both_preserved(self):
        finding = self.review["finding"].lower()
        self.assertIn("total system energy", finding)
        self.assertIn("internal", finding)
        self.assertIn("kinetic", finding)
        self.assertIn("potential", finding)
        sign = self.review["sign_convention_constraint"].lower()
        self.assertIn("work done by the system", sign)
        self.assertIn("alternate convention", sign)
        self.assertTrue(self.review["source_refs"])
        self.assertTrue(all(row["selection_reason"] for row in self.review["source_refs"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
