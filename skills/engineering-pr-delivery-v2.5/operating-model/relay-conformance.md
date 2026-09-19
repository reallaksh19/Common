# Relay conformance

Question: if the current conversation disappears immediately, can a competent replacement recover the correct roadmap position, reconstruct all material engineering context from repository state, independently prove takeover, resolve the correct live execution route, and continue safely without hidden chat context or stale evidence?

## Aggregate conformance through CP-R010

V2.5 validates the complete repository-neutral relay stack:

- `REPO_STATE` lifecycle/routing and current roadmap revision;
- `REPO_PROFILE` and pinned relay-protocol basis;
- deterministic executable frontier;
- one serial semantic EP or an Owner-approved parallel router whose lane EPs are semantic;
- typed inputs/oracles, executable DSTEP discovery, scope/anti-drift/step/report/successor contracts;
- candidate-independent `BATON_READY`;
- route/candidate `DISC-*` discovery evidence;
- fresh `QSET-*` + independently/deterministically evaluated `QUAL-*` when phase or material qualification boundary changes;
- route/candidate `TC-*` admission and exact evidence/contract digests;
- explicit Git execution basis and branch/worktree routing;
- drift and roadmap-continuity reconciliation;
- live-derived `MATERIAL_WRITE_READY` rather than persisted write permission;
- exact-head checkpoint evidence and QRV linkage;
- calculated Objective → Phase → WP → EP → Step → AC progress and Progress Basis;
- source-bound report projection and structured ordered next work;
- applicability-routed quality procedures and `QRV-*` evidence;
- independent execution, quality, evidence and stop state planes;
- checkpoint/join/replan successor custody;
- issue graph/tree/closure/supersession semantics;
- crash-safe GitHub projection generations/operations and verified readback reconciliation;
- human communication convergence through one report/communication projection;
- Owner-change intake/reconciliation over ODR + roadmap transaction authority;
- repository-only `ZERO_CONTEXT_RECONSTRUCTION` for active routes and non-executable lifecycle states;
- no unauthorized parallel material work.

`validate_relay_conformance.py` is the aggregate static entrypoint. Focused validators remain available for diagnostics and runtime-gated operations.

`cold_start_check.py` is a repository-recovery diagnostic. It is not candidate admission authority: `DISC/QUAL/TC` establish candidate-specific takeover and `material_write_ready.py` supplies the live write gate.

## Readiness predicates

V2.5 deliberately separates repository custody, candidate admission, external projection currentness, and live write permission.

### BATON_READY

Candidate-independent repository property:

```text
valid roadmap/frontier
+ semantic current EP/plan
+ valid predecessor custody
+ admitted profile/protocol basis
+ current-slice inputs/oracles
+ executable discovery contract
+ scope/anti-drift/report/successor contract
+ current QSET when qualification is required
+ no conversation dependency
```

A repository may be baton-ready before any future candidate exists.

### TAKEOVER_CERTIFIED(route,candidate)

Candidate/route-specific:

```text
BATON_READY
+ current DISC PASS
+ current QUAL PASS when required
+ current TC PASS
+ exact route/roadmap/material/EP/profile/predecessor/qualification bindings
```

TC document self-preparation is allowed; self-evaluation is not. The candidate may assemble its own TC record, while certification authority remains with deterministic/Owner/independent evaluation plus current evidence validation. Editing the EP, profile, predecessor baton, qualification evidence, roadmap basis, or material basis invalidates stale certification through digest/reference checks.

### PROJECTION_READY

Every required external coordination projection represents current repository truth. Projection lag does not rewrite engineering truth.

### HANDOVER_READY

```text
HANDOVER_READY = BATON_READY AND PROJECTION_READY
```

This is outgoing custody completeness, not candidate write permission.

### MATERIAL_WRITE_READY

```text
MATERIAL_WRITE_READY(route,candidate,live_git) =
    TAKEOVER_CERTIFIED(route,candidate)
AND live route valid
AND live Git/material basis acceptable
AND current drift/continuity permits WRITE
AND material_authority == WRITE
AND execution.can_continue == true
AND no active hard stop
```

It is deliberately runtime-derived and never stored as a timeless boolean. `ACTIVE` lifecycle or persisted `material_authority: WRITE` alone does not authorize an agent.

Conversely, lack of candidate certification does not justify changing route-level `material_authority` to READ_ONLY. Candidate admission failure is represented by `TAKEOVER_CERTIFIED=false`; READ_ONLY is reserved for route/repository constraints such as reconciliation, drift confirmation, Owner/authority boundaries, or other non-candidate-specific write restrictions.

