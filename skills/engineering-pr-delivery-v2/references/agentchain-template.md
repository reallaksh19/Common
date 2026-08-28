# Agent Chain Templates — version 3 qualification-first

## 1. ACTIVE.md

```text
CHAIN_STATE_VERSION: 3
CHAIN_ID: <CHAIN_ID>
MISSION: <one-line mission>
ACTIVE_ENDPOINT: EP-0001
ACTIVE_ENDPOINT_FILE: agents/chains/<CHAIN_ID>/endpoints/EP-0001.md
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
ROADMAPS: <path>@<blob-sha> | NONE — <reason>
ROADMAP_REVIEW_STATUS: COMPLETE | NOT_APPLICABLE | BLOCKED
HANDOVER_READY: TRUE
```

## 2. Non-terminal endpoint

```text
# EP-0001 — <title>
CHAIN_ID: <CHAIN_ID>
LEG_ID: LEG-001
ENDPOINT_ID: EP-0001
PREVIOUS_ENDPOINT: NONE — chain start
CUSTODY_EPOCH: 1
ROADMAPS: <binding>
ROADMAP_REVIEW_STATUS: <status>
HANDOVER_READY: TRUE
CREATED_AT:
ENDPOINT_REASON: CHAIN_START
TASK / ISSUE:
PR:
BRANCH:
CHECKPOINT_HEAD:
MAIN_HEAD_OBSERVED:
MERGE_BASE:
STATE: ACTIVE
ENGINEERING_STATE:
CUSTODY_STATE:
QUALIFICATION_STATE:
WRITE_AUTHORITY:
AUTO_STATE:
MERGE_AUTHORITY:

### Handover snapshot
Repo: <repo>
Task: <task>
Chain: <CHAIN_ID>
Endpoint: <EP>
PR: <PR>; PR status: <draft/open/etc>; Branch / PR head / main: <refs>
Merge authority: <state>
Engineering / custody / qualification / write state: <states>
Roadmap: <path@blob or NONE>
Inputs: <key pointers>
Benchmarks: <key pointers>
Governing docs / authoritative sources: <key pointers>
Current blocker: <one line>
Exact next action: <one executable work action>
Q1: <concise production-reconstruction exam prompt>
Q2: <concise calculation/failure-isolation prompt>
Q3: <concise authority/falsifier prompt>
Q4: <concise independent-oracle prompt>
Q5: <concise safe-patch/NO-PATCH prompt>

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
Compatibility locator only. The actual version-3 exam is the Takeover qualification pack below; Q1-Q5 are qualification, never the work baton.

### Takeover qualification pack
PURPOSE: QUALIFICATION_ONLY
NOT_AN_IMPLEMENTATION_TASK: TRUE
QUALIFICATION_PROTOCOL_VERSION: 3
QUALIFICATION_BASIS_HEAD: <sha>
QUESTION_SET_ID: QS-<CHAIN_ID>-0001
QUESTION_SET_STATUS: CURRENT
QUESTION_SET_AUTHOR: <prior-agent/question-authority>

#### Q1 — Production Trace
Repository anchors:
Production object/case:
Required technical work:
Required numerical/technical evidence:
First authority/ownership boundaries:
Fail if:

#### Q2 — Current Unresolved Problem / Failure Isolation
Repository anchors:
Calculation/reconstruction:
Required numerical/technical evidence:
Predicted intermediate values:
First wrong boundary:
Falsifier:
Fail if:

#### Q3 — Authority / Invariant
Repository anchors:
Required technical work:
Authority/source trace:
Protected invariant:
First wrong boundary:
Falsifier:
Invalid shortcut:
Fail if:

#### Q4 — Independent Validation
Repository anchors:
Required technical work:
Independent oracle:
Required numerical/technical evidence:
Units/sign/tolerance:
Falsifier:
Fail if:

#### Q5 — Next Contribution / Minimal Patch
Repository anchors:
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

The handover snapshot is <300 words; detailed exam content is outside that limit. Existing v1/v2 history is never rewritten. A replacement qualifies first on the latest accepted set, then reconciles and migrates to version 3 before material mutation.
