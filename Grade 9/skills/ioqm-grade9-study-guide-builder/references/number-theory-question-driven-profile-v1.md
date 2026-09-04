# Number Theory Question-Driven Study Guide Profile v1

**Purpose:** specialize the generalized study-guide builder for Grade 9 IOQM-style Number Theory using the production lessons demonstrated by the Number Theory v5 rebuild.

This profile specializes the v3 Analysis Engine / Student Book Generator contract. It does not weaken source custody, hint leakage, difficulty, visual, answer, or PDF-QA rules.

---

## 1. Learner objective

Teach a partially prepared Grade 9 learner to move from:

```text
surface wording
-> arithmetic structure
-> the right representation
-> a legal first move
-> finite execution
-> legality / boundary check
```

The learner may remember divisibility tests, standard factorisations, gcd/lcm formulas, modular arithmetic, or elementary prime factorisation, but should not be assumed to recognize which engine applies in a non-routine problem.

---

## 2. Number Theory skill granularity

Number Theory is especially vulnerable to umbrella labels that are too broad to be teachable first-step units.

Split by actual opening signature.

Examples from the v5 rebuild:

```text
FACTORISATION umbrella
-> NT-FACT-POW-01   difference/sum of powers
-> NT-FACT-SFFT-01  manufactured fixed-product factorisation
-> NT-FACT-POLY-01  polynomial to consecutive/near-consecutive factors

DIGIT SUM umbrella
-> NT-DIGSUM-01     congruence + bounded digit-sum structure
-> NT-CARRY-01      exact -9 per carry accounting

RECURRENCE umbrella
-> NT-REC-01        reduce affine recurrence modulo target
-> NT-WINDOW-01     subtract overlapping windows

COUNTING umbrella
-> NT-COUNT-01      fixed multiplicity / direct digit choices
-> NT-PIGEON-01     residue-class obstruction
-> NT-SQUAREGAP-01  monotone square-gap extremal reasoning
-> NT-PRIMEGRAPH-01 shared-prime graph modelling
```

These are not cosmetic subdivisions. They differ in recognition, representation, first move, or legality.

---

## 3. Stable skill registry demonstrated by the v5 rebuild

The rebuild resolved the teaching core into 36 stable skills:

1. `NT-DIV-01` - Divisibility and the Division Algorithm
2. `NT-GCD-01` - Euclidean Algorithm, GCD and LCM
3. `NT-PRIME-01` - Euclid's Lemma, FTA and prime-exponent thinking
4. `NT-DIVCNT-01` - Exponent vectors and divisor functions
5. `NT-DIO-LIN-01` - Bezout and linear Diophantine equations
6. `NT-MOD-01` - Congruence arithmetic and cancellation legality
7. `NT-MODINV-01` - Linear congruences and modular inverses
8. `NT-CRT-01` - Constructive CRT, including non-coprime moduli
9. `NT-ORDER-01` - Short residue cycles and multiplicative order
10. `NT-EULER-01` - Fermat, Euler and Euler phi
11. `NT-WILSON-01` - Wilson's theorem
12. `NT-LASTDIG-01` - Last digits by prime-power splitting and CRT
13. `NT-EXPGCD-01` - GCDs of exponential expressions
14. `NT-VAL-01` - Valuations and Legendre's formula
15. `NT-ZEROS-01` - Trailing zeros and last nonzero digits
16. `NT-POWER-01` - Perfect powers and squarefree structure
17. `NT-RESIDUE-01` - Reduced residues, phi sums and unit products
18. `NT-FACT-01` - Factorisation-engine method-selection umbrella
19. `NT-FACT-POW-01` - Difference/sum-of-powers factorisation
20. `NT-FACT-SFFT-01` - Manufactured factorisation and fixed-product forms
21. `NT-FACT-POLY-01` - Polynomial-to-consecutive-factor factorisation
22. `NT-FILTER-01` - Parity, bounds, discriminants and admissibility filters
23. `NT-GCDNORM-01` - GCD/LCM normalisation
24. `NT-PYTH-01` - Primitive Pythagorean triples
25. `NT-CONSUM-01` - Consecutive sums and odd-divisor structure
26. `NT-DIGIT-01` - Decimal place value, concatenation and deletion
27. `NT-BASE-01` - Other bases and digit validity
28. `NT-DIGSUM-01` - Digit-sum congruence and bounded digit sums
29. `NT-CARRY-01` - Exact carry accounting
30. `NT-FLOOR-01` - Floor functions as half-open intervals
31. `NT-REC-01` - Affine recurrences modulo a target
32. `NT-WINDOW-01` - Overlapping-window cancellation
33. `NT-COUNT-01` - Fixed-multiplicity and digit-choice counting
34. `NT-PIGEON-01` - Small-prime and residue-class obstruction
35. `NT-SQUAREGAP-01` - Monotone square-gap extremal reasoning
36. `NT-PRIMEGRAPH-01` - Shared-prime graph model

