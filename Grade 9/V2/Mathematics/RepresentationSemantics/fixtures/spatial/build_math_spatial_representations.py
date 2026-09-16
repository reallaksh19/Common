#!/usr/bin/env python3
"""Build the spatial-representation fixture.

Three data instances of the one generic contract, one per spatial class the stress test
exercised:

* `COORDINATE_PLANE` attempt surface for the Coordinate Geometry item whose midpoint M the
  learner must supply — M is declared `LEARNER_MUST_SUPPLY` and is **not** plotted;
* `COORDINATE_PLANE` solution surface for the same item, where M *is* plotted and the
  midpoint relation is asserted and checked;
* `NUMBER_LINE` for locating √2 between consecutive integers (Number Systems);
* `ANGLE_FIGURE` for a transversal item where the parallel fact is GIVEN and the
  co-interior pair is declared rather than read off the drawing (Lines & Angles).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PHASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PHASE / "engine"))

from validate_math_spatial_semantics import seal  # noqa: E402

OUT = PHASE / "fixtures" / "spatial" / "math-spatial-representations.fixture.json"


def coordinate_attempt() -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "surface": "ATTEMPT",
        "primitive": "COORDINATE_PLANE",
        "semantics": {
            "kind": "COORDINATE_PLANE",
            "x_domain": [-6, 6],
            "y_domain": [-2, 6],
            "tick_interval": {"x": 1, "y": 1},
            "origin": {"x": 0, "y": 0},
            "axis_direction": {"x": "RIGHT_POSITIVE", "y": "UP_POSITIVE"},
            "point_coordinates": [
                {"label": "A", "x": -2, "y": 3, "role": "GIVEN", "plotted": True},
                {"label": "B", "x": 4, "y": 3, "role": "GIVEN", "plotted": True},
                {"label": "M", "x": 1, "y": 3, "role": "LEARNER_MUST_SUPPLY",
                 "plotted": False},
            ],
            "declared_relations": [
                {"kind": "HORIZONTAL_SEGMENT", "point_labels": ["A", "B"]},
            ],
        },
        "representation_plan": {
            "givens": ["A", "B"],
            "learner_must_supply": ["M"],
            "answer_targets": ["M"],
        },
    }


def coordinate_solution() -> dict:
    spatial = coordinate_attempt()
    spatial["surface"] = "SOLUTION"
    points = spatial["semantics"]["point_coordinates"]
    points[2] = {"label": "M", "x": 1, "y": 3, "role": "DERIVED_CHECK", "plotted": True}
    spatial["semantics"]["declared_relations"] = [
        {"kind": "HORIZONTAL_SEGMENT", "point_labels": ["A", "B", "M"]},
        {"kind": "MIDPOINT_OF", "point_labels": ["M", "A", "B"]},
        {"kind": "EQUIDISTANT_FROM_FIRST", "point_labels": ["M", "A", "B"]},
    ]
    spatial["representation_plan"] = {
        "givens": ["A", "B"],
        "learner_must_supply": [],
        "answer_targets": ["M"],
    }
    return spatial


def number_line() -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "surface": "ATTEMPT",
        "primitive": "NUMBER_LINE",
        "semantics": {
            "kind": "NUMBER_LINE",
            "domain": [0, 4],
            "tick_interval": 0.5,
            "direction": "RIGHT_POSITIVE",
            "marked_points": [
                {"label": "1", "value": 1, "role": "GIVEN", "plotted": True},
                {"label": "2", "value": 2, "role": "GIVEN", "plotted": True},
                {"label": "root2", "value": 1.4142135624, "role": "LEARNER_MUST_SUPPLY",
                 "plotted": False},
            ],
        },
        "representation_plan": {
            "givens": ["1", "2"],
            "learner_must_supply": ["root2"],
            "answer_targets": ["root2"],
        },
    }


def angle_figure() -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "surface": "ATTEMPT",
        "primitive": "ANGLE_FIGURE",
        "semantics": {
            "kind": "ANGLE_FIGURE",
            "vertices": [
                {"label": "P", "x": 0, "y": 0},
                {"label": "Q", "x": 6, "y": 0},
                {"label": "R", "x": 0, "y": 4},
                {"label": "S", "x": 6, "y": 4},
                {"label": "T", "x": 2, "y": -2},
                {"label": "U", "x": 4, "y": 6},
            ],
            "rays": [
                {"from": "P", "to": "Q"},
                {"from": "R", "to": "S"},
                {"from": "P", "to": "T"},
                {"from": "R", "to": "U"},
            ],
            "marked_angles": [
                {"label": "a", "vertex": "P", "ray_a": "Q", "ray_b": "T",
                 "measure_deg": 65.0, "role": "GIVEN", "measure_shown": True},
                {"label": "b", "vertex": "R", "ray_a": "S", "ray_b": "U",
                 "measure_deg": 115.0, "role": "LEARNER_MUST_SUPPLY",
                 "measure_shown": False},
            ],
            "declared_angle_pairs": [
                {"kind": "CO_INTERIOR", "angle_labels": ["a", "b"]},
            ],
            "declared_parallel_facts": [
                {"line_a": "PQ", "line_b": "RS", "status": "GIVEN"},
            ],
            "parallel_marks": [
                {"line_a": "PQ", "line_b": "RS"},
            ],
        },
        "representation_plan": {
            "givens": ["a"],
            "learner_must_supply": ["b"],
            "answer_targets": ["b"],
        },
    }


BUILDERS = (coordinate_attempt, coordinate_solution, number_line, angle_figure)


def build() -> dict:
    return {
        "fixture_id": "MATH-SPATIAL-REPRESENTATIONS-v1",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "purpose": "Data instances of the generic spatial-representation contract, one per "
                   "spatial class exercised by the seven-topic stress test.",
        "representations": [seal(builder()) for builder in BUILDERS],
    }


def main() -> None:
    payload = build()
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: {len(payload['representations'])} representations")
    for r in payload["representations"]:
        print(f"  {r['primitive']:<18} {r['surface']:<9} "
              f"must_supply={r['representation_plan']['learner_must_supply']} "
              f"{r['spatial_id']}")


if __name__ == "__main__":
    main()
