#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AGENT_TASKS = ROOT / "Grade 9" / "V2" / "Shared" / "AgentTasks"
AGENT_ENGINE = AGENT_TASKS / "engine"
BLUEPRINT = ROOT / "Grade 9" / "V2" / "Physics" / "Blueprint"
BLUEPRINT_ENGINE = BLUEPRINT / "engine"
ASSESSMENT_INTAKE_ENGINE = ROOT / "Grade 9" / "V2" / "Physics" / "AssessmentIntake" / "engine"
COLD_ENGINE = ROOT / "Grade 9" / "V2" / "Physics" / "ColdStart" / "engine"
sys.path.insert(0, str(AGENT_ENGINE))
sys.path.insert(0, str(BLUEPRINT_ENGINE))
sys.path.insert(0, str(ASSESSMENT_INTAKE_ENGINE))
sys.path.insert(0, str(COLD_ENGINE))

from compile_execution_packet import compile_packet, digest  # noqa: E402
from consume_agent_task_packet import (  # noqa: E402
    BlueprintAgentTaskIntakeError,
    consume_execution_packet,
)
from run_agent_task_cold_start import run_packet_cold_start  # noqa: E402
from build_physics_assessment_intake import build_intake  # noqa: E402
from physics_cold_start_runner import validate_assessment_input_bindings  # noqa: E402

TASK_FIXTURE = AGENT_TASKS / "fixtures" / "valid" / "physics-subtopic-engineering.task.json"
ROUTED_TASK_FIXTURE = BLUEPRINT / "fixtures" / "agent-task-routed-motion.fixture.json"


def load_task() -> dict:
    task = json.loads(TASK_FIXTURE.read_text(encoding="utf-8"))
    task["task_id"] = "TASK-BLUEPRINT-INTAKE-SYNTHETIC"
    task["topic"] = "SYNTHETIC_TOPIC_ALPHA"
    task["subtopic"] = "SYNTHETIC_SUBTOPIC_BETA"
    task["target_consumers"] = ["PROBLEM_SEMANTICS", "PUBLICATION"]
    return task


def load_routed_task() -> dict:
    return json.loads(ROUTED_TASK_FIXTURE.read_text(encoding="utf-8"))


def binding_map(receipt: dict) -> dict[str, dict]:
    return {row["role"]: row for row in receipt["execution_route"]["input_bindings"]}


