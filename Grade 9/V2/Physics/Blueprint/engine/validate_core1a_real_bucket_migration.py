#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
PHYSICS = ROOT.parent
sys.path.insert(0, str(ROOT / "engine"))
from validate_engineering_gates_v2 import load as load_gate_registry, validate as validate_gate_registry  # noqa: E402


class MigrationValidationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def load_blueprint(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def load_physics(rel: str):
    return json.loads((PHYSICS / rel).read_text(encoding="utf-8"))


def fail(code: str, message: str):
    raise MigrationValidationError(code, message)


STAGES = [
    "1A0_LEARNER_STATE_GAP",
    "1A1_LEARNING_ATOMS",
    "1A2_INFERENTIAL_JUMPS",
    "1A3_COGNITIVE_TRANSFORMATION",
    "1A4_REPRESENTATION_REQUIREMENTS",
    "1A5_REPRESENTATION_CANDIDATES",
    "1A6_REPRESENTATION_DECISIONS",
    "1A7_PICTURE_WORD_SYMBOL_EQUATION_BRIDGE",
    "1A8_MISCONCEPTION_CONTRAST",
    "1A9_WORKED_FADED_INDEPENDENT_PLAN",
    "1A10_CORE2_TRANSFER_BRIDGE",
    "1A11_UNRESOLVED_JUMP_AUDIT",
]


def validate(audit: dict) -> dict:
    try:
        schema = load_blueprint("contracts/core1a-real-bucket-migration-audit.schema.json")
        jsonschema.validate(audit, schema)
    except jsonschema.ValidationError as exc:
        fail("E_MIGRATION_SCHEMA", exc.message)

    if [row["stage"] for row in audit["stage_audit"]] != STAGES:
        fail("E_MIGRATION_STAGE_ORDER", "stage audit must contain exact 1A0..1A11 order")

    manifest = load_physics("Core1A/registry/build-manifests/M2D-SBA-04-v1.json")
    profile = load_physics("Core1A/registry/physics-core1a-motion-in-a-plane-sba04-20pct-v1.json")
    if manifest["bucket_id"] != audit["bucket_id"]:
        fail("E_MIGRATION_BUCKET_DRIFT", "manifest bucket does not match audit")
    if manifest["handoff"]["status"] != audit["legacy_claim"]["status"]:
        fail("E_MIGRATION_LEGACY_CLAIM_DRIFT", "legacy COMPLETE claim changed or misreported")
    if audit["legacy_claim"]["accepted_as_v9_release_evidence"] is not False:
        fail("E_MIGRATION_LEGACY_AUTHORITY", "legacy COMPLETE may not authorize V9 release")

    bucket = next((b for b in profile["buckets"] if b["bucket_id"] == audit["bucket_id"]), None)
    if bucket is None:
        fail("E_MIGRATION_PROFILE_BUCKET_MISSING", audit["bucket_id"])
    learning_atoms = {a["atom_id"] for a in bucket["profiles"][0]["learning_atoms"]}
    stage_atoms = next(r for r in audit["stage_audit"] if r["stage"] == "1A1_LEARNING_ATOMS")
    if set(stage_atoms["artifact_refs"]) != learning_atoms:
        fail("E_MIGRATION_ATOM_COVERAGE", f"audit atoms do not exactly match repository atoms: expected={sorted(learning_atoms)}")

    primary_questions = set(manifest["primary_questions"])
    stage_transfer = next(r for r in audit["stage_audit"] if r["stage"] == "1A10_CORE2_TRANSFER_BRIDGE")
    if set(stage_transfer["artifact_refs"]) != primary_questions:
        fail("E_MIGRATION_TRANSFER_COVERAGE", "1A10 question coverage does not equal manifest primary_questions")

    releases = {q["question_id"]: q for q in manifest["question_release"]}
    for held_id in ("Q14", "Q27"):
        row = releases.get(held_id)
        if not row or row["status"] != "HELD" or "M2D-SBA-05" not in row["release_prerequisite_buckets"]:
            fail("E_MIGRATION_CROSS_BUCKET_HOLD", f"{held_id} must remain held for M2D-SBA-05")

    registry = load_gate_registry("policy/physics-technical-engineering-gates.v2.json")
    validate_gate_registry(registry)
    gate_map = {g["subtopic_id"]: g for g in registry["gates"]}
    for gid in audit["technical_gate_audit"]["ready_gate_ids"]:
        if gid not in gate_map or gate_map[gid]["status"] != "ENGINEERING_GATE_READY":
            fail("E_MIGRATION_READY_GATE_INVALID", gid)
    for gid in audit["technical_gate_audit"]["missing_gate_candidates"]:
        if gid in gate_map:
            fail("E_MIGRATION_GAP_STALE", f"{gid} now exists; migration audit must be updated")

    incomplete_stages = [r["stage"] for r in audit["stage_audit"] if r["evidence_state"] != "PRESENT"]
    technical_incomplete = audit["technical_gate_audit"]["status"] != "READY"
    if (incomplete_stages or technical_incomplete) and audit["release_authorized"]:
        fail("E_MIGRATION_FALSE_RELEASE", f"release true with technical/stage gaps: {incomplete_stages}")
    if (incomplete_stages or technical_incomplete) and not audit["block_reasons"]:
        fail("E_MIGRATION_BLOCK_REASONS_REQUIRED", "blocked migration requires reasons")

    return {
        "status": "PASS",
        "bucket_id": audit["bucket_id"],
        "legacy_claim": audit["legacy_claim"]["status"],
        "release_authorized": audit["release_authorized"],
        "technical_gate_status": audit["technical_gate_audit"]["status"],
        "incomplete_stages": incomplete_stages,
        "held_questions": [qid for qid, row in releases.items() if row["status"] == "HELD"],
    }


def main():
    rel = sys.argv[1] if len(sys.argv) > 1 else "topics/m2d-sba04-core1a-migration-audit.v1.json"
    print(json.dumps(validate(load_blueprint(rel)), indent=2))


if __name__ == "__main__":
    main()
