# Physics V2 Blueprint — evidence-adaptive orchestration

This directory is the orchestration layer above the Physics role-specific production kits. It makes execution order, evidence authority, validation discipline and downstream learner-product legality machine-enforceable.

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
- Core1A assimilation-before-manuscript discipline;
- active Core2A semantic/executable contract.

## Core2A authority boundary

Core2A is now `ACTIVE`, but it is strictly downstream:

```text
Core1 semantic boundary
∩ Core1A T-* TEACHING_COMPLETE receipts
∩ Core2 transfer envelope
∩ learner-product purpose
∩ owner policy
```

Core2A may select and scaffold learner practice. It may not rewrite Core2 source truth, invent untaught Physics, or infer learner mastery from publication completion.

A source question lacking required T receipts remains in immutable Core2 corpus custody and is marked `HELD_UNTIL_TEACHING_COMPLETE` for learner release.

Generated-original challenges fail closed unless their required capabilities are taught, their source/family bindings agree, their near-copy gate passes, and an approved Physics validator independently recomputes the underlying relation.

## Non-negotiable invariants

- Original evidence is authority; packets are claims.
- First role is evidence-adaptive, never topic-name hard-coded.
- Core1 and Core2 are distinct epistemic roles.
- The second role independently re-grounds before seeing upstream claims.
- Every handoff contains at most three subtopics; learning atoms are unbounded.
- Absence of evidence remains absence.
- Owner overrides alter action, never historical evidence.
- Core1A reasoning precedes manuscript generation.
- Core2A requires taught-state receipts.
- Teaching completion does not imply learner mastery.

## Running the architecture and Core2A proofs

```bash
python 'Grade 9/V2/Physics/Blueprint/contracts/validate_contracts.py'
python 'Grade 9/V2/Physics/Blueprint/engine/run_golden_fixtures.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_routing.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_independence.py'

python 'Grade 9/V2/Physics/Core2A/tests/test_physics_core2a.py'
python 'Grade 9/V2/Physics/Core2A/engine/run_physics_core2a.py' \
  --run 'Grade 9/V2/Physics/Core2A/golden/projectile-event/core2a-input.json' \
  --out-dir /tmp/physics-core2a
```

The Core2A golden is a process fixture only. It does not authorize every Motion-in-a-Plane problem family and does not replace human subject/pedagogy/assessment review.