## Qualification boundary

Fresh qualification is required when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

The durable transaction is:

```text
EP.qualification_boundary
→ QSET-* prepared by predecessor/authorized preparer
→ incoming candidate repository-only answers
→ independent/deterministic evaluation
→ QUAL-* PASS/FAIL
→ TC-* cites exact QUAL id/path/digest
```

Q1 traces production/state authority, Q2 reconstructs the engineering problem with concrete quantitative payload when applicable, Q3 establishes mutation/invariant/falsifier understanding, Q4 uses an independent oracle, and Q5 identifies the exact first safe implementation slice and predicted verification.

## Live checkout boundary

Static repository files cannot prove the operator's current checkout. Before material writes, run route/Git inspection and `material_write_ready.py --candidate-id ...` against the live repository.

A drift receipt authorizes only the observed transition it validates. Historical drift classification cannot authorize a later base movement.

## Progress, reports, and human views

`PROGRESS.yaml` is authoritative calculated progress through acceptance → step → EP → WP → phase → objective → overall.

`report_projection.py` derives structured status/acceptance/scope/next-work truth from repository authorities. `communication_projection.py` derives both technical and Owner-facing views from that same report projection. `owner_change_projection.py` derives change-impact reporting from ODR + roadmap transaction + current reconciliation.

Generated `REPORT`, `HANDOVER`, `TECHNICAL_STATUS.md`, `OWNER_STATUS.md`, `OWNER_CHANGE.md`, and roadmap/status Markdown are disposable projections. A disagreement with roadmap/EP/certification/checkpoint/progress/issue/QRV sources makes the projection stale; it never makes the source wrong.

## Quality and evidence

Every executable EP explicitly partitions the quality procedure library into applicable and not-applicable procedures. Applicable procedures produce exact-basis QRV evidence before checkpoint publication.

`NOT_RUN` remains evidence/quality truth rather than an automatic stop. Severity alone cannot create a hard stop. A blocking quality finding requires an existing hard-stop category plus durable basis.

## External GitHub projection

When GitHub coordination is required, current repository desired state is represented by an immutable `GHGEN-*` with stable `GHOP-*` operations. The publisher journals `ATTEMPTED_UNCONFIRMED` before external mutation, reads the external state back, and reconciles only verified observation into `ISSUE_GRAPH`/projection state.

Connector response alone is not convergence, body links are not native relationship proof, and superseded generations lose retry authority.

## Zero-context release proof — CP-R010

The defining release test is implemented and passing:

```text
Agent A with conversation
  → completes WP-A
  → persists CP-A / EP-B / QSET-B
  → conversation deleted
Agent B repository-only
  → reconstructs current route/context
  → DISC / QUAL / TC PASS
  → completes WP-B
  → persists CP-B / EP-C / QSET-C
  → conversation deleted
Agent C repository-only
  → reconstructs current route/context
  → independent QUAL / TC PASS
```

The stricter repository-only regression discards predecessor helper/process return values: B and C reopen persisted repository files and derive their own certification inputs. Agent C must recover task purpose, Owner decisions, predecessor facts/limitations, uncertainty, input authority/editability, benchmark/oracle, allowed/protected/prohibited scope, quality obligations/findings, evidence present/missing, tests/acceptance, first action, stale conditions, and exact next work.

Lifecycle certification covers `ACTIVE`, `ACTIVE + RECONCILING`, `PARALLEL`, `ACTIVE + required projection STALE`, `IDLE`, and `TERMINAL`; `INITIALIZING` remains covered by bootstrap/core tests. Recovery never invents WRITE authority.

## Current completion boundary

The functional relay through the end-to-end zero-chat proof is delivered through `CP-R010`.

```text
WP-01 semantic EP / repository admission        COMPLETE
WP-02 BATON_READY / DISC / TC / live write gate COMPLETE
WP-03 QSET / QUAL engineering qualification     COMPLETE
WP-04 progress / report / exact next work       COMPLETE
WP-05 crash-safe GitHub projection              COMPLETE
WP-06 quality procedures / QRV                  COMPLETE
WP-07 Owner + technical communication           COMPLETE
WP-08 Owner change intake                       COMPLETE
WP-09 A → B → C zero-chat certification         COMPLETE
WP-10 cross-surface self-consistency audit       CURRENT
WP-11 final PR readiness                         WAITING
```

A green generic suite proves the repository-neutral protocol checks executed successfully. It does not substitute for a downstream product, numerical, release, or human-acceptance validation.
