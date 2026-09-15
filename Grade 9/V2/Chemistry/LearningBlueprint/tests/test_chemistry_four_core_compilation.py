import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
CHEM_ROOT = ROOT.parent
LP_ENGINE = CHEM_ROOT / "LearnerProduct" / "engine"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(LP_ENGINE))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_core_authority import ChemistryCoreAuthorityError, compile_core_authority  # noqa: E402
from compile_chemistry_core_product_custody import ChemistryCoreProductCustodyError, compile_core_product_custody  # noqa: E402
from compile_chemistry_engineering_closure import digest as engineering_digest  # noqa: E402

REGISTRY = json.loads((ROOT / "policies/chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8"))


def transform_ref(row):
    return f"{row['from_mode']}->{row['to_mode']}|{row['target_core_role']}"


def make_production_audit(gate, *, role="PRODUCTION_SOURCE_AUDIT"):
    bindings = []
    for cid in gate["canonical_concept_ids"]:
        bindings.append({"asset_kind":"CONCEPT","asset_ref":cid,"authority_layer_ids":["SRC-TEST-AUTHORITY"],"scope_tier_id":"TEST_TIER","claim_class":"SOURCE_DEFINED","downstream_scope":"TEST_ONLY"})
    for eq in gate["mandatory_equations"]:
        bindings.append({"asset_kind":"EQUATION","asset_ref":eq["equation_id"],"authority_layer_ids":["SRC-TEST-AUTHORITY"],"scope_tier_id":"TEST_TIER","claim_class":"SOURCE_DEFINED","downstream_scope":"TEST_ONLY"})
    for tr in gate["required_transformations"]:
        bindings.append({"asset_kind":"TRANSFORMATION","asset_ref":transform_ref(tr),"authority_layer_ids":["SRC-TEST-AUTHORITY"],"scope_tier_id":"TEST_TIER","claim_class":"SOURCE_DEFINED","downstream_scope":"TEST_ONLY"})
    requirements = [kind for kind, values in (("CONCEPT",gate["canonical_concept_ids"]),("EQUATION",gate["mandatory_equations"]),("TRANSFORMATION",gate["required_transformations"])) if values]
    return {
        "schema_version":"2.0.0","audit_id":"CHEM-SOURCE-AUDIT-FOUR-CORE-TEST","gate_id":gate["subtopic_id"],"base_registry_ref":"policies/chemistry-technical-engineering-gates.v1.json","audit_role":role,
        "effective_provenance":{"authority_class":"SOURCE_DEFINED","source_curricula":["TEST ONLY"],"scope_policy":"TEST_POLICY","source_references":["TEST SOURCE REFERENCE"]},
        "source_layers":[{"layer_id":"SRC-TEST-AUTHORITY","authority_class":"SOURCE_DEFINED","source_ref":"TEST SOURCE REFERENCE","scope":"TEST ONLY","supports":["generic four-core compiler exercise"]}],
        "scope_tiers":[{"tier_id":"TEST_TIER","grade_band":"9","minimum_learner_grade":9,"description":"Test-only generic source-scope tier."}],
        "coverage_requirements":requirements,"asset_bindings":bindings,
        "learner_surface_policy":{"internal_concept_ids_hidden":True,"legacy_internal_ids":[],"forbidden_surface_labels":[],"preferred_surface_language":[]},
        "repair_records":[],"audit_status":"SOURCE_HARDENED"
    }


def make_request():
    return {
        "schema_version":"2.0.0","request_id":"CHEM-ENG-REQ-FOUR-CORE-TEST","subject":"CHEMISTRY",
        "requested_topic":"Generic four core test","requested_scope":"One direct engineering gate",
        "engineering_depth":"STANDARD","requested_action":"DECLARE_DIRECT_GATES",
        "requested_for":["CORE1A","CORE1B","CORE2A","CORE2B","PAL"]
    }


