#!/usr/bin/env python3
"""Production visual-QA gate layered on the real p97-p99 Core1 acceptance.

It reuses the full real-source acceptance contract while swapping in the
post-visual-QA source fixture.  The extra assertions prevent regression to the
single-angle Q9 visual or the money-only same-rate visual.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.Acceptance.Validation import validate_real_p97_p99_core1 as base_gate
from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.production_fixture import build_primary_input
from Grade4.V2.Mathematics.LearningDesign.engine.authoring_handoff import build_authoring_handoff


def fail(message: str) -> None:
    raise SystemExit(f"Real p97-p99 production-visual acceptance failed: {message}")


def _plan_for_source(handoff, qref: str):
    modules = list((handoff["authoring_result"].get("core1_plan") or {}).get("modules") or [])
    matches = [module for module in modules if qref in set(map(str, module.get("source_refs") or []))]
    if len(matches) != 1:
        fail(f"{qref}: expected one Core1 module, found {len(matches)}")
    module_id = matches[0]["module_id"]
    rows = [
        row for row in handoff["module_support"]
        if row.get("product") == "CORE1" and row.get("module_id") == module_id
    ]
    if len(rows) != 1:
        fail(f"{qref}: expected one Core1 support row, found {len(rows)}")
    return rows[0]["learning_representation_plan"]


def validate_visual_fixes() -> None:
    handoff = build_authoring_handoff(build_primary_input())

    q9 = _plan_for_source(handoff, "P97-Q9")
    q9_primary = q9.get("primary_visual") or {}
    if q9_primary.get("primitive_kind") != "ANGLE_CLASSIFICATION_SET":
        fail(f"P97-Q9 regressed to {q9_primary.get('primitive_kind')}")
    if list((q9_primary.get("semantic_params") or {}).get("degrees") or []) != [45, 90, 120, 180, 240]:
        fail(f"P97-Q9 classification coverage incomplete: {q9_primary.get('semantic_params')}")

    hats = _plan_for_source(handoff, "P99-Q2")
    hats_primary = hats.get("primary_visual") or {}
    if hats_primary.get("primitive_kind") != "RATE_SCALE_MODEL":
        fail(f"P99-Q2 regressed to {hats_primary.get('primitive_kind')}")
    params = hats_primary.get("semantic_params") or {}
    expected = {
        "base_amount": 120,
        "target_amount": 240,
        "base_count": 3,
        "target_count": None,
        "scale_factor": 2,
    }
    if any(params.get(key) != value for key, value in expected.items()):
        fail(f"P99-Q2 linked scale model changed: {params}")
    if "6" not in set(map(str, (hats.get("solution_guard") or {}).get("solution_tokens") or [])):
        fail("P99-Q2 final answer token is not protected by solution guard")


def main() -> None:
    validate_visual_fixes()
    # Reuse every existing real-source assertion and the canonical candidate
    # output path, but build it from the production visual selections above.
    base_gate.build_primary_input = build_primary_input
    base_gate.main()


if __name__ == "__main__":
    main()
