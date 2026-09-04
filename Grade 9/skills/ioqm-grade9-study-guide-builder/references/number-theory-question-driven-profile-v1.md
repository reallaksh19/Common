# Number Theory Question-Driven Study Guide Profile v2

**Purpose:** specialize the generalized study-guide builder for Grade 9 IOQM-style Number Theory using the v5 corpus decomposition and the v7/v8 student-surface rebuild lessons.

This profile keeps the 36-skill decomposition demonstrated by the 90-question architecture while requiring concept assimilation and loss-preserving compact packaging.

## 1. Learner objective

Teach a partially prepared Grade 9 learner to move from:

```text
surface wording
-> arithmetic structure
-> representation
-> legal first move
-> execution
-> variant / transfer recognition
-> legality / boundary check
```

The learner may remember standard school facts but should not be assumed to recognize the correct engine in a non-routine problem.

## 2. Stable skill granularity

Keep umbrella concepts only for navigation. Split executable skills when recognition, representation, first move, or legality differs.

The validated Number Theory registry contains 36 stable skills:

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

A new corpus may add or split skills if the Opening Signature requires it.

## 3. Required splits

Do not collapse:

```text
factorisation
-> powers / manufactured fixed product / consecutive-factor polynomial

digit sum
-> congruence/bounds / exact carries

recurrence
-> modular recurrence / overlapping-window subtraction

counting
-> fixed multiplicity / residue obstruction / square gaps / shared-prime graph
```

## 4. Dependency order

Recommended order:

```text
integer structure
-> Euclid / prime exponents / divisor functions
-> Bezout / congruence legality / inverses / CRT
-> cycles / Euler-Fermat / Wilson / last digits / exponential gcd
-> valuations / zeros / perfect powers / reduced residues
-> factor engines / filters / gcd-lcm normalisation / Pythagorean / consecutive sums
-> digits / bases / digit sums / carries
-> floors / recurrences / windows / counting / extremal / graph
-> mixed method selection
-> transfer labs
```

## 5. Number Theory concept-assimilation pattern

The v7 compact reference showed that a theorem sentence + FIRST MOVE + tiny example is often a revision card, not enough for first-time assimilation.

For unfamiliar/strategic skills, use a teacher-like flow:

```text
WHAT IS THIS?
TINY EXAMPLE
THE IOQM LINK
WHY IT WORKS
FIRST MOVE with numbers/symbols
VARIANTS AND CLOSE CONTRASTS
WATCH OUT with a real failure case
CHECK with executed verification
GUIDED PRACTICE
PRACTISE NEXT
```

Use these as roles, not equal-weight boxes.

### Example - Bezout / linear Diophantine

Before saying "test the gcd", explain what a linear Diophantine equation is and what Bezout means.

Tiny example:

```text
7 = 3(14) - 35
```

so integer combinations of 14 and 35 produce multiples of 7 but not 10.

Concrete FIRST MOVE:

```text
84x + 126y = 30

gcd(84,126)=42
42 does not divide 30
STOP: no integer solutions.
```

Variant coverage should include unrestricted integer solutions, positivity/range restrictions, congruence form, and more than two coefficients when relevant.

## 6. Legality must be concrete

High-risk checks include:

- modular cancellation / inverse gcd condition;
- CRT compatibility;
- order/Euler coprimality;
- Wilson prime modulus;
- Legendre prime valuation;
- factor-pair sign/parity/order restoration;
- base digit validity;
- strict floor endpoint;
- recurrence full-state repetition;
- primitive Pythagorean coprimality/opposite parity.

Prefer mathematical counterexamples and executed checks over generic prose.

## 7. Transfer labs

The 90-question architecture contains compound transfers beyond the 36 core skills. Preserve them in compact editions.

Representative labs include:

- zero-stripped factorials;
- idempotents modulo powers of 10;
- complete unit-group products;
- two-adic filtering through phi;
- reduced-residue sums plus geometric series;
- gcd of several linear forms;
- exponential gcd parity variants;
- last nonzero factorial digits;
- modular inverse periodic expansions;
- nested floors and roots;
- exact carry transfers;
- nested base/digit-sum minimisation;
- moving square intervals;
- gcd/lcm shape normalisation;
- squarefree polynomial values;
- divisor-count congruence from perfect powers;
- least exponent for a terminal block;
- factorial quotient integrality;
- square roots modulo powers of 10;
- same digit string in two bases;
- prime-triple cubic quotient;
- sum=product with ones;
- fourth-power injectivity modulo a prime;
- period of n^n modulo a prime;
- fixed-hypotenuse primitive Pythagorean counting.

Bridge count remains evidence-driven; these are demonstrated obligations, not a universal quota.

## 8. Student-facing transfer navigation

Use:

```text
Q003 -> Zero-stripped factorials -> review Valuations + Trailing zeros
```

not:

```text
Q003 -> NT-A01 + NT-VAL-01 + NT-ZEROS-01
```

IDs remain secondary build/retrieval anchors.

## 9. Practice Map

Practice Map means readable skill -> corpus question IDs. It must stay separate from the reviewer matrix and from Appendix B.

For questions with extra transfer edges, add a readable Transfer Map rather than expanding the core Practice Map into an engineering table.

## 10. Structural visuals

High-value forms include:

- exponent-choice grid;
- CRT split/merge lanes;
- residue cycle;
- valuation pipeline;
- fixed-product rectangle;
- Diophantine solution-line schematic;
- carry columns;
- base place-value diagram;
- floor interval number line;
- square-gap number line;
- shared-prime graph;
- Pythagorean parameter triangle.

Use only when they reduce reasoning load.

## 11. Packaging

The compact Number Theory reference is naturally suited to:

```text
REFERENCE_PLUS_PRACTICE_BOOK
```

when the frozen 90-question corpus remains beside it.

The reference may omit the 90 stems, but the package must retain 90/90 question routes, including transfer edges.

Do not describe the reference alone as self-contained.

## 12. Prototype gate

Before bulk generation, render and inspect at least:

- Bezout/Diophantine concept page;
- CRT or last-digits page;
- a visual skill page (e.g. carry/floor/graph);
- mixed router;
- Practice/Transfer Map.

Reject low contrast, broken heading colors, off-page tables, tiny navigation, raw-ID dominance, or card-stack pages that do not teach the mechanism.

## 13. Number Theory gates

```text
NT_STABLE_SKILLS = PASS_36_OF_36
NT_QUESTION_SUPPORT_PACKAGE = PASS_90_OF_90
NT_TRANSFER_EDGE_MANIFEST = PASS_90_OF_90
NT_HARD_TRANSFER_GAPS_WITHOUT_LAB = 0
NT_FACTORISATION_ENGINE_SPLIT = PASS
NT_DIGSUM_CARRY_SPLIT = PASS
NT_RECURRENCE_WINDOW_SPLIT = PASS
NT_COUNTING_ENGINE_SPLIT = PASS
NT_CONCEPT_ASSIMILATION = PASS_36_OF_36
NT_FIRST_MOVE_CONCRETE = PASS_36_OF_36
NT_TRANSFER_MAP_READABLE_NAME_FIRST = PASS
NT_RAW_IDS_PRIMARY_NAVIGATION = 0
NT_REQUIRED_VISUALS_MISSING = 0
```

These are static document/package checks, not learner-outcome claims.

## Final Number Theory rule

The student should not merely recognize theorem names. The student should be able to explain the idea, choose the representation, write a concrete first move, distinguish the subtle nearby variant, execute the route, and check the legality.
