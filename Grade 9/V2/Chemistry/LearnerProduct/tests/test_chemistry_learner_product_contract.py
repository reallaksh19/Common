from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema


TEST = Path(__file__).resolve()
LP_ROOT = TEST.parents[1]
ENGINE_PATH = LP_ROOT / "engine/run_chemistry_learner_product.py"
sys.path.insert(0, str(LP_ROOT / "engine"))

spec = importlib.util.spec_from_file_location("chem_lp_runner", ENGINE_PATH)
runner = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def valid_run():
    run = {
        "run_id": "CHEM-LPR-0123456789abcdef",
        "contract_version": "1.0.0",
        "subject": "CHEMISTRY",
        "inputs": {
            "learner_study_model_ref": "CHEM-LSM-TEST",
            "learner_study_model_digest": "1" * 64,
            "core1_plan_ref": "CHEM-C1-TEST",
            "core1_plan_digest": "2" * 64,
            "representation_bundle_ref": "CHEM-REP-TEST",
            "representation_bundle_digest": "3" * 64,
            "core2_plan_ref": "CHEM-C2-TEST",
            "core2_plan_digest": "4" * 64,
            "coverage_closure_ref": "CHEM-COV-TEST",
            "coverage_closure_digest": "5" * 64,
            "competitive_registry_ref": "CHEM-COMPETITIVE-ARCHETYPE-REGISTRY-v1",
            "competitive_registry_digest": "6" * 64,
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
        "requested_products": {
            "core1a": True,
            "core2a_source": True,
            "core2a_challenges": True,
        },
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


class TestChemistryLearnerProductFoundation(unittest.TestCase):
    def test_all_json_schemas_are_valid(self):
        for path in sorted((LP_ROOT / "contracts").glob("*.schema.json")):
            schema = load(path)
            jsonschema.Draft202012Validator.check_schema(schema)

    def test_valid_run_passes_foundation(self):
        evidence = runner.validate_foundation(valid_run())
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["execution_stage_count"], 26)

    def test_execution_order_is_locked(self):
        run = valid_run()
        run["execution_sequence"][3], run["execution_sequence"][4] = (
            run["execution_sequence"][4],
            run["execution_sequence"][3],
        )
        run["run_digest"] = runner.canonical_digest(run)
        with self.assertRaises((jsonschema.ValidationError, ValueError)):
            runner.validate_foundation(run)

    def test_digest_mismatch_fails(self):
        run = valid_run()
        run["run_digest"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "CHEM_LP_RUN_DIGEST_MISMATCH"):
            runner.validate_foundation(run)

    def test_challenges_require_competitive_registry(self):
        run = valid_run()
        run["inputs"]["competitive_registry_ref"] = None
        run["inputs"]["competitive_registry_digest"] = None
        run["run_digest"] = runner.canonical_digest(run)
        with self.assertRaisesRegex(ValueError, "CHEM_LP_CHALLENGE_REGISTRY_REQUIRED"):
            runner.validate_foundation(run)

    def test_generated_question_cannot_claim_official_past_provenance(self):
        schema = load(LP_ROOT / "contracts/chemistry-question-provenance.schema.json")
        bad = {
            "question_origin": "GENERATED_ORIGINAL",
            "display_inline": True,
            "learner_label": "WHERE THIS QUESTION CAME FROM",
            "citations": [
                {
                    "citation_kind": "GENERATED_ORIGINAL",
                    "label": "Fresh challenge",
                    "locator": "local:item-1",
                    "url": None,
                    "use": "ORIGIN_DISCLOSURE",
                    "text_relation": "FRESH_ORIGINAL",
                }
            ],
            "official_past_question_claim": True,
            "verified_official_source_ref": "fake-source",
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(schema).validate(bad)

    def test_source_question_provenance_is_valid(self):
        schema = load(LP_ROOT / "contracts/chemistry-question-provenance.schema.json")
        item = {
            "question_origin": "SOURCE_CORE2",
            "display_inline": True,
            "learner_label": "WHERE THIS QUESTION CAME FROM",
            "citations": [
                {
                    "citation_kind": "CORE2_SOURCE",
                    "label": "NCERT Exemplar Class IX Science — Unit 3",
                    "locator": "Question 26",
                    "url": "https://ncert.nic.in/example.pdf",
                    "use": "SOURCE_TEXT",
                    "text_relation": "EXACT_SOURCE",
                }
            ],
            "official_past_question_claim": False,
            "verified_official_source_ref": None,
        }
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(item)

    def test_closed_question_requires_quick_check_and_full_working(self):
        schema = load(LP_ROOT / "contracts/chemistry-answer-path.schema.json")
        good = {
            "question_ref": "Q1",
            "answer_path_kind": "OBJECTIVE_CHECKABLE",
            "learner_question_present": True,
            "answer_path_complete": True,
            "quick_check": {
                "learner_label": "QUICK CHECK",
                "answer_summary": "311 K",
                "unit": "K",
                "marking_points": [],
            },
            "full_working": {
                "learner_label": "FULL WORKING",
                "steps": ["K = °C + 273", "38 + 273 = 311 K"],
                "verification": "Kelvin value is larger than the Celsius value by 273.",
            },
            "expected_response_rubric": None,
        }
        jsonschema.Draft202012Validator(schema).validate(good)

        bad = copy.deepcopy(good)
        bad["full_working"] = None
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(schema).validate(bad)

    def test_open_question_requires_expected_response_rubric(self):
        schema = load(LP_ROOT / "contracts/chemistry-answer-path.schema.json")
        good = {
            "question_ref": "Q-open",
            "answer_path_kind": "OPEN_RUBRIC",
            "learner_question_present": True,
            "answer_path_complete": True,
            "quick_check": None,
            "full_working": None,
            "expected_response_rubric": {
                "learner_label": "EXPECTED RESPONSE",
                "criteria": ["States the relevant observation", "Links it to the Chemistry idea"],
            },
        }
        jsonschema.Draft202012Validator(schema).validate(good)

    def test_validate_only_writes_stage_evidence(self):
        run = valid_run()
        with tempfile.TemporaryDirectory() as td:
            manifest = Path(td) / "run.json"
            out = Path(td) / "out"
            manifest.write_text(json.dumps(run), encoding="utf-8")
            evidence = runner.validate_foundation(load(manifest))
            out.mkdir()
            (out / "evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
            self.assertTrue((out / "evidence.json").exists())


if __name__ == "__main__":
    unittest.main()
