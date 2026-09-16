#!/usr/bin/env python3
"""Tests for Chemistry Engineering Visibility Manifest."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_engineering_visibility_manifest import compile_visibility  # noqa: E402


class ChemistryEngineeringVisibilityTests(unittest.TestCase):
    def test_visibility_manifest_covers_all_52_gates(self):
        res = compile_visibility()
        self.assertEqual(res["subject"], "CHEMISTRY")
        self.assertEqual(res["visible_subtopic_count"], 52)
        self.assertEqual(len(res["visible_subtopics"]), 52)
        for sub in res["visible_subtopics"]:
            self.assertEqual(sub["visibility_tier"], "PUBLIC")
            self.assertIn("cbse_grade", sub)
            self.assertIn("jee_tier", sub)


if __name__ == "__main__":
    unittest.main()
