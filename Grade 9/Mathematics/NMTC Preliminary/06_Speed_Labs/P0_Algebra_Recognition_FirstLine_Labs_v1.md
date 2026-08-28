# P0 Algebra — Recognition & First-Line Speed Labs v1

## Purpose

Train the Preliminary bottleneck:

`recognize structure -> write first useful line`

No full solving is allowed in Round A or B.

All prompts are `AUTHOR_CREATED_FOUNDATION` or `AUTHOR_CREATED_TRANSFER`.

---

# Round A — Recognition only

## Rules

- Suggested working window: 20 seconds per item during practice; timing is a training target, not an official NMTC claim.
- Write only one code.
- Do not calculate beyond what is needed to identify the structure.

Codes:

- `PR` — power reduction from a relation
- `VT` — Vieta / root invariants
- `RM` — remainder / polynomial modular reduction
- `FT` — factor first / structural high degree
- `IR` — integer/positive-root constraint
- `CR` — common-root elimination
- `SH` — shifted/transformed roots/functions
- `BD` — bound/equality check
- `DR` — discriminant/root-count condition

## Prompts

1. `x^2=5x-2`, target contains `x^9`.
2. Roots `alpha,beta`; target is `alpha^2+beta^2`.
3. Polynomial divisible by `x^2+1`.
4. `x^4-13x^2+36=0`.
5. Four positive roots have sum 8 and product 16.
6. Two polynomials share a root and one is quadratic.
7. Roots of `f(x+4)` are requested.
8. “Find the maximum” under `ab=1`, `a,b>0`.
9. A quadratic has a repeated root.
10. `x^100+...` is divided by `x^2-1`.
11. Roots `alpha,beta`; target is `1/alpha+1/beta`.
12. A quartic has coefficients reading the same from both ends.
13. A cubic has positive integer roots and small integer coefficients.
14. `P(x)` is divided by `3x-9`.
15. Two polynomials share root `r`; the first gives `r^2=2r+1`.
16. Equation whose roots are `alpha+2,beta+2` is requested.
17. Parameter quadratic is required to have no real roots.
18. A polynomial is divisible by `x-7`.
19. A high-degree symmetric expression uses only `x+y` and `xy` naturally.
20. A problem asks for minimum under a positive fixed-product condition.

## Answer key

1. PR
2. VT
3. RM
4. FT
5. IR / BD — accept either if justified; ideal chain `BD -> equality -> IR/root structure`
6. CR
7. SH
8. BD
9. DR
10. RM
11. VT
12. FT
13. IR
14. RM — use the zero `x=3`
15. CR
16. SH / VT — both can be valid; learner must state chosen representation
17. DR
18. RM
19. FT / VT-style symmetric reduction — accept if the learner explicitly chooses `s=x+y,p=xy`
20. BD

## Pass standard

- `>=16/20`: operationally ready for First-Line Lab.
- `13–15`: repeat only missed mechanism families.
- `<13`: return to First-Step cards before timed solving.

---

# Round B — First line only

## Rules

Write exactly the first useful mathematical line or setup. Stop.

### B1
`x^2+x-3=0`, target contains `x^8`.

**Expected first line:** `x^2=3-x`.

### B2
Roots of `2x^2-7x+1=0` are `alpha,beta`; target is symmetric.

**Expected first line:** `alpha+beta=7/2, alpha beta=1/2`.

### B3
Find an unknown coefficient so a polynomial is divisible by `x^2+1`.

**Expected first line:** `x^2≡-1 (mod x^2+1)`.

### B4
Factor a reciprocal quartic with nonzero constant term.

**Expected first line:** divide by `x^2` and set `t=x+1/x` (when the coefficient pattern supports it).

### B5
Four positive numbers have sum 20 and product 625.

**Expected first line:** `AM=5, GM=625^(1/4)=5`; inspect equality.

### B6
`r` is a common root of a quadratic and a cubic.

**Expected first line:** solve the quadratic relation for `r^2` (or compute the cubic remainder modulo the quadratic).

### B7
A new polynomial has roots `alpha+3,beta+3`.

**Expected first line:** `new sum=(alpha+beta)+6`.

### B8
A problem asks for the maximum of `a+b` given `ab=1`, `a,b>0`.

**Expected first line:** set `a=t, b=1/t` and test growth as `t` varies.

### B9
A quadratic has a repeated real root.

**Expected first line:** `Delta=b^2-4ac=0`.

### B10
Remainder on division by `3x-6` is requested.

**Expected first line:** divisor zero is `x=2`; evaluate `P(2)`.

### B11
A monic cubic has positive integer roots, sum 7 and product 8.

**Expected first line:** list positive factor triples of 8 consistent with sum 7.

### B12
The coefficient of `x^N` in a product of finite geometric sums is requested.

**Expected first line:** interpret coefficient as the count of admissible exponent tuples summing to `N`.

## Pass standard

`>=10/12` structurally correct first lines.

A correct final answer reached from a poor first line does not count as a First-Line pass.

---

# Round C — Contrast speed

For each pair, state which move is cheaper and why.

1. High powers + quadratic relation: `solve roots` vs `reduce powers`.
2. Symmetric root target: `quadratic formula` vs `Vieta`.
3. Divisor `x-4`: `long division` vs `P(4)`.
4. Divisor `x^2+1`: `single substitution` vs `polynomial remainder reduction`.
5. “Maximum” under flexible positive-product constraint: `AM-GM immediately` vs `boundedness check first`.
6. Cubic with obvious integer root: `general cubic method` vs `factor first`.

Expected preferred moves:

`reduce, Vieta, P(4), polynomial reduction, boundedness first, factor first`.

---

# Diagnostic error mapping

| Error | Remediation |
|---|---|
| confuses PR and VT | repeat “what is the target asking?” contrasts |
| uses one substitution for quadratic divisor | revisit remainder-degree explanation |
| always chooses quadratic formula | redo “solve vs use root information” lab |
| misses palindromic quartic | practice coefficient-symmetry recognition |
| applies AM-GM to an unbounded maximum | boundedness contrast set |
| common root -> solves both polynomials | elimination/remainder common-root ladder |
| wrong zero for `ax+b` divisor | linear-divisor zero drill |

## Status

`LAB_STATUS: READY_FOR_INTERNAL_USE_v1`

Final publication still needs classroom readability/timing calibration and item-order review.
