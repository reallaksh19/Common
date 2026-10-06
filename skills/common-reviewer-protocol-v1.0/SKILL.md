---
name: common-reviewer-protocol-v1-0
description: Common technology-agnostic code-review floor for standalone self-review and governed Reviewer/Super-Reviewer execution. Combine with a Coordinator-created project review/acceptance protocol; never treat same-principal self-review as independent review.
---

# Common Reviewer Protocol v1.0

## Purpose

This package defines the **minimum reusable engineering-review floor** for code changes governed by Common protocols.

It is intentionally project-agnostic. It does not replace the project-specific review / acceptance protocol created during Coordinator bootstrap. The effective review basis is:

```text
COMMON REVIEWER PROTOCOL
+
PINNED PROJECT REVIEW / ACCEPTANCE PROTOCOL
+
REPOSITORY-SPECIFIC REQUIRED CHECKS / POLICIES
=
EFFECTIVE REVIEW PROFILE
```

Project-specific acceptance MAY strengthen or specialize this floor. It MUST NOT silently erase an applicable Common criterion. A genuinely inapplicable criterion is recorded `NOT_APPLICABLE` with a concrete basis. A waiver that relaxes an applicable requirement requires the authority defined by the governing lifecycle; self-review cannot grant its own risk-relaxation waiver.

## Research basis

The protocol is synthesized from broadly applicable review guidance rather than one repository's conventions:

- Google Engineering Practices: review design/system fit, functionality and edge cases, complexity, tests as maintained code, naming, comments, style, documentation, whole-file/system context, every assigned human-written line, and split changes that are too large to reason about effectively.
- Google Code Review Standard: technical facts over preference; approve improvement rather than demand perfection, while never knowingly degrading overall code health.
- OWASP Secure Code Review guidance: understand architecture and requirements, trace changed data/control flow and trust boundaries, inspect authentication/authorization/input handling/error handling/configuration/dependencies where applicable, and combine automated checks with human reasoning about business logic and context-specific risk.
- GitHub review guidance: review PR context, changed files, dependency/security impact and automated checks; standardize author context so reviewers can reconstruct purpose and testing.

See `RESEARCH_BASIS.md` for links and the mapping into this schema.

## Non-negotiable truth model

Review evidence is about the **actual candidate**, not the author's memory or intent.

```text
issue / plan / project protocol
        ↓
exact candidate + full affected context
        ↓
Common review criteria
        +
project-specific criteria/methods
        ↓
findings / bounded repairs
        ↓
re-run affected verification on final candidate
        ↓
review result
```

A green CI run is evidence for the checks it actually executed. It is not by itself proof of design quality, correct test assertions, business logic, integration fitness, security, accessibility, performance, data semantics, or other project-specific acceptance.

## Common criteria catalog

Every review consumes these stable criterion IDs. Each criterion is `REQUIRED`, `NOT_APPLICABLE`, or `WAIVED_BY_AUTHORITY`; omission is not a result.

### CR-01 — Basis, scope and coverage

Verify:

- the intended outcome and acceptance basis are identifiable;
- exact candidate/base/integration identity is known where material;
- review scope is explicit, including files/components intentionally excluded;
- the change is one coherent reviewable outcome or is split;
- mechanical/generated/vendor/lockfile deltas are distinguished from semantic authored changes;
- no relevant changed human-written code is silently skipped.

A review that covers only selected surfaces MUST say so and MUST NOT certify uncovered surfaces.

### CR-02 — Design and system fit

Ask whether the change belongs at this layer and integrates coherently with existing architecture.

Check for:

- unnecessary new abstractions, state machines, storage, registries or duplicate authorities;
- architectural boundary violations;
- hidden coupling or cross-component consequences;
- over-engineering for speculative future requirements;
- missed reuse of an existing supported mechanism;
- migration / backward-compatibility implications.

Large design defects should be surfaced before polishing local details.

### CR-03 — Functional correctness and negative behavior

Establish that behavior matches the declared outcome, including applicable:

- normal path;
- boundary / empty / null / malformed cases;
- failure and recovery path;
- state-transition validity;
- user-visible behavior;
- idempotency / retry behavior;
- concurrency / ordering / race behavior;
- backward compatibility.

Think adversarially about what can go wrong; do not infer correctness merely because the happy path runs.

### CR-04 — Simplicity, readability and maintainability

Check whether future maintainers can understand and safely change the implementation.

Review:

- avoidable complexity;
- function/class/module responsibility;
- naming and data shape clarity;
- duplication;
- dead or obsolete code;
- comments explaining **why** rather than restating obvious **what**;
- local consistency and applicable style rules;
- whether explanatory prose in the review should instead result in clearer code or durable documentation.

### CR-05 — Tests and verification quality

Do not review only whether tests passed; review the tests themselves.

Verify as applicable:

- changed behavior has meaningful test coverage at the right level;
- assertions prove the intended behavior rather than implementation trivia;
- negative/boundary cases are represented where risk warrants;
- a broken implementation would plausibly make the test fail;
- test fixtures/oracles are independent enough for the claim they support;
- tests are deterministic/reproducible or nondeterminism is explicitly bounded;
- generated snapshots/goldens are semantically inspected, not blindly accepted;
- required checks actually executed against the candidate being certified;
- `NOT_RUN`, `INCONCLUSIVE` and unavailable environments remain truthful.

