# Quadratics - Transformed Roots, Integer Roots & Structural Reduction
## Answer & Diagnostic Key - Issue #39

This key is teacher-facing. The final answers below were independently recomputed after the student module was authored. Numerical/algebraic answers were checked by a second route: transformed roots were checked from explicit roots where convenient, and power reductions were checked as polynomial remainders modulo the governing quadratic relation.

---

# 1. Reconnect diagnostic - first-line expectations

1. Write original \(S=9,P=14\), then transformed \(S'=S+4\) and \(P'=P+2S+4\).
2. \(P>0\) means the two **real** roots have the same sign; it does not yet prove positivity. Use \(S\) to distinguish both positive from both negative.
3. Positive integer roots must be positive factor pairs of \(24\), further filtered by any sum/parity/divisibility information.
4. Use \(x^2=2x+3\) as a replacement rule, or \(x^n=2x^{n-1}+3x^{n-2}\).
5. If \(f(r)=0\), then \(x+3=r\), so \(x=r-3\).
6. No. Recompute from the printed mathematics, preserve the printed source, record the disagreement, and classify the record according to source custody.

Diagnostic tags: `recognition`, `first_move`, `representation`, `domain`, `source_integrity`.

---

# 2. Strand A - transformed roots

## A1

Original equation:

\[
x^2-9x+14=0.
\]

So \(S=9,\;P=14\). New roots are \(\alpha+1,eta+1\):

\[
S'=11,\qquad P'=14+9+1=24.
\]

Therefore

\[
\boxed{y^2-11y+24=0}.
\]

**Independent check:** original roots are \(2,7\); transformed roots are \(3,8\), whose equation is \((y-3)(y-8)=0\).

**Likely diagnostic tag:** `TRANSFORM_SOLVED_ROOTS_UNNECESSARILY` if the learner starts with the quadratic formula.

## A2

For

\[
2x^2-5x-3=0,
\]

\[
S=\frac52,\qquad P=-\frac32.
\]

Reciprocal roots are valid because \(P\ne0\).

\[
S'=\frac SP=-\frac53,\qquad P'=\frac1P=-\frac23.
\]

Thus

\[
y^2+\frac53y-\frac23=0,
\]

or with integer coefficients,

\[
\boxed{3y^2+5y-2=0}.
\]

**Independent check:** original roots are \(-\tfrac12,3\); reciprocal roots are \(-2,\tfrac13\), giving \((y+2)(3y-1)=0\).

**Likely tags:** `domain`, `VIETA_SIGN_ERROR`, `TRANSFORM_SOLVED_ROOTS_UNNECESSARILY`.

## A3

For

\[
x^2-4x-1=0,
\]

\(S=4,\;P=-1\). For squared roots:

\[
S'=S^2-2P=16+2=18,\qquad P'=P^2=1.
\]

Therefore

\[
\boxed{y^2-18y+1=0}.
\]

**Independent check:** original roots are \(2\pm\sqrt5\); their squares are \(9\pm4\sqrt5\), with sum \(18\) and product \(1\).

## A4

\[
f(x+3)=(x+3)^2-6(x+3)+8=x^2-1.
\]

Hence

\[
\boxed{x=-1,1}.
\]

The structural first line is \(x+3=r\), where \(r\in\{2,4\}\), so \(x=r-3\).

**Likely tag:** `SHIFT_DIRECTION_ERROR` if the learner shifts roots by \(+3\).

---

# 3. Strand B - positive/integer roots

## B1

Positive factor pairs of \(21\) are \((1,21)\) and \((3,7)\). The sum \(10\) selects

\[
\boxed{3,7}.
\]

The quadratic is

\[
\boxed{x^2-10x+21=0}.
\]

## B2

Positive factor pairs of \(24\) include \((1,24),(2,12),(3,8),(4,6)\). Only \((4,6)\) differ by \(2\). Therefore

\[
k=4+6=\boxed{10}.
\]

