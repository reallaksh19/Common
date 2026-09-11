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

M-K currently closes repository-only semantic generation but correctly reports upstream Core1 PCK blockers. The production PCK promotion registry contains no fabricated human promotions, and not every assessment-scope full-teaching capability has a promoted PCK asset. Therefore the M-L exact binding is currently:

```text
candidate_class              SEMANTIC_COLD_START_EXACT_PACKAGE
materialization_state        BLOCKED_UPSTREAM_PCK
PUBLICATION_ENGINEERING      BLOCKED
SUBJECT_CORRECTNESS          NOT_RUN
PEDAGOGICAL_DESIGN           NOT_RUN
ASSESSMENT_DESIGN            NOT_RUN
VISUAL_USABILITY             NOT_RUN
MATURE_DESIGN_QUALITY        BLOCKED
REFERENCE_COMPARABILITY      NOT_RUN
learning effectiveness       NOT_RUN
mature product class         NOT_ELIGIBLE
```

This is the intended fail-closed state. #247 must remain open until a real rendered exact candidate exists and real authorized review evidence closes every required gate.

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
