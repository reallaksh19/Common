# NMTC Bhaskara Preliminary Archetype Catalogue v2

## Authority

This catalogue is derived from the solution-qualified 2018, 2019, 2023, 2024 and 2025 Bhaskara Preliminary corpus.

Use `01_PYQ_Corpus/Five_Year_Scored_Recurrence_v1.md` for the quantitative eligibility rules.

Archetypes describe **mathematical moves**, not surface wording.

## Status vocabulary

- `HISTORICALLY_RECURRENT_5Y` — clean scored variants occur across multiple qualified years and the family is stable enough for curriculum use.
- `RECURRENT_3Y_PLUS` — clean scored variants occur in at least three qualified years.
- `RECURRENT_2Y` — clean scored variants occur in at least two qualified years.
- `SINGLE_YEAR_CLEAN` — currently one clean scored year.
- `BONUS_SUPPORTED` — current PYQ support is bonus/starred rather than ordinary scored evidence.
- `SOURCE_CONFLICT_ONLY` — observed but clean canonical source is unresolved.
- `SYLLABUS_REQUIRED` — must be taught regardless of recurrence.

A family may be `SYLLABUS_REQUIRED` in addition to any recurrence status.

---

# Cross-domain super-families

| Super-family | Qualified-year signal | Status | Curriculum consequence |
|---|---:|---|---|
| `TRANSFORM_BEFORE_CALCULATE` | 5/5 | `HISTORICALLY_RECURRENT_5Y` | every major algebra/NT unit gets recognition + first-line drills |
| `RADICAL_EXPONENT_LOG_COMPRESSION` | 5/5 | `HISTORICALLY_RECURRENT_5Y` | teach representation switching before formula manipulation |
| `DIVISIBILITY_MODULAR_DIGIT_STRUCTURE` | 5/5 | `HISTORICALLY_RECURRENT_5Y` | connect modular arithmetic to digits, cycles, GCD/LCM and integrality |
| `SHORT_GEOMETRY_RECOGNITION_CHAIN` | 5/5 | `HISTORICALLY_RECURRENT_5Y` | geometry requires mark/construct/first-relation drills |
| `INEQUALITY_BOUND_OR_EQUALITY_STRUCTURE` | 5/5 | `HISTORICALLY_RECURRENT_5Y` | boundedness and equality conditions are first-move content |
| `POLYNOMIAL_ROOT_REMAINDER_VIETA_NETWORK` | clean scored support 4/5, plus conflicted 2025 evidence | `RECURRENT_3Y_PLUS` | P0 connected concept package |
| `RATE_PERCENT_INVARIANT_MODELING` | 4/5 | `RECURRENT_3Y_PLUS` | retain cumulative-foundation speed modeling |
| `SEQUENCE_RECURRENCE_ACCUMULATION` | clean 3/5 + conflicted 2025 GP item | `RECURRENT_3Y_PLUS` | add Preliminary layer to existing Sequence & Series architecture |
| `COMBINATORIAL_MODELING_BEYOND_NPR_NCR` | clean 2/5 with high 2019 ceiling | `RECURRENT_2Y` | full syllabus coverage + modeling bridges, not formula-only P&C |

---

# Algebra — stable families

| Family | Recognition trigger | First move | Status / evidence |
|---|---|---|---|
| `ALGEBRAIC_RELATION_POWER_REDUCTION` | high powers plus low-degree relation | rewrite `x^2`/low power and reduce recursively | `RECURRENT_3Y_PLUS`; 2018 Q06, 2023 Q03, 2024 Q01 |
| `POLYNOMIAL_MOD_REDUCTION` | remainder/divisibility by low-degree polynomial | reduce powers modulo divisor | `RECURRENT_2Y`; 2019 Q08, 2024 Q05/Q16 |
| `VIETA_TRANSFORMED_ROOTS` | symmetric/transformed root target | write sum/product before explicit roots | `RECURRENT_2Y` broader root network; 2024 Q14/Q22 plus neighboring years' root structures |
| `POSITIVE_INTEGER_ROOT_CONSTRAINT` | roots constrained positive/integer | combine Vieta with factor partitions, bounds or equality | `RECURRENT_2Y` broader family; clean 2024 Q17 + integer-root/Diophantine bridges |
| `STRUCTURAL_HIGH_DEGREE_FACTORIZATION` | cubic/quartic with small coefficients/symmetry | test identities/simple roots/substitution first | `RECURRENT_2Y`; 2019 Q25, 2024 Q24 |
| `COMMON_ROOT_ELIMINATION` | two polynomials share root | eliminate powers/parameter before solving | `BONUS_SUPPORTED`; 2023 Q16 |
| `IDENTITY_COLLAPSE` | long symmetric/conjugate expression | factor/reconstruct identity before expansion | `HISTORICALLY_RECURRENT_5Y` at super-family level |
| `LOG_VARIABLE_SUBSTITUTION` | log nested in power/root/equation | set transformed log variable | `RECURRENT_2Y`; 2024 Q12/Q28, 2025 Q12/Q27 |
| `EXPONENTIAL_NORMALIZATION` | related mixed bases | common bases / one ratio variable | `RECURRENT_2Y_PLUS`; 2023 Q07, 2024 Q04/Q09 |
| `FUNCTION_SHIFT_OR_ITERATION` | `f(x+c)` or `f(f(x))` | translate input / compose symbolically | `RECURRENT_2Y`; 2024 Q22, 2025 Q17 |
| `RATIONAL_ABSOLUTE_INTERVAL` | rational/absolute inequality | domain split and interval form | `RECURRENT_2Y` broader inequality family |
| `BOUND_BEFORE_OPTIMIZE` | max/min under flexible constraint | test boundedness before inequality | `RECURRENT_2Y_PLUS` within inequality family; 2023 Q17 key contrast |