**Likely tag:** `INTEGRALITY_IGNORED` if the learner solves a continuous parameter problem instead of using integer pairs.

## B3

For positive roots with product \(25\), AM-GM gives

\[
S\ge2\sqrt{25}=10.
\]

Here \(S=s\), so the smallest possible value is

\[
\boxed{s=10}.
\]

Equality gives roots \(5,5\).

**Independent check:** discriminant condition gives \(s^2-100\ge0\); positivity requires \(s>0\), hence \(s\ge10\).

**Likely tag:** `EQUALITY_BOUNDARY_MISSED` if unnecessary factor enumeration precedes the equality test.

## B4

Positive factor pairs of \(12\):

\[
(1,12),(2,6),(3,4).
\]

Their sums are \(13,8,7\), so

\[
\boxed{n\in\{7,8,13\}}.
\]

---

# 4. Strand C - structural reduction

## C1

Given \(x^2=3x-2\):

\[
x^3=3x^2-2x=7x-6,
\]

\[
x^4=7x^2-6x=7(3x-2)-6x=15x-14.
\]

Therefore

\[
\boxed{x^4=15x-14}.
\]

**Independent check:** polynomial remainder of \(x^4\) modulo \(x^2-3x+2\) is \(15x-14\).

## C2

Given \(x^2=x+2\):

\[
x^3=3x+2,
\]

\[
x^4=5x+6,
\]

\[
x^5=11x+10,
\]

\[
x^6=21x+22.
\]

Thus

\[
\boxed{x^6=21x+22}.
\]

**Independent check:** polynomial remainder of \(x^6\) modulo \(x^2-x-2\) is \(21x+22\).

## C3

From

\[
x^2+x+1=0,
\]

we get \(x^3=1\). Since \(100\equiv1\pmod3\),

\[
\boxed{x^{100}=x}.
\]

**Independent check:** polynomial remainder of \(x^{100}\) modulo \(x^2+x+1\) is \(x\).

## C4

With

\[
u+\frac1u=4,
\]

square:

\[
u^2+2+u^{-2}=16,
\]

so

\[
\boxed{u^2+u^{-2}=14}.
\]

Then

\[
(u+u^{-1})(u^2+u^{-2})
=u^3+u^{-3}+u+u^{-1},
\]

so

\[
4\cdot14=(u^3+u^{-3})+4.
\]

Therefore

\[
\boxed{u^3+u^{-3}=52}.
\]

**Independent check:** reciprocal recurrence \(A_n=4A_{n-1}-A_{n-2}\), with \(A_0=2,A_1=4\), gives \(A_2=14,A_3=52\).

---

# 5. Contrast-pair expectations

1. **Root transformation vs input shift:** transformed roots -> transform \(S,P\); \(f(x+h)=0\) -> \(x+h=r\), so roots shift by \(-h\).
2. **Positive real vs positive integer:** positive real needs reality plus sign invariants; integer adds finite factor/parity/divisibility cases.
3. **Root requested vs high power requested:** explicit roots can be justified for an individual-root target; a high power under a degree-2 relation should be reduced first.
4. **Clean source vs source conflict:** use qualified clean evidence normally; for a conflict, recompute and preserve the disagreement instead of editing the source.
5. **Reciprocal equation vs reciprocal sum:** an equation needs both transformed sum and product; a single invariant target needs only the requested quantity.
6. **Equality collapse vs enumeration:** test \(S=2\sqrt P\) for positive roots before listing discrete cases.

---

# 6. Recognition-only laboratory - expected first moves

1. Write \(S'=S+8,\;P'=P+4S+16\).
2. If \(f(r)=0\), write \(x-5=r\), so \(x=r+5\).
3. Write positive factor pairs of \(36\), then apply any sum/other restriction.
4. Write the reality condition plus \(S>0,P>0\).
5. Rewrite \(z^2=4z-1\) and reduce powers / use the induced recurrence.
6. Define \(A_n=w^n+w^{-n}\) and use \(A_n=3A_{n-1}-A_{n-2}\).
7. Check \(P\ne0\), then \(S'=S/P,\;P'=1/P\).
8. Recompute from print, preserve the source, record the disagreement, classify source conflict.

