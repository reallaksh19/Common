#!/usr/bin/env python3
"""Falsifier suite for spatial representation semantics (M-UPGRADE-2 item 4).

Each mutation is one of the visual-correctness defects the stress test named: a swapped
axis, a point moved out of its declared quadrant, a scale that breaks a declared relation,
an angle pair read off the drawing instead of declared, a parallel mark for something still
to be proved, and an attempt figure that plots its own answer.
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

PHASE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(PHASE / "engine"), str(PHASE / "fixtures" / "spatial")]

from validate_math_spatial_semantics import (  # noqa: E402
    FALSIFIERS,
    audit_spatial,
    load,
    seal,
    validate_spatial,
)

FIXTURE = load(PHASE / "fixtures" / "spatial"
               / "math-spatial-representations.fixture.json")
POLICY = load(PHASE / "policies" / "math-spatial-semantics-policy.json")
SCHEMA = json.loads((PHASE / "contracts" / "math-spatial-representation.schema.json")
                    .read_text(encoding="utf-8"))


def corpus() -> list[dict]:
    return copy.deepcopy(FIXTURE["representations"])


def pick(primitive: str, surface: str = "ATTEMPT") -> dict:
    return copy.deepcopy(next(r for r in FIXTURE["representations"]
                              if r["primitive"] == primitive and r["surface"] == surface))


class SpatialPositive(unittest.TestCase):
    def test_every_representation_validates_against_the_contract(self):
        validator = Draft202012Validator(SCHEMA)
        for r in corpus():
            with self.subTest(primitive=r["primitive"], surface=r["surface"]):
                validator.validate(r)

    def test_audit_passes_on_the_reference_corpus(self):
        audit = audit_spatial(corpus())
        self.assertEqual(audit["status"], "PASS")
        self.assertEqual(audit["primitives"],
                         ["ANGLE_FIGURE", "COORDINATE_PLANE", "NUMBER_LINE"])

    def test_exit_gate_learner_must_supply_is_separated_from_givens(self):
        """Issue #358 exit gate: at least one spatial item proves the separation."""
        attempt = pick("COORDINATE_PLANE", "ATTEMPT")
        plan = attempt["representation_plan"]
        self.assertEqual(plan["givens"], ["A", "B"])
        self.assertEqual(plan["learner_must_supply"], ["M"])
        self.assertEqual(set(plan["givens"]) & set(plan["learner_must_supply"]), set())
        target = next(p for p in attempt["semantics"]["point_coordinates"]
                      if p["label"] == "M")
        self.assertEqual(target["role"], "LEARNER_MUST_SUPPLY")
        self.assertFalse(target["plotted"], "the attempt figure must not plot the answer")
        self.assertEqual(validate_spatial(attempt), [])

    def test_the_same_point_is_plotted_on_the_solution_surface(self):
        solution = pick("COORDINATE_PLANE", "SOLUTION")
        target = next(p for p in solution["semantics"]["point_coordinates"]
                      if p["label"] == "M")
        self.assertTrue(target["plotted"])
        self.assertEqual(validate_spatial(solution), [])

    def test_coordinate_plane_declares_the_full_semantics(self):
        semantics = pick("COORDINATE_PLANE")["semantics"]
        for field in POLICY["coordinate_plane"]["required_declarations"]:
            self.assertIn(field, semantics, field)

    def test_audit_is_deterministic(self):
        self.assertEqual(audit_spatial(corpus())["corpus_digest"],
                         audit_spatial(corpus())["corpus_digest"])

    def test_policy_declares_every_falsifier_the_engine_can_raise(self):
        self.assertEqual(sorted(POLICY["falsifiers"]), sorted(FALSIFIERS))

    def test_spatial_semantics_are_classified_as_subject_correctness(self):
        self.assertEqual(POLICY["classification"], "SUBJECT_CORRECTNESS")


