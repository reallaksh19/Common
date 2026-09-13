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

import ncert_production_baselines as production  # noqa: E402
import run_chemistry_learner_product as runner  # noqa: E402
import run_chemistry_ncert_production as production_runner  # noqa: E402
from chemistry_cold_start_runner import run_cold_start  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def make_run(internals, topic_id="some-basic-concepts"):
    registry = load(LP / "registry" / "chemistry-competitive-archetype-registry.json")
    baseline = production.baseline_for_topic(topic_id)
    run_manifest = {
        "run_id": "CHEM-LPR-fedcba9876543210",
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
            "production_topic_id": topic_id,
            "production_baseline_ref": baseline["baseline_ref"],
            "production_baseline_digest": baseline["baseline_digest"],
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
    run_manifest["run_digest"] = runner.canonical_digest(run_manifest)
    return run_manifest


class ChemistryNCERTProductionBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures = CHEM / "AssessmentIntake" / "fixtures"
        _, cls.internals = run_cold_start(
            load(fixtures / "mixed-chemistry-source.fixture.json"),
            load(fixtures / "mixed-chemistry-question-set.fixture.json"),
            load(fixtures / "mixed-chemistry-external-corpus.fixture.json"),
            load(fixtures / "mixed-chemistry-topic-scope.fixture.json"),
            repo_root=REPO,
            run_id="CHEM-LP-PRODUCTION-BASELINE-TEST",
        )

    def test_pr346_dual_evidence_freezes_all_four_retained_denominators(self):
        report = production.validate_all_baselines()
        self.assertEqual(report["status"], "PASS")
        expected = {
            "some-basic-concepts": 68,
            "behaviour-of-gases": 27,
            "chemical-bonding": 38,
            "redox-reactions": 11,
        }
        self.assertEqual(set(report["topics"]), set(expected))
        for topic_id, count in expected.items():
            row = report["topics"][topic_id]
            self.assertEqual(row["retained_questions"], count)
            self.assertEqual(row["required_immediate_answer_checks"], count)
            self.assertEqual(row["required_full_solutions"], count)
            self.assertEqual(row["freeze_state"], "FROZEN_ELIGIBLE_ONLY")
            self.assertEqual(len(row["baseline_digest"]), 64)

    def test_matching_live_closure_can_bind_without_inventing_scanned_total(self):
        baseline = production.baseline_for_topic("some-basic-concepts")
        run = {
            "inputs": {
                "production_topic_id": "some-basic-concepts",
                "production_baseline_ref": baseline["baseline_ref"],
                "production_baseline_digest": baseline["baseline_digest"],
            }
        }
        closure = {"external_matrix": {"summary": {
            "eligible_total": 68,
            "placed_unique_total": 68,
            "missing_total": 0,
            "duplicate_primary_total": 0,
        }}}
        bound = production.assert_run_binding(run, closure)
        self.assertEqual(bound["retained_questions"], 68)
        self.assertIn("TOTAL_SCANNED", bound["unresolved_counters"])

    def test_partial_production_binding_fails_closed(self):
        run = make_run(self.internals)
        run["inputs"]["production_baseline_digest"] = None
        run["run_digest"] = runner.canonical_digest(run)
        with self.assertRaisesRegex(ValueError, r"^CHEM_LP_PRODUCTION_BASELINE_BINDING_INCOMPLETE"):
            production.validate_optional_run_binding_shape(run)

    def test_synthetic_fixture_cannot_masquerade_as_68_question_production_topic(self):
        run = make_run(self.internals, "some-basic-concepts")
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, r"^CHEM_LP_PRODUCTION_DENOMINATOR_DRIFT"):
                production_runner.execute_production(
                    copy.deepcopy(run),
                    copy.deepcopy(self.internals["study_model"]),
                    copy.deepcopy(self.internals["core1"]),
                    copy.deepcopy(self.internals["representations"]),
                    copy.deepcopy(self.internals["core2"]),
                    copy.deepcopy(self.internals["closure"]),
                    Path(td),
                    semantic_only=True,
                )

    def test_tampered_handoff_denominator_is_detected(self):
        manifest = load(production.MANIFEST_PATH)
        manifest["topics"][0]["retained_questions"] += 1
        with self.assertRaisesRegex(ValueError, r"^CHEM_LP_PRODUCTION_BASELINE_DENOMINATOR_DISAGREEMENT"):
            production.validate_topic_tables(manifest, copy.deepcopy(production.EXPECTED_TOPICS))

    def test_legacy_bundle_integrity_is_reported_separately_from_denominator_authority(self):
        bundle = production.inspect_legacy_source_bundle()
        self.assertIn(bundle["status"], {"PASS", "FAIL"})
        if bundle["status"] == "FAIL" and "actual_bytes" in bundle:
            self.assertTrue(
                bundle["actual_bytes"] != bundle["expected_bytes"]
                or bundle["actual_sha256"] != bundle["expected_sha256"]
                or not bundle["archive_readable"]
            )
        self.assertEqual(production.validate_all_baselines()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
