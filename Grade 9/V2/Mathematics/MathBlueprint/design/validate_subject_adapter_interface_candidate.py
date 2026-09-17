from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

DESIGN = Path(__file__).resolve().parent
ROOT = DESIGN.parent
INTERFACE = DESIGN / "stem-subject-adapter-interface.candidate.json"
INTERFACE_SCHEMA = DESIGN / "stem-subject-adapter-interface.candidate.schema.json"
C3_RECEIPT = DESIGN / "mathematics-generated-references.receipt.json"
CATALOG = DESIGN / "mathematics-architecture-catalog.candidate.json"
MATH_DOMAIN_SCHEMA = ROOT / "contracts" / "math-canonical-domain-registry.schema.json"
RECEIPT = DESIGN / "mathematics-subject-adapter-equivalence.receipt.json"
RECEIPT_SCHEMA = DESIGN / "mathematics-subject-adapter-equivalence.receipt.schema.json"

INTERFACE_REL = "design/stem-subject-adapter-interface.candidate.json"
INTERFACE_SCHEMA_REL = "design/stem-subject-adapter-interface.candidate.schema.json"
C3_RECEIPT_REL = "design/mathematics-generated-references.receipt.json"
CATALOG_REL = "design/mathematics-architecture-catalog.candidate.json"
MATH_DOMAIN_SCHEMA_REL = "contracts/math-canonical-domain-registry.schema.json"
VALIDATOR_REL = "design/validate_subject_adapter_interface_candidate.py"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def candidate_violations(
    candidate: dict,
    *,
    schema: dict,
    c3_receipt: dict,
    catalog: dict,
    math_domain_schema: dict,
    require_paths: bool = True,
) -> list[str]:
    violations: list[str] = []

    schema_errors = sorted(
        Draft202012Validator(schema).iter_errors(candidate),
        key=lambda error: list(error.path),
    )
    violations.extend(f"schema: {error.message}" for error in schema_errors)

    if c3_receipt.get("status") != "C3_GENERATED_REFERENCES_COMPLETE":
        violations.append("C4 requires completed C3 generated references")
    if c3_receipt.get("next_stage") != "C4_SUBJECT_ADAPTER_INTERFACE_READY":
        violations.append("C3 has not opened the C4 subject-adapter design gate")
    if c3_receipt.get("authority") != "NONE" or c3_receipt.get("semantic_change") != "NONE":
        violations.append("C4 may consume only non-authoritative semantic-noop C3 evidence")
    if c3_receipt.get("production_consumers_allowed") is not False:
        violations.append("C3 design evidence must remain forbidden to production consumers")

    operations = candidate.get("interface_operations", [])
    operation_ids = [row.get("operation_id") for row in operations]
    if len(operation_ids) != len(set(operation_ids)):
        violations.append("interface operation_id values must be unique")

    generic_text = json.dumps(operations, sort_keys=True).lower()
    for forbidden in ("mathematics", "chemistry", "math-", "topic ==", "subtopic =="):
        if forbidden in generic_text:
            violations.append(f"generic interface operation leaks subject/topic dispatch: {forbidden}")

    core_ids = {
        row["operation_id"]
        for row in operations
        if row.get("requirement") == "CORE" and row.get("operation_id")
    }
    conditional_ids = {
        row["operation_id"]
        for row in operations
        if row.get("requirement") == "CONDITIONAL_SUBJECT_CAPABILITY" and row.get("operation_id")
    }
    if not core_ids:
        violations.append("C4 must expose at least one core subject-adapter operation")

    math_projection = candidate.get("mathematics_projection", {})
    bindings = math_projection.get("operation_bindings", [])
    binding_ids = [row.get("operation_id") for row in bindings]
    if len(binding_ids) != len(set(binding_ids)):
        violations.append("Mathematics operation bindings must be unique by operation_id")
    if set(binding_ids) != core_ids:
        missing = sorted(core_ids - set(binding_ids))
        extra = sorted(set(binding_ids) - core_ids)
        violations.append(f"Mathematics bindings must equal CORE operations; missing={missing}, extra={extra}")
    if conditional_ids & set(binding_ids):
        violations.append("conditional subject capability cannot be silently promoted into Mathematics binding")

    catalog_rows = {row["component_id"]: row for row in catalog.get("components", [])}
    for binding in bindings:
        op_id = binding.get("operation_id", "<missing>")
        component_ids = binding.get("component_ids", [])
        declared_evidence: set[str] = set()
        for component_id in component_ids:
            component = catalog_rows.get(component_id)
            if component is None:
                violations.append(f"{op_id}: unknown C1 component_id: {component_id}")
                continue
            declared_evidence.update(component.get("evidence_paths", []))
        for rel in binding.get("evidence_paths", []):
            if rel not in declared_evidence:
                violations.append(f"{op_id}: evidence path is not declared by referenced C1 component(s): {rel}")
            if require_paths and not (ROOT / rel).exists():
                violations.append(f"{op_id}: missing current evidence path: {rel}")

    object_schema_rel = math_projection.get("canonical_object_schema_path")
    if object_schema_rel != MATH_DOMAIN_SCHEMA_REL:
        violations.append("Mathematics projection must point to the current Canonical Domain Registry schema")
    expected_object_types = math_domain_schema.get("$defs", {}).get("assetType", {}).get("enum", [])
    projected_object_types = math_projection.get("canonical_object_types", [])
    if len(projected_object_types) != len(set(projected_object_types)):
        violations.append("Mathematics canonical object types must be unique")
    if set(projected_object_types) != set(expected_object_types):
        violations.append(
            "Mathematics canonical object types must exactly match current domain registry assetType enum"
        )

    if math_projection.get("runtime_path_unchanged") is not True:
        violations.append("C4 may not claim or require a changed Mathematics runtime path")
    if math_projection.get("validation_weakened") is not False:
        violations.append("C4 may not weaken Mathematics validation")

    chemistry = candidate.get("chemistry_stress_target", {})
    if chemistry.get("authority") != "NONE":
        violations.append("Chemistry stress target cannot claim authority in C4")
    if chemistry.get("runtime_binding_present") is not False:
        violations.append("Chemistry stress target cannot claim a runtime binding in C4")
    if chemistry.get("production_registry_ref") is not None:
        violations.append("C4 must not invent a Chemistry production registry")
    if chemistry.get("production_validator_ref") is not None:
        violations.append("C4 must not invent a Chemistry production validator")
    if "LAB_SAFETY_AUTHORITY" not in chemistry.get("required_subject_specific_controls", []):
        violations.append("Chemistry stress target must reserve explicit laboratory safety authority")
    if "VALIDATE_SUBJECT_SAFETY" not in conditional_ids:
        violations.append("generic interface must expose conditional subject-safety validation")

    tracked = candidate.get("tracked_runtime_gap", {})
    if tracked.get("finding_id") != "C0-F007":
        violations.append("C4 must preserve custody of C0-F007")
    if tracked.get("classification") != "CURRENT + DOCUMENTED ONLY":
        violations.append("C4 must not upgrade C0-F007")
    if tracked.get("runtime_auto_materialization_executable") is not False:
        violations.append("C4 must not make C0-F007 executable")

    return violations


