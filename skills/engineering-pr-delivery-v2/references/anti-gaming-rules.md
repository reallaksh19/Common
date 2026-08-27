# Relay Anti-Gaming Rules

## Engineering evidence

Never:

- weaken a tolerance merely because a test fails;
- replace independent expected values with production output;
- change implementation and oracle together and call the result independent;
- delete, skip, or mute a difficult benchmark to obtain green status;
- hard-code fixture answers into production;
- silence fail-closed behavior to obtain PASS;
- claim source inspection as runtime execution;
- claim `NOT_RUN` as `PASS`;
- silently widen engineering authority from a narrower qualified source.

## Relay integrity

### REL-01 — No self-authorization

A candidate cannot grant itself engineering-critical write authority.

```text
candidate_id == verifier_id
-> INVALID_SELF_VERIFIED
```

### REL-02 — No post-answer exam rewriting

Do not rewrite Q1-Q5 after seeing the candidate answer merely to manufacture a pass/fail result.

If the question set was defective or stale, supersede it explicitly with a new endpoint/question-set ID and reason.

### REL-03 — Endpoint history is append-only

Do not edit an earlier technical endpoint to hide mistakes, uncertainty, or a failed hypothesis.

Correct it through supersession.

### REL-04 — No stale qualification

A verdict against a materially different repository state cannot authorize current engineering-critical mutation.

### REL-05 — No generic qualification

Five theory questions do not satisfy the gate merely because five headings exist.

### REL-06 — Questions target next work

A retrospective checklist that only confirms completed work is not a valid next-agent qualification set.

### REL-07 — Missing custody must remain visible

Inputs, benchmarks, common/governing docs, authoritative sources, production paths, and validation paths cannot be silently omitted.

Use explicit `NONE` or `UNRESOLVED` with rationale.

### REL-08 — Agent loss is not graceful handoff

Do not represent an abrupt disappearance as an intentional handover event.

Record recovery against the last durable endpoint.

### REL-09 — PR merge is not chain completion

Do not mark a chain complete because one PR merged when technical work remains.

### REL-10 — No chat-only authority

A prior agent's chat summary cannot override repository evidence or substitute for a missing durable engineering state.

### REL-11 — No silent source promotion

Being listed as an input/reference does not automatically make a source authoritative for every semantic field.

### REL-12 — No unbounded recovery guessing

If post-endpoint work cannot be reconciled without guessing engineering intent, quarantine/salvage/supersede rather than continuing from sunk cost.
