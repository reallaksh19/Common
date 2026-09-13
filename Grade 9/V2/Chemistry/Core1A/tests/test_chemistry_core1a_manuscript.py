#!/usr/bin/env python3
from __future__ import annotations

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
LP = CHEM / "LearnerProduct"

sys.path.insert(0, str(CORE1A / "engine"))
sys.path.insert(0, str(CHEM / "ColdStart" / "engine"))

from build_chemistry_core1a_bucket_plan import build_bucket_plan  # noqa: E402
from build_chemistry_core1a_manuscript import build_manuscript, digest, validate_manuscript  # noqa: E402
from chemistry_cold_start_runner import run_cold_start  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class ChemistryCore1AManuscriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures = CHEM / "AssessmentIntake" / "fixtures"
        _, internals = run_cold_start(
            load(fixtures / "mixed-chemistry-source.fixture.json"),
            load(fixtures / "mixed-chemistry-question-set.fixture.json"),
            load(fixtures / "mixed-chemistry-external-corpus.fixture.json"),
            load(fixtures / "mixed-chemistry-topic-scope.fixture.json"),
            repo_root=REPO,
            run_id="CHEM-C1A-MANUSCRIPT-INTEGRATION",
        )
        cls.core1 = internals["core1"]
        registry = load(CHEM / "ReasoningSemantics" / "registry" / "chemistry-problem-family-registry.json")
        synthesis = load(CORE1A / "policies" / "chemistry-core1a-bucket-synthesis-policy.json")
        cls.bucket_plan = build_bucket_plan(
            internals["study_model"], cls.core1, internals["representations"], internals["core2"],
            registry, synthesis, "CHEM-C1A-BP-MANUSCRIPT-v1",
        )
        cls.language = load(LP / "policies" / "chemistry-learner-language-policy.json")
        cls.answer = load(LP / "policies" / "chemistry-answer-path-policy.json")
        cls.manuscript = build_manuscript(
            cls.bucket_plan, cls.core1, cls.language, cls.answer, "CHEM-C1A-MANUSCRIPT-INTEGRATION-v1"
        )
        cls.schema = load(CORE1A / "contracts" / "chemistry-core1a-manuscript.schema.json")

    def test_schema_and_exact_bucket_order(self):
        Draft202012Validator(self.schema).validate(self.manuscript)
        self.assertEqual(
            [b["bucket_id"] for b in self.manuscript["buckets"]],
            [b["bucket_id"] for b in self.bucket_plan["buckets"]],
        )

    def test_every_core1_appendix_question_has_expected_response(self):
        required = len(self.core1["appendices"]["appendix_a"]["items"])
        self.assertEqual(self.manuscript["summary"]["practice_question_count"], required)
        self.assertEqual(self.manuscript["summary"]["open_rubric_count"], required)
        for bucket in self.manuscript["buckets"]:
            for item in bucket["practice_items"]:
                path = item["answer_path"]
                self.assertEqual(path["answer_path_kind"], "OPEN_RUBRIC")
                self.assertTrue(path["expected_response_rubric"]["criteria"])

    def test_missing_expected_response_fails(self):
        bad = copy.deepcopy(self.manuscript)
        target = next(item for b in bad["buckets"] for item in b["practice_items"])
        target["answer_path"]["expected_response_rubric"]["criteria"] = []
        bad["manuscript_digest"] = ""
        bad["manuscript_digest"] = digest(bad, "manuscript_digest")
        with self.assertRaisesRegex(ValueError, "CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING"):
            validate_manuscript(bad, self.bucket_plan, self.core1, self.language, self.answer)

    def test_deterministic_replay(self):
        again = build_manuscript(
            copy.deepcopy(self.bucket_plan), copy.deepcopy(self.core1), copy.deepcopy(self.language),
            copy.deepcopy(self.answer), "CHEM-C1A-MANUSCRIPT-INTEGRATION-v1",
        )
        self.assertEqual(self.manuscript, again)


if __name__ == "__main__":
    unittest.main()
