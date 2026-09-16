# V2.5 catch-up / completion roadmap

## Purpose

This roadmap completes the operational relay on top of the existing V2.5 control-plane kernel. It is not a rewrite of V2 and not a replacement of the strong roadmap/parallel/issue/projection machinery already implemented.

Sequencing remains strict:

> First make the baton trustworthy. Then independently prove that a replacement can pick it up. Then prove engineering qualification. Only then build full progress/handover, GitHub operations, quality procedures, and human-facing projections.

PR #396 remains draft throughout this roadmap. No downstream repository is an implementation target; real repositories remain read-only stress sources unless separately authorized.

## Current program state

```text
CP-R001  WP-00 Kernel baseline / object matrix      COMPLETE
   |
   v
CP-R002  WP-01 Semantic Execution Package           COMPLETE
   |
   v
CP-R003  WP-02 Baton readiness / Takeover Cert      COMPLETE
   |
   v
CP-R004  WP-03 Strong qualification                 COMPLETE*
   |
   v
WP-04    Full progress / handover / next-work       CURRENT FRONTIER*
```

`*` CP-R004 is content-complete and the program has been reconciled to the WP-04 successor, but formal checkpoint validity still requires corrected exact-head CI on the head containing CP-R004 and this program-state update. Until that run passes, do not claim WP-04 material execution has begun.

WP-01 made the forward baton semantic. WP-02 separated candidate-independent baton readiness from candidate admission and live write permission. WP-03 now adds evaluated engineering qualification through `QSET-* -> QUAL-* -> TC-*`.

## Progress Basis

| Work package | Weight | Status |
| --- | ---: | --- |
| WP-00 Kernel baseline / object matrix | 5 | COMPLETE — CP-R001 |
| WP-01 Semantic Execution Package | 18 | COMPLETE — CP-R002 |
| WP-02 Baton readiness + Takeover Certification | 18 | COMPLETE — CP-R003 |
| WP-03 Strong phase/boundary qualification | 12 | COMPLETE* — CP-R004 |
| WP-04 Full progress / handover / next-work contract | 12 | CURRENT FRONTIER* |
| WP-05 GitHub Program Projection operations | 8 | WAITING |
| WP-06 Quality Procedure Library | 10 | WAITING |
| WP-07 Human Communication | 6 | WAITING |
| WP-08 Owner Change Intake | 3 | WAITING |
| WP-09 End-to-end Relay Certification Matrix | 5 | WAITING |
| WP-10 Self-consistency Audit | 2 | WAITING |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

After CP-R004 passes corrected exact-head CI, earned completion is **53/100 = 53%**. Progress remains acceptance/checkpoint-derived; weights define the denominator, not manually typed completion claims.

## CI evidence rule

A whole-suite completion claim requires both explicit test surfaces:

```text
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests -p 'test*.py' -v
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests/stress -p 'test*.py' -v
```

Historical interpretation is corrected in `ci-evidence-correction.md`. Compiling stress modules is not equivalent to executing the synthetic stress suite.

## Dependency topology

```text
WP-00 Kernel baseline          COMPLETE
   |
   v
WP-01 Semantic EP              COMPLETE
   |
   v
WP-02 Baton readiness / TC     COMPLETE
   |
   v
WP-03 Strong qualification     COMPLETE* — CP-R004
   |
   v
WP-04 Progress / Handover      CURRENT*
   |
   +---------------------------+
   |                           |
   v                           v
WP-05 GitHub Ops         WP-06 Quality Procedures
   |                           |
   +-------------+-------------+
                 |
                 v
        WP-07 Human Communication
                 |
                 v
        WP-08 Owner Change Intake
                 |
                 v
     WP-09 End-to-end Certification
                 |
                 v
       WP-10 Self-consistency Audit
                 |
                 v
          WP-11 PR Readiness
```

Serial execution remains the default. Defined future work is not executable work.

---

## WP-00 — Kernel baseline / object matrix — COMPLETE

Checkpoint: `completion-checkpoints/CP-R001.yaml`.

The baseline audit froze actual branch behavior, classified existing objects, retained the strong roadmap/parallel/issue/projection kernel, and assigned stable findings BA-001 through BA-013.

---

## WP-01 — Semantic Execution Package — COMPLETE

Checkpoint: `completion-checkpoints/CP-R002.yaml`.

Implementation report: `wp-01-semantic-ep.md`.

Delivered:

