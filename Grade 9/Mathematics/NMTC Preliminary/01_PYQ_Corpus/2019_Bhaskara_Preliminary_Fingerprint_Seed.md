# 2019 Bhaskara Preliminary — Fingerprint Seed

Initial source: Cheenta reproduction, `https://cheenta.com/bhaskara-contest-nmtc-primary-2019-ix-and-x-grades-stage-i-problems-and-solution/`.

Independent recovery sources now include the Resonance-hosted 2019 Junior solution PDF and matching reproductions. The Cheenta page is **truncated after Q25**; it is not a complete paper source.

Corrected observed structure: **30 questions**; Q1–15 option-based, Q16–30 fill-in.

| ID | Domain | Mechanism / hidden structure | Seed archetype | Source status |
|---|---|---|---|---|
| `NMTC-BH-P-2019-Q01` | Combinatorics/NT | `ABCABC = 1001*ABC`; divisibility by 13 automatic, then digit constraints | `REPEATED_DIGIT_FACTOR_COUNT` | COMPLETE |
| `Q02` | Geometry | Perpendicular medians -> metric relation among sides | `PERPENDICULAR_MEDIANS_SIDE_RELATION` | COMPLETE |
| `Q03` | Geometry | Two isosceles triangles sharing a diagonal; classify incircle/circumcircle | `QUADRILATERAL_CYCLIC_TANGENTIAL_CLASSIFICATION` | COMPLETE |
| `Q04` | Number Theory | Integer cube sides with fixed sum of squares; enumerate representations then volumes | `INTEGER_SUM_OF_SQUARES_ENUMERATION` | COMPLETE |
| `Q05` | Geometry/Inequality | Rhombus diagonals satisfy fixed sum of squares; optimize with side constraints | `RHOMBUS_DIAGONAL_BOUND_OPTIMIZATION` | COMPLETE |
| `Q06` | Number Theory/Sequences | Consecutive block sums divisible by 11 | `PREFIX_SUM_MODULAR_BLOCK_COUNT` | COMPLETE |
| `Q07` | Combinatorics | Sum products over all nonempty subsets -> product expansion | `SUBSET_PRODUCT_GENERATING_PRODUCT` | COMPLETE |
| `Q08` | Algebra | Remainder mod `x^2-1`; reduce powers | `POLYNOMIAL_REMAINDER_POWER_REDUCTION` | COMPLETE |
| `Q09` | Combinatorics/Geometry | Count acute triangles among box vertices | `BOX_VERTEX_TRIANGLE_CLASSIFICATION_COUNT` | COMPLETE |
| `Q10` | Arithmetic | Long repeated-digit subtraction; borrow pattern controls digit sum | `REPEATED_DIGIT_BORROW_PATTERN` | COMPLETE |
| `Q11` | Number Theory/Algebra | Symmetric rational equation in positive integers; bound sum/product | `POSITIVE_INTEGER_SYMMETRIC_RATIONAL` | COMPLETE |
| `Q12` | Combinatorics | Count connected three-stamp shapes on supplied 16-stamp figure | `GRID_CONNECTED_TRIOMINO_COUNT` | IMAGE_REQUIRED_FOR_STUDENT_ANCHOR; answer recovered |
| `Q13` | Arithmetic/Algebra | Winner margins determine candidate votes | `MARGIN_SYSTEM_LINEAR_RECOVERY` | COMPLETE |
| `Q14` | Arithmetic/Combinatorics | Competition scoring; determine impossible listed score | `SCORING_SYSTEM_ATTAINABILITY` | SOURCE_RESOLVED_BY_INDEPENDENT_MATCH |
| `Q15` | Inequality/Combinatorics | Symmetric elementary-sum expression; convert to product and balance integers | `FIXED_SUM_SHIFTED_PRODUCT_MAX` | SOURCE_RESOLVED_BY_INDEPENDENT_MATCH |
| `Q16` | Number Theory | Place-value equation from quotient/remainder digit relation | `DIGIT_DIVISION_PLACE_VALUE` | COMPLETE |
| `Q17` | Number Theory | `N - digit_sum(N) = digit_sum(N)^2` | `DIGIT_SUM_DIOPHANTINE` | COMPLETE |
| `Q18` | Combinatorics | Complete anti-magic square via consecutive row/column/diagonal totals | `ANTIMAGIC_SQUARE_CONSTRAINT_PROPAGATION` | IMAGE_REQUIRED_FOR_STUDENT_ANCHOR; answer recovered |
| `Q19` | Arithmetic | Escalator rate + walking rate; two equations recover fixed step count | `ESCALATOR_RELATIVE_RATE` | COMPLETE |
| `Q20` | Sequences/Number Theory | Coin tower as difference of triangular numbers; maximize row count | `TRIANGULAR_NUMBER_DIFFERENCE_FACTOR_MAX` | SOURCE_RESOLVED_BY_INDEPENDENT_MATCH; BONUS |
| `Q21` | Geometry | Mutually tangent circles; center-distance equations | `MULTIPLE_TANGENT_CIRCLES_RADIUS` | IMAGE_REQUIRED_FOR_STUDENT_ANCHOR; answer recovered |
| `Q22` | Algebra | Power equals 1; split exponent-zero/base `±1` cases | `POWER_EQUALS_ONE_CASE_SPLIT` | COMPLETE |
| `Q23` | Combinatorics | Exact-length king paths on supplied grid | `KING_PATH_EXACT_MOVE_COUNT` | IMAGE_REQUIRED_FOR_STUDENT_ANCHOR; answer recovered |
| `Q24` | Geometry | Dense equal-length/angle configuration; chained isosceles/equilateral deductions | `EQUAL_LENGTH_GEOMETRY_ANGLE_CHAIN` | IMAGE_REQUIRED_FOR_STUDENT_ANCHOR; answer recovered |
| `Q25` | Algebra | High-degree symmetric equations -> ratio/factor reduction | `SYMMETRIC_HIGH_DEGREE_FACTOR_REDUCTION` | COMPLETE |
| `Q26` | Number Theory | Odd prime divisor of `2019^8+1`; multiplicative order forces `p ≡ 1 mod 16` | `PRIME_DIVISOR_ORDER_FILTER` | SOURCE_RECOVERED_AFTER_CHEENTA_TRUNCATION |
| `Q27` | Number Theory | `a^2-b^2=100c` under bounds; exploit square residues / factor structure | `BOUNDED_DIFFERENCE_SQUARES_MULTIPLE_COUNT` | SOURCE_RECOVERED_AFTER_CHEENTA_TRUNCATION |
| `Q28` | Number Theory/Combinatorics | Signed base-3 coefficients; unique balanced-ternary representation and sign count | `BALANCED_TERNARY_NONNEGATIVE_COUNT` | SOURCE_RECOVERED_AFTER_CHEENTA_TRUNCATION |
| `Q29` | Sequences | Functional recurrence `a_{m+n}=a_m+a_n+mn`; doubling indices | `FUNCTIONAL_SEQUENCE_DOUBLING` | SOURCE_RECOVERED_AFTER_CHEENTA_TRUNCATION |
| `Q30` | Algebra/Combinatorics | Coefficient of product of two finite geometric sums = count exponent pairs | `POLYNOMIAL_COEFFICIENT_PAIR_COUNT` | SOURCE_RECOVERED_AFTER_CHEENTA_TRUNCATION |

## Source recovery corrections

1. The earlier 25-question interpretation was false; the Cheenta webpage stops at Q25, but the Resonance 2019 Junior solution PDF and matching reproductions continue through Q30.
2. Q14's missing stem is recovered as an attainability question: determine which listed score is impossible.
3. Q15's final transcribed `T × 1` is independently matched as `T × I`.
4. Q20 is explicitly marked **BONUS** in the recovered solution source and must not contribute to ordinary scored-item frequency/difficulty statistics.
5. Q26–Q30 must be included in all 2019 domain/archetype counts.
