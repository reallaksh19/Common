# V2.5 completion architecture

## Status

This document is the normative completion architecture for Engineering Relay V2.5 in PR #396.

```text
WP-00 Kernel baseline / object matrix               DELIVERED — CP-R001
WP-01 Semantic Execution Package                    DELIVERED — CP-R002
WP-02 Baton readiness + Takeover Certification      DELIVERED — CP-R003
WP-03 Strong phase/boundary qualification           DELIVERED — CP-R004
WP-04 Full progress / handover / next-work          DELIVERED — CP-R005
WP-05 GitHub Program Projection operations          DELIVERED — CP-R006, exact-head CI pending
WP-06 Quality Procedure Library                     NEXT after CP-R006 CI PASS
```

WP-05 pre-checkpoint implementation verification passed corrected workflow **35140358167** on `f63fbf8fbf71a3ad24ce0fd57e4e97a584d8c02b`.

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
    ├── QSET-* when qualification is required
    └── structured next_work.steps[]
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
CRASH-SAFE EXTERNAL PROJECTION TRANSACTION
    ↓
SOURCE-DERIVED REPORT / HANDOVER PROJECTION
    ↓
NEXT EP
```

## Authority separation

```text
Owner intent / ODR       authoritative intent
Overall Roadmap          authoritative plan/topology
EP / Parallel Plan       authorized forward slice and exact next-work contract
DSTEP-*                  forward discovery requirements
QSET-*                   prepared qualification criteria
DISC-*                   candidate discovery evidence
QUAL-*                   evaluated engineering qualification evidence
TC-*                     route/candidate admission evidence
Live Git observation     runtime fact
CP                       backward execution truth
PROGRESS                 authoritative calculated progress hierarchy
ISSUE_GRAPH              reconciled issue coordination state
REPO_STATE               lifecycle/routing/state-plane/bootstrap locator
GHGEN/GHOP                desired external GitHub projection transaction
GitHub observation       verified external readback evidence
Report projection / MD   derived projection only
GitHub                   external coordination projection
Chat                     non-authoritative convenience
```

No downstream repository is a Common implementation target. Real repositories can reveal generic failure modes only through read-only stress/validation unless separately authorized.

## Delivered WP-01 — semantic baton

Executable EPs are semantically validated for serial work and approved parallel lanes. They contain typed slice-specific inputs/oracles, executable `DSTEP-*` discovery, bounded scope, structured anti-drift, exact implementation mappings, source-aware report payload requirements and durable successor outputs. `REPO_PROFILE` and the pinned relay-protocol basis are part of conformance.

## Delivered WP-02 — readiness and candidate admission

`BATON_READY` is repository-wide and candidate-independent. `TAKEOVER_CERTIFIED(route,candidate)` requires current candidate/route DISC/TC and QUAL when applicable. `HANDOVER_READY = BATON_READY AND PROJECTION_READY`. `MATERIAL_WRITE_READY` is live-derived from current certification, route/Git basis, drift/continuity, WRITE authority, execution continuation and stop state. A persisted WRITE enum alone never authorizes a candidate.

## Delivered WP-03 — strong engineering qualification

Fresh qualification is required for `PHASE_CHANGED` or `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`. The durable transaction is `EP.qualification_boundary -> QSET-* -> candidate answers -> independent/deterministic evaluation -> QUAL-* -> TC-*`. Q1 traces production/state authority, Q2 reconstructs the engineering problem with concrete values when quantitative, Q3 proves mutation/invariant/falsifier understanding, Q4 uses an independent oracle, and Q5 names the exact first safe change and predicted verification. Candidate-authored criteria/self-evaluation fail and changed QUAL evidence invalidates an issued TC.

## Delivered WP-04 — source-derived progress, handover and next work

`PROGRESS.yaml` is authoritative through Acceptance Criterion -> Implementation Step -> EP -> Work Package -> Phase -> Objective -> Overall Roadmap. `REPO_STATE.progress` values are checked mirrors only. Every executable EP carries ordered `next_work.steps[]`. `report_projection.py`, status and handover derive from authority objects and cannot override them.

## Delivered WP-05 — crash-safe GitHub Program Projection operations

GitHub remains external coordination only. The current desired GitHub generation is an immutable `GHGEN-*` object containing ordered stable `GHOP-*` operations:

```text
CREATE | LINK | UPDATE | PUBLISH_HANDOVER | SUPERSEDE | REVISE | CLOSE | REOPEN
```

The durable transaction is:

```text
select current GHOP
 -> persist ATTEMPTED_UNCONFIRMED before external write
 -> perform external mutation
 -> create durable GITHUB_OBSERVATION from readback
 -> verify desired issue state / relationship / operation marker
 -> reconcile ISSUE_GRAPH and projection readiness
