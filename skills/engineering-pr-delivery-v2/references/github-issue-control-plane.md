# GitHub-Issue Control Plane — durable multi-agent handover for issue-based work

## 1. Scope

This reference applies only when:

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE
WORK_ITEM_KEY: github:<owner>/<repo>#<issue-number>
```

For `REPOSITORY_TASK` or `OWNER_DIRECT`, repository custody (`agents/chains/**`, endpoints, material receipts, qualifications) remains sufficient; do not manufacture GitHub-Issue comments or an Issue Basis.

Repository artifacts remain the machine-verifiable authority. GitHub Issue comments are the synchronized human-visible control plane/navigation surface. A comment must never silently become engineering/source/roadmap/oracle authority merely because it is easier to read.

## 2. Authority stack

```text
explicit current Owner instruction
→ applicable Owner Roadmap(s)
→ immutable Issue Basis
→ mutable repository Issue Current State
→ active engineering chain / endpoints / receipts
→ PR / validation / release state
→ synchronized Issue comments as projection/navigation
```

An issue assignment does not grant roadmap mutation authority. Agent execution plans are not Owner Roadmaps.

Roadmap classes:

```text
OWNER_ROADMAP        Owner-controlled strategic/architectural authority
PROJECT_ROADMAP      repository roadmap; declare OWNER_CONTROLLED or MAINTAINER_CONTROLLED
ISSUE_EXECUTION_PLAN agent-maintained bounded plan inside issue/roadmap authority
ROADMAP_PROPOSAL     recommendation only until Owner-authorized
```

## 3. Immutable Issue Basis

At chain creation, capture the issue into:

```text
agents/chains/<CHAIN_ID>/issue-basis/<ISSUE_BASIS_ID>.md
```

Required header:

```text
ISSUE_BASIS_ID:
WORK_ITEM_KEY:
ISSUE_SOURCE:
ISSUE_SOURCE_SNAPSHOT_AT:
PREVIOUS_ISSUE_BASIS: NONE | <id>
CHANGE_AUTHORITY: INITIAL_CAPTURE | OWNER:<comment/locator>
ISSUE_BASIS_STATUS: CURRENT | SUPERSEDED
```

The basis preserves, item by item:

```text
### Original task / acceptance ledger
TASK-001 | <Owner requirement> | OPEN | <source locator>

### Input ledger
INPUT-001 | <input> | AVAILABLE | UNRESOLVED | NOT_APPLICABLE | <source/evidence>

### Benchmark / oracle ledger
BM-001 | <benchmark> | READY | PASS | FAIL | NOT_RUN | NOT_APPLICABLE | <authority/evidence>

### Roadmap ledger
RM-001 | <path/locator>@<blob/revision> | OWNER_ROADMAP | PRIMARY | ALIGNED | <authority>

### Owner qualification baseline
<question/challenge source + immutable baseline manifest locator>
```

The Issue Basis is immutable. If the Owner changes the task, create a new basis revision:

```text
IB-0001
→ Owner change
→ IB-0002
```

Never edit IB-0001 to make history look as though the new requirement always existed.

## 4. Mutable Issue Current State — cumulative no-dilution ledger

Do not require Agent 5 or Agent 10 to replay all endpoint deltas just to know current task/input/benchmark/roadmap state.

Maintain one repository-authoritative materialized current-state file:

```text
agents/chains/<CHAIN_ID>/issue-state/CURRENT.md
```

`ACTIVE.md` records:

```text
ISSUE_CURRENT_STATE_FILE: agents/chains/<CHAIN_ID>/issue-state/CURRENT.md
ISSUE_CURRENT_STATE_BASIS: <ISSUE_BASIS_ID>
ISSUE_CURRENT_STATE_ENDPOINT: <EP-ID>
```

`CURRENT.md` repeats the four protected ledgers item-by-item with current status/evidence:

```text
### Original task / acceptance ledger
### Input ledger
### Benchmark / oracle ledger
### Roadmap ledger
```

and the current Owner qualification baseline locator/status.

Rules:

1. Stable row IDs from the current Issue Basis cannot be silently deleted, renamed, merged or replaced.
2. Status may change only with a durable evidence locator or explicit Owner disposition.
3. Aggregate counts may summarize but never replace item-level rows.
4. `PASS`, `FAIL`, `NOT_RUN` and `NOT_APPLICABLE` remain distinct.
5. Newly discovered rows may be appended only with provenance and discovery endpoint.
6. A successor Issue Basis explicitly maps retained/added/removed Owner-authorized rows.
7. Every accepted endpoint updates `CURRENT.md` before the Issue Active Handover comment is synchronized.

The mutable `CURRENT.md` is current-state authority; immutable Issue Basis + endpoint history prove how it evolved.

## 5. Three GitHub Issue comment roles

### A. Immutable Chain Root comment — once per chain

Marker:

```text
<!-- ENG-PR-V2:CHAIN_ROOT
WORK_ITEM_KEY=github:owner/repo#123
CHAIN_ID=<CHAIN_ID>
ISSUE_BASIS_ID=<IB-ID>
-->
```

Contains:

- issue, chain and mode;
- Issue Basis and Issue Current State locators;
- original task/input/benchmark/roadmap baseline summaries;
- Owner qualification baseline status;
- initial endpoint;
- Active Handover comment ID.

Never edit it after publication.

### B. One mutable Active Handover comment — exactly one per non-terminal chain

Marker:

```text
<!-- ENG-PR-V2:ACTIVE
WORK_ITEM_KEY=github:owner/repo#123
CHAIN_ID=<CHAIN_ID>
-->
```

It is updated after every accepted endpoint and is the first issue comment a replacement agent should locate.

It projects the current repository `issue-state/CURRENT.md`, not a hand-written memory summary.

It must show current cumulative state:

```text
Repo / issue / chain / endpoint
PR / branch / head / main
PR status / mergeability / reviews / unresolved threads / required checks
merge authority / merge authorized
engineering / custody / qualification / write / AUTO
Issue Basis + current-state locator/status
Owner Roadmap(s) + bound revision/blob + alignment + mutation authority
other governing roadmaps + class + status
roadmap proposals / Owner decisions
original-task ledger summary + every OPEN/PARTIAL/BLOCKED row
input ledger summary + every UNRESOLVED/MISSING row
benchmark/oracle summary + every FAIL/NOT_RUN/BLOCKED row
qualification scope / question-set status / takeover-qualification readiness
current blocker / leg diagnosis / exact next action
endpoint history links
latest endpoint checkpoint comment ID
```

### C. Immutable Endpoint Checkpoint comment — one per accepted endpoint

Marker:

```text
<!-- ENG-PR-V2:ENDPOINT
CHAIN_ID=<CHAIN_ID>
ENDPOINT_ID=<EP-ID>
-->
```

Contains:

```text
Agent instance
Endpoint / predecessor endpoint
Previous Issue endpoint comment ID
PR head / main observed
Issue Basis ID + Issue Current State endpoint
Owner-roadmap bindings/drift
Original-task status changes
Input status changes
Benchmark/oracle status changes
Validation truth
Qualification scope / question-set action
Exact next action
```

For `proceed next, hand over ready`, it also contains the complete current Q1-Q5 and takeover-ready state.

Endpoint comments are append-only history. Do not edit old checkpoints to correct later understanding; publish a successor correction.

## 6. Repository↔Issue synchronization fields

Issue-based `ACTIVE.md` adds:

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE
ISSUE_BASIS_ID:
ISSUE_BASIS_FILE:
ISSUE_BASIS_STATUS: CURRENT
ISSUE_CURRENT_STATE_FILE:
ISSUE_CURRENT_STATE_BASIS:
ISSUE_CURRENT_STATE_ENDPOINT:
ISSUE_CHAIN_ROOT_COMMENT_ID:
ISSUE_ACTIVE_HANDOVER_COMMENT_ID:
ISSUE_LATEST_ENDPOINT_COMMENT_ID:
ISSUE_HANDOVER_SYNC_STATUS: IN_SYNC | STALE | NOT_RUN | FAILED
```

Each accepted issue-based endpoint records:

```text
ISSUE_ENDPOINT_COMMENT_ID:
PREVIOUS_ISSUE_ENDPOINT_COMMENT_ID:
```

The repository file paths/IDs are authoritative custody. Comment IDs provide bidirectional navigation and prove the human-visible projection was published.

## 7. Synchronization gate

For `WORK_ITEM_SOURCE: GITHUB_ISSUE`:

```text
accepted repository endpoint
→ update issue-state/CURRENT.md
→ immutable endpoint checkpoint comment published
→ mutable Active Handover comment updated from CURRENT.md
→ repository comment IDs recorded
→ ISSUE_HANDOVER_SYNC_STATUS = IN_SYNC
→ only then start another material progression
```

If Issue synchronization fails:

```text
preserve current material work and repository baton
ISSUE_HANDOVER_SYNC_STATUS = FAILED | STALE | NOT_RUN
CHAIN_HANDOVER_READY may remain TRUE only for repository custody
AUTO = BLOCKED before another material progression
```

Do not convert a connector/network failure into `IN_SYNC`.

## 8. Roadmap custody and drift

The Issue Basis pins every applicable roadmap by path/locator and immutable revision/blob where available. `CURRENT.md` carries the live classified status.

The Active Handover shows both the basis binding and current binding when they differ:

```text
Issue-basis roadmap: Overallroadmap_lafea.md@abc...
Current roadmap:     Overallroadmap_lafea.md@def...
Roadmap drift: STATUS_ONLY_DRIFT | OWNER_INTENT_DRIFT | ...
Disposition: ...
```

Roadmap drift classes:

```text
NO_DRIFT
STATUS_ONLY_DRIFT
OWNER_INTENT_DRIFT
ROADMAP_REMOVED
NEW_APPLICABLE_ROADMAP
UNKNOWN
```

Consequences:

```text
NO_DRIFT
→ continue

STATUS_ONLY_DRIFT
→ refresh status/proposal; may continue only if Owner intent/task authority is unchanged

OWNER_INTENT_DRIFT | NEW_APPLICABLE_ROADMAP | UNKNOWN
→ READ_ONLY
→ AUTO BLOCKED
→ re-ground / Owner decision

ROADMAP_REMOVED
→ do not silently keep treating removed roadmap as current authority
```

## 9. Five-agent takeover path

A sixth agent should need only:

```text
1. read issue body/current Owner comments
2. locate ENG-PR-V2:ACTIVE
3. resolve ISSUE_BASIS_ID and ISSUE_CURRENT_STATE_FILE
4. read latest endpoint checkpoint
5. verify WORK_ITEM_KEY/exclusive custody
6. inspect older history only where needed
7. admit current question set if takeover qualification is ready
8. qualify
9. reconcile post-basis drift
10. continue Exact Next Action
```

Old chats are never part of required custody.

## 10. Parent/program issue sets for multi-agent work

Complex issue programmes may use one immutable parent/program issue plus bounded child issues. This hierarchy supplements, not replaces, the per-issue custody model above.

### 10.1 Roles

```text
PROGRAM_ROOT    Owner/common-custody contract and partition registry
WORK_PACKAGE    bounded implementation/validation/integration child
REVISION        later material revision of completed/frozen predecessor child
```

The parent program is not a shared multi-writer production chain. Each material child/revision has its own `WORK_ITEM_KEY`, canonical chain and exclusive current agent custody.

### 10.2 Child relay fields

For `WORK_PACKAGE` and `REVISION`, ACTIVE/Issue Basis record:

```text
PROGRAM_ID:
PROGRAM_WORK_ITEM_KEY: github:<owner>/<repo>#<parent>
ISSUE_ROLE: WORK_PACKAGE | REVISION
WORK_PACKAGE_ID: WP-001
PARTITION_KEY: <PROGRAM_ID>/WP-001
PREDECESSOR_WORK_ITEM_KEY: NONE | github:<owner>/<repo>#<predecessor>
REVISION_SEQUENCE: 0 | 1 | 2 ...
INHERITED_PROGRAM_BASIS_REVISION:
INHERITED_INPUT_SET_ID:
INHERITED_BENCHMARK_SET_ID:
INHERITED_VALIDATION_SET_ID:
INHERITED_ROADMAP_SET_ID:
PARENT_TASK_ROWS:
USES_INPUT_ROWS:
USES_BENCHMARK_ROWS:
USES_VALIDATION_ROWS:
```

These are custody fields, not descriptive prose.

### 10.3 Parent/common authority inheritance

The child must resolve the current parent program basis before material write authority. Parent common rows are inherited by stable ID and cannot be silently redefined by a child.

If any inherited program basis/set ID differs from the parent's current authorized basis:

```text
PROGRAM_BASIS_DRIFT
→ WRITE_AUTHORITY: READ_ONLY
→ AUTO: BLOCKED
→ reconcile parent change / create successor child basis
```

A child may add child-specific local rows, but changing the meaning/tolerance/authority of a parent `INPUT-*`, `BM-*`, `VAL-*`, `RM-*` or allocated `TASK-*` row requires a parent program-basis revision.

### 10.4 Partition/overlap gate

Before WRITE_ALLOWED for a child, reconcile the parent's active work-package registry and open sibling PR/chain claims.

Check:

```text
PARTITION_KEY
owned authority domains
expected changed paths/components
protected sibling domains
dependency predecessors
active sibling PR/chain state
```

Classify:

```text
SAFE_DISJOINT
SAFE_SERIALIZED
COORDINATION_REQUIRED
BLOCKED_ACTIVE_SIBLING
UNKNOWN
```

Consequences:

```text
SAFE_DISJOINT
→ may proceed if all other gates pass

SAFE_SERIALIZED
→ may proceed only after predecessor terminal/frozen evidence

COORDINATION_REQUIRED
→ READ_ONLY until durable coordination/partition decision

BLOCKED_ACTIVE_SIBLING | UNKNOWN
→ WRITE_AUTHORITY: READ_ONLY
→ AUTO: BLOCKED
```

Read overlap on common source/benchmark files does not itself create write collision. Shared writes require explicit serialization/integration ownership.

### 10.5 Takeover versus revision

Agent replacement on an unfinished child does **not** create a new GitHub issue:

```text
same child WORK_ITEM_KEY
same canonical chain
new AGENT_INSTANCE_ID
qualification-first takeover
```

A new `REVISION` child/new chain is required when a later agent materially revises completed/frozen predecessor work or when the Owner explicitly requires a separately reviewable revision package.

For `REVISION`:

```text
PREDECESSOR_WORK_ITEM_KEY != NONE
REVISION_SEQUENCE > 0
same PARTITION_KEY by default
predecessor must be terminal/frozen unless Owner explicitly authorizes concurrent partitioned repair
```

### 10.6 Parent program status projection

The parent issue body/basis preserves the original Owner/common contract. Operational child status is projected through a mutable program-status comment or repository program-state artifact containing:

```text
WP/revision ID
child issue
status
chain/endpoint
PR / mergeability / checks
agent/custody state
dependency state
overlap disposition
common-set drift status
latest evidence / exact next action
```

Do not rewrite the parent Owner contract on every child update.

### 10.7 Program closure

Parent program completion requires reconciliation of all required child/revision evidence. A merged child PR does not by itself close the parent programme, and a child may not promote sibling/parent `NOT_RUN` evidence to PASS.
