"""
Candidate Export Generator for Primary Mathematics V2.
Aggregates Deep and Breadth golden realizations into candidate_export.json
for independent validation by BenchmarkAcceptance.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def generate_candidate_export(output_path: Path | None = None) -> Path:
    golden_dir = Path(__file__).resolve().parent.parent / "Golden"
    if output_path is None:
        output_path = Path(__file__).resolve().parent / "candidate_export.json"

    # 1. Load deep multiplication case
    with open(golden_dir / "deep_multiplication_23x6.json", "r", encoding="utf-8") as f:
        deep_mul = json.load(f)

    # 2. Load deep division cases
    with open(golden_dir / "deep_division_zero_cases.json", "r", encoding="utf-8") as f:
        deep_div_cases = json.load(f)

    # 3. Load breadth cases
    with open(golden_dir / "breadth_cases.json", "r", encoding="utf-8") as f:
        breadth_cases = json.load(f)

    all_cases: List[Dict[str, Any]] = [deep_mul] + deep_div_cases + breadth_cases

    candidate_export = {
        "candidate_id": "PRIMARY-MATH-V2-ENGINE-CANDIDATE-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine_version": "2.0.0-p0",
        "cases": all_cases
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(candidate_export, f, indent=2)

    return output_path


if __name__ == "__main__":
    out = generate_candidate_export()
    print(f"Generated candidate export with cases at: {out}")
