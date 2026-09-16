# Chemistry Engineering Discovery Quality Benchmark Report

## Executive Summary
- **Total Benchmark Queries**: 114
- **Target-Seeking Queries**: 104
- **Out-of-Domain Noise Queries**: 10
- **Top-1 Recall**: 100.0% (104/104)
- **Top-3 Recall**: 100.0% (104/104)
- **Top-5 Recall**: 100.0% (104/104)
- **Miss Rate**: 0.0% (0/104)
- **Noise Candidate Rate**: 7.28%
- **Vocabulary Contribution Rate**: 100.0%
- **Out-of-Domain Clean Pass Rate**: 100.0%

## Invariant Validation
- **Non-Authoritative Invariant**: PASS. All queries produced candidate receipts with `technical_authorization: NOT_EVALUATED`.
- **Deterministic Ranking**: PASS. Re-running queries produces bit-identical score order and digests.
- **Explicit Selection Enforcement**: PASS. `requires_explicit_exact_selection: True` in 100% of receipts.

## Identified Vocabulary Gaps
Zero vocabulary gaps detected across all test queries! 100% Top-1 recall achieved.