def make_manifest(gate, audit_ref="tests/in-memory-four-core-audit.json"):
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
    return {
        "schema_version":"2.0.0","manifest_id":"CHEM-ENG-MAN-FOUR-CORE-TEST","request_id":"CHEM-ENG-REQ-FOUR-CORE-TEST",
        "scope_kind":"SUBTOPIC","scope_ref":"TEST_ONLY","topic_id":"CHEM-FOUR-CORE-TEST","title":"Generic four core compiler test",
        "registry_ref":"policies/chemistry-technical-engineering-gates.v1.json","required_gate_ids":[gate["subtopic_id"]],
        "optional_gate_ids":[],"out_of_scope_gate_ids":[],"source_audits":[{"gate_id":gate["subtopic_id"],"audit_ref":audit_ref}],
        "external_prerequisite_resolutions":external,"source_item_status":"INDEPENDENT_OF_TECHNICAL_GATE","downstream_consumers":["PAL"]
    }


def bucket():
    return {
        "schema_version":"4.0.0","bucket_id":"TEST-BUCKET","subject":"CHEMISTRY","subtopic_id":"TEST_ONLY","title":"Test bucket",
        "difficulty_badge":"EASY","page_envelope":{"max_pages":5,"is_ceiling_not_quota":True},
        "research":{"mode":"OPTIONAL","research_refs":[],"research_questions":[]},
        "visual_plan":{"visual_jobs":["compare two governed representations"]},
        "decomposition":{"decision":"NOT_NEEDED","sub_subtopic_ids":[]},"realization_modes":["CORE1A","CORE1B"]
    }


def _representation_fixture(gate):
    engineering_refs = [row["representation_id"] for row in gate.get("representations", [])]
    concrete = [f"REP-TEST-CONCRETE-{index:02d}" for index, _ in enumerate(engineering_refs, 1)]
    # A renderable representation fixture is required now that the B-layer test
    # proves physical closure rather than only identifier custody. The synthetic
    # electron-transfer rows are test data; they do not define production authority.
    representations = [
        {
            "representation_id": ref,
            "primitive_id": "ELECTRON_TRANSFER_LEDGER",
            "chemical_entities": ["X", "X⁺", "Y", "Y⁻"],
            "notation_tokens": ["X", "X⁺", "Y", "Y⁻"],
            "source_semantic_data": {
                "chemical_entities": ["X", "X⁺", "Y", "Y⁻"],
                "verification_requirements": ["Check that electron loss equals electron gain."],
                "oxidation_states": [
                    {"element":"X","before":0,"after":1,"before_species":"X","after_species":"X⁺","electron_count":1},
                    {"element":"Y","before":0,"after":-1,"before_species":"Y","after_species":"Y⁻","electron_count":1},
                ],
            },
            "instructional_job": "Track a source-authorized before/after state change and its electron count.",
            "attention_target": "State direction, electron direction and equal exchange.",
            "learner_action_expected": "Compare both rows and verify equal electron exchange.",
            "condition_exception_context": [],
            "species_roles": [],
            "accessibility_text": "Synthetic test ledger with one electron lost and one electron gained.",
        }
        for ref in concrete
    ]
    bundle = {
        "bundle_id": "TEST-REP-BUNDLE",
        "representations": representations,
    }
    bindings = [
        {
            "representation_ref": rep_ref,
            "engineering_representation_refs": [engineering_ref],
        }
        for rep_ref, engineering_ref in zip(concrete, engineering_refs)
    ]
    return concrete, bundle, bindings


