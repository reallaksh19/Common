# Quadratics — Assimilation Book v2
## NMTC Bhaskara Preliminary / Grade IX-X competitive foundation

### Who this book is for

You probably already know some of the following: factorization, the quadratic formula, the word *discriminant*, and perhaps Vieta's formulas. The problem is usually not that every fact is missing. The problem is that the facts are not yet connected strongly enough to tell you **what to do first** when the question changes shape.

This book repairs those connections.

Learning loop:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Macro mathematics loop:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

---

# 0. Reconnect diagnostic

Do these without notes. Do not worry about speed.

1. Factor `x^2-7x+12`.
2. Solve `x^2-5x+6=0`.
3. For `x^2-7x+10=0`, state the sum and product of the roots.
4. What does `b^2-4ac=0` tell you about the roots of a quadratic?
5. Complete the square: `x^2-6x+5`.
6. If `x^2=x+1`, express `x^3` in the form `ax+b`.
7. Which method would you first test for `alpha^2+beta^2` if `alpha,beta` are roots of a known quadratic?
8. Which method would you first test for the minimum value of `x^2-8x+20`?

### Diagnostic interpretation

- Miss 1-2: repair factorization first.
- Miss 3 or 7: Vieta connection is weak.
- Miss 4: discriminant meaning is weak.
- Miss 5 or 8: graph/vertex representation is weak.
- Miss 6: equation-as-rewriting-rule connection is weak.

The goal is not to label you “weak.” It is to identify which bridge is missing.

---

# 1. One quadratic, several useful views

## RECONNECT

Take

`x^2-5x+6=0`.

You may already know that it factors as

`(x-2)(x-3)=0`.

So the roots are 2 and 3.

## DISCOVER

The same quadratic can be viewed as:

- standard form: `x^2-5x+6`;
- factor form: `(x-2)(x-3)`;
- root information: roots 2 and 3;
- graph: a parabola crossing the x-axis at 2 and 3.

No single form is always best.

## MAKE SENSE

Ask what the question wants.

| Target | Usually useful view |
|---|---|
| roots | factor / formula |
| sum/product of roots | coefficient-root invariants |
| number/nature of real roots | discriminant / graph |
| minimum/maximum value | vertex / completing square |
| high powers under a quadratic relation | reduction / recurrence |

**Internal rule:** *the requested information chooses the representation.*

## CONTRAST PAIR

For `x^2-8x+12=0`:

A. Find the larger root.

B. If roots are `alpha,beta`, find `alpha^2+beta^2`.

Same equation. Different target. A naturally asks for individual roots. B is symmetric and should trigger Vieta first.

## TRY — first move only

For each, write only the first useful move.

1. `x^2-13x+40=0`, find the roots.
2. roots `alpha,beta` of `3x^2-7x+2=0`, find `1/alpha+1/beta`.
3. choose `k` so `x^2+kx+9=0` has equal roots.
4. find the minimum of `x^2-10x+31`.
5. if `x^2=2x+3`, simplify `x^8`.

---

# 2. Discriminant: not a formula fragment, but root geometry

## RECONNECT

You may remember

`D=b^2-4ac`.

But what is it *for*?

## DISCOVER

Compare three parabolas:

- one crosses the x-axis twice;
- one just touches it;
- one misses it.

Those correspond to two, one repeated, or zero real roots.

## REALIZE

The discriminant classifies those cases:

- `D>0`: two distinct real roots;
- `D=0`: one repeated real root;
- `D<0`: no real roots.

## MAKE SENSE

From the quadratic formula

`x=(-b +- sqrt(D))/(2a)`,

the role of `D` becomes visible: the square root determines whether there are two real values, one repeated value, or no real values.

### Repeated root = tangency

If `D=0`, both formula branches give the same root. On the graph, the parabola touches the x-axis at one point.

## CONTRAST PAIR

A. “For what value of `k` does `x^2+kx+9=0` have equal roots?”

First move: `D=0`.

B. “Find the minimum value of `x^2+kx+9` for a given `k`.”

First move: complete the square / vertex view.

**Decision boundary:** root-count language -> discriminant; value-of-expression language -> vertex.

