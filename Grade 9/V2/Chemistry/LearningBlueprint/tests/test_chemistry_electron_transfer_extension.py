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
    compile_core_representation_intent,
)
from test_chemistry_four_core_compilation import (  # noqa: E402
    REGISTRY,
    make_manifest,
    make_production_audit,
    make_request,
)

REP_ROOT = ROOT.parent / "Representation" / "registry"
EXTENSION = json.loads((REP_ROOT / "chemistry-electron-transfer-primitive-extension.v1.json").read_text(encoding="utf-8"))
INTENT_EXTENSION = json.loads((REP_ROOT / "chemistry-electron-transfer-intent-extension.v1.json").read_text(encoding="utf-8"))
FACTS_EXTENSION = json.loads((REP_ROOT / "chemistry-electron-transfer-runtime-facts.v1.json").read_text(encoding="utf-8"))
FACT_BACKED_REP = "REP-CHEM-ELECTRON-TRANSFER-ARROWS"


def electron_transfer_gates():
    rows = []
    for gate in REGISTRY["subtopic_gates"]:
        reps = [row for row in gate.get("representations", []) if row.get("representation_type") == "ELECTRON_TRANSFER_DIAGRAM"]
        for rep in reps:
            rows.append((gate, rep))
    return rows


def fact_backed_gate():
    return next((gate, rep) for gate, rep in electron_transfer_gates() if rep["representation_id"] == FACT_BACKED_REP)


def packet_for(gate, audit_ref):
    audit = make_production_audit(gate)
    return compile_blueprint_obligations(
        make_request(),
        make_manifest(gate, audit_ref),
        registry=REGISTRY,
        source_audit_payloads={audit_ref: audit},
    )


class ChemistryElectronTransferExtensionTests(unittest.TestCase):
    def test_extension_is_subject_wide_and_renderer_selection_stays_forbidden(self):
        primitive = EXTENSION["primitives"][0]
        self.assertEqual(primitive["primitive_id"], "ELECTRON_TRANSFER_LEDGER")
        self.assertEqual(primitive["topic_scope_refs"], [])
        self.assertFalse(primitive["decorative"])
        self.assertTrue(EXTENSION["renderer_selection_forbidden"])
        self.assertEqual(primitive["runtime_fact_kind"], "ELECTRON_TRANSFER_STATE_LEDGER_V1")
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

    def test_intent_extension_and_runtime_facts_resolve_without_adapter_selection(self):
        gate, engineering_rep = fact_backed_gate()
        packet = packet_for(gate, "tests/in-memory-electron-transfer-extension-audit.json")
        intent = compile_core_representation_intent("CORE1A", packet)
        self.assertEqual(intent["policy_extension_refs"], [INTENT_EXTENSION["extension_id"]])
        target = next(
            row for row in intent["intents"]
            if row["source_representation_ref"] == engineering_rep["representation_id"]
        )
        self.assertEqual(target["primitive_id"], "ELECTRON_TRANSFER_LEDGER")
        self.assertEqual(target["source_representation_ref"], engineering_rep["representation_id"])
        self.assertEqual(target["capability_ref"], "CAP-TRACK-OXIDATION-STATE")

        realized = [row["intent_id"] for row in intent["intents"]]
        bundle, bindings = compile_core_representation_bundle(
            "CORE1A",
            packet,
            intent,
            realized,
            bundle_id="CHEM-REP-BUNDLE-ELECTRON-TRANSFER-TEST",
        )
        realized_target = next(
            row for row in bundle["representations"]
            if row["intent_ref"] == target["intent_id"]
        )
        target_binding = next(
            row for row in bindings
            if row["intent_ref"] == target["intent_id"]
        )
        self.assertIn(EXTENSION["extension_id"], bundle["primitive_registry_extension_refs"])
        self.assertIn(INTENT_EXTENSION["extension_id"], bundle["representation_intent_extension_refs"])
        self.assertIn(FACTS_EXTENSION["extension_id"], bundle["runtime_fact_extension_refs"])
        self.assertEqual(realized_target["primitive_id"], "ELECTRON_TRANSFER_LEDGER")
        self.assertEqual(realized_target["runtime_fact_ref"], FACTS_EXTENSION["fact_packets"][0]["fact_packet_id"])
        self.assertEqual(target_binding["engineering_representation_refs"], [engineering_rep["representation_id"]])
        self.assertFalse(bundle["summary"]["adapter_primitive_selection_allowed"])
        self.assertFalse(bundle["summary"]["adapter_scientific_semantics_allowed"])
        self.assertFalse(bundle["summary"]["adapter_runtime_facts_allowed"])

    def test_same_broad_type_without_asset_fact_packet_fails_closed(self):
        gate, engineering_rep = next(
            (gate, rep) for gate, rep in electron_transfer_gates()
            if rep["representation_id"] != FACT_BACKED_REP
        )
        packet = packet_for(gate, "tests/in-memory-electron-transfer-unbacked-audit.json")
        intent = compile_core_representation_intent("CORE1A", packet)
        target = next(row for row in intent["intents"] if row["source_representation_ref"] == engineering_rep["representation_id"])
        realized = [row["intent_id"] for row in intent["intents"]]
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            compile_core_representation_bundle(
                "CORE1A",
                packet,
                intent,
                realized,
                bundle_id="CHEM-REP-BUNDLE-ELECTRON-TRANSFER-UNBACKED-TEST",
            )
        self.assertEqual(ctx.exception.code, "CHEM_REP_RUNTIME_FACTS_REQUIRED")
        self.assertIn(target["source_representation_ref"], ctx.exception.message)

    def test_primitive_extension_cannot_enable_renderer_selection(self):
        gate, _ = fact_backed_gate()
        packet = packet_for(gate, "tests/in-memory-electron-transfer-extension-negative.json")
        intent = compile_core_representation_intent("CORE1A", packet)
        realized = [row["intent_id"] for row in intent["intents"]]
        bad = copy.deepcopy(EXTENSION)
        bad["renderer_selection_forbidden"] = False
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            compile_core_representation_bundle(
                "CORE1A",
                packet,
                intent,
                realized,
                representation_extensions=[bad],
                bundle_id="CHEM-REP-BUNDLE-ELECTRON-TRANSFER-NEGATIVE",
            )
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_EXTENSION_RENDERER_SELECTION_FORBIDDEN")

    def test_generic_extension_path_contains_no_topic_named_branch_or_adapter_semantics(self):
        compiler = (ENGINE / "compile_chemistry_core_representation_bundle.py").read_text(encoding="utf-8").lower()
        for forbidden in (
            "re" + "dox",
            "mn" + "o4",
            "perman" + "ganate",
            "representation_plan",
            "source_semantic_data",
            "runtime_fact_extensions",
        ):
            self.assertNotIn(forbidden, compiler)


if __name__ == "__main__":
    unittest.main()
