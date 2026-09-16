import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "policies" / "review-candidate-realization.v1.json").read_text(encoding="utf-8"))


class ReviewCandidatePolicyContractTests(unittest.TestCase):
    def test_structural_pass_is_not_review_readiness(self):
        self.assertIn("STRUCTURAL_PDF_PASS_IS_NOT_REVIEW_READINESS", POLICY["governing_principles"])
        self.assertEqual(POLICY["failure_status"], "ENGINEERING_PROOF")
        self.assertEqual(POLICY["review_candidate_status"], "MACHINE_REVIEW_CANDIDATE")

    def test_layout_does_not_author_chemistry(self):
        self.assertIn("LAYOUT_MAY_ORGANIZE_AUTHORIZED_CONTENT_BUT_MAY_NOT_AUTHOR_CHEMISTRY", POLICY["governing_principles"])
        self.assertIn("policies/v5-study-product-quality-policy.json", POLICY["authority_inputs"])
        self.assertIn("policies/v7-product-assurance-policy.json", POLICY["authority_inputs"])
        self.assertIn("policies/product-control-consolidation.v1.json", POLICY["authority_inputs"])

    def test_all_four_modes_have_distinct_surface_jobs(self):
        modes = POLICY["mode_required_surface_jobs"]
        self.assertEqual(set(modes), {"CORE1A", "CORE1B", "CORE2A", "CORE2B"})
        self.assertNotEqual(set(modes["CORE1A"]), set(modes["CORE1B"]))
        self.assertNotEqual(set(modes["CORE2A"]), set(modes["CORE2B"]))


if __name__ == "__main__":
    unittest.main()
