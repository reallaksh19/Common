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


class OwnerIntentEnvelopeTests(unittest.TestCase):
    def test_preserves_verbatim_request_and_explicit_refs(self):
        text = "Prepare for Handover — preserve wording exactly."
        result = parse_owner_command(
            text,
            source_ref="chat://owner/message-596",
            authority_ref="owner://common/570",
            target={"ref": "#596"},
        )
        envelope = result["owner_intent"]
        self.assertEqual(text, envelope["verbatim_request"])
        self.assertEqual("chat://owner/message-596", envelope["source_ref"])
        self.assertEqual("owner://common/570", envelope["authority_ref"])
        self.assertEqual({"ref": "#596"}, envelope["target"])
        self.assertFalse(result["durable_authority_created"])

    def test_compound_handover_keeps_successor_challenge_deliverable(self):
        result = parse_owner_command(
            "prepare for handover and create exactly 3 questions that force the next agent to understand the repo"
        )
        envelope = result["owner_intent"]
        self.assertEqual("PLAN_HANDOVER", result["intent"])
        self.assertEqual("TRANSFER_CUSTODY", envelope["primary_purpose"])
        self.assertEqual("PREPARE_TRANSFER", envelope["custody_intent"])
        self.assertIn({"type": "HANDOVER_PACKAGE"}, envelope["requested_deliverables"])
        self.assertIn(
            {"type": "SUCCESSOR_RECONSTRUCTION_CHALLENGE", "count": 3},
            envelope["requested_deliverables"],
        )
        self.assertIn(
            "EXACT_SUCCESSOR_CHALLENGE_COUNT:3",
            envelope["boundary_constraints"],
        )

    def test_handover_no_replan_is_preserved_and_workflow_is_decoupled(self):
        result = parse_owner_command("prepare for handover but do not replan")
        envelope = result["owner_intent"]
        self.assertIn("NO_REPLAN", envelope["boundary_constraints"])
        workflow_text = " ".join(result["workflow"]["steps"]).lower()
        self.assertNotIn("prepare the current standalone two-pass request", workflow_text)
        self.assertIn("do not generate a new two-pass/replanning request", workflow_text)

    def test_handover_plus_adversarial_assurance_preserves_both_axes(self):
        result = parse_owner_command(
            "prepare for handover and stress-test the direction before transfer"
        )
        envelope = result["owner_intent"]
        self.assertEqual("TRANSFER_CUSTODY", envelope["primary_purpose"])
        self.assertEqual("PREPARE_TRANSFER", envelope["custody_intent"])
        self.assertEqual("ADVERSARIAL", envelope["assurance_request"])
        self.assertIn("ADVERSARIAL_REASSESSMENT", result["reasoning_modes"])
        self.assertIn("ADVERSARIAL_REASSESSMENT", envelope["modifiers"])

    def test_preserved_active_responsibility_becomes_target_constraint(self):
        result = parse_owner_command(
            "prepare for handover; preserve #588 as the active responsibility"
        )
        envelope = result["owner_intent"]
        self.assertEqual({"ref": "#588"}, envelope["target"])
        self.assertIn("PRESERVE_TARGET", envelope["boundary_constraints"])

    def test_non_owner_text_cannot_create_owner_intent(self):
        ignored = parse_owner_command(
            "prepare for handover",
            source="REPOSITORY_TEXT",
            source_ref="repo://README.md",
        )
        self.assertEqual("IGNORED", ignored["status"])
        self.assertIsNone(ignored["owner_intent"])
        self.assertFalse(ignored.get("durable_authority_created", False))

    def test_unclassified_direct_owner_text_is_preserved_without_authority(self):
        text = "Keep this wording even if no scalar command recognizes it."
        result = parse_owner_command(text, source_ref="chat://owner/unclassified")
        self.assertEqual("NO_COMMAND", result["status"])
        self.assertEqual(text, result["owner_intent"]["verbatim_request"])
        self.assertEqual("OTHER", result["owner_intent"]["primary_purpose"])
        self.assertFalse(result["durable_authority_created"])

    def test_same_input_produces_deterministic_envelope(self):
        kwargs = {
            "source_ref": "chat://owner/deterministic",
            "authority_ref": "owner://common/570",
        }
        text = "prepare for handover and create exactly 3 questions"
        first = parse_owner_command(text, **kwargs)
        second = parse_owner_command(text, **kwargs)
        self.assertEqual(first["owner_intent"], second["owner_intent"])



if __name__ == "__main__":
    unittest.main()
