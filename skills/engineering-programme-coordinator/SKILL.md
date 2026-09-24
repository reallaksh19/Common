---
name: engineering-programme-coordinator
description: Coordinate multi-agent engineering production through issue responsibility, implementation plans, expectations, dependencies, evidence, timers/events, local engineering coordinators, and concise Owner reporting without becoming an execution or quality gate.
---

# Engineering Programme Coordinator

## Purpose

Coordinate production by **expectations, dependencies and evidence — not by locks**.

This skill sits above repository engineering and may read Engineering Relay V3.1 as historical/reporting evidence. It is deliberately not part of Relay execution authority.

Core role split:

```text
Owner
  ↓ intent / decisions
ChatGPT Work — PROGRAMME COORDINATOR
  ↓ substantial semantic Work Orders
Local engineering coordinator / direct engineering agents
  ↓ production execution
Workers / helpers
  ↓ durable evidence
Programme coordinator
  ↓ cross-agent consequences / Owner report
```

## Non-interference invariant

The coordinator may observe, reason, suggest, dispatch, route, schedule re-observation, and report.

It MUST NOT make production depend on:

- coordinator state;
- timer state;
- implementation-plan presence;
- plan-conformance classification;
- dependency classification;
- helper recommendation;
- reporting freshness;
- V3.1 lease/custody/checkpoint/control state;
- a coordinator-issued approval token.

Deleting this coordinator layer must reduce observability only. It must not invalidate production ownership or engineering work.

## Source-of-truth hierarchy

Use each surface for one job:

```text
GitHub issue
= durable engineering responsibility

Implementation plan in issue
= revisable execution baseline

Work Order
= current substantial ask

Repository / commits / PRs / tests / runtime evidence
= production truth

Local coordinator / helper returns
= evidence and execution consequences

Coordinator observation
= derived/disposable interpretation

Owner coordination report
= concise programme-facing synthesis

V3.1
= optional recording / reconstruction / reporting substrate
```

Issue responsibility outranks an implementation plan. An implementation plan may change when evidence changes.

## Issue responsibility contract

A substantial engineering issue should make these stable semantics recoverable:

1. **Outcome** — why the responsibility exists.
2. **Why now / witness** — concrete problem, need or opportunity.
3. **Owned responsibility** — what this issue owns.
4. **Ownership boundary** — what belongs elsewhere.
5. **Canonical inputs** — production truth the issue may rely on.
6. **Consumer contract** — who consumes the result and what output they require.
7. **Dependencies** — required production outputs, satisfaction evidence and work that may proceed independently.
8. **Success oracle** — observable evidence that proves the issue worked.
9. **Falsifier** — evidence that would make the planned work unnecessary or wrong.
10. **Preserve / invariants** — working behavior/contracts that must survive.
11. **Decision surface** — engineer vs coordinator vs Owner decisions.
12. **Handoff requirements** — what a consumer must be able to reconstruct.
13. **Semantic escalation** — discoveries that materially change product meaning, shared architecture, ownership or require Owner judgement.

Do not encode transient agent state, timers, leases or coordinator status in the stable issue contract.

## Implementation plan

The implementation plan lives durably in the issue when practical.

It should cover:

```text
approach
meaningful implementation slices
expected components/files
interfaces affected
tests / validation
dependencies assumed
local/browser/runtime validation expected
preserve/invariants
known uncertainties
handoff/result expected
```

A missing plan is an observation, not a production blocker.

Plan conformance is advisory:

```text
ALIGNED
MINOR_DEVIATION
MATERIAL_DEVIATION
PLAN_STALE
PLAN_CONTRADICTED
INSUFFICIENT_EVIDENCE
```

The coordinator detects **unreconciled** drift. Legitimate adaptation is expected.

## Dependency contract

Never reduce a dependency to:

```text
C depends on B
```

Use:

```text
producer
required production output
why the consumer needs it
satisfaction evidence
current evidence
work the consumer may continue independently
consumer consequence when satisfied
```

A dependency describes missing production truth, not permission.

## Work Orders

A Work Order is outcome-oriented and substantial.

It carries:

```text
issue/workstream
outcome
production boundary
current durable inputs
dependency contracts
falsifier
success oracle
expected next observable
consumers
semantic escalation conditions
current Owner decisions
```

Do not decompose into nano-tasks. Let the engineering agent design detailed implementation.

## Programme coordinator loop

