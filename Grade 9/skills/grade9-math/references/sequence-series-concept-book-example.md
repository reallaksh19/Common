# Sequence & Series — Mathematics Concept Book Exemplar

## Source authority

Primary source set:

- uploaded 23-page `Sequence and series - Math.pdf`;
- printed advanced source questions Q1-Q20 on pages 1-2 of that PDF;
- user-supplied 2026 JEE screenshots and the separately identified JEE bridge set are extension material, not handwritten-note authority.

Never present sigma/power-sum/JEE material as if it were written in the handwritten notes.

## Learning objective

Move the learner from formula recognition to independent structural recognition:

`PATTERN -> INVARIANT -> STRUCTURE -> TRANSFER`

using the cognitive sequence:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`.

## Six recurring lenses

- `POSITION` — `a_n`, indexing, odd/even rules, recurrence.
- `CHANGE` — finite differences, AP.
- `RATIO` — GP, repeated multiplication, convergence.
- `ACCUMULATION` — series, `S_n`, sigma, AP/GP sums.
- `TRANSFORM` — reciprocal/HP, logarithmic transform, pairing, splitting, telescoping.
- `REVERSE` — recover `a_n` from cumulative sums using `a_n = S_n - S_{n-1}`.

## Recommended chapter architecture

1. How to see Mathematics.
2. POSITION — what does the nth term mean?
3. CHANGE — AP as an invariant.
4. ACCUMULATION — from a series to sigma notation.
5. Why the AP sum formula has its shape.
6. RATIO — GP as repeated multiplication.
7. Finite GP — why multiplying by `r` helps.
8. Infinite GP — where the last term goes and why `|r| < 1` matters.
9. TRANSFORM — HP and reciprocals.
10. MEANS — AM, GM, HM.
11. REVERSE — recover a term from cumulative sums.
12. Power sums and hidden transformations.
13. ADOPT laboratory — mixed, unlabeled first-move problems.
14. JEE bridge — source-to-transfer map.
15. Source coverage / reconstruction test.

## Page archetype

For an AP nth-term page:

### SEE

Show `3, 7, 11, 15, 19, ...` and mark `+4` between terms.

### REALIZE

State: the first difference is invariant.

### UNDERSTAND

Build:

- term 1: `a`
- term 2: `a+d`
- term 3: `a+2d`
- term n: `a+(n-1)d`

Explain why `n-1` appears: moving from position 1 to position n requires exactly `n-1` jumps.

### ADOPT

- recognize `17, 23, 29, 35, ...`;
- write `a=17, d=6` as first move;
- transform `a_n - 2a_{n-1} + a_{n-2}=0` into equality of first differences;
- reject a GP ratio test because ratios are not constant;
- transfer to a source/JEE-style indexed-term condition.

## Summation exemplar

Teach:

`1 + 2 + 3 + 4 + 5`

before

`sum_{k=1}^5 k`.

Interpret sigma as:

- `Σ` = ADD;
- index = counter;
- lower value = START;
- upper value = STOP;
- expression = term generator.

Then train both directions:

`expand: sigma -> terms`

and

`compress: terms -> sigma`.

Only after this introduce:

- `sum 1`;
- `sum k`;
- `sum k^2`;
- `sum k^3`;
- split linear combinations;
- nested sums;
- alternating odd/even powers;
- telescoping.

## JEE bridge examples

Two central transfer anchors supplied by the user:

1. `1^3 - 2^3 + 3^3 - ... + 15^3` — alternating powers; choose odd/even split or adjacent pairing.
2. `1 + 1/2(1^2+2^2) + 1/3(1^2+2^2+3^2) + ...` to 10 terms — write the general term, collapse the inner square sum, then split the outer polynomial sum.

The First-Step product should teach recognition/hints; the Concept Book should explain why each transformation works.

## Acceptance rule

Do not publish until:

- handwritten/source coverage is mapped;
- extension material is labeled distinctly;
- every major concept passes MSRU-01..MSRU-15 as applicable;
- ADOPT contains genuine unlabeled transfer, not a near-copy;
- formulas can be reconstructed from the visible pattern/structure;
- summation is taught as repeated addition before symbolic manipulation;
- PDF math glyph/render QA passes.
