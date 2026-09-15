# Physics V2 — P-H Teaching primitives and representation closure

P-H implements issue #256 under the #320 catch-up. It is the phase that makes
`Grade 9/V2/Physics/Representation/registry/physics-teaching-primitive-registry.json`
exist for Physics (Mathematics and Chemistry already had theirs), and it makes those
primitives **real vector graphics** rather than prose labels.

```text
P-G Core1 study plan
+ P-F capability records (structural obligations)
+ P-A question set          (the only source of numeric quantities)
+ P-H primitive registry + page-intent profile + figure render contract
→ PhysicsRepresentationBundle
→ deterministic render
→ PhysicalPageMap with hash-bound, draw-time placement evidence
```

## The defect this phase exists to prevent

`TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED` — a "teaching primitive" that is only a
caption. P-H makes that machine-detectable in three layers:

1. **Registry.** Every primitive declares `realized_as_vector_graphics: true`, a
   `renderer_binding`, and a `minimum_vector_ops` floor.
2. **Renderer.** `render_primitive(kind, params, canvas, bbox)` draws through a
   `TracingCanvas` that counts `line / rect / roundRect / circle / arc / path` operations
   **separately from** text operations, and measures the real ink bounding box from the
   coordinates the primitive actually emitted.
3. **Custody.** The realizer refuses to emit a figure below its floor, and the independent
   audit recomputes the whole reconciliation from the PDF bytes and the page map.

Current proof on the merged motion assessment: **128 figures, 2,653 real vector
operations, 0 label-only figures, 32 pages, byte-deterministic across runs.**

## Primitives (19, all subject-wide generic)

The ten required by #256 / #234 Phase 7:

```text
PHENOMENON_SCENE   MOTION_STRIP          VECTOR_STATE_VIEW   PHASE_BOUNDARY_VIEW
TRAJECTORY_VIEW    POSITION_TIME_GRAPH   VELOCITY_TIME_GRAPH FORCE_DIAGRAM
SIGN_FRAME_OVERLAY DIAGRAM_EQUATION_BRIDGE
```

plus `ACCELERATION_TIME_GRAPH`, `STATE_TABLE`, `SLOPE_AREA_DECODER`,
`TIMELINE_INTERVAL_VIEW`, `RELATIVE_FRAME_VIEW`, `OPTION_GRAPH_SET_VIEW`,
`MINIMAL_PHYSICS_CONTRAST`, `VERIFICATION_CHECK_STRIP`, `MODEL_VALIDITY_GATE`.

Selection is driven by the P-F record's own representation requirements and structural
obligations through `physics-page-intent-profile.json`. Adding a new Physics
representation requirement is one data row, not a code branch.

## Stable render interface and the shared library

```python
render_primitive(kind, params, canvas, bbox) -> RenderEvidence
```

The drawing itself is delegated to the shared visual library vendored at
`Grade 9/V2/Shared/MasterTemplates/primitives/` (from draft PR #310 @ `88d3a719`):
`Vector1DDiagram` for the signed frame strip, `KinematicGraphRenderer` for the v-t graph
with Riemann area, `FreeBodyDiagramRenderer` for force diagrams, `CartesianPlotter2D` and
the shared card/arrow/palette helpers for everything composed here. The vendored files are
read-only for this PR; gaps found while integrating are recorded in
`Grade 9/V2/Shared/MasterTemplates/primitives/VENDORED.md` for upstream repair.

Because everything goes through `render_primitive`, swapping in a future shared release is
a change to this one adapter.

## Quantitative grounding — figures may not invent numbers

Every number in a figure is extracted from the P-A question set for an item in that
capability's own source scope trace, using the declared patterns in
`physics-figure-render-contract.json`, and is recorded in the spec's `source_quantities`
with the exact source text it came from. A spec whose required quantities are absent falls
back to a schematic variant and records `SCHEMATIC_STRUCTURE_ONLY`.

This caught a real defect: the shared `Vector1DDiagram.draw` substitutes a hard-coded
`+5 m East / -3 m West` journey when `legs` is omitted. Displaying that on a Physics item
that never stated it would be an invented quantity, so the adapter draws its own schematic
frame strip instead whenever the source states no journey legs
(`SHARED_LIBRARY_DEFAULT_JOURNEY_NOT_PRESENTED_AS_SOURCE`).

## Physical page custody

Ported from the `PhysicalPageMap` mechanism proved in draft PR #161 / PR #196
(`physics_page_custody.py`). Planned page numbers are never accepted as evidence:

```text
structure → PDF bytes + draw-time placement events → PDF SHA-256
→ PhysicalPageMap → independent custody audit
```

Checks: content custody, page-intent reconciliation, orphan continuation, physical bounds,
measured-ink escape, per-figure vector-op floor, exact artifact hash binding.

## Running

```bash
python "Grade 9/V2/Physics/Representation/contracts/validate_contracts.py"
python "Grade 9/V2/Physics/Representation/tests/test_physics_representations.py"
```

## Non-claims

P-H realizes representations and proves their physical custody. It does **not** claim
mature learner-product design quality, authorized subject or pedagogy review, or
publication readiness. Those states remain `PENDING` and are tracked at P-L. PR #156 is not
a producer input here.