## GUIDED EXAMPLE WITH FADING

Find `k` so `x^2-(k+2)x+9=0` has equal roots.

- H1 recognition: “equal roots” is information about root count.
- H2 structure: use the discriminant.
- H3 execution: `(k+2)^2-36=0`.

Solve: `k+2=+-6`, so `k=4` or `k=-8`.

Now try without hints:

1. `2x^2+kx+8=0` has equal roots. Find `k`.
2. `x^2-6x+m=0` has two distinct real roots. Find the condition on `m`.
3. `x^2+4x+t=0` has no real roots. Find the condition on `t`.

### SOURCE BRIDGE

`NMTC-BH-P-2018-Q07` is bonus evidence for the repeated-root/discriminant first move. Treat it as evidence, not ordinary scored recurrence.

---

# 3. Vieta: relationships without individual roots

## RECONNECT

For

`x^2-7x+10=0`,

roots are 2 and 5.

Notice:

`2+5=7`,

`2*5=10`.

## DISCOVER

Now take

`3x^2+11x-8=0`.

The roots are less pleasant, but their sum and product are still immediately available.

## MAKE SENSE — rebuild, do not memorize

If roots are `alpha,beta`, then

`a(x-alpha)(x-beta)`

expands to

`a[x^2-(alpha+beta)x+alpha beta]`.

Comparing with `ax^2+bx+c` gives

`S=alpha+beta=-b/a`,

`P=alpha beta=c/a`.

The minus sign comes from the factor expansion. If you forget the formula, rebuild it.

## THE SYMMETRY TEST

Before solving roots, ask:

> If I swap alpha and beta, does the target change?

If no, try rewriting in `S` and `P`.

Examples:

`alpha^2+beta^2=S^2-2P`

`alpha^3+beta^3=S^3-3PS`

`1/alpha+1/beta=S/P`

`alpha/beta+beta/alpha=(S^2-2P)/P`

`(alpha-beta)^2=S^2-4P`

## CONTRAST PAIR

A. Find the larger root of `2x^2-9x+3=0`.

B. Find `alpha^2+beta^2` for the same quadratic.

A needs individual-root information. B does not.

## GUIDED EXAMPLE

For `2x^2-9x+3=0`, roots `alpha,beta`, find `alpha^2+beta^2`.

`S=9/2`, `P=3/2`.

Then

`alpha^2+beta^2=S^2-2P=81/4-3=69/4`.

## TRY

1. `x^2-8x+11=0`, find `alpha^2+beta^2`.
2. `3x^2-5x-2=0`, find `1/alpha+1/beta`.
3. `2x^2+x-4=0`, find `(alpha-beta)^2`.
4. `x^2-6x+2=0`, find `alpha^3+beta^3`.

### PYQ MECHANISM GROUNDING

`NMTC-BH-P-2024-Q14` is a clean scored anchor for transformed-root Vieta. Use the mechanism; do not reproduce the full third-party statement here.

---

# 4. Transformed roots: change the information, not necessarily the roots

Suppose original roots are `alpha,beta` with sum `S` and product `P`.

## Shifted roots

New roots: `alpha+h`, `beta+h`.

New sum:

`S'=S+2h`.

New product:

`P'=P+hS+h^2`.

## Reciprocal roots

New roots: `1/alpha`, `1/beta`.

New sum `S'=S/P`, product `P'=1/P`.

## Squared roots

New sum `S'=S^2-2P`, product `P'=P^2`.

## MAKE SENSE

A monic quadratic with roots `u,v` is

`x^2-(u+v)x+uv=0`.

So transformed-root problems are often just “find the new sum and new product.”

## CONTRAST: shifted roots vs shifted input

- “roots become `alpha+2,beta+2`” -> transform root invariants;
- “solve `f(x+2)=0`” -> set a new variable or shift the function input.

Those are related but not identical operations.

## TRY

If roots of `x^2-6x+5=0` are `alpha,beta`, form a quadratic whose roots are:

1. `alpha+2,beta+2`;
2. `1/alpha,1/beta`;
3. `alpha^2,beta^2`.

### PYQ MECHANISM GROUNDING

