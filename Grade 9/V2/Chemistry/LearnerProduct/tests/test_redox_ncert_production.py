from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
LP = HERE.parents[1]
CHEM = LP.parent
REDOX = LP / "production" / "redox"
sys.path.insert(0, str(LP / "engine"))
sys.path.insert(0, str(REDOX))

import run_chemistry_ncert_production as production_runner  # noqa: E402
import build_redox_production_inputs as redox  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class RedoxNCERTProductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = redox.build_all()
        cls.answer_schema = load(LP / "contracts" / "chemistry-answer-path.schema.json")
        cls.provenance_schema = load(LP / "contracts" / "chemistry-question-provenance.schema.json")
        cls.source_item_schema = load(CHEM / "Core2A" / "contracts" / "chemistry-core2a-source-item.schema.json")

    def test_frozen_source_denominator_and_response_modes(self):
        core2 = self.bundle["core2"]
        self.assertEqual(len(core2["pages"]), 11)
        self.assertEqual(core2["summary"]["response_mode_counts"], {"CONSTRUCTED_RESPONSE": 6, "MCQ": 5})
        self.assertEqual([p["question_ref"] for p in core2["pages"]], [
            "U2Q2", "U2Q6", "U2Q7", "U2Q15C", "U2Q18B", "U2Q29A",
            "U2Q30F", "U2Q35", "U2Q38C", "SP1Q3", "SP2Q2",
        ])
        closure = self.bundle["closure"]["external_matrix"]["summary"]
        self.assertEqual(closure["eligible_total"], 11)
        self.assertEqual(closure["placed_unique_total"], 11)
        self.assertEqual(closure["missing_total"], 0)
        self.assertEqual(closure["duplicate_primary_total"], 0)

    def test_redox_depth_extension_is_explicit_not_extra_source_questions(self):
        profile = self.bundle["production_profile"]
        self.assertEqual(profile["source_question_denominator"], 11)
        extension = [
            cap for cap in profile["capability_order"]
            if profile["capabilities"][cap]["scope_class"] == "REDOX_DEPTH_EXTENSION"
        ]
        self.assertEqual(extension, [
            "CAP-TRACK-REACTING-SPECIES",
            "CAP-ATTACH-SPECIES-ROLE",
            "CAP-TRACK-OXIDATION-STATE",
        ])
        self.assertIn("PCK-REDOX-SELF-OTHER", profile["capabilities"]["CAP-ATTACH-SPECIES-ROLE"]["pck_asset_refs"])
        self.assertIn("PCK-REDOX-OXIDATION-LANE", profile["capabilities"]["CAP-TRACK-OXIDATION-STATE"]["pck_asset_refs"])
        ox = [r for r in self.bundle["representations"]["representations"] if r["primitive_id"] == "OXIDATION_STATE_LANE"]
        self.assertEqual(len(ox), 1)
        self.assertEqual(len(ox[0]["source_semantic_data"]["oxidation_states"]), 2)

    def test_semantic_run_closes_all_eleven_answer_paths_without_fake_options(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            package, _ = production_runner.execute_production(
                self.bundle["run"], self.bundle["study_model"], self.bundle["core1"],
                self.bundle["representations"], self.bundle["core2"], self.bundle["closure"],
                out, semantic_only=True,
            )
            self.assertEqual(package["semantic_complete_through"], "VALIDATE_ANSWER_CLOSURE")
            source_plan = load(out / "core2a_source_plan.json")
            self.assertEqual(source_plan["summary"]["source_questions_required"], 11)
            self.assertEqual(source_plan["summary"]["source_questions_realized"], 11)
            self.assertEqual(source_plan["summary"]["quick_checks_realized"], 11)
            self.assertEqual(source_plan["summary"]["full_workings_realized"], 11)
            by_ref = {item["question_ref"]: item for item in source_plan["items"]}
            for qid in ["U2Q15C", "U2Q18B", "U2Q29A", "U2Q30F", "U2Q35", "U2Q38C"]:
                item = by_ref[qid]
                self.assertEqual(item["source_snapshot"]["response_mode"], "CONSTRUCTED_RESPONSE")
                self.assertEqual(item["source_snapshot"]["options"], [])
                self.assertTrue(item["answer_path"]["quick_check"]["answer_summary"])
                self.assertTrue(item["answer_path"]["quick_check"]["marking_points"])
                self.assertTrue(item["answer_path"]["full_working"]["steps"])
            for item in source_plan["items"]:
                Draft202012Validator(self.source_item_schema).validate(item)
                Draft202012Validator(self.answer_schema).validate(item["answer_path"])
                Draft202012Validator(self.provenance_schema).validate(item["provenance"])
                self.assertEqual(item["provenance"]["citations"][0]["locator"], item["source_snapshot"]["source_locator"])

    def test_real_redox_run_reaches_frozen_handoff(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            production_runner.execute_production(
                self.bundle["run"], self.bundle["study_model"], self.bundle["core1"],
                self.bundle["representations"], self.bundle["core2"], self.bundle["closure"],
                out, semantic_only=False,
            )
            final_audit = load(out / "final_audit.json")
            handoff = load(out / "handoff_manifest.json")
            answer = load(out / "answer_closure_audit.json")
            self.assertEqual(final_audit["machine_status"], "PASS")
            self.assertFalse(final_audit["release_authorized"])
            self.assertEqual(handoff["status"], "MACHINE_COMPLETE_HUMAN_REVIEW_PENDING")
            self.assertEqual(answer["counts"]["objective_questions_total"], 11)
            self.assertEqual(answer["counts"]["quick_checks_total"], 11)
            self.assertEqual(answer["counts"]["full_workings_total"], 11)
            self.assertTrue((out / "chemistry_core1a.pdf").is_file())
            self.assertTrue((out / "chemistry_core2a.pdf").is_file())
            self.assertTrue((out / "production_baseline_binding.json").is_file())


if __name__ == "__main__":
    unittest.main()
