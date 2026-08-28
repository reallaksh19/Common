# Handover Snapshot — crash-ready card

## Purpose

Every non-terminal accepted endpoint contains one `### Handover snapshot` of **fewer than 300 words**. It lets a replacement locate the real task and immediately take the pre-authored qualification without reading a long work report first.

The snapshot is an index, not the detailed evidence store.

## Required contents

Use this compact order:

```text
Repo:
Task:
Chain:
Endpoint:

PR:
PR status:
Branch / PR head / main:
Merge authority:

Engineering / custody / qualification / write state:
Roadmap:
Inputs:
Benchmarks:
Governing docs / authoritative sources:
Current blocker:
Exact next action:

Q1: <concise expert prompt>
Q2: <concise expert prompt>
Q3: <concise expert prompt>
Q4: <concise expert prompt>
Q5: <concise expert prompt>
```

The five snapshot prompts must correspond exactly to the detailed `### Takeover qualification pack` below the snapshot.

## Word limit

`<300 words` applies to the complete snapshot including Q1-Q5. Keep long hashes/paths concise and point to detailed inventories below.

Do not weaken the examination to fit the limit. The snapshot Qs may be concise, while the detailed qualification pack specifies repository anchors, calculation/reconstruction, oracle, falsifier, and fail conditions.

## Crash discipline

Before a material batch, a valid current snapshot/Q-set must already exist. After a coherent material batch, publish the next endpoint before beginning another material batch.

If a crash occurs after the endpoint but before the next endpoint, the replacement qualifies against the pinned accepted basis first. Later commits/diffs are reconciled only after qualification PASS.

## Handover-ready marker

Canonical version-3 chain and endpoint state use:

```text
HANDOVER_READY: TRUE
```

Do not claim TRUE if the snapshot is missing, over 300 words, Q1-Q5 are missing/malformed, or the detailed question pack fails the quality gate.
