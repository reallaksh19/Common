#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]

class ChemistrySourceAuditError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message

def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def fail(code: str, message: str):
    raise ChemistrySourceAuditError(code, message)

def validate(audit: dict, registry: dict | None = None) -> dict:
    registry = registry or load(audit.get("base_registry_ref", "policies/chemistry-technical-engineering-gates.v1.json"))
    schema = load("contracts/chemistry-gate-source-audit.schema.json")
    Draft202012Validator.check_schema(schema)
    try:
        Draft202012Validator(schema).validate(audit)
    except ValidationError as exc:
        fail("CHEM_SOURCE_AUDIT_SCHEMA", f"{exc.message} at {list(exc.path)}")

    gate = next((g for g in registry["subtopic_gates"] if g["subtopic_id"] == audit["gate_id"]), None)
    if gate is None:
        fail("CHEM_SOURCE_AUDIT_GATE_MISSING", audit["gate_id"])

    layers = {x["layer_id"]: x for x in audit["source_layers"]}
    required_layers = {
        "SRC-NCERT-X-SCI-REDOX",
        "SRC-NCERT-XI-SYLLABUS-REDOX",
        "SRC-NCERT-XI-EXEMPLAR-REDOX",
        "SRC-STANDARD-REDOX-DERIVATION",
    }
    if not required_layers.issubset(layers):
        fail("CHEM_SOURCE_AUDIT_FORMAL_SOURCE_MISSING", f"missing={sorted(required_layers-set(layers))}")
    if layers["SRC-NCERT-XI-EXEMPLAR-REDOX"]["authority_class"] != "SOURCE_DEFINED":
        fail("CHEM_SOURCE_AUDIT_EXEMPLAR_AUTHORITY", "official NCERT Exemplar corpus must remain SOURCE_DEFINED")
    if layers["SRC-STANDARD-REDOX-DERIVATION"]["authority_class"] != "STANDARD_CHEMISTRY_DERIVED":
        fail("CHEM_SOURCE_AUDIT_DERIVATION_AUTHORITY", "illustrative derived redox equations must remain STANDARD_CHEMISTRY_DERIVED")

    def check_refs(items):
        for item in items:
            missing = set(item["authority_layer_ids"]) - set(layers)
            if missing:
                fail("CHEM_SOURCE_AUDIT_UNRESOLVED_SOURCE_REF", f"{item}: missing {sorted(missing)}")
    check_refs(audit["claim_bindings"]); check_refs(audit["equation_bindings"]); check_refs(audit["transformation_bindings"])

    expected_concepts = set(gate["canonical_concept_ids"])
    bound_concepts = {x["asset_id"] for x in audit["claim_bindings"]}
    if expected_concepts != bound_concepts:
        fail("CHEM_SOURCE_AUDIT_CONCEPT_COVERAGE", f"missing={sorted(expected_concepts-bound_concepts)} extra={sorted(bound_concepts-expected_concepts)}")

    expected_eq = {x["equation_id"] for x in gate["mandatory_equations"]}
    bound_eq = {x["equation_id"] for x in audit["equation_bindings"]}
    if expected_eq != bound_eq:
        fail("CHEM_SOURCE_AUDIT_EQUATION_COVERAGE", f"missing={sorted(expected_eq-bound_eq)} extra={sorted(bound_eq-expected_eq)}")

    concept_map = {x["asset_id"]: x for x in audit["claim_bindings"]}
    for cid in ("CON-CHEM-OIL-RIG", "CON-CHEM-OXIDATION-STATE-RULES", "CON-CHEM-AGENT-INVERSION"):
        if concept_map[cid]["scope_tier"] == "FOUNDATION_G10":
            fail("CHEM_SOURCE_AUDIT_SCOPE_LEAK", f"{cid} cannot be authorized solely as Grade 10 foundation")
    agent = concept_map["CON-CHEM-AGENT-INVERSION"]
    if agent["claim_class"] != "STANDARD_CHEMISTRY_DERIVED" or "SRC-STANDARD-REDOX-DERIVATION" not in agent["authority_layer_ids"]:
        fail("CHEM_SOURCE_AUDIT_DERIVED_CLAIM_CUSTODY", "agent assignment rule must retain standard-derived custody")

    if "CON-CHEM-OIL-RIG" not in audit["learner_surface_policy"]["legacy_internal_ids"] or not audit["learner_surface_policy"]["internal_concept_ids_hidden"]:
        fail("CHEM_SOURCE_AUDIT_LEARNER_JARGON", "legacy OIL-RIG concept ID must remain internal only")
    if "OIL RIG" not in audit["learner_surface_policy"]["forbidden_surface_labels"]:
        fail("CHEM_SOURCE_AUDIT_LEARNER_JARGON", "OIL RIG learner-facing label must be forbidden")

    permanganate = next((x for x in audit["transformation_bindings"] if "MnO4" in x["fingerprint"]), None)
    if permanganate is None or permanganate["scope_tier"] != "EXTENDED_G11":
        fail("CHEM_SOURCE_AUDIT_SCOPE_LEAK", "permanganate half-reaction must be EXTENDED_G11")
    if "SRC-STANDARD-REDOX-DERIVATION" not in permanganate["authority_layer_ids"]:
        fail("CHEM_SOURCE_AUDIT_DERIVED_CLAIM_CUSTODY", "permanganate illustrative half-reaction must retain derived custody")

    cuo = next((x for x in audit["equation_bindings"] if x["equation_id"] == "EQ-CHEM-REDOX-TRANSFER"), None)
    if cuo is None or cuo["scope_tier"] != "FOUNDATION_G10":
        fail("CHEM_SOURCE_AUDIT_FOUNDATION_BINDING", "CuO/H2 equation must retain Class X foundation custody")
    if "SRC-NCERT-X-SCI-REDOX" not in cuo["authority_layer_ids"]:
        fail("CHEM_SOURCE_AUDIT_FOUNDATION_BINDING", "CuO/H2 equation must retain Class X source custody")

    defects = {x["defect_id"] for x in audit["current_gate_defects"]}
    for required_defect in {
        "CHEM-REDOX-DEFECT-PROVENANCE-OVERCLAIM",
        "CHEM-REDOX-DEFECT-GRADE-SCOPE-LEAK",
        "CHEM-REDOX-DEFECT-LEARNER-JARGON",
        "CHEM-REDOX-DEFECT-EXEMPLAR-ATTRIBUTION",
    }:
        if required_defect not in defects:
            fail("CHEM_SOURCE_AUDIT_PROVENANCE_OVERCLAIM_UNRESOLVED", f"required repair record missing: {required_defect}")

    return {
        "status": "PASS",
        "audit_status": audit["audit_status"],
        "gate_id": audit["gate_id"],
        "effective_source_curriculum": audit["effective_provenance"]["source_curriculum"],
        "concept_binding_count": len(bound_concepts),
        "equation_binding_count": len(bound_eq),
        "source_layer_count": len(layers)
    }

def main():
    audit = load(sys.argv[1] if len(sys.argv) > 1 else "policies/chemistry-redox-source-audit.v1.json")
    print(json.dumps(validate(audit), indent=2))

if __name__ == "__main__":
    main()
