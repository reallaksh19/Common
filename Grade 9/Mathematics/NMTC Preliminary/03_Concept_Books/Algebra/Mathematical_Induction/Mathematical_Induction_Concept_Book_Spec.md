# Mathematical Induction — Concept Book Specification

## Cognitive contract

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Proof-performance spine:

`STATEMENT -> START -> HYPOTHESIS -> BRIDGE -> CLOSE -> CHECK`

The learner should finish this unit believing:

> Induction is not “assume the answer.” It is a mechanism for proving that truth propagates from one integer to the next.

---

# Unit 0 — Diagnostic prerequisites

Check fluency with:

- algebraic identities and factorization;
- sigma / finite-sum notation;
- divisibility notation;
- inequalities;
- recursive definitions;
- the distinction between an example and a proof.

If these fail, repair them before induction.

---

# Unit 1 — Why examples do not prove a universal statement

## SEE

A statement can be true for `n=1,2,3,4,5` and still fail later.

## REALIZE

Finite checking establishes only finitely many cases.

## UNDERSTAND

Induction proves a **link**:

`P(k) true -> P(k+1) true`.

Together with a true first case, that link propagates indefinitely through the allowed integer domain.

## CONTRAST

- checking ten cases;
- proving the next-case implication.

The second is the proof engine.

---

# Unit 2 — State P(n) exactly

Students must write the proposition before manipulating it.

Example:

`P(n): 1+2+...+n = n(n+1)/2`.

Do not start with “assume for k” before the proposition and domain are explicit.

Mandatory details:

- variable;
- domain (`n>=1`, `n>=2`, etc.);
- exact equality/divisibility/inequality claim.

---

# Unit 3 — The base case is structural, not ceremonial

The correct start is the smallest index in the claim.

If the statement is valid for `n>=2`, testing `n=1` is irrelevant and may even be false.

Train:

`Find n0 -> verify P(n0) -> then begin the induction step.`

Contrast:

- statement valid for all `n>=1`;
- statement valid only for `n>=4`.

---

# Unit 4 — The induction hypothesis

Write:

`Assume P(k) is true for an arbitrary integer k>=n0.`

Then write the exact usable relation.

Wrong forms:

- assume `P(k+1)`;
- assume the theorem is true for all n;
- use a stronger claim without proving it;
- substitute convenient numerical values for k.

---

# Unit 5 — Build P(k+1) from the new case

Start from the **left side / defining object of P(k+1)** whenever possible.

For sums:

`S_{k+1}=S_k + new term`.

For products:

`A_{k+1}=A_k * new factor`.

For powers/divisibility:

factor the `k+1` expression until the induction hypothesis appears.

For inequalities:

use the induction hypothesis, then prove the remaining comparison needed to reach the `k+1` target.

This unit is the main first-move training target.

---

# Unit 6 — Sum identities

Derive/verify by induction:

- `1+2+...+n = n(n+1)/2`;
- `1+3+...+(2n-1)=n^2`;
- `1^2+2^2+...+n^2 = n(n+1)(2n+1)/6` as a higher algebra bridge.

The formula may be discovered elsewhere; induction proves it once conjectured.

Wrong move:

> Treating induction as the method that necessarily discovers the closed form.

---

# Unit 7 — Divisibility statements

Patterns:

- `6 | (n^3-n)` for every positive integer n;
- `5 | (6^n-1)` for every positive integer n;
- more generally, when moving from k to k+1, factor the increment into a multiple of the required divisor plus the induction-hypothesis term.

Students must distinguish:

- divisibility proof;
- congruence shortcut;
- direct factorization that may be simpler than induction.

Method selection matters.

---

# Unit 8 — Inequalities

Teach only with domain control.

Example:

`2^n >= n+1` for `n>=0`.

Induction step:

`2^(k+1)=2*2^k >= 2(k+1) >= k+2` for `k>=0`.

A second example should begin at a later index, e.g. `3^n>n^2` for `n>=2`, to force start-index awareness.

Mandatory check:

The extra inequality used in the step must itself be valid on the induction domain.

---

# Unit 9 — Recurrence verification

Induction can verify a proposed formula for a recursively defined sequence.

Example architecture:

- recurrence supplied;
- candidate closed form supplied or previously derived;
- base case;
- substitute the induction hypothesis into the recurrence;
- recover the candidate formula for `k+1`.

Connect to the Sequence & Series overlay without relabeling its PYQs as induction questions.

---

# Unit 10 — Strong induction and multiple-base cases

Use only after ordinary induction is secure.

Strong hypothesis:

`P(n0), P(n0+1), ..., P(k)` are all assumed true to prove `P(k+1)`.

Use when the next case naturally depends on more than one earlier case.

Examples:

- recurrence depending on two previous terms;
- integer decomposition / factorization existence arguments.

Teach that strong induction is logically equivalent in strength to ordinary induction; it changes the usable hypothesis structure.

---

# Unit 11 — Broken proof laboratory

Students must diagnose:

1. missing base case;
2. wrong base index;
3. assuming `P(k+1)`;
4. circular algebra;
5. proving only `P(k)->P(k+2)` with insufficient starting cases;
6. using an inequality valid only for large k without checking the threshold;
7. changing the proposition halfway through;
8. checking examples and calling it induction.

---

# Unit 12 — Preliminary first-move laboratory

Before solving, classify:

- `SUM_ADD_TERM`;
- `PRODUCT_ADD_FACTOR`;
- `DIVISIBILITY_FACTOR_INCREMENT`;
- `INEQUALITY_BOUND_STEP`;
- `RECURRENCE_SUBSTITUTE_HYPOTHESIS`;
- `STRONG_INDUCTION_DEPENDS_ON_MULTIPLE_PRIOR_CASES`;
- `INDUCTION_NOT_CHEAPEST`.

The student must write the first useful line before completing the proof.

---

# Mastery standard

Student is ready when they can:

1. state `P(n)` and its domain correctly in 9/10 prompts;
2. identify the correct base index in 9/10 prompts;
3. write a valid induction hypothesis in 9/10 prompts;
4. produce the first useful `k+1` line in at least 8/10 mixed prompts;
5. complete identities/divisibility/inequality/recurrence proofs;
6. repair at least 4/5 broken proofs;
7. explain when induction is valid but strategically inferior to a direct proof.

## Source boundary

This package is `SYLLABUS_FIRST`. No fabricated PYQ recurrence or year/question labels are permitted.