Do not treat this registry as a universal syllabus cap. A new corpus may require a split or a new stable skill. Any addition must pass the opening-signature test.

---

## 4. Dependency order

A strong default dependency sequence is:

```text
integer structure
-> gcd / Euclidean algorithm
-> prime-exponent thinking
-> divisor functions
-> Bezout / linear Diophantine
-> congruence legality
-> inverses
-> CRT
-> short cycles / order / Euler / Wilson
-> decimal last-digit structure
-> valuations / factorial prime supply
-> perfect-power structure
-> integer-equation factor engines and filters
-> gcd/lcm normalisation and classical parametrisations
-> digits / bases
-> digit sums / exact carries
-> floors / recurrences / windows
-> counting / residue obstruction / extremal / graph bridges
-> mixed method selection
-> advanced transfer bridges
```

The exact chapter grouping may change, but the dependency logic must remain explicit.

---

## 5. Recognition -> first move examples

Number Theory support should be executable, not theorem-name-only.

Examples:

```text
same remainder
-> subtract expressions
-> write a divisibility/congruence statement

huge gcd of a^m-1 and a^n-1
-> reduce exponent pair by gcd / Euclidean structure

non-coprime modular cancellation
-> compute gcd(coefficient, modulus) first

CRT with non-coprime moduli
-> test compatibility before merging

last k decimal digits
-> consider 10^k = 2^k 5^k and CRT

n! contains p^r
-> compute v_p(n!)

gcd and lcm both unknown
-> write a = dx, b = dy, gcd(x,y)=1

unknown base numeral
-> expand place value and enforce digit < base before solving

exact digit-sum change under addition
-> count carries, not only mod 9

equal overlapping window sums
-> write adjacent windows and subtract

floor equality
-> convert to a half-open interval first
```

---

## 6. Legality is part of the method

Number Theory has many transformations that are easy to perform illegally.

Every relevant skill should teach the boundary condition beside the method:

- cancellation modulo `m` requires invertibility or correct modulus reduction;
- modular inverse exists only under the gcd solvability condition;
- CRT with non-coprime moduli requires compatibility;
- Euler/Fermat require their hypotheses;
- multiplicative order requires an invertible base;
- Wilson requires prime modulus;
- Legendre's formula uses prime valuation;
- factor-pair enumeration must restore parity/sign/ordering/integrality;
- unknown-base numerals require every digit to be valid;
- floor upper endpoints are strict;
- recurrence period claims require the relevant state to repeat;
- Pythagorean parametrisation needs coprimality/parity conditions in the primitive case.

A legality note should not be hidden in reviewer prose.

---

## 7. Student page grammar

For stable skills use the simple student surface:

```text
REMEMBER
SEE THE IDEA
TRY IT
FIRST MOVE
WATCH OUT
PRACTISE
```

Number Theory particularly benefits from a visually prominent FIRST MOVE because learners often know the theorem but fail to identify the legal opening.

Examples:

```text
FIRST MOVE
Before cancelling, compute gcd(c,m).
```

```text
FIRST MOVE
Write 10^k = 2^k 5^k.
```

```text
FIRST MOVE
Set a = dx, b = dy with gcd(x,y)=1.
```

```text
FIRST MOVE
Write k <= X < k+1.
```

The page may include a smaller `WHY` or `CHECK` sublabel, but these are subordinate to the main student anchors.

---

## 8. Method-selection router

After the learner has attempted an unaided Quick Check, teach a compact router based on discriminators rather than theorem names.

Useful decision boundaries:

