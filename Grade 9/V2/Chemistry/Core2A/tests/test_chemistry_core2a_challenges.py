#!/usr/bin/env python3
import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
CORE2A = HERE.parents[1]
CHEM = CORE2A.parent
REPO = CHEM.parents[2]
CORE1A = CHEM / "Core1A"
LP = CHEM / "LearnerProduct"

sys.path.insert(0, str(CORE2A / "engine"))
sys.path.insert(0, str(CORE1A / "engine"))
sys.path.insert(0, str(CHEM / "ColdStart" / "engine"))

from build_chemistry_core1a_bucket_plan import build_bucket_plan  # noqa: E402
from build_chemistry_core2a_source import build_source_plan  # noqa: E402
from build_chemistry_core2a_challenges import (  # noqa: E402
    build_challenge_plan,
    digest,
    validate_challenge_plan,
)
from chemistry_cold_start_runner import run_cold_start  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def redigest_item(item):
    item["item_digest"] = ""
    item["item_digest"] = digest(item, "item_digest")


def redigest_plan(plan):
    plan["plan_digest"] = ""
    plan["plan_digest"] = digest(plan, "plan_digest")
    return plan


class ChemistryCore2AChallengeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures = CHEM / "AssessmentIntake" / "fixtures"
        sources = load(fixtures / "mixed-chemistry-source.fixture.json")
        questions = load(fixtures / "mixed-chemistry-question-set.fixture.json")
        corpus = load(fixtures / "mixed-chemistry-external-corpus.fixture.json")
        topic = load(fixtures / "mixed-chemistry-topic-scope.fixture.json")
        _, internals = run_cold_start(
            copy.deepcopy(sources), copy.deepcopy(questions), copy.deepcopy(corpus), copy.deepcopy(topic),
            repo_root=REPO, run_id="CHEM-C2A-CHALLENGE-INTEGRATION-RUN",
        )
        cls.family_registry = load(CHEM / "ReasoningSemantics" / "registry" / "chemistry-problem-family-registry.json")
        cls.core1a_policy = load(CORE1A / "policies" / "chemistry-core1a-bucket-synthesis-policy.json")
        cls.bucket_plan = build_bucket_plan(
            internals["study_model"], internals["core1"], internals["representations"], internals["core2"],
            cls.family_registry, cls.core1a_policy, "CHEM-C1A-BP-CHALLENGE-INTEGRATION-v1",
        )
        cls.execution_policy = load(LP / "policies" / "chemistry-core2a-execution-policy.json")
        cls.source_policy = load(CORE2A / "policies" / "chemistry-core2a-source-realization-policy.json")
        cls.language_policy = load(LP / "policies" / "chemistry-learner-language-policy.json")
        cls.citation_policy = load(LP / "policies" / "chemistry-question-citation-policy.json")
        cls.answer_policy = load(LP / "policies" / "chemistry-answer-path-policy.json")
        cls.source_plan = build_source_plan(
            internals["core2"], cls.bucket_plan, cls.family_registry, cls.execution_policy, cls.source_policy,
            cls.language_policy, cls.citation_policy, cls.answer_policy, "CHEM-C2A-SOURCE-FOR-CHALLENGES-v1",
        )
        cls.competitive_policy = load(LP / "policies" / "chemistry-competitive-challenge-policy.json")
        cls.archetype_registry = load(LP / "registry" / "chemistry-competitive-archetype-registry.json")
        cls.challenge_policy = load(CORE2A / "policies" / "chemistry-core2a-challenge-realization-policy.json")
        cls.plan = build_challenge_plan(
            cls.source_plan, cls.bucket_plan, cls.family_registry, cls.execution_policy, cls.competitive_policy,
            cls.archetype_registry, cls.challenge_policy, cls.language_policy, cls.citation_policy,
            cls.answer_policy, "CHEM-C2A-CHALLENGE-PLAN-INTEGRATION-v1",
        )
        cls.item_schema = load(CORE2A / "contracts" / "chemistry-core2a-challenge-item.schema.json")
        cls.plan_schema = load(CORE2A / "contracts" / "chemistry-core2a-challenge-plan.schema.json")
        cls.provenance_schema = load(LP / "contracts" / "chemistry-question-provenance.schema.json")
        cls.answer_schema = load(LP / "contracts" / "chemistry-answer-path.schema.json")

    def validate(self, plan):
        return validate_challenge_plan(
            plan, self.source_plan, self.bucket_plan, self.family_registry, self.execution_policy,
            self.competitive_policy, self.archetype_registry, self.challenge_policy, self.language_policy,
            self.citation_policy, self.answer_policy,
        )

    def test_plan_and_items_validate(self):
        Draft202012Validator(self.plan_schema).validate(self.plan)
        self.assertGreater(len(self.plan["items"]), 0)
        for item in self.plan["items"]:
            Draft202012Validator(self.item_schema).validate(item)
            Draft202012Validator(self.provenance_schema).validate(item["provenance"])
            Draft202012Validator(self.answer_schema).validate(item["answer_path"])

    def test_one_near_transfer_per_supported_source_family(self):
        source_families = []
        for item in self.source_plan["items"]:
            family = item["core1a_binding"]["primary_problem_family_ref"]
            if family not in source_families:
                source_families.append(family)
        supported = [f for f in source_families if f in self.challenge_policy["supported_family_recipes"]]
        counts = {}
        for item in self.plan["items"]:
            if item["archetype_name"] == "NEAR_TRANSFER":
                counts[item["problem_family_ref"]] = counts.get(item["problem_family_ref"], 0) + 1
        self.assertEqual(set(counts), set(supported))
        self.assertTrue(all(counts[f] == 1 for f in supported))
        self.assertEqual(self.plan["summary"]["near_transfer_required"], len(supported))
        self.assertEqual(self.plan["summary"]["near_transfer_realized"], len(supported))

    def test_every_challenge_is_taught_independently_checked_and_not_near_copy(self):
        buckets = {b["bucket_id"]: b for b in self.bucket_plan["buckets"]}
        source_stems = {x["source_snapshot"]["stem"] for x in self.source_plan["items"]}
        for item in self.plan["items"]:
            bucket = buckets[item["core1a_binding"]["bucket_id"]]
            taught = set(bucket["primary_capability_refs"] + bucket["supporting_capability_refs"])
            self.assertEqual(set(item["core1a_binding"]["taught_capability_refs"]), taught)
            self.assertEqual(item["chemistry_validation"]["status"], "PASS")
            self.assertGreater(len(item["chemistry_validation"]["checks"]), 0)
            self.assertEqual(item["near_copy_check"]["status"], "PASS")
            self.assertFalse(item["near_copy_check"]["exact_copy"])
            self.assertNotIn(item["prompt"], source_stems)

    def test_generated_provenance_never_claims_official_past_question(self):
        for item in self.plan["items"]:
            prov = item["provenance"]
            self.assertEqual(prov["question_origin"], "GENERATED_ORIGINAL")
            self.assertFalse(prov["official_past_question_claim"])
            self.assertTrue(any(c["citation_kind"] == "GENERATED_ORIGINAL" for c in prov["citations"]))
            self.assertTrue(any(c["citation_kind"] == "CORE2_SOURCE" for c in prov["citations"]))

    def test_answer_closure_is_exact(self):
        total = len(self.plan["items"])
        summary = self.plan["summary"]
        self.assertEqual(summary["generated_items_total"], total)
        self.assertEqual(summary["independent_chemistry_checks_passed"], total)
        self.assertEqual(summary["near_copy_checks_passed"], total)
        self.assertEqual(summary["quick_checks_realized"], total)
        self.assertEqual(summary["full_workings_realized"], total)
        for item in self.plan["items"]:
            self.assertIsNotNone(item["answer_path"]["quick_check"])
            self.assertIsNotNone(item["answer_path"]["full_working"])

    def test_structural_variations_only_when_bucket_is_d2_or_d3(self):
        buckets = {b["bucket_id"]: b for b in self.bucket_plan["buckets"]}
        allowed = set(self.challenge_policy["selection"]["structural_variation_for_difficulty"])
        structural = [x for x in self.plan["items"] if x["archetype_name"] != "NEAR_TRANSFER"]
        for item in structural:
            self.assertIn(buckets[item["core1a_binding"]["bucket_id"]]["intrinsic_difficulty"], allowed)
        self.assertEqual(len(structural), self.plan["summary"]["structural_variations_required"])

    def test_exact_source_copy_fails_near_copy_gate(self):
        bad = copy.deepcopy(self.plan)
        item = bad["items"][0]
        anchor = next(x for x in self.source_plan["items"] if x["question_ref"] == item["anchor_source_question_ref"])
        item["prompt"] = anchor["source_snapshot"]["stem"]
        redigest_item(item)
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_GENERATED_ITEM_TOO_CLOSE_TO_SOURCE"):
            self.validate(bad)

    def test_answer_tamper_fails_independent_validation(self):
        bad = copy.deepcopy(self.plan)
        bad["items"][0]["chemistry_validation"]["expected_answer"] = "wrong"
        redigest_item(bad["items"][0])
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED"):
            self.validate(bad)

    def test_untaught_capability_injection_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["items"][0]["core1a_binding"]["taught_capability_refs"].append("CAP-NOT-TAUGHT")
        redigest_item(bad["items"][0])
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_UNTAUGHT_CHEMISTRY_REQUIRED"):
            self.validate(bad)

    def test_false_official_attribution_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["items"][0]["provenance"]["official_past_question_claim"] = True
        bad["items"][0]["provenance"]["verified_official_source_ref"] = "invented"
        redigest_item(bad["items"][0])
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_GENERATED_ITEM_FALSE_OFFICIAL_ATTRIBUTION"):
            self.validate(bad)

    def test_missing_quick_check_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["items"][0]["answer_path"]["quick_check"] = None
        redigest_item(bad["items"][0])
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_ANSWER_PATH_MISSING"):
            self.validate(bad)

    def test_deterministic_replay(self):
        again = build_challenge_plan(
            copy.deepcopy(self.source_plan), copy.deepcopy(self.bucket_plan), copy.deepcopy(self.family_registry),
            copy.deepcopy(self.execution_policy), copy.deepcopy(self.competitive_policy),
            copy.deepcopy(self.archetype_registry), copy.deepcopy(self.challenge_policy),
            copy.deepcopy(self.language_policy), copy.deepcopy(self.citation_policy), copy.deepcopy(self.answer_policy),
            "CHEM-C2A-CHALLENGE-PLAN-INTEGRATION-v1",
        )
        self.assertEqual(self.plan, again)


if __name__ == "__main__":
    unittest.main()
