# Sequence & Series — NMTC Preliminary Overlay Specification

## Role of this file

The existing `Grade 9/Mathematics/Sequence and Series/Sequence_Series_Concept_Book_Spec.md` is the deep concept authority.

This overlay specifies only what must be added for Bhaskara Preliminary performance.

## Do not duplicate

Do not reauthor from scratch:

- AP derivation;
- GP derivation;
- sigma meaning;
- power-sum explanations;
- finite/infinite GP conceptual distinction;
- `a_n=S_n-S_{n-1}` derivation;
- telescoping foundations.

Instead link the Preliminary drill to the relevant upstream concept section.

## Preliminary decision tree

Before calculating, ask in order:

1. **TERM OR SUM?** — is the target `a_n`, `S_n`, a block sum, or a transformed sum?
2. **CHANGE OR RATIO?** — additive invariant -> AP/differences; multiplicative invariant -> GP.
3. **CAN INDEXES CANCEL?** — selected/high-index GP often collapses by ratios.
4. **IS THE TERM POLYNOMIAL IN n?** — weighted sums may reduce to `Σn`, `Σn²`, `Σn³`.
5. **IS THE RECURRENCE IN THE WRONG VARIABLE?** — try reciprocal, difference, shift or ratio.
6. **CAN CUMULATIVE INFORMATION BE REVERSED?** — use `a_n=S_n-S_{n-1}`.
7. **IS IT INFINITE?** — write and verify `|r|<1` before using `a/(1-r)`.
8. **WILL NEIGHBORING TERMS CANCEL?** — test partial fractions/rationalization/telescoping.
9. **IS THE SOURCE ITSELF CLEAN?** — do not repair a PYQ to match an answer key.

## Required Preliminary mechanism families

### S1 — AP recognition under disguise

First moves:

- differences;
- endpoint/term-count relation;
- `a_n=a+(n-1)d`;
- block sum by difference of partial sums where faster.

### S2 — term versus sum

Mandatory contrast:

- `a_20` is one term;
- `S_20` is accumulation.

A learner who confuses these is not Preliminary-ready even if formulas are memorized.

### S3 — selected/high-index GP

First move:

> divide comparable terms or equations before solving for huge powers.

Target behavior:

`a_p/a_q=r^(p-q)`.

### S4 — weighted polynomial sums

Visible forms such as:

`Σ k(ak+b)`, `Σ(k²+k)`, or an nth term that expands polynomially.

First move:

`expand structurally -> split -> standard sums`.

Grounding: 2023 Q15 and 2024 Q10.

### S5 — recurrence linearization

Try, in order where natural:

- reciprocal;
- first difference;
- shift by a constant;
- ratio;
- partial-sum transformation.

Grounding: 2024 Q11.

### S6 — functional recurrence / strategic indices

For rules such as `a_{m+n}=...`, do not attempt a closed form first unless needed.

Ask:

> Which substitutions reach the requested index fastest?

Grounding: 2019 Q29.

### S7 — infinite GP constraints

Required sequence:

`identify a,r -> |r|<1 -> write each sum -> eliminate -> reconstruct requested target`.

Grounding: 2024 Q27.

### S8 — reverse from partial sums

First move:

`a_n=S_n-S_{n-1}`.

Contrast with differentiating/guessing a pattern from the polynomial expression for `S_n`.

### S9 — telescoping

Recognition triggers:

- neighboring linear factors;
- conjugate radicals;
- recurrence whose reciprocal differs by a constant.

### S10 — finite differences

If terms look polynomial rather than AP/GP:

`terms -> first differences -> second differences -> degree hypothesis -> verify`.

## First-move mastery requirement

For an unlabelled mixed set, learner must identify the correct move before calculation in at least 80% of items.

## Speed-layer design

Use three separate modes:

1. **Recognition-only** — identify structure, no solving.
2. **First-line-only** — write one mathematically useful line.
3. **Compact solve** — execute only after the first move is frozen.

Do not use raw speed to hide conceptual errors.

## Source integrity

`NMTC-BH-P-2025-Q30` remains `SOURCE_KEY_CONFLICT_NOT_CANONICAL`.

No author may change “second/third/fourth term” wording merely to make the provisional key work.

## Internal completion gate

Overlay is `INTERNAL_PACKAGE_COMPLETE_NOT_PUBLICATION_READY` only when:

- clean PYQ source map exists;
- student route points to upstream concepts;
- First-Step cards exist;
- F0→F4→PYQ→XF ladders exist;
- transfer bank math review passes;
- recognition and first-line labs exist;
- unlabelled mastery test exists;
- QA distinguishes deep-concept authority from Preliminary overlay authority.