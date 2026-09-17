from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location("compile_core1b", ROOT / "engine" / "compile_core1b.py")
mod = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)

class Core1BCompilerTests(unittest.TestCase):
    def load(self, family: str):
        return json.loads((ROOT / "golden" / family / "input.json").read_text(encoding="utf-8"))

    def test_equidistance_compiles_static_open_ended(self):
        out = mod.compile_plan(self.load("equidistant-point-on-axis"))
        self.assertEqual(out["delivery_mode"], "STATIC")
        self.assertEqual(out["pedagogy_mode"], "OPEN_ENDED")
        self.assertEqual(out["learner_role"], "RECONSTRUCT_AND_CONSOLIDATE")
        self.assertEqual(out["difficulty_governance"]["operational_badge"], "MEDIUM")
        self.assertTrue(out["quality_audit"]["attempt_precedes_explanation"])

    def test_every_substantive_block_gets_self_guided_frame(self):
        out = mod.compile_plan(self.load("linear-system-modelling")); required = set(mod.HELP_SEQUENCE)
        for block in out["blocks"]:
            if block["kind"] == "ANSWER_CHECK":
                self.assertNotIn("self_guided_frame", block); continue
            frame = block["self_guided_frame"]
            self.assertTrue(frame["attempt_first"]); self.assertEqual(set(frame["help_sequence"]), required); self.assertTrue(frame["concept_level_not_solution_dump"])

    def test_difficulty_governance_is_required(self):
        doc=self.load("equidistant-point-on-axis"); doc.pop("difficulty_governance")
        with self.assertRaisesRegex(ValueError,"CORE1B_DIFFICULTY_GOVERNANCE_MISSING"): mod.compile_plan(doc)

    def test_difficulty_consequence_cannot_drift(self):
        doc=self.load("equidistant-point-on-axis"); doc["difficulty_governance"]["page_ceiling"]=30
        with self.assertRaisesRegex(ValueError,"CORE1B_DIFFICULTY_CONSEQUENCE_DRIFT"): mod.compile_plan(doc)

    def test_derived_difficulty_must_match_dimensions(self):
        doc=self.load("equidistant-point-on-axis"); doc["difficulty_governance"]["derived_dimensions"]={k:4 for k in doc["difficulty_governance"]["derived_dimensions"]}
        with self.assertRaisesRegex(ValueError,"CORE1B_DERIVED_DIFFICULTY_MISMATCH"): mod.compile_plan(doc)

    def test_live_attempts_are_forbidden(self):
        doc=self.load("equidistant-point-on-axis"); doc["attempts"]=[]
        with self.assertRaisesRegex(ValueError,"CORE1B_LIVE_RUNTIME_FIELD_FORBIDDEN"): mod.compile_plan(doc)

    def test_new_math_is_forbidden(self):
        doc=self.load("equidistant-point-on-axis"); doc["blocks"][0]["new_math_refs"]=["MATH-UNTAUGHT-THEOREM"]
        with self.assertRaisesRegex(ValueError,"CORE1B_NEW_MATH_NOT_ALLOWED"): mod.compile_plan(doc)

    def test_unapproved_capability_is_forbidden(self):
        doc=self.load("linear-system-modelling"); doc["blocks"][0]["capability_refs"]=["MATH-QUADRATIC-FORMULA"]
        with self.assertRaisesRegex(ValueError,"CORE1B_UNAPPROVED_CAPABILITY_REF"): mod.compile_plan(doc)

    def test_close_independent_required(self):
        doc=self.load("equidistant-point-on-axis"); doc["blocks"]=[b for b in doc["blocks"] if b["kind"]!="CLOSE_INDEPENDENT"]
        with self.assertRaisesRegex(ValueError,"CORE1B_CLOSE_INDEPENDENT_MISSING"): mod.compile_plan(doc)

    def test_variation_may_not_change_multiple_critical_features_at_once(self):
        doc=self.load("linear-system-modelling"); row=next(b for b in doc["blocks"] if b["kind"]=="CONTROLLED_VARIATION")["rows"][1]; row["changed_features"]=["equation form","variable meaning"]
        with self.assertRaisesRegex(ValueError,"CORE1B_VARIATION_CHANGES_MULTIPLE_CRITICAL_FEATURES"): mod.compile_plan(doc)

if __name__ == "__main__": unittest.main(verbosity=2)
