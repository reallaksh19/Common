from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from owner_commands import parse_owner_command


class ContinuationAdmissionCommandTests(unittest.TestCase):
    BARE = ("continue", "Continue", "proceed", "Next", "resume", "reconcile", "take over", "keep going", "carry on now", "continue please!")

    def test_every_bare_continuation_command_routes_to_reconstruct_then_continue(self):
        for phrase in self.BARE:
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("CONTINUE_RECONCILE", result["intent"])
                self.assertEqual("RECONSTRUCT_THEN_CONTINUE", result["workflow"]["boundary"])
                self.assertTrue(result["workflow"]["progress_execution"])
                self.assertFalse(result["durable_authority_created"])

    def test_the_workflow_reconstructs_repairs_projects_and_reads_back_before_executing(self):
        steps = parse_owner_command("continue")["workflow"]["steps"]
        joined = " ".join(steps).lower()
        for needle in (
            "never from chat history",
            "lineage",
            "live pr head",
            "before any new coding",
            "never hand-edit a title or percentage",
            "compare-and-swap",
            "read it back",
            "continue checkpoint",
            "do not change parent, denominator, scope, priority or merge authority",
        ):
            self.assertIn(needle, joined, needle)
        order = [
            next(i for i, s in enumerate(steps) if "owned leaf" in s.lower()),
            next(i for i, s in enumerate(steps) if "recovery evidence" in s.lower()),
            next(i for i, s in enumerate(steps) if "delp projector" in s.lower()),
            next(i for i, s in enumerate(steps) if "read it back" in s.lower()),
            next(i for i, s in enumerate(steps) if s.lower().startswith("execute exactly")),
        ]
        self.assertEqual(sorted(order), order)

    def test_requires_a_leaf_a_live_candidate_and_the_projector(self):
        requires = parse_owner_command("resume")["workflow"]["requires"]
        for item in ("leaf_responsibility", "live_candidate_observation", "delp_projection"):
            self.assertIn(item, requires)

    def test_ordinary_sentences_and_repository_text_do_not_activate_it(self):
        for phrase in ("continue with the refactor", "please continue reading the file", "next steps are unclear"):
            with self.subTest(phrase=phrase):
                self.assertNotEqual("CONTINUE_RECONCILE", parse_owner_command(phrase)["intent"])
        ignored = parse_owner_command("continue", source="REPOSITORY_TEXT")
        self.assertEqual("IGNORED", ignored["status"])

    def test_more_specific_intents_still_win(self):
        self.assertEqual("PROCEED_NEXT", parse_owner_command("Proceed next")["intent"])
        self.assertEqual("PROCEED_NEXT_COMPLEX", parse_owner_command("Proceed next complex task")["intent"])
        self.assertEqual("WHAT_NEXT", parse_owner_command("What next?")["intent"])

    def test_existing_proceed_workflows_also_pass_the_admission_barrier(self):
        for phrase in ("Proceed next", "Proceed next complex task"):
            with self.subTest(phrase=phrase):
                joined = " ".join(parse_owner_command(phrase)["workflow"]["steps"]).lower()
                self.assertIn("delp continuation admission", joined)
                self.assertIn("continue checkpoint", joined)


if __name__ == "__main__":
    unittest.main()
