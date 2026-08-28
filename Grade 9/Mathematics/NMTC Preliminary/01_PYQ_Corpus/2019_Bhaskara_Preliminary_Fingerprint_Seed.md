# 2019 Bhaskara Preliminary — Fingerprint Seed

Source: Cheenta reproduction, `https://cheenta.com/bhaskara-contest-nmtc-primary-2019-ix-and-x-grades-stage-i-problems-and-solution/`

Provenance at ingestion: `P2_REPUTABLE_SECONDARY_ARCHIVE`.

Observed reproduced structure: **25 questions**; Q1–15 option-based, Q16–25 fill-in. This is important counter-evidence against hard-coding a universal 30-question historical format.

| ID | Domain | Mechanism / hidden structure | Seed archetype | Source status |
|---|---|---|---|---|
| `NMTC-BH-P-2019-Q01` | Combinatorics/NT | `ABCABC = 1001*ABC`; divisibility by 13 is automatic, leaving digit-constraint counting | `REPEATED_DIGIT_FACTOR_COUNT` | COMPLETE |
| `Q02` | Geometry | Perpendicular medians -> vector/median-length relation among sides | `PERPENDICULAR_MEDIANS_SIDE_RELATION` | COMPLETE |
| `Q03` | Geometry | Two isosceles triangles sharing a diagonal; test cyclic/incircle conditions | `QUADRILATERAL_CYCLIC_TANGENTIAL_CLASSIFICATION` | COMPLETE |
| `Q04` | Number Theory | Integer cube side lengths with fixed sum of squares; enumerate representations then volumes | `INTEGER_SUM_OF_SQUARES_ENUMERATION` | COMPLETE |
| `Q05` | Geometry/Inequality | Rhombus diagonals satisfy fixed sum of squares; optimize their sum with side constraints | `RHOMBUS_DIAGONAL_BOUND_OPTIMIZATION` | COMPLETE |
| `Q06` | Number Theory/Sequences | Consecutive block sums divisible by 11 -> equal prefix sums modulo 11 | `PREFIX_SUM_MODULAR_BLOCK_COUNT` | COMPLETE |
| `Q07` | Combinatorics | Sum products over all nonempty subsets -> expand product of `(1+1/k)` | `SUBSET_PRODUCT_GENERATING_PRODUCT` | COMPLETE |
| `Q08` | Algebra | Remainder mod `x^2-1`; reduce even powers using `x^2=1` | `POLYNOMIAL_REMAINDER_POWER_REDUCTION` | COMPLETE |
| `Q09` | Combinatorics/Geometry | Count acute triangles among box vertices using geometric classification | `BOX_VERTEX_TRIANGLE_CLASSIFICATION_COUNT` | COMPLETE |
| `Q10` | Arithmetic | Long repeated-digit subtraction; borrow pattern controls digit sum | `REPEATED_DIGIT_BORROW_PATTERN` | COMPLETE |
| `Q11` | Number Theory/Algebra | Symmetric rational equation in positive integers; use sum/product bounds/divisibility | `POSITIVE_INTEGER_SYMMETRIC_RATIONAL` | COMPLETE |
| `Q12` | Combinatorics | Count connected three-stamp shapes on a 4x4 grid | `GRID_CONNECTED_TRIOMINO_COUNT` | IMAGE_REQUIRED |
| `Q13` | Arithmetic/Algebra | Winner margins determine all candidate votes from one unknown and total sum | `MARGIN_SYSTEM_LINEAR_RECOVERY` | COMPLETE |
| `Q14` | Arithmetic | Competition scoring rules; reproduced source omits the actual asked quantity | `SCORING_SYSTEM_CASE_ANALYSIS` | SOURCE_INCOMPLETE |
| `Q15` | Inequality/Combinatorics | Symmetric sum of products under fixed positive-integer sum; balance variables | `FIXED_SUM_SYMMETRIC_PRODUCT_MAX` | TRANSCRIPTION_SUSPECT |
| `Q16` | Number Theory | Place-value equation from quotient/remainder digit relation | `DIGIT_DIVISION_PLACE_VALUE` | COMPLETE |
| `Q17` | Number Theory | Number minus digit sum equals square of digit sum; use divisibility/place value | `DIGIT_SUM_DIOPHANTINE` | COMPLETE |
| `Q18` | Combinatorics | Complete anti-magic square using row/column/diagonal consecutive-total constraints | `ANTIMAGIC_SQUARE_CONSTRAINT_PROPAGATION` | IMAGE_REQUIRED |
| `Q19` | Arithmetic | Escalator's own rate + walking rate; two time equations recover fixed step count | `ESCALATOR_RELATIVE_RATE` | COMPLETE |
| `Q20` | Sequences/Number Theory | Tallest decreasing-row coin tower -> largest triangular-number height under total | `TRIANGULAR_NUMBER_BOUND` | IMAGE_CONTEXT_REQUIRED |
| `Q21` | Geometry | Mutually tangent circles with one passing through outer center; radius geometry | `MULTIPLE_TANGENT_CIRCLES_RADIUS` | COMPLETE |
| `Q22` | Algebra | Expression to a variable exponent equals 1; enumerate base/exponent exceptional cases | `POWER_EQUALS_ONE_CASE_SPLIT` | COMPLETE |
| `Q23` | Combinatorics | Exact-length king paths on grid -> constrained path counting / recurrence | `KING_PATH_EXACT_MOVE_COUNT` | IMAGE_REQUIRED |
| `Q24` | Geometry | Dense equal-length/angle configuration; chained isosceles-angle deductions | `EQUAL_LENGTH_GEOMETRY_ANGLE_CHAIN` | IMAGE_REQUIRED |
| `Q25` | Algebra | Factor symmetric high-degree equations using powers of `xy` and `x+y`; reduce target | `SYMMETRIC_HIGH_DEGREE_FACTOR_REDUCTION` | COMPLETE |

## Format evidence

The reproduced 2019 Screening paper has 25 questions, unlike the 30-question reproductions currently available for 2018, 2023, 2024 and 2025. Therefore mock-paper format must be versioned by evidence rather than treated as timeless.
