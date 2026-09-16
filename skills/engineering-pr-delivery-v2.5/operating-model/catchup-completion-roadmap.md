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
CP-R003  WP-02 Baton readiness / Takeover Cert      COMPLETE
   |
   v
WP-03    Strong phase / material qualification      CURRENT FRONTIER
```

WP-01 made the forward baton semantic. WP-02 then separated candidate-independent `BATON_READY` from route/candidate-specific `TAKEOVER_CERTIFIED`, added `DISC-*` and `TC-*` evidence, and made `MATERIAL_WRITE_READY` a live-derived gate. WP-03 now owns evaluated engineering qualification.

## Progress Basis

| Work package | Weight | Status |
| --- | ---: | --- |
| WP-00 Kernel baseline / object matrix | 5 | COMPLETE — CP-R001 |
| WP-01 Semantic Execution Package | 18 | COMPLETE — CP-R002 |
| WP-02 Baton readiness + Takeover Certification | 18 | COMPLETE — CP-R003 |
| WP-03 Strong phase/boundary qualification | 12 | CURRENT FRONTIER |
| WP-04 Full progress / handover / next-work contract | 12 | WAITING |
| WP-05 GitHub Program Projection operations | 8 | WAITING |
| WP-06 Quality Procedure Library | 10 | WAITING |
| WP-07 Human Communication | 6 | WAITING |
| WP-08 Owner Change Intake | 3 | WAITING |
| WP-09 End-to-end Relay Certification Matrix | 5 | WAITING |
| WP-10 Self-consistency Audit | 2 | WAITING |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

After CP-R003 passes corrected exact-head CI, earned completion is **41/100 = 41%**. Progress remains acceptance/checkpoint-derived; weights define the denominator, not manually typed completion claims.

## CI evidence rule

The workflow must execute both explicit test surfaces:

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
WP-03 Strong qualification     CURRENT
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

---

## WP-02 — Baton readiness + Takeover Certification — COMPLETE

Checkpoint: `completion-checkpoints/CP-R003.yaml`.

Delivered:

- candidate-independent `BATON_READY` derived from repository baton semantics rather than lifecycle;
- route-scoped `DISC-*` candidate Discovery Receipts covering required `DSTEP-*` outputs;
- route/candidate-scoped `TC-*` Takeover Certification with explicit candidate, preparer and evaluator identity;
- prohibition of candidate self-preparation/self-certification;
- certification binding to roadmap/material basis plus semantic EP, `REPO_PROFILE` and predecessor-baton digests;
- exact route-scoped admissions for serial and approved parallel lanes;
- `PROJECTION_READY` kept independent from baton/candidate state;
- `HANDOVER_READY = BATON_READY AND PROJECTION_READY`;
- live-derived `MATERIAL_WRITE_READY`, which requires current candidate certification plus live route/Git context, write authority and no active hard stop;
- zero-context synthetic takeover proof;
- qualification-required routes cannot use TC to bypass missing `QUAL-*` evidence;
- corrected CI explicitly executes both root units and `tests/stress/`.

`TAKEOVER_CERTIFIED` and `MATERIAL_WRITE_READY` are route/candidate scoped, not misleading repository-global booleans.

---

## WP-03 — Strong phase / material-boundary qualification — CURRENT FRONTIER

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

### Required engineering content

Q1–Q5 must prove:

```text
Q1  actual production path / source trace
Q2  concrete engineering reconstruction where applicable
Q3  boundary/authority mutation plus falsifier
Q4  independent verification / benchmark reasoning
Q5  exact first safe implementation slice plus predicted verification result
```

A question pack is not enough. The candidate answers must be durably evaluated.

### Required binding

`QUAL-*` evidence must bind to:

- candidate identity;
- exact incoming EP/route;
- roadmap revision and work package;
- relevant material/engineering basis;
- the question-set identity and technical-boundary trigger;
- independent evaluator/deterministic oracle basis where applicable.

A relevant change to the engineering qualification boundary invalidates or requires replacement of the qualification evidence.

### TC integration

When qualification is required, `TC-*` may become PASS only after the referenced `QUAL-*` receipt is current and PASS. Qualification does not itself grant material write authority; live `MATERIAL_WRITE_READY` remains the final write gate.

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
[x] BATON_READY cannot be inferred from lifecycle.
[x] Candidate takeover requires current independent certification.
[x] Missing/stale TC prevents MATERIAL_WRITE_READY.
[ ] Required qualification has an evaluated QUAL receipt.
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
[x] V2 remains untouched through WP-02.
[x] No downstream-specific logic exists through WP-02.
```
