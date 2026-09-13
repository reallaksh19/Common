# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the **canonical orchestration root for Physics Blueprint work**. Role-specific sibling directories such as `CoreAuthoring/`, `Core2Transfer/`, `Core1A/` and `Core2A/` are subordinate execution kits; they do not define a second architecture.

The machine mapping is frozen in `policy/role-bindings.v1.json` so future work remains classified as Physics Blueprint work even when executable code lives in a specialist role folder.

## Current executable topology

```text
ORIGINAL GROUND TRUTH
        ↓
      CORE0
        ↓
CORE1 ↔ independent second pass ↔ CORE2
        ↓
       JOIN
        ↓
      CORE1A
assimilation + T-* taught-state receipts
        ↓
      CORE2A
purpose-conditioned transfer compiler
```

Execution order is not authority order. Core1 remains semantic intelligence, Core2 remains assessment/transfer intelligence, and the second specialist must independently re-ground before seeing upstream claims.

## Implemented architecture slices

- normalized evidence and deterministic `CORE1_FIRST | CORE2_FIRST | BLOCK` routing;
- fresh-instance independent second-pass protocol;
- packet provenance and max-three handoff transport rule;
- **Core1 × Core2 Join Gate** with exact demand-claim coverage and critical-conflict blocking;
- Core1A assimilation-before-manuscript discipline;
- active Core2A taught-state-gated transfer contract.

## Join Gate

Every Core2 demand claim must appear **exactly once** in a Join reconciliation row. `CONFIRMED` and `REFINED` claims require explicit Core1 semantic grounding plus assimilation obligations. `MISSING`, `UNSUPPORTED`, `CONTRADICTED`, `OUT_OF_SCOPE` and `UNKNOWN` remain visible states.

A required unresolved demand becomes `BLOCK` and makes the Join `JOIN_BLOCKED`. A deliberately non-blocking unresolved extension becomes `HOLD`, allowing `JOIN_READY_WITH_HOLDS` without rewriting uncertainty as low importance.

Core1A may consume Join output only when `assimilation_ready = true`.

## Core2A authority boundary

Core2A is `ACTIVE`, but strictly downstream:

```text
Core1 semantic boundary
∩ Core1A T-* TEACHING_COMPLETE receipts
∩ Core2 transfer envelope
∩ learner-product purpose
∩ owner policy
```

Core2A may select and scaffold learner practice. It may not rewrite Core2 source truth, invent untaught Physics, or infer learner mastery from publication completion.

A source question lacking required T receipts remains in immutable Core2 corpus custody and is marked `HELD_UNTIL_TEACHING_COMPLETE` for learner release.

Generated-original challenges fail closed unless required capabilities are taught, source/family bindings agree, near-copy checks pass, and an approved Physics validator independently recomputes the underlying relation.

## Non-negotiable invariants

- Original evidence is authority; packets are claims.
- First role is evidence-adaptive, never topic-name hard-coded.
- Core1 and Core2 are distinct epistemic roles.
- The second role independently re-grounds before seeing upstream claims.
- Every Core2 demand claim is reconciled exactly once at Join.
- Critical unresolved Join claims block Core1A.
- Every handoff contains at most three subtopics; learning atoms are unbounded.
- Absence of evidence remains absence.
- Owner overrides alter action, never historical evidence.
- Core1A reasoning precedes manuscript generation.
- Core2A requires taught-state receipts.
- Teaching completion does not imply learner mastery.

## Running the blueprint proofs

```bash
python 'Grade 9/V2/Physics/Blueprint/contracts/validate_contracts.py'
python 'Grade 9/V2/Physics/Blueprint/engine/run_golden_fixtures.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_routing.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_independence.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_join.py'
python 'Grade 9/V2/Physics/Blueprint/engine/compile_join.py' \
  'Grade 9/V2/Physics/Blueprint/fixtures/join/join-ready.json' \
  --out /tmp/physics-join.json

python 'Grade 9/V2/Physics/Core2A/tests/test_physics_core2a.py'
```

The Join and Core2A goldens are process fixtures. They prove architecture behavior; they do not authorize every Motion-in-a-Plane problem family or replace human subject/pedagogy/assessment review.