---

# Sequences & Series

| Family | Trigger | First move | Status |
|---|---|---|---|
| `RECURRENCE_LINEARIZATION` | nonlinear recurrence | reciprocal/difference transform | `RECURRENT_2Y` broader recurrence evidence; clean 2024 Q11 |
| `WEIGHTED_POWER_SUM_REDUCTION` | indexed weighted polynomial sum | expand into standard power sums | `RECURRENT_2Y`; 2023 Q15, 2024 Q10 |
| `INFINITE_GP_CONSTRAINT` | two related infinite sums | express in `a,r`; check `|r|<1` | `SINGLE_YEAR_CLEAN`; 2024 Q27 |
| `GP_PARAMETER_HIGH_INDEX_COLLAPSE` | selected terms / huge index ratios | use `a,r`; cancel common powers before calculating | `RECURRENT_2Y` broader GP evidence; 2023 Q29, 2025 Q30 source-conflicted |
| `FUNCTIONAL_SEQUENCE_RECURRENCE` | `a_{m+n}` rule | substitute useful indices strategically | `SINGLE_YEAR_CLEAN`; 2019 Q29 |

Existing `Sequence and Series/` remains the concept-depth exemplar. The NMTC Preliminary layer must map these mechanisms back to it.

---

# Number Theory

| Family | Trigger | First move | Status |
|---|---|---|---|
| `COMMON_REMAINDER_LCM` | same remainder under several divisors | subtract residue, take LCM | `RECURRENT_2Y` broader remainder family; clean 2025 Q01 |
| `COMMON_REMAINDER_GCD_DIFFERENCES` | greatest divisor leaves equal remainders | take pairwise differences, GCD | `SINGLE_YEAR_CLEAN`; 2024 Q21 |
| `SIMULTANEOUS_CONGRUENCE_RECONSTRUCTION` | multiple congruences | reconstruct common residue systematically | `SINGLE_YEAR_CLEAN`; 2024 Q20 |
| `MODULAR_POWER_CYCLE` | huge power / last digit / residue power | reduce base, detect cycle/order | `RECURRENT_3Y_PLUS`; 2018 Q29, 2019 Q26, 2025 Q13 |
| `PREFIX_RESIDUE_BLOCK_COUNT` | divisible consecutive-block sums | equal prefix residues modulo divisor | `SINGLE_YEAR_CLEAN`; 2019 Q06; high-ceiling bridge |
| `DIGIT_PLACE_VALUE_DIVISIBILITY` | digit conditions | encode number by place value / digit-sum rule | `RECURRENT_3Y_PLUS`; 2018 Q28, 2019 Q16/Q17, 2025 Q14/Q21 |
| `INTEGER_VALUED_RATIONAL_DIVISIBILITY` | rational function of integer must be integer | polynomial divide/substitute to divisor constraints | `RECURRENT_2Y_PLUS`; 2018 Q10/Q19, 2025 Q26 |
| `COPRIME_PERFECT_POWER_STRUCTURE` | product of coprime integers is square/power | force each coprime factor to be corresponding power | `RECURRENT_2Y` broader factor-pair family |
| `BALANCED_REPRESENTATION_COUNT` | signed powers / representation uniqueness | choose canonical representation before counting | `SINGLE_YEAR_CLEAN`; 2019 Q28; high-ceiling bridge |

