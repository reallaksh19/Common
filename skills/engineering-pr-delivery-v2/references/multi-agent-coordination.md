# Multi-Agent Coordination

## Purpose

A repo-wide relay index must also prevent two active chains from silently modifying the same engineering authority.

## Coordination source

Use the `ACTIVE CHAINS` table in `agents/agentchain.md` as the first navigation surface, then verify live PRs/branches and actual diffs.

The table is not a substitute for live GitHub state.

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

BLOCKED
  Active authority collision makes concurrent mutation unsafe.

UNKNOWN
  Insufficient evidence to establish independence.
```

`UNKNOWN` is not equivalent to `SAFE`.

## Authority overlap

No exact-file overlap does not prove engineering independence.

Examples of semantic overlap:

- one chain changes canonical units while another changes a solver consuming them;
- one chain changes a benchmark while another changes production against that benchmark;
- one chain changes source authority while another promotes a route that assumes it;
- two chains change separate UI and export paths that both publish the same engineering quantity.

## Chain row information

Where practical, include in the active-chain row or latest endpoint:

```text
current PR
authority domain
expected next-leg files/domains
dependency chain(s)
coordination state
```

## Divergent agents on one chain

If two agents continue from the same prior endpoint and create divergent material states:

1. stop treating either branch as automatically authoritative;
2. compare both against the common endpoint basis;
3. classify engineering differences and evidence;
4. select `CONTINUE`, `SALVAGE_PARTIAL`, `SUPERSEDE`, or a newly reconciled leg;
5. create a new endpoint documenting the custody/reconciliation decision.

Do not resolve engineering conflicts solely by choosing the newest timestamp or largest diff.

## PR transitions

When a chain moves to a successor PR, preserve:

```text
CHAIN_ID
PREVIOUS_ENDPOINT
predecessor PR
successor PR
reason for transition
known-good inherited evidence
unresolved work
```

The successor PR does not create a new engineering mission unless scope genuinely changes.
