from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from blueprint_common import seal_ground_truth, seal_learning_run
from run_dual_intelligence import (
    apply_cross_validation,
    build_cross_validation,
    build_first_work_order,
    build_second_independent_work_order,
    build_session,
    build_validation_work_order,
    materialize_context,
    seal_specialist_package,
)


class DualIntelligenceTests(unittest.TestCase):
    SUBTOPIC = "ALG-ROOT-RELATIONS"
    BUNDLE = "MATH-HB-0000000000000001"
    SYLLABUS = "GT-SYLLABUS-1111111111111111"
    QUESTIONS = "GT-QUESTION_CORPUS-2222222222222222"

    def manifest(self):
        return seal_ground_truth({
            "manifest_id": "",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "evidence_items": [
                {
                    "evidence_id": self.SYLLABUS,
                    "evidence_type": "SYLLABUS",
                    "authority_class": "AUTHORITATIVE_SOURCE",
                    "availability": "PRESENT",
                    "ref": "fixtures/syllabus.json",
                    "digest": "1" * 64,
                    "source_locator": "Algebra / roots",
                    "scope_refs": [self.SUBTOPIC],
                    "notes": None,
                    "conflict_refs": [],
                },
                {
                    "evidence_id": self.QUESTIONS,
                    "evidence_type": "QUESTION_CORPUS",
                    "authority_class": "ORIGINAL_EVIDENCE",
                    "availability": "PRESENT",
                    "ref": "fixtures/questions.json",
                    "digest": "2" * 64,
                    "source_locator": "Questions 1-8",
                    "scope_refs": [self.SUBTOPIC],
                    "notes": None,
                    "conflict_refs": [],
                },
            ],
            "manifest_digest": "",
        })

    def make_run(self, manifest, first_role="CORE1"):
        return seal_learning_run({
            "run_id": "",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "ground_truth_ref": manifest["manifest_id"],
            "ground_truth_digest": manifest["manifest_digest"],
            "control_plane": {
                "learner_prior_percent": 50,
                "learning_purpose": "CONSOLIDATION",
                "product_mode": "PRACTICE",
                "owner_override_refs": [],
            },
            "current_state": "ROUTED",
            "state_history": [
                {"sequence": 0, "state": "GT_READY", "reason_code": "TEST_GT"},
                {"sequence": 1, "state": "ROUTED", "reason_code": "TEST_ROUTE"},
            ],
            "routing_ref": "MATH-RP-SYNTHETIC",
            "bundles": [{
                "bundle_id": self.BUNDLE,
                "subtopic_refs": [self.SUBTOPIC],
                "first_role": first_role,
                "core1_execution_ref": None,
                "core2_execution_ref": None,
                "cross_validation_ref": None,
                "join_ref": None,
                "assimilation_plan_ref": None,
                "core1a_ref": None,
                "exposure_receipt_refs": [],
                "core2a_eligibility_ref": None,
                "core2a_ref": None,
            }],
            "publication_ref": None,
            "audit_ref": None,
            "run_digest": "",
        })

    def draft(self, role, *, two=False, wrong_type=False):
        if role == "CORE1":
            first = {
                "local_key": "a",
                "claim_type": "QUESTION_DEMAND" if wrong_type else "CONCEPT",
                "statement": "Roots, factors and coefficients form one semantic structure.",
                "subtopic_ref": self.SUBTOPIC,
                "evidence_refs": [self.SYLLABUS],
                "confidence": "HIGH",
                "dependency_local_keys": [],
                "unresolved_issue_refs": [],
            }
            second = {
                "local_key": "b",
                "claim_type": "CONCEPT_BOUNDARY",
                "statement": "Coefficient relations do not by themselves identify an ordered root.",
                "subtopic_ref": self.SUBTOPIC,
                "evidence_refs": [self.SYLLABUS],
                "confidence": "MEDIUM",
                "dependency_local_keys": ["a"],
                "unresolved_issue_refs": [],
            }
        else:
            first = {
                "local_key": "a",
                "claim_type": "QUESTION_DEMAND",
                "statement": "The corpus tests recognition of root-coefficient structure before calculation.",
                "subtopic_ref": self.SUBTOPIC,
                "evidence_refs": [self.QUESTIONS],
                "confidence": "HIGH",
                "dependency_local_keys": [],
                "unresolved_issue_refs": [],
            }
            second = {
                "local_key": "b",
                "claim_type": "HIDDEN_CONSTRAINT",
                "statement": "Some items conceal the useful symmetric relation in the target expression.",
                "subtopic_ref": self.SUBTOPIC,
                "evidence_refs": [self.QUESTIONS],
                "confidence": "MEDIUM",
                "dependency_local_keys": ["a"],
                "unresolved_issue_refs": [],
            }
        return {"claims": [first, second] if two else [first]}

    def prepare(self, first_role="CORE1", *, first_two=False):
        manifest = self.manifest()
        run = self.make_run(manifest, first_role)
        first_order = build_first_work_order(manifest, run, self.BUNDLE, "agent-first")
        first_context = materialize_context(manifest, run, first_order)
        first_package = seal_specialist_package(
            manifest, run, first_order, first_context,
            self.draft(first_role, two=first_two),
        )
        second_role = "CORE2" if first_role == "CORE1" else "CORE1"
        second_order = build_second_independent_work_order(
            manifest, run, self.BUNDLE, first_package, "agent-second"
        )
        second_context = materialize_context(manifest, run, second_order)
        second_package = seal_specialist_package(
            manifest, run, second_order, second_context, self.draft(second_role)
        )
        validation_order = build_validation_work_order(
            manifest, run, self.BUNDLE, first_package, second_package
        )
        validation_context = materialize_context(
            manifest, run, validation_order, packages=[first_package, second_package]
        )
        return (
            manifest, run, first_order, first_context, first_package,
            second_order, second_context, second_package,
            validation_order, validation_context,
        )

    def valid_authored(self, first_package, evidence_ref, *, classification="CONFIRMED", refined=None):
        return {
            "records": [{
                "first_claim_ref": claim["claim_id"],
                "classification": classification,
                "ground_truth_evidence_refs": [] if classification == "UNKNOWN" else [evidence_ref],
                "rationale": "Checked independently against original evidence.",
                "refined_statement": refined,
            } for claim in first_package["claims"]],
            "missing_findings": [],
        }

    def test_core1_first_firewall_and_cross_validated_state(self):
        items = self.prepare("CORE1")
        manifest, run, first_order, first_context, first_package, second_order, second_context, second_package, validation_order, validation_context = items
        self.assertEqual(first_context["context_mode"], "GROUND_TRUTH_ONLY")
        self.assertEqual(second_context["context_mode"], "GROUND_TRUTH_ONLY")
        self.assertEqual(second_context["upstream_packages"], [])
        self.assertEqual(second_context["withheld_upstream_package_refs"], [first_package["package_id"]])
        self.assertEqual(validation_context["context_mode"], "GROUND_TRUTH_PLUS_UPSTREAM_VALIDATION")
        validation = build_cross_validation(
            manifest, run, first_package, second_package,
            validation_order, validation_context,
            self.valid_authored(first_package, self.SYLLABUS),
        )
        updated = apply_cross_validation(run, first_package, second_package, validation)
        self.assertEqual(updated["run_id"], run["run_id"])
        self.assertEqual(updated["current_state"], "CROSS_VALIDATED")
        self.assertEqual(
            [x["state"] for x in updated["state_history"][-3:]],
            ["FIRST_CORE_COMPLETE", "SECOND_CORE_COMPLETE", "CROSS_VALIDATED"],
        )
        session = build_session(
            updated, first_order, first_context, first_package,
            second_order, second_context, second_package,
            validation_order, validation_context, validation,
        )
        self.assertEqual(session["status"], "CROSS_VALIDATED")
        self.assertNotEqual(session["first_agent_instance_id"], session["second_agent_instance_id"])

    def test_core2_first_is_symmetric(self):
        items = self.prepare("CORE2")
        manifest, run, _, _, first_package, _, second_context, second_package, validation_order, validation_context = items
        self.assertEqual(first_package["role"], "CORE2")
        self.assertEqual(second_package["role"], "CORE1")
        self.assertEqual(second_context["upstream_packages"], [])
        validation = build_cross_validation(
            manifest, run, first_package, second_package,
            validation_order, validation_context,
            self.valid_authored(first_package, self.QUESTIONS),
        )
        updated = apply_cross_validation(run, first_package, second_package, validation)
        self.assertEqual(updated["current_state"], "CROSS_VALIDATED")

    def test_same_agent_cannot_self_validate(self):
        manifest = self.manifest(); run = self.make_run(manifest, "CORE1")
        first_order = build_first_work_order(manifest, run, self.BUNDLE, "same-agent")
        first_context = materialize_context(manifest, run, first_order)
        first_package = seal_specialist_package(
            manifest, run, first_order, first_context, self.draft("CORE1")
        )
        with self.assertRaisesRegex(ValueError, "SELF_VALIDATION_INSTANCE_REUSE"):
            build_second_independent_work_order(
                manifest, run, self.BUNDLE, first_package, "same-agent"
            )

    def test_wrong_role_claim_type_is_rejected(self):
        manifest = self.manifest(); run = self.make_run(manifest, "CORE1")
        order = build_first_work_order(manifest, run, self.BUNDLE, "agent-first")
        context = materialize_context(manifest, run, order)
        with self.assertRaisesRegex(ValueError, "SPECIALIST_CLAIM_TYPE_WRONG_ROLE"):
            seal_specialist_package(
                manifest, run, order, context, self.draft("CORE1", wrong_type=True)
            )

    def test_every_first_claim_must_be_validated(self):
        items = self.prepare("CORE1", first_two=True)
        manifest, run, _, _, first_package, _, _, second_package, validation_order, validation_context = items
        authored = self.valid_authored(first_package, self.SYLLABUS)
        authored["records"] = authored["records"][:1]
        with self.assertRaisesRegex(ValueError, "CROSS_VALIDATION_FIRST_CLAIM_UNVALIDATED"):
            build_cross_validation(
                manifest, run, first_package, second_package,
                validation_order, validation_context, authored,
            )

    def test_refined_requires_refined_statement(self):
        items = self.prepare("CORE1")
        manifest, run, _, _, first_package, _, _, second_package, validation_order, validation_context = items
        authored = self.valid_authored(
            first_package, self.SYLLABUS, classification="REFINED", refined=None
        )
        with self.assertRaisesRegex(ValueError, "CROSS_VALIDATION_REFINED_STATEMENT_REQUIRED"):
            build_cross_validation(
                manifest, run, first_package, second_package,
                validation_order, validation_context, authored,
            )

    def test_missing_finding_must_reference_independent_claim(self):
        items = self.prepare("CORE1")
        manifest, run, _, _, first_package, _, _, second_package, validation_order, validation_context = items
        authored = self.valid_authored(first_package, self.SYLLABUS)
        authored["missing_findings"] = [{
            "second_claim_ref": "MATH-CL-ffffffffffffffff",
            "ground_truth_evidence_refs": [self.QUESTIONS],
            "rationale": "Independent pass found an omitted demand claim.",
        }]
        with self.assertRaisesRegex(ValueError, "CROSS_VALIDATION_SECOND_CLAIM_UNKNOWN"):
            build_cross_validation(
                manifest, run, first_package, second_package,
                validation_order, validation_context, authored,
            )

    def test_valid_missing_finding_is_preserved_not_mutated_into_first_package(self):
        items = self.prepare("CORE1")
        manifest, run, _, _, first_package, _, _, second_package, validation_order, validation_context = items
        before = copy.deepcopy(first_package)
        authored = self.valid_authored(first_package, self.SYLLABUS)
        authored["missing_findings"] = [{
            "second_claim_ref": second_package["claims"][0]["claim_id"],
            "ground_truth_evidence_refs": [self.QUESTIONS],
            "rationale": "Independent assessment pass identified an additional assessment demand.",
        }]
        validation = build_cross_validation(
            manifest, run, first_package, second_package,
            validation_order, validation_context, authored,
        )
        self.assertEqual(validation["missing_findings"][0]["classification"], "MISSING")
        self.assertEqual(first_package, before)


if __name__ == "__main__":
    unittest.main()