class SpatialFalsifiers(unittest.TestCase):
    def expect(self, code: str, representations: list[dict]):
        with self.assertRaises(ValueError) as ctx:
            audit_spatial(representations)
        self.assertIn(code, str(ctx.exception), f"expected {code}, got {ctx.exception}")

    # 1 — the answer plotted on the attempt page
    def test_ATTEMPT_REPRESENTATION_REVEALS_TARGET_coordinate_plane(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        next(p for p in bad["semantics"]["point_coordinates"]
             if p["label"] == "M")["plotted"] = True
        self.expect("ATTEMPT_REPRESENTATION_REVEALS_TARGET", [seal(bad)])

    # 2
    def test_ATTEMPT_REPRESENTATION_REVEALS_TARGET_number_line(self):
        bad = pick("NUMBER_LINE")
        next(p for p in bad["semantics"]["marked_points"]
             if p["label"] == "root2")["plotted"] = True
        self.expect("ATTEMPT_REPRESENTATION_REVEALS_TARGET", [seal(bad)])

    # 3
    def test_ATTEMPT_REPRESENTATION_REVEALS_TARGET_angle_measure(self):
        bad = pick("ANGLE_FIGURE")
        next(a for a in bad["semantics"]["marked_angles"]
             if a["label"] == "b")["measure_shown"] = True
        self.expect("ATTEMPT_REPRESENTATION_REVEALS_TARGET", [seal(bad)])

    # 4
    def test_SPATIAL_GIVEN_AND_TARGET_CONFLATED(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        bad["representation_plan"]["givens"] = ["A", "B", "M"]
        self.expect("SPATIAL_GIVEN_AND_TARGET_CONFLATED", [seal(bad)])

    # 5
    def test_SPATIAL_TARGET_NOT_DECLARED(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        bad["representation_plan"]["learner_must_supply"] = ["Z"]
        self.expect("SPATIAL_TARGET_NOT_DECLARED", [seal(bad)])

    # 6 — the swapped/inverted axis
    def test_AXIS_ORIENTATION_INCORRECT(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        bad["semantics"]["axis_direction"]["y"] = "DOWN_POSITIVE"
        self.expect("AXIS_ORIENTATION_INCORRECT", [seal(bad)])

    # 7
    def test_AXIS_ORIENTATION_INCORRECT_number_line(self):
        bad = pick("NUMBER_LINE")
        bad["semantics"]["direction"] = "LEFT_POSITIVE"
        self.expect("AXIS_ORIENTATION_INCORRECT", [seal(bad)])

    # 8 — a point outside its own declared domain renders cleanly but is wrong
    def test_COORDINATE_POINT_MISPLACED(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        next(p for p in bad["semantics"]["point_coordinates"]
             if p["label"] == "B")["x"] = 99
        self.expect("COORDINATE_POINT_MISPLACED", [seal(bad)])

    # 9 — the declared relation no longer holds for the declared coordinates
    def test_VISUAL_SEMANTIC_RELATION_MISMATCH_horizontal(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        next(p for p in bad["semantics"]["point_coordinates"]
             if p["label"] == "B")["y"] = 5
        self.expect("VISUAL_SEMANTIC_RELATION_MISMATCH", [seal(bad)])

    # 10
    def test_VISUAL_SEMANTIC_RELATION_MISMATCH_midpoint(self):
        bad = pick("COORDINATE_PLANE", "SOLUTION")
        next(p for p in bad["semantics"]["point_coordinates"]
             if p["label"] == "M")["x"] = 2
        self.expect("VISUAL_SEMANTIC_RELATION_MISMATCH", [seal(bad)])

    # 11
    def test_VISUAL_SEMANTIC_RELATION_MISMATCH_quadrant(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        bad["semantics"]["declared_relations"].append(
            {"kind": "IN_QUADRANT_I", "point_labels": ["A"]})
        self.expect("VISUAL_SEMANTIC_RELATION_MISMATCH", [seal(bad)])

    # 12
    def test_VISUAL_SEMANTIC_RELATION_MISMATCH_collinear(self):
        bad = pick("COORDINATE_PLANE", "SOLUTION")
        bad["semantics"]["point_coordinates"].append(
            {"label": "D", "x": 2, "y": 1, "role": "GIVEN", "plotted": True})
        bad["representation_plan"]["givens"].append("D")
        bad["semantics"]["declared_relations"].append(
            {"kind": "COLLINEAR", "point_labels": ["A", "B", "D"]})
        self.expect("VISUAL_SEMANTIC_RELATION_MISMATCH", [seal(bad)])

    # 13 — angle-pair identity read off the drawing rather than declared
    def test_ANGLE_PAIR_IDENTITY_MISMATCH_on_measures(self):
        bad = pick("ANGLE_FIGURE")
        angle_b = next(a for a in bad["semantics"]["marked_angles"] if a["label"] == "b")
        angle_b["measure_deg"] = 65.0          # co-interior angles must sum to 180
        self.expect("ANGLE_PAIR_IDENTITY_MISMATCH", [seal(bad)])

    # 14
    def test_ANGLE_PAIR_IDENTITY_MISMATCH_on_vertex_structure(self):
        bad = pick("ANGLE_FIGURE")
        bad["semantics"]["declared_angle_pairs"] = [
            {"kind": "LINEAR_PAIR", "angle_labels": ["a", "b"]}]
        self.expect("ANGLE_PAIR_IDENTITY_MISMATCH", [seal(bad)])

    # 15
    def test_ANGLE_PAIR_IDENTITY_MISMATCH_on_undeclared_angle(self):
        bad = pick("ANGLE_FIGURE")
        bad["semantics"]["declared_angle_pairs"] = [
            {"kind": "CO_INTERIOR", "angle_labels": ["a", "zz"]}]
        self.expect("ANGLE_PAIR_IDENTITY_MISMATCH", [seal(bad)])

    # 16 — the figure assumes what must be proved
    def test_GEOMETRY_ASSUMPTION_LEAK_on_unproved_parallel(self):
        bad = pick("ANGLE_FIGURE")
        bad["semantics"]["declared_parallel_facts"] = [
            {"line_a": "PQ", "line_b": "RS", "status": "TO_BE_PROVED"}]
        self.expect("GEOMETRY_ASSUMPTION_LEAK", [seal(bad)])

    # 17
    def test_GEOMETRY_ASSUMPTION_LEAK_on_undeclared_parallel_mark(self):
        bad = pick("ANGLE_FIGURE")
        bad["semantics"]["parallel_marks"].append({"line_a": "PT", "line_b": "RU"})
        self.expect("GEOMETRY_ASSUMPTION_LEAK", [seal(bad)])

    # 18
    def test_SPATIAL_REPRESENTATION_SEMANTICS_INVALID_on_tick_interval(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        bad["semantics"]["tick_interval"] = {"x": 50, "y": 50}
        self.expect("SPATIAL_REPRESENTATION_SEMANTICS_INVALID", [seal(bad)])

    # 19
    def test_SPATIAL_REPRESENTATION_SEMANTICS_INVALID_on_origin_outside_domain(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        bad["semantics"]["x_domain"] = [2, 8]
        self.expect("SPATIAL_REPRESENTATION_SEMANTICS_INVALID", [seal(bad)])

    # 20
    def test_SPATIAL_REPRESENTATION_SEMANTICS_INVALID_on_given_without_coordinates(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        point = next(p for p in bad["semantics"]["point_coordinates"] if p["label"] == "A")
        point["x"], point["y"] = None, None
        self.expect("SPATIAL_REPRESENTATION_SEMANTICS_INVALID", [seal(bad)])

    # 21
    def test_SPATIAL_REPRESENTATION_SEMANTICS_INVALID_on_digest_drift(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        bad["spatial_digest"] = "0" * 64
        self.expect("SPATIAL_REPRESENTATION_SEMANTICS_INVALID", [bad])

    # 22
    def test_SPATIAL_REPRESENTATION_SEMANTICS_INVALID_on_degenerate_angle(self):
        bad = pick("ANGLE_FIGURE")
        angle = next(a for a in bad["semantics"]["marked_angles"] if a["label"] == "a")
        angle["ray_b"] = angle["ray_a"]
        self.expect("SPATIAL_REPRESENTATION_SEMANTICS_INVALID", [seal(bad)])

    # 23
    def test_contract_rejects_a_coordinate_plane_without_axis_direction(self):
        bad = pick("COORDINATE_PLANE", "ATTEMPT")
        del bad["semantics"]["axis_direction"]
        with self.assertRaises(Exception):
            Draft202012Validator(SCHEMA).validate(bad)

    # 24
    def test_contract_rejects_a_zero_tick_interval(self):
        bad = pick("NUMBER_LINE")
        bad["semantics"]["tick_interval"] = 0
        with self.assertRaises(Exception):
            Draft202012Validator(SCHEMA).validate(bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
