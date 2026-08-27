# Repo-wide Agent Chain Schema

## Primary file

```text
agents/agentchain.md
```

This file is the repository-wide relay index and append-only endpoint ledger.

It is not a replacement for engineering evidence. It points to that evidence.

## Header

Start with:

```text
# Engineering Agent Chain

AGENTCHAIN_VERSION: 2

## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|
```

Only the compact `ACTIVE CHAINS` table is mutable summary state. Endpoint records below it are append-only after creation.

## Endpoint identifiers

Use repository-unique endpoint IDs. Recommended forms:

```text
EP-0001
EP-0002
```

or chain-prefixed forms where the repository benefits from them.

Every endpoint references `PREVIOUS_ENDPOINT` except the first endpoint of a chain.

## Mandatory endpoint schema

```text
## <ENDPOINT_ID>

CHAIN_ID:
LEG_ID:
ENDPOINT_ID:
PREVIOUS_ENDPOINT:

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

Recommended values:

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

Repositories may extend this vocabulary but must not use ambiguous reasons such as `UPDATE` when a more specific state applies.

## State values

Recommended:

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

A non-terminal endpoint must contain one executable next action.

Bad:

```text
Continue implementation.
Finish remaining work.
Review and proceed.
```

Good:

```text
Trace `transformLoadsToWrcFrame()` from the canonical global load object into the six WRC local components and independently reproduce the frozen gamma=5 case before modifying production.
```

## Empty sections

Do not silently omit mandatory inventories.

Use:

```text
NONE — no independent benchmark exists yet; creating one is part of the next leg.
```

or equivalent explicit reasoning.

## Append-only rule

After an endpoint is durable, do not rewrite its technical assertions to make history look cleaner.

A correction is a new endpoint with:

```text
SUPERSEDES_ENDPOINT:
SUPERSEDED_ASSERTION:
CORRECTED_STATE:
EVIDENCE:
```

The active-chain summary row may be updated to the newest endpoint.

## Completion endpoint

A terminal chain endpoint must replace the five questions with:

```text
NEXT_AGENT_QUALIFICATION: NOT_REQUIRED
QUESTION_SET_STATUS: NOT_REQUIRED
COMPLETION_BASIS:
```

Do not use this merely because a PR merged.
