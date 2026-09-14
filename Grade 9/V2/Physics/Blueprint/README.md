# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the **canonical orchestration root for Physics Blueprint work**. Role-specific sibling directories (`CoreAuthoring/`, `Core2Transfer/`, `Core1A/`, `Core1B/`, `Core2A/`, `Core2B/`, `Representation/`) are subordinate execution kits.

## Authority topology and learner runtime

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
1A12 manuscript + T receipts ─────────────→ CORE2A legal transfer pool
        ↓                                      ↓
released teaching authority                 exact legal-pool custody
        ↓                                      ↓
      CORE1B ── observed learner evidence ─→ CORE2B
        ↑                                      │
        └──── targeted repair request ─────────┘
                                               ↓
                                  attempts / retrieval evidence
                                               ↓
                                      EVIDENCE + CONTROL

Publication remains separate:
CORE1A released semantics → Publication IR → composition-only renderer → render custody/preflight
```

Execution order may vary. **Authority order may not.** A-layers authorize; B-layers execute authorized learner experiences and capture observed evidence.

## Core1B / Core2B governance adopted after PR #368 review

The A/B split is accepted as the right product architecture, with the B roles kept `DRAFT` until their execution contracts satisfy these Blueprint boundaries:

1. **Core1B is runtime, not teaching authority.** It must bind the exact released Core1A authority artifact by ref **and digest** before presenting or reorganizing instruction.
2. **Exposure is not mastery.** A Core1B exposure/completion receipt proves that an authorized experience occurred. Unit readiness flags, author configuration, a teaching receipt, or a simulated pass may never manufacture `INDEPENDENT`, `TRANSFER_READY`, or `ROBUST` learner state.
3. **Learner state requires observed evidence.** Only provenance-backed learner response, diagnostic, or teacher observation may update learner control state. Runtime evidence is append-only; later evidence can supersede a current estimate but may not rewrite history.
4. **Core2B selects; Core2A legalizes.** Core2B must bind the exact Core2A legal-pool ref and digest and the exact upstream item ref. A local `core2a_legal: true` flag is not custody.
5. **Escalation is per required capability.** A single session-wide learner state is insufficient for an item requiring multiple capabilities. Every required capability must independently meet the item's evidence floor.
6. **Representation transfer requires matching evidence.** Merely teaching a representation convention does not prove the learner can transfer through it; selection must bind observed representation evidence when the item relies on that shift.
7. **Transfer demand is multidimensional.** A scalar `T0…T8` ladder may be useful as a display/order hint, but cannot be the sole authorization rule. Structural distance, representation change, model discrimination, multi-step bridging, synthesis, and competitive mixing are separate dimensions. In particular, **discrimination and synthesis are not consecutive mastery states**.
8. **Repair is a request, not authority.** Core2B may route the smallest explanatory prerequisite set back to Core1B and then return to the original target. That request may not mutate Core1A teaching authority or Core2A legality.
9. **Purpose and retrieval never expand legality.** `FIRST_STUDY / PRACTICE / REVISION / COMPETITIVE_EXAM` and a due-retrieval state may change selection inside the legal pool only.

The normative contract is `policy/b-layer-runtime-boundary.v1.json`, enforced by `engine/validate_b_layer_boundary.py` and falsifier tests.

## Implemented Blueprint guarantees

The Blueprint governs evidence-adaptive routing, independent second-role re-grounding, Core1 × Core2 Join, learner-state × purpose control, cognition-before-manuscript Core1A execution, taught-state-gated Core2A, the draft B-layer runtime boundary, lossless Publication IR, finished-PDF custody/preflight, and real Motion-in-a-Plane representation readiness.

The subject-wide 2D representation extension provides seven generic vector primitives:

```text
CARTESIAN_FRAME_2D
VECTOR_COMPONENTS_2D
STATE_SEQUENCE_2D
PATH_ANATOMY_2D
EVENT_COMPARE_2D
PARAMETRIC_ELIMINATION_BRIDGE_2D
OBSERVER_LINE_OF_SIGHT_2D
```

Together with governed existing primitives, the real 10-concept Motion-in-a-Plane chapter reaches `10/10 READY_FOR_REALIZATION`. That closes the representation gap only; it does not authorize publication.

## Real Motion-in-a-Plane composition gate

`engine/compile_m2d_composition_plan.py` maps every real chapter concept to its exact semantic digest, source/equation/Core2 refs, illustration archetype, explicitly authorized representation refs, and learner page intent.

Publication IR requires both:

```text
representation readiness = READY_FOR_RENDER_ADAPTER
AND
real Core1A manuscript release = repository-backed non-golden 1A12 provenance
```

The current real repository state remains intentionally blocked on the second condition:

```text
10 concepts mapped
representation_status = READY_FOR_RENDER_ADAPTER
manuscript_release_status = ABSENT
composition_status = BLOCKED_UPSTREAM_MANUSCRIPT_RELEASE
publication_ir_gate = BLOCKED
renderer_invocation_allowed = false
release_authorized = false
next_action = MIGRATE_REAL_CORE1A_STAGE_RELEASE
```

Figure availability and learner-runtime availability can never substitute for Core1A pedagogical/manuscript release evidence.

## Render and release authority

The renderer remains composition-only. Even a future `READY_FOR_PUBLICATION_IR` composition plan must first pass the lossless Publication IR compiler. Finished PDFs then pass exact artifact custody and actual-PDF preflight. Machine success ends at human visual review pending, never automatic release authorization.

## Current next tranche

Two migrations may now proceed independently without crossing authority boundaries:

- migrate a **real Core1A bucket** into the Blueprint stage machine, beginning with `M2D-SBA-04`;
- revise PR #368's Core1B/Core2B draft contracts to bind exact A-layer digests and observed learner evidence, then activate the B roles only after those falsifiers pass.
