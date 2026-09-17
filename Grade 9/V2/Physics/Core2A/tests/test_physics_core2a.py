#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve()
C2A = HERE.parents[1]
ENGINE = C2A / "engine"
sys.path.insert(0, str(ENGINE))

from run_physics_core2a import compile_core2a


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class PhysicsCore2ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load(C2A / "golden" / "projectile-event" / "core2a-input.json")
        cls.source_schema = load(C2A / "contracts" / "physics-core2a-source-item.schema.json")
        cls.challenge_schema = load(C2A / "contracts" / "physics-core2a-challenge-item.schema.json")
        cls.run_schema = load(C2A / "contracts" / "physics-core2a-run.schema.json")
        cls.t_schema = load(C2A.parent / "Core1A" / "contracts" / "physics-taught-state-receipt.schema.json")

    def test_golden_competition_run_passes_and_schemas_validate(self):
        jsonschema.validate(self.fixture, self.run_schema)
        for receipt in self.fixture["taught_receipts"]:
            jsonschema.validate(receipt, self.t_schema)
        product, audit = compile_core2a(self.fixture)
        self.assertEqual(audit["status"], "PASS")
        self.assertEqual(product["source_corpus_count"], 1)
        self.assertEqual(product["source_selected_count"], 1)
        self.assertEqual(len(product["generated_items"]), 2)
        for item in product["source_items"]:
            jsonschema.validate(item, self.source_schema)
        for item in product["generated_items"]:
            jsonschema.validate(item, self.challenge_schema)

    def test_taught_complete_does_not_claim_mastery(self):
        product, _ = compile_core2a(self.fixture)
        self.assertTrue(product["authority_statement"]["learner_mastery_not_inferred_from_publication"])
        self.assertEqual(self.fixture["taught_receipts"][0]["learner_evidence_state"], "UNKNOWN")

    def test_missing_teaching_receipt_holds_source_question(self):
        run = copy.deepcopy(self.fixture)
        run["taught_receipts"] = []
        run["challenge_candidates"] = []
        run["purpose"] = "REVISION"
        product, audit = compile_core2a(run)
        self.assertEqual(product["source_selected_count"], 0)
        self.assertEqual(product["source_held_count"], 1)
        self.assertEqual(audit["source_held_count"], 1)

    def test_generated_item_cannot_require_untaught_capability(self):
        run = copy.deepcopy(self.fixture)
        run["challenge_candidates"][0]["required_capability_refs"].append("PHY-CAP-UNTaught")
        with self.assertRaisesRegex(ValueError, "CORE2A_UNTAUGHT_PHYSICS_REQUIRED"):
            compile_core2a(run)

    def test_independent_physics_recompute_rejects_wrong_answer_model(self):
        run = copy.deepcopy(self.fixture)
        run["challenge_candidates"][0]["physics_validation_case"]["expected_u"] = 25
        with self.assertRaisesRegex(ValueError, "CORE2A_PHYSICS_VALIDATION_FAILED"):
            compile_core2a(run)

    def test_canonical_answer_must_match_independent_recompute(self):
        run = copy.deepcopy(self.fixture)
        run["challenge_candidates"][0]["canonical_answer"] = "25 m/s upward"
        with self.assertRaisesRegex(ValueError, "CORE2A_PHYSICS_VALIDATION_FAILED:ANSWER_EQUIVALENCE"):
            compile_core2a(run)

    def test_declared_units_are_validated(self):
        run = copy.deepcopy(self.fixture)
        run["challenge_candidates"][0]["physics_validation_case"]["a_unit"] = "m/s"
        with self.assertRaisesRegex(ValueError, "CORE2A_PHYSICS_VALIDATION_FAILED:UNIT"):
            compile_core2a(run)

    def test_near_copy_is_rejected(self):
        run = copy.deepcopy(self.fixture)
        run["challenge_candidates"][0]["prompt"] = run["source_items"][0]["core2_representation"]["source_body"]["stem"]
        with self.assertRaisesRegex(ValueError, "CORE2A_GENERATED_ITEM_TOO_CLOSE_TO_SOURCE"):
            compile_core2a(run)

    def test_false_official_generated_attribution_is_rejected(self):
        run = copy.deepcopy(self.fixture)
        run["challenge_candidates"][0]["official_past_question_claim"] = True
        with self.assertRaisesRegex(ValueError, "CORE2A_FALSE_OFFICIAL_ATTRIBUTION"):
            compile_core2a(run)

    def test_competition_requires_near_and_structural_per_selected_bucket(self):
        run = copy.deepcopy(self.fixture)
        run["challenge_candidates"] = run["challenge_candidates"][:1]
        with self.assertRaisesRegex(ValueError, "CORE2A_PURPOSE_COVERAGE_GAP"):
            compile_core2a(run)

    def test_practice_preserves_all_releasable_source_items(self):
        run = copy.deepcopy(self.fixture)
        run["purpose"] = "PRACTICE"
        run["taught_receipts"][0]["purpose_ref"] = "PRACTICE"
        run["challenge_candidates"] = [run["challenge_candidates"][0]]
        product, _ = compile_core2a(run)
        self.assertEqual(product["source_selected_count"], product["source_corpus_count"])

    def test_purpose_is_mandatory(self):
        run = copy.deepcopy(self.fixture)
        run["purpose"] = None
        with self.assertRaisesRegex(ValueError, "CORE2A_PURPOSE_REQUIRED"):
            compile_core2a(run)


if __name__ == "__main__":
    unittest.main()
