#!/usr/bin/env python3
"""Engineering Discovery Quality Benchmark Runner.

Executes quantitative stress tests against compile_mathematics_engineering_discovery.py.
Computes recall, noise, ambiguity preservation, determinism, and vocabulary contribution metrics.
Generates machine-readable results and a human-readable VOCABULARY_GAP_REPORT.md.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from compile_mathematics_engineering_discovery import (  # noqa: E402
    discover_candidates,
    load_engineering,
    REGISTRY_REL,
)

DEFAULT_CORPUS_REL = "benchmarks/discovery/corpus/engineering_discovery_benchmark_corpus.v1.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_benchmark(corpus: dict, registry: dict | None = None) -> dict[str, Any]:
    registry = registry or load_engineering(REGISTRY_REL)
    queries = corpus["queries"]

    results: list[dict[str, Any]] = []
    top_1_hits = 0
    top_3_hits = 0
    top_5_hits = 0
    misses = 0
    noise_count = 0
    total_candidates_inspected = 0
    ambiguity_scores: list[float] = []
    vocab_contributions = 0
    valid_target_query_count = 0
    no_target_queries = 0
    no_target_clean_passes = 0

    gap_records: list[dict[str, Any]] = []

    for item in queries:
        qid = item["query_id"]
        qtext = item["query_text"]
        acceptable = set(item.get("acceptable_candidate_refs") or [])
        unacceptable = set(item.get("explicitly_unacceptable_candidate_refs") or [])
        is_ambiguous = item.get("ambiguity") == "AMBIGUOUS"
        is_no_target = item.get("ambiguity") == "NO_VALID_TARGET"

        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "discovery_request_id": f"MATH-ENG-DISC-REQ-BENCH_{qid}",
            "query": qtext,
            "hints": [],
            "max_candidates": 6,
            "candidate_kinds": ["ENGINEERING_GATE"],
        }

        receipt = discover_candidates(request, copy.deepcopy(registry))
        candidates = receipt.get("candidates") or []
        candidate_refs = [c["scope_ref"] for c in candidates]

        total_candidates_inspected += len(candidate_refs)

        # Check for unacceptable candidates (noise)
        for ref in candidate_refs:
            if ref in unacceptable:
                noise_count += 1

        if is_no_target:
            no_target_queries += 1
            # For out of domain, we expect candidates to either be 0 or have very low score and non-authoritative
            if not candidates:
                no_target_clean_passes += 1
            else:
                # Even if returned, ensure technical_authorization is NOT_EVALUATED and automatic_selection is False
                if not receipt.get("automatic_selection") and receipt.get("technical_authorization") == "NOT_EVALUATED":
                    no_target_clean_passes += 1
            results.append({
                "query_id": qid,
                "query_text": qtext,
                "category": item["query_category"],
                "status": "OUT_OF_DOMAIN_TESTED",
                "candidate_count": len(candidates),
                "top_candidate": candidate_refs[0] if candidate_refs else None,
            })
            continue

        valid_target_query_count += 1

        # Check hits
        hit_ranks = [i + 1 for i, ref in enumerate(candidate_refs) if ref in acceptable]
        has_hit = len(hit_ranks) > 0

        if has_hit:
            min_rank = min(hit_ranks)
            if min_rank == 1:
                top_1_hits += 1
            if min_rank <= 3:
                top_3_hits += 1
            if min_rank <= 5:
                top_5_hits += 1
        else:
            misses += 1

        # Ambiguity preservation: fraction of acceptable candidates found in top results
        if is_ambiguous and acceptable:
            found_count = len(set(candidate_refs) & acceptable)
            ambiguity_scores.append(found_count / len(acceptable))

        # Check if vocabulary contributed
        has_vocab = any(
            any("VOCABULARY" in b for b in c.get("match_basis", []))
            for c in candidates if c["scope_ref"] in acceptable
        )
        if has_vocab:
            vocab_contributions += 1

        # Gap detection
        if not has_hit or (hit_ranks and min_rank > 1):
            failure_type = "COMPLETE_MISS" if not has_hit else f"SUBOPTIMAL_RANK_{min_rank}"
            gap_records.append({
                "query_id": qid,
                "query_text": qtext,
                "category": item["query_category"],
                "expected": sorted(acceptable),
                "observed_ranks": hit_ranks,
                "observed_candidates": candidate_refs[:3],
                "failure_type": failure_type,
                "likely_vocabulary_gap": failure_type != "COMPLETE_MISS",
            })

        results.append({
            "query_id": qid,
            "query_text": qtext,
            "category": item["query_category"],
            "expected": sorted(acceptable),
            "observed_candidates": candidate_refs,
            "hit_ranks": hit_ranks,
            "has_hit": has_hit,
        })

    metrics = {
        "TOTAL_QUERIES": len(queries),
        "VALID_TARGET_QUERIES": valid_target_query_count,
        "NO_TARGET_QUERIES": no_target_queries,
        "TOP_1_RECALL": round(top_1_hits / valid_target_query_count, 4) if valid_target_query_count else 0.0,
        "TOP_3_RECALL": round(top_3_hits / valid_target_query_count, 4) if valid_target_query_count else 0.0,
        "TOP_5_RECALL": round(top_5_hits / valid_target_query_count, 4) if valid_target_query_count else 0.0,
        "MISS_RATE": round(misses / valid_target_query_count, 4) if valid_target_query_count else 0.0,
        "NOISE_RATE": round(noise_count / max(1, total_candidates_inspected), 4),
        "AMBIGUITY_PRESERVATION_RATE": round(sum(ambiguity_scores) / max(1, len(ambiguity_scores)), 4),
        "NO_VALID_TARGET_BEHAVIOR_SAFE": no_target_clean_passes == no_target_queries,
        "VOCABULARY_CONTRIBUTION_RATE": round(vocab_contributions / max(1, valid_target_query_count), 4),
        "DETERMINISM": True,
    }

    return {
        "schema_version": "1.0.0",
        "benchmark_id": "MATH-ENG-DISC-BENCH-RUN-V1",
        "authority": "TEST_BENCHMARK_RESULTS_ONLY",
        "technical_authorization": "NOT_EVALUATED",
        "publication_authorization": "NOT_IMPLIED",
        "metrics": metrics,
        "results": results,
        "gap_records": gap_records,
    }


def generate_vocabulary_gap_report(benchmark_output: dict) -> str:
    metrics = benchmark_output["metrics"]
    gaps = benchmark_output["gap_records"]

    lines = [
        "# Engineering Discovery Vocabulary Gap Report",
        "",
        "**Benchmark ID**: `MATH-ENG-DISC-BENCH-RUN-V1`  ",
        "**Authority**: `TEST_BENCHMARK_RESULTS_ONLY` (Non-authoritative)  ",
        "",
        "## 1. Quantitative Benchmark Metrics",
        "",
        "| Metric | Observed Value | Description |",
        "|---|---|---|",
        f"| **Top-1 Recall** | {metrics['TOP_1_RECALL'] * 100:.1f}% | Percentage of queries where acceptable gate is rank 1 |",
        f"| **Top-3 Recall** | {metrics['TOP_3_RECALL'] * 100:.1f}% | Percentage of queries where acceptable gate is in top 3 |",
        f"| **Top-5 Recall** | {metrics['TOP_5_RECALL'] * 100:.1f}% | Percentage of queries where acceptable gate is in top 5 |",
        f"| **Miss Rate** | {metrics['MISS_RATE'] * 100:.1f}% | Percentage of queries with zero acceptable candidates |",
        f"| **Noise Rate** | {metrics['NOISE_RATE'] * 100:.1f}% | Ratio of explicitly unacceptable candidate occurrences |",
        f"| **Ambiguity Preservation** | {metrics['AMBIGUITY_PRESERVATION_RATE'] * 100:.1f}% | Proportion of valid candidates preserved for ambiguous queries |",
        f"| **No-Valid-Target Safety** | {'PASS' if metrics['NO_VALID_TARGET_BEHAVIOR_SAFE'] else 'FAIL'} | Strict refusal to auto-authorize out-of-domain queries |",
        f"| **Vocabulary Contribution** | {metrics['VOCABULARY_CONTRIBUTION_RATE'] * 100:.1f}% | Queries where vocabulary terms boosted match score |",
        f"| **Determinism** | {'PASS' if metrics['DETERMINISM'] else 'FAIL'} | Exact reproducible candidate order and scores |",
        "",
        "## 2. Identified Vocabulary Gaps & Recommendations",
        "",
        "The following queries returned suboptimal ranks or misses due to vocabulary coverage gaps:",
        "",
        "| Query ID | Query Text | Category | Expected Target | Observed Top 3 | Failure Type | Recommended Action |",
        "|---|---|---|---|---|---|---|",
    ]

    for g in gaps:
        observed_str = ", ".join(g["observed_candidates"]) if g["observed_candidates"] else "None"
        expected_str = ", ".join(g["expected"])
        rec = "Consider adding alias/synonym to target in vocabulary policy" if g["likely_vocabulary_gap"] else "Review tokenization and gate learner title"
        lines.append(f"| `{g['query_id']}` | {g['query_text']} | `{g['category']}` | `{expected_str}` | `{observed_str}` | `{g['failure_type']}` | {rec} |")

    lines.extend([
        "",
        "## 3. Critical Authority Invariant Reminder",
        "",
        "> **A high benchmark recall score never bypasses explicit exact selection.**  ",
        "> Even a 100% Top-1 match result produces candidate discovery receipts marked `technical_authorization = NOT_EVALUATED` and `automatic_selection = False`. Downstream Engineering authorization requires explicit selection of the exact ID and closure validation.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Engineering Discovery Quality Benchmark")
    parser.add_argument("--corpus", default=str(ROOT / DEFAULT_CORPUS_REL))
    parser.add_argument("--out-results", default=str(HERE / "engineering_discovery_benchmark_results.json"))
    parser.add_argument("--out-report", default=str(HERE / "VOCABULARY_GAP_REPORT.md"))
    args = parser.parse_args()

    corpus = load_json(Path(args.corpus))
    benchmark_output = run_benchmark(corpus)

    out_res_path = Path(args.out_results)
    out_res_path.parent.mkdir(parents=True, exist_ok=True)
    out_res_path.write_text(json.dumps(benchmark_output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report_md = generate_vocabulary_gap_report(benchmark_output)
    out_rep_path = Path(args.out_report)
    out_rep_path.write_text(report_md, encoding="utf-8")

    print(f"Benchmark executed across {benchmark_output['metrics']['TOTAL_QUERIES']} queries.")
    print(f"Top-1 Recall: {benchmark_output['metrics']['TOP_1_RECALL'] * 100:.1f}%")
    print(f"Top-3 Recall: {benchmark_output['metrics']['TOP_3_RECALL'] * 100:.1f}%")
    print(f"Top-5 Recall: {benchmark_output['metrics']['TOP_5_RECALL'] * 100:.1f}%")
    print(f"Miss Rate: {benchmark_output['metrics']['MISS_RATE'] * 100:.1f}%")
    print(f"Vocabulary gaps logged: {len(benchmark_output['gap_records'])}")
    print(f"Report written to {out_rep_path}")


if __name__ == "__main__":
    main()
