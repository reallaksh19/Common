# Radicals, Exponents & Logarithmic Transformations — Wave 4 Answer & Diagnostic Key v2

`ISSUE_AUTHORITY: #45`

`WAVE: 4 — MIXED_MASTERY_AND_TRANSFER`

`AUDIENCE: TEACHER / SELF-REVIEW AFTER ATTEMPT`

`STATUS: INTERNAL_KEY_SOURCE`

This key corresponds to `Radical_Exponent_Log_Wave4_Mixed_Mastery_Student_v2.md`.

All assessment items are author-created. Historical NMTC IDs are mechanism provenance only and are not being reproduced as question text here.

---

# A. Recognition-only key — 20/20

| Item | Best code | Why |
|---:|---|---|
| 1 | `CB` | all radicals reduce to the same `sqrt(2)` basis |
| 2 | `HS` | structured `A-Bsqrt(d)` is a hidden binomial square |
| 3 | `PR` | principal square root of a square gives an absolute value |
| 4 | `EM` | negative/fractional exponent meaning must be stabilized first |
| 5 | `EN` | 32 and 8 are powers of 2 |
| 6 | `EV` | quadratic in the repeated positive object `2^x` |
| 7 | `ER` | homogeneous two-base powers reduce by a ratio variable |
| 8 | `RQ` + `DR` | radical equation needs sign/domain custody before squaring |
| 9 | `ZR` | immediate division can lose the `x=3` zero case |
| 10 | `RI` | symmetric reciprocal target; recurrence is natural |
| 11 | `LD` | direct log-to-exponent meaning |
| 12 | `LV` | polynomial in `log_3 x` |
| 13 | `LS` | whole repeated object is `sqrt(log_2 x)` |
| 14 | `LA` | related log bases encode a power relation |
| 15 | `LI` | exact exponent/log inverse structure |
| 16 | `DR` | transformed candidates still require admissibility/original checking |
| 17 | `QC` + `DR` | key conflicts with original domain; recompute and preserve disposition |
| 18 | `DR` | cubing over the reals is reversible/injective |
| 19 | `EM` | negative exponent means reciprocal, not negative value |
| 20 | `EV` | `16^x=(4^x)^2`, so the repeated positive object is `4^x` |

`RECOGNITION_KEY: 20/20 internally audited`

---

# B. First-useful-line key — 12/12

A mathematically equivalent first line is acceptable if it preserves the same structure and conditions.

## B1

`sqrt(72)-sqrt(18)+sqrt(8)=6sqrt(2)-3sqrt(2)+2sqrt(2)`.

Diagnostic: `COMMON_BASIS_NOT_FOUND` if terms are attacked independently without normalization.

## B2

Seek a positive difference `sqrt(m)-sqrt(n)` with

`m+n=29`, `mn=180`.

Equivalently, recognize `m=20`, `n=9` only after setting up the reverse-square structure.

Diagnostic: `HIDDEN_POWER_NOT_TESTED`.

## B3

`sqrt((3x-4)^2)=|3x-4|`.

It equals `3x-4` only when `x>=4/3`.

Diagnostic: `PRINCIPAL_ROOT_GAP`.

## B4

`125^(-2/3)=1/(125^(2/3))`.

A next valid rewrite is `1/(cuberoot(125))^2`.

Diagnostic: `EXPONENT_INVERSE_GAP`.

## B5

`2^(6x)=2^(3x+6)`.

Diagnostic: `BASE_NORMALIZATION_GAP`.

## B6

Let `t=3^x>0`; then

`t^2-13t+36=0`.

Diagnostic: `REPEATED_OBJECT_GAP` or `POSITIVE_RANGE_NOT_CARRIED`.

## B7

Divide by `9^x>0`, then let `t=(4/3)^x>0`:

`t^2-10t+9=0`.

Diagnostic: `RATIO_VARIABLE_NOT_SEEN`.

## B8

Because the left side is non-negative, require `x-2>=0`, so `x>=2`; then

`x+6=(x-2)^2`.

