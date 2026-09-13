# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the **canonical orchestration root for Physics Blueprint work**. Role-specific sibling directories (`CoreAuthoring/`, `Core2Transfer/`, `Core1A/`, `Core2A/`, `Representation/`) are subordinate execution kits; `policy/role-bindings.v1.json` freezes the reasoning-role mapping.

## Executable topology

```text
ORIGINAL GROUND TRUTH
        ↓
      CORE0
        ↓
CORE1 ↔ independent second pass ↔ CORE2
        ↓
       JOIN
        ↓
learner state × purpose
        ↓
CORE1A 1A0…1A11
        ↓
1A12 manuscript + T receipts
        ↓
      CORE2A
        ↓
PUBLICATION IR
lossless semantic audit
        ↓
representation readiness
        ↓
existing Physics render stack
composition only
        ↓
RENDER CUSTODY
        ↓
actual-PDF preflight
        ↓
MACHINE PASS
+ HUMAN VISUAL REVIEW PENDING
```

## Blueprint guarantees now implemented

The Blueprint governs evidence-adaptive routing, independent second-role re-grounding, Core1 × Core2 Join, learner-state × purpose control, cognition-before-manuscript Core1A execution, taught-state-gated Core2A, lossless Publication IR, finished-PDF custody/preflight, and real Motion-in-a-Plane representation readiness.

## Publication and render authority

The renderer is **not** a reasoning role. Publication IR fixes semantic authority upstream and renderer authority to composition only. Render custody binds the exact Publication IR digest, renderer-report digest and finished-PDF SHA. Actual-PDF preflight inspects physical geometry, observed text font floor, page bounds, learner-visible internal identifiers, raster nonblank state and report/PDF page-count custody.

Machine success still ends at:

```text
MACHINE_PREFLIGHT_PASS_HUMAN_VISUAL_REVIEW_PENDING
release_authorized = false
```

## Motion-in-a-Plane representation gap and closure

The first real readiness compilation correctly produced:

```text
10 real chapter concepts
1 READY_FOR_REALIZATION
9 BLOCKED_NEEDS_PRIMITIVE
status = BLOCKED_REPRESENTATION_GAP
```

The blocked cognitive jobs were not patched with generic schematics. They were converted into a subject-wide 2D Physics representation extension under `Representation/`.

The extension adds seven generic, topic-unbound vector primitives:

```text
CARTESIAN_FRAME_2D
VECTOR_COMPONENTS_2D
STATE_SEQUENCE_2D
PATH_ANATOMY_2D
EVENT_COMPARE_2D
PARAMETRIC_ELIMINATION_BRIDGE_2D
OBSERVER_LINE_OF_SIGHT_2D
```

Each declares an instructional job, translation obligation, learner action, renderer constraints and minimum real vector-operation floor. Defaults are `SCHEMATIC_STRUCTURE_ONLY`: they carry structure, not invented numerical quantities. The existing `RELATIVE_FRAME_VIEW` and `OPTION_GRAPH_SET_VIEW` remain reused where their governed jobs actually match.

After explicit per-concept authorization against the combined subject-wide primitive registries, the real M2D readiness gate is now expected to produce:

```text
10 READY_FOR_REALIZATION
0 BLOCKED_NEEDS_PRIMITIVE
status = READY_FOR_RENDER_ADAPTER
release_authorized = false
```

The gate remains fail-closed: topic-name similarity cannot authorize a primitive; clearing a missing capability without a real authorized vector primitive is rejected; chapter concept/archetype drift is rejected.

## Render process proof

`engine/build_render_process_golden.py` invokes the existing `Core1A/engine/render_physics_core1a.py` and the Blueprint finished-PDF preflight. CI uploads the process PDF, renderer report, Publication IR, render custody, preflight report, raster proofs and real M2D readiness report.

The process PDF remains synthetic and does **not** assert production Motion-in-a-Plane maturity.

## Current next boundary

Once the 2D primitive extension and readiness closure are green, the next tranche is a **real Motion-in-a-Plane composition adapter**. It must consume the source-locked chapter plan plus exact authorized primitive refs, emit Publication IR before drawing, reuse the existing page/render infrastructure, and then pass the same actual-PDF preflight. Human actual-size figure/page review remains mandatory before any mature-product release claim.
