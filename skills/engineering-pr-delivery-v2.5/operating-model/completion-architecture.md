# V2.5 completion architecture

## Status

This document is the normative completion architecture for Engineering Relay V2.5 in PR #396.

```text
WP-00 Kernel baseline / object matrix               DELIVERED — CP-R001
WP-01 Semantic Execution Package                    DELIVERED — CP-R002
WP-02 Baton readiness + Takeover Certification      DELIVERED — CP-R003
WP-03 Strong phase/boundary qualification           DELIVERED — CP-R004
WP-04 Full progress / handover / next-work          DELIVERED — CP-R005
WP-05 GitHub Program Projection operations          DELIVERED — CP-R006
WP-06 Quality Procedure Library                     DELIVERED — CP-R007
WP-07 Human Communication                           CURRENT FRONTIER
```

CP-R007 checkpoint/status verification passed workflow **35147172696** on `d695329c5bf69fa6c127ae2b47dc35d99227631b`, including compile, 7 root units and 118 synthetic stress tests.

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
    ├── quality applicability router
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
APPLICABLE QUALITY PROCEDURES / TEST / BENCHMARK EVIDENCE
    ↓
QRV-* QUALITY REVIEW
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
EP / Parallel Plan       authorized forward slice, quality applicability, exact next work
DSTEP-*                  forward discovery requirements
QSET-*                   prepared qualification criteria
DISC-*                   candidate discovery evidence
QUAL-*                   evaluated engineering qualification evidence
TC-*                     route/candidate admission evidence
Live Git observation     runtime fact
QRV-*                    exact-basis quality review evidence
CP                       backward execution truth + QRV pointer
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

Fresh qualification is required for `PHASE_CHANGED` or `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`. The durable transaction is `EP.qualification_boundary -> QSET-* -> candidate answers -> independent/deterministic evaluation -> QUAL-* -> TC-*`. Q1 traces production/state authority, Q2 reconstructs the engineering problem with concrete values when quantitative, Q3 proves mutation/invariant/falsifier understanding, Q4 uses an independent oracle, and Q5 names the exact first safe change and predicted verification.

## Delivered WP-04 — source-derived progress, handover and next work

`PROGRESS.yaml` is authoritative through Acceptance Criterion -> Implementation Step -> EP -> Work Package -> Phase -> Objective -> Overall Roadmap. `REPO_STATE.progress` values are checked mirrors only. Every executable EP carries ordered `next_work.steps[]`. Report/status/handover derive from authority objects and cannot override them.

## Delivered WP-05 — crash-safe GitHub Program Projection operations

GitHub remains external coordination only. Immutable `GHGEN-*` generations contain stable `GHOP-*` operations `CREATE | LINK | UPDATE | PUBLISH_HANDOVER | SUPERSEDE | REVISE | CLOSE | REOPEN`. Every external mutation is durably marked `ATTEMPTED_UNCONFIRMED` before the call, then read back through `GITHUB_OBSERVATION` and reconciled. `ISSUE_GRAPH.github_state = ABSENT | OPEN | CLOSED | UNKNOWN`; native relationship success requires native provider verification.

## Delivered WP-06 — procedural quality and QRV evidence

Quality is routed before execution and evidenced before checkpoint. Every EP partitions all built-in quality procedures exactly once:

```text
software-design
coding
ui-ux
testing
engineering-numerics
code-review
accessibility
performance
migration
github-delivery
```

Applicable procedures require reason + review focus. Not-applicable procedures require a concrete reason but do not perform ceremonial review. Each blueprint defines WHEN TO APPLY, REQUIRED INPUTS, PROCEDURE, BEST-PRACTICE CHECKLIST, ANTI-PATTERNS, REQUIRED ARTIFACTS, VERIFICATION, QUALITY FINDING CLASSIFICATION, TRUE HARD-STOP CONDITIONS, OWNER REPORT and SUCCESSOR HANDOVER.

The durable quality transaction is:

```text
EP quality router
 -> applicable procedure execution
 -> QRV-* bound to EP digest / roadmap revision / material ref / router snapshot
 -> procedure results + QF-* findings
 -> execution-effect derivation
 -> exact unresolved-finding transfer
 -> checkpoint QRV id/path/digest
 -> derived report projection
```

Procedure results are `CLEAR | FINDINGS | NOT_RUN`. `NOT_RUN` may produce `NEEDS_ATTENTION` but does not automatically stop execution. Severity alone never grants stop authority. A `QF-*` finding can block only when it maps to an existing true hard-stop category with durable basis. Ordinary maintainability/design/UX/accessibility/performance/migration/test-gap concerns may remain visible and non-blocking.

Deferred, Owner-review-required and unresolved findings transfer exactly through QRV successor handover. A checkpoint cannot publish an executable successor while its QRV contains a true blocking finding. Parallel lane checkpoints use lane-specific QRVs.

Report projection source-binds checkpoint QRV id/digest and exposes QRV state/findings/execution effect/Owner report/transfer as derived information; generated reports never become quality authority.

WP-06 evidence:

```text
pre-checkpoint implementation
  c5a3f8dfb9111081b15fef607dd2b6e7ba8ae868
  workflow 35146877546 — PASS

CP-R007 checkpoint/status
  d695329c5bf69fa6c127ae2b47dc35d99227631b
  workflow 35147172696 — PASS

root units: 7
stress tests: 118
```

## Current WP-07 — Human Communication

WP-07 is the sole material frontier. It must derive separate technical and Owner-facing communication from the same authoritative report projection without creating a second truth source.

The Owner view must explain in plain language:

- what the system can do now;
- what it will not change;
- why the current work exists;
- what evidence exists and what is missing;
- material quality concerns without relay jargon;
- roadmap/progress changes;
- exact next work;
- any genuine Owner decision required.

Technical status may retain relay terminology. Owner status must translate it rather than hiding it.

## Remaining target layers

```text
WP-07 Human Communication / Owner projection       CURRENT
WP-08 Owner Change Intake over ODR transactions    WAITING
WP-09 End-to-end A -> B -> C certification         WAITING
WP-10 self-consistency audit                       WAITING
WP-11 PR readiness; never automatic merge          WAITING
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
QRV-xxxx    Quality Review
QF-xxxx     Quality Finding
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
GitHub operations                COMPLETE — CP-R006
quality procedures               COMPLETE — CP-R007
human communication              CURRENT — WP-07
owner change intake              WAITING
end-to-end certification         WAITING
self-consistency audit           WAITING
PR readiness                     WAITING
```
