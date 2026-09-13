from __future__ import annotations

import copy, json, sys, unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))
from common import BlueprintError
from compile_learner_state import compile_learner_state
from compile_purpose import compile_purpose
from compile_assimilation import compile_assimilation
from compile_taught_state import compile_taught_state
from run_blueprint_v2 import run_v2


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class BlueprintV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = load(ROOT / "golden" / "v2-assimilation-goldens.json")["fixtures"]
        cls.schemas = {name: load(ROOT / "contracts" / name) for name in [
            "learner-input.schema.json", "purpose-input.schema.json", "assimilation-design.schema.json",
            "learner-state.schema.json", "purpose-packet.schema.json", "assimilation-bundle.schema.json", "taught-state.schema.json"
        ]}

    def execute(self, fixture):
        return run_v2(copy.deepcopy(fixture["join"]), copy.deepcopy(fixture["learner"]), copy.deepcopy(fixture["purpose"]), copy.deepcopy(fixture["design"]))

    def test_multiple_goldens_cover_readiness_and_purpose(self):
        purposes, depths = set(), set()
        for fixture in self.fixtures:
            jsonschema.Draft202012Validator(self.schemas["learner-input.schema.json"]).validate(fixture["learner"])
            jsonschema.Draft202012Validator(self.schemas["purpose-input.schema.json"]).validate(fixture["purpose"])
            jsonschema.Draft202012Validator(self.schemas["assimilation-design.schema.json"]).validate(fixture["design"])
            result = self.execute(fixture)
            purposes.add(result["purpose"]["mode"])
            depths.add(result["learner_state"]["scaffold_depth"])
            jsonschema.Draft202012Validator(self.schemas["learner-state.schema.json"]).validate(result["learner_state"])
            jsonschema.Draft202012Validator(self.schemas["purpose-packet.schema.json"]).validate(result["purpose"])
            jsonschema.Draft202012Validator(self.schemas["assimilation-bundle.schema.json"]).validate(result["assimilation"])
            self.assertTrue(result["assimilation"]["manuscript_ready"])
            atoms = sum(len(row["learning_atoms"]) for row in result["assimilation"]["capability_treatments"])
            self.assertGreaterEqual(atoms, fixture["expected"]["min_atoms"])
        self.assertEqual(purposes, {"FIRST_STUDY", "REVISION", "COMPETITIVE_EXAM"})
        self.assertEqual(depths, {"DEEP", "MODERATE", "LIGHT"})

    def test_readiness_prior_is_not_fabricated_diagnosis(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "GRAVITY-LOW-FIRST-STUDY")
        state = compile_learner_state(fixture["join"], fixture["learner"])
        self.assertEqual(state["prior_interpretation"], "PRIOR_ONLY_NOT_DIAGNOSIS")
        self.assertTrue(all(row["state"] == "UNKNOWN" for row in state["capabilities"]))

    def test_blocked_join_cannot_compile(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["join"]["join_state"] = "BLOCK_CONFLICT"
        with self.assertRaises(BlueprintError) as ctx:
            compile_learner_state(fixture["join"], fixture["learner"])
        self.assertEqual(ctx.exception.code, "ASSIMILATION_JOIN_NOT_READY")

    def test_purpose_is_mandatory(self):
        with self.assertRaises(BlueprintError) as ctx:
            compile_purpose({"purpose_request_id": "X", "mode": None})
        self.assertEqual(ctx.exception.code, "LEARNING_PURPOSE_UNRESOLVED")

    def test_more_than_three_learning_atoms_is_allowed(self):
        result = self.execute(self.fixtures[0])
        self.assertGreater(len(result["assimilation"]["capability_treatments"][0]["learning_atoms"]), 3)

    def test_low_readiness_unbridged_jump_fails(self):
        fixture = copy.deepcopy(self.fixtures[0])
        step = fixture["design"]["capability_treatments"][0]["inference_chain"]["steps"][0]
        step["bridge_required"], step["bridge"] = False, ""
        learner = compile_learner_state(fixture["join"], fixture["learner"])
        purpose = compile_purpose(fixture["purpose"])
        with self.assertRaises(BlueprintError) as ctx:
            compile_assimilation(fixture["join"], learner, purpose, fixture["design"])
        self.assertEqual(ctx.exception.code, "INFERENCE_JUMP_UNBRIDGED")

    def test_important_equation_without_anatomy_fails(self):
        fixture = copy.deepcopy(self.fixtures[0])
        del fixture["design"]["capability_treatments"][0]["equations"][0]["validity_limits"]
        learner = compile_learner_state(fixture["join"], fixture["learner"])
        purpose = compile_purpose(fixture["purpose"])
        with self.assertRaises(BlueprintError) as ctx:
            compile_assimilation(fixture["join"], learner, purpose, fixture["design"])
        self.assertEqual(ctx.exception.code, "IMPORTANT_EQUATION_ANATOMY_INCOMPLETE")

    def test_representation_without_cognitive_requirement_fails(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["design"]["capability_treatments"][0]["representations"][0]["requirement"]["must_not_imply"] = ""
        learner = compile_learner_state(fixture["join"], fixture["learner"])
        purpose = compile_purpose(fixture["purpose"])
        with self.assertRaises(BlueprintError) as ctx:
            compile_assimilation(fixture["join"], learner, purpose, fixture["design"])
        self.assertEqual(ctx.exception.code, "REPRESENTATION_COGNITIVE_REQUIREMENT_INCOMPLETE")

    def test_representation_candidate_competition_required(self):
        fixture = copy.deepcopy(self.fixtures[0])
        rep = fixture["design"]["capability_treatments"][0]["representations"][0]
        rep["candidates"] = rep["candidates"][:1]
        rep["single_candidate_waiver"] = None
        learner = compile_learner_state(fixture["join"], fixture["learner"])
        purpose = compile_purpose(fixture["purpose"])
        with self.assertRaises(BlueprintError) as ctx:
            compile_assimilation(fixture["join"], learner, purpose, fixture["design"])
        self.assertEqual(ctx.exception.code, "REPRESENTATION_CANDIDATE_COMPETITION_MISSING")

    def test_purpose_cannot_enable_prerequisite_bypass(self):
        fixture = self.fixtures[1]
        learner = compile_learner_state(fixture["join"], fixture["learner"])
        purpose = compile_purpose(fixture["purpose"])
        purpose["prerequisite_bypass_allowed"] = True
        with self.assertRaises(BlueprintError) as ctx:
            compile_assimilation(fixture["join"], learner, purpose, fixture["design"])
        self.assertEqual(ctx.exception.code, "PURPOSE_PREREQUISITE_BYPASS_FORBIDDEN")

    def test_taught_state_requires_realization_evidence(self):
        assimilation = self.execute(self.fixtures[1])["assimilation"]
        cap = assimilation["capability_treatments"][0]["capability_ref"]
        flags = ["taught", "represented", "worked", "faded", "independent", "checked"]
        realization = {"realization_id": "ION-R1", "capabilities": [{"capability_ref": cap, **{flag: True for flag in flags}, "evidence_refs": {flag: [f"ART-{flag}"] for flag in flags}}]}
        taught = compile_taught_state(assimilation, realization)
        jsonschema.Draft202012Validator(self.schemas["taught-state.schema.json"]).validate(taught)
        self.assertEqual(len(taught["capabilities"]), 1)
        bad = copy.deepcopy(realization)
        bad["capabilities"][0]["evidence_refs"]["independent"] = []
        with self.assertRaises(BlueprintError) as ctx:
            compile_taught_state(assimilation, bad)
        self.assertEqual(ctx.exception.code, "TAUGHT_STATE_POSITIVE_WITHOUT_EVIDENCE")

    def test_independent_without_check_cannot_be_receipted(self):
        assimilation = self.execute(self.fixtures[2])["assimilation"]
        cap = assimilation["capability_treatments"][0]["capability_ref"]
        realization = {"realization_id": "R", "capabilities": [{"capability_ref": cap, "taught": True, "represented": True, "worked": True, "faded": True, "independent": True, "checked": False, "evidence_refs": {"taught": ["A"], "represented": ["B"], "worked": ["C"], "faded": ["D"], "independent": ["E"]}}]}
        with self.assertRaises(BlueprintError) as ctx:
            compile_taught_state(assimilation, realization)
        self.assertEqual(ctx.exception.code, "TAUGHT_STATE_INDEPENDENT_WITHOUT_CHECK")

    def test_same_topic_different_purpose_changes_contract_not_truth(self):
        first_study = self.execute(self.fixtures[0])
        revision = self.execute(self.fixtures[2])
        self.assertNotEqual(first_study["purpose"]["terminal_capabilities"], revision["purpose"]["terminal_capabilities"])
        self.assertIn("CAP-APEX-STATE", {row["capability_ref"] for row in first_study["assimilation"]["capability_treatments"]})
        self.assertIn("CAP-APEX-STATE", {row["capability_ref"] for row in revision["assimilation"]["capability_treatments"]})

    def test_deterministic_replay(self):
        first = self.execute(self.fixtures[1])
        second = self.execute(self.fixtures[1])
        self.assertEqual(first["manifest"]["digest"], second["manifest"]["digest"])
        self.assertEqual(first["assimilation"]["digest"], second["assimilation"]["digest"])


if __name__ == "__main__":
    unittest.main()
