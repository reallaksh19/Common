# Physics V2 — P-B Source Integrity / Item Validity / Assessment Safety

Implements issue **#250** under Physics assessment-first roadmap **#248** / programme **#234**.

P-B consumes the exact source-faithful `QuestionSet` produced by P-A and creates the mandatory safety boundary before any learner attempt can influence learner state:

```text
QuestionSet (P-A source/representation custody)
    ↓
PhysicsSourceIntegrityReview
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

P-B answers only:

- Is the Physics source intact enough to interpret?
- Is the item physically/mathematically valid as written?
- Which model, frame, sign convention or assumption is required?
- What canonical answer set or answer conditions are defensible?
- Is a source answer-key assertion consistent with canonical Physics?
- What diagnostic use is safe?

P-B does **not** perform question→scope mapping, problem-family modelling, learner diagnosis, Study Synthesis, Core1/Core2 authoring or publication.

The review engine deliberately accepts no `AttemptSet` and no learner-state input. `attempt_data_consumed=false` and `review_precedes_attempt_interpretation=true` are contract invariants.

## Two distinct judgments

Source integrity and item validity are deliberately separate.

```text
source_integrity_state
  CLEAN
  TYPOGRAPHIC_OR_OCR_AMBIGUITY
  DATA_ERROR
  TRUNCATED_OR_MISSING_FIGURE
  REVIEW_REQUIRED

validity_state
  CLEAN
  VALID_ASSUMPTION_SENSITIVE
  VALID_MULTIPLE_MODELS_OR_INTERPRETATIONS
  UNDERDETERMINED
  MATHEMATICAL_OR_DOMAIN_ISSUE
  KEY_ERROR
  DATA_ERROR
  TRUNCATED_OR_MISSING_FIGURE
  REVIEW_REQUIRED
```

A clean extraction can still contain a bad Physics question. A damaged source can contain a mathematically meaningful item that cannot yet be certified. The two states must not be collapsed.

## Representation custody

Each review is bound to the exact P-A representation IDs, digests, kinds and statuses. P-B therefore knows whether an answer depends on a graph, option figure, motion diagram or missing/truncated representation.

A missing source graph remains missing. `reconstruction_performed=false` is required for the pilot and the engine rejects silent invention.

## Assumption / frame custody

`VALID_ASSUMPTION_SENSITIVE` is allowed only when the review preserves the assumption needed for the claimed answer.

The review also records frame/sign assumptions separately, e.g. upward-positive, common ground frame, or positive direction along the initial velocity.

## OCR / notation ambiguity

`TYPOGRAPHIC_OR_OCR_AMBIGUITY` may be resolved only by inspecting the rendered source. If the rendered source is not available, the review must stay explicitly `UNRESOLVED`; it cannot be silently normalized into confident Physics.

The public-synthetic P-A fixture has no rendered page artifact. Q14 is intentionally below the P-A confidence threshold, so P-B leaves its potential notation/source ambiguity unresolved and excludes it from negative inference.

Low confidence is not itself a proof of a typo; it is a reason to withhold certification until source inspection.

## Pilot decisions

Reference cases in the Motion fixture:

- **Q3** — `VALID_ASSUMPTION_SENSITIVE`: `-4 m/s²` is valid under uniform acceleration (or as an explicitly average acceleration); the assumption is preserved.
- **Q8** — ordinary graph-dependent item: the v–t representation is present and digest-bound.
- **Q9** — `MATHEMATICAL_OR_DOMAIN_ISSUE`: the preserved stem describes a release but asks no assessable quantity.
- **Q10** — `UNDERDETERMINED`: the two-phase data do not specify one target/end condition.
- **Q13** — `TRUNCATED_OR_MISSING_FIGURE`: the graph needed for acceleration is missing and cannot be invented.
- **Q14 + Q14.a/b/c** — unresolved `TYPOGRAPHIC_OR_OCR_AMBIGUITY` / `REVIEW_REQUIRED` because P-A records extraction confidence 0.89 and no rendered source is available in the fixture.

Every parent question and explicit subpart has exactly one review.

## Source-key firewall

A source answer key is evidence from the source, never canonical Physics truth.

```text
source assertion
    ↓ compare only
canonical reviewed answer / conditions
```

For option-keyed items, disagreement must become explicit `KEY_ERROR`. The source key is never allowed to overwrite the canonical reviewed option set.

## Review provenance

The pilot registry states:

```text
review_class = AI_ASSISTED_REFERENCE_REVIEW
human_assessment_expert_review = false
```

This is architecture/reference evidence, not an authorized human Physics/assessment-expert pass.

## Exit gate

P-B is complete only when:

1. P-A source/representation fidelity validation succeeds first;
2. every normalized question and subpart has exactly one review;
3. every review is bound to the exact source question digest;
4. every source representation binding matches the P-A representation digest/status;
5. OCR ambiguity is rendered-source-checked or explicitly unresolved;
6. missing/truncated figures are never reconstructed;
7. assumption-sensitive answers preserve the needed model assumption;
8. underdetermined/domain-defective items cannot create negative learner evidence;
9. source-key mismatch cannot override canonical Physics;
10. review-required items fail closed;
11. the engine consumes no learner attempt/state data;
12. deterministic replay is byte-stable.

Next phase after P-A/P-B merge: **#251 / P-C — scope, system/frame/model and problem-family resolution**.
