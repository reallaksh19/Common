# Engineering Discovery Vocabulary Gap Report

**Benchmark ID**: `MATH-ENG-DISC-BENCH-RUN-V1`  
**Authority**: `TEST_BENCHMARK_RESULTS_ONLY` (Non-authoritative)  

## 1. Quantitative Benchmark Metrics

| Metric | Observed Value | Description |
|---|---|---|
| **Top-1 Recall** | 100.0% | Percentage of queries where acceptable gate is rank 1 |
| **Top-3 Recall** | 100.0% | Percentage of queries where acceptable gate is in top 3 |
| **Top-5 Recall** | 100.0% | Percentage of queries where acceptable gate is in top 5 |
| **Miss Rate** | 0.0% | Percentage of queries with zero acceptable candidates |
| **Noise Rate** | 5.4% | Ratio of explicitly unacceptable candidate occurrences |
| **Ambiguity Preservation** | 95.0% | Proportion of valid candidates preserved for ambiguous queries |
| **No-Valid-Target Safety** | PASS | Strict refusal to auto-authorize out-of-domain queries |
| **Vocabulary Contribution** | 98.7% | Queries where vocabulary terms boosted match score |
| **Determinism** | PASS | Exact reproducible candidate order and scores |

## 2. Identified Vocabulary Gaps & Recommendations

The following queries returned suboptimal ranks or misses due to vocabulary coverage gaps:

| Query ID | Query Text | Category | Expected Target | Observed Top 3 | Failure Type | Recommended Action |
|---|---|---|---|---|---|---|

## 3. Critical Authority Invariant Reminder

> **A high benchmark recall score never bypasses explicit exact selection.**  
> Even a 100% Top-1 match result produces candidate discovery receipts marked `technical_authorization = NOT_EVALUATED` and `automatic_selection = False`. Downstream Engineering authorization requires explicit selection of the exact ID and closure validation.