---

# 7. Transfer bank

## X1 - compound transformation

Original \(S=7,P=10\). After adding \(2\):

\[
S_1=11,\qquad P_1=10+14+4=28.
\]

Now take reciprocals:

\[
S'=\frac{11}{28},\qquad P'=\frac1{28}.
\]

Therefore

\[
\boxed{28y^2-11y+1=0}.
\]

**Independent check:** original roots are \(2,5\); transformed roots are \(1/4,1/7\), giving \((4y-1)(7y-1)=0\).

## X2 - shift, then square

Original \(S=5,P=5\). For \(\alpha-1,eta-1\):

\[
S_1=3,\qquad P_1=5-5+1=1.
\]

Squaring those shifted roots gives

\[
S'=S_1^2-2P_1=9-2=7,\qquad P'=1.
\]

Thus

\[
\boxed{y^2-7y+1=0}.
\]

## X3 - domain boundary

\[
x^2-4x=x(x-4),
\]

so the roots are \(0,4\). One reciprocal would be \(1/0\), undefined. Also \(P=0\), so the reciprocal formulas are invalid.

\[
\boxed{\text{No reciprocal-root quadratic exists for both roots.}}
\]

**Likely tag:** `domain`.

## X4 - parity before enumeration

Product \(15\) is odd, so two integer roots must both be odd. The sum of two odd integers is even, but the required sum is \(9\), odd.

\[
\boxed{\text{Impossible}}.
\]

**Independent factor-pair check:** positive pairs \((1,15)\) and \((3,5)\) have sums \(16\) and \(8\), not \(9\).

## X5 - divisibility filter

Positive integer roots sum to \(14\). If at least one is divisible by \(5\), the possible unordered pairs are

\[
(4,10),\qquad(5,9).
\]

Since \(m\) is the product,

\[
\boxed{m\in\{40,45\}}.
\]

## X6 - positive-real boundary

For

\[
x^2-sx+6=0,
\]

\(S=s,\;P=6>0\). Reality requires

\[
s^2-24\ge0.
\]

Positivity requires \(s>0\), so

\[
\boxed{s\ge2\sqrt6}.
\]

At equality the repeated root is \(\sqrt6>0\), which is allowed because “not necessarily distinct” was stated.

## X7 - reduction without roots

\[
r^2=2r-2.
\]

Then

\[
r^3=2r^2-2r=2r-4,
\]

\[
r^4=2r^2-4r=2(2r-2)-4r=-4.
\]

Hence

\[
\boxed{r^4=-4}.
\]

**Independent check:** remainder of \(r^4\) modulo \(r^2-2r+2\) is \(-4\).

## X8 - recurrence transfer

From \(x^2=1-x\), repeated reduction gives

\[
x^3=2x-1,
\]

\[
x^4=2-3x,
\]

\[
x^5=5x-3,
\]

\[
x^6=5-8x,
\]

\[
x^7=13x-8.
\]

Therefore

\[
\boxed{x^7=13x-8}.
\]

**Independent check:** remainder of \(x^7\) modulo \(x^2+x-1\) is \(13x-8\).

## X9 - reciprocal-cycle transfer

Let \(A_n=v^n+v^{-n}\). Given \(A_1=1\) and \(A_0=2\),

\[
A_n=A_{n-1}-A_{n-2}.
\]

Thus

\[
A_2=-1,\ A_3=-2,\ A_4=-1,\ A_5=1,\ A_6=2.
\]

So

\[
\boxed{v^6+v^{-6}=2}.
\]

## X10 - source integrity

Expected decision:

\[
\boxed{\text{Preserve the printed mathematics and classify the record as source conflict.}}
\]

