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

EXTENSION = json.loads(
    (ROOT.parent / "Representation" / "registry" / "chemistry-electron-transfer-primitive-extension.v1.json").read_text(encoding="utf-8")
)


def electron_transfer_gates():
    rows = []
    for gate in REGISTRY["subtopic_gates"]:
        reps = [row for row in gate.get("representations", []) if row.get("representation_type") == "ELECTRON_TRANSFER_DIAGRAM"]
        if reps:
            rows.append((gate, reps[0]))
    return rows


class ChemistryElectronTransferExtensionTests(unittest.TestCase):
    def test_extension_is_subject_wide_and_renderer_selection_stays_forbidden(self):
        primitive = EXTENSION["primitives"][0]
        self.assertEqual(primitive["primitive_id"], "ELECTRON_TRANSFER_LEDGER")
        self.assertEqual(primitive["topic_scope_refs"], [])
        self.assertFalse(primitive["decorative"])
        self.assertTrue(EXTENSION["renderer_selection_forbidden"])
        self.assertTrue({
            "STATE_VALUES_EXPLICIT",
            "ELECTRON_COUNT_EXPLICIT",
            "LOSS_GAIN_DIRECTION_FROM_STATE_CHANGE",
            "ELECTRON_EXCHANGE_BALANCED",
            "SPECIES_IDENTITY_STABLE",
        }.issubset(set(primitive["renderer_constraints"])))

    def test_registry_contains_multiple_engineering_gates_with_electron_transfer_diagram(self):
        rows = electron_transfer_gates()
        self.assertGreaterEqual(len(rows), 2)
        self.assertGreaterEqual(len({gate["subtopic_id"] for gate, _ in rows}), 2)

    def test_extension_compiles_from_engineering_representation_metadata_without_topic_branch(self):
        gate, engineering_rep = electron_transfer_gates()[0]
        audit_ref = "tests/in-memory-electron-transfer-extension-audit.json"
        audit = make_production_audit(gate)
        packet = compile_blueprint_obligations(
            make_request(),
            make_manifest(gate, audit_ref),
            registry=REGISTRY,
            source_audit_payloads={audit_ref: audit},
        )
        plan = {
            "plan_id": "CHEM-REP-PLAN-ELECTRON-TRANSFER-TEST",
            "representations": [{
                "representation_id": "REP-TEST-ELECTRON-TRANSFER-LEDGER",
                "engineering_representation_refs": [engineering_rep["representation_id"]],
                "capability_ref": "CAP-TRACK-REACTING-SPECIES",
                "primitive_id": "ELECTRON_TRANSFER_LEDGER",
                "chemical_entities": ["A", "A+", "B", "B-"],
                "source_semantic_data": {
                    "chemical_entities": ["A", "A+", "B", "B-"],
                    "oxidation_states": [
                        {"element": "A", "before": 0, "after": 1, "before_species": "A", "after_species": "A+", "electron_count": 1},
                        {"element": "B", "before": 0, "after": -1, "before_species": "B", "after_species": "B-", "electron_count": 1},
                    ],
                    "verification_requirements": ["electrons lost equals electrons gained"],
                },
                "notation_tokens": ["A", "A+", "B", "B-"],
            }],
        }
        bundle, bindings = compile_core_representation_bundle(
            "CORE1A",
            packet,
            plan,
            bundle_id="CHEM-REP-BUNDLE-ELECTRON-TRANSFER-TEST",
        )
        self.assertIn(EXTENSION["extension_id"], bundle["primitive_registry_extension_refs"])
        self.assertEqual(bundle["representations"][0]["primitive_id"], "ELECTRON_TRANSFER_LEDGER")
        self.assertEqual(bindings[0]["engineering_representation_refs"], [engineering_rep["representation_id"]])

    def test_extension_cannot_enable_renderer_selection_or_override_registry(self):
        gate, engineering_rep = electron_transfer_gates()[0]
        audit_ref = "tests/in-memory-electron-transfer-extension-negative.json"
        audit = make_production_audit(gate)
        packet = compile_blueprint_obligations(
            make_request(), make_manifest(gate, audit_ref), registry=REGISTRY, source_audit_payloads={audit_ref: audit}
        )
        plan = {
            "representations": [{
                "representation_id": "REP-TEST-ELECTRON-TRANSFER-NEGATIVE",
                "engineering_representation_refs": [engineering_rep["representation_id"]],
                "capability_ref": "CAP-TRACK-REACTING-SPECIES",
                "primitive_id": "ELECTRON_TRANSFER_LEDGER",
                "source_semantic_data": {"chemical_entities": ["A", "A+"]},
            }]
        }
        bad = copy.deepcopy(EXTENSION)
        bad["renderer_selection_forbidden"] = False
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            compile_core_representation_bundle(
                "CORE1A", packet, plan, representation_extensions=[bad], bundle_id="CHEM-REP-BUNDLE-ELECTRON-TRANSFER-NEGATIVE"
            )
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_EXTENSION_RENDERER_SELECTION_FORBIDDEN")

    def test_generic_extension_path_contains_no_topic_named_branch(self):
        compiler = (ENGINE / "compile_chemistry_core_representation_bundle.py").read_text(encoding="utf-8").lower()
        for forbidden in ("re" + "dox", "mn" + "o4", "perman" + "ganate"):
            self.assertNotIn(forbidden, compiler)


if __name__ == "__main__":
    unittest.main()
