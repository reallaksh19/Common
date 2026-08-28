# 2018 Bhaskara Preliminary — Fingerprint Seed

Source: Cheenta reproduction, `https://cheenta.com/bhaskara-contest-nmtc-junior-2018-ix-and-x-grades-stage-i-problems-and-solution/`

Independent match: a second reproduction carrying the AMTI Junior paper/solution text was used to resolve scoring disposition and answer/source conflicts. This supports P1 faithful-match treatment for matched items but is not an AMTI-hosted P0 source.

Observed reproduced structure: 30 questions; Q1–15 option-based, Q16–30 fill-in.

| ID | Domain | Mechanism / hidden structure | Seed archetype | Source status |
|---|---|---|---|---|
| `NMTC-BH-P-2018-Q01` | Algebra | Simplify radicals to a common basis before division | `RADICAL_COMMON_BASIS_SIMPLIFICATION` | COMPLETE |
| `Q02` | Arithmetic | Train length/speed from pole and platform crossing times | `RELATIVE_LENGTH_SPEED_RECOVERY` | COMPLETE |
| `Q03` | Algebra | Multivariable polynomial/factor question whose listed options do not match the reproduced expression | `MULTIVARIABLE_FACTORIZATION_PATTERN` | `SOURCE_RESOLVED_BY_INDEPENDENT_MATCH`; **BONUS** |
| `Q04` | Algebra | Subtract same unknown from four numbers and impose proportion | `COMMON_SHIFT_PROPORTION_EQUATION` | COMPLETE |
| `Q05` | Algebra | Mixed exponential equation; direct substitution gives `x=3`, absent from listed choices | `MIXED_BASE_EXPONENTIAL_EQUATION` | `SOURCE_RESOLVED_BY_INDEPENDENT_MATCH`; **BONUS** |
| `Q06` | Algebra | Given quadratic relation reduces cubic polynomial value | `ALGEBRAIC_RELATION_POWER_REDUCTION` | COMPLETE |
| `Q07` | Algebra | Parameter quadratic has a repeated root -> discriminant zero; recovered values `4,-20`, requested sum `-16` absent from listed options | `QUADRATIC_PARAMETER_DOUBLE_ROOT` | `SOURCE_RESOLVED_BY_INDEPENDENT_MATCH`; **BONUS** |
| `Q08` | Number Theory | Trailing zeros of `100!` -> count factors of 5 | `FACTORIAL_TRAILING_ZERO_VALUATION` | COMPLETE |
| `Q09` | Geometry/Arithmetic | Similar scaling: 20% side increase -> square scale for area | `SIMILAR_FIGURE_AREA_SCALE` | COMPLETE |
| `Q10` | Number Theory | Coprime rational expression constrained to be integer; use divisibility | `COPRIME_RATIONAL_INTEGRALITY` | COMPLETE |
| `Q11` | Number Theory | Four-digit square with fixed first/last digits; narrow square interval and units digit | `PERFECT_SQUARE_DIGIT_CONSTRAINT` | COMPLETE |
| `Q12` | Inequality | Reciprocal linear constraint; minimize sum using Cauchy/AM-GM structure | `RECIPROCAL_CONSTRAINT_MINIMUM` | COMPLETE |
| `Q13` | Algebra/Inequality | Minimize positive-definite quadratic form by completing squares | `QUADRATIC_FORM_MINIMUM` | COMPLETE |
| `Q14` | Geometry | Incenter angle theorem `90 + A/2` | `INCENTER_ANGLE_RELATION` | COMPLETE |
| `Q15` | Geometry | Square + rhombus equal-side angle chain | `SQUARE_RHOMBUS_ANGLE_CHAIN` | `IMAGE_REQUIRED_FOR_STUDENT_ANCHOR`; recovered answer `15°` |
| `Q16` | Geometry | Square with points on adjacent sides and `45°` apex relation; derive length ratio | `SQUARE_45_DEGREE_LENGTH_RATIO` | COMPLETE; solution independently matched |
| `Q17` | Arithmetic | Five consecutive numbers; average identifies middle term | `CONSECUTIVE_NUMBERS_AVERAGE_CENTER` | COMPLETE |
| `Q18` | Number Theory | `n^2+96=m^2` -> factor difference of squares and count factor pairs | `PERFECT_SQUARE_DIFFERENCE_FACTOR_PAIRS` | COMPLETE |
| `Q19` | Number Theory | Integer square root of rational function -> rearrange to divisor/bound conditions | `INTEGER_RADICAL_RATIONAL_CONSTRAINT` | COMPLETE |
| `Q20` | Algebra/Number Theory | Reduced fraction with numerator/denominator relation and unit increase | `FRACTION_DIOPHANTINE_LINEAR` | COMPLETE |
| `Q21` | Algebra | Let `x=t+1/t`; cubic identity collapses target | `RECIPROCAL_CUBE_IDENTITY` | COMPLETE |
| `Q22` | Geometry | Heptagon interior-angle sum with repeated unknown angle | `POLYGON_ANGLE_SUM_UNKNOWN` | COMPLETE |
| `Q23` | Geometry | Altitude splits base in fixed ratio; difference of squared sides collapses | `ALTITUDE_SIDE_SQUARE_DIFFERENCE` | COMPLETE |
| `Q24` | Geometry/Mensuration | Cube -> inscribed sphere -> inscribed cube; scale through diameters/diagonals | `NESTED_CUBE_SPHERE_SCALING` | COMPLETE |
| `Q25` | Number Theory | Multiple of 7 constrained by square-root interval | `MULTIPLE_IN_SQUARE_INTERVAL` | COMPLETE |
| `Q26` | Algebra | Radical ratio equation; cross multiply then square with domain check | `RADICAL_RATIO_EQUATION` | COMPLETE |
| `Q27` | Arithmetic/Algebra | Work-rate change from `M,m` to `M+N,m-n`; eliminate total work | `WORK_RATE_PARAMETER_ELIMINATION` | COMPLETE |
| `Q28` | Number Theory | Two-digit number digit sum + reversal difference | `DIGIT_REVERSAL_LINEAR_SYSTEM` | COMPLETE |
| `Q29` | Number Theory | Units digit of huge power -> last-digit cycle | `MODULAR_LAST_DIGIT_CYCLE` | COMPLETE |
| `Q30` | Algebra | Cyclic ratio system; normalize by total/sum variables | `CYCLIC_RATIO_SYSTEM` | COMPLETE |

## Resolution record

The seed-stage interpretation treated Q03/Q05/Q07 as unexplained source conflicts. Independent solution recovery now explicitly identifies all three as **Bonus** items. Their mathematics may inform concept research, but they must be excluded from ordinary scored-question frequency and difficulty statistics.

Detailed first moves, derived answers, profiles, and qualification counts are in `2018_Bhaskara_Preliminary_Qualification_v1.md`.