The student/editor should:

1. recompute from the printed statement;
2. retain the printed sign;
3. record how the provisional key disagrees;
4. identify any sign reversal only as a diagnostic observation, not as an edit;
5. keep the record as `SOURCE_CONFLICT_EVIDENCE`, not a canonical clean PYQ.

For this unit the relevant record is `NMTC-BH-P-2025-Q20`. No reconstructed source stem should be substituted into student practice.

---

# 8. Error taxonomy and repair route

| Error tag | What it reveals | Repair |
|---|---|---|
| `TRANSFORM_SOLVED_ROOTS_UNNECESSARILY` | representation/efficiency gap | redo one transformed problem using only \(S,P\) |
| `SHIFT_DIRECTION_ERROR` | decision-boundary gap | use \(x+h=r\) on two close shift contrasts |
| `POSITIVE_PRODUCT_ONLY` | sign-invariant gap | compare \((+,+)\) and \((-,-)\) pairs with same product |
| `INTEGRALITY_IGNORED` | condition/domain gap | force factor-pair/parity reasoning before algebra |
| `EQUALITY_BOUNDARY_MISSED` | structural-recognition gap | test AM-GM equality before enumeration |
| `SOLVED_WHEN_REDUCTION_WAS_ENOUGH` | first-move/representation gap | write the rewrite rule before any quadratic formula |
| `RELATION_TREATED_AS_IDENTITY` | domain/logical gap | state explicitly which specified root/value satisfies the relation |
| `SOURCE_CONFLICT_NOT_FLAGGED` | source-integrity/checking gap | recompute from print and preserve provenance status |
| `VIETA_SIGN_ERROR` | reconstruction gap | rebuild from factor expansion rather than memory |
| `calculation` | arithmetic execution gap | recompute after structure is correctly chosen |

---

# 9. Independent answer-audit ledger

| ID | Promoted result | Independent route | Status |
|---|---|---|---|
| A1 | \(y^2-11y+24=0\) | explicit roots \(2,7\to3,8\) | PASS |
| A2 | \(3y^2+5y-2=0\) | explicit roots \(-1/2,3\to-2,1/3\) | PASS |
| A3 | \(y^2-18y+1=0\) | explicit squared roots \(9\pm4\sqrt5\) | PASS |
| A4 | \(x=-1,1\) | direct expansion of \(f(x+3)\) | PASS |
| B1 | roots \(3,7\) | factor-pair enumeration | PASS |
| B2 | \(k=10\) | unique product-24 pair differing by 2 | PASS |
| B3 | \(s=10\) | AM-GM and discriminant cross-check | PASS |
| B4 | \(n=7,8,13\) | all positive factor pairs of 12 | PASS |
| C1 | \(15x-14\) | polynomial remainder mod governing quadratic | PASS |
| C2 | \(21x+22\) | polynomial remainder mod governing quadratic | PASS |
| C3 | \(x\) | cycle and polynomial remainder | PASS |
| C4 | \(14,52\) | reciprocal recurrence | PASS |
| X1 | \(28y^2-11y+1=0\) | explicit roots \(2,5\to1/4,1/7\) | PASS |
| X2 | \(y^2-7y+1=0\) | sequential transformed invariants | PASS |
| X3 | invalid reciprocal pair | explicit zero root | PASS |
| X4 | impossible | parity plus factor-pair cross-check | PASS |
| X5 | \(m=40,45\) | exhaustive positive integer pairs summing 14 | PASS |
| X6 | \(s\ge2\sqrt6\) | discriminant + Vieta sign conditions | PASS |
| X7 | \(-4\) | polynomial remainder | PASS |
| X8 | \(13x-8\) | polynomial remainder | PASS |
| X9 | \(2\) | recurrence from \(A_0,A_1\) | PASS |
| X10 | preserve/classify conflict | repository source-integrity contract | PASS |

**Audit result:** all 22 promoted practice/transfer outcomes independently checked.
