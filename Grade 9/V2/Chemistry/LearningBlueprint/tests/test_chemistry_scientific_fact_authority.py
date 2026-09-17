import copy
import inspect
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_scientific_fact_authority import (  # noqa: E402
    ChemistryScientificFactAuthorityError,
    compile_scientific_fact_authority,
    digest,
)

AUTHORITY_PATH = ROOT / "policies" / "chemistry-scientific-facts.v1.json"
RETIRED_C_H_PATH = ROOT.parent / "Representation" / "registry" / "chemistry-electron-transfer-runtime-facts.v1.json"


class ChemistryScientificFactAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.authority = json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))

    def test_scientific_facts_are_upstream_and_not_owned_by_representation(self):
        self.assertEqual(self.authority["subject"], "CHEMISTRY")
        self.assertEqual(self.authority["authority_scope"], "ENGINEERING_AND_BLUEPRINT_SCIENTIFIC_FACTS")
        self.assertTrue(self.authority["adapter_authored_facts_forbidden"])
        self.assertFalse(self.authority["representation_layer_owns_scientific_facts"])
        self.assertFalse(RETIRED_C_H_PATH.exists())

        compiled = compile_scientific_fact_authority()
        authority_id = self.authority["authority_id"]
        self.assertEqual(compiled["authority_refs"], [authority_id])
        self.assertEqual(compiled["authority_digests"][authority_id], digest(self.authority))
        self.assertEqual(len(compiled["packet_authority"]), len(self.authority["fact_packets"]))
        for packet in self.authority["fact_packets"]:
            lineage = compiled["packet_authority"][packet["fact_packet_id"]]
            self.assertEqual(lineage["authority_ref"], authority_id)
            self.assertEqual(lineage["authority_digest"], digest(self.authority))

    def test_fact_kind_validation_happens_before_representation_runtime_projection(self):
        bad = copy.deepcopy(self.authority)
        bad["fact_packets"][0]["parameters"]["oxidation_states"][1]["electron_count"] = 4
        with self.assertRaises(ChemistryScientificFactAuthorityError) as ctx:
            compile_scientific_fact_authority([bad])
        self.assertEqual(ctx.exception.code, "CHEM_SCI_FACT_ELECTRON_EXCHANGE_UNBALANCED")

    def test_unknown_fact_kind_fails_closed(self):
        bad = copy.deepcopy(self.authority)
        bad["fact_packets"][0]["fact_kind"] = "SYNTHETIC_UNKNOWN_FACT_V1"
        with self.assertRaises(ChemistryScientificFactAuthorityError) as ctx:
            compile_scientific_fact_authority([bad])
        self.assertEqual(ctx.exception.code, "CHEM_SCI_FACT_KIND_UNSUPPORTED")

    def test_duplicate_packet_or_semantic_instance_fails_closed(self):
        bad_packet = copy.deepcopy(self.authority)
        duplicate = copy.deepcopy(bad_packet["fact_packets"][0])
        duplicate["semantic_instance_ref"] = "CHEM-SEM-INSTANCE-SYNTHETIC-DUPLICATE-v1"
        bad_packet["fact_packets"].append(duplicate)
        with self.assertRaises(ChemistryScientificFactAuthorityError) as ctx:
            compile_scientific_fact_authority([bad_packet])
        self.assertEqual(ctx.exception.code, "CHEM_SCI_FACT_PACKET_DUPLICATE")

        bad_instance = copy.deepcopy(self.authority)
        duplicate = copy.deepcopy(bad_instance["fact_packets"][0])
        duplicate["fact_packet_id"] = "CHEM-REP-FACT-SYNTHETIC-DUPLICATE-v1"
        bad_instance["fact_packets"].append(duplicate)
        with self.assertRaises(ChemistryScientificFactAuthorityError) as ctx:
            compile_scientific_fact_authority([bad_instance])
        self.assertEqual(ctx.exception.code, "CHEM_SCI_FACT_SEMANTIC_INSTANCE_DUPLICATE")

    def test_generic_scientific_fact_compiler_contains_no_topic_control_flow(self):
        source = inspect.getsource(__import__("compile_chemistry_scientific_fact_authority")).lower()
        for forbidden in ("re" + "dox", "thermo" + "dynamics", "perman" + "ganate", "mn" + "o4"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
