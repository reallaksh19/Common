#!/usr/bin/env python3
"""Falsifier suite for Core1 reconstruction depth and the cross-core bridge.

Each mutation removes exactly the kind of evidence that was missing when Core2 turned out
to be more mature than Core1: the derivation behind RECONSTRUCT, the materialized worked
instance, the transfer instance, the taught direction of a theorem, or the Core1 evidence a
Core2 reasoning state depends on.
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
sys.path[:0] = [str(MATH / "MathTypesetting" / "engine"),
                str(MATH / "LearnerRealization" / "engine"),
                str(PHASE / "engine"), str(PHASE / "fixtures")]

from validate_core1_reconstruction import (  # noqa: E402
    FALSIFIERS,
    audit_reconstruction,
    build_bridge,
    derive_teaching_evidence,
    load,
    seal_chain,
    validate_chain,
)

FIXTURE = load(PHASE / "fixtures" / "math-reconstruction-chains.fixture.json")
REFERENCE = load(MATH / "LearnerRealization" / "fixtures"
                 / "math-reference-realizations.fixture.json")
POLICY = load(PHASE / "policies" / "math-core1-reconstruction-policy.json")
ROLES = load(MATH / "LearnerRealization" / "registry"
             / "math-realization-role-registry.json")

LESSON_FACTOR = "MATH-C1L-FACTOR-THEOREM"
LESSON_IRRATIONAL = "MATH-C1L-IRRATIONAL-PRODUCT"


def store() -> dict:
    out = {}
    for directory in (PHASE / "contracts",
                      MATH / "LearnerRealization" / "contracts",
                      MATH / "MathTypesetting" / "contracts"):
        for p in sorted(directory.glob("*.schema.json")):
            doc = json.loads(p.read_text(encoding="utf-8"))
            out[doc["$id"]] = doc
    return out


STORE = store()


def validator(schema_id: str) -> Draft202012Validator:
    root = STORE[schema_id]
    return Draft202012Validator(root, resolver=RefResolver.from_schema(root, store=STORE))


def realizations() -> dict[str, dict]:
    out = {r["item_ref"]: r for r in REFERENCE["realizations"]}
    out.update({r["item_ref"]: r for r in FIXTURE["generated_realizations"]})
    return copy.deepcopy(out)


def chains() -> list[dict]:
    return copy.deepcopy(FIXTURE["chains"])


def chain(lesson_ref: str) -> dict:
    return copy.deepcopy(next(c for c in FIXTURE["chains"]
                              if c["lesson_ref"] == lesson_ref))


def rows() -> list[dict]:
    return copy.deepcopy(FIXTURE["bridge_rows"])


def audit(chain_list=None, realization_map=None, bridge=None):
    return audit_reconstruction(
        chain_list if chain_list is not None else chains(),
        realization_map if realization_map is not None else realizations(),
        bridge_rows=rows() if bridge is None else bridge,
        topic_ref="MIXED_GRADE9",
        theorem_based_lessons=FIXTURE["theorem_based_lessons"],
    )


class ReconstructionPositive(unittest.TestCase):
    def test_every_chain_validates_against_the_contract(self):
        v = validator("math-core1-reconstruction-chain.schema.json")
        for c in chains():
            with self.subTest(lesson=c["lesson_ref"]):
                v.validate(c)

    def test_bridge_validates_against_the_contract(self):
        bridge = build_bridge("MIXED_GRADE9", rows(), chains())
        validator("math-cross-core-bridge-manifest.schema.json").validate(bridge)

    def test_audit_passes_on_the_reference_chains(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["cross_core_unresolved"], [])

    def test_exit_gate_full_chain_is_realized_in_order(self):
        """Issue #358 item 6: the chain is realized, not merely labelled."""
        full = chain(LESSON_FACTOR)
        present = [s["stage"] for s in full["stages"]]
        self.assertEqual([s for s in present if s in POLICY["required_chain"]],
                         POLICY["required_chain"])
        reconstruct = next(s for s in full["stages"] if s["stage"] == "RECONSTRUCT")
        self.assertEqual(reconstruct["evidence_kind"], "DERIVATION")
        self.assertGreaterEqual(len(reconstruct["derivation"]), 3)
        for stage in ("WORKED", "GUIDED", "FADED", "INDEPENDENT", "TRANSFER"):
            entry = next(s for s in full["stages"] if s["stage"] == stage)
            self.assertEqual(entry["evidence_kind"], "REALIZATION")
            self.assertIn(entry["realization_ref"], realizations())

    def test_item2_realizations_are_reused_by_item6(self):
        """The stated dependency: item 2's route-state objects build item 6's chain."""
        worked = next(s for s in chain(LESSON_FACTOR)["stages"] if s["stage"] == "WORKED")
        self.assertEqual(worked["realization_ref"], "PY-W1")
        self.assertIn("PY-W1", {r["item_ref"] for r in REFERENCE["realizations"]})

    def test_teaching_evidence_is_derived_not_declared(self):
        c = chain(LESSON_FACTOR)
        self.assertEqual(sorted(c["realized_teaching_evidence"]),
                         derive_teaching_evidence(c, realizations(), ROLES))
        self.assertIn(f"{LESSON_FACTOR}#TRANSFORM", c["realized_teaching_evidence"])

    def test_trivial_states_do_not_count_as_teaching_evidence(self):
        c = chain(LESSON_IRRATIONAL)
        # S1 is a trivial CLASSIFY step inside the RECONSTRUCT derivation
        self.assertNotIn(f"{LESSON_IRRATIONAL}#CLASSIFY", c["realized_teaching_evidence"])

    def test_short_chain_is_legal_for_a_non_full_treatment(self):
        short = chain(LESSON_IRRATIONAL)
        self.assertEqual(short["treatment"], "VERIFY_ONLY")
        self.assertNotIn(short["treatment"], POLICY["full_treatments"])
        self.assertEqual(validate_chain(short, realizations(), theorem_based=True), [])

    def test_false_converse_carries_its_counterexample(self):
        direction = chain(LESSON_IRRATIONAL)["theorem_direction"]
        self.assertFalse(direction["converse"]["is_true"])
        self.assertIn("√2", direction["counterexample_when_converse_false"])

    def test_cross_core_invariant_is_stated_and_empty(self):
        result = audit()
        self.assertEqual(result["cross_core_invariant"],
                         POLICY["cross_core_invariant"])
        self.assertEqual(result["bridge"]["unresolved"], [])

    def test_audit_is_deterministic(self):
        self.assertEqual(audit()["corpus_digest"], audit()["corpus_digest"])

    def test_policy_declares_every_falsifier_the_engine_can_raise(self):
        self.assertEqual(sorted(POLICY["falsifiers"]), sorted(FALSIFIERS))


