# Mathematics V2 M-L — exact-product mature-quality gate

Implements the executable release-gate infrastructure required by #247. It does **not** declare the current Mathematics product mature.

## State separation

The gate tracks these states independently:

```text
PUBLICATION_ENGINEERING
SUBJECT_CORRECTNESS
PEDAGOGICAL_DESIGN
ASSESSMENT_DESIGN
VISUAL_USABILITY
MATURE_DESIGN_QUALITY
REFERENCE_COMPARABILITY
```

Learning effectiveness is separate:

```text
NOT_RUN
PILOT_EVIDENCE
STUDY_REQUIRED
VALIDATED
```

A mature-looking or machine-green artifact does not imply learning effectiveness.

## Exact candidate custody

`math-exact-candidate-binding.schema.json` binds a candidate to the selected M-K generation report, the Run A/B reproducibility proof, Core2 and coverage digests, Core1 authorization state, and—when materialized—the exact two PDF artifact hashes and publication-manifest digests.

Any artifact-set digest change invalidates prior review evidence. Human and frozen-reference evidence must bind both the candidate digest and the exact artifact-set digest.

## Required sequence

```text
exact candidate binding
→ machine falsifiers / exact publication custody
→ AI pre-review
→ authorized Mathematics subject review
→ authorized pedagogy review
→ authorized assessment review
→ authorized visual/usability review
→ frozen-reference comparative validation
→ V2_MATURE_INSTRUCTIONAL_PRODUCT
```

The frozen mature reference is final-validation-only and cannot be a normal producer input.

Subject, pedagogy and visual review receipts are normalized from the shared HumanReview authority. Assessment design remains a separate Math review dimension because the existing shared review intake currently covers subject, pedagogy and visual review only.

## Current repository state

M-G promotion now runs for real, so M-K materializes a Core1 plan and the
renderer (`Publication/engine/realize_math_core_products.py`) produces a real
two-product package. The bound PCK carries AI-assisted reference review only, so
`pck_release_legal` is `false` and `pck_expert_review_state` is `PENDING`.

`build_rendered_binding()` binds the real rendered package. Evaluating it in
`REAL_RELEASE` mode gives:

```text
candidate_class              RENDERED_TWO_PRODUCT_EXACT_CANDIDATE
materialization_state        RENDERED_EXACT
core1_authoring_status       PROVISIONAL_PLAN_READY
pck_expert_review_state      PENDING
PUBLICATION_ENGINEERING      PASS
SUBJECT_CORRECTNESS          NOT_RUN
PEDAGOGICAL_DESIGN           NOT_RUN
ASSESSMENT_DESIGN            NOT_RUN
VISUAL_USABILITY             NOT_RUN
MATURE_DESIGN_QUALITY        BLOCKED
REFERENCE_COMPARABILITY      NOT_RUN
learning effectiveness       NOT_RUN
mature product class         NOT_ELIGIBLE
```

with blockers including `M-L:PCK_EXPERT_REVIEW_PENDING`,
`M-L:AI_PRE_REVIEW_NOT_RUN` and `M-L:REAL_RUNTIME_CANDIDATE_REQUIRED`.

Only `PUBLICATION_ENGINEERING` moved. That is the intended fail-closed state:
machine-green rendering is not a subject, pedagogy, assessment or visual PASS.
A candidate resting on provisional PCK can never be classified
`V2_MATURE_INSTRUCTIONAL_PRODUCT` — `PROVISIONAL_PCK_MARKED_MATURE` fires even
when every other gate is satisfied.

#247 must remain open until authorized human review evidence, bound to the exact
artifact-set digest, closes every required gate.

`build_fixture_binding()` (no render) still produces the semantic-only binding,
now in state `SEMANTIC_READY_RENDER_NOT_BOUND` rather than
`BLOCKED_UPSTREAM_PCK`.

## Test-only positive path

CI constructs a synthetic rendered two-product binding and test-only review receipts only to prove that the state machine can reach all quality PASS states in isolation. The resulting class is:

```text
TEST_ONLY_MATURE_GATE_LOGIC_PASS
```

It is always `release_evidence_eligible=false` and can never become `V2_MATURE_INSTRUCTIONAL_PRODUCT`.

## Validation

```bash
python 'Grade 9/V2/Mathematics/Validation/MatureGate/contracts/validate_contracts.py'
python 'Grade 9/V2/Mathematics/Validation/MatureGate/tests/test_math_mature_gate.py'
```

Passing these checks proves release-gate logic, exact-hash custody, authority separation, and fail-closed behaviour. It is not an authorized subject/pedagogy/assessment/visual PASS and is not evidence of learning efficacy.
