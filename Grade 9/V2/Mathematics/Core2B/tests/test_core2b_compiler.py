from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve(); ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location("compile_core2b", ROOT / "engine" / "compile_core2b.py")
mod = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)

class Core2BCompilerTests(unittest.TestCase):
    def load(self, family: str):
        return json.loads((ROOT / "golden" / family / "input.json").read_text(encoding="utf-8"))

    def test_equidistance_compiles_static_open_ended(self):
        out=mod.compile_plan(self.load("equidistant-point-on-axis"))
        self.assertEqual(out["delivery_mode"],"STATIC"); self.assertEqual(out["pedagogy_mode"],"OPEN_ENDED")
        self.assertEqual(out["learner_role"],"SELECT_TRANSFER_DISCRIMINATE_SYNTHESIZE")
        self.assertEqual(out["compile_ceiling"],"M5_METHOD_DISCRIMINATION")
        self.assertTrue(out["quality_audit"]["learner_calibration_bound"]); self.assertTrue(out["quality_audit"]["question_custody_complete"])

    def test_every_item_gets_transfer_help_frame(self):
        out=mod.compile_plan(self.load("linear-system-modelling")); required=set(mod.HELP_SEQUENCE)
        for item in out["items"]:
            frame=item["self_guided_frame"]; self.assertTrue(frame["attempt_first"]); self.assertEqual(set(frame["help_sequence"]),required); self.assertTrue(frame["concept_level_not_solution_dump"])

    def test_generation_calibration_is_required(self):
        doc=self.load("equidistant-point-on-axis"); doc.pop("generation_calibration")
        with self.assertRaisesRegex(ValueError,"CORE2B_GENERATION_CALIBRATION_MISSING"): mod.compile_plan(doc)

    def test_percentage_path_requires_capability_knowledge(self):
        doc=self.load("equidistant-point-on-axis"); doc["generation_calibration"]["calibration_basis"]["capability_knowledge"]=[]
        with self.assertRaisesRegex(ValueError,"CORE2B_CAPABILITY_KNOWLEDGE_REQUIRED"): mod.compile_plan(doc)

    def test_item_capability_must_have_knowledge_when_percent_path_used(self):
        doc=self.load("equidistant-point-on-axis"); doc["generation_calibration"]["calibration_basis"]["capability_knowledge"]=[{"capability_ref":"MATH-EQUIDISTANT-POINT-ON-AXIS","percent":75}]
        with self.assertRaisesRegex(ValueError,"CORE2B_ITEM_CAPABILITY_KNOWLEDGE_MISSING"): mod.compile_plan(doc)

    def test_owner_override_can_replace_percentage(self):
        doc=self.load("equidistant-point-on-axis")
        doc["generation_calibration"]["calibration_basis"]={"type":"OWNER_OVERRIDE","owner_ref":"OWNER-1","reason":"Diagnostic knowledge percentage unavailable for this learner."}
        mod.compile_plan(doc)

    def test_item_must_be_core2a_legal(self):
        doc=self.load("linear-system-modelling"); doc["items"][0]["core2a_item_ref"]="NOT-LEGAL"
        with self.assertRaisesRegex(ValueError,"CORE2B_ITEM_NOT_CORE2A_LEGAL"): mod.compile_plan(doc)

    def test_ceiling_is_compile_time_gate(self):
        doc=self.load("equidistant-point-on-axis"); doc["max_demand_level"]="M2_REPRESENTATION_TRANSFER"
        with self.assertRaisesRegex(ValueError,"CORE2B_TRANSFER_EXCEEDS_COMPILE_CEILING"): mod.compile_plan(doc)

    def test_discrimination_family_label_must_be_hidden(self):
        doc=self.load("linear-system-modelling"); item=next(x for x in doc["items"] if x["demand_level"]=="M5_METHOD_DISCRIMINATION"); item["family_label_visible"]=True
        with self.assertRaisesRegex(ValueError,"CORE2B_FAMILY_LABEL_LEAK"): mod.compile_plan(doc)

    def test_question_answer_contract_is_required(self):
        doc=self.load("equidistant-point-on-axis"); doc["items"][0]["answer_contract_ref"]=""
        with self.assertRaisesRegex(ValueError,"CORE2B_QUESTION_CUSTODY_INCOMPLETE"): mod.compile_plan(doc)

    def test_generated_question_cannot_masquerade_as_source(self):
        doc=self.load("equidistant-point-on-axis"); item=doc["items"][0]; item["source_question_no"]="Q1"; item["source_relation"]="EXACT_SOURCE"
        with self.assertRaisesRegex(ValueError,"CORE2B_GENERATED_MASQUERADES_AS_SOURCE"): mod.compile_plan(doc)

    def test_generated_lineage_required_for_structural_sibling(self):
        doc=self.load("linear-system-modelling"); item=doc["items"][1]; item["parent_question_refs"]=[]
        with self.assertRaisesRegex(ValueError,"CORE2B_GENERATED_LINEAGE_MISSING"): mod.compile_plan(doc)

    def test_unverified_official_claim_fails(self):
        doc=self.load("linear-system-modelling"); item=doc["items"][0]; item["official_past_question_claim"]=True
        with self.assertRaisesRegex(ValueError,"CORE2B_UNVERIFIED_OFFICIAL_CLAIM"): mod.compile_plan(doc)

    def test_hidden_structure_answer_is_mathematically_verified(self):
        doc=self.load("equidistant-point-on-axis"); item=next(x for x in doc["items"] if x["item_id"]=="B-EQ-H1"); self.assertEqual(item["answer_check"],"x=1/4; P=(1/4,0).")
        x=1/4; self.assertEqual((x+3)**2+16,(x-5)**2+4)

if __name__ == "__main__": unittest.main(verbosity=2)
