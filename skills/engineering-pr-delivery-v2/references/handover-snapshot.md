# Active Handover Snapshot — mandatory repository-work response envelope

## Purpose

The Active handover is no longer an occasional end-of-session artifact. For every response that performed, attempted, audited, blocked, resumed, advanced, completed or re-grounded repository work, the agent's **first user-visible section** is the Active handover snapshot.

No narrative prose precedes it. After the snapshot, show the full active qualification questions. Optional turn-specific reporting is limited to `## Changed this turn` with at most eight concise bullets unless the Owner explicitly asks for a detailed report.

## Durable endpoint structure

New successor endpoints under `HANDOVER_PROTOCOL_VERSION: 2` contain two separate sections:

```text
### Active handover snapshot
Repo:
Task:
Chain:
Endpoint:
PR:
PR status:
Branch / PR head / main:
Merge authority:
Engineering / custody / qualification / write state:
AUTO:
Protocol basis / status:
Roadmap:
Inputs:
Benchmarks:
Governing docs / authoritative sources:
Current blocker:
Leg diagnosis:
Exact next action:

### Active qualification questions
Q1: <full expert prompt>
Q2: <full expert prompt>
Q3: <full expert prompt>
Q4: <full expert prompt>
Q5: <full expert prompt>
```

The full questions correspond exactly to the detailed `### Takeover qualification pack` below them. They are not topic labels.

## Word limit

The `<220 words` target applies only to the State Card inside `### Active handover snapshot`.

Q1-Q5 are deliberately outside that limit. Do not remove numerical values, coordinates, loads, dimensions, integration points, required derivations, independent-oracle requirements, falsifiers or NO-PATCH reasoning to make the card shorter.

Historical v3 endpoints using `### Handover snapshot` and the former `<300 words including Q1-Q5` format remain immutable history. The next material leg adopts protocol version 2.

## Every-response triggers

The Active handover envelope is mandatory after all of these, not only at a traditional handover:

```text
proceed next
AUTO batch
read-only audit
blocked / NOT_RUN outcome
PR create/update
review/status re-ground
material batch completion
owner-decision boundary
merge boundary
explicit handover
task completion
```

Saying only `EP-xxxx contains Q1-Q5` is invalid.

## Readiness evidence

New endpoints use:

```text
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE: <durable evidence locator or NONE>
HANDOVER_READY: TRUE | FALSE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
```

`HANDOVER_READY: TRUE` is valid only when:

```text
HANDOVER_CONTENT_READY == TRUE
HANDOVER_VALIDATION_STATUS == PASS
HANDOVER_VALIDATION_EVIDENCE is non-empty and not NONE
```

If structural/qualification handover validation is `NOT_RUN` or `FAIL`, keep the baton content but report:

```text
HANDOVER_CONTENT_READY: TRUE
HANDOVER_VALIDATION_STATUS: NOT_RUN | FAIL
HANDOVER_READY: FALSE
```

This prevents self-declared readiness from being mistaken for executed validation evidence.

## Crash discipline

Before a material batch, a current work-ahead endpoint and full expert Q1-Q5 must already exist. After a coherent material batch, publish the receipt/successor endpoint before another material batch begins. A replacement qualifies against the pinned accepted basis first; later crash-window work is reconciled only after qualification PASS.
