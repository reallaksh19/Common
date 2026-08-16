# Sequence & Series Concept Book Specification

## Cognitive contract

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Mathematics mastery target:

`PATTERN -> INVARIANT -> STRUCTURE -> TRANSFER`

## Chapter architecture

1. **How to see Mathematics** — use the six lenses: POSITION, CHANGE, RATIO, ACCUMULATION, TRANSFORM, REVERSE.
2. **POSITION** — sequence, indexing, nth term, piecewise odd/even rules, recurrence.
3. **CHANGE** — finite differences, arithmetic progression, nth term.
4. **ACCUMULATION** — series, `S_n`, sigma notation.
5. **AP sum** — derive why `n/2`, `2a+(n-1)d`, and endpoint-average forms appear.
6. **RATIO** — GP as repeated multiplication; `a r^(n-1)` and why exponent is `n-1`.
7. **Finite GP** — derive by multiplying by `r` and subtracting; explain cancellation.
8. **Infinite GP** — convergence and why the residual term vanishes only when `|r|<1`.
9. **TRANSFORM** — HP through reciprocals; logarithmic/AP transform where source-supported.
10. **MEANS** — AM, GM, HM and relationships.
11. **REVERSE** — recover a term from a sum: `a_n = S_n - S_{n-1}`.
12. **Power sums and hidden transformations** — `sum k`, `sum k^2`, `sum k^3`, nested sums, alternating powers, telescoping.
13. **ADOPT laboratory** — mixed unlabeled problems; no chapter labels before attempt.
14. **JEE bridge** — staged source-to-transfer examples.
15. **Source coverage and reconstruction test**.

## Six chapter lenses

### POSITION

Ask: what lives at term `n`?

Representations: list -> indexed table -> general term.

### CHANGE

Ask: what repeats additively?

Representations: terms -> first differences -> AP relation.

### RATIO

Ask: what repeats multiplicatively?

Representations: terms -> adjacent ratios -> GP relation.

### ACCUMULATION

Ask: what happens when terms are added?

Representations: visible addition -> `S_n` -> sigma notation.

### TRANSFORM

Ask: can a hard-looking object be changed into an easier equivalent one?

Examples: reciprocate, pair, split odd/even, factor, rationalize, telescope, take logarithms where justified.

### REVERSE

Ask: can local information be recovered from cumulative information?

Primary relation: `a_n = S_n - S_{n-1}`.

## Mandatory page behavior

Every major concept must include:

1. SEE representation before general rule;
2. REALIZE invariant/hidden structure;
3. UNDERSTAND derivation/reconstruction;
4. at least one contrast or plausible wrong method;
5. ADOPT first-move prompt;
6. non-identical transfer/rebuild prompt;
7. CONNECT source IDs/bridge IDs.

## Summation pedagogy

Required order:

`ordinary addition -> index/counter -> start/stop -> expansion -> compression -> splitting -> standard sums -> hidden transformations`.

Do not teach sigma as a formula list. First show what terms the counter generates.

The standard power sums are introduced as tools after sigma meaning is secure:

- `sum 1 = n`;
- `sum k = n(n+1)/2`;
- `sum k^2 = n(n+1)(2n+1)/6`;
- `sum k^3 = [n(n+1)/2]^2`.

For Grade 9 foundation, derive or motivate where useful, but do not let derivation of every power-sum identity block the main structural objective.

## JEE bridge policy

JEE items are bridge/transfer material. Preserve year/shift metadata where verified, adapt wording rather than reproducing facsimiles, use staged hints, and map every bridge item to the concept(s) it exercises.

The bridge must progress from direct recognition to structural transformation and multi-concept transfer.

## Publication acceptance

Applicable MSRU-01..MSRU-15 gates must pass. In particular:

- no naked formulas;
- source/extension provenance separated;
- summation grounded in repeated addition;
- ADOPT contains genuine transfer;
- math glyphs, superscripts/subscripts, radicals, sigma signs and inequalities render correctly at normal reading size.