class BlueprintAgentTaskIntakeTests(unittest.TestCase):
    def test_valid_packet_without_route_request_is_context_only_and_held(self):
        packet = compile_packet(load_task())
        receipt = consume_execution_packet(packet)

        self.assertEqual(receipt["status"], "ACCEPTED_AS_DELEGATION_CONTEXT")
        self.assertEqual(receipt["packet_digest"], packet["packet_digest"])
        self.assertEqual(receipt["execution_route"]["status"], "HELD_NO_ROUTE_REQUESTED")
        self.assertFalse(receipt["execution_route"]["execution_authorized"])
        self.assertEqual(receipt["execution_route"]["authorization_scope"], "P-A_INPUT_SELECTION_ONLY")
        self.assertIsNone(receipt["execution_route"]["route_id"])
        self.assertEqual(receipt["execution_route"]["input_bindings"], [])
        self.assertEqual(receipt["execution_route"]["label_inference"], "PROHIBITED")
        self.assertEqual(receipt["authority_boundary"]["scope_selection"], "REPOSITORY_GOVERNED_NOT_PACKET")
        self.assertEqual(receipt["authority_boundary"]["domain_truth"], "REPOSITORY_GOVERNED_NOT_PACKET")
        self.assertEqual(receipt["authority_boundary"]["engineering_readiness"], "RECOMPUTE_FROM_GOVERNED_SCOPE")
        self.assertEqual(receipt["authority_boundary"]["consumer_permissions"], "NOT_AUTHORIZED_BY_PACKET")
        self.assertEqual(receipt["authority_boundary"]["publication"], "NOT_AUTHORIZED_BY_PACKET")
        self.assertNotIn("scope_ref", receipt)
        self.assertNotIn("engineering_ready", receipt)

    def test_exact_opaque_route_resolves_repository_owned_p_a_inputs(self):
        packet = compile_packet(load_routed_task())
        receipt = consume_execution_packet(packet)
        route = receipt["execution_route"]

        self.assertEqual(route["status"], "RESOLVED_REPOSITORY_ROUTE")
        self.assertTrue(route["execution_authorized"])
        self.assertEqual(route["authorization_scope"], "P-A_INPUT_SELECTION_ONLY")
        self.assertEqual(route["route_id"], "PHY-PA-ROUTE-001-V1")
        self.assertEqual(route["label_inference"], "PROHIBITED")
        self.assertEqual(route["route_registry"]["registry_id"], "PHY-BLUEPRINT-EXECUTION-ROUTES-v1")
        roles = binding_map(receipt)
        self.assertEqual(set(roles), {"QUESTION_SET", "DECLARED_TOPIC_SCOPE", "ATTEMPT_SET"})
        self.assertTrue(roles["QUESTION_SET"]["required"])
        self.assertTrue(roles["DECLARED_TOPIC_SCOPE"]["required"])
        self.assertFalse(roles["ATTEMPT_SET"]["required"])
        for row in roles.values():
            self.assertTrue((ROOT / row["path"]).is_file())
            self.assertRegex(row["sha256"], r"^sha256:[0-9a-f]{64}$")

    def test_resolved_route_can_feed_existing_p_a_without_becoming_scope_authority(self):
        receipt = consume_execution_packet(compile_packet(load_routed_task()))
        roles = binding_map(receipt)
        question_set = json.loads((ROOT / roles["QUESTION_SET"]["path"]).read_text(encoding="utf-8"))
        topic_scope = json.loads((ROOT / roles["DECLARED_TOPIC_SCOPE"]["path"]).read_text(encoding="utf-8"))
        attempts = json.loads((ROOT / roles["ATTEMPT_SET"]["path"]).read_text(encoding="utf-8"))

        no_attempt = build_intake(
            copy.deepcopy(question_set),
            copy.deepcopy(topic_scope),
            None,
            "PHY-ROUTE-PROOF-NO-ATTEMPT",
        )
        with_attempt = build_intake(
            copy.deepcopy(question_set),
            copy.deepcopy(topic_scope),
            copy.deepcopy(attempts),
            "PHY-ROUTE-PROOF-WITH-ATTEMPT",
        )

        self.assertEqual(no_attempt["subject"], "PHYSICS")
        self.assertEqual(no_attempt["question_set_digest"], with_attempt["question_set_digest"])
        self.assertEqual(no_attempt["declared_topic_scope_digest"], with_attempt["declared_topic_scope_digest"])
        self.assertEqual(no_attempt["attempt_mode"], "ABSENT")
        self.assertEqual(with_attempt["attempt_mode"], "PRESENT")
        self.assertEqual(receipt["authority_boundary"]["scope_selection"], "REPOSITORY_GOVERNED_NOT_PACKET")
        self.assertEqual(receipt["authority_boundary"]["engineering_readiness"], "RECOMPUTE_FROM_GOVERNED_SCOPE")

    def test_route_id_not_labels_controls_input_selection(self):
        task_a = load_routed_task()
        task_b = copy.deepcopy(task_a)
        task_b["task_id"] = "TASK-BLUEPRINT-ROUTE-METAMORPHIC"
        task_b["grade"] = 11
        task_b["curriculum"] = {"system": "SYNTHETIC_CURRICULUM", "version": "X"}
        task_b["topic"] = "COMPLETELY_DIFFERENT_TOPIC_LABEL"
        task_b["subtopic"] = "COMPLETELY_DIFFERENT_SUBTOPIC_LABEL"
        task_b["learner_state"] = "SYNTHETIC_LEARNER_STATE"
        task_b["engineering_depth"] = "RESEARCH"
        task_b["target_consumers"] = ["PUBLICATION"]

        receipt_a = consume_execution_packet(compile_packet(task_a))
        receipt_b = consume_execution_packet(compile_packet(task_b))

        self.assertNotEqual(receipt_a["packet_digest"], receipt_b["packet_digest"])
        self.assertEqual(receipt_a["execution_route"], receipt_b["execution_route"])
        self.assertEqual(receipt_a["authority_boundary"], receipt_b["authority_boundary"])
        self.assertEqual(receipt_b["execution_route"]["status"], "RESOLVED_REPOSITORY_ROUTE")
        self.assertEqual(receipt_b["authority_boundary"]["publication"], "NOT_AUTHORIZED_BY_PACKET")

    def test_unknown_exact_route_is_held_and_never_falls_back_to_labels(self):
        task = load_routed_task()
        task["execution_route_id"] = "PHY-PA-ROUTE-999-V1"
        task["topic"] = "Motion"
        task["subtopic"] = "Exact labels still cannot select a route"
        receipt = consume_execution_packet(compile_packet(task))

        self.assertEqual(receipt["execution_route"]["status"], "HELD_ROUTE_UNRESOLVED")
        self.assertFalse(receipt["execution_route"]["execution_authorized"])
        self.assertEqual(receipt["execution_route"]["route_id"], "PHY-PA-ROUTE-999-V1")
        self.assertEqual(receipt["execution_route"]["input_bindings"], [])
        self.assertEqual(receipt["execution_route"]["label_inference"], "PROHIBITED")

    def test_topic_subtopic_learner_and_depth_variation_without_route_stays_held(self):
        task_a = load_task()
        task_b = copy.deepcopy(task_a)
        task_b["task_id"] = "TASK-BLUEPRINT-INTAKE-SYNTHETIC-2"
        task_b["topic"] = "SYNTHETIC_TOPIC_GAMMA"
        task_b["subtopic"] = "SYNTHETIC_SUBTOPIC_DELTA"
        task_b["learner_state"] = "SYNTHETIC_LEARNER_STATE"
        task_b["engineering_depth"] = "RESEARCH"

        receipt_a = consume_execution_packet(compile_packet(task_a))
        receipt_b = consume_execution_packet(compile_packet(task_b))

        self.assertNotEqual(receipt_a["packet_digest"], receipt_b["packet_digest"])
        self.assertEqual(receipt_a["authority_boundary"], receipt_b["authority_boundary"])
        self.assertEqual(receipt_a["execution_route"], receipt_b["execution_route"])
        self.assertEqual(receipt_a["status"], receipt_b["status"])

    def test_requested_consumer_is_intent_not_permission_even_when_route_resolves(self):
        task = load_routed_task()
        task["target_consumers"] = ["PUBLICATION"]
        packet = compile_packet(task)
        receipt = consume_execution_packet(packet)

        self.assertEqual(receipt["execution_intent"]["target_consumers"], ["PUBLICATION"])
        self.assertEqual(packet["engineering_preflight"]["consumer_permissions"]["PUBLICATION"]["status"], "NOT_EVALUATED")
        self.assertEqual(receipt["execution_route"]["status"], "RESOLVED_REPOSITORY_ROUTE")
        self.assertTrue(receipt["execution_route"]["execution_authorized"])
        self.assertEqual(receipt["authority_boundary"]["publication"], "NOT_AUTHORIZED_BY_PACKET")

    def test_route_input_digest_tamper_fails_before_cold_start(self):
        receipt = consume_execution_packet(compile_packet(load_routed_task()))
        bindings = copy.deepcopy(receipt["execution_route"]["input_bindings"])
        bindings[0]["sha256"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "ASSESSMENT_INPUT_DIGEST_MISMATCH"):
            validate_assessment_input_bindings(bindings, ROOT)

    def test_routed_packet_traverses_existing_cold_start_without_gaining_release_authority(self):
        packet = compile_packet(load_routed_task())
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            receipt = run_packet_cold_start(packet, out)
            no_attempt = json.loads((out / "no-attempt" / "run_report.json").read_text(encoding="utf-8"))
            with_attempts = json.loads((out / "with-attempts" / "run_report.json").read_text(encoding="utf-8"))

            self.assertEqual(receipt["route_id"], "PHY-PA-ROUTE-001-V1")
            self.assertTrue(receipt["comparison_invariants_all_true"])
            self.assertEqual(receipt["engineering"]["no_attempt_consumer_status"], "ALLOWED")
            self.assertEqual(receipt["engineering"]["with_attempts_consumer_status"], "ALLOWED")
            self.assertTrue(receipt["engineering"]["requirement_state_identical"])
            self.assertEqual(receipt["publication_authorization"], "NOT_IMPLIED")
            self.assertEqual(receipt["human_review_authorization"], "NOT_IMPLIED")

            roles = {row["role"]: row for row in receipt["assessment_input_bindings"]}
            no_reads = set(no_attempt["runtime_dependency_audit"]["runtime_reads"])
            with_reads = set(with_attempts["runtime_dependency_audit"]["runtime_reads"])
            self.assertIn(roles["QUESTION_SET"]["path"], no_reads)
            self.assertIn(roles["DECLARED_TOPIC_SCOPE"]["path"], no_reads)
            self.assertNotIn(roles["ATTEMPT_SET"]["path"], no_reads)
            self.assertIn(roles["ATTEMPT_SET"]["path"], with_reads)
            self.assertEqual(no_attempt["manifest_digest"], with_attempts["manifest_digest"])
            self.assertEqual(no_attempt["assessment_truth"]["assessment_scope_digest"], with_attempts["assessment_truth"]["assessment_scope_digest"])
            self.assertEqual(no_attempt["assessment_truth"]["engineering_readiness_digest"], with_attempts["assessment_truth"]["engineering_readiness_digest"])

    def test_tampered_packet_fails_closed(self):
        packet = compile_packet(load_task())
        packet["task"]["topic"] = "TAMPERED_TOPIC"
        with self.assertRaisesRegex(BlueprintAgentTaskIntakeError, "E_BLUEPRINT_EXECUTION_PACKET_INVALID"):
            consume_execution_packet(packet)

    def test_recomputed_manual_readiness_still_fails_closed(self):
        packet = compile_packet(load_task())
        packet["engineering_preflight"]["engineering_state"] = "READY_FOR_TECHNICAL_CONSUMPTION"
        packet["packet_digest"] = digest({k: v for k, v in packet.items() if k != "packet_digest"})
        with self.assertRaisesRegex(BlueprintAgentTaskIntakeError, "E_BLUEPRINT_EXECUTION_PACKET_INVALID"):
            consume_execution_packet(packet)

    def test_stale_repository_head_fails_closed(self):
        packet = compile_packet(load_task())
        stale_head = "f" * 40 if packet["repository_state"]["resolved_head"] != "f" * 40 else "e" * 40
        with self.assertRaisesRegex(BlueprintAgentTaskIntakeError, "E_BLUEPRINT_EXECUTION_PACKET_STALE"):
            consume_execution_packet(packet, current_head=stale_head)

    def test_bound_authority_digest_drift_fails_closed(self):
        packet = compile_packet(load_task())
        packet["authority_bindings"][0]["sha256"] = "sha256:" + "0" * 64
        packet["packet_digest"] = digest({k: v for k, v in packet.items() if k != "packet_digest"})
        with self.assertRaisesRegex(BlueprintAgentTaskIntakeError, "E_BLUEPRINT_BOUND_AUTHORITY_DRIFT"):
            consume_execution_packet(packet)

    def test_physics_blueprint_rejects_other_subject_even_with_recomputed_digest(self):
        packet = compile_packet(load_task())
        packet["task"]["subject"] = "CHEMISTRY"
        packet["learning_engineering_state"]["subject_adapter"]["subject"] = "CHEMISTRY"
        packet["packet_digest"] = digest({k: v for k, v in packet.items() if k != "packet_digest"})
        with self.assertRaisesRegex(BlueprintAgentTaskIntakeError, "E_BLUEPRINT_TASK_SUBJECT_MISMATCH"):
            consume_execution_packet(packet)


if __name__ == "__main__":
    unittest.main()
