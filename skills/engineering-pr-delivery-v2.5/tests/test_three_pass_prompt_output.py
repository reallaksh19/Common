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

GOOD = f"""# SCHEMA EXECUTION HANDSHAKE

PROTOCOL REVISION:
TPG-3P-2026-09-21-R9

GENERATOR MODE:
THREE_PASS_ONLY

SCHEMA FETCH STATUS:
LIVE_THIS_RUN

SCHEMA CONTENT SHA:
{SHA}

HANDSHAKE STATUS:
PASS

# SCHEMA BASIS

PROTOCOL REVISION:
TPG-3P-2026-09-21-R9

GENERATOR MODE:
THREE_PASS_ONLY

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
USER INTENT:
audit the exact issue and then implement the smallest justified authorized action
INTENT TYPE:
ANALYZE_THEN_ACT
AUTHORIZED ACTIONS:
update the target artifact and verify the result
INTENT BOUNDARY:
do not expand beyond the issue
INTENT COMPLETION TEST:
the justified action is performed and verified
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
ROADMAP SYNTHESIS QUESTION:
what the relevant roadmap should preserve, revise, add, defer, or remove
TECHNICAL PROOF QUESTION:
which falsifier and quantitative or executable oracle proves a material technical gap
INTENT EXECUTION QUESTION:
how to fulfill the authorized action after comparison
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
INTENT-FIDELITY GATE:
PASS — analysis leads to authorized execution
ARTIFACT-ERASURE GATE:
PASS — artifact form not required
CURRENT-VOCABULARY GATE:
PASS — clean
PROMPT-1 OBJECT GATE:
PASS — correct object
HUMAN-Q-LABEL GATE:
PASS — no machine labels
PROMPT-1 REPOSITORY-IDENTITY GATE:
PASS — repository identity absent from Prompt 1
HUMAN-IMMERSION GATE:
PASS — human/domain scenario only
PROMPT-3 FREEDOM GATE:
PASS — artifact may close
PROMPT-3 ROADMAP-SYNTHESIS GATE:
PASS — roadmap is a revisable hypothesis, not the destination
PROMPT-3 TECHNICAL-PROOF GATE:
PASS — material technical changes require a falsifier and claim-specific proof
COMPLEX Q1–Q5 COVERAGE:
PASS — N/A when OFF
MODE-ISOLATION GATE:
PASS — no extra protocol stage

## PROMPT 1 — IMAGINE

Think independently about the specific unresolved domain problem.

## PROMPT 2 — UNDERSTAND

Inspect current reality.

## PROMPT 3 — REVALIDATE AND MOVE FORWARD

Use the actual Prompt-1 and Prompt-2 outputs; retrieve or explicitly regenerate a missing result rather than inventing it.
Treat Prompt-1 as the independent baseline, not immutable truth; verified evidence may revise it.
STEP BACK — inspect the relevant roadmap/task landscape and ownership boundaries; widen understanding, not ownership.
RECONCILE — compare the baseline, verified reality, and the roadmap; state the independent current gap before inherited candidate solutions are considered.
CRITIQUE THE CLAIM — define a GAP WITNESS and DISPROOF CONDITION, require quantitative or executable proof, try the stronger case with the existing model first, and withdraw or narrow architecture that proves unnecessary.
A PROBE / EVIDENCE TASK may investigate an unproved hypothesis without admitting the hypothesized capability as product scope.
DECIDE — preserve, revise, add, defer, remove, or leave unchanged; require positive evidence for narrowing, removal, closure, or ownership transfer and choose the smallest evidence-supported move.
At completion report:
THREE_PASS_REASONING_STATUS: THREE_PASS_COMPLETE
FOLLOW_ON_QUALIFICATION_QUESTION_SET: NOT_APPLICABLE
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
        bad = GOOD.replace(
            "INDEPENDENT WORK PRODUCT:\ntransparent reconstruction and comparison\n",
            "",
        )
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(
            any("INDEPENDENT WORK PRODUCT:" in e for e in errors),
            errors,
        )

    def test_no_witness_may_be_explicit(self):
        no_witness = GOOD.replace("PROBLEM WITNESS TYPE:\nbenchmark", "PROBLEM WITNESS TYPE:\nNONE")
        self.assertEqual(MOD.validate_text(no_witness, SHA), [])

    def test_wrong_generator_mode_is_rejected(self):
        bad = GOOD.replace("GENERATOR MODE:\nTHREE_PASS_ONLY", "GENERATOR MODE:\nENGINEERING_DELIVERY")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("GENERATOR MODE must be THREE_PASS_ONLY" in e for e in errors))

    def test_machine_q_labels_are_rejected(self):
        bad = GOOD.replace(
            "Think independently about the specific unresolved domain problem.",
            "Q1 — PRODUCTION_PATH\nrequired_output_keys: production_entrypoint, authority_source",
        )
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(
            any("machine/taxonomy surface language" in e for e in errors),
            errors,
        )

    def test_missing_handshake_is_rejected(self):
        bad = GOOD[GOOD.index("# SCHEMA BASIS"):]
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("SCHEMA EXECUTION HANDSHAKE" in e for e in errors), errors)

    def test_wrong_protocol_revision_is_rejected(self):
        bad = GOOD.replace("TPG-3P-2026-09-21-R9", "TPG-STALE-REVISION", 1)
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("PROTOCOL REVISION" in e for e in errors), errors)

    def test_handshake_basis_sha_mismatch_is_rejected(self):
        other = "0" * 40
        bad = GOOD.replace(f"SCHEMA CONTENT SHA:\n{SHA}", f"SCHEMA CONTENT SHA:\n{other}", 1)
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("does not match expected current SHA" in e or "SHA must match" in e for e in errors), errors)

    def test_compatibility_wrapper_uses_standalone_validator(self):
        self.assertEqual(MOD.EXPECTED_PROTOCOL_REVISION, "TPG-3P-2026-09-21-R9")
        canonical = ROOT.parent / "three-pass-prompt-generator" / "validate.py"
        self.assertTrue(canonical.exists(), canonical)

    def test_user_intent_is_required(self):
        bad = GOOD.replace("USER INTENT:\naudit the exact issue and then implement the smallest justified authorized action\n", "")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("USER INTENT" in e for e in errors), errors)

    def test_intent_fidelity_gate_must_pass(self):
        bad = GOOD.replace("INTENT-FIDELITY GATE:\nPASS — analysis leads to authorized execution", "INTENT-FIDELITY GATE:\nFAIL — action disappeared")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("INTENT-FIDELITY GATE must PASS" in e for e in errors), errors)

    def test_intent_boundary_is_required(self):
        bad = GOOD.replace("INTENT BOUNDARY:\ndo not expand beyond the issue\n", "")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("preflight missing INTENT BOUNDARY:" in e for e in errors), errors)

    def test_prompt3_requires_three_pass_terminal_disposition(self):
        bad = GOOD.replace("THREE_PASS_REASONING_STATUS: THREE_PASS_COMPLETE\nFOLLOW_ON_QUALIFICATION_QUESTION_SET: NOT_APPLICABLE", "")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("THREE_PASS_COMPLETE terminal disposition" in e for e in errors), errors)

    def test_prompt3_requires_roadmap_synthesis(self):
        bad = GOOD.replace("roadmap/task landscape", "surrounding context").replace("the roadmap", "the current plan")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("roadmap/task landscape" in e for e in errors), errors)

    def test_prompt3_requires_ownership_discipline(self):
        bad = GOOD.replace("STEP BACK — inspect the relevant roadmap/task landscape and ownership boundaries; widen understanding, not ownership.\n", "STEP BACK — inspect the relevant roadmap/task landscape.\n")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("ownership" in e for e in errors), errors)

    def test_prompt3_requires_cold_start_context_integrity(self):
        bad = GOOD.replace("Use the actual Prompt-1 and Prompt-2 outputs; retrieve or explicitly regenerate a missing result rather than inventing it.\n", "Use Prompt-1 and Prompt-2.\n")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("cold-start handling" in e for e in errors), errors)

    def test_prompt3_treats_prompt1_as_revisable_baseline(self):
        bad = GOOD.replace("Treat Prompt-1 as the independent baseline, not immutable truth; verified evidence may revise it.\n", "Treat Prompt-1 as the independent baseline.\n")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("revise the Prompt-1 baseline" in e for e in errors), errors)

    def test_prompt3_requires_independent_gap_before_candidates(self):
        bad = GOOD.replace("state the independent current gap before inherited candidate solutions are considered", "review inherited candidate solutions")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("current gap independently" in e for e in errors), errors)

    def test_prompt3_requires_gap_witness(self):
        bad = GOOD.replace("define a GAP WITNESS and DISPROOF CONDITION, ", "define a DISPROOF CONDITION, ")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("gap witness" in e for e in errors), errors)

    def test_prompt3_requires_disproof_condition(self):
        bad = GOOD.replace("define a GAP WITNESS and DISPROOF CONDITION, ", "define a GAP WITNESS, ")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("disprove the proposed architecture" in e for e in errors), errors)

    def test_prompt3_requires_quantitative_or_executable_proof(self):
        bad = GOOD.replace("require quantitative or executable proof, ", "")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("quantitative or executable" in e for e in errors), errors)

    def test_prompt3_requires_existing_model_first(self):
        bad = GOOD.replace("try the stronger case with the existing model first, and ", "")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("existing/current model first" in e for e in errors), errors)

    def test_prompt3_requires_withdrawal_when_architecture_unnecessary(self):
        bad = GOOD.replace("and withdraw or narrow architecture that proves unnecessary", "")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("proposed architecture is not justified" in e for e in errors), errors)

    def test_prompt3_distinguishes_probe_from_capability_admission(self):
        bad = GOOD.replace("A PROBE / EVIDENCE TASK may investigate an unproved hypothesis without admitting the hypothesized capability as product scope.\n", "")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("probe/evidence task from capability admission" in e for e in errors), errors)

    def test_prompt3_requires_positive_evidence_for_removal(self):
        bad = GOOD.replace("require positive evidence for narrowing, removal, closure, or ownership transfer and ", "")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("positive evidence" in e for e in errors), errors)

    def test_prompt3_keywords_do_not_replace_behavior(self):
        bad = GOOD.replace(
            "CRITIQUE THE CLAIM — define a GAP WITNESS and DISPROOF CONDITION, require quantitative or executable proof, try the stronger case with the existing model first, and withdraw or narrow architecture that proves unnecessary.\n",
            "CRITIQUE THE CLAIM — think critically about the proposed architecture.\n",
        )
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("gap witness" in e for e in errors), errors)
        self.assertTrue(any("disprove the proposed architecture" in e for e in errors), errors)
        self.assertTrue(any("existing/current model first" in e for e in errors), errors)

    def test_prompt1_rejects_repository_identity_even_inside_prohibition(self):
        bad = GOOD.replace("Think independently about the specific unresolved domain problem.", "Think independently about the specific unresolved domain problem. Do not refer to the repository reallaksh19/Common.")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("repository leak score must be 0" in e for e in errors), errors)

    def test_prompt1_rejects_generic_repository_deferral_formula(self):
        bad = GOOD.replace("Think independently about the specific unresolved domain problem.", "Think independently about the specific unresolved domain problem. Do not inspect the repository before answering.")
        errors = MOD.validate_text(bad, SHA)
        self.assertTrue(any("repository leak score must be 0" in e for e in errors), errors)

    def test_prompt1_repository_leak_formula_rejects_multiple_forms(self):
        variants = (
            "Do not refer to the repository reallaksh19/Common.",
            "Without opening the repo, reason about the problem.",
            "Ignore the current GitHub repository before answering.",
            "Do not inspect https://github.com/example/repo before answering.",
        )
        for phrase in variants:
            bad = GOOD.replace("Think independently about the specific unresolved domain problem.", f"Think independently about the specific unresolved domain problem. {phrase}")
            errors = MOD.validate_text(bad, SHA)
            self.assertTrue(any("repository leak score must be 0" in e for e in errors), (phrase, errors))

if __name__ == "__main__":
    unittest.main()
