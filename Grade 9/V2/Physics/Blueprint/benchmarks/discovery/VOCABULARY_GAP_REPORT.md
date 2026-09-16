# Physics Engineering Discovery Quality Benchmark Report

## Executive Summary
- **Total Benchmark Queries**: 167
- **Target-Seeking Queries**: 163
- **Out-of-Domain Noise Queries**: 4
- **Top-1 Recall**: 100.0% (163/163)
- **Top-3 Recall**: 100.0% (163/163)
- **Top-5 Recall**: 100.0% (163/163)
- **Miss Rate**: 0.0% (0/163)
- **Noise Candidate Rate**: 0.00%
- **Vocabulary Contribution Rate**: 100.0%
- **Out-of-Domain Clean Pass Rate**: 100.0%

## Invariant Validation
- **Non-Authoritative Invariant**: PASS. All queries produced candidate receipts with `technical_authorization: NOT_EVALUATED`.
- **Deterministic Ranking**: PASS. Re-running queries produces bit-identical score order and digests.
- **Explicit Selection Enforcement**: PASS. `requires_explicit_exact_selection: True` in 100% of receipts.

## Identified Vocabulary Gaps
Zero vocabulary gaps detected across all test queries! 100% Top-5 recall achieved.
