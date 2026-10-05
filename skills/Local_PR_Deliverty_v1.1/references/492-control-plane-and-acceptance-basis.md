# #492 Local v1.1 control-plane and acceptance-basis invariants

This reference implements the reconciled architecture from Common #492. It is deliberately additive to the v1.1 foundation in PR #490.

## 1. Canonical engineering identity

For native work, `TASK` is the Production Responsibility.

```text
TASK.kind = RESPONSIBILITY
TASK.task_id = PRD-017
```

Do not create a second mutable `PRODUCTION_RESPONSIBILITY` authority record.

GitHub representation is metadata:

```text
PRD-017
  representation.kind = SINGLE_ISSUE | ISSUE_SET | CONTINUATION
  primary_issue
  member_issues
  predecessor_attempt_refs
  delivery_pr_history
  pr = one active material delivery candidate at a time
```

A replacement executor, replacement PR, new attempt, target drift or acceptance replay does not create a new responsibility. Responsibility split/transfer/supersession is a semantic authority event, not a scope-string comparison.

Historical `TASK.kind=CHILD` records remain immutable and readable. Runtime may project their provider topology into a responsibility-shaped read view; it must not rewrite historical identity.

## 2. Parent TASK is the control plane

Do not create a second mutable `PARENT_CONTROL` authority store.

Native Parent TASK may expose:

```text
control_plane
  bootstrap_state
  current_acceptance_epoch_id
  acceptance_basis_registry
  responsibility_registry
  authority_grant_refs
```

Release is per responsibility:

```text
PRD-001 READY
PRD-002 BLOCKED_DEPENDENCY
PRD-003 READY
```

`bootstrap_state=ESTABLISHED` means the parent acceptance/control basis exists. It is not an engineering PASS or Owner merge token.

## 3. Acceptance Epoch and Review Lease are different axes

`ACCEPTANCE_EPOCH` means:

> which adopted project acceptance basis is governing.

It contains project-protocol identity, protected-surface identity, adoption provenance and basis-change classification. It MUST NOT contain candidate/base/environment freshness.

`REVIEW_LEASE` continues to mean:

> whether evidence/verdict is fresh for the exact candidate, base, integration tree, dependencies, environment and context.

Native Review Leases bind `acceptance_epoch_id` and `acceptance_profile_digest`. Those fields are optional for legacy leases so history remains readable.

## 4. Acceptance change: proposal -> authority -> adoption -> epoch

Reviewer and Super Reviewer are productive roles and may improve the acceptance surface where valuable. Discovery does not automatically change the governing basis.

```text
ACCEPTANCE_SURFACE_DEFECT / IMPROVEMENT
  -> ACCEPTANCE_CHANGE_PROPOSAL
  -> scoped authority evaluation
  -> adoption
  -> new ACCEPTANCE_EPOCH
  -> fresh same-stage attempt
  -> required replay
```

Record separate principals where they differ:

```text
PROPOSED_BY
IMPLEMENTED_BY
ADOPTED_BY
RISK_ACCEPTED_BY
```

## 5. Change kind and risk effect are orthogonal

`change_kind` describes what changed:

```text
DEFECT_REPAIR
COVERAGE_EXTENSION
METHOD_CHANGE
ORACLE_CHANGE
BASELINE_CHANGE
TOLERANCE_CHANGE
REQUIREMENT_CHANGE
CLARIFICATION
```

`risk_effect` describes the acceptance effect:

```text
STRENGTHENING
NEUTRAL
RELAXING
UNKNOWN
```

`RELAXING` and `UNKNOWN` require separately scoped `RISK_RELAXATION` authority. A label such as `CLARIFICATION` cannot bypass this check.

## 6. Authority is provenance-bearing and scoped

Do not infer authority from a role label or Boolean.

Capabilities are separate:

```text
ROLE_EXECUTION
PRODUCT_WRITE
ACCEPTANCE_POLICY_WRITE
RISK_RELAXATION
MERGE
```

An `AUTHORITY_GRANT` names principal, capability, parent/responsibility/epoch scope, issuer, instruction reference, source/authentication provenance, issue time, expiry and revocation.

Coordinator role does not imply merge or risk-relaxation authority.

## 7. Acceptance Profile is the responsibility-specific applicable subset

The Project Protocol is the immutable/versioned catalog. A native Responsibility TASK points to one authoritative Acceptance Profile instead of duplicating `TASK.acceptance`.

The profile explicitly selects criteria and binds each required role to project-declared verification methods. Common MUST validate:

```text
selected criterion
AND criterion role requirement
AND method declared by criterion
AND role in method.applies_to_roles
AND harness/gate binding
AND required evidence classes
```

Applicability is explicit; Common does not guess project semantics.

The profile is content-addressed by canonical `digest`, and native stage/review-lease evidence binds that digest.

## 8. Historical evidence is immutable

Never mutate evidence to say that an old observation became false.

```text
EV-17
candidate=abc
AE-001
PASS
```

remains historical truth.

Current validity is derived from:

```text
EVIDENCE + CURRENT CANDIDATE/BASIS/PROFILE/SURFACE/ENV/DEPENDENCIES
  -> EVIDENCE_VALIDITY projection
```

## 9. Replay is dependency-aware and fail-conservative

Replay may be selective only when declared material-input/rerun-policy data proves the affected method set.

```text
known dependency map -> selective replay allowed
unknown impact        -> full required-set replay
```

Candidate, dependency, environment, project protocol, Acceptance Profile, protected fixture/helper/oracle/toolchain and target-integration changes can all invalidate evidence.

## 10. v3.2 is frozen; v3.5 is the future nested Coder protocol

`engineering-pr-delivery-v3.2/**` is not modified by #492 implementation.

The nested Coder integration is a separate responsibility (#494) and will create additive `engineering-pr-delivery-v3.5` from an exact pinned v3.2 basis.

Local responsibility and nested engineering responsibility must remain distinguishable; v3.5 completion may not mean Local Reviewer/Super Reviewer lifecycle completion.
