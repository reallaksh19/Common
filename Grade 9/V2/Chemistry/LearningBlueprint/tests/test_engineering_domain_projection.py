#!/usr/bin/env python3
"""Tests for Chemistry Engineering Domain Projection."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from project_engineering_to_domain_registry import project_registry  # noqa: E402
from project_engineering_to_domain_registry_v2 import project_registry_v2  # noqa: E402


class ChemistryEngineeringDomainProjectionTests(unittest.TestCase):
    def test_project_registry_covers_all_52_gates(self):
        res = project_registry()
        self.assertEqual(len(res["projected_gates"]), 52)
        self.assertEqual(res["subject"], "CHEMISTRY")
        self.assertEqual(res["target_domain"], "CANONICAL_DOMAIN_REGISTRY")

    def test_project_registry_v2_includes_pedagogy_anchors(self):
        res_v2 = project_registry_v2()
        self.assertEqual(len(res_v2["projected_gates"]), 52)
        self.assertEqual(res_v2["schema_version"], "2.0.0")
        for g in res_v2["projected_gates"]:
            self.assertIn("pedagogy_anchor", g)
            self.assertIn("cbse_grade", g["pedagogy_anchor"])
            self.assertIn("jee_tier", g["pedagogy_anchor"])


if __name__ == "__main__":
    unittest.main()
