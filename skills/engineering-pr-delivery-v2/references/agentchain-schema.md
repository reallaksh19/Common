# Agent Chain Schema

## Canonical repository layout

For new chains use:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-answer.md
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-verdict.md
```

Optional/legacy navigation surface:

```text
agents/agentchain.md
```

`ACTIVE.md` is authoritative current state for exactly one chain. Endpoint files are immutable durable baton records. `agents/agentchain.md` is a derived/compatibility dashboard and must not be required for every endpoint advance.

This eliminates cross-chain relay conflicts when WRC, LAFEA, LoadCalc, or other independent workstreams advance concurrently.

## Endpoint identity

The endpoint key is:

```text
(CHAIN_ID, ENDPOINT_ID)
```

Endpoint IDs are chain-local. Therefore all of these are valid simultaneously:

```text
ADV-WRC-1389/EP-0001
ADV-LAFEA-1422/EP-0001
ADV-LOADCALC-1505/EP-0001
```

Within one chain, an endpoint ID may appear only once.

`PREVIOUS_ENDPOINT` is also chain-local:

- first endpoint: `NONE — chain start`;
- later endpoint: immediately preceding endpoint in the same chain;
- no cross-chain predecessor;
- no skipping a newer same-chain endpoint;
- two direct successors from one prior endpoint are a custody divergence requiring reconciliation.

## ACTIVE.md schema

```text
CHAIN_STATE_VERSION: 1
CHAIN_ID:
MISSION:
ACTIVE_ENDPOINT:
ACTIVE_ENDPOINT_FILE:
PR:
BRANCH:
HEAD:
STATE:
AUTHORITY_DOMAIN:
ACTIVE_CUSTODIAN:
CUSTODY_EPOCH:
COORDINATION_STATE:
DEPENDENCIES:
```

Canonical endpoint locator:

```text
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
```

Rules:

- directory name equals `CHAIN_ID`;
- `ACTIVE_ENDPOINT` resolves within that chain's `endpoints/` directory;
- `HEAD` matches the active endpoint `CHECKPOINT_HEAD`;
- `STATE` matches the active endpoint `STATE`;
- `CUSTODY_EPOCH` matches the active endpoint epoch;
- `ACTIVE_CUSTODIAN` is explicit;
- `COORDINATION_STATE` is one of `SAFE`, `COORDINATION_REQUIRED`, `BLOCKED_BY_ACTIVE_CHAIN`, `UNKNOWN`, `NOT_APPLICABLE`;
- terminal `COMPLETE` / `SUPERSEDED` chains may retain `ACTIVE.md`, but are excluded from active dashboards.

## Custody epoch

Every canonical endpoint contains:

```text
CUSTODY_EPOCH: <positive integer>
```

The root endpoint uses `1`. Every direct successor increments exactly by one.

When advancing `ACTIVE.md`, use the exact repository version/blob that was read. If the write conflicts or the epoch changed, do not force the update. Re-ground the chain and reconcile competing work.

See `chain-concurrency.md`.

## Detailed endpoint file

Default path:

```text
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
```

Mandatory body:

```text
# <ENDPOINT_ID> — <short endpoint title>

CHAIN_ID:
LEG_ID:
ENDPOINT_ID:
PREVIOUS_ENDPOINT:
CUSTODY_EPOCH:

CREATED_AT:
ENDPOINT_REASON:

TASK / ISSUE:
PR:
BRANCH:

CHECKPOINT_HEAD:
MAIN_HEAD_OBSERVED:
MERGE_BASE:

STATE:

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
QUESTION_SET_STATUS: CURRENT | STALE | NOT_REQUIRED

#### Q1 — Production Trace
#### Q2 — Current Unresolved Problem / Failure Isolation
#### Q3 — Authority / Invariant
#### Q4 — Independent Validation
#### Q5 — Next Contribution / Minimal Patch
```

## Endpoint reason values

Recommended:

```text
CHAIN_START
NORMAL_CHECKPOINT
PRE_MUTATION
POST_MUTATION
VALIDATION
BLOCKER_CHANGE
AGENT_STOP
AGENT_LOST_RECOVERY
PR_TRANSITION
LEGACY_TO_RELAY_MIGRATION
READY_FOR_NEXT_LEG
TASK_COMPLETE
SUPERSESSION
```

## State values

```text
ACTIVE
QUALIFICATION_REQUIRED
RECOVERY_REQUIRED
BLOCKED
READY_FOR_NEXT_LEG
COMPLETE
SUPERSEDED
```

## Exact next action

Every non-terminal endpoint must contain one executable next action.

Bad:

```text
Continue implementation.
Review and proceed.
```

Good:

```text
Trace transformLoadsToWrcFrame() from the canonical global load object into the six WRC local components and independently reproduce the frozen gamma=5 case before modifying production.
```

## Mandatory source/reference inventories

Every endpoint contains:

```text
Inputs
Benchmarks
Common / governing documents
Authoritative sources
Production paths
Validation / test paths
```

If genuinely absent, record `NONE — <reason>` rather than omitting it.

## Append-only endpoint rule

Once a detailed endpoint is durable, do not rewrite its technical assertions to make history cleaner. Correct by adding a later endpoint with explicit supersession/reconciliation evidence.

`ACTIVE.md` is the only routinely mutable relay file for that chain.

## Crash windows

### Endpoint written, ACTIVE.md not advanced

The new endpoint is an orphan durable artifact. Do not delete it silently. Re-ground, classify, then either advance `ACTIVE.md` or supersede/reconcile explicitly.

### ACTIVE.md stale write

If another agent advanced the chain first, Git/version checks or `CUSTODY_EPOCH` mismatch must fail closed. Re-ground rather than force-pushing a stale pointer.

## Completion

A terminal endpoint uses:

```text
STATE: COMPLETE
NEXT_AGENT_QUALIFICATION: NOT_REQUIRED
QUESTION_SET_STATUS: NOT_REQUIRED
COMPLETION_BASIS:
```

`ACTIVE.md` may remain as the terminal current-state record. Derived dashboards omit terminal chains automatically.

## Legacy format compatibility

Existing repositories may contain:

```text
agents/agentchain.md
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

Those artifacts remain valid historical/recovery evidence. Do not mass-rewrite them.

Legacy-format chains may finish under the legacy validator or deliberately migrate at a new endpoint. New chains should use `agents/chains/**`.

Use:

```text
validate_agentchain.py      legacy shared-index format
validate_chain_store.py     canonical chain-local format
```
