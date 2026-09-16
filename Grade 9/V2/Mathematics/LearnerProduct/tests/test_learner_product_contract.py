#!/usr/bin/env python3
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve()
LP = HERE.parents[1]
ENGINE = LP / "engine" / "run_learner_product.py"
RUN_SCHEMA = LP / "contracts" / "math-learner-product-run.schema.json"
PROV_SCHEMA = LP / "contracts" / "math-question-provenance.schema.json"

spec = importlib.util.spec_from_file_location("run_learner_product", ENGINE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class LearnerProductContractTests(unittest.TestCase):
    def sample_run(self):
        schema = json.loads(RUN_SCHEMA.read_text(encoding="utf-8"))
        sequence = schema["properties"]["execution_sequence"]["const"]
        return {
            "run_id": "MATH-LPR-0123456789abcdef",
            "contract_version": "1.0.0",
            "subject": "MATHEMATICS",
            "inputs": {
                "learner_study_model_ref": "MATH-LSM-DEMO",
                "learner_study_model_digest": "1" * 64,
                "core1_plan_ref": "MATH-C1SP-0123456789abcdef",
                "core1_plan_digest": "2" * 64,
                "core2_plan_ref": "MATH-C2TP-0123456789abcdef",
                "core2_plan_digest": "3" * 64,
                "competitive_registry_ref": None,
                "competitive_registry_digest": None,
            },
            "policy_refs": dict(mod.EXPECTED_POLICIES),
            "execution_sequence": sequence,
            "requested_products": {"core1a": True, "core2a_source": True, "core2a_challenges": True},
            "outputs": {
                "core1a_bucket_plan_ref": None,
                "core1a_manuscript_ref": None,
                "core2a_challenge_plan_ref": None,
                "artifact_manifest_ref": None,
            },
            "run_digest": "4" * 64,
        }

    def test_run_schema_locks_execution_order(self):
        run = self.sample_run()
        schema = json.loads(RUN_SCHEMA.read_text(encoding="utf-8"))
        jsonschema.validate(run, schema)
        run["execution_sequence"] = list(reversed(run["execution_sequence"]))
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(run, schema)

    def test_generated_question_cannot_claim_official_past_source(self):
        schema = json.loads(PROV_SCHEMA.read_text(encoding="utf-8"))
        item = {
            "question_origin": "GENERATED_ORIGINAL",
            "display_inline": True,
            "learner_label": "Where this question came from",
            "citations": [{
                "citation_kind": "GENERATED_ORIGINAL",
                "label": "Workbook original",
                "locator": "C1",
                "use": "ORIGIN_DISCLOSURE",
                "text_relation": "FRESH_ORIGINAL",
                "url": None,
            }],
            "official_past_question_claim": True,
            "verified_official_source_ref": "fake",
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(item, schema)

    def test_validate_manifest_checks_policy_bindings(self):
        run = self.sample_run()
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "run.json"
            p.write_text(json.dumps(run), encoding="utf-8")
            loaded = mod.validate_manifest(p)
            self.assertEqual(loaded["run_id"], run["run_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
