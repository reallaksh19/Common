# Repo-wide Agent Chain Schema

## Repository layout

```text
agents/agentchain.md
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

`agents/agentchain.md` is the compact repository-wide traffic/index log.

Detailed endpoint files are immutable durable baton records. They contain the engineering state, source custody, next action, and five questions.

This split avoids making one ever-growing Markdown file a multi-agent write hotspot.

## Compact index

Start with:

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

### ACTIVE CHAINS rules

- one row for every non-terminal chain;
- no row for a terminal `COMPLETE` or `SUPERSEDED` chain;
- `Latest endpoint` must be the actual latest endpoint logged for that chain;
- `Endpoint file` must resolve to that endpoint's current repository file;
- row `State` must match the detailed endpoint `STATE`;
- an active row may not use a historical legacy blob locator.

### ENDPOINT LOG rules

The endpoint log is append-only after a row is durable.

Normal locator:

```text
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

For controlled migration of endpoints that existed before the split architecture, a historical row may use:

```text
git-blob:<40-hex-blob-sha>#<ENDPOINT_ID>
```

A legacy blob locator is historical custody only. It must never be the active endpoint of a non-terminal chain.

## Endpoint identifiers and lineage

Use repository-unique endpoint IDs, for example:

```text
EP-0001
EP-0002
```

or chain-prefixed forms where useful.

`PREVIOUS_ENDPOINT` is chain-local:

- the first endpoint of a chain uses `NONE — chain start` or equivalent;
- every later endpoint points to the immediately preceding/latest endpoint for the same `CHAIN_ID`;
- it may not skip a newer endpoint;
- it may not point into another chain.

## Detailed endpoint file

Default path:

```text
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

Mandatory body:

```text
# <ENDPOINT_ID> — <short endpoint title>

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

Repositories may extend the vocabulary but should prefer precise reasons over `UPDATE`.

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
Trace `transformLoadsToWrcFrame()` from the canonical global load object into the six WRC local components and independently reproduce the frozen gamma=5 case before modifying production.
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

Do not silently omit an inventory. If genuinely absent, state for example:

```text
NONE — no independent benchmark exists yet; creating one is part of the next leg.
```

## Append-only endpoint rule

Once a detailed endpoint file is durable, do not rewrite its technical assertions to make history cleaner.

Correct by creating a later endpoint with explicit fields such as:

```text
SUPERSEDES_ENDPOINT:
SUPERSEDED_ASSERTION:
CORRECTED_STATE:
EVIDENCE:
```

Only the compact current `ACTIVE CHAINS` row is routinely replaced as custody advances. The endpoint log gains a new row rather than rewriting old rows.

## Crash between endpoint and index update

Because endpoint creation and index update are separate repository writes, a crash may leave a detailed endpoint file that is not yet logged.

Treat this as an orphan durable endpoint:

1. do not delete it silently;
2. re-ground it against live repository state;
3. classify it as valid/recoverable/untrusted;
4. repair the index with recovery provenance or supersede it explicitly.

The validator should detect unlogged endpoint files so the condition cannot remain silent.

## Completion endpoint

A terminal `COMPLETE` endpoint replaces the five questions with:

```text
NEXT_AGENT_QUALIFICATION: NOT_REQUIRED
QUESTION_SET_STATUS: NOT_REQUIRED
COMPLETION_BASIS:
```

Remove the chain from `ACTIVE CHAINS`; retain its `ENDPOINT LOG` row.

A PR merge alone is not a completion basis.
