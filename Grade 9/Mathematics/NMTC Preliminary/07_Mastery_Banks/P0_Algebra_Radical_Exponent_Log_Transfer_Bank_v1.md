# P0 Algebra — Radical / Exponent / Log Transfer Bank v1

## Purpose

18 original non-identical transfer items grounded in the qualified Preliminary mechanism families.

Every item is:

`AUTHOR_CREATED_TRANSFER`

No item is presented as an NMTC previous-year question.

Profile:

`C/R/F/S/A/H/K/B/T/P`

= conceptual / recognition / first-move / reasoning / algebra / hidden structure / cases / calculation burden / trap density / time pressure.

---

# Family A — Common radical / exponent basis

## A1
Simplify

`(sqrt(72)-sqrt(8))/sqrt(2)`.

**Answer:** `4`.

**Solution:** `sqrt72=6sqrt2`, `sqrt8=2sqrt2`; numerator `4sqrt2`.

**Profile:** `2/3/2/2/2/3/1/2/2/2`; DIRECT.

## A2
Let `t=cuberoot(2)`. Simplify

`cuberoot(54)+cuberoot(128)-cuberoot(2)`.

**Answer:** `6t=6cuberoot(2)`.

**Solution:** `3t+4t-t`.

**Profile:** `3/4/3/2/2/4/1/2/2/3`; FAST_IF_RECOGNIZED.

## A3
Evaluate exactly

`32^(3/5)`.

**Answer:** `8`.

**Solution:** `32=2^5`, so `(2^5)^(3/5)=2^3`.

**Profile:** `2/3/2/2/2/3/2/1/2/2`; DIRECT.

---

# Family B — Reconstruct hidden surds

## B1
Simplify

`sqrt(7+4sqrt(3))`.

**Answer:** `2+sqrt(3)`.

**Solution:** `(2+sqrt3)^2=7+4sqrt3`.

**Profile:** `4/5/4/3/3/5/2/2/4/4`; FAST_IF_RECOGNIZED.

## B2
Simplify

`sqrt(13-4sqrt(10))`.

**Answer:** `2sqrt(2)-sqrt(5)`.

**Solution:** `(sqrt8-sqrt5)^2=8+5-2sqrt40=13-4sqrt10`; the displayed root is positive because `sqrt8>sqrt5`.

**Profile:** `5/6/5/4/4/6/3/3/5/5`; FAST_IF_RECOGNIZED.

## B3
Evaluate

`(7+4sqrt3)^(3/2)-(7-4sqrt3)^(3/2)`.

**Answer:** `30sqrt3`.

**Solution:** `7±4sqrt3=(2±sqrt3)^2`, with both `2±sqrt3>0`. Thus the expression is `(2+s)^3-(2-s)^3`, `s=sqrt3`, equal to `24s+2s^3=30s`.

**Profile:** `6/7/6/5/5/7/3/4/6/6`; MULTISTEP.

---

# Family C — Reciprocal invariants and radical equations

## C1
If `t+1/t=6`, find `t^3+1/t^3`.

**Answer:** `198`.

**Solution:** `t^3+t^-3=6^3-3·6=198`.

**Profile:** `4/5/4/3/3/5/2/2/4/4`; FAST_IF_RECOGNIZED.

## C2
Let

`x=(sqrt5+1)/(sqrt5-1)`.

Find `x+1/x` without first finding a decimal value of `x`.

**Answer:** `3`.

**Solution:**

`x+1/x=[(sqrt5+1)^2+(sqrt5-1)^2]/(5-1)=12/4=3`.

**Profile:** `5/6/5/4/4/6/2/3/5/5`; FAST_IF_RECOGNIZED.

## C3
Solve

`sqrt(x+7)=(3/2)sqrt(x-2)`.

**Answer:** `46/5`.

**Solution:** domain `x>=2`. Square: `x+7=(9/4)(x-2)` -> `4x+28=9x-18` -> `x=46/5`, valid in the original equation.

**Profile:** `4/4/4/4/4/4/4/3/5/4`; MULTISTEP.

---

# Family D — Exponential normalization

## D1
Solve

