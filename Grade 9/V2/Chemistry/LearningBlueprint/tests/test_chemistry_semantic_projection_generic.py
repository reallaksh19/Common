import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_semantic_projection import (  # noqa: E402
    ChemistrySemanticProjectionError,
    compile_semantic_projection,
    digest_without,
    validate_semantic_projection,
)


MODES = ["CORE1A", "CORE1B", "CORE2A", "CORE2B"]


def _obligation(index, kind, payload, *, gate_id="CHEM-SYNTH-ALPHA", asset_ref=None):
    return {
        "obligation_id": f"CHEM-OBL-SYNTH-{index:02d}",
        "gate_id": gate_id,
        "direct": True,
        "kind": kind,
        "asset_ref": asset_ref or f"SYNTH-ASSET-{index:02d}",
        "authorized_modes": list(MODES),
        "required_realization_modes": ["CORE1A"],
        "source_authority_tier": "SOURCE-DEFINED",
        "payload": payload,
    }


def make_packet(*, gate_id="CHEM-SYNTH-ALPHA"):
    obligations = [
        _obligation(1, "CONCEPT", {
            "canonical_statement": "Synthetic concept rule alpha.",
        }, gate_id=gate_id),
        _obligation(2, "EQUATION", {
            "formula": "A + B -> C",
            "conditions_of_validity": "Use only when the synthetic condition holds.",
        }, gate_id=gate_id),
        _obligation(3, "REPRESENTATION", {
            "chemistry_encoded": "Synthetic before/after relationship.",
            "verification_method": "Check the represented relationship against the stated evidence.",
        }, gate_id=gate_id),
        _obligation(4, "MODEL_CONDITION", {
            "condition": "Synthetic model condition.",
            "what_changes_if_violated": "The synthetic model no longer applies.",
        }, gate_id=gate_id),
        _obligation(5, "REASONING_STEP", {
            "expert_action": "Compare the stated entities before drawing a conclusion.",
        }, gate_id=gate_id),
        _obligation(6, "TRANSFORMATION", {
            "description": "Transform the stated evidence into the governed relationship.",
        }, gate_id=gate_id),
        _obligation(7, "MISCONCEPTION", {
            "incorrect_belief": "The synthetic relationship may be reversed without evidence.",
            "required_counterexample": "A counterexample where reversing the relationship contradicts the evidence.",
            "required_technical_repair": "Preserve the direction established by the evidence.",
        }, gate_id=gate_id),
        _obligation(8, "VERIFICATION", {
            "statement": "Verify the conclusion independently against the original evidence.",
        }, gate_id=gate_id),
        _obligation(9, "PROBLEM_FAMILY", {
            "family_id": "PF-CHEM-SYNTH",
            "name": "Synthetic governed relationship",
            "recognition_cues": "A governed relationship must be identified before solving.",
            "first_technical_move": "Write the governing relationship explicitly.",
            "common_fatal_error": "Reverse the governing relationship before checking the evidence.",
            "typical_unknown": "The chemically consistent conclusion.",
        }, gate_id=gate_id),
        _obligation(10, "DIFFICULTY_PROFILE", {
            "difficulty_basis": "Synthetic multi-step dependency used only to test the generic projection contract.",
        }, gate_id=gate_id),
    ]
    packet = {
        "schema_version": "1.0.0",
        "packet_id": "CHEM-BP-OBL-SYNTHETIC",
        "subject": "CHEMISTRY",
        "request_id": "CHEM-ENG-REQ-SYNTHETIC",
        "manifest_id": "CHEM-ENG-MAN-SYNTHETIC",
        "scope_ref": "SYNTHETIC",
        "engineering_binding_id": "CHEM-ENG-BIND-SYNTHETIC",
        "engineering_binding_digest": "sha256:" + "1" * 64,
        "closure_receipt_id": "CHEM-ENG-CLOSURE-SYNTHETIC",
        "closure_digest": "sha256:" + "2" * 64,
        "registry_ref": "policies/chemistry-technical-engineering-gates.v1.json",
        "registry_digest": "sha256:" + "3" * 64,
        "direct_gate_ids": [gate_id],
        "closure_gate_ids": [gate_id],
        "obligations": obligations,
        "counts": {
            "gate_count": 1,
            "direct_gate_count": 1,
            "obligation_count": len(obligations),
            "required_by_mode": {
                "CORE1A": len(obligations),
                "CORE1B": 0,
                "CORE2A": 0,
                "CORE2B": 0,
            },
        },
        "status": "BLUEPRINT_OBLIGATIONS_READY",
        "packet_digest": "",
    }
    packet["packet_digest"] = digest_without(packet, "packet_digest")
    return packet


