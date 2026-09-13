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
from build_chemistry_core2a_source import build_source_plan, digest, validate_source_plan  # noqa: E402
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


class ChemistryCore2ASourceTests(unittest.TestCase):
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
            run_id="CHEM-C2A-SOURCE-INTEGRATION-RUN",
        )
        cls.core2 = internals["core2"]
        cls.family_registry = load(CHEM / "ReasoningSemantics" / "registry" / "chemistry-problem-family-registry.json")
        cls.core1a_policy = load(CORE1A / "policies" / "chemistry-core1a-bucket-synthesis-policy.json")
        cls.bucket_plan = build_bucket_plan(
            internals["study_model"],
            internals["core1"],
            internals["representations"],
            cls.core2,
            cls.family_registry,
            cls.core1a_policy,
            "CHEM-C1A-BP-C2A-INTEGRATION-v1",
        )
        cls.execution_policy = load(LP / "policies" / "chemistry-core2a-execution-policy.json")
        cls.source_policy = load(CORE2A / "policies" / "chemistry-core2a-source-realization-policy.json")
        cls.language_policy = load(LP / "policies" / "chemistry-learner-language-policy.json")
        cls.citation_policy = load(LP / "policies" / "chemistry-question-citation-policy.json")
        cls.answer_policy = load(LP / "policies" / "chemistry-answer-path-policy.json")
        cls.plan = build_source_plan(
            cls.core2,
            cls.bucket_plan,
            cls.family_registry,
            cls.execution_policy,
            cls.source_policy,
            cls.language_policy,
            cls.citation_policy,
            cls.answer_policy,
            "CHEM-C2A-SOURCE-PLAN-INTEGRATION-v1",
        )
        cls.item_schema = load(CORE2A / "contracts" / "chemistry-core2a-source-item.schema.json")
        cls.plan_schema = load(CORE2A / "contracts" / "chemistry-core2a-source-plan.schema.json")
        cls.provenance_schema = load(LP / "contracts" / "chemistry-question-provenance.schema.json")
        cls.answer_schema = load(LP / "contracts" / "chemistry-answer-path.schema.json")

    def validate(self, plan):
        return validate_source_plan(
            plan,
            self.core2,
            self.bucket_plan,
            self.family_registry,
            self.execution_policy,
            self.source_policy,
            self.language_policy,
            self.citation_policy,
            self.answer_policy,
        )

    def test_real_core2_plan_realizes_every_source_item_in_order(self):
        Draft202012Validator(self.plan_schema).validate(self.plan)
        self.assertEqual(
            [item["question_ref"] for item in self.plan["items"]],
            [page["question_ref"] for page in self.core2["pages"]],
        )
        self.assertEqual(self.plan["summary"]["source_questions_required"], len(self.core2["pages"]))
        self.assertEqual(self.plan["summary"]["source_questions_realized"], len(self.core2["pages"]))

    def test_each_item_closes_schema_provenance_and_answer_path(self):
        for item in self.plan["items"]:
            Draft202012Validator(self.item_schema).validate(item)
            Draft202012Validator(self.provenance_schema).validate(item["provenance"])
            Draft202012Validator(self.answer_schema).validate(item["answer_path"])
            self.assertEqual(item["answer_path"]["answer_path_kind"], "OBJECTIVE_CHECKABLE")
            self.assertIsNotNone(item["answer_path"]["quick_check"])
            self.assertIsNotNone(item["answer_path"]["full_working"])

    def test_source_snapshot_is_lossless_against_c_i(self):
        by_ref = {page["question_ref"]: page for page in self.core2["pages"]}
        for item in self.plan["items"]:
            page = by_ref[item["question_ref"]]
            snap = item["source_snapshot"]
            self.assertEqual(snap["stem"], page["source_stem"])
            self.assertEqual(snap["options"], page["source_options"])
            self.assertEqual(snap["subparts"], page["source_subparts"])
            self.assertEqual(snap["figure_semantic"], page["source_figure_semantic"])
            self.assertEqual(snap["condition_text"], page["source_condition_text"])
            self.assertEqual(snap["source_qc_status"], page["source_qc_status"])
            self.assertEqual(snap["source_fidelity"], page["source_fidelity"])

    def test_core1a_hint_evidence_is_reused_not_reinvented(self):
        bucket_by_question = {}
        for bucket in self.bucket_plan["buckets"]:
            hints = {row["question_ref"]: row for row in bucket["core2_hint_bindings"]}
            for question_ref in bucket["core2_primary_question_refs"]:
                bucket_by_question[question_ref] = (bucket, hints[question_ref])
        for item in self.plan["items"]:
            bucket, hint = bucket_by_question[item["question_ref"]]
            binding = item["core1a_binding"]
            self.assertEqual(binding["bucket_id"], bucket["bucket_id"])
            self.assertEqual(binding["h1_evidence_refs"], hint["h1_evidence_refs"])
            self.assertEqual(binding["h2_evidence_refs"], hint["h2_evidence_refs"])
            self.assertEqual(binding["h3_evidence_refs"], hint["h3_evidence_refs"])

    def test_support_is_attempt_first_and_teacher_facing(self):
        forbidden = [term.lower() for term in self.language_policy["forbidden_learner_terms"]]
        for item in self.plan["items"]:
            support = item["learner_support"]
            self.assertTrue(support["support_initially_hidden"])
            self.assertTrue(support["small_clue"])
            self.assertTrue(support["bigger_clue"])
            self.assertTrue(support["how_do_i_start"])
            self.assertTrue(support["write_this_first"].startswith("Start by completing this line"))
            text = json.dumps(support, ensure_ascii=False).lower()
            self.assertFalse([term for term in forbidden if term in text])

    def test_fixture_source_links_are_kept_internal_not_renderable_provenance(self):
        for item in self.plan["items"]:
            raw = item["internal_source_custody"]["source_link_internal"]
            if raw.startswith("fixture://"):
                self.assertFalse(item["internal_source_custody"]["display_url_allowed"])
                self.assertNotIn(raw, json.dumps(item["provenance"], ensure_ascii=False))
                self.assertIsNone(item["provenance"]["citations"][0]["url"])

    def test_answer_closure_counts_are_exact(self):
        count = len(self.core2["pages"])
        summary = self.plan["summary"]
        self.assertEqual(summary["quick_checks_required"], count)
        self.assertEqual(summary["quick_checks_realized"], count)
        self.assertEqual(summary["full_workings_required"], count)
        self.assertEqual(summary["full_workings_realized"], count)
        self.assertEqual(summary["hint_reveals_required"], 3 * count)
        self.assertEqual(summary["hint_reveals_bound"], 3 * count)
        self.assertEqual(summary["raw_internal_source_links_rendered"], 0)

    def test_source_text_drift_fails_closed(self):
        bad = copy.deepcopy(self.plan)
        bad["items"][0]["source_snapshot"]["stem"] += " changed"
        redigest_item(bad["items"][0])
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_SOURCE_INTEGRITY_DRIFT"):
            self.validate(bad)

    def test_answer_path_deletion_fails_closed(self):
        bad = copy.deepcopy(self.plan)
        bad["items"][0]["answer_path"]["quick_check"] = None
        redigest_item(bad["items"][0])
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_ANSWER_PATH_MISSING"):
            self.validate(bad)

    def test_hint_binding_drift_fails_closed(self):
        bad = copy.deepcopy(self.plan)
        bad["items"][0]["core1a_binding"]["h3_evidence_refs"] = ["NOT-PRETAUGHT"]
        redigest_item(bad["items"][0])
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_HINT_ATOM_NOT_PRETAUGHT"):
            self.validate(bad)

    def test_provenance_deletion_fails_closed(self):
        bad = copy.deepcopy(self.plan)
        bad["items"][0]["provenance"]["citations"] = []
        redigest_item(bad["items"][0])
        redigest_plan(bad)
        with self.assertRaisesRegex(ValueError, r"^CORE2A_QUESTION_CITATION_MISSING"):
            self.validate(bad)

    def test_deterministic_replay(self):
        again = build_source_plan(
            copy.deepcopy(self.core2),
            copy.deepcopy(self.bucket_plan),
            copy.deepcopy(self.family_registry),
            copy.deepcopy(self.execution_policy),
            copy.deepcopy(self.source_policy),
            copy.deepcopy(self.language_policy),
            copy.deepcopy(self.citation_policy),
            copy.deepcopy(self.answer_policy),
            "CHEM-C2A-SOURCE-PLAN-INTEGRATION-v1",
        )
        self.assertEqual(self.plan, again)


if __name__ == "__main__":
    unittest.main()
