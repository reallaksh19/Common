# Number Theory Question-Driven Study Guide Profile v3

**Purpose:** specialize the Grade 9 platform + IOQM builder for Number Theory using the 90-question corpus analysis and the later student-surface rebuild lessons.

This profile deliberately removes the earlier mistake of treating the demonstrated 36-skill analysis as a learner-facing target. The 36 nodes remain useful evidence from one corpus; they are **not a golden syllabus, chapter count, concept count, or page target**.

---

## 1. Learner objective

Teach a partially prepared Grade 9 learner to move from:

```text
surface wording
-> arithmetic structure
-> useful representation
-> legal first move
-> execution
-> subtle variant / transfer recognition
-> legality / boundary check
```

The learner may remember formulas and school procedures but should not be assumed to recognize the correct engine in a non-routine problem.

---

## 2. Syllabus first, corpus second

Begin with the intended Number Theory syllabus/scope. Then use the frozen contest corpus to discover which concepts, variants, representations and transfer edges require teaching depth.

The corpus audits the syllabus-based teaching architecture; it does not become the syllabus by accident.

Typical Number Theory syllabus families include:

- divisibility and integer structure;
- gcd/lcm and Euclidean algorithm;
- prime factorisation and exponent thinking;
- Diophantine equations;
- congruences and modular equations;
- CRT;
- powers modulo integers;
- factorials, valuations and trailing zeros;
- perfect powers/squarefree structure;
- integer factorisation engines and admissibility filters;
- classical integer parametrisations;
- decimal/base representations, digit sums and carries;
- floor/recurrence/window methods;
- number-theoretic counting, extremal and graph bridges.

New research/corpora may justify additional or differently grouped teaching units.

---

## 3. Demonstrated 90-question analysis nodes - evidence, not a quota

The earlier 90-question architecture resolved support into these 36 internal stable nodes:

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

These are **internal support nodes** demonstrated by that corpus.

Do not require the student book to contain exactly 36 units.

Examples:

- congruence cancellation + linear congruences + modular inverses may form one coherent learner journey;
- last digits may need several learner episodes even though one internal node stores the core support;
- valuations + trailing zeros may be best taught as one linked sequence with multiple variants;
- a future corpus may require a new split or a new concept entirely.

Success is 100% required concept assimilation and question support, not `36/36` as a page count.

---

## 4. Required internal split examples

Keep umbrella concepts only for navigation when actual openings differ.

Do not collapse internally:

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

The learner-facing book may later regroup these when the resulting concept journey is clearer.

---

## 5. Dependency and concept-link examples

A strong default dependency flow is:

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
-> corpus-driven transfer labs
```

Show important learner-visible links when useful:

```text
GCD -> Bezout -> modular inverse -> CRT
```

```text
prime factorisation -> exponent vectors -> divisor count -> perfect powers -> valuations
```

```text
place value -> unknown bases -> digit sums -> carries
```

```text
cycles/order -> Euler/Fermat -> last digits -> CRT/valuation split
```

---

## 6. Difficulty model and badges

Use the Grade 9 Mathematics difficulty vector underneath every scored concept/question where practical:

```text
conceptual
recognition
reasoning_steps
algebra
hidden_structure
constraints_cases
calculation_burden
trap_density
```

Student badges are summaries.

### Concept badge

Use a range when transfer is materially harder than the core:

```text
Chinese Remainder Theorem
[CORE D3] [TRANSFER D5] [HIGH-YIELD]
```

### Question badge

```text
Q17 [D4 ADVANCED] [TRANSFER] [OFFICIAL PYQ]
```

### Learner-specific badge

Only after diagnosis:

```text
[YOUR STATUS: DEVELOPING] [DO FIRST]
```

Never collapse authored difficulty, learner mastery and personalized priority.

---

## 7. Number Theory concept-assimilation pattern

A theorem sentence + FIRST MOVE + tiny example may be enough for revision, but often not for first-time assimilation.

For unfamiliar/strategic concepts, use a teacher-like flow chosen from:

```text
WHAT IS THIS?
TINY CONCRETE EXAMPLE
CONNECTS TO...
THE IOQM LINK
WHY IT WORKS
COMPLETE WORKED EXAMPLE
FIRST MOVE with numbers/symbols
VARIANT
SUBTLE VARIANT / CLOSE CONTRAST
WATCH OUT with a real failure case
CHECK with executed verification
VISUAL HELPER
GUIDED PRACTICE
NOTICE / RECALL / START
INDEPENDENT PRACTICE
```

These are teaching roles, not mandatory equal-weight cards.

A simple concept may take half a page. A major linked concept may take several pages.

Page count is not a quality metric.

---

## 8. Example - Bezout / linear Diophantine

Before saying `test the gcd`, explain what a linear Diophantine equation is and what Bezout means.

Tiny example:

```text
7 = 3(14) - 35
```

so integer combinations of 14 and 35 can produce every multiple of 7 but not 10.

Concrete FIRST MOVE:

```text
84x + 126y = 30

