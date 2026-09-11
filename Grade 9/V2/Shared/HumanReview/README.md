# V2 Shared Human Review Intake

This directory defines how authorized human review evidence is ingested and projected into subject, pedagogy, and visual quality gates.

It does **not** decide canonical truth, learner state, Study Synthesis, Learning Design, publication structure, or benchmark comparison. It cannot manufacture reviewer authorization and it cannot treat AI/CI output as human approval.

Core flow:

```text
ExactCandidateBinding
+ ReviewerAuthorizationRegistry
+ HumanReviewPolicy
+ subject-specific rubrics
+ HumanReviewSubmission[]
        ↓
HumanReviewIntakeResult
        ↓
QualityReviewSummary projection
```

A `REAL_RELEASE` projection requires a `REAL` reviewer registry. `TEST_ONLY` fixtures are permanently non-releaseable.
