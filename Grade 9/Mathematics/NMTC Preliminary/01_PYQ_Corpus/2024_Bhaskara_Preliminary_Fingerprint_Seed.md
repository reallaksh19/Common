# 2024 Bhaskara Preliminary — Fingerprint Seed

Source: Cheenta reproduction, `https://cheenta.com/screening-test-bhaskara-contestnmtc-junior-level-ix-and-x-grades2024-2025/`

Provenance at ingestion: `P2_REPUTABLE_SECONDARY_ARCHIVE`.

Observed paper structure: 30 questions; Q1–Q15 MCQ, Q16–Q30 fill-in.

This is a **mechanism seed**, not a final solved/verified corpus. Full third-party question wording is intentionally not reproduced here.

| ID | Format | Domain | Mechanism / hidden structure | Seed archetype | Source status |
|---|---|---|---|---|---|
| `NMTC-BH-P-2024-Q01` | MCQ | Algebra | Reduce high powers using the given quadratic relation instead of solving for the root | `ALGEBRAIC_RELATION_POWER_REDUCTION` | COMPLETE |
| `Q02` | MCQ | Geometry/Arithmetic | Clock-hand angular speeds and relative-angle calculation | `CLOCK_RELATIVE_ANGULAR_SPEED` | COMPLETE |
| `Q03` | MCQ | Geometry | Diameter + two tangents; angle chase from tangent/radius/circle relations | `CIRCLE_TANGENT_ANGLE_CHAIN` | IMAGE_REQUIRED |
| `Q04` | MCQ | Algebra | Reorganize mixed exponential terms to expose a common factor/base relation | `EXPONENTIAL_EQUATION_FACTOR_TRANSFORM` | COMPLETE |
| `Q05` | MCQ | Algebra | Divisibility by quadratic factor -> coefficient/remainder constraints | `POLYNOMIAL_DIVISIBILITY_COEFFICIENT_MATCH` | COMPLETE |
| `Q06` | MCQ | Algebra | Symmetric products in rational equation; simplify before expansion | `RATIONAL_EQUATION_SYMMETRIC_PRODUCT` | COMPLETE |
| `Q07` | MCQ | Algebra | Coupled radical equations; subtract/factor using `a != b` | `COUPLED_RADICAL_DIFFERENCE_FACTOR` | COMPLETE |
| `Q08` | MCQ | Geometry | Tangents + a parallel chord/line convert angle information | `TANGENT_PARALLEL_ANGLE_TRANSFER` | IMAGE_REQUIRED |
| `Q09` | MCQ | Algebra | Same-base exponential equation; isolate exponent then match requested quadratic | `EXPONENTIAL_POWER_NORMALIZATION` | COMPLETE |
| `Q10` | MCQ | Algebra/Sequences | Structured weighted square sum -> polynomial expansion + standard power sums | `WEIGHTED_POWER_SUM_REDUCTION` | TRANSCRIPTION_SUSPECT |
| `Q11` | MCQ | Sequences | Recurrence linearizes after taking reciprocals; then summation/telescoping structure | `RECURRENCE_RECIPROCAL_LINEARIZATION` | COMPLETE |
| `Q12` | MCQ | Algebra/Logs | Set logarithm as a variable and convert exponent equation to algebraic equation | `LOG_EXPONENT_QUADRATIC_SUBSTITUTION` | COMPLETE |
| `Q13` | MCQ | Geometry/Sequences | Successively tangent circles inside a fixed angle produce a scale/ratio progression | `TANGENT_CIRCLES_HOMOTHETY_RATIO` | IMAGE_REQUIRED |
| `Q14` | MCQ | Algebra | Recover original quadratic data from mistaken coefficient, then form equation in root ratios | `VIETA_TRANSFORMED_ROOT_RATIO` | COMPLETE |
| `Q15` | MCQ | Algebra | Difference of squares + common binomial factor; avoid brute expansion | `IDENTITY_DIFFERENCE_OF_SQUARES_FACTOR` | COMPLETE |
| `Q16` | Fill | Algebra | Polynomial division by `x^2+1` gives alternating coefficient pattern; exploit even power | `QUOTIENT_COEFFICIENT_PERIODICITY` | COMPLETE |
| `Q17` | Fill | Algebra/Inequality | Positive quartic roots with product 1 and sum 4 force equality; then Vieta | `VIETA_AMGM_EQUALITY_ROOT_COLLAPSE` | COMPLETE |
| `Q18` | Fill | Geometry | Semicircle + tangent length/ratio relation | `SEMICIRCLE_TANGENT_LENGTH_RATIO` | IMAGE_REQUIRED |
| `Q19` | Fill | Geometry/Trig | Triangle tangent ratio + angle identity, then side ratio | `TRIANGLE_TANGENT_RATIO_TO_SIDE_RATIO` | COMPLETE |
| `Q20` | Fill | Number Theory | Simultaneous small congruences; reconstruct residue modulo 120 | `SIMULTANEOUS_CONGRUENCE_RECONSTRUCTION` | COMPLETE |
| `Q21` | Fill | Number Theory | Same remainder divisor -> GCD of pairwise differences | `COMMON_REMAINDER_GCD_DIFFERENCES` | COMPLETE |
| `Q22` | Fill | Algebra/Functions | Function argument shift moves roots; use Vieta after translation | `FUNCTION_SHIFT_ROOT_TRANSLATION` | COMPLETE |
| `Q23` | Fill | Mensuration | Largest cylinder inside cube; geometric constraint fixes radius/height | `INSCRIBED_CYLINDER_IN_CUBE` | COMPLETE |
| `Q24` | Fill | Algebra | Factor quartic and identify irreducible quadratic factor | `QUARTIC_STRUCTURAL_FACTORIZATION` | COMPLETE |
| `Q25` | Fill | Geometry | Square embedded against semicircle; metric relation from figure | `SQUARE_SEMICIRCLE_METRIC_RELATION` | IMAGE_REQUIRED |
| `Q26` | Fill | Algebra | Nested radicals simplify through a disguised identity / normalization | `RADICAL_EXPRESSION_IDENTITY_NORMALIZATION` | COMPLETE |
| `Q27` | Fill | Sequences/Number Theory | Infinite GP and sum-of-squares relation determine ratio; final floor operation | `INFINITE_GP_SUM_SQUARES_CONSTRAINT` | COMPLETE |
| `Q28` | Fill | Algebra/Logs | Convert logarithmic exponent and simplify power exactly | `LOG_EXPONENT_EXACT_SIMPLIFICATION` | COMPLETE |
| `Q29` | Fill | Geometry | Square/tangent/semicircle area relation | `TANGENT_SEMICIRCLE_AREA_TO_RADIUS` | IMAGE_REQUIRED |
| `Q30` | Fill | Algebra | Odd-power polynomial gives `f(-x)=-f(x)`; combine with absolute/trig bound | `ODD_FUNCTION_SYMMETRY_PLUS_BOUND` | COMPLETE |

## Immediate observations — not yet frequency claims

The single 2024 paper already exhibits repeated Preliminary behaviors that the curriculum must train:

- **transform before calculate**;
- use Vieta without solving roots explicitly;
- exploit symmetry/parity/reciprocal transformations;
- recognize polynomial divisibility/remainder structure;
- compress logarithmic and exponential expressions;
- use recurrence transformations;
- combine geometry facts in short angle/metric chains;
- use congruence/GCD structures for remainder questions;
- switch from a long-looking expression to a standard invariant or identity.

Do not convert these observations into cross-year weights until the remaining years are fingerprinted.
