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
    run_manifest = {
        "run_id": "CHEM-LPR-89abcdef01234567",
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
    run_manifest["run_digest"] = runner.canonical_digest(run_manifest)
    return run_manifest


class ChemistryLearnerProductRenderPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures = CHEM / "AssessmentIntake" / "fixtures"
        _, cls.internals = run_cold_start(
            load(fixtures / "mixed-chemistry-source.fixture.json"),
            load(fixtures / "mixed-chemistry-question-set.fixture.json"),
            load(fixtures / "mixed-chemistry-external-corpus.fixture.json"),
            load(fixtures / "mixed-chemistry-topic-scope.fixture.json"),
            repo_root=REPO,
            run_id="CHEM-LP-RENDER-GOLDEN-COLDSTART",
        )
        cls.run_manifest = make_run(cls.internals)

    def execute(self):
        td = tempfile.TemporaryDirectory()
        out = Path(td.name) / "out"
        package, files = runner.execute_full_pipeline(
            copy.deepcopy(self.run_manifest),
            copy.deepcopy(self.internals["study_model"]),
            copy.deepcopy(self.internals["core1"]),
            copy.deepcopy(self.internals["representations"]),
            copy.deepcopy(self.internals["core2"]),
            copy.deepcopy(self.internals["closure"]),
            out,
        )
        return td, out, package, files

    def test_full_pipeline_reaches_frozen_handoff_without_release_claim(self):
        td, out, package, files = self.execute()
        try:
            self.assertEqual(package["complete_through"], "FREEZE_HANDOFF")
            self.assertEqual(package["machine_status"], "PASS")
            self.assertFalse(package["release_authorized"])
            self.assertTrue((out / "chemistry_core1a.pdf").exists())
            self.assertTrue((out / "chemistry_core2a.pdf").exists())
            self.assertEqual(files["visual_preflight.json"]["status"], "PASS")
            self.assertEqual(files["final_audit.json"]["machine_status"], "PASS")
            self.assertEqual(files["handoff_manifest.json"]["status"], "MACHINE_COMPLETE_HUMAN_REVIEW_PENDING")
            stages = files["learner_product_stage_evidence.json"]["stages"]
            self.assertEqual([row["stage"] for row in stages], runner.EXECUTION_SEQUENCE)
            self.assertTrue(all(row["status"] == "PASS" for row in stages))
        finally:
            td.cleanup()

    def test_actual_pdf_preflight_proves_font_geometry_raster_and_no_id_leaks(self):
        td, _, _, files = self.execute()
        try:
            report = files["visual_preflight.json"]
            for product in report["products"].values():
                self.assertEqual(product["font_floor_status"], "PASS")
                self.assertEqual(product["physical_rectangles"]["clipping_count"], 0)
                self.assertEqual(product["physical_rectangles"]["overlap_count"], 0)
                self.assertEqual(product["pdf_parse_and_raster"]["internal_identifier_leaks"], {})
                self.assertEqual(product["pdf_parse_and_raster"]["blank_sample_pages"], [])
                self.assertGreaterEqual(len(product["pdf_parse_and_raster"]["raster_proof"]), 2)
                self.assertEqual(product["visual_obligation_closure"]["status"], "PASS")
        finally:
            td.cleanup()

    def test_render_is_deterministic(self):
        td1, _, package1, files1 = self.execute()
        td2, _, package2, files2 = self.execute()
        try:
            self.assertEqual(package1, package2)
            self.assertEqual(files1["render_manifest.json"]["core1a"]["pdf_sha256"], files2["render_manifest.json"]["core1a"]["pdf_sha256"])
            self.assertEqual(files1["render_manifest.json"]["core2a"]["pdf_sha256"], files2["render_manifest.json"]["core2a"]["pdf_sha256"])
            self.assertEqual(files1["visual_preflight.json"], files2["visual_preflight.json"])
        finally:
            td1.cleanup(); td2.cleanup()


if __name__ == "__main__":
    unittest.main()
