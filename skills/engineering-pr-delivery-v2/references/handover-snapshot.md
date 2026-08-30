# Active Handover Snapshot — mandatory repository-work response envelope

## Purpose

Every response that performed, attempted, audited, blocked, resumed, advanced, completed or re-grounded repository work starts with:

```text
# Active handover snapshot
```

No narrative prose precedes it.

The snapshot is always shown. **Full Q1-Q5 are not always shown.** Their generation/display is controlled only by the three Owner progression commands in `owner-progression-commands.md`.

## State Card

New successor endpoints under `HANDOVER_PROTOCOL_VERSION: 2` contain:

```text
### Active handover snapshot
Repo:
Task:
Chain:
Endpoint:

PR:
PR status:
Branch / PR head / main:
Mergeability:
Reviews:
Unresolved review threads:
Required checks:
Merge authority:
Merge authorized:

Engineering / custody / qualification / write state:
AUTO:
Protocol basis / status:
Work item / source:
Issue basis: <id/status or NOT_APPLICABLE>

Owner roadmap(s):
Other governing roadmaps:
Roadmap alignment / drift:
Roadmap mutation authority:

Original task status:
Inputs:
Benchmarks / oracles:

Qualification:
Scope:
Question set:
Question status:
Question action:
Takeover qualification ready:
Chain handover ready:

Current blocker:
Leg diagnosis:
Exact next action:
```

The State Card target is `<220 words`; concise counts are allowed only when unresolved/failed/open rows remain durably locatable in the Issue Basis/endpoint/ledger.

`MERGE_AUTHORITY` and `MERGEABILITY` are independent. Always show both. Also show whether merge has actually been authorized in the current chain state.

## Question display

### `proceed next`

If the current Q-set remains valid:

```text
Question action: REUSED
Question display: HIDE
```

Do not print unchanged Q1-Q5.

If the qualification scope changed or the set became stale, refresh and show full questions:

```text
## Active qualification questions
Q1 ...
Q2 ...
Q3 ...
Q4 ...
Q5 ...
```

### `proceed next, no Qs`

```text
Question action: SUPPRESSED_BY_OWNER
Question display: HIDE
```

Never generate, refresh or display Q1-Q5 in that bounded progression. If existing coverage becomes stale, show:

```text
Question status: STALE
Takeover qualification ready: FALSE
```

The chain may still be handover-recoverable because task/input/benchmark/roadmap/PR custody is separate from qualification readiness.

### `proceed next, hand over ready`

Full current Q1-Q5 are mandatory in the response and durable takeover checkpoint. If they are stale, refresh them before claiming takeover readiness.

```text
## Active qualification questions
Q1 ... Q5 ...
```

If current questions/sync/validation cannot be completed, report the exact blocker and leave the applicable readiness flag FALSE.

## Changed-this-turn reporting

After the snapshot and any command-required questions, normal reporting is:

```text
## Changed this turn
```

with at most eight concise delta bullets unless the Owner asks for a detailed report.

Do not replace cumulative State Card custody with a long narrative.

## Issue-based cumulative state

For `WORK_ITEM_SOURCE: GITHUB_ISSUE`, the State Card must carry current cumulative status for:

```text
original issue task / acceptance obligations
inputs
benchmarks / oracles
Owner Roadmap(s) and other applicable roadmaps
```

These categories cannot disappear merely because nothing changed this turn. The GitHub Issue Active Handover comment contains the same cumulative state and links to the current Issue Basis and endpoint history. See `github-issue-control-plane.md`.

## Readiness fields

Use distinct readiness planes:

```text
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE: <durable evidence or NONE>
HANDOVER_READY: TRUE | FALSE              # legacy/aggregate compatibility
CHAIN_HANDOVER_READY: TRUE | FALSE
TAKEOVER_QUALIFICATION_READY: TRUE | FALSE
```

`CHAIN_HANDOVER_READY` means the engineering chain can be reconstructed from durable task/roadmap/input/benchmark/PR/endpoint state.

`TAKEOVER_QUALIFICATION_READY` means a valid current Q-set is available for a replacement to enter admission/qualification immediately.

For new states, `HANDOVER_READY` should reflect complete takeover readiness:

```text
HANDOVER_READY == CHAIN_HANDOVER_READY && TAKEOVER_QUALIFICATION_READY
```

subject to handover validation/sync evidence. `proceed next, no Qs` may legitimately end with:

```text
CHAIN_HANDOVER_READY: TRUE
TAKEOVER_QUALIFICATION_READY: FALSE
HANDOVER_READY: FALSE
```

## GitHub-Issue synchronization

For issue-based work, `proceed next, hand over ready` requires:

```text
ISSUE_HANDOVER_SYNC_STATUS: IN_SYNC
```

before `CHAIN_HANDOVER_READY: TRUE` is claimed as the current human-visible control-plane state.

Ordinary `proceed next` also updates the mutable Active Handover comment after the accepted endpoint. If synchronization fails, preserve repository custody but block the next material progression until the Issue projection is reconciled.

## Crash discipline

A valid Q-set is required for **takeover qualification**, not for every same-agent endpoint. Qualification is scope-bound rather than turn-bound.

Before a replacement takes custody:

```text
TAKEOVER_QUALIFICATION_READY: TRUE
→ question-set admission
→ qualification
```

If FALSE, the replacement remains READ_ONLY while an independent question authority/Owner establishes a current set.

Historical endpoints/comments remain immutable.