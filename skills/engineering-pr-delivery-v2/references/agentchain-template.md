# Agent Chain Templates — version 3 custody + handover protocol 2

## 1. ACTIVE.md

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
MERGE_AUTHORIZED: FALSE
MERGEABILITY: UNKNOWN
REVIEW_COUNT: 0
UNRESOLVED_REVIEW_THREADS: 0
REQUIRED_CHECKS_STATUS: NONE | PASS | FAIL | NOT_RUN | MIXED
AUTHORITY_DOMAIN: <domain>
ACTIVE_CUSTODIAN: <human-readable agent label>
AGENT_INSTANCE_ID: <agent-class>:<UUID>
WORK_ITEM_SOURCE: GITHUB_ISSUE | REPOSITORY_TASK | OWNER_DIRECT
WORK_ITEM_KEY: <stable identity>
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
WORK_ITEM_PARTITION: NONE | <partition id>
WORK_ITEM_PARTITION_AUTHORITY: NONE | OWNER:<durable locator>
CUSTODY_EPOCH: 1
COORDINATION_STATE: SAFE
DEPENDENCIES: NONE
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <40-hex live Common commit actually read>
COMMON_PROTOCOL_STATUS: CURRENT
ROADMAPS: <path>@<blob-sha> | NONE — <reason>
ROADMAP_REVIEW_STATUS: COMPLETE | NOT_APPLICABLE | BLOCKED
ROADMAP_ALIGNMENT: ALIGNED | STATUS_ONLY_DRIFT | OWNER_INTENT_DRIFT | ROADMAP_REMOVED | NEW_APPLICABLE_ROADMAP | UNKNOWN | NOT_APPLICABLE
ROADMAP_MUTATION_AUTHORITY: NONE | OWNER:<locator>
QUALIFICATION_SCOPE_ID: <scope-id>
QUESTION_SET_ID: <id | NONE>
QUESTION_SET_STATUS: CURRENT | STALE | NOT_APPLICABLE
QUESTION_PACK_ACTION: REUSED | REFRESHED | SUPPRESSED_BY_OWNER | NOT_APPLICABLE
QUESTION_DISPLAY: SHOW | HIDE
OWNER_PROGRESSION_COMMAND: PROCEED_NEXT | PROCEED_NEXT_NO_QS | PROCEED_NEXT_HANDOVER_READY
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE: <durable evidence or NONE>
CHAIN_HANDOVER_READY: TRUE | FALSE
TAKEOVER_QUALIFICATION_READY: TRUE | FALSE
HANDOVER_READY: TRUE | FALSE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE: NONE | <owner locator>
OWNER_QUALIFICATION_BASELINE_MANIFEST: NONE | <repo-relative JSON path>
OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE | SATISFIED | BLOCKED
```

### Additional ACTIVE.md fields for GitHub-Issue work

Only when `WORK_ITEM_SOURCE: GITHUB_ISSUE`:

```text
WORK_ITEM_KEY: github:<owner>/<repo>#<issue>
ISSUE_BASIS_ID:
ISSUE_BASIS_FILE: agents/chains/<CHAIN_ID>/issue-basis/<IB>.md
ISSUE_BASIS_STATUS: CURRENT
ISSUE_CURRENT_STATE_FILE: agents/chains/<CHAIN_ID>/issue-state/CURRENT.md
ISSUE_CURRENT_STATE_BASIS: <IB>
ISSUE_CURRENT_STATE_ENDPOINT: <EP>
ISSUE_CHAIN_ROOT_COMMENT_ID:
ISSUE_ACTIVE_HANDOVER_COMMENT_ID:
ISSUE_LATEST_ENDPOINT_COMMENT_ID:
ISSUE_HANDOVER_SYNC_STATUS: IN_SYNC | STALE | NOT_RUN | FAILED
```

For `REPOSITORY_TASK` or `OWNER_DIRECT`, omit the Issue-only fields.

## 2. Non-terminal endpoint

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
WORK_ITEM_SOURCE:
WORK_ITEM_KEY:
WORK_ITEM_MODE:
AGENT_INSTANCE_ID:
OWNER_PROGRESSION_COMMAND:
QUALIFICATION_SCOPE_ID:
QUESTION_SET_ID:
QUESTION_SET_STATUS:
QUESTION_PACK_ACTION:
QUESTION_DISPLAY:
CHAIN_HANDOVER_READY:
TAKEOVER_QUALIFICATION_READY:
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE:
OWNER_QUALIFICATION_BASELINE_MANIFEST:
OWNER_QUALIFICATION_BASELINE_STATUS:
ROADMAPS:
ROADMAP_REVIEW_STATUS:
ROADMAP_ALIGNMENT:
ROADMAP_MUTATION_AUTHORITY:
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY:
HANDOVER_VALIDATION_STATUS:
HANDOVER_VALIDATION_EVIDENCE:
HANDOVER_READY:
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
TASK / ISSUE:
PR:
PR_STATUS:
MERGEABILITY:
REVIEW_COUNT:
UNRESOLVED_REVIEW_THREADS:
REQUIRED_CHECKS_STATUS:
MERGE_AUTHORITY:
MERGE_AUTHORIZED:
BRANCH:
CHECKPOINT_HEAD:
QUALIFICATION_BASIS_HEAD:
MAIN_HEAD_OBSERVED:
MERGE_BASE:
STATE:
ENGINEERING_STATE:
CUSTODY_STATE:
QUALIFICATION_STATE:
WRITE_AUTHORITY:
AUTO_STATE:
```

