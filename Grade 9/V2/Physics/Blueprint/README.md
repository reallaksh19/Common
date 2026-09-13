# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the **canonical orchestration root for Physics Blueprint work**. Role-specific sibling directories (`CoreAuthoring/`, `Core2Transfer/`, `Core1A/`, `Core2A/`) are subordinate execution kits; `policy/role-bindings.v1.json` freezes that mapping.

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

- evidence-adaptive routing, never topic-name routing;
- independent second-role re-grounding;
- Core1 × Core2 Join with exact demand coverage and critical-conflict blocking;
- learner `20/50/80` prior resolved to capability state, with real learner evidence distinguished from teaching receipts;
- orthogonal purpose contracts;
- strict Core1A cognition-before-manuscript state machine;
- Motion-in-a-Plane real topic pilot deriving `CORE2_FIRST` from evidence rather than its name;
- taught-state-gated Core2A;
- Publication IR with a fail-closed lossless semantic boundary;
- render custody plus independent actual-PDF preflight.

## Publication and render authority

The renderer is **not** a reasoning role. Publication IR can consume only upstream artifacts whose release state is already `RELEASED`. Required semantic refs must survive the lossless audit before rendering.

```text
semantic_authority = UPSTREAM_ONLY
renderer_authority = COMPOSITION_ONLY
renderer_may_introduce_semantic_claims = false
renderer_may_substitute_representation = false
```

The Blueprint render layer does not replace the existing Physics renderer. It binds the exact Publication IR digest, renderer-report digest and finished-PDF SHA in a render-custody object, then independently inspects the finished PDF.

Actual-PDF preflight checks:

- SHA custody against the renderer report and render-custody object;
- A4 page geometry;
- actual extracted-text font floor;
- text bounding boxes against physical page bounds;
- learner-visible internal-identifier leakage;
- first/middle/last raster proofs at 144 dpi;
- effectively blank sampled pages;
- renderer-reported page count against the physical PDF.

Machine success deliberately emits:

```text
MACHINE_PREFLIGHT_PASS_HUMAN_VISUAL_REVIEW_PENDING
release_authorized = false
```

Machine renderability is not equivalent to mature visual quality or human subject/pedagogy/assessment approval.

## Render process golden

`engine/build_render_process_golden.py` invokes the existing `Core1A/engine/render_physics_core1a.py`, not a second rendering stack. It freezes the publication plan, rendered PDF, renderer report, Publication IR, render custody, preflight report and raster proofs into one reviewable process artifact.

The golden is a **process proof only**. It does not assert that the synthetic fixture is a production Motion-in-a-Plane learner product.

## Current next boundary

The Blueprint now governs reasoning through actual rendered-artifact custody and machine preflight. The next tranche is to bind the **real Motion-in-a-Plane publication candidate** to this render gate, then perform actual-size human figure/page review and repair before any mature-product release claim.
