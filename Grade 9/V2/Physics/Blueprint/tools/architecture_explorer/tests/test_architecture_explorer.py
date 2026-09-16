#!/usr/bin/env python3
"""Tests for Physics Blueprint Architecture Explorer."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TOOL_DIR = HERE.parent
sys.path.insert(0, str(TOOL_DIR))

from generate_architecture_manifest import BLUEPRINT_ROOT, scan_components


class PhysicsArchitectureExplorerTests(unittest.TestCase):
    def test_manifest_generation_is_deterministic(self):
        m1 = scan_components(BLUEPRINT_ROOT)
        m2 = scan_components(BLUEPRINT_ROOT)
        self.assertEqual(m1["manifest_digest"], m2["manifest_digest"])
        self.assertEqual(m1["component_count"], m2["component_count"])
        self.assertEqual(m1["relation_count"], m2["relation_count"])

    def test_observation_manifest_carries_no_technical_authorization(self):
        m = scan_components(BLUEPRINT_ROOT)
        self.assertEqual(m["authority"], "DERIVED_ARCHITECTURE_OBSERVATION")
        self.assertEqual(m["technical_authorization"], "NOT_EVALUATED")
        self.assertEqual(m["publication_authorization"], "NOT_IMPLIED")

    def test_derived_relation_cannot_be_mislabeled_explicit(self):
        m = scan_components(BLUEPRINT_ROOT)
        for rel in m["relations"]:
            if rel["relation_type"] in {"REFERENCES", "VALIDATES", "CONSUMES", "PRODUCES"}:
                self.assertEqual(rel["confidence"], "DERIVED")

    def test_adding_synthetic_schema_causes_it_to_appear_generically(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            contracts = tmp_root / "contracts"
            contracts.mkdir(parents=True)

            synthetic_schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Synthetic Test Schema",
                "properties": {"schema_version": {"const": "1.0.0"}}
            }
            (contracts / "synthetic-test.schema.json").write_text(json.dumps(synthetic_schema), encoding="utf-8")

            m = scan_components(tmp_root)
            self.assertIn("schema:synthetic-test.schema.json", m["components"])
            comp = m["components"]["schema:synthetic-test.schema.json"]
            self.assertEqual(comp["title"], "Synthetic Test Schema")
            self.assertEqual(comp["component_type"], "SCHEMA")

    def test_adding_synthetic_validator_updates_graph_generically(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            contracts = tmp_root / "contracts"
            engine = tmp_root / "engine"
            contracts.mkdir(parents=True)
            engine.mkdir(parents=True)

            (contracts / "synthetic-gate.schema.json").write_text("{}", encoding="utf-8")
            validator_code = 'SCHEMA = "synthetic-gate.schema.json"\ndef validate(): pass\n'
            (engine / "validate_synthetic_gate.py").write_text(validator_code, encoding="utf-8")

            m = scan_components(tmp_root)
            self.assertIn("schema:synthetic-gate.schema.json", m["components"])
            self.assertIn("engine:validate_synthetic_gate.py", m["components"])

            schema_comp = m["components"]["schema:synthetic-gate.schema.json"]
            self.assertIn("engine:validate_synthetic_gate.py", schema_comp["validator_refs"])

            rel = next((r for r in m["relations"] if r["source"] == "engine:validate_synthetic_gate.py"), None)
            self.assertIsNotNone(rel)
            self.assertEqual(rel["relation_type"], "VALIDATES")
            self.assertEqual(rel["confidence"], "DERIVED")

    def test_unknown_or_orphan_schema_is_tracked_in_gap_reports(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            contracts = tmp_root / "contracts"
            contracts.mkdir(parents=True)
            (contracts / "lonely-orphan.schema.json").write_text("{}", encoding="utf-8")

            m = scan_components(tmp_root)
            self.assertIn("schema:lonely-orphan.schema.json", m["gap_reports"]["schemas_without_validator"])
            self.assertIn("schema:lonely-orphan.schema.json", m["gap_reports"]["orphan_schemas"])

    def test_topic_specific_physics_terms_are_not_present_in_explorer_code(self):
        source = (TOOL_DIR / "generate_architecture_manifest.py").read_text(encoding="utf-8")
        forbidden = ["bernoulli", "refraction", "kinematics", "torricelli", "archimedes"]
        for word in forbidden:
            self.assertNotIn(word, source.lower())

    def test_check_mode_passes_when_manifest_is_up_to_date(self):
        from generate_architecture_manifest import main
        old_argv = sys.argv
        try:
            sys.argv = ["generate_architecture_manifest.py", "--check"]
            main()
        finally:
            sys.argv = old_argv

    def test_check_mode_raises_system_exit_when_manifest_is_tampered(self):
        from generate_architecture_manifest import main
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_manifest = Path(tmpdir) / "architecture_observation_manifest.json"
            tmp_manifest.write_text(json.dumps({"manifest_digest": "sha256:forged_digest_000000000"}), encoding="utf-8")
            old_argv = sys.argv
            try:
                sys.argv = ["generate_architecture_manifest.py", "--check", "--out", str(tmp_manifest)]
                with self.assertRaises(SystemExit) as ctx:
                    main()
                self.assertIn("OUT OF DATE", str(ctx.exception))
            finally:
                sys.argv = old_argv

    def test_check_mode_raises_system_exit_when_manifest_file_missing(self):
        from generate_architecture_manifest import main
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_manifest = Path(tmpdir) / "non_existent_manifest.json"
            old_argv = sys.argv
            try:
                sys.argv = ["generate_architecture_manifest.py", "--check", "--out", str(tmp_manifest)]
                with self.assertRaises(SystemExit) as ctx:
                    main()
                self.assertIn("not found", str(ctx.exception))
            finally:
                sys.argv = old_argv


if __name__ == "__main__":
    unittest.main(verbosity=2)
