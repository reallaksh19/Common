# P0 Algebra — Radical / Exponent / Log Mastery Test v1

## Purpose

Unlabelled mixed assessment for the Radical / Exponent / Logarithmic Transformations package.

All questions are original `AUTHOR_CREATED_TRANSFER` items. They are not NMTC PYQs.

Before solving each item, write one first-move code:

- `CB` common basis
- `HS` hidden surd
- `RI` reciprocal invariant
- `RE` radical equation
- `EN` exponential normalization
- `LS` logarithmic substitution
- `LI` log/exponent inverse relation
- `DR` domain/reversibility check
- `QC` source/consistency check

Suggested internal training window: **40 minutes** for all 12 after instruction. This is not an official NMTC timing claim.

---

# Student paper

## Q1
Simplify

`(sqrt(162)-sqrt(18))/sqrt(2)`.

## Q2
Simplify

`sqrt(18-6sqrt5)`.

## Q3
If

`t+1/t=4`,

find

`t^4+1/t^4`.

## Q4
Solve over the reals:

`sqrt(x+4)=x-2`.

## Q5
Solve

`27^x=9^(x+1)`.

## Q6
Solve

`4^x-10·2^x+16=0`.

## Q7
Solve

`(log_2 x)^2-4log_2 x+3=0`.

## Q8
Solve

`log_2 x-5sqrt(log_2 x)+4=0`.

## Q9
Positive `x,y` satisfy

`log_4 x=log_2 y`

and

`x-y=6`.

Find `x+y`.

## Q10
Evaluate exactly

`8^(log_2 3)`.

## Q11 — sign discipline

A student writes

`sqrt((a-3)^2)=a-3`

for every real `a`.

Is the statement valid? Give the correct form and the condition under which the student's form is valid.

## Q12 — false-law / source-integrity check

A printed solution contains the step

`log_2(x+4)=log_2 x+log_2 4`.

State whether the step is valid. If it is invalid, give the correct action a student or editor should take rather than continuing from it.

---

# Answer and review section

## Q1
**First move:** `CB`.

`sqrt162=9sqrt2`, `sqrt18=3sqrt2`.

So

`(9sqrt2-3sqrt2)/sqrt2=6`.

**Answer:** `6`.

**Error tags:** `COMMON_BASIS_NOT_FOUND`, `RADICAL_SIMPLIFICATION_ERROR`.

---

## Q2
**First move:** `HS`.

Seek `sqrt a-sqrt b` with

`a+b=18`, `2sqrt(ab)=6sqrt5`.

Thus `ab=45`, so `{a,b}={15,3}`.

Because `sqrt15>sqrt3`,

**Answer:** `sqrt15-sqrt3`.

Check:

`(sqrt15-sqrt3)^2=18-6sqrt5`.

**Error tags:** `HIDDEN_SURD_NOT_RECONSTRUCTED`, `PRINCIPAL_ROOT_SIGN_ERROR`.

---

## Q3
**First move:** `RI`.

`t^2+t^-2=4^2-2=14`.

Then

`t^4+t^-4=14^2-2=194`.

**Answer:** `194`.

**Error tags:** `RECIPROCAL_INVARIANT_MISSED`, `SOLVED_VARIABLE_UNNECESSARILY`.

---

## Q4
**First move:** `RE` + `DR`.

The right side must be nonnegative, so `x>=2`.

Square:

`x+4=(x-2)^2=x^2-4x+4`.

Thus

`x^2-5x=0`, giving candidates `x=0,5`.

Only `x=5` satisfies the domain and original equation.

**Answer:** `5`.

**Error tags:** `RADICAL_DOMAIN_NOT_NOTICED`, `EXTRANEOUS_ROOT_NOT_CHECKED`.

---

## Q5
**First move:** `EN`.

`27=3^3`, `9=3^2`.

`3^(3x)=3^(2x+2)`.

Therefore `x=2`.

**Answer:** `2`.

**Error tags:** `EXPONENTIAL_BASES_NOT_NORMALIZED`.

---

## Q6
**First move:** `EN`.

Let `t=2^x>0`.

Then

`t^2-10t+16=0`

