# Mathematics V2 — M-B Assessment Review / Safety Gate

Implements issue **#237** under Math catch-up parent **#235** and programme **#234**.

This phase consumes the source-faithful `QuestionSet` produced by M-A and creates the mandatory safety boundary before any learner attempt is interpreted:

```text
QuestionSet (M-A)
    ↓
AssessmentItemReview
    ↓
DiagnosticUsePolicy
    ↓
AssessmentReviewBundle
    ↓
only later: AttemptSet interpretation / Learner Intelligence
```

## Authority boundary

M-B answers only:

- Is the assessment item mathematically usable as written?
- What answer set or answer conditions are mathematically valid?
- Is a source answer key consistent with the canonical review?
- What diagnostic use is safe for this item?

M-B **does not** perform learner diagnosis, question→topic mapping, problem-family modelling, Core1 study synthesis, Core2 hint design, or publication.

The review engine deliberately has no `AttemptSet` input. `attempt_data_consumed=false` is a contract invariant.

## Validity states

```text
VALID
VALID_MULTIPLE_SOLUTIONS
UNDERDETERMINED
AMBIGUOUS
KEY_ERROR
DATA_ERROR
REVIEW_REQUIRED
```

## Diagnostic-use states

```text
FULL
PARTIAL
POSITIVE_EVIDENCE_ONLY
EXCLUDE_FROM_NEGATIVE_INFERENCE
```

The policy is fail-closed. In particular:

- `UNDERDETERMINED` cannot create negative evidence or confident diagnosis.
- `VALID_MULTIPLE_SOLUTIONS` must preserve every accepted solution represented by the review.
- `KEY_ERROR` preserves canonical mathematics and marks the source key as a conflicting source assertion.
- `DATA_ERROR` and `REVIEW_REQUIRED` cannot become confident learner diagnosis.

## Pilot fixture decisions

The M-A mixed Grade-9 fixture is reviewed item-by-item and subpart-by-subpart.

Important reference cases:

- **Q5** — ordinary valid MCQ; source key `d` agrees with canonical answer.
- **Q9** — `UNDERDETERMINED`; substituting `x=y` gives `(2+c)x=8`, so there is no unique `c`.
- **Q12** — `VALID_MULTIPLE_SOLUTIONS`; both `(0,2sqrt(3))` and `(3,-sqrt(3))` are valid third vertices.
- **Q14** — valid multi-stage item; Q14.a, Q14.b and Q14.c each have independent review identities.

Every parent question and every explicit subpart must have exactly one review entry.

## Source-key rule

A source answer key is evidence from the assessment source, never mathematical authority.

```text
source key
   ↓ compare only
canonical reviewed answer set
```

If they disagree, the item must be explicitly classified `KEY_ERROR`; the source key is never allowed to overwrite the canonical reviewed answer.

## Review provenance

The pilot registry is marked:

```text
review_class = AI_ASSISTED_REFERENCE_REVIEW
human_assessment_expert_review = false
```

This is architecture/reference implementation evidence. It is **not** represented as an authorized human assessment-expert pass.

## M-B exit gate

M-B is complete only when:

1. M-A source-fidelity validation succeeds first.
2. every normalized question and subpart has exactly one explicit review;
3. every review is bound to the exact M-A source digest;
4. each validity state has an explicit diagnostic-use rule;
5. underdetermined/ambiguous/review-required states fail closed for negative diagnosis;
6. multiple-solution items preserve the valid answer set;
7. source-key disagreement cannot override canonical mathematics;
8. the review engine consumes no attempt or learner-state data;
9. deterministic replay is byte-stable.

Next phase: **#238 / M-C — scope reconciliation and Question→Math authority mapping**.
