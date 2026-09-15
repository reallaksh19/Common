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
assert report["counts"]["already_reconciled_count"] == 12
assert report["counts"]["migration_gap_count"] == 31
assert report["target_control_plane"]["canonical_v3_gate_count"] == 23
assert report["target_control_plane"]["readiness_rule"] == "DERIVED_BY_PRODUCTION_V3_VALIDATOR"
assert report["target_control_plane"]["source_self_asserted_readiness_imported"] is False
assert report["target_control_plane"]["case_specific_overrides"] == "PROHIBITED"

for gap in report["migration_gaps"]:
    assert gap["promotion_status"] == "BLOCKED_PENDING_V3_ENRICHMENT"
    assert gap["promotion_authorized"] is False
    assert gap["blocked_by"] == BLOCKER_CODES
    assert gap["discarded_source_control_fields"] == ["technical_readiness", "release_checklist"]
    assert "question_id" not in gap
    assert "item_id" not in gap
    assert "stress_test_ref" not in gap

# Q15 is permitted to stress-test downstream behavior, but it is not an input
# to the subject-wide migration compiler or its engineering logic.
assert "Q15" not in json.dumps(report, sort_keys=True)

manifest = load("provenance/pr383/source-snapshot.manifest.json")

bad = copy.deepcopy(manifest)
bad["source"]["registry_git_blob_sha"] = "0" * 40
expect_code(lambda: verify_snapshot_identity(bad), "E_PR383_SNAPSHOT_REGISTRY_BLOB_DRIFT")

bad = copy.deepcopy(manifest)
bad["source"]["schema_git_blob_sha"] = "0" * 40
expect_code(lambda: verify_snapshot_identity(bad), "E_PR383_SNAPSHOT_SCHEMA_BLOB_DRIFT")

print("PR383 -> canonical v3 migration-gap compiler: PASS")
print(json.dumps(report["counts"], sort_keys=True))
