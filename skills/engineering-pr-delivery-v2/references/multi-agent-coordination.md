# Multi-Agent Coordination

## Purpose

Allow multiple agents to work concurrently in one repository without manufacturing bookkeeping conflicts, while still preventing silent engineering-authority collisions.

## Coordination source

For canonical chains, discover current state from:

```text
agents/chains/*/ACTIVE.md
```

Then read each referenced active endpoint and verify live PRs/branches/diffs.

`agents/agentchain.md` is a derived/legacy navigation surface, not the canonical mutable pointer for new chains.

## Different modules / independent chains

WRC, LAFEA, LoadCalc, and other independent workstreams should use separate chain directories:

```text
agents/chains/ADV-WRC-1389/**
agents/chains/ADV-LAFEA-1422/**
agents/chains/ADV-LOADCALC-1505/**
```

They may each use `EP-0001`, `EP-0002`, and so on because endpoint identity is `(CHAIN_ID, ENDPOINT_ID)`.

Independent agents do not edit each other's `ACTIVE.md` or endpoint files.

## Check dimensions

Before a new material leg and before engineering-critical mutation compare active chains for:

```text
exact-file overlap
path-prefix overlap
engineering/software authority overlap
benchmark/oracle overlap
shared controlled inputs
release/publication overlap
dependency or stacked-PR relationship
main/base drift
```

## Classification

```text
SAFE
  No material collision or dependency requiring coordination.

COORDINATION_REQUIRED
  Work may proceed only with explicit ordering, ownership, or reconciliation.

BLOCKED_BY_ACTIVE_CHAIN
  Active authority collision makes concurrent mutation unsafe.

UNKNOWN
  Insufficient evidence to establish independence.
```

`UNKNOWN` is not `SAFE`.

## Authority overlap

No exact-file overlap does not prove engineering independence.

Examples:

- one chain changes canonical units while another changes a solver consuming them;
- one chain changes a benchmark while another changes production against that benchmark;
- one chain changes source authority while another promotes a route that assumes it;
- two chains change separate UI/export paths that publish the same engineering quantity.

## Chain-local custody

Each chain's `ACTIVE.md` carries:

```text
ACTIVE_CUSTODIAN
CUSTODY_EPOCH
COORDINATION_STATE
DEPENDENCIES
```

The endpoint carries the same `CUSTODY_EPOCH`.

Advancing one chain requires compare-and-swap discipline on that chain's current `ACTIVE.md` only. A different chain's advancement must not force a relay conflict.

## Divergent agents on one chain

If two agents continue from the same prior endpoint:

```text
EP-0007
  -> EP-0008-A
  -> EP-0008-B
```

then:

1. stop treating either branch as automatically authoritative;
2. compare both against the common endpoint basis;
3. classify engineering differences/evidence;
4. select `CONTINUE`, `SALVAGE_PARTIAL`, `SUPERSEDE`, or a reconciled leg;
5. create a later reconciliation endpoint;
6. advance `ACTIVE.md` only from the accepted lineage.

Do not resolve by timestamp, larger diff, or force-writing `ACTIVE.md`.

## Stale-write rule

An agent advancing `ACTIVE.md` must write against the exact repository blob/version it read and increment `CUSTODY_EPOCH` by one.

If the write conflicts or the observed epoch changed:

```text
STALE_WRITE
→ READ_ONLY
→ re-ground chain
→ reconcile
```

Do not force a stale current pointer.

## PR transitions

When a chain moves to a successor PR, preserve:

```text
CHAIN_ID
PREVIOUS_ENDPOINT
CUSTODY_EPOCH sequence
predecessor PR
successor PR
reason for transition
known-good inherited evidence
unresolved work
```

A successor PR does not create a new engineering mission unless scope genuinely changes.

## Executable overlap check

Canonical chain-local store:

```text
python skills/engineering-pr-delivery-v2/scripts/detect_chain_overlap.py .
```

Legacy shared-index repositories remain supported by passing `agents/agentchain.md` instead.

See `chain-concurrency.md`.
