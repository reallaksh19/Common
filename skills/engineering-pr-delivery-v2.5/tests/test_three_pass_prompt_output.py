from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_three_pass_prompt_output.py"
SPEC = importlib.util.spec_from_file_location("three_pass_validator", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)

SHA = "a" * 40

GOOD = f"""# SCHEMA BASIS

SCHEMA SOURCE:
canonical

SCHEMA REF:
main

SCHEMA CONTENT SHA:
{SHA}

SCHEMA FETCH STATUS:
LIVE_THIS_RUN

SCHEMA COMPATIBILITY:
PASS

LEGACY-SIGNATURE GATE:
PASS — clean

# LOT 1 — ISSUE_TASK: Example issue

## PREFLIGHT RECORD

LOT:
1
USER-REQUESTED LEVEL:
ISSUE_TASK
USER-REQUESTED TARGET:
Example issue
LEVEL INTERPRETATION:
stay issue-level
TARGET TITLE / SURFACE:
Example issue
TARGET LINK:
https://example.invalid/1
PARENT REPOSITORY / SYSTEM:
example/repo
REPOSITORY / SYSTEM LINK:
https://example.invalid/repo
REQUEST MODE:
REVIEW
COMPLEX MODE:
OFF
CURRENT ARTIFACT FORM:
issue
CURRENT STATED ANSWER / IMPLEMENTATION:
current proposal
CURRENT-STATE FACTS:
facts for pass 2
CURRENT ANSWER QUARANTINE:
today's option set
TARGET ANCHORS:
named domain
PROBLEM WITNESS TYPE:
benchmark
PROBLEM WITNESS SOURCE:
retained case
PROBLEM WITNESS PAYLOAD:
real inputs and reported output
WITNESS CLAIM(S) TO REPRODUCE:
reported comparison
WHY THIS WITNESS EXPOSES THE ISSUE:
working the case reveals the issue
WITNESS INTERPRETATION QUARANTINE:
current recommendation
INDEPENDENT WORK PRODUCT:
transparent reconstruction and comparison
WHY NOW:
a defined lifecycle hand-off created this exact issue
STARTING PREMISE:
the issue starts from a changed programme state
RESPONSIBLE ACTOR / JOB:
owner resolving this exact issue
OWNED QUESTION:
what this issue specifically must decide
NON-GOALS / OWNERSHIP BOUNDARY:
do not absorb parent or sibling work
ISSUE DIFFERENTIATOR:
distinct from its parent and nearest sibling
PROBLEM KERNEL:
specific unresolved issue
UNDERLYING HUMAN PROBLEM:
specific problem
HUMAN OUTCOME:
useful outcome
GENUINE CONSTRAINTS:
real constraint
EXPERTISE:
domain expert
IMAGINATION OBJECT:
independent handling of the problem
REALITY OBJECT:
current truth
COMPARISON QUESTION:
what remains now
HANDOVER DESTINATION:
understanding for successor
LOT/LEVEL BOUNDARY GATE:
PASS — correct level
SPECIFICITY-FLOOR GATE:
PASS — specific
TASK-CONTRACT FIDELITY GATE:
PASS — exact assignment survives
NEIGHBOUR-SEPARATION GATE:
PASS — not parent/sibling
PROBLEM-WITNESS SELECTION GATE:
PASS — concrete benchmark selected
WITNESS-INDEPENDENCE GATE:
PASS — reported result is reproduced, not inherited
KERNEL-COVERAGE GATE:
PASS — kernel survives
SAME-ISSUE IDENTITY GATE:
PASS — recognisable
ANSWER-EXCLUSION GATE:
PASS — answer hidden
ARTIFACT-ERASURE GATE:
PASS — artifact form not required
CURRENT-VOCABULARY GATE:
PASS — clean
PROMPT-1 OBJECT GATE:
PASS — correct object
HUMAN-IMMERSION GATE:
PASS — human/domain scenario only
PROMPT-3 FREEDOM GATE:
PASS — artifact may close
COMPLEX Q1–Q5 COVERAGE:
PASS — N/A when OFF
QSET-SEPARATION GATE:
PASS — no formal relay QSET

## PROMPT 1 — IMAGINE

Think independently about the specific unresolved domain problem.

## PROMPT 2 — UNDERSTAND

Inspect current reality.

## PROMPT 3 — REVALIDATE AND MOVE FORWARD

First determine today's remaining problem, then decide the artifact's disposition.
"""

STALE = """Reworked.

# PROMPT 1 — IMAGINE

The register is the thing you are imagining.

# PROMPT 2 — UNDERSTAND

Inspect it.

# PROMPT 3 — REVALIDATE AND MOVE FORWARD

Produce the reconciled register.
"""


class ThreePassPromptOutputTests(unittest.TestCase):
    def test_current_shape_passes(self):
        self.assertEqual(MOD.validate_text(GOOD, SHA), [])

    def test_stale_register_path_is_rejected(self):
        errors = MOD.validate_text(STALE, SHA)
        joined = "\n".join(errors)
        self.assertIn("SCHEMA BASIS", joined)
        self.assertIn("legacy active signature", joined)
        self.assertIn("at least one '# LOT ...' section", joined)

    def test_wrong_schema_sha_is_rejected(self):
        errors = MOD.validate_text(GOOD, "b" * 40)
        self.assertTrue(any("does not match expected current SHA" in e for e in errors))


    def test_prompt1_method_language_is_rejected(self):
        bad = GOOD.replace(
            "Think independently about the specific unresolved domain problem.",
            "This answer will be used as a fixed independent reference in a later pass. Do not inspect the current repository before answering.",
        )
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("leaks generator/method language" in e for e in errors))

    def test_formal_qset_protocol_is_rejected(self):
        bad = GOOD + "\nQUALIFICATION GATE — ANSWER QSET Q1–Q5\nschema_version: relay-v2.5-question-set\n"
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("formal relay QSET/admission protocol" in e for e in errors))

    def test_issue_task_contract_is_required(self):
        bad = GOOD.replace("WHY NOW:", "WHY-NOT:")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("ISSUE_TASK missing WHY NOW:" in e for e in errors))

    def test_selected_witness_requires_work_product(self):
        bad = GOOD.replace("INDEPENDENT WORK PRODUCT:\ntransparent reconstruction and comparison", "INDEPENDENT WORK PRODUCT:\n")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("selected witness requires non-empty INDEPENDENT WORK PRODUCT:" in e for e in errors))

    def test_no_witness_may_be_explicit(self):
        no_witness = GOOD.replace("PROBLEM WITNESS TYPE:\nbenchmark", "PROBLEM WITNESS TYPE:\nNONE")
        self.assertEqual(MOD.validate_text(no_witness, SHA), [])

if __name__ == "__main__":
    unittest.main()
