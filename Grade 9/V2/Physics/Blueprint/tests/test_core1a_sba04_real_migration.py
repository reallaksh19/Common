#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from compile_core1a_real_bucket_migration import compile_audit  # noqa: E402
from validate_core1a_real_bucket_migration import MigrationValidationError, load_blueprint, validate  # noqa: E402

AUDIT = load_blueprint("topics/m2d-sba04-core1a-migration-audit.v1.json")
SPEC_REF = AUDIT["migration_spec_ref"]
SPEC = load_blueprint(SPEC_REF)


def must_fail(doc, code):
    try:
        validate(doc)
    except MigrationValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


# The canonical audit is compiler output from declared data, not a hand-maintained case exception.
assert compile_audit(SPEC, spec_ref=SPEC_REF) == AUDIT

# Positive: live Engineering closure is READY, but incomplete pedagogical stages and explicit transfer holds keep release closed.
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
assert next(r for r in AUDIT["stage_audit"] if r["stage"] == "1A2_INFERENTIAL_JUMPS")["evidence_state"] == "PARTIAL"
assert next(r for r in AUDIT["stage_audit"] if r["stage"] == "1A11_UNRESOLVED_JUMP_AUDIT")["evidence_state"] == "PARTIAL"
assert result["held_questions"] == ["Q14", "Q27"]
assert len(result["high_fragility_step_refs"]) == 8
assert result["learning_atom_ids"] == [f"M2D-SBA-04{x}" for x in "ABCDEFG"]
assert result["transfer_routine_ids"] == [f"M2D-SBA-04-R{x}" for x in range(1, 5)]

# Falsifier 1: legacy COMPLETE may never be promoted directly to current release authority.
bad = copy.deepcopy(AUDIT)
bad["legacy_claim"]["accepted_as_v9_release_evidence"] = True
must_fail(bad, "E_MIGRATION_SCHEMA")

# Falsifier 2: release cannot open while compiler-derived pedagogical gaps or transfer holds remain.
bad = copy.deepcopy(AUDIT)
bad["release_authorized"] = True
must_fail(bad, "E_MIGRATION_FALSE_RELEASE")

# Falsifier 3: learning-atom coverage must exactly match the selected repository profile.
bad = copy.deepcopy(AUDIT)
stage = next(r for r in bad["stage_audit"] if r["stage"] == "1A1_LEARNING_ATOMS")
stage["artifact_refs"].remove("M2D-SBA-04F")
must_fail(bad, "E_MIGRATION_ATOM_COVERAGE")

# Falsifier 4: Core2 transfer coverage must preserve all manifest-declared primary question IDs.
bad = copy.deepcopy(AUDIT)
stage = next(r for r in bad["stage_audit"] if r["stage"] == "1A10_CORE2_TRANSFER_BRIDGE")
stage["artifact_refs"].remove("Q40")
must_fail(bad, "E_MIGRATION_TRANSFER_COVERAGE")

# Falsifier 5: direct-gate custody cannot drift from the live Engineering Gate closure.
bad = copy.deepcopy(AUDIT)
bad["technical_gate_audit"]["direct_gate_ids"].remove("PHY-M2D-SPEED-AT-HEIGHT")
must_fail(bad, "E_MIGRATION_DIRECT_GATE_DRIFT")

# Falsifier 6: transitive-closure custody cannot omit a real prerequisite.
bad = copy.deepcopy(AUDIT)
bad["technical_gate_audit"]["closure_gate_ids"].remove("PHY-VEC-BASICS")
must_fail(bad, "E_MIGRATION_CLOSURE_GATE_DRIFT")

# Falsifier 7: technical READY/INCOMPLETE is derived from the live Engineering Gate closure, not manually editable.
bad = copy.deepcopy(AUDIT)
bad["technical_gate_audit"]["status"] = "INCOMPLETE"
must_fail(bad, "E_MIGRATION_TECHNICAL_STATUS_DRIFT")

# Falsifier 8: the audit cannot switch its Engineering binding independently of the migration spec.
bad = copy.deepcopy(AUDIT)
bad["technical_gate_audit"]["engineering_manifest_ref"] = "fixtures/engineering-workbench/m2d-sba23-manifest.v3.json"
must_fail(bad, "E_MIGRATION_ENGINEERING_BINDING_DRIFT")

# Falsifier 9: canonical stage order comes from the global Core1A stage-machine policy.
bad = copy.deepcopy(AUDIT)
bad["stage_audit"][2], bad["stage_audit"][3] = bad["stage_audit"][3], bad["stage_audit"][2]
must_fail(bad, "E_MIGRATION_STAGE_ORDER")

# Falsifier 10: source custody is derived from declared build/spec inputs; remembered extras cannot be smuggled in.
bad = copy.deepcopy(AUDIT)
bad["source_refs"].append("policy/core1a-stage-machine.v1.json")
bad["source_refs"].sort()
must_fail(bad, "E_MIGRATION_SOURCE_CUSTODY_DRIFT")

# Architectural guard: case facts are data, not Python branches in the generic compiler/validator.
for rel in ("engine/compile_core1a_real_bucket_migration.py", "engine/validate_core1a_real_bucket_migration.py"):
    text = (ROOT / rel).read_text(encoding="utf-8")
    for forbidden in ("M2D-SBA-04", "M2D-SBA-05", "Q14", "Q27"):
        assert forbidden not in text, f"CASE_LITERAL_LEAK:{rel}:{forbidden}"

print("Core1A real-bucket migration: PASS (generic compiler + real SBA04 data + fail-closed 1A12 boundary)")
