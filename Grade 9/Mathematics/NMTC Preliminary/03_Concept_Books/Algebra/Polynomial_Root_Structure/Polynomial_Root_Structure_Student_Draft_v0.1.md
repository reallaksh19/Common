# Polynomial & Root Structure
## NMTC Bhaskara Preliminary — Student Concept Book Draft v0.1

> **Goal:** learn to see what a polynomial problem is *really asking* before you calculate.

This is not a formula sheet.

You will repeatedly use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

and, while solving:

`RECOGNIZE -> FIRST MOVE -> SOLVE -> CHECK -> TRANSFER`

---

# 0. Before you begin — 8-question diagnostic

Do these without notes.

1. Factor `x^2-7x+12`.
2. Expand `(x+2)^3`.
3. If `x^2=3x-2`, express `x^3` in the form `ax+b`.
4. Find `P(2)` for `P(x)=x^3-4x+1`.
5. Solve `x^2-5x+6=0`.
6. If two numbers have sum 7 and product 10, what are they?
7. What is the zero of `2x-6`?
8. Is `x^2+1=0` possible for real `x`?

### Diagnostic answers

1. `(x-3)(x-4)`
2. `x^3+6x^2+12x+8`
3. `x^3=x(3x-2)=3x^2-2x=3(3x-2)-2x=7x-6`
4. `8-8+1=1`
5. `x=2,3`
6. `2,5`
7. `x=3`
8. No, because `x^2>=0` for real `x`.

If you missed 3 or more, repair basic factorization/equation skills first.

---

# 1. One polynomial can wear different clothes

## SEE

Look at these three lines:

`P(x)=x^2-5x+6`

`P(x)=(x-2)(x-3)`

`roots: 2 and 3`

They describe the same polynomial information in different forms.

Which form is best for each job?

- Find `P(10)`?
- Find the roots?
- Find the sum of the roots?
- See immediately whether `x=2` makes the polynomial zero?

## REALIZE

A strong Preliminary solver does not ask:

> “Which formula belongs to this chapter?”

They ask:

> “Which representation makes this question smallest?”

That question will appear throughout this book.

## UNDERSTAND

From

`P(x)=a(x-alpha)(x-beta)`

we can see three kinds of information at once:

- `a,b,c` tell us coefficient structure;
- `alpha,beta` tell us roots;
- the factors tell us when the polynomial vanishes.

### Contrast

If `P(2)=0`, then `x-2` is a factor.

If `P(2)=5`, then 5 is only the remainder when dividing by `x-2`. It does **not** tell us that `x-5` is a factor.

## ADOPT — first move only

For each, do **not solve**. Write the best representation.

A. `x^2-11x+30`

B. a quadratic with roots `alpha,beta`, asking for `alpha^2+beta^2`

C. a polynomial divided by `x-7`

D. a polynomial divisible by `x^2+1`

### Check

A. factor/root view is promising;
B. root sum/product view;
C. evaluation at `x=7`;
D. remainder modulo a quadratic, not one-number substitution.

---

# 2. High powers often mean: reduce, do not solve

## SEE

Suppose

`x^2+x+1=0`.

Then immediately:

`x^2=-x-1`.

Now multiply by `x`:

`x^3=-x^2-x`.

Replace `x^2` again:

`x^3=-(-x-1)-x=1`.

So suddenly:

`x^3=1`, `x^4=x`, `x^5=x^2`, `x^6=1`, ...

A frightening `x^100` is no longer frightening.

## REALIZE

The equation is not merely something to solve.

It is a **rewriting machine**.

Whenever you see `x^2`, you may replace it with `-x-1`.

## UNDERSTAND

If `x` satisfies a quadratic relation, then every high power can be reduced until only `1` and `x` remain.

This is why a Preliminary question can contain huge powers but require only a few lines.

### Worked example

If

`x^2=2x+3`,

find `x^4` in the form `ax+b`.

First:

`x^3=x(2x+3)=2x^2+3x`

`=2(2x+3)+3x=7x+6`.

Then:

`x^4=x(7x+6)=7x^2+6x`

`=7(2x+3)+6x`

`=20x+21`.

No roots were needed.

## WHY NOT? — the tempting wrong method

You could solve `x^2=2x+3` first.

