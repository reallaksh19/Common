# NMTC Bhaskara Preliminary Archetype Catalogue

## Status vocabulary

- `SINGLE_PAPER_SEED` — observed in one ingested paper only.
- `RECURRENCE_SEED_2Y` — structurally related mechanisms observed in both current ingested years; not yet a historical-frequency claim.
- `HISTORICALLY_RECURRENT` — may be used only after additional-year corpus analysis.
- `SYLLABUS_REQUIRED` — required by syllabus regardless of observed recurrence.

Archetypes describe the **mathematical move**, not surface wording.

## Algebra — candidate families

| Family | Recognition trigger | First-move discipline | Current evidence status |
|---|---|---|---|
| `ALGEBRAIC_RELATION_POWER_REDUCTION` | very high powers plus a low-degree relation | reduce powers recursively; do not solve unnecessarily | `SINGLE_PAPER_SEED` |
| `POLYNOMIAL_DIVISIBILITY_COEFFICIENT_MATCH` | polynomial divisible by stated factor | use remainder/factor constraints | `RECURRENCE_SEED_2Y` at broader polynomial-structure family |
| `VIETA_TRANSFORMED_ROOTS` | roots requested through symmetric/transformed expression | write sum/product before individual roots | `RECURRENCE_SEED_2Y` |
| `INTEGER_ROOTS_VIETA` | polynomial roots constrained to positive/integer values | combine Vieta with integer partitions/bounds | `RECURRENCE_SEED_2Y` |
| `IDENTITY_COLLAPSE` | huge-looking radical/power/polynomial expression with conjugate/symmetric form | factor or identify standard identity before expansion | `RECURRENCE_SEED_2Y` |
| `LOG_VARIABLE_SUBSTITUTION` | logarithm appears inside power/square-root/exponent | set transformed log variable and solve algebraically | `RECURRENCE_SEED_2Y` |
| `EXPONENTIAL_NORMALIZATION` | mixed powers with related bases | express through compatible bases/common factors | `RECURRENCE_SEED_2Y` at transform family |
| `FUNCTION_TRANSFORM_OR_ITERATION` | shifted or composed function | translate input / simplify composition first | `RECURRENCE_SEED_2Y` |
| `RATIONAL_OR_ABSOLUTE_INTERVAL` | rational expression inside inequality/absolute value | convert to intervals with domain exclusions | `SINGLE_PAPER_SEED` |

## Sequences & Series — candidate families

| Family | Recognition trigger | First move | Current evidence status |
|---|---|---|---|
| `RECURRENCE_LINEARIZATION` | nonlinear-looking recurrence | try reciprocal/difference transform | `SINGLE_PAPER_SEED` |
| `WEIGHTED_POWER_SUM_REDUCTION` | indexed weighted polynomial sum | expand by powers of index, use standard sums | `SINGLE_PAPER_SEED` |
| `INFINITE_GP_CONSTRAINT` | sum to infinity plus another GP-derived sum | express both through `a,r`; enforce convergence | `SINGLE_PAPER_SEED` |
| `GP_TERM_CONSTRAINT` | relations among selected GP terms/sums | normalize through `a,r` and eliminate efficiently | `RECURRENCE_SEED_2Y` |

The existing `Sequence and Series/` folder remains the concept-book exemplar, but Preliminary practice must now be mapped back to these PYQ mechanisms.

## Number Theory — candidate families

| Family | Recognition trigger | First move | Current evidence status |
|---|---|---|---|
| `COMMON_REMAINDER_LCM` | same remainder under several divisors | subtract fixed remainder; use LCM | `RECURRENCE_SEED_2Y` at remainder family |
| `COMMON_REMAINDER_GCD_DIFFERENCES` | greatest divisor leaving equal remainders | take pairwise differences; compute GCD | `SINGLE_PAPER_SEED` |
| `SIMULTANEOUS_CONGRUENCE_RECONSTRUCTION` | several distinct remainder conditions | encode congruences, reconstruct target modulus | `SINGLE_PAPER_SEED` |
| `MODULAR_POWER_OR_SQUARE` | remainder of power/square requested | reduce base first; exploit residue cycle when needed | `RECURRENCE_SEED_2Y` at modular family |
| `DIGIT_DIVISIBILITY_COUNT` | digit-pattern number plus divisibility | translate place value/digit-sum rule, then count | `RECURRENCE_SEED_2Y` |
| `INTEGER_VALUED_RATIONAL_DIVISIBILITY` | rational function of natural `n` must be integer | divide algebraically and reduce to divisor constraints | `SINGLE_PAPER_SEED` |

## Geometry — candidate families

Geometry families are provisional until source figures are captured and verified.

| Family | Recognition trigger | First move | Current evidence status |
|---|---|---|---|
| `CIRCLE_TANGENT_ANGLE_CHAIN` | tangent(s), radius/diameter, chord, requested angle | mark right/equal tangent relations before chasing | `RECURRENCE_SEED_2Y` |
| `TANGENT_PARALLEL_TRANSFER` | tangent plus a line parallel to another tangent/chord | transfer angles, then apply circle theorem/similarity | `RECURRENCE_SEED_2Y` |
| `CIRCLE_OR_SEMICIRCLE_METRIC` | square/rectangle/semicircle/tangent lengths | identify right triangles/similarity/power relations | `RECURRENCE_SEED_2Y` |
| `TANGENT_CIRCLES_HOMOTHETY` | successive touching circles in fixed angle | use common-center-angle similarity / scale ratio | `SINGLE_PAPER_SEED` |
| `POLYGON_ANGLE_CHAIN` | polygon with linked angle expressions/bisectors | express all angles through one variable, then sum | `SINGLE_PAPER_SEED` |

## Arithmetic/Foundation — candidate families

These appear in the Preliminary corpus even though they are not all named in the Junior-added syllabus; they must be handled through the cumulative prerequisite map.

| Family | Recognition trigger | First move | Status |
|---|---|---|---|
| `PAIRWISE_WORK_RATE_RECONSTRUCTION` | pairwise rates for three workers | add pair equations to recover total rate | `SINGLE_PAPER_SEED` |
| `PERCENT_COMPLEMENT_TOTAL` | percentages plus known remainder count | compute remaining percentage first | `SINGLE_PAPER_SEED` |
| `PERCENTAGE_INVARIANT_DRY_MASS` | concentration/water percentage changes | identify conserved non-water mass | `SINGLE_PAPER_SEED` |

## Authoring consequence

Each stable recurring archetype must eventually have:

1. one Concept Book home;
2. one First-Step recognition card;
3. an F0–F4 practice ladder;
4. at least one verified PYQ anchor;
5. one non-identical transfer problem;
6. one recognition-only timed drill;
7. one plausible wrong-method contrast.

Do not promote a family to `HISTORICALLY_RECURRENT` from 2024–2025 evidence alone.
