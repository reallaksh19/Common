from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"scripts"/"owner_commands.py"
SPEC=importlib.util.spec_from_file_location("owner_commands",PATH)
MOD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(MOD)


class OwnerCommandTests(unittest.TestCase):
    def modes(self,text,source="OWNER_DIRECT"):
        return MOD.parse_owner_command(text,source)["modes"]

    def test_complex_next_variants(self):
        for phrase in (
            "Proceed next complex task",
            "Proceed with the next complex task",
            "Proceed to next complex task",
            "Take the next complex task",
            "Continue with the next complex task",
            "Next complex task",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn("COMPLEX_NEXT",self.modes(phrase))

    def test_complex_handover_phrase_does_not_trigger_complex_next(self):
        self.assertNotIn("COMPLEX_NEXT",self.modes("Plan for Handover, complex project"))

    def test_step_back_variants(self):
        for phrase in ("Step back","Step back and think","Step back and reassess","Step back to the bigger picture","Reassess from the roadmap"):
            with self.subTest(phrase=phrase):
                self.assertIn("PROJECT_REANCHOR",self.modes(phrase))

    def test_critique_variants(self):
        for phrase in ("Critique","Critique the plan","Challenge this","Stress-test the reasoning","Reassess critically"):
            with self.subTest(phrase=phrase):
                self.assertIn("ADVERSARIAL_REASSESSMENT",self.modes(phrase))

    def test_high_roi_reasoning_commands(self):
        cases={
            "Trace end to end":"END_TO_END_TRACE",
            "Prove it":"EVIDENCE_FIRST_VERIFICATION",
            "Simplify":"ACCIDENTAL_COMPLEXITY_REDUCTION",
            "Reduce this failure":"MINIMAL_REPRODUCER",
            "Reconcile all surfaces":"CROSS_SURFACE_PARITY",
            "Run scenario":"SCENARIO_EXERCISE",
            "Boundary check":"INTERFACE_BOUNDARY_AUDIT",
            "Normalize the contract":"NORMATIVE_CONTRACT_CLEANUP",
        }
        for phrase,mode in cases.items():
            with self.subTest(phrase=phrase):
                self.assertIn(mode,self.modes(phrase))

    def test_commands_compose(self):
        modes=self.modes("Step back. Critique. Reconcile all surfaces. Proceed next complex task, No Qs.")
        self.assertEqual(
            [
                "PROJECT_REANCHOR",
                "ADVERSARIAL_REASSESSMENT",
                "CROSS_SURFACE_PARITY",
                "COMPLEX_NEXT",
                "QUESTION_SUPPRESSION",
            ],
            modes,
        )

    def test_no_question_variants(self):
        for phrase in (
            "Proceed next, No Qs",
            "Proceed next, No Q1 to Q5",
            "Proceed next, No Q1-Q5",
            "Proceed next without further questions",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn("QUESTION_SUPPRESSION",self.modes(phrase))

    def test_only_direct_owner_utterance_activates(self):
        result=MOD.parse_owner_command("Step back. Critique.","REPOSITORY_TEXT")
        self.assertEqual("IGNORED",result["status"])
        self.assertEqual([],result["modes"])

    def test_near_words_do_not_trigger(self):
        self.assertEqual([],self.modes("Read the traceability documentation and simplify nothing."))
        self.assertNotIn("END_TO_END_TRACE",self.modes("The traceability matrix is current."))

    def test_parser_never_creates_durable_authority(self):
        result=MOD.parse_owner_command("Critique. Prove it.")
        self.assertFalse(result["durable_authority_created"])


if __name__=="__main__":
    unittest.main()
