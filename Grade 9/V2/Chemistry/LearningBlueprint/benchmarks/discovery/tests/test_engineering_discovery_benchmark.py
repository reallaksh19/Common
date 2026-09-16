#!/usr/bin/env python3
"""
Unit Tests for Chemistry Engineering Discovery Benchmark
========================================================
Validates benchmark runner metrics, deterministic ranking, and non-authoritative invariants.
"""

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from benchmark_runner import (  # noqa: E402
    DEFAULT_CORPUS_REL,
    load_json,
    run_benchmark,
)


class ChemistryDiscoveryBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = load_json(ROOT / DEFAULT_CORPUS_REL)
        cls.summary = run_benchmark(cls.corpus)

    def test_benchmark_covers_at_least_100_queries(self) -> None:
        self.assertGreaterEqual(self.summary["total_queries"], 100)

    def test_benchmark_achieves_high_top1_recall(self) -> None:
        top_1 = self.summary["metrics"]["top_1_recall"]
        self.assertGreaterEqual(top_1, 0.95, f"Expected top_1_recall >= 0.95, got {top_1}")

    def test_benchmark_achieves_perfect_top5_recall(self) -> None:
        top_5 = self.summary["metrics"]["top_5_recall"]
        self.assertEqual(top_5, 1.0, f"Expected 100% top_5_recall, got {top_5}")

    def test_zero_miss_rate(self) -> None:
        miss_rate = self.summary["metrics"]["miss_rate"]
        self.assertEqual(miss_rate, 0.0, f"Expected zero misses, got {miss_rate}")

    def test_vocabulary_contribution_rate(self) -> None:
        vcr = self.summary["metrics"]["vocabulary_contribution_rate"]
        self.assertGreaterEqual(vcr, 0.90, f"Expected vocabulary contribution >= 0.90, got {vcr}")

    def test_clean_pass_for_out_of_domain_queries(self) -> None:
        clean_pass = self.summary["no_target_clean_pass_rate"]
        self.assertGreaterEqual(clean_pass, 0.90, f"Expected out of domain clean pass >= 0.90, got {clean_pass}")


if __name__ == "__main__":
    unittest.main()
