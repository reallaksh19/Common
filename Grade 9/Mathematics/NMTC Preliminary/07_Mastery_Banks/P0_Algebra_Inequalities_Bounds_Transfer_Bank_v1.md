# P0 Algebra — Inequalities / Bounds / Equality Transfer Bank v1

## Purpose

18 original non-identical transfer items grounded in qualified Bhaskara Preliminary mechanisms.

Every item is `AUTHOR_CREATED_TRANSFER`, not a previous-year question.

Profile order:

`C/R/F/S/A/H/K/B/T/P`

= conceptual / recognition / first move / reasoning / algebra / hidden structure / cases / calculation burden / trap density / time pressure.

---

# Family A — Boundedness + AM-GM direction

## A1
Positive `a,b` satisfy `ab=36`.

Find the minimum of `a+b`. Does a maximum exist?

**Answer:** minimum `12` at `a=b=6`; no maximum.

**Solution:** AM-GM gives `a+b>=12`. For maximum, set `a=t`, `b=36/t`; target -> infinity as `t->infinity`.

**Profile:** `4/5/5/4/3/6/3/2/7/5`; FAST_IF_RECOGNIZED.

## A2
Positive `x,y` satisfy `x+y=16`.

Find the maximum of `xy`.

**Answer:** `64` at `x=y=8`.

**Solution:** `xy <= ((x+y)/2)^2=64`.

**Profile:** `3/4/3/2/2/4/2/1/3/3`; DIRECT.

## A3
Positive `x,y,z` satisfy `xyz=8`.

Find the minimum of `x+y+z`. Does a maximum exist?

**Answer:** minimum `6` at `x=y=z=2`; no maximum.

**Solution:** AM-GM gives sum >=6. For unboundedness take `x=t`, `y=1`, `z=8/t`; sum -> infinity.

**Profile:** `5/6/6/4/3/7/4/2/7/6`; FAST_IF_RECOGNIZED.

---

# Family B — Reciprocal / Cauchy-Engel

## B1
Positive `a,b` satisfy

`1/a+4/b=1`.

Find the least possible `a+b`.

**Answer:** `9`.

**Solution:**

`1/a+4/b >= (1+2)^2/(a+b)=9/(a+b)`.

Since left side is 1, `a+b>=9`. Equality occurs at `a=3,b=6`.

**Profile:** `5/6/5/4/4/6/3/3/5/5`; FAST_IF_RECOGNIZED.

## B2
Positive `x,y` satisfy

`4/x+9/y=1`.

Find the least possible `x+y`.

**Answer:** `25`.

**Solution:**

`4/x+9/y >= (2+3)^2/(x+y)=25/(x+y)`.

Equality is attained at `x=10,y=15`.

**Profile:** `5/6/5/4/4/6/3/3/5/5`; FAST_IF_RECOGNIZED.

## B3
Positive `p,q` satisfy

`1/p+16/q=2`.

Find the least possible `p+q`.

**Answer:** `25/2`.

**Solution:**

`1/p+16/q >=25/(p+q)`.

Thus `2>=25/(p+q)`, so `p+q>=25/2`. Equality at `p=5/2,q=10`.

**Profile:** `6/6/6/5/5/6/4/3/5/5`; MULTISTEP.

---

# Family C — Completing squares / zero collapse

## C1
Find the minimum of

`x^2-8x+21`.

**Answer:** `5` at `x=4`.

**Solution:** `(x-4)^2+5`.

**Profile:** `2/3/2/2/3/3/1/2/2/2`; DIRECT.

## C2
Find the minimum of

`x^2+y^2-6x+4y+20`.

**Answer:** `7` at `(3,-2)`.

**Solution:** `(x-3)^2+(y+2)^2+7`.

**Profile:** `4/4/4/3/4/4/2/3/3/3`; DIRECT.

## C3
Real `x,y` satisfy

`(x-2)^2+(y+1)^2=0`.

Find `2x-3y`.

**Answer:** `7`.

**Solution:** each square is zero, so `x=2,y=-1`.

**Profile:** `3/5/4/2/2/5/1/1/4/3`; FAST_IF_RECOGNIZED.

---

# Family D — Discriminant feasibility

## D1
Find all `k` such that

`x^2+kx+16=0`

