#!/usr/bin/env python3
from __future__ import annotations

import copy
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from compile_core1a_real_bucket_migration import MigrationCompilationError, compile_audit  # noqa: E402
from validate_core1a_real_bucket_migration import MigrationValidationError, load_blueprint, validate  # noqa: E402

AUDIT = load_blueprint("topics/m2d-sba04-core1a-migration-audit.v1.json")
SPEC_REF = AUDIT["migration_spec_ref"]
SPEC = load_blueprint(SPEC_REF)
CANONICAL_STAGE_EVIDENCE = [
    "topics/m2d-sba04-stage-evidence/1a0-learner-state-gap.v1.json",
    "topics/m2d-sba04-stage-evidence/1a2-inferential-jump-closure.v1.json",
    "topics/m2d-sba04-stage-evidence/1a3-cognitive-transformation.v1.json",
    "topics/m2d-sba04-stage-evidence/1a4-representation-requirements.v1.json",
    "topics/m2d-sba04-stage-evidence/1a5-representation-candidates.v1.json",
    "topics/m2d-sba04-stage-evidence/1a6-representation-decision.v1.json",
    "topics/m2d-sba04-stage-evidence/1a7-pwse-bridge.v1.json",
    "topics/m2d-sba04-stage-evidence/1a9-worked-faded-independent.v1.json",
    "topics/m2d-sba04-stage-evidence/1a11-unresolved-jump-closure.v1.json",
]
LEARNER_GAP_RECEIPT = "fixtures/core1a-migration-stage-evidence/valid-learner-state-gap.json"
CANDIDATE_RECEIPT = "fixtures/core1a-migration-stage-evidence/valid-representation-candidates.json"
DECISION_RECEIPT = "fixtures/core1a-migration-stage-evidence/valid-representation-decision.json"
LINEAGE_RECEIPT = "fixtures/core1a-migration-stage-evidence/valid-worked-faded-lineage.json"
WRONG_KIND_RECEIPT = "fixtures/core1a-migration-stage-evidence/wrong-kind.json"
MALFORMED_GAP_NO_INVENTORY_RECEIPT = "fixtures/core1a-migration-stage-evidence/malformed-learner-state-gap-no-inventory.json"
MALFORMED_GAP_PUBLICATION_EVIDENCE_RECEIPT = "fixtures/core1a-migration-stage-evidence/malformed-learner-state-gap-publication-evidence.json"
MALFORMED_LINEAGE_RECEIPT = "fixtures/core1a-migration-stage-evidence/malformed-worked-faded-lineage.json"


def must_fail(doc, code):
    try:
        validate(doc)
    except MigrationValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def must_compile_fail(spec, code):
    try:
        compile_audit(spec, spec_ref=SPEC_REF)
    except MigrationCompilationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def stage_state(audit, stage):
    return next(r for r in audit["stage_audit"] if r["stage"] == stage)["evidence_state"]


# The canonical audit is compiler output from declared data, not a hand-maintained case exception.
assert SPEC["stage_evidence_refs"] == CANONICAL_STAGE_EVIDENCE
assert compile_audit(SPEC, spec_ref=SPEC_REF) == AUDIT

# Positive: every pre-manuscript stage is evidence-backed, Engineering is READY, and the completed SBA05 bridge has released Q14/Q27.
result = validate(AUDIT)
assert result["status"] == "PASS"
assert result["legacy_claim"] == "COMPLETE"
assert result["release_authorized"] is True
assert result["technical_gate_status"] == "READY"
assert result["engineering_registry_ref"] == "GENERATED:physics-technical-engineering-gates.v3"
assert result["engineering_gate_count"] == 11
assert result["engineering_registry_digest"].startswith("sha256:")
assert result["engineering_closure_digest"].startswith("sha256:")
assert result["incomplete_stages"] == []
assert all(row["evidence_state"] == "PRESENT" for row in AUDIT["stage_audit"])
assert result["held_questions"] == []
assert AUDIT["block_reasons"] == []
assert len(result["high_fragility_step_refs"]) == 8
assert result["learning_atom_ids"] == [f"M2D-SBA-04{x}" for x in "ABCDEFG"]
assert result["transfer_routine_ids"] == [f"M2D-SBA-04-R{x}" for x in range(1, 5)]

# Falsifier 1: legacy COMPLETE may never be promoted directly to current release authority.
bad = copy.deepcopy(AUDIT)
bad["legacy_claim"]["accepted_as_v9_release_evidence"] = True
must_fail(bad, "E_MIGRATION_SCHEMA")