- semantic EP validation for serial active EPs and every approved parallel lane EP;
- `DSTEP-*` executable discovery instructions with `DISC-*` reserved for candidate evidence;
- typed slice-specific inputs and benchmark/oracle contracts;
- strong allowed-read/write, protected, prohibited and Owner-reserved scope;
- structured anti-drift and executable implementation mappings;
- source/reconciliation-aware report payload contracts;
- durable successor outputs;
- `REPO_PROFILE` admission and relay-protocol binding;
- repository-neutral negative regressions proving hollow EPs fail.

---

## WP-02 — Baton readiness + Takeover Certification — COMPLETE

Checkpoint: `completion-checkpoints/CP-R003.yaml`.

Delivered:

- candidate-independent `BATON_READY` derived from repository semantics rather than lifecycle;
- route-scoped `DISC-*` candidate Discovery Receipts;
- route/candidate-scoped `TC-*` Takeover Certification;
- candidate/preparer/evaluator independence rules;
- certification binding to roadmap/material basis plus semantic EP, repository-profile and predecessor-baton digests;
- route-scoped admissions for serial and approved parallel lanes;
- independent `PROJECTION_READY` and `HANDOVER_READY = BATON_READY AND PROJECTION_READY`;
- live-derived `MATERIAL_WRITE_READY` requiring current candidate certification plus current route/Git/write conditions;
- repository-neutral zero-context takeover proof;
- corrected CI that explicitly executes root units and `tests/stress/`.

---

## WP-03 — Strong phase / material-boundary qualification — COMPLETE*

Checkpoint: `completion-checkpoints/CP-R004.yaml`.

Implementation report: `wp-03-qualification.md`.

Delivered transaction:

```text
semantic EP
 -> qualification_boundary
 -> QSET-* Question Set prepared by outgoing agent
 -> zero-chat candidate answers
 -> independent/deterministic evaluation
 -> QUAL-* PASS/FAIL
 -> TC-* cites exact QUAL id/path/digest
 -> TAKEOVER_CERTIFIED(route,candidate)
```

Fresh qualification is required when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

Q1–Q5 now prove:

```text
Q1  actual production path / source trace
Q2  engineering reconstruction; concrete payload for quantitative work
Q3  authority/boundary mutation + protected invariant + exact falsifier
Q4  independent verification / benchmark reasoning
Q5  exact first safe implementation slice + predicted verification
```

QSET and QUAL are bound to the exact route, roadmap revision, work package and semantic EP digest. Candidate-authored criteria and candidate self-evaluation are rejected. Deterministic evaluation requires explicit deterministic expectations. QUAL mutation invalidates an already-issued TC through receipt-digest binding.

Inline `phase_transition.questions` is retired as an executable qualification contract.

Pre-checkpoint aligned evidence:

```text
head:     3e32dcc562651db019a0ff4e9cf48e4099ab43bd
workflow: 35098797964
compile:  PASS
units:    PASS
stress:   PASS — 99 discovered synthetic tests
```

Formal completion requires the final exact CP-R004/program-status head to pass the same corrected CI surfaces.

---

## WP-04 — Full progress / handover / next-work contract — CURRENT FRONTIER*

### Outcome

The Owner and a successor can see the complete project state and exact next work without reading raw YAML or trusting manually mirrored percentages.

### Authority requirements

Progress/reporting must derive from authoritative objects:

```text
OVERALL_ROADMAP
PROGRESS
EP / approved lane EP
CP
DISC / QUAL / TC when relevant
ISSUE_GRAPH
REPO_STATE only for lifecycle/routing facts that it actually owns
```

A generated report is a projection, not a new authority source.

### Required hierarchy

Render:

```text
Overall
  Objective
    Phase
      Work Package
        Task / implementation step
          Acceptance Criterion
```

Each useful level must expose calculated state/progress and evidence/disposition where applicable.

### Current execution projection

Show at minimum:

```text
current objective / phase / WP
current EP or approved lane
current implementation step
current acceptance/evidence state
current baton/takeover/write readiness as applicable
```

Do not treat unverified `REPO_STATE.progress.phase_percent` or `ep_percent` as human-report authority. Derive or reconcile them from `PROGRESS.yaml`, roadmap and EP/CP acceptance state.

### Detailed next-work contract

Replace dependence on a vague scalar `next_action` with ordered source-derived next work containing:

```text
order
action
targets
required inputs
required tests/oracles
acceptance IDs
expected result
stop/reconciliation conditions
phase/material-boundary qualification flag
```

### Structured report projection

