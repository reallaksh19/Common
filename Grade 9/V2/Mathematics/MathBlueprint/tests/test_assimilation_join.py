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
    build_validation_work_order,
    materialize_context,
    seal_specialist_package,
)
from build_assimilation_demand import (
    apply_assimilation_demand,
    build_assimilation_demand,
    seal_learner_state,
)


class AssimilationJoinTests(unittest.TestCase):
    SUBTOPIC = "ALG-VIETA"
    BUNDLE = "MATH-HB-0000000000000002"
    SYLLABUS = "GT-SYLLABUS-aaaaaaaaaaaaaaaa"
    QUESTIONS = "GT-QUESTION_CORPUS-bbbbbbbbbbbbbbbb"

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
                    "ref": "fixture/syllabus",
                    "digest": "a" * 64,
                    "source_locator": "Algebra",
                    "scope_refs": [self.SUBTOPIC],
                    "notes": None,
                    "conflict_refs": [],
                },
                {
                    "evidence_id": self.QUESTIONS,
                    "evidence_type": "QUESTION_CORPUS",
                    "authority_class": "ORIGINAL_EVIDENCE",
                    "availability": "PRESENT",
                    "ref": "fixture/questions",
                    "digest": "b" * 64,
                    "source_locator": "Q1-Q8",
                    "scope_refs": [self.SUBTOPIC],
                    "notes": None,
                    "conflict_refs": [],
                },
            ],
            "manifest_digest": "",
        })

    def routed_run(self, manifest, purpose="CONSOLIDATION"):
        mode = {
            "FIRST_STUDY": "STARTER",
            "CONSOLIDATION": "PRACTICE",
            "REVISION": "REVISION",
            "COMPETITIVE_EXAM": "COMPETITION",
        }[purpose]
        return seal_learning_run({
            "run_id": "",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "ground_truth_ref": manifest["manifest_id"],
            "ground_truth_digest": manifest["manifest_digest"],
            "control_plane": {
                "learner_prior_percent": 50,
                "learning_purpose": purpose,
                "product_mode": mode,
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
                "first_role": "CORE1",
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

    def cross_validated(self, purpose="CONSOLIDATION", classification="CONFIRMED"):
        manifest = self.manifest()
        run = self.routed_run(manifest, purpose)
        first_order = build_first_work_order(manifest, run, self.BUNDLE, "join-core1")
        first_context = materialize_context(manifest, run, first_order)
        first = seal_specialist_package(manifest, run, first_order, first_context, {
            "claims": [{
                "local_key": "sem",
                "claim_type": "CONCEPT",
                "statement": "The sum and product of roots are encoded by coefficients.",
                "subtopic_ref": self.SUBTOPIC,
                "evidence_refs": [self.SYLLABUS],
                "confidence": "HIGH",
                "dependency_local_keys": [],
                "unresolved_issue_refs": [],
            }]
        })
        second_order = build_second_independent_work_order(
            manifest, run, self.BUNDLE, first, "join-core2"
        )
        second_context = materialize_context(manifest, run, second_order)
        second = seal_specialist_package(manifest, run, second_order, second_context, {
            "claims": [{
                "local_key": "assess",
                "claim_type": "QUESTION_DEMAND",
                "statement": "Questions require recognizing the useful symmetric relation before calculation.",
                "subtopic_ref": self.SUBTOPIC,
                "evidence_refs": [self.QUESTIONS],
                "confidence": "HIGH",
                "dependency_local_keys": [],
                "unresolved_issue_refs": [],
            }]
        })
        validation_order = build_validation_work_order(
            manifest, run, self.BUNDLE, first, second
        )
        validation_context = materialize_context(
            manifest, run, validation_order, packages=[first, second]
        )
        record = {
            "first_claim_ref": first["claims"][0]["claim_id"],
            "classification": classification,
            "ground_truth_evidence_refs": [] if classification == "UNKNOWN" else [self.SYLLABUS],
            "rationale": "Independent validation against original evidence.",
            "refined_statement": None,
        }
        validation = build_cross_validation(
            manifest, run, first, second, validation_order, validation_context,
            {"records": [record], "missing_findings": []},
        )
        cross_run = apply_cross_validation(run, first, second, validation)
        return manifest, cross_run, first, second, validation

    def spec(self, run, first, second, *, origin_refs=None, learner_state_ref=None, blocking=None, deferred=None):
        origins = origin_refs or [first["claims"][0]["claim_id"], second["claims"][0]["claim_id"]]
        return {
            "schema_version": "1.0.0",
            "run_ref": run["run_id"],
            "bundle_ref": self.BUNDLE,
            "learner_capability_state_ref": learner_state_ref,
            "obligations": [{
                "local_key": "understand-and-recognize",
                "obligation_type": "INFERENCE_BRIDGE",
                "statement": "Connect coefficient information to the symmetric root relation before selecting a calculation.",
                "origin_claim_refs": origins,
                "capability_refs": ["CAP-VIETA-01"],
                "required_before_core2a": True,
                "notes": None,
            }],
            "owner_constraints": [{
                "constraint_id": "OWNER-C-1",
                "mode": "SOFT",
                "target": "SEQUENCING",
                "instruction": "Keep the source anchor after the concept bridge."
            }],
            "blocking_conflict_record_refs": blocking or [],
            "deferred_conflicts": deferred or [],
            "unresolved_issue_refs": [],
        }

    def test_join_requires_cross_validated_run(self):
        manifest = self.manifest(); run = self.routed_run(manifest)
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_REQUIRES_CROSS_VALIDATED"):
            build_assimilation_demand(run, {}, {}, {}, {
                "schema_version": "1.0.0", "run_ref": run["run_id"], "bundle_ref": self.BUNDLE,
                "learner_capability_state_ref": None, "obligations": [{}], "owner_constraints": [],
                "blocking_conflict_record_refs": [], "deferred_conflicts": [], "unresolved_issue_refs": []
            })

    def test_absent_learner_state_stays_unknown_not_weak(self):
        _, run, first, second, validation = self.cross_validated()
        demand = build_assimilation_demand(
            run, first, second, validation, self.spec(run, first, second)
        )
        self.assertEqual(demand["learner_gaps"][0]["readiness"], "UNKNOWN")
        self.assertEqual(
            demand["learner_gaps"][0]["gap_state"],
            "UNKNOWN_REQUIRES_PROBE_OR_FULL_SUPPORT",
        )
        self.assertTrue(any(x["unknown_type"] == "LEARNER_CAPABILITY" for x in demand["unknowns"]))
        self.assertEqual(demand["owner_constraints"][0]["authority_class"], "OWNER_CONTROL")
        updated = apply_assimilation_demand(run, demand)
        self.assertEqual(updated["current_state"], "JOIN_READY")

    def test_capability_state_is_used_without_replacing_prior(self):
        _, run, first, second, validation = self.cross_validated()
        state = seal_learner_state(run, self.BUNDLE, {
            "capabilities": [{
                "capability_ref": "CAP-VIETA-01",
                "readiness": "DEVELOPING",
                "basis": "OWNER_DECLARED_BASELINE",
                "evidence_refs": [],
                "owner_control_ref": "OWNER-BASELINE-1",
                "notes": "Operational starting baseline, not evidence."
            }]
        })
        demand = build_assimilation_demand(
            run, first, second, validation,
            self.spec(run, first, second, learner_state_ref=state["state_id"]),
            learner_state=state,
        )
        gap = demand["learner_gaps"][0]
        self.assertEqual(gap["readiness"], "DEVELOPING")
        self.assertEqual(gap["gap_state"], "BRIDGE_OR_PRACTICE_REQUIRED")
        self.assertEqual(gap["basis"], "OWNER_DECLARED_BASELINE")
        self.assertEqual(state["prior_percent"], 50)

    def test_competition_purpose_cannot_drop_foundations(self):
        _, run, first, second, validation = self.cross_validated("COMPETITIVE_EXAM")
        demand = build_assimilation_demand(
            run, first, second, validation, self.spec(run, first, second)
        )
        self.assertIn("RECOGNIZE_STRUCTURE_UNDER_DISGUISE", demand["purpose_requirements"])
        self.assertIn("DO_NOT_SKIP_NECESSARY_FOUNDATIONS", demand["purpose_requirements"])

    def test_unknown_claim_is_preserved_and_cannot_ground_obligation(self):
        _, run, first, second, validation = self.cross_validated(classification="UNKNOWN")
        self.assertEqual(validation["records"][0]["classification"], "UNKNOWN")
        spec = self.spec(
            run, first, second,
            origin_refs=[first["claims"][0]["claim_id"]],
        )
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_OBLIGATION_ORIGIN_NOT_ADMISSIBLE"):
            build_assimilation_demand(run, first, second, validation, spec)

    def test_conflict_requires_explicit_disposition(self):
        _, run, first, second, validation = self.cross_validated(classification="CONTRADICTED")
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_CONFLICT_DISPOSITION_MISSING"):
            build_assimilation_demand(
                run, first, second, validation,
                self.spec(run, first, second, origin_refs=[second["claims"][0]["claim_id"]]),
            )

    def test_blocking_conflict_blocks_run_but_preserves_conflict(self):
        _, run, first, second, validation = self.cross_validated(classification="CONTRADICTED")
        conflict_ref = validation["records"][0]["record_id"]
        spec = self.spec(
            run, first, second,
            origin_refs=[second["claims"][0]["claim_id"]],
            blocking=[conflict_ref],
        )
        demand = build_assimilation_demand(run, first, second, validation, spec)
        self.assertEqual(demand["status"], "BLOCKED_CONFLICT")
        self.assertTrue(demand["conflicts"][0]["blocking"])
        updated = apply_assimilation_demand(run, demand)
        self.assertEqual(updated["current_state"], "BLOCKED_CONFLICT")

    def test_deferred_conflict_is_visible_and_join_can_continue(self):
        _, run, first, second, validation = self.cross_validated(classification="UNSUPPORTED")
        conflict_ref = validation["records"][0]["record_id"]
        spec = self.spec(
            run, first, second,
            origin_refs=[second["claims"][0]["claim_id"]],
            deferred=[{"record_ref": conflict_ref, "reason": "Not used by any current assimilation obligation."}],
        )
        demand = build_assimilation_demand(run, first, second, validation, spec)
        self.assertEqual(demand["status"], "JOIN_READY")
        self.assertFalse(demand["conflicts"][0]["blocking"])
        self.assertIsNotNone(demand["conflicts"][0]["defer_reason"])


if __name__ == "__main__":
    unittest.main()
