# Relay conformance

Question: if the current conversation disappears immediately, can a competent replacement recover the correct roadmap position, locate a semantically complete baton, independently prove takeover, resolve the correct live execution route, and continue safely without hidden chat context or stale evidence?

## Kernel conformance today

The current PR #396 kernel validates:

- `REPO_STATE` lifecycle/routing and current roadmap revision;
- deterministic executable frontier;
- one serial EP or an Owner-approved parallel router covering that frontier;
- structural EP context, inputs/scope/acceptance/tests/report/successor duties;
- explicit Git execution basis and branch/worktree routing;
- drift and roadmap-continuity reconciliation;
- exact-head checkpoint evidence;
- deterministic progress and roadmap transactions;
- independent execution, quality, evidence and stop state;
- checkpoint/join/replan successor custody;
- issue graph/closure/supersession semantics;
- external projection convergence separately from repository recovery;
- no unauthorized parallel material work.

`cold_start_check.py` is stricter than structural conformance about hidden chat dependence, but the kernel does not yet provide the full candidate-specific takeover certification required by the completion architecture.

## Completion conformance target

The normative target is `operating-model/completion-architecture.md` and the implementation order is `operating-model/catchup-completion-roadmap.md`.

Completion conformance separates five predicates:

```text
BATON_READY
TAKEOVER_CERTIFIED
PROJECTION_READY
HANDOVER_READY
MATERIAL_WRITE_READY
```

A conforming completed relay must prove:

### Baton readiness

- authoritative roadmap/frontier is valid;
- one-WP EP/plan is semantically complete rather than merely structurally populated;
- predecessor custody is valid;
- current-slice input and benchmark/oracle contracts are complete;
- repository discovery is executable and receipt-producing;
- scope/protected/prohibited/anti-drift contracts are complete;
- implementation steps and exact report/successor payloads are executable without chat context.

`BATON_READY` is a property of the repository baton and must be decidable before a future replacement agent is known.

### Candidate takeover

The incoming candidate independently produces required discovery/qualification evidence and receives a current Takeover Certification on the exact roadmap/EP/Git-material basis.

The candidate does not author the criteria, answer them, and unilaterally declare itself qualified. Objective parts may be deterministically evaluated; engineering comprehension that cannot be mechanically proved needs a durable independent evaluation basis.

### Projection readiness

External GitHub/coordination projection is current independently of engineering repository truth. Projection lag does not erase a valid baton or candidate evidence.

### Handover readiness

```text
HANDOVER_READY = BATON_READY AND PROJECTION_READY
```

This is outgoing custody completeness, not candidate write permission.

### Material write readiness

```text
MATERIAL_WRITE_READY =
    TAKEOVER_CERTIFIED
AND live route valid
AND live Git/material basis valid
AND current drift/continuity permits WRITE
AND material_authority == WRITE
AND no active hard stop
```

An `ACTIVE` lifecycle is never sufficient proof of any of these predicates by itself.

## Live checkout boundary

Static repository files cannot prove the operator's current checkout. Before material writes, live route and Git context must still be resolved against the selected EP/plan.

## Reports and generated views

Reports, Owner status, technical status and handover Markdown are projections of authority objects. They do not become competing sources of truth. If a generated report disagrees with roadmap/EP/certification/checkpoint/progress/issue sources, the projection is stale or invalid.

## Defining release test

Completion requires an Agent A -> Agent B -> Agent C relay with chat custody deliberately removed between candidates. If Agent C needs prior conversation to reconstruct any material Owner intent, current task, input authority, benchmark/oracle, scope, evidence, quality obligation, next work or staleness condition, V2.5 completion fails.

A green generic suite proves reusable protocol checks executed successfully. It does not prove a particular downstream product, engineering calculation, release, or human UX acceptance.