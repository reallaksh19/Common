from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema


KIT = Path(__file__).resolve().parents[1]
ENGINE = KIT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from build_product_packet import build_product_packet, validate_product_packet  # noqa: E402
from common import ProductionKitError  # noqa: E402
from learning_representation import build_representation_plan, validate_representation_plan  # noqa: E402
from source_answer_validator import validate_source_answer  # noqa: E402
from task_router import route_task  # noqa: E402


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ChemistryProductionKitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_set = load_json(KIT / "golden" / "fixtures.json")
        cls.fixtures = cls.fixture_set["fixtures"]
        cls.task_schema = load_json(KIT / "contracts" / "chemistry-production-task.schema.json")
        cls.question_schema = load_json(KIT / "contracts" / "chemistry-source-question.schema.json")
        cls.answer_schema = load_json(KIT / "contracts" / "chemistry-answer-record.schema.json")
        cls.packet_schema = load_json(KIT / "contracts" / "chemistry-product-packet.schema.json")

    def execute_fixture(self, fixture):
        task = copy.deepcopy(fixture["task"])
        questions = copy.deepcopy(fixture["questions"])
        answers = copy.deepcopy(fixture["answers"])

        jsonschema.Draft202012Validator(self.task_schema).validate(task)
        for question in questions:
            jsonschema.Draft202012Validator(self.question_schema).validate(question)
        for answer in answers:
            jsonschema.Draft202012Validator(self.answer_schema).validate(answer)

        route = route_task(task)
        audit = validate_source_answer(task, route, questions, answers)
        reps = build_representation_plan(task, route, questions)
        validate_representation_plan(reps, questions)
        packet = build_product_packet(task, route, questions, answers, reps)
        validate_product_packet(task, route, packet)
        jsonschema.Draft202012Validator(self.packet_schema).validate(packet)
        return route, audit, reps, packet

    def test_multiple_goldens_cover_all_products_and_core2a_modes(self):
        products = set()
        modes = set()
        per_product_count = {}
        for fixture in self.fixtures:
            route, audit, reps, packet = self.execute_fixture(fixture)
            product = fixture["task"]["product"]
            products.add(product)
            per_product_count[product] = per_product_count.get(product, 0) + 1
            self.assertEqual(audit["status"], "PASS")
            self.assertEqual(len(packet["questions"]), len(fixture["task"]["question_refs"]))
            self.assertEqual(len(reps["question_plans"]), len(fixture["task"]["question_refs"]))
            if product == "CORE2A":
                modes.add(fixture["task"]["purpose"])
                for question_packet in packet["questions"]:
                    self.assertLessEqual(len(question_packet["sheets"]), 2)
                    sheet1_types = [b["type"] for b in question_packet["sheets"][0]["blocks"]]
                    self.assertIn("SOURCE", sheet1_types)
            self.assertEqual(route["product"], product)

        self.assertEqual(products, {"CORE1", "CORE2", "CORE1A", "CORE2A"})
        self.assertEqual(modes, {"STARTER", "PRACTICE", "REVISION", "COMPETITION"})
        self.assertGreaterEqual(per_product_count["CORE1"], 2)
        self.assertGreaterEqual(per_product_count["CORE2"], 2)
        self.assertGreaterEqual(per_product_count["CORE1A"], 2)
        self.assertGreaterEqual(per_product_count["CORE2A"], 4)

    def test_competition_sheet1_has_question_specific_source_and_technical_clues(self):
        fixture = next(f for f in self.fixtures if f["fixture_id"] == "CORE2A-COMPETITION")
        _, _, _, packet = self.execute_fixture(fixture)
        sheet1 = packet["questions"][0]["sheets"][0]
        blocks = sheet1["blocks"]
        self.assertEqual(blocks[0]["type"], "SOURCE")
        self.assertIn("SOF", blocks[0]["text"])
        self.assertIn("HBCSE", blocks[0]["text"])
        self.assertEqual(blocks[-1]["type"], "TECHNICAL_CLUES")
        self.assertEqual(len(blocks[-1]["clues"]), 2)
        self.assertTrue(any("2q" in clue for clue in blocks[-1]["clues"]))

    def test_workspace_is_demand_sized_not_fixed(self):
        starter = next(f for f in self.fixtures if f["fixture_id"] == "CORE2A-STARTER")
        revision = next(f for f in self.fixtures if f["fixture_id"] == "CORE2A-REVISION")
        _, _, _, starter_packet = self.execute_fixture(starter)
        _, _, _, revision_packet = self.execute_fixture(revision)
        self.assertNotEqual(
            starter_packet["questions"][0]["workspace_mm"],
            revision_packet["questions"][0]["workspace_mm"],
        )
        self.assertLess(revision_packet["questions"][0]["workspace_mm"], 40)

    def test_core2a_unresolved_purpose_fails_closed(self):
        fixture = copy.deepcopy(next(f for f in self.fixtures if f["fixture_id"] == "CORE2A-PRACTICE"))
        fixture["task"]["purpose"] = None
        with self.assertRaises(ProductionKitError) as ctx:
            route_task(fixture["task"])
        self.assertEqual(ctx.exception.code, "CORE2A_PURPOSE_UNRESOLVED")

    def test_core2a_sheet1_source_cannot_be_disabled(self):
        fixture = copy.deepcopy(next(f for f in self.fixtures if f["fixture_id"] == "CORE2A-REVISION"))
        fixture["task"]["constraints"]["source_on_sheet1"] = False
        with self.assertRaises(ProductionKitError) as ctx:
            route_task(fixture["task"])
        self.assertEqual(ctx.exception.code, "CORE2A_SHEET1_SOURCE_MISSING")

    def test_missing_answer_fails_closure(self):
        fixture = copy.deepcopy(next(f for f in self.fixtures if f["fixture_id"] == "CORE2-SOURCE-MCQ"))
        route = route_task(fixture["task"])
        with self.assertRaises(ProductionKitError) as ctx:
            validate_source_answer(fixture["task"], route, fixture["questions"], [])
        self.assertEqual(ctx.exception.code, "ANSWER_DENOMINATOR_MISMATCH")

    def test_unknown_representation_capability_fails(self):
        fixture = copy.deepcopy(next(f for f in self.fixtures if f["fixture_id"] == "CORE1-FORMULA-TEACH"))
        fixture["questions"][0]["capability_refs"] = ["CAP-NOT-REGISTERED"]
        route = route_task(fixture["task"])
        validate_source_answer(fixture["task"], route, fixture["questions"], fixture["answers"])
        with self.assertRaises(ProductionKitError) as ctx:
            build_representation_plan(fixture["task"], route, fixture["questions"])
        self.assertEqual(ctx.exception.code, "REPRESENTATION_CAPABILITY_UNMAPPED")

    def test_deterministic_replay(self):
        fixture = next(f for f in self.fixtures if f["fixture_id"] == "CORE2A-COMPETITION")
        first = self.execute_fixture(fixture)
        second = self.execute_fixture(fixture)
        self.assertEqual(first[0]["route_digest"], second[0]["route_digest"])
        self.assertEqual(first[1]["audit_digest"], second[1]["audit_digest"])
        self.assertEqual(first[2]["representation_plan_digest"], second[2]["representation_plan_digest"])
        self.assertEqual(first[3]["packet_digest"], second[3]["packet_digest"])


if __name__ == "__main__":
    unittest.main()