But then you create two roots and substitute each into high powers. That is more work and more opportunity for error.

The question asks for information that the relation itself already controls.

## PYQ CONNECTION

This first move is directly supported by qualified Preliminary items:

- `NMTC-BH-P-2018-Q06`;
- `NMTC-BH-P-2023-Q03`;
- `NMTC-BH-P-2024-Q01`.

The exact paper wording is kept in source custody; the mathematical lesson here is **power reduction before explicit root solving**.

## ADOPT

### A. Direct
If `t^2=t+1`, express `t^5` as `at+b`.

### B. Disguised
If `u+1/u=3`, find `u^2+1/u^2`.

### C. Transfer
If `z^2-2z+2=0`, build a cycle or recurrence for `z^n` and decide the cheapest way to simplify `z^8`.

### Answers

A. `t^3=2t+1`, `t^4=3t+2`, `t^5=5t+3`.

B. `(u+1/u)^2=u^2+2+1/u^2=9`, so answer `7`.

C. One route: `z^2=2z-2`; reduce repeatedly. Another useful observation is that the roots have a simple complex structure, but explicit complex roots are unnecessary for a Preliminary reduction problem.

---

# 3. Remainder Theorem — understand why it works

## SEE

Ordinary integer division:

`17 = 5·3 + 2`.

The 2 is what remains.

Polynomial division has the same structure:

`P(x)=(x-a)Q(x)+r`.

Here `r` is a constant remainder because the divisor has degree 1.

Now substitute `x=a`:

`P(a)=(a-a)Q(a)+r=r`.

## REALIZE

Substitution works because the divisor becomes zero.

That is the whole theorem.

## UNDERSTAND

### Remainder Theorem
When `P(x)` is divided by `x-a`, the remainder is `P(a)`.

### Factor Theorem
If `P(a)=0`, then the remainder is zero, so `x-a` divides `P(x)`.

Factor Theorem is not a separate magic trick. It is the zero-remainder case.

## Contrast — a common trap

Divisor: `2x-6`.

Its zero is not 6.

Solve:

`2x-6=0` -> `x=3`.

So the relevant substitution is `x=3`.

Never use the false rule:

> “Plug in the constant from the divisor.”

Use the correct rule:

> “Plug in the **zero of the divisor**.”

## Worked example

Find the remainder when

`P(x)=x^3+2x^2-5x+7`

is divided by `x-2`.

`P(2)=8+8-10+7=13`.

Remainder = `13`.

## ADOPT

1. Find the remainder of `x^4+3x-2` on division by `x+1`.
2. What condition on `k` makes `x-3` a factor of `x^3+kx-12`?
3. For divisor `3x-6`, which number should you substitute?

### Answers

1. substitute `x=-1`: `1-3-2=-4`.
2. `27+3k-12=0`, so `k=-5`.
3. `x=2`.

---

# 4. Quadratic divisors: think in remainders, not one substitution

## SEE

Suppose we divide by `x^2-1`.

Because

`x^2-1=0`

inside remainder calculations, we may write

`x^2 ≡ 1`.

Then:

`x^3 ≡ x`

`x^4 ≡ 1`

`x^5 ≡ x`.

So a huge polynomial collapses to the form

`ax+b`.

## REALIZE

A divisor of degree 2 leaves a remainder of degree at most 1.

Therefore one number is not enough to describe the remainder.

This is why `P(a)` alone is not a complete method for a general quadratic divisor.

## UNDERSTAND — three useful cycles

### Modulo `x^2-1`

`x^2≡1`.

Even powers -> 1.

Odd powers -> `x`.

### Modulo `x^2+1`

`x^2≡-1`.

Powers cycle:

`x, -1, -x, 1, ...`

### Modulo `x^2+x+1`

`x^2≡-x-1`.

Multiplying by `x` gives

`x^3≡1`.

Again a short cycle appears.

## PYQ CONNECTION

Qualified scored anchors include:

- `NMTC-BH-P-2019-Q08`;
- `NMTC-BH-P-2024-Q05`;
- `NMTC-BH-P-2024-Q16`.

## Worked example

Find the remainder of

`x^11+2x^5+7`

when divided by `x^2+1`.

Since `x^2≡-1`:

`x^4≡1`.

`x^11=x^(8+3)≡x^3≡-x`.

