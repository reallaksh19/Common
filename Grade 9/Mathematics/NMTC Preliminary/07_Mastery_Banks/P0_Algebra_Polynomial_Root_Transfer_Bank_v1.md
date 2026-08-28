# P0 Algebra — Polynomial & Root Structure Transfer Bank v1

## Purpose

Original, non-identical transfer problems grounded in the mechanism families observed in qualified Bhaskara Preliminary PYQs.

These are **not previous-year questions**.

Provenance for every item:

`AUTHOR_CREATED_TRANSFER`

Each item has been independently derived for this bank and includes a compact review solution.

Difficulty profile uses:

`C/R/F/S/A/H/K/B/T/P`

= conceptual / recognition / first-move / reasoning-steps / algebra / hidden-structure / constraints-cases / calculation-burden / trap-density / time-pressure, each 0–10.

---

# Family A — Power reduction

## A1
A real or complex number `x` satisfies

`x^2=2x+1`.

Express `x^5` in the form `ax+b`.

**First move:** use the relation as a rewriting rule.

**Answer:** `29x+12`.

**Compact solution:**

`x^3=2x^2+x=5x+2`

`x^4=5x^2+2x=12x+5`

`x^5=12x^2+5x=29x+12`.

**Profile:** `3/4/3/3/4/4/1/3/3/3`; `FAST_IF_RECOGNIZED`.

---

## A2
If

`u+1/u=4`,

find

`u^4+1/u^4`.

**First move:** build reciprocal power sums, not the quadratic roots.

**Answer:** `194`.

**Compact solution:**

`u^2+u^-2=4^2-2=14`.

Then

`u^4+u^-4=14^2-2=194`.

**Profile:** `4/5/4/3/3/5/2/2/4/4`; `FAST_IF_RECOGNIZED`.

---

## A3
A number `r` satisfies

`r^2-r+2=0`.

Express `r^6` as a linear expression in `r`.

**Answer:** `5r+2`.

**Compact solution:** use `r^2=r-2` repeatedly:

`r^3=-r-2`,

`r^4=-3r+2`,

`r^5=-r+6`,

`r^6=5r+2`.

**Profile:** `4/5/4/5/4/5/1/4/4/4`; `MULTISTEP`.

---

# Family B — Polynomial remainder / divisibility

## B1
Find the remainder when

`x^37+2x^14+5`

is divided by `x^2+1`.

**First move:** use the four-step power cycle from `x^2≡-1`.

**Answer:** `x+3`.

**Compact solution:**

`x^37≡x`, `x^14≡-1`.

So remainder `x-2+5=x+3`.

**Profile:** `3/4/3/3/3/4/1/2/3/3`; `FAST_IF_RECOGNIZED`.

---

## B2
Find `a` if

`x^5+a x^3+2x`

is divisible by `x^2+1`.

**Answer:** `3`.

**Compact solution:** modulo `x^2+1`:

`x^5≡x`, `x^3≡-x`.

Remainder is

`(1-a+2)x=(3-a)x`.

Divisibility requires `a=3`.

**Profile:** `4/5/4/3/4/5/2/2/4/4`; `FAST_IF_RECOGNIZED`.

---

## B3
Find `k` if

`x^8+kx^4+1`

is divisible by `x^2+x+1`.

**Answer:** `1`.

**Compact solution:** from `x^3≡1`:

`x^8≡x^2≡-x-1`,

`x^4≡x`.

Remainder:

`(-x-1)+kx+1=(k-1)x`.

Hence `k=1`.

**Profile:** `5/6/5/4/4/6/2/3/5/5`; `FAST_IF_RECOGNIZED`.

---

# Family C — Vieta and transformed roots

## C1
The roots of

`2x^2-5x-3=0`

are `alpha,beta`.

Find `alpha^2+beta^2` without solving for the roots.

**Answer:** `37/4`.

**Compact solution:**

`alpha+beta=5/2`, `alpha beta=-3/2`.

So

`alpha^2+beta^2=25/4+3=37/4`.

**Profile:** `3/4/3/2/3/4/1/2/3/3`; `DIRECT`.

---

## C2
The roots of

`3x^2+7x+2=0`

are `alpha,beta`.

Form the equation whose roots are

`1/alpha,1/beta`.

**Answer:** `2y^2+7y+3=0`.

**Compact solution:**

Original sum `=-7/3`, product `=2/3`.

Reciprocal-root sum `=(-7/3)/(2/3)=-7/2`.

Product `=3/2`.

So

`y^2+(7/2)y+3/2=0`.

Multiply by 2.

**Profile:** `4/5/4/4/4/5/2/3/4/4`; `MULTISTEP`.

---

## C3
The roots of

`x^2-4x+1=0`

are `alpha,beta`.

Form the monic quadratic whose roots are

`alpha+2,beta+2`.

**Answer:** `y^2-8y+13=0`.

**Compact solution:**

Original sum `4`, product `1`.

New sum `8`.

New product:

`alpha beta+2(alpha+beta)+4=1+8+4=13`.

**Profile:** `4/4/4/3/4/4/1/2/3/3`; `DIRECT`.

---

# Family D — Positive/integer roots, bounds and equality

## D1
Four positive numbers have sum `12` and product `81`.

Find the sum of their squares.

**First move:** compare arithmetic and geometric means.

