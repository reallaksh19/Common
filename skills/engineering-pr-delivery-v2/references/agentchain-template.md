# Agent Chain Templates — version 3 qualification-first

## ACTIVE.md

```text
CHAIN_STATE_VERSION: 3
CHAIN_ID: <CHAIN_ID>
MISSION: <one-line mission>
ACTIVE_ENDPOINT: EP-0001
ACTIVE_ENDPOINT_FILE: agents/chains/<CHAIN_ID>/endpoints/EP-0001.md
MATERIAL_HISTORY_ROOT_BASE: <40-hex commit before first material batch>
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: agents/chains/<CHAIN_ID>/endpoints/EP-0001.md
PR: <number-or-PENDING>
BRANCH: <branch>
HEAD: <accepted checkpoint head>
STATE: ACTIVE
ENGINEERING_STATE: READY
CUSTODY_STATE: HELD
QUALIFICATION_STATE: NOT_REQUIRED
WRITE_AUTHORITY: WRITE_ALLOWED
AUTO_STATE: NOT_APPLICABLE
MERGE_AUTHORITY: OWNER_ONLY
AUTHORITY_DOMAIN: <domain>
ACTIVE_CUSTODIAN: <agent-id>
CUSTODY_EPOCH: 1
COORDINATION_STATE: SAFE
DEPENDENCIES: NONE
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <40-hex live Common commit actually read for this leg>
COMMON_PROTOCOL_STATUS: CURRENT
ROADMAPS: <path>@<blob-sha> | NONE — <reason>
ROADMAP_REVIEW_STATUS: COMPLETE | NOT_APPLICABLE | BLOCKED
HANDOVER_READY: TRUE
```

`MATERIAL_HISTORY_ROOT_BASE` anchors the append-only material-batch audit for this chain. `MATERIAL_LEG_PREWORK_ENDPOINT_FILE` points to the work-ahead endpoint for the current material batch; after that batch completes, preserve its proof in a `material-legs/<MATERIAL_LEG_ID>.md` receipt before starting the next batch.

## Non-terminal endpoint

```text
# EP-0001 — <title>
CHAIN_ID:
LEG_ID:
ENDPOINT_ID:
PREVIOUS_ENDPOINT:
CUSTODY_EPOCH:
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS:
COMMON_PROTOCOL_STATUS: CURRENT
PREWORK_QUALIFICATION_READY: TRUE
QUALIFICATION_PROFILE: FEA | WRC_LOCAL_STRESS | LOAD_CALC | FIXED_FORMAT_WRITER | PARSER_TOPOLOGY | SOURCE_GOVERNANCE | GENERAL_ENGINEERING
ROADMAPS:
ROADMAP_REVIEW_STATUS:
HANDOVER_READY: TRUE
TASK / ISSUE:
PR:
BRANCH:
CHECKPOINT_HEAD:
MAIN_HEAD_OBSERVED:
MERGE_BASE:
STATE:
ENGINEERING_STATE:
CUSTODY_STATE:
QUALIFICATION_STATE:
WRITE_AUTHORITY:
AUTO_STATE:
MERGE_AUTHORITY:

### Handover snapshot
Repo:
Task:
Chain:
Endpoint:
PR:
PR status:
Branch / PR head / main:
Merge authority:
Engineering / custody / qualification / write state:
Protocol basis / status:
Roadmap:
Inputs:
Benchmarks:
Governing docs / authoritative sources:
Current blocker:
Exact next action:
Q1: <concise production reconstruction>
Q2: <concise calculation/failure isolation>
Q3: <concise authority/falsifier>
Q4: <concise independent oracle/reconstruction>
Q5: <concise safe patch/NO-PATCH>

### Mission
### This leg completed
### Currently in progress
### Remaining work
### Exact next action
### Known / proven
### Not proven
### NOT_RUN
### Active hypothesis
### Falsifier
### Protected invariants
### Do not redo
### Do not change
### Expected next-leg files / domains
### Owner roadmaps
### Inputs
### Benchmarks
### Common / governing documents
### Authoritative sources
### Production paths
### Validation / test paths
### Changed during this leg
### Validation summary
### Open risks / questions

### Takeover qualification pack
PURPOSE: QUALIFICATION_ONLY
NOT_AN_IMPLEMENTATION_TASK: TRUE
QUALIFICATION_PROTOCOL_VERSION: 3
QUALIFICATION_PROFILE: <same profile as endpoint>
QUALIFICATION_BASIS_HEAD:
QUESTION_SET_ID:
QUESTION_SET_STATUS: CURRENT
QUESTION_SET_AUTHOR:
QUESTION_SET_ADMISSION_REQUIREMENT: REQUIRED_ON_TAKEOVER

#### Q1 — Production Trace
Repository anchors:
Production object/case:
Domain challenge:
Exact repository data required:
Required technical work:
Required numerical/technical evidence:
First authority/ownership boundaries:
Fail if:

#### Q2 — Current Unresolved Problem / Failure Isolation
Repository anchors:
Domain challenge:
Exact repository data required:
Calculation/reconstruction:
Required numerical/technical evidence:
Predicted intermediate values:
First wrong boundary:
Falsifier:
Fail if:

#### Q3 — Authority / Invariant
Repository anchors:
Domain challenge:
Exact repository data required:
Required technical work:
Authority/source trace:
Protected invariant:
First wrong boundary:
Falsifier:
Invalid shortcut:
Fail if:

#### Q4 — Independent Validation
Repository anchors:
Domain challenge:
Exact repository data required:
Calculation/reconstruction:
Required technical work:
Independent oracle:
Required numerical/technical evidence:
Units/sign/tolerance:
Falsifier:
Fail if:

#### Q5 — Next Contribution / Minimal Patch
Repository anchors:
Domain challenge:
Exact repository data required:
Required technical work:
Safe patch boundary:
Expected before/after evidence:
Protected unchanged domains:
Validation required:
Negative test:
Rollback/falsifier boundary:
No-patch condition:
Fail if:
```

