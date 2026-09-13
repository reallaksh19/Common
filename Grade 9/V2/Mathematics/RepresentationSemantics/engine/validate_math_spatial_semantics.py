#!/usr/bin/env python3
"""Spatial representation semantics (M-UPGRADE-2 item 4).

Coordinate Geometry made the point that generalises to every spatial topic: a clean,
in-bounds, deterministically rendered figure can still be mathematically wrong, and an
"answer-neutral" attempt page can still give the answer away through the picture.

So a spatial primitive is not `points + axes + relations`. It declares its own semantics —
domain, tick interval, origin, axis direction, coordinates, angle-pair identity, parallel
facts — and the representation plan declares which objects are **givens** and which the
learner **must supply**. Both are then checked.

This sits under *subject correctness*, not `VISUAL_USABILITY`.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any

PHASE = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = PHASE / "policies" / "math-spatial-semantics-policy.json"

FALSIFIERS = (
    "SPATIAL_REPRESENTATION_SEMANTICS_INVALID",
    "ATTEMPT_REPRESENTATION_REVEALS_TARGET",
    "SPATIAL_GIVEN_AND_TARGET_CONFLATED",
    "SPATIAL_TARGET_NOT_DECLARED",
    "COORDINATE_POINT_MISPLACED",
    "AXIS_ORIENTATION_INCORRECT",
    "VISUAL_SEMANTIC_RELATION_MISMATCH",
    "ANGLE_PAIR_IDENTITY_MISMATCH",
    "GEOMETRY_ASSUMPTION_LEAK",
    "SPATIAL_SEMANTICS_GATE_FAILED",
)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def load(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def seal(spatial: dict) -> dict:
    out = copy.deepcopy(spatial)
    out.pop("spatial_id", None)
    out.pop("spatial_digest", None)
    out["spatial_id"] = "MATH-SPATIAL-" + digest(out)[:16]
    out["spatial_digest"] = digest(out, "spatial_digest")
    return out


# --------------------------------------------------------------------------
# shared plan checks
# --------------------------------------------------------------------------
def _labels_and_roles(spatial: dict) -> dict[str, str]:
    semantics = spatial["semantics"]
    kind = semantics["kind"]
    if kind == "COORDINATE_PLANE":
        return {p["label"]: p["role"] for p in semantics["point_coordinates"]}
    if kind == "NUMBER_LINE":
        return {p["label"]: p["role"] for p in semantics["marked_points"]}
    return {a["label"]: a["role"] for a in semantics["marked_angles"]}


def _plan_failures(spatial: dict) -> list[str]:
    plan = spatial["representation_plan"]
    roles = _labels_and_roles(spatial)
    failures: list[str] = []

    overlap = sorted(set(plan["givens"]) & set(plan["learner_must_supply"]))
    if overlap:
        failures.append(f"SPATIAL_GIVEN_AND_TARGET_CONFLATED:{','.join(overlap)}")
    target_overlap = sorted(set(plan["givens"]) & set(plan["answer_targets"]))
    if target_overlap:
        failures.append(f"SPATIAL_GIVEN_AND_TARGET_CONFLATED:answer:{','.join(target_overlap)}")

    for label in plan["givens"] + plan["learner_must_supply"] + plan["answer_targets"]:
        if label not in roles:
            failures.append(f"SPATIAL_TARGET_NOT_DECLARED:{label}")

    for label, role in sorted(roles.items()):
        if role == "GIVEN" and label not in plan["givens"]:
            failures.append(f"SPATIAL_TARGET_NOT_DECLARED:given_not_in_plan:{label}")
        if role == "LEARNER_MUST_SUPPLY" and label not in plan["learner_must_supply"]:
            failures.append(f"SPATIAL_TARGET_NOT_DECLARED:target_not_in_plan:{label}")
    return failures


# --------------------------------------------------------------------------
# COORDINATE_PLANE
# --------------------------------------------------------------------------
def _coordinate_plane_failures(spatial: dict, policy: dict) -> list[str]:
    s = spatial["semantics"]
    failures: list[str] = []
    attempt = spatial["surface"] == "ATTEMPT"
    x_lo, x_hi = s["x_domain"]
    y_lo, y_hi = s["y_domain"]

    if x_lo >= x_hi or y_lo >= y_hi:
        failures.append("SPATIAL_REPRESENTATION_SEMANTICS_INVALID:empty_domain")
    min_ticks = int(policy["coordinate_plane"]["min_ticks_per_axis"])
    for axis, (lo, hi, step) in {
        "x": (x_lo, x_hi, s["tick_interval"]["x"]),
        "y": (y_lo, y_hi, s["tick_interval"]["y"]),
    }.items():
        if hi > lo and (hi - lo) / step < min_ticks:
            failures.append(f"SPATIAL_REPRESENTATION_SEMANTICS_INVALID:tick_interval_{axis}")

    if policy["coordinate_plane"]["require_canonical_axis_direction"]:
        if s["axis_direction"]["x"] != "RIGHT_POSITIVE":
            failures.append(f"AXIS_ORIENTATION_INCORRECT:x:{s['axis_direction']['x']}")
        if s["axis_direction"]["y"] != "UP_POSITIVE":
            failures.append(f"AXIS_ORIENTATION_INCORRECT:y:{s['axis_direction']['y']}")

    if not (x_lo <= s["origin"]["x"] <= x_hi and y_lo <= s["origin"]["y"] <= y_hi):
        failures.append("SPATIAL_REPRESENTATION_SEMANTICS_INVALID:origin_outside_domain")

    coords: dict[str, tuple[float, float]] = {}
    for point in s["point_coordinates"]:
        label, role = point["label"], point["role"]
        x, y = point.get("x"), point.get("y")
        plotted = point.get("plotted", role == "GIVEN")
        if role == "GIVEN":
            if x is None or y is None:
                failures.append(f"SPATIAL_REPRESENTATION_SEMANTICS_INVALID:"
                                f"given_without_coordinates:{label}")
                continue
        if x is None or y is None:
            continue
        coords[label] = (float(x), float(y))
        if not (x_lo <= x <= x_hi and y_lo <= y <= y_hi):
            failures.append(f"COORDINATE_POINT_MISPLACED:{label}:outside_declared_domain")
        # the answer must not be drawn on the attempt page
        if attempt and plotted and role in ("LEARNER_MUST_SUPPLY", "DERIVED_CHECK"):
            failures.append(f"ATTEMPT_REPRESENTATION_REVEALS_TARGET:{label}")

    for relation in s["declared_relations"]:
        failures.extend(_relation_failures(relation, coords, policy))
    return failures


def _relation_failures(relation: dict, coords: dict[str, tuple[float, float]],
                       policy: dict) -> list[str]:
    tol = float(policy["coordinate_plane"]["coordinate_tolerance"])
    kind = relation["kind"]
    labels = relation["point_labels"]
    missing = [l for l in labels if l not in coords]
    if missing:
        # a relation over a point the learner has not supplied yet is legitimate on the
        # attempt surface; a relation over an undeclared point is not
        return []
    points = [coords[l] for l in labels]
    out: list[str] = []

    def mismatch(detail: str) -> None:
        out.append(f"VISUAL_SEMANTIC_RELATION_MISMATCH:{kind}:{','.join(labels)}:{detail}")

    if kind == "HORIZONTAL_SEGMENT":
        if max(p[1] for p in points) - min(p[1] for p in points) > tol:
            mismatch("y_values_differ")
    elif kind == "VERTICAL_SEGMENT":
        if max(p[0] for p in points) - min(p[0] for p in points) > tol:
            mismatch("x_values_differ")
    elif kind == "COLLINEAR":
        if len(points) >= 3:
            (x1, y1), (x2, y2) = points[0], points[1]
            for (x3, y3) in points[2:]:
                area2 = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
                if area2 > tol:
                    mismatch("nonzero_triangle_area")
                    break
    elif kind == "EQUIDISTANT_FROM_FIRST":
        base = points[0]
        distances = [math.dist(base, p) for p in points[1:]]
        if distances and max(distances) - min(distances) > tol:
            mismatch("distances_differ")
    elif kind == "MIDPOINT_OF":
        if len(labels) == 3:
            m, a, b = points
            if abs(m[0] - (a[0] + b[0]) / 2) > tol or abs(m[1] - (a[1] + b[1]) / 2) > tol:
                mismatch("not_the_midpoint")
    elif kind == "ON_X_AXIS":
        if any(abs(p[1]) > tol for p in points):
            mismatch("y_not_zero")
    elif kind == "ON_Y_AXIS":
        if any(abs(p[0]) > tol for p in points):
            mismatch("x_not_zero")
    elif kind.startswith("IN_QUADRANT_"):
        signs = {"IN_QUADRANT_I": (1, 1), "IN_QUADRANT_II": (-1, 1),
                 "IN_QUADRANT_III": (-1, -1), "IN_QUADRANT_IV": (1, -1)}[kind]
        for (x, y) in points:
            if math.copysign(1, x) != signs[0] or math.copysign(1, y) != signs[1] \
                    or abs(x) <= tol or abs(y) <= tol:
                mismatch("wrong_quadrant")
                break
    return out


# --------------------------------------------------------------------------
# NUMBER_LINE
# --------------------------------------------------------------------------
def _number_line_failures(spatial: dict, policy: dict) -> list[str]:
    s = spatial["semantics"]
    failures: list[str] = []
    attempt = spatial["surface"] == "ATTEMPT"
    lo, hi = s["domain"]
    if lo >= hi:
        failures.append("SPATIAL_REPRESENTATION_SEMANTICS_INVALID:empty_domain")
    elif (hi - lo) / s["tick_interval"] < int(policy["number_line"]["min_ticks"]):
        failures.append("SPATIAL_REPRESENTATION_SEMANTICS_INVALID:tick_interval")
    if policy["number_line"]["require_canonical_direction"] and \
            s["direction"] != "RIGHT_POSITIVE":
        failures.append(f"AXIS_ORIENTATION_INCORRECT:{s['direction']}")
    for point in s["marked_points"]:
        value, role, label = point.get("value"), point["role"], point["label"]
        plotted = point.get("plotted", role == "GIVEN")
        if role == "GIVEN" and value is None:
            failures.append("SPATIAL_REPRESENTATION_SEMANTICS_INVALID:"
                            f"given_without_value:{label}")
            continue
        if value is None:
            continue
        if not (lo <= value <= hi):
            failures.append(f"COORDINATE_POINT_MISPLACED:{label}:outside_declared_domain")
        if attempt and plotted and role in ("LEARNER_MUST_SUPPLY", "DERIVED_CHECK"):
            failures.append(f"ATTEMPT_REPRESENTATION_REVEALS_TARGET:{label}")
    return failures


# --------------------------------------------------------------------------
# ANGLE_FIGURE
# --------------------------------------------------------------------------
def _angle_figure_failures(spatial: dict, policy: dict) -> list[str]:
    s = spatial["semantics"]
    failures: list[str] = []
    attempt = spatial["surface"] == "ATTEMPT"
    tol = float(policy["angle_figure"]["measure_tolerance_deg"])
    vertices = {v["label"] for v in s["vertices"]}
    angles = {a["label"]: a for a in s["marked_angles"]}

    for angle in s["marked_angles"]:
        for key in ("vertex", "ray_a", "ray_b"):
            if angle[key] not in vertices:
                failures.append("SPATIAL_REPRESENTATION_SEMANTICS_INVALID:"
                                f"unknown_point:{angle['label']}:{angle[key]}")
        if angle["ray_a"] == angle["ray_b"]:
            failures.append("SPATIAL_REPRESENTATION_SEMANTICS_INVALID:"
                            f"degenerate_angle:{angle['label']}")
        shown = angle.get("measure_shown", angle["role"] == "GIVEN")
        if attempt and shown and angle["role"] in ("LEARNER_MUST_SUPPLY", "DERIVED_CHECK"):
            failures.append(f"ATTEMPT_REPRESENTATION_REVEALS_TARGET:{angle['label']}")

    # angle-pair identity is semantic; it may not be inferred from drawing position alone
    for declared_pair in s["declared_angle_pairs"]:
        a_label, b_label = declared_pair["angle_labels"]
        a, b = angles.get(a_label), angles.get(b_label)
        if a is None or b is None:
            failures.append(f"ANGLE_PAIR_IDENTITY_MISMATCH:{a_label},{b_label}:undeclared")
            continue
        kind = declared_pair["kind"]
        if kind in ("LINEAR_PAIR", "VERTICALLY_OPPOSITE", "ADJACENT"):
            if a["vertex"] != b["vertex"]:
                failures.append(f"ANGLE_PAIR_IDENTITY_MISMATCH:{kind}:{a_label},{b_label}:"
                                "different_vertices")
        if kind in ("CORRESPONDING", "ALTERNATE_INTERIOR", "CO_INTERIOR"):
            if a["vertex"] == b["vertex"]:
                failures.append(f"ANGLE_PAIR_IDENTITY_MISMATCH:{kind}:{a_label},{b_label}:"
                                "same_vertex")
        both = a.get("measure_deg") is not None and b.get("measure_deg") is not None
        if both:
            total = a["measure_deg"] + b["measure_deg"]
            if kind == "LINEAR_PAIR" and abs(total - 180.0) > tol:
                failures.append(f"ANGLE_PAIR_IDENTITY_MISMATCH:LINEAR_PAIR:"
                                f"{a_label},{b_label}:sum={total}")
            if kind == "CO_INTERIOR" and abs(total - 180.0) > tol:
                failures.append(f"ANGLE_PAIR_IDENTITY_MISMATCH:CO_INTERIOR:"
                                f"{a_label},{b_label}:sum={total}")
            if kind in ("VERTICALLY_OPPOSITE", "CORRESPONDING", "ALTERNATE_INTERIOR") and \
                    abs(a["measure_deg"] - b["measure_deg"]) > tol:
                failures.append(f"ANGLE_PAIR_IDENTITY_MISMATCH:{kind}:{a_label},{b_label}:"
                                "measures_differ")

    # a figure may not silently assume what must be proved
    given_parallels = {(f["line_a"], f["line_b"]) for f in s["declared_parallel_facts"]
                       if f["status"] == "GIVEN"}
    to_prove = {(f["line_a"], f["line_b"]) for f in s["declared_parallel_facts"]
                if f["status"] == "TO_BE_PROVED"}
    for mark in s["parallel_marks"]:
        key = (mark["line_a"], mark["line_b"])
        reversed_key = (mark["line_b"], mark["line_a"])
        if key in to_prove or reversed_key in to_prove:
            failures.append(f"GEOMETRY_ASSUMPTION_LEAK:parallel_mark_for_unproved:"
                            f"{mark['line_a']}|{mark['line_b']}")
        elif key not in given_parallels and reversed_key not in given_parallels:
            failures.append(f"GEOMETRY_ASSUMPTION_LEAK:undeclared_parallel_mark:"
                            f"{mark['line_a']}|{mark['line_b']}")
    return failures


# --------------------------------------------------------------------------
# the gate
# --------------------------------------------------------------------------
def validate_spatial(spatial: dict, *, policy: dict | None = None) -> list[str]:
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    failures: list[str] = []
    if spatial["semantics"]["kind"] != spatial["primitive"]:
        failures.append("SPATIAL_REPRESENTATION_SEMANTICS_INVALID:primitive_kind_mismatch")
        return failures
    if spatial["spatial_digest"] != digest(spatial, "spatial_digest"):
        failures.append(f"SPATIAL_REPRESENTATION_SEMANTICS_INVALID:digest_drift:"
                        f"{spatial['spatial_id']}")
    failures.extend(_plan_failures(spatial))
    dispatch = {
        "COORDINATE_PLANE": _coordinate_plane_failures,
        "NUMBER_LINE": _number_line_failures,
        "ANGLE_FIGURE": _angle_figure_failures,
    }
    failures.extend(dispatch[spatial["primitive"]](spatial, policy))
    return sorted(set(failures))


def audit_spatial(representations: list[dict], *, policy: dict | None = None) -> dict:
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    failures: list[str] = []
    for spatial in representations:
        for code in validate_spatial(spatial, policy=policy):
            failures.append(f"{code}@{spatial['spatial_id']}")
    if failures:
        fail("SPATIAL_SEMANTICS_GATE_FAILED", "|".join(sorted(set(failures))))

    attempt_surfaces = [r for r in representations if r["surface"] == "ATTEMPT"]
    return {
        "status": "PASS",
        "representation_count": len(representations),
        "primitives": sorted({r["primitive"] for r in representations}),
        "attempt_surfaces": len(attempt_surfaces),
        "learner_must_supply_declared": sum(
            len(r["representation_plan"]["learner_must_supply"]) for r in representations),
        "answer_targets_declared": sum(
            len(r["representation_plan"]["answer_targets"]) for r in representations),
        "corpus_digest": digest(sorted(r["spatial_digest"] for r in representations)),
        "checks": [
            "DECLARED_DOMAIN_TICKS_ORIGIN_AND_AXIS_DIRECTION",
            "EVERY_POINT_INSIDE_ITS_DECLARED_DOMAIN",
            "DECLARED_RELATIONS_HOLD_FOR_THE_DECLARED_COORDINATES",
            "ANGLE_PAIR_IDENTITY_IS_SEMANTIC_NOT_POSITIONAL",
            "NO_PARALLEL_MARK_FOR_AN_UNPROVED_FACT",
            "GIVENS_AND_LEARNER_TARGETS_ARE_DISJOINT",
            "ATTEMPT_FIGURE_DOES_NOT_PLOT_ITS_OWN_ANSWER",
        ],
        "release_meaning": "PUBLICATION_ENGINEERING only; this is subject correctness "
                           "evidence for figures, not a visual-usability or expert-review "
                           "PASS, both of which remain PENDING",
    }