### CR-06 — Interfaces, data and compatibility

Where the change crosses an interface, verify:

- input/output contracts;
- serialization/schema compatibility;
- cardinality, units, precision and ordering semantics;
- persistence/migration behavior;
- API/CLI/UI compatibility;
- consumer/provider assumptions;
- canonical-source and derived-artifact relationships;
- rollback or downgrade implications when material.

### CR-07 — Security, privacy and trust boundaries

Apply proportionately to changed risk surfaces. Review changed sources → transformations → sinks and any trust-boundary crossing.

Consider as applicable:

- input validation / output encoding;
- authentication and session assumptions;
- authorization and privilege checks;
- secret/credential handling;
- filesystem/process/network execution;
- injection/path traversal/deserialization risk;
- sensitive-data exposure in logs/errors/artifacts;
- dependency changes and known-risk surface;
- secure defaults/configuration;
- resource exhaustion / abuse paths.

A reviewer who lacks the required expertise MUST record the limitation and require an appropriate specialist/project method when the risk is material.

### CR-08 — Reliability, errors, concurrency and operability

Check applicable operational behavior:

- errors are handled at the correct layer;
- failures do not corrupt state or silently continue;
- retry/timeout/cancellation behavior is coherent;
- transactions/atomicity/rollback are sound where needed;
- concurrent access and ordering assumptions are explicit;
- resource lifetime/cleanup is correct;
- observability/logging is sufficient without leaking sensitive data;
- performance/resource regressions are considered where the changed path is sensitive.

### CR-09 — Documentation and change communication

Verify durable documentation is updated when the change alters how users/developers build, configure, call, test, operate or release the system.

The PR/task handoff should explain:

- what changed and why;
- important design choices;
- validation performed;
- known limitations / follow-up;
- migration or operator action when applicable.

### CR-10 — Integration, regression and release fitness

Before a review can complete, reconcile the final candidate against:

- affected existing behavior;
- declared dependencies and consumers;
- merge/base/integration drift where material;
- repository required checks;
- unresolved review findings;
- project-specific acceptance methods;
- release/rollback requirements if the responsibility includes release readiness.

No generic Common review may substitute for a missing project-specific benchmark, browser check, numerical oracle, accessibility audit, hardware test, domain correctness check or other specialized method required by the project protocol.

## Finding taxonomy

Every material finding is classified so review does not silently become a second unbounded implementation phase.

```text
BLOCKING_DEFECT
  Candidate violates an applicable Common/project requirement.

BOUNDED_PRODUCT_FIX
  Localized repair within the current responsibility and permitted review-repair envelope.

MATERIAL_SCOPE_CHANGE
  Repair changes the responsibility outcome/scope or exceeds its bounded repair envelope.

ACCEPTANCE_SURFACE_DEFECT
  Project/common review method, fixture, oracle, tolerance or acceptance definition is itself defective.

EXTERNAL_DEPENDENCY
  Required truth depends on unavailable external/provider/environment state.

ADVISORY
  Improvement that is not required for the current acceptance result.
```

`MATERIAL_SCOPE_CHANGE` is split/continuation work, not a reason for the reviewer to silently keep coding. `ACCEPTANCE_SURFACE_DEFECT` uses the governing acceptance-revision process; do not weaken the test until the current candidate passes. `EXTERNAL_DEPENDENCY` remains `NOT_RUN` / blocked where required.

## Standalone self-review mode

Standalone execution may not have a distinct Reviewer principal. It still MUST perform a minimum review before claiming responsibility completion.

The same principal therefore performs a **fresh, explicitly labeled self-review attempt** after implementation reaches a candidate boundary.

```text
IMPLEMENTATION CANDIDATE
        ↓
freeze exact review basis / candidate
        ↓
TASK_EVIDENCE — SELF_REVIEW_START
        ↓
reconstruct from issue/plan/protocol + actual files
        ↓
execute CR-01..CR-10 applicability
        + project-specific review methods
        ↓
record findings before repairs
        ↓
bounded repair if permitted
        ↓
rerun affected Common/project methods on final candidate
        ↓
TASK_EVIDENCE — SELF_REVIEW_END
        ↓
only then may TASK_RESULT claim responsibility completion
```

### Self-review independence truth

Self-review MUST record:

```text
REVIEW_MODE: SELF_REVIEW
AUTHOR_PRINCIPAL: <principal>
REVIEW_PRINCIPAL: <same principal>
PRINCIPAL_INDEPENDENCE: NONE
CONTEXT_RESET: FRESH_REVIEW_ATTEMPT
```

`CONTEXT_RESET` means the agent stops relying on its implementation memory and reconstructs the review basis/candidate from durable sources. It does **not** make the review independent.

Self-review MUST NOT emit claims such as `INDEPENDENT_REVIEW`, `INDEPENDENT_APPROVAL`, `DISTINCT_PRINCIPAL`, or equivalent.

