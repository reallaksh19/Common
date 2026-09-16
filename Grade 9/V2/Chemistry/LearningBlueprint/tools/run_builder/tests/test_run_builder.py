#!/usr/bin/env python3
"""Tests for Chemistry LearningBlueprint Run Builder Configuration Compiler."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TOOL_DIR = HERE.parent
sys.path.insert(0, str(TOOL_DIR))

from compile_run import compile_manifest, compile_prompt, validate_all_fixtures, validate_config

FIXTURE_PATH = TOOL_DIR / "fixtures" / "cbse_class9_matter_atoms.json"


class ChemistryRunBuilderTests(unittest.TestCase):
    def setUp(self):
        self.base_config = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_complete_configuration_compiles_successfully(self):
        manifest = compile_manifest(self.base_config)
        prompt = compile_prompt(self.base_config)
        self.assertEqual(manifest["validation"]["status"], "VALID")
        self.assertEqual(manifest["validation"]["error_count"], 0)
        self.assertIn("Chemical Symbols", prompt)
        self.assertIn("CHEMISTRY", prompt)
        self.assertIn("CBSE_BOARD_EXAM", prompt)

    def test_missing_subtopic_blocks_compilation(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["subtopic_request"] = ""
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        codes = [e["code"] for e in manifest["validation"]["errors"]]
        self.assertIn("FIELD_REQUIRED", codes)

    def test_known_percentage_without_calibration_policy_or_waiver_blocks(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["learner_knowledge_mode"] = "KNOWN_PERCENT"
        cfg["learner_knowledge_percent"] = 75
        cfg["knowledge_calibration_policy_ref"] = ""
        cfg["owner_waiver_id"] = ""
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        err = next(e for e in manifest["validation"]["errors"] if e["field"] == "learner_knowledge_percent")
        self.assertIn("Conditioning practice on learner knowledge percent requires", err["message"])

    def test_unknown_knowledge_does_not_invent_number(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["learner_knowledge_mode"] = "UNKNOWN"
        cfg["learner_knowledge_percent"] = None
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "VALID")
        prompt = compile_prompt(cfg)
        self.assertIn("UNKNOWN (Percent: N/A)", prompt)

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
        cfg2["requested_engineering_depth"] = "RESEARCH"
        m2 = compile_manifest(cfg2)
        self.assertNotEqual(m1["manifest_digest"], m2["manifest_digest"])

    def test_free_text_subtopic_without_gate_remains_non_authoritative(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["exact_gate_id"] = None
        manifest = compile_manifest(cfg)
        self.assertIsNone(manifest["engineering"]["exact_gate_selected"])
        self.assertFalse(manifest["engineering"]["exact_resolver_passed"])
        self.assertEqual(manifest["dependencies"]["prerequisites_status"], "UNRESOLVED")

    def test_unsupported_grade_fails(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["current_grade"] = 12
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        self.assertTrue(any(e["code"] == "INVALID_GRADE" for e in manifest["validation"]["errors"]))

    def test_sdu_isolation_invariant(self):
        cfg = copy.deepcopy(self.base_config)
        cfg["core1_difficulty_control"] = "ADAPT_TO_LEARNER"
        manifest = compile_manifest(cfg)
        self.assertEqual(manifest["validation"]["status"], "INVALID")
        self.assertTrue(any(e["code"] == "SDU_LEARNER_ADAPTATION_FORBIDDEN" for e in manifest["validation"]["errors"]))

    def test_validate_all_four_fixtures(self):
        results = validate_all_fixtures()
        self.assertEqual(len(results), 4)
        for r in results:
            self.assertEqual(r["status"], "VALID")
            self.assertEqual(r["error_count"], 0)
            self.assertTrue(r["digest"].startswith("sha256:"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
