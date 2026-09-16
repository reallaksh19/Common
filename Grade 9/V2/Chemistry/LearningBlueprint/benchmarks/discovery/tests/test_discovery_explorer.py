#!/usr/bin/env python3
"""
Unit Tests for Chemistry Discovery Explorer Web UI Assets
"""

import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


class ChemistryDiscoveryExplorerUITests(unittest.TestCase):
    def test_html_ui_exists_and_contains_portal_elements(self) -> None:
        html_file = HERE / "index.html"
        self.assertTrue(html_file.exists())
        content = html_file.read_text(encoding="utf-8")
        self.assertIn("Chemistry Engineering Discovery Explorer", content)
        self.assertIn("discovery_explorer.js", content)
        self.assertIn("discovery_explorer.css", content)

    def test_css_and_js_exist(self) -> None:
        css_file = HERE / "discovery_explorer.css"
        js_file = HERE / "discovery_explorer.js"
        self.assertTrue(css_file.exists())
        self.assertTrue(js_file.exists())
        self.assertGreater(len(css_file.read_text(encoding="utf-8")), 200)
        self.assertGreater(len(js_file.read_text(encoding="utf-8")), 500)


if __name__ == "__main__":
    unittest.main()
