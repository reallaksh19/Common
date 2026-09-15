#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import load
from compile_chemistry_product_engineering_custody import (
    ChemistryProductEngineeringCustodyError,
    compile_product_custody,
)
from validate_pal_engineering_ready import (
    ChemistryPALEngineeringError,
    validate_pal_engineering_ready,
)

REQUEST = load("fixtures/engineering-workbench/redox-request.v1.json")
MANIFEST = load("fixtures/engineering-workbench/redox-manifest.v1.json")
CCBOM = load("golden/v7/ccbom-redox.json")
SCOPE = load("fixtures/engineering-workbench/redox-product-source-scope.v1.json")
AUTHORITY = load("golden/v7/core1a-study-note-redox-authority.json")

Draft202012Validator.check_schema(load("contracts/chemistry-product-engineering-custody-v1.schema.json"))
Draft202012Validator.check_schema(load("contracts/chemistry-product-source-scope-v1.schema.json"))

custody = compile_product_custody(REQUEST, MANIFEST, CCBOM, SCOPE, AUTHORITY)
assert custody["status"] == "ENGINEERING_CUSTODY_READY"
assert custody["scope_ref"] == CCBOM["subtopic_id"]
assert custody["ccbom_id"] == CCBOM["ccbom_id"]
assert custody["product_scope_contract_id"] == SCOPE["scope_contract_id"]
assert custody["product_authority_id"] == AUTHORITY["authority_id"]
assert custody["product_scope_contract_digest"].startswith("sha256:")
assert custody["product_authority_digest"].startswith("sha256:")
assert custody["engineering_binding_id"] == "CHEM-ENG-BIND-REDOX-001"
assert custody["engineering_binding_digest"].startswith("sha256:")
assert custody["ccbom_digest"].startswith("sha256:")
assert custody["source_item_status"] == "SOURCE_HELD"
assert len(custody["source_audit_states"]) >= 1

result = validate_pal_engineering_ready(REQUEST, MANIFEST, CCBOM, SCOPE, AUTHORITY, custody)
assert result["status"] == "PASS"
assert result["engineering_binding_digest"] == custody["engineering_binding_digest"]
assert result["closure_digest"] == custody["closure_digest"]
assert result["product_scope_contract_digest"] == custody["product_scope_contract_digest"]
assert result["product_authority_digest"] == custody["product_authority_digest"]

bad_manifest = copy.deepcopy(MANIFEST)
bad_manifest["downstream_consumers"].remove("PAL")
try:
    compile_product_custody(REQUEST, bad_manifest, CCBOM, SCOPE, AUTHORITY)
except ChemistryProductEngineeringCustodyError as exc:
    assert exc.code == "CHEM_PRODUCT_PAL_NOT_AUTHORIZED"
else:
    raise AssertionError("PAL must be explicitly authorized by engineering binding")

bad_ccbom = copy.deepcopy(CCBOM)
bad_ccbom["subtopic_id"] = "REDOX-OTHER"
try:
    compile_product_custody(REQUEST, MANIFEST, bad_ccbom, SCOPE, AUTHORITY)
except ChemistryProductEngineeringCustodyError as exc:
    assert exc.code == "CHEM_PRODUCT_ENGINEERING_SCOPE_MISMATCH"
else:
    raise AssertionError("CCBOM scope drift must fail")

bad_authority = copy.deepcopy(AUTHORITY)
bad_authority["subtopic_id"] = "REDOX-OTHER"
try:
    compile_product_custody(REQUEST, MANIFEST, CCBOM, SCOPE, bad_authority)
except ChemistryProductEngineeringCustodyError as exc:
    assert exc.code == "CHEM_PRODUCT_AUTHORITY_SCOPE_MISMATCH"
else:
    raise AssertionError("product authority scope drift must fail")

for field in [
    "ccbom_digest",
    "product_scope_contract_digest",
    "product_authority_digest",
    "engineering_binding_digest",
    "closure_digest",
    "registry_digest",
]:
    stale = copy.deepcopy(custody)
    stale[field] = "sha256:" + "0" * 64
    try:
        validate_pal_engineering_ready(REQUEST, MANIFEST, CCBOM, SCOPE, AUTHORITY, stale)
    except ChemistryPALEngineeringError as exc:
        assert exc.code == "CHEM_PAL_ENGINEERING_CUSTODY_STALE"
    else:
        raise AssertionError(f"stale {field} must fail")

stale = copy.deepcopy(custody)
stale["source_audit_states"] = []
try:
    validate_pal_engineering_ready(REQUEST, MANIFEST, CCBOM, SCOPE, AUTHORITY, stale)
except ChemistryPALEngineeringError as exc:
    assert exc.code == "CHEM_PAL_ENGINEERING_CUSTODY_STALE"
else:
    raise AssertionError("source-audit custody loss must fail")

changed_scope = copy.deepcopy(SCOPE)
changed_scope["extension_reason"] += " Revalidated after source-scope review."
try:
    validate_pal_engineering_ready(REQUEST, MANIFEST, CCBOM, changed_scope, AUTHORITY, custody)
except ChemistryPALEngineeringError as exc:
    assert exc.code == "CHEM_PAL_ENGINEERING_CUSTODY_STALE"
else:
    raise AssertionError("changed product scope contract must invalidate prior custody")

changed_authority = copy.deepcopy(AUTHORITY)
changed_authority["content_objects"][0]["learner_payload"] += " Track before you label."
try:
    validate_pal_engineering_ready(REQUEST, MANIFEST, CCBOM, SCOPE, changed_authority, custody)
except ChemistryPALEngineeringError as exc:
    assert exc.code == "CHEM_PAL_ENGINEERING_CUSTODY_STALE"
else:
    raise AssertionError("changed product authority must invalidate prior custody")

print("Chemistry Product Engineering Custody: PASS")
