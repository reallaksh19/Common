#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AGENT_TASKS = ROOT / "Grade 9" / "V2" / "Shared" / "AgentTasks"
AGENT_ENGINE = AGENT_TASKS / "engine"
BLUEPRINT_ENGINE = ROOT / "Grade 9" / "V2" / "Physics" / "Blueprint" / "engine"
sys.path.insert(0, str(AGENT_ENGINE))
sys.path.insert(0, str(BLUEPRINT_ENGINE))

from compile_execution_packet import compile_packet, digest  # noqa: E402
from consume_agent_task_packet import (  # noqa: E402
    BlueprintAgentTaskIntakeError,
    consume_execution_packet,
)

TASK_FIXTURE = AGENT_TASKS / "fixtures" / "valid" / "physics-subtopic-engineering.task.json"


def load_task() -> dict:
    task = json.loads(TASK_FIXTURE.read_text(encoding="utf-8"))
    task["task_id"] = "TASK-BLUEPRINT-INTAKE-SYNTHETIC"
    task["topic"] = "SYNTHETIC_TOPIC_ALPHA"
    task["subtopic"] = "SYNTHETIC_SUBTOPIC_BETA"
    task["target_consumers"] = ["PROBLEM_SEMANTICS", "PUBLICATION"]
    return task


class BlueprintAgentTaskIntakeTests(unittest.TestCase):
    def test_valid_packet_is_context_only(self):
        packet = compile_packet(load_task())
        receipt = consume_execution_packet(packet)

        self.assertEqual(receipt["status"], "ACCEPTED_AS_DELEGATION_CONTEXT")
        self.assertEqual(receipt["packet_digest"], packet["packet_digest"])
        self.assertEqual(receipt["authority_boundary"]["scope_selection"], "REPOSITORY_GOVERNED_NOT_PACKET")
        self.assertEqual(receipt["authority_boundary"]["domain_truth"], "REPOSITORY_GOVERNED_NOT_PACKET")
        self.assertEqual(receipt["authority_boundary"]["engineering_readiness"], "RECOMPUTE_FROM_GOVERNED_SCOPE")
        self.assertEqual(receipt["authority_boundary"]["consumer_permissions"], "NOT_AUTHORIZED_BY_PACKET")
        self.assertEqual(receipt["authority_boundary"]["publication"], "NOT_AUTHORIZED_BY_PACKET")
        self.assertNotIn("scope_ref", receipt)
        self.assertNotIn("engineering_ready", receipt)

    def test_topic_subtopic_and_learner_variation_do_not_change_authority_boundary(self):
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
        self.assertEqual(receipt_a["status"], receipt_b["status"])

    def test_target_consumer_is_intent_not_permission(self):
        task = load_task()
        task["target_consumers"] = ["PUBLICATION"]
        packet = compile_packet(task)
        receipt = consume_execution_packet(packet)

        self.assertEqual(receipt["execution_intent"]["target_consumers"], ["PUBLICATION"])
        self.assertEqual(packet["engineering_preflight"]["consumer_permissions"]["PUBLICATION"]["status"], "NOT_EVALUATED")
        self.assertEqual(receipt["authority_boundary"]["publication"], "NOT_AUTHORIZED_BY_PACKET")

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

    def test_physics_blueprint_rejects_other_subject_even_with_recomputed_digest(self):
        packet = compile_packet(load_task())
        packet["task"]["subject"] = "CHEMISTRY"
        packet["learning_engineering_state"]["subject_adapter"]["subject"] = "CHEMISTRY"
        packet["packet_digest"] = digest({k: v for k, v in packet.items() if k != "packet_digest"})
        with self.assertRaisesRegex(BlueprintAgentTaskIntakeError, "E_BLUEPRINT_TASK_SUBJECT_MISMATCH"):
            consume_execution_packet(packet)


if __name__ == "__main__":
    unittest.main()
