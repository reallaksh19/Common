#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
CORE1B = HERE.parents[1]
ENGINE = CORE1B / "engine" / "compile_hard_redox_bucket_v2.py"
INPUT = CORE1B / "golden" / "hard-redox-production" / "input.json"
SPEC = importlib.util.spec_from_file_location("chem_core1b_hard_v2", ENGINE)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class HardRedoxProductionTests(unittest.TestCase):
    def payload(self):
        return json.loads(INPUT.read_text(encoding="utf-8"))

    def test_production_bucket_renders_24_pages_inside_hard_ceiling(self):
        with tempfile.TemporaryDirectory() as td:
            audit = mod.compile_product(self.payload(), Path(td))
            self.assertEqual(audit["status"], "PASS")
            self.assertEqual(audit["realized_pages"], 24)
            self.assertEqual(audit["page_ceiling"], 30)
            self.assertEqual(audit["blueprint_v4"]["difficulty_badge"], "HARD")
            self.assertEqual(audit["research_evidence_count"], 4)
            self.assertEqual(audit["answer_closure_pages"], 24)
            self.assertEqual(audit["representation_authority"], ["SYMBOLIC"])
            self.assertTrue(audit["module_specific_hint_ladders"])
            self.assertEqual(audit["hint_ladder_count"], 8)
            self.assertTrue((Path(td) / "chemistry_core1b_hard_redox.pdf").exists())

    def test_each_module_has_a_distinct_conceptual_hint_ladder(self):
        ladders = [tuple(mod.module_hints(module)) for module in self.payload()["module_sequence"]]
        self.assertEqual(len(ladders), 8)
        self.assertEqual(len(set(ladders)), 8)
        self.assertIn("same element", " ".join(mod.module_hints("SPECIES_IDENTITY")).lower())
        self.assertIn("bookkeeping", " ".join(mod.module_hints("OXIDATION_STATE_MEANING")).lower())
        self.assertIn("electron", " ".join(mod.module_hints("ELECTRON_CONSEQUENCE")).lower())
        self.assertIn("agent", " ".join(mod.module_hints("AGENT_ROLE")).lower())
        self.assertIn("reconstruct", " ".join(mod.module_hints("FADING_TEACH_BACK")).lower())

    def test_module_sequence_is_fixed_for_this_production_golden(self):
        inp = self.payload()
        inp["module_sequence"] = list(reversed(inp["module_sequence"]))
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_HARD_MODULE_SEQUENCE_INVALID"):
            mod.v1.validate(inp)

    def test_particle_representation_cannot_be_added_locally(self):
        inp = self.payload()
        inp["representation_authority"] = ["SYMBOLIC", "PARTICLE"]
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_HARD_REPRESENTATION_AUTHORITY_DRIFT"):
            mod.v1.validate(inp)

    def test_learner_knowledge_cannot_control_hard_depth(self):
        inp = self.payload()
        inp["knowledge_percent"] = 40
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_KNOWLEDGE_CONTAMINATION"):
            mod.v1.validate(inp)

    def test_reaction_authority_is_frozen(self):
        inp = self.payload()
        inp["governed_facts"]["reaction"] = "NEW REACTION"
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_HARD_REACTION_AUTHORITY_DRIFT"):
            mod.v1.validate(inp)

    def test_deep_research_evidence_is_required(self):
        inp = self.payload()
        inp["research_evidence"] = inp["research_evidence"][:1]
        with self.assertRaisesRegex(ValueError, "CHEM_CORE1B_HARD_RESEARCH_EVIDENCE_INCOMPLETE"):
            mod.v1.validate(inp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
