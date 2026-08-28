# P0 Algebra — Radical / Exponent / Log Practice Ladders v1

## Contract

Each family progresses:

`F0 FOUNDATION -> F1 DIRECT -> F2 STANDARD -> F3 DISGUISED -> F4 PRELIMINARY -> PYQ -> XF TRANSFER`

From F2 onward, learner writes the first move before calculating.

---

# Ladder 1 — Common radical basis

## F0
Simplify `sqrt(75)`.

**Answer:** `5sqrt(3)`.

## F1
Simplify `sqrt(12)+sqrt(27)-sqrt(3)`.

**Answer:** `4sqrt(3)`.

## F2
Simplify

`(sqrt(18)+sqrt(8))/sqrt(2)`.

**Answer:** `5`.

## F3
Let `t=cuberoot(2)`. Simplify `cuberoot(16)+cuberoot(54)` in terms of `t`.

**Answer:** `2t+3t=5t`.

## F4
A quotient contains several square roots sharing only `sqrt(2)` and `sqrt(3)` as independent bases. Rewrite numerator and denominator completely before dividing.

## PYQ
- `NMTC-BH-P-2018-Q01`
- `NMTC-BH-P-2023-Q26`
- `NMTC-BH-P-2025-Q03`

## XF
Create a new expression using `sqrt(5),sqrt(20),sqrt(45),sqrt(80)` whose numerator and denominator share a factor after common-basis reduction.

---

# Ladder 2 — Reconstruct hidden surds

## F0
Expand `(sqrt(5)+sqrt(2))^2`.

**Answer:** `7+2sqrt(10)`.

## F1
Rewrite `7+2sqrt(10)` as a square.

**Answer:** `(sqrt(5)+sqrt(2))^2`.

## F2
Simplify `sqrt(9+4sqrt(5))`.

**Answer:** `sqrt(5)+2`.

## F3
Recognize `14-6sqrt(5)` as a square and simplify its principal square root.

**Answer:** `3-sqrt(5)` because `(3-sqrt(5))^2=14-6sqrt(5)` and `3>sqrt(5)`.

## F4
A conjugate pair `A±Bsqrt(d)` is raised to `3/2`. Reconstruct both bases as squares, then convert to cubes before combining.

## PYQ
- `NMTC-BH-P-2023-Q21`
- `NMTC-BH-P-2025-Q04`
- `NMTC-BH-P-2024-Q26`

## XF
Use `11±6sqrt(2)=(3±sqrt(2))^2` and ask for an exact difference/sum of `3/2` powers.

---

# Ladder 3 — Reciprocal radical invariant

## F0
If `t+1/t=5`, find `t^2+1/t^2`.

**Answer:** `23`.

## F1
If `t+1/t=3`, find `t^3+1/t^3`.

**Answer:** `18`.

## F2
If `x=(sqrt(a+b)+sqrt(a-b))/(sqrt(a+b)-sqrt(a-b))`, look for `x+1/x` before solving for `a,b`.

## F3
A cube-root pair gives `t^3+t^-3`; recover it from `t+t^-1` using the cubic identity.

## F4
A radical ratio is designed so the target is `x+1/x` rather than `x`. Compute the symmetric invariant directly.

## PYQ
- `NMTC-BH-P-2018-Q21`
- `NMTC-BH-P-2025-Q09`

## XF
Author a new square-root ratio with parameters `p,q` where the requested target is `x+1/x`, and choose values giving a rational result.

---

# Ladder 4 — Radical equations and checking

## F0
Solve `sqrt(x)=3`.

**Answer:** `9`.

## F1
Solve `sqrt(x+1)=x-1` with domain checking.

**Answer:** `x=3`.

**Reason:** domain `x>=1`; squaring gives `x+1=(x-1)^2`, so `x=0 or 3`; only 3 survives.

## F2
Solve `sqrt(x+4)=2sqrt(x-5)`.

**Answer:** `x=8`.

## F3
Solve a ratio of two radicals by cross-multiplying before squaring.

## F4
Contrast a square-root equation with a cube-root equation: identify which transformation can introduce extraneous roots and which is reversible over reals.

## PYQ
- clean: `NMTC-BH-P-2018-Q26`
- QC contrast only: `NMTC-BH-P-2025-Q18`

## XF
Solve `sqrt(2x+3)=3sqrt(x-1)` and verify in the original equation.

**Answer:** `x=12/7`? Check: `2x+3=9x-9` -> `12=7x` -> `x=12/7`, domain `x>=1`, valid.

---

# Ladder 5 — Normalize exponential bases

## F0
Rewrite `8^x` and `4^x` as powers of 2.

## F1
Solve `4^x=8`.

**Answer:** `x=3/2`.

## F2
Solve `2^(2x)-5·2^x+4=0` using `t=2^x`.

**Answer:** `x=0 or 2`.

## F3
An equation contains both `2^x` and `3^x`; divide by a suitable common exponential factor and set `t=(2/3)^x`.

## F4
Decide whether common-base normalization or logarithms gives the shorter first move. Justify before solving.

