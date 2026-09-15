#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import load
from validate_product_source_scope import (
    ChemistryProductSourceScopeError,
    validate_product_source_scope,
)

SCOPE = load("fixtures/engineering-workbench/redox-product-source-scope.v1.json")
AUDIT = load("policies/chemistry-redox-source-audit.v1.json")
AUTHORITY = load("golden/v7/core1a-study-note-redox-authority.json")

Draft202012Validator.check_schema(load("contracts/chemistry-product-source-scope-v1.schema.json"))

result = validate_product_source_scope(SCOPE, AUDIT, AUTHORITY)
assert result["status"] == "PASS"
assert result["learner_grade"] == 9
assert result["authorized_scope_tiers"] == ["FORMAL_G11", "FOUNDATION_G10"]
assert result["held_scope_tiers"] == ["EXTENDED_G11"]
assert result["learning_atom_count"] == 4
assert result["held_guard_count"] == 1

bad = copy.deepcopy(SCOPE)
bad["learning_atom_scope_assignments"] = bad["learning_atom_scope_assignments"][:-1]
try:
    validate_product_source_scope(bad, AUDIT, AUTHORITY)
except ChemistryProductSourceScopeError as exc:
    assert exc.code == "CHEM_PRODUCT_SCOPE_ASSIGNMENT_INCOMPLETE"
else:
    raise AssertionError("missing learning-atom scope assignment must fail")

bad = copy.deepcopy(SCOPE)
bad["learning_atom_scope_assignments"][0]["scope_tier"] = "EXTENDED_G11"
try:
    validate_product_source_scope(bad, AUDIT, AUTHORITY)
except ChemistryProductSourceScopeError as exc:
    assert exc.code == "CHEM_PRODUCT_SCOPE_UNAUTHORIZED_TIER"
else:
    raise AssertionError("held source tier must not enter product authority")

bad = copy.deepcopy(SCOPE)
bad["extension_authority_ref"] = ""
bad["extension_reason"] = ""
try:
    validate_product_source_scope(bad, AUDIT, AUTHORITY)
except ChemistryProductSourceScopeError as exc:
    assert exc.code == "CHEM_PRODUCT_SCOPE_EXTENSION_AUTHORITY_MISSING"
else:
    raise AssertionError("higher-grade extension must have explicit authority")

bad = copy.deepcopy(SCOPE)
bad["held_transformation_guards"] = []
try:
    validate_product_source_scope(bad, AUDIT, AUTHORITY)
except ChemistryProductSourceScopeError as exc:
    assert exc.code == "CHEM_PRODUCT_SCOPE_HELD_GUARD_INCOMPLETE"
else:
    raise AssertionError("held source transformation must have downstream guard")

leak = copy.deepcopy(AUTHORITY)
leak["content_objects"][0]["learner_payload"] = "Balance MnO4 in an acidic half-reaction before continuing."
try:
    validate_product_source_scope(SCOPE, AUDIT, leak)
except ChemistryProductSourceScopeError as exc:
    assert exc.code == "CHEM_PRODUCT_SCOPE_HELD_CONTENT_LEAK"
else:
    raise AssertionError("EXTENDED_G11 permanganate leakage must fail")

jargon = copy.deepcopy(AUTHORITY)
jargon["content_objects"][0]["learner_payload"] = "Use OIL RIG to decide the change."
try:
    validate_product_source_scope(SCOPE, AUDIT, jargon)
except ChemistryProductSourceScopeError as exc:
    assert exc.code == "CHEM_PRODUCT_SCOPE_LEARNER_JARGON_LEAK"
else:
    raise AssertionError("source-audit learner-surface jargon guard must fail")

print("Chemistry Product Source Scope: PASS")
