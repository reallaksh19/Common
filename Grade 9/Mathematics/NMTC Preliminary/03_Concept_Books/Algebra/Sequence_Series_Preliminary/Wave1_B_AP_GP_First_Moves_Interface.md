# Issue #49 — Wave 1B Interface: AP / GP First Moves

`STREAM: W1-B`

`STATUS: PASS_INTERNAL`

## 1. CONCEPT_SCOPE

Owns additive-versus-multiplicative classification, normalization before classification, AP/GP first moves, finite-versus-infinite GP conditions, and convergence custody.

## 2. PREREQUISITES

- subtraction and nonzero-term division;
- indexed terms;
- exponent basics;
- finite sums;
- target-object selection from W1-A.

## 3. LIKELY_HALF_KNOWLEDGE

Learner remembers AP/GP formulas but may classify by visual growth, forget why the exponent is `n-1`, and use `a/(1-r)` without checking convergence.

## 4. RECOGNITION_CUES

- repeated additive increment -> inspect first differences;
- repeated multiplicative scaling -> inspect adjacent ratios;
- transformed/normalized list may reveal one of these only after simplification;
- word “infinite” triggers a convergence check before sum formula.

## 5. FIRST_MOVES

- AP candidate: write `a_{n+1}-a_n`;
- GP candidate: write `a_{n+1}/a_n` for valid nonzero terms;
- infinite GP: write `|r|<1` before `S=a/(1-r)`;
- do not write a closed formula before confirming the invariant.

## 6. INVARIANT_OR_STRUCTURE

- AP: constant first difference `d`;
- GP: constant adjacent ratio `r`;
- `n-1` is the number of changes/scalings from term 1 to term n;
- finite GP cancellation is algebraic; infinite GP additionally requires residual-tail decay.

## 7. REPRESENTATION_SWITCHES

- list -> difference table;
- list -> ratio table;
- normalized expression -> AP/GP invariant;
- finite geometric addition -> shifted subtraction;
- infinite sum -> finite partial sum plus limiting condition.

## 8. CONDITION_INDEX_ENDPOINT_CHECKS

- ratio test requires relevant denominator terms nonzero;
- finite GP requires no convergence condition;
- infinite real GP requires `|r|<1`;
- preserve sign when `r<0`;
- nth-term exponent is `n-1` from index distance.

## 9. DECISION_BOUNDARIES

- AP versus GP;
- finite GP versus infinite GP;
- visual “fast growth” versus actual invariant test;
- direct formula use versus normalize/classify first.

## 10. MISCONCEPTION_TRAPS

`AP_GP_SURFACE_CLASSIFICATION`, `INDEX_SHIFT_OFF_BY_ONE`, `INFINITE_GP_CONVERGENCE_OMITTED`, `NEGATIVE_RATIO_SIGN_LOST`, `FORMULA_BEFORE_INVARIANT`.

## 11. CONTRAST_PAIRS

1. `5,9,13,17,...` -> constant difference; `5,10,20,40,...` -> constant ratio.
2. finite `3+6+...+96` can be summed for `r=2`; an infinite GP with `r=2` has no finite geometric sum.
3. `2,-1,1/2,-1/4,...` is a convergent GP despite alternating signs because `|r|=1/2`.

## 12. TRANSFER_MECHANISMS

- normalized fractions/radicals whose invariant is hidden;
- multiplicative geometric scaling in a non-sequence surface;
- finite and infinite versions with identical first terms but different admissibility;
- ask the learner to justify classification without naming a formula.

## 13. SOURCE_CUSTODY

`NMTC-BH-P-2024-Q27` is the clean scored anchor for coupled infinite-GP constraints and convergence. `NMTC-BH-P-2024-Q13` is geometry-primary `BRIDGE_EVIDENCE`: it may support constant-ratio recognition but receives no Sequence recurrence-frequency credit.

## 14. CANDIDATE_MASTERY_ITEMS

1. Classify `7,11,15,19,...`. Expected AP, `d=4`.
2. Classify `3,6,12,24,...`. Expected GP, `r=2`.
3. Infinite GP `2,-1,1/2,-1/4,...`: verify convergence and sum. Expected `r=-1/2`, `S=4/3`.
4. Finite GP with `a=3,r=2,n=6`: find sum. Expected `189`; convergence condition is irrelevant.
5. Classify `2,2sqrt(2),4,4sqrt(2),...`. Expected GP, `r=sqrt(2)`; corresponding infinite sum would diverge because `|r|>1`.

`CANDIDATE_AUDIT: 5/5 independently recomputed — PASS`

## 15. DIAGNOSTIC_TAGS

`AP_GP_SURFACE_CLASSIFICATION`, `DIFFERENCE_RATIO_NOT_TESTED`, `INDEX_SHIFT_OFF_BY_ONE`, `FINITE_INFINITE_CONFUSION`, `CONVERGENCE_OMITTED`, `RATIO_DOMAIN_ERROR`.

## 16. H3_TO_H0_FADE_PLAN

- H3: write a difference/ratio table or the convergence inequality explicitly.
- H2: name only the invariant to test: additive, multiplicative, or tail decay.
- H1: ask “change, ratio, or infinite-condition?”
- H0: unlabelled sequence/sum; learner classifies, states conditions and starts independently.

`W1-B_GATE: PASS`