`x^5=x^(4+1)≡x`.

So remainder:

`-x+2x+7=x+7`.

## ADOPT

1. Find the remainder of `x^100+x^7+1` modulo `x^2-1`.
2. Find the remainder of `x^20+x^3` modulo `x^2+1`.
3. Derive the power cycle modulo `x^2+x+1` yourself.

### Answers

1. `1+x+1=x+2`.
2. `x^20≡1`, `x^3≡-x`, so `1-x`.
3. `x^3≡1`; cycle repeats every 3 powers.

---

# 5. Vieta — the roots may be ugly, but their relationships are simple

## SEE

Take

`x^2-7x+10=0`.

Roots are 2 and 5.

Notice:

`2+5=7`

`2·5=10`.

Now consider

`3x^2+11x-8=0`.

The roots may not be pleasant to find mentally.

But their sum and product are still immediately available.

## REALIZE

The coefficients already contain useful information about the roots.

You often do **not** need the roots themselves.

## UNDERSTAND — rebuild Vieta

If roots are `alpha,beta`, then

`a(x-alpha)(x-beta)`

`=a[x^2-(alpha+beta)x+alpha beta]`.

Compare with

`ax^2+bx+c`.

Therefore:

`alpha+beta=-b/a`

and

`alpha beta=c/a`.

Do not memorize these without remembering where the signs came from.

## FIRST MOVE TEST

Suppose the target is:

`alpha^2+beta^2`.

Do you need `alpha` and `beta` separately?

No.

Use:

`alpha^2+beta^2=(alpha+beta)^2-2alpha beta`.

### Another

`1/alpha+1/beta=(alpha+beta)/(alpha beta)`.

### Another

`alpha/beta+beta/alpha`

`=(alpha^2+beta^2)/(alpha beta)`

`=((alpha+beta)^2-2alpha beta)/(alpha beta)`.

## PYQ CONNECTION

`NMTC-BH-P-2024-Q14` is a strong qualified anchor: after recovering the correct quadratic information, the efficient route is Vieta on a transformed-root ratio—not explicit solution of the roots.

## Contrast

### Question A
Find the larger root.

You probably need individual roots.

### Question B
Find `alpha^2+beta^2`.

You probably do not.

Mastery means seeing that difference quickly.

## ADOPT

For `2x^2-9x+3=0` with roots `alpha,beta`, find without solving the roots:

1. `alpha+beta`
2. `alpha beta`
3. `alpha^2+beta^2`
4. `1/alpha+1/beta`

### Answers

1. `9/2`
2. `3/2`
3. `(9/2)^2-3=69/4`
4. `(9/2)/(3/2)=3`

---

# 6. Transformed roots: change the information, not necessarily the roots

## SEE

Suppose `alpha,beta` are roots of a quadratic.

What if a new equation has roots:

`alpha+1, beta+1`?

Do we need to find `alpha,beta` first?

No.

New sum:

`(alpha+1)+(beta+1)=(alpha+beta)+2`.

New product:

`(alpha+1)(beta+1)=alpha beta+(alpha+beta)+1`.

That is enough to build the new quadratic.

## REALIZE

A transformed-root problem is often still a sum/product problem.

## UNDERSTAND

### Reciprocal roots

New roots:

`1/alpha,1/beta`.

New sum:

`(alpha+beta)/(alpha beta)`.

New product:

`1/(alpha beta)`.

### Squared roots

New sum:

`alpha^2+beta^2`.

New product:

`alpha^2 beta^2=(alpha beta)^2`.

### Shifted function input

If you know information about `f(x+1)`, sometimes it is cleaner to set

`y=x+1`.

Now rewrite the function in `y` before discussing roots.

## PYQ CONNECTION

- `NMTC-BH-P-2024-Q22` supports “shift first, then use root structure.”

## ADOPT

Let roots of `x^2-6x+5=0` be `alpha,beta`.

Form the monic quadratic whose roots are:

1. `alpha+2,beta+2`;
2. `1/alpha,1/beta`.

### Answers

Original sum `6`, product `5`.

1. new sum `10`; new product `5+12+4=21`; equation `x^2-10x+21=0`.
2. new sum `6/5`; product `1/5`; multiply through by 5: `5x^2-6x+1=0`.

---

