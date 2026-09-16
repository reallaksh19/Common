#!/usr/bin/env python3
"""Tests for Engineering Discovery Benchmark Explorer UI and Workbench Portal."""

from __future__ import annotations

import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
DISCOVERY_DIR = HERE.parent
BLUEPRINT_ROOT = DISCOVERY_DIR.parents[1]
TOOLS_DIR = BLUEPRINT_ROOT / "tools"


class DiscoveryExplorerTests(unittest.TestCase):
    def test_discovery_explorer_html_exists_and_references_assets(self):
        html_path = DISCOVERY_DIR / "index.html"
        self.assertTrue(html_path.exists(), "discovery/index.html must exist")
        content = html_path.read_text(encoding="utf-8")
        self.assertIn("discovery_explorer.css", content)
        self.assertIn("discovery_explorer.js", content)
        self.assertIn("CANDIDATE_DISCOVERY_ONLY", content)
        self.assertIn("NOT_EVALUATED", content)

    def test_discovery_explorer_contains_all_five_navigation_views(self):
        html_path = DISCOVERY_DIR / "index.html"
        content = html_path.read_text(encoding="utf-8")
        for view in ["overview", "queries", "playground", "vocabulary", "academician"]:
            self.assertIn(f'data-view="{view}"', content)
            self.assertIn(f'id="{view}View"', content)

    def test_discovery_explorer_js_contains_no_topic_specific_hardcoding(self):
        js_path = DISCOVERY_DIR / "discovery_explorer.js"
        self.assertTrue(js_path.exists(), "discovery_explorer.js must exist")
        content = js_path.read_text(encoding="utf-8")
        # Ensure generic scoring logic has no hardcoded topic branches
        forbidden = [
            'topic === "Theory of Equations"',
            'subtopic === "quadratic"',
            'query === "Vieta"',
        ]
        for pattern in forbidden:
            self.assertNotIn(pattern, content)

    def test_unified_workbench_portal_exists_and_links_all_four_tools(self):
        portal_path = TOOLS_DIR / "index.html"
        self.assertTrue(portal_path.exists(), "tools/index.html must exist")
        content = portal_path.read_text(encoding="utf-8")
        self.assertIn("run_builder/index.html", content)
        self.assertIn("architecture_explorer/index.html", content)
        self.assertIn("../benchmarks/discovery/index.html", content)
        self.assertIn("../CORE_ARCHITECTURE_DRIFT_AUDIT.md", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
