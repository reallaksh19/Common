# Post-Basis Drift Classification

## Purpose

Qualification proves competence against the accepted qualification basis. After PASS, the replacement reconciles the live repository while still READ_ONLY. This step decides whether that qualification still covers the engineering boundary that now exists.

## Required classification

```text
POST_BASIS_DRIFT:
NONE
METADATA_ONLY
MATERIAL_WITHIN_QUALIFIED_BOUNDARY
MATERIAL_BOUNDARY_CHANGED
AUTHORITY_CHANGED
CONTAMINATED
```

`NONE` means live material state equals the qualification basis.

`METADATA_ONLY` means later changes are relay/navigation/documentary metadata with no production, test, benchmark, source, oracle, methodology, release-authority or roadmap-intent effect.

`MATERIAL_WITHIN_QUALIFIED_BOUNDARY` means material code/evidence changed after the basis, but the exact unresolved engineering boundary tested by Q1-Q5 is demonstrably unchanged.

`MATERIAL_BOUNDARY_CHANGED` means the implementation problem, expected patch boundary, production trace, benchmark, numerical behavior or required validation changed.

`AUTHORITY_CHANGED` means roadmap intent, engineering source, oracle, methodology, publication/release authority or another governing boundary changed.

`CONTAMINATED` means safe separation cannot be proven.

## Authority consequence

```text
NONE | METADATA_ONLY
-> QUALIFICATION_COVERAGE: RETAINED
-> WRITE_ALLOWED may be granted only if all other current-state authority checks are clear

MATERIAL_WITHIN_QUALIFIED_BOUNDARY
-> QUALIFICATION_COVERAGE: INDEPENDENT_CONFIRMATION_REQUIRED
-> an independent reviewer must explicitly confirm coverage
-> only then may current-state authority clear

MATERIAL_BOUNDARY_CHANGED | AUTHORITY_CHANGED | CONTAMINATED
-> QUALIFICATION_COVERAGE: REQUALIFICATION_REQUIRED
-> WRITE_AUTHORITY: READ_ONLY
-> independently authored fresh Q1-Q5 against the recovered basis
-> qualification again before custody/write
```

The candidate must not self-classify material drift as covered and self-enable writes.

## Reconciliation receipt

Recommended fields:

```text
QUALIFICATION_PROTOCOL_VERSION: 3
CHAIN_ID:
ENDPOINT_ID:
QUESTION_SET_ID:
QUALIFICATION_BASIS_HEAD:
CANDIDATE_ID:
RECONCILIATION_REVIEWER_ID:
LIVE_HEAD:
POST_BASIS_COMMITS:
POST_BASIS_DRIFT:
QUALIFICATION_COVERAGE:
CURRENT_STATE_AUTHORITY: CLEAR | BLOCKED
WRITE_AUTHORITY_DECISION: READ_ONLY | WRITE_ALLOWED
RECONCILIATION_EVIDENCE:
```

When `WRITE_AUTHORITY_DECISION: WRITE_ALLOWED`, the reviewer must be independent of the candidate and all other roadmap/source/oracle/overlap/validation gates must also be clear.

## Reality-check example

If an accepted endpoint is at `5dc...` and live head `02fb...` contains only relay-pointer commits:

```text
POST_BASIS_DRIFT: METADATA_ONLY
QUALIFICATION_COVERAGE: RETAINED
```

If the later commits modify the solver, expected benchmark, owner roadmap authority, or the safe patch boundary, the classification must escalate and may require requalification.
