# Agent Chain Templates

## 1. Canonical chain state — `agents/chains/<CHAIN_ID>/ACTIVE.md`

```text
CHAIN_STATE_VERSION: 1
CHAIN_ID: <CHAIN_ID>
MISSION: <one-line mission>
ACTIVE_ENDPOINT: EP-0001
ACTIVE_ENDPOINT_FILE: agents/chains/<CHAIN_ID>/endpoints/EP-0001.md
PR: #<number-or-PENDING>
BRANCH: <branch>
HEAD: <sha>
STATE: QUALIFICATION_REQUIRED
AUTHORITY_DOMAIN: <engineering/software authority domain>
ACTIVE_CUSTODIAN: <agent-id>
CUSTODY_EPOCH: 1
COORDINATION_STATE: SAFE
DEPENDENCIES: NONE
```

Rules:

- one mutable `ACTIVE.md` per chain;
- different chains never edit each other's `ACTIVE.md`;
- advance using exact prior repository blob/version and `CUSTODY_EPOCH + 1`;
- conflict/epoch change = stale write -> re-ground;
- terminal chains may retain `ACTIVE.md` with `COMPLETE`/`SUPERSEDED`.

## 2. Canonical endpoint — `agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md`

```text
# EP-0001 — <short endpoint title>

CHAIN_ID: <CHAIN_ID>
LEG_ID: LEG-001
ENDPOINT_ID: EP-0001
PREVIOUS_ENDPOINT: NONE — chain start
CUSTODY_EPOCH: 1

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
QUESTION_SET_ID: QS-<CHAIN_ID>-0001
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

`EP-0001` may be reused in another chain because the full key is `(CHAIN_ID, ENDPOINT_ID)`.

## 3. Example parallel chains

```text
agents/chains/ADV-WRC-1389/
  ACTIVE.md
  endpoints/EP-0001.md

agents/chains/ADV-LAFEA-1422/
  ACTIVE.md
  endpoints/EP-0001.md

agents/chains/ADV-LOADCALC-1505/
  ACTIVE.md
  endpoints/EP-0001.md
```

This is valid and should not create relay conflicts.

## 4. Derived dashboard

Generate repo-wide navigation with:

```text
python skills/engineering-pr-delivery-v2/scripts/render_agentchain_dashboard.py .
```

The output is derived from `agents/chains/*/ACTIVE.md`. Normal chain advancement does not require committing a shared dashboard update.

## 5. Terminal endpoint

A terminal endpoint uses:

```text
STATE: COMPLETE
NEXT_AGENT_QUALIFICATION: NOT_REQUIRED
QUESTION_SET_STATUS: NOT_REQUIRED
COMPLETION_BASIS: <objective evidence>
```

Update that chain's `ACTIVE.md` to the terminal endpoint/epoch. Derived dashboards omit terminal chains.

## 6. Legacy compatibility

Historical/shared-index repositories may still contain:

```text
agents/agentchain.md
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

Do not mass-rewrite that history. Existing legacy chains may finish there or deliberately migrate. New chains should use `agents/chains/**`.
