# V2.5 catch-up / completion roadmap

## Purpose

This roadmap completes the operational relay on top of the existing V2.5 control-plane kernel. It is not a rewrite of V2 and not a replacement of the strong roadmap/parallel/issue/projection machinery already implemented.

Sequencing remains strict:

> First make the baton trustworthy. Then independently prove that a replacement can pick it up. Only then expand qualification, handover/progress, GitHub operations, quality procedures, and human-facing projections.

PR #396 remains draft throughout this roadmap. No downstream repository is an implementation target; real repositories remain read-only stress sources unless separately authorized.

## Current program state

```text
CP-R001  WP-00 Kernel baseline / object matrix      COMPLETE
   |
   v
CP-R002  WP-01 Semantic Execution Package           COMPLETE
   |
   v
WP-02    Baton readiness + Takeover Certification   CURRENT FRONTIER
```

WP-01 has delivered semantic EP validation, DSTEP discovery instructions, typed current-slice inputs/oracles, strong scope/anti-drift/implementation/report contracts, REPO_PROFILE admission, and relay-protocol binding. WP-02 must now prove independent candidate takeover without weakening those contracts.

## Progress Basis

| Work package | Weight | Status |
| --- | ---: | --- |
| WP-00 Kernel baseline / object matrix | 5 | COMPLETE — CP-R001 |
| WP-01 Semantic Execution Package | 18 | COMPLETE — CP-R002 |
| WP-02 Baton readiness + Takeover Certification | 18 | CURRENT FRONTIER |
| WP-03 Strong phase/boundary qualification | 12 | WAITING |
| WP-04 Full progress / handover / next-work contract | 12 | WAITING |
| WP-05 GitHub Program Projection operations | 8 | WAITING |
| WP-06 Quality Procedure Library | 10 | WAITING |
| WP-07 Human Communication | 6 | WAITING |
| WP-08 Owner Change Intake | 3 | WAITING |
| WP-09 End-to-end Relay Certification Matrix | 5 | WAITING |
| WP-10 Self-consistency Audit | 2 | WAITING |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

After CP-R002 is validated on the final exact head, earned completion is **23/100 = 23%**. Progress remains acceptance/checkpoint-derived; weights define the denominator, not manually typed completion claims.

## Dependency topology

```text
WP-00 Kernel baseline          COMPLETE
   |
   v
WP-01 Semantic EP              COMPLETE
   |
   v
WP-02 Baton readiness + Takeover Certification
   |
   v
ZERO-CONTEXT TAKEOVER PROOF
   |
   v
WP-03 Strong qualification
   |
   v
WP-04 Progress / Handover
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

- semantic EP validator used by serial aggregate conformance and parallel lane admission;
- `DSTEP-*` executable discovery instructions with `DISC-*` reserved for candidate evidence;
- typed inputs with current-slice applicability/resolution and executable-state rules;
- typed benchmark/oracle contracts;
- allowed-write/read, protected, prohibited and Owner-reserved scope;
- structured anti-drift;
- exact implementation-step mappings;
- source/reconciliation-aware report payload contracts;
- durable successor outputs;
- dedicated `REPO_PROFILE` validation in aggregate conformance;
- enforced `relay_protocol.version/basis_ref` binding;
- repository-neutral negative regressions proving hollow EPs fail.

WP-01 intentionally does not create candidate certification. That is the current WP-02 frontier.

---

## WP-02 — Baton readiness + Takeover Certification — CURRENT FRONTIER

### Outcome

Separate three questions that the old kernel partially conflates:

```text
1. Did the outgoing agent leave a complete repository baton?
2. Did this incoming candidate independently prove takeover?
3. Is this candidate allowed to write engineering state right now?
```

### Predicates

Implement:

```text
BATON_READY
TAKEOVER_CERTIFIED
PROJECTION_READY
HANDOVER_READY
MATERIAL_WRITE_READY
```

Target semantics:

```text
BATON_READY = semantic repository baton proof
HANDOVER_READY = BATON_READY AND PROJECTION_READY
TAKEOVER_CERTIFIED = current candidate has valid DISC/QUAL/TC basis
MATERIAL_WRITE_READY = TAKEOVER_CERTIFIED + live route/git/write authority + no hard stop
```

Lifecycle alone must never imply `BATON_READY`.

### Candidate Discovery Receipt

Add durable `DISC-*` candidate evidence bound to:

- candidate identity;
- EP/parallel lane or integration route;
- roadmap revision;
- predecessor baton;
- exact material/Git basis;
- executed `DSTEP-*` instructions and observed outputs.

### Takeover Certification

Add durable `TC-*` certification with:

```text
candidate
prepared_by
evaluated_by
basis
DISC result
QUAL result when required
verdict
staleness/invalidation conditions
```

Self-certification is not allowed. Deterministic validators may certify objective facts; non-mechanical engineering-comprehension claims require a durable independent evaluation basis.

### Invalidation

Certification becomes stale when a relevant change occurs in:

- roadmap/current WP contract;
- EP or parallel route;
- predecessor checkpoint/join/replan baton;
- branch/material/base basis;
- current-required input or benchmark/oracle contract;
- allowed/protected/prohibited/Owner-reserved scope;
- qualification basis.

### Mandatory proof before WP-03

Run an actual repository-neutral zero-context takeover against a semantically rich EP. A fresh candidate must discover and reconstruct the current slice from repository state alone and receive current certification. Do not start WP-03 until this passes.

---

## WP-03 — Strong phase / material-boundary qualification

### Outcome

Qualification proves technical understanding rather than question metadata.

Fresh qualification is required when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

The transaction is:

```text
QUESTION_SET
 -> candidate answers
 -> independent evaluation
 -> QUAL-* receipt
 -> Takeover Certification reconciliation
```

Q1–Q5 prove production trace, engineering reconstruction where applicable, boundary/falsifier understanding, independent verification, and exact first safe slice.

---

## WP-04 — Full progress / handover / next-work contract

### Outcome

The Owner and successor can see the complete project state without reading YAML.

Required hierarchy:

```text
Overall -> Objective -> Phase -> Work Package -> Task / implementation step -> Acceptance Criterion
```

Render calculated progress, current execution, acceptance/evidence, and detailed ordered next work from source objects. Retire unverified `phase_percent`/`ep_percent` mirrors as human-report authority.

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
[ ] BATON_READY cannot be inferred from lifecycle.
[ ] Candidate takeover requires current independent certification.
[ ] Missing/stale TC prevents MATERIAL_WRITE_READY.
[ ] Required qualification has an evaluated QUAL receipt.
[ ] Owner handover contains full roadmap/WP/task/AC progress.
[ ] Detailed ordered next work is rendered.
[x] EP exact return report contract is source/reconciliation aware.
[ ] Generated report is reconciled to source objects.
[ ] GitHub parent/child/supersession/closure operations are defined.
[ ] Quality procedures produce scoped QRV artifacts.
[ ] Owner communication is plain-language by default.
[ ] Representative lifecycle cold-start/certification matrix passes.
[ ] Agent A -> B -> C zero-chat relay passes.
[ ] Schema/template/validator/renderer/docs audit is clean.
[ ] Final generic CI passes on exact release-candidate head.
[x] V2 remains untouched through WP-01.
[x] No downstream-specific logic exists through WP-01.
```