Diagnostic: `REVERSIBILITY_GAP` / `DOMAIN_GAP`.

## B9

Use the zero-product cases:

`x-3=0` or `x+5=0`.

Diagnostic: `ZERO_CASE_GAP`.

## B10

Let `S_n=t^n+t^-n`, with `S_0=2`, `S_1=4`; then

`S_2=4S_1-S_0=14`.

Diagnostic: `INVARIANT_GAP` if the learner first solves for `t`.

## B11

Let `t=log_5 x`, with `x>0`; then

`t^2-6t+5=0`.

Diagnostic: `LOG_INVERSE_GAP` / `DOMAIN_GAP`.

## B12

For `x,y>0`,

`log_4 x=(1/2)log_2 x=log_2 y`, hence

`x=y^2`.

Diagnostic: `LOG_TO_ALGEBRA_GAP`.

`FIRST_LINE_KEY: 12/12 internally audited`

---

# C. Mixed solve & transfer key — 18/18

## C1

**First move:** `CB`.

`sqrt(200)=10sqrt(2)`, `sqrt(32)=4sqrt(2)`, `sqrt(8)=2sqrt(2)`.

Therefore

`(10-4+2)sqrt(2)/sqrt(2)=8`.

**Answer:** `8`.

## C2

**First move:** `HS`.

`29-12sqrt(5)=(sqrt(20)-3)^2=(2sqrt(5)-3)^2`.

Since `2sqrt(5)-3>0`, the principal root is

**Answer:** `2sqrt(5)-3`.

## C3

**First move:** `HS`.

`11+6sqrt(2)=(3+sqrt(2))^2`,

`11-6sqrt(2)=(3-sqrt(2))^2`,

and both `3±sqrt(2)` are positive.

Thus the expression is

`(3+sqrt(2))^3-(3-sqrt(2))^3`.

Using `(a+b)^3-(a-b)^3=6a^2b+2b^3` with `a=3`, `b=sqrt(2)` gives

`54sqrt(2)+4sqrt(2)=58sqrt(2)`.

**Answer:** `58sqrt(2)`.

## C4

**First move:** `EM`.

`125^(-2/3)=1/(125^(2/3))=1/5^2`.

**Answer:** `1/25`.

## C5

**First move:** `EN`.

`32^x=8^(x+2)`

`2^(5x)=2^(3x+6)`.

Hence `5x=3x+6`.

**Answer:** `x=3`.

## C6

**First move:** `EV`.

Let `t=3^x>0`.

`t^2-13t+36=0=(t-4)(t-9)`.

So `t=4` or `9`.

**Answer:** `x=log_3 4` or `x=2`.

Both transformed roots are positive and therefore admissible exponential values.

## C7

**First move:** `ER`.

Divide by `9^x>0` and set `t=(4/3)^x>0`:

`t^2-10t+9=0=(t-1)(t-9)`.

Thus `t=1` or `9`.

**Answer:** `x=0` or `x=log_(4/3) 9`.

## C8

**First move:** `RQ + DR`.

Original equation:

`sqrt(x+6)=x-2`.

The right side must be non-negative, so `x>=2`. On that domain both sides are non-negative, and squaring is reversible:

`x+6=(x-2)^2`

`x^2-5x-2=0`.

Algebraic roots:

`x=(5±sqrt(33))/2`.

Only `(5+sqrt(33))/2` is at least 2.

**Answer:** `x=(5+sqrt(33))/2`.

`DOMAIN/EXTRANEOUS_CHECK: PASS`.

## C9

**First move:** `RQ + DR`.

Original domain requires `x>=5`.

Square:

`x+4=4(x-5)`

so `3x=24` and `x=8`.

It lies in the original domain and satisfies the original equation.

**Answer:** `x=8`.

`DOMAIN_CHECK: PASS`.

## C10

**First move:** `ZR`.

Zero-product cases give

`x-2=0` or `x+5=0`.

**Answer:** `x=2,-5`.

Dividing by `x-2` first is unsafe because it assumes `x-2!=0` and would lose the valid solution `x=2`.

