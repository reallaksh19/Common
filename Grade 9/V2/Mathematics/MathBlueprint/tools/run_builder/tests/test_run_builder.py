#!/usr/bin/env python3
"""Tests for MathBlueprint Run Builder Configuration Compiler."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL_DIR = HERE.parent
import sys
sys.path.insert(0, str(TOOL_DIR))

from compile_run import compile_manifest, compile_prompt, validate_run_configuration

FIXTURE_PATH = TOOL_DIR / "fixtures" / "theory_of_equations_jee_fixture.json"


class RunBuilderTests(unittest.TestCase):
    def setUp(self):
        self.base_config = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_complete_configuration_compiles_successfully(self):
        manifest = compile_manifest(self.base_config)
        prompt = compile_prompt(self.base_config)
        self.assertEqual(manifest["validation"]["status"], "VALID")
        self.assertEqual(manifest["validation"]["error_count"], 0)
        self.assertIn("Theory of Equations", prompt)
        self.assertIn("70%", prompt)
        self.assertIn("RESEARCH", prompt)

    def test_missing_subtopic_blocks_compilation(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["subtopic_request"] = ""
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        codes = [e["code"] for e in manifest["validation"]["errors"]]
        self.assertIn("MISSING_REQUIRED_INPUT", codes)
        self.assertTrue(any(e["field"] == "subtopic_request" for e in manifest["validation"]["errors"]))

    def test_known_percentage_without_source_blocks(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["knowledge_source_ref"] = ""
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        self.assertTrue(any(e["field"] == "knowledge_source_ref" for e in manifest["validation"]["errors"]))

    def test_known_percentage_without_calibration_policy_blocks(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["knowledge_calibration_policy_ref"] = ""
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        err = next(e for e in manifest["validation"]["errors"] if e["field"] == "knowledge_calibration_policy_ref")
        self.assertIn("The percentage does not independently determine learner support", err["message"])

    def test_unknown_knowledge_does_not_invent_number(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["learner_knowledge_mode"] = "UNKNOWN"
        cfg["learner_knowledge_percent"] = None
        cfg["knowledge_source_ref"] = ""
        cfg["knowledge_calibration_policy_ref"] = ""
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "VALID")
        self.assertIsNone(manifest["learner"]["knowledge_percent"])
        self.assertEqual(manifest["learner"]["knowledge_mode"], "UNKNOWN")
        # Ensure it does NOT default to 50% or any arbitrary percentage
        prompt = compile_prompt(cfg)
        self.assertIn("UNKNOWN (Percent: N/A)", prompt)

    def test_unknown_knowledge_with_percentage_fails_validation(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["learner_knowledge_mode"] = "UNKNOWN"
        cfg["learner_knowledge_percent"] = 50
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        self.assertTrue(any(e["field"] == "learner_knowledge_percent" for e in manifest["validation"]["errors"]))

    def test_generated_manifest_and_prompt_are_deterministic(self):
        m1 = compile_manifest(self.base_config)
        m2 = compile_manifest(self.base_config)
        self.assertEqual(m1["manifest_digest"], m2["manifest_digest"])
        p1 = compile_prompt(self.base_config)
        p2 = compile_prompt(self.base_config)
        self.assertEqual(p1, p2)

    def test_changing_one_input_changes_manifest_digest_deterministically(self):
        m1 = compile_manifest(self.base_config)
        cfg2 = copy.deepcopy(self.base_config)
        cfg2["requested_engineering_depth"] = "STANDARD"
        m2 = compile_manifest(cfg2)
        self.assertNotEqual(m1["manifest_digest"], m2["manifest_digest"])

    def test_free_text_subtopic_remains_non_authoritative(self):
        manifest = compile_manifest(self.base_config)
        self.assertEqual(manifest["subtopic_authority_state"], "NON_AUTHORITATIVE_FREE_TEXT")
        self.assertEqual(manifest["dependencies"]["subtopic_resolution"]["current_state"], "NON_AUTHORITATIVE_FREE_TEXT")
        self.assertIsNone(manifest["engineering"]["exact_gate_selected"])
        self.assertFalse(manifest["engineering"]["exact_resolver_passed"])

    def test_unsupported_enum_values_fail(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["requested_engineering_depth"] = "SUPER_DEEP_INVENTED"
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        self.assertTrue(any(e["code"] == "UNKNOWN_POLICY" and e["field"] == "requested_engineering_depth" for e in manifest["validation"]["errors"]))

    def test_owner_notes_do_not_silently_override_structured_fields(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["owner_scope_notes"] = "Please treat depth as FOUNDATION and grade as 12."
        manifest = compile_manifest(cfg)
        # Structured depth and grade must remain intact
        self.assertEqual(manifest["engineering"]["requested_depth"], "RESEARCH")
        self.assertEqual(manifest["learner"]["current_grade"], 9)
        self.assertEqual(manifest["context"]["owner_scope_notes"], cfg["owner_scope_notes"])

    def test_subject_and_topic_do_not_create_topic_specific_js_branches(self):
        js_source = (TOOL_DIR / "run_builder.js").read_text(encoding="utf-8")
        forbidden = [
            'topic === "Theory of Equations"',
            'topic.includes("quadratic")',
            'knowledgePercent >= 70',
            'exam === "JEE"',
        ]
        for pattern in forbidden:
            self.assertNotIn(pattern, js_source)

    def test_ioqm_olympiad_geometry_fixture_compiles_successfully(self):
        fixture_path = TOOL_DIR / "fixtures" / "ioqm_olympiad_geometry_fixture.json"
        cfg = json.loads(fixture_path.read_text(encoding="utf-8"))
        manifest = compile_manifest(cfg)
        prompt = compile_prompt(cfg)
        self.assertEqual(manifest["validation"]["status"], "VALID")
        self.assertEqual(manifest["learner"]["knowledge_mode"], "UNKNOWN")
        self.assertEqual(manifest["core1_control"]["owner_difficulty_override"], "HARD")
        self.assertIn("IOQM / Regional Mathematical Olympiad", prompt)

    def test_cbse_linear_equations_fixture_compiles_successfully(self):
        fixture_path = TOOL_DIR / "fixtures" / "cbse_linear_equations_fixture.json"
        cfg = json.loads(fixture_path.read_text(encoding="utf-8"))
        manifest = compile_manifest(cfg)
        prompt = compile_prompt(cfg)
        self.assertEqual(manifest["validation"]["status"], "VALID")
        self.assertEqual(manifest["learner"]["knowledge_percent"], 85)
        self.assertEqual(manifest["engineering"]["requested_depth"], "STANDARD")
        self.assertIn("CBSE Board Examination", prompt)

    def test_cbse_g10_trig_circles_fixture_compiles_successfully(self):
        fixture_path = TOOL_DIR / "fixtures" / "cbse_g10_trig_circles_fixture.json"
        cfg = json.loads(fixture_path.read_text(encoding="utf-8"))
        manifest = compile_manifest(cfg)
        prompt = compile_prompt(cfg)
        self.assertEqual(manifest["validation"]["status"], "VALID")
        self.assertEqual(manifest["learner"]["knowledge_percent"], 88)
        self.assertEqual(manifest["engineering"]["requested_depth"], "STANDARD")
        self.assertEqual(manifest["learner"]["current_grade"], 10)
        self.assertIn("CBSE Class 10 Board Examination", prompt)

    def test_ioqm_g9_number_theory_fixture_compiles_successfully(self):
        fixture_path = TOOL_DIR / "fixtures" / "ioqm_g9_number_theory_fixture.json"
        cfg = json.loads(fixture_path.read_text(encoding="utf-8"))
        manifest = compile_manifest(cfg)
        prompt = compile_prompt(cfg)
        self.assertEqual(manifest["validation"]["status"], "VALID")
        self.assertEqual(manifest["learner"]["knowledge_mode"], "UNKNOWN")
        self.assertEqual(manifest["core1_control"]["owner_difficulty_override"], "HARD")
        self.assertEqual(manifest["learner"]["current_grade"], 9)
        self.assertIn("IOQM / PRMO Mathematical Olympiad", prompt)

    def test_validate_all_fixtures_passes_all_curated_fixtures(self):
        from compile_run import validate_all_fixtures
        results = validate_all_fixtures()
        self.assertEqual(len(results), 5)
        for r in results:
            self.assertEqual(r["status"], "VALID")
            self.assertEqual(r["error_count"], 0)
            self.assertTrue(r["digest"].startswith("sha256:"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
