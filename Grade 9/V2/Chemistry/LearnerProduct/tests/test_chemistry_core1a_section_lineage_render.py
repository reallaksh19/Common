import json
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]
CHEM_ROOT = LP_ROOT.parent
sys.path.insert(0, str(LP_ROOT / "engine"))
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

from render_chemistry_a_content_first import render_core1a_content_first  # noqa: E402

POLICY = json.loads(
    (LP_ROOT / "policies" / "chemistry-learner-render-policy.json").read_text(encoding="utf-8")
)


class ChemistryCore1ASectionLineageRenderTests(unittest.TestCase):
    def manuscript(self):
        return {
            "manuscript_id": "TEST-CORE1A-SECTION-LINEAGE",
            "manuscript_digest": "sha256:" + "1" * 64,
            "buckets": [
                {
                    "learner_title": "Two distinct learning jobs",
                    "bucket_invariant": "Each section keeps its own learner-facing identity.",
                    "learning_atoms": [
                        {"atom_id": "ATOM-A", "learner_title": "Identify the conserved entity"},
                        {"atom_id": "ATOM-B", "learner_title": "Verify the governing relationship"},
                    ],
                    "teaching_sections": [
                        {
                            "capability_ref": "CAP-SHARED-GENERIC",
                            "see": "First governed explanation.",
                            "explain": ["Track the entity before applying a rule."],
                            "representation_refs": [],
                        },
                        {
                            "capability_ref": "CAP-SHARED-GENERIC",
                            "see": "Second governed explanation.",
                            "explain": ["Run the independent verification after applying the rule."],
                            "representation_refs": [],
                        },
                    ],
                    "problem_family_routines": [],
                    "practice_items": [],
                    "readiness_gate": {},
                }
            ],
        }

    def representations(self):
        return {
            "bundle_id": "TEST-EMPTY-REP-BUNDLE",
            "bundle_digest": "sha256:" + "2" * 64,
            "representations": [],
        }

    def test_distinct_atom_titles_survive_shared_capability(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "core1a-lineage.pdf"
            metrics = render_core1a_content_first(
                self.manuscript(), self.representations(), POLICY, path
            )
            self.assertTrue(path.is_file())
            self.assertEqual(metrics["product"], "CORE1A")
            document = pymupdf.open(path)
            text = "\n".join(page.get_text() for page in document)
            self.assertIn("Identify the conserved entity", text)
            self.assertIn("Verify the governing relationship", text)
            self.assertNotIn("SHARED GENERIC", text.upper())
            closure = metrics["section_visual_closure"]
            self.assertEqual([row["learning_atom_ref"] for row in closure], ["ATOM-A", "ATOM-B"])
            self.assertEqual(
                [row["learner_heading"] for row in closure],
                ["Identify the conserved entity", "Verify the governing relationship"],
            )

    def test_renderer_fails_if_atom_title_is_missing(self):
        manuscript = self.manuscript()
        manuscript["buckets"][0]["learning_atoms"][1]["learner_title"] = ""
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "CHEM_LP_RENDER_CORE1A_ATOM_TITLE_REQUIRED"):
                render_core1a_content_first(
                    manuscript,
                    self.representations(),
                    POLICY,
                    Path(td) / "missing-title.pdf",
                )


if __name__ == "__main__":
    unittest.main()
