# P2 Mathematical Induction — F0 -> F4 -> XF Ladder

All items are author-created unless explicitly tagged otherwise.

## Family 1 — Proposition and base

- F0: state `P(n)` for `1+...+n=n(n+1)/2`.
- F1: identify the base for a claim valid for `n>=3`.
- F2: repair a proof that tests `n=1` for a claim beginning at `n=4`.
- F3: distinguish domain `n>=0` from `n>=1` in an exponent inequality.
- F4: given a false early case but true later pattern, identify the earliest plausible induction start.
- XF: explain why a correct induction step cannot rescue a false starting case.

## Family 2 — Sum identities

- F0: prove `1+3+...+(2n-1)=n^2`.
- F1: prove `2+4+...+2n=n(n+1)`.
- F2: prove `1+2+...+n=n(n+1)/2`.
- F3: prove `1^2+...+n^2=n(n+1)(2n+1)/6`.
- F4: prove a weighted sum identity after algebraic simplification.
- XF: decide whether telescoping is cheaper than induction for a supplied finite sum.

## Family 3 — Products

- F0: append the next factor to a finite product.
- F1: prove `2*4*...*2n=2^n n!`.
- F2: prove a factorial/product identity.
- F3: handle a product beginning at `n=2`.
- F4: prove a rational product formula where cancellation must be preserved.
- XF: compare induction with direct telescoping product simplification.

## Family 4 — Divisibility

- F0: prove `5 | (6^n-1)`.
- F1: prove `7 | (8^n-1)`.
- F2: prove `3 | (4^n-1)`.
- F3: prove `8 | (3^(2n)-1)`.
- F4: prove a divisibility claim with a two-term recurrence in the expression.
- XF: reject induction when direct factorization of `n^3-n` is shorter.

## Family 5 — Inequalities

- F0: prove `2^n>=n+1` for `n>=0`.
- F1: prove `3^n>n^2` for `n>=2`.
- F2: prove `n!>=2^(n-1)` for `n>=1`.
- F3: prove a rational inequality requiring an extra monotonic comparison.
- F4: identify the correct threshold before proving an exponential-polynomial inequality.
- XF: diagnose an induction proof whose auxiliary inequality fails at small k.

## Family 6 — Recurrence verification

- F0: verify `a_n=3*2^(n-1)-1` for `a_1=2, a_{n+1}=2a_n+1`.
- F1: verify a linear recurrence closed form.
- F2: verify a recurrence with an additive n-term.
- F3: verify a Fibonacci-type identity with two base cases.
- F4: choose ordinary vs strong/multi-case induction.
- XF: explain why verification is not the same as discovering the formula.

## Family 7 — Step size and multiple bases

- F0: if `P(k)->P(k+2)`, identify missing coverage.
- F1: establish bases `P(1),P(2)`.
- F2: trace which integers each base reaches.
- F3: generalize to step size 3.
- F4: repair a proof that proves only one residue class.
- XF: formulate the minimal base set for a step-size-r induction.

## Family 8 — Strong induction

- F0: distinguish `P(k)` from `P(1)...P(k)`.
- F1: prove a two-previous-term recurrence property.
- F2: prove every integer `n>=2` can be written as a product of primes or is prime (ceiling bridge).
- F3: use earlier decompositions to prove a representation claim.
- F4: decide whether strong induction is necessary or merely convenient.
- XF: rewrite a strong induction proof as ordinary induction on a strengthened proposition.

## Family 9 — Broken proof repair

- F0: missing base.
- F1: assumes `P(k+1)`.
- F2: changes domain during proof.
- F3: proves `P(k)->P(k+2)` with one base.
- F4: uses division by an expression that can be zero.
- XF: identify the earliest invalid logical step in a polished-looking fake proof.

## Family 10 — Method selection / source integrity

- F0: direct factorization vs induction.
- F1: congruence vs induction.
- F2: telescoping vs induction.
- F3: recurrence solving vs induction verification.
- F4: source claims “official induction PYQ” without provenance.
- XF: choose the cheapest valid proof and separately classify its source status.
