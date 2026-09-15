#!/usr/bin/env python3
from __future__ import annotations
import copy, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_chemistry_gate_source_audit import ChemistrySourceAuditError, load, validate

AUDIT = load("policies/chemistry-redox-source-audit.v1.json")
REGISTRY = load("policies/chemistry-technical-engineering-gates.v1.json")

def must_fail(audit, code):
    try:
        validate(audit, REGISTRY)
    except ChemistrySourceAuditError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")

result = validate(AUDIT, REGISTRY)
assert result["status"] == "PASS"
assert result["audit_status"] == "SOURCE_HARDENED"
assert result["concept_binding_count"] == 3
assert result["equation_binding_count"] == 1
assert result["source_layer_count"] == 3

# Preserve schema validity while removing the required formal-authority identity.
bad = copy.deepcopy(AUDIT)
next(x for x in bad["source_layers"] if x["layer_id"] == "SRC-NCERT-XI-SYLLABUS-REDOX")["layer_id"] = "SRC-NCERT-XI-SYLLABUS-OTHER"
must_fail(bad, "CHEM_SOURCE_AUDIT_FORMAL_SOURCE_MISSING")

bad = copy.deepcopy(AUDIT)
next(x for x in bad["claim_bindings"] if x["asset_id"] == "CON-CHEM-OXIDATION-STATE-RULES")["scope_tier"] = "FOUNDATION_G10"
must_fail(bad, "CHEM_SOURCE_AUDIT_SCOPE_LEAK")

bad = copy.deepcopy(AUDIT)
bad["equation_bindings"] = []
must_fail(bad, "CHEM_SOURCE_AUDIT_SCHEMA")

bad = copy.deepcopy(AUDIT)
bad["learner_surface_policy"]["forbidden_surface_labels"] = ["agent inversion"]
must_fail(bad, "CHEM_SOURCE_AUDIT_LEARNER_JARGON")

bad = copy.deepcopy(AUDIT)
next(x for x in bad["transformation_bindings"] if "MnO4" in x["fingerprint"])["scope_tier"] = "FOUNDATION_G10"
must_fail(bad, "CHEM_SOURCE_AUDIT_SCOPE_LEAK")

bad = copy.deepcopy(AUDIT)
bad["current_gate_defects"] = [x for x in bad["current_gate_defects"] if x["defect_id"] != "CHEM-REDOX-DEFECT-PROVENANCE-OVERCLAIM"]
must_fail(bad, "CHEM_SOURCE_AUDIT_PROVENANCE_OVERCLAIM_UNRESOLVED")

print("Chemistry Redox source hardening: PASS")
