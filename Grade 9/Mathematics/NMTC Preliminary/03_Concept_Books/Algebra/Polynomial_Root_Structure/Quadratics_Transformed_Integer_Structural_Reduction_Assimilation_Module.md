# Quadratics - Transformed Roots, Integer Roots & Structural Reduction
## Assimilation Module - NMTC Preliminary / Grade IX-X

### Who this module is for

You can probably solve a routine quadratic. You may also remember the sum and product of roots. The missing connection is often this:

> **A quadratic contains more information than its two individual roots.**

In this unit you will learn to use that information before you calculate.

The three habits are:

1. **Transformed roots:** transform the **sum and product** first.
2. **Restricted roots:** translate every adjective - real, positive, integer - into a mathematical condition.
3. **High powers:** use the quadratic relation as a **rewriting machine** before solving for the root.

Learning sequence:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

### Attempt-before-hint contract

Every practice item starts at **H0**: attempt the first useful line without help. If you are stuck, reveal only the listed support for that item. Across each ladder the maximum support fades from `H3 -> H2 -> H1 -> H0`.

- `H3 EXECUTION` - one first algebraic relation.
- `H2 STRUCTURE` - the representation or invariant to use.
- `H1 RECOGNITION` - only the clue to notice.
- `H0 INDEPENDENT` - no hint.

### Non-negotiable first-line rule

Before any long calculation, write one of these as appropriate:

- the transformed sum and product;
- the sign/integer constraints;
- the quadratic rewriting rule or recurrence.

Do **not** start by solving the quadratic unless the target actually needs individual roots.

---

# 0. RECONNECT - what do you already own?

Do not solve fully. Write only the **first useful line**.

1. The roots of a quadratic have sum \(9\) and product \(14\). A new equation has roots \(\alpha+2,eta+2\). What two quantities would you compute first?
2. Two real roots have positive product. What does that tell you - and what does it **not** yet tell you?
3. A monic quadratic has positive integer roots and constant term \(24\). What discrete information is immediately available?
4. A number \(x\) satisfies \(x^2=2x+3\). If the target is \(x^{12}\), what relation should you use before considering the quadratic formula?
5. If \(f(r)=0\), what are the roots in \(x\) of \(f(x+3)=0\)?
6. A printed source statement and its provisional key disagree after a correct derivation. Should you alter the printed sign to make them agree?

If 1 is difficult, the transformed-invariant bridge is missing. If 2-3 are difficult, the restriction bridge is missing. If 4 is difficult, the rewriting-machine bridge is missing. If 5 is difficult, the shift-direction boundary is missing. If 6 is difficult, source integrity needs attention.

---

# 1. STRAND A - transformed roots without solving the original roots

## RECONNECT

Take the familiar quadratic

\[
x^2-7x+10=0.
\]

Its roots are \(2\) and \(5\). Suppose a new equation must have roots \(2+3\) and \(5+3\), namely \(5\) and \(8\).

The new roots have

\[
\text{sum}=13,\qquad \text{product}=40.
\]

The new monic quadratic is therefore

\[
y^2-13y+40=0.
\]

Nothing surprising happened because the original roots were easy. Now hide the roots and keep only what the quadratic already stores:

\[
S=\alpha+\beta,\qquad P=\alpha\beta.
\]

The same transformation can be done without finding \(\alpha\) or \(eta\).

## DISCOVER - shift the pair, not the individual roots

If the new roots are \(\alpha+h\) and \(eta+h\), then their sum is

\[
(\alpha+h)+(\beta+h)=S+2h.
\]

Their product is

\[
(\alpha+h)(\beta+h)=P+hS+h^2.
\]

So the useful information after a shift is

\[
S'=S+2h,\qquad P'=P+hS+h^2.
\]

Only after those two lines do we form

\[
y^2-S'y+P'=0.
\]

### Expert noticing

The target asks for a **new quadratic**, not for \(\alpha\) and \(eta\) separately. That is the clue that transformed sum/product should come before explicit roots.

