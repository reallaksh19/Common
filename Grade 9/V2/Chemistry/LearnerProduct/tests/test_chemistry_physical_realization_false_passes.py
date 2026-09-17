import json
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]
CHEM_ROOT = LP_ROOT.parent
BP_ROOT = CHEM_ROOT / "LearningBlueprint"
sys.path.insert(0, str(LP_ROOT / "engine"))

from chemistry_review_candidate_preflight import ROLE_NAV_LABELS, review_candidate_checks  # noqa: E402
from chemistry_review_writer import ROLE_LABELS, ReviewWriter  # noqa: E402
from preflight_chemistry_core_product import representation_physical_closure  # noqa: E402
from render_chemistry_a_content_first import _begin_attempt_support_episode, _render_attempt_support  # noqa: E402

V5 = json.loads((BP_ROOT / "policies" / "v5-study-product-quality-policy.json").read_text(encoding="utf-8"))
PRODUCT_CONTROL = json.loads((BP_ROOT / "policies" / "product-control-consolidation.v1.json").read_text(encoding="utf-8"))
REVIEW = json.loads((BP_ROOT / "policies" / "review-candidate-realization.v1.json").read_text(encoding="utf-8"))
RENDER_POLICY = json.loads((LP_ROOT / "policies" / "chemistry-learner-render-policy.json").read_text(encoding="utf-8"))


class FakeWriter:
    small = 9.25
    body = 10.5
    leading = 14.0
    width = 511.0
    margin = 42.0

    def __init__(self):
        self.ensure_calls = []
        self.roles = []
        self.panels = []

    def _wrap(self, text, font, size, width):
        words = str(text or "").split()
        return [" ".join(words)] if words else [""]

    def ensure(self, height, label="continuation", role=None):
        self.ensure_calls.append((height, label, role))

    def set_page_role(self, role):
        self.roles.append(role)

    def clue_panel(self, title, text, ref=None):
        self.panels.append(("CLUE_PANEL", title, text, ref))

    def verification_panel(self, title, text, ref=None):
        self.panels.append(("VERIFICATION_PANEL", title, text, ref))


