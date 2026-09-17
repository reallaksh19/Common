#!/usr/bin/env python3
"""Validate C5 SIL contract family, field-level subcontracts, and PR #395 custody.

Design-only proof. Passing this validator does not create subject, technical,
publication, learner, or runtime authority.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
DESIGN = Path(__file__).resolve().parent

FAMILY_PATH = DESIGN / "stem-subtopic-intelligence-contract-family.candidate.json"
FAMILY_SCHEMA_PATH = DESIGN / "stem-subtopic-intelligence-contract-family.candidate.schema.json"
C4_RECEIPT_PATH = DESIGN / "mathematics-subject-adapter-equivalence.receipt.json"
DOMAIN_SCHEMA_PATH = ROOT / "contracts" / "math-canonical-domain-registry.schema.json"
RECEIPT_PATH = DESIGN / "mathematics-c5-sil-contracts.receipt.json"

FIELD_SCHEMAS = {
    "STEM-SIL-SUBTOPIC-PACK": DESIGN / "stem-subtopic-intelligence-pack.candidate.schema.json",
    "STEM-SIL-LEARNING-TRANSITION": DESIGN / "stem-learning-transition.candidate.schema.json",
    "STEM-SIL-SOURCE-SELECTION-PROFILE": DESIGN / "stem-source-selection-profile.candidate.schema.json",
    "STEM-SIL-LIBRARY-GAP": DESIGN / "stem-library-gap.candidate.schema.json",
    "STEM-SIL-COVERAGE-REPORT": DESIGN / "stem-library-coverage-report.candidate.schema.json",
}

EXPECTED_PR395_HEAD = "242878b04787905087060318c14b89b14238f195"
EXPECTED_PR395_ARTIFACTS = {
    "Grade 9/V2/Mathematics/MathBlueprint/SUBTOPIC_INTELLIGENCE_INTAKE_SPECIFICATION.md": "1131a05b8c125a8c253dad37bd0b31990f81a27b",
    "Grade 9/V2/Mathematics/MathBlueprint/engine/validate_subtopic_intelligence_library.py": "af9eff27888618e5b3c769a2d21a3de8d561efe2",
    "Grade 9/V2/Mathematics/MathBlueprint/references/NANO_LEVEL_SUBTOPIC_INTELLIGENCE_RESEARCH.md": "491f7024af886b8b9c31a4e329e5ead29caf1ec0",
    "Grade 9/V2/Mathematics/MathBlueprint/tools/sil_explorer/generate_sil_catalog.py": "59d9c0d67896f7c0d4488576903f543cc9886221",
}
EXPECTED_CONTRACT_IDS = set(FIELD_SCHEMAS)
EXPECTED_DEPENDENCIES = {
    "LOGICAL_DEPENDENCY": ("SUBJECT_ENGINEERING", False),
    "ASSESSMENT_CAPABILITY_DEPENDENCY": ("ASSESSMENT", False),
    "INSTRUCTIONAL_SEQUENCE": ("LEARNING_STRUCTURE", True),
    "REPRESENTATION_BRIDGE": ("LEARNING_STRUCTURE", True),
    "REPAIR_SEQUENCE": ("LEARNING_STRUCTURE", True),
}
EXPECTED_EXACT_REF_FIELDS = {
    "ref",
    "ref_type",
    "subject_id",
    "registry_ref",
    "registry_version_or_digest",
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


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


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
    family: dict[str, Any],
    family_schema: dict[str, Any],
    field_schemas: dict[str, dict[str, Any]],
    c4: dict[str, Any],
    domain_schema: dict[str, Any],
    receipt: dict[str, Any] | None = None,
    check_disk_custody: bool = True,
) -> list[str]:
    errors: list[str] = []

    def need(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        Draft202012Validator.check_schema(family_schema)
        Draft202012Validator(family_schema).validate(family)
    except Exception:
        errors.append("C5_FAMILY_SCHEMA_VALIDATION")

    for schema in field_schemas.values():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception:
            errors.append("C5_FIELD_SCHEMA_INVALID")

    need(family.get("status") == "C5_SUBTOPIC_INTELLIGENCE_CONTRACT_FAMILY_CANDIDATE", "C5_FAMILY_STATUS")
    need(family.get("authority") == "NONE", "C5_FAMILY_AUTHORITY")
    need(family.get("semantic_change") == "NONE", "C5_FAMILY_SEMANTIC_CHANGE")
    need(family.get("runtime_migration_authorized") is False, "C5_RUNTIME_MIGRATION")
    need(family.get("production_consumers_allowed") is False, "C5_PRODUCTION_CONSUMER")
    need(family.get("next_stage") == "C6_MATHEMATICS_SIL_PILOT_READY", "C5_NEXT_STAGE")

    doctrine = family.get("central_doctrine", {})
    need(doctrine.get("pack_may_define_subject_truth") is False, "C5_PACK_SUBJECT_TRUTH")
    need(doctrine.get("exact_authority_resolution_required") is True, "C5_EXACT_AUTHORITY")
    need(doctrine.get("topic_specific_dispatch_forbidden") is True, "C5_TOPIC_DISPATCH")
    need(doctrine.get("learner_state_is_run_specific") is True, "C5_LEARNER_SEPARATION")
    need(doctrine.get("coverage_may_authorize") is False, "C5_COVERAGE_AUTHORITY")

    contract_objects = family.get("contract_objects", [])
    need({x.get("contract_id") for x in contract_objects} == EXPECTED_CONTRACT_IDS, "C5_CONTRACT_SET")
    for item in contract_objects:
        need(item.get("may_inline_subject_truth") is False, "C5_CONTRACT_INLINE_TRUTH")
        need(item.get("may_grant_technical_authority") is False, "C5_CONTRACT_TECH_AUTH")
        need(item.get("may_grant_publication_authority") is False, "C5_CONTRACT_PUBLICATION_AUTH")

    deps = {x.get("dependency_class"): x for x in family.get("dependency_classes", [])}
    need(set(deps) == set(EXPECTED_DEPENDENCIES), "C5_DEPENDENCY_SET")
    for dep_id, (owner, may_define) in EXPECTED_DEPENDENCIES.items():
        row = deps.get(dep_id, {})
        need(row.get("owner_domain") == owner, "C5_DEPENDENCY_OWNER")
        need(row.get("sil_may_define") is may_define, "C5_DEPENDENCY_AUTHORITY")

    exact_ref = family.get("exact_reference_contract", {})
    need(set(exact_ref.get("required_fields", [])) == EXPECTED_EXACT_REF_FIELDS, "C5_EXACT_REF_FIELDS")
    need(exact_ref.get("free_text_may_promote") is False, "C5_FREE_TEXT_PROMOTION")
    need(exact_ref.get("unresolved_ref_action") == "EMIT_GAP_AND_BLOCK_DEPENDENT_CLAIM", "C5_UNRESOLVED_REF_ACTION")

    locks = family.get("compiled_pack_locks", {})
    need(locks.get("view_class") == "COMPILED_SUBTOPIC_INTELLIGENCE_CONTEXT", "C5_PACK_VIEW_CLASS")
    need(locks.get("authority") == "COMPOSITION_OF_BOUND_GOVERNED_REFERENCES", "C5_PACK_AUTHORITY_LOCK")
    need(locks.get("technical_authorization") == "NOT_GRANTED_BY_PACK", "C5_PACK_TECH_LOCK")
    need(locks.get("publication_authorization") == "NOT_IMPLIED", "C5_PACK_PUBLICATION_LOCK")
    need(locks.get("learner_mastery_claim") == "NOT_IMPLIED", "C5_PACK_MASTERY_LOCK")

    pr395 = family.get("pr395_integration", {})
    need(pr395.get("source_pr") == 395, "C5_PR395_NUMBER")
    need(pr395.get("source_head_sha") == EXPECTED_PR395_HEAD, "C5_PR395_HEAD")
    need(pr395.get("import_mode") == "DIGEST_PINNED_CANDIDATE_SOURCE_ONLY", "C5_PR395_IMPORT_MODE")
    need(pr395.get("packet_authority") == "NONE", "C5_PR395_PACKET_AUTHORITY")
    need(pr395.get("direct_runtime_import_allowed") is False, "C5_PR395_RUNTIME_IMPORT")
    need(pr395.get("direct_normative_import_allowed") is False, "C5_PR395_NORMATIVE_IMPORT")
    artifacts = {x.get("path"): x.get("git_blob_sha") for x in pr395.get("source_artifacts", [])}
    need(artifacts == EXPECTED_PR395_ARTIFACTS, "C5_PR395_ARTIFACT_PINS")
    for mapping in pr395.get("layer_mapping", []):
        need(mapping.get("automatic_authority_promotion") is False, "C5_PR395_LAYER_PROMOTION")

    tracked = family.get("tracked_runtime_gap", {})
    need(tracked.get("finding_id") == "C0-F007", "C5_F007_ID")
    need(tracked.get("classification") == "CURRENT + DOCUMENTED ONLY", "C5_F007_CLASS")
    need(tracked.get("runtime_auto_materialization_executable") is False, "C5_F007_EXECUTABLE")

    source_stage = family.get("source_stage", {})
    need(c4.get("status") == source_stage.get("required_status") == "C4_SUBJECT_ADAPTER_INTERFACE_EXTRACTED", "C5_C4_STATUS")
    need(c4.get("next_stage") == source_stage.get("required_next_stage") == "C5_SUBTOPIC_INTELLIGENCE_LIBRARY_CONTRACTS_READY", "C5_C4_NEXT_STAGE")
    need(c4.get("authority") == "NONE" and c4.get("runtime_migration_authorized") is False, "C5_C4_NON_AUTHORITY")

    try:
        asset_types = domain_schema["$defs"]["assetType"]["enum"]
    except Exception:
        asset_types = []
    projection = family.get("mathematics_reference_projection", {})
    need(len(asset_types) == 13, "C5_CURRENT_MATH_OBJECT_COUNT")
    need(projection.get("canonical_object_types") == asset_types, "C5_MATH_PROJECTION_DRIFT")

    pack = field_schemas.get("STEM-SIL-SUBTOPIC-PACK", {})
    pprops = pack.get("properties", {})
    need(pack.get("additionalProperties") is False, "C5_PACK_OPEN_SCHEMA")
    need(pprops.get("view_class", {}).get("const") == locks.get("view_class"), "C5_PACK_SCHEMA_VIEW")
    need(pprops.get("authority", {}).get("const") == locks.get("authority"), "C5_PACK_SCHEMA_AUTHORITY")
    need(pprops.get("technical_authorization", {}).get("const") == locks.get("technical_authorization"), "C5_PACK_SCHEMA_TECH_AUTH")
    need(pprops.get("publication_authorization", {}).get("const") == locks.get("publication_authorization"), "C5_PACK_SCHEMA_PUBLICATION_AUTH")
    need(pprops.get("learner_mastery_claim", {}).get("const") == locks.get("learner_mastery_claim"), "C5_PACK_SCHEMA_MASTERY")
    need(not (property_names(pack) & FORBIDDEN_PACK_PROPERTY_NAMES), "C5_INLINE_SUBJECT_TRUTH_FORBIDDEN")
    pack_ref_required = set(pack.get("$defs", {}).get("exactRef", {}).get("required", []))
    need(pack_ref_required == EXPECTED_EXACT_REF_FIELDS, "C5_PACK_EXACT_REF_FIELDS")

    transition = field_schemas.get("STEM-SIL-LEARNING-TRANSITION", {})
    tprops = transition.get("properties", {})
    need(set(tprops.get("transition_kind", {}).get("enum", [])) == set(EXPECTED_DEPENDENCIES), "C5_TRANSITION_KIND_DRIFT")
    need(bool(transition.get("allOf")), "C5_TRANSITION_CROSS_FIELD_GUARD")

    source = field_schemas.get("STEM-SIL-SOURCE-SELECTION-PROFILE", {})
    sprops = source.get("properties", {})
    need(sprops.get("authority", {}).get("const") == "NONE", "C5_SOURCE_AUTHORITY")
    need(sprops.get("technical_authorization", {}).get("const") == "NOT_IMPLIED", "C5_SOURCE_TECH_AUTH")
    need("why_preferred" in sprops and "known_limitations" in sprops, "C5_SOURCE_RATIONALE")

    gap = field_schemas.get("STEM-SIL-LIBRARY-GAP", {})
    gprops = gap.get("properties", {})
    need("MISSING_SUBJECT_TRUTH" in set(gprops.get("gap_class", {}).get("enum", [])), "C5_GAP_SUBJECT_TRUTH")
    need("ENRICH_ENGINEERING" in set(gprops.get("recommended_action_class", {}).get("enum", [])), "C5_GAP_ENGINEERING_ROUTE")

    coverage = field_schemas.get("STEM-SIL-COVERAGE-REPORT", {})
    cprops = coverage.get("properties", {})
    need(cprops.get("authority", {}).get("const") == "DERIVED_LIBRARY_COVERAGE", "C5_COVERAGE_DERIVED_AUTHORITY")
    need(cprops.get("technical_authorization", {}).get("const") == "NOT_IMPLIED", "C5_COVERAGE_TECH_AUTH")
    need(cprops.get("publication_authorization", {}).get("const") == "NOT_IMPLIED", "C5_COVERAGE_PUBLICATION_AUTH")

    if receipt is not None:
        need(receipt.get("status") == "C5_SUBTOPIC_INTELLIGENCE_LIBRARY_CONTRACTS_INTEGRATED", "C5_RECEIPT_STATUS")
        need(receipt.get("authority") == "NONE", "C5_RECEIPT_AUTHORITY")
        need(receipt.get("runtime_migration_authorized") is False, "C5_RECEIPT_RUNTIME")
        need(receipt.get("next_stage") == "C6_MATHEMATICS_SIL_PILOT_READY", "C5_RECEIPT_NEXT_STAGE")
        if check_disk_custody:
            custody = receipt.get("source_custody", {})
            for key, value in list(custody.items()):
                if not key.endswith("_path"):
                    continue
                sha_key = key[:-5] + "_git_blob_sha"
                expected = custody.get(sha_key)
                if expected:
                    path = ROOT / value if not value.startswith("design/") else ROOT / value
                    need(path.is_file(), "C5_RECEIPT_PATH_MISSING")
                    if path.is_file():
                        need(git_blob(path) == expected, "C5_RECEIPT_BLOB_DRIFT")

    return errors


def load_field_schemas() -> dict[str, dict[str, Any]]:
    return {contract_id: load(path) for contract_id, path in FIELD_SCHEMAS.items()}


def main() -> None:
    family = load(FAMILY_PATH)
    family_schema = load(FAMILY_SCHEMA_PATH)
    fields = load_field_schemas()
    c4 = load(C4_RECEIPT_PATH)
    domain = load(DOMAIN_SCHEMA_PATH)
    receipt = load(RECEIPT_PATH) if RECEIPT_PATH.exists() else None
    errors = validate_documents(family, family_schema, fields, c4, domain, receipt=receipt)
    if errors:
        print("C5 SIL contract validation: FAIL")
        for code in errors:
            print(f"  - {code}")
        raise SystemExit(1)
    print("C5 SIL contract validation: PASS")
    print(f"  family contracts: {len(family['contract_objects'])}")
    print(f"  field schemas: {len(fields)}")
    print(f"  PR395 candidate pins: {len(family['pr395_integration']['source_artifacts'])}")
    print("  runtime migration: false; automatic authority promotion: false")


if __name__ == "__main__":
    main()
