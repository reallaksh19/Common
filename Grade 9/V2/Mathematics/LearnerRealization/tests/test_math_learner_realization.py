#!/usr/bin/env python3
"""Falsifier suite for the learner mathematical realization layer.

The reference corpus is the *correct* artifact. Every falsifier test mutates it in exactly
one way and requires an exact named gate. The mutations are the ones the PR #323 stress
test actually produced: an operation named but not demonstrated, a route that could be
transplanted onto an unrelated item, an authoring obligation left in the learner surface,
an answer replaced by a self-check, a transformation with no invariant witness.
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
sys.path[:0] = [str(MATH / "MathTypesetting" / "engine"), str(PHASE / "engine"),
                str(PHASE / "fixtures")]

from math_expression import GlyphRegistry, num, op, radical, seq, sym, txt  # noqa: E402
from learner_copy import (  # noqa: E402
    approved_labels,
    audit_learner_copy,
    banned_tokens,
    load_policy,
    warm_title,
)
from learner_realization import (  # noqa: E402
    audit_realizations,
    load,
    prose_text,
    realization_texts,
    seal_realization,
    validate_answer_custody,
    validate_realization,
)

FIXTURE = load(PHASE / "fixtures" / "math-reference-realizations.fixture.json")
ROLES = load(PHASE / "registry" / "math-realization-role-registry.json")
POLICY = load(PHASE / "policies" / "math-learner-realization-policy.json")
COPY_REGISTRY = load(PHASE / "registry" / "math-learner-copy-registry.json")
COPY_POLICY = load(MATH / "LearnerProduct" / "policies"
                   / "math-learner-language-policy.json")
REG = GlyphRegistry()


def store() -> dict:
    out = {}
    for directory in (PHASE / "contracts", MATH / "MathTypesetting" / "contracts"):
        for p in sorted(directory.glob("*.schema.json")):
            doc = json.loads(p.read_text(encoding="utf-8"))
            out[doc["$id"]] = doc
    return out


STORE = store()


def validator(schema_id: str) -> Draft202012Validator:
    root = STORE[schema_id]
    return Draft202012Validator(root, resolver=RefResolver.from_schema(root, store=STORE))


def corpus() -> list[dict]:
    return copy.deepcopy(FIXTURE["realizations"])


def item(realizations: list[dict], ref: str) -> dict:
    return next(r for r in realizations if r["item_ref"] == ref)


def reseal(realization: dict) -> dict:
    out = seal_realization(realization)
    realization.clear()
    realization.update(out)
    return realization


class RealizationPositive(unittest.TestCase):
    def test_every_realization_validates_against_the_contract(self):
        v = validator("math-learner-realization.schema.json")
        for realization in corpus():
            with self.subTest(item=realization["item_ref"]):
                v.validate(realization)

    def test_every_route_state_validates_against_the_contract(self):
        v = validator("math-route-state.schema.json")
        for realization in corpus():
            for step in realization["derivation"]:
                with self.subTest(item=realization["item_ref"], step=step["step_id"]):
                    v.validate(step)

    def test_every_answer_custody_validates_against_the_contract(self):
        v = validator("math-answer-custody.schema.json")
        for realization in corpus():
            with self.subTest(item=realization["item_ref"]):
                v.validate(realization["answer_custody"])

    def test_audit_passes_on_the_reference_corpus(self):
        audit = audit_realizations(corpus(),
                                  parameterized_items=FIXTURE["parameterized_items"])
        self.assertEqual(audit["status"], "PASS")
        self.assertEqual(audit["realization_count"], 4)
        self.assertEqual(audit["typesetting_audit"]["status"], "PASS")

    def test_exit_gate_two_topics_show_real_substitution_and_typeset_math(self):
        """Issue #358 exit gate: a real worked instance renders proper math typesetting
        and demonstrates the actual substitution, for at least two stress-tested topics."""
        worked = [r for r in corpus() if r["role"] == "WORKED"]
        self.assertGreaterEqual(len({r["topic_ref"] for r in worked}), 2)
        for realization in worked:
            substituted = [s for s in realization["derivation"]
                           if s.get("substitution") is not None]
            self.assertTrue(substituted, realization["item_ref"])
            text = "\n".join(realization_texts(realization, REG))
            self.assertNotIn("sqrt", text.lower())
            self.assertNotIn("^", text)
        surd = item(corpus(), "NS-W1")
        statement = prose_text(surd["statement"], REG)
        self.assertIn("√7", statement)
        poly = item(corpus(), "PY-W1")
        self.assertIn("x³ − 2x² − x + 2", prose_text(poly["statement"], REG))

    def test_exit_gate_one_transformation_chain_carries_an_invariant_witness(self):
        witnesses = [s["equivalence_witness"] for r in corpus() for s in r["derivation"]
                     if s.get("equivalence_witness")]
        self.assertGreaterEqual(len(witnesses), 1)
        self.assertTrue(any(w["preserved_invariant"] == "SOLUTION_SET" for w in witnesses))
        for w in witnesses:
            self.assertTrue(w["precondition"].strip())

    def test_exit_gate_no_learner_question_lacks_an_answer_artifact(self):
        for realization in corpus():
            self.assertEqual(
                validate_answer_custody(realization["answer_custody"], reg=REG), [])

    def test_sufficiency_verdict_is_a_first_class_state(self):
        parameterized = item(corpus(), "LE-I1")
        states = [s for s in parameterized["derivation"] if s["role"] == "CHECK_SUFFICIENCY"]
        self.assertEqual(len(states), 1)
        self.assertIn(states[0]["sufficiency"]["status"],
                      POLICY["sufficiency_policy"]["states"])

    def test_audit_is_deterministic(self):
        a = audit_realizations(corpus(), parameterized_items=FIXTURE["parameterized_items"])
        b = audit_realizations(corpus(), parameterized_items=FIXTURE["parameterized_items"])
        self.assertEqual(a["corpus_digest"], b["corpus_digest"])

    def test_policy_declares_every_falsifier_the_registry_names(self):
        for code in ROLES["falsifiers"]:
            self.assertIn(code, POLICY["falsifiers"], code)


class RealizationFalsifiers(unittest.TestCase):
    def expect(self, code: str, realizations: list[dict], **kwargs):
        with self.assertRaises(ValueError) as ctx:
            audit_realizations(realizations,
                               parameterized_items=kwargs.pop(
                                   "parameterized_items", FIXTURE["parameterized_items"]),
                               **kwargs)
        self.assertIn(code, str(ctx.exception), f"expected {code}, got {ctx.exception}")

    # 1 — the exact Theory-of-Equations v2 defect
    def test_MATH_OPERATION_NAMED_BUT_NOT_DEMONSTRATED(self):
        bad = corpus()
        target = item(bad, "PY-W1")
        step = next(s for s in target["derivation"] if s["step_id"] == "S5")
        step["substitution"] = None
        step["output_state"] = copy.deepcopy(step["input_state"])
        reseal(target)
        self.expect("MATH_OPERATION_NAMED_BUT_NOT_DEMONSTRATED", bad)

    # 2
    def test_MATH_OPERATION_NAMED_BUT_NOT_DEMONSTRATED_on_generic_justification(self):
        bad = corpus()
        target = item(bad, "NS-W1")
        step = next(s for s in target["derivation"] if s["step_id"] == "S5")
        step["operation"]["rule_or_justification"] = "Apply the relevant formula as required."
        reseal(target)
        self.expect("MATH_OPERATION_NAMED_BUT_NOT_DEMONSTRATED", bad)

    # 3
    def test_LEARNER_STEP_WITHOUT_MATHEMATICAL_STATE_TRANSITION(self):
        bad = corpus()
        target = item(bad, "CG-G1")
        step = next(s for s in target["derivation"] if s["step_id"] == "S4")
        step["input_state"] = None
        reseal(target)
        self.expect("LEARNER_STEP_WITHOUT_MATHEMATICAL_STATE_TRANSITION", bad)

    # 4
    def test_WORKED_EXAMPLE_UNINSTANTIATED_on_authoring_obligation(self):
        bad = corpus()
        target = item(bad, "NS-W1")
        target["statement"] = [{"segment": "TEXT",
                                "text": "Author a new instance of the surd family."}]
        reseal(target)
        self.expect("WORKED_EXAMPLE_UNINSTANTIATED", bad)

    # 5
    def test_WORKED_EXAMPLE_UNINSTANTIATED_on_unresolved_template_token(self):
        bad = corpus()
        target = item(bad, "PY-W1")
        target["derivation"][0]["learner_explanation"] = \
            "You are given the cubic {polynomial} and asked about the factor."
        reseal(target)
        self.expect("WORKED_EXAMPLE_UNINSTANTIATED", bad)

    # 6
    def test_WORKED_EXAMPLE_UNINSTANTIATED_on_empty_derivation(self):
        bad = corpus()
        target = item(bad, "CG-G1")
        target["derivation"] = []
        with self.assertRaises(Exception):
            audit_realizations(bad)

    # 7 — RC-7: reasoning text that could be attached to any unrelated item
    def test_LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS_on_generic_prose(self):
        bad = corpus()
        target = item(bad, "LE-I1")
        for step in target["derivation"]:
            step["learner_explanation"] = "Carry out the algebra in the structured workspace."
        reseal(target)
        self.expect("LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS", bad)

    # 8 — the cross-item adversarial transplant
    def test_LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS_on_transplanted_prose(self):
        bad = corpus()
        donor = item(bad, "NS-W1")["derivation"][3]
        recipient = item(bad, "PY-W1")["derivation"][3]
        recipient["learner_explanation"] = donor["learner_explanation"]
        recipient["operation"]["rule_or_justification"] = \
            donor["operation"]["rule_or_justification"]
        reseal(item(bad, "PY-W1"))
        self.expect("LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS", bad)

    # 9
    def test_LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM_on_ungrounded_hint(self):
        bad = corpus()
        target = item(bad, "PY-W1")
        target["scaffold"]["H1"]["text"] = \
            "Think about what the suggested factor is telling you to test."
        reseal(target)
        self.expect("LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM", bad)

    # 10
    def test_LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM_on_anchor_absent_from_statement(self):
        bad = corpus()
        target = item(bad, "CG-G1")
        target["item_anchors"] = ["(7, 9)", "(4, 3)"]
        reseal(target)
        self.expect("LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM", bad)

    # 11
    def test_LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM_on_unresolved_hint_step(self):
        bad = corpus()
        target = item(bad, "NS-W1")
        target["scaffold"]["H2"]["derived_from_step_id"] = "S99"
        reseal(target)
        self.expect("LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM", bad)

    # 12
    def test_SCAFFOLD_DISCLOSES_SOLUTION(self):
        bad = corpus()
        target = item(bad, "LE-I1")
        target["scaffold"]["H1"]["text"] = \
            "The point (2, 1) forces k = 4, so substitute that straight away."
        reseal(target)
        self.expect("SCAFFOLD_DISCLOSES_SOLUTION", bad)

    # 13
    def test_EQUIVALENCE_TRANSFORMATION_WITHOUT_INVARIANT_WITNESS(self):
        bad = corpus()
        target = item(bad, "LE-I1")
        next(s for s in target["derivation"]
             if s["step_id"] == "S4")["equivalence_witness"] = None
        reseal(target)
        self.expect("EQUIVALENCE_TRANSFORMATION_WITHOUT_INVARIANT_WITNESS", bad)

    # 14
    def test_EQUIVALENCE_TRANSFORMATION_PRECONDITION_MISSING(self):
        bad = corpus()
        target = item(bad, "NS-W1")
        next(s for s in target["derivation"]
             if s["step_id"] == "S4")["equivalence_witness"]["precondition"] = "   "
        reseal(target)
        self.expect("EQUIVALENCE_TRANSFORMATION_PRECONDITION_MISSING", bad)

    # 15
    def test_EQUIVALENCE_TRANSFORMATION_WITHOUT_INVARIANT_WITNESS_when_nothing_changed(self):
        bad = corpus()
        target = item(bad, "NS-W1")
        witness = next(s for s in target["derivation"]
                       if s["step_id"] == "S4")["equivalence_witness"]
        witness["after_relation"] = copy.deepcopy(witness["before_relation"])
        reseal(target)
        self.expect("EQUIVALENCE_TRANSFORMATION_WITHOUT_INVARIANT_WITNESS", bad)

    # 16
    def test_SOLUTION_SET_NOT_PRESERVED_WITHOUT_CHECK(self):
        """Squaring both sides can add roots; declaring it reversible is the defect."""
        bad = corpus()
        target = item(bad, "LE-I1")
        witness = next(s for s in target["derivation"]
                       if s["step_id"] == "S4")["equivalence_witness"]
        witness["operation"] = "SQUARE_BOTH_SIDES"
        witness["reversible"] = True
        reseal(target)
        self.expect("SOLUTION_SET_NOT_PRESERVED_WITHOUT_CHECK", bad)

    # 17
    def test_SOLUTION_SET_NOT_PRESERVED_WITHOUT_CHECK_when_no_extraneous_check_is_given(self):
        bad = corpus()
        target = item(bad, "LE-I1")
        witness = next(s for s in target["derivation"]
                       if s["step_id"] == "S4")["equivalence_witness"]
        witness["operation"] = "SQUARE_BOTH_SIDES"
        witness["reversible"] = False
        witness["extraneous_root_check"] = None
        reseal(target)
        self.expect("SOLUTION_SET_NOT_PRESERVED_WITHOUT_CHECK", bad)

    # 18
    def test_PARAMETERIZED_ITEM_WITHOUT_SUFFICIENCY_CHECK(self):
        bad = corpus()
        target = item(bad, "LE-I1")
        target["derivation"] = [s for s in target["derivation"]
                                if s["role"] != "CHECK_SUFFICIENCY"]
        reseal(target)
        self.expect("PARAMETERIZED_ITEM_WITHOUT_SUFFICIENCY_CHECK", bad)

    # 19
    def test_LEARNER_QUESTION_WITHOUT_ANSWER(self):
        bad = corpus()
        target = item(bad, "NS-W1")
        target["answer_custody"]["final_answer"] = None
        reseal(target)
        self.expect("LEARNER_QUESTION_WITHOUT_ANSWER", bad)

    # 20
    def test_SELF_CHECK_SUBSTITUTED_FOR_ANSWER(self):
        bad = corpus()
        target = item(bad, "CG-G1")
        target["answer_custody"]["final_answer"] = None
        target["answer_custody"]["final_answer_prose"] = None
        target["answer_custody"]["quick_check"] = "Check that your midpoint looks sensible."
        reseal(target)
        self.expect("SELF_CHECK_SUBSTITUTED_FOR_ANSWER", bad)

    # 21
    def test_ANSWER_WITHOUT_VERIFICATION_when_not_executable(self):
        bad = corpus()
        target = item(bad, "PY-W1")
        target["answer_custody"]["independent_verification"]["executable"] = False
        reseal(target)
        self.expect("ANSWER_WITHOUT_VERIFICATION", bad)

    # 22
    def test_ANSWER_WITHOUT_VERIFICATION_when_generic(self):
        bad = corpus()
        target = item(bad, "PY-W1")
        target["answer_custody"]["independent_verification"]["statement"] = \
            "Check your answer before moving on."
        reseal(target)
        self.expect("ANSWER_WITHOUT_VERIFICATION", bad)

    # 23
    def test_ATTEMPT_PAGE_ANSWER_LEAKAGE(self):
        bad = corpus()
        target = item(bad, "CG-G1")
        target["statement"].append({"segment": "TEXT", "text": "The midpoint is M = (1, 3)."})
        reseal(target)
        self.expect("ATTEMPT_PAGE_ANSWER_LEAKAGE", bad)

    # 24
    def test_PROOF_PROMPT_WITHOUT_MODEL_PROOF(self):
        custody = copy.deepcopy(item(corpus(), "PY-W1")["answer_custody"])
        custody["answer_kind"] = "PROOF"
        custody["final_answer"] = None
        custody["model_proof_steps"] = []
        custody["final_answer_prose"] = "The result follows."
        failures = validate_answer_custody(custody, reg=REG)
        self.assertTrue(any(f.startswith("PROOF_PROMPT_WITHOUT_MODEL_PROOF")
                            for f in failures), failures)

    # 25
    def test_CONSTRUCTION_WITHOUT_VERIFICATION_CONDITIONS(self):
        custody = copy.deepcopy(item(corpus(), "CG-G1")["answer_custody"])
        custody["answer_kind"] = "CONSTRUCTION"
        custody["construction_verification_conditions"] = []
        failures = validate_answer_custody(custody, reg=REG)
        self.assertTrue(any(f.startswith("CONSTRUCTION_WITHOUT_VERIFICATION_CONDITIONS")
                            for f in failures), failures)

    # 26
    def test_MULTIPLE_VALID_ANSWERS_WITHOUT_ADMISSIBILITY_RULE(self):
        custody = copy.deepcopy(item(corpus(), "LE-I1")["answer_custody"])
        custody["answer_kind"] = "MULTIPLE_VALID"
        custody["acceptance_rule"] = None
        custody["admissible_answers"] = [num(4)]
        failures = validate_answer_custody(custody, reg=REG)
        self.assertTrue(any(f.startswith("MULTIPLE_VALID_ANSWERS_WITHOUT_ADMISSIBILITY_RULE")
                            for f in failures), failures)

    # 27
    def test_OPEN_RESPONSE_WITHOUT_ACCEPTANCE_CRITERIA(self):
        custody = copy.deepcopy(item(corpus(), "NS-W1")["answer_custody"])
        custody["answer_kind"] = "OPEN_RESPONSE"
        custody["acceptance_rule"] = None
        failures = validate_answer_custody(custody, reg=REG)
        self.assertTrue(any(f.startswith("OPEN_RESPONSE_WITHOUT_ACCEPTANCE_CRITERIA")
                            for f in failures), failures)

    # 28
    def test_COUNTEREXAMPLE_WITHOUT_WITNESS(self):
        custody = copy.deepcopy(item(corpus(), "NS-W1")["answer_custody"])
        custody["answer_kind"] = "COUNTEREXAMPLE"
        custody["final_answer"] = None
        custody["counterexample_witness"] = None
        failures = validate_answer_custody(custody, reg=REG)
        self.assertTrue(any(f.startswith("COUNTEREXAMPLE_WITHOUT_WITNESS")
                            for f in failures), failures)

    # 29
    def test_digest_drift_is_caught(self):
        bad = corpus()
        item(bad, "NS-W1")["realization_digest"] = "0" * 64
        self.expect("LEARNER_REALIZATION_DIGEST_DRIFT", bad)

    # 30
    def test_ascii_flattening_in_learner_prose_is_caught(self):
        bad = corpus()
        target = item(bad, "NS-W1")
        target["derivation"][0]["learner_explanation"] = \
            "You are given the fraction with sqrt(7) - 2 underneath, so x^2 matters."
        reseal(target)
        self.expect("MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT", bad)


class LearnerCopyBoundary(unittest.TestCase):
    """Item 9 — enforces #351's central learner-language policy; does not duplicate it."""

    def test_the_authority_is_351s_central_policy_not_a_parallel_registry(self):
        self.assertEqual(COPY_REGISTRY["authority"]["policy_id"], COPY_POLICY["policy_id"])
        self.assertNotIn("banned_learner_tokens", COPY_REGISTRY,
                         "the consumer registry must not carry a ban-list of its own")
        self.assertEqual(load_policy()["policy_id"], "MATH-LEARNER-LANGUAGE-v1")

    def test_policy_id_is_unchanged_so_the_run_manifest_binding_still_resolves(self):
        sys.path.insert(0, str(MATH / "LearnerProduct" / "engine"))
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "run_learner_product",
            MATH / "LearnerProduct" / "engine" / "run_learner_product.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.EXPECTED_POLICIES["learner_language_policy"],
                         COPY_POLICY["policy_id"])

    def test_every_policy_forbidden_term_is_enforced(self):
        enforced = set(banned_tokens())
        for token in COPY_POLICY["forbidden_learner_terms"]:
            self.assertIn(token, enforced, token)

    def test_core1a_legacy_ban_list_is_preserved_not_narrowed(self):
        sys.path.insert(0, str(MATH / "Core1A" / "engine"))
        import build_math_core1a_textbook as core1a  # noqa: E402
        enforced = set(core1a.FORBIDDEN_LEARNER_TOKENS)
        for token in core1a.LEGACY_FORBIDDEN_LEARNER_TOKENS:
            self.assertIn(token, enforced, f"Core1A already banned {token!r}")
        for token in COPY_POLICY["forbidden_learner_terms"]:
            self.assertIn(token, enforced, f"policy term {token!r} not enforced by Core1A")

    def test_the_gap_this_item_closed_is_the_role_label(self):
        """The original policy list is substring-based, so a bare role label passed it."""
        for label in ("RECONSTRUCT", "CONTRAST", "VERIFY"):
            self.assertNotIn(label.lower(), COPY_POLICY["forbidden_learner_terms"])
            self.assertIn(label, COPY_POLICY["forbidden_learner_role_labels"])

    def test_core2a_declared_falsifier_now_has_an_implementation(self):
        profile = load(MATH / "Core2A" / "policies"
                       / "math-core2a-textbook-quality-profile.json")
        self.assertIn("CORE2A_LEARNER_JARGON_LEAK", profile["required_falsifiers"])
        stages = {c["stage"] for c in COPY_REGISTRY["consumers"]}
        self.assertIn("CORE2A", stages)
        with self.assertRaises(ValueError) as ctx:
            audit_learner_copy(["The reasoning route for this item is fixed."], stage="CORE2A")
        self.assertIn("CORE2A_LEARNER_JARGON_LEAK", str(ctx.exception))

    def test_role_labels_map_to_the_policys_public_titles(self):
        for role in ("RECONSTRUCT", "CONTRAST", "ANCHOR", "REPRESENT",
                     "CHECK_SUFFICIENCY", "SELECT_THEOREM", "READINESS"):
            title = warm_title(role)
            self.assertNotEqual(title, role)
            self.assertFalse(title.isupper(), role)

    def test_approved_public_labels_come_from_the_policy(self):
        labels = approved_labels()
        self.assertEqual(labels["ATTEMPT"], "TRY IT FIRST")
        self.assertEqual(labels["SOLUTION"], "FULL WORKING")
        self.assertEqual(labels["VERIFICATION"], "QUICK CHECK")
        # VERIFY's public title is the policy's own approved label, not an invented one
        self.assertEqual(warm_title("VERIFY"), labels["VERIFICATION"])

    def test_INTERNAL_REASONING_LABEL_EXPOSED_AS_LEARNER_COPY(self):
        with self.assertRaises(ValueError) as ctx:
            audit_learner_copy(["RECONSTRUCT the rule from the two cases."],
                               stage="LEARNER_REALIZATION")
        self.assertIn("INTERNAL_REASONING_LABEL_EXPOSED_AS_LEARNER_COPY", str(ctx.exception))
        self.assertIn("ROLE_LABEL:RECONSTRUCT", str(ctx.exception))

    def test_approved_labels_are_not_flagged_as_role_labels(self):
        audit_learner_copy([
            "QUICK CHECK",
            "TRY IT FIRST",
            "FULL WORKING",
            "WHERE THIS QUESTION CAME FROM",
        ], stage="CORE2A")

    def test_lowercase_english_words_are_not_false_positives(self):
        audit_learner_copy([
            "Verify your answer by substituting x = 2 back into the cubic.",
            "Represent the two points on the plane and compare their heights.",
            "Contrast this with the case where the denominator is already rational.",
        ], stage="LEARNER_REALIZATION")

    def test_INTERNAL_IDENTIFIER_EXPOSED_AS_LEARNER_COPY(self):
        with self.assertRaises(ValueError) as ctx:
            audit_learner_copy(["See MATH-PF-SURD-RATIONALISATION for more practice."],
                               stage="LEARNER_REALIZATION")
        self.assertIn("INTERNAL_IDENTIFIER_EXPOSED_AS_LEARNER_COPY", str(ctx.exception))

    def test_reference_corpus_learner_text_is_clean_for_every_consumer_stage(self):
        texts = [t for r in corpus() for t in realization_texts(r, REG)]
        for stage in ("CORE1A", "CORE2A", "LEARNER_REALIZATION"):
            with self.subTest(stage=stage):
                self.assertEqual(audit_learner_copy(texts, stage=stage)["status"], "PASS")


if __name__ == "__main__":
    unittest.main(verbosity=2)
