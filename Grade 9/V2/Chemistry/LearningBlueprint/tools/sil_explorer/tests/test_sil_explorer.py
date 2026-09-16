#!/usr/bin/env python3
"""Tests for Chemistry SIL Explorer Catalog Generator."""

import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL_DIR = HERE.parent


class ChemistrySILExplorerTests(unittest.TestCase):
    def test_sil_catalog_data_file_exists_and_covers_52_packets(self):
        js_file = TOOL_DIR / "sil_catalog_data.js"
        self.assertTrue(js_file.exists())
        content = js_file.read_text(encoding="utf-8")
        self.assertIn("window.SIL_CATALOG", content)
        # Should count 52 occurrences of "gate_id"
        self.assertEqual(content.count('"gate_id":'), 52)

    def test_ui_files_exist(self):
        self.assertTrue((TOOL_DIR / "index.html").exists())
        self.assertTrue((TOOL_DIR / "sil_explorer.css").exists())
        self.assertTrue((TOOL_DIR / "sil_explorer.js").exists())


if __name__ == "__main__":
    unittest.main()
