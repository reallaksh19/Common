import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
TESTS = ROOT / "tests"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(TESTS))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_core_representation_bundle import (  # noqa: E402
    ChemistryCoreRepresentationError,
    compile_core_representation_bundle,
)
from test_chemistry_four_core_compilation import (  # noqa: E402
    REGISTRY,
    make_manifest,
    make_production_audit,
    make_request,
)


class ChemistryCoreRepresentationBundleTests(unittest.TestCase):
    def setUp(self):
        self.gate = REGISTRY["subtopic_gates"][0]
        self.audit_ref = "tests/in-memory-representation-bundle-audit.json"
        self.audit = make_production_audit(self.gate)
        self.packet = compile_blueprint_obligations(
            make_request(),
            make_manifest(self.gate, self.audit_ref),
            registry=REGISTRY,
            source_audit_payloads={self.audit_ref: self.audit},
        )
        self.engineering_rep = self.gate["representations"][0]["representation_id"]
        self.plan = {
            "plan_id": "CHEM-REP-PLAN-TEST",
            "representations": [{
                "representation_id": "REP-TEST-GOVERNED-01",
                "engineering_representation_refs": [self.engineering_rep],
                "capability_ref": "CAP-READ-FORMULA",
                "primitive_id": "FORMULA_ANATOMY_VIEW",
                "chemical_entities": ["X"],
                "source_semantic_data": {
                    "chemical_entities": ["X"],
                    "verification_requirements": ["Check the notation position before interpreting the symbol."],
                },
                "notation_tokens": ["X"],
                "accessibility_text": "Annotated symbolic representation used only for generic compiler testing.",
            }],
        }

    def compile(self, plan=None):
        return compile_core_representation_bundle(
            "CORE1A",
            self.packet,
            plan or self.plan,
            bundle_id="CHEM-REP-BUNDLE-TEST",
        )

    def test_explicit_plan_compiles_through_existing_c_h_authority(self):
        bundle, bindings = self.compile()
        self.assertEqual(bundle["summary"]["renderer_selection_allowed"], False)
        self.assertEqual(bundle["summary"]["required_engineering_representation_count"], 1)
        self.assertEqual(bundle["representations"][0]["primitive_id"], "FORMULA_ANATOMY_VIEW")
        self.assertEqual(bindings[0]["engineering_representation_refs"], [self.engineering_rep])

    def test_required_engineering_representation_cannot_be_omitted(self):
        bad = {"plan_id": "CHEM-REP-PLAN-EMPTY", "representations": []}
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            self.compile(bad)
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_REQUIRED_ENGINEERING_REPRESENTATION_MISSING")

    def test_plan_cannot_bind_visual_to_unauthorized_engineering_representation(self):
        bad = copy.deepcopy(self.plan)
        bad["representations"][0]["engineering_representation_refs"] = ["REP-ENGINEERING-NOT-AUTHORIZED"]
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            self.compile(bad)
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_ENGINEERING_REF_UNAUTHORIZED")

    def test_primitive_must_be_capability_compatible_and_page_intent_authorized(self):
        bad = copy.deepcopy(self.plan)
        bad["representations"][0]["primitive_id"] = "OXIDATION_STATE_LANE"
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            self.compile(bad)
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_CAPABILITY_PRIMITIVE_MISMATCH")

    def test_generic_representation_compiler_has_no_topic_branch(self):
        text = (ENGINE / "compile_chemistry_core_representation_bundle.py").read_text(encoding="utf-8").lower()
        for forbidden in ("re" + "dox", "mn" + "o4", "perman" + "ganate"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