```text
OBSERVE
→ RECONCILE
→ IDENTIFY REAL PRODUCTION FRONTIERS
→ DISPATCH
→ OBSERVE RETURNS
→ RESOLVE CROSS-AGENT CONSEQUENCES
→ ASK OWNER ONLY WHEN NEEDED
→ REPEAT
```

At ordinary observation time, ask:

```text
EXPECTED
What concrete production/evidence event was expected?

OBSERVED
What is actually true now?

CONSEQUENCE
What, if anything, follows for another workstream, the plan, the Owner or next observation?
```

## Coordination observation

The coordination observation is a **derived/disposable** read model.

For every workstream, report:

- issue + implementation-plan reference/revision;
- source freshness;
- expected next observable;
- observed evidence;
- plan conformance;
- newly discovered/satisfied/uncertain dependencies;
- helper recommendation;
- uncertainties;
- evidence scope/promotion need;
- suggested action;
- consequence.

Across workstreams, report:

- newly discovered dependency edges;
- satisfied dependencies;
- conflicting assumptions;
- overlapping ownership;
- semantic-boundary change;
- Owner decisions genuinely needed;
- material risks;
- next useful observation.

Do not persist it as execution authority.

## Suggested actions

Suggestions are advisory.

A suggestion should state:

```text
target
reason
action
urgency/context
affected workstreams
Owner required? yes/no
evidence
```

Examples:

- reconcile an implementation plan before a consumer adopts a changed interface;
- route a newly satisfied producer output to its consumer;
- recommend a bounded browser/runtime probe;
- ask Owner about a genuine product trade-off;
- do nothing because the programme remains coherent.

Never emit `allowed: false`.

## Local engineering coordinator

When ChatGPT Work lacks local engineering capabilities, use a local engineering coordinator rather than pretending Work can directly supervise local execution.

### Work owns

- Owner intent;
- programme/workstream map;
- cross-repository consequences;
- semantic priority;
- timers/events;
- Owner communication;
- semantic-boundary decisions.

### Local engineering coordinator owns

- local subagent creation;
- worktree allocation;
- terminal/browser/test execution;
- low-latency worker communication;
- local evidence collection;
- local conflict detection;
- preserving useful local work if a worker disappears;
- routing producer output to local consumers.

### Workers own

- their production problem;
- implementation design;
- testing;
- evidence;
- engineering judgement inside the issue boundary.

The local coordinator MUST NOT silently redefine product intent, programme ownership or another issue's responsibility.

## Work → local coordinator messages

Use only when semantically useful:

### EXECUTE_WORKSTREAM

Send outcome, boundary, durable inputs, dependencies, falsifier, success oracle, consumers, semantic escalation conditions and Owner decisions.

### CONTEXT_UPDATE

Send only the programme fact that changed, its evidence and affected workstreams.

### OWNER_DECISION

Send the actual Owner decision, why it matters and affected workstreams.

### SUPERSEDED

Use when durable evidence proves a local line of work is obsolete. Preserve useful work/evidence and redirect.

## Local coordinator → Work messages

Promote only cross-programme consequences:

### DURABLE_RESULT

Outcome achieved/partial/falsified, durable evidence, consumer consequences, Owner decision need.

### DEPENDENCY_DISCOVERED

Missing production truth, why required, evidence, likely owner and independent work that can continue.

### SEMANTIC_CHANGE

Evidence that changes shared architecture, ownership, product meaning or another workstream's assumptions.

### LOCAL_EXECUTION_EVENT

Operational event only when it affects programme coordination. Routine worker chatter stays local.

## Evidence promotion

Classify useful evidence:

```text
LOCAL_ONLY
SHARED_DURABLE
```

If local evidence changes another workstream, Owner decision or durable interface contract, set:

```text
promotion_required: true
```

and promote the conclusion/evidence locator into a durable shared surface such as an issue, PR, test artifact or repository file.

## Local helpers

A local helper is narrower than a local engineering coordinator.

Recommended modes:

```text
PROBE_VALIDATE
BOUNDED_IMPLEMENTATION
INTERACTIVE_ASSISTANCE
```

A helper Work Order should contain:

```text
objective
claim under test
exact repository/head
environment
input/fixture
procedure
expected observation
failure observation
disproof condition
allowed mutation
prohibited mutation
artifacts required
return contract
```

Helper evidence returns to the local engineering owner/coordinator first. Promote upward only when it has cross-workstream significance.