**Answer:** `36`.

**Compact solution:**

AM `=3`; GM `=81^(1/4)=3`.

Equality forces all four numbers to be `3`.

Sum of squares `=4·9=36`.

**Profile:** `5/6/5/3/3/6/3/2/5/5`; `FAST_IF_RECOGNIZED`.

---

## D2
The monic cubic

`x^3-6x^2+11x-k=0`

has three positive integer roots.

Find `k`.

**Answer:** `6`.

**Compact solution:**

Vieta gives root sum `6` and pairwise-product sum `11`.

The positive integer triple is `1,2,3`.

Product `=6`, so `k=6`.

**Profile:** `5/6/5/4/4/6/6/3/5/5`; `CASE_HEAVY`.

---

## D3
Positive real numbers `a,b` satisfy

`ab=1`.

Does `a+b` have a maximum?

**Answer:** No; it is unbounded above.

**Compact solution:**

Let `a=t`, `b=1/t`, with `t>0`.

Then `a+b=t+1/t -> infinity` as `t->infinity`.

A minimum exists (`2`), but no maximum.

**Profile:** `5/6/6/3/2/7/4/2/7/5`; `FAST_IF_RECOGNIZED`.

**Trap:** blindly applying AM-GM and reporting 2 as a maximum.

---

# Family E — Structural cubic/quartic reduction

## E1
Solve

`x^4-5x^2+4=0`.

**First move:** treat it as a quadratic in `x^2`.

**Answer:** `x=±1,±2`.

**Compact solution:**

`(x^2-1)(x^2-4)=0`.

**Profile:** `3/4/3/2/3/4/2/2/3/3`; `DIRECT`.

---

## E2
Factor completely over the reals:

`x^4+5x^3+8x^2+5x+1`.

**First move:** notice reciprocal/palindromic coefficients.

**Answer:**

`(x+1)^2(x^2+3x+1)`.

**Compact solution:** for `x≠0`, divide by `x^2` and set `t=x+1/x`:

`t^2+5t+6=0`, so `t=-2` or `-3`.

These correspond to

`x^2+2x+1` and `x^2+3x+1`.

Their product is the original quartic.

**Profile:** `7/8/7/6/6/8/3/4/7/7`; `FAST_IF_RECOGNIZED`.

---

## E3
Find the largest real root of

`x^3-4x^2-x+4=0`.

**First move:** factor by grouping.

**Answer:** `4`.

**Compact solution:**

`x^2(x-4)-1(x-4)=(x-4)(x^2-1)`

`=(x-4)(x-1)(x+1)`.

**Profile:** `3/4/3/2/3/4/1/2/3/3`; `DIRECT`.

---

# Family F — Common-root elimination

## F1
A number `r` is a common root of

`x^2-3x+1=0`

and

`x^3-3x^2+x+k=0`.

Find `k`.

**Answer:** `0`.

**Compact solution:** the second polynomial is

`x(x^2-3x+1)+k`.

At the common root, the product term is zero, so `k=0`.

**Profile:** `4/6/5/2/3/6/1/1/4/4`; `FAST_IF_RECOGNIZED`.

---

## F2
Integers `m,n` are such that the polynomials

`x^2+x-1`

and

`x^3+2x^2+mx+n`

have a common root.

Find `m+n`.

**Answer:** `-1`.

**Compact solution:** modulo `x^2+x-1`, we have `x^2=1-x` and `x^3=2x-1`.

So the second polynomial reduces to

`mx+n+1`.

The roots of `x^2+x-1` are irrational. For integer `m,n`, an irrational root can satisfy `mx+n+1=0` only when

`m=0`, `n=-1`.

Thus `m+n=-1`.

**Profile:** `7/8/7/6/6/8/6/4/7/7`; `MULTISTEP`.

---

## F3
The polynomials

`x^2-2x-1`

and

`x^3-5x+k`

have a common root.

Find `k`.

**Answer:** `-2`.

**Compact solution:** from the quadratic:

`x^2=2x+1`, hence

`x^3=2x^2+x=5x+2`.

So at either root,

`x^3-5x+k=2+k`.

For a common root, `k=-2`.

**Profile:** `5/6/5/4/4/6/2/3/5/5`; `FAST_IF_RECOGNIZED`.

---

# Transfer-bank mastery rule

The student should not be told the family label on first attempt.

A family is adopted only when the learner can:

1. name the first move;
2. solve at least 2 of its 3 transfer items;
3. explain one tempting wrong move;
4. solve a fresh variant with changed coefficients/surface form.

## Error tags

- `SOLVED_WHEN_REDUCTION_WAS_ENOUGH`
- `EXPANDED_BEFORE_FACTORING`
- `VIETA_SIGN_ERROR`
- `ROOTS_SOLVED_UNNECESSARILY`
- `WRONG_DIVISOR_ZERO`
- `POLYNOMIAL_MOD_CYCLE_ERROR`
- `IGNORED_INTEGER_POSITIVE_CONSTRAINT`
- `FAILED_BOUNDEDNESS_CHECK`
- `COMMON_ROOT_NOT_ELIMINATED`
- `DOMAIN_OR_CONVENTION_ERROR`

## Review status

`MATH_REVIEW: PASS_v1`

All 18 author-created items have independently derived answers in this file. A second editorial pass is still required before publication/PDF generation.
