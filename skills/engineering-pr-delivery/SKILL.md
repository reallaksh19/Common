---
name: engineering-pr-delivery
description: Govern implementation, debugging, investigation, technical review, validation, PR delivery, and handover for engineering-software repository work. Use when working on a Git repository, GitHub issue, or pull request where production behavior, changed-file control, validation evidence, engineering authority, numerical correctness, or durable agent handover must be maintained. Do not use for standalone programming explanations or small code examples without repository work.
---

# Engineering PR Delivery

## Purpose

Deliver usable production capability through a traceable, evidence-backed repository workflow.

```text
production behavior
-> real production integration
-> observable result
-> focused software validation
-> engineering validation where applicable
-> changed-file reconciliation
-> durable handover
```

Schemas, validators, documentation, tests, or abstractions alone do not establish production completion.

## Core invariants

- Keep assignment work on one PR unless the owner explicitly changes scope.
- Do not merge unless explicitly instructed.
- Do not silently broaden scope.
- Do not call an unexecuted check `PASS`.
- Do not convert assumptions or source inspection into runtime proof.
- Do not introduce hidden engineering defaults, silent fallback engineering data, production mocks, or authority-changing shims.
- Do not change an authority boundary unless required by the task and explicitly recorded.
- Do not commit unrelated files, backup copies, formatting churn, or unrelated dependency upgrades.
- A new abstraction must have a real production consumer in the same PR.
- Another competent agent must be able to continue from the repository, PR, and work report without conversation history.

## 1. Classify the task

Determine the independent classifications before acting.

### Work intent

- `IMPLEMENT`
- `INVESTIGATE`
- `REVIEW`
- `AUDIT`
- `HANDOVER`

### Repository state

- `NO_PR`
- `NEW_PR_REQUIRED`
- `EXISTING_PR`

### Mutation authority

- `READ_ONLY`
- `WRITE_ALLOWED`

### Criticality

- `STANDARD`
- `ENGINEERING_CRITICAL`
- `SAFETY_CRITICAL`

A task may transition between work intents. Do not modify repository state when mutation authority is `READ_ONLY`.

Set `ENGINEERING_CRITICAL` or higher when work affects solver mechanics, FEA, stress, loads, formulas, geometry/topology, meshing, units, material/section/property authority, code assessment, engineering result recovery, or engineering exports.

## 2. Follow the execution state machine

Use the applicable states:

```text
BOOTSTRAP -> BASELINE -> PLAN -> IMPLEMENT -> VALIDATE -> RECONCILE -> HANDOVER -> CLOSURE
```

Review/audit work may stop after `BASELINE`, inspection/validation, and `HANDOVER`.

Continuation work must recover existing state before resuming.

Do not jump from `BOOTSTRAP` directly to production implementation.

Read `references/stage-protocol.md`.

## 3. Establish repository ground truth

Before implementation claims or planning, establish mutable repository state from the repository/GitHub, not from conversation history.

Read `references/repository-ground-truth.md`.

If repository, work report, local checkout, PR metadata, or conversation history disagree, record and reconcile the discrepancy before relying on the disputed value.

## 4. Recover or initialize one living work report

For implementation work maintain exactly one current report:

```text
agents/PR<NUMBER>_workreport.md
```

Before a PR number exists:

```text
agents/PR_PENDING_workreport.md
```

If a valid report exists, recover and synchronize it rather than replacing it.

Read `references/workreport-template.md`.

The report is current-state authority for the assignment, but live repository state overrides stale report metadata.

## 5. Establish technical baseline before editing

Inspect the real production path and distinguish claim state:

- `OBSERVED` — directly verified.
- `DEMONSTRATED` — reproducibly validated.
- `INFERRED` — supported indirectly.
- `EXPECTED` — predicted but unverified.
- `ASSUMED` — intentionally accepted without proof.
- `UNKNOWN` — insufficient evidence.

Also classify baseline findings as:

- `PREEXISTING`
- `INTRODUCED_BY_CURRENT_WORK`
- `UNKNOWN_ORIGIN`

