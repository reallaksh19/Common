# AUTO MODE — Relay Execution

## Purpose

AUTO MODE allows a currently qualified agent to progress automatically through the approved engineering mission without routine phase-by-phase confirmation.

It does not remove relay, qualification, concurrency, owner-roadmap, code-quality, source-authority, or validation controls.

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

Before material coding, version-2 chains also require current `ROADMAPS` binding and `ROADMAP_REVIEW_STATUS`.

## Execution loop

While no hard stop exists:

1. re-check live repository and active-chain overlap state;
2. read the exact current `ACTIVE.md` repository blob/version and `CUSTODY_EPOCH`;
3. verify every bound roadmap blob is still current;
4. if starting a new material leg, read/re-ground every applicable owner roadmap before coding;
5. select the next bounded action inside the approved mission and owner-roadmap intent;
6. preserve current hypothesis, prediction, invariants, expected changed files, roadmap alignment, and code-quality boundary;
7. implement one coherent unit;
8. validate;
9. create the next immutable endpoint with `CUSTODY_EPOCH + 1`;
10. update that chain's `ACTIVE.md` against the exact prior repository version;
11. if the update conflicts or epoch changed, classify `STALE_WRITE`, stop mutation, and re-ground;
12. refresh Q1-Q5 for the next unresolved leg;
13. continue automatically.

Routine phase completion is not a reason to ask whether to continue.

Different independent chains do not update each other's `ACTIVE.md` and therefore should not block one another merely for relay bookkeeping.

## Roadmap proposal boundary

AUTO MODE may create an immutable roadmap proposal when evidence suggests a strategic improvement, for example:

```text
major concept/architecture change
new benchmark family
benchmark replacement
phase reorder
new capability/scope addition
source/authority boundary change
status refresh after material drift
```

The proposal remains advisory. AUTO MODE does **not** authorize mutation of an owner roadmap.

Roadmap write permission must be explicit and separate from:

```text
AUTO MODE
permission to proceed
PR merge authorization
issue assignment
prior roadmap authorization
```

If the next safe technical step requires changing owner roadmap intent first, stop at `OWNER_DECISION_REQUIRED` and present the proposal.

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

A material roadmap intent change may also make an existing qualification stale and require re-grounding/requalification.

## Crash safety

Because an AUTO agent may disappear at any point, every material endpoint must remain recoverable without chat context.

Never postpone all relay state until the end of a long autonomous batch.

If an endpoint is written but `ACTIVE.md` is not advanced, treat it as an orphan durable endpoint and reconcile it. If another agent advanced the same chain first, do not force the pointer.

If a roadmap changed while the agent was unavailable, the old roadmap blob binding is stale; re-read it before material production mutation.

## Hard stops

Stop automatic production mutation when:

- the next action materially expands approved scope;
- planned implementation contradicts owner roadmap intent;
- a roadmap mutation is required but explicit owner roadmap-write authorization is absent;
- a bound roadmap blob changed and has not been re-read/reconciled;
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

On hard stop create an endpoint with the appropriate state and exact next action. Do not fabricate a successful custody or roadmap update.

## Merge

AUTO MODE never implies AUTO MERGE.

Merge authorization never implies owner-roadmap write authorization.
