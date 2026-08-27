# AUTO MODE — Relay Execution

## Purpose

AUTO MODE allows a currently qualified agent to progress automatically through the approved engineering mission without routine phase-by-phase confirmation.

It does not remove the relay or qualification controls.

## Activation

When the owner explicitly uses `AUTO MODE`, record in the latest endpoint or active-chain state:

```text
EXECUTION_MODE: AUTO
AUTO_STATE: RUNNING
SCOPE_AUTHORITY: LOCKED_TO_APPROVED_MISSION
MERGE_AUTHORITY: OWNER_ONLY unless separately authorized
```

## Execution loop

While no hard stop exists:

1. re-check live repository and active-chain overlap state;
2. select the next bounded action inside the approved mission;
3. preserve current hypothesis, prediction, invariants, and expected changed files;
4. implement one coherent unit;
5. validate;
6. create/refresh the endpoint;
7. refresh Q1-Q5 for the next unresolved leg;
8. continue automatically.

Routine phase completion is not a reason to ask whether to continue.

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

## Hard stops

Stop automatic production mutation when:

- the next action materially expands approved scope;
- engineering/source/benchmark/oracle/publication authority must change beyond approved bounds;
- an independent oracle materially contradicts implementation and bounded isolation has not resolved the discrepancy;
- qualification becomes stale or invalid;
- an active-chain authority collision is `BLOCKED` or unresolved `UNKNOWN`;
- continuing requires guessing engineering intent;
- validation would require weakening expected values/tolerances;
- a destructive/security/credential operation needs new authorization;
- merge is next but merge authority is absent;
- repeated diagnosis no longer has a concrete hypothesis, falsifier, and isolating experiment.

On hard stop create an endpoint with:

```text
STATE: BLOCKED | RECOVERY_REQUIRED | QUALIFICATION_REQUIRED
AUTO_STATE: BLOCKED | OWNER_DECISION_REQUIRED | TAKEOVER_REQUIRED
EXACT_NEXT_ACTION:
Q1..Q5:
```

## Merge

AUTO MODE never implies AUTO MERGE.