def two_page_metrics_with_illegal_cover_continuation():
    return {
        "composition_system": "CHEMISTRY_REVIEW_GRADE_V1",
        "page_count": 2,
        "page_labels": [
            {"page": 1, "label": "attempt", "role": "QUESTION_EPISODE"},
            {"page": 2, "label": "continuation", "role": "COVER"},
        ],
        "draw_ops": [
            {"page": 1, "kind": "NAV_HEADER", "x0": 0, "y0": 812, "x1": 595, "y1": 842, "text": "ATTEMPT"},
            {"page": 1, "kind": "QUESTION_PANEL", "x0": 42, "y0": 300, "x1": 553, "y1": 740},
            {"page": 1, "kind": "WORKSPACE_PANEL", "x0": 42, "y0": 120, "x1": 553, "y1": 285},
            {"page": 1, "kind": "CLUE_PANEL", "x0": 42, "y0": 80, "x1": 553, "y1": 110},
            {"page": 1, "kind": "ANSWER_PANEL", "x0": 42, "y0": 60, "x1": 553, "y1": 78},
            {"page": 1, "kind": "VERIFICATION_PANEL", "x0": 42, "y0": 45, "x1": 553, "y1": 58},
            {"page": 2, "kind": "NAV_HEADER", "x0": 0, "y0": 812, "x1": 595, "y1": 842, "text": "START HERE"},
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

    def test_page_role_nav_mismatch_fails_closed(self):
        metrics = two_page_metrics_with_illegal_cover_continuation()
        metrics["page_labels"][0]["role"] = "SOLUTION"
        result = review_candidate_checks(metrics, V5, PRODUCT_CONTROL, REVIEW, "CORE1B")
        page1 = next(row for row in result["page_checks"] if row["page"] == 1)
        self.assertTrue(any(
            value.startswith("CHEM_REVIEW_PAGE_ROLE_NAV_MISMATCH")
            for value in page1["failures"]
        ))

    def test_renderer_and_preflight_role_nav_contracts_cannot_drift(self):
        self.assertEqual(ROLE_LABELS, ROLE_NAV_LABELS)

    def test_role_transition_is_physical_not_metadata_only(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "role-transition.pdf"
            writer = ReviewWriter(path, "Generic role transition test", RENDER_POLICY)
            self.assertEqual(writer.page, 1)
            writer.set_page_role("QUESTION_EPISODE")
            self.assertEqual(writer.page, 1)
            self.assertEqual(writer.current_role, "QUESTION_EPISODE")
            first_nav = next(
                row for row in writer.draw_ops
                if row["page"] == 1 and row["kind"] == "NAV_HEADER"
            )
            self.assertEqual(first_nav["text"], "ATTEMPT")
            self.assertEqual(writer.page_labels[0]["role"], "QUESTION_EPISODE")

            writer.heading("Generic attempt", level=2, ref="ATTEMPT-1")
            writer.question_text("Use the governed evidence to determine the result.", ref="ATTEMPT-1")
            writer.set_page_role("SOLUTION")
            self.assertEqual(writer.page, 2)
            self.assertEqual(writer.page_labels[0]["role"], "QUESTION_EPISODE")
            self.assertEqual(writer.page_labels[1]["role"], "SOLUTION")
            second_nav = next(
                row for row in writer.draw_ops
                if row["page"] == 2 and row["kind"] == "NAV_HEADER"
            )
            self.assertEqual(second_nav["text"], "CHECK")
            writer.answer_panel("CHECK", "Compare against the governed result.", ref="ATTEMPT-1")
            writer.finish()

            doc = pymupdf.open(path)
            self.assertIn("ATTEMPT", doc[0].get_text())
            self.assertIn("CHECK", doc[1].get_text())
            doc.close()

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

    def test_core2_support_episode_is_reserved_and_rendered_as_semantic_surfaces(self):
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
        self.assertGreater(height, 400.0)
        self.assertEqual(label, "attempt support")
        self.assertEqual(role, "QUESTION_EPISODE")
        self.assertEqual(writer.roles, ["QUESTION_EPISODE"])

        _render_attempt_support(writer, support, "TEST-SUPPORT")
        kinds = [row[0] for row in writer.panels]
        self.assertEqual(kinds.count("CLUE_PANEL"), 6)
        self.assertEqual(kinds.count("VERIFICATION_PANEL"), 1)
        self.assertTrue(all(row[3] == "TEST-SUPPORT" for row in writer.panels))

        source = (LP_ROOT / "engine" / "render_chemistry_a_content_first.py").read_text(encoding="utf-8")
        self.assertNotIn("_attempt_support,", source)
        self.assertIn("_render_attempt_support(writer, support, ref)", source)

    def test_automatic_continuation_repeats_current_semantic_heading_physically(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "continuation-context.pdf"
            writer = ReviewWriter(path, "Generic continuation context test", RENDER_POLICY)
            writer.new_page("generic concept", role="CONCEPT_EXPLANATION")
            writer.heading("Generic concept context", level=2, ref="GENERIC-CONTEXT")
            writer.y = writer.margin + 12.0
            writer.para("Continue the governed learner reasoning without losing its section context.", ref="GENERIC-CONTEXT")
            metrics = writer.finish()

            continuation_rows = [row for row in metrics["draw_ops"] if row["kind"] == "CONTINUATION_HEADER"]
            self.assertEqual(len(continuation_rows), 1)
            continuation = continuation_rows[0]
            self.assertGreater(continuation["page"], 2)
            self.assertEqual(continuation["text"], "Generic concept context")
            self.assertEqual(continuation["content_ref"], "GENERIC-CONTEXT")

            doc = pymupdf.open(path)
            page_text = doc[continuation["page"] - 1].get_text("text")
            self.assertIn("CONTINUING", page_text)
            self.assertIn("Generic concept context", page_text)
            doc.close()

    def test_heading_moves_before_it_can_be_orphaned(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "heading-keep-with-next.pdf"
            writer = ReviewWriter(path, "Generic heading keep-with-next test", RENDER_POLICY)
            writer.new_page("generic concept", role="CONCEPT_EXPLANATION")
            writer.heading("Earlier generic section", level=2, ref="EARLIER")
            writer.y = 130.0
            old_page = writer.page
            writer.heading("Next generic section", level=2, ref="NEXT")
            writer.concept_panel("FIRST CONTENT", "Governed content remains with the section heading.", ref="NEXT")
            metrics = writer.finish()

            next_heading_rows = [
                row for row in metrics["draw_ops"]
                if row["kind"] == "TEXT" and row.get("text") == "Next generic section"
            ]
            self.assertEqual(len(next_heading_rows), 1)
            self.assertGreater(next_heading_rows[0]["page"], old_page)
            self.assertFalse(any(
                row["kind"] == "CONTINUATION_HEADER" and row["page"] == next_heading_rows[0]["page"]
                for row in metrics["draw_ops"]
            ))

            doc = pymupdf.open(path)
            old_text = doc[old_page - 1].get_text("text")
            new_text = doc[next_heading_rows[0]["page"] - 1].get_text("text")
            self.assertNotIn("Next generic section", old_text)
            self.assertIn("Next generic section", new_text)
            self.assertIn("FIRST CONTENT", new_text)
            doc.close()

    def test_static_b_physical_representation_is_post_attempt_and_topic_neutral(self):
        source = (LP_ROOT / "engine" / "render_chemistry_static_b_product.py").read_text(encoding="utf-8")
        self.assertIn("used_representation_refs", source)
        self.assertIn("writer.primitive", source)
        self.assertNotIn("CLUE ROUTE", source)
        self.assertIn("RESUME YOUR RECONSTRUCTION", source)
        self.assertIn("RESUME YOUR SOLUTION", source)
        resume_solution = source.index('"RESUME YOUR SOLUTION"')
        resume_workspace = source.index("w.workspace(4, ref)", resume_solution)
        solution_page = source.index('w.new_page("Core2B solution"', resume_solution)
        self.assertLess(resume_solution, resume_workspace)
        self.assertLess(resume_workspace, solution_page)
        self.assertLess(source.index('w.answer_panel("EXPECTED RESPONSE"'), source.index('_render_used_representations(w, payload, ref + "-CHECK")'))
        self.assertLess(source.index('_render_used_representations(w, payload, ref + "-CHECK")'), source.index('w.verification_panel("VERIFY"'))
        lowered = source.lower()
        for forbidden in ("re" + "dox", "mn" + "o4", "perman" + "ganate"):
            self.assertNotIn(forbidden, lowered)


if __name__ == "__main__":
    unittest.main()