If the project protocol, repository policy, risk class, Owner instruction or lifecycle requires a distinct Reviewer/Super Reviewer, self-review is only pre-review evidence and cannot satisfy that requirement.

### Minimum self-review method

The self-review attempt MUST:

1. reread the task/plan and effective acceptance profile;
2. observe exact current candidate/base and semantic changed-file surface;
3. inspect every human-written changed region within the claimed review scope, plus enough surrounding/system context to assess fit;
4. assess all CR criteria for applicability and result;
5. execute the Coordinator-created project review methods applicable to this responsibility;
6. inspect relevant test code/oracles, not merely test outcomes;
7. run/consume required automated checks and preserve `NOT_RUN` truth;
8. freeze findings before substantial repair;
9. classify repairs using the finding taxonomy;
10. rerun affected verification against the final candidate;
11. publish coverage, findings, limitations, evidence refs and remaining work.

## Local / distinct Reviewer mode

When a lifecycle such as Local PR Delivery supplies a distinct Reviewer or Coordinator/Super Reviewer, the same Common catalog remains the generic floor.

The effective role slice is determined by the pinned project acceptance profile. A distinct Reviewer may rely on Coder self-review evidence as context, but MUST independently inspect/reconstruct the claims assigned to the Reviewer role; prior self-review is not inherited approval.

Super Review uses the same Common floor where applicable plus its independent project harness/oracle/integration methods. Reviewer evidence cannot be renamed into Super Reviewer evidence.

## Effective review profile schema

Each responsibility MUST resolve a machine-readable effective profile before review:

```yaml
review_profile:
  common_protocol:
    ref: <exact ref>
    version: 1.0
    digest: <digest>

  project_protocol:
    ref: <exact ref>
    digest: <digest>

  role: SELF_REVIEW | REVIEWER | SUPER_REVIEWER

  common_criteria:
    CR-01: REQUIRED
    CR-02: REQUIRED
    CR-03: REQUIRED
    CR-04: REQUIRED
    CR-05: REQUIRED
    CR-06: REQUIRED | NOT_APPLICABLE
    CR-07: REQUIRED | NOT_APPLICABLE
    CR-08: REQUIRED | NOT_APPLICABLE
    CR-09: REQUIRED | NOT_APPLICABLE
    CR-10: REQUIRED

  project_method_ids: [...]
  specialist_required: [...]
```

Use `schemas/common-review-profile.schema.yaml` for the normative machine shape.

## Review evidence

Reuse the governing engineering publication family rather than creating heartbeat/review-comment spam.

Recommended durable evidence subtypes:

```text
TASK_EVIDENCE — SELF_REVIEW_START
TASK_EVIDENCE — SELF_REVIEW_END
TASK_EVIDENCE — REVIEWER_START
TASK_EVIDENCE — REVIEWER_END
TASK_EVIDENCE — SUPER_REVIEW_START
TASK_EVIDENCE — SUPER_REVIEW_END
```

Each END record identifies:

- exact input and final candidate;
- review mode / principal independence;
- Common protocol ref/digest;
- project protocol ref/digest;
- criterion applicability/results;
- project methods executed and their evidence refs;
- files/surfaces covered and explicitly excluded;
- findings discovered and dispositions;
- repairs made in review;
- verification rerun on final candidate;
- unresolved required defects/checks;
- next lifecycle action.

## Completion rule

A standalone responsibility MUST NOT claim `TASK_RESULT RESPONSIBILITY_COMPLETE=YES` unless:

- required Common criteria are complete on the final candidate;
- required project-specific review methods are complete on the final candidate;
- no unresolved blocking defect remains;
- required unavailable checks remain truthfully blocking/NOT_RUN rather than being promoted to PASS;
- the result clearly says `SELF_REVIEW` and `PRINCIPAL_INDEPENDENCE: NONE` when no distinct reviewer existed.

Where distinct review is required, self-review completion does not authorize merge/release or lifecycle advancement past that requirement.

## Review comment severity

When producing human-facing findings, use explicit severity/intent labels:

```text
BLOCKER: required before acceptance
REQUIRED: required correction, non-catastrophic
ADVISORY: worthwhile follow-up, not required for current acceptance
NIT: non-blocking polish/style
QUESTION: clarification needed before result can be established
```

Technical facts, project requirements and applicable style rules outrank personal preference.

## Protocol evolution

Every active review pins the exact Common Reviewer Protocol ref/digest. A later `common-reviewer-protocol-v1.1` or same-version digest change does not silently rewrite active evidence.

Activation/successor scanning SHOULD report:

```text
COMMON_REVIEW_PROTOCOL_REVISION_NOTICE
pinned: <version/ref/digest>
discovered: <version/ref/digest>
integration_impact:
  NONE | NEW_TASKS_RECOMMENDED | PROJECT_PROFILE_REVIEW_REQUIRED |
  LOCAL_ADAPTER_REVISION_REQUIRED | RELAY_ADAPTER_REVISION_REQUIRED
migration: NOT_AUTOMATIC
```

New protocol versions must state compatibility with Local / engineering-delivery versions and project review-profile schema versions before becoming preferred defaults.