`NMTC-BH-P-2024-Q22` supports the “shift first, then use root structure” mechanism.

---

# 5. Positive and integer roots are extra equations

“Roots are real” and “roots are positive integers” are not nearly the same amount of information.

For a quadratic with real roots `alpha,beta`:

- `P=alpha beta>0` means the roots have the same sign;
- `S=alpha+beta>0` then forces both to be positive;
- integer roots additionally require integer factor-pair structure when coefficients permit it.

## CONTRAST PAIR

A. Roots are positive real numbers, sum 8, product 12.

B. Roots are positive integers, sum 8, product 12.

In B the factor pairs of 12 make the possibilities discrete immediately.

## EQUALITY COLLAPSE

If positive roots have fixed sum and product satisfying an equality condition, AM-GM can force the roots to be equal.

For positive `alpha,beta`:

`alpha+beta >= 2sqrt(alpha beta)`.

Equality occurs only when `alpha=beta`.

### PYQ MECHANISM GROUNDING

`NMTC-BH-P-2024-Q17` is a clean anchor for positive-root/equality structure. `NMTC-BH-P-2023-Q13` is bridge evidence for discriminant/integer-case reasoning.

## TRY

1. A monic quadratic has positive integer roots, sum 11 and product 24. Find the roots.
2. `x^2-sx+16=0` has positive equal roots. Find `s`.
3. A monic quadratic has positive integer roots differing by 1 and product 20. Find it.

---

# 6. A quadratic relation can be a rewriting machine

## RECONNECT

If `x^2=x+1`, you might first think “solve the quadratic.”

But if the target is `x^20`, solving may be wasteful.

## DISCOVER

Use the relation repeatedly:

`x^2=x+1`

`x^3=2x+1`

`x^4=3x+2`

`x^5=5x+3`.

A recurrence appears.

## REALIZE

A quadratic relation reduces every higher power to a linear form `ax+b`.

The equation is not only a root-finding problem. It is a **rewriting rule**.

## CONTRAST PAIR

A. Find the roots of `x^2-x-1=0`.

B. If `x` satisfies `x^2=x+1`, simplify `x^8`.

A may justify the formula. B should first trigger reduction.

## TRY

1. If `x^2=2x+3`, express `x^5` as `ax+b`.
2. If `x^2+x+1=0`, simplify `x^100`.
3. If `u+1/u=3`, find `u^2+1/u^2` and then `u^3+1/u^3` without solving for `u`.

### PYQ MECHANISM GROUNDING

Clean anchors:

- `NMTC-BH-P-2018-Q06`;
- `NMTC-BH-P-2023-Q03`;
- `NMTC-BH-P-2024-Q01`.

These support “transform/reduce before calculate.”

---

# 7. Vertex/completing-square view: when the question asks for value, not roots

## RECONNECT

Take

`x^2-6x+5`.

Complete the square:

`x^2-6x+5=(x-3)^2-4`.

## REALIZE

Because `(x-3)^2>=0`, the minimum value is `-4`, attained at `x=3`.

This is a different question from asking how many roots the equation has.

## CONTRAST PAIR

- “minimum value of `x^2-6x+5`” -> complete square;
- “number of real roots of `x^2-6x+5=0`” -> discriminant or factorization.

## TRY

1. Find the minimum of `x^2-10x+31`.
2. Find the maximum of `-2x^2+8x-3`.
3. For what `m` is the minimum of `x^2-4x+m` equal to 5?

---

# 8. Parameter questions: translate words into conditions

Parameter problems become manageable once the phrase is translated into a mathematical condition.

| Phrase | Translate first to |
|---|---|
| equal roots | `D=0` |
| two distinct real roots | `D>0` |
| no real roots | `D<0` |
| positive roots | real + `S>0`, `P>0` |
| integer roots | Vieta + discrete factor/divisibility constraints |
| minimum/maximum prescribed | vertex/completing-square condition |

## TRY — classify before solving

For each write the condition only:

1. `x^2+kx+12=0` has equal roots.
2. `2x^2-(m+1)x+3=0` has no real roots.
3. `x^2-sx+15=0` has positive integer roots.
4. the minimum of `x^2-6x+t` is 4.

