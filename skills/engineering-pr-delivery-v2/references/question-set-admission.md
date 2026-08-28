# Question-Set Admission Gate

## Purpose

Qualification must be first, but the candidate must not be forced to take an invalid exam. Before Q1-Q5 are answered, perform a narrow READ_ONLY admission check on the question set itself.

This is **not engineering recovery**, not a second qualification, and not task execution. It only decides whether the pre-authored exam is legitimate enough to administer.

## Admission states

```text
QUESTION_SET_ADMISSION_STATUS:
VALID
STALE
MALFORMED
AUTHORITY_CONTAMINATED
INSUFFICIENT_TECHNICAL_DEPTH
```

Only `VALID` may proceed to takeover qualification.

## Required admission checks

Confirm:

1. exactly Q1-Q5 exist and the expert-question quality gate passes;
2. `QUALIFICATION_BASIS_HEAD` exists and is retrievable;
3. question-set repository anchors resolve against the pinned basis;
4. roadmap, source, benchmark, oracle, methodology and release-authority assumptions embedded in the questions are valid for that basis;
5. no question relies on an unapproved owner-roadmap mutation or other unproven authority;
6. the set was not weakened/re-authored by the candidate for self-qualification.

A question set can therefore be technically current but `AUTHORITY_CONTAMINATED`.

## Admission authority

For a normal version-3 endpoint, the outgoing endpoint author pre-authors the exam and records its source/roadmap bindings. On takeover, an independent admission authority/verifier or deterministic validator confirms admission before the candidate answers.

For a legacy v1/v2 endpoint, admission is mandatory because older endpoints may not satisfy current question-quality or authority-binding rules.

The candidate may provide read-only evidence but cannot be the sole authority that converts its own set to `VALID`.

Recommended receipt:

```text
QUALIFICATION_PROTOCOL_VERSION: 3
CHAIN_ID:
ENDPOINT_ID:
QUESTION_SET_ID:
QUALIFICATION_BASIS_HEAD:
QUESTION_SET_ADMISSION_STATUS: VALID
ADMISSION_AUTHORITY_ID:
BASIS_RETRIEVABLE: TRUE
TECHNICAL_DEPTH_STATUS: PASS
ROADMAP_AUTHORITY_STATUS: VALID | NOT_APPLICABLE
SOURCE_ORACLE_AUTHORITY_STATUS: VALID | NOT_APPLICABLE
LEGACY_SET: TRUE | FALSE
ADMISSION_EVIDENCE:
```

If a candidate is already identified, also record `CANDIDATE_ID`; `ADMISSION_AUTHORITY_ID == CANDIDATE_ID` cannot by itself establish `VALID`.

## Failure handling

```text
VALID
-> take Q1-Q5

STALE / MALFORMED / AUTHORITY_CONTAMINATED / INSUFFICIENT_TECHNICAL_DEPTH
-> remain READ_ONLY
-> independent question authority / Owner repairs or adopts a valid set
-> candidate does not self-author and self-qualify
```

Question-set repair changes the exam, not the engineering task. The replacement still qualifies before substantive crash-window reconciliation.
