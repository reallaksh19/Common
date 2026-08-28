# P0 Algebra — Polynomial & Root Structure Mastery Test v1

## Purpose

Unlabelled mixed test for the first P0 algebra package.

All questions are original `AUTHOR_CREATED_TRANSFER` items. They are not NMTC PYQs.

The learner must write a **first-move code** before each solution:

- `PR` power reduction
- `VT` Vieta
- `RM` remainder/mod polynomial
- `FT` factor first
- `IR` integer/positive-root constraint
- `CR` common-root elimination
- `SH` shift/transformed roots
- `BD` boundedness/equality
- `QC` source/consistency check

Suggested training window: 45 minutes for all 12 after the unit is learned. This is an internal mastery target, not an official NMTC timing claim.

---

# Student paper

## Q1
A number `x` satisfies

`x^2=3x-1`.

Express `x^4` in the form `ax+b`.

---

## Q2
Find the remainder when

`x^31+3x^18+2`

is divided by `x^2+1`.

---

## Q3
The roots of

`2x^2+3x-4=0`

are `alpha,beta`.

Find

`alpha/beta + beta/alpha`

without finding `alpha,beta` separately.

---

## Q4
The roots of

`x^2-6x+7=0`

are `alpha,beta`.

Form the monic quadratic whose roots are

`alpha+1,beta+1`.

---

## Q5
Solve

`x^4-10x^2+9=0`.

Then find the product of its positive roots.

---

## Q6
The polynomials

`x^2-x-1`

and

`x^3-2x-k`

have a common root.

Find `k`.

---

## Q7
For what values of `m` does

`x^2+(m+2)x+9=0`

have a repeated real root?

Find the sum of those values of `m`.

---

## Q8
Four positive numbers have sum `20` and product `625`.

Find the sum of their squares.

---

## Q9
Factor as far as possible over the rational numbers:

`x^4+4x^3+5x^2+4x+1`.

---

## Q10
Find the remainder when

`P(x)=x^3-4x+5`

is divided by `2x-6`.

---

## Q11
Positive real numbers `a,b` satisfy `ab=1`.

Does `a^2+b^2` have a maximum? Justify.

---

## Q12 — source-integrity check

A printed practice item says:

> `x^3-6x^2+11x+(5-k)=0` has three positive integer roots. Find `k`.

A supplied answer key says `k=0`.

Determine what the **printed mathematics** gives, and state what should be done with the disagreement.

---

# Answer and review section

## Q1
**First move:** `PR`.

`x^2=3x-1`.

`x^3=3x^2-x=3(3x-1)-x=8x-3`.

`x^4=8x^2-3x=8(3x-1)-3x=21x-8`.

**Answer:** `21x-8`.

**Error tags:** `SOLVED_WHEN_REDUCTION_WAS_ENOUGH`, `SIGN_ERROR`.

---

## Q2
**First move:** `RM`.

Modulo `x^2+1`, `x^2≡-1`, so powers cycle every 4.

`x^31`: `31≡3 (mod4)` -> `-x`.

`x^18`: `18≡2 (mod4)` -> `-1`.

Remainder:

`-x-3+2=-x-1`.

**Answer:** `-x-1`.

**Error tags:** `POLYNOMIAL_MOD_CYCLE_ERROR`.

---

## Q3
**First move:** `VT`.

`alpha+beta=-3/2`, `alpha beta=-2`.

`alpha^2+beta^2=(alpha+beta)^2-2alpha beta`

`=9/4+4=25/4`.

Therefore

`alpha/beta+beta/alpha=(alpha^2+beta^2)/(alpha beta)`

`=(25/4)/(-2)=-25/8`.

**Answer:** `-25/8`.

**Error tags:** `VIETA_SIGN_ERROR`, `ROOTS_SOLVED_UNNECESSARILY`.

---

## Q4
**First move:** `SH` or `VT`.

Original sum `6`, product `7`.

New sum:

`(alpha+1)+(beta+1)=8`.

New product:

`(alpha+1)(beta+1)=7+6+1=14`.

**Answer:** `y^2-8y+14=0`.

**Error tags:** `TRANSFORMED_ROOT_PRODUCT_ERROR`.

---

## Q5
**First move:** `FT`.

