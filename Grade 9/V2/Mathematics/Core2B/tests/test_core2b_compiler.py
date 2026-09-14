from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location("compile_core2b", ROOT / "engine" / "compile_core2b.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class Core2BCompilerTests(unittest.TestCase):
    def load(self, family: str):
        return json.loads((ROOT / "golden" / family / "input.json").read_text(encoding="utf-8"))

    def test_equidistance_compiles_static(self):
        out = mod.compile_plan(self.load("equidistant-point-on-axis"))
        self.assertEqual(out["delivery_mode"], "STATIC")
        self.assertEqual(out["compile_ceiling"], "M5_METHOD_DISCRIMINATION")
        self.assertTrue(out["quality_audit"]["all_items_core2a_legal"])

    def test_linear_system_compiles_same_engine(self):
        out = mod.compile_plan(self.load("linear-system-modelling"))
        self.assertEqual(out["delivery_mode"], "STATIC")
        self.assertEqual(out["items"][-1]["demand_level"], "M6_FAMILY_DISCRIMINATION")

    def test_live_attempts_are_forbidden(self):
        doc = self.load("equidistant-point-on-axis")
        doc["attempts"] = []
        with self.assertRaisesRegex(ValueError, "CORE2B_LIVE_RUNTIME_FIELD_FORBIDDEN"):
            mod.compile_plan(doc)

    def test_item_must_be_core2a_legal(self):
        doc = self.load("linear-system-modelling")
        doc["items"][0]["item_id"] = "NOT-LEGAL"
        with self.assertRaisesRegex(ValueError, "CORE2B_ITEM_NOT_CORE2A_LEGAL"):
            mod.compile_plan(doc)

    def test_ceiling_is_compile_time_gate(self):
        doc = self.load("equidistant-point-on-axis")
        doc["max_demand_level"] = "M2_REPRESENTATION_TRANSFER"
        with self.assertRaisesRegex(ValueError, "CORE2B_TRANSFER_EXCEEDS_COMPILE_CEILING"):
            mod.compile_plan(doc)

    def test_discrimination_family_label_must_be_hidden(self):
        doc = self.load("linear-system-modelling")
        item = next(x for x in doc["items"] if x["demand_level"] == "M5_METHOD_DISCRIMINATION")
        item["family_label_visible"] = True
        with self.assertRaisesRegex(ValueError, "CORE2B_FAMILY_LABEL_LEAK"):
            mod.compile_plan(doc)

    def test_unapproved_capability_fails(self):
        doc = self.load("equidistant-point-on-axis")
        doc["items"][0]["capability_refs"] = ["MATH-UNTaught-CAPABILITY"]
        with self.assertRaisesRegex(ValueError, "CORE2B_UNAPPROVED_CAPABILITY_REF"):
            mod.compile_plan(doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
