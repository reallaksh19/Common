import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_engineering_authorization_binding import compile_binding  # noqa: E402
from compile_chemistry_engineering_closure import ChemistryEngineeringClosureError, compile_closure, digest  # noqa: E402
from compile_chemistry_engineering_passport import compile_passport  # noqa: E402
from compile_chemistry_product_engineering_custody import ChemistryProductEngineeringCustodyError, compile_product_custody  # noqa: E402
from validate_pal_engineering_ready import validate_pal_engineering_ready  # noqa: E402
from validate_product_source_scope import ChemistryProductSourceScopeError, validate_product_source_scope  # noqa: E402

REGISTRY = json.loads((ROOT / "policies/chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8"))
STRESS_AUDIT = json.loads((ROOT / "stress_tests/redox/source-audit.v2.json").read_text(encoding="utf-8"))


def transform_ref(row):
    return f"{row['from_mode']}->{row['to_mode']}|{row['target_core_role']}"


def make_production_audit(gate):
    bindings = []
    for cid in gate["canonical_concept_ids"]:
        bindings.append({"asset_kind":"CONCEPT","asset_ref":cid,"authority_layer_ids":["SRC-TEST-AUTHORITY"],"scope_tier_id":"TEST_TIER","claim_class":"SOURCE_DEFINED","downstream_scope":"TEST_ONLY source-scope exercise"})
    for eq in gate["mandatory_equations"]:
        bindings.append({"asset_kind":"EQUATION","asset_ref":eq["equation_id"],"authority_layer_ids":["SRC-TEST-AUTHORITY"],"scope_tier_id":"TEST_TIER","claim_class":"SOURCE_DEFINED","downstream_scope":"TEST_ONLY source-scope exercise"})
    for tr in gate["required_transformations"]:
        bindings.append({"asset_kind":"TRANSFORMATION","asset_ref":transform_ref(tr),"authority_layer_ids":["SRC-TEST-AUTHORITY"],"scope_tier_id":"TEST_TIER","claim_class":"SOURCE_DEFINED","downstream_scope":"TEST_ONLY source-scope exercise"})
    requirements = [kind for kind, values in (("CONCEPT",gate["canonical_concept_ids"]),("EQUATION",gate["mandatory_equations"]),("TRANSFORMATION",gate["required_transformations"])) if values]
    return {
        "schema_version":"2.0.0","audit_id":"CHEM-SOURCE-AUDIT-GENERIC-TEST-V2","gate_id":gate["subtopic_id"],"base_registry_ref":"policies/chemistry-technical-engineering-gates.v1.json","audit_role":"PRODUCTION_SOURCE_AUDIT",
        "effective_provenance":{"authority_class":"SOURCE_DEFINED","source_curricula":["TEST ONLY"],"scope_policy":"TEST_POLICY","source_references":["TEST SOURCE REFERENCE"]},
        "source_layers":[{"layer_id":"SRC-TEST-AUTHORITY","authority_class":"SOURCE_DEFINED","source_ref":"TEST SOURCE REFERENCE","scope":"TEST ONLY","supports":["generic validator exercise"]}],
        "scope_tiers":[{"tier_id":"TEST_TIER","grade_band":"9","minimum_learner_grade":9,"description":"Test-only generic source-scope tier."}],
        "coverage_requirements":requirements,"asset_bindings":bindings,
        "learner_surface_policy":{"internal_concept_ids_hidden":True,"legacy_internal_ids":[],"forbidden_surface_labels":[],"preferred_surface_language":[]},
        "repair_records":[],"audit_status":"SOURCE_HARDENED"
    }


def make_request(gate):
    return {"schema_version":"2.0.0","request_id":"CHEM-ENG-REQ-GENERIC-TEST","subject":"CHEMISTRY","requested_topic":"Generic test scope","requested_scope":"One declared direct gate plus derived prerequisites","engineering_depth":"STANDARD","requested_action":"DECLARE_DIRECT_GATES","requested_for":["CDAU","PAL"]}


def make_manifest(gate, audit_ref="tests/in-memory-production-audit.json"):
    external, closure = [], {gate["subtopic_id"]}
    changed = True
    while changed:
        changed = False
        for gid in list(closure):
            row = next((g for g in REGISTRY["subtopic_gates"] if g["subtopic_id"] == gid), None)
            if not row:
                continue
            for prereq in row.get("prerequisite_ids", []):
                if prereq.startswith("CHEM-"):
                    if prereq not in closure:
                        closure.add(prereq); changed = True
                elif prereq not in {x["dependency_id"] for x in external}:
                    external.append({"dependency_id":prereq,"status":"RESOLVED_BY_AUTHORITY","evidence_ref":"TEST_ONLY"})
    return {"schema_version":"2.0.0","manifest_id":"CHEM-ENG-MAN-GENERIC-TEST","request_id":"CHEM-ENG-REQ-GENERIC-TEST","scope_kind":"SUBTOPIC","scope_ref":"TEST_ONLY","topic_id":"CHEM-GENERIC-TEST","title":"Generic Workbench test","registry_ref":"policies/chemistry-technical-engineering-gates.v1.json","required_gate_ids":[gate["subtopic_id"]],"optional_gate_ids":[],"out_of_scope_gate_ids":[],"source_audits":[{"gate_id":gate["subtopic_id"],"audit_ref":audit_ref}],"external_prerequisite_resolutions":external,"source_item_status":"INDEPENDENT_OF_TECHNICAL_GATE","downstream_consumers":["CDAU","PAL"]}


