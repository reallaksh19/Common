#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_chemistry_engineering_gates import ChemistryEngineeringGateValidationError, validate as validate_v1
from validate_chemistry_gate_source_audit import ChemistrySourceAuditError, validate as validate_source_audit

ROOT = Path(__file__).resolve().parents[1]


class ChemistryEngineeringGateV2Error(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryEngineeringGateV2Error(code, message)


def load_registry() -> dict:
    return json.loads((ROOT / "policies/chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8"))


def load_redox_source_audit() -> dict:
    return json.loads((ROOT / "policies/chemistry-redox-source-audit.v1.json").read_text(encoding="utf-8"))


def validate(registry: dict) -> list[str]:
    try:
        validated = validate_v1(registry)
    except ChemistryEngineeringGateValidationError as exc:
        fail("CHEM_ENG_REGISTRY_V1_INVALID", f"{exc.code}: {exc.message}")

    if registry.get("schema_version") != "1.0.0":
        fail("CHEM_ENG_REGISTRY_VERSION", "registry schema_version must remain 1.0.0 for Workbench v1")
    if registry.get("registry_id") != "CHEM-G9-11-TECHNICAL-ENGINEERING-GATES-v1":
        fail("CHEM_ENG_REGISTRY_ID", "unexpected canonical registry_id")
    if registry.get("authority") != "CANONICAL_DOMAIN_REGISTRY":
        fail("CHEM_ENG_REGISTRY_AUTHORITY", "registry authority must be CANONICAL_DOMAIN_REGISTRY")
    if registry.get("governing_standard") != "FAIL_CLOSED_ENGINEERING_GATES":
        fail("CHEM_ENG_REGISTRY_STANDARD", "unexpected governing standard")
    if registry.get("maturity") != "ENGINEERING":
        fail("CHEM_ENG_MATURITY_OVERREACH", "registry maturity is engineering-only")

    for gate in registry["subtopic_gates"]:
        gid = gate["subtopic_id"]
        if gate.get("maturity") != "ENGINEERING" or gate["difficulty_profile"].get("maturity") != "ENGINEERING":
            fail("CHEM_ENG_MATURITY_OVERREACH", f"{gid} may not claim empirical/psychometric maturity")
        actual_concepts = {item["concept_id"] for item in gate["technical_core"]}
        if set(gate["canonical_concept_ids"]) != actual_concepts:
            fail("CHEM_ENG_CONCEPT_CUSTODY_MISMATCH", f"{gid} canonical_concept_ids do not equal technical_core IDs")
        if gate["technical_readiness"] == "ENGINEERING_GATE_READY":
            required_nonempty = ["technical_core","representations","reasoning_sequence","misconceptions","mandatory_verifications","problem_families","falsification_cases"]
            for key in required_nonempty:
                if not gate.get(key):
                    fail("CHEM_ENG_READY_CONTENT_INCOMPLETE", f"{gid} READY but {key} is empty")
            false_checks = [k for k, v in gate["release_checklist"].items() if v is not True]
            if false_checks:
                fail("CHEM_ENG_READY_CHECKLIST_CONTRADICTION", f"{gid} READY with false checks {false_checks}")

    # Redox gate v1 overstates Class-X-only provenance. Workbench readiness therefore
    # consumes the explicit source-hardening audit and grade-band custody map.
    try:
        source_result = validate_source_audit(load_redox_source_audit(), registry)
    except ChemistrySourceAuditError as exc:
        fail("CHEM_ENG_SOURCE_AUDIT_INVALID", f"{exc.code}: {exc.message}")
    if source_result.get("audit_status") != "SOURCE_HARDENED":
        fail("CHEM_ENG_SOURCE_AUDIT_NOT_READY", "Redox source audit is not SOURCE_HARDENED")

    return validated


if __name__ == "__main__":
    doc = load_registry()
    ids = validate(doc)
    print(json.dumps({
        "status":"PASS",
        "registry_id":doc["registry_id"],
        "gate_count":len(ids),
        "redox_source_audit":"SOURCE_HARDENED",
        "gates":ids
    }, indent=2))
