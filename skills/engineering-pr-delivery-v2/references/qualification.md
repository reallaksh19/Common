# Takeover Qualification — Expert Engineering Gate

## Purpose

Takeover qualification answers one question **before a replacement agent takes custody**:

> Does this candidate demonstrate enough live-repository and domain-engineering competence to be trusted with the next unresolved implementation boundary?

It is not the task itself, not a recovery checklist, not a theory quiz, and not permission to merge.

## Qualification is first

After a prior agent disappears or custody changes, the candidate begins READ_ONLY and performs only the minimal bootstrap needed to locate:

```text
repository
chain / ACTIVE.md
latest accepted endpoint
PR
QUESTION_SET_ID
QUALIFICATION_BASIS_HEAD
Q1-Q5
```

The candidate then takes the exam **before substantive recovery/reconciliation**.

It may read pinned code/tests/data/roadmaps/sources and perform calculations needed to answer. It may not mutate accepted engineering state, advance custody, create an accepted recovery endpoint, change production/tests/oracles/roadmaps, or resume AUTO MODE.

## PASS is not WRITE_ALLOWED

Qualification proves competence, not current-state safety.

After independent PASS:

```text
QUALIFICATION_STATE: PASS
CUSTODY_STATE: QUALIFIED_PENDING_RECONCILIATION
WRITE_AUTHORITY: READ_ONLY
```

Only then may the candidate reconcile live PR/main, crash-window commits, active-chain overlap, roadmap/source changes, orphan endpoints, reviews/checks, and validation drift. If that reconciliation is safe, custody may become `HELD` and write authority may become `WRITE_ALLOWED`.

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

Hard rule:

```text
candidate_id == verifier_id
-> INVALID_SELF_VERIFIED
```

## Mandatory five questions

The headings remain stable for compatibility, but their technical meaning is strict.

### Q1 — Production Trace

This is **production reconstruction**, not “describe the flow.”

Require a real object/case/value from the current task, such as:

- actual FEA element/node/load case and mesh hash;
- actual WRC geometry/load vector and transformed component;
- actual CAESAR record/pointer/cardinality and byte span;
- actual production request/model/result identity.

The candidate must extract exact repository identifiers/data and trace the same object/value through the real production boundaries. Generic architecture prose fails.

Required structured fields:

```text
Repository anchors:
Production object/case:
Required technical work:
Required numerical/technical evidence:
First authority/ownership boundaries:
Fail if:
```

### Q2 — Current Unresolved Problem / Failure Isolation

Require a real calculation or technically exact reconstruction tied to the current unresolved issue.

Examples:

- T6 shape-function derivatives, Jacobian and `det(J)` at a stated integration point;
- frame stiffness/end-force/reaction calculation;
- WRC `r x F`, transferred moment and local component mapping;
- pressure/stress/unit transformation;
- fixed-format I13 pointer/cardinality/physical-span arithmetic;
- parser/state-machine/hash reconstruction where arithmetic is not the natural domain.

The candidate must state predicted values at relevant implementation boundaries, identify the first wrong boundary, and give an observation that falsifies the diagnosis.

Required fields:

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

Require exact source/engineering/software ownership, not policy recitation.

The candidate must connect the current implementation boundary to authoritative sources/inputs/roadmap constraints, state what may and may not change, and reject at least one plausible but invalid shortcut.

Required fields:

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

Require an independent expected result. Production output cannot be its own oracle.

Acceptable classes include:

```text
hand/closed-form calculation
authoritative published example/code equation
independent arithmetic/postimage construction
cross-solver result
experimental evidence
independently frozen expected value
```

The candidate must show units, signs/coordinates, tolerance, provenance, and limitations where applicable.

Required fields:

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

This is a **safe implementation boundary exam**, not an implementation instruction.

The candidate must state what the smallest legitimate patch would be **if** the evidence authorizes a patch, including exact file/function/domain, expected before/after values, focused/public tests, negative test, protected unchanged domains, rollback condition, and when the correct action is NO PATCH.

Required fields:

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

A valid engineering-critical set normally requires:

```text
exactly 5 questions
>=3 questions with exact live-repository anchors
>=2 questions with numerical/hand or equivalent exact technical reconstruction
>=1 end-to-end production reconstruction
>=1 independent oracle
>=1 explicit falsifier
Q5 includes exact safe-patch and NO-PATCH boundaries
```

For non-numerical domains, a technically demanding substitute is allowed, for example exact byte offsets, pointer/cardinality arithmetic, parser transitions, topology ownership, deterministic hash/state reconstruction. “Explain the code” is not a substitute.

Reject questions that:

- can be answered without opening the pinned repository basis;
- could be copied unchanged into another project;
- ask mainly about completed work rather than the next unresolved boundary;
- use generic theory as the main evidence;
- lack actual IDs/data/files/functions/coordinates where available;
- lack calculation/reconstruction where technically applicable;
- ask the candidate to perform the patch as part of qualification;
- make production output the expected oracle.

Weak examples that must fail:

```text
Explain how the solver works.
Trace Writer2.
Describe the benchmark.
Which file would you inspect?
What would you change?
```

## Candidate artifact

Recommended path:

```text
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-answer.md
```

Minimum header:

```text
CHAIN_ID:
ENDPOINT_ID:
QUESTION_SET_ID:
QUALIFICATION_BASIS_HEAD:
CANDIDATE_ID:
LIVE_PR_HEAD_OBSERVED:
LIVE_MAIN_HEAD_OBSERVED:
```

The answer may report observed live drift, but it must answer the exam against the pinned basis. Full crash-window reconciliation is post-PASS work.

## Independent verdict

Recommended path:

```text
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-verdict.md
```

Score:

```text
Q1 __/20
Q2 __/20
Q3 __/20
Q4 __/20
Q5 __/20
TOTAL __/100
MINIMUM_QUESTION __/20
```

Default pass:

```text
total >= 92/100
minimum each >= 17/20
```

Verdicts:

```text
PASS_QUALIFIED_READ_ONLY
FAIL_READ_ONLY
DEFERRED_READ_ONLY
INVALID_SELF_VERIFIED
```

A PASS verdict does not itself grant `WRITE_ALLOWED`.

## Scoring emphasis

Use domain-expert evidence, not verbosity:

```text
Exact live repository evidence       /5
Correct technical reconstruction     /5
Independent engineering reasoning    /4
Falsifier / failure isolation        /3
Authority / safe patch protection    /3
                                      20
```

Automatic fail for fabricated repository evidence, unsafe source/authority assumptions, production-as-oracle reasoning, tolerance weakening to force green, NOT_RUN represented as PASS, or self-verification.
