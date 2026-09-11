# Learner Intelligence Engine — Phase 5

This phase turns the architecture and policy from Phases 1–4 into a small deterministic reference engine.

The engine is intentionally conservative. It does not infer hidden psychological causes, does not equate a wrong answer with a confirmed misconception, and does not collapse a failed final answer over earlier demonstrated reasoning.

## Inputs

- structured cross-subject reasoning fixture;
- capability registry fixture;
- versioned state-reduction policy.

## Outputs

The reference engine emits a deterministic diagnostic run containing:

- preserved capability evidence;
- candidate failure capability evidence;
- required diagnostic actions;
- conservative capability-state projections;
- cross-subject recurring-failure candidates;
- explicit forbidden conclusions;
- input and output digests.

## Invariants

1. Same evidence + same registry + same policy => byte-stable semantic output.
2. One ordinary failure cannot by itself produce `REPAIR_REQUIRED`.
3. Upstream success remains present when a later step fails.
4. Ambiguous observations require a diagnostic probe.
5. A shared capability may aggregate evidence across subjects, but cross-subject recurrence is only a candidate root cause, never a proven cognitive cause.
6. Psychological causes such as attention or working-memory limits are not inferred from answer sheets alone.
7. Subject failures remain attached to the subject reasoning contract unless the evidence explicitly points to a shared capability.

This engine is a reference implementation and falsifier surface, not a psychometric mastery model or production adaptive scheduler.
