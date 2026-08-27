# Agent Chain Templates

## 1. Repo-wide compact index — `agents/agentchain.md`

```text
# Engineering Agent Chain

AGENTCHAIN_VERSION: 2

## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | Endpoint file | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|---|

## ENDPOINT LOG

| Endpoint | Chain | Leg | Checkpoint head | State | Locator |
|---|---|---|---|---|---|
```

For a live chain, add one `ACTIVE CHAINS` row and one append-only `ENDPOINT LOG` row per endpoint.

## 2. Detailed endpoint — `agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md`

```text
# EP-0001 — <short endpoint title>

CHAIN_ID:
LEG_ID:
ENDPOINT_ID: EP-0001
PREVIOUS_ENDPOINT: NONE — chain start

CREATED_AT:
ENDPOINT_REASON: CHAIN_START

TASK / ISSUE:
PR:
BRANCH:

CHECKPOINT_HEAD:
MAIN_HEAD_OBSERVED:
MERGE_BASE:

STATE: QUALIFICATION_REQUIRED

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

QUALIFICATION_BASIS_HEAD:
QUESTION_SET_ID:
QUESTION_SET_STATUS: CURRENT

#### Q1 — Production Trace

Repository anchors:
Required evidence:
Falsifier / decisive observation:

#### Q2 — Current Unresolved Problem / Failure Isolation

Repository anchors:
Prediction:
Required evidence:
Falsifier:

#### Q3 — Authority / Invariant

Repository anchors:
Required authority trace:
Protected invariant:
Invalid shortcut to reject:

#### Q4 — Independent Validation

Repository anchors:
Independent oracle/reference required:
Units/sign/tolerance requirements:
Required evidence:

#### Q5 — Next Contribution / Minimal Patch

Repository anchors:
Smallest legitimate change:
Expected changed files/domains:
Protected unchanged files/domains:
Validation required:
Rollback/falsifier boundary:
```

## 3. Example index rows

```text
## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | Endpoint file | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|---|
| EXAMPLE-1 | Close example engineering discrepancy | EP-0002 | agents/agentchain/EXAMPLE-1/EP-0002.md | #42 | QUALIFICATION_REQUIRED | example authority | Incoming agent answers EP-0002 Q1-Q5 before mutation |

## ENDPOINT LOG

| Endpoint | Chain | Leg | Checkpoint head | State | Locator |
|---|---|---|---|---|---|
| EP-0001 | EXAMPLE-1 | LEG-001 | abc123 | QUALIFICATION_REQUIRED | agents/agentchain/EXAMPLE-1/EP-0001.md |
| EP-0002 | EXAMPLE-1 | LEG-001 | def456 | QUALIFICATION_REQUIRED | agents/agentchain/EXAMPLE-1/EP-0002.md |
```

For a migrated historical endpoint that predates split endpoint files:

```text
| EP-0001 | LEGACY-CHAIN | LEG-001 | abc123 | QUALIFICATION_REQUIRED | git-blob:<40hex>#EP-0001 |
```

Historical blob locators may appear only in `ENDPOINT LOG`, never as the active endpoint file for a non-terminal chain.
