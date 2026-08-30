# Reality-check P0 — mandatory reporting, qualification floor and exclusive work-item custody

This reference is a binding amendment to `engineering-pr-delivery-v2`. Where older wording conflicts, this file wins for new material legs and successor endpoints.

## 1. Every repository-work response starts with the active handover

For any response that performed, attempted, audited, blocked, resumed, advanced, completed or re-grounded repository work, the first user-visible section is:

```text
# Active handover snapshot
```

No narrative prose precedes it.

This applies to `proceed next`, AUTO batches, audit-only turns, blocker discovery, NOT_RUN outcomes, PR creation/update, review gates, merge gates and ordinary task completion. The snapshot is not an occasional handover event; it is the standard completion envelope.

After the snapshot, show the full active qualification questions. Optional turn-specific prose is limited to:

```text
## Changed this turn
```

with at most eight concise bullets unless the Owner explicitly asks for a detailed report.

## 2. State Card and qualification questions are separate

The durable endpoint uses:

```text
### Active handover snapshot
<state card only; target <220 words>

### Active qualification questions
Q1: <full prompt>
Q2: <full prompt>
Q3: <full prompt>
Q4: <full prompt>
Q5: <full prompt>
```

The State Card word limit does **not** apply to Q1-Q5. Do not shorten calculations, numerical inputs, derivations, oracle requirements or falsifiers to fit the card.

Required State Card fields:

```text
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
```

## 3. Owner-authored qualification is a floor, never a suggestion

Before authoring a new Q1-Q5 pack, inspect the current Owner instruction, issue body/appendix, Owner roadmap and accepted handover for existing qualification questions or explicit technical challenges.

Record:

```text
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE: NONE | <owner source locator>
OWNER_QUALIFICATION_BASELINE_MANIFEST: NONE | <repo-relative JSON manifest>
OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE | SATISFIED | BLOCKED
```

If Owner-authored questions exist, they are the minimum technical difficulty and coverage floor. The active pack may reorganize or make them harder/more repository-specific, but it may not silently remove:

- supplied numerical values, coordinates, geometry, loads, material data or integration points;
- requested derivations or hand calculations;
- required engineering mechanisms/theory;
- independent-oracle requirements;
- falsifiers, negative cases or safe-patch/NO-PATCH reasoning.

A baseline manifest maps each Owner question to one or more active questions and lists required literal payload and required technical obligations. `validate_owner_qualification_baseline.py` fails if active questions lose that material.

## 4. Concrete engineering payload is mandatory

For `FEA`, `WRC_LOCAL_STRESS`, `LOAD_CALC` and `FIXED_FORMAT_WRITER`, marker names and technical verbs are not sufficient.

New profile-v2 packs declare:

```text
QUALIFICATION_PROFILE_VERSION: 2
```

and each question carries:

```text
Concrete payload:
Required derivation:
```

For numerical engineering profiles, at least two questions must contain a real hand-computable payload with concrete values/coordinates/loads/dimensions/record offsets or equivalent exact data. Q2 and Q4 must each contain a non-empty `Concrete payload` and `Required derivation` unless the profile is explicitly non-numerical.

A prompt such as `Reconstruct the distorted T6 Jacobian` without the element coordinates/integration point is insufficient when those values are known from the Owner baseline or repository fixture.

## 5. Exact work-item ownership precedes semantic overlap

Every new material leg/successor endpoint records:

```text
WORK_ITEM_KEY: <stable identity, e.g. github:owner/repo#1535>
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
AGENT_INSTANCE_ID: <agent-class>:<UUID>
```

A model family/name is not an agent instance identity. `OPENAI-GPT-5.6-SOL` alone is invalid.

For `EXCLUSIVE`, no two non-terminal canonical chains may hold the same `WORK_ITEM_KEY`. A second agent must join/take over the existing chain under qualification-first rules or stop.

`PARTITIONED` is allowed only with:

```text
WORK_ITEM_PARTITION: <non-overlapping scope>
WORK_ITEM_PARTITION_AUTHORITY: OWNER:<durable authorization locator>
```

Two active partitions with the same partition identity also fail closed.

Exact work-item collision is checked before path/authority semantic overlap. Semantic overlap remains an additional gate.

## 6. Handover readiness is evidence, not self-declaration

New successor endpoints use:

```text
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE: <receipt/command/evidence locator or NONE>
HANDOVER_READY: TRUE | FALSE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
```

Rules:

```text
HANDOVER_READY: TRUE
requires
HANDOVER_CONTENT_READY: TRUE
AND HANDOVER_VALIDATION_STATUS: PASS
AND non-empty HANDOVER_VALIDATION_EVIDENCE
```

If structural/qualification handover validation is `NOT_RUN` or `FAIL`, `HANDOVER_READY` is `FALSE`. This does not erase the baton; it accurately distinguishes content availability from validated readiness.

## 7. New-material adoption gate

Before a new material batch after this amendment, the active/successor state must satisfy:

```text
current Common basis
canonical v3 chain path
WORK_ITEM_KEY + mode
valid UUID-backed AGENT_INSTANCE_ID
HANDOVER_PROTOCOL_VERSION: 2
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
QUALIFICATION_PROFILE_VERSION: 2
pre-work endpoint committed before material mutation
```

Historical endpoints remain immutable evidence. They are not rewritten merely to satisfy this amendment; the next material leg deliberately adopts the new fields.
