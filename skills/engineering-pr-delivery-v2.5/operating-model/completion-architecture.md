# V2.5 completion architecture

## Status

Engineering Relay V2.5 through WP-09 was merged by explicitly authorized PR #396 at `fb28a0817cab109a1120e3826ce11439b49586de`. WP-10/WP-11 completion work continues on draft PR #409.

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
WP-09 End-to-end Relay Certification Matrix         DELIVERED — CP-R010
WP-10 Self-consistency Audit                        CONDITIONAL — CP-R011 exact-head CI pending
WP-11 PR Readiness                                  WAITING
```

Conversation is acceleration, never custody.

## Governing relay

```text
OWNER INTENT / ODR
    ↓
OVERALL ROADMAP + ROADMAP REVISION
    ↓
EXECUTABLE FRONTIER
    ↓
SEMANTIC EP / OWNER-APPROVED PARALLEL PLAN
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
SOURCE-DERIVED REPORT / COMMUNICATION / OWNER-CHANGE PROJECTIONS
    ↓
ZERO_CONTEXT_RECONSTRUCTION
    ↓
NEXT EP / JOIN / REPLAN / IDLE / TERMINAL
```

## Authority separation

```text
Owner intent / ODR          authoritative intent
Overall Roadmap             authoritative plan/topology
Roadmap revision            authoritative mutation transaction
EP / Parallel Plan          authorized current slice
DSTEP-*                     forward discovery requirements
QSET-*                      prepared qualification criteria
DISC-*                      candidate discovery evidence
QUAL-*                      evaluated qualification evidence
TC-*                        route/candidate admission evidence
Live Git observation        runtime fact
QRV-*                       exact-basis quality evidence
CP                          backward execution truth
PROGRESS                    calculated progress authority
ISSUE_GRAPH                 repository coordination truth
REPO_STATE                  lifecycle/routing/bootstrap locator + checked mirrors
GHGEN/GHOP                  desired external GitHub transaction
GITHUB_OBSERVATION          verified external readback evidence
Report/communication/change derived projections only
ZERO_CONTEXT_RECONSTRUCTION derived repository-only recovery projection
GitHub UI                    external coordination projection
Chat                         non-authoritative convenience
```

No downstream repository is a Common implementation target. Real repositories may reveal generic failure modes only through read-only validation unless separately authorized.

## Delivered invariants

### Semantic baton

Executable EPs are semantically validated for typed slice inputs/oracles, executable discovery, bounded scope/anti-drift, exact implementation mappings, acceptance/tests, quality routing, report payloads, and exact ordered next work. `REPO_PROFILE` and protocol basis are part of admission.

### Readiness and takeover

`BATON_READY` is candidate-independent. `TAKEOVER_CERTIFIED(route,candidate)` requires current route/candidate DISC/QUAL/TC evidence. `HANDOVER_READY = BATON_READY AND PROJECTION_READY`. `MATERIAL_WRITE_READY` is live-derived from current certification, route/Git basis, drift/continuity, WRITE authority, execution continuation, and stop state; persisted WRITE alone never authorizes a candidate.

### Engineering qualification

Fresh qualification is required for `PHASE_CHANGED` or `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`. The durable transaction is `EP.qualification_boundary → QSET-* → candidate answers → independent/deterministic evaluation → QUAL-* → TC-*`.

### Progress and handover

`PROGRESS.yaml` is authoritative through acceptance criterion → implementation step → EP → WP → phase → objective → overall roadmap. `REPO_STATE.progress` values are checked mirrors. Report/status/handover derive from authority objects and cannot override them.

### Crash-safe GitHub projection

Immutable `GHGEN-*` generations contain stable `GHOP-*` operations. External mutation is journaled `ATTEMPTED_UNCONFIRMED` before the provider call, then verified by readback before ISSUE_GRAPH/repository reconciliation. Unknown outcomes are reconciled before retry; superseded generations lose retry authority.

### Procedural quality and QRV

Every EP partitions the full built-in quality library. Applicable procedures require reason + review focus; explicit non-applicability requires reason. `QRV-*` binds exact EP/material/router basis. `NOT_RUN` remains evidence/quality truth, severity alone cannot create a stop, and unresolved findings transfer exactly.

### Human communication

A single source-derived communication projection produces `TECHNICAL_STATUS.md` and plain-language `OWNER_STATUS.md`. Material truth—scope, evidence gaps, quality risk, decisions, stops, progress, and exact next work—cannot be hidden or promoted into competing authority.

### Owner Change Intake

Owner intent changes use ODR semantic intent plus `OWNER_INTENT_MUTATION` roadmap revision. The derived Owner-change view exposes before/after concept, retained/invalidated behavior, new scope, roadmap/progress/issue effects, active-work disposition, resulting frontier, and applied state without becoming another authority source.

### Zero-chat release certification — CP-R010

The defining A → B → C proof crosses three dependency-ordered work packages. B and C reopen persisted repository artifacts after prior process/chat custody is discarded, reconstruct material context, and independently produce current DISC/QUAL/TC evidence. Lifecycle certification covers ACTIVE, RECONCILING, PARALLEL, stale required projection, IDLE, and TERMINAL; INITIALIZING remains covered by bootstrap/core tests.

CP-R010's final canonical predecessor head `581735fb302cae9a1d8ccd0d518c3a463bb68a4c` passed workflow `35192761449`: compile, 7 root units, 135 stress tests.

## WP-10 — cross-surface consistency

WP-10 adds a deterministic release guard instead of a one-time prose audit:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/self_consistency_audit.py .
```

It checks YAML contract parseability, durable-object surfaces, quality blueprint procedure structure, aggregate/focused validator reachability, renderer/operator documentation, authority vocabulary, generic portability, and CI coverage.

The initial red run (`35197070033`) exposed stale CP-R002-era authority/conformance docs, missing zero-context/operator reachability, lack of a stable quality model, and audit-definition false positives. Those were resolved. Corrected head `3beae3849550fb0cd28abe658c63d1d770d9d3fa` passed workflow `35197671662` with self-consistency `0 warning(s)`, 7 root units, and 135 stress tests. Documentation-aligned head `f741a54da9e22e6a2f75aa15f54fd53563ee69de` passed workflow `35197914544`.

`CP-R011` now exists. Formal WP-10 closure and 99% earned completion require exact-head CI on CP-R011 plus the reconciled completion-program state.

## Current object namespaces

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

## Remaining target

```text
CP-R011 exact-head verification
   ↓
WP-11 PR Readiness
   ↓
100% completion + explicit Owner merge decision for PR #409
```

PR #409 remains draft. There is no automatic merge gate in the skill.
