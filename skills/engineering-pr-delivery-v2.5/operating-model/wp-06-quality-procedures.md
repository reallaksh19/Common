# WP-06 — Quality Procedure Library and QRV evidence

## Status

WP-06 implements applicability-routed engineering quality procedures and first-class `QRV-*` Quality Review evidence. Quality remains a separate state plane from execution, evidence and true hard stops.

The governing rule is:

```text
EP quality router
  -> applicable procedures only
  -> procedure execution/review
  -> QRV-* on exact EP/material basis
  -> findings + evidence + disposition
  -> checkpoint QRV pointer/digest
  -> derived report projection
```

A quality concern is not automatically a blocker. Execution is blocked only when a QRV finding maps to an existing true hard-stop category with durable basis.

## Built-in procedure library

The built-in procedures are:

```text
software-design
coding
ui-ux
testing
engineering-numerics
code-review
accessibility
performance
migration
github-delivery
```

Every blueprint now contains the required procedural sections:

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

`validate_blueprints.py` enforces that structure and rejects hollow procedure files.

## Applicability routing

Every executable EP must partition the entire built-in library exactly once:

```yaml
quality:
  applicable:
    - blueprint: coding
      reason: ...
      review_focus: [...]
  not_applicable:
    - blueprint: engineering-numerics
      reason: ...
  review_contract:
    required: true
    required_before_checkpoint: true
    receipt_namespace: QRV-
    required_outputs: [procedure_results, findings, owner_report, successor_handover]
  findings_policy: ...
  ordinary_findings_are_hard_stops: false
```

Applicable procedures require a concrete review focus. A not-applicable procedure requires a concrete reason but no artificial review work. Silent omission, duplicate classification and unknown procedures fail conformance.

## Quality Review receipt

A `QRV-*` binds to:

- exact EP id/path and canonical contract digest;
- roadmap revision;
- exact material ref;
- reviewer identity/type;
- exact snapshot of the EP quality router;
- one result for every applicable procedure;
- findings and execution effect;
- Owner-facing summary;
- exact successor transfer of unresolved findings.

Procedure results are:

```text
CLEAR
FINDINGS
NOT_RUN
```

`NOT_RUN` carries an explicit cause and remains evidence/quality truth. It does not automatically create an execution stop.

## Finding model

Findings use `QF-*` and record blueprint, classification, severity, disposition, statement and durable evidence.

Severity alone never grants stop authority. A finding may use `blocks_execution: true` only when it has a valid hard-stop mapping to an existing relay category and trigger, for example:

```text
PROTECTED_INVARIANT -> PROTECTED_INVARIANT_FAILURE
ESSENTIAL_INPUT      -> ESSENTIAL_INPUT_MISSING
AUTHORITY            -> AUTHORITY_VIOLATION / OWNER_DECISION_REQUIRED
UNSAFE_ENGINEERING_RESULT -> UNSAFE_ENGINEERING_RESULT
```

A HIGH maintainability, design, UX, performance or test-gap finding can therefore remain `NEEDS_ATTENTION` without inventing a hard stop.

## Custody and checkpoint rules

Before checkpoint publication, a quality-required EP must have a current QRV. The checkpoint points to the QRV by id/path/digest. The QRV material ref must equal the checkpoint material ref, and checkpoint `quality_findings` mirrors the QRV finding ids.

A QRV containing a true blocking finding cannot publish an executable successor checkpoint. Deferred, Owner-review-required and unresolved findings must be transferred exactly to `successor_handover.unresolved_findings` with explicit follow-up.

Parallel lane checkpoints use lane-specific QRVs; quality review is not waived for parallel execution.

## Derived reporting

`report_projection.py` includes the checkpoint QRV as derived quality evidence and binds its id/digest under `generated_from`. Generated reports expose QRV state/findings/execution effect/Owner report/successor transfer but never become quality authority.

## Validators

```text
validate_blueprints.py
validate_quality_router.py
validate_quality_review.py
```

All three participate in aggregate relay conformance.

## Synthetic regression matrix

`tests/stress/test_quality_procedures.py` proves:

- the built-in procedure library is structurally procedural;
- the EP router is a complete partition;
- applicable review focus is mandatory while N/A ceremony is not;
- a clear QRV exactly covers applicable procedures;
- `NOT_RUN` produces attention but not a hard stop;
- a HIGH ordinary quality finding remains non-blocking;
- a blocking finding requires a valid true-hard-stop mapping;
- unresolved findings cannot disappear from successor handover.

Existing parallel convergence tests were also migrated so lane checkpoints carry lane-specific QRVs.

## Validation evidence

Pre-checkpoint aligned implementation:

```text
head: c5a3f8dfb9111081b15fef607dd2b6e7ba8ae868
workflow: 35146877546
compile: PASS
root unit tests: PASS (7)
synthetic stress tests: PASS (118)
```

Earlier integration runs were intentionally allowed to expose legacy fixture gaps: the first failed root fixture still used `quality.blueprints`; the second failed one parallel-join fixture whose lane checkpoints had no QRV. Both were migrated without weakening the new rules.

## Explicit non-goals

WP-06 does not implement plain-language Owner status presentation (WP-07), Owner change intake (WP-08), the full A -> B -> C relay proof (WP-09), final schema/template/validator/doc consistency audit (WP-10), or PR readiness/merge (WP-11).
