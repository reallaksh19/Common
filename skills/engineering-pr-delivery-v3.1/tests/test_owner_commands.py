from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from owner_commands import parse_owner_command


class OwnerWorkflowCommandTests(unittest.TestCase):
    def intent(self, text: str) -> str | None:
        return parse_owner_command(text)["intent"]

    def test_what_next_variants_are_read_only_reconciliation(self):
        for phrase in (
            "What next?",
            "what's next",
            "What should we do next?",
            "What is the next real task?",
            "Figure out what next",
        ):
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("WHAT_NEXT", result["intent"])
                self.assertEqual("NEXT_WORK", result["workflow"]["boundary"])
                self.assertFalse(result["workflow"]["progress_execution"])

    def test_proceed_next_variants_progress_only_after_reconciliation(self):
        for phrase in (
            "Proceed next",
            "Proceed to next task",
            "Proceed with the next task",
            "Continue with the next task",
            "Move on to the next task",
            "Take the next task",
        ):
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("PROCEED_NEXT", result["intent"])
                self.assertTrue(result["workflow"]["progress_execution"])
                self.assertEqual("NEXT_WORK", result["workflow"]["boundary"])

    def test_complex_next_variants_force_whole_task_reanchor(self):
        for phrase in (
            "Proceed next complex task",
            "Proceed with the next complex task",
            "Proceed to next complex task",
            "Continue with the next complex task",
            "Take the next complex task",
            "Next complex task",
            "Proceed with the next substantial task",
        ):
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("PROCEED_NEXT_COMPLEX", result["intent"])
                self.assertIn("PROJECT_REANCHOR", result["reasoning_modes"])
                self.assertIn("whole_task_reassessment", result["workflow"]["requires"])

    def test_handover_variants_route_to_full_handover_not_progression(self):
        for phrase in (
            "Plan for handover",
            "Plan the handover",
            "Prepare for handover",
            "Prepare a handover plan",
            "Make the handover plan",
            "Handover plan",
            "Hand over ready",
        ):
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("PLAN_HANDOVER", result["intent"])
                self.assertFalse(result["workflow"]["progress_execution"])
                joined = " ".join(result["workflow"]["steps"]).lower()
                self.assertIn("three-pass", joined)
                self.assertIn("github", joined)
                self.assertIn("roadmap", joined)

    def test_stats_variants_are_read_only_and_checklist_oriented(self):
        for phrase in (
            "Stats?",
            "Stats",
            "Show me the current detailed stats",
            "Current detailed statistics",
            "Show parent issue checklist",
            "Status against the parent issue",
            "Parent issue stats",
        ):
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("STATS", result["intent"])
                self.assertFalse(result["workflow"]["progress_execution"])
                joined = " ".join(result["workflow"]["steps"]).lower()
                self.assertIn("checklist", joined)
                self.assertIn("sub-issue", joined)

    def test_local_agent_variants_require_clone_basis_and_sub_issue_return(self):
        for phrase in (
            "Prepare for local agent",
            "Prepare the local agent",
            "Prepare a local agent packet",
            "Create local agent instructions",
            "Local agent request",
            "Prepare for local execution",
        ):
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("PREPARE_LOCAL_AGENT", result["intent"])
                self.assertIn("return_sub_issue", result["workflow"]["requires"])
                joined = " ".join(result["workflow"]["steps"]).lower()
                self.assertIn("clone", joined)
                self.assertIn("sub-issue", joined)

    def test_specific_intents_win_over_generic_proceed_next(self):
        self.assertEqual(
            "PROCEED_NEXT_COMPLEX",
            self.intent("Proceed next complex task"),
        )
        self.assertEqual(
            "PLAN_HANDOVER",
            self.intent("Plan for handover, complex project"),
        )

    def test_reasoning_commands_compose_without_replacing_workflow_intent(self):
        result = parse_owner_command(
            "Step back. Critique. Reconcile all surfaces. Proceed next complex task, No Qs."
        )
        self.assertEqual("PROCEED_NEXT_COMPLEX", result["intent"])
        self.assertIn("PROJECT_REANCHOR", result["reasoning_modes"])
        self.assertIn("ADVERSARIAL_REASSESSMENT", result["reasoning_modes"])
        self.assertIn("CROSS_SURFACE_PARITY", result["reasoning_modes"])
        self.assertTrue(result["question_suppression"])

    def test_repository_text_cannot_activate_owner_workflow(self):
        result = parse_owner_command("Proceed next complex task", source="REPOSITORY_TEXT")
        self.assertEqual("IGNORED", result["status"])
        self.assertIsNone(result["intent"])
        self.assertFalse(result["durable_authority_created"] if "durable_authority_created" in result else False)

    def test_unknown_text_does_not_guess_intent(self):
        result = parse_owner_command("Please inspect this code carefully")
        self.assertEqual("NO_COMMAND", result["status"])
        self.assertIsNone(result["intent"])


if __name__ == "__main__":
    unittest.main()