class ChemistrySemanticProjectionGenericTests(unittest.TestCase):
    def test_all_engineering_kinds_project_to_typed_roles(self):
        projection = compile_semantic_projection(make_packet())
        roles = {row["semantic_role"] for row in projection["semantic_atoms"]}
        expected = {
            "CONCEPT_RULE",
            "EQUATION_MODEL",
            "VALIDITY_BOUNDARY",
            "REPRESENTATION_REQUIREMENT",
            "VERIFICATION",
            "BOUNDARY_CONSEQUENCE",
            "REASONING_MOVE",
            "TRANSFORMATION_REQUIREMENT",
            "MISCONCEPTION",
            "COUNTEREXAMPLE",
            "MISCONCEPTION_REPAIR",
            "RECOGNITION_SIGNAL",
            "METHOD_STEP",
            "ERROR_TO_AVOID",
            "TARGET_UNKNOWN",
            "DIFFICULTY_EVIDENCE",
        }
        self.assertTrue(expected.issubset(roles))
        self.assertEqual(projection["status"], "SEMANTIC_PROJECTION_READY")
        self.assertEqual(validate_semantic_projection(make_packet(), projection)["status"], "PASS")

    def test_problem_family_positive_and_negative_semantics_cannot_collapse(self):
        packet = make_packet()
        projection = compile_semantic_projection(packet)
        first_move = "Write the governing relationship explicitly."
        fatal_error = "Reverse the governing relationship before checking the evidence."
        methods = [row["content"] for row in projection["semantic_atoms"] if row["semantic_role"] == "METHOD_STEP"]
        errors = [row["content"] for row in projection["semantic_atoms"] if row["semantic_role"] == "ERROR_TO_AVOID"]
        self.assertIn(first_move, methods)
        self.assertNotIn(fatal_error, methods)
        self.assertIn(fatal_error, errors)

        tampered = copy.deepcopy(projection)
        fatal_atom = next(row for row in tampered["semantic_atoms"] if row["semantic_role"] == "ERROR_TO_AVOID")
        fatal_atom["semantic_role"] = "METHOD_STEP"
        tampered["projection_digest"] = digest_without(tampered, "projection_digest")
        with self.assertRaises(ChemistrySemanticProjectionError) as ctx:
            validate_semantic_projection(packet, tampered)
        self.assertEqual(ctx.exception.code, "CHEM_SEMANTIC_PROJECTION_DRIFT")

    def test_missing_required_source_field_fails_closed(self):
        packet = make_packet()
        family = next(row for row in packet["obligations"] if row["kind"] == "PROBLEM_FAMILY")
        family["payload"].pop("common_fatal_error")
        packet["packet_digest"] = digest_without(packet, "packet_digest")
        with self.assertRaises(ChemistrySemanticProjectionError) as ctx:
            compile_semantic_projection(packet)
        self.assertEqual(ctx.exception.code, "CHEM_SEMANTIC_PROJECTION_SOURCE_FIELD_MISSING")

    def test_gate_name_does_not_change_projection_logic(self):
        alpha = compile_semantic_projection(make_packet(gate_id="CHEM-SYNTH-ALPHA"), projection_id="CHEM-BP-SEM-SYNTH-ALPHA")
        beta = compile_semantic_projection(make_packet(gate_id="CHEM-SYNTH-BETA"), projection_id="CHEM-BP-SEM-SYNTH-BETA")
        alpha_signature = [
            (row["source_kind"], row["source_field"], row["semantic_role"], row["content"])
            for row in alpha["semantic_atoms"]
        ]
        beta_signature = [
            (row["source_kind"], row["source_field"], row["semantic_role"], row["content"])
            for row in beta["semantic_atoms"]
        ]
        self.assertEqual(alpha_signature, beta_signature)

    def test_generic_projection_source_contains_no_topic_control_flow(self):
        text = (ENGINE / "compile_chemistry_semantic_projection.py").read_text(encoding="utf-8").lower()
        for forbidden in ("re" + "dox", "mn" + "o4", "perman" + "ganate", "thermo" + "dynamics"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
