import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
TESTS = ROOT / "tests"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(TESTS))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_representation_intent import (  # noqa: E402
    ChemistryRepresentationIntentError,
    compile_representation_intent,
    validate_representation_intent,
)
from compile_chemistry_semantic_projection import compile_semantic_projection  # noqa: E402
from test_chemistry_unknown_gate_metamorphic import (  # noqa: E402
    manifest,
    registry,
    request,
    synthetic_gate,
)


class ChemistryRepresentationIntentTests(unittest.TestCase):
    def packet_for(self, gate_id="CHEM-SYNTH-REP-ALPHA", suffix="REPALPHA"):
        gate = synthetic_gate(gate_id, suffix, ["MATH-BASIC-ARITHMETIC"])
        req = request(f"CHEM-ENG-REQ-{suffix}")
        man = manifest(req["request_id"], f"CHEM-ENG-MAN-{suffix}", gate["subtopic_id"])
        packet = compile_blueprint_obligations(req, man, registry=registry(gate))
        return gate, packet

    def test_engineering_semantics_and_c_h_authority_compile_intent_without_adapter_payload(self):
        gate, packet = self.packet_for()
        projection = compile_semantic_projection(packet)
        intent = compile_representation_intent("CORE1A", packet, semantic_projection=projection)

        self.assertEqual(intent["status"], "REPRESENTATION_INTENT_READY")
        self.assertEqual(intent["counts"]["authorized_representation_count"], 1)
        self.assertEqual(intent["counts"]["required_representation_count"], 1)
        row = intent["intents"][0]
        engineering = gate["representations"][0]
        self.assertEqual(row["source_representation_ref"], engineering["representation_id"])
        self.assertEqual(row["capability_ref"], "CAP-TRANSLATE-PARTICLE-SYMBOL")
        self.assertEqual(row["primitive_id"], "MACRO_PARTICLE_SYMBOLIC_BRIDGE")
        self.assertEqual(row["scientific_semantics"]["chemistry_encoded"], engineering["chemistry_encoded"])
        self.assertEqual(row["scientific_semantics"]["mandatory_labels"], engineering["mandatory_labels"])
        self.assertIn("REPRESENTATION_REQUIREMENT", row["scientific_semantics"]["semantic_roles"])
        self.assertEqual(row["selection_authority"], "ENGINEERING_REPRESENTATION_TYPE_PLUS_C_H_PAGE_INTENT")

    def test_supplied_intent_cannot_reclassify_or_replace_governed_semantics(self):
        _, packet = self.packet_for()
        projection = compile_semantic_projection(packet)
        intent = compile_representation_intent("CORE1A", packet, semantic_projection=projection)
        tampered = copy.deepcopy(intent)
        tampered["intents"][0]["scientific_semantics"]["chemistry_encoded"] = "Adapter invented replacement meaning."
        from compile_chemistry_representation_intent import digest_without
        tampered["intent_packet_digest"] = digest_without(tampered, "intent_packet_digest")
        with self.assertRaises(ChemistryRepresentationIntentError) as ctx:
            validate_representation_intent(
                "CORE1A", packet, tampered, semantic_projection=projection
            )
        self.assertEqual(ctx.exception.code, "CHEM_REP_INTENT_DRIFT")

    def test_unmapped_representation_type_fails_closed(self):
        gate, _ = self.packet_for("CHEM-SYNTH-REP-UNMAPPED", "REPUNMAPPED")
        gate["representations"][0]["representation_type"] = "SYNTHETIC_NEVER_REGISTERED_TYPE"
        req = request("CHEM-ENG-REQ-REPUNMAPPED2")
        man = manifest(req["request_id"], "CHEM-ENG-MAN-REPUNMAPPED2", gate["subtopic_id"])
        packet = compile_blueprint_obligations(req, man, registry=registry(gate))
        with self.assertRaises(ChemistryRepresentationIntentError) as ctx:
            compile_representation_intent("CORE1A", packet)
        self.assertEqual(ctx.exception.code, "CHEM_REP_INTENT_TYPE_UNMAPPED")

    def test_policy_cannot_authorize_primitive_outside_c_h_page_intent(self):
        _, packet = self.packet_for("CHEM-SYNTH-REP-BAD-POLICY", "REPBADPOLICY")
        from compile_chemistry_representation_intent import load
        policy = load("policies/chemistry-representation-intent.v1.json")
        bad = copy.deepcopy(policy)
        bad["representation_type_rules"]["JOHNSTONE_TRIPLET_DIAGRAM"] = {
            "capability_ref": "CAP-TRANSLATE-PARTICLE-SYMBOL",
            "primitive_id": "CONSERVATION_LEDGER",
        }
        with self.assertRaises(ChemistryRepresentationIntentError) as ctx:
            compile_representation_intent("CORE1A", packet, policy=bad)
        self.assertIn(
            ctx.exception.code,
            {"CHEM_REP_INTENT_POLICY_CAPABILITY_MISMATCH", "CHEM_REP_INTENT_POLICY_PAGE_INTENT_REJECTED"},
        )

    def test_unknown_gate_rename_preserves_representation_intent_structure(self):
        _, alpha_packet = self.packet_for("CHEM-SYNTH-REP-X", "REPX")
        _, beta_packet = self.packet_for("CHEM-SYNTH-REP-Y", "REPY")
        alpha = compile_representation_intent("CORE1A", alpha_packet)
        beta = compile_representation_intent("CORE1A", beta_packet)
        self.assertEqual(
            [
                (
                    row["representation_type"], row["capability_ref"], row["primitive_id"],
                    tuple(row["scientific_semantics"]["semantic_roles"]), row["required_realization"],
                )
                for row in alpha["intents"]
            ],
            [
                (
                    row["representation_type"], row["capability_ref"], row["primitive_id"],
                    tuple(row["scientific_semantics"]["semantic_roles"]), row["required_realization"],
                )
                for row in beta["intents"]
            ],
        )

    def test_generic_bridge_has_no_topic_name_control_flow_or_adapter_plan_input(self):
        text = (ENGINE / "compile_chemistry_representation_intent.py").read_text(encoding="utf-8").lower()
        self.assertNotIn("redox", text)
        self.assertNotIn("permanganate", text)
        self.assertNotIn("mno4", text)
        self.assertNotIn("representation_plan", text)
        self.assertNotIn("source_semantic_data", text)


if __name__ == "__main__":
    unittest.main()