```

A missing connector response never proves the mutation did not occur. An uncertain CREATE must be reconciled by the stable `GHOP-*` marker/locator before retry. Verified readback may recover a lost connector receipt using explicit recovery evidence.

`ISSUE_GRAPH.github_state` is last verified external reality:

```text
ABSENT | OPEN | CLOSED | UNKNOWN
```

OPEN/CLOSED require a verified locator. ABSENT has no locator. UNKNOWN preserves a prior locator when external state must be re-observed.

A successor `GHGEN-*` can supersede an obsolete generation while retaining its attempt/receipt history. Old unfinished operations lose retry authority. Projection history distinguishes before-publication, attempted-with-unknown-outcome, and published-but-unconfirmed supersession.

Native parent/sub-issue and other GitHub relationship success may be claimed only if the provider/integration can create and read back that native relationship. A Markdown link or prose reference is not native relationship convergence.

Aggregate relay conformance validates the current GitHub generation and its history. `PROJECTION_READY` becomes true only after the current generation is fully reconciled.

WP-05 pre-checkpoint evidence: head `f63fbf8fbf71a3ad24ce0fd57e4e97a584d8c02b`, workflow **35140358167**, compile + root units + 111 stress tests PASS.

## Next target — WP-06 Quality Procedure Library

After CP-R006 exact-head CI passes, WP-06 is the sole material frontier. It must add applicability-routed procedural blueprints and first-class `QRV-*` Quality Review evidence while preserving the existing separation between quality findings, evidence state and true hard stops.

Each blueprint must contain:

```text
WHEN TO APPLY
REQUIRED INPUTS
PROCEDURE
BEST-PRACTICE CHECKLIST
ANTI-PATTERNS
REQUIRED ARTIFACTS
VERIFICATION
QUALITY FINDING CLASSIFICATION
TRUE HARD-STOP CONDITIONS
OWNER REPORT
SUCCESSOR HANDOVER
```

Quality must improve engineering rather than recreate blocker-heavy flows.

## Remaining target layers

```text
WP-06  Quality Procedure Library + QRV-* evidence   NEXT after CP-R006 CI PASS
WP-07  Human Communication / Owner projection       WAITING
WP-08  Owner Change Intake over ODR transactions    WAITING
WP-09  End-to-end A -> B -> C certification         WAITING
WP-10  self-consistency audit                       WAITING
WP-11  PR readiness; never automatic merge          WAITING
```

## Object namespaces

```text
DSTEP-xxxx  EP discovery instruction
DISC-xxxx   Discovery Receipt
QSET-xxxx   Qualification Question Set
QUAL-xxxx   Qualification Receipt
TC-xxxx     Takeover Certification
GHGEN-xxxx  GitHub projection generation
GHOP-xxxx   GitHub projection operation
QRV-xxxx    Quality Review             [WP-06]
CP-xxxx     Checkpoint
ODR-xxxx    Owner Decision Record
```

Existing plan/join/replan/drift namespaces remain unchanged.

## Defining release proof

WP-09 remains `AGENT A -> CHAT DELETED -> AGENT B -> CHAT DELETED -> AGENT C`. Agent C must reconstruct Owner intent, roadmap position, predecessor facts/limitations, current task, inputs/editability, benchmarks/oracles, scope, quality obligations, tests, acceptance, progress, staleness and exact next work from repository state alone and obtain current independent certification. If prior conversation is materially required, V2.5 fails.

## Validation evidence discipline

A whole-suite claim requires both root unit discovery and dedicated synthetic stress discovery on the claimed exact head. Historical workflow evidence is interpreted according to `ci-evidence-correction.md`.

## Implementation sequence

```text
baseline                         COMPLETE — CP-R001
semantic EP                      COMPLETE — CP-R002
baton readiness / TC             COMPLETE — CP-R003
strong qualification             COMPLETE — CP-R004
full progress/handover           COMPLETE — CP-R005
GitHub operations                COMPLETE — CP-R006, exact-head CI pending
quality procedures               NEXT after CP-R006 CI PASS
human communication / intake     WAITING
end-to-end certification         WAITING
self-consistency audit           WAITING
PR readiness                     WAITING
```