`8^x=4^(x+1)`.

**Answer:** `2`.

**Solution:** `2^(3x)=2^(2x+2)`.

**Profile:** `2/3/2/2/2/3/1/1/2/2`; DIRECT.

## D2
Solve

`4^x-5·2^x+4=0`.

**Answer:** `x=0,2`.

**Solution:** set `t=2^x>0`; `t^2-5t+4=0`; `t=1,4`.

**Profile:** `4/5/4/3/4/5/2/2/4/4`; FAST_IF_RECOGNIZED.

## D3
Solve

`9^x-10·6^x+9·4^x=0`.

**Answer:** `x=0` or `x=log_(3/2)9`.

**Solution:** divide by `4^x>0`; set `t=(3/2)^x>0`. Then `t^2-10t+9=0`, so `t=1,9`.

**Profile:** `6/7/6/5/5/7/3/4/6/6`; FAST_IF_RECOGNIZED.

---

# Family E — Logarithmic variable substitution

## E1
Solve

`(log_2 x)^2-3log_2 x+2=0`.

**Answer:** `x=2,4`.

**Solution:** `t=log_2 x`; `t=1,2`; map back.

**Profile:** `3/4/3/3/3/4/3/2/3/3`; DIRECT.

## E2
Solve

`log_2 x-4sqrt(log_2 x)+3=0`.

**Answer:** `x=2,512`.

**Solution:** set `t=sqrt(log_2 x)>=0`; `t^2-4t+3=0`; `t=1,3`; hence `log_2 x=1,9`.

**Profile:** `5/6/6/4/4/6/4/3/6/5`; FAST_IF_RECOGNIZED.

## E3
Solve

`(log_3 x)^2=4log_3 x+5`.

**Answer:** `x=1/3,243`.

**Solution:** `t=log_3 x`; `t^2-4t-5=0`; `t=-1,5`; both give positive `x`.

**Profile:** `4/5/4/3/3/5/3/2/4/4`; DIRECT.

---

# Family F — Log systems and exact inverse structure

## F1
Positive `x,y` satisfy

`log_4 x=log_2 y`

and

`x-y=12`.

Find `x+y`.

**Answer:** `20`.

**Solution:** `x=y^2`; `y^2-y-12=0`; positive `y=4`; `x=16`.

**Profile:** `5/6/5/4/4/6/4/3/5/5`; MULTISTEP.

## F2
Positive `x,y` satisfy

`log_9 x=log_3 y`

and

`x-y=20`.

Find `x+y`.

**Answer:** `30`.

**Solution:** `x=y^2`; `y^2-y-20=0`; positive `y=5`, `x=25`.

**Profile:** `5/6/5/4/4/6/4/3/5/5`; MULTISTEP.

## F3
Evaluate exactly

`25^(log_5 2)`.

**Answer:** `4`.

**Solution:** `25=5^2`, so `(5^2)^(log_5 2)=5^(2log_5 2)=(5^(log_5 2))^2=4`.

**Profile:** `4/5/4/3/3/5/2/2/4/4`; FAST_IF_RECOGNIZED.

---

# Mastery rule

A family is adopted only if the learner can:

1. name the first move before calculation;
2. solve at least 2/3 items;
3. state the relevant domain/reversibility condition;
4. solve a fresh surface-changed item preserving the invariant.

## Error tags

- `COMMON_BASIS_NOT_FOUND`
- `FALSE_RADICAL_DISTRIBUTION`
- `PRINCIPAL_ROOT_SIGN_ERROR`
- `SQUARED_TOO_EARLY`
- `EXTRANEOUS_ROOT_NOT_CHECKED`
- `RECIPROCAL_INVARIANT_MISSED`
- `EXPONENTIAL_BASES_NOT_NORMALIZED`
- `UNNECESSARY_LOG_USE`
- `LOG_DOMAIN_IGNORED`
- `WRONG_LOG_SUBSTITUTION_OBJECT`
- `EXACT_INVERSE_STRUCTURE_MISSED`

## Review state

`MATH_REVIEW: PASS_v1`

All 18 answers above have compact independent derivations. Final editorial/classroom calibration remains pending.
