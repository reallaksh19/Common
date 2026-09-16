# V2.5 completion architecture

## Status

This document is the normative completion architecture for Engineering Relay V2.5 in PR #396.

```text
WP-00 Kernel baseline / object matrix               DELIVERED — CP-R001
WP-01 Semantic Execution Package                    DELIVERED — CP-R002
WP-02 Baton readiness + Takeover Certification      DELIVERED — CP-R003
WP-03 Strong phase/boundary qualification           DELIVERED — CP-R004
WP-04 Full progress / handover / next-work          CURRENT FRONTIER
```

CP-R004/status verification passed corrected workflow **35099657641** on `e3dd0c7d14b2958a65427935303f481bc17a8b5d` before WP-04 activation.

Conversation is acceleration, never custody.

## Governing relay

```text
OWNER INTENT / ODR
    ↓
OVERALL ROADMAP
    ↓
EXECUTABLE FRONTIER
    ↓
SEMANTIC EP / APPROVED PARALLEL PLAN
    ├── DSTEP-* discovery contract
    └── QSET-* when qualification is required
    ↓
BATON_READY
    ↓
ZERO-CONTEXT INCOMING CANDIDATE
    ├── DISC-* repository discovery evidence
    └── QUAL-* evaluated engineering evidence when required
    ↓
TC-* TAKEOVER CERTIFICATION
    ↓
TAKEOVER_CERTIFIED(route,candidate)
    ↓
MATERIAL_WRITE_READY(route,candidate,live Git)
    ↓
IMPLEMENTATION
    ↓
QUALITY / TEST / BENCHMARK EVIDENCE
    ↓
CHECKPOINT
    ↓
ROADMAP / PROGRESS / ISSUE RECONCILIATION
    ↓
STRUCTURED PROGRESS / HANDOVER PROJECTION      [WP-04]
    ↓
NEXT EP
```

## Authority separation

```text
Owner intent / ODR       authoritative intent
Overall Roadmap          authoritative plan/topology
EP / Parallel Plan       authorized forward slice
DSTEP-*                  forward discovery requirements
QSET-*                   prepared qualification criteria
DISC-*                   candidate discovery evidence
QUAL-*                   evaluated engineering qualification evidence
TC-*                     route/candidate admission evidence
Live Git observation     runtime fact
CP                       backward execution truth
PROGRESS / ISSUE_GRAPH   reconciled repository state
Generated report/MD      projection only
GitHub                   external coordination projection
Chat                     non-authoritative convenience
```

No downstream repository is a Common implementation target. Real repositories can reveal generic failure modes only through read-only stress/validation unless separately authorized.

## Delivered WP-01 — semantic baton

Executable EPs are semantically validated for serial work and approved parallel lanes. They contain typed slice-specific inputs/oracles, executable `DSTEP-*` discovery, bounded scope, structured anti-drift, exact implementation mappings, source-aware report payload requirements and durable successor outputs. `REPO_PROFILE` and the pinned relay-protocol basis are part of conformance.

Current-slice unresolved requirements can withhold execution; future/informational items do not recreate an everything-is-blocked workflow.

## Delivered WP-02 — readiness and candidate admission

### BATON_READY

Repository-wide and candidate-independent. It proves the repository contains a complete zero-context baton before a future replacement exists.

### TAKEOVER_CERTIFIED(route,candidate)

Route/candidate-specific. It requires current `BATON_READY`, a current PASS `DISC-*`, a current PASS `TC-*`, and a current PASS `QUAL-*` when the EP declares a qualification boundary. Evidence is revalidated against the current roadmap, route, EP/profile/predecessor digests and material basis.

### PROJECTION_READY / HANDOVER_READY

```text
PROJECTION_READY = required external projections represent current repository truth
HANDOVER_READY   = BATON_READY AND PROJECTION_READY
```

### MATERIAL_WRITE_READY

Runtime-only:

```text
TAKEOVER_CERTIFIED
AND live route matches
AND live Git/material basis acceptable
AND drift/continuity permits WRITE
AND material_authority == WRITE
AND execution.can_continue
AND no active hard stop
```

`material_authority: WRITE` alone never authorizes a candidate.

## Delivered WP-03 — strong engineering qualification

Qualification is required when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

A material boundary includes substantial changes in production path, engineering authority, numerical method, protected invariant, input authority, or verification/oracle class.

