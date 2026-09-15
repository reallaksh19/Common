import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]
CHEM_ROOT = LP_ROOT.parent
BP_ROOT = CHEM_ROOT / "LearningBlueprint"
sys.path.insert(0, str(LP_ROOT / "engine"))

from chemistry_review_candidate_preflight import review_candidate_checks  # noqa: E402
from preflight_chemistry_core_product import representation_physical_closure  # noqa: E402
from render_chemistry_a_content_first import _begin_attempt_support_episode  # noqa: E402

V5 = json.loads((BP_ROOT / "policies" / "v5-study-product-quality-policy.json").read_text(encoding="utf-8"))
PRODUCT_CONTROL = json.loads((BP_ROOT / "policies" / "product-control-consolidation.v1.json").read_text(encoding="utf-8"))
REVIEW = json.loads((BP_ROOT / "policies" / "review-candidate-realization.v1.json").read_text(encoding="utf-8"))


class FakeWriter:
    small = 9.25
    body = 10.5
    leading = 14.0
    width = 511.0
    margin = 42.0

    def __init__(self):
        self.ensure_calls = []
        self.roles = []

    def _wrap(self, text, font, size, width):
        words = str(text or "").split()
        return [" ".join(words)] if words else [""]

    def ensure(self, height, label="continuation", role=None):
        self.ensure_calls.append((height, label, role))

    def set_page_role(self, role):
        self.roles.append(role)


def two_page_metrics_with_illegal_cover_continuation():
    return {
        "composition_system": "CHEMISTRY_REVIEW_GRADE_V1",
        "page_count": 2,
        "page_labels": [
            {"page": 1, "label": "attempt", "role": "QUESTION_EPISODE"},
            {"page": 2, "label": "continuation", "role": "COVER"},
        ],
        "draw_ops": [
            {"page": 1, "kind": "QUESTION_PANEL", "x0": 42, "y0": 300, "x1": 553, "y1": 740},
            {"page": 1, "kind": "WORKSPACE_PANEL", "x0": 42, "y0": 120, "x1": 553, "y1": 285},
            {"page": 1, "kind": "CLUE_PANEL", "x0": 42, "y0": 80, "x1": 553, "y1": 110},
            {"page": 1, "kind": "ANSWER_PANEL", "x0": 42, "y0": 60, "x1": 553, "y1": 78},
            {"page": 1, "kind": "VERIFICATION_PANEL", "x0": 42, "y0": 45, "x1": 553, "y1": 58},
            {"page": 2, "kind": "ACTION_PANEL", "x0": 42, "y0": 680, "x1": 553, "y1": 740},
        ],
    }


class ChemistryPhysicalRealizationFalsePassTests(unittest.TestCase):
    def test_cover_role_after_first_page_never_exempts_density(self):
        result = review_candidate_checks(
            two_page_metrics_with_illegal_cover_continuation(),
            V5,
            PRODUCT_CONTROL,
            REVIEW,
            "CORE1B",
        )
        self.assertEqual(result["status"], "FAIL")
        page2 = next(row for row in result["page_checks"] if row["page"] == 2)
        self.assertEqual(page2["minimum_active_height_ratio"], V5["page_architecture"]["content_page_min_active_area_ratio"])
        self.assertIn("CHEM_REVIEW_COVER_ROLE_AFTER_FIRST_PAGE", page2["failures"])
        self.assertTrue(any("CHEM_REVIEW_UNJUSTIFIED_EMPTY_PAGE_AREA" in value for value in page2["failures"]))

    def test_authority_used_representation_must_be_physically_drawn(self):
        authority = {
            "representation_closure": {
                "used_representation_refs": ["REP-A"],
                "defined_representation_refs": ["REP-A"],
            }
        }
        missing = representation_physical_closure({"primitives": []}, authority)
        self.assertEqual(missing["status"], "FAIL")
        self.assertTrue(any(value.startswith("CHEM_CORE_PREFLIGHT_REPRESENTATION_NOT_PHYSICALLY_REALIZED") for value in missing["failures"]))

        passed = representation_physical_closure({"primitives": [{"representation_ref": "REP-A"}]}, authority)
        self.assertEqual(passed["status"], "PASS")

    def test_renderer_cannot_physically_add_an_unused_representation(self):
        authority = {
            "representation_closure": {
                "used_representation_refs": ["REP-A"],
                "defined_representation_refs": ["REP-A", "REP-B"],
            }
        }
        result = representation_physical_closure(
            {"primitives": [{"representation_ref": "REP-A"}, {"representation_ref": "REP-B"}]},
            authority,
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(value.startswith("CHEM_CORE_PREFLIGHT_REPRESENTATION_PHYSICAL_AUTHORITY_DRIFT") for value in result["failures"]))

    def test_core2_support_episode_is_reserved_before_incremental_drawing(self):
        writer = FakeWriter()
        support = {
            "write_this_first": "state the target",
            "small_clue": "identify the entities",
            "bigger_clue": "compare the representation",
            "how_do_i_start": "write the first relation",
            "watch_for_this": "preserve identity",
            "think_it_through": ["track one step", "track the next step"],
            "check_your_chemistry": ["run an independent check"],
        }
        _begin_attempt_support_episode(writer, support)
        self.assertEqual(len(writer.ensure_calls), 1)
        height, label, role = writer.ensure_calls[0]
        self.assertGreater(height, 250.0)
        self.assertEqual(label, "attempt support")
        self.assertEqual(role, "QUESTION_EPISODE")
        self.assertEqual(writer.roles, ["QUESTION_EPISODE"])

    def test_static_b_physical_representation_is_post_attempt_and_topic_neutral(self):
        source = (LP_ROOT / "engine" / "render_chemistry_static_b_product.py").read_text(encoding="utf-8")
        self.assertIn("used_representation_refs", source)
        self.assertIn("writer.primitive", source)
        self.assertNotIn("CLUE ROUTE", source)
        self.assertLess(source.index('w.answer_panel("EXPECTED RESPONSE"'), source.index('_render_used_representations(w, payload, ref + "-CHECK")'))
        self.assertLess(source.index('_render_used_representations(w, payload, ref + "-CHECK")'), source.index('w.verification_panel("VERIFY"'))
        lowered = source.lower()
        for forbidden in ("re" + "dox", "mn" + "o4", "perman" + "ganate"):
            self.assertNotIn(forbidden, lowered)


if __name__ == "__main__":
    unittest.main()
