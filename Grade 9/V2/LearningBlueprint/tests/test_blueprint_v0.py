from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from apply_owner_override import apply_owner_override  # noqa: E402
from common import BlueprintError  # noqa: E402
from freeze_ground_truth import freeze_ground_truth  # noqa: E402
from route_evidence import route_evidence  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class BlueprintV0Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gt_schema = load(ROOT / "contracts" / "ground-truth-manifest.schema.json")
        cls.routing_schema = load(ROOT / "contracts" / "routing-input.schema.json")
        cls.route_packet_schema = load(ROOT / "contracts" / "routing-decision.schema.json")
        cls.override_schema = load(ROOT / "contracts" / "owner-override.schema.json")
        cls.packet_schema = load(ROOT / "contracts" / "packet-envelope.schema.json")
        cls.goldens = load(ROOT / "golden" / "routing-goldens.json")["fixtures"]

    def validate_route_packet(self, route):
        route_schema = copy.deepcopy(self.route_packet_schema)
        route_schema["allOf"][0] = copy.deepcopy(self.packet_schema)
        jsonschema.Draft202012Validator(route_schema).validate(route)

    def test_all_routing_goldens(self):
        decisions = set()
        for fixture in self.goldens:
            jsonschema.Draft202012Validator(self.gt_schema).validate(fixture["ground_truth"])
            jsonschema.Draft202012Validator(self.routing_schema).validate(fixture["routing_input"])
            frozen = freeze_ground_truth(copy.deepcopy(fixture["ground_truth"]))
            route = route_evidence(copy.deepcopy(fixture["ground_truth"]), copy.deepcopy(fixture["routing_input"]))
            if "override" in fixture:
                jsonschema.Draft202012Validator(self.override_schema).validate(fixture["override"])
                route = apply_owner_override(route, copy.deepcopy(fixture["override"]))
            decisions.add(route["system_decision"])
            self.assertEqual(route["system_decision"], fixture["expected_system_decision"], fixture["fixture_id"])
            self.assertEqual(route["final_decision"], fixture["expected_final_decision"], fixture["fixture_id"])
            self.validate_route_packet(route)
            if "expected_assessment_interpretation" in fixture:
                self.assertEqual(frozen["assessment_evidence_interpretation"], fixture["expected_assessment_interpretation"])

        self.assertEqual(decisions, {"CORE1_FIRST", "CORE2_FIRST", "BLOCK_INSUFFICIENT_EVIDENCE", "BLOCK_CONFLICT"})

    def test_zero_questions_is_not_zero_importance(self):
        fixture = next(f for f in self.goldens if f["fixture_id"] == "SUPPLIED-ZERO-QUESTION-CORPUS")
        frozen = freeze_ground_truth(copy.deepcopy(fixture["ground_truth"]))
        self.assertEqual(frozen["assessment_evidence_interpretation"], "NO_ASSESSMENT_ITEMS_IN_SUPPLIED_CORPUS")
        encoded = json.dumps(frozen)
        self.assertNotIn("exam_importance", encoded)
        self.assertNotIn("exam_frequency", encoded)

    def test_ground_truth_contract_rejects_derived_exam_claim(self):
        fixture = copy.deepcopy(self.goldens[0]["ground_truth"])
        fixture["exam_importance"] = 0
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.gt_schema).validate(fixture)

    def test_handoff_more_than_three_subtopics_fails(self):
        fixture = copy.deepcopy(self.goldens[0])
        fixture["routing_input"]["subtopic_refs"] = ["A", "B", "C", "D"]
        with self.assertRaises(BlueprintError) as ctx:
            route_evidence(fixture["ground_truth"], fixture["routing_input"])
        self.assertEqual(ctx.exception.code, "HANDOFF_SUBTOPIC_BOUND_INVALID")

    def test_handoff_bound_does_not_create_learning_atom_limit(self):
        invariants = load(ROOT / "BLUEPRINT_INVARIANTS.json")
        rules = {row["rule"] for row in invariants["invariants"]}
        self.assertIn("HANDOFF_BUNDLE_MAXIMUM_IS_THREE_SUBTOPICS_ONLY_AND_DOES_NOT_LIMIT_LEARNING_ATOMS", rules)

    def test_absent_evidence_cannot_have_refs(self):
        fixture = copy.deepcopy(self.goldens[0]["ground_truth"])
        fixture["evidence"]["question_corpus"] = {
            "state": "ABSENT",
            "refs": [{"ref_id": "BAD", "location": "fixture://bad", "authority_class": "USER_SUPPLIED", "integrity_state": "CLEAN"}]
        }
        with self.assertRaises(BlueprintError) as ctx:
            freeze_ground_truth(fixture)
        self.assertEqual(ctx.exception.code, "ABSENT_EVIDENCE_HAS_SOURCE_REFS")

    def test_owner_override_preserves_system_finding(self):
        fixture = copy.deepcopy(next(f for f in self.goldens if f["fixture_id"] == "HARD-OWNER-ROUTE-OVERRIDE"))
        route = route_evidence(fixture["ground_truth"], fixture["routing_input"])
        overridden = apply_owner_override(route, fixture["override"])
        self.assertEqual(overridden["system_decision"], "CORE1_FIRST")
        self.assertEqual(overridden["final_decision"], "CORE2_FIRST")
        self.assertEqual(overridden["override_audit"]["system_finding"], "CORE1_FIRST")
        self.assertTrue(overridden["override_audit"]["applied"])
        self.validate_route_packet(overridden)

    def test_soft_override_cannot_bypass_block(self):
        fixture = copy.deepcopy(next(f for f in self.goldens if f["fixture_id"] == "SOFT-OVERRIDE-CANNOT-BYPASS-CONFLICT"))
        route = route_evidence(fixture["ground_truth"], fixture["routing_input"])
        overridden = apply_owner_override(route, fixture["override"])
        self.assertEqual(overridden["system_decision"], "BLOCK_CONFLICT")
        self.assertEqual(overridden["final_decision"], "BLOCK_CONFLICT")
        self.assertFalse(overridden["override_audit"]["applied"])
        self.validate_route_packet(overridden)

    def test_deterministic_replay(self):
        fixture = copy.deepcopy(next(f for f in self.goldens if f["fixture_id"] == "COARSE-SYLLABUS-RICH-QUESTIONS"))
        a = route_evidence(fixture["ground_truth"], fixture["routing_input"])
        b = route_evidence(fixture["ground_truth"], fixture["routing_input"])
        self.assertEqual(a["digest"], b["digest"])


if __name__ == "__main__":
    unittest.main()