`ZERO_CASE_CHECK: PASS`.

## C11

**First move:** `RI`.

Let `S_n=x^n+x^-n`, with `S_0=2`, `S_1=4`.

`S_2=4*4-2=14`.

`S_3=4*14-4=52`.

`S_4=4*52-14=194`.

`S_5=4*194-52=724`.

**Answer:** `724`.

No explicit solution for `x` is required.

## C12

**First move:** `RI` plus the symmetric/asymmetric boundary.

From `x+1/x=4`,

`(x-1/x)^2=(x+1/x)^2-4=12`.

Thus

`x-1/x=±2sqrt(3)`.

Then

`x^2-1/x^2=(x+1/x)(x-1/x)=±8sqrt(3)`.

**Conclusion:** the value is **not uniquely determined**; the two possible values are `±8sqrt(3)`.

Diagnostic: `INVARIANT_OVERGENERALIZED` if the learner assumes every expression is determined by the symmetric invariant.

## C13

**First move:** `LV`.

Let `t=log_2 x`, with `x>0`.

`t^2-5t+4=0=(t-1)(t-4)`.

So `t=1,4`.

**Answer:** `x=2,16`.

Both are in the original log domain.

## C14

**First move:** `LS`.

Let

`u=sqrt(log_3 x)>=0`.

Then

`u^2-4u+3=0=(u-1)(u-3)`.

Both roots are non-negative: `u=1,3`.

Therefore `log_3 x=1,9`.

**Answer:** `x=3,19683`.

`SUBSTITUTION_RANGE_CHECK: PASS`.

## C15

**First move:** `LA`.

Because `x,y>0`,

`log_9 x=log_3 y`

becomes

`(1/2)log_3 x=log_3 y`, hence `x=y^2`.

With `x-y=20`:

`y^2-y-20=0=(y-5)(y+4)`.

Positivity gives `y=5`, so `x=25`.

**Answer:** `x+y=30`.

`DOMAIN_FILTER: PASS`.

## C16

**First move:** `LI`.

`27^(log_3 5)=(3^3)^(log_3 5)=3^(3log_3 5)`

`=(3^(log_3 5))^3=5^3`.

**Answer:** `125`.

## C17

**First move:** `LA + DR`.

Original log arguments require

`x-1>0` and `7-x>0`, so

`1<x<7`.

On this domain, same-base log injectivity gives

`x-1=7-x`.

Thus `2x=8` and `x=4`, which lies in the original domain.

**Answer:** `x=4`.

`DOMAIN_CHECK: PASS`.

## C18

**First move:** `PR`.

`sqrt((x-1)^2)=|x-1|`.

So

`|x-1|=3`, giving

`x-1=3` or `x-1=-3`.

**Answer:** `x=4,-2`.

The `±` comes from solving the absolute-value equation, not from the radical symbol itself.

`PRINCIPAL_ROOT_CHECK: PASS`.

`SOLVE_TRANSFER_KEY: 18/18 internally audited`

---

# D. WHY-NOT key — 6/6

## D1 — `sqrt(a+b)` splitting

**Classification:** generally **invalid**.

The radical product property does not distribute over addition. For example, `sqrt(9+16)=5` while `sqrt(9)+sqrt(16)=7`.

Diagnostic: `FALSE_RADICAL_DISTRIBUTION`.

## D2 — negative exponent as negative value

**Classification:** **invalid**.

For non-zero `a`, `a^-2=1/a^2`. The minus sign belongs to the exponent and encodes multiplicative inverse; it is not a sign attached to the value.

Diagnostic: `EXPONENT_INVERSE_GAP`.

## D3 — take logs first in `8^x=4^(x+1)`

**Classification:** mathematically valid but **inferior**.

Both bases are powers of 2, so normalization immediately gives a linear exponent equation and preserves exact structure without introducing logarithms.

Diagnostic: `METHOD_CHOICE_GAP`.

## D4 — square before restrictions

**Classification:** the forward squaring step is legal as an implication, but treating it as automatic equivalence is **unsafe/inferior**.

