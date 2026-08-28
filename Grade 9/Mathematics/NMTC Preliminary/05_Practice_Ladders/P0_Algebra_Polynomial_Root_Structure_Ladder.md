# P0 Algebra — Polynomial & Root Structure Practice Ladder v1

## Ladder contract

Each mechanism progresses through:

`F0 -> F1 -> F2 -> F3 -> F4 -> PYQ -> XF`

- `F0 FOUNDATION` — prerequisite mechanic.
- `F1 DIRECT` — concept is visible.
- `F2 STANDARD` — one clean application.
- `F3 DISGUISED` — surface form hides the move.
- `F4 PRELIMINARY` — compact mixed reasoning under screening conditions.
- `PYQ` — verified/qualified Previous-Year anchor where available.
- `XF TRANSFER` — non-identical author-created problem preserving the invariant.

The learner must state the **first move** before solving from F2 onward.

Full third-party PYQ wording is not reproduced here; use stable IDs and source locators.

---

# Ladder 1 — Reduce high powers from a relation

## F0
If `x^2=2x+3`, express `x^3` in the form `ax+b`.

**Target first move:** multiply the relation by `x`, then reduce `x^2` again.

## F1
If `x^2+x-1=0`, express `x^4` as a linear expression in `x`.

## F2
If `t^2=3t-1`, find the remainder-form expression for `t^6` without solving for `t`.

## F3
A number `u` satisfies `u+1/u=3`. Find `u^3+1/u^3`.

**Hidden relation:** square/cube the reciprocal invariant, not the underlying quadratic roots.

## F4
A root `r` of `r^2+r+1=0` is used in a long expression containing powers up to `r^100`. Determine the useful power cycle before evaluating anything.

## PYQ
- `NMTC-BH-P-2018-Q06`
- `NMTC-BH-P-2023-Q03`
- `NMTC-BH-P-2024-Q01`

## XF
Let `z` satisfy `z^2-2z+2=0`. Evaluate a new expression such as `z^8-4z^7+...` designed to collapse after modular reduction. Change coefficients and target from every PYQ.

---

# Ladder 2 — Remainder / divisibility modulo a polynomial

## F0
Find the remainder when `x^3+2x+1` is divided by `x-2`.

## F1
Find the remainder of `x^10+x^3+1` modulo `x^2-1` using `x^2≡1`.

## F2
Find the remainder of `x^11+2x^5+7` modulo `x^2+1`.

## F3
A polynomial with unknown coefficient is divisible by `x^2+1`. Reduce all powers first and solve only the remainder coefficients.

## F4
A high-degree quotient/remainder problem has periodic signs after division by `x^2+1`. Determine the period before counting coefficients.

## PYQ
- `NMTC-BH-P-2019-Q08`
- `NMTC-BH-P-2024-Q05`
- `NMTC-BH-P-2024-Q16`

## XF
Use divisor `x^2+x+1` and ask for an unknown coefficient or high-power remainder. The solution must derive the cycle rather than copy the `x^2±1` pattern.

---

# Ladder 3 — Vieta before solving roots

## F0
For `x^2-9x+14=0`, state sum and product of roots.

## F1
Without finding roots, compute `alpha^2+beta^2`.

## F2
Without finding roots, compute `alpha/beta+beta/alpha`.

## F3
Given a quadratic with awkward irrational roots, compute a symmetric reciprocal expression.

## F4
A student solved the wrong quadratic and obtained two roots. Recover the intended coefficient, then evaluate a transformed-root expression without solving the corrected quadratic.

## PYQ
- `NMTC-BH-P-2024-Q14`

## XF
Create an original “wrong coefficient” or “shifted roots” problem with different coefficients and target such as `(alpha-beta)^2/(alpha beta)`.

---

# Ladder 4 — Positive/integer roots + equality/bounds

## F0
Positive numbers have sum 4 and product 1. What does AM-GM say about equality?

## F1
Four positive roots have sum 4 and product 1. Show what the roots must be.

## F2
Use the forced root multiset to recover a coefficient of the polynomial.

## F3
Positive integer roots have specified sum and pairwise-product sum. Enumerate the multiset before touching the constant term.

## F4
Before optimizing a symmetric expression under a product constraint, determine whether it is bounded.

