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
WP-07 Human Communication                           DELIVERED — CP-R008
WP-08 Owner Change Intake                           DELIVERED — CP-R009
WP-09 End-to-end Relay Certification Matrix         CURRENT FRONTIER
```

CP-R009 checkpoint/status verification passed workflow **35188484127** on `2edfa74b0e27f88e895354211a4a4ed2c8d09e91`, including compile, 7 root units and 131 synthetic stress tests.

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
SOURCE-DERIVED REPORT PROJECTION
    ↓
COMMUNICATION PROJECTION
    ├── TECHNICAL_STATUS.md
    └── OWNER_STATUS.md
    ↓
OWNER CHANGE PROJECTION WHEN APPLICABLE
    └── OWNER_CHANGE.md
    ↓
NEXT EP
```

## Authority separation

```text
Owner intent / ODR        authoritative intent, including semantic change_intake for INTENT_MUTATION
Overall Roadmap           authoritative plan/topology
Roadmap revision          authoritative structural mutation transaction
EP / Parallel Plan        authorized forward slice, quality applicability, exact next work
DSTEP-*                   forward discovery requirements
QSET-*                    prepared qualification criteria
DISC-*                    candidate discovery evidence
QUAL-*                    evaluated engineering qualification evidence
TC-*                      route/candidate admission evidence
Live Git observation      runtime fact
QRV-*                     exact-basis quality review evidence
CP                        backward execution truth + QRV pointer
PROGRESS                  authoritative calculated progress hierarchy
ISSUE_GRAPH               reconciled issue coordination state
REPO_STATE                lifecycle/routing/state-plane/bootstrap locator
GHGEN/GHOP                desired external GitHub projection transaction
GitHub observation        verified external readback evidence
Report projection         derived structured projection only
Communication projection  derived human-facing projection only
Owner-change projection   derived Owner-change projection only
OWNER_STATUS.md           generated plain-language projection only
TECHNICAL_STATUS.md       generated technical projection only
OWNER_CHANGE.md           generated change-impact projection only
GitHub                    external coordination projection
Chat                      non-authoritative convenience
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

Quality is routed before execution and evidenced before checkpoint. Every EP partitions all built-in quality procedures exactly once. Applicable procedures require reason + review focus; explicit not-applicable procedures require reason without ceremonial execution. `QRV-*` is bound to EP digest, roadmap revision, material ref and router snapshot. `NOT_RUN` remains evidence/quality truth rather than automatic stop, and severity alone never grants stop authority. Deferred/unresolved findings transfer exactly through successor handover and checkpoints bind QRV by id/path/digest.

## Delivered WP-07 — source-derived human communication

WP-07 adds no authority plane. It derives one shared communication projection from the source-derived report projection. Technical status retains protocol precision; Owner status communicates current capability, purpose, protected/non-change scope, evidence/missing evidence, quality/limitations, roadmap/progress, exact next work, genuine Owner decisions and active stops in ordinary language. Owner-reserved scope does not fabricate a decision request, and non-blocking quality risk does not become a fake stop.

## Delivered WP-08 — Owner Change Intake

WP-08 adds no second change authority. Material Owner-intent change is represented as:

```text
Owner source
 -> ODR-* decision + change_intake semantic summary
 -> OWNER_INTENT_MUTATION roadmap revision
 -> roadmap / Progress Basis / issue / active-EP reconciliation
 -> owner_change_projection.py
 -> OWNER_CHANGE.md
```

`ODR.change_intake` records previous concept, requested concept, retained behavior, invalidated behavior and new scope. The roadmap revision remains authoritative for actual added/removed/changed/unaffected topology, Progress Basis change, issue reconciliation and resulting frontier.

For a current applied Owner mutation, conformance requires:

- an APPLIED ODR of kind `INTENT_MUTATION`;
- concrete change-intake semantics;
- exact ODR/revision linkage;
- current Progress Basis equal to `progress_basis_change.new_basis`;
- `frontier_after` equal to the computed resulting frontier;
- explicit active-work disposition;
- visible issue reconciliation when affected issues are named.

A CAPTURED ODR may be rendered for discussion but cannot claim a post-change frontier or applied status. Derived current-EP dispositions are `NO_ACTIVE_EP | PENDING_OWNER_CHANGE | INVALIDATED | RECONCILE_REQUIRED | CONTINUE_UNCHANGED`; `UNCLASSIFIED` fails an applied current change.

WP-08 evidence:

```text
documentation-aligned implementation
  fb5e0b15f25884793e38ba694505b748acaf84fd
  workflow 35188301698 — PASS

CP-R009 checkpoint/status
  2edfa74b0e27f88e895354211a4a4ed2c8d09e91
  workflow 35188484127 — PASS

root units: 7
stress tests: 131
```

## Remaining target layers

```text
WP-09 End-to-end A -> B -> C certification         CURRENT
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

WP-09 is now current and remains the defining release proof: `AGENT A -> CHAT DELETED -> AGENT B -> CHAT DELETED -> AGENT C`. Agent C must reconstruct Owner intent, roadmap position, predecessor facts/limitations, current task, inputs/editability, benchmarks/oracles, scope, quality obligations, tests, acceptance, progress, staleness and exact next work from repository state alone and obtain current independent certification. If prior conversation is materially required, V2.5 fails.

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
human communication              COMPLETE — CP-R008
owner change intake              COMPLETE — CP-R009
end-to-end certification         CURRENT — WP-09
self-consistency audit           WAITING
PR readiness                     WAITING
```