`=(t-2)(t-8)`.

So `t=2,8`, hence

**Answer:** `x=1,3`.

**Error tags:** `EXPONENTIAL_BASES_NOT_NORMALIZED`, `POSITIVE_SUBSTITUTION_DOMAIN_IGNORED`.

---

## Q7
**First move:** `LS`.

Let `t=log_2 x`, with `x>0`.

`t^2-4t+3=0`, so `t=1,3`.

Thus

**Answer:** `x=2,8`.

**Error tags:** `WRONG_LOG_SUBSTITUTION_OBJECT`, `LOG_DOMAIN_IGNORED`.

---

## Q8
**First move:** `LS`.

Let

`t=sqrt(log_2 x)>=0`.

Then

`t^2-5t+4=0`, so `t=1,4`.

Thus

`log_2 x=1,16`.

**Answer:** `x=2,65536`.

**Error tags:** `WRONG_LOG_SUBSTITUTION_OBJECT`, `LOST_SQUARE_ON_BACK_SUBSTITUTION`, `LOG_DOMAIN_IGNORED`.

---

## Q9
**First move:** `LI`.

`log_4 x=log_2 y`

means

`(1/2)log_2 x=log_2 y`.

Hence `x=y^2` for positive `x,y`.

Now

`y^2-y=6`, so

`(y-3)(y+2)=0`.

Positivity gives `y=3`, `x=9`.

**Answer:** `12`.

**Error tags:** `LOG_TO_ALGEBRA_LINK_MISSED`, `LOG_DOMAIN_IGNORED`.

---

## Q10
**First move:** `LI`.

`8^(log_2 3)=(2^3)^(log_2 3)`

`=2^(3log_2 3)`

`=(2^(log_2 3))^3=3^3`.

**Answer:** `27`.

**Error tags:** `EXACT_INVERSE_STRUCTURE_MISSED`, `DECIMAL_APPROXIMATION_TOO_EARLY`.

---

## Q11
**First move:** `DR`.

For every real `a`,

`sqrt((a-3)^2)=|a-3|`.

It equals `a-3` only when

`a>=3`.

**Answer:** student's unrestricted statement is invalid.

**Error tags:** `PRINCIPAL_ROOT_SIGN_ERROR`.

---

## Q12
**First move:** `QC`.

The step is invalid.

The valid product law is

`log_b(uv)=log_bu+log_bv`,

not a corresponding law for addition.

There is no simplification

`log_2(x+4)=log_2x+2`.

**Correct action:** stop, re-check the source/derivation, mark the step as a mathematical error or `SOURCE_CONFLICT` where appropriate, and continue only from valid mathematics.

**Error tags:** `FALSE_LOG_SUM_LAW`, `SOURCE_CONFLICT_NOT_FLAGGED`.

---

# Internal scoring

Suggested diagnostic scoring:

- 1 mark: correct first-move classification;
- 2 marks: correct mathematics;
- 1 mark: domain/sign/reversibility check where applicable.

This is not an official NMTC marking scheme.

## Mastery bands

### `ADOPTED`

- at least 10/12 first moves correct;
- at least 10/12 mathematical conclusions correct;
- Q4, Q11 and Q12 correct because they test checking discipline rather than routine mechanics.

### `MECHANICS_OK_RECOGNITION_WEAK`

Final answers mostly correct, but fewer than 10 first moves correct.

Remediation: repeat Recognition Lab and First-Line Lab rather than adding routine worksheets.

### `DOMAIN_REVERSIBILITY_GAP`

Any two failures among Q4, Q8, Q9, Q11.

Remediation: revisit domain, principal-root and reversible-transformation sections.

### `STRUCTURE_GAP`

Misses two or more among Q2, Q3, Q6, Q8, Q10.

Remediation: representation-switch ladder.

### `CHECKING_GAP`

Fails Q12 despite strong calculation performance.

Remediation: false-law/source-integrity contrast set.

---

# Publication state

`MATH_REVIEW: PASS_v1`

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`

`FINAL_EDITORIAL_QA: NOT_RUN`

Ready for internal diagnostic use, not final student publication/PDF release.
