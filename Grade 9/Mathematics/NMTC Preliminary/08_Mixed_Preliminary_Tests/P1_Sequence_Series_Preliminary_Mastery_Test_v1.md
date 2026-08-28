# P1 Sequence & Series — Preliminary Mastery Test v1

All items are unlabelled and author-created. Suggested internal window: 45 minutes; this is not an official NMTC timing claim.

## Student paper

1. An AP satisfies `a_5=18`, `a_17=54`. Find `S_20`.
2. A GP satisfies `a_3=20`, `a_6=160`. Find `a_15/a_11`.
3. Evaluate `Σ_{n=1}^{15} n(3n-1)`.
4. `a_1=1/2`, `a_{n+1}=a_n/(1+a_n)`. Find `a_25`.
5. `a_1=0`, `a_{n+1}=3a_n+4`. Find `a_6`.
6. `a_{m+n}=a_m+a_n+mn` and `a_1=1`. Find `a_8`.
7. An infinite GP has sum 10 and sum of squares 20. Find `a,r`.
8. `S_n=n²+4n`. Find `a_n`.
9. Evaluate `Σ_{k=1}^{10} 1/[k(k+1)]`.
10. Evaluate `Σ_{k=1}^{15} 1/(sqrt(k)+sqrt(k+1))`.
11. Find the 20th term of `3,8,15,24,35,...`.
12. A reproduced historical GP problem gives a printed relation that leads to value `X`, while the supplied provisional key corresponds to a different term relation and gives `Y`. What is the correct source-handling action?

---

# Answer / review section

## Q1
`54-18=12d`, so `d=3`; `a=6`; `a_20=63`; `S_20=10(6+63)=690`.

**Answer:** `690`.
**Tags:** `TERM_SUM_CONFUSION`, `AP_INDEX_GAP_ERROR`.

## Q2
`r³=160/20=8`, so `r=2`; `a_15/a_11=r^4=16`.

**Answer:** `16`.
**Tag:** `GP_HIGH_POWER_EXPANDED`.

## Q3
`3Σn²-Σn=3·1240-120=3600`.

**Answer:** `3600`.
**Tag:** `WEIGHTED_SUM_NOT_SPLIT`.

## Q4
Let `b_n=1/a_n`. Then `b_{n+1}=b_n+1`, `b_1=2`; hence `b_n=n+1`.

**Answer:** `a_25=1/26`.
**Tag:** `RECURRENCE_TRANSFORM_MISSED`.

## Q5
Fixed point is `-2`; let `b_n=a_n+2`. Then `b_{n+1}=3b_n`, `b_1=2`.

`b_6=2·3^5=486`, so `a_6=484`.

**Answer:** `484`.
**Tag:** `SHIFT_SIGN_ERROR`.

## Q6
Use strategic doubling or recognize `a_n=n(n+1)/2`.

`a_2=3`, `a_4=10`, `a_8=36`.

**Answer:** `36`.
**Tag:** `FUNCTIONAL_RECURRENCE_OVERDERIVED`.

## Q7
`|r|<1`.

`a/(1-r)=10`, `a²/(1-r²)=20`.

Substitute `a=10(1-r)`:

`5(1-r)/(1+r)=1`, so `r=2/3`, `a=10/3`.

**Answer:** `(a,r)=(10/3,2/3)`.
**Tag:** `INFINITE_GP_CONVERGENCE_OMITTED`.

## Q8
`a_n=S_n-S_{n-1}`.

`=n²+4n-[n²+2n-3]=2n+3`.

**Answer:** `2n+3`.
**Tag:** `REVERSE_FROM_SUM_MISSED`.

## Q9
`1/[k(k+1)]=1/k-1/(k+1)`.

**Answer:** `10/11`.
**Tag:** `TELESCOPING_ENDPOINT_ERROR`.

## Q10
Rationalize to `sqrt(k+1)-sqrt(k)`.

**Answer:** `sqrt16-sqrt1=3`.
**Tag:** `RADICAL_TELESCOPE_MISSED`.

## Q11
Differences are `5,7,9,11,...`; constant second difference 2. Pattern `a_n=n²+2n`.

**Answer:** `440`.
**Tag:** `FINITE_DIFFERENCE_CLASSIFICATION_ERROR`.

## Q12
Do not alter the stem. Preserve the printed result and key evidence separately; classify the item `SOURCE_KEY_CONFLICT_NOT_CANONICAL` until original-source resolution.

**Answer:** flag/preserve/block canonical use.
**Tag:** `SOURCE_CONFLICT_SILENTLY_REPAIRED`.

---

# Mastery bands

### ADOPTED
- at least 10/12 correct first moves;
- at least 9/12 final outcomes correct;
- Q4 recurrence transform, Q7 convergence, Q8 reverse-from-sum and Q12 source QC all correct.

### FORMULA_KNOWLEDGE_RECOGNITION_WEAK
Good arithmetic but fewer than 10 correct first moves. Return to recognition/first-line labs.

### RECURRENCE_TRANSFORM_GAP
Miss Q4 and/or Q5. Return to reciprocal/shift cards.

### ACCUMULATION_GAP
Miss Q3, Q8 or telescoping pair Q9/Q10. Return to ACCUMULATION/REVERSE upstream concepts.

### SOURCE_QC_GAP
Miss Q12. Do not promote historical content until source-custody behavior is repaired.

## Review state

`MATH_REVIEW: PASS_v1`

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`

`FINAL_EDITORIAL_RENDER_QA: NOT_RUN`