# 7. Positive or integer roots give extra structure

## SEE

Compare:

> A polynomial has four real roots.

with

> A polynomial has four **positive** roots whose sum is 4 and product is 1.

The second statement is much stronger.

By AM-GM:

`(r1+r2+r3+r4)/4 >= (r1r2r3r4)^(1/4)`.

Both sides are 1.

Equality occurs only when

`r1=r2=r3=r4=1`.

## REALIZE

Positivity/integrality is not decoration. It can determine the roots without solving the polynomial.

## UNDERSTAND

### Positive roots
Use:

- AM-GM equality;
- sum/product bounds;
- sign restrictions.

### Integer roots
Use:

- factor pairs of the constant term;
- integer partitions of the root sum;
- parity/divisibility;
- discriminant-square conditions.

## PYQ CONNECTION

- `NMTC-BH-P-2024-Q17` is a clean equality-collapse anchor.
- `NMTC-BH-P-2023-Q13` is a nearby integer/discriminant bridge.

## Very important contrast — bounded or unbounded?

The words “maximum” or “minimum” do not guarantee that a finite maximum/minimum exists.

`NMTC-BH-P-2023-Q17` is valuable because the correct first move is to test boundedness. The requested maximum is unbounded.

Always ask:

> “Can I make this expression grow without limit while preserving the constraint?”

before applying an inequality mechanically.

---

# 8. Cubic and quartic: do not panic at the degree

## SEE

Consider

`x^4+x^3-7x^2-x+6`.

Before searching for a quartic formula, test small integers.

At `x=1`:

`1+1-7-1+6=0`.

So `x-1` is a factor.

The degree drops immediately.

## REALIZE

In Preliminary mathematics, a higher-degree equation is often testing **structure recognition**, not your knowledge of general high-degree formulas.

## UNDERSTAND — first-move ladder

When you see a cubic/quartic, ask in this order:

1. Can I factor a visible identity?
2. Are `±1` or small factor candidates roots?
3. Is it really quadratic in `x^2`?
4. Is it symmetric/reciprocal?
5. Are roots restricted to integers/positive numbers?
6. Can a given relation reduce the degree?

Only after these should you consider heavier methods.

## PYQ CONNECTION

- `NMTC-BH-P-2019-Q25` — high-degree symmetric reduction;
- `NMTC-BH-P-2024-Q24` — simple-root factorization before residual quadratic.

## ADOPT

For each, write the **first move only**.

A. `x^4-5x^2+4=0`

B. `x^4+3x^3-3x-1=0`

C. `x^4+5x^3+6x^2+5x+1=0`

Suggested recognition:

A. set `t=x^2` / factor `(x^2-1)(x^2-4)`.

B. test `x=1` and `x=-1`, then factor.

C. reciprocal/palindromic structure suggests divide by `x^2` and try `t=x+1/x` (for `x≠0`).

---

# 9. Common roots: eliminate before solving everything

## SEE

Suppose `r` is a common root of

`r^2+ar+b=0`

and

`r^3+cr+d=0`.

You could solve both equations.

But the first equation already tells you how to replace `r^2`, and therefore `r^3`.

## REALIZE

“Common root” means both equations are true at the same number.

That lets us combine them to eliminate powers or parameters.

## UNDERSTAND

From

`r^2=-ar-b`,

multiply by `r`:

`r^3=-ar^2-br`.

Reduce `r^2` again.

Now insert into the cubic.

A cubic condition may collapse to a linear condition in `r` and the parameters.

## PYQ EVIDENCE

`NMTC-BH-P-2023-Q16` supports this mechanism, but the recovered paper marks it **BONUS**. Therefore it is high-ceiling evidence, not ordinary scored-frequency evidence.

The canonical learning problems for this section should be original author-created scored-level items.

---

# 10. Source integrity is part of mathematics

A strong student does not force an answer key to be correct.

Suppose your derivation from a printed problem gives one result, but the supplied key gives another.

Do this:

1. re-check your algebra;
2. re-check domains and conventions;
3. compare the exact printed signs/words;
4. if the conflict remains, mark the source as unresolved.

Do **not** silently change the problem to match the key.

## Real corpus lesson

`NMTC-BH-P-2025-Q20` has a reproduced sign/key conflict. The positive-integer root structure fixes the likely coefficient relation, but the printed sign and provisional key do not agree.

