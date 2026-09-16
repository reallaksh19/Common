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
    _engineering_representation_types,
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
    def packet_for(self, gate_id="CHEM-SYNTH-REP-ALPHA", suffix="REPALPHA", representation_type=None):
        gate = synthetic_gate(gate_id, suffix, ["MATH-BASIC-ARITHMETIC"])
        if representation_type is not None:
            gate["representations"][0]["representation_type"] = representation_type
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
        self.assertEqual(intent["policy_extension_refs"], [])
        row = intent["intents"][0]
        engineering = gate["representations"][0]
        self.assertEqual(row["source_representation_ref"], engineering["representation_id"])
        self.assertEqual(row["capability_ref"], "CAP-TRANSLATE-PARTICLE-SYMBOL")
        self.assertEqual(row["primitive_id"], "MACRO_PARTICLE_SYMBOLIC_BRIDGE")
        self.assertEqual(row["scientific_semantics"]["chemistry_encoded"], engineering["chemistry_encoded"])
        self.assertEqual(row["scientific_semantics"]["mandatory_labels"], engineering["mandatory_labels"])
        self.assertIn("REPRESENTATION_REQUIREMENT", row["scientific_semantics"]["semantic_roles"])
        self.assertEqual(row["selection_authority"], "ENGINEERING_REPRESENTATION_TYPE_PLUS_C_H_PAGE_INTENT")

    def test_base_policy_has_exact_engineering_representation_type_coverage(self):
        from compile_chemistry_representation_intent import load
        policy = load("policies/chemistry-representation-intent.v1.json")
        self.assertEqual(set(policy["representation_type_rules"]), _engineering_representation_types())
        self.assertEqual(len(policy["representation_type_rules"]), 16)

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

    def test_policy_coverage_drift_fails_closed(self):
        _, packet = self.packet_for("CHEM-SYNTH-REP-COVERAGE", "REPCOVERAGE")
        from compile_chemistry_representation_intent import load
        policy = load("policies/chemistry-representation-intent.v1.json")
        missing = copy.deepcopy(policy)
        missing["representation_type_rules"].pop("JOHNSTONE_TRIPLET_DIAGRAM")
        with self.assertRaises(ChemistryRepresentationIntentError) as ctx:
            compile_representation_intent("CORE1A", packet, policy=missing)
        self.assertEqual(ctx.exception.code, "CHEM_REP_INTENT_POLICY_TYPE_COVERAGE")

    def test_valid_engineering_type_without_c_h_support_fails_explicitly(self):
        _, packet = self.packet_for(
            "CHEM-SYNTH-REP-BLOCKED",
            "REPBLOCKED",
            representation_type="BCA_MOLE_TABLE",
        )
        with self.assertRaises(ChemistryRepresentationIntentError) as ctx:
            compile_representation_intent("CORE1A", packet)
        self.assertEqual(ctx.exception.code, "CHEM_REP_INTENT_C_H_SUPPORT_MISSING")
        self.assertIn("BCA_MOLE_TABLE", ctx.exception.message)

    def test_additive_extension_can_resolve_only_a_blocked_engineering_type(self):
        gate, packet = self.packet_for(
            "CHEM-SYNTH-REP-EXTENSION",
            "REPEXTENSION",
            representation_type="BCA_MOLE_TABLE",
        )
        extension = {
            "extension_id": "CHEM-REP-INTENT-EXT-SYNTHETIC-BCA-TEST",
            "schema_version": "1.0.0",
            "subject": "CHEMISTRY",
            "extends_policy": "CHEM-ENGINEERING-REPRESENTATION-INTENT-v1",
            "additive_only": True,
            "representation_type_rules": {
                "BCA_MOLE_TABLE": {
                    "status": "RESOLVED",
                    "capability_ref": "CAP-CHECK-ATOM-CONSERVATION",
                    "primitive_id": "CONSERVATION_LEDGER",
                }
            },
        }
        intent = compile_representation_intent(
            "CORE1A", packet, representation_intent_extensions=[extension]
        )
        row = intent["intents"][0]
        self.assertEqual(row["source_representation_ref"], gate["representations"][0]["representation_id"])
        self.assertEqual(row["primitive_id"], "CONSERVATION_LEDGER")
        self.assertEqual(intent["policy_extension_refs"], [extension["extension_id"]])
        self.assertEqual(
            row["scientific_semantics"]["chemistry_encoded"],
            gate["representations"][0]["chemistry_encoded"],
        )

    def test_extension_cannot_override_already_resolved_type(self):
        _, packet = self.packet_for("CHEM-SYNTH-REP-OVERRIDE", "REPOVERRIDE")
        extension = {
            "extension_id": "CHEM-REP-INTENT-EXT-SYNTHETIC-OVERRIDE-TEST",
            "schema_version": "1.0.0",
            "subject": "CHEMISTRY",
            "extends_policy": "CHEM-ENGINEERING-REPRESENTATION-INTENT-v1",
            "additive_only": True,
            "representation_type_rules": {
                "JOHNSTONE_TRIPLET_DIAGRAM": {
                    "status": "RESOLVED",
                    "capability_ref": "CAP-TRANSLATE-PARTICLE-SYMBOL",
                    "primitive_id": "PARTICLE_MODEL_VIEW",
                }
            },
        }
        with self.assertRaises(ChemistryRepresentationIntentError) as ctx:
            compile_representation_intent(
                "CORE1A", packet, representation_intent_extensions=[extension]
            )
        self.assertEqual(ctx.exception.code, "CHEM_REP_INTENT_EXTENSION_OVERRIDE_FORBIDDEN")

    def test_extension_cannot_introduce_type_outside_engineering_enum(self):
        _, packet = self.packet_for("CHEM-SYNTH-REP-EXT-UNKNOWN", "REPEXTUNKNOWN")
        extension = {
            "extension_id": "CHEM-REP-INTENT-EXT-SYNTHETIC-UNKNOWN-TEST",
            "schema_version": "1.0.0",
            "subject": "CHEMISTRY",
            "extends_policy": "CHEM-ENGINEERING-REPRESENTATION-INTENT-v1",
            "additive_only": True,
            "representation_type_rules": {
                "SYNTHETIC_NOT_AN_ENGINEERING_TYPE": {
                    "status": "RESOLVED",
                    "capability_ref": "CAP-READ-FORMULA",
                    "primitive_id": "FORMULA_ANATOMY_VIEW",
                }
            },
        }
        with self.assertRaises(ChemistryRepresentationIntentError) as ctx:
            compile_representation_intent(
                "CORE1A", packet, representation_intent_extensions=[extension]
            )
        self.assertEqual(ctx.exception.code, "CHEM_REP_INTENT_EXTENSION_TYPE_UNKNOWN")

    def test_policy_cannot_authorize_primitive_outside_c_h_page_intent(self):
        _, packet = self.packet_for("CHEM-SYNTH-REP-BAD-POLICY", "REPBADPOLICY")
        from compile_chemistry_representation_intent import load
        policy = load("policies/chemistry-representation-intent.v1.json")
        bad = copy.deepcopy(policy)
        bad["representation_type_rules"]["JOHNSTONE_TRIPLET_DIAGRAM"] = {
            "status": "RESOLVED",
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
