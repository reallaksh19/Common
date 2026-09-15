#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema

from compile_pr383_v3_migration_gaps import (
    DISCOVERY_CATALOG_REL,
    SNAPSHOT_MANIFEST_REL,
    canonical_digest,
    git_blob_sha,
    load,
    verify_snapshot_identity,
)
from validate_engineering_discovery_catalog import validate as validate_discovery_catalog

ROOT = Path(__file__).resolve().parents[1]
V3_GATE_SCHEMA_REL = "contracts/physics-technical-engineering-gate-v3.schema.json"
PREFLIGHT_SCHEMA_REL = "contracts/physics-engineering-migration-preflight.schema.json"

SOURCE_TO_V3_COLLECTION = {
    "concepts": "technical_core",
    "relations": "mandatory_equations",
    "model_conditions": "model_conditions",
    "representations": "representations",
    "reasoning_sequence": "reasoning_sequence",
    "required_transformations": "required_transformations",
    "misconceptions": "misconceptions",
    "problem_families": "problem_families",
    "falsification_cases": "falsification_cases",
}


class MigrationPreflightError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str) -> None:
    raise MigrationPreflightError(code, message)


def derive_v3_minimums(schema: dict) -> dict[str, int]:
    try:
        properties = schema["$defs"]["gate"]["properties"]
    except KeyError as exc:
        fail("E_ENG_PREFLIGHT_TARGET_SCHEMA_SHAPE", f"missing target schema key {exc}")
    return {
        field: int(properties[field].get("minItems", 0))
        for field in SOURCE_TO_V3_COLLECTION
    }


def source_counts(gate: dict) -> dict[str, int]:
    return {
        v3_field: len(gate.get(source_field, []))
        for v3_field, source_field in SOURCE_TO_V3_COLLECTION.items()
    }


def validate_report(report: dict) -> None:
    try:
        jsonschema.validate(report, load(PREFLIGHT_SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("E_ENG_PREFLIGHT_REPORT_SCHEMA", exc.message)


def compile_report() -> dict:
    manifest = load(SNAPSHOT_MANIFEST_REL)
    identity = verify_snapshot_identity(manifest)
    registry_v1 = load(manifest["local"]["registry_ref"])
    source_map = {gate["subtopic_id"]: gate for gate in registry_v1["subtopic_gates"]}

    catalog = load(DISCOVERY_CATALOG_REL)
    validate_discovery_catalog(catalog)
    migration_ids = [
        entry["discovery_gate_id"]
        for entry in catalog["discovered_subtopics"]
        if entry["disposition"] == "MIGRATION_REQUIRED"
    ]

    v3_schema = load(V3_GATE_SCHEMA_REL)
    minimums = derive_v3_minimums(v3_schema)
    target_schema_sha = git_blob_sha(ROOT / V3_GATE_SCHEMA_REL)

    entries = []
    satisfied = 0
    for gate_id in migration_ids:
        gate = source_map[gate_id]
        counts = source_counts(gate)
        failures = [field for field in SOURCE_TO_V3_COLLECTION if counts[field] < minimums[field]]
        passes = not failures
        satisfied += int(passes)
        entries.append(
            {
                "discovery_gate_id": gate_id,
                "source_gate_digest": canonical_digest(gate),
                "source_counts": counts,
                "v3_minimums": minimums,
                "unsatisfied_minimums": failures,
                "structural_minimums_satisfied": passes,
                "promotion_authorized": False,
                "readiness_authorized": False,
            }
        )

    report = {
        "schema_version": "1.0.0",
        "report_id": "PR383-TO-V3-SOURCE-STRUCTURAL-PREFLIGHT",
        "source_snapshot": {
            "pr_number": manifest["source"]["pr_number"],
            "head_sha": manifest["source"]["head_sha"],
            "registry_git_blob_sha": identity["registry_git_blob_sha"],
            "source_gate_count": len(source_map),
        },
        "target_contract": {
            "schema_ref": V3_GATE_SCHEMA_REL,
            "schema_git_blob_sha": target_schema_sha,
            "minimums_derived_from_schema": True,
            "readiness_rule": "STRUCTURAL_PREFLIGHT_NEVER_GRANTS_ENGINEERING_READINESS",
        },
        "counts": {
            "migration_gap_count": len(entries),
            "structural_minimums_satisfied_count": satisfied,
            "structural_minimums_blocked_count": len(entries) - satisfied,
        },
        "entries": entries,
    }
    validate_report(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile source-only structural preflight for unresolved Physics v3 migrations")
    parser.add_argument("--out")
    args = parser.parse_args()
    report = compile_report()
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
        print(json.dumps({"status":"COMPILED","report_id":report["report_id"],"counts":report["counts"]}, indent=2))
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
