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
    compile_core_representation_bundle,
    compile_core_representation_intent,
)
from compile_chemistry_representation_runtime_facts import (  # noqa: E402
    ChemistryRepresentationRuntimeFactsError,
    compile_runtime_fact_authority,
    resolve_runtime_fact_parameters,
)
from test_chemistry_four_core_compilation import (  # noqa: E402
    REGISTRY,
    make_manifest,
    make_production_audit,
    make_request,
)

FACTS_PATH = ROOT.parent / "Representation" / "registry" / "chemistry-electron-transfer-runtime-facts.v1.json"
TARGET_REP = "REP-CHEM-ELECTRON-TRANSFER-ARROWS"
TARGET_PRIMITIVE = "ELECTRON_TRANSFER_LEDGER"
TARGET_FACT_KIND = "ELECTRON_TRANSFER_STATE_LEDGER_V1"


def target_gate():
    for gate in REGISTRY["subtopic_gates"]:
        if TARGET_REP in {row.get("representation_id") for row in gate.get("representations", [])}:
            return gate
    raise AssertionError("target governed representation is missing from Engineering registry")


def packet_and_intent():
    gate = target_gate()
    audit_ref = "tests/in-memory-runtime-facts-audit.json"
    packet = compile_blueprint_obligations(
        make_request(),
        make_manifest(gate, audit_ref),
        registry=REGISTRY,
        source_audit_payloads={audit_ref: make_production_audit(gate)},
    )
    intent = compile_core_representation_intent("CORE1A", packet)
    target = next(row for row in intent["intents"] if row["source_representation_ref"] == TARGET_REP)
    return gate, packet, intent, target


class ChemistryRepresentationRuntimeFactsTests(unittest.TestCase):
    def test_source_bound_fact_packet_reaches_runtime_parameters_without_adapter_data(self):
        _, packet, intent, target = packet_and_intent()
        self.assertEqual(target["primitive_id"], TARGET_PRIMITIVE)
        realized = [row["intent_id"] for row in intent["intents"]]
        bundle, _ = compile_core_representation_bundle(
            "CORE1A",
            packet,
            intent,
            realized,
            bundle_id="CHEM-REP-BUNDLE-RUNTIME-FACTS-TEST",
        )
        rep = next(row for row in bundle["representations"] if row["intent_ref"] == target["intent_id"])
        self.assertEqual(rep["runtime_fact_kind"], TARGET_FACT_KIND)
        self.assertEqual(rep["runtime_fact_ref"], "CHEM-REP-FACT-ELECTRON-TRANSFER-ARROWS-v1")
        self.assertEqual(rep["runtime_fact_source_equation_refs"], ["EQ-CHEM-REDOX-TRANSFER"])
        self.assertEqual(len(rep["runtime_parameters"]["oxidation_states"]), 2)
        self.assertEqual(
            sum(row["electron_count"] for row in rep["runtime_parameters"]["oxidation_states"] if row["after"] > row["before"]),
            sum(row["electron_count"] for row in rep["runtime_parameters"]["oxidation_states"] if row["after"] < row["before"]),
        )
        self.assertFalse(bundle["summary"]["adapter_runtime_facts_allowed"])
        self.assertEqual(bundle["summary"]["runtime_fact_count"], 1)

    def test_primitive_requiring_facts_fails_when_asset_fact_packet_is_missing(self):
        _, packet, _, target = packet_and_intent()
        authority = compile_runtime_fact_authority(extensions=[])
        primitive = {"runtime_fact_kind": TARGET_FACT_KIND}
        with self.assertRaises(ChemistryRepresentationRuntimeFactsError) as ctx:
            resolve_runtime_fact_parameters(target, packet, primitive, authority)
        self.assertEqual(ctx.exception.code, "CHEM_REP_RUNTIME_FACTS_REQUIRED")

    def test_runtime_fact_source_equation_must_be_authorized_by_same_gate(self):
        _, packet, _, target = packet_and_intent()
        extension = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
        extension["fact_packets"][0]["source_equation_refs"] = ["EQ-CHEM-NOT-AUTHORIZED"]
        authority = compile_runtime_fact_authority([extension])
        primitive = {"runtime_fact_kind": TARGET_FACT_KIND}
        with self.assertRaises(ChemistryRepresentationRuntimeFactsError) as ctx:
            resolve_runtime_fact_parameters(target, packet, primitive, authority)
        self.assertEqual(ctx.exception.code, "CHEM_REP_RUNTIME_FACT_EQUATION_UNAUTHORIZED")

    def test_unbalanced_governed_electron_counts_fail_before_render(self):
        extension = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
        bad = copy.deepcopy(extension)
        bad["fact_packets"][0]["parameters"]["oxidation_states"][1]["electron_count"] = 4
        with self.assertRaises(ChemistryRepresentationRuntimeFactsError) as ctx:
            compile_runtime_fact_authority([bad])
        self.assertEqual(ctx.exception.code, "CHEM_REP_FACT_ELECTRON_EXCHANGE_UNBALANCED")

    def test_runtime_fact_compiler_contains_no_topic_or_prose_parser_control_flow(self):
        text = (ENGINE / "compile_chemistry_representation_runtime_facts.py").read_text(encoding="utf-8").lower()
        for forbidden in (
            "re" + "dox",
            "perm" + "anganate",
            "mn" + "o4",
            "meaning_of_symbols",
            "re.findall",
            "source_semantic_data",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
