#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "architecture_observer"))

from generate_observation_manifest import build_observation  # noqa: E402


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_integration_policy_is_non_authoritative():
    policy = load("policy/physics-pr402-integration.v1.json")
    assert policy["source_pr"] == 402
    assert policy["source_head"] == "efd5d47df8daa3de5996d8419652dd76cb08dc89"
    assert policy["canonical_pr"] == 350
    assert policy["authority"] == "NON_AUTHORITATIVE_RECONCILIATION"
    assert policy["rules"]["source_branch_may_define_runtime_authority"] is False
    assert policy["rules"]["aggregate_v1_registry_may_replace_v3"] is False
    assert policy["rules"]["observability_may_grant_readiness"] is False
    assert policy["rules"]["sil_content_may_bypass_learning_engineering_promotion"] is False
    assert policy["rules"]["all_regression_and_stress_execution_owned_by_blueprint"] is True


def test_observation_binds_current_v3_and_discovery_without_authorizing():
    observation = build_observation()
    assert observation["authority"] == "DERIVED_OBSERVABILITY_ONLY"
    assert observation["engineering_authorization"] == "NOT_EVALUATED"
    assert observation["publication_authorization"] == "NOT_IMPLIED"
    assert observation["canonical_v3"]["registry_id"] == "PHYSICS-TECHNICAL-ENGINEERING-GATES-V3"
    assert observation["canonical_v3"]["gate_count"] == 26
    assert observation["discovery_coverage"]["discovered_subtopic_count"] == 43
    assert observation["discovery_coverage"]["migration_required_count"] == 24
    assert observation["invariants"]["parallel_engineering_authority_prohibited"] is True


def test_grade9_work_energy_is_current_v3_but_grade11_variable_force_remains_held():
    observation = build_observation()
    rows = {row["discovery_gate_id"]: row for row in observation["work_energy_reconciliation"]}
    expected = {
        "PHY-WORK-ENERGY-POWER",
        "PHY-ENERGY-CONSERVATION-LAW",
        "PHY-WEP-VARIABLE-FORCE",
    }
    assert set(rows) == expected
    assert rows["PHY-WORK-ENERGY-POWER"]["disposition"] == "EXACT_V3_ID"
    assert rows["PHY-WORK-ENERGY-POWER"]["v3_gate_ids"] == ["PHY-WORK-ENERGY-POWER"]
    assert rows["PHY-ENERGY-CONSERVATION-LAW"]["disposition"] == "EXACT_V3_ID"
    assert rows["PHY-ENERGY-CONSERVATION-LAW"]["v3_gate_ids"] == ["PHY-ENERGY-CONSERVATION-LAW"]
    assert rows["PHY-WEP-VARIABLE-FORCE"]["disposition"] == "MIGRATION_REQUIRED"
    assert rows["PHY-WEP-VARIABLE-FORCE"]["v3_gate_ids"] == []
    assert rows["PHY-WORK-ENERGY-POWER"]["curriculum_grade"] == 9
    assert rows["PHY-ENERGY-CONSERVATION-LAW"]["curriculum_grade"] == 9
    assert rows["PHY-WEP-VARIABLE-FORCE"]["curriculum_grade"] == 11


def test_observer_does_not_depend_on_parallel_v1_registry():
    text = (ROOT / "tools" / "architecture_observer" / "generate_observation_manifest.py").read_text(encoding="utf-8")
    assert "physics-technical-engineering-gates.v1.json" not in text
    assert "compile_physics_engineering_workbench.py" not in text
    assert "build_physics_engineering_gate_registry_v3" in text
    assert "physics-engineering-discovery-catalog.pr383.v1.json" in text


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"PR402 observability integration: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
