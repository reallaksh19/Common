# Chemistry Architecture Governance

This file governs how topic-specific proofs interact with the Chemistry V2 architecture.

## Non-negotiable authority rule

A topic-specific case is evidence **about** the architecture. It is not the architecture's ground truth.

For the current stress case:

```text
REDOX
= STRESS_TEST / REGRESSION / SOURCE-SCOPE EXERCISE
!= GROUND TRUTH
!= CANONICAL DOMAIN AUTHORITY
!= GENERIC ENGINE DESIGN INPUT
!= DEFAULT POLICY BASIS
```

A Redox case may expose a defect, falsify a generic contract, prove that a generic contract handles a difficult case, or exercise source-scope custody. It may not create a new generic rule merely because the rule is convenient for Redox.

## Required direction of authority

```text
subject-wide Chemistry contracts / registries
        ↓
generic engineering + Blueprint engines
        ↓
topic manifest / source scope / stress fixture
        ↓
Redox (or any other topic) execution
        ↓
PASS / FAIL / blocker evidence
```

The reverse direction is forbidden:

```text
Redox fixture
        ✕
        ↓
hard-coded generic branch
        ✕
        ↓
subject-wide authority
```

## Generic-engine constraints

Generic production engines must be driven by stable IDs, contracts, registries, manifests, capability/gate data, source-scope records and explicit policy inputs.

They must not:

- branch on a topic name such as `REDOX`;
- import a golden/stress fixture as producer authority;
- open a committed golden/fixture path internally to obtain production semantics;
- infer Chemistry scope from what happens to exist in a stress case;
- promote stress-test success into canonical subject authority.

Topic-specific data belongs at the edge of the system. The generic engine receives it through a contract and treats it as data.

## What a stress test can legitimately change

A failing stress test can justify a **generic** change only when the defect is stated independently of the topic and the resulting rule is expressible over generic contract fields.

Examples of acceptable defect classes include:

- an unresolved prerequisite was silently ignored;
- a source-scope tier leaked into an unauthorized product;
- a required representation was not realized;
- a closure receipt became stale after authority changed;
- a product omitted a mandatory CCBOM object.

The repair must be written against the relevant generic object (`gate`, `manifest`, `source_scope`, `CCBOM`, `TTU`, `custody`, etc.), not against a Redox identifier.

## Pull-request consolidation

`chemistry-pr-consolidation.v1.json` is the current machine-readable migration ledger. Its purpose is to prevent useful generic controls from being lost while reducing the number of simultaneously evolving Chemistry draft PRs.

No PR should be closed solely because a newer PR exists. A supersession requires one of:

1. the useful authority/mechanism is already present in the active lineage;
2. it has been explicitly ported and validated;
3. it is intentionally retained only as regression/migration evidence.

## Current target stack

```text
#371 Blueprint architecture
  ↓
#384 complete technical gate registry
  ↓
#381 Engineering Workbench
  ↓
#385 Redox stress test (non-authoritative)
```

#385 remains a stress test even if it eventually passes every machine and human product gate. Passing Redox does not prove that Chemistry architecture is complete; it proves only the declared generic contracts against that stress case.