def payloads(gate=None):
    gate = gate or REGISTRY["subtopic_gates"][0]
    rep_refs, rep_bundle, bindings = _representation_fixture(gate)
    return {
        "CORE1A": {
            "manuscript":{
                "manuscript_id":"TEST-MANUSCRIPT",
                "buckets":[{
                    "learning_atoms":[{"atom_id":"ATOM-1"}],
                    "teaching_sections":[{"representation_refs":rep_refs}],
                }],
            },
            "representation_bundle":copy.deepcopy(rep_bundle),
            "representation_bindings":copy.deepcopy(bindings),
        },
        "CORE1B": {
            "subject":"CHEMISTRY","delivery_mode":"STATIC","new_chemistry_refs":[],"module_ref":"MODULE-1","title":"Reconstruct the model",
            "instruction_bucket":bucket(),"capability_ref":"CAP-TEST","approved_capability_refs":["CAP-TEST"],
            "problem_family_ref":"PF-TEST","approved_problem_family_refs":["PF-TEST"],
            "used_representation_refs":rep_refs,"approved_representation_refs":rep_refs,
            "representation_bundle":copy.deepcopy(rep_bundle),"representation_bindings":copy.deepcopy(bindings),
            "task_prompt":"Explain the relationship and show the decisive chemical reasoning.",
            "canonical_answer":"The response must preserve the stated chemical identity and apply the governing relationship consistently.",
            "check":"Re-read the givens and independently verify the final relationship.","help_mode":"PROGRESSIVE_FIXED",
            "help":[
                {"level":"H1_ORIENT","text":"Identify exactly what must remain chemically unchanged."},
                {"level":"H2_REPRESENT","text":"Make a compact representation of the entities you need to compare."},
                {"level":"H3_PRINCIPLE","text":"State the governing chemical relationship before manipulating symbols."},
                {"level":"H4_FIRST_MOVE","text":"Apply that relationship to the first stated entity."}
            ],"workspace_lines":5
        },
        "CORE2A": {
            "source_plan":{"items":[{
                "item_id":"ITEM-1",
                "learner_support":{"see_the_idea":{"pre_taught_representation_refs":rep_refs}},
                "core1a_binding":{"h2_evidence_refs":[]},
            }]},"challenge_plan":None,
            "representation_bundle":copy.deepcopy(rep_bundle),
            "representation_bindings":copy.deepcopy(bindings),
        },
        "CORE2B": {
            "subject":"CHEMISTRY","delivery_mode":"STATIC","new_chemistry_refs":[],
            "learner_conditioning":{"schema_version":"4.0.0","mode":"KNOWLEDGE_PERCENT","knowledge_percent":50},
            "selected_item_id":"ITEM-1","legal_core2a_item_ids":["ITEM-1"],"question_mode":"FROZEN_SOURCE_ITEM",
            "source_item":{"item_id":"ITEM-1","source_locator":"Synthetic source used only for compiler testing","stem":"Determine the chemically consistent conclusion from the stated evidence.","canonical_answer":"The conclusion follows from the preserved chemical relationship.","problem_family_ref":"PF-TEST","provenance_class":"SOURCE_CORE2"},
            "used_representation_refs":rep_refs,"approved_representation_refs":rep_refs,
            "representation_bundle":copy.deepcopy(rep_bundle),"representation_bindings":copy.deepcopy(bindings),
            "help_mode":"PROGRESSIVE_FIXED","help":[
                {"level":"H1_ORIENT","text":"State the target before doing any manipulation."},
                {"level":"H2_STRUCTURE","text":"Separate the decisive evidence from descriptive detail."},
                {"level":"H3_REPRESENTATION","text":"Represent the quantities or species that must be compared."},
                {"level":"H4_PRINCIPLE","text":"Write the governing chemical rule in words."},
                {"level":"H5_FIRST_MOVE","text":"Apply the rule to the first piece of evidence."},
                {"level":"H6_PARTIAL_PATH","text":"Carry that result into the remaining comparison."},
                {"level":"H7_FULL_SOLUTION","text":"Complete the reasoning chain without changing the source question."},
                {"level":"H8_VERIFY_REFLECT","text":"Independently verify the conclusion against the original evidence."}
            ],"full_solution":"Apply the governing relationship to each stated entity, preserve identity, and compare the resulting states.",
            "verify_reflect":"Check the conclusion directly against the original evidence and the governing relationship.","workspace_lines":6
        }
    }


def scope_for(authority, audit, audit_ref):
    return {
        "schema_version":"1.0.0","scope_contract_id":f"CHEM-CORE-SCOPE-FOUR-CORE-TEST-{authority['product_mode']}",
        "product_mode":authority["product_mode"],"gate_id":audit["gate_id"],"subtopic_id":authority["subtopic_id"],
        "source_audit_ref":audit_ref,"source_audit_digest":engineering_digest(audit),"learner_grade":9,"program_context":"GRADE_LEVEL",
        "authorized_scope_tiers":["TEST_TIER"],"held_scope_tiers":[],"extension_authority_ref":"","extension_reason":"",
        "scope_unit_assignments":[{**row,"scope_tier":"TEST_TIER"} for row in authority["scope_units"]],
        "held_transformation_guards":[],"status":"CORE_SCOPE_READY"
    }


