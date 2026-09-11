# Mathematics Item Review Policy v1

## Purpose

This policy defines the epistemic boundary between **assessment-item validity** and **learner inference**.

The mandatory order is:

```text
source-faithful normalized item
→ mathematical item review
→ diagnostic-use classification
→ learner attempt interpretation
```

Attempt evidence is never permitted to influence whether the assessment item itself is valid.

## Review questions

For every question or explicit subpart, the reviewer must determine:

1. Is the prompt mathematically well-posed?
2. Is the source data internally consistent?
3. Is there one answer, several legitimate answers, a condition set, or an explanation rubric?
4. If a source answer key exists, does it agree with the reviewed mathematics?
5. What diagnostic use is safe?

## State semantics

`VALID` means the item is well-posed for its intended mathematical demand.

`VALID_MULTIPLE_SOLUTIONS` means more than one mathematically valid solution exists and the complete accepted set or acceptance conditions must be preserved. It must never be collapsed to one source-preferred key.

`UNDERDETERMINED` means the supplied information does not select a unique answer demanded by the wording. It may support positive evidence from valid reasoning but cannot create negative evidence.

`AMBIGUOUS` means materially different reasonable interpretations remain. Negative learner inference is forbidden until ambiguity is resolved.

`KEY_ERROR` means the item mathematics is reviewable but the source answer-key assertion conflicts with the reviewed answer. Canonical mathematics wins; the source key remains preserved as provenance.

`DATA_ERROR` means erroneous or contradictory source data prevents safe item use.

`REVIEW_REQUIRED` means evidence is insufficient for a safe review decision. It fails closed for learner diagnosis.

## Canonical-answer representation

The registry separates:

```text
accepted_answers[]
accepted_option_labels[]
answer_conditions[]
uniqueness_status
```

This avoids forcing explanation items, condition-set items and multi-solution geometry into a single answer-key string.

## Diagnostic-use policy

The machine policy defines, for each validity state:

```text
positive_inference_allowed
negative_inference_allowed
confident_diagnosis_allowed
```

Later learner-intelligence phases must consume these constraints rather than infer safety from correctness alone.

## Canonical math references

`canonical_math_refs[]` in M-B are stable mathematical review anchors. M-B does not yet own full question→scope resolution; M-C resolves assessment scope and canonical graph bindings.

## Human authority

The checked-in pilot registry is an AI-assisted reference implementation with deterministic falsifiers. It does not claim authorized human assessment review. Any future release requiring such authority must attach review evidence separately.