---

# Geometry

Exact figure custody remains a separate publication requirement.

| Family | Trigger | First move | Status |
|---|---|---|---|
| `CIRCLE_TANGENT_ANGLE_CHAIN` | tangent/radius/chord/diameter | mark right angles and equal tangents before chasing | `HISTORICALLY_RECURRENT_5Y` at geometry super-family level |
| `TANGENT_PARALLEL_TRANSFER` | tangent plus parallel line | transfer angles, then circle theorem/similarity | `RECURRENT_2Y` |
| `CIRCLE_SEMICIRCLE_METRIC` | tangent + circle + square/rectangle lengths | identify right triangle/similarity/power relation | `RECURRENT_3Y_PLUS` |
| `CIRCLE_TANGENCY_SCALE` | successive/multiple tangent circles | center-distance or homothety scale | `RECURRENT_2Y` broader family |
| `POLYGON_ANGLE_CHAIN` | linked polygon angles/bisectors | one variable + angle sum | `RECURRENT_2Y` broader short-chain family |
| `TRIANGLE_MEDIAN_METRIC` | median and side lengths | Apollonius/median relation before angle chase | `SINGLE_YEAR_CLEAN_OR_SOURCE_GATED`; syllabus bridge |
| `ALTITUDE_SQUARE_DIFFERENCE` | altitude splits base, side-square target | subtract Pythagorean relations to cancel altitude | `SINGLE_YEAR_CLEAN`; 2018 Q23 |

Apollonius, Stewart, alternate segment and intersecting-chord theorem remain `SYLLABUS_REQUIRED` even where exact recurrence is sparse.

---

# Combinatorics

| Family | Trigger | First move | Status |
|---|---|---|---|
| `DIGIT_CONSTRAINT_COUNT` | digit restrictions + parity/divisibility | define positions, restrictions, then multiply/case split | `RECURRENT_2Y_PLUS` |
| `SUBSET_PRODUCT_EXPANSION` | sum over products of subsets | convert to `∏(1+a_i)` | `SINGLE_YEAR_CLEAN`; 2019 Q07 |
| `GRID_PATH_STATE_COUNT` | exact-move path | define states/recurrence before enumeration | `SINGLE_YEAR_CLEAN`; 2019 Q23; figure-gated |
| `COEFFICIENT_AS_COUNT` | coefficient of product of sums | translate exponent target to integer-pair count | `SINGLE_YEAR_CLEAN`; 2019 Q30 |
| `GEOMETRIC_CONFIGURATION_COUNT` | count shapes/vertex configurations | classify disjoint geometric cases | `SINGLE_YEAR_CLEAN`; 2019 high-ceiling evidence |

Fundamental counting, P&C, pigeonhole and inclusion-exclusion are `SYLLABUS_REQUIRED` regardless of sparse recurrence.

---

# Arithmetic / cumulative foundation

| Family | Trigger | First move | Status |
|---|---|---|---|
| `PAIRWISE_RATE_RECONSTRUCTION` | pairwise worker rates | add equations to recover total rate | `RECURRENT_2Y` broader rate family |
| `PERCENT_COMPLEMENT_TOTAL` | categories + remaining count | compute complement percentage first | `RECURRENT_2Y` broader percent family |
| `PERCENTAGE_INVARIANT_MASS` | concentration/water percentage change | track conserved dry/solute mass | `SINGLE_YEAR_CLEAN`; 2025 Q29 |
| `CLOCK_RELATIVE_ANGULAR_SPEED` | clock-hand angle/time | include both hand angular speeds | `SINGLE_YEAR_CLEAN`; 2024 Q02 |

---

# Mandatory low-recurrence syllabus nodes

The following remain `SYLLABUS_REQUIRED` and must not be omitted or mislabeled as unimportant:

- Mathematical Induction;
- Greatest Integer / Least Integer functions;
- explicit Stewart / Apollonius coverage;
- pigeonhole and inclusion-exclusion.

For these nodes, use syllabus-first author-created foundation/transfer material until a clean qualified PYQ anchor is available.

---

# Authoring contract

Every stable recurring archetype must eventually have:

1. Concept Book home;
2. First-Step recognition card;
3. `F0 -> F4` ladder;
4. clean PYQ anchor where available;
5. non-identical transfer;
6. recognition-only timed drill;
7. wrong-method contrast;
8. source/provenance record.

Do not use recurrence status to replace source custody or syllabus obligation.