## MAKE SENSE - reciprocals

Suppose the new roots are

\[
\frac1\alpha,\qquad \frac1\beta.
\]

First check the domain: neither original root may be \(0\), so

\[
P=\alpha\beta\ne0.
\]

Then

\[
S'=\frac1\alpha+\frac1\beta
   =\frac{\alpha+\beta}{\alpha\beta}
   =\frac SP,
\]

and

\[
P'=\frac1{\alpha\beta}=\frac1P.
\]

Again, the transformed quadratic follows from \(S',P'\).

## MAKE SENSE - squared roots

If the new roots are \(\alpha^2,eta^2\), then

\[
S'=\alpha^2+\beta^2
=(\alpha+\beta)^2-2\alpha\beta
=S^2-2P,
\]

while

\[
P'=\alpha^2\beta^2=P^2.
\]

The pattern is now visible:

> **Transform the pair information first; solve individual roots only if the target demands them.**

---

## DECISION BOUNDARY 1 - transformed roots vs shifted function input

These two statements look similar but point in opposite directions.

### A. New roots are \(\alpha+3,eta+3\)

You are directly changing the **root values**. Use transformed \(S',P'\).

### B. Solve \(f(x+3)=0\), where \(f(r)=0\)

Now \(x+3\) must equal an original root \(r\):

\[
x+3=r\quad\Longrightarrow\quad x=r-3.
\]

So the roots of the shifted-input equation move by \(-3\), not \(+3\).

**Repair statement:** changing roots and changing the input are related operations, but they are not the same instruction.

---

## DECISION BOUNDARY 2 - reciprocal roots vs reciprocal sum

- If the task says **form the equation** whose roots are \(1/\alpha,1/\beta\), you need both \(S'\) and \(P'\).
- If the task asks only for \(1/\alpha+1/\beta\), compute only \(S/P\). Building a whole quadratic would create unnecessary work.

The target chooses how much information to construct.

---

## TRY -> DIAGNOSE -> FADE: transformed-root ladder

**For every item:** first write the transformed sum/product or the input-shift relation. Only then continue.

### A1 - maximum support H3

The roots of

\[
x^2-9x+14=0
\]

are \(\alpha,eta\). Form the monic quadratic whose roots are \(\alpha+1,eta+1\).

Attempt H0 first.

If needed, H3: start with

\[
S'=S+2,\qquad P'=P+S+1.
\]

### A2 - maximum support H2

The roots of

\[
2x^2-5x-3=0
\]

are \(\alpha,eta\). Form an integer-coefficient quadratic whose roots are \(1/\alpha,1/\beta\).

Attempt H0 first.

If needed, H2: use the reciprocal transformed sum and product; check \(P\ne0\).

### A3 - maximum support H1

The roots of

\[
x^2-4x-1=0
\]

are \(\alpha,eta\). Form the monic quadratic whose roots are \(\alpha^2,eta^2\).

Attempt H0 first.

If needed, H1: ask whether the individual roots are actually needed.

### A4 - H0 independent contrast

Let

\[
f(t)=t^2-6t+8.
\]

Solve

\[
f(x+3)=0.
\]

Before expanding anything, write the relation between \(x+3\) and an original root of \(f\).

### DIAGNOSE

If A1-A3 led you to the quadratic formula, tag the error `TRANSFORM_SOLVED_ROOTS_UNNECESSARILY`.

If A4 produced roots shifted by \(+3\), tag the error `SHIFT_DIRECTION_ERROR`.

---

## SOURCE MECHANISM NOTE

`NMTC-BH-P-2024-Q22` is a `CLEAN_SCORED_ANCHOR` for the mechanism **shift the argument first, then use root structure**. The historical ID grounds the mechanism; this module does not reproduce the full source item.

---

# 2. STRAND B - positive roots and integer roots are different kinds of information

## RECONNECT - product tells only part of the sign story

Compare the pairs

