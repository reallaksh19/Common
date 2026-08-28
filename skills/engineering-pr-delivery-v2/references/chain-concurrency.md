# Chain-Local Concurrency and Custody

## Purpose

Allow many independent engineering chains to advance in the same repository without creating relay-file conflicts merely because they share one bookkeeping file.

The canonical write authority for a new chain is chain-local:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
```

`agents/agentchain.md` is a derived/compatibility dashboard. It is not the authoritative active pointer for canonical chain-local work and does not need to change at every endpoint.

## Endpoint identity

Endpoint IDs are unique **within a chain**, not across the repository.

Valid:

```text
ADV-WRC-1389/EP-0001
ADV-LAFEA-1422/EP-0001
ADV-LOADCALC-1505/EP-0001
```

Invalid:

```text
ADV-WRC-1389/EP-0003
ADV-WRC-1389/EP-0003
```

The durable endpoint key is:

```text
(CHAIN_ID, ENDPOINT_ID)
```

Question-set IDs should remain visibly namespaced by chain, for example:

```text
QS-ADV-WRC-1389-0003
QS-ADV-LAFEA-1422-0003
```

## ACTIVE.md

`ACTIVE.md` is the single mutable current-state record for one chain.

Required fields:

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

Example:

```text
CHAIN_STATE_VERSION: 1
CHAIN_ID: ADV-WRC-1389
MISSION: Close bounded WRC gamma=5 production qualification
ACTIVE_ENDPOINT: EP-0012
ACTIVE_ENDPOINT_FILE: agents/chains/ADV-WRC-1389/endpoints/EP-0012.md
PR: 1510
BRANCH: emp1-wrc-next-batch
HEAD: <sha>
STATE: ACTIVE
AUTHORITY_DOMAIN: WRC_EMP1
ACTIVE_CUSTODIAN: agent-b
CUSTODY_EPOCH: 12
COORDINATION_STATE: SAFE
DEPENDENCIES: NONE
```

A terminal chain may keep `ACTIVE.md` with `STATE: COMPLETE` or `SUPERSEDED`; discovery tools ignore terminal chains.

## Custody epoch / compare-and-swap rule

Every endpoint in a canonical chain records:

```text
CUSTODY_EPOCH: <positive integer>
```

The first endpoint uses `1`. Every direct successor increments by exactly one.

Before updating `ACTIVE.md`:

1. read its current repository blob/version and `CUSTODY_EPOCH`;
2. create the next immutable endpoint from that exact state;
3. update `ACTIVE.md` using the exact prior blob/version and `epoch + 1`;
4. if the write is rejected, conflicts, or the observed epoch changed, stop and re-ground.

Do not force a stale update merely because both agents began from the same endpoint.

This is a repository compare-and-swap discipline. Git merge conflicts and contents-API blob-SHA checks are both valid stale-write signals.

## Same-chain divergence

Two successors from one endpoint are not silently accepted:

```text
EP-0004
  -> EP-0005-A
  -> EP-0005-B
```

The validator reports divergent custody. Incoming work must compare both material states and create an explicit reconciliation/supersession endpoint. Newest timestamp or largest diff does not win automatically.

## Different-chain concurrency

Independent chains should not touch each other's relay state:

```text
WRC agent
  -> agents/chains/ADV-WRC-1389/**

LAFEA agent
  -> agents/chains/ADV-LAFEA-1422/**

LoadCalc agent
  -> agents/chains/ADV-LOADCALC-1505/**
```

They coordinate only when there is a real overlap in:

```text
exact file/path
authority domain
benchmark/oracle
controlled input
release/publication authority
dependency/stacking
```

No relay-file collision should manufacture a coordination problem that does not exist in the engineering work.

## Derived dashboard

Use:

```text
python skills/engineering-pr-delivery-v2/scripts/render_agentchain_dashboard.py .
```

to render current non-terminal chain traffic from `agents/chains/*/ACTIVE.md`.

The rendered dashboard is navigation convenience only. It may be regenerated for reporting or maintenance, but normal endpoint advancement must not require a shared dashboard commit.

## Legacy compatibility

Repositories that already contain:

```text
agents/agentchain.md
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

retain those artifacts as historical/recovery evidence. Do not mass-rewrite immutable history.

Existing legacy-format chains may finish in legacy format or migrate at a deliberate endpoint. New chains and new independent workstreams should use the canonical chain-local store.

During migration, use the old `validate_agentchain.py` for legacy history and `validate_chain_store.py` for canonical chain-local state.
