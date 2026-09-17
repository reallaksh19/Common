import copy
import inspect
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
TESTS = ROOT / "tests"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(TESTS))

from compile_chemistry_core_authority import compile_core_authority  # noqa: E402
from compile_chemistry_learner_gate_projection import (  # noqa: E402
    ChemistryLearnerGateProjectionError,
    compile_learner_gate_projection,
    digest_without,
    validate_learner_gate_projection,
)
from compile_chemistry_semantic_projection import compile_semantic_projection  # noqa: E402
from test_chemistry_semantic_projection_generic import make_packet  # noqa: E402


def _core1a_payload_for_packet(packet):
    representation_obligations = [
        row for row in packet["obligations"]
        if row["kind"] == "REPRESENTATION" and row["direct"]
    ]
    if len(representation_obligations) != 1:
        raise AssertionError("synthetic learner-gate fixture expects exactly one direct representation")
    engineering_ref = representation_obligations[0]["asset_ref"]
    concrete_ref = "REP-TEST-LEARNER-GATE"
    return {
        "manuscript": {
            "manuscript_id": "TEST-LEARNER-GATE-MANUSCRIPT",
            "buckets": [{
                "learning_atoms": [{"atom_id": "ATOM-LEARNER-GATE-1"}],
                "teaching_sections": [{"representation_refs": [concrete_ref]}],
            }],
        },
        "representation_bundle": {
            "bundle_id": "TEST-LEARNER-GATE-REP-BUNDLE",
            "representations": [{"representation_id": concrete_ref}],
        },
        "representation_bindings": [{
            "representation_ref": concrete_ref,
            "engineering_representation_refs": [engineering_ref],
        }],
    }


