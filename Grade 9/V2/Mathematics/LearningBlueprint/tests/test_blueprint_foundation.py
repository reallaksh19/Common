#!/usr/bin/env python3
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from blueprint_common import digest, load, seal_learning_run, validate_ground_truth_manifest, validate_learning_run
from build_ground_truth_manifest import build_manifest
from init_math_learning_run import build_run


class BlueprintFoundationTests(unittest.TestCase):
    def build_spec(self, local_name="questions.json"):
        return {
            "spec_version": "1.0.0",
            "subject": "MATHEMATICS",
            "items": [
                {
                    "evidence_type": "QUESTION_CORPUS",
                    "authority_class": "ORIGINAL_EVIDENCE",
                    "availability": "PRESENT",
                    "source_path": local_name,
                    "ref": "fixture/questions.json",
                    "declared_digest": None,
                    "source_locator": "fixture",
                    "scope_refs": ["ALGEBRA"],
                    "notes": None,
                    "conflict_refs": []
                },
                {
                    "evidence_type": "SYLLABUS",
                    "authority_class": "AUTHORITATIVE_SOURCE",
                    "availability": "ABSENT",
                    "source_path": None,
                    "ref": None,
                    "declared_digest": None,
                    "source_locator": None,
                    "scope_refs": [],
                    "notes": "No syllabus supplied.",
                    "conflict_refs": []
                }
            ]
        }

    def test_manifest_keeps_absence_explicit_without_negative_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "questions.json").write_text('{"questions": []}\n', encoding="utf-8")
            manifest = build_manifest(self.build_spec(), base_dir=root)
            validate_ground_truth_manifest(manifest)
            syllabus = next(x for x in manifest["evidence_items"] if x["evidence_type"] == "SYLLABUS")
            self.assertEqual(syllabus["availability"], "ABSENT")
            self.assertIsNone(syllabus["ref"])
            self.assertIsNone(syllabus["digest"])
            self.assertNotIn("importance", syllabus)
            policy = load(ROOT / "policies" / "math-evidence-state-policy.json")
            self.assertIn("LOW_IMPORTANCE", policy["states"]["ABSENT"]["forbidden_inferences"])

    def test_manifest_identity_is_deterministic_and_order_independent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "questions.json").write_text('{"questions": [1]}\n', encoding="utf-8")
            spec = self.build_spec()
            a = build_manifest(copy.deepcopy(spec), base_dir=root)
            spec["items"] = list(reversed(spec["items"]))
            b = build_manifest(spec, base_dir=root)
            self.assertEqual(a["manifest_id"], b["manifest_id"])
            self.assertEqual(a["manifest_digest"], b["manifest_digest"])

    def test_ground_truth_schema_rejects_derived_claim_authority(self):
        schema = load(ROOT / "contracts" / "math-ground-truth-manifest.schema.json")
        item = {
            "evidence_id": "GT-SYLLABUS-0123456789abcdef",
            "evidence_type": "SYLLABUS",
            "authority_class": "DERIVED_CLAIM",
            "availability": "PRESENT",
            "ref": "x",
            "digest": "1" * 64,
            "source_locator": None,
            "scope_refs": [],
            "notes": None,
            "conflict_refs": []
        }
        manifest = {
            "manifest_id": "MATH-GT-0123456789abcdef",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "evidence_items": [item],
            "manifest_digest": "2" * 64
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(manifest, schema)

    def test_conflicted_evidence_requires_conflict_refs(self):
        schema = load(ROOT / "contracts" / "math-ground-truth-manifest.schema.json")
        item = {
            "evidence_id": "GT-ANSWER_KEY-0123456789abcdef",
            "evidence_type": "ANSWER_KEY",
            "authority_class": "ORIGINAL_EVIDENCE",
            "availability": "CONFLICTED",
            "ref": "answer-key",
            "digest": "1" * 64,
            "source_locator": None,
            "scope_refs": [],
            "notes": None,
            "conflict_refs": []
        }
        manifest = {
            "manifest_id": "MATH-GT-0123456789abcdef",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "evidence_items": [item],
            "manifest_digest": "2" * 64
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(manifest, schema)

    def test_learning_run_starts_only_at_gt_ready(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "questions.json").write_text('{"questions": []}\n', encoding="utf-8")
            manifest = build_manifest(self.build_spec(), base_dir=root)
            run = build_run(
                manifest,
                learner_prior_percent=20,
                learning_purpose="FIRST_STUDY",
                product_mode="STARTER",
            )
            validate_learning_run(run)
            self.assertEqual(run["current_state"], "GT_READY")
            self.assertEqual(run["bundles"], [])
            self.assertIsNone(run["routing_ref"])
            self.assertEqual(run["control_plane"]["learner_prior_percent"], 20)

    def test_bundle_transport_limit_is_three_not_learning_atom_limit(self):
        schema = load(ROOT / "contracts" / "math-learning-run-blueprint.schema.json")
        bundle = {
            "bundle_id": "MATH-HB-0123456789abcdef",
            "subtopic_refs": ["A", "B", "C", "D"],
            "first_role": None,
            "core1_execution_ref": None,
            "core2_execution_ref": None,
            "cross_validation_ref": None,
            "join_ref": None,
            "assimilation_plan_ref": None,
            "core1a_ref": None,
            "exposure_receipt_refs": [],
            "core2a_eligibility_ref": None,
            "core2a_ref": None
        }
        run = {
            "run_id": "MATH-MLR-0123456789abcdef",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "ground_truth_ref": "MATH-GT-0123456789abcdef",
            "ground_truth_digest": "1" * 64,
            "control_plane": {"learner_prior_percent": None, "learning_purpose": None, "product_mode": None, "owner_override_refs": []},
            "current_state": "ROUTED",
            "state_history": [{"sequence": 0, "state": "ROUTED", "reason_code": "TEST"}],
            "routing_ref": "R-1",
            "bundles": [bundle],
            "publication_ref": None,
            "audit_ref": None,
            "run_digest": "2" * 64
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(run, schema)

    def test_root_schema_does_not_hard_code_core1_first(self):
        schema = load(ROOT / "contracts" / "math-learning-run-blueprint.schema.json")
        enum = schema["$defs"]["bundle"]["properties"]["first_role"]["enum"]
        self.assertEqual(set(x for x in enum if x is not None), {"CORE1", "CORE2"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
