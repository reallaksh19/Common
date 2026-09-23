# Engineering Relay V3.1 — recorder-first model

## Purpose

V3.1 is a durable engineering **recording, continuity and reconstruction machine**.

It records:

- programme/issue context;
- execution packages;
- current actor/lease;
- checkpoints, including failed or partial evidence;
- controls and warnings;
- material/drift observations;
- continuation receipts;
- handover/recovery history;
- local-execution evidence;
- delivery/provider observations;
- roadmap and closure history.

It does **not** stop engineering work because a coordination precondition is missing.

## Base mantra

Persist enough truth that another agent can reconstruct what happened and continue without hidden chat context.

```text
observe
→ record
→ continue
→ reconstruct when needed
```

not:

```text
observe
→ invent a gate
→ block engineering
```

## Recorder boundaries

Policy conditions are advisory:

- lease/custody mismatch;
- stale epoch;
- active predecessor;
- inactivity horizon;
- changed unaccepted material;
- programme selection;
- controls;
- scope/protected-path declarations;
- material drift;
- checkpoint PASS/FAIL state;
- quality state;
- handover freshness;
- provider/delivery state;
- Owner delivery-authority observation.

Structural integrity remains enforced:

- parseable/schema-valid records at write boundaries;
- immutable IDs are not overwritten;
- event history remains append-only;
- transactions remain atomic/recoverable.

## Checkpoints

A checkpoint is a durable report of engineering state. It may contain PASS or FAIL evidence.

Recording a checkpoint does not claim that all acceptance criteria passed. Downstream projections may separately decide whether a checkpoint constitutes accepted evidence.

## Handover and recovery

Handover and recovery are history labels, not prerequisites for continuation.

A successor can take over immediately. The recorder preserves predecessor state and records what evidence was or was not available.

## Local execution

Local helpers still do not become the engineering voice merely by returning evidence. Their results are recorded as external evidence. The current engineering agent decides what to do next, but Relay does not block that decision.

## Non-goals

V3.1 does not:

- authorize GitHub permissions;
- guarantee code correctness;
- replace tests/review;
- infer academic/product truth;
- fabricate evidence;
- hide unresolved warnings;
- use older protocol generations as fallback authority.