class ChemistryLearnerGateProjectionTests(unittest.TestCase):
    def test_every_direct_nonmetadata_semantic_role_maps_to_exact_learner_job_and_polarity(self):
        packet = make_packet()
        semantic = compile_semantic_projection(packet)
        projection = compile_learner_gate_projection(packet, semantic_projection=semantic)
        self.assertEqual(projection["status"], "LEARNER_GATE_PROJECTION_READY")
        by_role = {row["semantic_role"]: row for row in projection["learner_gates"]}
        expected = {
            "CONCEPT_RULE": ("STATE_OR_EXPLAIN_RULE", "POSITIVE"),
            "EQUATION_MODEL": ("USE_EQUATION_MODEL", "POSITIVE"),
            "VALIDITY_BOUNDARY": ("CHECK_VALIDITY_BOUNDARY", "CONTEXT"),
            "REPRESENTATION_REQUIREMENT": ("READ_OR_CONSTRUCT_REPRESENTATION", "POSITIVE"),
            "VERIFICATION": ("VERIFY_RESULT", "POSITIVE"),
            "BOUNDARY_CONSEQUENCE": ("EXPLAIN_BOUNDARY_CONSEQUENCE", "CONTEXT"),
            "REASONING_MOVE": ("EXECUTE_REASONING_MOVE", "POSITIVE"),
            "TRANSFORMATION_REQUIREMENT": ("PERFORM_TRANSFORMATION", "POSITIVE"),
            "MISCONCEPTION": ("REJECT_MISCONCEPTION", "NEGATIVE"),
            "COUNTEREXAMPLE": ("USE_COUNTEREXAMPLE", "POSITIVE"),
            "MISCONCEPTION_REPAIR": ("APPLY_MISCONCEPTION_REPAIR", "POSITIVE"),
            "RECOGNITION_SIGNAL": ("RECOGNIZE_PROBLEM_FAMILY", "CONTEXT"),
            "METHOD_STEP": ("EXECUTE_METHOD_STEP", "POSITIVE"),
            "ERROR_TO_AVOID": ("AVOID_FATAL_ERROR", "NEGATIVE"),
            "TARGET_UNKNOWN": ("IDENTIFY_TARGET_UNKNOWN", "CONTEXT"),
        }
        self.assertEqual(set(by_role), set(expected))
        for role, pair in expected.items():
            self.assertEqual((by_role[role]["learner_job"], by_role[role]["polarity"]), pair, role)
        semantic_by_id = {row["semantic_id"]: row for row in semantic["semantic_atoms"]}
        for gate in projection["learner_gates"]:
            self.assertEqual(gate["content"], semantic_by_id[gate["source_semantic_id"]]["content"])
        difficulty = next(row for row in semantic["semantic_atoms"] if row["semantic_role"] == "DIFFICULTY_EVIDENCE")
        self.assertIn(difficulty["semantic_id"], projection["metadata_semantic_ids"])
        self.assertNotIn(difficulty["semantic_id"], {row["source_semantic_id"] for row in projection["learner_gates"]})
        self.assertEqual(validate_learner_gate_projection(packet, projection, semantic_projection=semantic)["status"], "PASS")

    def test_fatal_error_and_misconception_never_become_positive_method_jobs(self):
        projection = compile_learner_gate_projection(make_packet())
        fatal = next(row for row in projection["learner_gates"] if row["semantic_role"] == "ERROR_TO_AVOID")
        misconception = next(row for row in projection["learner_gates"] if row["semantic_role"] == "MISCONCEPTION")
        method = next(row for row in projection["learner_gates"] if row["semantic_role"] == "METHOD_STEP")
        self.assertEqual((fatal["learner_job"], fatal["polarity"]), ("AVOID_FATAL_ERROR", "NEGATIVE"))
        self.assertEqual((misconception["learner_job"], misconception["polarity"]), ("REJECT_MISCONCEPTION", "NEGATIVE"))
        self.assertEqual((method["learner_job"], method["polarity"]), ("EXECUTE_METHOD_STEP", "POSITIVE"))

    def test_prerequisite_semantics_remain_context_and_do_not_become_learner_content(self):
        packet = make_packet()
        prerequisite = next(row for row in packet["obligations"] if row["kind"] == "CONCEPT")
        prerequisite["gate_id"] = "CHEM-SYNTH-PREREQUISITE"
        prerequisite["direct"] = False
        prerequisite["required_realization_modes"] = []
        packet["closure_gate_ids"] = ["CHEM-SYNTH-PREREQUISITE", "CHEM-SYNTH-ALPHA"]
        packet["counts"]["gate_count"] = 2
        packet["packet_digest"] = digest_without(packet, "packet_digest")
        semantic = compile_semantic_projection(packet)
        prereq_atom = next(row for row in semantic["semantic_atoms"] if row["source_obligation_id"] == prerequisite["obligation_id"])
        projection = compile_learner_gate_projection(packet, semantic_projection=semantic)
        self.assertIn(prereq_atom["semantic_id"], projection["context_semantic_ids"])
        self.assertNotIn(prereq_atom["semantic_id"], {row["source_semantic_id"] for row in projection["learner_gates"]})
        self.assertEqual(projection["counts"]["context_semantic_count"], 1)
        realized = [row["obligation_id"] for row in packet["obligations"] if "CORE1A" in row["authorized_modes"]]
        authority = compile_core_authority(
            "CORE1A", "SYNTHETIC", _core1a_payload_for_packet(packet), packet, realized,
            authority_id="CHEM-CORE-AUTH-LEARNER-GATE-CONTEXT-TEST",
            payload_ref="tests/learner-gate-context.json",
        )
        self.assertIn(prereq_atom["semantic_id"], authority["learner_gate_closure"]["context_semantic_ids"])
        self.assertEqual(authority["learner_gate_closure"]["status"], "PASS")

    def test_authorized_and_required_modes_are_copied_not_expanded(self):
        packet = make_packet()
        concept = next(row for row in packet["obligations"] if row["kind"] == "CONCEPT")
        concept["authorized_modes"] = ["CORE1A", "CORE2A"]
        concept["required_realization_modes"] = ["CORE1A"]
        packet["packet_digest"] = digest_without(packet, "packet_digest")
        projection = compile_learner_gate_projection(packet)
        gate = next(row for row in projection["learner_gates"] if row["source_obligation_id"] == concept["obligation_id"])
        self.assertEqual(gate["authorized_modes"], ["CORE1A", "CORE2A"])
        self.assertEqual(gate["required_realization_modes"], ["CORE1A"])

    def test_core_authority_records_required_and_realized_learner_gate_closure(self):
        packet = make_packet()
        projection = compile_learner_gate_projection(packet)
        realized = [row["obligation_id"] for row in packet["obligations"] if "CORE1A" in row["authorized_modes"]]
        authority = compile_core_authority(
            "CORE1A", "SYNTHETIC", _core1a_payload_for_packet(packet), packet, realized,
            authority_id="CHEM-CORE-AUTH-LEARNER-GATE-TEST",
            payload_ref="tests/learner-gate.json",
        )
        closure = authority["learner_gate_closure"]
        self.assertEqual(closure["status"], "PASS")
        self.assertEqual(authority["learner_gate_projection_id"], projection["projection_id"])
        self.assertEqual(closure["authorized_learner_gate_ids"], sorted(row["learner_gate_id"] for row in projection["learner_gates"]))
        self.assertEqual(closure["required_learner_gate_ids"], closure["realized_learner_gate_ids"])
        self.assertTrue(closure["metadata_semantic_ids"])

    def test_downstream_learner_job_reclassification_fails_canonical_recompile(self):
        packet = make_packet()
        projection = compile_learner_gate_projection(packet)
        tampered = copy.deepcopy(projection)
        fatal = next(row for row in tampered["learner_gates"] if row["semantic_role"] == "ERROR_TO_AVOID")
        fatal["learner_job"] = "EXECUTE_METHOD_STEP"
        fatal["polarity"] = "POSITIVE"
        tampered["projection_digest"] = digest_without(tampered, "projection_digest")
        with self.assertRaises(ChemistryLearnerGateProjectionError) as ctx:
            validate_learner_gate_projection(packet, tampered)
        self.assertEqual(ctx.exception.code, "CHEM_LEARNER_GATE_PROJECTION_DRIFT")

    def test_gate_rename_does_not_change_learner_job_structure(self):
        alpha = compile_learner_gate_projection(make_packet(gate_id="CHEM-SYNTH-ALPHA"), projection_id="CHEM-BP-LG-SYNTH-ALPHA")
        beta = compile_learner_gate_projection(make_packet(gate_id="CHEM-SYNTH-BETA"), projection_id="CHEM-BP-LG-SYNTH-BETA")
        def signature(projection):
            return [(row["semantic_role"], row["learner_job"], row["polarity"], row["content"], row["authorized_modes"], row["required_realization_modes"]) for row in projection["learner_gates"]]
        self.assertEqual(signature(alpha), signature(beta))
        self.assertEqual(alpha["counts"]["metadata_semantic_count"], beta["counts"]["metadata_semantic_count"])

    def test_generic_compiler_contains_no_topic_control_flow(self):
        source = inspect.getsource(__import__("compile_chemistry_learner_gate_projection")).lower()
        for forbidden in ("re" + "dox", "thermo" + "dynamics", "perman" + "ganate", "mn" + "o4"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