# Falsifier 2: canonical release authority may not be manually forced closed once governed blockers are gone.
bad = copy.deepcopy(AUDIT)
bad["release_authorized"] = False
must_fail(bad, "E_MIGRATION_RELEASE_DRIFT")

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

# Typed receipt positive 0: 1A0 requires an explicit intrinsic-design/control-state gap inventory.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [LEARNER_GAP_RECEIPT]
probe_audit = compile_audit(probe, spec_ref=SPEC_REF)
assert stage_state(probe_audit, "1A0_LEARNER_STATE_GAP") == "PRESENT"
assert stage_state(probe_audit, "1A5_REPRESENTATION_CANDIDATES") == "MISSING"
assert probe_audit["release_authorized"] is False

# Typed receipt falsifier 0a: a learner-state claim without any capability gap inventory is not admissible.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [MALFORMED_GAP_NO_INVENTORY_RECEIPT]
must_compile_fail(probe, "E_MIG_COMPILE_STAGE_RECEIPT_SCHEMA")

# Typed receipt falsifier 0b: publication teaching receipts may not masquerade as learner evidence.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [MALFORMED_GAP_PUBLICATION_EVIDENCE_RECEIPT]
must_compile_fail(probe, "E_MIG_COMPILE_STAGE_RECEIPT_SCHEMA")

# Typed receipt positive 1: candidate-set proof can promote 1A5 only; it cannot imply a representation decision.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [CANDIDATE_RECEIPT]
probe_audit = compile_audit(probe, spec_ref=SPEC_REF)
assert stage_state(probe_audit, "1A5_REPRESENTATION_CANDIDATES") == "PRESENT"
assert stage_state(probe_audit, "1A6_REPRESENTATION_DECISIONS") == "MISSING"
assert probe_audit["release_authorized"] is False

# Typed receipt positive 2: an explicit decision receipt independently promotes 1A6 after candidate evidence is present.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [CANDIDATE_RECEIPT, DECISION_RECEIPT]
probe_audit = compile_audit(probe, spec_ref=SPEC_REF)
assert stage_state(probe_audit, "1A5_REPRESENTATION_CANDIDATES") == "PRESENT"
assert stage_state(probe_audit, "1A6_REPRESENTATION_DECISIONS") == "PRESENT"
assert probe_audit["release_authorized"] is False

# Typed receipt positive 3: worked/faded evidence requires an explicit worked -> faded -> independent lineage fingerprint.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [LINEAGE_RECEIPT]
probe_audit = compile_audit(probe, spec_ref=SPEC_REF)
assert stage_state(probe_audit, "1A9_WORKED_FADED_INDEPENDENT_PLAN") == "PRESENT"
assert probe_audit["release_authorized"] is False

# Typed receipt falsifier 1: a decision-shaped receipt may not masquerade as candidate-set evidence.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [WRONG_KIND_RECEIPT]
must_compile_fail(probe, "E_MIG_COMPILE_STAGE_RECEIPT_SCHEMA")

# Typed receipt falsifier 2: a worked/faded claim without an invariant lineage fingerprint is not admissible.
probe = copy.deepcopy(SPEC)
probe["stage_evidence_refs"] = [MALFORMED_LINEAGE_RECEIPT]
must_compile_fail(probe, "E_MIG_COMPILE_STAGE_RECEIPT_SCHEMA")

# Architectural guard: case facts are data, not Python branches in the generic compiler/validator.
for rel in ("engine/compile_core1a_real_bucket_migration.py", "engine/validate_core1a_real_bucket_migration.py"):
    text = (ROOT / rel).read_text(encoding="utf-8")
    for forbidden in ("M2D-SBA-04", "M2D-SBA-05", "Q14", "Q27"):
        assert forbidden not in text, f"CASE_LITERAL_LEAK:{rel}:{forbidden}"

# Keep all real SBA04 authored-evidence receipts on the same authoritative CI path as the aggregate migration test.
for rel in (
    "tests/test_core1a_sba04_real_inferential_jump_receipt.py",
    "tests/test_core1a_sba04_real_cognitive_transformation_receipt.py",
    "tests/test_core1a_sba04_real_representation_requirements_receipt.py",
    "tests/test_core1a_sba04_real_representation_design.py",
    "tests/test_core1a_sba04_real_pwse_bridge.py",
    "tests/test_core1a_sba04_real_worked_faded_lineage.py",
    "tests/test_core1a_sba04_unresolved_jump_audit.py",
    "tests/test_core1a_sba04_real_learner_state_gap.py",
):
    runpy.run_path(str(ROOT / rel), run_name="__main__")

print("Core1A real-bucket migration: PASS (canonical real SBA04 evidence + completed SBA05 cross-bucket bridge authorize release)")