For GitHub-Issue work also record:

```text
ISSUE_BASIS_ID:
ISSUE_BASIS_FILE:
ISSUE_BASIS_STATUS:
ISSUE_CURRENT_STATE_FILE:
ISSUE_CURRENT_STATE_BASIS:
ISSUE_CURRENT_STATE_ENDPOINT:
ISSUE_ENDPOINT_COMMENT_ID:
PREVIOUS_ISSUE_ENDPOINT_COMMENT_ID:
ISSUE_HANDOVER_SYNC_STATUS:
```

### Active handover snapshot

```text
Repo:
Task:
Chain:
Endpoint:
PR:
PR status:
Branch / PR head / main:
Mergeability:
Reviews:
Unresolved review threads:
Required checks:
Merge authority:
Merge authorized:
Engineering / custody / qualification / write state:
AUTO:
Protocol basis / status:
Work item / source:
Issue basis: <id/status | NOT_APPLICABLE>
Owner roadmap(s):
Other governing roadmaps:
Roadmap alignment / drift:
Roadmap mutation authority:
Original task status:
Inputs:
Benchmarks / oracles:
Qualification:
Scope:
Question set:
Question status:
Question action:
Takeover qualification ready:
Chain handover ready:
Current blocker:
Leg diagnosis:
Exact next action:
```

### Active qualification questions

Durable endpoint storage retains the current pack even when user-facing `QUESTION_DISPLAY: HIDE`; reuse means preserve the existing pack unchanged, not regenerate it.

```text
Q1: <full current prompt>
Q2: <full current prompt>
Q3: <full current prompt>
Q4: <full current prompt>
Q5: <full current prompt>
```

### Required narrative/evidence sections

```text
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
### Takeover qualification pack
```

## 3. Takeover qualification pack

```text
PURPOSE: QUALIFICATION_ONLY
NOT_AN_IMPLEMENTATION_TASK: TRUE
QUALIFICATION_PROTOCOL_VERSION: 3
QUALIFICATION_PROFILE: <same profile as endpoint>
QUALIFICATION_PROFILE_VERSION: 2
QUALIFICATION_BASIS_HEAD:
QUALIFICATION_SCOPE_ID:
QUESTION_SET_ID:
QUESTION_SET_STATUS: CURRENT | STALE
QUESTION_SET_AUTHOR:
QUESTION_SET_ADMISSION_REQUIREMENT: REQUIRED_ON_TAKEOVER
OWNER_QUALIFICATION_BASELINE_SOURCE:
OWNER_QUALIFICATION_BASELINE_MANIFEST:
OWNER_QUALIFICATION_BASELINE_STATUS:
```

Keep the detailed Q1-Q5 schema from `qualification.md` / `qualification-profiles.md`: repository anchors, concrete payload, required derivation, independent oracle/falsifier and Q5 safe-patch/rollback/NO-PATCH fields.

## 4. Issue Basis

```text
# agents/chains/<CHAIN_ID>/issue-basis/<IB-ID>.md
ISSUE_BASIS_ID:
WORK_ITEM_KEY:
ISSUE_SOURCE:
ISSUE_SOURCE_SNAPSHOT_AT:
PREVIOUS_ISSUE_BASIS:
CHANGE_AUTHORITY:
ISSUE_BASIS_STATUS:

### Original task / acceptance ledger
TASK-001 | ...

### Input ledger
INPUT-001 | ...

### Benchmark / oracle ledger
BM-001 | ...

### Roadmap ledger
RM-001 | ...

### Owner qualification baseline
...
```

## 5. Issue Current State

```text
# agents/chains/<CHAIN_ID>/issue-state/CURRENT.md
ISSUE_BASIS_ID:
CURRENT_ENDPOINT:
UPDATED_AT_HEAD:

### Original task / acceptance ledger
### Input ledger
### Benchmark / oracle ledger
### Roadmap ledger
### Owner qualification baseline
```

Stable row IDs from the Issue Basis cannot disappear without explicit Owner-authorized basis revision.

## 6. Material-leg completion receipt

```text
CHAIN_ID:
MATERIAL_LEG_ID:
PREVIOUS_MATERIAL_LEG:
MATERIAL_LEG_BASE:
MATERIAL_LEG_PREWORK_ENDPOINT_FILE:
MATERIAL_LEG_HEAD:
MATERIAL_LEG_HISTORY_STATUS: RECORDED
MATERIAL_SCOPE:
```

## 7. Command-specific response behavior

The user-visible response always starts with the State Card.

```text
proceed next
→ hide unchanged Qs; show full Q1-Q5 only if refreshed

proceed next, no Qs
→ do not create/refresh/display Qs

proceed next, hand over ready
→ ensure current Q-set; show full Q1-Q5; synchronize Issue control plane when applicable
```

See `owner-progression-commands.md`.

## 8. Historical compatibility

Existing endpoints remain immutable. New fields apply at the next accepted successor endpoint. Non-issue chains do not gain Issue-only requirements.