Add a generated/reconciled structured report whose source bindings are explicit. If report content disagrees with source objects, the report is stale/invalid; it never overrides roadmap, EP, CP, progress, certification or issue truth.

### Acceptance direction

WP-04 should prove at least:

- stale phase/EP percentage mirrors cannot mislead the rendered handover;
- Objective -> Phase -> WP -> Step -> AC checklist is complete and source-derived;
- completed, active, pending, superseded and not-run evidence are represented without collapsing meanings;
- exact next work is structured and test/acceptance bound;
- report projection can be regenerated/reconciled idempotently from source objects;
- serial, reconciliation and approved-parallel states render without inventing a material task.

Owner-language simplification beyond basic clarity remains WP-07; WP-04 first establishes truthful complete information architecture.

---

## WP-05 — GitHub Program Projection operations

Operationalize repository-authoritative GitHub transactions:

```text
CREATE | LINK | UPDATE | PUBLISH HANDOVER | SUPERSEDE | REVISE | CLOSE | REOPEN
```

Use existing idempotent projection generations and reconcile receipts back into `ISSUE_GRAPH.yaml`.

---

## WP-06 — Quality Procedure Library

Turn existing blueprint principles into scoped procedures with applicability, required inputs, method, artifacts, verification, finding classification, true hard-stop conditions, Owner report, and successor duties. Applicable procedures produce `QRV-*` evidence. Quality findings do not automatically become hard stops.

---

## WP-07 — Human Communication

Generate distinct technical and plain-language Owner projections from the same authority objects. The Owner view explains capabilities, restrictions, evidence, gaps, roadmap effect, next work and genuine decisions without making control-plane vocabulary the primary interaction language.

---

## WP-08 — Owner Change Intake

Provide a human interface to ODR/roadmap mutation showing previous intent, new intent, retained/invalidated work, progress-basis effect, issue impact, active-EP disposition and new frontier. This does not replace ODR authority.

---

## WP-09 — End-to-end Relay Certification Matrix

Run representative lifecycle scenarios and the defining A -> B -> C zero-chat relay. Agent C must reconstruct material custody and obtain independent certification without prior conversation.

Representative scenarios include serial, continuity, reconciliation, parallel join/replan, stale projection, idle/terminal, phase transition, Owner intent mutation and issue supersession.

---

## WP-10 — Self-consistency Audit

Audit:

```text
schema <-> template
template <-> validator
validator <-> renderer
renderer <-> docs
docs <-> SKILL.md
object <-> producer/consumer
lifecycle <-> authority
progress <-> acceptance
issue <-> roadmap
certification <-> readiness
```

This WP also closes BA-003/BA-013 by proving declarative schema coverage complements—rather than replaces—procedural semantic validation.

---

## WP-11 — PR Readiness

Only after WP-09 and WP-10 pass:

- verify generic CI on exact head;
- verify V2 untouched;
- verify no downstream-specific logic;
- inspect every change outside the V2.5 skill tree;
- generate final architecture index/operator quick-start/representative relay example;
- update PR description to delivered semantics;
- perform final independent review.

Do not merge automatically.

## Anti-drift during catch-up

Do not spend material effort on downstream adoption, project-specific adapters, new engineering domains, cosmetic projection work, or merge preparation before the owning WP is current.

Every proposed addition should answer:

> Does this make a zero-context successor materially more capable of safely continuing the engineering project?

If not, it is outside the current frontier.

## Merge gate

PR #396 remains draft until the exact head proves all of the following:

```text
[x] Hollow EP fails semantic validation.
[x] Rich standalone EP passes.
[x] BATON_READY cannot be inferred from lifecycle.
[x] Candidate takeover requires current independent certification.
[x] Missing/stale TC prevents MATERIAL_WRITE_READY.
[x] Required qualification has an evaluated QUAL receipt.
[ ] Owner handover contains full roadmap/WP/task/AC progress.
[ ] Detailed ordered next work is rendered.
[x] EP exact return report contract is source/reconciliation aware.
[ ] Generated report is reconciled to source objects.
[ ] GitHub parent/child/supersession/closure operations are operationally defined.
[ ] Quality procedures produce scoped QRV artifacts.
[ ] Owner communication is plain-language by default.
[ ] Representative lifecycle cold-start/certification matrix passes.
[ ] Agent A -> B -> C zero-chat relay passes.
[ ] Schema/template/validator/renderer/docs audit is clean.
[ ] Final generic CI passes on exact release-candidate head.
[x] V2 remains untouched through WP-03.
[x] No downstream-specific logic exists through WP-03.
```
