import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
TESTS = ROOT / "tests"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(TESTS))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_learner_gate_projection import compile_learner_gate_projection  # noqa: E402
from compile_chemistry_semantic_projection import compile_semantic_projection  # noqa: E402
from test_chemistry_four_core_compilation import (  # noqa: E402
    REGISTRY,
    make_manifest,
    make_production_audit,
    make_request,
)

TARGET_GATE = "CHEM-THERMO-FIRST-LAW-WORK"


class ChemistryLearnerGateProjectionThermodynamicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate = next(row for row in REGISTRY["subtopic_gates"] if row["subtopic_id"] == TARGET_GATE)
        cls.audit_ref = "tests/in-memory-thermodynamics-first-law-audit.json"
        cls.packet = compile_blueprint_obligations(
            make_request(),
            make_manifest(cls.gate, cls.audit_ref),
            registry=REGISTRY,
            source_audit_payloads={cls.audit_ref: make_production_audit(cls.gate)},
        )
        cls.semantic = compile_semantic_projection(cls.packet)
        cls.learner = compile_learner_gate_projection(cls.packet, semantic_projection=cls.semantic)

    def test_production_first_law_gate_reaches_learner_projection_without_topic_branch(self):
        self.assertEqual(self.packet["direct_gate_ids"], [TARGET_GATE])
        self.assertEqual(self.learner["status"], "LEARNER_GATE_PROJECTION_READY")
        direct_source_gates = {row["source_gate_id"] for row in self.learner["learner_gates"]}
        self.assertEqual(direct_source_gates, {TARGET_GATE})
        self.assertGreater(self.learner["counts"]["learner_gate_count"], 0)

    def test_first_law_sign_model_boundary_method_error_and_repair_keep_distinct_jobs(self):
        rows = self.learner["learner_gates"]
        by_role = {}
        for row in rows:
            by_role.setdefault(row["semantic_role"], []).append(row)
        for role in (
            "CONCEPT_RULE",
            "EQUATION_MODEL",
            "VALIDITY_BOUNDARY",
            "REASONING_MOVE",
            "MISCONCEPTION",
            "COUNTEREXAMPLE",
            "MISCONCEPTION_REPAIR",
            "VERIFICATION",
            "RECOGNITION_SIGNAL",
            "METHOD_STEP",
            "ERROR_TO_AVOID",
        ):
            self.assertTrue(by_role.get(role), role)

        methods = by_role["METHOD_STEP"]
        errors = by_role["ERROR_TO_AVOID"]
        misconceptions = by_role["MISCONCEPTION"]
        repairs = by_role["MISCONCEPTION_REPAIR"]
        self.assertTrue(all(row["learner_job"] == "EXECUTE_METHOD_STEP" and row["polarity"] == "POSITIVE" for row in methods))
        self.assertTrue(all(row["learner_job"] == "AVOID_FATAL_ERROR" and row["polarity"] == "NEGATIVE" for row in errors))
        self.assertTrue(all(row["learner_job"] == "REJECT_MISCONCEPTION" and row["polarity"] == "NEGATIVE" for row in misconceptions))
        self.assertTrue(all(row["learner_job"] == "APPLY_MISCONCEPTION_REPAIR" and row["polarity"] == "POSITIVE" for row in repairs))
        self.assertFalse({row["source_semantic_id"] for row in methods} & {row["source_semantic_id"] for row in errors})

        corpus = " ".join(row["content"] for row in rows).casefold()
        self.assertIn("delta u", corpus)
        self.assertIn("expansion", corpus)
        self.assertIn("isothermal", corpus)

    def test_prerequisite_closure_remains_context_not_automatic_learner_content(self):
        semantic_by_id = {row["semantic_id"]: row for row in self.semantic["semantic_atoms"]}
        context_rows = [semantic_by_id[semantic_id] for semantic_id in self.learner["context_semantic_ids"]]
        self.assertTrue(context_rows)
        self.assertTrue(any(row["source_gate_id"] != TARGET_GATE for row in context_rows))
        self.assertTrue(all(row["direct"] is False for row in context_rows))
        learner_semantic_ids = {row["source_semantic_id"] for row in self.learner["learner_gates"]}
        self.assertFalse(learner_semantic_ids & set(self.learner["context_semantic_ids"]))

    def test_difficulty_evidence_stays_metadata_only_even_for_direct_gate(self):
        semantic_by_id = {row["semantic_id"]: row for row in self.semantic["semantic_atoms"]}
        metadata_rows = [semantic_by_id[semantic_id] for semantic_id in self.learner["metadata_semantic_ids"]]
        direct_difficulty = [
            row for row in metadata_rows
            if row["source_gate_id"] == TARGET_GATE and row["semantic_role"] == "DIFFICULTY_EVIDENCE"
        ]
        self.assertTrue(direct_difficulty)
        learner_semantic_ids = {row["source_semantic_id"] for row in self.learner["learner_gates"]}
        self.assertFalse({row["semantic_id"] for row in direct_difficulty} & learner_semantic_ids)


if __name__ == "__main__":
    unittest.main()