## PYQ
- `NMTC-BH-P-2024-Q17` — clean scored equality-collapse anchor.
- `NMTC-BH-P-2023-Q17` — clean scored **unboundedness contrast**.

## Source-QC contrast
- `NMTC-BH-P-2025-Q20` — use only to show printed-stem/key sign conflict; not a canonical exercise.

## XF
Give positive roots with a different forced equality point or an unbounded reciprocal-scaling family and require the learner to decide `BOUND` vs `UNBOUNDED` before any inequality.

---

# Ladder 5 — Structural cubic/quartic factorization

## F0
Factor a cubic after being told one integer root.

## F1
Test `±1, ±2` as rational roots of a quartic with small integer constant.

## F2
Factor a quartic into a linear factor and cubic/quadratic, then stop when the target no longer needs all roots.

## F3
Rewrite a symmetric high-degree expression using `s=x+y`, `p=xy`.

## F4
Given two high-degree symmetric equations, reduce to a low-degree relation before evaluating a target.

## PYQ
- `NMTC-BH-P-2019-Q25`
- `NMTC-BH-P-2024-Q24`

## XF
Construct a reciprocal or palindromic quartic requiring `t=x+1/x`, with coefficients unrelated to the PYQs.

---

# Ladder 6 — Common-root elimination

## F0
If a number satisfies two linear equations, eliminate the number to get a parameter relation.

## F1
If `r` is a common root of a quadratic and cubic, use the quadratic to reduce `r^3` in the cubic.

## F2
Eliminate the highest power by multiplying/subtracting the two polynomial equations.

## F3
Two polynomials with parameters share a root; derive a parameter equation without solving either polynomial completely.

## F4
Choose between:

- resultant-like elimination by hand;
- factor theorem;
- explicit root solving.

Justify the cheapest path.

## PYQ evidence
- `NMTC-BH-P-2023-Q16` — `BONUS_EVIDENCE`, not ordinary scored anchor.

## XF
Author-created scored-level common-root problem with smaller degree/clean coefficients. It must be the canonical teaching target because the available PYQ evidence is bonus-only.

---

# Ladder 7 — Function/root transformations

## F0
If `f(x)=x^2-3x+2`, expand `f(y-1)`.

## F1
Given roots of `f(x)`, determine how roots shift under `f(x+1)`.

## F2
Form an equation whose roots are `alpha+2,beta+2` using new sum/product.

## F3
Form an equation whose roots are `1/alpha,1/beta`, including the condition that neither root is zero.

## F4
A function equation is shifted and then a root-symmetric expression is requested. Choose between variable substitution and direct transformed-root Vieta.

## PYQ
- `NMTC-BH-P-2024-Q22`

## XF
Use a shift of `-3` plus reciprocal target, forcing the learner to combine variable translation and Vieta.

---

# Mixed Preliminary speed lab

## Round A — recognition only

For 20 short prompts, student writes one code only:

- `PR` = power reduction;
- `VT` = Vieta;
- `RM` = remainder/mod-polynomial;
- `FT` = factor first;
- `IR` = integer-root constraint;
- `CR` = common-root elimination;
- `SH` = shift/transformed roots;
- `BD` = bound/equality check.

Target: `>=16/20` correct without calculation.

## Round B — first line only

For 12 prompts, write only the first mathematical line.

Target: `>=10/12` structurally correct.

## Round C — compact solve

8 mixed F3/F4 items.

Target: `>=6/8` correct with no source/domain violations.

## Round D — PYQ/XF alternation

Alternate one qualified PYQ anchor with one non-identical transfer from the same family.

Passing requires success on **both**. Solving only the familiar PYQ is not mastery.

---

# Error-analysis tags

Every wrong answer must be classified as one of:

- `SOLVED_WHEN_REDUCTION_WAS_ENOUGH`;
- `EXPANDED_BEFORE_FACTORING`;
- `VIETA_SIGN_ERROR`;
- `ROOTS_SOLVED_UNNECESSARILY`;
- `WRONG_DIVISOR_ZERO`;
- `POLYNOMIAL_MOD_CYCLE_ERROR`;
- `IGNORED_INTEGER_POSITIVE_CONSTRAINT`;
- `FAILED_BOUNDEDNESS_CHECK`;
- `DOMAIN_ERROR`;
- `SOURCE_CONFLICT_NOT_FLAGGED`.

The remediation set should be selected by error tag, not simply by giving “more hard questions.”
