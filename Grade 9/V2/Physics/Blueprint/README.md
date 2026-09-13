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
existing Physics renderer
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

The Blueprint now governs evidence-adaptive routing, independent second-role re-grounding, Core1 × Core2 Join, learner-state × purpose control, cognition-before-manuscript Core1A execution, taught-state-gated Core2A, lossless Publication IR, finished-PDF custody/preflight, and a real Motion-in-a-Plane representation-readiness gate.

## Publication and render authority

The renderer is **not** a reasoning role. Publication IR fixes semantic authority upstream and renderer authority to composition only. Render custody binds the exact Publication IR digest, renderer-report digest and finished-PDF SHA. Actual-PDF preflight checks physical geometry, observed text font floor, page bounds, learner-visible internal identifiers, raster nonblank state and report/PDF page-count custody.

Machine success still ends at:

```text
MACHINE_PREFLIGHT_PASS_HUMAN_VISUAL_REVIEW_PENDING
release_authorized = false
```

## Real Motion-in-a-Plane representation readiness

`engine/compile_m2d_render_readiness.py` compiles the **real source-locked Motion-in-a-Plane chapter plan** against the actual subject-wide Physics primitive registry. Authorization is explicit per concept; name similarity and a primitive's generic schematic fallback are not enough to satisfy a missing cognitive job.

The v1 baseline is intentionally fail-closed:

```text
10 real chapter concepts
1 READY_FOR_REALIZATION
9 BLOCKED_NEEDS_PRIMITIVE
status = BLOCKED_REPRESENTATION_GAP
```

`RELATIVE_MOTION_FOUNDATION` is currently realizable with governed `RELATIVE_FRAME_VIEW`. The remaining concepts expose explicit subject-wide primitive capabilities that do not yet exist safely, including 2D coordinate framing, perpendicular vector decomposition, shared-clock projectile state sequences, apex-event state preservation, same-height projectile comparison, time-elimination trajectory bridging, and observer line-of-sight geometry.

This is a stronger result than forcing the existing `TRAJECTORY_VIEW` or 1D-oriented vector semantics onto a different cognitive purpose. In particular, `TRAJECTORY_VIEW` is governed to distinguish travelled path from displacement/chord; it is not automatically legal as a projectile-dynamics teaching figure merely because the word “trajectory” matches.

## Render process proof

`engine/build_render_process_golden.py` invokes the existing `Core1A/engine/render_physics_core1a.py` and the Blueprint finished-PDF preflight. CI uploads the PDF, renderer report, Publication IR, render custody, preflight report, raster proofs, and the real M2D readiness report as one review artifact.

The rendered golden remains a **process proof only**. It does not assert that the synthetic fixture is a production Motion-in-a-Plane learner product.

## Current next boundary

The next Blueprint tranche is **representation-gap closure**: implement the missing subject-wide 2D Physics primitives in the subordinate `Representation/` kit, with vector-operation evidence and no invented quantities, then recompile this readiness gate. Only after required concepts become realizable should a real Motion-in-a-Plane page adapter be allowed to emit a learner PDF for actual-size human review.
