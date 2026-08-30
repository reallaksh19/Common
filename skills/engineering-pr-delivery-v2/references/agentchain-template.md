# Agent Chain Templates — version 3 custody + handover protocol 2

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
ACTIVE_CUSTODIAN: <human-readable agent label>
AGENT_INSTANCE_ID: <agent-class>:<UUID>
WORK_ITEM_KEY: <stable identity, e.g. github:owner/repo#1535>
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
WORK_ITEM_PARTITION: NONE | <partition id>
WORK_ITEM_PARTITION_AUTHORITY: NONE | OWNER:<durable locator>
CUSTODY_EPOCH: 1
COORDINATION_STATE: SAFE
DEPENDENCIES: NONE
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <40-hex live Common commit actually read for this leg>
COMMON_PROTOCOL_STATUS: CURRENT
ROADMAPS: <path>@<blob-sha> | NONE — <reason>
ROADMAP_REVIEW_STATUS: COMPLETE | NOT_APPLICABLE | BLOCKED
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE
HANDOVER_VALIDATION_STATUS: PASS
HANDOVER_VALIDATION_EVIDENCE: <durable receipt/command evidence>
HANDOVER_READY: TRUE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE: NONE | <owner locator>
OWNER_QUALIFICATION_BASELINE_MANIFEST: NONE | <repo-relative JSON path>
OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE | SATISFIED | BLOCKED
```

For `WORK_ITEM_MODE: PARTITIONED`, `WORK_ITEM_PARTITION` and Owner partition authority are mandatory. A model family/name is not a valid unique `AGENT_INSTANCE_ID`.

`MATERIAL_HISTORY_ROOT_BASE` anchors append-only material-batch history. `MATERIAL_LEG_PREWORK_ENDPOINT_FILE` points to the work-ahead endpoint for the current batch.

## Non-terminal endpoint

```text
# EP-0001 — <title>
CHAIN_ID:
LEG_ID:
ENDPOINT_ID:
PREVIOUS_ENDPOINT:
CUSTODY_EPOCH:
ENDPOINT_REASON:
CHAIN_STATE_VERSION: 3
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS:
COMMON_PROTOCOL_STATUS: CURRENT
PREWORK_QUALIFICATION_READY: TRUE
QUALIFICATION_PROFILE: FEA | WRC_LOCAL_STRESS | LOAD_CALC | FIXED_FORMAT_WRITER | PARSER_TOPOLOGY | SOURCE_GOVERNANCE | GENERAL_ENGINEERING
QUALIFICATION_PROFILE_VERSION: 2
WORK_ITEM_KEY:
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
AGENT_INSTANCE_ID: <agent-class>:<UUID>
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE:
OWNER_QUALIFICATION_BASELINE_MANIFEST:
OWNER_QUALIFICATION_BASELINE_STATUS:
ROADMAPS:
ROADMAP_REVIEW_STATUS:
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE:
HANDOVER_READY: TRUE | FALSE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
TASK / ISSUE:
PR:
BRANCH:
CHECKPOINT_HEAD:
QUALIFICATION_BASIS_HEAD:
QUESTION_SET_ID:
QUESTION_SET_STATUS: CURRENT | STALE
MAIN_HEAD_OBSERVED:
MERGE_BASE:
STATE:
ENGINEERING_STATE:
CUSTODY_STATE:
QUALIFICATION_STATE:
WRITE_AUTHORITY:
AUTO_STATE:
MERGE_AUTHORITY:

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
Q1: <full production reconstruction prompt with concrete payload where applicable>
Q2: <full calculation/failure-isolation prompt>
Q3: <full authority/falsifier prompt>
Q4: <full independent-oracle/reconstruction prompt>
Q5: <full safe-patch/rollback/NO-PATCH prompt>

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

### Next-agent qualification
Q1-Q5 below are takeover qualification only, never the task list.

### Takeover qualification pack
PURPOSE: QUALIFICATION_ONLY
NOT_AN_IMPLEMENTATION_TASK: TRUE
QUALIFICATION_PROTOCOL_VERSION: 3
QUALIFICATION_PROFILE: <same profile as endpoint>
QUALIFICATION_PROFILE_VERSION: 2
QUALIFICATION_BASIS_HEAD:
QUESTION_SET_ID:
QUESTION_SET_STATUS: CURRENT
QUESTION_SET_AUTHOR: <agent-instance-id or independent question authority>
QUESTION_SET_ADMISSION_REQUIREMENT: REQUIRED_ON_TAKEOVER
OWNER_QUALIFICATION_BASELINE_SOURCE:
OWNER_QUALIFICATION_BASELINE_MANIFEST:
OWNER_QUALIFICATION_BASELINE_STATUS:

#### Q1 — Production Trace
Repository anchors:
Production object/case:
Domain challenge:
Exact repository data required:
Concrete payload:
Required derivation:
Required technical work:
Required numerical/technical evidence:
First authority/ownership boundaries:
Fail if:

#### Q2 — Current Unresolved Problem / Failure Isolation
Repository anchors:
Domain challenge:
Exact repository data required:
Concrete payload:
Required derivation:
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
Concrete payload:
Required derivation:
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
Concrete payload:
Required derivation:
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
Concrete payload:
Required derivation:
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

The State Card under `### Active handover snapshot` targets <220 words. Full Q1-Q5 are outside that limit and must preserve Owner/numerical detail.

At every bounded repository-work response, the user-visible response starts with the Active handover snapshot, then full active Q1-Q5, then optional `Changed this turn` delta bullets. No prose precedes the snapshot.

## Owner baseline manifest

If Owner-authored qualification/challenges exist, create:

```text
agents/chains/<CHAIN_ID>/qualification-baselines/<BASELINE_ID>.json
```

following `owner-qualification-baseline.md`. The manifest preserves supplied literals, concepts and required obligations and maps them to active Q1-Q5.

## Material-leg completion receipt

After each completed material batch, before starting another:

```text
# agents/chains/<CHAIN_ID>/material-legs/LEG-001.md
CHAIN_ID:
MATERIAL_LEG_ID: LEG-001
PREVIOUS_MATERIAL_LEG: NONE | LEG-000
MATERIAL_LEG_BASE: <commit before first material commit>
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: agents/chains/<CHAIN_ID>/endpoints/<EP>.md
MATERIAL_LEG_HEAD: <last material commit>
MATERIAL_LEG_HISTORY_STATUS: RECORDED
MATERIAL_SCOPE: <bounded material change>
```

Inter-leg gaps and trailing changes after the last receipt must be relay/qualification-only.

## Takeover admission receipt

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
OWNER_BASELINE_STATUS: SATISFIED | NOT_APPLICABLE
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

Existing history is never rewritten. New requirements apply at the next material leg/successor endpoint.
