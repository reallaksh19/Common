# Mathematical Induction — Source Coverage Map v1

## Authority position

The current qualified five-year Preliminary corpus (2018, 2019, 2023, 2024, 2025) does **not** contain a dense clean set of induction questions sufficient to claim historical recurrence.

The dependency map and archetype catalogue classify Mathematical Induction as `SYLLABUS_REQUIRED` despite weak/absent current recurrence.

Therefore:

- no five-year induction percentage is published;
- no existing non-induction PYQ is relabeled as induction;
- all teaching examples and transfer items here are author-created unless a future source-qualified anchor is recovered;
- 2022 recovery may change the evidence picture and must trigger requalification.

## Neighboring source-supported mechanisms

These do not become induction anchors, but they provide useful transfer bridges:

| Neighboring mechanism | Qualified evidence | Induction connection |
|---|---|---|
| functional recurrence | 2019 Q29 | repeated-index structure; induction can later prove a derived closed form if one is established |
| weighted sums | 2023 Q15; 2024 Q10 | closed-form sum identities are natural induction targets |
| recurrence transformation | 2024 Q11 | distinguishes solving a recurrence from proving a formula about it |
| modular/divisibility structure | multiple years | divisibility statements such as `m | (a_n-b_n)` are natural induction exercises, but the PYQs themselves are not relabeled |
| polynomial power reduction | multiple years | repeated algebraic structure can motivate recursive proof, not historical induction evidence |

## Coverage classes

### Foundation induction

`AUTHOR_CREATED_FOUNDATION`

- meaning of proposition `P(n)`;
- base case;
- induction hypothesis;
- induction step;
- correct starting index;
- finite checking vs proof for all integers;
- invalid/circular proof detection.

### Standard transfer

`AUTHOR_CREATED_TRANSFER`

- finite-sum identities;
- divisibility identities;
- inequality chains;
- recurrence/closed-form verification;
- geometric or combinatorial formulas already discovered by another method.

### Ceiling bridge

`AUTHOR_CREATED_TRANSFER_HIGH_CEILING`

- strong induction;
- multiple-base cases;
- statements valid only from `n>=n0`;
- proof repair / falsifier analysis.

## Promotion rule

If a future original or independently verified Bhaskara Preliminary induction question is recovered:

1. assign stable ID `NMTC-BH-P-YYYY-QNN`;
2. qualify the mathematics independently;
3. add it here with provenance/disposition;
4. update the five/six-year recurrence model without retroactively relabeling author-created material.

## Current source-readiness verdict

`READY_FOR_SYLLABUS_FIRST_AUTHORING`

`NOT_READY_FOR_HISTORICAL_FREQUENCY_CLAIM`
