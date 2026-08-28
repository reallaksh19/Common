# P0 Algebra — Inequalities / Bounds / Equality Mastery Test v1

## Purpose

Unlabelled mixed test. All items are `AUTHOR_CREATED_TRANSFER`, not NMTC PYQs.

Before each solution, write one first-move code:

`BD / AM / CY / CS / ZZ / DR / AV / RI / IC / DB / QC`.

Suggested internal window: 45 minutes. Not an official NMTC timing claim.

---

# Student paper

## Q1
Positive `a,b` satisfy `ab=49`.

Find the minimum of `a+b` and state whether a maximum exists.

## Q2
Positive `a,b` satisfy

`1/a+9/b=1`.

Find the least possible `a+b`.

## Q3
Find the minimum of

`x^2+y^2-4x+8y+25`.

## Q4
Real numbers `p,q` satisfy

`(p-5)^2+(q+2)^2=0`.

Find `p^2+q^2`.

## Q5
For what real `m` does

`x^2+(m-2)x+9=0`

have real roots?

## Q6
Solve

`|x-5|>=3`.

## Q7
Solve

`((x+1)(x-4))/(x-2)>0`.

## Q8
How many integers satisfy

`3/|x-7|>1`?

## Q9
Find the maximum value of

`4+2sin t`.

## Q10
Positive integers `a,b` satisfy `a+b=11`.

Find the maximum of `ab`.

## Q11 — source-integrity check

A printed practice item says:

“Positive `a,b` satisfy `ab=9`. Find the maximum of `a+b`.”

A supplied key says `6`.

What does the printed mathematics say, and what should happen to the key disagreement?

## Q12
A monic quartic has four positive roots. Their product is `81` and their sum is `12`.

Find the sum of the squares of the roots.

---

# Answer / review section

## Q1
**Code:** `BD` + `AM`.

AM-GM:

`a+b>=2sqrt49=14`, equality at `a=b=7`.

For maximum, set `a=t`, `b=49/t`; sum -> infinity.

**Answer:** minimum `14`; no maximum.

**Error tags:** `MIN_REPORTED_AS_MAX`, `BOUNDEDNESS_NOT_TESTED`.

## Q2
**Code:** `CY`.

`1/a+9/b >=(1+3)^2/(a+b)=16/(a+b)`.

Left side is 1, so `a+b>=16`.

Equality is attainable.

**Answer:** `16`.

**Error tags:** `CAUCHY_STRUCTURE_MISSED`, `EQUALITY_CONDITION_OMITTED`.

## Q3
**Code:** `CS`.

`x^2-4x + y^2+8y+25`

`=(x-2)^2-4+(y+4)^2-16+25`

`=(x-2)^2+(y+4)^2+5`.

**Answer:** minimum `5`.

**Error tag:** `COMPLETING_SQUARE_SIGN_ERROR`.

## Q4
**Code:** `ZZ`.

Both squares are non-negative and sum to zero:

`p=5`, `q=-2`.

`p^2+q^2=25+4=29`.

**Answer:** `29`.

**Error tag:** `ZERO_SUM_SQUARE_NOT_COLLAPSED`.

## Q5
**Code:** `DR`.

`D=(m-2)^2-36>=0`.

So:

`|m-2|>=6`.

Hence:

`m<=-4` or `m>=8`.

**Answer:** `(-infinity,-4] union [8,infinity)`.

**Error tag:** `DISCRIMINANT_WRONG_DIRECTION`.

## Q6
**Code:** `AV`.

Distance from 5 is at least 3:

`x<=2` or `x>=8`.

**Answer:** `(-infinity,2] union [8,infinity)`.

**Error tag:** `ABSOLUTE_VALUE_INTERVAL_REVERSED`.

## Q7
**Code:** `RI`.

Critical points:

`-1`, `2` (excluded), `4`.

Sign chart gives positive on:

`(-1,2)` and `(4,infinity)`.

Strict inequality excludes numerator zeros.

**Answer:** `(-1,2) union (4,infinity)`.

**Error tags:** `RATIONAL_SIGN_CHART_ERROR`, `DENOMINATOR_ZERO_INCLUDED`.

## Q8
**Code:** `AV` + `IC`.

Domain `x!=7`.

`3/|x-7|>1` gives:

`|x-7|<3`.

Thus:

`4<x<10`, excluding 7.

Integer solutions:

`5,6,8,9`.

**Answer:** `4`.

**Error tags:** `DENOMINATOR_ZERO_INCLUDED`, `INTEGER_FILTER_APPLIED_TOO_EARLY`.

## Q9
**Code:** `DB`.

`sin t<=1`.

So:

`4+2sin t<=6`.

Equality is attainable.

**Answer:** `6`.

**Error tag:** `DIRECT_BOUND_DIRECTION_WRONG`.

## Q10
**Code:** `AM` + equality-feasibility check.

Over positive reals:

`ab<=121/4=30.25`, equality would require `a=b=5.5`, impossible for integers.

Nearest integer split:

`5,6`, product `30`.

**Answer:** `30`.

**Error tags:** `EQUALITY_CONDITION_INFEASIBLE`, `INTEGER_FILTER_APPLIED_TOO_EARLY`.

## Q11
**Code:** `QC` + `BD`.

For `ab=9`, AM-GM gives minimum `a+b=6` at `a=b=3`.

There is no maximum: take `a=t`, `b=9/t` and let `t->infinity`.

**Answer:** printed problem has no maximum. Key value `6` is the minimum. Record `SOURCE_CONFLICT`; do not silently change “maximum” to “minimum”.

**Error tag:** `SOURCE_CONFLICT_NOT_FLAGGED`.

## Q12
**Code:** `AM`.

For four positive roots:

AM `=12/4=3`.

GM `=81^(1/4)=3`.

AM=GM, so all four roots are 3.

Sum of squares:

`4·9=36`.

**Answer:** `36`.

**Error tags:** `EQUALITY_CONDITION_OMITTED`, `ROOTS_SOLVED_UNNECESSARILY`.

---

# Mastery bands

### `ADOPTED`

- >=10/12 first-move codes correct;
- >=9/12 final answers correct;
- Q1 boundedness, Q8 domain exclusion, Q10 equality feasibility and Q11 source QC all correct.

### `FORMULA_KNOWLEDGE_RECOGNITION_WEAK`

- >=9 final answers but <10 first moves.

Remediation: recognition + first-line labs.

### `BOUND_DIRECTION_GAP`

Miss Q1 or Q11.

Remediation: boundedness-first contrasts.

### `DOMAIN_INTERVAL_GAP`

Miss two among Q5–Q8.

Remediation: discriminant/absolute/rational interval ladder.

### `EQUALITY_GAP`

Miss Q10 or Q12 despite quoting AM-GM.

Remediation: equality feasibility drills.

## Review status

`MATH_REVIEW: PASS_v1`

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`

`FINAL_EDITORIAL_RENDER_QA: NOT_RUN`
