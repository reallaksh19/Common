# V2.5 object / authority matrix

## Purpose

This is the living completion-program authority map. WP-00 established the baseline; WP-01 has now delivered the semantic EP/repository-admission changes. Target objects that remain unimplemented stay explicitly marked `ADD`.

Legend:

```text
KEEP        retain current concept and authority role
STRENGTHEN  retain concept but deepen validation/semantics
REPLACE     retire weak current behavior behind a stronger contract
DEPRECATE   remove as an authority mechanism after replacement is live
ADD         target object does not yet exist
DERIVED     projection only; never authority
```

## Authority hierarchy

```text
OWNER INTENT / ODR
        |
        v
OVERALL ROADMAP
        |
        v
EXECUTABLE FRONTIER
        |
        v
SEMANTIC EP / APPROVED PARALLEL PLAN
        |
        +--> DSTEP discovery contract
        |
        v
BATON semantic proof                 [WP-02 predicate still pending]
        |
        v
candidate DISC / QUAL / TC           [pending]
        |
        v
live route + material basis + write readiness
        |
        v
IMPLEMENTATION
        |
        v
QUALITY REVIEW + TEST/BENCHMARK EVIDENCE
        |
        v
CHECKPOINT
        |
        v
ROADMAP / PROGRESS / ISSUE RECONCILIATION
```

Generated reports and external projections sit downstream of these objects and may not override them.

## Current matrix after CP-R002

| Object / control | Role | Current enforcement / remaining gap | Classification | Next owner |
| --- | --- | --- | --- | --- |
| Owner Decision Record (`ODR`) | Explicit Owner intent/disposition | Dedicated validator; roadmap intent mutations bind to applied ODRs | KEEP | — |
| `OVERALL_ROADMAP.yaml` | Authoritative objectives/phases/WPs/dependencies/state | Roadmap/frontier/transaction validators | KEEP | — |
| Roadmap revision / continuity receipt | Mutation history + active-EP disposition | Dedicated transaction/continuity validation | KEEP | — |
| Executable frontier | Derived eligible WP set | Deterministic computation from roadmap | KEEP / DERIVED | — |
| `REPO_STATE.yaml` | Current route/batons/state summaries | Lifecycle/routing plus protocol binding enforced; readiness/progress mirrors still need later reconciliation | STRENGTHEN | WP-02 / WP-04 |
| `REPO_STATE.relay_protocol` | Pins protocol version/Common basis | `version: 2.5` + explicit non-placeholder `basis_ref` enforced procedurally and modeled in schema | KEEP | WP-10 schema audit |
| `REPO_PROFILE.yaml` | Repository discovery/profile metadata | Dedicated validator + aggregate-conformance admission | KEEP | WP-10 schema audit |
| Execution Package (`EP`) | One-WP forward executable contract | Structural + semantic validation now enforced for serial active EPs and parallel lane EPs | KEEP + future integration | WP-02 readiness |
| `DSTEP-*` discovery instruction | Forward executable repository-discovery contract | Namespace/action/question/outputs/receipt/failure behavior validated | KEEP | WP-02 consumes |
| Discovery Receipt (`DISC-*`) | Candidate's durable discovery result | Not implemented | ADD | WP-02 |
| Parallel Plan / Join / Replan | Owner-approved router, convergence, replan custody | Dedicated validators; lane EPs now also pass semantic EP validator | KEEP | — |
| Drift Receipt / live Git observation | Drift classification + live checkout facts | Dedicated static/runtime separation | KEEP | — |
| Checkpoint (`CP`) | Backward execution truth | Exact material basis + successor linkage | KEEP | — |
| Progress Basis / `PROGRESS.yaml` | Calculated progress authority/projection | Core calculation validated; phase/EP human mirrors remain weak | KEEP + STRENGTHEN projection | WP-04 |
| `ISSUE_GRAPH.yaml` | Repository model of GitHub coordination | Strong relationship/tree/closure/supersession validation | KEEP | WP-05 ops |
| Projection generation state | External publication custody | Generation/idempotency/staleness checks | KEEP | — |
| State planes | Execution/quality/evidence/stop dimensions | Strong separation and stop/write consistency | KEEP | — |
| `repository_ready` kernel field | Current repository-recovery summary | Still lifecycle-derived rather than semantic baton proof | REPLACE SEMANTICS | WP-02 |
| `projection_ready` | External projection-current summary | Current projection-state summary | MAP to `PROJECTION_READY` | WP-02 |
| `handover_ready` | Combined repository+projection summary | Still uses old repository-ready operand | REPLACE left operand with `BATON_READY` | WP-02 |
| `BATON_READY` | Complete baton for unknown future candidate | Not implemented | ADD | WP-02 |
| Takeover Certification (`TC-*`) | Candidate-specific admission proof | Not implemented | ADD | WP-02 |
| `TAKEOVER_CERTIFIED` | Candidate-specific predicate | Not implemented | ADD | WP-02 |
| `MATERIAL_WRITE_READY` | Final current-candidate write predicate | Distributed write checks exist; no candidate-certified aggregate predicate | ADD | WP-02 |
| Qualification Question Set | Prepared technical criteria | Q1-Q5 focus/anchors validated; answers/evaluation absent | STRENGTHEN | WP-03 |
| Qualification Receipt (`QUAL-*`) | Candidate answers + independent evaluation | Not implemented | ADD | WP-03 |
| `cold_start_check.py` | Repository-only reconstructability check | Aggregate conformance now includes semantic EP/profile/protocol checks; still not candidate certification | STRENGTHEN then subordinate | WP-02 |
| EP report contract | Exact return/reconciliation contract | Every mandatory heading now requires source objects + required fields | KEEP | WP-04 rendering |
| Structured generated report | Reconciled source-derived machine report | Not implemented | ADD / DERIVED | WP-04 |
| Quality blueprint applicability / `QRV-*` | Procedure routing + quality evidence | Current quality section/blueprints remain thin | STRENGTHEN / ADD | WP-06 |
| `render_status.py` / `render_handover.py` | Human/technical projections | Still control-plane-heavy; progress checklist incomplete | STRENGTHEN / split views | WP-04 / WP-07 |
| `OWNER_STATUS.md` | Plain-language Owner view | Not implemented | ADD / DERIVED | WP-07 |
| `TECHNICAL_STATUS.md` | Detailed engineering view | Not implemented | ADD / DERIVED | WP-07 |
| Declarative schema layer | Object-shape contracts | Updated for WP-01 objects but not executed generically by CI | STRENGTHEN | WP-10 |
| Procedural validator layer | Semantic/cross-object conformance | Primary enforcement layer; WP-01 adds EP semantics/profile admission/protocol binding | KEEP + STRENGTHEN | all WPs |
| CI workflow | Compile + complete unit/stress suite | Strong scoped guardrail; no generic schema runner yet | KEEP + STRENGTHEN | WP-10 |
| Chat conversation | Convenience context only | Explicitly non-authoritative | KEEP NON-AUTHORITY | — |

