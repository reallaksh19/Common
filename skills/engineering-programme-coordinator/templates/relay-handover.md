# [Relay Handover] Programme Operational Ledger

This child issue is the durable **current operational index** for one programme.

It is continuously useful during multi-agent execution, not only when a human/agent hands over.

It is an index to durable evidence, not the engineering truth itself.

```text
ISSUE_ROLE: RELAY_HANDOVER
PARENT_PROGRAMME: github:<owner>/<repo>#<parent>
PROGRAMME_BASIS_REVISION: PB-....
RELAY_PROTOCOL: V3.1_ONLY
```

## Non-authority rule

Missing, stale or incorrect Handover content may reduce observability/reconstruction quality.

It does **not** invalidate production work, revoke ownership, block coding, block PRs or authorize execution.

A ledger statement such as "B produced X" is not proof by itself. Link the commit/PR/test/artifact that proves X.

## Programme basis

- Parent:
- Current effective programme basis:
- Last observed main:
- Last reconciled at:

## Workstreams

### <A> — <child issue>

**Owned outcome:** ...

**Implementation plan:** PRESENT / MISSING / STALE / UNKNOWN — <ref/revision>

**Agent / local coordinator ref:** ...

**Branch:** ...

**PR:** ...

**Exact head:** ...

**Expected next observable:** ...

**Latest durable evidence:**

- ...

**Next programme consequence:** ...

Repeat for every active/nonterminal workstream.

## Dependency ledger

| Producer | Required production output | Consumer | State | Evidence | Independent work |
| --- | --- | --- | --- | --- | --- |
| B | ... | C | MISSING / UNCERTAIN / DISCOVERED / SATISFIED / SUPERSEDED | ... | ... |

Do not represent dependencies as permission locks.

## Nonterminal PRs

Carry every nonterminal PR until it is merged, closed or superseded.

| PR | Workstream | Lifecycle | Head | Base | Mergeability / review | Note |
| --- | --- | --- | --- | --- | --- | --- |
| #... | ... | DRAFT / OPEN / CHANGES_REQUESTED / CONFLICTED / REVIEWABLE / UNKNOWN | ... | ... | ... | ... |

## Pending items

- ...

## Known issues

- ...

## Negative knowledge / do-not-reopen

For each important rejected path or disproved assumption:

### NK-...

**Statement:** ...

**Evidence:**

- ...

**Reopen only if:** ...

This prevents replacement agents from re-running already-settled dead ends.

## Recent producer → consumer handoffs

### <producer> → <consumer>

**Output:** ...

**Evidence:**

- ...

**Proved:**

- ...

**Not proved:**

- ...

**Known limitations:**

- ...

**Consumer must not infer:**

- ...

## Local engineering coordination

Promote only programme-significant local results:

- durable result;
- discovered production dependency;
- semantic change;
- local evidence requiring shared promotion;
- session loss with material programme consequence.

Do not copy routine worker chatter or command logs here.

## Owner decisions needed

Prefer:

```text
NONE
```

When needed, state the exact decision, why it belongs to the Owner, affected workstreams, evidence and reversible consequences.

## Next coordinator action

What is the smallest useful coordination move now?

Examples:

- route B's durable output to C;
- send a CONTEXT_UPDATE to local coordinator;
- observe an expected PR result later;
- reconcile a semantic change;
- ask Owner one genuine question;
- do nothing.

## Next useful observation

**Reason:** ...

**Expected evidence:**

- ...

A timer/event may be used to wake this observation, but the timer is never authority.
