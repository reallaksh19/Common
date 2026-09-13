#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

BP = Path(__file__).resolve().parents[1]


def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compiler = mod("bp_m2d_render_readiness", BP / "engine" / "compile_m2d_render_readiness.py")
POLICY = json.loads((BP / "policy" / "m2d-representation-requirements.v1.json").read_text())
PRIMITIVES = compiler.combined_primitive_registry()


class MotionInAPlaneRenderReadinessTests(unittest.TestCase):
    def report(self, policy=None, primitives=None):
        return compiler.compile_readiness(
            compiler.real_chapter_plan(),
            primitives or PRIMITIVES,
            policy or POLICY,
        )

    def test_real_chapter_becomes_fully_realizable_only_after_generic_2d_closure(self):
        report = self.report()
        self.assertEqual(report["summary"]["concept_count"], 10)
        self.assertEqual(report["summary"]["ready_count"], 10)
        self.assertEqual(report["summary"]["blocked_count"], 0)
        self.assertEqual(report["summary"]["status"], "READY_FOR_RENDER_ADAPTER")
        self.assertFalse(report["summary"]["release_authorized"])
        self.assertTrue(all(row["state"] == "READY_FOR_REALIZATION" for row in report["concepts"]))

    def test_policy_cannot_omit_a_real_concept(self):
        policy = copy.deepcopy(POLICY)
        policy["requirements"] = policy["requirements"][:-1]
        with self.assertRaisesRegex(AssertionError, "M2D_RENDER_POLICY_CONCEPT_COVERAGE_DRIFT"):
            self.report(policy=policy)

    def test_unknown_primitive_cannot_be_authorized(self):
        policy = copy.deepcopy(POLICY)
        row = next(x for x in policy["requirements"] if x["concept_id"] == "RELATIVE_MOTION_FOUNDATION")
        row["authorized_existing_primitive_refs"] = ["MAGIC_PROJECTILE_PICTURE"]
        with self.assertRaisesRegex(AssertionError, "M2D_RENDER_UNKNOWN_AUTHORIZED_PRIMITIVE"):
            self.report(policy=policy)

    def test_name_similarity_does_not_clear_a_declared_missing_job(self):
        policy = copy.deepcopy(POLICY)
        row = next(x for x in policy["requirements"] if x["concept_id"] == "PROJECTILE_FOUNDATION")
        row["authorized_existing_primitive_refs"] = ["TRAJECTORY_VIEW"]
        row["missing_primitive_capabilities"] = ["STATE_SEQUENCE_2D"]
        report = self.report(policy=policy)
        item = next(x for x in report["concepts"] if x["concept_id"] == "PROJECTILE_FOUNDATION")
        self.assertEqual(item["state"], "BLOCKED_NEEDS_PRIMITIVE")

    def test_policy_cannot_claim_ready_without_a_real_primitive(self):
        policy = copy.deepcopy(POLICY)
        row = next(x for x in policy["requirements"] if x["concept_id"] == "M2D_FOUNDATION")
        row["authorized_existing_primitive_refs"] = []
        with self.assertRaisesRegex(AssertionError, "M2D_RENDER_REQUIREMENT_UNSATISFIED_WITHOUT_PRIMITIVE"):
            self.report(policy=policy)

    def test_chapter_archetype_drift_is_detected(self):
        policy = copy.deepcopy(POLICY)
        row = next(x for x in policy["requirements"] if x["concept_id"] == "PROJECTILE_APEX")
        row["illustration_archetype"] = "ANATOMY"
        with self.assertRaisesRegex(AssertionError, "M2D_RENDER_ARCHETYPE_DRIFT"):
            self.report(policy=policy)

    def test_subject_wide_2d_extension_is_part_of_the_exact_registry_digest(self):
        ids = {row["primitive_id"] for row in PRIMITIVES["primitives"]}
        for required in [
            "CARTESIAN_FRAME_2D","VECTOR_COMPONENTS_2D","STATE_SEQUENCE_2D",
            "PATH_ANATOMY_2D","EVENT_COMPARE_2D","PARAMETRIC_ELIMINATION_BRIDGE_2D",
            "OBSERVER_LINE_OF_SIGHT_2D"
        ]:
            self.assertIn(required, ids)


if __name__ == "__main__":
    unittest.main()
