# V3.1 Parent Issue and Handover Ledger Protocol

## Purpose

A governed parent issue states the human/programme problem. One dedicated `[Relay Handover]` child/sub-issue is the provider-facing operational ledger for that parent.

The Handover issue is a generated/provider projection. It is not roadmap, checkpoint, EP, lease, control, or acceptance authority.

## Responsibility model

| Actor | Responsibility | Must not do |
| --- | --- | --- |
| Owner | Decide intent-bearing goal/scope/priority changes and authorize material transfer/supersession/closure when required | Maintain routine relay bookkeeping |
| Active execution agent | Discover facts, implement bounded work, write canonical relay transactions/evidence, raise pending/KI/offload facts | Manually maintain duplicate parent/ledger status tables |
| Relay | Derive parent summary + Handover ledger, synchronize provider state, and verify readback | Invent Owner intent or accepted engineering truth |
| Local/helper agent | Execute the bounded request and return evidence | Update parent issue, Handover ledger, roadmap, checkpoint, or EP authority |
| Successor/recovery agent | Reconstruct durable truth and continue/recover through normal admission | Rewrite predecessor history |
| Prompt 0.5/1/2/2.5 | Reason, challenge, verify, and propose disposition | Mutate provider/governing state directly |
| Prompt 3 | Execute an already-authorized reconciliation and verify its effect | Create new Owner intent |

The shorthand is:

```text
OWNER  -> DECIDES
AGENT  -> DISCOVERS + PRODUCES EVIDENCE
RELAY  -> RECORDS + SYNCHRONIZES + READS BACK
PROVIDER -> STORES/REPORTS EXTERNAL STATE
```

## Parent issue contents

The parent issue stays compact:

- governing goal/acceptance;
- programme relationship;
- generated Relay section with current frontier, progress, handover-ledger link, pending/KI/offload counts and issue disposition.

The agent does not manually maintain the generated Relay section.

## Dedicated Handover issue contents

Exactly one Handover issue is associated with each governed parent issue. Its current body is regenerated from durable relay truth and contains:

- EP index and current frontier;
- parent progress;
- pending items from existing `PEND-*` tracked controls;
- known issues from existing `KI-*` tracked controls;
- EP offloads/local-helper work and their states;
- current delivery/PR state;
- handover/recovery-relevant event history;
- immediate next action.

No duplicate pending, known-issue, offload, EP, or checkpoint authority is created.

Historical provider comments may record synchronized handover/recovery milestones, but repository EVENTS/CHECKPOINTS remain the reconstructable basis.

## Provider synchronization

Relay performs provider synchronization after a canonical change that materially changes the parent/ledger projection.

```text
canonical relay transaction/evidence
        ->
regenerate HANDOVER_LEDGER + PARENT_RELAY_SUMMARY
        ->
apply authorized GitHub body/comment change
        ->
read provider state back
        ->
compare normalized readback
```

Provider sync failure is a coordination/delivery problem unless the requested engineering action explicitly requires provider convergence. Do not turn a stale GitHub projection into accepted engineering truth.

## Parent issue upgrade protocol

Prompt 1 may challenge the parent framing. Prompt 2 verifies current reality. Prompt 2.5 proposes one existing disposition:

```text
NO_CHANGE
UPDATE
LINK
TRANSFER
SPLIT
SUPERSEDE
CLOSE
UNKNOWN / OWNER_DECISION_REQUIRED
```

Prompt 1/2/2.5 do not mutate the parent.

### Relay may synchronize without new Owner intent

Relay may update provider status when it is only reporting already-governed truth, for example:

- acceptance/progress state;
- current EP/lease/frontier;
- pending/KI/offload state;
- PR/delivery state;
- already-authorized relationship/readback.

### Owner authority is required

Require direct Owner authority when the proposed change alters governing intent, including:

- changing the human goal;
- materially expanding/narrowing governing scope;
- changing acceptance meaning rather than status;
- transferring responsibility where ownership/goal changes;
- superseding the governing issue;
- closing/cancelling work despite unresolved governed obligations.

## Transfer to a new GitHub issue

TRANSFER preserves history.

1. Determine exact transferred scope/acceptance/pending/KI/offload references.
2. Obtain Owner authority if the transfer changes governing intent/ownership.
3. Create or identify the target parent issue.
4. Ensure the target has its own dedicated Handover issue.
5. Add typed `TRANSFERS_TO` / related lineage on the source observation and reciprocal provider context on the target.
6. Synchronize the old Handover ledger with what moved and what remains.
7. Seed the target Handover ledger with inherited references and provenance.
8. Read back both provider issues.
9. Never delete historical ownership from the source issue.

SPLIT follows the same rule but retains governed work in both issues. SUPERSEDE moves the governing formulation itself; the old issue remains historical and points to the replacement.

## Abandonment robustness

The Handover ledger must be reconstructable without a final action from the disappearing agent. The next process derives EP status from durable EP/lease/checkpoint/event state. If an EP is no longer current/owned and has no accepted completion checkpoint, the projection exposes `RECOVERY_REQUIRED` rather than hiding it.

This projection does not itself decide process liveness; it makes loss of custody visible once canonical custody state is updated/recovered.