\[
(2,6)\qquad\text{and}\qquad(-2,-6).
\]

Both pairs have positive product \(12\). So

\[
P>0
\]

does **not** by itself mean the roots are positive. It means the two real roots have the same sign.

Now compare their sums:

\[
2+6=8>0,\qquad -2-6=-8<0.
\]

For two **real** roots:

- \(P>0\) -> same sign;
- \(S>0\) then selects both positive;
- \(S<0\) selects both negative.

The word **real** matters. Sign language is not meaningful if the roots are non-real.

## DISCOVER - positivity is continuous, integrality is discrete

Suppose two positive real roots have sum \(10\) and product \(21\). Many real-number arguments are possible, but the pair is already fixed by the quadratic

\[
t^2-10t+21=0.
\]

Now add one word: **integer**.

If the roots are positive integers with product \(21\), only the positive factor pairs are possible:

\[
(1,21),\ (3,7).
\]

The sum condition then selects \((3,7)\).

That is the crucial boundary:

> **positivity gives sign restrictions; integrality turns the search into discrete factor/divisibility cases.**

## MAKE SENSE - factor pairs, parity and divisibility

For a monic quadratic

\[
x^2-Sx+P=0
\]

with integer roots, the roots themselves are integer factor pairs of \(P\) whose sum is \(S\).

Before enumerating every pair, use cheap filters:

- if \(P\) is odd, both integer roots are odd, so their sum is even;
- if \(P\) is even, at least one root is even;
- a divisibility condition such as “one root is a multiple of \(5\)” may leave only a few pairs;
- positivity removes all negative factor pairs.

These are not extra formulas. They are consequences of integer arithmetic.

---

## MAKE SENSE - equality can collapse the search

For positive roots \(\alpha,eta\), AM-GM gives

\[
\frac{\alpha+\beta}{2}\ge\sqrt{\alpha\beta}.
\]

Equivalently,

\[
S\ge2\sqrt P.
\]

Equality occurs only when

\[
\alpha=\beta.
\]

So if the given data sit exactly on the equality boundary, do **not** start listing factor pairs. The roots are forced equal immediately.

---

## DECISION BOUNDARY 3 - positive real vs positive integer roots

### A. Positive real roots

Translate first to:

1. roots are real;
2. \(S>0\);
3. \(P>0\).

For a parameterized quadratic, the reality condition may come from the discriminant.

### B. Positive integer roots

All of the above may matter, but integrality adds:

- factor-pair restrictions;
- parity;
- divisibility;
- finite case checking.

**Repair statement:** positive and integer are independent constraints. Never use one as a substitute for the other.

---

## DECISION BOUNDARY 4 - equality collapse vs ordinary enumeration

### A. Positive roots with \(S^2=4P\)

The equality boundary forces equal roots.

### B. Positive integer roots away from the equality boundary

Use factor pairs and discrete filters.

**Repair statement:** test a structural equality before doing casework.

---

## TRY -> DIAGNOSE -> FADE: positive/integer-root ladder

**For every item:** before solving, write whether the problem needs sign/reality information, integer factor-pair information, or an equality test.

### B1 - maximum support H3

A monic quadratic has positive integer roots with sum \(10\) and product \(21\). Find the roots and write the quadratic.

Attempt H0 first.

If needed, H3: list positive factor pairs of \(21\) and test their sums.

### B2 - maximum support H2

The quadratic

\[
x^2-kx+24=0
\]

has positive integer roots differing by \(2\). Find \(k\).

Attempt H0 first.

If needed, H2: the roots are a positive factor pair of \(24\).

### B3 - maximum support H1

The quadratic

\[
x^2-sx+25=0
\]

has positive real roots. Find the smallest possible real value of \(s\).

Attempt H0 first.

If needed, H1: identify the equality boundary for two positive numbers with fixed product.

### B4 - H0 independent

The quadratic

\[
x^2-nx+12=0
\]

has positive integer roots. Find all possible integer values of \(n\).

### DIAGNOSE

