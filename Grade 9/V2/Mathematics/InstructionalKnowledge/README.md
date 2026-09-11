# Mathematics V2 — Instructional Knowledge (M-G)

Tracking: #242 under Mathematics catch-up roadmap #235.

This authority owns the **Mathematics PCK lifecycle**, not learner treatment and not page rendering.

```text
Math PCK candidate
  + canonical capability/problem-family refs
  + provenance
  + applicability / limitations
        ↓
authorized HUMAN_SUBJECT + HUMAN_PEDAGOGY review
through Shared/HumanReview
        ↓
Math PCK Promotion Registry
        ↓
producer-legal PCK
```

## Non-negotiable boundary

`CANDIDATE != PROMOTED`.

The current candidate registry contains ten Math PCK pilot drafts required by #242. They are intentionally marked:

```text
lifecycle_status = CANDIDATE
review.status = PENDING_HUMAN_REVIEW
authoring_origin = AI_ASSISTED_DRAFT
```

The production promotion registry is intentionally empty until admissible human review evidence exists. CI or an AI agent cannot manufacture that authority.

A production promotion record must bind the exact candidate digest and prove:

```text
promotion_status = PROMOTED
review_source = HUMAN_REVIEW_INTAKE_RESULT
review_registry_class = REAL
review_dimensions includes SUBJECT and PEDAGOGY
producer_legal = true
```

Test-only promotion fixtures live downstream under `Core1Authoring/fixtures/` and are structurally non-releaseable.

## Pilot PCK coverage

The candidate set covers the ten M-G pilot jobs:

```text
EQUALITY_PRESERVATION
EXPRESSION_IDENTITY
BINOMIAL_SQUARE_RECONSTRUCTION
ORDERED_PAIR_SEMANTICS
SLOPE_AS_RATE_OF_CHANGE
COLLINEARITY_BY_COMMON_DIRECTION
SIMULTANEOUS_EQUATION_ELIMINATION
GEOMETRY_TO_ALGEBRA_BRIDGE
SOLUTION_VERIFICATION
WORD_TO_EQUATION_MODELLING
```

Each candidate carries capability refs, applicability conditions, anchor, representation path, ordinary-language bridge, reconstruction route, controlled contrast, worked-example family, misconception discriminator, repair route, verification method, fading dimensions, transfer family, limitations, provenance, review state, and digest.

This directory does not decide `VERIFY_ONLY`, `ACTIVE_STUDY`, `REPAIR_BEFORE`, `REPAIR_IN_UNIT`, or `PROBE_FIRST`. Those remain upstream Study Synthesis decisions.