def product_material(audit):
    authority = {"authority_id":"TEST-PRODUCT-AUTHORITY","subtopic_id":"TEST_ONLY","learning_atoms":[{"atom_id":"ATOM-1"}],"content_objects":[]}
    scope = {"schema_version":"2.0.0","scope_contract_id":"CHEM-PRODUCT-SCOPE-GENERIC-TEST","gate_id":audit["gate_id"],"subtopic_id":"TEST_ONLY","source_audit_ref":"tests/in-memory-production-audit.json","source_audit_digest":digest(audit),"learner_grade":9,"program_context":"GRADE_LEVEL","authorized_scope_tiers":["TEST_TIER"],"held_scope_tiers":[],"extension_authority_ref":"","extension_reason":"","learning_atom_scope_assignments":[{"learning_atom_id":"ATOM-1","scope_tier":"TEST_TIER"}],"held_transformation_guards":[],"status":"SCOPE_CONTRACT_READY"}
    ccbom = {"schema_version":"7.0.0","ccbom_id":"CCBOM-GENERIC-TEST","subtopic_id":"TEST_ONLY","registry_ref":"TEST_ONLY","assets":[{"asset_id":"ATOM-1","asset_class":"LEARNING_ATOM","authority_ref":"TEST-PRODUCT-AUTHORITY","core_dispositions":{}}],"coverage_summary":{"mandatory_total":1,"mandatory_closed":1,"unresolved_asset_ids":[]}}
    return authority, scope, ccbom