The durable transaction is:

```text
EP.qualification_boundary
 -> QSET-* prepared by outgoing agent
 -> candidate Q1–Q5 answers with zero chat custody
 -> independent/deterministic evaluation
 -> QUAL-* PASS/FAIL
 -> TC-* cites exact QUAL id/path/digest
 -> TAKEOVER_CERTIFIED
```

Q1–Q5 enforce:

```text
Q1 actual production/source trace
Q2 engineering reconstruction; concrete values for quantitative work
Q3 mutation + protected invariant + exact falsifier
Q4 independent benchmark/oracle verification
Q5 exact first safe change + predicted verification
```

QSET/QUAL bind to the exact route, roadmap revision, work package and semantic EP digest. The candidate cannot prepare its own QSET or act as its own independent evaluator. Deterministic evaluation requires explicit deterministic expected outputs. QUAL PASS requires PASS evaluation and durable basis for every question. Changing QUAL evidence invalidates a TC through receipt-digest binding.

Inline `phase_transition.questions` is retired as an executable qualification contract.

Qualification is admission evidence, not material write authority.

## Current WP-04 — progress, handover, and exact next work

WP-04 establishes truthful complete information architecture before WP-07 simplifies Owner language.

### Source authority

Progress and reports derive from:

```text
OVERALL_ROADMAP
PROGRESS
EP / approved lane EP
CP
DISC / QSET / QUAL / TC when relevant
ISSUE_GRAPH
REPO_STATE only for lifecycle/routing facts it owns
```

Generated reports never become a competing source of truth.

### Required hierarchy

```text
Overall
  Objective
    Phase
      Work Package
        Task / implementation step
          Acceptance Criterion
```

Human-report percentages/state must be calculated or reconciled from authoritative objects. Unverified mirrored `REPO_STATE.progress.phase_percent` / `ep_percent` values must not control handover output.

### Exact next work

The relay must produce ordered successor actions with:

```text
order
action
targets
inputs
tests/oracles
acceptance IDs
expected result
stop/reconciliation conditions
qualification-boundary flag
```

A single vague `next_action` string is insufficient as the successor work contract.

### Structured report projection

A report declares source bindings. If its contents disagree with the source objects, it is stale/invalid and must be regenerated. It never overrides roadmap, EP, CP, progress, issue or certification authority.

## Remaining target layers

```text
WP-05  GitHub Program Projection operations
WP-06  Quality Procedure Library + QRV-* evidence
WP-07  Human Communication / Owner projection
WP-08  Owner Change Intake over ODR/roadmap transactions
WP-09  End-to-end lifecycle and A -> B -> C zero-chat certification
WP-10  schema/template/validator/renderer/docs self-consistency audit
WP-11  PR readiness; never automatic merge
```

## Object namespaces

```text
DSTEP-xxxx  EP discovery instruction
DISC-xxxx   Discovery Receipt
QSET-xxxx   Qualification Question Set
QUAL-xxxx   Qualification Receipt
TC-xxxx     Takeover Certification
QRV-xxxx    Quality Review             [WP-06]
CP-xxxx     Checkpoint
ODR-xxxx    Owner Decision Record
```

Existing plan/join/replan/drift namespaces remain unchanged.

## Defining release proof

WP-09 remains:

```text
AGENT A -> CHAT DELETED -> AGENT B -> CHAT DELETED -> AGENT C
```

Agent C must reconstruct Owner intent, roadmap position, predecessor facts/limitations, current task, inputs and editability, benchmarks/oracles, scope, quality obligations, tests, acceptance, staleness and exact next work from repository state alone and obtain current independent certification.

If prior conversation is materially required, V2.5 fails its release criterion.

## Validation evidence discipline

A whole-suite claim requires both explicit CI test surfaces on the claimed head:

```text
root unit discovery
synthetic tests/stress discovery
```

Historical workflow evidence is interpreted according to `ci-evidence-correction.md`.

## Implementation sequence

```text
baseline                         COMPLETE — CP-R001
semantic EP                      COMPLETE — CP-R002
baton readiness / TC             COMPLETE — CP-R003
strong qualification             COMPLETE — CP-R004
full progress/handover           CURRENT — WP-04
GitHub operations + quality      WAITING
human communication / intake     WAITING
end-to-end certification         WAITING
self-consistency audit           WAITING
PR readiness                     WAITING
```
