# Inequalities, Bounds & Equality Conditions
## NMTC Bhaskara Preliminary — Student Concept Book Draft v0.1

> **Goal:** do not ask “Which inequality formula should I use?” first. Ask **what is bounded, whether the bound exists, and when equality can occur**.

Use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

and while solving:

`BOUND? -> DOMAIN? -> FIRST MOVE -> EQUALITY? -> VERIFY -> TRANSFER`.

---

# 0. Diagnostic

Try without notes.

1. Is `(a+b)/2 >= sqrt(ab)` valid for all real `a,b`?
2. If `ab=1` and `a,b>0`, does `a+b` have a maximum?
3. What does equality in AM-GM require for two positive numbers?
4. Rewrite `x^2-6x+11` as a square plus constant.
5. If `u^2+v^2=0` for real `u,v`, what follows?
6. What condition on the discriminant gives a repeated real root?
7. Solve `|x-4|<2`.
8. Can `x=3` be included in a solution set containing `1/(x-3)`?

### Answers

1. Not as stated for arbitrary reals because `sqrt(ab)` requires `ab>=0`; standard AM-GM is for non-negative/positive quantities.
2. No.
3. `a=b`.
4. `(x-3)^2+2`.
5. `u=0`, `v=0`.
6. `D=0`.
7. `2<x<6`.
8. No; denominator zero is excluded.

---

# 1. First question: does the requested extremum exist?

## SEE

Positive numbers `a,b` satisfy:

`ab=1`.

Find the maximum of `a+b`.

A common reflex is:

`a+b >= 2sqrt(ab)=2`.

But that is a **lower bound**.

It says nothing about a maximum.

## REALIZE

Before optimizing, test whether the target can escape.

Let:

`a=t`, `b=1/t`, with `t>0`.

Then:

`a+b=t+1/t`.

As `t` becomes very large, `t+1/t` becomes arbitrarily large.

Therefore:

- minimum exists: `2`;
- maximum does not exist.

## UNDERSTAND

An inequality can prove one side of a bound while the other side remains unbounded.

So the correct order is:

`ASK WHICH DIRECTION IS NEEDED -> TEST BOUNDEDNESS -> THEN CHOOSE A TOOL`.

## PYQ CONNECTION

`NMTC-BH-P-2023-Q17` is a key Preliminary contrast: the requested maximum is unbounded. The first move is a boundedness test, not blind AM-GM.

## ADOPT

For positive `x,y` with `xy=9`:

1. Does `x+y` have a minimum?
2. Does it have a maximum?

**Answer:** minimum `6`, no maximum.

---

# 2. AM-GM begins with a square, not a formula

For positive `a,b`:

`(sqrt(a)-sqrt(b))^2 >= 0`.

Expand:

`a+b-2sqrt(ab) >= 0`.

So:

`a+b >= 2sqrt(ab)`.

Divide by 2:

`(a+b)/2 >= sqrt(ab)`.

This is the two-variable AM-GM inequality.

## Equality condition

The square becomes zero exactly when:

`sqrt(a)=sqrt(b)`

so:

`a=b`.

This is not an afterthought. It tells you **where the bound is attained**.

---

# 3. Fixed product and fixed sum are different optimization problems

## Fixed positive product

If:

`ab=P`,

then:

`a+b >= 2sqrt(P)`.

So the sum has a **minimum** at:

`a=b=sqrt(P)`.

There is generally no maximum unless another condition bounds the variables.

## Fixed positive sum

If:

`a+b=S`,

then:

`S/2 >= sqrt(ab)`.

Square:

`ab <= S^2/4`.

So the product has a **maximum** at:

`a=b=S/2`.

### Contrast

Do not memorize “AM-GM gives maximum/minimum.”

Ask:

- what is fixed?
- what is the target?
- which direction does the inequality produce?

---

# 4. Equality can collapse an entire root problem

Suppose four positive numbers have:

- product `1`;
- sum `4`.

AM-GM gives:

`(sum)/4 >= fourth_root(product)`

`1 >= 1`.

Equality holds.

Therefore all four numbers must be equal to 1.

If those four numbers are the positive roots of a quartic, you have recovered all roots without solving the quartic.

## PYQ CONNECTION

`NMTC-BH-P-2024-Q17` uses this equality-collapse idea with positive roots and Vieta data.

## ADOPT

Four positive numbers have product `16` and sum `8`.

AM-GM gives average `2`, geometric mean `2`, so equality holds.

Therefore all four numbers equal `2`.

---

# 5. Reciprocal constraints suggest Cauchy/Engel

## SEE

Suppose positive `a,b` satisfy:

`1/a + 9/b = 1`.

Find the least possible `a+b`.