Treat as quadratic in `x^2`:

`(x^2-1)(x^2-9)=0`.

Roots:

`±1,±3`.

Positive roots are `1,3`.

**Answer:** product `3`.

**Error tags:** `EXPANDED_BEFORE_FACTORING`.

---

## Q6
**First move:** `CR`.

From

`x^2-x-1=0`,

`x^2=x+1`.

Then

`x^3=x(x+1)=x^2+x=2x+1`.

At a common root:

`x^3-2x-k=(2x+1)-2x-k=1-k=0`.

**Answer:** `k=1`.

**Error tags:** `COMMON_ROOT_NOT_ELIMINATED`.

---

## Q7
**First move:** repeated root -> discriminant zero (`DR`).

`(m+2)^2-36=0`.

So

`m+2=±6`.

`m=4,-8`.

**Answer:** sum `-4`.

**Error tags:** `DISCRIMINANT_SIGN_ERROR`.

---

## Q8
**First move:** `IR/BD` equality condition.

Arithmetic mean:

`20/4=5`.

Geometric mean:

`625^(1/4)=5`.

AM=GM, so all four positive numbers equal 5.

Sum of squares:

`4·25=100`.

**Answer:** `100`.

**Error tags:** `EQUALITY_CONDITION_IGNORED`.

---

## Q9
**First move:** `FT`, recognize palindromic structure.

A compact rational factorization is

`(x^2+x+1)(x^2+3x+1)`.

Expanding verifies:

`x^4+4x^3+5x^2+4x+1`.

The first quadratic has discriminant `-3`; the second has discriminant `5`. Neither factors further over the rational numbers.

**Answer:** `(x^2+x+1)(x^2+3x+1)`.

**Error tags:** `PALINDROMIC_STRUCTURE_MISSED`.

---

## Q10
**First move:** `RM`.

The zero of `2x-6` is `x=3`.

Remainder:

`P(3)=27-12+5=20`.

**Answer:** `20`.

**Error tags:** `WRONG_DIVISOR_ZERO`.

---

## Q11
**First move:** `BD`.

Set

`a=t`, `b=1/t`, `t>0`.

Then

`a^2+b^2=t^2+1/t^2`.

As `t->infinity`, this tends to infinity.

**Answer:** no maximum; unbounded above.

**Error tags:** `FAILED_BOUNDEDNESS_CHECK`.

---

## Q12
**First move:** `QC` plus `IR/VT`.

For three positive integer roots, Vieta gives:

sum `=6`, pairwise-product sum `=11`.

The roots are `1,2,3`, whose product is `6`.

For a monic cubic

`x^3-6x^2+11x+(5-k)`,

the constant term equals `-product=-6`.

So

`5-k=-6`, hence

`k=11`.

The supplied key `k=0` conflicts with the printed mathematics.

**Correct action:** re-check source/edition/key, then mark `SOURCE_CONFLICT`; do not silently alter the stem or force the key.

**Answer from printed stem:** `11`.

**Error tags:** `SOURCE_CONFLICT_NOT_FLAGGED`.

---

# Scoring and diagnosis

Suggested internal scoring:

- 1 mark first-move classification;
- 2 marks correct mathematical execution;
- 1 mark check/condition where applicable.

Not an official NMTC marking scheme.

## Mastery bands

### `ADOPTED`

- at least 10/12 first moves correct;
- at least 9/12 final mathematical answers correct;
- Q11 boundedness and Q12 source-integrity both correct.

### `MECHANICS_OK_RECOGNITION_WEAK`

- at least 9 final answers correct but fewer than 10 first moves correct.

Remediation: Recognition/First-Line Lab, not more routine solving.

### `STRUCTURE_GAPS`

- misses two or more among Q1/Q2/Q3/Q6/Q9.

Remediation: return to power reduction, polynomial modulo, Vieta, common-root and structural-factor units.

### `CHECKING_GAP`

- fails Q11 or Q12 despite otherwise strong solving.

Remediation: boundedness/source-QC contrast set.

---

# Publication status

`MATH_REVIEW: PASS_v1`

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`

`FINAL_EDITORIAL_QA: NOT_RUN`

This test is ready for internal content development and diagnostic trials, not final publication/PDF release.
