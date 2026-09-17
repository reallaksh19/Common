import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHEM_ROOT = ROOT.parent
LP_ROOT = CHEM_ROOT / "LearnerProduct"
sys.path.insert(0, str(LP_ROOT / "engine"))

from chemistry_content_first_preflight import content_first_page_checks  # noqa: E402

POLICY = json.loads((LP_ROOT / "policies" / "chemistry-learner-render-policy.json").read_text(encoding="utf-8"))


def metrics_with_second_page_span(y0: float, y1: float):
    return {
        "product": "CORE1A",
        "pagination_mode": "CONTENT_FIRST",
        "page_count": 2,
        "page_labels": [
            {"page": 1, "label": "cover"},
            {"page": 2, "label": "semantic block"},
        ],
        "draw_ops": [
            {"page": 1, "kind": "TEXT", "x0": 42, "y0": 700, "x1": 300, "y1": 760, "content_ref": "COVER"},
            {"page": 1, "kind": "FOOTER", "x0": 500, "y0": 20, "x1": 550, "y1": 30, "content_ref": None},
            {"page": 2, "kind": "TEXT", "x0": 42, "y0": y0, "x1": 300, "y1": y1, "content_ref": "BLOCK-1"},
            {"page": 2, "kind": "FOOTER", "x0": 500, "y0": 20, "x1": 550, "y1": 30, "content_ref": None},
        ],
    }


class ChemistryFourCoreContentFirstTests(unittest.TestCase):
    def test_sparse_noncover_semantic_fragment_fails_closed(self):
        result = content_first_page_checks(metrics_with_second_page_span(700, 740), POLICY, "CORE1A")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("CHEM_LP_RENDER_SPARSE_SEMANTIC_FRAGMENT" in row for row in result["failures"]))

    def test_moderately_sparse_noncover_page_also_fails_at_engineering_floor(self):
        result = content_first_page_checks(metrics_with_second_page_span(640, 760), POLICY, "CORE2A")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("CHEM_LP_RENDER_SPARSE_SEMANTIC_FRAGMENT" in row for row in result["failures"]))

    def test_content_bearing_noncover_page_passes(self):
        result = content_first_page_checks(metrics_with_second_page_span(560, 760), POLICY, "CORE1A")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["failures"], [])

    def test_cover_is_exempt_but_content_first_mode_is_mandatory(self):
        metrics = metrics_with_second_page_span(560, 760)
        metrics["draw_ops"][0]["y0"] = 745
        metrics["draw_ops"][0]["y1"] = 760
        result = content_first_page_checks(metrics, POLICY, "CORE1A")
        self.assertEqual(result["status"], "PASS")
        metrics["pagination_mode"] = "PAGE_TARGETED"
        result = content_first_page_checks(metrics, POLICY, "CORE1A")
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("CHEM_CORE_PREFLIGHT_CONTENT_FIRST_MODE_MISSING", result["failures"])

    def test_static_b_modes_are_not_density_rewritten_by_a_layer_policy(self):
        result = content_first_page_checks({}, POLICY, "CORE1B")
        self.assertEqual(result["status"], "NOT_APPLICABLE")
        self.assertEqual(result["failures"], [])

    def test_unified_runner_routes_a_modes_through_content_first_renderer(self):
        runner = (LP_ROOT / "engine" / "run_chemistry_core_product.py").read_text(encoding="utf-8")
        self.assertIn("render_core1a_content_first", runner)
        self.assertIn("render_core2a_content_first", runner)
        renderer = (LP_ROOT / "engine" / "render_chemistry_a_content_first.py").read_text(encoding="utf-8")
        self.assertNotIn('writer.new_page("Core (1A) practice")', renderer)
        self.assertNotIn('writer.new_page("fresh challenge practice")', renderer)
        self.assertIn('writer.new_page("Core (1A) expected response", role="SOLUTION")', renderer)
        self.assertIn('writer.new_page("answer check", role="SOLUTION")', renderer)
        self.assertNotIn('writer.new_page("full working")', renderer)
        self.assertIn('"full working",', renderer)
        self.assertIn("moved = writer.page != before", renderer)
        self.assertIn("if moved:", renderer)
        lowered = renderer.lower()
        for forbidden in ("redox", "mno4", "permanganate"):
            self.assertNotIn(forbidden, lowered)

    def test_policy_forbids_page_count_targeting_and_sets_sparse_floor(self):
        cfg = POLICY["preflight"]["content_first_pagination"]
        self.assertEqual(set(cfg["products"]), {"CORE1A", "CORE2A"})
        self.assertFalse(cfg["page_count_is_quality_metric"])
        self.assertEqual(cfg["minimum_noncover_active_height_ratio"], 0.18)


if __name__ == "__main__":
    unittest.main()