The coefficients `1` and `9` are squares:

`1^2`, `3^2`.

Cauchy/Engel gives:

`(a+b)(1/a+9/b) >= (1+3)^2`.

Since the reciprocal expression equals 1:

`a+b >= 16`.

## Equality condition

Equality in Engel form occurs when the relevant ratios are proportional. Here it leads to:

`a/1 = b/3` in the appropriate squared-coefficient formulation, giving the attaining pair after substitution.

The important point is not memorizing the equality formula; it is verifying that the lower bound can actually be attained.

## PYQ CONNECTION

`NMTC-BH-P-2018-Q12` is a clean reciprocal-bound anchor.

---

# 6. Completing a square manufactures a bound

## SEE

Find the minimum of:

`x^2-6x+11`.

Complete the square:

`x^2-6x+11`

`=(x-3)^2+2`.

Since:

`(x-3)^2 >= 0`,

the expression is at least 2.

Equality occurs at:

`x=3`.

So minimum is:

`2`.

## Two variables

Find the minimum of:

`x^2+y^2+2x-4y+7`.

Group:

`x^2+2x + y^2-4y +7`

`=(x+1)^2-1 +(y-2)^2-4+7`

`=(x+1)^2+(y-2)^2+2`.

Minimum is 2 at:

`x=-1`, `y=2`.

## PYQ CONNECTION

`NMTC-BH-P-2018-Q13` supports completing-square optimization.

---

# 7. Zero sum of squares is stronger than a normal bound

For real numbers:

`A^2>=0`, `B^2>=0`.

If:

`A^2+B^2=0`,

then neither square can be positive.

Therefore:

`A=0`, `B=0`.

## Example

If:

`(x-4)^2+(y+3)^2=0`,

then:

`x=4`, `y=-3`.

No further solving is needed.

## Why this matters in NMTC

A problem may display enormous powers in the target, but the constraints may first force two variables to exact values or opposites.

## PYQ CONNECTION

`NMTC-BH-P-2025-Q16` collapses to a sum of squares equal to zero; the huge odd powers become easy only after this move.

---

# 8. Discriminant is not only for solving quadratics

For:

`ax^2+bx+c=0`,

real roots require:

`D=b^2-4ac >=0`.

Repeated real root requires:

`D=0`.

## Parameter example

For what `k` does:

`x^2-4x+k=0`

have real roots?

`D=16-4k >=0`.

So:

`k<=4`.

No explicit roots were required.

## Integer filtering

If a Diophantine relation is quadratic in `x`, you can require the discriminant to be:

- non-negative;
- often a perfect square.

That can drastically reduce possible integer parameters.

## PYQ CONNECTION

`NMTC-BH-P-2023-Q13` uses discriminant feasibility in an integer-solution problem.

---

# 9. Absolute value is distance

`|x-a|` means distance from `x` to `a` on the number line.

## Inside

`|x-a|<r`

means distance from `a` is less than `r`:

`a-r < x < a+r`.

## Outside

`|x-a|>r`

means:

`x<a-r` or `x>a+r`.

### Example

`|x-5|<2`

gives:

`3<x<7`.

### Strict vs non-strict

- `<` excludes endpoints;
- `<=` includes endpoints;
- `>` excludes boundary points;
- `>=` includes boundary points.

---

# 10. Absolute value in a denominator: domain first

Solve:

`2/|x-13| > 8/9`.

First:

`x!=13`.

Since denominator magnitude is positive away from 13:

`18 > 8|x-13|`

so:

`|x-13| < 9/4`.

Therefore:

`43/4 < x < 61/4`, with `x!=13`.

If the problem asks for integer solutions:

`11,12,14,15`.

There are 4.

## PYQ CONNECTION

`NMTC-BH-P-2025-Q10` is a clean Preliminary anchor for this exact workflow.

---

# 11. Rational inequalities need sign analysis

Solve:

`(x-3)/(x+2) >=0`.

Critical points:

- numerator zero: `x=3`;
- denominator zero: `x=-2` (excluded).

Intervals:

`(-infinity,-2)`, `(-2,3)`, `(3,infinity)`.

Test signs:

- left interval: positive;
- middle: negative;
- right: positive.

Because inequality is `>=0`, include numerator zero `3`.

Never include denominator zero `-2`.

Solution:

`(-infinity,-2) union [3,infinity)`.

## Why not cross-multiply blindly?

Multiplying by `x+2` would require knowing its sign. If it is negative, the inequality direction reverses.

A sign chart avoids that trap.

---

# 12. Integer/natural filtering comes last

Suppose you solve two inequalities and obtain:

`0.7 < x < 2.3`.

If the problem asks for natural numbers, only after the real intersection do you list:

`x=1,2`.

