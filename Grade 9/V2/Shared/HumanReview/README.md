# V2 Shared Human Review Intake

This directory defines how authorized human review evidence is ingested and projected into subject, pedagogy, assessment (when a subject policy requires it), and visual quality gates.

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

A policy declares its active review dimensions through `required_pass_submissions`. The legacy Math path remains `SUBJECT/PEDAGOGY/VISUAL`; subjects that require an independent assessment gate may additionally declare `ASSESSMENT` and map dimensions to subject-specific quality-state names with `quality_state_by_dimension`.

For multi-artifact products, `artifact_sha256_refs` on the candidate and `candidate_artifact_sha256_refs` on each submission provide exact byte custody for the full artifact set. `require_exact_artifact_set_binding=true` makes that set binding mandatory.

A `REAL_RELEASE` projection requires a `REAL` reviewer registry. `TEST_ONLY` fixtures are permanently non-releaseable.
