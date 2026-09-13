# Physics V2 — Core (2A): taught-state-gated transfer compiler

Core (2) remains the complete source-transfer authority. Core (2A) is a downstream learner-product compiler. It selects and realizes transfer practice for a stated learner purpose, but it may not change Physics truth, Core (2) source identity, Core (1A) teaching authority or learner-evidence history.

## Semantic contract

```text
Core1 semantic boundary
∩ Core1A T-* TEACHING_COMPLETE receipts
∩ Core2 transfer envelope
∩ learner-product purpose
∩ owner policy
        ↓
      Core2A
```

A publication receipt proves that the learner product taught a capability. It does **not** prove that the learner mastered it. `learner_evidence_state = UNKNOWN` is therefore a legal and expected state.

## Purpose is mandatory

Exactly one purpose is required:

```text
FIRST_STUDY
PRACTICE
REVISION
COMPETITIVE_EXAM
```

Purpose changes source-question selection, generated challenge mix and support density. Purpose never expands legal Physics scope.

## Two lanes

### SOURCE_CORE2

The complete Core (2) corpus remains immutable authority. Core (2A) may select a purpose-dependent subset for a learner product, but it never deletes an unselected source question from Core (2).

A source item is learner-releasable only when every required capability has a matching `T-PHY-*` receipt with:

```text
publication_state = TEACHING_COMPLETE
learner_profile_ref = requested learner profile
purpose_ref = requested purpose
```

Otherwise the source question remains in corpus custody with `HELD_UNTIL_TEACHING_COMPLETE`.

### GENERATED_ORIGINAL

Fresh questions may be realized only when:

- the anchor Core (2) question is itself releasable and its problem-family/bucket binding agrees;
- every required capability has a matching teaching-complete receipt;
- the Physics validator type is supported and independently recomputes the governed relation;
- declared SI units are valid and the recomputed result matches the learner-facing canonical answer;
- the generated prompt passes near-copy checking against all source stems;
- staged help does not disclose the answer or duplicate full-working steps;
- provenance explicitly says `GENERATED_ORIGINAL` and does not claim false official-question provenance.

Unsupported Physics validators fail closed. They are not free-written.

## Physics validation

The v1 executable validator registry authorizes:

```text
CONSTANT_ACCELERATION_VELOCITY
CONSTANT_ACCELERATION_INITIAL_VELOCITY
CONSTANT_ACCELERATION_EVENT_TIME
VECTOR_DOT_PERPENDICULAR
SPEED_FROM_COMPONENTS
```

The engine independently recomputes the relevant relation, validates declared SI units, and binds the recomputed numeric result to the learner-facing canonical answer before emitting PASS. Additional problem families require an explicit validator before generated challenges from those families are production-legal.

## Purpose behavior

```text
FIRST_STUDY
  first releasable source anchor per bucket
  guided direct challenge when available
  high support

PRACTICE
  all releasable Core2 source items
  near-transfer challenges when available
  support initially hidden

REVISION
  highest-demand representative source item per bucket
  compact retrieval/diagnostic use
  no generated challenge requirement

COMPETITIVE_EXAM
  highest-demand representative source item per bucket
  at least one NEAR_TRANSFER
  at least one structural variation
  structural difficulty, not arithmetic ugliness
```

Structural variations include reversed targets, hidden information, representation shifts, event constraints, parameter constraints, error diagnosis, compare/rank and multi-step bridges.

## Executable surfaces

```text
contracts/
  physics-core2a-run.schema.json
  physics-core2a-source-item.schema.json
  physics-core2a-challenge-item.schema.json

policies/
  physics-core2a-purpose-policy.json
  physics-core2a-challenge-policy.json
  physics-core2a-validator-registry.json

engine/
  core2a_common.py
  run_physics_core2a.py

golden/projectile-event/
  core2a-input.json

tests/
  test_physics_core2a.py
```

Run the golden:

```bash
python 'Grade 9/V2/Physics/Core2A/engine/run_physics_core2a.py' \
  --run 'Grade 9/V2/Physics/Core2A/golden/projectile-event/core2a-input.json' \
  --out-dir /tmp/physics-core2a

python 'Grade 9/V2/Physics/Core2A/tests/test_physics_core2a.py'
```

## Release boundary

This v1 activates the **semantic/executable Core2A model**. It does not claim that all Motion-in-a-Plane problem families are validator-backed yet, and it does not authorize a learner-facing PDF release. New generated families must acquire explicit Physics validators and tests before use.
