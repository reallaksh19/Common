#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_core1a_real_bucket_migration import (  # noqa: E402
    MigrationCompilationError,
    compile_audit_with_facts,
    load_json,
    resolve_repo_ref,
)


class MigrationValidationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def load_blueprint(rel: str):
    return load_json(ROOT / rel)


def fail(code: str, message: str) -> None:
    raise MigrationValidationError(code, message)


def validate(audit: dict) -> dict:
    try:
        jsonschema.validate(audit, load_blueprint("contracts/core1a-real-bucket-migration-audit.schema.json"))
    except jsonschema.ValidationError as exc:
        fail("E_MIGRATION_SCHEMA", exc.message)

    stages = load_blueprint("policy/core1a-stage-machine.v1.json")["pre_manuscript_stages"]
    if [row["stage"] for row in audit["stage_audit"]] != stages:
        fail("E_MIGRATION_STAGE_ORDER", "stage audit must contain the canonical pre-manuscript stage order")

    try:
        spec_path = resolve_repo_ref(audit["migration_spec_ref"])
        spec = load_json(spec_path)
        expected, facts = compile_audit_with_facts(spec, spec_ref=audit["migration_spec_ref"])
    except MigrationCompilationError as exc:
        fail("E_MIGRATION_DERIVATION", f"{exc.code}: {exc.message}")

    if audit["bucket_id"] != expected["bucket_id"]:
        fail("E_MIGRATION_BUCKET_DRIFT", f"audit bucket {audit['bucket_id']} != spec-derived {expected['bucket_id']}")
    if audit["source_refs"] != expected["source_refs"]:
        fail("E_MIGRATION_SOURCE_CUSTODY_DRIFT", "audit source_refs do not equal the spec-derived repository source set")

    if audit["legacy_claim"]["status"] != expected["legacy_claim"]["status"] or audit["legacy_claim"]["claim_ref"] != expected["legacy_claim"]["claim_ref"]:
        fail("E_MIGRATION_LEGACY_CLAIM_DRIFT", "legacy claim no longer matches the declared repository claim")
    if audit["legacy_claim"]["accepted_as_v9_release_evidence"] is not False:
        fail("E_MIGRATION_LEGACY_AUTHORITY", "legacy completion may not authorize current Core1A release")

    technical = audit["technical_gate_audit"]
    expected_technical = expected["technical_gate_audit"]
    if (
        technical["engineering_request_ref"] != expected_technical["engineering_request_ref"]
        or technical["engineering_manifest_ref"] != expected_technical["engineering_manifest_ref"]
        or technical["registry_ref"] != expected_technical["registry_ref"]
    ):
        fail("E_MIGRATION_ENGINEERING_BINDING_DRIFT", "technical audit bindings differ from the migration spec/live Engineering Gate authority")
    if set(technical["direct_gate_ids"]) != set(expected_technical["direct_gate_ids"]):
        fail("E_MIGRATION_DIRECT_GATE_DRIFT", f"audit direct gates do not match current Engineering Gate closure: {expected_technical['direct_gate_ids']}")
    if set(technical["closure_gate_ids"]) != set(expected_technical["closure_gate_ids"]):
        fail("E_MIGRATION_CLOSURE_GATE_DRIFT", f"audit closure gates do not match current Engineering Gate closure: {expected_technical['closure_gate_ids']}")
    if technical["status"] != expected_technical["status"]:
        fail("E_MIGRATION_TECHNICAL_STATUS_DRIFT", f"audit={technical['status']} current={expected_technical['status']}")

    actual_rows = {row["stage"]: row for row in audit["stage_audit"]}
    expected_rows = {row["stage"]: row for row in expected["stage_audit"]}
    atom_stage = stages[1]
    if set(actual_rows[atom_stage]["artifact_refs"]) != set(expected_rows[atom_stage]["artifact_refs"]):
        fail("E_MIGRATION_ATOM_COVERAGE", "learning-atom evidence does not exactly match the selected repository profile")
    transfer_stage = stages[10]
    if set(actual_rows[transfer_stage]["artifact_refs"]) != set(expected_rows[transfer_stage]["artifact_refs"]):
        fail("E_MIGRATION_TRANSFER_COVERAGE", "Core2 transfer evidence does not exactly match build-manifest primary questions")

    for stage in stages:
        if actual_rows[stage] != expected_rows[stage]:
            fail("E_MIGRATION_STAGE_EVIDENCE_DRIFT", f"{stage} differs from evidence derived by the generic migration compiler")

    incomplete_stages = [row["stage"] for row in expected["stage_audit"] if row["evidence_state"] != "PRESENT"]
    if audit["release_authorized"] and not expected["release_authorized"]:
        fail("E_MIGRATION_FALSE_RELEASE", f"release true with governed blockers: {incomplete_stages}")
    if audit["release_authorized"] != expected["release_authorized"]:
        fail("E_MIGRATION_RELEASE_DRIFT", f"audit={audit['release_authorized']} derived={expected['release_authorized']}")
    if audit["block_reasons"] != expected["block_reasons"]:
        fail("E_MIGRATION_BLOCK_REASON_DRIFT", "block reasons do not equal the compiler-derived blockers")

    receipt = facts["engineering_receipt"]
    return {
        "status": "PASS",
        "bucket_id": audit["bucket_id"],
        "legacy_claim": audit["legacy_claim"]["status"],
        "release_authorized": audit["release_authorized"],
        "technical_gate_status": expected_technical["status"],
        "engineering_registry_ref": receipt["registry_ref"],
        "engineering_registry_digest": receipt["registry_digest"],
        "engineering_closure_digest": receipt["closure_digest"],
        "engineering_gate_count": receipt["counts"]["transitive_gate_count"],
        "incomplete_stages": incomplete_stages,
        "held_questions": facts["held_questions"],
        "high_fragility_step_refs": facts["high_fragility_step_refs"],
        "learning_atom_ids": facts["learning_atom_ids"],
        "transfer_routine_ids": facts["transfer_routine_ids"],
    }


def main() -> None:
    rel = sys.argv[1] if len(sys.argv) > 1 else "topics/m2d-sba04-core1a-migration-audit.v1.json"
    print(json.dumps(validate(load_blueprint(rel)), indent=2))


if __name__ == "__main__":
    main()