gcd(84,126)=42
42 does not divide 30
STOP: no integer solutions.
```

Variants may include:

- unrestricted integer family;
- positive/nonnegative solutions;
- bounded/range-constrained solutions;
- linear congruence as `ax-my=b`;
- more than two coefficients.

WATCH OUT should use an actual contrast, not `be careful` prose.

CHECK should substitute an actual parameter family back into the equation.

---

## 9. Legality must be concrete

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

---

## 10. Variant/transfer obligations from the demonstrated corpus

The earlier 90-question analysis found compound transfers beyond core concepts. Preserve such obligations when they remain required by the frozen corpus.

Representative examples:

- zero-stripped factorials;
- idempotents modulo powers of 10;
- complete unit-group products;
- two-adic filtering through phi;
- reduced-residue sums plus geometric series;
- gcd of several linear forms;
- exponential-gcd parity variants;
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
- period of `n^n` modulo a prime;
- fixed-hypotenuse primitive Pythagorean counting.

Bridge/Variant count is evidence-driven. This list is historical evidence from one corpus, not a universal quota.

---

## 11. Last-digits teaching must not be overcompressed

A learner may need distinct episodes for:

```text
coprime base -> cycle/order
non-coprime base -> valuation/stabilisation
last k digits -> split 2^k / 5^k
specified terminal block -> congruence in each lane
factorial last nonzero digit -> zero stripping + modular structure
```

Do not force all of this onto one compact card merely because one internal support node is named `Last digits`.

---

## 12. Valuation teaching should expose the chain

A strong assimilation sequence is:

```text
what v_p(n) means
-> valuations of products/powers
-> divisibility as exponent inequalities
-> Legendre for n!
-> trailing zeros
-> largest k with M^k | N
-> factorial quotient integrality
-> zero-stripped factorial transfer
```

Use exponent/valuation diagrams when they reduce working-memory load.

---

## 13. Student-facing practice and transfer navigation

Practice Map:

```text
readable concept -> corpus question IDs
```

For extra transfer:

```text
Q003 -> Zero-stripped factorials -> review Valuations + Trailing zeros
```

not:

```text
Q003 -> NT-A01 + NT-VAL-01 + NT-ZEROS-01
```

Internal IDs remain secondary build/retrieval anchors.

---

## 14. Structural visuals

High-value Number Theory forms include:

- Euclidean remainder ladder;
- exponent-choice grid;
- Diophantine solution-line/lattice schematic;
- congruence-class strip;
- CRT split/merge lanes;
- residue cycle;
- valuation supply pipeline;
- 2/5 trailing-zero pairing;
- fixed-product rectangle;
- factor-pair table/number line;
- carry columns;
- base place-value blocks;
- floor half-open interval;
- recurrence state arrows;
- overlapping-window cancellation;
- residue pigeonholes;
- square-gap number line;
- shared-prime graph;
- Pythagorean parameter sketch.

Use only when they reduce reasoning load. Required visuals must reach final-size QA.

---

## 15. Learner-specific Part 0

Ask the learner's self-estimated knowledge, then verify with a short unaided recognition/first-move diagnostic.

Part 0 may show, for example:

```text
CRT [CORE D3 | TRANSFER D5]
[YOUR STATUS: WEAK] [DO FIRST]
```

and:

```text
Wilson [CORE D2 | TRANSFER D4]
[YOUR STATUS: STRONG] [QUICK RETEST]
```

Do not use authored difficulty as the learner's personal status.

---

## 16. Prototype gate

Before bulk generation, render and inspect at least five representative concept journeys when doing a major Number Theory rebuild. A strong set includes:

- Bezout/Diophantine;
- congruence cancellation + modular equation/inverse journey;
- CRT;
- last-digits journey;
- valuations/Legendre.

Also inspect one Appendix A question page with badges/hints and one Part 0 navigation page.

Reject:

- low contrast;
- broken heading colors;
- tiny badges/navigation;
- raw-ID dominance;
- card-stack pages without a teaching narrative;
- missing concept links;
- vague first move/watch-out/check;
- missing required visual.

---

## 17. Number Theory gates

Do **not** use `PASS_36_OF_36` as the main book acceptance condition.

Use:

```text
NT_SYLLABUS_ANCHORING = PASS
NT_CORPUS_SUPPORT = PASS_n_OF_n
NT_PRIMARY_CONCEPT_MAPPING = PASS_n_OF_n
NT_EXECUTABLE_ROUTE = PASS_n_OF_n
NT_REQUIRED_VARIANTS_TAUGHT = PASS_n_OF_n
NT_HARD_TRANSFER_GAPS_WITHOUT_SUPPORT = 0
NT_MODULAR_LEGALITY_COVERAGE = PASS
NT_FACTORISATION_ENGINE_SPLIT = PASS
NT_DIGSUM_CARRY_SPLIT = PASS
NT_RECURRENCE_WINDOW_SPLIT = PASS
NT_COUNTING_ENGINE_SPLIT = PASS
NT_CONCEPT_ASSIMILATION = PASS_ALL_REQUIRED_TEACHING_UNITS
NT_CONCEPT_LINKS_VISIBLE = PASS
NT_FIRST_MOVE_CONCRETE = PASS
NT_WATCH_OUT_CONCRETE = PASS_FOR_RISKY_METHODS
NT_CHECK_EXECUTED = PASS_FOR_RISKY_METHODS
NT_CONCEPT_BADGES = PASS_WHERE_DISPLAYED
NT_QUESTION_BADGES = PASS_WHERE_DISPLAYED
NT_DIFFICULTY_MASTERY_PRIORITY_CONFLATION = 0
NT_RAW_IDS_PRIMARY_NAVIGATION = 0
NT_REQUIRED_VISUALS_MISSING = 0
```

For the demonstrated 90-question corpus, `n=90`. For another corpus, use its actual count.

These are static document/package checks, not learner-outcome claims.

---

## Final Number Theory rule

Do not optimize for `36 skills`, `39 pages`, `100 pages`, or any other predetermined production number.

Optimize for:

```text
concept assimilation
+ concept linking
+ recognition
+ representation
+ concrete first move
+ executable variants/transfer
+ legality
+ visual offloading
+ fading help
+ complete corpus support
```

The student should finish Number Theory able to explain the idea, recognize when it applies, distinguish the subtle nearby case, start legally, execute, check, and transfer.
