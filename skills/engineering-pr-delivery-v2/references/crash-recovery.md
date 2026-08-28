# Crash Recovery — qualification first

## Governing rule

An abrupt loss must not require the outgoing agent. The last accepted endpoint already contains the work baton and next-agent exam.

## Entry state

```text
TAKEOVER_AUTHORITY: READ_ONLY
CUSTODY_STATE: TAKEOVER_REQUIRED
QUALIFICATION_STATE: PENDING
WRITE_AUTHORITY: READ_ONLY
AUTO_STATE: PAUSED
```

## Step 1 — minimal bootstrap and exam admission only

Before qualification the replacement may only:

1. locate repository/chain, `ACTIVE.md`, accepted endpoint and PR;
2. locate `QUESTION_SET_ID` and `QUALIFICATION_BASIS_HEAD`;
3. perform the READ_ONLY question-set admission check;
4. read pinned code/tests/data/roadmap/source/oracle evidence needed to answer Q1-Q5;
5. perform calculations needed for the exam.

It may not reconcile later commits as accepted work, advance custody, mutate production/tests/oracles/roadmaps, create an accepted recovery endpoint, or resume AUTO MODE.

Admission states:

```text
VALID
STALE
MALFORMED
AUTHORITY_CONTAMINATED
INSUFFICIENT_TECHNICAL_DEPTH
```

Only `VALID` proceeds. Legacy v1/v2 sets require explicit admission under the current rules. A candidate may not repair/admit its own exam and self-qualify.

## Step 2 — takeover qualification

Answer admitted Q1-Q5 against the pinned basis and obtain independent verification.

```text
FAIL/DEFERRED -> remain READ_ONLY
PASS -> QUALIFIED_PENDING_RECONCILIATION, still READ_ONLY
```

## Step 3 — post-PASS reconciliation

Only after PASS:

1. fetch live main/base, PR head, merge base, diff, reviews/checks;
2. inspect every commit/path after the qualification basis;
3. inspect orphan/divergent endpoints;
4. re-read current owner roadmap(s), sources, benchmarks, oracles and methodology authority;
5. compare active chains/overlap/dependencies;
6. classify crash-window recoverability as needed;
7. classify `POST_BASIS_DRIFT`;
8. determine whether qualification coverage is retained, independently confirmed, or stale;
9. only then create the recovery/reconciliation endpoint and advance `ACTIVE.md`;
10. grant `WRITE_ALLOWED` only if qualification coverage and all current-state authority are clear.

## Post-basis drift

```text
NONE | METADATA_ONLY
-> QUALIFICATION_COVERAGE: RETAINED

MATERIAL_WITHIN_QUALIFIED_BOUNDARY
-> QUALIFICATION_COVERAGE: INDEPENDENTLY_CONFIRMED required

MATERIAL_BOUNDARY_CHANGED | AUTHORITY_CHANGED | CONTAMINATED
-> QUALIFICATION_COVERAGE: REQUALIFICATION_REQUIRED
-> WRITE_AUTHORITY: READ_ONLY
-> fresh independently authored Q1-Q5
-> qualify again before custody/write
```

Material commits after the accepted endpoint do not automatically invalidate the first exam; the replacement qualifies against the accepted basis first. But post-PASS reconciliation may prove that a **second qualification** is required for the recovered live boundary.

## Recovery classifications

For crash-window work itself, retain:

```text
RECOVERABLE
PARTIAL_UNKNOWN
CONTAMINATED
UNTRUSTED
```

Recovery outcomes remain:

```text
CONTINUE
SALVAGE_PARTIAL
SUPERSEDE
ABANDON
```

Agent replacement alone does not require a new PR. Unpushed/local-only work is not recoverable authority.
