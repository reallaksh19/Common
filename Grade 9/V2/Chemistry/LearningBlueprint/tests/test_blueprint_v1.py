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

from common import BlueprintError  # noqa: E402
from compile_join import compile_join  # noqa: E402
from freeze_specialist_pass import freeze_specialist_pass  # noqa: E402
from run_blueprint_v1 import run_v1  # noqa: E402
from validate_specialist_relay import validate_specialist_relay  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class BlueprintV1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.specialist_schema = load(ROOT / "contracts" / "specialist-pass.schema.json")
        cls.validation_schema = load(ROOT / "contracts" / "validation-packet.schema.json")
        cls.join_schema = load(ROOT / "contracts" / "join-packet.schema.json")
        cls.fixtures = load(ROOT / "golden" / "v1-intelligence-goldens.json")["fixtures"]

    def materialize(self, fixture):
        data = copy.deepcopy(fixture)
        first_receipt = freeze_specialist_pass(data["first_pass"])
        second_receipt = freeze_specialist_pass(data["second_pass"])
        data["validation"]["first_pass_freeze_digest"] = first_receipt["freeze_digest"]
        data["validation"]["second_pass_freeze_digest"] = second_receipt["freeze_digest"]
        return data

    def execute(self, fixture):
        data = self.materialize(fixture)
        jsonschema.Draft202012Validator(self.specialist_schema).validate(data["first_pass"])
        jsonschema.Draft202012Validator(self.specialist_schema).validate(data["second_pass"])
        jsonschema.Draft202012Validator(self.validation_schema).validate(data["validation"])
        audit = validate_specialist_relay(data["first_pass"], data["second_pass"], data["validation"])
        join = compile_join(data["first_pass"], data["second_pass"], data["validation"])
        jsonschema.Draft202012Validator(self.join_schema).validate(join)
        return data, audit, join

    def test_v1_goldens_cover_both_orders_and_block_states(self):
        orders = set()
        states = set()
        for fixture in self.fixtures:
            data, audit, join = self.execute(fixture)
            orders.add((data["first_pass"]["role"], data["second_pass"]["role"]))
            states.add(join["join_state"])
            self.assertEqual(audit["status"], "PASS")
            self.assertTrue(audit["fresh_instance_verified"])
            self.assertTrue(audit["blind_grounding_verified"])
            self.assertTrue(audit["reveal_after_freeze_verified"])
            self.assertEqual(join["join_state"], fixture["expected_join_state"])
            self.assertEqual(
                sorted(row["capability_ref"] for row in join["obligations"]),
                sorted(fixture["expected_obligation_capabilities"]),
            )
            self.assertEqual(
                sorted(row["capability_ref"] for row in join["semantic_without_assessment_evidence"]),
                sorted(fixture["expected_semantic_without_assessment"]),
            )
        self.assertEqual(orders, {("CORE1", "CORE2"), ("CORE2", "CORE1")})
        self.assertEqual(states, {"READY_FOR_LEARNER_STATE", "BLOCK_CONFLICT", "BLOCK_MISSING_SEMANTIC_SUPPORT"})

    def test_v1_runner_obeys_v0_route_order(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "ASSESSMENT-FIRST-ALIGNED")
        data = self.materialize(fixture)
        result = run_v1(data["route"], data["first_pass"], data["second_pass"], data["validation"])
        self.assertEqual(result["manifest"]["first_specialist"], "CORE2")
        self.assertEqual(result["manifest"]["second_specialist"], "CORE1")
        self.assertEqual(result["manifest"]["status"], "PASS")

    def test_route_order_mismatch_fails(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "SEMANTIC-FIRST-ALIGNED")
        data = self.materialize(fixture)
        data["route"]["final_decision"] = "CORE2_FIRST"
        with self.assertRaises(BlueprintError) as ctx:
            run_v1(data["route"], data["first_pass"], data["second_pass"], data["validation"])
        self.assertEqual(ctx.exception.code, "BLUEPRINT_V1_ROUTE_ORDER_MISMATCH")

    def test_blind_pass_cannot_contain_upstream_packet_refs(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["second_pass"]["upstream_packet_refs"] = [fixture["first_pass"]["packet_id"]]
        with self.assertRaises(BlueprintError) as ctx:
            freeze_specialist_pass(fixture["second_pass"])
        self.assertEqual(ctx.exception.code, "SPECIALIST_BLIND_PASS_HAS_UPSTREAM_ACCESS")

    def test_fresh_instance_is_required(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "SEMANTIC-FIRST-ALIGNED")
        data = self.materialize(fixture)
        data["second_pass"]["instance_id"] = data["first_pass"]["instance_id"]
        data = self.materialize(data)
        with self.assertRaises(BlueprintError) as ctx:
            validate_specialist_relay(data["first_pass"], data["second_pass"], data["validation"])
        self.assertEqual(ctx.exception.code, "SPECIALIST_INSTANCE_REUSED")

    def test_reveal_before_second_freeze_fails(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "ASSESSMENT-FIRST-ALIGNED")
        data = self.materialize(fixture)
        data["validation"]["reveal_after_second_freeze"] = False
        with self.assertRaises(BlueprintError) as ctx:
            validate_specialist_relay(data["first_pass"], data["second_pass"], data["validation"])
        self.assertEqual(ctx.exception.code, "VALIDATION_REVEAL_BEFORE_SECOND_FREEZE")

    def test_every_upstream_claim_requires_one_comparison(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "SEMANTIC-FIRST-ALIGNED")
        data = self.materialize(fixture)
        data["validation"]["comparisons"] = data["validation"]["comparisons"][:-1]
        with self.assertRaises(BlueprintError) as ctx:
            validate_specialist_relay(data["first_pass"], data["second_pass"], data["validation"])
        self.assertEqual(ctx.exception.code, "VALIDATION_UPSTREAM_CLAIM_COVERAGE_INCOMPLETE")

    def test_semantic_without_question_demand_is_preserved_not_downgraded(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "SEMANTIC-FIRST-ALIGNED")
        _, _, join = self.execute(fixture)
        row = next(item for item in join["semantic_without_assessment_evidence"] if item["capability_ref"] == "CAP-GRAVITY-DIRECTION")
        self.assertEqual(row["interpretation"], "NO_ASSESSMENT_DEMAND_EVIDENCE_DOES_NOT_IMPLY_LOW_IMPORTANCE")

    def test_missing_semantic_support_blocks_join_without_inventing_support(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "ASSESSMENT-DEMAND-MISSING-SEMANTIC-SUPPORT")
        _, _, join = self.execute(fixture)
        self.assertEqual(join["join_state"], "BLOCK_MISSING_SEMANTIC_SUPPORT")
        self.assertEqual(join["assessment_without_semantic_support"][0]["capability_ref"], "CAP-HIDDEN-CONSTRAINT")

    def test_material_conflict_remains_visible(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "MATERIAL-CONFLICT-BLOCKS-JOIN")
        _, audit, join = self.execute(fixture)
        self.assertEqual(audit["material_conflict_claim_refs"], ["D-C1"])
        self.assertEqual(join["join_state"], "BLOCK_CONFLICT")
        self.assertIn("MATERIAL_CORE1_CORE2_CONFLICT", join["unresolved"])

    def test_deterministic_replay(self):
        fixture = next(row for row in self.fixtures if row["fixture_id"] == "ASSESSMENT-FIRST-ALIGNED")
        data1, audit1, join1 = self.execute(fixture)
        data2, audit2, join2 = self.execute(fixture)
        self.assertEqual(data1["validation"]["first_pass_freeze_digest"], data2["validation"]["first_pass_freeze_digest"])
        self.assertEqual(audit1["audit_digest"], audit2["audit_digest"])
        self.assertEqual(join1["digest"], join2["digest"])


if __name__ == "__main__":
    unittest.main()
