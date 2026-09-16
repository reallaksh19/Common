# Engineering Discovery Vocabulary Gap Report

**Benchmark ID**: `MATH-ENG-DISC-BENCH-RUN-V1`  
**Authority**: `TEST_BENCHMARK_RESULTS_ONLY` (Non-authoritative)  

## 1. Quantitative Benchmark Metrics

| Metric | Observed Value | Description |
|---|---|---|
| **Top-1 Recall** | 69.3% | Percentage of queries where acceptable gate is rank 1 |
| **Top-3 Recall** | 93.5% | Percentage of queries where acceptable gate is in top 3 |
| **Top-5 Recall** | 96.8% | Percentage of queries where acceptable gate is in top 5 |
| **Miss Rate** | 3.2% | Percentage of queries with zero acceptable candidates |
| **Noise Rate** | 3.6% | Ratio of explicitly unacceptable candidate occurrences |
| **Ambiguity Preservation** | 78.3% | Proportion of valid candidates preserved for ambiguous queries |
| **No-Valid-Target Safety** | PASS | Strict refusal to auto-authorize out-of-domain queries |
| **Vocabulary Contribution** | 30.6% | Queries where vocabulary terms boosted match score |
| **Determinism** | PASS | Exact reproducible candidate order and scores |

## 2. Identified Vocabulary Gaps & Recommendations

The following queries returned suboptimal ranks or misses due to vocabulary coverage gaps:

