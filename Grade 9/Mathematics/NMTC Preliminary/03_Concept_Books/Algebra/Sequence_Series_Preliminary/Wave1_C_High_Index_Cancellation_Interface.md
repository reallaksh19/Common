# Issue #49 — Wave 1C Interface: High-Index Cancellation

`STREAM: W1-C`

`STATUS: PASS_INTERNAL`

## 1. CONCEPT_SCOPE

Owns selected-term GP comparison, index-gap compression, ratio cancellation, and the decision to avoid constructing huge powers when only a relative term relation is needed.

## 2. PREREQUISITES

- GP nth-term representation;
- exponent laws;
- adjacent/selected term ratios;
- nonzero denominator conditions.

## 3. LIKELY_HALF_KNOWLEDGE

Learner can write `a_n=ar^(n-1)` but substitutes large indices separately, solves for `a` and `r` unnecessarily, or loses the exponent gap when dividing two selected terms.

## 4. RECOGNITION_CUES

- two or more GP terms at widely separated indices;
- target is a ratio of selected terms;
- equations share the same first term and large common powers;
- “high index” is visible but exact term values are not intrinsically required.

## 5. FIRST_MOVES

- write comparable selected-term relations;
- divide before expanding;
- use `a_p/a_q=r^(p-q)`;
- solve only for the power of `r` actually required by the target.

## 6. INVARIANT_OR_STRUCTURE

The first term and common exponent offset cancel in ratios of terms from the same GP. The target sees only index distance.

## 7. REPRESENTATION_SWITCHES

- two huge term formulas -> one small exponent-gap equation;
- exact selected terms -> ratio relation;
- target term ratio -> power of `r` without reconstructing `a`.

## 8. CONDITION_INDEX_ENDPOINT_CHECKS

- denominator selected term must be nonzero;
- exponent is `(p-1)-(q-1)=p-q`;
- preserve sign for negative `r` and parity of exponent gap;
- do not infer a unique real `r` from an even-power relation unless needed and justified.

## 9. DECISION_BOUNDARIES

- relative target versus absolute target;
- divide comparable relations versus solve the entire GP;
- odd exponent gap may determine sign; even exponent gap may not;
- cancellation is useful only when terms belong to the same GP under the same parameters.

## 10. MISCONCEPTION_TRAPS

`GP_HIGH_POWER_EXPANDED`, `INDEX_GAP_ERROR`, `FIRST_TERM_NOT_CANCELLED`, `UNNECESSARY_PARAMETER_SOLVE`, `NEGATIVE_RATIO_PARITY_ERROR`.

## 11. CONTRAST_PAIRS

1. Find `a_40/a_35` -> directly `r^5`; find `a_40` -> may require `a` as well.
2. `a_100/a_97=-8` gives `r^3=-8`; an even-gap ratio such as `r^2=4` alone does not distinguish `r=2` from `r=-2`.
3. Comparing terms from one GP permits cancellation; comparing unrelated sequences does not.

## 12. TRANSFER_MECHANISMS

- population/scaling states indexed by time where only relative growth is asked;
- geometrically scaled lengths with far-separated stages;
- selected-term equations disguised as products or ratios;
- targets that require only another index gap, not `a` or a huge term.

## 13. SOURCE_CUSTODY

`NMTC-BH-P-2023-Q29` is the clean scored anchor: the qualified mechanism is to divide GP relations/cancel common powers before solving unnecessary high-index quantities. Historical wording is not reproduced here.

## 14. CANDIDATE_MASTERY_ITEMS

1. GP with `a_3=12,a_6=96`. Find `a_20/a_17`. From `r^3=8`, expected `8`.
2. GP with `a_5=48,a_8=384`. Find `a_30/a_26`. `r^3=8`, so `r=2`; expected `16`.
3. GP with `a_25/a_22=27`. Find `a_40/a_38`. `r^3=27`, expected `r^2=9`.
4. GP with `a_100/a_97=-8`. Find `a_60/a_58`. `r=-2`; expected `4`.
5. GP with `a_4=54,a_7=1458`. Find `a_50/a_47`. `r^3=27`; expected `27`, with no need to compute `a_50`.

`CANDIDATE_AUDIT: 5/5 independently recomputed — PASS`

## 15. DIAGNOSTIC_TAGS

`GP_HIGH_POWER_EXPANDED`, `INDEX_GAP_ERROR`, `RATIO_SIGN_ERROR`, `UNNECESSARY_A_SOLVE`, `UNNECESSARY_HUGE_TERM`, `SELECTED_TERM_RATIO_MISSED`.

## 16. H3_TO_H0_FADE_PLAN

- H3: write both selected terms and divide them explicitly.
- H2: cue “compare the terms before solving parameters.”
- H1: point only to the large common index structure.
- H0: far-index GP problem with no method label; learner must choose cancellation independently.

`W1-C_GATE: PASS`