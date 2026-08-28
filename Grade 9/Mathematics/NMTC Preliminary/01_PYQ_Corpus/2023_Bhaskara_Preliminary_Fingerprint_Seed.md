# 2023 Bhaskara Preliminary — Fingerprint Seed

Initial source: Cheenta reproduction.

Qualification source: Resonance-hosted 2023 NMTC Junior Stage-I answer key and worked-solution PDF, carrying the Association of Mathematics Teachers of India Bhaskara Screening heading and complete Q1–Q30 answer table.

Observed structure: 30 questions, Q1–15 option-based and Q16–30 fill-in.

| ID | Domain | Mechanism / hidden structure | Seed archetype | Qualified source/scoring status |
|---|---|---|---|---|
| `NMTC-BH-P-2023-Q01` | Algebra | Expand `(x+c)^3` and match coefficients | `POLYNOMIAL_PERFECT_POWER_COEFFICIENT_MATCH` | scored; key D |
| `Q02` | Geometry | Median metric relation then isosceles angle extraction | `TRIANGLE_MEDIAN_METRIC_ANGLE` | scored key B but `SOURCE_CONFLICT`: side data conflicts with stated `40°` |
| `Q03` | Algebra | Use quadratic relation to reduce higher powers / reciprocal powers | `ALGEBRAIC_RELATION_POWER_REDUCTION` | scored; `k=70` |
| `Q04` | Algebra | Cube-root expression engineered for algebraic identity | `CUBE_ROOT_IDENTITY_COLLAPSE` | scored; solution gives `3∛42`; secondary notation needs custody |
| `Q05` | Geometry | Intersecting-chord/secant power gives a value absent listed options | `POWER_OF_POINT_LENGTH_RECOVERY` | key `*`; scoring unresolved; not ordinary scored evidence |
| `Q06` | Geometry | Equal arc/chord + similarity | `CIRCLE_ARC_CHORD_SIMILARITY` | key C / `22.5`; target-label conflict in secondary text; figure gated |
| `Q07` | Algebra | Normalize exponential ratio to quadratic in `(2/3)^x` | `EXPONENTIAL_RATIO_NORMALIZATION` | scored; 2 real roots |
| `Q08` | Inequality | Weighted product maximum under quadratic resource constraint | `WEIGHTED_PRODUCT_MAX_UNDER_QUADRATIC_CONSTRAINT` | **BONUS**; derived value absent options |
| `Q09` | Algebra/Number Theory | Square/subtract simultaneous integer equations | `INTEGER_SYSTEM_SUBSTITUTION_COUNT` | scored; 2 pairs |
| `Q10` | Geometry | Shaded area in three unit squares | `UNIT_SQUARE_SHADED_AREA` | scored; figure gated |
| `Q11` | Geometry | Diameter/circle angle chase | `CIRCLE_DIAMETER_ANGLE_CHAIN` | scored; figure gated |
| `Q12` | Number Theory/Combinatorics | Mod-4 parity/residue ordered-pair count | `ORDERED_PAIR_MODULAR_COUNT` | scored key D / 1250; exact statement corrupted in secondary text -> source gated |
| `Q13` | Number Theory | Positive integer solutions via discriminant perfect-square restriction | `POSITIVE_INTEGER_QUADRATIC_DIOPHANTINE` | scored; 2 pairs |
| `Q14` | Algebra | Pair sum/difference squares and cancel | `ALGEBRAIC_IDENTITY_COLLAPSE` | scored; key B |
| `Q15` | Sequences | Weighted arithmetic-pattern sum -> `3Σn²+Σn` | `WEIGHTED_ARITHMETIC_SUM` | scored; 122500 |
| `Q16` | Algebra | Two polynomials share a root; eliminate common-root powers/parameter | `COMMON_ROOT_POLYNOMIAL_ELIMINATION` | **BONUS** |
| `Q17` | Inequality | Test boundedness under product constraint | `PRODUCT_CONSTRAINT_UNBOUNDEDNESS_TEST` | scored; answer `∞`; source is mathematically unbounded, not a finite-maximum defect |
| `Q18` | Number Theory | Consecutive coprime factors cannot form positive square product | `CONSECUTIVE_PRODUCT_PERFECT_SQUARE` | scored; 0 |
| `Q19` | Geometry | Square equal-distance condition -> perpendicular bisector + area ratio | `SQUARE_EQUAL_DISTANCE_AREA_RATIO` | scored; 19 |
| `Q20` | Algebra/Exponents | Radical/exponential equations -> relations in exponent ratios | `EXPONENT_SYSTEM_LINEARIZATION` | scored; sum of roots 4; notation requires careful custody |
| `Q21` | Algebra | Nested radicals reconstructed as simpler square-root sum | `NESTED_RADICAL_RECONSTRUCTION` | scored; 8 |
| `Q22` | Geometry | Equal-length/cyclic angle chain | `GEOMETRY_ANGLE_CHAIN` | scored; 114°; figure gated |
| `Q23` | Algebra | Add-one transformation exposes reciprocal/AP-like linear structure | `CYCLIC_RATIO_ALGEBRA_REDUCTION` | scored; 2 |
| `Q24` | Algebra/Means | AM and GM -> sum/product -> recover larger number | `AM_GM_RECOVER_NUMBERS` | scored; 32 |
| `Q25` | Combinatorics | Count two-digit numbers with different odd digits | `DIGIT_COUNT_DISTINCT_PARITY` | **SOURCE_CONFLICT**: printed wording implies 20, supplied solution/key gives 12 |
| `Q26` | Algebra | Cube roots to common basis `t=∛2` | `CUBE_ROOT_BASIS_SIMPLIFICATION` | scored; 84 |
| `Q27` | Algebra | `xy/(x+y)` relations become linear after reciprocals | `RECIPROCAL_SYSTEM_LINEARIZATION` | scored; 36 |
| `Q28` | Algebra/Number Theory | Intersect inequalities, retain natural numbers, sum | `INTEGER_INTERVAL_FROM_INEQUALITIES` | scored; 1 |
| `Q29` | Sequences | GP parameter recovery; huge-index ratios collapse | `GP_PARAMETER_RECOVERY_HIGH_INDEX_COLLAPSE` | scored; 5 |
| `Q30` | Algebra/Geometry | Area + base-height difference -> quadratic -> reduced ratio | `AREA_CONSTRAINT_QUADRATIC_RECOVERY` | scored; 7 |

## Scoring/source custody

- explicit bonus: Q08, Q16;
- starred/no-normal-option status: Q05;
- clean-source conflicts/blockers: Q02, Q05, Q06, Q12, Q25;
- figure-gated student anchors: Q06, Q10, Q11, Q22 (and retain Q19 figure where available).

Detailed answer/path reasoning is in `2023_Bhaskara_Preliminary_Qualification_v1.md`.
