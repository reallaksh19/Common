# NMTC Bhaskara Preliminary — Concept Dependency Map v1

## Purpose

This map converts the solution-qualified 2018, 2019, 2023, 2024 and 2025 Preliminary corpus into an order for teaching and self-study.

It is **not a chapter-weightage table**. Dependency outranks frequency: a low-frequency prerequisite may be mandatory because several high-frequency mechanisms depend on it.

Use together with:

- `01_PYQ_Corpus/Five_Year_Scored_Recurrence_v1.md`;
- `02_Archetypes/NMTC_Preliminary_Archetype_Catalogue.md`;
- the Grade 9 Mathematics `SEE -> REALIZE -> UNDERSTAND -> ADOPT` contract.

## Global learning spine

```text
FOUNDATION FLUENCY
  -> REPRESENTATION SWITCHING
  -> STRUCTURAL RECOGNITION
  -> FIRST USEFUL MOVE
  -> COMPACT EXECUTION
  -> DOMAIN / BOUNDARY CHECK
  -> NON-IDENTICAL TRANSFER
  -> MIXED PRELIMINARY SPEED
```

The recurrent five-year signal says that `REPRESENTATION SWITCHING -> FIRST USEFUL MOVE` is the main performance bottleneck, especially in Algebra and Number Theory.

---

# A. Algebra dependency spine

## A0 — prerequisites

Student must already be secure with:

- algebraic identities;
- factorization;
- linear equations;
- exponents and radicals;
- fractions/rational expressions;
- coordinate/graph basics;
- inequalities on the number line;
- elementary AP/GP language.

Failure at A0 is remediated through a foundation bridge; it is not disguised as an NMTC topic failure.

## A1 — structure before expansion

Core invariant:

> A large expression is often a small expression written in an inconvenient representation.

Required capabilities:

- factor before expanding;
- detect conjugates and perfect-square/cube forms;
- use `t + 1/t`, reciprocal, parity and symmetry substitutions;
- reduce high powers from a low-degree relation;
- choose a transformed variable for logs/exponents.

PYQ evidence includes 2018 Q01/Q06/Q21, 2019 Q08/Q25, 2023 Q03/Q07/Q14/Q21/Q26/Q27, 2024 Q01/Q04/Q06/Q07/Q09/Q12/Q15/Q26/Q28/Q30, and 2025 Q03/Q04/Q09/Q12/Q16/Q17/Q22/Q24/Q27.

A1 is the gateway to nearly every later Algebra unit.

## A2 — quadratic structure

Prerequisites: A1.

Teach as four connected views:

1. equation form;
2. factor/root form;
3. graph/discriminant form;
4. coefficient/root relation form.

Required capabilities:

- solve only when individual roots are genuinely needed;
- use discriminant for root existence/repetition;
- use sum/product of roots;
- reconstruct a quadratic from roots or transformed roots;
- test equality/bound conditions attached to positive roots.

## A3 — Vieta and transformed roots

Prerequisites: A2 + symmetry from A1.

Recognition triggers:

- requested expression is symmetric in roots;
- roots are transformed by reciprocal, square, ratio or shift;
- integer/positive-root restrictions are given;
- coefficients are known but explicit roots look ugly.

First move:

`write alpha+beta and alpha*beta before solving the quadratic.`

PYQ anchors:

- 2024 Q14 — root-ratio expression after recovering the original quadratic;
- 2024 Q17 — four positive roots + AM-GM equality collapse;
- 2024 Q22 — function shift followed by Vieta;
- 2025 Q20 — useful as a **source-conflict contrast**, not canonical anchor, because stem/key sign custody is unresolved.

## A4 — polynomial factor / remainder network

Prerequisites: A1 + A2.

Required capabilities:

- Factor Theorem as zero remainder;
- Remainder Theorem as substitution for divisor `x-a`;
- reduction modulo a polynomial such as `x^2-1`, `x^2+1`, `x^2+x+1`;
- divisibility by a quadratic through remainder/coefficient constraints;
- structural factorization before quartic formulas;
- common-root elimination without solving all roots.

Clean PYQ anchors:

- 2018 Q06 — reduce target modulo `x^2+x+1`;
- 2019 Q08 — reduce powers modulo `x^2-1`;
- 2024 Q05 — divisibility by `x^2+1`;
- 2024 Q16 — quotient-coefficient periodicity under division by `x^2+1`;
- 2024 Q24 — factor easy rational roots before attacking the residual quadratic.

Bonus-only evidence:

- 2023 Q16 — common-root elimination; retain as high-ceiling extension, not ordinary scored recurrence.

## A5 — higher-degree equations by reduction

Prerequisites: A3 + A4.

Student should not be trained to treat every cubic/quartic as a new formula chapter.

Required first moves:

- search for easy rational/integer roots;
- use symmetry/substitution;
- reduce through a supplied algebraic relation;
- exploit integer-root sum/product restrictions;
- factor into lower-degree pieces.

PYQ anchors include 2019 Q25, 2024 Q24 and the 2025 cubic/root-structure family, with 2025 Q20 blocked as a canonical anchor until the sign conflict is resolved.

## A6 — radicals, exponents and logarithmic transformations

Prerequisites: A1 + A2.

Required switches:

- common radical basis;
- conjugate pair to perfect square/cube;
- same-base exponent normalization;
- `t = log_b x`;
- `t = sqrt(log_b x)` when justified;
- convert logarithmic equality back to algebra with domain checks.

Clean anchors include 2023 Q07/Q21/Q26, 2024 Q04/Q12/Q28, 2025 Q03/Q04/Q12/Q27.

