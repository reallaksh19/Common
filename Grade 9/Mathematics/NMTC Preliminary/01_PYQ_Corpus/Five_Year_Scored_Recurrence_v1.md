# NMTC Bhaskara Preliminary — Five-Year Scored Recurrence v1

## Purpose

This is the first quantitative curriculum signal derived from the solution-qualified 2018, 2019, 2023, 2024 and 2025 Bhaskara Preliminary corpus.

It is **not official AMTI weightage** and is **not psychometric calibration**. It is an operational classification used to decide teaching/practice emphasis while preserving every explicit syllabus topic.

## Eligibility rule

A question enters the ordinary recurrence denominator only when:

`scoring known + mathematical path qualified + primary mechanism classifiable + no unresolved source conflict that changes the mechanism/answer`.

Excluded from ordinary recurrence:

- bonus questions;
- starred/unknown-scoring items;
- unresolved stem/key/source conflicts affecting the canonical mathematics.

Figure-dependent questions may enter broad domain recurrence when the complete source/solution fixes the mathematical configuration, but they remain blocked as exact student-facing anchors until figure custody is complete.

## Eligible denominator by year

| Year | Normalized slots | Excluded from ordinary scored recurrence | Eligible questions |
|---|---:|---|---:|
| 2018 | 30 | Q03/Q05/Q07 bonus | 27 |
| 2019 | 30 | Q20 bonus | 29 |
| 2023 | 30 | Q08/Q16 bonus; Q05 starred; Q02/Q06/Q12/Q25 unresolved source conflicts | 23 |
| 2024 | 30 | none at v1 qualification level | 30 |
| 2025 | 30 | Q08/Q18/Q20/Q30 stem/key conflicts | 26 |
| **Total** | **150** | **15 excluded** | **135** |

The 15 excluded slots remain visible as `BONUS_EVIDENCE`, `STARRED_EVIDENCE`, or `SOURCE_CONFLICT_EVIDENCE`; they are not discarded.

## Primary-domain operational classification

For this table each eligible question receives exactly one primary curriculum domain. `Sequences & Series`, logarithms, equations and inequalities are counted under **Algebra**, consistent with the supplied Junior syllabus grouping. Everyday rate/percentage/clock items that primarily test cumulative pre-Junior foundations are kept in **Arithmetic/Foundation** rather than artificially inflating an explicit Junior topic.

| Year | Algebra | Geometry | Number Theory | Combinatorics | Arithmetic / cumulative foundation | Eligible total |
|---|---:|---:|---:|---:|---:|---:|
| 2018 | 9 | 7 | 8 | 0 | 3 | 27 |
| 2019 | 5 | 5 | 8 | 7 | 4 | 29 |
| 2023 | 17 | 4 | 2 | 0 | 0 | 23 |
| 2024 | 19 | 8 | 2 | 0 | 1 | 30 |
| 2025 | 11 | 8 | 4 | 1 | 2 | 26 |
| **5-year total** | **61** | **32** | **24** | **8** | **10** | **135** |
| **Operational share** | **45.2%** | **23.7%** | **17.8%** | **5.9%** | **7.4%** | **100%** |

### Interpretation guardrail

Do **not** publish these percentages to students as “NMTC official chapter weightage.” They are a five-year, source-qualified working sample. In particular:

- Combinatorics is explicit syllabus and cannot be reduced to 5.9% curriculum coverage merely because this sample is sparse outside 2019.
- Mathematical induction and greatest/least integer functions are explicit syllabus even if not strongly represented in the currently qualified five-year set.
- 2022 is still missing and may materially alter recurrence.

## Cross-year mechanism families

These are multi-tag recurrence families, so counts may overlap. The strongest v1 signal is **years present**, not a single additive percentage.

