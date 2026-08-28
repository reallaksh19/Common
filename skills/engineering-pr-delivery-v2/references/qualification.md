# Takeover Qualification — Expert Engineering Gate

## Purpose

Takeover qualification answers, before a replacement takes custody:

> Does this candidate demonstrate enough live-repository and domain-engineering competence to be trusted with the next unresolved implementation boundary?

It is not the task, not crash-window reconciliation, not a theory quiz, and not merge permission.

## Precondition — admitted question set

Before the candidate answers Q1-Q5, the set must pass `references/question-set-admission.md`:

```text
QUESTION_SET_ADMISSION_STATUS: VALID
```

`STALE`, `MALFORMED`, `AUTHORITY_CONTAMINATED`, or `INSUFFICIENT_TECHNICAL_DEPTH` remain READ_ONLY and require independent repair/adoption. The candidate cannot weaken or self-admit its own replacement exam.

## Qualification is first

After admission, the candidate answers the exam **before substantive recovery/reconciliation**. It may read pinned code/tests/data/roadmaps/sources and perform calculations required by Q1-Q5. It may not mutate accepted engineering state, advance custody, create an accepted recovery endpoint, change production/tests/oracles/roadmaps, or resume AUTO MODE.

## PASS is not WRITE_ALLOWED

Version-3 artifacts declare:

```text
QUALIFICATION_PROTOCOL_VERSION: 3
```

Valid pass:

```text
VERDICT: PASS_QUALIFIED_READ_ONLY
```

After PASS:

```text
QUALIFICATION_STATE: PASS
CUSTODY_STATE: QUALIFIED_PENDING_RECONCILIATION
WRITE_AUTHORITY: READ_ONLY
```

Only post-basis reconciliation and drift classification can retain/confirm qualification coverage and clear current-state authority.

## Roles

```text
ENDPOINT / QUESTION AUTHOR
  pre-authors Q1-Q5

ADMISSION AUTHORITY
  confirms the set is legitimate enough to administer

INCOMING CANDIDATE
  answers while READ_ONLY

INDEPENDENT VERIFIER
  evaluates correctness and evidence
```

The candidate cannot be its own verifier, and cannot be the sole admission authority for its own set.

## Q1 — Production Trace

Require a real current object/case/value and exact repository anchors. Examples: actual FEA element/node/load case/hash, WRC geometry/load vector, CAESAR record/pointer/cardinality/byte span, or exact request/model/result identity.

Required fields:

```text
Repository anchors:
Production object/case:
Required technical work:
Required numerical/technical evidence:
First authority/ownership boundaries:
Fail if:
```

## Q2 — Current Unresolved Problem / Failure Isolation

Require real calculation or exact technical reconstruction tied to the unresolved problem: T6 Jacobian/det(J), frame stiffness/end force, WRC `r x F`/local mapping, stress/unit transformation, fixed-format I13 pointer/cardinality arithmetic, parser/hash/state reconstruction, or equivalent.

```text
Repository anchors:
Calculation/reconstruction:
Required numerical/technical evidence:
Predicted intermediate values:
First wrong boundary:
Falsifier:
Fail if:
```

## Q3 — Authority / Invariant

Require exact source/engineering/software ownership, what may/may not change, a decisive falsifier, and a plausible invalid shortcut.

```text
Repository anchors:
Required technical work:
Authority/source trace:
Protected invariant:
First wrong boundary:
Falsifier:
Invalid shortcut:
Fail if:
```

## Q4 — Independent Validation

Require an independent expected result: hand/closed-form calculation, authoritative published example/code equation, independent arithmetic/postimage, cross-solver, experiment, or independently frozen expected value. Production output cannot be its own oracle.

```text
Repository anchors:
Required technical work:
Independent oracle:
Required numerical/technical evidence:
Units/sign/tolerance:
Falsifier:
Fail if:
```

## Q5 — Next Contribution / Minimal Patch

This is a safe implementation-boundary exam, not an instruction to patch. Require exact first wrong boundary, smallest legitimate patch if evidence authorizes it, before/after values, protected domains, tests, rollback and NO-PATCH condition.

```text
Repository anchors:
Required technical work:
Safe patch boundary:
Expected before/after evidence:
Protected unchanged domains:
Validation required:
Negative test:
Rollback/falsifier boundary:
No-patch condition:
Fail if:
```

Do not write Q5 as an imperative implementation task.

## Set-level quality gate

Normally require exactly five questions; >=3 with exact repository anchors; >=2 numerical/hand or equivalent exact technical reconstructions; >=1 end-to-end production reconstruction; >=1 independent oracle; >=1 explicit falsifier; Q5 with safe-patch and NO-PATCH boundaries.

Reject questions that can be answered without the pinned repository basis, could be copied unchanged into another task, lack real IDs/data/files/functions where available, lack calculation where applicable, ask the candidate to perform the patch, or use production output as the oracle.

Weak examples that must fail:

```text
Explain how the solver works.
Trace Writer2.
Describe the benchmark.
Which file would you inspect?
What would you change?
```

## Scoring

Default engineering-critical pass:

```text
total >= 92/100
minimum each >= 17/20
```

Version-3 verdicts:

```text
PASS_QUALIFIED_READ_ONLY
FAIL_READ_ONLY
DEFERRED_READ_ONLY
INVALID_SELF_VERIFIED
```

PASS does not itself grant `WRITE_ALLOWED`.