class ChemistryFourCoreCompilationTests(unittest.TestCase):
    def setUp(self):
        self.gate = REGISTRY["subtopic_gates"][0]
        self.audit_ref = "tests/in-memory-four-core-audit.json"
        self.audit = make_production_audit(self.gate)
        self.request = make_request()
        self.manifest = make_manifest(self.gate, self.audit_ref)
        self.audit_payloads = {self.audit_ref:self.audit}
        self.packet = compile_blueprint_obligations(self.request,self.manifest,registry=REGISTRY,source_audit_payloads=self.audit_payloads)

    def realized_for(self, mode):
        return [row["obligation_id"] for row in self.packet["obligations"] if mode in row["authorized_modes"]]

    def authority_for(self, mode):
        return compile_core_authority(mode,"TEST_ONLY",payloads(self.gate)[mode],self.packet,self.realized_for(mode),authority_id=f"CHEM-CORE-AUTH-FOUR-CORE-TEST-{mode}",payload_ref=f"tests/{mode.lower()}.json")

    def test_engineering_compiles_to_topic_neutral_obligations(self):
        self.assertEqual(self.packet["status"],"BLUEPRINT_OBLIGATIONS_READY")
        self.assertEqual(self.packet["direct_gate_ids"],[self.gate["subtopic_id"]])
        self.assertGreater(self.packet["counts"]["obligation_count"],0)
        kinds = {row["kind"] for row in self.packet["obligations"]}
        self.assertTrue({"CONCEPT","REPRESENTATION","REASONING_STEP","VERIFICATION","DIFFICULTY_PROFILE"}.issubset(kinds))

    def test_all_four_modes_compile_authority_and_current_custody(self):
        for mode in ("CORE1A","CORE1B","CORE2A","CORE2B"):
            authority = self.authority_for(mode)
            self.assertEqual(authority["representation_closure"]["status"], "PASS")
            scope = scope_for(authority,self.audit,self.audit_ref)
            custody = compile_core_product_custody(self.request,self.manifest,self.packet,scope,authority,registry=REGISTRY,source_audit_payloads=self.audit_payloads)
            self.assertEqual(custody["status"],"CORE_PRODUCT_CUSTODY_READY")
            self.assertEqual(custody["product_mode"],mode)

    def test_core1a_required_obligation_cannot_be_dropped(self):
        realized = self.realized_for("CORE1A")
        required = next(row["obligation_id"] for row in self.packet["obligations"] if row["direct"] and "CORE1A" in row["required_realization_modes"])
        with self.assertRaises(ChemistryCoreAuthorityError) as ctx:
            compile_core_authority("CORE1A","TEST_ONLY",payloads(self.gate)["CORE1A"],self.packet,[x for x in realized if x != required],authority_id="CHEM-CORE-AUTH-FOUR-CORE-NEGATIVE",payload_ref="tests/negative.json")
        self.assertEqual(ctx.exception.code,"CHEM_CORE_AUTH_REQUIRED_OBLIGATION_MISSING")

    def test_required_core1a_representation_must_be_used(self):
        payload = payloads(self.gate)["CORE1A"]
        payload["manuscript"]["buckets"][0]["teaching_sections"][0]["representation_refs"] = []
        with self.assertRaises(ChemistryCoreAuthorityError) as ctx:
            compile_core_authority("CORE1A","TEST_ONLY",payload,self.packet,self.realized_for("CORE1A"),authority_id="CHEM-CORE-AUTH-REP-MISSING",payload_ref="tests/rep-missing.json")
        self.assertEqual(ctx.exception.code,"CHEM_CORE_AUTH_REQUIRED_REPRESENTATION_UNREALIZED")

    def test_representation_binding_cannot_expand_engineering_authority(self):
        payload = payloads(self.gate)["CORE1A"]
        payload["representation_bindings"][0]["engineering_representation_refs"] = ["REP-UNAUTHORIZED-TEST"]
        with self.assertRaises(ChemistryCoreAuthorityError) as ctx:
            compile_core_authority("CORE1A","TEST_ONLY",payload,self.packet,self.realized_for("CORE1A"),authority_id="CHEM-CORE-AUTH-REP-UNAUTHORIZED",payload_ref="tests/rep-unauthorized.json")
        self.assertEqual(ctx.exception.code,"CHEM_CORE_AUTH_REPRESENTATION_ASSET_UNAUTHORIZED")

    def test_used_representation_must_have_engineering_binding(self):
        payload = payloads(self.gate)["CORE1B"]
        payload["representation_bindings"] = []
        with self.assertRaises(ChemistryCoreAuthorityError) as ctx:
            compile_core_authority("CORE1B","TEST_ONLY",payload,self.packet,self.realized_for("CORE1B"),authority_id="CHEM-CORE-AUTH-REP-UNBOUND",payload_ref="tests/rep-unbound.json")
        self.assertEqual(ctx.exception.code,"CHEM_CORE_AUTH_REPRESENTATION_USE_UNBOUND")

    def test_stale_obligation_packet_cannot_establish_custody(self):
        authority = self.authority_for("CORE2A")
        scope = scope_for(authority,self.audit,self.audit_ref)
        stale = copy.deepcopy(self.packet); stale["closure_digest"] = "sha256:" + "0"*64
        with self.assertRaises(ChemistryCoreProductCustodyError) as ctx:
            compile_core_product_custody(self.request,self.manifest,stale,scope,authority,registry=REGISTRY,source_audit_payloads=self.audit_payloads)
        self.assertIn(ctx.exception.code,{"CHEM_CORE_CUSTODY_OBLIGATION_DIGEST_MISMATCH","CHEM_CORE_CUSTODY_CLOSURE_DRIFT"})

    def test_stress_audit_cannot_establish_four_core_custody(self):
        stress = make_production_audit(self.gate,role="STRESS_TEST_SOURCE_AUDIT")
        stress_packet = compile_blueprint_obligations(self.request,self.manifest,registry=REGISTRY,source_audit_payloads={self.audit_ref:stress})
        mode = "CORE2A"
        authority = compile_core_authority(mode,"TEST_ONLY",payloads(self.gate)[mode],stress_packet,[row["obligation_id"] for row in stress_packet["obligations"] if mode in row["authorized_modes"]],authority_id="CHEM-CORE-AUTH-STRESS-NEGATIVE",payload_ref="tests/stress.json")
        scope = scope_for(authority,stress,self.audit_ref)
        with self.assertRaises(ChemistryCoreProductCustodyError) as ctx:
            compile_core_product_custody(self.request,self.manifest,stress_packet,scope,authority,registry=REGISTRY,source_audit_payloads={self.audit_ref:stress})
        self.assertEqual(ctx.exception.code,"CHEM_CORE_CUSTODY_SOURCE_AUDIT_NOT_PRODUCTION")

    def test_static_b_modes_render_and_preflight_from_exact_custody(self):
        try:
            from run_chemistry_core_product import run_core_product
        except ModuleNotFoundError as exc:
            if exc.name in {"reportlab", "pymupdf", "fitz"}:
                self.skipTest(f"render dependency not installed in Blueprint-only workflow: {exc.name}")
            raise
        for mode in ("CORE1B","CORE2B"):
            authority = self.authority_for(mode)
            scope = scope_for(authority,self.audit,self.audit_ref)
            custody = compile_core_product_custody(self.request,self.manifest,self.packet,scope,authority,registry=REGISTRY,source_audit_payloads=self.audit_payloads)
            with tempfile.TemporaryDirectory() as td:
                render, preflight = run_core_product(custody,authority,payloads(self.gate)[mode],Path(td))
                self.assertEqual(preflight["status"],"PASS")
                self.assertEqual(render["product_mode"],mode)
                self.assertTrue((Path(td) / render["artifact"]["path"]).exists())
                self.assertEqual(
                    set(preflight["physical_representation_closure"]["physically_realized_representation_refs"]),
                    set(authority["representation_closure"]["used_representation_refs"]),
                )

    def test_generic_compilers_do_not_branch_on_topic_names(self):
        names = [
            "compile_chemistry_blueprint_obligations.py","compile_chemistry_core_authority.py",
            "validate_chemistry_core_source_scope.py","compile_chemistry_core_product_custody.py",
        ]
        for name in names:
            text = (ENGINE / name).read_text(encoding="utf-8").lower()
            self.assertNotIn("redox",text,name)
            self.assertNotIn("mno4",text,name)
            self.assertNotIn("permanganate",text,name)


if __name__ == "__main__":
    unittest.main()
