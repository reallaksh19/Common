#!/usr/bin/env python3
"""Falsifiers for learner-facing Core2A source provenance locators."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
CORE2A = HERE.parents[1]
sys.path.insert(0, str(CORE2A / "engine"))

from build_chemistry_core2a_source import learner_question_locator  # noqa: E402


class ChemistryCore2APublicProvenanceTests(unittest.TestCase):
    def test_fixture_id_is_not_exposed(self):
        public = learner_question_locator("EXT01")
        self.assertEqual(public, "source item 1")
        self.assertNotIn("EXT01", public)

    def test_ncert_style_unit_question_locator_is_human_readable(self):
        self.assertEqual(learner_question_locator("U1-Q12"), "unit 1, question 12")
        self.assertEqual(learner_question_locator("U03Q026"), "unit 3, question 26")

    def test_sample_paper_locator_is_human_readable(self):
        self.assertEqual(learner_question_locator("SP1-Q2"), "sample paper 1, question 2")
        self.assertEqual(learner_question_locator("SP02Q017"), "sample paper 2, question 17")

    def test_simple_question_locator_is_human_readable(self):
        self.assertEqual(learner_question_locator("Q7"), "question 7")
        self.assertEqual(learner_question_locator("QUESTION-004"), "question 4")

    def test_unknown_machine_id_fails_safe_to_generic_public_label(self):
        value = "CHEM-INTERNAL-QUESTION-abc123"
        public = learner_question_locator(value)
        self.assertEqual(public, "source question")
        self.assertNotIn(value, public)


if __name__ == "__main__":
    unittest.main()
