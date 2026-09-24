# V3.1 Parent Programme and [Relay Handover] Operational Ledger

## Purpose

Use GitHub as the durable programme specification and coordination record while keeping V3.1 recorder-first.

For a multi-agent programme:

```text
PARENT PROGRAMME ISSUE
= governing human/programme contract

OWNER-AUTHORIZED AMENDMENTS
= durable semantic chronology

CHILD IMPLEMENTATION ISSUES
= bounded engineering responsibilities
  + agent-authored implementation plans
  + meaningful task evidence/results

[Relay Handover] CHILD
= current programme operational ledger / reconstruction index

PRs / commits / tests / artifacts
= material and exact-head evidence

V3.1
= record / reconstruct / project / report
```

None of these coordination surfaces is engineering permission.

## Responsibility model

| Actor | Owns |
| --- | --- |
| Owner | Human/programme intent, genuine product decisions, intent-bearing amendments |
| Programme coordinator | Cross-agent consequences, dependency routing, useful parallelism, temporal re-observation, concise Owner reporting |
| Engineering agent | Its bounded production problem, implementation plan, implementation details, validation and handoff |
| Local engineering coordinator | Local workers/worktrees/tests/browser/runtime orchestration where needed |
| Helper | Bounded probe/validation/implementation task and evidence return |
| V3.1 | Durable recorder/reconstruction/read-model/provider projection |

## Parent programme issue

The parent preserves stable programme semantics:

- Owner outcome and why-now;
- non-goals;
- programme basis revision;
- effective Owner/programme amendment index;
- canonical source/input registry;
- workstream/ownership partition;
- producer/consumer contracts;
- dependencies expressed as required production outputs;
- programme invariants;
- programme exit criteria;
- engineer/coordinator/Owner decision boundaries.

Do not use the parent as a per-command status log.

## Child implementation issue

The child issue is the durable home for one engineering responsibility.

It carries:

- owned outcome;
- ownership/conflict boundary;
- canonical inputs;
- producer/consumer contract;
- real dependencies + independent work;
- falsifier;
- success oracle;
- implementation plan;
- task evidence/results;
- expected handoff;
- semantic escalation conditions.

The engineering agent publishes its own implementation plan there.

## Agent task publication lifecycle

Normal durable task publications are:

```text
IMPLEMENTATION_PLAN
PLAN_UPDATE
TASK_EVIDENCE
TASK_RESULT
```

The agent does not publish every command or timer tick.

### IMPLEMENTATION_PLAN

After live revalidation and before substantial material modification, publish the current plan when practical.

A plan is not approval. Do not wait for Relay/coordinator permission after publishing it.

### PLAN_UPDATE

Use only when material evidence changes the approach while the owned responsibility remains the same.

Plan revision does not require a new EP.

### TASK_EVIDENCE

Use when an intermediate result changes reconstruction or another workstream's next action.

### TASK_RESULT

Use at a meaningful delivery/handoff boundary. Link exact branch/PR/base/head and validation evidence.

See `agent-task-publication.md`.

## EP relationship

The EP records bounded task identity.

In the new programme topology an EP may carry both:

```text
programme_parent
= governing parent programme issue

parent_issue
= owned child implementation issue
```

Older EPs may have only `parent_issue`; V3.1 treats that issue as the reconstruction root for compatibility.

The EP may record an initial implementation-plan basis if one existed when the EP was created, but current plan revision comes from the child-issue provider observation.

Do not create a new EP merely because the plan was first published or revised.

## Dedicated [Relay Handover] child

Create exactly one programme operational ledger issue named:

```text
[Relay Handover] <programme>
```

The provider sync may reuse older `[Relay]` case issues for compatibility, but newly materialized issues use `[Relay Handover]`.

The ledger indexes rather than duplicates:

- programme basis;
- workstream / EP / child issue;
- implementation-plan state/ref/revision;
- expected next observable;
- branch/PR/exact-head material;
- all nonterminal PRs when provider information is available;
- pending items and known issues;
- required production-output dependencies;
- negative knowledge / do-not-reopen;
- meaningful local/helper returns;
- producer→consumer handoffs;
- Owner decisions needed;
- next coordinator action;
- next useful observation.

A ledger statement does not prove a production claim. Link exact durable evidence.

## Programme-root versus child-task observation

The programme Handover ledger is rooted at the programme parent.

The current task plan may live on a child implementation issue.

V3.1 therefore supports:

```text
programme parent observation
+
optional work/child issue observation
        ↓
programme Handover ledger
```

The work-issue observation supplies current plan/publication context; the programme observation supplies programme basis/progress/Handover identity.

## Provider synchronization

Provider synchronization is a reporting/reconstruction operation:

```text
durable V3.1 / production evidence
→ regenerate derived Handover projection
→ update only Relay-managed provider block
→ read back
→ compare normalized content
```

Provider sync failure is a reporting/delivery problem. It does not invalidate production work.

## Negative knowledge

Preserve rejected approaches and accepted do-not-reopen conclusions with evidence and a reopen condition.

The coordinator should consult them before dispatching a replacement agent so sessions do not repeat already-settled dead ends.

## Session-loss recovery

If an agent disappears:

1. read the child issue;
2. read current implementation plan;
3. inspect EP/task snapshot;
4. inspect branch/PR/exact head;
5. inspect task evidence and durable tests/artifacts;
6. determine what production consequence remains unfinished;
7. give a successor the smallest reconstruction packet.

No lease-expiry or recovery ceremony is required to make already-existing production evidence valid.

V3.1 may record the executor change for history.

## Coordinator observation

The coordinator should reason:

```text
EXPECTED
what plan/evidence event should happen next?

OBSERVED
what durable evidence exists now?

CONSEQUENCE
what changes for this workstream, a consumer, the Owner, or next observation?
```

Timers wake this observation; timers never authorize engineering.

## Semantic programme changes

Only explicit Owner/programme amendments alter governing programme meaning.

When evidence changes programme outcome, ownership, shared interface semantics, or canonical source authority:

- preserve the old basis;
- record the new evidence;
- update the effective amendment/disposition;
- route affected workstreams;
- regenerate deeper three-pass reasoning if the semantic boundary truly changed.

Routine plan changes, commits, PR updates and tests do not automatically change programme meaning.

## Non-authority invariant

Missing or stale:

- implementation plan;
- Handover ledger;
- V3.1 projection;
- timer;
- coordinator report;
- lease/checkpoint/control observation;

may reduce reconstruction quality.

They do not block coding, invalidate material, revoke engineering responsibility, or create permission.

## V3.1 only

Use Engineering Relay V3.1 only for current recording/reconstruction/reporting semantics.

Do not use V3 or V2.5 as live coordination, recovery, gating, handover or Owner-command protocols.
