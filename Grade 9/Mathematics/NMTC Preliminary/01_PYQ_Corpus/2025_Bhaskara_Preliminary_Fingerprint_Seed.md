# 2025 Bhaskara Preliminary — Fingerprint Seed

Source: Cheenta reproduction, `https://cheenta.com/nmtc-screening-test-bhaskara-contest-2025/`

Provenance at ingestion: `P2_REPUTABLE_SECONDARY_ARCHIVE`.

Observed paper structure: 30 questions; Q1–Q15 MCQ, Q16–Q30 fill-in.

This is a **mechanism seed**, not a final solved/verified corpus. Full third-party question wording is intentionally not reproduced here.

| ID | Format | Domain | Mechanism / hidden structure | Seed archetype | Source status |
|---|---|---|---|---|---|
| `NMTC-BH-P-2025-Q01` | MCQ | Number Theory | Common remainder with several divisors -> LCM plus fixed residue, then largest 4-digit value | `COMMON_REMAINDER_LCM_BOUND` | COMPLETE |
| `Q02` | MCQ | Geometry | Shaded-area relation inside rectangle | `RECTANGLE_SHADED_AREA_DECOMPOSITION` | IMAGE_REQUIRED |
| `Q03` | MCQ | Algebra/Radicals | Normalize seventh-root expression and isolate a rational parameter | `RADICAL_EQUATION_COMMON_ROOT_FACTOR` | COMPLETE |
| `Q04` | MCQ | Algebra | Conjugate surds raised to fractional power; identify perfect-square/cube structure before expansion | `CONJUGATE_SURD_POWER_COLLAPSE` | COMPLETE |
| `Q05` | MCQ | Geometry | Multi-angle figure; short angle chase | `GEOMETRY_ANGLE_CHAIN` | IMAGE_REQUIRED |
| `Q06` | MCQ | Geometry/Trig | Right triangle, inradius/circumradius and half-angle expressions | `RIGHT_TRIANGLE_RADIUS_HALF_ANGLE` | COMPLETE |
| `Q07` | MCQ | Algebra/Graphs | Absolute-value equations as intersecting V-shaped loci; recover coordinate sum | `ABSOLUTE_VALUE_LOCUS_INTERSECTION` | COMPLETE |
| `Q08` | MCQ | Arithmetic | Pairwise work rates -> recover individual/combined rate; ask for half-work time | `PAIRWISE_WORK_RATE_RECONSTRUCTION` | COMPLETE |
| `Q09` | MCQ | Algebra | Radical ratio; rationalize / cross-transform to target symmetric expression | `RADICAL_RATIO_RATIONALIZATION_TARGET` | COMPLETE |
| `Q10` | MCQ | Algebra/Inequality | Absolute rational inequality -> interval restriction -> count integral solutions | `RATIONAL_ABSOLUTE_INEQUALITY_INTEGER_COUNT` | COMPLETE |
| `Q11` | MCQ | Geometry | Two touching circles + tangents + angle relations | `TWO_CIRCLES_TANGENT_ANGLE_CHAIN` | IMAGE_REQUIRED |
| `Q12` | MCQ | Algebra/Logs | Let `t=sqrt(log_2 x)`; solve quadratic in transformed variable and map back | `LOG_SQRT_QUADRATIC_SUBSTITUTION` | COMPLETE |
| `Q13` | MCQ | Number Theory | Square a known residue modulo 11 | `MODULAR_SQUARE_DIRECT` | COMPLETE |
| `Q14` | MCQ | Number Theory/Algebra | Digit-place representation + digit relation + product condition | `DIGIT_EQUATION_PLACE_VALUE` | COMPLETE |
| `Q15` | MCQ | Geometry | Pentagon angle relations and angle bisectors | `POLYGON_ANGLE_BISECTOR_CHAIN` | IMAGE_REQUIRED |
| `Q16` | Fill | Algebra | Realness forces equality from `(b+c)^2=-4a^2`; collapse variables then odd powers cancel | `REAL_CONSTRAINT_SUM_SQUARE_COLLAPSE` | COMPLETE |
| `Q17` | Fill | Algebra/Functions | Iterate a fractional-linear function and simplify composition before solving | `MOBIUS_FUNCTION_ITERATION` | COMPLETE |
| `Q18` | Fill | Algebra | Cube-root equation; cube/factor after structure recognition, then sum roots | `CUBE_ROOT_EQUATION_FACTORIZATION` | COMPLETE |
| `Q19` | Fill | Geometry | Touching quadrants / midpoint angle relation | `TOUCHING_QUADRANTS_ANGLE` | IMAGE_REQUIRED |
| `Q20` | Fill | Algebra/Number Theory | Cubic with three positive integer roots; Vieta fixes the root multiset | `CUBIC_POSITIVE_INTEGER_ROOTS_VIETA` | COMPLETE |
| `Q21` | Fill | Combinatorics/Number Theory | Count 3-digit numbers with fixed units digit satisfying divisibility by 9 | `DIGIT_COUNT_DIVISIBILITY_CONSTRAINT` | COMPLETE |
| `Q22` | Fill | Algebra | Difference-of-cubes identity collapses a large expression | `DIFFERENCE_OF_CUBES_COLLAPSE` | COMPLETE |
| `Q23` | Fill | Arithmetic | Percent categories; infer total from remaining count | `PERCENT_COMPLEMENT_TOTAL` | COMPLETE |
| `Q24` | Fill | Algebra | Evaluate difference of absolute polynomial expressions at large positive parameter; determine signs then cancel | `ABSOLUTE_POLYNOMIAL_SIGN_CANCELLATION` | COMPLETE |
| `Q25` | Fill | Geometry | Rectangle diagonal extension intersects circular hoop at highest point; metric geometry | `RECTANGLE_CIRCLE_SECANT_METRIC` | IMAGE_REQUIRED |
| `Q26` | Fill | Number Theory/Algebra | Rational expression in natural `n`; polynomial division/divisibility reduces to finite divisor conditions | `INTEGER_VALUED_RATIONAL_DIVISIBILITY` | COMPLETE |
| `Q27` | Fill | Algebra/Logs | Convert logarithmic equation to algebraic relation and intersect with quadratic constraint | `LOG_SYSTEM_ALGEBRAIC_CONVERSION` | COMPLETE |
| `Q28` | Fill | Geometry | Tangents + parallel segment + given lengths; similarity/power relation | `TANGENT_PARALLEL_LENGTH_TRANSFER` | IMAGE_REQUIRED |
| `Q29` | Fill | Arithmetic | Dry mass is invariant while water percentage changes | `PERCENTAGE_INVARIANT_DRY_MASS` | COMPLETE |
| `Q30` | Fill | Sequences | GP term-difference and partial-sum constraints determine ratio/terms | `GP_TERM_DIFFERENCE_CONSTRAINT` | COMPLETE |

## Immediate observations — not yet cross-year weights

The 2025 paper reinforces several behaviors also visible in 2024:

- substitution into a simpler variable rather than direct attack;
- identity recognition in radicals and powers;
- modular and divisibility compression;
- Vieta for integer/root structure;
- percentage/rate problems governed by an invariant rather than routine formulas;
- geometry that depends on quick recognition of tangent, parallel, radius, similarity, and angle relations;
- objective questions whose main difficulty is selecting the right first move, not lengthy calculation.

These overlaps become candidate recurring archetypes only after independent solution checking and additional-year ingestion.