## A7 — inequalities, bounds and equality conditions

Prerequisites: A1 + A2.

Required order:

`BOUND? -> DOMAIN? -> CHOOSE INEQUALITY -> EQUALITY CONDITION -> VERIFY`

Teach boundedness before AM-GM/Cauchy optimization.

Key contrast anchor:

- 2023 Q17 — requested maximum is unbounded; the correct first move is to test boundedness, not blindly apply an inequality.

Other evidence:

- 2018 Q12/Q13;
- 2024 Q17;
- 2025 Q10.

---

# B. Number Theory dependency spine

## N0 — prerequisites

- factorization and divisibility;
- HCF/LCM;
- prime factorization;
- parity;
- place value;
- integer equations.

## N1 — congruence as compressed remainder language

Teach concrete remainder patterns before notation.

`ordinary remainder -> congruence -> addition/multiplication -> powers -> cycles`

Anchors: 2018 Q29, 2025 Q13.

## N2 — same-remainder structures

Two distinct first moves must be contrasted:

- same remainder under several **divisors** -> subtract residue, use LCM;
- greatest divisor leaving same remainder on several **numbers** -> take differences, use GCD.

Anchors: 2025 Q01 and 2024 Q21.

## N3 — divisibility + place value + digit structure

Prerequisites: N0/N1.

Anchors: 2019 Q16/Q17, 2025 Q14/Q21.

## N4 — integer-valued expressions and divisor reduction

Prerequisites: A1 + N0.

Anchors: 2018 Q10/Q19 and 2025 Q26.

## N5 — high-ceiling modular reasoning

Prerequisites: N1–N4.

Includes multiplicative-order style filtering, prefix residues and structured representation.

2019 proves this ceiling is legitimate Preliminary evidence:

- Q06 prefix residues modulo 11;
- Q26 multiplicative-order filtering;
- Q28 balanced ternary as representation/counting bridge.

These are bridge/ceiling items, not the starting point for modular arithmetic.

---

# C. Geometry dependency spine

Geometry uses:

`SEE FIGURE -> MARK GIVEN -> MARK FORCED FACTS -> CHOOSE ONE RELATION -> CHAIN -> CHECK`

## G0 — prerequisite visual grammar

- triangle angle sum;
- isosceles consequences;
- parallel-line angles;
- Pythagoras;
- similarity/congruence;
- polygon angle sums;
- basic area/ratio.

## G1 — circle angle grammar

- center/arc/chord relation;
- angle in same segment;
- diameter/right angle;
- cyclic quadrilateral.

## G2 — tangent grammar

Prerequisites: G1.

- radius perpendicular to tangent;
- equal tangents;
- tangent-chord/alternate segment;
- tangent + parallel transfer.

This is P0 because short circle/tangent chains appear in every qualified year.

## G3 — power/intersecting-chord metric

Prerequisites: G1/G2 + similarity.

## G4 — triangle metric theorems

- medians / Apollonius;
- cevians / Stewart;
- altitude metric identities;
- incenter/circumcenter relations.

PYQ recurrence is lower than G1/G2, but the syllabus obligation is explicit.

## G5 — composite short-chain geometry

Combine no more than a few strong relations under Preliminary time pressure. Figure-recognition cards are mandatory.

Exact student anchors remain blocked wherever original figure custody is incomplete.

---

# D. Sequences & Series dependency spine

Use the existing `Sequence and Series/` architecture as concept authority.

Add a Preliminary layer in this order:

1. pattern/term/recurrence recognition;
2. AP/GP parameter recovery;
3. sums and reverse-from-sum;
4. transformed recurrence;
5. weighted/power sums;
6. infinite-GP condition;
7. mixed high-index collapse.

Clean anchors include 2019 Q29, 2023 Q15/Q29, 2024 Q11/Q27. 2025 Q30 remains source-conflicted and cannot be a canonical scored anchor.

---

# E. Combinatorics dependency spine

The sparse five-year frequency does not justify shallow coverage.

Teach:

`MODEL OUTCOME -> MULTIPLY/SPLIT -> REMOVE OVERCOUNT -> COMPLEMENT -> FORCE -> VERIFY`

1. Fundamental Principle of Counting;
2. casework;
3. permutations;
4. combinations;
5. complement;
6. inclusion-exclusion;
7. pigeonhole;
8. representation/path/subset/coefficient-counting bridges.

2019 supplies legitimate high-ceiling Preliminary evidence beyond routine `nPr/nCr`: subset-product expansion, exact paths, balanced ternary, coefficient counting.

---

# F. Explicit syllabus topics with weak current recurrence

These remain mandatory:

- Mathematical Induction;
- Greatest Integer / Least Integer functions.

They receive **syllabus-first** concept books and practice ladders, but no fabricated PYQ frequency claim.

---

# Recommended build order

1. `P0 Algebra Structure Network` — A1 through A5.
2. `Radical / Exponent / Log Transformation` — A6.
3. `Inequality / Bound / Equality` — A7.
4. `Modular / Divisibility / Digit Structure` — N1 through N5.
5. `Circle / Tangent Recognition` — G1 through G3.
6. `Sequence & Series Preliminary Layer`.
7. remaining explicit syllabus units.

## Publication rule

A concept node is not `READY` merely because its notes exist. It must have:

- prerequisite diagnostic;
- SEE object;
- invariant;
- reconstruction;
- contrast/wrong move;
- First-Step card;
- F0–F4 ladder;
- clean PYQ anchor where available;
- non-identical transfer;
- unlabelled mixed test;
- applicable `PRELIM-*` and `MSRU-*` gates passed.
