#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from validate_engineering_discovery_catalog import validate as validate_discovery_catalog  # noqa: E402
from validate_engineering_gates_v3 import validate as validate_v3_registry  # noqa: E402

SNAPSHOT_MANIFEST_REL = "provenance/pr383/source-snapshot.manifest.json"
DISCOVERY_CATALOG_REL = "policy/physics-engineering-discovery-catalog.pr383.v1.json"
REPORT_SCHEMA_REL = "contracts/physics-engineering-migration-gap-report.schema.json"

BLOCKER_CODES = [
    "V3_SCOPE_STATE_REVIEW_REQUIRED",
    "V3_APPLICABLE_CORES_REQUIRED",
    "V3_REQUIRED_INVARIANT_PROFILE_REQUIRED",
    "V3_RELATION_SYMBOL_SEMANTICS_REQUIRED",
    "V3_MODEL_CONDITION_BINDINGS_REQUIRED",
    "V3_REPRESENTATION_SEMANTIC_BINDINGS_REQUIRED",
    "V3_REASONING_DEPENDENCY_BINDINGS_REQUIRED",
    "V3_TRANSFORMATION_STABLE_IDS_REQUIRED",
    "V3_MISCONCEPTION_REPRESENTATION_REPAIR_REQUIRED",
    "V3_PROBLEM_FAMILY_TECHNICAL_BINDINGS_REQUIRED",
    "V3_FALSIFICATION_STABLE_FAILURE_CODES_REQUIRED",
]

PRESERVED_SOURCE_FIELDS = [
    "subtopic_id",
    "learner_title",
    "chapter",
    "jee_tier",
    "cbse_ref",
    "authority_tier",
    "provenance",
    "canonical_concept_ids",
    "prerequisite_ids",
    "linked_buckets",
    "linked_problem_family_ids",
    "technical_core",
    "mandatory_equations",
    "representations",
    "model_conditions",
    "reasoning_sequence",
    "required_transformations",
    "misconceptions",
    "mandatory_verifications",
    "problem_families",
    "difficulty_profile",
    "falsification_cases",
]

DISCARDED_SOURCE_CONTROL_FIELDS = [
    "technical_readiness",
    "release_checklist",
]


class PR383MigrationGapError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str) -> None:
    raise PR383MigrationGapError(code, message)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    framed = f"blob {len(raw)}\0".encode("ascii") + raw
    return hashlib.sha1(framed).hexdigest()


def verify_snapshot_identity(manifest: dict) -> dict:
    source = manifest["source"]
    local = manifest["local"]

    registry_path = ROOT / local["registry_ref"]
    schema_path = ROOT / local["schema_ref"]

    actual_registry_blob = git_blob_sha(registry_path)
    actual_schema_blob = git_blob_sha(schema_path)

    if actual_registry_blob != source["registry_git_blob_sha"]:
        fail(
            "E_PR383_SNAPSHOT_REGISTRY_BLOB_DRIFT",
            f"expected {source['registry_git_blob_sha']} got {actual_registry_blob}",
        )
    if actual_schema_blob != source["schema_git_blob_sha"]:
        fail(
            "E_PR383_SNAPSHOT_SCHEMA_BLOB_DRIFT",
            f"expected {source['schema_git_blob_sha']} got {actual_schema_blob}",
        )

    return {
        "registry_git_blob_sha": actual_registry_blob,
        "schema_git_blob_sha": actual_schema_blob,
    }