| Query ID | Query Text | Category | Expected Target | Observed Top 3 | Failure Type | Recommended Action |
|---|---|---|---|---|---|---|
| `Q12` | nature of roots real and equal | `SCHOOL_TERMINOLOGY` | `MATH-QUAD-EQUATIONS` | `MATH-NUM-RADICALS, MATH-QUAD-EQUATIONS, MATH-ALG-COMPLEX-NUMBERS` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q16` | Theory of Equations | `COMPETITION_TERMINOLOGY` | `MATH-ALG-POLYNOMIALS, MATH-QUAD-EQUATIONS` | `MATH-LIN-EQUATIONS, MATH-QUAD-EQUATIONS, MATH-TRIG-EQUATIONS` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q18` | Newton sums for symmetric power sums of roots | `COMPETITION_TERMINOLOGY` | `MATH-ALG-POLYNOMIALS, MATH-QUAD-EQUATIONS` | `MATH-SEQ-GP-SPECIAL, MATH-ALG-POLY-ZEROS-GRAPH, MATH-QUAD-EQUATIONS` | `SUBOPTIMAL_RANK_3` | Consider adding alias/synonym to target in vocabulary policy |
| `Q19` | Common roots condition between two quadratic equations | `COMPETITION_TERMINOLOGY` | `MATH-QUAD-EQUATIONS` | `MATH-LIN-EQUATIONS, MATH-QUAD-EQUATIONS, MATH-TRIG-EQUATIONS` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q20` | Transformation of equations roots reciprocated | `COMPETITION_TERMINOLOGY` | `MATH-ALG-POLYNOMIALS, MATH-QUAD-EQUATIONS` | `MATH-LIN-EQUATIONS, MATH-QUAD-EQUATIONS, MATH-TRIG-EQUATIONS` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q24` | hcf and lcm by prime factorisation | `REGIONAL_TERMS` | `MATH-NUM-EUCLID-DIVISION` | `MATH-ALG-POLYNOMIALS, MATH-NUM-EUCLID-DIVISION, MATH-NUM-IRRATIONAL-PROOF` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q26` | QE | `ABBREVIATIONS` | `MATH-QUAD-EQUATIONS` | `None` | `COMPLETE_MISS` | Review tokenization and gate learner title |
| `Q28` | BPT Basic Proportionality Theorem | `ABBREVIATIONS` | `MATH-GEO-TRIANGLES` | `MATH-ALG-BINOMIAL-THEOREM, MATH-ALG-POLYNOMIALS, MATH-GEO-EUCLID-FOUNDATIONS` | `COMPLETE_MISS` | Review tokenization and gate learner title |
| `Q30` | pythagorean trig identities | `ABBREVIATIONS` | `MATH-TRIG-RATIOS` | `MATH-ALG-POLYNOMIALS, MATH-TRIG-RATIOS, MATH-TRIG-COMPOUND-ANGLES` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q32` | alpha plus beta minus b over a | `NOTATION_NAMES` | `MATH-QUAD-EQUATIONS` | `MATH-NUM-RADICALS, MATH-ALG-POLY-ZEROS-GRAPH, MATH-QUAD-EQUATIONS` | `SUBOPTIMAL_RANK_3` | Consider adding alias/synonym to target in vocabulary policy |
| `Q34` | sin squared theta plus cos squared theta | `NOTATION_NAMES` | `MATH-TRIG-RATIOS` | `MATH-ALG-COMPLEX-NUMBERS, MATH-TRIG-EQUATIONS, MATH-TRIG-EXTENDED-DOMAIN` | `SUBOPTIMAL_RANK_4` | Consider adding alias/synonym to target in vocabulary policy |
| `Q45` | Theorey of Equations | `MINOR_MISSPELLINGS` | `MATH-ALG-POLYNOMIALS, MATH-QUAD-EQUATIONS` | `MATH-LIN-EQUATIONS, MATH-QUAD-EQUATIONS, MATH-TRIG-EQUATIONS` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q49` | theory-of-equations | `SPACING_HYPHENATION` | `MATH-ALG-POLYNOMIALS, MATH-QUAD-EQUATIONS` | `MATH-LIN-EQUATIONS, MATH-QUAD-EQUATIONS, MATH-TRIG-EQUATIONS` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q53` | Finding roots when equation has degree two | `CONCEPTUAL_PARAPHRASES` | `MATH-QUAD-EQUATIONS` | `MATH-LIN-EQUATIONS, MATH-QUAD-EQUATIONS, MATH-LINES-2D` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q54` | Splitting middle term to find factors | `CONCEPTUAL_PARAPHRASES` | `MATH-ALG-POLYNOMIALS, MATH-QUAD-EQUATIONS` | `MATH-SEQ-AP, MATH-ALG-POLYNOMIALS, MATH-ALG-BINOMIAL-THEOREM` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q55` | Check if two lines intersect coincide or parallel | `CONCEPTUAL_PARAPHRASES` | `MATH-LIN-EQUATIONS` | `MATH-GEO-LINES-ANGLES, MATH-LINES-2D, MATH-LIN-EQUATIONS` | `SUBOPTIMAL_RANK_3` | Consider adding alias/synonym to target in vocabulary policy |
| `Q56` | Roots | `AMBIGUOUS_PHRASES` | `MATH-ALG-POLY-ZEROS-GRAPH, MATH-NUM-RADICALS, MATH-QUAD-EQUATIONS` | `MATH-ALG-COMPLEX-NUMBERS, MATH-ALG-POLY-ZEROS-GRAPH, MATH-ALG-POLYNOMIALS` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q64` | Radical square roots in quadratic formula | `ADVERSARIAL_NEAR_MISS` | `MATH-NUM-RADICALS, MATH-QUAD-EQUATIONS` | `MATH-ALG-POLYNOMIALS, MATH-QUAD-EQUATIONS, MATH-GEO-COORDINATES` | `SUBOPTIMAL_RANK_2` | Consider adding alias/synonym to target in vocabulary policy |
| `Q65` | Circle theorem inscribed angle in a triangle | `ADVERSARIAL_NEAR_MISS` | `MATH-GEO-CIRCLES, MATH-GEO-TRIANGLES` | `MATH-ALG-BINOMIAL-THEOREM, MATH-CONIC-CIRCLE, MATH-GEO-LINES-ANGLES` | `SUBOPTIMAL_RANK_5` | Consider adding alias/synonym to target in vocabulary policy |

## 3. Critical Authority Invariant Reminder

> **A high benchmark recall score never bypasses explicit exact selection.**  
> Even a 100% Top-1 match result produces candidate discovery receipts marked `technical_authorization = NOT_EVALUATED` and `automatic_selection = False`. Downstream Engineering authorization requires explicit selection of the exact ID and closure validation.
