# Counting / Permutations / Pigeonhole / Inclusion–Exclusion — Source Coverage Map v1

## Authority

This map uses the solution-qualified 2018, 2019, 2023, 2024 and 2025 Bhaskara Preliminary corpus already retained in this workspace.

`COMBINATORIAL_MODELING_BEYOND_NPR_NCR` is cleanly represented in two qualified years, with 2019 showing unusually high ceiling. Fundamental counting, permutations/combinations, pigeonhole and inclusion–exclusion remain syllabus-required regardless of recurrence density.

## Evidence classes

- `CLEAN_SCORED_ANCHOR`
- `FIGURE_GATED_ANCHOR`
- `BRIDGE_EVIDENCE`
- `SOURCE_CONFLICT_EVIDENCE`
- `SYLLABUS_FIRST_AUTHOR_CREATED`

## Qualified mechanism map

| Mechanism | PYQ ID | Role | First move / invariant |
|---|---|---|---|
| subset-product expansion | `NMTC-BH-P-2019-Q07` | `CLEAN_SCORED_ANCHOR` | translate sum of subset-products to `product(1+a_i)-1` |
| geometric configuration classification | `NMTC-BH-P-2019-Q09` | `CLEAN_SCORED_ANCHOR_WITH_MODEL_HELPFUL` | classify vertex triples into disjoint geometric types before counting |
| connected configuration count | `NMTC-BH-P-2019-Q12` | `FIGURE_GATED_ANCHOR` | define connected three-cell/stamp configurations on supplied figure; exact figure required |
| exceptional-case enumeration | `NMTC-BH-P-2019-Q22` | `BRIDGE_EVIDENCE` | split `A^B=1` into disjoint base/exponent cases, then count distinct solutions |
| exact-move path/state count | `NMTC-BH-P-2019-Q23` | `FIGURE_GATED_ANCHOR` | define states / recurrence before counting paths |
| balanced representation count | `NMTC-BH-P-2019-Q28` | `CLEAN_HIGH_CEILING_BRIDGE` | exploit unique signed-power representation before coefficient/sign counting |
| coefficient as count | `NMTC-BH-P-2019-Q30` | `CLEAN_SCORED_ANCHOR` | coefficient of product of finite sums = count exponent pairs meeting target |
| digit restriction + divisibility count | `NMTC-BH-P-2025-Q21` | `CLEAN_SCORED_ANCHOR` | define digit positions, impose mod-9 restriction, count valid ordered digit pairs including residue-0 duplication |
| inequality-to-integer count | `NMTC-BH-P-2025-Q10` | `BRIDGE_EVIDENCE` | solve real interval first, then count admissible integers |
| odd-digit two-digit count | `NMTC-BH-P-2023-Q25` | `SOURCE_CONFLICT_EVIDENCE` | printed wording gives 20 by `5*4`; supplied key/solution gives 12 after an unexplained digit restriction; do not canonicalize |

## Syllabus-first nodes

The current five-year clean corpus does not justify waiting for a PYQ before teaching:

- fundamental multiplication and addition principles;
- factorial notation;
- permutations with/without repetition at Grade IX/X foundation depth;
- combinations as unordered selection;
- complementary counting;
- pigeonhole principle;
- inclusion–exclusion for two and three sets;
- simple derangement/adjacency restrictions only as transfer, not as formula memorization.

These use `AUTHOR_CREATED_FOUNDATION` and `AUTHOR_CREATED_TRANSFER` provenance.

## Publication constraints

1. Do not reconstruct 2019 Q12/Q23 figures from prose.
2. Do not use 2023 Q25 as an answer-authority example.
3. Do not present the five-year 5.9% primary-domain share as official NMTC weightage.
4. Keep high-ceiling 2019 items as evidence of possibility, not as the entry difficulty for every learner.