---

# 9. Error laboratory — learn the boundary, not just the rule

## Error 1: quadratic formula reflex

If the target is symmetric in roots or a high power under a low-degree relation, solving roots may be unnecessary.

## Error 2: Vieta sign memory

Rebuild from `a(x-alpha)(x-beta)`.

## Error 3: positive product means positive roots

Positive product means *same sign*. Use the sum to choose positive vs negative.

## Error 4: equation vs identity

If `x` is a root of `x^2=x+1`, the relation is valid for those roots. It is not a polynomial identity true for every real `x`.

## Error 5: source/key disagreement

If a printed stem mathematically implies a result different from the key, do not force the derivation to match the key. Mark the source conflict and preserve the printed mathematics.

`NMTC-BH-P-2025-Q20` is retained only as `SOURCE_CONFLICT_EVIDENCE` for this lesson.

---

# 10. Faded practice ladder

## Round 1 — H2 available

1. `2x^2-5x-3=0`, roots `alpha,beta`. Find `alpha^2+beta^2`.
2. choose `k` so `x^2-(k+1)x+4=0` has repeated roots.
3. if `x^2=3x-1`, express `x^4` as `ax+b`.

## Round 2 — H1 only

4. `3x^2-10x+2=0`, find `1/alpha+1/beta`.
5. form the equation whose roots are 2 more than the roots of `x^2-7x+10=0`.
6. find the minimum of `2x^2-12x+25`.

## Round 3 — H0 independent

7. roots `alpha,beta` of `x^2-4x-1=0`. Find `alpha^3+beta^3`.
8. find all `m` such that `x^2-mx+m=0` has equal roots.
9. if `z^2+z+1=0`, simplify `z^2026`.
10. a monic quadratic has positive integer roots and coefficients sum to zero. Build possible examples and state the structural constraint.

---

# 11. Mixed ADOPT laboratory — no chapter labels

For each item:

1. state the visible clue;
2. state the first move;
3. solve;
4. name one tempting alternative and why you rejected it.

A. A quadratic has exactly one real root and contains a parameter.

B. A target is `alpha/beta+beta/alpha`.

C. A relation gives `x^2=1-x` and asks for `x^50`.

D. A quadratic expression asks for its least possible value.

E. Roots are positive integers and their product is fixed.

F. A transformed equation has roots `alpha+3,beta+3`.

G. The answer key conflicts with a derivation from the printed sign.

---

# 12. Six-question mastery check

For each core idea — discriminant, Vieta, transformed roots, power reduction, vertex view — answer:

1. What did you notice?
2. Why does the method work?
3. What clue would make you think of it?
4. What similar-looking situation would require a different method?
5. Can you write the first two useful lines without help?
6. Can you solve a disguised version?

You are ready for mixed Preliminary work only when these answers are stable without chapter labels.

---

# Quick answer/check section

Selected answers:

Diagnostic: 1. `(x-3)(x-4)`; 2. `2,3`; 3. `7,10`; 4. repeated real root; 5. `(x-3)^2-4`; 6. `2x+1`; 7. Vieta/symmetric rewrite; 8. complete square/vertex.

Section 2: 1. `k=+-8`; 2. `m<9`; 3. `t>4`.

Section 3: 1. `42`; 2. `-5/2`; 3. `17/4`; 4. `180`.

Section 4 for `x^2-6x+5`: shifted by 2 -> `x^2-10x+21=0`; reciprocal -> `5x^2-6x+1=0`; squared -> `x^2-26x+25=0`.

Section 5: 1. roots `3,8`; 2. `s=8`; 3. roots `4,5`, equation `x^2-9x+20=0`.

Section 6: 1. `x^3=7x+6`, `x^4=20x+21`, `x^5=61x+60`; 2. powers cycle with `x^3=1`, so `x^100=x`; 3. `7`, then `18`.

Section 7: 1. `6`; 2. `5`; 3. `t=9`.

## Source boundary

Historical IDs above are mechanism grounding only. Full third-party problem statements are not reproduced. Practice is author-created unless explicitly identified otherwise. Bonus/source-conflict evidence retains its disposition and does not inflate recurrence.
