#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
CORE2B = HERE.parents[1]
ENGINE = CORE2B / "engine" / "compile_chemistry_core2b.py"
SPEC = importlib.util.spec_from_file_location("chem_core2b", ENGINE)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ChemistryCore2BSelfTutorTests(unittest.TestCase):
    def golden(self, family="evidence-to-claim"):
        return json.loads((CORE2B / "golden" / family / "input.json").read_text(encoding="utf-8"))

    def test_knowledge_percent_golden_resolves_v4_support(self):
        with tempfile.TemporaryDirectory() as td:
            audit = mod.compile_product(self.golden("evidence-to-claim"), Path(td))
            self.assertEqual(audit["status"], "PASS")
            self.assertEqual(audit["conditioning_mode"], "KNOWLEDGE_PERCENT")
            self.assertEqual(audit["knowledge_percent"], 50)
            self.assertEqual(audit["resolved_support_profile"]["support_density"], "MEDIUM")
            self.assertEqual(audit["resolved_support_profile"]["hint_entry_level"], "H2_STRUCTURE")
            self.assertEqual(audit["artifact"]["pages"], 2)
            plan = json.loads((Path(td) / "core2b_plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["knowledge_interpretation"], "SUPPORT_PRIOR_NOT_MASTERY_MEASUREMENT")
            self.assertEqual(plan["selected_item_id"], "U2Q35")

    def test_owner_override_golden_waives_percent_without_fabricating_one(self):
        with tempfile.TemporaryDirectory() as td:
            audit = mod.compile_product(self.golden("reaction-classification"), Path(td))
            self.assertEqual(audit["conditioning_mode"], "OWNER_OVERRIDE")
            self.assertTrue(audit["owner_override_auditable"])
            self.assertFalse(audit["fabricated_knowledge_percent"])
            self.assertNotIn("knowledge_percent", audit)
            self.assertEqual(audit["resolved_support_profile"]["support_density"], "LOW")
            self.assertEqual(audit["artifact"]["pages"], 3)
            plan = json.loads((Path(td) / "core2b_plan.json").read_text(encoding="utf-8"))
            self.assertNotIn("knowledge_percent", plan)
            self.assertTrue(plan["owner_override_auditable"])
            self.assertEqual(plan["selected_item_id"], "U2Q29A")

    def test_unresolved_conditioning_fails_closed(self):
        inp = self.golden()
        inp.pop("learner_conditioning")
        with self.assertRaisesRegex(ValueError, "CHEM_CORE2_LEARNER_CONDITION_UNRESOLVED"):
            mod.validate(inp)

    def test_invalid_knowledge_percent_fails_closed(self):
        inp = self.golden()
        inp["learner_conditioning"]["knowledge_percent"] = 101
        with self.assertRaisesRegex(ValueError, "CHEM_V4_KNOWLEDGE_PERCENT_INVALID"):
            mod.validate(inp)

    def test_dual_conditioning_authority_fails_closed(self):
        inp = self.golden()
        inp["learner_conditioning"]["owner_override"] = {
            "reason": "invalid dual authority",
            "support_profile": {},
            "demand_profile": {}
        }
        with self.assertRaisesRegex(ValueError, "CHEM_V4_CONDITIONING_DUAL_AUTHORITY"):
            mod.validate(inp)

    def test_knowledge_percent_changes_support_not_frozen_item_identity(self):
        inp = self.golden()
        inp["learner_conditioning"]["knowledge_percent"] = 90
        with tempfile.TemporaryDirectory() as td:
            audit = mod.compile_product(inp, Path(td))
            self.assertEqual(audit["selected_item_id"], "U2Q35")
            self.assertEqual(audit["resolved_support_profile"]["support_density"], "MINIMAL")
            self.assertEqual(audit["resolved_support_profile"]["hint_entry_level"], "H4_PRINCIPLE")
            self.assertEqual(audit["artifact"]["pages"], 3)

    def test_runtime_field_fails_closed(self):
        inp = self.golden()
        inp["attempt_history"] = []
        with self.assertRaisesRegex(ValueError, "CHEM_B_LIVE_RUNTIME_FIELD_PRESENT"):
            mod.validate(inp)

    def test_item_must_be_core2a_legal(self):
        inp = self.golden()
        inp["legal_core2a_item_ids"] = []
        with self.assertRaisesRegex(ValueError, "CHEM_CORE2B_ITEM_NOT_CORE2A_LEGAL"):
            mod.validate(inp)

    def test_source_identity_must_be_frozen(self):
        inp = self.golden()
        inp["source_item"]["item_id"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "CHEM_CORE2B_SOURCE_IDENTITY_DRIFT"):
            mod.validate(inp)

    def test_complete_help_ladder_is_required(self):
        inp = self.golden()
        inp["help"] = inp["help"][:-1]
        with self.assertRaisesRegex(ValueError, "CHEM_CORE2B_HELP_ORDER_INVALID"):
            mod.validate(inp)

    def test_answer_closure_is_mandatory(self):
        inp = self.golden()
        inp["full_solution"] = ""
        with self.assertRaisesRegex(ValueError, "CHEM_CORE2B_ANSWER_CLOSURE_MISSING"):
            mod.validate(inp)

    def test_new_chemistry_fails_closed(self):
        inp = self.golden()
        inp["new_chemistry_refs"] = ["UNTAUGHT-CHEMISTRY"]
        with self.assertRaisesRegex(ValueError, "CHEM_B_NEW_CHEMISTRY_INTRODUCED"):
            mod.validate(inp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