| Mechanism family | Clean scored years present | Evidence level | Curriculum consequence |
|---|---:|---|---|
| `TRANSFORM_BEFORE_CALCULATE` — substitution, identity, reciprocal/common-basis, normalize first | **5/5** | VERY_STRONG | every algebra unit needs explicit transformation recognition + first-line drills |
| `RADICAL_EXPONENT_LOG_COMPRESSION` | **5/5** | VERY_STRONG | teach common basis, conjugate/perfect-square recognition, log-variable substitution, exponent linearization |
| `DIVISIBILITY_MODULAR_DIGIT_STRUCTURE` | **5/5** | VERY_STRONG | modular arithmetic must connect to remainders, digits, GCD/LCM, cycles and integer-valued expressions |
| `SHORT_GEOMETRY_RECOGNITION_CHAIN` | **5/5** | VERY_STRONG | geometry teaching must emphasize what to mark/construct first, not theorem memorization |
| `INEQUALITY_BOUND_OR_EQUALITY_STRUCTURE` | **5/5** | STRONG | include boundedness check, equality condition and completion/AM-GM style recognition |
| `POLYNOMIAL_ROOT_REMAINDER_VIETA_NETWORK` | **4/5 clean** + 2025 conflicted cubic item | STRONG | teach quadratics/higher-degree/remainder/Vieta as connected structures rather than isolated chapters |
| `RATE_PERCENT_INVARIANT_MODELING` | **4/5** | MODERATE_STRONG | cumulative arithmetic needs compact model-translation drills because it still consumes Preliminary slots |
| `SEQUENCE_RECURRENCE_ACCUMULATION` | **3/5 clean** + 2025 conflicted GP item | MODERATE | retain deep Sequence & Series architecture; add Preliminary recognition layer rather than formula-only revision |
| `COMBINATORIAL_MODELING_BEYOND_NPR_NCR` | **2/5 clean** | SPARSE_BUT_HIGH_CEILING | explicit syllabus requires full coverage; 2019 proves path/subset/coefficient/balanced-ternary style modeling can appear |

## What the recurrence says about difficulty

The corpus does **not** support a preparation strategy of “memorize formulas and do many similar examples.” Recurring scored mechanisms instead favor:

1. reducing a large-looking expression to a small invariant;
2. changing representation before calculating;
3. using a relation (Vieta/remainder/modular/reciprocal/identity) without solving every underlying variable;
4. recognizing a short geometry configuration rapidly;
5. checking domains, boundedness, parity, integrality and source consistency;
6. translating word models into one or two equations with minimal algebra.

## Curriculum priority seed

### P0 — high recurrence + high transfer value

- Algebraic structure / transformation toolkit
- Quadratics + Vieta + transformed roots
- Higher-degree equations + factor/remainder reduction
- Radicals, exponents and logarithmic transformations
- Basic inequalities, bounds and equality conditions
- Modular arithmetic + divisibility + digit/remainder structures
- Circle/tangent/angle and short metric geometry recognition

### P1 — explicit syllabus + meaningful PYQ evidence

- Sequences & Series Preliminary recognition layer
- counting principle / permutations-combinations / modeling
- pigeonhole and inclusion-exclusion
- Apollonius / Stewart and mixed triangle geometry
- cumulative rate, percentage, clock and mensuration modeling

### P2 coverage risk — explicit syllabus but weak/absent current five-year evidence

These must **not** be omitted:

- Mathematical Induction
- Greatest Integer / Least Integer functions
- syllabus-specific items that may be historically sparse in the five currently qualified papers

P2 means lower PYQ recurrence evidence, **not lower syllabus obligation**.

## Next promotion gate

Before calling this a stable historical weighting model:

1. recover and qualify 2022;
2. re-run the same eligibility/classification rules;
3. freeze exact per-question taxonomy in machine-readable form;
4. verify figure-dependent mechanism tags against retained figures;
5. then publish `Six_Year_Scored_Recurrence_v2` and use it to size question-bank/lab allocations.

This v1 is sufficient to begin **content architecture and first chapter prioritization**, but not to claim official weightage.