class ReconstructionFalsifiers(unittest.TestCase):
    def expect(self, code: str, fn):
        with self.assertRaises(ValueError) as ctx:
            fn()
        self.assertIn(code, str(ctx.exception), f"expected {code}, got {ctx.exception}")

    def reseal(self, c: dict) -> dict:
        return seal_chain(c, realizations(), ROLES)

    def with_chain(self, c: dict) -> list[dict]:
        others = [x for x in chains() if x["lesson_ref"] != c["lesson_ref"]]
        return others + [c]

    # 1 — the stage label exists, the chain does not
    def test_CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE(self):
        bad = chain(LESSON_FACTOR)
        bad["stages"] = [s for s in bad["stages"] if s["stage"] != "TRANSFER"]
        self.expect("CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 2
    def test_CORE1_CHAIN_ORDER_DRIFT(self):
        bad = chain(LESSON_FACTOR)
        index = {s["stage"]: i for i, s in enumerate(bad["stages"])}
        a, b = index["WORKED"], index["GUIDED"]
        bad["stages"][a], bad["stages"][b] = bad["stages"][b], bad["stages"][a]
        self.expect("CORE1_CHAIN_ORDER_DRIFT",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 3 — RECONSTRUCT reduced to prose
    def test_CORE1_RECONSTRUCTION_WITHOUT_DERIVATION(self):
        bad = chain(LESSON_FACTOR)
        stage = next(s for s in bad["stages"] if s["stage"] == "RECONSTRUCT")
        stage["evidence_kind"] = "PROSE"
        stage["prose"] = ("The factor theorem says that (x - a) is a factor exactly when "
                          "p(a) is zero, which is a very useful shortcut to remember.")
        stage["derivation"] = []
        self.expect("CORE1_RECONSTRUCTION_WITHOUT_DERIVATION",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 4
    def test_CORE1_RECONSTRUCTION_WITHOUT_DERIVATION_when_too_shallow(self):
        bad = chain(LESSON_FACTOR)
        stage = next(s for s in bad["stages"] if s["stage"] == "RECONSTRUCT")
        stage["derivation"] = stage["derivation"][:1]
        self.expect("CORE1_RECONSTRUCTION_WITHOUT_DERIVATION",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 5
    def test_CORE1_WORKED_INSTANCE_NOT_MATERIALIZED(self):
        bad = chain(LESSON_FACTOR)
        next(s for s in bad["stages"]
             if s["stage"] == "WORKED")["realization_ref"] = "NOT-A-REAL-ITEM"
        self.expect("CORE1_WORKED_INSTANCE_NOT_MATERIALIZED",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 6
    def test_CORE1_TRANSFER_INSTANCE_MISSING(self):
        bad = chain(LESSON_FACTOR)
        next(s for s in bad["stages"]
             if s["stage"] == "TRANSFER")["realization_ref"] = None
        self.expect("CORE1_TRANSFER_INSTANCE_MISSING",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 7 — a referenced instance that does not itself pass the item-2 gate
    def test_CORE1_STAGE_UNDERREALIZED_when_the_instance_fails_the_realization_gate(self):
        broken = realizations()
        target = broken["FT-G1"]
        for step in target["derivation"]:
            step["learner_explanation"] = "Carry out the algebra in the structured workspace."
        self.expect("CORE1_STAGE_UNDERREALIZED", lambda: audit(realization_map=broken))

    # 8
    def test_CORE1_STAGE_UNDERREALIZED_on_thin_prose(self):
        bad = chain(LESSON_FACTOR)
        next(s for s in bad["stages"] if s["stage"] == "EXPLAIN")["prose"] = "It works."
        self.expect("CORE1_STAGE_UNDERREALIZED",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 9
    def test_CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE_on_declared_evidence_drift(self):
        bad = chain(LESSON_FACTOR)
        bad["realized_teaching_evidence"] = sorted(
            set(bad["realized_teaching_evidence"]) | {f"{LESSON_FACTOR}#MODEL"})
        self.expect("CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE",
                    lambda: audit(self.with_chain(bad)))

    # 10
    def test_CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE_on_digest_drift(self):
        bad = chain(LESSON_FACTOR)
        bad["chain_digest"] = "0" * 64
        self.expect("CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE",
                    lambda: audit(self.with_chain(bad)))

    # 11
    def test_THEOREM_DIRECTION_NOT_DECLARED(self):
        bad = chain(LESSON_FACTOR)
        bad["theorem_direction"] = None
        self.expect("THEOREM_DIRECTION_NOT_DECLARED",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 12
    def test_CONVERSE_RESTATES_FORWARD_STATEMENT(self):
        bad = chain(LESSON_FACTOR)
        direction = bad["theorem_direction"]
        direction["converse"]["condition"] = direction["forward"]["condition"]
        direction["converse"]["conclusion"] = direction["forward"]["conclusion"]
        self.expect("CONVERSE_RESTATES_FORWARD_STATEMENT",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 13
    def test_THEOREM_DIRECTION_NOT_DECLARED_when_a_false_converse_has_no_counterexample(self):
        bad = chain(LESSON_IRRATIONAL)
        bad["theorem_direction"]["counterexample_when_converse_false"] = None
        self.expect("THEOREM_DIRECTION_NOT_DECLARED",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 14 — Core2 needs the converse, Core1 taught only the forward direction
    def test_CONVERSE_USED_WITHOUT_BEING_TAUGHT(self):
        bad = chain(LESSON_FACTOR)
        bad["theorem_direction"]["direction_taught"] = "FORWARD"
        self.expect("CONVERSE_USED_WITHOUT_BEING_TAUGHT",
                    lambda: audit(self.with_chain(self.reseal(bad))))

    # 15 — the central cross-core invariant
    def test_CORE1_CORE2_REASONING_COVERAGE_GAP_on_untaught_state(self):
        bad_rows = rows()
        bad_rows[0]["reasoning_states"].append({
            "role": "MODEL", "trivial": False, "uses_converse": False,
            "core1_evidence_ref": f"{LESSON_FACTOR}#MODEL",
        })
        self.expect("CORE1_CORE2_REASONING_COVERAGE_GAP", lambda: audit(bridge=bad_rows))

    # 16
    def test_CORE1_CORE2_REASONING_COVERAGE_GAP_on_missing_evidence_ref(self):
        bad_rows = rows()
        bad_rows[1]["reasoning_states"][0]["core1_evidence_ref"] = None
        self.expect("CORE1_CORE2_REASONING_COVERAGE_GAP", lambda: audit(bridge=bad_rows))

    # 17 — a lesson reference is not evidence; the state-level token is
    def test_CORE1_CORE2_REASONING_COVERAGE_GAP_on_lesson_level_reference_only(self):
        bad_rows = rows()
        bad_rows[0]["reasoning_states"][1]["core1_evidence_ref"] = LESSON_FACTOR
        self.expect("CORE1_CORE2_REASONING_COVERAGE_GAP", lambda: audit(bridge=bad_rows))

    # 18
    def test_CORE1_CORE2_REASONING_COVERAGE_GAP_on_unresolved_first_recovery(self):
        bad_rows = rows()
        bad_rows[2]["first_recovery_evidence_ref"] = f"{LESSON_IRRATIONAL}#SETUP"
        self.expect("CORE1_CORE2_REASONING_COVERAGE_GAP", lambda: audit(bridge=bad_rows))

    # 19 — removing the teaching evidence, not the reference, still fails
    def test_CORE1_CORE2_REASONING_COVERAGE_GAP_when_core1_stops_teaching_the_state(self):
        thin = chain(LESSON_FACTOR)
        stage = next(s for s in thin["stages"] if s["stage"] == "GUIDED")
        stage["evidence_kind"] = "REALIZATION"
        thin["stages"] = [s for s in thin["stages"] if s["stage"] != "TRANSFER"]
        # keep the chain legal by dropping to a non-full treatment, then confirm the
        # cross-core gate still catches the now-untaught TRANSFORM state
        thin["treatment"] = "VERIFY_ONLY"
        for s in thin["stages"]:
            if s["stage"] in ("WORKED", "GUIDED", "FADED", "INDEPENDENT"):
                s["evidence_kind"] = "PROSE"
                s["prose"] = ("Work through the example in class before trying the exercise "
                              "set on the next page of this booklet.")
                s["realization_ref"] = None
        self.expect("CORE1_CORE2_REASONING_COVERAGE_GAP",
                    lambda: audit(self.with_chain(self.reseal(thin))))

    # 20
    def test_contract_rejects_a_stage_outside_the_declared_vocabulary(self):
        bad = chain(LESSON_FACTOR)
        bad["stages"][0]["stage"] = "NOT_A_STAGE"
        with self.assertRaises(Exception):
            validator("math-core1-reconstruction-chain.schema.json").validate(bad)

    # 21
    def test_contract_rejects_a_malformed_evidence_token(self):
        bad = chain(LESSON_FACTOR)
        bad["realized_teaching_evidence"] = ["not-an-evidence-token"]
        with self.assertRaises(Exception):
            validator("math-core1-reconstruction-chain.schema.json").validate(bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