| Nearby choices | Correct discriminator |
|---|---|
| divisibility vs congruence | Is a modulus/remainder already visible? |
| short cycle vs Euler | Is a tiny proven cycle easier, and is the base coprime? |
| Euler vs order | Need any valid period or the least period? |
| CRT vs one modulus | Does splitting expose prime-power structure? |
| divisor count vs valuation | Counting divisors or measuring exponent supply? |
| digit sum mod 9 vs carries | Congruence-only information or exact change? |
| factorisation vs bounds | Can the equation become a fixed product immediately? |
| gcd/lcm formula vs normalisation | Do both gcd and lcm occur with unknown numbers? |
| floor algebra vs interval | Interval first; ordinary algebra afterward. |
| counting vs pigeonhole | Count legal objects, or prove unavoidable repetition/obstruction? |

The router is a retrieval aid, not a pre-diagnostic hint sheet.

---

## 9. Worked Bridge policy

The Number Theory v5 rebuild expanded bridges only after question-to-method analysis exposed transfer gaps.

Preserve that policy:

```text
bridge count = transfer-gap evidence
not = fixed chapter quota
```

A Number Theory bridge is especially useful when a normal skill page does not prepare a half-ready learner for a compound representation such as:

- valuation + zero stripping;
- idempotents modulo powers of 10;
- complete unit-group products;
- divisor-count constraints on perfect powers;
- nested digit-sum minimisation;
- floor boundary jumps;
- factorial quotient integrality;
- square roots modulo powers of 10;
- same digit string in two bases;
- prime-structure graph modelling;
- fixed-hypotenuse primitive Pythagorean triples.

The bridge should end with a transfer prompt, not the original corpus answer.

---

## 10. Visual pedagogy

Use structural visuals only when they offload real reasoning.

High-value Number Theory visual forms include:

- exponent-vector grids;
- CRT split/merge diagrams;
- valuation supply bars;
- carry columns;
- base place-value diagrams;
- floor half-open interval number lines;
- recurrence state/period arrows;
- overlapping-window cancellation diagrams;
- residue/pigeonhole cycle strips;
- shared-prime graphs;
- Pythagorean parameter sketches.

Reject decorative prime-number imagery or generic number-themed art.

---

## 11. Appendix A hints

For a partial-knowledge learner, use plain-language local help:

```text
NOTICE
recognition clue only

RECALL
readable stable skill name; stable ID may appear secondarily

START
first executable setup only
```

Do not make `H1/H2/H3` the main student labels.

Use less support on later attempts.

Every Appendix A question still requires an auditable route to a taught stable skill/bridge even if the learner does not open the hint.

---

## 12. Short-horizon route

A Number Theory 3-day student edition may use:

```text
Day 1 - recognize
Quick Check -> fix weak high-value skills -> 1-2 practice questions each

Day 2 - practise
same skills, new questions, less help

Day 3 - mix
unlabelled mixed questions; repair repeated mistakes only
```

A Quick Check should test first-move recognition rather than full solutions.

Priority remains separate from authored difficulty.

---

## 13. Student edition publication boundary

The learner-facing artifact should not require the student to read production evidence.

Preferred student edition contains:

- simple Navigator when useful;
- dependency-ordered reference core;
- targeted Worked Bridges;
- quiet support map;
- Appendix A deliberate practice;
- Appendix B reliable-source mixed challenges;
- Appendix C compact memory helper.

Reviewer/build evidence belongs in a separate dossier or clearly separated reviewer artifact.

Do not put `PR140`, gate tables, corpus-custody matrices, or production-state labels into the normal student page header.

---

## 14. Number Theory gates

Recommended domain gates:

```text
NT_STABLE_SKILL_SPLIT_AUDIT = PASS
NT_ORPHAN_METHODS = 0
NT_MODULAR_LEGALITY_COVERAGE = PASS
NT_FACTORISATION_ENGINE_SPLIT = PASS
NT_DIGSUM_CARRY_SPLIT = PASS
NT_RECURRENCE_WINDOW_SPLIT = PASS
NT_COUNTING_ENGINE_SPLIT = PASS
NT_HARD_TRANSFER_GAPS_WITHOUT_BRIDGE = 0
NT_FIRST_MOVE_PROMINENCE = PASS_n_OF_n
NT_STUDENT_HINT_LABELS_PLAIN_LANGUAGE = PASS_n_OF_n
```

These are static document gates, not learner-outcome claims.

---

## Final Number Theory rule

The student should not finish a Number Theory chapter merely knowing more theorems.

The student should become faster at deciding:

```text
What structure is hiding here?
What representation compresses it?
What is the first legal move?
What condition could make that move invalid?
```
