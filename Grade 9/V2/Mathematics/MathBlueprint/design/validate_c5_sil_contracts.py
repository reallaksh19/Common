#!/usr/bin/env python3
"""C5 design validator for SIL contracts and PR #395 integration.

This validator proves architecture/custody properties only. It does not promote
SIL contracts, PR #395 prose, research, or tooling into production authority.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DESIGN = Path(__file__).resolve().parent

CATALOG_PATH = DESIGN / "c5-sil-contract-catalog.candidate.json"
INTEGRATION_PATH = DESIGN / "pr395-sil-integration.candidate.json"
C4_RECEIPT_PATH = DESIGN / "mathematics-subject-adapter-equivalence.receipt.json"
DOMAIN_SCHEMA_PATH = ROOT / "contracts" / "math-canonical-domain-registry.schema.json"

EXPECTED_PR395_HEAD = "242878b04787905087060318c14b89b14238f195"
EXPECTED_C4_BLOB = "b7c264572bb3092a73bf95e4ec46e8872bf1cb72"
EXPECTED_CONTRACT_IDS = {
    "SIL-PACK",
    "SIL-LEARNING-TRANSITION",
    "SIL-SOURCE-SELECTION",
    "SIL-GAP",
    "SIL-COVERAGE",
}
FORBIDDEN_PACK_PROPERTY_NAMES = {
    "expression",
    "equation",
    "formula",
    "statement",
    "derivation_steps",
    "canonical_solution",
    "mathematical_truth",
    "problem_prompt",
}
ALLOWED_PR395_CLASSIFICATIONS = {
    "CANDIDATE_SUBTOPIC_CORPUS",
    "STRUCTURAL_VALIDATOR_REFERENCE",
    "CANDIDATE_RESEARCH_CORPUS",
    "OBSERVABILITY_TOOLING_CANDIDATE",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)], cwd=ROOT, text=True
    ).strip()


def property_names(node: Any) -> set[str]:
    out: set[str] = set()
    if isinstance(node, dict):
        props = node.get("properties")
        if isinstance(props, dict):
            out.update(props.keys())
        for value in node.values():
            out.update(property_names(value))
    elif isinstance(node, list):
        for value in node:
            out.update(property_names(value))
    return out


def validate_documents(
    catalog: dict[str, Any],
    integration: dict[str, Any],
    schemas: dict[str, dict[str, Any]],
    c4: dict[str, Any],
    domain_schema: dict[str, Any],
    check_disk_custody: bool = True,
) -> list[str]:
    errors: list[str] = []

    def need(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    need(catalog.get("status") == "DESIGN_CONTRACTS_READY", "C5_CATALOG_STATUS")
    need(catalog.get("authority") == "NONE", "C5_CATALOG_AUTHORITY")
    need(catalog.get("semantic_change") == "NONE", "C5_CATALOG_SEMANTIC_CHANGE")
    need(catalog.get("runtime_migration_authorized") is False, "C5_RUNTIME_MIGRATION")
    need(catalog.get("production_consumers_allowed") is False, "C5_PRODUCTION_CONSUMER")
    need(catalog.get("next_stage") == "C6_MATHEMATICS_SIL_PILOT_READY", "C5_NEXT_STAGE")

    contracts = catalog.get("contracts", [])
    need({c.get("contract_id") for c in contracts} == EXPECTED_CONTRACT_IDS, "C5_CONTRACT_SET")
    for contract in contracts:
        need(contract.get("authority_effect") == "NONE", "C5_CONTRACT_AUTHORITY_EFFECT")
        rel = contract.get("path", "")
        need(rel.startswith("design/") and rel.endswith(".candidate.schema.json"), "C5_CONTRACT_LOCATION")
        schema = schemas.get(contract.get("contract_id"))
        need(isinstance(schema, dict), "C5_SCHEMA_MISSING")
        if check_disk_custody and rel:
            path = ROOT / rel
            need(path.is_file(), "C5_SCHEMA_PATH_MISSING")
            if path.is_file():
                need(git_blob(path) == contract.get("git_blob_sha"), "C5_SCHEMA_BLOB_DRIFT")

    pack = schemas.get("SIL-PACK", {})
    props = pack.get("properties", {})
    need(pack.get("additionalProperties") is False, "C5_PACK_OPEN_SCHEMA")
    need(props.get("authority", {}).get("const") == "NONE", "C5_PACK_AUTHORITY")
    need(props.get("technical_authorization", {}).get("const") == "NOT_GRANTED_BY_PACK", "C5_PACK_TECH_AUTH")
    need(props.get("publication_authorization", {}).get("const") == "NOT_IMPLIED", "C5_PACK_PUBLICATION_AUTH")
    need(props.get("learner_mastery_claim", {}).get("const") == "NOT_IMPLIED", "C5_PACK_MASTERY")
    need("subject_object_refs" in props, "C5_PACK_EXACT_SUBJECT_REFS")
    need(not (property_names(pack) & FORBIDDEN_PACK_PROPERTY_NAMES), "C5_INLINE_SUBJECT_TRUTH_FORBIDDEN")

    transition = schemas.get("SIL-LEARNING-TRANSITION", {})
    tprops = transition.get("properties", {})
    kinds = set(tprops.get("transition_kind", {}).get("enum", []))
    classes = set(tprops.get("transition_authority_class", {}).get("enum", []))
    need("LOGICAL_DEPENDENCY_REFERENCE" in kinds, "C5_LOGICAL_DEPENDENCY_KIND")
    need("INSTRUCTIONAL_SEQUENCE" in kinds and "REPAIR_SEQUENCE" in kinds, "C5_PEDAGOGY_TRANSITION_KINDS")
    need("SUBJECT_REFERENCE_ONLY" in classes and "PEDAGOGY_GOVERNED" in classes, "C5_TRANSITION_AUTHORITY_CLASSES")
    need(bool(transition.get("allOf")), "C5_TRANSITION_CROSS_FIELD_GUARD")

    source = schemas.get("SIL-SOURCE-SELECTION", {})
    sprops = source.get("properties", {})
    need(sprops.get("authority", {}).get("const") == "NONE", "C5_SOURCE_AUTHORITY")
    need(sprops.get("technical_authorization", {}).get("const") == "NOT_IMPLIED", "C5_SOURCE_TECH_AUTH")
    need("why_preferred" in sprops and "known_limitations" in sprops, "C5_SOURCE_RATIONALE")

    coverage = schemas.get("SIL-COVERAGE", {})
    cprops = coverage.get("properties", {})
    need(cprops.get("authority", {}).get("const") == "DERIVED_LIBRARY_COVERAGE", "C5_COVERAGE_AUTHORITY")
    need(cprops.get("technical_authorization", {}).get("const") == "NOT_IMPLIED", "C5_COVERAGE_TECH_AUTH")
    need(cprops.get("publication_authorization", {}).get("const") == "NOT_IMPLIED", "C5_COVERAGE_PUBLICATION_AUTH")

    gap = schemas.get("SIL-GAP", {})
    gprops = gap.get("properties", {})
    need("MISSING_SUBJECT_TRUTH" in set(gprops.get("gap_class", {}).get("enum", [])), "C5_GAP_SUBJECT_TRUTH")
    need("ENRICH_ENGINEERING" in set(gprops.get("recommended_action_class", {}).get("enum", [])), "C5_GAP_ENGINEERING_ROUTE")

    need(integration.get("authority") == "NONE", "C5_PR395_AUTHORITY")
    need(integration.get("semantic_change") == "NONE", "C5_PR395_SEMANTIC_CHANGE")
    need(integration.get("runtime_migration_authorized") is False, "C5_PR395_RUNTIME_MIGRATION")
    need(integration.get("production_consumers_allowed") is False, "C5_PR395_PRODUCTION_CONSUMER")
    need(integration.get("normalization_rule") == "EXACT_REFERENCE_COMPOSITION_ONLY", "C5_PR395_NORMALIZATION")
    source_pr = integration.get("source_pull_request", {})
    need(source_pr.get("number") == 395, "C5_PR395_NUMBER")
    need(source_pr.get("head_sha") == EXPECTED_PR395_HEAD, "C5_PR395_HEAD")
    need(source_pr.get("relationship") == "DIVERGED", "C5_PR395_RELATIONSHIP")
    need(source_pr.get("ahead_by") == 21 and source_pr.get("behind_by") == 9, "C5_PR395_DIVERGENCE_COUNTS")
    need(source_pr.get("whole_branch_merge_authorized") is False, "C5_PR395_WHOLE_MERGE")

    surfaces = integration.get("candidate_surfaces", [])
    need(len(surfaces) == 4, "C5_PR395_SURFACE_COUNT")
    for surface in surfaces:
        need(surface.get("classification") in ALLOWED_PR395_CLASSIFICATIONS, "C5_PR395_SURFACE_CLASSIFICATION")
        need(surface.get("technical_authorization") == "NOT_IMPLIED", "C5_PR395_SURFACE_TECH_AUTH")
        need(bool(surface.get("git_blob_sha")) and len(surface.get("git_blob_sha", "")) == 40, "C5_PR395_SURFACE_BLOB")
    need(len(integration.get("explicit_non_imports", [])) >= 6, "C5_PR395_NON_IMPORTS")

    boundary = integration.get("c4_boundary_ref", {})
    need(boundary.get("git_blob_sha") == EXPECTED_C4_BLOB, "C5_C4_PIN")
    need(c4.get("status") == "C4_SUBJECT_ADAPTER_INTERFACE_EXTRACTED", "C5_C4_STATUS")
    need(c4.get("next_stage") == "C5_SUBTOPIC_INTELLIGENCE_LIBRARY_CONTRACTS_READY", "C5_C4_NEXT_STAGE")
    need(c4.get("authority") == "NONE" and c4.get("runtime_migration_authorized") is False, "C5_C4_NON_AUTHORITY")
    tracked = c4.get("tracked_runtime_gap", {})
    need(tracked.get("finding_id") == "C0-F007", "C5_F007_ID")
    need(tracked.get("classification") == "CURRENT + DOCUMENTED ONLY", "C5_F007_CLASS")
    need(tracked.get("runtime_auto_materialization_executable") is False, "C5_F007_EXECUTABLE")
    if check_disk_custody:
        need(git_blob(C4_RECEIPT_PATH) == EXPECTED_C4_BLOB, "C5_C4_BLOB_DRIFT")
        need(git_blob(INTEGRATION_PATH) == catalog.get("integration_manifest", {}).get("git_blob_sha"), "C5_INTEGRATION_BLOB_DRIFT")

    try:
        asset_types = domain_schema["$defs"]["assetType"]["enum"]
    except Exception:
        asset_types = []
    need(len(asset_types) == 13, "C5_CURRENT_MATH_OBJECT_VOCABULARY")
    need("EQUATION" in asset_types and "PROBLEM_FAMILY" in asset_types and "MISCONCEPTION" in asset_types, "C5_MATH_OBJECT_SENTINELS")

    return errors


def load_schemas(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for contract in catalog["contracts"]:
        result[contract["contract_id"]] = load(ROOT / contract["path"])
    return result


def main() -> None:
    catalog = load(CATALOG_PATH)
    integration = load(INTEGRATION_PATH)
    schemas = load_schemas(catalog)
    errors = validate_documents(catalog, integration, schemas, load(C4_RECEIPT_PATH), load(DOMAIN_SCHEMA_PATH))
    if errors:
        print("C5 SIL contract validation: FAIL")
        for code in errors:
            print(f"  - {code}")
        raise SystemExit(1)
    print("C5 SIL contract validation: PASS")
    print(f"  contracts: {len(catalog['contracts'])}")
    print(f"  PR395 candidate surfaces: {len(integration['candidate_surfaces'])}")
    print("  authority: NONE; runtime migration: false; publication authorization: NOT_IMPLIED")


if __name__ == "__main__":
    main()
