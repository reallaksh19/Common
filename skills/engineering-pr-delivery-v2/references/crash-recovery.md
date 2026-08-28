# Crash Recovery — qualification first

## Governing rule

An abrupt loss must not require the outgoing agent. The last accepted endpoint already contains the work baton and the next-agent exam.

## Entry state

On agent loss:

```text
TAKEOVER_AUTHORITY: READ_ONLY
CUSTODY_STATE: TAKEOVER_REQUIRED
QUALIFICATION_STATE: PENDING
WRITE_AUTHORITY: READ_ONLY
AUTO_STATE: PAUSED
```

## Step 1 — minimal bootstrap only

Before qualification, the replacement may only locate/read enough to take the exam:

1. repository and chain;
2. `ACTIVE.md` and referenced accepted endpoint;
3. PR identity;
4. `QUESTION_SET_ID` and `QUALIFICATION_BASIS_HEAD`;
5. pinned repository/source/roadmap evidence needed to answer Q1-Q5.

It may inspect and calculate as part of the examination. It may not reconcile later commits as accepted work, advance custody, mutate production/tests/oracles/roadmaps, create an accepted recovery endpoint, or resume AUTO MODE.

## Step 2 — takeover qualification

Answer the pre-authored Q1-Q5 against the pinned accepted basis. Obtain independent verification.

```text
FAIL/DEFERRED -> remain READ_ONLY
PASS -> QUALIFIED_PENDING_RECONCILIATION, still READ_ONLY
```

## Step 3 — post-PASS reconciliation

Only after PASS:

1. fetch live main/base, PR head, merge base, diff, reviews/checks;
2. inspect every commit/path after the accepted endpoint basis;
3. inspect orphan/divergent endpoints;
4. re-read current owner roadmap(s) and source/benchmark/oracle authority;
5. compare active chains/overlap/dependencies;
6. classify crash-window work:

```text
RECOVERABLE
PARTIAL_UNKNOWN
CONTAMINATED
UNTRUSTED
```

7. create the recovery/reconciliation endpoint;
8. advance `ACTIVE.md` using exact-version/custody-epoch discipline;
9. grant `WRITE_ALLOWED` only if current-state authority is safe.

## Crash-window principle

Material commits after the last accepted endpoint do not automatically make its qualification unusable. The endpoint exam tests competence at the last accepted basis; post-basis work is exactly what the qualified replacement must reconcile afterward.

If the pinned basis/question set itself cannot be recovered or is malformed, stop. An independent question authority/Owner must repair or adopt a valid qualification set. The candidate may not create a replacement exam and use it to self-qualify.

## Recovery outcomes

```text
CONTINUE
SALVAGE_PARTIAL
SUPERSEDE
ABANDON
```

Agent replacement alone does not require a new PR.

## Unpersisted work

Unpushed/local-only work is not recoverable authority. Never invent it from chat summaries.
