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
LOCAL_AUTHORITY_PATH = ROOT / "golden" / "v7" / "core1a-study-note-redox-authority.json"
TARGET_REP = "REP-CHEM-ELECTRON-TRANSFER-ARROWS"
TARGET_PRIMITIVE = "ELECTRON_TRANSFER_LEDGER"
TARGET_FACT_KIND = "ELECTRON_TRANSFER_STATE_LEDGER_V1"
ENGINEERING_INSTANCE = "CHEM-SEM-INSTANCE-REDOX-CUO-H2-v1"
LOCAL_INSTANCE = "CHEM-SEM-INSTANCE-REDOX-ZN-CU-v1"


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
    def test_engineering_fact_packet_is_default_when_no_local_semantic_authority_is_requested(self):
        _, packet, intent, target = packet_and_intent()
        self.assertEqual(target["primitive_id"], TARGET_PRIMITIVE)
        realized = [row["intent_id"] for row in intent["intents"]]
        bundle, bindings = compile_core_representation_bundle(
            "CORE1A",
            packet,
            intent,
            realized,
            bundle_id="CHEM-REP-BUNDLE-RUNTIME-FACTS-TEST",
        )
        rep = next(row for row in bundle["representations"] if row["intent_ref"] == target["intent_id"])
        self.assertEqual(rep["runtime_fact_kind"], TARGET_FACT_KIND)
        self.assertEqual(rep["runtime_fact_ref"], "CHEM-REP-FACT-ELECTRON-TRANSFER-ARROWS-v1")
        self.assertEqual(rep["semantic_instance_ref"], ENGINEERING_INSTANCE)
        self.assertEqual(rep["runtime_fact_source_authority_kind"], "ENGINEERING_OBLIGATION")
        self.assertEqual(rep["runtime_fact_source_equation_refs"], ["EQ-CHEM-REDOX-TRANSFER"])
        self.assertEqual(len(rep["runtime_parameters"]["oxidation_states"]), 2)
        self.assertEqual(
            sum(row["electron_count"] for row in rep["runtime_parameters"]["oxidation_states"] if row["after"] > row["before"]),
            sum(row["electron_count"] for row in rep["runtime_parameters"]["oxidation_states"] if row["after"] < row["before"]),
        )
        binding = next(row for row in bindings if row["representation_ref"] == rep["representation_id"])
        self.assertEqual(binding["semantic_instance_ref"], ENGINEERING_INSTANCE)
        self.assertFalse(bundle["summary"]["adapter_runtime_facts_allowed"])
        self.assertEqual(bundle["summary"]["runtime_fact_count"], 1)
        self.assertEqual(bundle["summary"]["semantic_instance_count"], 1)

    def test_blueprint_semantic_authority_selects_matching_local_fact_packet_without_adapter_facts(self):
        _, packet, intent, target = packet_and_intent()
        local = json.loads(LOCAL_AUTHORITY_PATH.read_text(encoding="utf-8"))
        authority_ref = local["authority_id"]
        realized = [row["intent_id"] for row in intent["intents"]]
        bundle, bindings = compile_core_representation_bundle(
            "CORE1A",
            packet,
            intent,
            realized,
            semantic_instance_authorities={authority_ref: local},
            semantic_instance_authority_refs=[authority_ref],
            bundle_id="CHEM-REP-BUNDLE-LOCAL-SEMANTIC-INSTANCE-TEST",
        )
        rep = next(row for row in bundle["representations"] if row["intent_ref"] == target["intent_id"])
        self.assertEqual(rep["semantic_instance_ref"], LOCAL_INSTANCE)
        self.assertEqual(rep["runtime_fact_ref"], "CHEM-REP-FACT-ELECTRON-TRANSFER-ZN-CU-v1")
        self.assertEqual(rep["runtime_fact_source_authority_kind"], "BLUEPRINT_CONTENT_AUTHORITY")
        self.assertEqual(rep["runtime_fact_source_authority_ref"], authority_ref)
        self.assertIn("OBJ-ZN-HALF", rep["runtime_fact_source_content_object_refs"])
        self.assertEqual(rep["runtime_parameters"]["oxidation_states"][0]["element"], "Zn")
        binding = next(row for row in bindings if row["representation_ref"] == rep["representation_id"])
        self.assertEqual(binding["semantic_instance_ref"], LOCAL_INSTANCE)
        self.assertEqual(binding["runtime_fact_source_authority_ref"], authority_ref)
        self.assertFalse(bundle["summary"]["adapter_scientific_semantics_allowed"])

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

    def test_blueprint_fact_packet_must_resolve_every_cited_content_object(self):
        _, packet, _, target = packet_and_intent()
        local = json.loads(LOCAL_AUTHORITY_PATH.read_text(encoding="utf-8"))
        authority_ref = local["authority_id"]
        broken = copy.deepcopy(local)
        broken["content_objects"] = [
            row for row in broken["content_objects"] if row["object_id"] != "OBJ-ZN-HALF"
        ]
        authority = compile_runtime_fact_authority()
        primitive = {"runtime_fact_kind": TARGET_FACT_KIND}
        with self.assertRaises(ChemistryRepresentationRuntimeFactsError) as ctx:
            resolve_runtime_fact_parameters(
                target,
                packet,
                primitive,
                authority,
                semantic_instance_authorities={authority_ref: broken},
                semantic_instance_authority_refs=[authority_ref],
            )
        self.assertEqual(ctx.exception.code, "CHEM_REP_RUNTIME_FACT_BLUEPRINT_OBJECT_UNAUTHORIZED")

    def test_multiple_local_fact_packets_for_same_authority_fail_ambiguous(self):
        _, packet, _, target = packet_and_intent()
        local = json.loads(LOCAL_AUTHORITY_PATH.read_text(encoding="utf-8"))
        authority_ref = local["authority_id"]
        extension = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
        duplicate = copy.deepcopy(extension["fact_packets"][1])
        duplicate["fact_packet_id"] = "CHEM-REP-FACT-ELECTRON-TRANSFER-ZN-CU-ALT-v1"
        duplicate["semantic_instance_ref"] = "CHEM-SEM-INSTANCE-REDOX-ZN-CU-ALT-v1"
        extension["fact_packets"].append(duplicate)
        authority = compile_runtime_fact_authority([extension])
        primitive = {"runtime_fact_kind": TARGET_FACT_KIND}
        with self.assertRaises(ChemistryRepresentationRuntimeFactsError) as ctx:
            resolve_runtime_fact_parameters(
                target,
                packet,
                primitive,
                authority,
                semantic_instance_authorities={authority_ref: local},
                semantic_instance_authority_refs=[authority_ref],
            )
        self.assertEqual(ctx.exception.code, "CHEM_REP_RUNTIME_FACT_SEMANTIC_INSTANCE_AMBIGUOUS")

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