Do not round endpoints or test integers before the correct interval is known.

## PYQ CONNECTION

`NMTC-BH-P-2023-Q28` supports this interval-then-natural-number workflow.

---

# 13. Direct bounds: isolate the bounded piece

For all real `x`:

`-1<=cos x<=1`.

So:

`|2cos x|<=2`.

If another part of an expression is exactly known, do not overwork the bounded piece.

## Example

Suppose an odd function satisfies:

`f(-4)=18`.

Then:

`f(4)=-18`.

Therefore:

`|f(4)|=18`.

So:

`|f(4)|+|2cos x| <=20`.

## PYQ CONNECTION

`NMTC-BH-P-2024-Q30` combines odd symmetry with a direct trigonometric bound.

---

# 14. Equality condition can fail even when the inequality is correct

Suppose an inequality proves:

`F(x,y)>=10`.

That does **not** automatically mean the minimum is 10.

You must check whether the equality conditions are compatible with:

- positivity;
- integrality;
- another equation;
- geometric constraints;
- excluded values.

If equality is impossible, 10 is only a lower bound, not an attained minimum.

This distinction is essential in contest problems.

---

# 15. Source integrity is part of mathematical checking

Suppose a printed problem asks for a **maximum** under `ab=1`, `a,b>0`, while an answer key gives `2`.

The mathematics says:

- 2 is the minimum of `a+b`;
- no maximum exists.

Correct action:

1. preserve the printed wording;
2. solve it independently;
3. record `SOURCE_CONFLICT`;
4. do not silently replace “maximum” by “minimum”.

This is exactly why our PYQ corpus separates clean anchors from conflicts.

---

# 16. FIRST-MOVE LAB — do not solve

Choose:

`BD / AM / CY / CS / ZZ / DR / AV / RI / IC / DB / QC`.

1. `ab=4`, ask maximum `a+b`, `a,b>0`.
2. `x+y=20`, ask maximum `xy`.
3. `1/a+4/b=1`, ask minimum `a+b`.
4. `x^2-10x+29`, ask minimum.
5. `(x-2)^2+(y+5)^2=0`.
6. parameter quadratic must have real roots.
7. `|x-7|<3`.
8. `(x-1)/(x+4)<0`.
9. inequality solved; now asks number of integer solutions.
10. expression includes `3cos t` and all other terms are exact.
11. supplied answer claims a maximum but an escaping family exists.

### Key

1 `BD`; 2 `AM`; 3 `CY`; 4 `CS`; 5 `ZZ`; 6 `DR`; 7 `AV`; 8 `RI`; 9 `IC`; 10 `DB`; 11 `QC/BD`.

---

# 17. Mixed self-test

## Q1
Positive `a,b` satisfy `ab=16`. Find minimum `a+b` and state whether a maximum exists.

**Answer:** minimum 8 at `a=b=4`; no maximum.

## Q2
Positive `x,y` satisfy `x+y=18`. Find maximum `xy`.

**Answer:** `81` at `x=y=9`.

## Q3
Find minimum:

`x^2+y^2-4x+6y+20`.

**Answer:** `(x-2)^2+(y+3)^2+7`, minimum `7`.

## Q4
Solve:

`|x-3|>=5`.

**Answer:** `x<=-2` or `x>=8`.

## Q5
Solve:

`(x-2)/(x+1)<0`.

**Answer:** `-1<x<2`.

## Q6
For what `k` does `x^2+kx+9=0` have a repeated real root?

**Answer:** `k=±6`.

## Q7
Positive `a,b` satisfy `1/a+9/b=1`. What is the least possible `a+b`?

**Answer:** `16`.

## Q8
A printed item says “maximum of `a+b` when `ab=1`, `a,b>0`” and a key says 2. What should you report?

**Answer:** printed problem has no maximum; 2 is the minimum; flag source/key conflict.

---

# 18. Adoption checklist

You are not done merely because you can quote AM-GM.

You should be able to answer **yes** to all:

- Can I test boundedness before selecting an inequality?
- Can I distinguish minimum from maximum direction?
- Can I derive two-variable AM-GM from a square?
- Can I state and verify equality conditions?
- Can I recognize a reciprocal/Cauchy structure?
- Can I complete a square without sign errors?
- Can I use `D>=0` as a feasibility filter?
- Can I solve absolute inequalities as distance problems?
- Can I exclude denominator zeros?
- Can I solve the real interval before counting integers?
- Can I flag a source conflict instead of forcing a key?

If not, return to the first failed question rather than doing more random practice.

## Draft status

`MATH_PASS: v0.1`

`CLASSROOM_TIMING: NOT_RUN`

`FINAL_EDITORIAL_RENDER_QA: NOT_RUN`
