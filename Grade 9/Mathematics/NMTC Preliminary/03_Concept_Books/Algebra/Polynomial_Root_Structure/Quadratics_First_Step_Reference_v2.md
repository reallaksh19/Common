# Quadratics — First-Step Reference v2
## Use after the Assimilation Book

This is a compression/revision layer. It assumes the main ideas have already been made meaningful.

`SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`

---

# 1. Recognition atlas

| If you see... | Test this first |
|---|---|
| small integer coefficients, roots requested | factorization |
| exactly one / repeated real root | `D=0` |
| two distinct real roots | `D>0` |
| no real roots | `D<0` |
| minimum / maximum of quadratic expression | complete square / vertex |
| `alpha^2+beta^2`, reciprocal sum, root ratio | Vieta using `S,P` |
| roots shifted, squared, reciprocal | transform `S,P` |
| positive roots | reality + `S>0`, `P>0` |
| positive integer roots | Vieta + factor-pair/divisibility structure |
| large powers with a quadratic relation | reduce powers |
| same root satisfies two equations | eliminate |
| printed key conflicts with mathematics | source-integrity check |

---

# 2. Phrase decoder

- “equal roots” -> repeated root -> `D=0`.
- “real and distinct” -> `D>0`.
- “no real solution” -> `D<0`.
- “least/greatest value” -> graph/vertex representation.
- “sum/product/expression in roots” -> ask whether individual roots are actually needed.
- “positive integer roots” -> convert Vieta into a discrete factor-pair problem.
- “given `x^2=...`, find `x^n`” -> relation is a rewriting machine.
- “roots become `alpha+h,beta+h`” -> transform invariants.

---

# 3. Quick decision tree

```text
What is the question asking for?

INDIVIDUAL ROOT(S)?
    -> factor / formula / structural factor first

NUMBER OR NATURE OF REAL ROOTS?
    -> discriminant

MINIMUM / MAXIMUM VALUE?
    -> complete square / vertex

SYMMETRIC EXPRESSION IN ROOTS?
    -> write S=alpha+beta, P=alpha beta

TRANSFORMED ROOTS?
    -> transform S,P before solving roots

POSITIVE / INTEGER ROOT RESTRICTIONS?
    -> Vieta + sign / factor pairs / bounds

HIGH POWERS UNDER LOW-DEGREE RELATION?
    -> reduce / recur / look for cycle

SOURCE OR KEY LOOKS INCONSISTENT?
    -> derive from printed mathematics, then flag conflict
```

---

# 4. First-Step Cards

## Card A — Factor view

**Clue:** roots requested; coefficients factor cleanly.

**Write:** product-sum pair for `ac` and `b`, or direct factorization.

**Do not:** use the quadratic formula automatically when factorization is immediate.

## Card B — Discriminant

**Clue:** equal / distinct / no real roots, often with a parameter.

**Write:** `D=b^2-4ac` and the required sign condition.

**Check:** strict vs non-strict inequality.

## Card C — Vieta

**Clue:** target is symmetric in roots.

**Write:** `S=-b/a`, `P=c/a`.

**Then:** rewrite target in `S,P`.

**Check:** if alpha and beta swap, should the target stay unchanged?

## Card D — Transformed roots

**Clue:** new roots are shifted/reciprocal/squared versions.

**Write:** new sum and product.

**Then:** build `x^2-S'x+P'=0`.

## Card E — Positive/integer roots

**Clue:** positivity/integrality language.

**Write:** Vieta constraints first.

**Then:** add sign, factor-pair, divisibility, parity, or bound information.

## Card F — Power reduction

**Clue:** large exponent, but a quadratic relation is given.

**Write:** isolate `x^2` and reduce.

**Check:** is there a short recurrence/cycle?

## Card G — Vertex view

**Clue:** least/greatest possible value.

**Write:** complete the square, or use vertex coordinate after meaning is understood.

---

# 5. Contrast pairs

## Pair 1

- Find the larger root -> individual roots.
- Find `alpha^2+beta^2` -> Vieta.

## Pair 2

- Equal roots -> discriminant.
- Minimum value -> vertex/completing square.

## Pair 3

- Positive real roots -> sign + reality.
- Positive integer roots -> add discrete factor-pair restrictions.

## Pair 4

- Solve `x^2-x-1=0` -> root solving may be justified.
- Simplify `x^20` given `x^2=x+1` -> reduction first.

## Pair 5

- roots are `alpha+2,beta+2` -> transform `S,P`.
- solve `f(x+2)=0` -> shift input/variable carefully.

---

# 6. Recognition laboratory — DO NOT SOLVE

Write only the first move.

1. `x^2+(m-1)x+4=0` has equal roots.
2. roots `alpha,beta` of `2x^2-7x+1=0`; target `alpha^2+beta^2`.
3. find the minimum of `3x^2-12x+19`.
4. `x^2=3x-1`; target `x^9`.
5. monic quadratic has positive integer roots with product 18.
6. new roots are `1/alpha,1/beta`.
7. same number is a root of two polynomial equations.
8. official-looking key disagrees with the sign forced by Vieta.
9. quadratic has two real distinct roots.
10. target is the larger root of an ugly quadratic.

### Recognition answers

1. `D=0`.
2. `S,P`; rewrite target.
3. complete square / vertex.
4. isolate `x^2`; reduce/recur.
5. Vieta + positive factor pairs of 18.
6. new `S'=S/P`, `P'=1/P`.
7. eliminate using both equations at the shared root.
8. source-integrity check; do not force the key.
9. `D>0`.
10. individual-root method may be necessary.

---

# 7. Thirty-second checks

Before committing to a method ask:

1. What exactly is requested?
2. Does the target need individual roots?
3. Is there a representation that makes the target smaller?
4. Is a parameter phrase secretly a discriminant/sign condition?
5. Is the given quadratic relation meant as a rewriting rule?
6. Have I used every restriction: real, positive, integer, equal, distinct?
7. Does my answer satisfy the original equation/condition?

---

# 8. Source-to-first-step map

| PYQ ID | Evidence role | First-step mechanism |
|---|---|---|
| `NMTC-BH-P-2018-Q06` | clean scored | reduce high powers from quadratic relation |
| `NMTC-BH-P-2023-Q03` | clean scored | reciprocal/low-degree reduction |
| `NMTC-BH-P-2024-Q01` | clean scored | use `x^2=1-x`; recurrence |
| `NMTC-BH-P-2024-Q14` | clean scored | transformed-root Vieta |
| `NMTC-BH-P-2024-Q17` | clean scored | positive roots + equality collapse |
| `NMTC-BH-P-2024-Q22` | clean scored | shift first, then root structure |
| `NMTC-BH-P-2018-Q07` | bonus evidence | repeated root -> `D=0` |
| `NMTC-BH-P-2023-Q13` | bridge evidence | quadratic/discriminant/integer cases |
| `NMTC-BH-P-2025-Q20` | source conflict only | source-QC; not canonical practice |

---

# 9. Can I start without help?

For an unfamiliar quadratic problem, can you answer all of these before seeing a solution?

1. What visible clue matters?
2. Which representation makes the problem smallest?
3. What is the first useful line?
4. Which tempting method are you deliberately not using?
5. What condition must be checked at the end?

If yes, the concept is becoming operational rather than memorized.
