# 2023 Bhaskara Preliminary — Fingerprint Seed

Source: Cheenta reproduction, `https://cheenta.com/bhaskara-contest-nmtc-junior-level-ix-and-x-grades-2023-problems-and-solutions/`

Provenance at ingestion: `P2_REPUTABLE_SECONDARY_ARCHIVE`.

Observed structure: 30 questions, with Q1–15 option-based and Q16–30 fill-in on the reproduced page.

| ID | Domain | Mechanism / hidden structure | Seed archetype | Source status |
|---|---|---|---|---|
| `NMTC-BH-P-2023-Q01` | Algebra | Expand `(x+c)^3` and match coefficients | `POLYNOMIAL_PERFECT_POWER_COEFFICIENT_MATCH` | COMPLETE |
| `Q02` | Geometry | Median with side data; metric relation then angle extraction | `TRIANGLE_MEDIAN_METRIC_ANGLE` | IMAGE_REQUIRED |
| `Q03` | Algebra | Use given quadratic relation to reduce higher powers in a rational expression | `ALGEBRAIC_RELATION_POWER_REDUCTION` | COMPLETE |
| `Q04` | Algebra | Cube-root/radical expression engineered for an algebraic identity | `CUBE_ROOT_IDENTITY_COLLAPSE` | TRANSCRIPTION_SUSPECT |
| `Q05` | Geometry | Equal segments + midpoint; metric geometry from figure | `EQUAL_SEGMENT_MIDPOINT_METRIC` | IMAGE_REQUIRED |
| `Q06` | Geometry | Arc/circle metric relation | `CIRCLE_ARC_CHORD_METRIC` | SOURCE_CONFLICT |
| `Q07` | Algebra | Normalize exponential ratio into a simpler base variable | `EXPONENTIAL_RATIO_NORMALIZATION` | COMPLETE |
| `Q08` | Inequality | Maximize monomial under quadratic constraint using weighted AM-GM / substitution | `WEIGHTED_PRODUCT_MAX_UNDER_QUADRATIC_CONSTRAINT` | COMPLETE |
| `Q09` | Number Theory/Algebra | Substitute one integer equation into another; bound possible integer values | `INTEGER_SYSTEM_SUBSTITUTION_COUNT` | COMPLETE |
| `Q10` | Geometry | Shaded area in three unit squares | `UNIT_SQUARE_SHADED_AREA` | IMAGE_REQUIRED |
| `Q11` | Geometry | Diameter/circle angle chase | `CIRCLE_DIAMETER_ANGLE_CHAIN` | IMAGE_REQUIRED |
| `Q12` | Number Theory/Combinatorics | Count ordered pairs satisfying a modular residue condition | `ORDERED_PAIR_MODULAR_COUNT` | TRANSCRIPTION_SUSPECT |
| `Q13` | Number Theory | Positive integer solutions of quadratic-linear Diophantine equation | `POSITIVE_INTEGER_QUADRATIC_DIOPHANTINE` | COMPLETE |
| `Q14` | Algebra | Large expression collapses by grouping/sum-of-squares identity | `ALGEBRAIC_IDENTITY_COLLAPSE` | COMPLETE |
| `Q15` | Sequences | Weighted arithmetic-pattern sum -> polynomial/power sums | `WEIGHTED_ARITHMETIC_SUM` | COMPLETE |
| `Q16` | Algebra | Two polynomials share a root; eliminate common-root powers/parameter | `COMMON_ROOT_POLYNOMIAL_ELIMINATION` | COMPLETE |
| `Q17` | Inequality | Product-fixed positive reals with symmetric quadratic sum | `PRODUCT_CONSTRAINT_SYMMETRIC_BOUND` | SOURCE_CONFLICT |
| `Q18` | Number Theory | Consecutive integers product is a square; exploit coprimality | `CONSECUTIVE_PRODUCT_PERFECT_SQUARE` | COMPLETE |
| `Q19` | Geometry | Interior point in square with equal-distance constraints; area ratio | `SQUARE_EQUAL_DISTANCE_AREA_RATIO` | IMAGE_REQUIRED |
| `Q20` | Algebra/Exponents | Simultaneous radical/exponential equations; convert to linear relations in exponents | `EXPONENT_SYSTEM_LINEARIZATION` | TRANSCRIPTION_SUSPECT |
| `Q21` | Algebra | Nested radicals collapse to sum of square roots | `NESTED_RADICAL_RECONSTRUCTION` | COMPLETE |
| `Q22` | Geometry | Figure-based angle chase | `GEOMETRY_ANGLE_CHAIN` | IMAGE_REQUIRED |
| `Q23` | Algebra | Cyclic rational relation -> normalize ratios and derive target square ratio | `CYCLIC_RATIO_ALGEBRA_REDUCTION` | COMPLETE |
| `Q24` | Algebra/Means | Given AM and GM, recover two positive numbers by sum/product | `AM_GM_RECOVER_NUMBERS` | COMPLETE |
| `Q25` | Combinatorics | Count two-digit numbers with distinct odd digits | `DIGIT_COUNT_DISTINCT_PARITY` | COMPLETE |
| `Q26` | Algebra | Cube-root expression simplification by common radical basis | `CUBE_ROOT_BASIS_SIMPLIFICATION` | COMPLETE |
| `Q27` | Algebra | `xy/(x+y)` relations become linear after reciprocals | `RECIPROCAL_SYSTEM_LINEARIZATION` | COMPLETE |
| `Q28` | Algebra/Number Theory | Intersect inequalities, retain natural numbers, sum them | `INTEGER_INTERVAL_FROM_INEQUALITIES` | COMPLETE |
| `Q29` | Sequences | Determine GP parameters from low terms; huge-index ratios collapse to `r` and `a` | `GP_PARAMETER_RECOVERY_HIGH_INDEX_COLLAPSE` | COMPLETE |
| `Q30` | Algebra/Geometry | Triangle area plus base-height difference -> quadratic then reduced ratio | `AREA_CONSTRAINT_QUADRATIC_RECOVERY` | COMPLETE |

## QC blockers found at seed stage

- Q06 reproduction appears internally inconsistent in the text (a stated length is then apparently requested); figure/original-paper recovery is required.
- Q12 mathematical expression is visibly corrupted in the reproduction and must not become a canonical anchor yet.
- Q17 as transcribed asks for a maximum under `abcd=1` for an expression that appears unbounded; likely wording/sign/minimum transcription issue. Treat as `SOURCE_CONFLICT` until original evidence is recovered.
- Q20 notation appears damaged and requires source comparison.