For this book it is therefore a **source-QC contrast**, not a normal PYQ exercise.

This is what mathematically responsible preparation looks like.

---

# 11. FIRST-MOVE LAB — no solving allowed

Write only one label for each prompt:

`POWER REDUCTION / VIETA / REMAINDER / FACTOR FIRST / INTEGER ROOTS / COMMON ROOT / SHIFT / BOUND CHECK`

1. A root satisfies `x^2=4x-1`; target contains `x^12`.
2. Roots `alpha,beta`; target is `1/alpha+1/beta`.
3. A polynomial is divisible by `x^2+1`.
4. A quartic has constant term 6 and small integer coefficients.
5. Four positive roots have sum and product fixed.
6. Two polynomials share a root.
7. Roots of `f(x+3)` are requested.
8. A problem asks for a “maximum” under a reciprocal product constraint.

### Classification

1. POWER REDUCTION
2. VIETA
3. REMAINDER
4. FACTOR FIRST
5. INTEGER ROOTS / equality structure
6. COMMON ROOT
7. SHIFT
8. BOUND CHECK

If you needed to calculate to choose the label, repeat the recognition cards.

---

# 12. Mixed self-test

## Q1
If `x^2-3x+1=0`, find `x^3+1/x^3` without solving for `x`.

## Q2
For roots `alpha,beta` of `3x^2-10x+2=0`, find `alpha^2+beta^2`.

## Q3
Find the remainder of `x^25+x^4+3` on division by `x^2+1`.

## Q4
A monic quadratic has roots `alpha,beta` with `alpha+beta=8`, `alpha beta=12`. Form the equation whose roots are `alpha+1,beta+1`.

## Q5
A quartic has four positive roots, sum 8 and product 16. What equality pattern should you test first?

## Q6
A polynomial is divisible by `2x-5`. Which value should be substituted to test the linear factor?

## Q7
A cubic with integer coefficients has integer roots and constant term `-6`. Name the small root candidates worth testing before any cubic formula.

## Q8
Two polynomials share root `r`; one gives a formula for `r^2`. What should you do before solving either polynomial completely?

---

# 13. Self-test answers and checks

## A1
From `x^2-3x+1=0`, divide by `x` (`x≠0`):

`x+1/x=3`.

Then

`x^3+1/x^3=(x+1/x)^3-3(x+1/x)=27-9=18`.

## A2
Sum `=10/3`, product `=2/3`.

`alpha^2+beta^2=100/9-4/3=88/9`.

## A3
Modulo `x^2+1`, powers cycle every 4.

`x^25≡x`, `x^4≡1`.

Remainder `x+4`.

## A4
New sum `10`.

New product `12+8+1=21`.

Equation `x^2-10x+21=0`.

## A5
AM-GM:

average root `=2`, geometric mean `=2`; equality suggests all four roots equal 2.

## A6
Zero of `2x-5` is `x=5/2`.

## A7
Candidates divide 6:

`±1,±2,±3,±6`.

Not all will work; they are first tests.

## A8
Use the `r^2` relation to reduce higher powers in the other polynomial, then eliminate.

---

# 14. Mastery checklist

You are ready to leave this unit only if you can say YES to all:

- [ ] I can explain why Remainder Theorem works.
- [ ] I can rebuild Vieta from factor form.
- [ ] I know when **not** to solve a quadratic.
- [ ] I can reduce high powers using a low-degree relation.
- [ ] I can reduce powers modulo `x^2-1`, `x^2+1`, and derive a new cycle myself.
- [ ] I can form equations for shifted/reciprocal roots.
- [ ] I test simple factorization before treating a cubic/quartic as “hard.”
- [ ] I use integer/positive-root restrictions as information.
- [ ] I test whether an optimization is bounded.
- [ ] I can recognize a source/key conflict without silently repairing it.
- [ ] On an unlabeled mixed set, I can choose the correct first move before calculating.

## Current draft status

`STUDENT_DRAFT_v0.1`

Still required before publication:

- larger F0–F4 exercise bank;
- non-identical transfer set with fully reviewed solutions;
- timed recognition sheet;
- mastery test with error-tag diagnostics;
- typography/PDF rendering QA;
- final source/provenance appendix.