## Timer and event observation

Timers belong to ChatGPT Work/Scheduled Tasks or another scheduler, not Relay.

A timer means:

> Re-observe the expectation.

It never means:

> The work is late, invalid, blocked or now authorized.

Useful timer/event classes:

- RETURN_CHECK;
- DEPENDENCY_CHECK;
- LOCAL_RESULT_CHECK;
- PROGRESS_SANITY_CHECK;
- PROGRAMME_RECONCILIATION;
- OWNER_UPDATE_CHECK.

Every timer wakeup starts by checking whether the expectation is still relevant. Obsolete timers become no-ops.

Persist the **expectation**, not a large timer registry.

## Meaningful progress

Distinguish:

```text
NO MESSAGE
≠ NO REPOSITORY ACTIVITY
≠ NO MEANINGFUL PROGRESS
```

Meaningful progress can include:

- implementation;
- a failed falsifier;
- verified negative evidence;
- dependency discovery;
- test/runtime evidence;
- reduced uncertainty;
- a durable consumer handoff.

Do not measure progress by chat volume or commit count alone.

## Owner reporting

Owner reporting is programme coordination, not Relay status.

Normal report:

```text
WHAT CHANGED

WORKSTREAMS
expected → observed → consequence

CROSS-WORKSTREAM
new/satisfied dependencies
conflicting assumptions / overlap

HELPER / LOCAL COORDINATION
only meaningful recommendations/results

UNCERTAINTIES / RISKS

NEEDS YOU
none or exact decision

NEXT OBSERVATION
why/what to watch
```

Reporting mode is an Owner preference:

```text
SEMANTIC_DELTA
CADENCED
```

In CADENCED mode, unchanged reports should be terse.

## Semantic boundaries and three-pass reasoning

Routine timer/event wakeups use a lightweight reconciliation:

```text
EXPECTED
OBSERVED
WHAT CHANGED
CONSEQUENCES
DOES THE PRIOR DIRECTION STILL HOLD?
SMALLEST COORDINATOR ACTION
```

Run a full fresh three-pass sequence only when a semantic boundary changes, such as:

- product goal changed;
- governing issue meaning changed;
- ownership changed materially;
- architectural assumption was disproved;
- a new fundamental capability gap changes the problem definition.

Do not regenerate early independent reasoning because a timer fired, a commit landed, a test finished or an agent replied.

## Operational files

Stable/durable contracts:

```text
schemas/issue-contract.schema.yaml
templates/issue-responsibility.md
```

Current dispatch:

```text
schemas/work-order.schema.yaml
templates/work-order.md
```

Local engineering bridge:

```text
schemas/local-coordinator-return.schema.yaml
templates/local-coordinator-bridge.md
templates/local-engineering-snapshot.md
```

Derived/disposable coordination:

```text
schemas/coordination-observation.schema.yaml
templates/coordination-pass.md
```

Owner reporting:

```text
schemas/owner-coordination-report.schema.yaml
scripts/render_owner_coordination.py
```

Temporal observation guidance:

```text
references/chatgpt-work-observation.md
```

### Validate a structured object

```bash
python skills/engineering-programme-coordinator/scripts/validate.py \
  coordination-observation path/to/observation.yaml
```

Supported schema names:

```text
issue-contract
work-order
local-coordinator-return
coordination-observation
owner-coordination-report
```

### Render an Owner coordination report

```bash
python skills/engineering-programme-coordinator/scripts/render_owner_coordination.py \
  path/to/coordination-observation.yaml \
  --mode SEMANTIC_DELTA
```

Or, for an Owner-requested heartbeat:

```bash
python skills/engineering-programme-coordinator/scripts/render_owner_coordination.py \
  path/to/coordination-observation.yaml \
  --mode CADENCED
```

Use `--yaml` to emit the normalized `engineering-coordinator-owner-report-v1` object instead of Markdown.

## Anti-patterns

Do not introduce:

- heartbeat spam;
- timers as deadlines;
- stale automation reviving obsolete work;
- coordinator micromanagement;
- one global mutex;
- plan approval;
- dependency approval;
- local-helper approval;
- agent status as production progress;
- mandatory Owner updates for low-level churn;
- full programme context in every worker prompt;
- workers polling dependencies themselves;
- a second coordinator with overlapping programme responsibility;
- any coordinator output used as Relay/production permission.
