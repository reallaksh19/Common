# Spatial representation semantics (M-UPGRADE-2 item 4)

An additive extension to the M-H RepresentationSemantics phase. Nothing in `README.md`,
`math-representation-spec.schema.json`, `math-teaching-primitive-registry.json` or the
existing engine changes; this adds the missing *semantic* layer beneath the primitives.

## Why a vector primitive is not enough

Coordinate Geometry made the general point: a clean, in-bounds, deterministically rendered
figure can still be mathematically wrong, and an "answer-neutral" attempt page can still
give the answer away through the picture. The existing `COORDINATE_PLANE` primitive
described *what to draw*; it did not declare what makes the drawing correct.

So a spatial representation now declares its own semantics, and both the semantics and the
plan are checked:

```text
COORDINATE_PLANE   x_domain  y_domain  tick_interval  origin  axis_direction
                   point_coordinates[{label, x, y, role, plotted}]
                   declared_relations[{kind, point_labels}]

NUMBER_LINE        domain  tick_interval  direction  marked_points[...]

ANGLE_FIGURE       vertices  rays  marked_angles[{label, vertex, ray_a, ray_b, measure, role}]
                   declared_angle_pairs[{kind, angle_labels}]
                   declared_parallel_facts[{line_a, line_b, status}]  parallel_marks[...]
```

## learner_must_supply is separated from givens

This is the second half of item 4, and it is what stops a figure from silently revealing
the answer:

```json
"representation_plan": {
  "givens": ["A", "B"],
  "learner_must_supply": ["M"],
  "answer_targets": ["M"]
}
```

On an `ATTEMPT` surface a point, value or angle measure whose role is
`LEARNER_MUST_SUPPLY` or `DERIVED_CHECK` may not be plotted or shown. The *same* item's
`SOLUTION` surface plots it and additionally asserts `MIDPOINT_OF` and
`EQUIDISTANT_FROM_FIRST`, which are then checked against the declared coordinates. Givens
and learner targets must be disjoint, and every label named in the plan must exist in the
primitive.

## Declared relations are checked, not decorative

`HORIZONTAL_SEGMENT`, `VERTICAL_SEGMENT`, `COLLINEAR`, `EQUIDISTANT_FROM_FIRST`,
`MIDPOINT_OF`, `ON_X_AXIS`, `ON_Y_AXIS` and the four quadrant relations are each evaluated
against the coordinates the figure declares. Moving one point breaks the relation and the
gate fires — which is exactly the "clean but semantically wrong diagram" the stress test
described.

For `ANGLE_FIGURE`, angle-pair identity is **semantic**: a `LINEAR_PAIR` must share a
vertex, a `CORRESPONDING` pair must not, a `LINEAR_PAIR` or `CO_INTERIOR` pair with both
measures known must sum to 180, and a `VERTICALLY_OPPOSITE`/`CORRESPONDING`/
`ALTERNATE_INTERIOR` pair must be equal. A `parallel_marks` entry for a fact whose status
is `TO_BE_PROVED` — or for no declared fact at all — raises `GEOMETRY_ASSUMPTION_LEAK`: the
figure may not assume what the proof is supposed to establish.

## Falsifiers

```text
SPATIAL_REPRESENTATION_SEMANTICS_INVALID
ATTEMPT_REPRESENTATION_REVEALS_TARGET
SPATIAL_GIVEN_AND_TARGET_CONFLATED
SPATIAL_TARGET_NOT_DECLARED
COORDINATE_POINT_MISPLACED
AXIS_ORIENTATION_INCORRECT
VISUAL_SEMANTIC_RELATION_MISMATCH
ANGLE_PAIR_IDENTITY_MISMATCH
GEOMETRY_ASSUMPTION_LEAK
SPATIAL_SEMANTICS_GATE_FAILED
```

`policies/math-spatial-semantics-policy.json` classifies these as
`SUBJECT_CORRECTNESS`, not `VISUAL_USABILITY`, per the consolidated review.

## Files

```text
contracts/math-spatial-representation.schema.json
policies/math-spatial-semantics-policy.json
engine/validate_math_spatial_semantics.py
fixtures/spatial/build_math_spatial_representations.py
fixtures/spatial/math-spatial-representations.fixture.json
tests/test_math_spatial_semantics.py
```

The fixture lives under `fixtures/spatial/` deliberately: the existing M-H contract
validator globs `fixtures/*.fixture.json` and validates every match against the
representation-*spec* schema, so a differently shaped sibling in that directory would break
it. Keeping the new fixture one level down leaves #323's validator untouched and still
passing.

## Release meaning

`PUBLICATION_ENGINEERING` only. Passing these gates is subject-correctness evidence for
figures; visual usability and expert review remain `PENDING`.
