import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHEM_ROOT = ROOT.parent
LP_ROOT = CHEM_ROOT / "LearnerProduct"
sys.path.insert(0, str(LP_ROOT / "engine"))

from chemistry_review_candidate_preflight import review_candidate_checks  # noqa: E402

V5 = json.loads((ROOT / "policies" / "v5-study-product-quality-policy.json").read_text(encoding="utf-8"))
PRODUCT_CONTROL = json.loads((ROOT / "policies" / "product-control-consolidation.v1.json").read_text(encoding="utf-8"))
REVIEW = json.loads((ROOT / "policies" / "review-candidate-realization.v1.json").read_text(encoding="utf-8"))


def plain_document_metrics():
    return {
        "page_count": 2,
        "page_labels": [
            {"page": 1, "label": "cover", "role": "COVER"},
            {"page": 2, "label": "body", "role": "CONCEPT_EXPLANATION"},
        ],
        "draw_ops": [
            {"page": 1, "kind": "TEXT", "x0": 42, "y0": 700, "x1": 300, "y1": 730},
            {"page": 2, "kind": "TEXT", "x0": 42, "y0": 350, "x1": 500, "y1": 750},
        ],
    }


def designed_core1b_metrics():
    return {
        "composition_system": "CHEMISTRY_REVIEW_GRADE_V1",
        "page_count": 2,
        "page_labels": [
            {"page": 1, "label": "attempt", "role": "QUESTION_EPISODE"},
            {"page": 2, "label": "reconstruct", "role": "TTU_RECONSTRUCTION"},
        ],
        "draw_ops": [
            {"page": 1, "kind": "NAV_HEADER", "x0": 0, "y0": 812, "x1": 595, "y1": 842, "text": "ATTEMPT"},
            {"page": 1, "kind": "QUESTION_PANEL", "x0": 42, "y0": 590, "x1": 553, "y1": 740},
            {"page": 1, "kind": "ACTION_PANEL", "x0": 42, "y0": 490, "x1": 553, "y1": 575},
            {"page": 1, "kind": "WORKSPACE_PANEL", "x0": 42, "y0": 220, "x1": 553, "y1": 475},
            {"page": 1, "kind": "TEXT", "x0": 56, "y0": 610, "x1": 500, "y1": 630},
            {"page": 2, "kind": "NAV_HEADER", "x0": 0, "y0": 812, "x1": 595, "y1": 842, "text": "RECONSTRUCT"},
            {"page": 2, "kind": "CLUE_PANEL", "x0": 42, "y0": 560, "x1": 553, "y1": 740},
            {"page": 2, "kind": "ANSWER_PANEL", "x0": 42, "y0": 370, "x1": 553, "y1": 545},
            {"page": 2, "kind": "VERIFICATION_PANEL", "x0": 42, "y0": 240, "x1": 553, "y1": 355},
            {"page": 2, "kind": "TEXT", "x0": 56, "y0": 600, "x1": 500, "y1": 620},
        ],
    }


class ChemistryReviewCandidateRealizationTests(unittest.TestCase):
    def test_plain_typeset_document_is_engineering_proof_not_review_candidate(self):
        result = review_candidate_checks(plain_document_metrics(), V5, PRODUCT_CONTROL, REVIEW, "CORE1A")
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["maturity_state"], "ENGINEERING_PROOF")
        self.assertIn("CHEM_REVIEW_PLAIN_DOCUMENT_LAYOUT", result["failures"])
        self.assertTrue(any("CHEM_REVIEW_MAJOR_SEMANTIC_SURFACE_MISSING" in row for row in result["failures"]))

    def test_review_gate_uses_current_v5_page_architecture_thresholds(self):
        result = review_candidate_checks(designed_core1b_metrics(), V5, PRODUCT_CONTROL, REVIEW, "CORE1B")
        self.assertEqual(result["content_page_min_active_area_ratio"], V5["page_architecture"]["content_page_min_active_area_ratio"])
        self.assertEqual(result["workspace_page_min_active_area_ratio"], V5["page_architecture"]["workspace_page_min_active_area_ratio"])
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["maturity_state"], "MACHINE_REVIEW_CANDIDATE")

    def test_static_b_renderer_is_not_forced_three_sheet_scaffold(self):
        source = (LP_ROOT / "engine" / "render_chemistry_static_b_product.py").read_text(encoding="utf-8")
        self.assertIn("ReviewWriter", source)
        self.assertNotIn('w.new_page()\n    w.heading("CLUES")', source)
        self.assertNotIn('w.new_page()\n    w.heading("FULL SOLUTION")', source)
        self.assertIn("WORKSPACE_PANEL", (LP_ROOT / "engine" / "chemistry_review_writer.py").read_text(encoding="utf-8"))

    def test_design_gate_and_writer_are_topic_neutral(self):
        sources = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in [
                ROOT / "policies" / "review-candidate-realization.v1.json",
                LP_ROOT / "engine" / "chemistry_review_candidate_preflight.py",
                LP_ROOT / "engine" / "chemistry_review_writer.py",
            ]
        )
        forbidden = ("re" + "dox", "mn" + "o4", "per" + "manganate")
        for token in forbidden:
            self.assertNotIn(token, sources)


if __name__ == "__main__":
    unittest.main()
