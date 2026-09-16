#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AGENT_TASKS = ROOT / "Grade 9" / "V2" / "Shared" / "AgentTasks"
AGENT_ENGINE = AGENT_TASKS / "engine"
PHYSICS_ENGINE = ROOT / "Grade 9" / "V2" / "Physics" / "Blueprint" / "engine"
sys.path.insert(0, str(AGENT_ENGINE))
sys.path.insert(0, str(PHYSICS_ENGINE))

from compile_execution_packet import compile_packet  # noqa: E402
from compile_engineering_readiness import compile_readiness  # noqa: E402
from validate_execution_report import validate_report  # noqa: E402

TASK_PATH = AGENT_TASKS / "fixtures" / "valid" / "physics-relative-motion-governed.task.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class GovernedPhysicsCaseIntegrationTests(unittest.TestCase):
    def test_packet_front_door_does_not_replace_engineering_authority(self):
        task = load(TASK_PATH)
        packet = compile_packet(task)
        by_role = {row["role"]: row for row in packet["governed_input_bindings"]}
        self.assertEqual(set(by_role), {"ENGINEERING_REQUEST", "ENGINEERING_MANIFEST"})

        request = load(ROOT / by_role["ENGINEERING_REQUEST"]["path"])
        manifest = load(ROOT / by_role["ENGINEERING_MANIFEST"]["path"])
        self.assertEqual(request["engineering_depth"], task["engineering_depth"])
        self.assertEqual(request["request_id"], manifest["request_id"])

        # Delegation preflight is intentionally non-authorizing.
        self.assertEqual(packet["engineering_preflight"]["engineering_state"], "NOT_EVALUATED")
        self.assertTrue(
            all(
                packet["engineering_preflight"]["consumer_permissions"][consumer]["status"] == "NOT_EVALUATED"
                for consumer in task["target_consumers"]
            )
        )

        # The current subject compiler and Shared EngineeringGate produce the real state.
        engineering, domain, envelope = compile_readiness(request, manifest)
        self.assertEqual(engineering["request_id"], request["request_id"])
        self.assertEqual(envelope["request_id"], request["request_id"])
        self.assertEqual(envelope["manifest_id"], manifest["manifest_id"])
        self.assertEqual(envelope["authority_layer"], "ENGINEERING_GATE")
        self.assertEqual(envelope["publication_authorization"], "NOT_IMPLIED")
        self.assertEqual(envelope["consumer_permissions"]["PUBLICATION"]["status"], "NOT_AUTHORIZED")
        self.assertIn(envelope["consumer_permissions"]["CCU"]["status"], {"ALLOWED", "BLOCKED"})

        # Report the downstream result without allowing the task layer to invent it.
        report = {
            "schema_version": "1.0.0",
            "task_id": task["task_id"],
            "packet_digest": packet["packet_digest"],
            "start_head": packet["repository_state"]["resolved_head"],
            "end_head": packet["repository_state"]["resolved_head"],
            "execution_result": "COMPLETE",
            "engineering_state": (
                "READY" if envelope["overall_state"] == "READY_FOR_TECHNICAL_CONSUMPTION" else "BLOCKED"
            ),
            "research_state": envelope["dimensions"]["research_provenance"],
            "consumer_permissions": {
                consumer: envelope["consumer_permissions"][consumer]
                for consumer in task["target_consumers"]
            },
            "publication_state": "NOT_IMPLIED",
            "authority_bindings_used": packet["authority_bindings"],
            "changed_files": [],
            "tests": [{"name": "current Physics readiness pipeline", "result": "PASS"}],
            "workflows": [],
            "blockers": [row["message"] for row in envelope["blockers"]],
            "limitations": [],
            "unresolved": [],
            "architecture_findings": [
                "Execution packet preserved exact input/authority custody while downstream EngineeringGate remained the sole readiness authority."
            ],
            "memory_dependency_detected": False,
        }
        validate_report(packet, report)
        self.assertEqual(domain["engineering_receipt_ref"], engineering["receipt_id"])


if __name__ == "__main__":
    unittest.main()
