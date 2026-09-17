#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_engineering_migration_preflight import (  # noqa: E402
    MigrationPreflightError,
    compile_report,
    validate_report,
)


def expect_code(fn, code: str) -> None:
    try:
        fn()
    except MigrationPreflightError as exc:
        assert exc.code == code, (exc.code, exc.message)
        return
    raise AssertionError(f"expected {code}")


report = compile_report()
assert report["source_snapshot"]["pr_number"] == 383
assert report["source_snapshot"]["head_sha"] == "e92481f6e03a8bb49a55f568b03cba7c12fb942a"
assert report["source_snapshot"]["source_gate_count"] == 43
assert report["counts"]["migration_gap_count"] == 24
assert report["counts"]["structural_minimums_satisfied_count"] == 0
assert report["counts"]["structural_minimums_blocked_count"] == 24
assert report["target_contract"]["minimums_derived_from_schema"] is True
assert report["target_contract"]["readiness_rule"] == "STRUCTURAL_PREFLIGHT_NEVER_GRANTS_ENGINEERING_READINESS"

entries = {row["discovery_gate_id"]: row for row in report["entries"]}
kin = entries["PHY-KIN-1D-MOTION"]
assert kin["source_counts"]["required_transformations"] == 1
assert kin["v3_minimums"]["required_transformations"] == 2
assert "required_transformations" in kin["unsatisfied_minimums"]
assert kin["structural_minimums_satisfied"] is False
assert "PHY-GRAV-UNIVERSAL-LAW" not in entries
assert "PHY-GRAV-FREE-FALL" not in entries
assert "PHY-FORCE-NEWTON-LAWS" not in entries
assert "PHY-KIN-2D-PROJECTILE" not in entries
assert "PHY-KIN-RELATIVE-2D" not in entries
assert "PHY-WORK-ENERGY-POWER" not in entries
assert "PHY-ENERGY-CONSERVATION-LAW" not in entries

for row in report["entries"]:
    failures = [field for field, minimum in row["v3_minimums"].items() if row["source_counts"][field] < minimum]
    assert row["unsatisfied_minimums"] == failures
    assert row["structural_minimums_satisfied"] is (not failures)
    assert row["promotion_authorized"] is False
    assert row["readiness_authorized"] is False

assert "Q15" not in json.dumps(report, sort_keys=True)

bad = copy.deepcopy(report)
bad["entries"][0]["promotion_authorized"] = True
expect_code(lambda: validate_report(bad), "E_ENG_PREFLIGHT_REPORT_SCHEMA")

bad = copy.deepcopy(report)
bad["entries"][0]["readiness_authorized"] = True
expect_code(lambda: validate_report(bad), "E_ENG_PREFLIGHT_REPORT_SCHEMA")

print("Physics PR383 -> v3 source structural preflight: PASS")
print(json.dumps(report["counts"], sort_keys=True))