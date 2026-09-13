#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
LP = HERE.parents[1]
CHEM = LP.parent
REPO = CHEM.parents[2]

sys.path.insert(0, str(LP / "engine"))
sys.path.insert(0, str(CHEM / "ColdStart" / "engine"))

import run_chemistry_learner_product as runner  # noqa: E402
from chemistry_cold_start_runner import run_cold_start  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def make_run(internals):
    registry = load(LP / "registry" / "chemistry-competitive-archetype-registry.json")
    run = {
        "run_id": "CHEM-LPR-a1b2c3d4e5f60718",
        "contract_version": "1.0.0",
        "subject": "CHEMISTRY",
        "inputs": {
            "learner_study_model_ref": internals["study_model"]["study_model_id"],
            "learner_study_model_digest": internals["study_model"]["study_model_digest"],
            "core1_plan_ref": internals["core1"]["plan_id"],
            "core1_plan_digest": internals["core1"]["plan_digest"],
            "representation_bundle_ref": internals["representations"]["bundle_id"],
            "representation_bundle_digest": internals["representations"]["bundle_digest"],
            "core2_plan_ref": internals["core2"]["plan_id"],
            "core2_plan_digest": internals["core2"]["plan_digest"],
            "coverage_closure_ref": internals["closure"]["closure_id"],
            "coverage_closure_digest": internals["closure"]["closure_digest"],
            "competitive_registry_ref": registry["registry_id"],
            "competitive_registry_digest": runner.object_digest(registry),
        },
        "policy_refs": {
            "core1a_execution_policy": "CHEM-CORE1A-EXECUTION-v1",
            "core2a_execution_policy": "CHEM-CORE2A-EXECUTION-v1",
            "learner_language_policy": "CHEM-LEARNER-LANGUAGE-v1",
            "question_citation_policy": "CHEM-QUESTION-CITATION-v1",
            "competitive_challenge_policy": "CHEM-COMPETITIVE-CHALLENGE-v1",
            "answer_path_policy": "CHEM-ANSWER-PATH-v1",
        },
        "execution_sequence": list(runner.EXECUTION_SEQUENCE),
        "requested_products": {"core1a": True, "core2a_source": True, "core2a_challenges": True},
        "outputs": {
            "core1a_bucket_plan_ref": None,
            "core1a_manuscript_ref": None,
            "core2a_source_plan_ref": None,
            "core2a_challenge_plan_ref": None,
            "answer_closure_audit_ref": None,
            "artifact_manifest_ref": None,
            "handoff_manifest_ref": None,
        },
        "run_digest": "0" * 64,
    }
    run["run_digest"] = runner.canonical_digest(run)
    return run


class ChemistryLearnerProductSemanticPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures = CHEM / "AssessmentIntake" / "fixtures"
        _, cls.internals = run_cold_start(
            load(fixtures / "mixed-chemistry-source.fixture.json"),
            load(fixtures / "mixed-chemistry-question-set.fixture.json"),
            load(fixtures / "mixed-chemistry-external-corpus.fixture.json"),
            load(fixtures / "mixed-chemistry-topic-scope.fixture.json"),
            repo_root=REPO,
            run_id="CHEM-LP-SEMANTIC-GOLDEN-COLDSTART",
        )
        cls.run = make_run(cls.internals)
        cls.golden = load(LP / "golden" / "some-basic-concepts" / "expected-semantic-slice.json")

    def execute(self):
        td = tempfile.TemporaryDirectory()
        out = Path(td.name) / "out"
        package, files = runner.execute_semantic_pipeline(
            copy.deepcopy(self.run),
            copy.deepcopy(self.internals["study_model"]),
            copy.deepcopy(self.internals["core1"]),
            copy.deepcopy(self.internals["representations"]),
            copy.deepcopy(self.internals["core2"]),
            copy.deepcopy(self.internals["closure"]),
            out,
        )
        return td, out, package, files

    def test_runner_executes_semantic_chain_through_answer_closure(self):
        td, out, package, files = self.execute()
        try:
            self.assertEqual(package["semantic_complete_through"], "VALIDATE_ANSWER_CLOSURE")
            self.assertTrue(package["render_pending"])
            for name in [
                "core1a_bucket_plan.json", "core1a_build_state.json", "core1a_manuscript.json",
                "core2a_source_plan.json", "core2a_challenge_plan.json", "answer_closure_audit.json",
                "learner_product_stage_evidence.json", "semantic_package_manifest.json",
            ]:
                self.assertTrue((out / name).exists(), name)
            audit = files["answer_closure_audit.json"]
            counts = audit["counts"]
            self.assertEqual(counts["objective_questions_total"], counts["quick_checks_total"])
            self.assertEqual(counts["objective_questions_total"], counts["full_workings_total"])
            self.assertEqual(counts["open_questions_total"], counts["expected_response_rubrics_total"])
            stages = files["learner_product_stage_evidence.json"]["stages"]
            self.assertEqual([s["stage"] for s in stages], runner.EXECUTION_SEQUENCE)
            self.assertTrue(all(s["status"] == "PASS" for s in stages[:22]))
            self.assertTrue(all(s["status"] == "PENDING_RENDER_BOUNDARY" for s in stages[22:]))
        finally:
            td.cleanup()

    def test_some_basic_concepts_golden_slice_is_stable(self):
        td, _, package, files = self.execute()
        try:
            expected = self.golden["required_invariants"]
            selected_refs = self.golden["selected_source_question_refs"]
            families = self.golden["selected_problem_family_refs"]
            source = files["core2a_source_plan.json"]
            challenges = files["core2a_challenge_plan.json"]
            selected = [i for i in source["items"] if i["question_ref"] in selected_refs]
            self.assertEqual([i["question_ref"] for i in selected], selected_refs)
            self.assertEqual(len(selected), expected["source_items_selected"])
            self.assertEqual([i["core1a_binding"]["primary_problem_family_ref"] for i in selected], families)
            self.assertTrue(all(i["answer_path"]["quick_check"] for i in selected))
            self.assertTrue(all(i["answer_path"]["full_working"] for i in selected))
            self.assertTrue(all(
                i["core1a_binding"]["h1_evidence_refs"] and i["core1a_binding"]["h2_evidence_refs"] and i["core1a_binding"]["h3_evidence_refs"]
                for i in selected
            ))
            near = [i for i in challenges["items"] if i["problem_family_ref"] in families and i["archetype_name"] == "NEAR_TRANSFER"]
            self.assertEqual(len(near), len(families))
            self.assertTrue(all(i["chemistry_validation"]["status"] == "PASS" for i in near))
            self.assertTrue(all(i["near_copy_check"]["status"] == "PASS" for i in near))
            self.assertTrue(all(i["answer_path"]["quick_check"] and i["answer_path"]["full_working"] for i in near))
            self.assertTrue(all(i["provenance"]["official_past_question_claim"] is False for i in near))
            self.assertEqual(package["semantic_complete_through"], expected["semantic_complete_through"])
            self.assertEqual(package["render_pending"], expected["render_stages_pending"])
        finally:
            td.cleanup()

    def test_upstream_digest_tamper_fails_before_synthesis(self):
        bad = copy.deepcopy(self.internals["core1"])
        bad["plan_digest"] = "f" * 64
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "CHEM_LP_UPSTREAM_DIGEST_MISMATCH:core1_plan"):
                runner.execute_semantic_pipeline(
                    copy.deepcopy(self.run), copy.deepcopy(self.internals["study_model"]), bad,
                    copy.deepcopy(self.internals["representations"]), copy.deepcopy(self.internals["core2"]),
                    copy.deepcopy(self.internals["closure"]), Path(td),
                )

    def test_deterministic_semantic_replay(self):
        td1, _, package1, files1 = self.execute()
        td2, _, package2, files2 = self.execute()
        try:
            self.assertEqual(package1, package2)
            self.assertEqual(files1["core1a_bucket_plan.json"], files2["core1a_bucket_plan.json"])
            self.assertEqual(files1["core1a_manuscript.json"], files2["core1a_manuscript.json"])
            self.assertEqual(files1["core2a_source_plan.json"], files2["core2a_source_plan.json"])
            self.assertEqual(files1["core2a_challenge_plan.json"], files2["core2a_challenge_plan.json"])
        finally:
            td1.cleanup(); td2.cleanup()


if __name__ == "__main__":
    unittest.main()
