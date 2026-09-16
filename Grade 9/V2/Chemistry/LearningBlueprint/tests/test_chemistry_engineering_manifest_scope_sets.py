import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_engineering_closure import ChemistryEngineeringClosureError, compile_closure  # noqa: E402

REGISTRY = json.loads((ROOT / "policies/chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8"))


def request():
    return {
        "schema_version": "2.0.0",
        "request_id": "CHEM-ENG-REQ-SCOPE-SETS-TEST",
        "subject": "CHEMISTRY",
        "requested_topic": "Synthetic gate scope-set test",
        "requested_scope": "Generic manifest semantics only",
        "engineering_depth": "STANDARD",
        "requested_action": "DECLARE_DIRECT_GATES",
        "requested_for": ["CORE1A"],
    }


def manifest(required, optional=None, out_of_scope=None):
    return {
        "schema_version": "2.0.0",
        "manifest_id": "CHEM-ENG-MAN-SCOPE-SETS-TEST",
        "request_id": "CHEM-ENG-REQ-SCOPE-SETS-TEST",
        "scope_kind": "TOPIC",
        "scope_ref": "SCOPE-SETS-TEST",
        "topic_id": "CHEM-SCOPE-SETS-TEST",
        "title": "Synthetic gate scope-set test",
        "registry_ref": "policies/chemistry-technical-engineering-gates.v1.json",
        "required_gate_ids": list(required),
        "optional_gate_ids": list(optional or []),
        "out_of_scope_gate_ids": list(out_of_scope or []),
        "source_audits": [],
        "external_prerequisite_resolutions": [
            {
                "dependency_id": "MATH-BASIC-ARITHMETIC",
                "status": "RESOLVED_BY_AUTHORITY",
                "evidence_ref": "SYNTHETIC_TEST_ONLY",
            }
        ],
        "source_item_status": "INDEPENDENT_OF_TECHNICAL_GATE",
        "downstream_consumers": ["PAL"],
    }


class ChemistryEngineeringManifestScopeSetTests(unittest.TestCase):
    def test_optional_and_out_of_scope_sets_remain_outside_required_closure(self):
        receipt = compile_closure(
            request(),
            manifest(
                ["CHEM-SYM-LITERACY"],
                optional=["CHEM-ION-VALENCY"],
                out_of_scope=["CHEM-FORMULA-CONSTRUCTION"],
            ),
            registry=REGISTRY,
        )
        self.assertEqual(receipt["closure_status"], "READY")
        self.assertEqual(receipt["direct_gate_ids"], ["CHEM-SYM-LITERACY"])
        self.assertEqual(receipt["optional_gate_ids"], ["CHEM-ION-VALENCY"])
        self.assertEqual(receipt["out_of_scope_gate_ids"], ["CHEM-FORMULA-CONSTRUCTION"])
        self.assertNotIn("CHEM-ION-VALENCY", receipt["closure_gate_ids"])
        self.assertNotIn("CHEM-FORMULA-CONSTRUCTION", receipt["closure_gate_ids"])
        self.assertEqual(receipt["counts"]["optional_gate_count"], 1)
        self.assertEqual(receipt["counts"]["out_of_scope_gate_count"], 1)

    def test_scope_sets_must_be_pairwise_disjoint(self):
        bad = manifest(
            ["CHEM-SYM-LITERACY"],
            optional=["CHEM-SYM-LITERACY"],
        )
        with self.assertRaises(ChemistryEngineeringClosureError) as ctx:
            compile_closure(request(), bad, registry=REGISTRY)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_GATE_SCOPE_SET_OVERLAP")

    def test_required_gate_cannot_depend_on_declared_optional_gate(self):
        bad = manifest(
            ["CHEM-ION-VALENCY"],
            optional=["CHEM-SYM-LITERACY"],
        )
        with self.assertRaises(ChemistryEngineeringClosureError) as ctx:
            compile_closure(request(), bad, registry=REGISTRY)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_OPTIONAL_GATE_REQUIRED_BY_CLOSURE")

    def test_required_gate_cannot_depend_on_declared_out_of_scope_gate(self):
        bad = manifest(
            ["CHEM-ION-VALENCY"],
            out_of_scope=["CHEM-SYM-LITERACY"],
        )
        with self.assertRaises(ChemistryEngineeringClosureError) as ctx:
            compile_closure(request(), bad, registry=REGISTRY)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_REQUIRED_DEPENDENCY_OUT_OF_SCOPE")

    def test_optional_or_out_of_scope_gate_must_exist_in_registry(self):
        bad = manifest(
            ["CHEM-SYM-LITERACY"],
            optional=["CHEM-SYNTH-NOT-IN-REGISTRY"],
        )
        with self.assertRaises(ChemistryEngineeringClosureError) as ctx:
            compile_closure(request(), bad, registry=REGISTRY)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_DECLARED_GATE_MISSING")


if __name__ == "__main__":
    unittest.main()
