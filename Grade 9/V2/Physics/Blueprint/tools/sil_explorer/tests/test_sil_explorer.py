#!/usr/bin/env python3
"""Unit tests for the Physics Subtopic Intelligence Library (SIL) Explorer UI and Catalog Data."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIL_EXPLORER_DIR = HERE.parent
TOOLS_DIR = SIL_EXPLORER_DIR.parent
PORTAL_HTML = TOOLS_DIR / "index.html"
INDEX_HTML = SIL_EXPLORER_DIR / "index.html"
CSS_FILE = SIL_EXPLORER_DIR / "sil_explorer.css"
JS_FILE = SIL_EXPLORER_DIR / "sil_explorer.js"
CATALOG_DATA_JS = SIL_EXPLORER_DIR / "sil_catalog_data.js"


class SilExplorerTests(unittest.TestCase):

    def test_sil_explorer_html_exists_and_links_assets(self) -> None:
        self.assertTrue(INDEX_HTML.exists(), "index.html must exist")
        self.assertTrue(CSS_FILE.exists(), "sil_explorer.css must exist")
        self.assertTrue(JS_FILE.exists(), "sil_explorer.js must exist")
        self.assertTrue(CATALOG_DATA_JS.exists(), "sil_catalog_data.js must exist")

        content = INDEX_HTML.read_text(encoding="utf-8")
        self.assertIn("sil_explorer.css", content)
        self.assertIn("sil_catalog_data.js", content)
        self.assertIn("sil_explorer.js", content)
        self.assertIn("packet-list", content)
        self.assertIn("detail-area", content)

    def test_sil_catalog_data_covers_all_43_packets(self) -> None:
        content = CATALOG_DATA_JS.read_text(encoding="utf-8")
        json_match = re.search(r"window\.SIL_CATALOG\s*=\s*(\[.*?\]);\s*$", content, re.DOTALL)
        self.assertIsNotNone(json_match, "sil_catalog_data.js must declare window.SIL_CATALOG as a JSON array")

        catalog = json.loads(json_match.group(1))
        self.assertEqual(len(catalog), 43, "Catalog must contain exactly 43 foundation packets covering Grades 9–11")

        expected_gates = [
            # Grade 9 (10 gates)
            "PHY-KIN-1D-MOTION",
            "PHY-KIN-MOTION-GRAPHS",
            "PHY-FORCE-NEWTON-LAWS",
            "PHY-FORCE-MOMENTUM-IMPULSE",
            "PHY-GRAV-UNIVERSAL-LAW",
            "PHY-GRAV-FREE-FALL",
            "PHY-FLUID-BUOYANCY-ARCHIMEDES",
            "PHY-WORK-ENERGY-POWER",
            "PHY-ENERGY-CONSERVATION-LAW",
            "PHY-SOUND-LONGITUDINAL-WAVES",
            # Grade 10 (7 gates)
            "PHY-OPTICS-REFLECTION-MIRRORS",
            "PHY-OPTICS-REFRACTION-LENSES",
            "PHY-OPTICS-HUMAN-EYE",
            "PHY-OPTICS-DISPERSION-SCATTERING",
            "PHY-ELEC-CURRENT-OHM",
            "PHY-ELEC-POWER-JOULE",
            "PHY-MAG-INDUCTION-FARADAY",
            # Grade 11 (26 gates)
            "PHY-VEC-BASICS",
            "PHY-VEC-COMPONENTS",
            "PHY-VEC-ADD-SUB",
            "PHY-KIN-2D-PROJECTILE",
            "PHY-KIN-CIRCULAR-UNIFORM",
            "PHY-KIN-CIRCULAR-DYNAMICS",
            "PHY-KIN-RELATIVE-2D",
            "PHY-NLM-INTERACTION",
            "PHY-NLM-FBD",
            "PHY-NLM-FIRST-LAW",
            "PHY-NLM-SECOND-LAW",
            "PHY-NLM-THIRD-LAW",
            "PHY-NLM-NORMAL",
            "PHY-NLM-TENSION",
            "PHY-NLM-FRICTION",
            "PHY-NLM-CONNECTED",
            "PHY-WEP-VARIABLE-FORCE",
            "PHY-SYS-CENTRE-MASS",
            "PHY-ROT-RIGID-BODY",
            "PHY-ROT-ANGULAR-MOMENTUM",
            "PHY-GRAV-PLANETARY-ORBITS",
            "PHY-SOLID-ELASTICITY-HOOKE",
            "PHY-FLUID-BERNOULLI-EQUATION",
            "PHY-THERMO-FIRST-SECOND-LAW",
            "PHY-OSC-SHM-WAVES",
            "PHY-MAG-FIELD-LORENTZ",
        ]

        found_gates = [p["gate_id"] for p in catalog]
        for gate in expected_gates:
            self.assertIn(gate, found_gates, f"Gate {gate} must be present in catalog")

        for packet in catalog:
            self.assertGreaterEqual(len(packet["preconditions"]), 1, f"Packet {packet['gate_id']} must have preconditions")
            self.assertGreaterEqual(len(packet["atoms"]), 4, f"Packet {packet['gate_id']} must have at least 4 atoms")
            self.assertGreaterEqual(len(packet["misconceptions"]), 2, f"Packet {packet['gate_id']} must have at least 2 misconceptions")
            self.assertGreaterEqual(len(packet["ttus"]), 2, f"Packet {packet['gate_id']} must have at least 2 TTUs")
            self.assertGreaterEqual(len(packet["exam_families"]), 2, f"Packet {packet['gate_id']} must have at least 2 exam families")

    def test_sil_explorer_offline_capability(self) -> None:
        """Proves no external CDN links exist so the tool runs completely offline."""
        for path in [INDEX_HTML, CSS_FILE, JS_FILE]:
            content = path.read_text(encoding="utf-8")
            self.assertNotIn("http://", content, f"{path.name} must not contain insecure HTTP links")
            self.assertNotIn("https://cdn", content, f"{path.name} must not contain external CDN scripts")
            self.assertNotIn("unpkg.com", content, f"{path.name} must not depend on unpkg")
            self.assertNotIn("cdnjs.cloudflare.com", content, f"{path.name} must not depend on cdnjs")

    def test_portal_links_to_sil_explorer(self) -> None:
        content = PORTAL_HTML.read_text(encoding="utf-8")
        self.assertIn('href="sil_explorer/index.html"', content, "Workbench portal must link to SIL Explorer")
        self.assertIn("Launch SIL Explorer", content)

    def test_sil_explorer_js_renders_all_four_layers(self) -> None:
        content = JS_FILE.read_text(encoding="utf-8")
        self.assertIn("layer1", content)
        self.assertIn("layer2", content)
        self.assertIn("layer3", content)
        self.assertIn("layer4", content)
        self.assertIn("renderSvgForTtu", content)

    def test_sil_catalog_data_is_deterministic(self) -> None:
        content = CATALOG_DATA_JS.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("// Subtopic Intelligence Library - Catalog Data"))
        self.assertIn("window.SIL_CATALOG = [", content)


if __name__ == "__main__":
    unittest.main()
