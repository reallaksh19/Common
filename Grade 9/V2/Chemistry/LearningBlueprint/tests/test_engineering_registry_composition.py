#!/usr/bin/env python3
"""Tests for Chemistry Engineering Registry Composition & Extension Catalog."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from engineering_registry_composition import (  # noqa: E402
    canonical_source_custody,
    load_canonical_engineering_registry,
    load_extension_catalog,
)


class ChemistryEngineeringRegistryCompositionTests(unittest.TestCase):
    def test_extension_catalog_loads_and_matches_base_blob(self):
        cat = load_extension_catalog()
        self.assertEqual(cat["subject"], "CHEMISTRY")
        self.assertEqual(cat["catalog_id"], "CHEM-ENG-EXT-CATALOG-V1")

    def test_canonical_registry_loads_52_gates(self):
        reg = load_canonical_engineering_registry()
        self.assertEqual(len(reg["subtopic_gates"]), 52)

    def test_source_custody_reports_clean_state(self):
        cust = canonical_source_custody()
        self.assertEqual(cust["base_registry_ref"], "policies/chemistry-technical-engineering-gates.v1.json")
        self.assertEqual(cust["extensions"], [])


if __name__ == "__main__":
    unittest.main()