Never convert an assumption, expectation, or source inspection into a demonstrated fact.

## 6. Register every credible finding

Use durable IDs:

- `ISS-###` confirmed defect
- `IMP-###` improvement opportunity
- `RISK-###` engineering/release risk
- `DEC-###` deliberate decision
- `QST-###` unresolved question
- `DEBT-###` accepted technical debt

Read `references/finding-taxonomy.md`.

Never silently discard a credible finding because it is outside scope. Resolve, accept, defer, reject with rationale, block, or transfer it.

## 7. Protect authority boundaries

Before changing ownership of engineering data, calculation logic, topology, persistence, publication, rendering, export, registries, classifications, or similar authoritative behavior, read `references/authority-boundaries.md`.

Intentional authority changes require a `DEC-*` item and focused validation.

## 8. Plan small reviewable stages

Before each implementation stage record current truth, objective, expected files, engineering rationale, planned behavior, edge cases, validation, and known risks.

Then implement.

After each stage record implementation performed, deviations, actual behavior, validation, new findings, remaining risks, and stage decision.

Do not implement first and retrospectively invent the plan.

## 9. Implement action-first

Prefer:

```text
production behavior
-> real production consumer
-> operator-visible/downloadable/measurable result
-> focused regression validation
-> minimum durable evidence
```

Do not substitute:

```text
schema -> validator -> framework -> placeholder adapter -> no usable capability
```

Use this acceptance question throughout:

> Can the intended operator now use, see, calculate, download, export, inspect, or measure the intended capability through the real production path?

If `No`, do not claim production completion.

Read `references/coding-policy.md` for implementation conventions.

## 10. Apply validation discipline

Read `references/validation-common.md`.

Record validation in three independent dimensions.

### Status

- `PASS`
- `FAIL`
- `NOT_RUN`
- `NOT_APPLICABLE`

### Observation

- `LOCAL_EXECUTION`
- `REMOTE_EXECUTION`
- `SOURCE_INSPECTION`
- `ARTIFACT_INSPECTION`
- `USER_SUPPLIED`
- `INFERRED`
- `NOT_OBSERVED`

### Oracle

- `NONE`
- `IMPLEMENTATION_COUPLED`
- `INDEPENDENT_REPRODUCTION`
- `ANALYTICAL`
- `AUTHORITATIVE_REFERENCE`
- `CROSS_SOLVER`
- `EXPERIMENTAL`

A regression test with an implementation-coupled oracle may be useful, but it is not independent engineering verification.

If criticality is `ENGINEERING_CRITICAL` or `SAFETY_CRITICAL`, read `references/engineering-validation.md` before planning implementation and apply all relevant requirements.

## 11. Enforce integrity / anti-gaming rules

Read `references/anti-gaming-rules.md`.

Never obtain a green gate by weakening the gate instead of correcting production behavior unless the gate itself is independently demonstrated to be wrong.

## 12. Validate semantic impact and negative assurance

For engineering-sensitive changes trace the relevant chain, for example:

```text
authority -> canonical data -> transformation -> solver/calculation -> recovery -> publication -> report/UI/export
```

Record both:

- behavior intended to change; and
- behavior required to remain invariant.

Provide evidence for both where material.

## 13. Reconcile changed files

Before closure compare the documented changed-file ledger against the actual PR/repository changed-file list.

Every discrepancy must be investigated. Any unexplained changed file blocks closure.

Use `scripts/reconcile_changed_files.py` when a local checkout is available.

## 14. Maintain handover continuously

The current report must always state:

- what is now true;
- what is being worked on;
- what remains unfinished;
- what must not be assumed;
- current PR/branch/HEAD;
- last completed/current stage;
- known failing checks;
- open questions;
- important deferred work;
- highest-risk remaining item;
- exact next action.

Do not write vague handover text such as `Continue implementation`.

## 15. Closure

Read `references/closure-gate.md`.

Do not collapse implementation, integration, software validation, engineering validation, and release readiness into one `DONE` state.

If mandatory closure conditions remain unmet, report the work as partial or blocked rather than complete.
