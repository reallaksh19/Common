#!/usr/bin/env python3
import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
CORE1A = HERE.parents[1]
CHEM = CORE1A.parent
REPO = CHEM.parents[2]

sys.path.insert(0, str(CORE1A / "engine"))
sys.path.insert(0, str(CHEM / "ColdStart" / "engine"))

from build_chemistry_core1a_bucket_plan import (  # noqa: E402
    build_bucket_plan,
    digest,
    validate_bucket_plan,
)
from chemistry_cold_start_runner import run_cold_start  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def redigest(plan):
    plan["plan_digest"] = ""
    plan["plan_digest"] = digest(plan, "plan_digest")
    return plan


class ChemistryCore1ABucketPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures = CHEM / "AssessmentIntake" / "fixtures"
        evidence = CHEM / "LearnerEvidence" / "fixtures"
        sources = load(fixtures / "mixed-chemistry-source.fixture.json")
        questions = load(fixtures / "mixed-chemistry-question-set.fixture.json")
        corpus = load(fixtures / "mixed-chemistry-external-corpus.fixture.json")
        topic = load(fixtures / "mixed-chemistry-topic-scope.fixture.json")
        attempts = load(evidence / "chemistry-diagnostic-attempt-set.fixture.json")
        evidence_ledger = load(evidence / "chemistry-learner-evidence-ledger.fixture.json")
        _, internals = run_cold_start(
            copy.deepcopy(sources),
            copy.deepcopy(questions),
            copy.deepcopy(corpus),
            copy.deepcopy(topic),
            copy.deepcopy(attempts),
            copy.deepcopy(evidence_ledger),
            repo_root=REPO,
            run_id="CHEM-C1A-INTEGRATION-RUN",
        )
        cls.study = internals["study_model"]
        cls.core1 = internals["core1"]
        cls.representations = internals["representations"]
        cls.core2 = internals["core2"]
        cls.family_registry = load(CHEM / "ReasoningSemantics" / "registry" / "chemistry-problem-family-registry.json")
        cls.policy = load(CORE1A / "policies" / "chemistry-core1a-bucket-synthesis-policy.json")
        cls.schema = load(CORE1A / "contracts" / "chemistry-core1a-bucket-plan.schema.json")
        cls.plan = build_bucket_plan(
            cls.study,
            cls.core1,
            cls.representations,
            cls.core2,
            cls.family_registry,
            cls.policy,
            "CHEM-C1A-BP-INTEGRATION-v1",
        )

    def test_real_cold_start_chain_builds_schema_valid_bucket_plan(self):
        Draft202012Validator(self.schema).validate(self.plan)
        self.assertEqual(self.plan["coverage"]["status"], "PASS")
        self.assertEqual(
            len(self.plan["coverage"]["required_capability_refs"]),
            len(self.study["capability_records"]),
        )
        self.assertEqual(
            self.plan["coverage"]["hint_reveals_required"],
            3 * len(self.core2["pages"]),
        )
        self.assertEqual(
            self.plan["coverage"]["hint_reveals_bound"],
            self.plan["coverage"]["hint_reveals_required"],
        )

    def test_capability_state_and_treatment_are_preserved_exactly(self):
        source = {
            row["capability_ref"]: (row["learner_state"], row["treatment"], row["priority"])
            for row in self.study["capability_records"]
        }
        realized = {
            row["capability_ref"]: (row["learner_state"], row["treatment"], row["priority"])
            for bucket in self.plan["buckets"]
            for row in bucket["learner_treatment_by_capability"]
        }
        self.assertEqual(realized, source)
        raw = json.dumps(self.plan)
        self.assertNotIn('"20%"', raw)
        self.assertNotIn('"50%"', raw)

    def test_every_ch_representation_has_exactly_one_bucket_home(self):
        expected = [row["representation_id"] for row in self.representations["representations"]]
        actual = [
            row["representation_ref"]
            for bucket in self.plan["buckets"]
            for row in bucket["representation_obligations"]
        ]
        self.assertCountEqual(actual, expected)
        self.assertEqual(len(actual), len(set(actual)))

    def test_every_core2_question_and_hint_reveal_is_closed(self):
        expected_questions = [page["question_ref"] for page in self.core2["pages"]]
        mapped = [
            question_ref
            for bucket in self.plan["buckets"]
            for question_ref in bucket["core2_primary_question_refs"]
        ]
        self.assertCountEqual(mapped, expected_questions)
        bindings = [
            binding
            for bucket in self.plan["buckets"]
            for binding in bucket["core2_hint_bindings"]
        ]
        self.assertEqual(len(bindings), len(expected_questions))
        for binding in bindings:
            self.assertTrue(binding["h1_evidence_refs"])
            self.assertTrue(binding["h2_evidence_refs"])
            self.assertTrue(binding["h3_evidence_refs"])

    def test_problem_family_invariant_is_registry_grounded(self):
        family_by_id = {row["family_id"]: row for row in self.family_registry["families"]}
        for bucket in self.plan["buckets"]:
            family = family_by_id[bucket["primary_problem_family_ref"]]
            self.assertEqual(bucket["bucket_invariant"], family["chemical_signature"])
            self.assertEqual(
                bucket["readiness_gate"]["required_dimensions"],
                ["RECOGNISE", "REPRESENT", "FIRST_MOVE", "FINISH_AND_VERIFY"],
            )

    def test_treatment_drift_fails_closed(self):
        bad = copy.deepcopy(self.plan)
        row = bad["buckets"][0]["learner_treatment_by_capability"][0]
        row["treatment"] = "READY_VERIFY_ONLY" if row["treatment"] != "READY_VERIFY_ONLY" else "ACTIVE_STUDY"
        redigest(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE1A_TREATMENT_DRIFT"):
            validate_bucket_plan(bad, self.study, self.core1, self.representations, self.core2, self.family_registry, self.policy)

    def test_missing_representation_fails_closed(self):
        bad = copy.deepcopy(self.plan)
        bad["buckets"][0]["representation_obligations"].pop()
        redigest(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE1A_VISUAL_OBLIGATION_UNCLOSED"):
            validate_bucket_plan(bad, self.study, self.core1, self.representations, self.core2, self.family_registry, self.policy)

    def test_unbound_hint_fails_closed(self):
        bad = copy.deepcopy(self.plan)
        target = next(bucket for bucket in bad["buckets"] if bucket["core2_hint_bindings"])
        target["core2_hint_bindings"][0]["h3_evidence_refs"] = ["NONEXISTENT-EVIDENCE"]
        redigest(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE1A_HINT_NOT_PRETAUGHT"):
            validate_bucket_plan(bad, self.study, self.core1, self.representations, self.core2, self.family_registry, self.policy)

    def test_missing_core2_mapping_fails_closed(self):
        bad = copy.deepcopy(self.plan)
        target = next(bucket for bucket in bad["buckets"] if bucket["core2_primary_question_refs"])
        target["core2_primary_question_refs"].pop()
        redigest(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE1A_CORE2_MAPPING_INCOMPLETE"):
            validate_bucket_plan(bad, self.study, self.core1, self.representations, self.core2, self.family_registry, self.policy)

    def test_deterministic_replay(self):
        second = build_bucket_plan(
            copy.deepcopy(self.study),
            copy.deepcopy(self.core1),
            copy.deepcopy(self.representations),
            copy.deepcopy(self.core2),
            copy.deepcopy(self.family_registry),
            copy.deepcopy(self.policy),
            "CHEM-C1A-BP-INTEGRATION-v1",
        )
        self.assertEqual(canonical_json(self.plan), canonical_json(second))


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
