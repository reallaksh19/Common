#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_pr383_v3_migration_gaps import (  # noqa: E402
    BLOCKER_CODES,
    PR383MigrationGapError,
    compile_report,
    load,
    validate_report,
    verify_snapshot_identity,
)


def expect_code(fn, code: str) -> None:
    try:
        fn()
    except PR383MigrationGapError as exc:
        assert exc.code == code, (exc.code, exc.message)
        return
    raise AssertionError(f"expected {code}")


report = compile_report()

assert report["source_snapshot"]["pr_number"] == 383
assert report["source_snapshot"]["head_sha"] == "e92481f6e03a8bb49a55f568b03cba7c12fb942a"
assert report["source_snapshot"]["source_gate_count"] == 43
assert report["counts"]["discovered_subtopic_count"] == 43
assert report["counts"]["already_reconciled_count"] == 19
assert report["counts"]["migration_gap_count"] == 24
assert report["target_control_plane"]["canonical_v3_gate_count"] == 26
assert report["target_control_plane"]["readiness_rule"] == "DERIVED_BY_PRODUCTION_V3_VALIDATOR"
assert report["target_control_plane"]["source_self_asserted_readiness_imported"] is False
assert report["target_control_plane"]["case_specific_overrides"] == "PROHIBITED"

reconciled = {row["discovery_gate_id"]: row for row in report["already_reconciled"]}
assert reconciled["PHY-GRAV-UNIVERSAL-LAW"]["disposition"] == "MAPPED_V3"
assert reconciled["PHY-GRAV-UNIVERSAL-LAW"]["v3_gate_ids"] == ["PHY-GRAV-FORCE", "PHY-GRAV-FIELD"]
assert reconciled["PHY-GRAV-FREE-FALL"]["disposition"] == "MAPPED_V3"
assert reconciled["PHY-GRAV-FREE-FALL"]["v3_gate_ids"] == [
    "PHY-GRAV-FORCE",
    "PHY-GRAV-FIELD",
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-VELOCITY-EVOLUTION",
    "PHY-M2D-SAME-HEIGHT-VELOCITY",
]
assert reconciled["PHY-FORCE-NEWTON-LAWS"]["disposition"] == "MAPPED_V3"
assert reconciled["PHY-FORCE-NEWTON-LAWS"]["v3_gate_ids"] == [
    "PHY-NLM-INTERACTION",
    "PHY-NLM-FBD",
    "PHY-NLM-FIRST-LAW",
    "PHY-NLM-SECOND-LAW",
    "PHY-NLM-THIRD-LAW",
]
assert reconciled["PHY-KIN-2D-PROJECTILE"]["disposition"] == "MAPPED_V3"
assert reconciled["PHY-KIN-2D-PROJECTILE"]["v3_gate_ids"] == [
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-VELOCITY-EVOLUTION",
]
assert reconciled["PHY-KIN-RELATIVE-2D"]["disposition"] == "MAPPED_V3"
assert reconciled["PHY-KIN-RELATIVE-2D"]["v3_gate_ids"] == ["PHY-M2D-RELATIVE-VELOCITY"]
assert reconciled["PHY-WORK-ENERGY-POWER"]["disposition"] == "EXACT_V3_ID"
assert reconciled["PHY-WORK-ENERGY-POWER"]["v3_gate_ids"] == ["PHY-WORK-ENERGY-POWER"]
assert reconciled["PHY-ENERGY-CONSERVATION-LAW"]["disposition"] == "EXACT_V3_ID"
assert reconciled["PHY-ENERGY-CONSERVATION-LAW"]["v3_gate_ids"] == ["PHY-ENERGY-CONSERVATION-LAW"]
assert all(row["discovery_gate_id"] != "PHY-GRAV-UNIVERSAL-LAW" for row in report["migration_gaps"])
assert all(row["discovery_gate_id"] != "PHY-GRAV-FREE-FALL" for row in report["migration_gaps"])
assert all(row["discovery_gate_id"] != "PHY-FORCE-NEWTON-LAWS" for row in report["migration_gaps"])
assert all(row["discovery_gate_id"] != "PHY-KIN-2D-PROJECTILE" for row in report["migration_gaps"])
assert all(row["discovery_gate_id"] != "PHY-KIN-RELATIVE-2D" for row in report["migration_gaps"])
assert all(row["discovery_gate_id"] != "PHY-WORK-ENERGY-POWER" for row in report["migration_gaps"])
assert all(row["discovery_gate_id"] != "PHY-ENERGY-CONSERVATION-LAW" for row in report["migration_gaps"])

for gap in report["migration_gaps"]:
    assert gap["promotion_status"] == "BLOCKED_PENDING_V3_ENRICHMENT"
    assert gap["promotion_authorized"] is False
    assert gap["blocked_by"] == BLOCKER_CODES
    assert gap["discarded_source_control_fields"] == ["technical_readiness", "release_checklist"]
    assert "question_id" not in gap
    assert "item_id" not in gap
    assert "stress_test_ref" not in gap

assert "Q15" not in json.dumps(report, sort_keys=True)

manifest = load("provenance/pr383/source-snapshot.manifest.json")

bad = copy.deepcopy(manifest)
bad["source"]["registry_git_blob_sha"] = "0" * 40
expect_code(lambda: verify_snapshot_identity(bad), "E_PR383_SNAPSHOT_REGISTRY_BLOB_DRIFT")

bad = copy.deepcopy(manifest)
bad["source"]["schema_git_blob_sha"] = "0" * 40
expect_code(lambda: verify_snapshot_identity(bad), "E_PR383_SNAPSHOT_SCHEMA_BLOB_DRIFT")

bad_report = copy.deepcopy(report)
bad_report["migration_gaps"][0]["promotion_authorized"] = True
expect_code(lambda: validate_report(bad_report), "E_PR383_MIGRATION_REPORT_SCHEMA")

bad_report = copy.deepcopy(report)
bad_report["target_control_plane"]["source_self_asserted_readiness_imported"] = True
expect_code(lambda: validate_report(bad_report), "E_PR383_MIGRATION_REPORT_SCHEMA")

print("PR383 -> canonical v3 migration-gap compiler: PASS")
print(json.dumps(report["counts"], sort_keys=True))