def validate_report(report: dict) -> None:
    try:
        jsonschema.validate(report, load(REPORT_SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("E_PR383_MIGRATION_REPORT_SCHEMA", exc.message)


def compile_report() -> dict:
    manifest = load(SNAPSHOT_MANIFEST_REL)
    identity = verify_snapshot_identity(manifest)

    registry_v1 = load(manifest["local"]["registry_ref"])
    schema_v1 = load(manifest["local"]["schema_ref"])
    try:
        jsonschema.validate(registry_v1, schema_v1)
    except jsonschema.ValidationError as exc:
        fail("E_PR383_SNAPSHOT_SCHEMA_INVALID", exc.message)

    catalog = load(DISCOVERY_CATALOG_REL)
    validate_discovery_catalog(catalog)

    source_gates = registry_v1["subtopic_gates"]
    source_map = {gate["subtopic_id"]: gate for gate in source_gates}
    if len(source_map) != len(source_gates):
        fail("E_PR383_SNAPSHOT_DUPLICATE_ID", "snapshot contains duplicate subtopic_id")

    catalog_ids = {entry["discovery_gate_id"] for entry in catalog["discovered_subtopics"]}
    source_ids = set(source_map)
    if source_ids != catalog_ids:
        fail(
            "E_PR383_SNAPSHOT_CATALOG_ID_DRIFT",
            f"snapshot-only={sorted(source_ids - catalog_ids)} catalog-only={sorted(catalog_ids - source_ids)}",
        )

    registry_v3 = build_registry()
    validate_v3_registry(registry_v3)
    current_v3_ids = {gate["subtopic_id"] for gate in registry_v3["gates"]}

    gaps = []
    exact_or_mapped = []
    for entry in catalog["discovered_subtopics"]:
        gate_id = entry["discovery_gate_id"]
        gate = source_map[gate_id]
        disposition = entry["disposition"]

        if disposition == "MIGRATION_REQUIRED":
            if gate_id in current_v3_ids:
                fail(
                    "E_PR383_MIGRATION_STALE_HOLD",
                    f"{gate_id} now exists in canonical v3 and must be reconciled before gap compilation",
                )
            gaps.append(
                {
                    "discovery_gate_id": gate_id,
                    "source_gate_digest": canonical_digest(gate),
                    "curriculum": {
                        "cbse_ref": gate["cbse_ref"],
                        "jee_tier": gate["jee_tier"],
                    },
                    "source_authority": {
                        "authority_tier": gate["authority_tier"],
                        "provenance": gate["provenance"],
                    },
                    "preserved_source_fields": PRESERVED_SOURCE_FIELDS,
                    "discarded_source_control_fields": DISCARDED_SOURCE_CONTROL_FIELDS,
                    "blocked_by": BLOCKER_CODES,
                    "promotion_status": "BLOCKED_PENDING_V3_ENRICHMENT",
                    "promotion_authorized": False,
                }
            )
        else:
            exact_or_mapped.append(
                {
                    "discovery_gate_id": gate_id,
                    "disposition": disposition,
                    "v3_gate_ids": entry["v3_gate_ids"],
                    "source_gate_digest": canonical_digest(gate),
                }
            )

    report = {
        "schema_version": "1.0.0",
        "report_id": "PR383-TO-CANONICAL-V3-MIGRATION-GAPS",
        "source_snapshot": {
            "pr_number": manifest["source"]["pr_number"],
            "head_sha": manifest["source"]["head_sha"],
            **identity,
            "source_gate_count": len(source_gates),
            "source_registry_digest": canonical_digest(registry_v1),
        },
        "target_control_plane": {
            "registry_ref": "GENERATED:physics-technical-engineering-gates.v3",
            "canonical_v3_gate_count": len(current_v3_ids),
            "readiness_rule": "DERIVED_BY_PRODUCTION_V3_VALIDATOR",
            "source_self_asserted_readiness_imported": False,
            "case_specific_overrides": "PROHIBITED",
        },
        "counts": {
            "discovered_subtopic_count": len(source_gates),
            "already_reconciled_count": len(exact_or_mapped),
            "migration_gap_count": len(gaps),
        },
        "already_reconciled": exact_or_mapped,
        "migration_gaps": gaps,
    }
    validate_report(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile fail-closed PR383 to canonical v3 engineering migration gaps")
    parser.add_argument("--out")
    args = parser.parse_args()

    report = compile_report()
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
        print(json.dumps({"status": "COMPILED", "report_id": report["report_id"], "counts": report["counts"]}, indent=2))
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
