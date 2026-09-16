# V2.5 catch-up / completion roadmap

## Purpose

This roadmap completes the operational relay on top of the existing V2.5 control-plane kernel. It is not a rewrite of V2 and not a replacement of the strong roadmap/parallel/issue/projection machinery already implemented.

The sequencing rule is strict:

> First make the baton trustworthy. Then independently prove that a replacement can pick it up. Only then expand GitHub operations, quality procedures, and human-facing projections.

PR #396 remains draft throughout this roadmap. No downstream repository is an implementation target; real repositories remain read-only stress sources unless separately authorized.

## Progress Basis

Completion progress uses a new explicit catch-up basis rather than continuing any older narrative percentage.

Suggested weights:

| Work package | Weight |
| --- | ---: |
| WP-00 Kernel baseline / object matrix | 5 |
| WP-01 Semantic Execution Package | 18 |
| WP-02 Baton readiness + Takeover Certification | 18 |
| WP-03 Strong phase/boundary qualification | 12 |
| WP-04 Full progress / handover / next-work contract | 12 |
| WP-05 GitHub Program Projection operations | 8 |
| WP-06 Quality Procedure Library | 10 |
| WP-07 Human Communication | 6 |
| WP-08 Owner Change Intake | 3 |
| WP-09 End-to-end Relay Certification Matrix | 5 |
| WP-10 Self-consistency Audit | 2 |
| WP-11 PR Readiness | 1 |
| **Total** | **100** |

Earned progress remains acceptance-driven under each WP. These weights are denominator structure, not manually typed completion percentages.

## Dependency topology

```text
WP-00 Kernel baseline
   |
   v
WP-01 Semantic EP
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

## Initial frontier and EP sequence

Only WP-00 is executable initially.

```text
WP-00 Kernel baseline
  -> EP-R001
  -> CP-R001

WP-01 Semantic EP
  -> EP-R002
  -> CP-R002

WP-02 Baton readiness + Takeover Certification
  -> EP-R003
```

WP-01 depends on WP-00. WP-02 depends on WP-01. One EP must not own all three WPs.

---

## WP-00 — Kernel baseline / object matrix

### Outcome

Freeze and classify the current kernel before semantic replacement work begins.

### Procedure

- record exact branch/base/head and current green workflow evidence;
- inventory every V2.5 schema, template, validator, renderer, blueprint, generated projection and operating-model document;
- map each object to authority, producer, consumers, validator(s), renderer(s), lifecycle and replacement relationship;
- classify each contract as `KEEP | STRENGTHEN | REPLACE | DEPRECATE`;
- identify fields no validator reads, validators no producer satisfies, duplicate concepts, obsolete field names, and projections that could become competing truth sources;
- explicitly mark the current readiness fields as kernel semantics pending WP-02 migration.

### Required artifact

`operating-model/object-authority-matrix.md` updated from template to audited reality.

### Acceptance

- complete V2.5 object inventory exists;
- every writable source has one authority role;
- every projection identifies its source objects;
- replacement/deprecation candidates are named before code changes;
- baseline synthetic suite remains green.

---

## WP-01 — Semantic Execution Package

### Outcome

An EP cannot pass because it merely contains the correct headings. It must contain enough engineering content for a zero-context successor to execute the current slice.

### Required changes

#### Typed inputs

Require stable ID/name, description, authority, source, current value/resolution mechanism, type/units, editability, applicability, resolution state, consumers, validation and stale conditions.

Applicability:

```text
CURRENT_STEP_REQUIRED
CURRENT_EP_REQUIRED
FUTURE_STEP
INFORMATIONAL
```

Resolution:

```text
READY
OWNER_EDITABLE_READY
DEFERRED_NOT_CURRENTLY_REQUIRED
MISSING_BLOCKING
INVALID
STALE
```

Only unresolved conditions relevant to the current authorized slice remove current WRITE permission.

#### Typed benchmarks/oracles

Require purpose, source, payload, expected result, tolerance where applicable, oracle class, independence, applicability, resolution and test/acceptance mappings.

#### Executable discovery contract

Each step defines action, target, question, expected outputs, receipt requirement and stop/reconciliation conditions. The future receipt namespace is `DISC-xxxx`.

#### Strong scope

Distinguish allowed write, allowed read, protected, prohibited and Owner-reserved domains/invariants.

#### Structured anti-drift

Stable invalidation rules replace empty/vague `stale_if` lists. Explicit no-known-condition rationale is required when applicable.

#### Executable implementation steps

Each step carries objective, targets, reads, writes, inputs, acceptance, tests, expected intermediate state and stop conditions.

#### Exact report / successor contract

Define required payloads, not section-name presence.

### Negative regressions

Must reject at least:

- semantically empty required inputs;
- semantically empty required benchmarks;
- vague discovery step with no expected outputs;
- empty scope that claims executability;
- empty anti-drift without explicit rationale;
- vague implementation step;
- report headings with no reconciliation payload.

### Exit gate

A rich repository-neutral synthetic EP passes; deliberately hollow EPs fail for semantic reasons.

---

## WP-02 — Baton readiness + Takeover Certification

### Outcome

Separate outgoing baton quality from candidate-specific takeover and live write permission.

### New predicates

Implement the target predicates defined in `completion-architecture.md`:

```text
BATON_READY
TAKEOVER_CERTIFIED
PROJECTION_READY
HANDOVER_READY
MATERIAL_WRITE_READY
```

Lifecycle alone must never imply `BATON_READY`.

### Takeover Certification

Add durable candidate-specific certification bound to exact roadmap, EP/plan, predecessor baton and Git/material basis.

Required identities include candidate, preparer and independent evaluator. Self-certification is not allowed.

### Discovery Receipt

Candidate discovery produces a durable `DISC-xxxx` receipt bound to the EP and current material basis.

### Invalidation

Takeover certification becomes stale when a relevant EP, roadmap contract, predecessor baton, branch/material basis, current-slice input/benchmark requirement, scope or qualification basis changes.

### Exit gate

Must reject:

```text
ACTIVE + no current TC + TAKEOVER_CERTIFIED=true
```

and must reject live WRITE readiness when certification is absent/stale even if the baton itself remains complete.

### Mandatory proof before WP-03

Run an actual zero-context synthetic takeover against a semantically rich EP. Do not start WP-03 until this passes.

---

## WP-03 — Strong phase / material-boundary qualification

### Outcome

Qualification proves technical understanding rather than question metadata.

### Trigger

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

A materially new boundary includes substantial change in production path, engineering authority, numerical method, protected/safety invariant, input authority or verification/oracle class.

### Transaction

```text
QUESTION_SET
 -> candidate answers
 -> independent evaluation
 -> QUAL-xxxx receipt
 -> certification reconciliation
