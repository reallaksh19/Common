# Chemistry V2 — source-integrity and assessment-item review policy (C-B)

Implements issue #264 after C-A intake/source custody (#263).

## Boundary

C-B answers a narrow question before scope mapping or learner diagnosis:

> Can this normalized source assertion or assessment item safely influence Chemistry teaching, scope resolution, or learner evidence, and under what constraints?

The mandatory order is:

```text
Normalized ChemistrySourceSet / QuestionSet
→ source-integrity review
→ assessment-item validity review
→ diagnostic-use policy
→ only then C-C scope resolution / C-E learner inference
```

Attempt data is forbidden from deciding item validity. An item is not made valid or invalid because a learner succeeded or failed on it.

## Source assertion is not canonical truth

Intake preserves what the source says, including defects. C-B may identify a typo, OCR ambiguity, charge/formula ambiguity, equation/coefficient issue, missing representation, or condition dependency, but it never rewrites provenance.

A learner-use repair requires an explicit `ChemistryQCEvent` when policy requires it:

```text
source_before
learner_use_after
rationale
evidence_locator
scope_changed = false
```

The original source assertion remains auditable.

## Source-integrity states

```text
CLEAN
SOURCE_INTERNAL_TYPO
TYPOGRAPHIC_OR_OCR_AMBIGUITY
FORMULA_OR_CHARGE_AMBIGUITY
EQUATION_OR_COEFFICIENT_ISSUE
TRUNCATED_OR_MISSING_STRUCTURE_OR_FIGURE
REVIEW_REQUIRED
```

`FORMULA_OR_CHARGE_AMBIGUITY`, OCR ambiguity, and missing/truncated representations require rendered-source inspection before confident use. If inspection has not resolved the uncertainty, the item remains excluded from negative inference.

## Item-validity states

```text
VALID
VALID_CONDITION_SENSITIVE
VALID_MULTIPLE_INTERPRETATIONS
UNDERDETERMINED
CHEMICAL_DOMAIN_ISSUE
KEY_ERROR
DATA_ERROR
REVIEW_REQUIRED
```

Source keys are evidence, not canonical Chemistry authority. A mismatch between a source key and a reviewed canonical answer must be represented explicitly as `KEY_ERROR`; the key cannot override Chemistry truth merely because it is printed.

## Diagnostic-use states

```text
FULL
PARTIAL
POSITIVE_EVIDENCE_ONLY
EXCLUDE_FROM_NEGATIVE_INFERENCE
```

These are constrained jointly by source integrity and item validity. Examples:

- `UNDERDETERMINED` cannot create negative learner evidence.
- unresolved formula/charge ambiguity cannot be used as confident evidence.
- a chemical-domain-defective item cannot be rewritten as learner error.
- `REVIEW_REQUIRED` is fail-closed.
- a condition-sensitive item is usable only with the condition preserved.

## Chemistry-specific non-negotiables

1. Formula, subscript, coefficient, ionic charge, state and condition are distinct semantic features.
2. A missing structure, particle view, figure or apparatus dependency is not invented during review.
3. A repair does not silently expand declared/source topic scope.
4. Canonical Chemistry references document the review rationale but do not authorize C-B to broaden C-C scope.
5. Review artifacts contain no learner diagnosis or attempt interpretation.
6. Review records are bound to exact C-A source/question digests.
7. Question and subpart review coverage is complete before downstream use.
8. Technical C-B PASS does not claim human Chemistry-expert approval; `review_provenance` records that authority separately.

## Pilot intent

The mixed synthetic fixture is deliberately cross-topic rather than Redox-only. The C-B review package must be expressive enough for clean items, explicit source typos, unresolved formula/charge OCR ambiguity, condition-sensitive chemistry, underdetermined/domain-defective items, missing representations, and ordinary external-question custody.

## Out of scope

C-B does **not** decide:

```text
external-corpus ELIGIBLE / PARTIAL / OUT_OF_SCOPE
source-obligation extraction
question→concept/capability mapping
problem families / reasoning routes
learner diagnosis or treatment
Core Study Guide / Appendix A/B/C authoring
ExamSIDE Core2 support
rendering / publication
```
