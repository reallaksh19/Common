# Multi-Agent Programme Issues — durable specification + operational ledger

Use this model when one Owner outcome spans several meaningful workstreams.

## 1. Topology

```text
PARENT PROGRAMME ISSUE
= governing programme specification

OWNER-AUTHORIZED AMENDMENTS / COMMENTS
= durable semantic chronology

[Relay Handover] CHILD
= current operational ledger / reconstruction index

CHILD IMPLEMENTATION ISSUES
= bounded engineering responsibilities

PRs / commits / tests / artifacts
= material and exact-head evidence

Relay V3.1
= recorder / reconstruction / reporting only
```

Use V3.1 only. V3/V2.5 are historical compatibility material, not live coordination semantics.

## 2. Parent issue

The parent preserves:

- Owner outcome / why-now;
- non-goals;
- current programme basis revision;
- effective amendment index;
- canonical input/source registry;
- programme invariants;
- workstream/ownership registry;
- producer/consumer contracts;
- dependency contracts;
- programme exit criteria;
- engineer/coordinator/Owner decision boundaries.

Do not turn the parent into a per-turn status log.

## 3. Owner-authorized amendments

Use explicit amendment comments for real semantic changes.

Kinds:

```text
OWNER_AMENDMENT
OWNER_DECISION
RESPONSIBILITY_TRANSFER
PROGRAMME_DISCOVERY
EVIDENCE_RECORD
```

Each records:

```text
BASIS
CHANGE
WHY
AFFECTS
DOES NOT AFFECT
SUPERSEDES
```

Keep the parent effective-amendment index current.

## 4. Dedicated [Relay Handover] child

Create exactly one operational-ledger issue per programme.

It records/indexes:

- programme basis;
- active/nonterminal workstreams;
- implementation-plan refs;
- branches / PRs / exact heads;
- expected next observables;
- dependency states;
- all nonterminal PRs;
- pending items;
- known issues;
- negative knowledge;
- producer→consumer handoffs;
- programme-significant local execution results;
- Owner decisions needed;
- next coordinator action;
- next useful observation.

Its contents are evidence pointers and coordination context, not authority.

## 5. Child profiles

### WORK_PACKAGE
Substantial bounded implementation or validation responsibility.

### PARALLEL_FOCUSED
Small/medium independent task such as:

- falsifier implementation;
- stale expectation correction;
- source-derived oracle/backlog update;
- focused guardrail debt;
- bounded integration finding.

### REVISION
Material revision of completed/frozen predecessor work.

### INTEGRATION
Cross-workstream consumer/closure work.

Each child states outcome, witness, ownership boundary, canonical inputs, producer/consumer contract, real dependencies, independent work, falsifier, success oracle, implementation plan, expected handoff and semantic escalation.

## 6. Parallelism

Do not predeclare a global serial/parallel lock.

Derive current relationship from production truth:

```text
CAN_RUN_NOW
CAN_RUN_PARTIALLY
NEEDS_OUTPUT_FROM <producer>
MAY_CONFLICT_WITH <workstream>
```

A shared file is not automatically a programme dependency. Use isolated branches/worktrees and integration where possible.

## 7. Dependencies

Record the missing production output, not merely an issue edge.

```text
producer
consumer
required output
why required
satisfaction evidence
independent work
consumer consequence
```

Do not wait for producer issue closure if the required durable output already exists.

## 8. Implementation plans

Each agent should publish a revisable implementation plan when practical.

A plan is an execution baseline for reconstruction and plan-conformance reasoning.

Missing/stale plans reduce coordinator confidence; they never revoke engineering agency.

## 9. PR/material truth

PRs are implementation/exact-head validation vehicles.

Carry every nonterminal PR in the Handover ledger until terminal.

A PR merge is not automatically a programme exit criterion.

## 10. Coordinator use

The coordinator joins:

```text
parent
+ effective amendments
+ Handover
+ child responsibility
+ implementation plans
+ nonterminal PRs
+ current production evidence
+ negative knowledge
```

to derive outcome, ownership, producer-consumer, dependency, expectation, material, evidence, negative-knowledge, decision and temporal graphs.

Use those to:

- maximize parallel-safe execution;
- route outputs to consumers;
- detect unreconciled plan drift;
- choose useful timers/events;
- recommend helpers/local engineering coordinator;
- recover after session loss;
- avoid repeated dead ends;
- detect semantic boundaries;
- produce concise Owner reports;
- map child outputs back to parent EXIT criteria.

See `engineering-programme-coordinator/references/coordinator-information-use.md`.

## 11. Completion

Programme completion is determined from parent exit criteria and exact durable evidence.

For each criterion:

```text
SATISFIED
PARTIAL
OPEN
DEFERRED
NOT_APPLICABLE
```

Do not invent completion percentages from merged child counts.
