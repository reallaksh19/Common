#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

BP = Path(__file__).resolve().parents[1]
PHYS = BP.parent


def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compiler = mod("bp_m2d_render_readiness", BP / "engine" / "compile_m2d_render_readiness.py")
POLICY = json.loads((BP / "policy" / "m2d-representation-requirements.v1.json").read_text())
PRIMITIVES = json.loads((PHYS / "Representation" / "registry" / "physics-teaching-primitive-registry.json").read_text())


class MotionInAPlaneRenderReadinessTests(unittest.TestCase):
    def report(self, policy=None, primitives=None):
        return compiler.compile_readiness(
            compiler.real_chapter_plan(),
            primitives or PRIMITIVES,
            policy or POLICY,
        )

    def test_real_chapter_is_accounted_for_exactly_once(self):
        report = self.report()
        self.assertEqual(report["summary"]["concept_count"], 10)
        self.assertEqual(report["summary"]["ready_count"], 1)
        self.assertEqual(report["summary"]["blocked_count"], 9)
        self.assertEqual(report["summary"]["status"], "BLOCKED_REPRESENTATION_GAP")
        self.assertFalse(report["summary"]["release_authorized"])
        states = {row["concept_id"]: row["state"] for row in report["concepts"]}
        self.assertEqual(states["RELATIVE_MOTION_FOUNDATION"], "READY_FOR_REALIZATION")
        self.assertEqual(states["PROJECTILE_COMPONENT_CLOCK"], "BLOCKED_NEEDS_PRIMITIVE")

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

    def test_name_similarity_does_not_clear_missing_cognitive_job(self):
        policy = copy.deepcopy(POLICY)
        row = next(x for x in policy["requirements"] if x["concept_id"] == "PROJECTILE_FOUNDATION")
        row["authorized_existing_primitive_refs"] = ["TRAJECTORY_VIEW"]
        report = self.report(policy=policy)
        item = next(x for x in report["concepts"] if x["concept_id"] == "PROJECTILE_FOUNDATION")
        self.assertEqual(item["state"], "BLOCKED_NEEDS_PRIMITIVE")
        self.assertIn("PROJECTILE_STATE_SEQUENCE_2D", item["missing_primitive_capabilities"])

    def test_policy_cannot_claim_ready_without_a_real_primitive(self):
        policy = copy.deepcopy(POLICY)
        row = next(x for x in policy["requirements"] if x["concept_id"] == "M2D_FOUNDATION")
        row["missing_primitive_capabilities"] = []
        with self.assertRaisesRegex(AssertionError, "M2D_RENDER_REQUIREMENT_UNSATISFIED_WITHOUT_PRIMITIVE"):
            self.report(policy=policy)

    def test_chapter_archetype_drift_is_detected(self):
        policy = copy.deepcopy(POLICY)
        row = next(x for x in policy["requirements"] if x["concept_id"] == "PROJECTILE_APEX")
        row["illustration_archetype"] = "ANATOMY"
        with self.assertRaisesRegex(AssertionError, "M2D_RENDER_ARCHETYPE_DRIFT"):
            self.report(policy=policy)


if __name__ == "__main__":
    unittest.main()
