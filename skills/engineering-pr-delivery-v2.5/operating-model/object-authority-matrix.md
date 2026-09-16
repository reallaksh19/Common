# V2.5 object / authority matrix

## Purpose

This is the WP-00 baseline map for the catch-up/completion roadmap. It distinguishes authoritative state, forward work contracts, backward evidence, candidate certification, and generated projections. It is intentionally explicit about which target objects are **not yet implemented**.

Legend:

```text
KEEP        current kernel concept is retained
STRENGTHEN  current concept remains but semantic contract must deepen
REPLACE     current behavior/meaning will be replaced by a stronger contract
ADD         target object does not yet exist in the kernel
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
EP / APPROVED PARALLEL PLAN
        |
        +--> BATON semantic validation
        |
        v
candidate DISC / QUAL / TC
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

## Core matrix

| Object / concept | Role | Authority class | Producer | Primary consumers | Current validator / mechanism | Target action |
| --- | --- | --- | --- | --- | --- | --- |
| Owner Decision Record (`ODR`) | Explicit Owner intent/disposition | AUTHORITATIVE OWNER DECISION | Owner-directed transaction | Roadmap revisions, execution authority, change intake | `validate_owner_decision.py` | KEEP |
| `OVERALL_ROADMAP.yaml` | Program/objective/phase/WP topology and status | AUTHORITATIVE PLAN | Roadmap transaction | Frontier, progress, EP generation, issue projection | roadmap/frontier/transaction validators | KEEP |
| Roadmap revision | Immutable mutation receipt | AUTHORITATIVE HISTORY | Roadmap transaction | Continuity, progress, issue projection | `validate_roadmap_transaction.py` | KEEP |
| Roadmap continuity receipt | Active-EP disposition across revisions | AUTHORITATIVE EXECUTION RECONCILIATION | Reconciliation transaction | Active EP, write authority | `validate_roadmap_continuity.py` | KEEP |
| Executable frontier | Derived eligible WP set | DERIVED FROM ROADMAP | Deterministic computation | EP/parallel router | frontier validators | KEEP |
| Execution Package (`EP`) | One-WP forward executable contract | AUTHORITATIVE FOR AUTHORIZED SLICE under roadmap | EP producer | Candidate, execution, CP | structural/self-contained/acceptance validators | STRENGTHEN — WP-01 semantic contract |
| Parallel Plan | Owner-approved multi-WP router | AUTHORITATIVE EXECUTION ROUTER under roadmap | Owner-approved plan transaction | Lane EP selection, join/replan | parallel-plan validator | KEEP |
| Parallel Join Receipt | Multi-parent convergence baton | AUTHORITATIVE CONVERGENCE HISTORY | Join transaction | Integration EP | join validator | KEEP |
| Parallel Replan Receipt | Retire invalid topology + transfer custody | AUTHORITATIVE REPLAN HISTORY | Replan transaction | Replacement EP/plan | replan validator | KEEP |
| Drift Receipt | Base movement classification | AUTHORITATIVE RECONCILIATION EVIDENCE | Git/reconciliation procedure | Material authority | drift validator | KEEP |
| Git observation | Live branch/worktree/material/base fact | LIVE OBSERVATION | Runtime command | Write readiness | route/context scripts | KEEP |
| Checkpoint (`CP`) | Backward truth of one EP result | AUTHORITATIVE EXECUTION HISTORY | Completing agent | Roadmap/progress/issues/successor | checkpoint/linkage validators | KEEP |
| Progress Basis | Denominator/numerator basis | AUTHORITATIVE CALCULATION BASIS | Roadmap/progress transaction | Progress projection | progress validator | KEEP |
| `PROGRESS.yaml` | Calculated progress state | DERIVED / RECONCILED | Progress calculation | Owner/reporting | progress validator | KEEP; deepen task/AC projection in WP-04 |
| `ISSUE_GRAPH.yaml` | Repository model of GitHub coordination relationships | AUTHORITATIVE REPOSITORY PROJECTION MODEL, not roadmap authority | Issue reconciliation | GitHub operations/reporting | issue graph/closure/supersession validators | KEEP; operationalize in WP-05 |
| Projection generation state | Desired/observed external publication state | AUTHORITATIVE PUBLICATION CUSTODY | Projection transaction | Handover readiness | projection validator | KEEP |
| State planes | Execution/quality/evidence/stop truth dimensions | AUTHORITATIVE CURRENT STATE SUMMARY when reconciled to sources | Relay reconciliation | Human/machine views | state-plane validator | KEEP |
| `repository_ready` kernel field | Existing repository-recovery boolean | CURRENT KERNEL SUMMARY | Current reconciliation | Handover | projection/readiness validator | REPLACE SEMANTICS — split into BATON_READY vs candidate certification in WP-02 |
| `projection_ready` kernel field | External projection current | SUMMARY | Projection reconciliation | Handover | projection validator | MAP TO `PROJECTION_READY` in WP-02 |
| `handover_ready` kernel field | Current combined repository+projection readiness | SUMMARY | Relay reconciliation | Owner/handover | projection validator | MAP TO `HANDOVER_READY = BATON_READY AND PROJECTION_READY` |
| `BATON_READY` | Repository baton semantically complete for unknown future successor | TARGET SUMMARY PREDICATE | Baton semantic validators | Outgoing handover, incoming TC | not yet implemented | ADD — WP-02 |
| Discovery contract in EP | Questions/actions replacement must execute | FORWARD CONTRACT | EP producer | Incoming candidate | current EP structural validation only | STRENGTHEN — WP-01 |
| Discovery Receipt (`DISC`) | Candidate's durable independent repository discovery result | CANDIDATE EVIDENCE | Incoming candidate | TC/evaluator | not yet implemented | ADD — WP-02 |
| Qualification Question Set | Prepared technical admission criteria | FORWARD CONTRACT | Outgoing relay | Incoming candidate/evaluator | current Q1-Q5 validator | STRENGTHEN — WP-03 |
| Qualification Receipt (`QUAL`) | Candidate answers + independent evaluation | CANDIDATE EVIDENCE / ADMISSION BASIS | Incoming candidate + evaluator | TC/write readiness | not yet implemented | ADD — WP-03 |
| Takeover Certification (`TC`) | Candidate-specific proof of takeover | CANDIDATE CERTIFICATION | Independent evaluator/deterministic validators | Write readiness | not yet implemented | ADD — WP-02 |
| `TAKEOVER_CERTIFIED` | Candidate-specific certification predicate | TARGET SUMMARY PREDICATE | TC reconciliation | Write readiness | not yet implemented | ADD — WP-02 |
| `MATERIAL_WRITE_READY` | Final permission predicate for current candidate | TARGET SUMMARY PREDICATE | Runtime reconciliation | Engineering write action | current material_authority/live checks only | ADD — WP-02 |
| Quality applicability | Which blueprints apply and why | FORWARD CONTRACT | EP producer | Quality reviewer | current quality section | STRENGTHEN — WP-06 |
| Quality Review (`QRV`) | Applied quality procedures/findings | EXECUTION EVIDENCE | Agent/reviewer | CP/report/Owner | not yet implemented | ADD — WP-06 |
| Structured report | Reconciled machine report of source objects | DERIVED PROJECTION | Generator | Owner/technical renderers | current report contract only | REPLACE as generated/reconciled projection — WP-04/WP-07 |
| `OWNER_STATUS.md` | Plain-language Owner view | DERIVED PROJECTION | Renderer | Owner | current status/handover renderer | ADD/REPLACE — WP-07 |
| `TECHNICAL_STATUS.md` | Machine/engineering-detail view | DERIVED PROJECTION | Renderer | Engineers/agents | current status renderer | ADD/REPLACE — WP-07 |
| `HANDOVER.md` | Successor/Owner custody projection | DERIVED PROJECTION | Renderer | Owner/successor | current handover renderer | STRENGTHEN — WP-04/WP-07 |
| Chat conversation | Convenience context only | NON-AUTHORITATIVE | User/agent | None required for custody | `chat_context_required: false` | KEEP NON-AUTHORITY |

## Source-of-truth rules

1. Owner intent and applied ODRs govern intent changes.
2. The Overall Roadmap governs engineering plan/topology.
3. EP/Parallel Plan governs the currently authorized execution slice but cannot redefine roadmap intent.
4. Candidate DISC/QUAL/TC objects prove candidate admission; they cannot rewrite the EP or roadmap.
5. Checkpoints record what actually happened; they cannot silently redefine Owner intent.
6. Progress and issue graph are reconciled repository state derived from roadmap/execution facts.
7. GitHub is an external coordination projection, not an alternate roadmap authority.
8. Structured reports and generated Markdown are projections. If they disagree with source objects, they are stale/invalid.
9. Conversation is never custody.

## Replacement map

The catch-up revamp intentionally replaces only weak semantics:

```text
key-presence EP validation
    -> semantic EP validation

repository_ready inferred mainly from lifecycle
    -> BATON_READY from semantic baton proof

candidate understanding implicit in cold-start
    -> DISC + QUAL + TC candidate admission

section-name report validation
    -> source-reconciled structured report contract

Q1-Q5 metadata grounding only
    -> question set + evaluated QUAL receipt

single technical/control-plane renderer
    -> technical projection + plain-language Owner projection
```

The roadmap, serial/parallel control model, exact-head evidence, drift/continuity, checkpoint custody, progress basis, issue relationship model, and projection-generation idempotency remain foundations rather than targets for replacement.

## WP-00 audit completion criteria

Before WP-00 can checkpoint complete, this matrix must be reconciled against the actual branch contents and augmented with any object/script that was missed. In particular, the audit must identify:

- fields no validator consumes;
- validators with no producing transaction;
- templates that do not match validators;
- renderers using retired fields;
- duplicate readiness/authority concepts;
- generated projections that can accidentally become writable truth;
- object paths/namespaces that collide or are ambiguous.

This initial matrix is the architecture baseline, not evidence that WP-00 has already passed.