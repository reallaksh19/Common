# Polynomials, Roots, Vieta & Remainders
## Integrated Assimilation Book

> **The requested information chooses the representation.**

---

## 1. RECONNECT - one polynomial, several useful forms

Consider

`P(x)=x^2-5x+6`.

Expanded form exposes coefficients:

`x^2-5x+6`.

Factored form exposes zeros:

`(x-2)(x-3)`.

Root list exposes the same zero information directly:

`2,3`.

No representation is universally best.

### First attempt

For each request, name the cheapest representation before solving.

1. Find the roots of `x^2-5x+6`.
2. Find the sum and product of the roots of `2x^2-5x-3`.
3. Decide how many real roots `x^2-4x+5=0` has.
4. Find the remainder of `x^100` when reduced under `x^2=1`.

---

## 2. DISCOVER - roots and factors are the same zero structure

If `P(r)=0`, then `x-r` is a factor of `P(x)`.

For a quadratic with roots `alpha,beta` and leading coefficient `a`,

`P(x)=a(x-alpha)(x-beta)`.

Expanding,

`P(x)=a[x^2-(alpha+beta)x+alpha beta]`.

Compare this with

`ax^2+bx+c`.

Coefficient matching gives

`-a(alpha+beta)=b`, so

`alpha+beta=-b/a`,

and

`a alpha beta=c`, so

`alpha beta=c/a`.

This is **Vieta derived from factor expansion**. It is not an independent formula list.

### Use the information the target asks for

For `x^2-7x+10=0`, if the target is `alpha^2+beta^2`, do not solve roots first:

`alpha+beta=7`, `alpha beta=10`,

so

`alpha^2+beta^2=49-20=29`.

### Contrast

- “find `alpha,beta`” -> individual roots may be needed;
- “find `alpha^2+beta^2`” -> symmetric invariants are enough.

---

## 3. MAKE SENSE - discriminant describes quadratic root behavior

For

`ax^2+bx+c=0`, `a!=0`,

the quadratic formula is

`x=(-b +- sqrt(b^2-4ac))/(2a)`.

The quantity

`Delta=b^2-4ac`

controls real-root behavior:

- `Delta>0`: two distinct real roots;
- `Delta=0`: one repeated real root;
- `Delta<0`: no real roots.

### Root geometry

The parabola `y=ax^2+bx+c` meets the x-axis twice, touches once, or does not meet it according to the same three cases.

### Mandatory boundary with ALG-02

Question: “How many real roots does `x^2-4x+5=0` have?”  
Use discriminant: `Delta=16-20=-4`, so none.

Question: “What is the minimum value of `x^2-4x+5`?”  
That is an optimization request. Complete the square in ALG-02:
`(x-2)^2+1`, minimum `1`.

Same quadratic, different requested information, different canonical method.

---

## 4. DISCOVER - transformed roots and shifted input move in opposite directions

Suppose `P(x)` has roots `alpha,beta`.

To build a polynomial with roots `alpha+c, beta+c`, replace `x` by `x-c`:

`Q(x)=P(x-c)`.

Why? If `x=alpha+c`, then `x-c=alpha`, so `P(alpha)=0`.

### Example

`P(x)=x^2-5x+6` has roots `2,3`.

Roots shifted **up by 4** are `6,7`.

Use

`Q(x)=P(x-4)=(x-6)(x-7)=x^2-13x+42`.

But `P(x+4)` has roots `-2,-1`.

> Root shift `+c` requires input shift `-c`.

---

## 5. MAKE SENSE - remainder theorem and factor theorem

When a polynomial `P(x)` is divided by `x-a`, the remainder is `P(a)`.

Reason: division gives

`P(x)=(x-a)Q(x)+r`,

where `r` is constant. Set `x=a`:

`P(a)=r`.

Therefore:

- remainder on division by `x-a` is `P(a)`;
- `x-a` is a factor exactly when `P(a)=0`.

### Example

For `P(x)=x^3+2x+5`, remainder on division by `x-2` is

`P(2)=8+4+5=17`.

---

## 6. DISCOVER - polynomial reduction is the canonical extension of ALG-01 relation rewriting

ALG-01 taught the local habit: if an admissible `x` satisfies `x^2=3x-1`, replace higher powers rather than solving the roots.