class ChemistryEngineeringWorkbenchV2Tests(unittest.TestCase):
    def setUp(self):
        self.gate = REGISTRY["subtopic_gates"][0]
        self.audit = make_production_audit(self.gate)
        self.request = make_request(self.gate)
        self.manifest = make_manifest(self.gate)
        self.audit_payloads = {self.manifest["source_audits"][0]["audit_ref"]: self.audit}

    def test_direct_gate_closure_binding_and_passport_are_generic(self):
        receipt = compile_closure(self.request,self.manifest,registry=REGISTRY,source_audit_payloads=self.audit_payloads)
        self.assertEqual(receipt["closure_status"],"READY")
        self.assertEqual(receipt["counts"]["production_source_audit_count"],1)
        self.assertEqual(receipt["counts"]["stress_source_audit_count"],0)
        self.assertEqual(receipt["source_audit_states"][0]["authority_effect"],"SOURCE_SCOPE_EVIDENCE_ONLY")
        self.assertEqual(compile_binding(self.request,self.manifest,registry=REGISTRY,source_audit_payloads=self.audit_payloads)["status"],"ENGINEERING_AUTHORIZED")
        self.assertEqual(compile_passport(self.request,receipt)["technical_state"],"ENGINEERING_READY")

    def test_source_audit_must_be_explicit_not_topic_triggered(self):
        manifest = copy.deepcopy(self.manifest); manifest["source_audits"] = []
        receipt = compile_closure(self.request,manifest,registry=REGISTRY)
        self.assertEqual(receipt["source_audit_states"],[])

    def test_source_audit_outside_closure_fails(self):
        manifest = copy.deepcopy(self.manifest)
        other = REGISTRY["subtopic_gates"][-1]["subtopic_id"]
        manifest["source_audits"] = [{"gate_id":other,"audit_ref":"tests/outside.json"}]
        with self.assertRaises(ChemistryEngineeringClosureError) as ctx:
            compile_closure(self.request,manifest,registry=REGISTRY,source_audit_payloads={"tests/outside.json":self.audit})
        self.assertEqual(ctx.exception.code,"CHEM_ENG_SOURCE_AUDIT_OUTSIDE_CLOSURE")

    def test_research_depth_fails_closed_without_evidence(self):
        request = copy.deepcopy(self.request); request["engineering_depth"] = "RESEARCH"
        receipt = compile_closure(request,self.manifest,registry=REGISTRY,source_audit_payloads=self.audit_payloads)
        self.assertEqual(receipt["closure_status"],"BLOCKED")
        codes = {b["code"] for b in receipt["blockers"]}
        self.assertIn("CHEM_ENG_RESEARCH_DOSSIER_REQUIRED",codes); self.assertIn("CHEM_ENG_CLAIM_LEDGER_REQUIRED",codes)

    def test_request_schema_does_not_claim_auto_discovery(self):
        schema = json.loads((ROOT / "contracts/chemistry-engineering-request.schema.json").read_text(encoding="utf-8"))
        bad = copy.deepcopy(self.request); bad["requested_action"] = "AUTO_DISCOVER"
        with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(bad,schema)

    def test_stress_audit_cannot_authorize_product_scope(self):
        authority = {"subtopic_id":"TEST-SUBTOPIC","learning_atoms":[{"atom_id":"ATOM-1"}],"content_objects":[]}
        scope = {"schema_version":"2.0.0","scope_contract_id":"CHEM-PRODUCT-SCOPE-STRESS-NEGATIVE","gate_id":STRESS_AUDIT["gate_id"],"subtopic_id":"TEST-SUBTOPIC","source_audit_ref":"stress_tests/redox/source-audit.v2.json","source_audit_digest":digest(STRESS_AUDIT),"learner_grade":11,"program_context":"GRADE_LEVEL","authorized_scope_tiers":[x["tier_id"] for x in STRESS_AUDIT["scope_tiers"]],"held_scope_tiers":[],"extension_authority_ref":"","extension_reason":"","learning_atom_scope_assignments":[{"learning_atom_id":"ATOM-1","scope_tier":STRESS_AUDIT["scope_tiers"][0]["tier_id"]}],"held_transformation_guards":[],"status":"SCOPE_CONTRACT_READY"}
        with self.assertRaises(ChemistryProductSourceScopeError) as ctx: validate_product_source_scope(scope,STRESS_AUDIT,authority,REGISTRY)
        self.assertEqual(ctx.exception.code,"CHEM_PRODUCT_SCOPE_STRESS_AUDIT_NOT_AUTHORITY")

    def test_production_audit_authorizes_generic_product_and_pal_custody(self):
        authority, scope, ccbom = product_material(self.audit)
        self.assertEqual(validate_product_source_scope(scope,self.audit,authority,REGISTRY)["status"],"PASS")
        custody = compile_product_custody(self.request,self.manifest,ccbom,scope,authority,registry=REGISTRY,source_audit_payloads=self.audit_payloads)
        self.assertEqual(custody["status"],"ENGINEERING_CUSTODY_READY")
        pal = validate_pal_engineering_ready(self.request,self.manifest,ccbom,scope,authority,custody,registry=REGISTRY,source_audit_payloads=self.audit_payloads)
        self.assertEqual(pal["status"],"PASS")

    def test_stress_audit_cannot_establish_product_custody(self):
        stress_gate = next(g for g in REGISTRY["subtopic_gates"] if g["subtopic_id"] == STRESS_AUDIT["gate_id"])
        request = make_request(stress_gate)
        manifest = make_manifest(stress_gate,"stress_tests/redox/source-audit.v2.json")
        authority = {"authority_id":"TEST-STRESS-AUTHORITY","subtopic_id":"TEST_ONLY","learning_atoms":[{"atom_id":"ATOM-1"}],"content_objects":[]}
        first_tier = STRESS_AUDIT["scope_tiers"][0]["tier_id"]
        scope = {"schema_version":"2.0.0","scope_contract_id":"CHEM-PRODUCT-SCOPE-STRESS-CUSTODY","gate_id":STRESS_AUDIT["gate_id"],"subtopic_id":"TEST_ONLY","source_audit_ref":"stress_tests/redox/source-audit.v2.json","source_audit_digest":digest(STRESS_AUDIT),"learner_grade":11,"program_context":"GRADE_LEVEL","authorized_scope_tiers":[x["tier_id"] for x in STRESS_AUDIT["scope_tiers"]],"held_scope_tiers":[],"extension_authority_ref":"","extension_reason":"","learning_atom_scope_assignments":[{"learning_atom_id":"ATOM-1","scope_tier":first_tier}],"held_transformation_guards":[],"status":"SCOPE_CONTRACT_READY"}
        ccbom = {"schema_version":"7.0.0","ccbom_id":"CCBOM-STRESS-NEGATIVE","subtopic_id":"TEST_ONLY","registry_ref":"TEST_ONLY","assets":[{"asset_id":"ATOM-1","asset_class":"LEARNING_ATOM","authority_ref":"TEST-STRESS-AUTHORITY","core_dispositions":{}}],"coverage_summary":{"mandatory_total":1,"mandatory_closed":1,"unresolved_asset_ids":[]}}
        with self.assertRaises(ChemistryProductEngineeringCustodyError) as ctx:
            compile_product_custody(request,manifest,ccbom,scope,authority,registry=REGISTRY,source_audit_payloads={"stress_tests/redox/source-audit.v2.json":STRESS_AUDIT})
        self.assertEqual(ctx.exception.code,"CHEM_PRODUCT_SOURCE_AUDIT_NOT_PRODUCTION")

    def test_generic_workbench_engines_have_no_redox_branching(self):
        names = ["validate_chemistry_engineering_registry_runtime.py","compile_chemistry_engineering_closure.py","compile_chemistry_engineering_authorization_binding.py","compile_chemistry_engineering_passport.py","validate_product_source_scope.py","compile_chemistry_product_engineering_custody.py","validate_cdau_engineering_ready.py","validate_pal_engineering_ready.py"]
        for name in names:
            text = (ENGINE / name).read_text(encoding="utf-8").lower()
            self.assertNotIn("redox",text,name); self.assertNotIn("mno4",text,name); self.assertNotIn("permanganate",text,name)


if __name__ == "__main__": unittest.main()
