# AUTO MODE — Relay Execution

## Purpose

AUTO MODE allows a currently qualified agent to progress automatically through the approved engineering mission without routine phase-by-phase confirmation.

It does not remove relay, qualification, concurrency, code-quality, or source/validation controls.

## Activation

When the owner explicitly uses `AUTO MODE`, record in the chain's current state or latest endpoint:

```text
EXECUTION_MODE: AUTO
AUTO_STATE: RUNNING
SCOPE_AUTHORITY: LOCKED_TO_APPROVED_MISSION
MERGE_AUTHORITY: OWNER_ONLY unless separately authorized
```

For canonical chains, current custody is in:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
```

## Execution loop

While no hard stop exists:

1. re-check live repository and active-chain overlap state;
2. read the exact current `ACTIVE.md` repository blob/version and `CUSTODY_EPOCH`;
3. select the next bounded action inside the approved mission;
4. preserve current hypothesis, prediction, invariants, expected changed files, and code-quality boundary;
5. implement one coherent unit;
6. validate;
7. create the next immutable endpoint with `CUSTODY_EPOCH + 1`;
8. update that chain's `ACTIVE.md` against the exact prior repository version;
9. if the update conflicts or epoch changed, classify `STALE_WRITE`, stop mutation, and re-ground;
10. refresh Q1-Q5 for the next unresolved leg;
11. continue automatically.

Routine phase completion is not a reason to ask whether to continue.

Different independent chains do not update each other's `ACTIVE.md` and therefore should not block one another merely for relay bookkeeping.

## Qualification boundary

AUTO MODE is scoped to a qualified custody window.

A new incoming candidate must still complete takeover qualification before engineering-critical mutation.

AUTO MODE cannot convert:

```text
READ_ONLY
```

into:

```text
WRITE_ALLOWED
```

without a valid qualification verdict.

## Crash safety

Because an AUTO agent may disappear at any point, every material endpoint must remain recoverable without chat context.

Never postpone all relay state until the end of a long autonomous batch.

If an endpoint is written but `ACTIVE.md` is not advanced, treat it as an orphan durable endpoint and reconcile it. If another agent advanced the same chain first, do not force the pointer.

## Hard stops

Stop automatic production mutation when:

- the next action materially expands approved scope;
- engineering/source/benchmark/oracle/publication authority must change beyond approved bounds;
- an independent oracle materially contradicts implementation and bounded isolation has not resolved the discrepancy;
- qualification becomes stale or invalid;
- the same-chain `ACTIVE.md` write is stale/conflicted;
- active-chain authority collision is `BLOCKED_BY_ACTIVE_CHAIN` or unresolved `UNKNOWN`;
- continuing requires guessing engineering intent;
- validation would require weakening expected values/tolerances;
- code-quality boundaries can only be satisfied through speculative/unused abstractions or unrelated refactor;
- a destructive/security/credential operation needs new authorization;
- merge is next but merge authority is absent;
- repeated diagnosis no longer has a concrete hypothesis, falsifier, and isolating experiment.

On hard stop create an endpoint with the appropriate state and exact next action. Do not fabricate a successful custody update after a stale-write failure.

## Merge

AUTO MODE never implies AUTO MERGE.
