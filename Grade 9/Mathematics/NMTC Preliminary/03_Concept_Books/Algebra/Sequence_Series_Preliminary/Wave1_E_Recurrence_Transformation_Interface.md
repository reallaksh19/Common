# Issue #49 — Wave 1E Interface: Recurrence Transformation

`STREAM: W1-E`

`STATUS: PASS_INTERNAL`

## 1. CONCEPT_SCOPE

Owns transformation choice for recurrences: reciprocal, fixed-point shift, first-difference/ratio when natural, strategic indices for functional recurrences, and the distinction between discovering a closed form and verifying one.

## 2. PREREQUISITES

- recurrence iteration;
- algebraic substitution;
- AP/GP invariants;
- reciprocal manipulation;
- initial-condition use.

## 3. LIKELY_HALF_KNOWLEDGE

Learner can generate terms but often iterates to large n, treats reciprocal/shift as isolated tricks, or attempts a universal formula when one strategic index path would answer the question.

## 4. RECOGNITION_CUES

- fractional recurrence with `a_n` in denominator-like structure -> test reciprocal;
- affine `a_{n+1}=pa_n+q` -> test fixed-point shift;
- recurrence already written as a difference/ratio -> expose that invariant;
- `a_{m+n}` functional rule -> choose index pairs that reach the target efficiently.

## 5. FIRST_MOVES

- ask which variable makes the update simpler;
- reciprocal candidate: `b_n=1/a_n`;
- affine candidate: solve `c=pc+q`, then set `b_n=a_n-c`;
- functional recurrence: choose target-building pairs before seeking closed form;
- verification task: substitute proposed form into recurrence and initial condition.

## 6. INVARIANT_OR_STRUCTURE

A recurrence can be complicated in one coordinate and simple in another. The best transform converts the update to constant difference, constant ratio, or an efficiently navigable index relation.

## 7. REPRESENTATION_SWITCHES

- nonlinear fraction -> reciprocal variable;
- affine recurrence -> deviation from fixed point;
- functional relation -> index graph/doubling path;
- guessed formula -> substitution check;
- term iteration -> transformed AP/GP.

## 8. CONDITION_INDEX_ENDPOINT_CHECKS

- transformed variable must be defined (`a_n≠0` before reciprocal);
- carry the initial condition into the transformed sequence;
- after solving transformed recurrence, map back to `a_n`;
- a verification must check both recurrence and base/initial condition;
- strategic indices must remain within the recurrence domain.

## 9. DECISION_BOUNDARIES

- reciprocal versus fixed-point shift;
- brute iteration versus transform;
- strategic index route versus global closed form;
- closed-form discovery versus verification;
- transform that simplifies structure versus transform that merely changes notation.

## 10. MISCONCEPTION_TRAPS

`RECURRENCE_BRUTE_ITERATION`, `WRONG_TRANSFORM_CHOICE`, `INITIAL_CONDITION_DROPPED`, `MAP_BACK_OMITTED`, `DISCOVERY_VERIFICATION_CONFUSION`, `FUNCTIONAL_RECURRENCE_OVERGENERALIZED`.

## 11. CONTRAST_PAIRS

1. `a_{n+1}=a_n/(1+a_n)` -> reciprocal is natural; `a_{n+1}=2a_n+3` -> fixed-point shift is natural.
2. For one requested `a_8` under an `a_{m+n}` rule, strategic doubling may be shorter than deriving all `a_n`.
3. Substituting `a_n=2^n-1` into a recurrence verifies it; it does not reveal how one originally discovered it.

## 12. TRANSFER_MECHANISMS

- population/score recurrences transformed around equilibrium;
- resistor/rate-style reciprocal updates;
- functional recurrences with target indices reachable by doubling/decomposition;
- present a closed form and ask whether the work shown is discovery or proof.

## 13. SOURCE_CUSTODY

Clean scored anchors:
- `NMTC-BH-P-2019-Q29` — functional recurrence / strategic equal-index substitutions;
- `NMTC-BH-P-2024-Q11` — reciprocal transform exposing an additive/telescoping recurrence.

The same 2024 Q11 may bridge W1-F for telescoping behavior but receives only one historical frequency credit.

## 14. CANDIDATE_MASTERY_ITEMS

1. `a_1=1`, `a_{n+1}=a_n/(1+a_n)`. Find `a_20`. Reciprocal gives `1/a_n=n`; expected `1/20`.
2. `a_1=1`, `a_{n+1}=2a_n+3`. Shift by fixed point `-3`; expected `a_10=2045`.
3. `a_{m+n}=a_m+a_n+2mn`, `a_1=1`. Find `a_8` using strategic doubling. Expected `64`.
4. `a_1=5`, `a_{n+1}=3a_n-4`. Shift by fixed point 2; expected `a_6=731`.
5. Recurrence `a_1=1`, `a_{n+1}=2a_n+1`. A proposed form is `a_n=2^n-1`. Task: classify substitution into recurrence + base case. Expected: valid verification, not a discovery method.

`CANDIDATE_AUDIT: 5/5 independently recomputed — PASS`

## 15. DIAGNOSTIC_TAGS

`RECURRENCE_BRUTE_ITERATION`, `RECIPROCAL_CUE_MISSED`, `FIXED_POINT_SHIFT_MISSED`, `INITIAL_CONDITION_ERROR`, `STRATEGIC_INDEX_MISSED`, `DISCOVERY_VERIFICATION_CONFUSION`.

## 16. H3_TO_H0_FADE_PLAN

- H3: provide the transformed variable or strategic index pair.
- H2: state only the transform family: reciprocal, shift, difference/ratio, strategic index.
- H1: point to the algebraic shape that should trigger a transform.
- H0: mixed recurrence; learner must choose, justify and execute the transform independently.

`W1-E_GATE: PASS`