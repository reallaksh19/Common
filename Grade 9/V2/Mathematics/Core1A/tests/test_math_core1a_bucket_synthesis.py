#!/usr/bin/env python3
import importlib.util
import json
import sys
import unittest
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve()
C1A = HERE.parents[1]
ENGINE = C1A / "engine"
sys.path.insert(0, str(ENGINE))

import core1a_bucket_synthesis as buckets

SCHEMA = json.loads((C1A / "contracts" / "math-core1a-bucket-plan.schema.json").read_text(encoding="utf-8"))


class Core1ABucketSynthesisTests(unittest.TestCase):
    def lesson(self, cap, role, family, qrefs, pck, treatment="ACTIVE_STUDY"):
        return {
            "lesson_id": "MATH-C1L-" + buckets.digest(cap)[:16],
            "learner_title": cap.replace("MATH-", "").replace("-", " ").title(),
            "capability_ref": cap,
            "treatment": treatment,
            "scope_role": role,
            "assessment_question_refs": qrefs,
            "pck_asset_refs": [pck],
            "required_pck_jobs": ["COMPLETE_CONCEPT_RECONSTRUCTION"],
            "instructional_sequence": ["ANCHOR", "REPRESENT", "EXPLAIN", "WORKED", "GUIDED", "FADED", "INDEPENDENT", "VERIFY", "TRANSFER"],
            "representation_requirements": ["REP-" + cap],
            "problem_authoring_plans": [{"problem_family_ref": family, "instance_role": "WORKED"}],
            "verification_requirements": ["VERIFY-" + cap],
            "future_evidence_obligations": [{} for _ in range(8)],
            "scope_trace": {"study_scope_ref": "SCOPE", "study_model_capability_ref": cap},
        }

    def plan(self, cap, role, qrefs, prereqs, state, confidence, treatment, priority, family):
        return {
            "capability_ref": cap,
            "scope_role": role,
            "assessment_question_refs": qrefs,
            "prerequisite_refs": prereqs,
            "learner_state_readiness": state,
            "learner_state_confidence": confidence,
            "learner_state_observation_refs": ["OBS-" + cap],
            "treatment": treatment,
            "priority_band": priority,
            "sequencing_rationale": "Preserve learner-conditioned treatment from M-F.",
            "required_pck_jobs": ["COMPLETE_CONCEPT_RECONSTRUCTION"],
            "representation_requirements": ["REP-" + cap],
            "problem_family_refs": [family],
            "verification_requirements": ["VERIFY-" + cap],
            "future_evidence_obligations": [{"dimension": d, "status": "NOT_EVIDENCED", "evidence_needed": "future evidence"} for d in ["acquisition","independent_reconstruction","delayed_retention","near_transfer","far_transfer","mixed_discrimination","fluency","timed_performance"]],
        }

    def fixture(self):
        family = "MATH-PF-SHARED-MODEL"
        c1, c2, pre = "MATH-CAP-A", "MATH-CAP-B", "MATH-PREQ-P"
        pck1, pck2, pckp = "MATH-PCK-A-v1", "MATH-PCK-B-v1", "MATH-PCK-P-v1"
        lessons = [
            self.lesson(c1, "DIRECT_ASSESSED", family, ["Q1"], pck1, "ACTIVE_STUDY"),
            self.lesson(pre, "PREREQUISITE_SUPPORT", "MATH-PF-BRIDGE", [], pckp, "REPAIR_BEFORE"),
            self.lesson(c2, "DIRECT_ASSESSED", family, ["Q2"], pck2, "VERIFY_ONLY"),
        ]
        plans = [
            self.plan(c1, "DIRECT_ASSESSED", ["Q1"], [pre], "DEVELOPING", 0.82, "ACTIVE_STUDY", "CORE_STUDY", family),
            self.plan(pre, "PREREQUISITE_SUPPORT", [], [], "DEVELOPING", 0.91, "REPAIR_BEFORE", "EARLY_REPAIR", "MATH-PF-BRIDGE"),
            self.plan(c2, "DIRECT_ASSESSED", ["Q2"], [], "READY", 0.88, "VERIFY_ONLY", "VERIFY_AND_MOVE_ON", family),
        ]
        study = {
            "study_model_id": "MATH-LSM-0123456789abcdef",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "study_scope_ref": "SCOPE",
            "study_scope_digest": "0" * 64,
            "learner_state_snapshot_ref": "STATE",
            "learner_state_snapshot_digest": "1" * 64,
            "learner_attempt_mode": "PRESENT",
            "treatment_policy_version": "MATH-MF-TREATMENT-v1",
            "capability_plans": plans,
            "longitudinal_initialization": {"dimensions": ["acquisition","independent_reconstruction","delayed_retention","near_transfer","far_transfer","mixed_discrimination","fluency","timed_performance"], "invariant": "CURRENT_SUCCESS_DOES_NOT_CLOSE_DELAYED_OR_TRANSFER_OBLIGATIONS"},
            "input_digest": "2" * 64,
            "study_model_digest": "",
        }
        study["study_model_digest"] = buckets.digest(study, "study_model_digest")
        core1 = {
            "core1_study_plan_id": "MATH-C1SP-0123456789abcdef",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "release_class": "TEST_ONLY",
            "study_model_ref": study["study_model_id"],
            "study_model_digest": study["study_model_digest"],
            "lessons": lessons,
            "scope_completeness": {"required_capability_refs": [c1, pre, c2], "covered_capability_refs": [c1, pre, c2], "omitted_capability_refs": [], "status": "PASS"},
            "plan_digest": "a" * 64,
        }
        assets = {
            pck1: {"asset_id": pck1, "capability_refs": [c1], "anchor": "Use one shared mathematical structure to connect the first capability.", "reconstruction_route": ["identify the common structure", "apply it to the first capability"]},
            pck2: {"asset_id": pck2, "capability_refs": [c2], "anchor": "Use one shared mathematical structure to connect the second capability.", "reconstruction_route": ["identify the common structure", "apply it to the second capability"]},
            pckp: {"asset_id": pckp, "capability_refs": [pre], "anchor": "Repair the prerequisite before dependent work.", "reconstruction_route": ["reconstruct the prerequisite"]},
        }
        families = {
            family: {"family_id": family, "problem_signature": {"target_job": "coordinate both capabilities through one shared invariant"}},
            "MATH-PF-BRIDGE": {"family_id": "MATH-PF-BRIDGE", "problem_signature": {"target_job": "reconstruct a prerequisite bridge"}},
        }
        return core1, study, assets, families

    def test_bucket_synthesis_groups_shared_family_and_attaches_single_prerequisite(self):
        core1, study, assets, families = self.fixture()
        plan = buckets.synthesize_bucket_plan(core1, study, assets, families)
        jsonschema.validate(plan, SCHEMA)
        self.assertEqual(len(plan["buckets"]), 1)
        bucket = plan["buckets"][0]
        self.assertEqual(set(bucket["member_capability_refs"]), {"MATH-CAP-A", "MATH-CAP-B", "MATH-PREQ-P"})
        self.assertEqual(set(bucket["primary_capability_refs"]), {"MATH-CAP-A", "MATH-CAP-B"})
        self.assertEqual(bucket["supporting_capability_refs"], ["MATH-PREQ-P"])
        self.assertEqual(bucket["bucket_invariant"]["source_type"], "PROBLEM_FAMILY_TARGET_JOB")

    def test_learner_state_and_treatment_are_copied_not_reinvented(self):
        core1, study, assets, families = self.fixture()
        plan = buckets.synthesize_bucket_plan(core1, study, assets, families)
        rows = {r["capability_ref"]: r for r in plan["buckets"][0]["learner_treatment_by_capability"]}
        self.assertEqual(rows["MATH-CAP-A"]["learner_state_readiness"], "DEVELOPING")
        self.assertEqual(rows["MATH-CAP-B"]["learner_state_readiness"], "READY")
        self.assertEqual(rows["MATH-PREQ-P"]["treatment"], "REPAIR_BEFORE")
        self.assertNotIn("FOUNDATION", json.dumps(plan))
        self.assertNotIn("PARTIAL", json.dumps(plan))

    def test_treatment_drift_fails_closed(self):
        core1, study, assets, families = self.fixture()
        core1["lessons"][0]["treatment"] = "VERIFY_ONLY"
        with self.assertRaisesRegex(ValueError, "CORE1A_TREATMENT_DRIFT"):
            buckets.synthesize_bucket_plan(core1, study, assets, families)


if __name__ == "__main__":
    unittest.main(verbosity=2)