The principal radical is non-negative, so the right side must satisfy `x-2>=0`. Writing that restriction first makes the logic and later filtering explicit.

Diagnostic: `REVERSIBILITY_GAP`.

## D5 — divide by `x-2`

**Classification:** **invalid as an equivalent step** unless the zero case is separately preserved.

The factor may be zero. Dividing by it would discard the valid solution `x=2`.

Diagnostic: `ZERO_CASE_GAP`.

## D6 — choose `t=log_2 x`

**Classification:** valid but **inferior**.

It leaves a `sqrt(t)` term. Choosing `u=sqrt(log_2 x)>=0` turns both the log and square-root-log terms into a quadratic polynomial in one variable and carries the natural range explicitly.

Diagnostic: `REPEATED_OBJECT_GAP`.

`WHY_NOT_KEY: 6/6 internally audited`

---

# E. Diagnostic synthesis

Use errors by mechanism rather than raw score alone.

| Diagnostic tag | Evidence pattern | Repair destination |
|---|---|---|
| `REPRESENTATION_GAP` | misses CB/HS/EN/ER/LA/LI recognition | Wave-2 representation sections, then Wave-3 decision tree |
| `PRINCIPAL_ROOT_GAP` | B3/C18/D4-type sign confusion | principal-root contrast + radical equation checkpoint |
| `EXPONENT_INVERSE_GAP` | A4/A19/B4/D2 misses | exponent meaning `EM`, not extra base-normalization drills |
| `REPEATED_OBJECT_GAP` | EV/LV/LS substitution choice unstable | repeated-object contrasts and first-line practice |
| `REVERSIBILITY_GAP` | C8/C17/D4 or transformed-root acceptance errors | `<=>` versus `=>` checkpoint |
| `ZERO_CASE_GAP` | A9/B9/C10/D5 | zero-factor protection before division |
| `INVARIANT_GAP` | explicit solving used for C11 | reciprocal invariant recurrence |
| `INVARIANT_OVERGENERALIZED` | C12 treated as unique | symmetric-vs-asymmetric target boundary |
| `DOMAIN_GAP` | log/radical restrictions omitted | domain ledger + original check |
| `METHOD_CHOICE_GAP` | valid but expensive method selected despite obvious structure | WHY-NOT contrasts / decision tree |
| `SOURCE_INTEGRITY_GAP` | A17 key is forced despite invalid domain | recompute -> classify source disposition |
| `EXECUTION_ERROR` | correct first move/conditions but arithmetic fails | targeted calculation repair only |

## Suggested internal mastery interpretation

`ADOPTED` requires all of the following:

- recognition: at least 17/20;
- first useful line: at least 10/12;
- solve/transfer: at least 15/18 correct conclusions;
- WHY-NOT: at least 5/6 with valid reason;
- no more than one failure among the explicit domain/reversibility/zero-case checks.

`MECHANICS_OK_METHOD_CHOICE_WEAK`: solve score is strong but recognition/WHY-NOT is below threshold.

`DOMAIN_REVERSIBILITY_GAP`: two or more failures on C8, C9, C10, C14, C15, C17, C18 or corresponding first-line/WHY-NOT items.

`REPRESENTATION_UNSTABLE`: recognition below 14/20 even if routine calculations are acceptable.

These are internal teaching diagnostics, not an official NMTC marking scheme.

---

# F. Provenance custody

Mechanism grounding remains unchanged from Waves 0–3:

- 16 `CLEAN_SCORED_ANCHOR` IDs;
- `NMTC-BH-P-2023-Q04` and `NMTC-BH-P-2023-Q20` remain `SOURCE_SENSITIVE_EVIDENCE` only;
- `NMTC-BH-P-2025-Q18` remains `SOURCE_CONFLICT_EVIDENCE` / QC only;
- no topic-specific `BONUS_EVIDENCE` is inferred;
- all Wave-4 question text is author-created and has no fake NMTC year/question attribution.

`FINAL_INDEPENDENT_QA: separate Wave-4 QA file`

`PDF_RENDER_QA: NOT_RUN — Wave 5`
