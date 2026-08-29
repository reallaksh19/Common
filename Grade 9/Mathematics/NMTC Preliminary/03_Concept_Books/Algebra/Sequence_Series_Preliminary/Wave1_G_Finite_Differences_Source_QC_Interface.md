# Issue #49 — Wave 1G Interface: Finite Differences & Source QC

`STREAM: W1-G`

`STATUS: PASS_INTERNAL`

## 1. CONCEPT_SCOPE

Owns first/second/higher finite-difference recognition, low-degree polynomial hypotheses and verification, primary-mechanism versus incidental-sequence classification, and source-conflict custody including 2025 Q30.

## 2. PREREQUISITES

- subtraction across successive terms;
- indexed values at equally spaced integer indices;
- basic polynomial substitution;
- independent checking of a printed mathematical statement.

## 3. LIKELY_HALF_KNOWLEDGE

Learner may know that constant second differences “mean quadratic” but may accept a guessed rule without verification. A familiar AP/GP surface can also cause the learner to overlook source contradictions or misclassify a cross-domain problem as sequence-primary.

## 4. RECOGNITION_CUES

- neither first difference nor adjacent ratio is constant;
- first differences themselves form a simple progression;
- repeated differences become constant;
- historical wording and supplied key do not produce the same mathematics;
- sequence/ratio structure appears inside another primary domain such as geometry.

## 5. FIRST_MOVES

- build first differences, then second/higher differences only as needed;
- use constant dth difference as a degree-d hypothesis signal;
- derive or fit a candidate low-degree rule and verify against all available terms/conditions;
- for source conflict: solve the printed mathematics independently before considering the key;
- classify primary mechanism before assigning source-frequency credit.

## 6. INVARIANT_OR_STRUCTURE

- polynomial sequences at equally spaced integer indices have eventually constant finite differences at degree order;
- a difference table is evidence for a structural hypothesis, not a proof by itself outside the observed data;
- provenance/domain classification is part of mathematical custody: mechanism appearance and primary-domain evidence are not identical.

## 7. REPRESENTATION_SWITCHES

- visible list -> finite-difference table;
- constant differences -> polynomial-degree hypothesis;
- hypothesized formula -> substitution verification;
- historical stem/key pair -> two independently evaluated mathematical claims;
- cross-domain item -> primary mechanism + bridge mechanism labels.

## 8. CONDITION_INDEX_ENDPOINT_CHECKS

- indices must be equally spaced for the standard finite-difference degree signal;
- verify the proposed formula at all supplied indices and any additional stated condition;
- do not extrapolate recurrence/frequency from a source-conflicted item;
- do not count bridge evidence as primary Sequence recurrence evidence;
- preserve exact conflict wording/disposition.

## 9. DECISION_BOUNDARIES

- constant first difference -> AP; constant second difference -> quadratic-type, not AP;
- finite-difference hypothesis versus verified nth-term rule;
- sequence-primary item versus incidental geometric scaling;
- source conflict versus “obvious correction”.

## 10. MISCONCEPTION_TRAPS

`FINITE_DIFFERENCE_CLASSIFICATION_ERROR`, `DEGREE_HYPOTHESIS_UNVERIFIED`, `AP_FORCED_ON_SECOND_DIFFERENCE`, `SOURCE_KEY_TRUSTED_OVER_MATH`, `SOURCE_SILENT_REPAIR`, `PRIMARY_DOMAIN_INFLATION`.

## 11. CONTRAST_PAIRS

1. `2,6,12,20,30,...` has nonconstant first differences but constant second differences; it is not an AP.
2. A fitted quadratic matching a few terms is a hypothesis until checked against the given structure/terms.
3. `NMTC-BH-P-2024-Q13` contains geometric scaling but is geometry-primary; `NMTC-BH-P-2023-Q29` is a clean Sequence/GP anchor.
4. `NMTC-BH-P-2025-Q30`: printed third/fourth-term relation and provisional keyed 31 cannot both be canonical; do not edit the stem.

## 12. TRANSFER_MECHANISMS

- table of counts/areas whose second differences are constant;
- polynomial growth disguised as a figurate-number pattern;
- ask learner to distinguish discovery signal from proof;
- source-QC case where one-word term-position change would make a key work;
- cross-domain constant-ratio pattern requiring bridge-only classification.

## 13. SOURCE_CUSTODY

- `NMTC-BH-P-2025-Q30 = SOURCE_CONFLICT_EVIDENCE / SOURCE_KEY_CONFLICT_NOT_CANONICAL`; permitted for source-QC only, blocked exact anchor and no clean frequency credit.
- `NMTC-BH-P-2024-Q13 = BRIDGE_EVIDENCE`, geometry-primary; constant-ratio recognition only, no Sequence recurrence-frequency credit.
- finite-difference foundation is supplied by deep Sequence & Series authority and author-created foundation items, not by inventing a clean NMTC anchor.

## 14. CANDIDATE_MASTERY_ITEMS

1. `2,6,12,20,30,...`: second differences are constant 2; infer/verify `a_n=n(n+1)`; expected `a_15=240`.
2. `1,8,27,64,...`: cubic hypothesis `a_n=n^3`; expected `a_8=512`; verify rather than accept from appearance alone.
3. `3,8,15,24,35,...`: constant second difference 2; infer/verify `a_n=n^2+2n`; expected `a_10=120`.
4. A historical GP-looking item’s printed term comparison and key imply different results. Expected first action: independently solve printed mathematics, record `SOURCE_CONFLICT`, block canonical use; do not repair wording.
5. Circle radii form a GP because of homothety, but the question’s primary mechanism is geometry. Expected classification: `BRIDGE_EVIDENCE`, no Sequence-frequency credit.

`CANDIDATE_AUDIT: 5/5 independently checked — PASS`

## 15. DIAGNOSTIC_TAGS

`FINITE_DIFFERENCE_CLASSIFICATION_ERROR`, `DEGREE_HYPOTHESIS_UNVERIFIED`, `AP_GP_REFLEX`, `SOURCE_CONFLICT_MISSED`, `SOURCE_SILENT_REPAIR`, `PRIMARY_DOMAIN_INFLATION`.

## 16. H3_TO_H0_FADE_PLAN

- H3: supply the first difference row or explicit source-conflict comparison.
- H2: cue finite-difference degree signal or provenance/domain check.
- H1: point only to “not AP/GP yet” or “stem/key disagree”.
- H0: unlabelled pattern/source case; learner must choose finite differences or source-QC independently and justify the classification.

`W1-G_GATE: PASS`