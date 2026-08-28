# P0 Algebra — Inequalities / Bounds / Equality First-Step Cards

## Use

Student sees an unlabelled problem and must identify the first move before calculating.

Performance loop:

`SEE -> BOUND? -> DOMAIN? -> FIRST MOVE -> EQUALITY? -> CHECK`

---

## Card 1 — Requested maximum/minimum

**SEE**: “maximum”, “minimum”, “least”, “greatest”, “largest”, “smallest”.

**FIRST QUESTION**: does that extremum exist?

**FIRST MOVE**: try an escaping family or obvious bound before applying a named inequality.

Example trigger:

`ab=1`, ask maximum of `a+b`.

Try `a=t`, `b=1/t`. As `t->infinity`, target -> infinity.

**DO NOT**: write AM-GM and call its lower bound a maximum.

**Code**: `BD`.

---

## Card 2 — Positive variables, fixed product, sum requested

**SEE**: positive variables; product fixed; sum or sum of squares asked.

**FIRST MOVE**: check whether a lower bound is natural and whether equality is feasible.

For two variables:

`a+b >= 2sqrt(ab)`.

**EQUALITY**: `a=b`.

**DO NOT** infer a maximum unless another bound exists.

**Code**: `AM`.

---

## Card 3 — Positive variables, fixed sum, product requested

**SEE**: positive variables; sum fixed; product requested.

**FIRST MOVE**: AM-GM gives an upper bound on the product.

For `a+b=S`:

`ab <= (S/2)^2`.

**EQUALITY**: `a=b=S/2`.

**Code**: `AM`.

---

## Card 4 — Reciprocal constraint + linear target

**SEE**: terms such as `1/a`, `k/a`, `m/b`; target resembles `a+b`.

**FIRST MOVE**: test Engel/Cauchy pairing.

Prototype:

`a+b` with `1/a+9/b`.

Use

`(1+3)^2 <= (a+b)(1/a+9/b)`.

**DOMAIN**: denominators positive/nonzero as required.

**EQUALITY**: proportionality condition must be checked.

**Code**: `CY`.

---

## Card 5 — Quadratic expression in one/two variables

**SEE**: `x^2+bx+c`, or sum of quadratics.

**FIRST MOVE**: complete square before trying calculus or guessing.

`x^2-6x+11=(x-3)^2+2`.

**BOUND**: lower bound 2.

**EQUALITY**: `x=3`.

**Code**: `CS`.

---

## Card 6 — Sum of squares equals zero

**SEE**: real variables; expression becomes `A^2+B^2=0`.

**FIRST MOVE**: each square must be zero.

`A=0`, `B=0`.

**DO NOT** keep solving a large system once zero-collapse is available.

**Code**: `ZZ`.

---

## Card 7 — Parameter controls existence of real roots

**SEE**: parameterized quadratic; asks possible parameter/range/count.

**FIRST MOVE**: discriminant.

Real roots: `D>=0`.

Repeated root: `D=0`.

No real root: `D<0`.

**Code**: `DR`.

---

## Card 8 — Absolute value around linear expression

**SEE**: `|x-a|<r`, `<=`, `>`, `>=`.

**FIRST MOVE**: read absolute value as distance.

`|x-a|<r` -> inside interval.

`|x-a|>r` -> outside interval.

**Code**: `AV`.

---

## Card 9 — Absolute value in denominator

**SEE**: `c/|x-a| > k` or similar.

**FIRST MOVE**:

1. record `x!=a`;
2. convert inequality to a distance bound;
3. then count/filter integers.

**DO NOT** include the denominator-zero point.

**Code**: `AV` then `IC`.

---

## Card 10 — Rational inequality

**SEE**: fraction compared with 0.

**FIRST MOVE**:

1. factor numerator/denominator;
2. list zeros and excluded points;
3. build sign intervals.

**DO NOT** cross-multiply by an expression of unknown sign without splitting cases.

**Code**: `RI`.

---

## Card 11 — Real interval then integer count

**SEE**: inequality plus “integer/natural solutions”, count or sum.

**FIRST MOVE**: solve the real inequality first.

Then:

`REAL SET -> DOMAIN FILTER -> INTEGER/NATURAL FILTER -> COUNT/SUM`.

**Code**: `IC`.

---

## Card 12 — Trigonometric or standard direct bound

**SEE**: `sin`, `cos`, square/nonnegative magnitude embedded in larger expression.

**FIRST MOVE**: isolate the directly bounded piece.

`|cos x|<=1`, `A^2>=0`.

Use that bound only in the direction requested.

**Code**: `DB`.

---

## Card 13 — Equality value is offered in answer choices

**SEE**: options include the obvious AM-GM equality value.

**FIRST MOVE**: verify equality is actually feasible under **all** conditions.

A bound is not attained merely because the inequality has an equality case in isolation.

**Code**: `AM` + feasibility check.

---

## Card 14 — Source/key claims an extremum that mathematics rejects

**SEE**: printed stem and supplied answer/key disagree.

**FIRST MOVE**: solve printed mathematics independently.

Then record:

`SOURCE_CONFLICT`.

**DO NOT** alter the inequality sign/word “maximum”/constraint to fit the key.

**Code**: `QC`.

---

# Contrast pairs

1. `ab=1`: minimum of `a+b` **exists**; maximum does **not**.
2. `a+b=10`: maximum of `ab` exists; minimum over positive reals is not attained if strict positivity only and no lower bound away from 0.
3. `D>=0` means real-root feasibility; `D=0` means repeated root.
4. `|x-a|<r` is inside; `|x-a|>r` is outside.
5. numerator zero may be included; denominator zero never is.
6. real interval is not yet an integer answer.

# Adoption criterion

A student has adopted A7 only when, on mixed prompts, they can correctly write one of:

`BD / AM / CY / CS / ZZ / DR / AV / RI / IC / DB / QC`

before calculation and justify why it applies.
