#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_core1a_real_bucket_migration import MigrationValidationError, load_blueprint, validate  # noqa: E402

AUDIT = load_blueprint("topics/m2d-sba04-core1a-migration-audit.v1.json")


def must_fail(doc, code):
    try:
        validate(doc)
    except MigrationValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


# Positive: technical Engineering closure is now READY, but legacy COMPLETE still cannot authorize Core1A release.
result = validate(AUDIT)
assert result["status"] == "PASS"
assert result["legacy_claim"] == "COMPLETE"
assert result["release_authorized"] is False
assert result["technical_gate_status"] == "READY"
assert result["engineering_registry_ref"] == "GENERATED:physics-technical-engineering-gates.v3"
assert result["engineering_gate_count"] == 11
assert result["engineering_registry_digest"].startswith("sha256:")
assert result["engineering_closure_digest"].startswith("sha256:")
assert "1A0_LEARNER_STATE_GAP" in result["incomplete_stages"]
assert "1A2_INFERENTIAL_JUMPS" in result["incomplete_stages"]
assert "1A11_UNRESOLVED_JUMP_AUDIT" in result["incomplete_stages"]
assert set(result["held_questions"]) >= {"Q14", "Q27"}

# Falsifier 1: legacy COMPLETE may never be promoted directly to current release authority.
bad = copy.deepcopy(AUDIT)
bad["legacy_claim"]["accepted_as_v9_release_evidence"] = True
must_fail(bad, "E_MIGRATION_SCHEMA")

# Falsifier 2: release cannot open while explicit pedagogical stage gaps remain, even with technical READY.
bad = copy.deepcopy(AUDIT)
bad["release_authorized"] = True
must_fail(bad, "E_MIGRATION_FALSE_RELEASE")

# Falsifier 3: learning-atom coverage must exactly match repository state.
bad = copy.deepcopy(AUDIT)
stage = next(r for r in bad["stage_audit"] if r["stage"] == "1A1_LEARNING_ATOMS")
stage["artifact_refs"].remove("M2D-SBA-04F")
must_fail(bad, "E_MIGRATION_ATOM_COVERAGE")

# Falsifier 4: Core2 transfer coverage must preserve all primary question IDs.
bad = copy.deepcopy(AUDIT)
stage = next(r for r in bad["stage_audit"] if r["stage"] == "1A10_CORE2_TRANSFER_BRIDGE")
stage["artifact_refs"].remove("Q40")
must_fail(bad, "E_MIGRATION_TRANSFER_COVERAGE")

# Falsifier 5: direct-gate custody cannot drift from the live Workbench manifest/receipt.
bad = copy.deepcopy(AUDIT)
bad["technical_gate_audit"]["direct_gate_ids"].remove("PHY-M2D-SPEED-AT-HEIGHT")
must_fail(bad, "E_MIGRATION_DIRECT_GATE_DRIFT")

# Falsifier 6: transitive-closure custody cannot omit a real prerequisite.
bad = copy.deepcopy(AUDIT)
bad["technical_gate_audit"]["closure_gate_ids"].remove("PHY-VEC-BASICS")
must_fail(bad, "E_MIGRATION_CLOSURE_GATE_DRIFT")

# Falsifier 7: technical READY/INCOMPLETE is derived from the current Workbench closure, not manually editable.
bad = copy.deepcopy(AUDIT)
bad["technical_gate_audit"]["status"] = "INCOMPLETE"
must_fail(bad, "E_MIGRATION_TECHNICAL_STATUS_DRIFT")

# Falsifier 8: migration cannot silently bind another bucket's Workbench manifest.
bad = copy.deepcopy(AUDIT)
bad["technical_gate_audit"]["engineering_manifest_ref"] = "fixtures/engineering-workbench/m2d-sba23-manifest.v3.json"
must_fail(bad, "E_MIGRATION_ENGINEERING_REQUEST_MANIFEST_MISMATCH")

# Falsifier 9: stage order cannot drift.
bad = copy.deepcopy(AUDIT)
bad["stage_audit"][2], bad["stage_audit"][3] = bad["stage_audit"][3], bad["stage_audit"][2]
must_fail(bad, "E_MIGRATION_STAGE_ORDER")

print("Core1A M2D-SBA-04 real migration audit: PASS (live v3 Workbench technical authority + fail-closed pedagogical release)")
