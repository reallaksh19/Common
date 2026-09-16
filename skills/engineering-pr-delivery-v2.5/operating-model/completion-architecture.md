# V2.5 completion architecture

## Status

This document is the normative completion architecture for Engineering Relay V2.5 in PR #396.

```text
WP-00 Kernel baseline / object matrix               DELIVERED — CP-R001
WP-01 Semantic Execution Package                    DELIVERED — CP-R002
WP-02 Baton readiness + Takeover Certification      DELIVERED — CP-R003
WP-03 Strong phase/boundary qualification           DELIVERED — CP-R004
WP-04 Full progress / handover / next-work          DELIVERED — CP-R005; exact-head CI pending
WP-05 GitHub Program Projection operations          CONDITIONAL NEXT FRONTIER
```

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
PROGRESS                  authoritative calculated progress hierarchy
ISSUE_GRAPH               reconciled issue coordination state
REPO_STATE                lifecycle/routing/state-plane/bootstrap locator
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

Fresh qualification is required for `PHASE_CHANGED` or `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`. The durable transaction is:

```text
EP.qualification_boundary
 -> QSET-* prepared by outgoing agent
 -> candidate Q1-Q5 answers with zero chat custody
 -> independent/deterministic evaluation
 -> QUAL-* PASS/FAIL
 -> TC-* cites exact QUAL id/path/digest
 -> TAKEOVER_CERTIFIED
```

Q1 traces production/state authority, Q2 reconstructs the engineering problem with concrete values when quantitative, Q3 proves mutation/invariant/falsifier understanding, Q4 uses an independent oracle, and Q5 names the exact first safe change and predicted verification. Candidate-authored criteria/self-evaluation fail and changed QUAL evidence invalidates an issued TC.

## Delivered WP-04 — source-derived progress, handover and next work

### Progress authority

The hierarchy is now:

```text
Acceptance Criterion
 -> Implementation Step
 -> EP
 -> Work Package
 -> Phase
 -> Objective
 -> Overall Roadmap
```

`PROGRESS.yaml` is authoritative. It must cover every roadmap Objective/Phase/WP plus the active EP, implementation steps and acceptance criteria. Acceptance rows carry status and durable basis. `REPO_STATE.progress` percentages are compatibility/location mirrors only and must agree with the authoritative rows.

`progress_projection.py` builds the derived hierarchy used by generated views.

### Exact next work

Every executable semantic EP carries ordered `next_work.steps[]` containing:

```text
order
action
targets
inputs
tests
benchmarks/oracles
acceptance IDs
expected result
stop/reconciliation conditions
```

The execution state-plane `next_action` remains a short machine hint; it is not the successor work package.

### Structured report projection

`report_projection.py` derives report state from repository authority objects and records source digests for repository state, roadmap, progress, issue graph, EP and checkpoint. `validate_report_projection.py` participates in aggregate conformance. `render_report_projection.py`, `render_status.py` and `render_handover.py` consume derived state.

Generated YAML/Markdown never becomes writable truth. A source change causes regeneration/source-digest change; stale generated output cannot override authority objects.

### Handover

The handover renders Objective -> Phase -> WP -> Step -> AC percentages/status/basis plus exact ordered next work. Existing parallel-plan, join and replan custody remains visible. Bootstrap emits complete zero-weight roadmap progress without fabricating an EP; parallel convergence reconciles integration progress before cold start.

WP-07 still owns the separate plain-language Owner communication layer; WP-04 establishes truthful complete content first.

## Conditional next WP-05 — GitHub Program Projection operations

GitHub remains an external coordination projection. WP-05 will operationalize:

```text
CREATE | LINK | UPDATE | PUBLISH_HANDOVER | SUPERSEDE | REVISE | CLOSE | REOPEN
```

Operations must be prepared durably, published with stable generation identity, receipt-backed, verified, reconciled into `ISSUE_GRAPH.yaml`, and idempotent across crash/retry. Parent/subissue and evidence-preserving supersession/closure semantics already delivered by the kernel remain authoritative; WP-05 adds the operating transaction, not a second issue model.

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

Agent C must reconstruct Owner intent, roadmap position, predecessor facts/limitations, current task, inputs/editability, benchmarks/oracles, scope, quality obligations, tests, acceptance, progress, staleness and exact next work from repository state alone and obtain current independent certification. If prior conversation is materially required, V2.5 fails.

## Validation evidence discipline

A whole-suite claim requires both root unit discovery and dedicated synthetic stress discovery on the claimed exact head. Historical workflow evidence is interpreted according to `ci-evidence-correction.md`.

## Implementation sequence

```text
baseline                         COMPLETE — CP-R001
semantic EP                      COMPLETE — CP-R002
baton readiness / TC             COMPLETE — CP-R003
strong qualification             COMPLETE — CP-R004
full progress/handover           COMPLETE — CP-R005; exact-head CI pending
GitHub operations                NEXT after CP-R005 CI
quality procedures               WAITING
human communication / intake     WAITING
end-to-end certification         WAITING
self-consistency audit           WAITING
PR readiness                     WAITING
```
