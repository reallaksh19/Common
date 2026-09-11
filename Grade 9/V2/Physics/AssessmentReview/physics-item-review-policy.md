# Physics Item Review Policy — v1.0.0

## Purpose

This policy separates **what the source visibly contains** from **what Physics can safely conclude**. It is applied before any learner attempt is interpreted.

Mandatory order:

```text
normalized source
→ source-integrity review
→ item-validity review
→ diagnostic-use rule
→ learner inference later
```

## Source integrity

`CLEAN` means the preserved source is sufficiently intact for review. It does not certify the Physics.

`TYPOGRAPHIC_OR_OCR_AMBIGUITY` means notation/text may be damaged or uncertain. Resolution requires rendered-source inspection. Without that inspection, the review must stay `UNRESOLVED`; no silent correction is allowed.

`DATA_ERROR` means the source data themselves are defective or mutually inconsistent.

`TRUNCATED_OR_MISSING_FIGURE` means a physically meaningful required representation is absent or truncated. The missing graph/diagram may not be reconstructed from expectation or from the answer key.

`REVIEW_REQUIRED` is the fail-closed source state when current evidence is insufficient for certification.

## Item validity

`CLEAN` means the item is physically and mathematically usable under its stated information.

`VALID_ASSUMPTION_SENSITIVE` means the result is valid only under a model assumption that must remain explicit in the review.

`VALID_MULTIPLE_MODELS_OR_INTERPRETATIONS` means more than one physically legitimate interpretation/model survives the written source. The review must preserve the alternatives/conditions and cannot punish a learner for choosing another valid interpretation.

`UNDERDETERMINED` means the requested result is not uniquely determined by the information given.

`MATHEMATICAL_OR_DOMAIN_ISSUE` means the item is not a valid assessable Physics task as written (for example, no requested quantity, physically impossible premise, or domain defect).

`KEY_ERROR` means the source answer-key assertion conflicts with canonical reviewed Physics.

`DATA_ERROR` means numerical/physical data prevent a valid unique interpretation.

`TRUNCATED_OR_MISSING_FIGURE` means the item cannot be completed because a required representation is absent.

`REVIEW_REQUIRED` means the item cannot yet support confident diagnostic inference.

## Diagnostic use

```text
FULL
PARTIAL
POSITIVE_EVIDENCE_ONLY
EXCLUDE_FROM_NEGATIVE_INFERENCE
```

Core safety rules:

- `UNDERDETERMINED` cannot generate negative learner evidence.
- `MATHEMATICAL_OR_DOMAIN_ISSUE`, `DATA_ERROR`, `TRUNCATED_OR_MISSING_FIGURE`, and `REVIEW_REQUIRED` cannot become learner-failure evidence.
- unresolved `TYPOGRAPHIC_OR_OCR_AMBIGUITY` is excluded from negative inference;
- `VALID_ASSUMPTION_SENSITIVE` is usable only with the preserved assumption;
- multiple valid models/interpretations cannot be forced into one source-key answer;
- source keys are assertions, not authority.

## Representations

Physics meaning can live in a graph, scale, arrow, vector direction, sign convention, reference frame, option figure or motion diagram. Review bindings therefore carry exact source representation IDs and digests from P-A.

`reconstruction_performed=true` is forbidden by v1 for missing/truncated source representations.

## Provenance

Reference registry decisions are `AI_ASSISTED_REFERENCE_REVIEW` with `human_assessment_expert_review=false`. Human expert authorization, where required by later release gates, remains a separate event.