## WP-01 reconciliation of baseline findings

```text
BA-001 relay protocol pin not enforced        RESOLVED by WP-01
BA-002 REPO_PROFILE not admitted              RESOLVED by WP-01
BA-004 EP semantics too weak                  RESOLVED for forward EP contract by WP-01
BA-005 DISC/DSTEP namespace collision         RESOLVED for forward instruction namespace by WP-01
BA-006 cold start != candidate certification  SEMANTIC SIDE STRENGTHENED; certification remains WP-02
BA-009 report headings only                   EP CONTRACT RESOLVED; generated report reconciliation remains WP-04/WP-07
```

Still carried:

```text
BA-003 executable generic schema conformance  WP-10
BA-007 readiness predicates                   WP-02
BA-008 phase/EP progress mirrors              WP-04
BA-010 qualification receipt/evaluation       WP-03
BA-011 Owner/technical handover separation    WP-04/WP-07
BA-012 full quality procedures                WP-06
BA-013 procedural/schema layer audit          WP-10
```

## Source-of-truth rules

1. Owner intent and applied ODRs govern intent changes.
2. Overall Roadmap governs engineering plan/topology.
3. EP/Parallel Plan governs the currently authorized execution slice but cannot redefine roadmap intent.
4. `DSTEP-*` defines what an incoming candidate must discover; future `DISC/QUAL/TC` objects will record/evaluate candidate evidence and cannot rewrite roadmap/EP authority.
5. Checkpoints record what actually happened; they cannot silently redefine Owner intent.
6. Progress and issue graph remain reconciled repository state derived from roadmap/execution facts.
7. GitHub is an external coordination projection, not an alternate roadmap authority.
8. Report contracts define required return payload, while generated reports remain derived projections.
9. Conversation is never custody.
