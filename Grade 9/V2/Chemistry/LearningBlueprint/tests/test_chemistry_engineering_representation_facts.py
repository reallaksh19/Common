import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_engineering_representation_facts import (  # noqa: E402
    ChemistryEngineeringRepresentationFactsError,
    compile_engineering_representation_facts,
)
from compile_chemistry_representation_runtime_facts import compile_runtime_fact_authority  # noqa: E402

AUTHORITY_PATH = ROOT / "policies" / "chemistry-engineering-representation-facts.v1.json"
REGISTRY_PATH = ROOT / "policies" / "chemistry-technical-engineering-gates.v1.json"
LOCAL_FACTS_PATH = ROOT.parent / "Representation" / "registry" / "chemistry-electron-transfer-runtime-facts.v1.json"
TARGET_GATE = "CHEM-REDOX-OXIDATION"
TARGET_REP = "REP-CHEM-ELECTRON-TRANSFER-ARROWS"
TARGET_EQ = "EQ-CHEM-REDOX-TRANSFER"
TARGET_PACKET = "CHEM-REP-FACT-ELECTRON-TRANSFER-ARROWS-v1"
TARGET_INSTANCE = "CHEM-SEM-INSTANCE-REDOX-CUO-H2-v1"
AUTHORITY_ID = "CHEM-ENG-REPRESENTATION-FACTS-v1"


def authority():
    return json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))


def registry():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


class ChemistryEngineeringRepresentationFactsTests(unittest.TestCase):
    def test_default_authority_binds_fact_packet_to_exact_engineering_assets(self):
        compiled = compile_engineering_representation_facts()
        self.assertEqual(compiled["status"], "ENGINEERING_REPRESENTATION_FACTS_READY")
        self.assertEqual(compiled["authority_id"], AUTHORITY_ID)
        self.assertTrue(compiled["authority_digest"].startswith("sha256:"))
        self.assertTrue(compiled["registry_digest"].startswith("sha256:"))
        self.assertEqual(compiled["semantic_instance_refs"], [TARGET_INSTANCE])
        self.assertEqual(len(compiled["fact_packets"]), 1)
        packet = compiled["fact_packets"][0]
        self.assertEqual(packet["fact_packet_id"], TARGET_PACKET)
        self.assertEqual(packet["source_gate_id"], TARGET_GATE)
        self.assertEqual(packet["source_representation_ref"], TARGET_REP)
        self.assertEqual(packet["source_equation_refs"], [TARGET_EQ])
        self.assertEqual(packet["source_authority_kind"], "ENGINEERING_OBLIGATION")
        self.assertEqual(packet["source_authority_ref"], AUTHORITY_ID)

    def test_unknown_gate_representation_and_equation_fail_closed(self):
        cases = (
            ("source_gate_id", "CHEM-SYNTH-NOT-A-GATE", "CHEM_ENG_REP_FACT_GATE_MISSING"),
            ("source_representation_ref", "REP-SYNTH-NOT-A-REP", "CHEM_ENG_REP_FACT_REPRESENTATION_UNAUTHORIZED"),
        )
        for field, value, code in cases:
            with self.subTest(field=field):
                bad = authority()
                bad["fact_packets"][0][field] = value
                with self.assertRaises(ChemistryEngineeringRepresentationFactsError) as ctx:
                    compile_engineering_representation_facts(bad)
                self.assertEqual(ctx.exception.code, code)

        bad = authority()
        bad["fact_packets"][0]["source_equation_refs"] = ["EQ-SYNTH-NOT-A-EQUATION"]
        with self.assertRaises(ChemistryEngineeringRepresentationFactsError) as ctx:
            compile_engineering_representation_facts(bad)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_REP_FACT_EQUATION_UNAUTHORIZED")

    def test_chemical_entity_must_match_governed_engineering_equation(self):
        bad = authority()
        bad["fact_packets"][0]["parameters"]["chemical_entities"] = ["synthetic equation drift"]
        with self.assertRaises(ChemistryEngineeringRepresentationFactsError) as ctx:
            compile_engineering_representation_facts(bad)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_REP_FACT_CHEMICAL_ENTITY_DRIFT")

    def test_engineering_fact_kind_is_scientifically_validated_before_downstream_use(self):
        bad = authority()
        bad["fact_packets"][0]["parameters"]["oxidation_states"][1]["electron_count"] = 4
        with self.assertRaises(ChemistryEngineeringRepresentationFactsError) as ctx:
            compile_engineering_representation_facts(bad)
        self.assertEqual(ctx.exception.code, "CHEM_REP_FACT_ELECTRON_EXCHANGE_UNBALANCED")

    def test_engineering_representation_fact_key_cannot_be_ambiguous(self):
        bad = authority()
        duplicate = copy.deepcopy(bad["fact_packets"][0])
        duplicate["fact_packet_id"] = "CHEM-REP-FACT-ELECTRON-TRANSFER-ARROWS-ALT-v1"
        duplicate["semantic_instance_ref"] = "CHEM-SEM-INSTANCE-ENGINEERING-ALT-v1"
        bad["fact_packets"].append(duplicate)
        with self.assertRaises(ChemistryEngineeringRepresentationFactsError) as ctx:
            compile_engineering_representation_facts(bad)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_REP_FACT_REPRESENTATION_AMBIGUOUS")

    def test_c_h_registry_no_longer_contains_engineering_obligation_packets(self):
        local = json.loads(LOCAL_FACTS_PATH.read_text(encoding="utf-8"))
        self.assertTrue(local["fact_packets"])
        self.assertTrue(all(row["source_authority_kind"] == "BLUEPRINT_CONTENT_AUTHORITY" for row in local["fact_packets"]))
        self.assertNotIn(TARGET_PACKET, {row["fact_packet_id"] for row in local["fact_packets"]})
        runtime = compile_runtime_fact_authority()
        packets = runtime["fact_packets_by_representation"][TARGET_REP]
        engineering = next(row for row in packets if row["source_authority_kind"] == "ENGINEERING_OBLIGATION")
        self.assertEqual(engineering["fact_packet_id"], TARGET_PACKET)
        self.assertEqual(engineering["source_authority_ref"], AUTHORITY_ID)
        self.assertEqual(runtime["engineering_authority_ref"], AUTHORITY_ID)

    def test_registry_identity_drift_fails_closed(self):
        bad = authority()
        bad["registry_id"] = "CHEM-SYNTHETIC-REGISTRY"
        with self.assertRaises(ChemistryEngineeringRepresentationFactsError) as ctx:
            compile_engineering_representation_facts(bad, registry=registry())
        self.assertEqual(ctx.exception.code, "CHEM_ENG_REP_FACT_REGISTRY_ID_DRIFT")

    def test_generic_compilers_contain_no_topic_control_flow(self):
        for filename in (
            "compile_chemistry_engineering_representation_facts.py",
            "compile_chemistry_representation_runtime_facts.py",
            "validate_chemistry_representation_fact_packet.py",
        ):
            source = (ENGINE / filename).read_text(encoding="utf-8").lower()
            for forbidden in ("re" + "dox", "thermo" + "dynamics", "perman" + "ganate", "mn" + "o4"):
                self.assertNotIn(forbidden, source, filename)


if __name__ == "__main__":
    unittest.main()