ALG-03 generalizes this to polynomial reduction.

Modulo the relation

`x^2-3x+1=0`,

we may write

`x^2 ≡ 3x-1`.

Every higher power reduces to degree less than `2`.

For example,

`x^3 ≡ x(3x-1) = 3x^2-x ≡ 8x-3`,

and ultimately

`x^5 ≡ 55x-21`.

The language is now about the **remainder class modulo a polynomial**, not only values at individual roots.

### Contrast

To find `x^2026` modulo `x^2+x+1`, do not calculate 2026 multiplications.

Because

`x^3-1=(x-1)(x^2+x+1)`,

we have

`x^3 ≡ 1 (mod x^2+x+1)`.

Since `2026 ≡ 1 (mod 3)`,

`x^2026 ≡ x`.

---

## 7. MAKE SENSE - common-root elimination lowers degree

Suppose a number is a common root of

`x^2-5x+6=0`

and

`x^2-4x+3=0`.

Subtract the equations:

`-x+3=0`.

So any common root must be `x=3`.

Check it in both originals: it works.

This is cheaper than solving two quadratics separately and intersecting the answer sets.

---

## 8. TRY - H3 -> H2 -> H1 -> H0

Attempt before support.

### H3 - execution relation supplied

Roots `alpha,beta` of `x^2-8x+12=0`. Find `alpha^2+beta^2`.

Use Vieta `alpha+beta=8`, `alpha beta=12`, then
`alpha^2+beta^2=(alpha+beta)^2-2alpha beta=40`.

### H2 - representation supplied

Find the polynomial whose roots are `5` more than the roots of `x^2-3x-4`.

Cue: use `P(x-5)` and simplify.

### H1 - recognition clue

Find the remainder of `x^50` modulo `x^2-1`.

Clue: do not expand powers; reduce the relation first.

### H0 - no route supplied

Two monic quadratics share a root:
`x^2-7x+10=0`, `x^2-5x+4=0`. Find the common root.

---

## 9. DIAGNOSE - four representation errors

### Error A - solve roots when target is symmetric

Repair: Vieta first; solve roots only if target still distinguishes them.

### Error B - use discriminant for a vertex-value request

Repair: root count -> ALG-03 discriminant; minimum/maximum -> ALG-02 square completion.

### Error C - shift polynomial input in the same direction as desired root shift

Repair: test one root. Root `alpha+c` must make the **input** equal `alpha`, hence `P(x-c)`.

### Error D - calculate high powers directly

Repair: identify the polynomial relation and reduce after each multiplication, or exploit periodicity.

---

## 10. ADOPT - one topic-wide First-Step logic

```text
REQUEST
 -> roots individually?          -> factor/solve
 -> symmetric root information? -> Vieta
 -> root count/behavior?         -> discriminant
 -> transformed roots?          -> transform input
 -> remainder/factor?           -> evaluate or divide
 -> high power modulo relation? -> reduce
 -> common root?                -> eliminate
 -> CHECK
```

---

## 11. Historical anchor traces

### `IOQM-2025-Q16`
Combine the given polynomial functions so the root information is visible. The independently verified route reconstructs a quadratic with roots `-2,3`, determines its scale, and recovers the requested value `22`.

### `IOQM-2025-Q24`
Factor the divisor as `(x^2+1)(x^2+x+1)` and reduce `x^2025` modulo the polynomial instead of computing the high power. The independently verified remainder evaluated at the requested point gives `53`.

### `IOQM-2024-Q24`
The coefficient restriction creates a finite structural polynomial problem; exhaustive independent checking of the admissible binary-coefficient configurations confirms answer `50`.

### `IOQM-2023-Q12`
A cubic identity creates a factorized alternative; parity/admissibility eliminates one branch and the remaining equal-structure branch gives answer `18`.

These anchors are mechanism evidence, not weightage evidence.

---

## 12. TRANSFER

- symmetric root expressions -> algebraic invariants without explicit roots;
- parameter root-count questions -> discriminant feasibility;
- recurrence/high-power problems -> polynomial reduction / periodic remainders;
- common-root systems -> elimination/GCD thinking;
- transformed-root questions -> input transformation, a useful precursor to functional transformations.

## Final belief

> **Before solving a polynomial, I ask what information the target needs and choose the representation that exposes exactly that information.**