The snapshot is <300 words; detailed Q1–Q5 remain outside that limit.

`PREWORK_QUALIFICATION_READY: TRUE` is valid only when this endpoint and its expert Q1–Q5 were committed before the first material change of the batch. `validate_prework_history.py` proves the current batch ordering; append-only material-leg receipts preserve the proof for all completed batches.

At every substantive user-facing handover/status boundary, reproduce the concise active snapshot including Q1–Q5. Do not merely state that the endpoint contains questions.

## Material-leg completion receipt

After each completed material batch, before starting another:

```text
# agents/chains/<CHAIN_ID>/material-legs/LEG-001.md
CHAIN_ID:
MATERIAL_LEG_ID: LEG-001
PREVIOUS_MATERIAL_LEG: NONE | LEG-000
MATERIAL_LEG_BASE: <commit before this batch's first material commit; prework endpoint already exists or is introduced after this base>
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: agents/chains/<CHAIN_ID>/endpoints/<EP>.md
MATERIAL_LEG_HEAD: <last material commit in this batch>
MATERIAL_LEG_HISTORY_STATUS: RECORDED
MATERIAL_SCOPE: <bounded material change>
```

Inter-leg gaps and trailing changes after the last receipt must be relay/qualification-only. See `material-leg-history.md`.

## Takeover admission receipt

Recommended:

```text
QUALIFICATION_PROTOCOL_VERSION: 3
CHAIN_ID:
ENDPOINT_ID:
QUESTION_SET_ID:
QUALIFICATION_BASIS_HEAD:
QUESTION_SET_ADMISSION_STATUS: VALID
ADMISSION_AUTHORITY_ID:
BASIS_RETRIEVABLE: TRUE
TECHNICAL_DEPTH_STATUS: PASS
ROADMAP_AUTHORITY_STATUS: VALID | NOT_APPLICABLE
SOURCE_ORACLE_AUTHORITY_STATUS: VALID | NOT_APPLICABLE
LEGACY_SET: TRUE | FALSE
ADMISSION_EVIDENCE:
```

## Post-PASS reconciliation receipt

```text
QUALIFICATION_PROTOCOL_VERSION: 3
CHAIN_ID:
ENDPOINT_ID:
QUESTION_SET_ID:
QUALIFICATION_BASIS_HEAD:
CANDIDATE_ID:
RECONCILIATION_REVIEWER_ID:
LIVE_HEAD:
POST_BASIS_COMMITS:
POST_BASIS_DRIFT:
QUALIFICATION_COVERAGE:
CURRENT_STATE_AUTHORITY: CLEAR | BLOCKED
WRITE_AUTHORITY_DECISION: READ_ONLY | WRITE_ALLOWED
RECONCILIATION_EVIDENCE:
```

Existing v1/v2 history is never rewritten. A legacy set must be admitted before use; after qualification and reconciliation, migrate to version 3 before material mutation.