If you used only \(P>0\) to claim positivity, tag `POSITIVE_PRODUCT_ONLY`.

If you treated B2 or B4 as unrestricted real-root problems, tag `INTEGRALITY_IGNORED`.

If you enumerated many cases in B3 before testing equality, tag `EQUALITY_BOUNDARY_MISSED`.

---

## SOURCE MECHANISM NOTE

- `NMTC-BH-P-2024-Q17` is a `CLEAN_SCORED_ANCHOR` for positive-root/equality-collapse structure.
- `NMTC-BH-P-2023-Q13` is `BRIDGE_EVIDENCE` for admissible integer/discriminant case reasoning. It supports the transition but must not be inflated into exact recurrence evidence for this entire strand.

---

# 3. STRAND C - a quadratic relation is a rewriting machine

## RECONNECT

Suppose a number \(x\) satisfies

\[
x^2=2x+3.
\]

If the question asks for the roots of \(x^2-2x-3=0\), solving is reasonable.

But suppose the question asks for \(x^6\). The equation gives a cheaper piece of information:

> every time \(x^2\) appears, replace it by \(2x+3\).

Watch what happens:

\[
x^3=x(2x+3)=2x^2+3x=7x+6.
\]

The degree has collapsed back to \(1\).

Then

\[
x^4=x(7x+6)=7x^2+6x=20x+21.
\]

The relation is functioning as a **rewriting machine**, not merely an equation to solve.

## DISCOVER - derive the recurrence

Let the relation be

\[
x^2=px+q.
\]

Multiply by \(x^{n-2}\) for \(n\ge2\):

\[
x^n=px^{n-1}+qx^{n-2}.
\]

That recurrence shows why every higher power can be reduced to a linear expression

\[
A_nx+B_n.
\]

No radical expressions are needed.

### Expert noticing

The target contains a **high power**, while the given relation has degree \(2\). That gap in degree is the clue: reduce the power before solving for \(x\).

---

## MAKE SENSE - special relations can create cycles

If

\[
x^2+x+1=0,
\]

then

\[
x^2=-x-1.
\]

Multiply by \(x\):

\[
x^3=-x^2-x=1.
\]

Therefore powers repeat every three steps:

\[
x^3=1,\quad x^4=x,\quad x^5=x^2,\quad x^6=1,\ldots
\]

A huge exponent now reduces to a remainder modulo \(3\).

The cycle was **derived** from the quadratic relation; it was not guessed.

---

## MAKE SENSE - reciprocal powers can also recur

Suppose \(u\ne0\) and

\[
u+\frac1u=k.
\]

Define

\[
A_n=u^n+u^{-n}.
\]

Multiply \(A_{n-1}\) by \(k=u+u^{-1}\):

\[
kA_{n-1}
=(u+u^{-1})(u^{n-1}+u^{-(n-1)})
=A_n+A_{n-2}.
\]

So

\[
A_n=kA_{n-1}-A_{n-2}.
\]

This is another low-degree structural reduction. The underlying quadratic for \(u\) exists, but solving it is usually the expensive route.

---

## DECISION BOUNDARY 5 - solve the quadratic vs reduce powers first

### A. Find the larger root of \(x^2-5x+1=0\)

The target distinguishes the roots. Individual roots are relevant.

### B. A root \(x\) satisfies \(x^2-5x+1=0\). Simplify \(x^{20}\) to \(Ax+B\)

The target is a high power under a degree-2 relation. Rewrite first.

**Why explicit solving is inferior in B:** it creates two radical root expressions, raises them to high powers, and introduces work that the recurrence avoids. The relation already contains exactly the information needed.

---

## TRY -> DIAGNOSE -> FADE: structural-reduction ladder

**For every item:** first write the replacement rule or recurrence. Do not begin with the quadratic formula.

### C1 - maximum support H3

If

\[
x^2=3x-2,
\]

express \(x^4\) in the form \(Ax+B\).

Attempt H0 first.

