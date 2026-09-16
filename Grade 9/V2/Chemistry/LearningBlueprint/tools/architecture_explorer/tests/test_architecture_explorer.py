#!/usr/bin/env python3
"""Tests for Chemistry Architecture Explorer Manifest Generator."""

import json
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TOOL_DIR = HERE.parent
sys.path.insert(0, str(TOOL_DIR))

from generate_architecture_manifest import scan_components


class ChemistryArchitectureExplorerTests(unittest.TestCase):
    def test_scan_finds_schemas_policies_engines_and_tests(self):
        m = scan_components()
        self.assertEqual(m["subject"], "CHEMISTRY")
        self.assertGreater(m["component_count"], 20)
        self.assertIn("manifest_digest", m)
        self.assertTrue(m["manifest_digest"].startswith("sha256:"))

    def test_manifest_on_disk_is_in_sync(self):
        manifest_file = TOOL_DIR / "architecture_observation_manifest.json"
        self.assertTrue(manifest_file.exists())
        on_disk = json.loads(manifest_file.read_text(encoding="utf-8"))
        fresh = scan_components()
        self.assertEqual(on_disk["manifest_digest"], fresh["manifest_digest"])


if __name__ == "__main__":
    unittest.main()
