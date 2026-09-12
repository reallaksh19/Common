#!/usr/bin/env python3
"""Instructional-completeness gate for the p97-99 Grade 4 study journey."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.StudyDesign.engine.study_journey import validate_study_journey
from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.study_journey_fixture import (
    ALL_REFS,
    build_study_journey,
)


def main() -> None:
    plan = build_study_journey()
    result = validate_study_journey(plan)

    if result["source_coverage_count"] != len(ALL_REFS):
        raise SystemExit(f"coverage mismatch: {result}")
    if result["worked_example_count"] < 5:
        raise SystemExit(f"teach-first journey has too few worked examples: {result}")
    if result["independent_block_count"] < 7:
        raise SystemExit(f"journey has too little independent/transfer evidence: {result}")

    block_types = {
        block["block_type"]
        for module in plan["modules"]
        for block in module["blocks"]
    }
    required_types = {
        "SEE_DISCOVER", "CONNECT", "WORKED_EXAMPLE", "GUIDED_TRY",
        "INDEPENDENT_TRY", "ERROR_ANALYSIS", "RETRIEVAL", "SELF_CHECK",
    }
    missing = required_types - block_types
    if missing:
        raise SystemExit(f"study journey missing pedagogical block types: {sorted(missing)}")

    # The procedural module must teach before the 7048/24 independent task.
    division = next(m for m in plan["modules"] if m["module_id"] == "M3-WRITTEN-DIVISION")
    types = [b["block_type"] for b in division["blocks"]]
    if types.index("WORKED_EXAMPLE") > types.index("INDEPENDENT_TRY"):
        raise SystemExit("written division publishes independent work before a worked example")

    # Source defects/ambiguities that drove the original acceptance work remain represented.
    covered = {ref for module in plan["modules"] for ref in module["source_refs"]}
    for qref in ("P97-Q4", "P97-Q6", "P97-Q9"):
        if qref not in covered:
            raise SystemExit(f"source caveat lost from study journey: {qref}")

    print({"status": "PASS", **result})


if __name__ == "__main__":
    main()
