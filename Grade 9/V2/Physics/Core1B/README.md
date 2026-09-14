# Physics Core1B — learner concept-construction runtime

Core1B executes already-released Core1A teaching authority for a particular learner. It does not author new Physics or infer mastery from an authored unit.

## Required input custody

Every unit binds the exact `core1a_release_ref` and `core1a_release_digest`. The runtime validates that binding before instruction. A unit can reorganize/scaffold only the atoms and problem families authorized upstream.

## Adaptive atom graph

The atom registry is deliberately fine-grained for fragile learners. It is not a mandatory script. A prerequisite may be omitted only when an earlier provenance-backed observed event already shows that atom secure.

## Readiness versus evidence

`readiness_requirements` states what the learner must demonstrate. It is configuration, not evidence. Learner state can change only from append-only observed events whose basis is `LEARNER_RESPONSE`, `DIAGNOSTIC`, or `TEACHER_OBSERVATION`.

Core1B may establish `INDEPENDENT`. Transfer readiness/robustness belongs downstream to Core2B evidence.

If Core1A requires model-validity understanding, `applicability` is mandatory. `explain` is mandatory only when the upstream capability contract requires explanation.

## Runtime flow

```text
released Core1A authority
  -> select/skip atoms using observed evidence
  -> learner-facing instruction
  -> independent attempt
  -> observed event
  -> evidence-derived release receipt
```

A Core1B release receipt proves that observed evidence satisfied the unit's required criteria. It does not legalize transfer items; Core2A remains the transfer-legality authority.
