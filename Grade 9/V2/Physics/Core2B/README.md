# Physics V2 — Core2B Evidence-Gated Transfer Runtime

Core2B is the learner-facing transfer runtime downstream of Core2A. It consumes only Core2A-legal items and uses learner evidence to govern attempt-first support, transfer distance, repair routing, competitive progression, and retrieval.

## Governing question

> From the currently legal transfer envelope, what is the highest-value next experience that challenges this learner without depending on untaught Physics or hiding a prerequisite failure behind solution hints?

## Two gates

Gate A is owned upstream by Core2A: source binding, taught-state, purpose, validator, answer/unit closure, near-copy and provenance.

Gate B is owned here: learner state, transfer distance, representation coverage, error history, hint dependence and retrieval due state.

Core2B may never override Gate A.

## Transfer ladder

```text
T0 DIRECT
T1 NEAR_TRANSFER
T2 REPRESENTATION_TRANSFER
T3 REVERSED_TARGET
T4 CONSTRAINT_TRANSFER
T5 DISCRIMINATION
T6 MULTI_STEP_BRIDGE
T7 SYNTHESIS
T8 COMPETITIVE_MIXED
```

Numerical ugliness is not a transfer level.

## Default escalation

- SUPPORTED -> T0 only
- INDEPENDENT -> T0/T1
- INDEPENDENT + representation evidence -> T2
- TRANSFER_READY -> T3/T4/T5
- TRANSFER_READY across compatible families -> T6/T7
- ROBUST -> T8

Policies are configurable and require empirical calibration; they are not claims of universal mastery thresholds.

## Hint policy

Core2B hints reactivate previously taught knowledge. They do not introduce new Physics. Hints should preserve the target reasoning demand and remain initially hidden where purpose requires attempt-first work.

Internal hint levels:

`NO_HINT -> RETRIEVAL_CUE -> REPRESENTATION_CUE -> MODEL_CUE -> FIRST_MOVE_CUE -> FULL_SOLUTION`

Learners should see natural language, not these labels.

## Error routing

A wrong answer is not a diagnosis. Core2B classifies the likely failure using the attempt plus existing evidence. Examples: event clock, sign convention, model selection, applicability condition, representation, algebra, units, careless execution.

Where the error points to a prerequisite knowledge gap, Core2B emits a Core1B repair request rather than repeating the whole SBA.

## Discrimination vs synthesis

Discrimination asks which model applies. Synthesis asks how multiple taught models combine. Track these separately.

## Retrieval

Core2B owns recurrence scheduling. A first policy may revisit after short, medium and longer delays with changed representation and mixed context. Exact intervals are configuration, not semantic truth.

## Production surfaces

```text
contracts/
  physics-core2b-session.schema.json
  physics-core2b-attempt.schema.json
  physics-core2b-retrieval-state.schema.json
policies/
  physics-core2b-escalation-policy.json
  physics-core2b-hint-policy.json
  physics-core2b-error-taxonomy.json
engine/
  core2b_common.py
  run_core2b.py
golden/projectile-vertical-event/
  core2b-session.json
tests/
  test_physics_core2b.py
```

The golden demonstrates legal-pool custody, evidence-gated selection, hint leakage protection, error classification, repair handoff, and retrieval update.