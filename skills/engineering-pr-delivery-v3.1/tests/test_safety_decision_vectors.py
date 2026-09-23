from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from programme_reconciliation import assess_boundary
from relay_can import evaluate
from test_programme_reconciliation import observation
from test_relay_can import WRITE_PATH, prepare_git


class SafetyDecisionVectorTests(unittest.TestCase):
    """Cross-boundary compatibility vectors for Relay's preserved safety kernel."""

    def test_active_execution_action_vector(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            vector = {
                "MATERIAL_WRITE": evaluate(
                    root,
                    "MATERIAL_WRITE",
                    path=WRITE_PATH,
                    base_ref=base_ref,
                ),
                "CHECKPOINT": evaluate(root, "CHECKPOINT", base_ref=base_ref),
                "HANDOVER": evaluate(root, "HANDOVER"),
                "MERGE": evaluate(root, "MERGE"),
                "RELEASE": evaluate(root, "RELEASE"),
            }

            self.assertTrue(vector["MATERIAL_WRITE"]["allowed"], vector)
            self.assertTrue(vector["CHECKPOINT"]["allowed"], vector)
            self.assertTrue(vector["HANDOVER"]["allowed"], vector)

            for action in ("MERGE", "RELEASE"):
                self.assertFalse(vector[action]["allowed"], vector)
                self.assertIn("DELIVERY_VEHICLE_REQUIRED", vector[action]["reason_codes"])
                self.assertIn(
                    "OWNER_DELIVERY_AUTHORITY_REQUIRED",
                    vector[action]["reason_codes"],
                )

    def test_owner_reselection_displaces_stale_execution_at_actor_boundaries(self):
        current_parent = {"repository": "example/project", "number": 1771}
        observations = [
            observation(1771, acceptance_state="PENDING"),
            observation(1775, acceptance_state="PENDING"),
        ]
        selected = "example/project#1775"

        handover = assess_boundary(
            current_parent,
            observations,
            boundary="HANDOVER",
            selected_frontier_ref=selected,
        )
        next_work = assess_boundary(
            current_parent,
            observations,
            boundary="NEXT_WORK",
            selected_frontier_ref=selected,
        )
        recovery = assess_boundary(
            current_parent,
            observations,
            boundary="RECOVERY_TAKEOVER",
            selected_frontier_ref=selected,
        )
        admission = assess_boundary(
            current_parent,
            observations,
            boundary="ADMIT_TASK",
            selected_frontier_ref=selected,
        )

        for decision in (handover, next_work):
            self.assertEqual("READY", decision["status"])
            self.assertEqual("SWITCH_FRONTIER", decision["continuation"])
            self.assertEqual(selected, decision["next_frontier"])
            self.assertEqual(selected, decision["executable_frontier"])

        for decision in (recovery, admission):
            self.assertEqual("PROGRAMME_FRONTIER_MISMATCH", decision["status"])
            self.assertEqual(selected, decision["executable_frontier"])
            self.assertIn(
                "CURRENT_PARENT_NOT_SELECTED_FRONTIER",
                decision["reason_codes"],
            )

    def test_blocked_selected_frontier_does_not_fall_through(self):
        current_parent = {"repository": "example/project", "number": 288}
        observations = [
            observation(284, acceptance_state="PENDING"),
            observation(286, acceptance_state="DEFERRED"),
            observation(288, acceptance_state="BLOCKED"),
        ]
        selected = "example/project#288"

        handover = assess_boundary(
            current_parent,
            observations,
            boundary="HANDOVER",
            selected_frontier_ref=selected,
        )
        next_work = assess_boundary(
            current_parent,
            observations,
            boundary="NEXT_WORK",
            selected_frontier_ref=selected,
        )
        recovery = assess_boundary(
            current_parent,
            observations,
            boundary="RECOVERY_TAKEOVER",
            selected_frontier_ref=selected,
        )
        admission = assess_boundary(
            current_parent,
            observations,
            boundary="ADMIT_TASK",
            selected_frontier_ref=selected,
        )

        for decision in (handover, next_work):
            self.assertEqual("READY", decision["status"])
            self.assertEqual("BLOCKED_SELECTED_FRONTIER", decision["continuation"])
            self.assertEqual(selected, decision["next_frontier"])
            self.assertIsNone(decision["executable_frontier"])
            self.assertIn(
                "example/project#284",
                decision["reconciliation"]["alternate_live_frontiers"],
            )

        for decision in (recovery, admission):
            self.assertEqual("PROGRAMME_FRONTIER_BLOCKED", decision["status"])
            self.assertEqual("BLOCKED_SELECTED_FRONTIER", decision["continuation"])
            self.assertEqual(selected, decision["next_frontier"])
            self.assertIsNone(decision["executable_frontier"])
            self.assertEqual(
                ["SELECTED_FRONTIER_BLOCKED"],
                decision["reason_codes"],
            )

    def test_generated_state_deletion_does_not_change_action_decisions(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            def decisions() -> dict[str, tuple[bool, list[str]]]:
                results = {
                    "MATERIAL_WRITE": evaluate(
                        root,
                        "MATERIAL_WRITE",
                        path=WRITE_PATH,
                        base_ref=base_ref,
                    ),
                    "CHECKPOINT": evaluate(root, "CHECKPOINT", base_ref=base_ref),
                    "HANDOVER": evaluate(root, "HANDOVER"),
                    "MERGE": evaluate(root, "MERGE"),
                    "RELEASE": evaluate(root, "RELEASE"),
                }
                return {
                    action: (result["allowed"], result["reason_codes"])
                    for action, result in results.items()
                }

            before = decisions()
            shutil.rmtree(root / "relay/GENERATED")
            after = decisions()
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