def current_violations() -> list[str]:
    return candidate_violations(
        load_json(INTERFACE),
        schema=load_json(INTERFACE_SCHEMA),
        c3_receipt=load_json(C3_RECEIPT),
        catalog=load_json(CATALOG),
        math_domain_schema=load_json(MATH_DOMAIN_SCHEMA),
    )


def expected_receipt() -> dict:
    candidate = load_json(INTERFACE)
    c3_receipt = load_json(C3_RECEIPT)
    catalog = load_json(CATALOG)
    math_domain_schema = load_json(MATH_DOMAIN_SCHEMA)
    violations = candidate_violations(
        candidate,
        schema=load_json(INTERFACE_SCHEMA),
        c3_receipt=c3_receipt,
        catalog=catalog,
        math_domain_schema=math_domain_schema,
    )
    if violations:
        raise ValueError("C4 subject-adapter candidate violations: " + "; ".join(violations))

    operations = candidate["interface_operations"]
    core_ids = {
        row["operation_id"] for row in operations if row["requirement"] == "CORE"
    }
    conditional_ids = sorted(
        row["operation_id"]
        for row in operations
        if row["requirement"] == "CONDITIONAL_SUBJECT_CAPABILITY"
    )

    return {
        "schema_version": "0.1.0",
        "status": "C4_SUBJECT_ADAPTER_INTERFACE_EXTRACTED",
        "authority": "NONE",
        "semantic_change": "NONE",
        "runtime_migration_authorized": False,
        "production_consumers_allowed": False,
        "equivalence_status": "PASS_DESIGN_PROJECTION_ONLY",
        "mathematics_runtime_path_changed": False,
        "mathematics_validation_weakened": False,
        "mathematics_object_type_count": len(candidate["mathematics_projection"]["canonical_object_types"]),
        "bound_core_operation_count": len(core_ids),
        "conditional_unbound_operation_ids": conditional_ids,
        "chemistry_status": candidate["chemistry_stress_target"]["status"],
        "source_custody": {
            "interface_path": INTERFACE_REL,
            "interface_git_blob_sha": git_blob_sha(INTERFACE),
            "interface_schema_path": INTERFACE_SCHEMA_REL,
            "interface_schema_git_blob_sha": git_blob_sha(INTERFACE_SCHEMA),
            "c3_receipt_path": C3_RECEIPT_REL,
            "c3_receipt_git_blob_sha": git_blob_sha(C3_RECEIPT),
            "catalog_path": CATALOG_REL,
            "catalog_git_blob_sha": git_blob_sha(CATALOG),
            "mathematics_domain_schema_path": MATH_DOMAIN_SCHEMA_REL,
            "mathematics_domain_schema_git_blob_sha": git_blob_sha(MATH_DOMAIN_SCHEMA),
            "validator_path": VALIDATOR_REL,
            "validator_git_blob_sha": git_blob_sha(Path(__file__)),
        },
        "tracked_runtime_gap": {
            "finding_id": "C0-F007",
            "classification": "CURRENT + DOCUMENTED ONLY",
            "runtime_auto_materialization_executable": False,
        },
        "next_stage": "C5_SUBTOPIC_INTELLIGENCE_LIBRARY_CONTRACTS_READY",
    }


def validate_receipt(receipt: dict) -> list[str]:
    errors = sorted(
        Draft202012Validator(load_json(RECEIPT_SCHEMA)).iter_errors(receipt),
        key=lambda error: list(error.path),
    )
    return [f"receipt schema: {error.message}" for error in errors]


def write_receipt() -> None:
    receipt = expected_receipt()
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


def check_receipt() -> None:
    expected = expected_receipt()
    actual = load_json(RECEIPT)
    errors = validate_receipt(actual)
    if errors:
        raise SystemExit("; ".join(errors))
    if actual != expected:
        raise SystemExit("C4 equivalence receipt is stale; run validator with --write")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write_receipt()
    else:
        check_receipt()


if __name__ == "__main__":
    main()