If needed, H3: start with

\[
x^3=x(3x-2)=3x^2-2x
\]

and replace \(x^2\) again.

### C2 - maximum support H2

If

\[
x^2=x+2,
\]

express \(x^6\) in the form \(Ax+B\).

Attempt H0 first.

If needed, H2: keep reducing every \(x^2\) so the expression never needs degree above \(1\).

### C3 - maximum support H1

If

\[
x^2+x+1=0,
\]

simplify \(x^{100}\).

Attempt H0 first.

If needed, H1: look for a short power cycle before repeated multiplication.

### C4 - H0 independent

A nonzero number \(u\) satisfies

\[
u+\frac1u=4.
\]

Without solving for \(u\), find

\[
u^2+\frac1{u^2}
\]

and then

\[
u^3+\frac1{u^3}.
\]

### DIAGNOSE

If your first line in C1-C4 was the quadratic formula, tag `SOLVED_WHEN_REDUCTION_WAS_ENOUGH`.

If you used the relation as though it were true for every possible \(x\), tag `RELATION_TREATED_AS_IDENTITY`. The replacement rule is valid for the specified value/root satisfying the relation.

---

## SOURCE MECHANISM NOTE

Clean scored mechanism anchors for reduction are:

- `NMTC-BH-P-2018-Q06` - quadratic relation -> reduce before solving;
- `NMTC-BH-P-2023-Q03` - reciprocal/low-degree relation -> collapse higher powers;
- `NMTC-BH-P-2024-Q01` - recurrence generated from a relation of the form \(x^2=1-x\).

These IDs ground the mechanism. The practice below is author-created and intentionally uses different surfaces and targets.

---

# 4. DIAGNOSE - six close contrasts

For each pair, write **which first move changes and why**. Do not solve unless needed to justify your choice.

## Contrast 1 - root transform / input shift

A. New roots: \(\alpha+2,eta+2\).

B. New equation: \(f(x+2)=0\).

Boundary: direct root transformation vs variable/input translation.

## Contrast 2 - positive real / positive integer

A. \(x^2-sx+12=0\) has positive real roots.

B. \(x^2-sx+12=0\) has positive integer roots.

Boundary: sign/reality inequalities vs discrete factor pairs.

## Contrast 3 - root requested / high power requested

A. Find the larger root of \(x^2-x-1=0\).

B. A root satisfies \(x^2=x+1\); simplify \(x^{12}\).

Boundary: individual-root information vs rewriting-machine information.

## Contrast 4 - clean source / conflicted source

A. Your derivation agrees with the qualified source key.

B. Your derivation from the printed mathematics disagrees with a provisional key.

Boundary: normal use vs source-conflict classification; never alter the mathematics silently.

## Contrast 5 - reciprocal equation / reciprocal target

A. Form the equation for roots \(1/\alpha,1/\beta\).

B. Find only \(1/\alpha+1/\beta\).

Boundary: build both \(S',P'\) vs compute only the requested invariant.

## Contrast 6 - equality collapse / factor enumeration

A. Positive roots satisfy \(S=2\sqrt P\).

B. Positive integer roots have a non-equality pair of \(S,P\).

Boundary: equality forces equal roots vs ordinary factor-pair search.

---

# 5. ADOPT - recognition-only laboratory

Write only: **clue -> structure -> first line**.

1. “The new roots are each \(4\) more than the old roots.”
2. “The roots of \(f(x-5)=0\) are required.”
3. “Both roots are positive integers.”
4. “The product is positive and the roots are real.”
5. “A root satisfies \(x^2=4x-1\), and the target contains \(x^{25}\).”
6. “\(w+w^{-1}=3\), and the target contains \(w^8+w^{-8}\).”
7. “The transformed roots are reciprocals.”
8. “The printed source sign and the provisional key cannot both be true.”

A concept is not adopted if you can calculate after being told the method but cannot choose the first line here.

---

# 6. TRANSFER - 10 non-identical problems

