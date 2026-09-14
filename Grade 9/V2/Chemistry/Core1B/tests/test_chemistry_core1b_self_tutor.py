#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve()
CORE1B = HERE.parents[1]
ENGINE = CORE1B / "engine" / "compile_chemistry_core1b.py"
SPEC = importlib.util.spec_from_file_location("chem_core1b", ENGINE)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ChemistryCore1BSelfTutorTests(unittest.TestCase):
    def golden(self, family="observation-inference"):
        return json.loads((CORE1B / "golden" / family / "input.json").read_text(encoding="utf-8"))

    def test_both_goldens_compile_with_v4_bucket_authority(self):
        expected = {
            "observation-inference": ("EASY", 10),
            "redox-species-role": ("HARD", 30),
        }
        for family, (badge, pages) in expected.items():
            with self.subTest(family=family), tempfile.TemporaryDirectory() as td:
                audit = mod.compile_product(self.golden(family), Path(td))
                self.assertEqual(audit["status"], "PASS")
                self.assertEqual(audit["delivery_mode"], "STATIC")
                self.assertEqual(audit["live_runtime_fields"], "ABSENT")
                self.assertEqual(audit["new_chemistry_refs"], [])
                self.assertEqual(audit["blueprint_v4"]["difficulty_badge"], badge)
                self.assertEqual(audit["blueprint_v4"]["max_pages"], pages)
                self.assertFalse(audit["learner_knowledge_used_for_depth"])
                self.assertTrue((Path(td) / "chemistry_core1b.pdf").exists())
                plan = json.loads((Path(td) / "core1b_plan.json").read_text(encoding="utf-8"))
                self.assertEqual(plan["difficulty_badge"], badge)
                self.assertTrue(plan["page_envelope_is_ceiling_not_quota"])

    def test_runtime_field_fails_closed(self):
        inp = self.golden()
        inp["learner_response"] = "student answer"
        with self.assertRaisesRegex(ValueError, "CHEM_B_LIVE_RUNTIME_FIELD_PRESENT"):
            mod.validate(inp)

    def test_core1_knowledge_contamination_fails_closed(self):
        inp = self.golden()
        inp["knowledge_percent"] = 50
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_KNOWLEDGE_CONTAMINATION"):
            mod.validate(inp)

    def test_bucket_is_mandatory(self):
        inp = self.golden()
        inp.pop("instruction_bucket")
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_BLUEPRINT_V4_BUCKET_REQUIRED"):
            mod.validate(inp)

    def test_page_envelope_cannot_exceed_v4_badge_ceiling(self):
        inp = self.golden()
        inp["instruction_bucket"]["page_envelope"]["max_pages"] = 11
        with self.assertRaisesRegex(ValueError, "CHEM_V4_BUCKET_PAGE_ENVELOPE_INVALID"):
            mod.validate(inp)

    def test_medium_and_hard_research_is_enforced_by_v4(self):
        inp = self.golden("redox-species-role")
        inp["instruction_bucket"]["research"]["research_refs"] = []
        with self.assertRaisesRegex(ValueError, "CHEM_V4_HARD_DEEP_RESEARCH_MISSING"):
            mod.validate(inp)

    def test_new_chemistry_fails_closed(self):
        inp = self.golden()
        inp["new_chemistry_refs"] = ["UNTAUGHT-CHEMISTRY"]
        with self.assertRaisesRegex(ValueError, "CHEM_B_NEW_CHEMISTRY_INTRODUCED"):
            mod.validate(inp)

    def test_capability_outside_upstream_authority_fails(self):
        inp = self.golden()
        inp["capability_ref"] = "CAP-NOT-AUTHORIZED"
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_AUTHORITY_SCOPE_VIOLATION"):
            mod.validate(inp)

    def test_help_must_be_progressive_and_unique(self):
        inp = self.golden()
        inp["help"][0], inp["help"][1] = inp["help"][1], inp["help"][0]
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_HELP_ORDER_INVALID"):
            mod.validate(inp)

    def test_answer_closure_is_mandatory(self):
        inp = self.golden()
        inp["canonical_answer"] = ""
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_ANSWER_CLOSURE_MISSING"):
            mod.validate(inp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
