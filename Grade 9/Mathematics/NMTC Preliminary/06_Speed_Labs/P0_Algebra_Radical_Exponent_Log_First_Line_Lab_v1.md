# P0 Algebra — Radical / Exponent / Log First-Line Lab v1

## Purpose

Train the learner to write the **first mathematically useful line** before completing the solution.

All items are original. None is an NMTC PYQ.

Suggested internal target:

- 12 items;
- 20 seconds each;
- write only the first useful line or substitution;
- do not finish the calculation in Round A.

This is an internal speed target, not an official NMTC timing claim.

---

# Student sheet

## Q1
Simplify `sqrt(98)-sqrt(32)`.

Write the first useful line.

## Q2
Simplify `sqrt(9+4sqrt5)`.

Write the first useful structural equation.

## Q3
If `t+1/t=7`, find `t^5+1/t^5`.

Write the first recurrence/invariant line.

## Q4
Solve `sqrt(x+10)=(3/2)sqrt(x-2)`.

Write the first line including the domain.

## Q5
Solve `16^x=8^(x+2)`.

Write the normalized-base line.

## Q6
Solve `9^x-10·3^x+9=0`.

Write the substitution.

## Q7
Solve `(log_2 x)^2-7log_2 x+12=0`.

Write the substitution and domain.

## Q8
Solve `log_3 x-5sqrt(log_3 x)+6=0`.

Write the best substitution, not merely the innermost one.

## Q9
Positive `x,y` satisfy `log_9 x=log_3 y`.

Write the equivalent algebraic relation.

## Q10
Evaluate exactly `27^(log_3 2)`.

Write the exponent-log inverse rewrite.

## Q11
A transformed radical equation produces candidate roots `2` and `8`.

Write the required final checking action.

## Q12
A printed solution writes `sqrt((x-4)^2)=x-4` without a condition on `x`.

Write the correction.

---

# Review key

## Q1
`sqrt(98)-sqrt(32)=7sqrt2-4sqrt2`.

Code: `CB`.

## Q2
Seek positive `a,b` such that

`a+b=9`, `2sqrt(ab)=4sqrt5`.

Equivalently `ab=20`.

Code: `HS`.

## Q3
Start with

`t^2+t^-2=(t+t^-1)^2-2=47`,

then build upward, or define `S_n=7S_(n-1)-S_(n-2)`.

Code: `RI`.

## Q4
`x>=2`, then square both sides:

`x+10=(9/4)(x-2)`.

Code: `RE` + `DR`.

## Q5
`2^(4x)=2^(3x+6)`.

Code: `EN`.

## Q6
Let `t=3^x>0`; then

`t^2-10t+9=0`.

Code: `EN`.

## Q7
Let `t=log_2 x`, with `x>0`; then

`t^2-7t+12=0`.

Code: `LS`.

## Q8
Let

`t=sqrt(log_3 x)>=0`.

Then the equation becomes

`t^2-5t+6=0`.

Code: `LS`.

## Q9
`log_9 x=log_3 y` means

`(1/2)log_3 x=log_3 y`, hence `x=y^2` for positive `x,y`.

Code: `LI`.

## Q10
`27^(log_3 2)=(3^3)^(log_3 2)=3^(3log_3 2)=2^3`.

Code: `LI`.

## Q11
Substitute **each candidate into the original radical equation**, not only the squared/transformed equation.

Code: `DR`.

## Q12
`sqrt((x-4)^2)=|x-4|`.

It equals `x-4` only when `x>=4`.

Code: `DR`.

---

# Scoring

- 1 point: correct family/representation.
- 1 point: mathematically valid first line including required domain/sign condition.

Maximum: 24.

Suggested internal bands:

- `22–24`: FIRST_LINE_READY
- `18–21`: MINOR_RECOGNITION_GAPS
- `14–17`: FIRST_MOVE_UNSTABLE
- `<14`: RETURN_TO_CONCEPT_BOOK

## Review status

`MATH_REVIEW: PASS_v1`

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`