These are deliberately mixed. No method label is supplied. **Write the first useful line before solving.**

### X1 - compound transformation

The roots of

\[
x^2-7x+10=0
\]

are \(\alpha,eta\). Form an integer-coefficient quadratic whose roots are

\[
\frac1{\alpha+2},\qquad\frac1{\beta+2}.
\]

### X2 - shift, then square

The roots of

\[
x^2-5x+5=0
\]

are \(\alpha,eta\). Form the monic quadratic whose roots are

\[
(\alpha-1)^2,\qquad(\beta-1)^2.
\]

### X3 - domain boundary

The roots of

\[
x^2-4x=0
\]

are \(\alpha,eta\). A student writes down an equation for the reciprocal roots \(1/\alpha,1/\beta\). Explain why that transformation is not valid.

### X4 - parity before enumeration

Can a monic quadratic have positive integer roots with sum \(9\) and product \(15\)? Give a one-line structural reason before listing any factor pairs.

### X5 - divisibility filter

The quadratic

\[
x^2-14x+m=0
\]

has positive integer roots, and at least one root is divisible by \(5\). Find all possible values of \(m\).

### X6 - positive-real boundary

For which real values of \(s\) does

\[
x^2-sx+6=0
\]

have two positive real roots, not necessarily distinct?

### X7 - reduction without roots

A number \(r\) satisfies

\[
r^2-2r+2=0.
\]

Evaluate \(r^4\) without solving for \(r\).

### X8 - recurrence transfer

A number \(x\) satisfies

\[
x^2=1-x.
\]

Express \(x^7\) in the form \(Ax+B\).

### X9 - reciprocal-cycle transfer

A nonzero number \(v\) satisfies

\[
v+\frac1v=1.
\]

Find

\[
v^6+\frac1{v^6}
\]

without solving for \(v\).

### X10 - source integrity

A qualified source record is tagged `SOURCE_CONFLICT_EVIDENCE`. Recalculation from the printed mathematics gives a positive-integer root structure consistent with one coefficient sign, while the provisional key corresponds to the opposite sign. What should a responsible student/editor do with this record?

Do **not** reconstruct or alter the historical question. State the source-handling decision.

---

# 7. SOURCE-QC BOX - NMTC-BH-P-2025-Q20

The repository classifies `NMTC-BH-P-2025-Q20` as `SOURCE_CONFLICT_EVIDENCE` only.

The qualified source record says that the positive-integer structure identifies the relevant root pattern, but the **printed sign and provisional key do not agree**. Therefore:

1. derive from the printed mathematics as printed;
2. compare that derivation with the provisional key;
3. record the exact disagreement;
4. preserve the printed sign - do **not** flip it silently;
5. keep the record as source-QC evidence, not a canonical clean PYQ.

This is a mathematical skill, not merely an editorial rule: a correct derivation does not become wrong because a key says something else.

---

# 8. Six-question assimilation check

For each of the three strands, answer all six questions in your own words.

1. **What did you notice?** What visible clue triggered the structure?
2. **Why does it work?** Can you derive the transformed sum/product, sign restriction, or recurrence?
3. **What clue would make you think of it?** Can you recognize it without a chapter label?
4. **What similar-looking case needs a different method?** State one decision boundary.
5. **Can you write the first two useful lines without help?** No formula sheet.
6. **Can you solve a disguised version?** Use one of X1-X10.

If you fail question 3, the gap is recognition. If you fail question 4, the gap is method selection. If you fail question 5, the gap is first-move execution. If you fail question 6, the gap is transfer.

---

# 9. ADOPT - final internal rules

> **Transformed roots:** I transform \(S,P\) before I solve roots.

> **Restricted roots:** I translate “real,” “positive,” and “integer” separately; integrality adds discrete arithmetic.

> **High powers:** I turn the quadratic into a rewriting rule before I calculate.

> **Source integrity:** if printed mathematics and a key disagree, I recompute and classify the conflict; I do not silently repair the source.
