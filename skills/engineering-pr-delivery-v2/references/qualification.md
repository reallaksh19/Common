# Takeover Qualification — Expert Engineering Gate

## Purpose

Takeover qualification answers one question **before a replacement agent takes custody**:

> Does this candidate demonstrate enough live-repository and domain-engineering competence to be trusted with the next unresolved implementation boundary?

It is not the task itself, not a recovery checklist, not a theory quiz, and not permission to merge.

## Qualification is first

After a prior agent disappears or custody changes, the candidate begins READ_ONLY and performs only the minimal bootstrap needed to locate the repository, chain/ACTIVE.md, latest accepted endpoint, PR, `QUESTION_SET_ID`, `QUALIFICATION_BASIS_HEAD`, and Q1-Q5.

The candidate then takes the exam **before substantive recovery/reconciliation**. It may read pinned code/tests/data/roadmaps/sources and perform calculations needed to answer. It may not mutate accepted engineering state, advance custody, create an accepted recovery endpoint, change production/tests/oracles/roadmaps, or resume AUTO MODE.

## PASS is not WRITE_ALLOWED

Qualification proves competence, not current-state safety. Version-3 answer and verdict artifacts declare:

```text
QUALIFICATION_PROTOCOL_VERSION: 3
```

A valid pass verdict is:

```text
VERDICT: PASS_QUALIFIED_READ_ONLY
```

After PASS:

```text
QUALIFICATION_STATE: PASS
CUSTODY_STATE: QUALIFIED_PENDING_RECONCILIATION
WRITE_AUTHORITY: READ_ONLY
```

Only then may the candidate reconcile live PR/main, crash-window commits, active-chain overlap, roadmap/source changes, orphan endpoints, reviews/checks, and validation drift. If safe, custody may become `HELD` and write authority may become `WRITE_ALLOWED`.

Legacy qualification artifacts without `QUALIFICATION_PROTOCOL_VERSION: 3` retain the old verdict vocabulary for compatibility; they do not redefine the new version-3 authority model.

## Always-ready question set

Every non-terminal endpoint pre-authors exactly Q1-Q5 for the **next unresolved implementation boundary**. This is what makes abrupt loss recoverable.

A crash after the accepted endpoint may leave later commits. Those commits form a crash window; they do not erase the exam. The candidate qualifies against the pinned accepted basis first and reconciles the later material after PASS.

The question set becomes unusable only when its pinned basis/artifacts cannot be retrieved or the set is malformed. A candidate may not author an easier replacement set and use it to self-qualify.

## Roles

```text
ENDPOINT / QUESTION AUTHOR
  pre-authors Q1-Q5 before a crash can occur

INCOMING CANDIDATE
  answers against the pinned basis while READ_ONLY

INDEPENDENT VERIFIER
  evaluates technical correctness and evidence
```

`candidate_id == verifier_id` is invalid self-verification.

## Mandatory five questions

### Q1 — Production Trace

Production reconstruction, not “describe the flow.” Require a real object/case/value such as an actual FEA element/node/load case/hash, WRC geometry/load vector, CAESAR record/pointer/cardinality/byte span, or exact production request/model/result identity. The candidate extracts exact data and traces the same object/value through real boundaries.

Required fields:

```text
Repository anchors:
Production object/case:
Required technical work:
Required numerical/technical evidence:
First authority/ownership boundaries:
Fail if:
```

### Q2 — Current Unresolved Problem / Failure Isolation

Require a real calculation or exact technical reconstruction tied to the unresolved problem: T6 Jacobian/det(J), frame stiffness/end force, WRC `r x F`/local mapping, stress/unit transformation, fixed-format I13 pointer/cardinality arithmetic, parser/hash/state reconstruction, or equivalent. Require predicted intermediates, first wrong boundary and falsifier.

```text
Repository anchors:
Calculation/reconstruction:
Required numerical/technical evidence:
Predicted intermediate values:
First wrong boundary:
Falsifier:
Fail if:
```

### Q3 — Authority / Invariant

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

### Q4 — Independent Validation

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

### Q5 — Next Contribution / Minimal Patch

This is a **safe implementation boundary exam**, not an instruction to patch. The candidate states the smallest legitimate patch **if** evidence authorizes it, exact files/functions, expected before/after values, tests, protected domains, rollback and when NO PATCH is correct.

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

Do not write Q5 as `Implement...`, `Fix...`, `Modify...`, or another task imperative.

## Set-level quality gate

Normally require exactly five questions; >=3 with exact repository anchors; >=2 numerical/hand or equivalent exact technical reconstructions; >=1 end-to-end production reconstruction; >=1 independent oracle; >=1 explicit falsifier; and Q5 with safe-patch + NO-PATCH boundaries.

For non-numerical domains, exact byte offsets, pointer/cardinality arithmetic, parser transitions, topology ownership or deterministic hash/state reconstruction may substitute. “Explain the code” does not.

Reject questions that can be answered without the pinned repository basis, could be copied unchanged into another project, lack actual IDs/data/files/functions where available, lack calculation where applicable, ask the candidate to perform the patch, or make production output the oracle.

Weak examples that must fail:

```text
Explain how the solver works.
Trace Writer2.
Describe the benchmark.
Which file would you inspect?
What would you change?
```

## Candidate/verdict artifacts

Recommended answer header:

```text
QUALIFICATION_PROTOCOL_VERSION: 3
CHAIN_ID:
ENDPOINT_ID:
QUESTION_SET_ID:
QUALIFICATION_BASIS_HEAD:
CANDIDATE_ID:
LIVE_PR_HEAD_OBSERVED:
LIVE_MAIN_HEAD_OBSERVED:
```

Recommended verdict header adds:

```text
QUALIFICATION_PROTOCOL_VERSION: 3
VERIFIER_ID:
VERDICT_BASIS_HEAD:
AUTOMATIC_FAILURE_REASON:
```

Score Q1-Q5 /20. Default pass is total >=92/100 and every question >=17/20.

Version-3 verdicts:

```text
PASS_QUALIFIED_READ_ONLY
FAIL_READ_ONLY
DEFERRED_READ_ONLY
INVALID_SELF_VERIFIED
```

A PASS verdict does not itself grant `WRITE_ALLOWED`.