## PYQ
- `NMTC-BH-P-2023-Q07`
- `NMTC-BH-P-2024-Q04`
- `NMTC-BH-P-2024-Q09`

## XF
Solve `9^x-10·6^x+9·4^x=0` by dividing by `4^x` and setting `t=(3/2)^x`.

**Answer:** `t^2-10t+9=0`; `t=1 or 9`; so `x=0` or `x=log_(3/2) 9`.

---

# Ladder 6 — Log meaning and laws

## F0
Convert `5^3=125` into logarithmic form.

**Answer:** `log_5 125=3`.

## F1
Using exponent laws, explain why `log_b(MN)=log_b M+log_b N` for positive `M,N` and valid base `b`.

## F2
Solve `log_2 x=5`.

**Answer:** `32`.

## F3
Solve `log_3(x-1)=2`, including domain.

**Answer:** `10`.

## F4
Reject the false manipulation `log(a+b)=log a+log b` by a numerical counterexample.

## PYQ
PYQs usually assume this foundation; the deeper anchors occur in the substitution ladders below.

## XF
Derive the quotient and power rules from exponent form without using them as memorized facts.

---

# Ladder 7 — Log-variable substitution

## F0
Let `t=log_2 x`; rewrite `(log_2 x)^2-5log_2 x+6=0`.

## F1
Solve it.

**Answer:** `t=2,3`, so `x=4,8`.

## F2
If `sqrt(log_2 x)` repeats, set the whole square-root log equal to `t`, with `t>=0`.

## F3
Solve `log_2 x-3sqrt(log_2 x)+2=0`.

**Answer:** set `t=sqrt(log_2 x)`; `t^2-3t+2=0`; `t=1,2`; `x=2,16`.

## F4
Given an expression with both `sqrt(log_b x)` and `log_b x`, choose between `t=log_b x` and `u=sqrt(log_b x)` before solving; justify the cheaper algebra.

## PYQ
- `NMTC-BH-P-2024-Q12`
- `NMTC-BH-P-2025-Q12`

## XF
Solve `log_3 x-5sqrt(log_3 x)+6=0`.

**Answer:** `sqrt(log_3 x)=2 or 3`; `x=3^4=81` or `3^9=19683`.

---

# Ladder 8 — Log systems to algebra

## F0
If `log_2 x=log_2 y`, what follows under valid domains?

**Answer:** `x=y`.

## F1
Convert `log_4 x=log_2 y` to an algebraic relation.

**Answer:** `x=y^2`, with `x,y>0`.

## F2
Combine that with `x+y=6` and solve positive solutions.

**Answer:** `y^2+y-6=0`; `y=2`, `x=4`.

## F3
A log relation and a quadratic/polynomial relation produce several algebraic candidates; reject any violating the original log domains.

## F4
Use two different bases only until they have been translated to one base/power relation; then finish algebraically.

## PYQ
- `NMTC-BH-P-2025-Q27`

## XF
Solve positive `x,y` satisfying `log_9 x=log_3 y` and `x-y=6`.

**Answer:** `x=y^2`; `y^2-y-6=0`; positive `y=3`, so `x=9`.

---

# Ladder 9 — Exact log-exponent simplification

## F0
Simplify `2^(log_2 7)`.

**Answer:** `7`.

## F1
Simplify `10^(log_10 3)`.

**Answer:** `3`.

## F2
Rewrite an awkward base as a power of 10 before applying an exponent containing `log_10`.

## F3
Use change of base only if it produces exact cancellation.

## F4
Choose exact structure over decimal approximation in a multi-step expression.

## PYQ
- `NMTC-BH-P-2024-Q28`

## XF
Simplify exactly `(10^(-1/2))^(-2log_10 5)`.

**Answer:** exponent product is `log_10 5`; result `5`.

---

# Mixed speed contract

Recognition codes:

- `CB` common basis
- `RS` reconstruct surd
- `RI` reciprocal invariant
- `RQ` radical equation
- `EN` exponential normalization
- `LV` log variable
- `LA` log to algebra
- `LE` log/exponent exact simplification
- `DC` domain/check

Targets:

- recognition: `>=16/20`;
- first-line: `>=10/12`;
- mixed solve: `>=8/10` after instruction;
- at least one valid domain/check statement on every radical/log equation where applicable.

## Error tags

- `RADICAL_NOT_REDUCED_TO_COMMON_BASIS`
- `FALSE_RADICAL_DISTRIBUTION`
- `PRINCIPAL_ROOT_SIGN_ERROR`
- `SQUARED_TOO_EARLY`
- `EXTRANEOUS_ROOT_NOT_CHECKED`
- `EXPONENTIAL_BASES_NOT_NORMALIZED`
- `LOG_DOMAIN_IGNORED`
- `WRONG_LOG_SUBSTITUTION_OBJECT`
- `DECIMAL_APPROXIMATION_BEFORE_EXACT_SIMPLIFICATION`
- `TRANSFORMED_MULTIPLICITY_CONFUSED_WITH_ORIGINAL_ROOT_SET`
