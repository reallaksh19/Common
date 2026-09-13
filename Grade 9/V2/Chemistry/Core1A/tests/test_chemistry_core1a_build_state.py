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

from build_chemistry_core1a_bucket_plan import build_bucket_plan  # noqa: E402
from build_chemistry_core1a_build_state import compile_build_state, digest, validate_build_state  # noqa: E402
from chemistry_cold_start_runner import run_cold_start  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def redigest(state):
    state["build_state_digest"] = ""
    state["build_state_digest"] = digest(state, "build_state_digest")
    return state


class ChemistryCore1ABuildStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures = CHEM / "AssessmentIntake" / "fixtures"
        sources = load(fixtures / "mixed-chemistry-source.fixture.json")
        questions = load(fixtures / "mixed-chemistry-question-set.fixture.json")
        corpus = load(fixtures / "mixed-chemistry-external-corpus.fixture.json")
        topic = load(fixtures / "mixed-chemistry-topic-scope.fixture.json")
        _, internals = run_cold_start(
            copy.deepcopy(sources),
            copy.deepcopy(questions),
            copy.deepcopy(corpus),
            copy.deepcopy(topic),
            repo_root=REPO,
            run_id="CHEM-C1A-BUILD-STATE-RUN",
        )
        family_registry = load(CHEM / "ReasoningSemantics" / "registry" / "chemistry-problem-family-registry.json")
        policy = load(CORE1A / "policies" / "chemistry-core1a-bucket-synthesis-policy.json")
        cls.plan = build_bucket_plan(
            internals["study_model"],
            internals["core1"],
            internals["representations"],
            internals["core2"],
            family_registry,
            policy,
            "CHEM-C1A-BP-BUILD-STATE-v1",
        )
        cls.state = compile_build_state(cls.plan, "CHEM-C1A-BUILD-STATE-INTEGRATION-v1")
        cls.schema = load(CORE1A / "contracts" / "chemistry-core1a-build-state.schema.json")

    def test_build_state_is_schema_valid_and_deterministic(self):
        Draft202012Validator(self.schema).validate(self.state)
        second = compile_build_state(copy.deepcopy(self.plan), "CHEM-C1A-BUILD-STATE-INTEGRATION-v1")
        self.assertEqual(self.state, second)

    def test_zero_primary_buckets_are_skipped_not_deleted(self):
        by_id = {row["bucket_id"]: row for row in self.state["entries"]}
        self.assertEqual(set(by_id), {bucket["bucket_id"] for bucket in self.plan["buckets"]})
        for bucket in self.plan["buckets"]:
            row = by_id[bucket["bucket_id"]]
            if not bucket["core2_primary_question_refs"]:
                self.assertEqual(row["publication_state"], "SKIP_NO_PRIMARY_CORE2")
            else:
                self.assertEqual(row["publication_state"], "READY_FOR_REALIZATION")

    def test_next_active_bucket_is_first_non_skipped_bucket(self):
        expected = next(
            (bucket["bucket_id"] for bucket in self.plan["buckets"] if bucket["core2_primary_question_refs"]),
            None,
        )
        self.assertEqual(self.state["next_active_bucket"], expected)

    def test_question_count_drift_fails_closed(self):
        bad = copy.deepcopy(self.state)
        bad["entries"][0]["primary_core2_question_count"] += 1
        redigest(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE1A_BUILD_STATE_QUESTION_COUNT_DRIFT"):
            validate_build_state(bad, self.plan)

    def test_next_bucket_drift_fails_closed(self):
        bad = copy.deepcopy(self.state)
        bad["next_active_bucket"] = None
        redigest(bad)
        if any(row["publication_state"] == "READY_FOR_REALIZATION" for row in bad["entries"]):
            with self.assertRaisesRegex(ValueError, r"^CORE1A_BUILD_STATE_NEXT_BUCKET_DRIFT"):
                validate_build_state(bad, self.plan)


if __name__ == "__main__":
    unittest.main()