```

### Q1-Q5 target

- Q1 actual production/source trace;
- Q2 concrete engineering reconstruction where the domain permits;
- Q3 boundary/authority mutation and falsifier;
- Q4 independent verification/benchmark reasoning;
- Q5 exact first safe implementation slice and predicted verification result.

Correct anchors with meaningless answers fail.

---

## WP-04 — Full progress / handover / next-work contract

### Outcome

The Owner and successor can see the complete project state without reading YAML.

### Required hierarchy

```text
Overall
 -> Objective
 -> Phase
 -> Work Package
 -> Task / implementation step
 -> Acceptance Criterion
```

Every level exposes status and calculated progress, with evidence where meaningful.

### Current execution

Show current WP, EP, step, acceptance, tests and live material authority.

### Next-work contract

Replace dependence on one `next_action` sentence with ordered structured steps carrying action, targets, inputs, tests, acceptance, expected result and stop/reconciliation conditions.

### Exit gate

Generated handover must answer: where are we, what is done, what remains, what is happening now, and exactly what happens next.

---

## WP-05 — GitHub Program Projection operations

### Outcome

Turn the strong issue graph into an operational GitHub transaction while keeping repository authority primary.

### Operations

```text
CREATE
LINK
UPDATE
PUBLISH HANDOVER
SUPERSEDE
REVISE
CLOSE
REOPEN
```

Each operation uses the existing projection-generation/idempotency machinery: durable desired operation -> external action -> receipt -> verification -> issue-graph reconciliation -> projection convergence.

Cover parent/child creation/linking/rollup/closure and supersession transfer/closure explicitly.

---

## WP-06 — Quality Procedure Library

### Outcome

Quality becomes a usable engineering procedure library rather than principles or a universal checklist.

### Common blueprint skeleton

```text
WHEN TO APPLY
REQUIRED INPUTS
PROCEDURE
BEST-PRACTICE CHECKLIST
ANTI-PATTERNS
REQUIRED ARTIFACTS
VERIFICATION
QUALITY FINDING CLASSIFICATION
TRUE HARD-STOP CONDITIONS
OWNER REPORT
SUCCESSOR HANDOVER
```

### Applicability router

Every EP explicitly names applicable and not-applicable quality blueprints with reasons. Do not run every blueprint mechanically.

### Quality Review

Applicable procedures produce `QRV-xxxx` Quality Review artifacts. Quality findings do not become hard stops by default.

---

## WP-07 — Human Communication

### Outcome

Separate machine truth from Owner-facing language.

Machine views may use control-plane states. Owner views explain capabilities, restrictions, evidence, gaps, roadmap impact, next work and genuine Owner decisions in plain engineering language.

Add a human-communication blueprint and generate distinct technical and Owner projections from the same authority objects.

---

## WP-08 — Owner Change Intake

### Outcome

Make Owner-intent mutations immediately understandable without weakening ODR authority.

Owner-facing change intake must show previous intent, new intent, retained work, invalidated work, new scope, progress-basis effect, issue impact, active EP disposition, new frontier and application/decision status.

This is the human interface to ODR, not a replacement for ODR.

---

## WP-09 — End-to-end Relay Certification Matrix

### Outcome

This is the defining release criterion for V2.5.

### Representative lifecycle scenarios

At minimum:

```text
ACTIVE normal serial
ACTIVE + CONTINUE_UNCHANGED
RECONCILING
PARALLEL
PARALLEL -> JOIN
PARALLEL -> REPLAN
STALE projection
IDLE
TERMINAL
PHASE TRANSITION
OWNER INTENT MUTATION
ISSUE SUPERSESSION
```

### A -> B -> C zero-chat relay

The core release test deliberately deletes chat custody between agents.

Agent C must reconstruct without chat:

- why the task exists;
- governing Owner decisions;
- predecessor facts/limitations;
- current roadmap position;
- current task/first safe step;
- editable versus authoritative inputs;
- benchmark/oracle contract;
- allowed/protected/prohibited writes;
- applicable quality obligations;
- required tests/acceptance;
- exact next work;
- EP invalidation/staleness conditions.

If prior conversation is materially required, the release test fails.

---

## WP-10 — Self-consistency audit

### Outcome

Prove the system is coherent rather than merely large.

Audit:

```text
schema <-> template
template <-> validator
validator <-> renderer
renderer <-> docs
docs <-> SKILL.md
object <-> producer
object <-> consumer
lifecycle <-> authority
progress <-> acceptance
issue <-> roadmap
certification <-> readiness
```

Find fields no validator reads, validators no producer satisfies, duplicate concepts, silent defaults, obsolete aliases, multiple authorities, stale renderers and retired documentation.

---

## WP-11 — PR Readiness

Only after WP-09 and WP-10 pass:

- verify complete generic CI on exact head;
- verify V2 remains untouched;
- verify no downstream-specific logic;
- inspect every change outside the V2.5 skill tree;
- generate final architecture index and operator quick-start;
- generate a representative synthetic relay example;
- update PR description to delivered semantics;
- perform final independent review.

Do not merge automatically.

## Anti-drift during catch-up

Do not spend material effort on downstream adoption, project-specific adapters, new engineering domains, additional exotic issue relationships, extra parallel features, cosmetic Markdown polish, or merge preparation until their dependency WP is current.

Every proposed addition should answer:

> Does this make a zero-context successor materially more capable of safely continuing the engineering project?

If not, it is outside the current catch-up frontier.

## Merge gate

PR #396 remains draft until the exact head proves all of the following:

```text
[ ] Hollow EP fails semantic validation.
[ ] Rich standalone EP passes.
[ ] BATON_READY cannot be inferred from lifecycle.
[ ] Candidate takeover requires current independent certification.
[ ] Missing/stale TC prevents MATERIAL_WRITE_READY.
[ ] Required qualification has an evaluated QUAL receipt.
[ ] Owner handover contains full roadmap/WP/task/AC progress.
[ ] Detailed ordered next work is rendered.
[ ] Exact return report is reconciled to source objects.
[ ] GitHub parent/child/supersession/closure operations are defined.
[ ] Quality procedures produce scoped QRV artifacts.
[ ] Owner communication is plain-language by default.
[ ] Representative lifecycle cold-start/certification matrix passes.
[ ] Agent A -> B -> C zero-chat relay passes.
[ ] Schema/template/validator/renderer/docs audit is clean.
[ ] Generic CI passes on exact head.
[ ] V2 remains untouched.
[ ] No downstream-specific logic exists.
```
