# Engineering PR Delivery V3.5 — Common Reviewer integration contract

## Status

This file is the active Common Reviewer integration contract for the V3.5 package on `main`.

V3.5 MUST consume the reusable Common Reviewer Protocol:

```text
skills/common-reviewer-protocol-v1.0/
```

and combine it with the Coordinator-created project review / acceptance protocol.

## Required effective review basis

```text
COMMON_REVIEWER_PROTOCOL
+
PROJECT_REVIEW_PROTOCOL
+
REPOSITORY_REQUIRED_CHECKS
=
EFFECTIVE_REVIEW_PROFILE
```

The effective profile MUST bind exact Common/project refs and digests and MUST identify which Common criteria are required, inapplicable, or authority-waived.

## Standalone mode

When V3.5 is invoked without Local PR Delivery, a fresh responsibility/programme MUST bootstrap its decomposition and project review basis before material coding.

Topology rule:

```text
R = 1 -> STANDALONE_SINGLE_RESPONSIBILITY_BOOTSTRAP
R >= 2 -> STANDALONE_PROGRAMME_COORDINATOR_BOOTSTRAP
```

Programme bootstrap MUST satisfy the decomposition-quality gate defined by `PROGRAMME_DECOMPOSITION_PROGRESS.md` before releasing Coder responsibilities.

## Minimum same-principal self-review

Standalone V3.5 MUST require a fresh self-review attempt between implementation candidate and responsibility-complete result:

```text
IMPLEMENTATION
 -> TASK_EVIDENCE — SELF_REVIEW_START
 -> Common CR-01..CR-10
 -> project review methods
 -> freeze/classify findings
 -> bounded repair where permitted
 -> rerun affected verification on final candidate
 -> TASK_EVIDENCE — SELF_REVIEW_END
 -> completion decision
```

Truth fields:

```text
REVIEW_MODE: SELF_REVIEW
PRINCIPAL_INDEPENDENCE: NONE
CONTEXT_RESET: FRESH_REVIEW_ATTEMPT
COMMON_REVIEW_PROTOCOL_REF + DIGEST
PROJECT_REVIEW_PROTOCOL_REF + DIGEST
FINAL_CANDIDATE
```

A context reset does not create principal independence. V3.5 MUST reject any attempt to represent same-principal self-review as independent Reviewer/Super-Reviewer evidence.

## Distinct-review escalation

Self-review is only a minimum floor. If Owner/repository/Local/project/risk policy requires a distinct reviewer or specialist, V3.5 MUST leave responsibility completion blocked until that requirement is satisfied or explicitly waived by the correct authority.

Examples of risk that may require a specialist/distinct method include material:

- security/privacy/trust-boundary changes;
- concurrency/transactional correctness;
- accessibility/internationalization;
- safety-critical or regulated behavior;
- numerical/domain or hardware-specific correctness;
- release/infrastructure authority changes.

## Common review coverage

V3.5 MUST support the Common catalog:

```text
CR-01 Basis/scope/coverage
CR-02 Design/system fit
CR-03 Functional/negative correctness
CR-04 Simplicity/readability/maintainability
CR-05 Tests/verification quality
CR-06 Interfaces/data/compatibility
CR-07 Security/privacy/trust boundaries
CR-08 Reliability/errors/concurrency/operability
CR-09 Documentation/change communication
CR-10 Integration/regression/release fitness
```

and preserve explicit coverage/exclusions, criterion applicability basis, findings/dispositions and final-candidate replay.

## Finding / repair behavior

Use Common classes:

```text
BLOCKING_DEFECT
BOUNDED_PRODUCT_FIX
MATERIAL_SCOPE_CHANGE
ACCEPTANCE_SURFACE_DEFECT
EXTERNAL_DEPENDENCY
ADVISORY
```

Do not let self-review become an unbounded second Coder phase. Material scope changes use split/continuation. Acceptance-surface defects use acceptance revision. Required unavailable checks remain NOT_RUN/blocking.

## Progress and title projection

Review completion only advances declared delivery/evidence units. It MUST NOT award semantic Coder progress based on review activity, comments, files inspected, checks executed or elapsed time.

The existing `P/E/D/A` decomposition and liveness model remains orthogonal:

```text
P = nested engineering semantic progress
E = evidenced progress
D = Local/phase/programme delivery progress
A = activity/checkpoint epoch
```

## Local embedding

When V3.5 is nested under Local PR Delivery:

- Local owns lifecycle authority and any requirement for distinct review or authorized role collapse;
- Common Reviewer Protocol is the generic review floor;
- the project acceptance profile supplies specialized methods;
- where solo execution is explicitly permitted, SELF_CHECK_CONTEXT_V1 is the mandatory minimum review context with principal independence NONE;
- where governed review is required, REVIEW_CONTEXT_V1 records truthful DEGRADED or DISTINCT independence;
- self-review evidence cannot satisfy a distinct-review requirement when one is explicitly required;
- V3.5 completion remains scoped to its nested engineering responsibility and never means Local PRD completion.

## Version integration

V3.5 MUST pin the Common Reviewer Protocol ref/digest in activation/review evidence and participate in successor scanning.

A Common Reviewer Protocol revision MUST produce an integration-impact notice rather than silent migration, including whether V3.5 adapter/schema/tests require revision before the new review version becomes preferred.