has a repeated real root. Also find the sum of the possible `k` values.

**Answer:** `k=±8`; sum `0`.

**Solution:** `k^2-64=0`.

**Profile:** `3/4/3/2/3/4/2/2/3/3`; DIRECT.

## D2
For what real `m` does

`x^2-6x+m=0`

have at least one real root?

**Answer:** `m<=9`.

**Solution:** `36-4m>=0`.

**Profile:** `3/4/3/2/3/4/2/2/3/3`; DIRECT.

## D3
For what real `m` does

`x^2+(m-1)x+m=0`

have real roots?

**Answer:** `m<=3-2sqrt2` or `m>=3+2sqrt2`.

**Solution:**

`D=(m-1)^2-4m=m^2-6m+1>=0`.

Roots of the boundary quadratic are `3±2sqrt2`; upward parabola is non-negative outside.

**Profile:** `5/6/5/5/5/6/4/4/6/5`; MULTISTEP.

---

# Family E — Absolute / rational intervals

## E1
How many integers satisfy

`|x-6|<4`?

**Answer:** `7`.

**Solution:** `2<x<10`; integers `3,4,5,6,7,8,9`.

**Profile:** `2/3/2/2/2/3/2/2/3/2`; DIRECT.

## E2
How many integers satisfy

`3/|x-5|>1`?

**Answer:** `4`.

**Solution:** domain `x!=5`; inequality gives `|x-5|<3`, so `2<x<8`, excluding 5. Integers `3,4,6,7`.

**Profile:** `4/5/5/4/3/5/4/3/6/5`; FAST_IF_RECOGNIZED.

## E3
Solve

`((x-1)(x-4))/(x+2) <=0`.

**Answer:** `(-infinity,-2) union [1,4]`.

**Solution:** critical points `-2,1,4`; sign chart; `-2` excluded, numerator zeros included.

**Profile:** `5/6/5/5/4/5/6/4/7/6`; CASE_HEAVY.

---

# Family F — Direct bounds / equality feasibility / source QC

## F1
Find the maximum and minimum of

`5+3cos t`.

**Answer:** maximum `8`, minimum `2`.

**Solution:** `-1<=cos t<=1`.

**Profile:** `2/3/2/2/2/3/1/1/2/2`; DIRECT.

## F2
A printed item says:

“Positive `a,b` satisfy `ab=4`. Find the maximum of `a+b`.”

A supplied key says `4`.

What should be recorded?

**Answer:** printed problem has no maximum; `4` is the minimum at `a=b=2`; record `SOURCE_CONFLICT` rather than changing the stem.

**Profile:** `6/7/7/4/2/8/3/2/9/6`; FAST_IF_RECOGNIZED.

## F3
Positive integers `a,b` satisfy `a+b=7`.

Find the maximum of `ab` and explain why the continuous AM-GM equality value is not attained.

**Answer:** `12`, attained at `(3,4)` or `(4,3)`.

**Solution:** real AM-GM bound is `ab<=49/4=12.25`, with equality requiring `a=b=3.5`, impossible for integers. Test nearest integer pair 3 and 4.

**Profile:** `5/6/6/4/3/7/5/3/7/5`; FAST_IF_RECOGNIZED.

---

# Error tags

- `AMGM_USED_BEFORE_BOUNDEDNESS`
- `MIN_REPORTED_AS_MAX`
- `EQUALITY_CONDITION_OMITTED`
- `EQUALITY_CONDITION_INFEASIBLE`
- `CAUCHY_COEFFICIENT_SQUARE_MISSED`
- `COMPLETING_SQUARE_SIGN_ERROR`
- `ZERO_SUM_SQUARE_NOT_COLLAPSED`
- `DISCRIMINANT_WRONG_DIRECTION`
- `ABSOLUTE_VALUE_INTERVAL_REVERSED`
- `DENOMINATOR_ZERO_INCLUDED`
- `STRICT_ENDPOINT_INCLUDED`
- `RATIONAL_SIGN_CHART_ERROR`
- `INTEGER_FILTER_APPLIED_TOO_EARLY`
- `SOURCE_CONFLICT_NOT_FLAGGED`

## Review state

`MATH_REVIEW: PASS_v1`

All 18 items have independently derived solutions above. Final classroom timing/render QA remains outside this internal math pass.
