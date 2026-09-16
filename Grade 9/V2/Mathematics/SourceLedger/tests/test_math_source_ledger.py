#!/usr/bin/env python3
"""Falsifier suite for two-dimensional source completeness and the rendered witness.

The three mutation classes below are the three independent failures the seven-topic stress
test produced, reproduced exactly:

    drop a top-level row          -> CORE2_SOURCE_CORPUS_COVERAGE_GAP
    drop one subpart of a compound question, leaving the row count unchanged
                                  -> CORE2_ATOMIC_ASK_COVERAGE_GAP
    cover options C and D with the next panel on the rendered page
                                  -> ASSESSMENT_OBJECT_OCCLUSION
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
sys.path[:0] = [str(PHASE / "engine"), str(PHASE / "fixtures")]

from build_math_source_ledger import (  # noqa: E402
    audit_source_completeness,
    digest,
    freeze_manifest,
    load,
    reconcile,
    rendered_coverage_witness,
    shape_of,
    validate_manifest,
)
from render_attempt_probe import page_texts, render  # noqa: E402

MANIFEST = load(PHASE / "fixtures" / "math-source-corpus.fixture.json")
AUTHORED = load(PHASE / "fixtures" / "math-authored-plan.fixture.json")
POLICY = load(PHASE / "policies" / "math-source-completeness-policy.json")
KINDS = load(PHASE / "registry" / "math-atomic-ask-kind-registry.json")
TMP = Path("/tmp/math-source-ledger")
TMP.mkdir(parents=True, exist_ok=True)


def store() -> dict:
    out = {}
    for p in sorted((PHASE / "contracts").glob("*.schema.json")):
        doc = json.loads(p.read_text(encoding="utf-8"))
        out[doc["$id"]] = doc
    return out


STORE = store()


def validator(schema_id: str) -> Draft202012Validator:
    root = STORE[schema_id]
    return Draft202012Validator(root, resolver=RefResolver.from_schema(root, store=STORE))


def manifest() -> dict:
    return copy.deepcopy(MANIFEST)


def authored() -> dict:
    return copy.deepcopy(AUTHORED)


def page(plan: dict, ref: str) -> dict:
    return next(p for p in plan["pages"] if p["question_ref"] == ref)


def clean_render(name: str = "clean", **kwargs):
    pdf, object_map = render(manifest(), TMP / f"probe-{name}.pdf", **kwargs)
    return pdf, object_map, page_texts(pdf)


class LedgerPositive(unittest.TestCase):
    def test_manifest_validates_against_the_contract(self):
        validator("math-source-corpus-manifest.schema.json").validate(MANIFEST)

    def test_manifest_is_frozen_and_self_consistent(self):
        self.assertEqual(validate_manifest(MANIFEST, kinds=KINDS), [])
        self.assertEqual(MANIFEST["frozen_at_stage"], "BEFORE_AUTHORING")

    def test_completeness_is_genuinely_two_dimensional(self):
        """4 top-level rows, 12 atomic asks: the second number is not derivable from
        the first, which is the whole point of the second dimension."""
        self.assertEqual(len(MANIFEST["required_question_refs"]), 4)
        self.assertEqual(len(MANIFEST["required_atomic_ask_refs"]), 12)

    def test_ledger_passes_and_validates_on_the_complete_plan(self):
        pdf, object_map, texts = clean_render()
        ledger = audit_source_completeness(manifest(), authored(), object_map=object_map,
                                           rendered_page_text=texts)
        self.assertEqual(ledger["status"], "PASS")
        self.assertEqual(ledger["reconciliation"]["unresolved"], [])
        validator("math-source-reconciliation-ledger.schema.json").validate(ledger)

    def test_object_map_validates_against_the_contract(self):
        _, object_map, _ = clean_render()
        validator("math-rendered-object-map.schema.json").validate(object_map)

    def test_reconciliation_block_reports_every_required_field(self):
        pdf, object_map, texts = clean_render()
        ledger = reconcile(manifest(), authored(), object_map=object_map,
                           rendered_page_text=texts)
        for field in ("required_source_rows", "included_source_rows",
                      "required_atomic_asks", "included_atomic_asks", "concept_linked",
                      "core1_evidence_linked", "solution_complete",
                      "verification_complete", "render_visible", "unresolved"):
            self.assertIn(field, ledger["reconciliation"], field)

    def test_ledger_is_deterministic(self):
        _, object_map, texts = clean_render()
        a = reconcile(manifest(), authored(), object_map=object_map, rendered_page_text=texts)
        b = reconcile(manifest(), authored(), object_map=object_map, rendered_page_text=texts)
        self.assertEqual(a["ledger_digest"], b["ledger_digest"])

    def test_freezing_derives_the_required_lists_rather_than_trusting_them(self):
        lying = manifest()
        lying["required_atomic_ask_refs"] = ["Q1#OPT-A"]
        refrozen = freeze_manifest(lying)
        self.assertEqual(len(refrozen["required_atomic_ask_refs"]), 12)

    def test_exit_gate_completeness_survives_to_the_rendered_page(self):
        _, object_map, texts = clean_render()
        witness = rendered_coverage_witness(manifest(), object_map,
                                            rendered_page_text=texts, policy=POLICY)
        self.assertTrue(witness["evaluated"])
        self.assertEqual(witness["checked"], 12)
        self.assertEqual(witness["visible"], 12)
        self.assertEqual((witness["missing"], witness["occluded"], witness["clipped"]),
                         ([], [], []))


class LedgerFalsifiers(unittest.TestCase):
    def expect(self, code: str, fn):
        with self.assertRaises(ValueError) as ctx:
            fn()
        self.assertIn(code, str(ctx.exception), f"expected {code}, got {ctx.exception}")

    # 1 — the Number Systems failure: a top-level row silently absent
    def test_CORE2_SOURCE_CORPUS_COVERAGE_GAP(self):
        plan = authored()
        plan["pages"] = [p for p in plan["pages"] if p["question_ref"] != "Q3"]
        self.expect("CORE2_SOURCE_CORPUS_COVERAGE_GAP",
                    lambda: audit_source_completeness(manifest(), plan))

    # 2 — the Polynomials failure: row count unchanged, one atomic ask gone
    def test_CORE2_ATOMIC_ASK_COVERAGE_GAP_with_unchanged_row_count(self):
        plan = authored()
        target = page(plan, "Q3")
        target["atomic_ask_refs"] = [r for r in target["atomic_ask_refs"] if r != "Q3#SUB-b"]
        target["subpart_shape"]["subpart_count"] -= 1
        self.assertEqual(len(plan["pages"]), 4)          # top-level count is still perfect
        self.expect("CORE2_ATOMIC_ASK_COVERAGE_GAP",
                    lambda: audit_source_completeness(manifest(), plan))

    # 3 — a lost proof obligation in a compound "prove ... and hence deduce ..." item
    def test_CORE2_ATOMIC_ASK_COVERAGE_GAP_on_lost_proof_obligation(self):
        plan = authored()
        target = page(plan, "Q2")
        target["atomic_ask_refs"] = ["Q2#PROOF-1"]
        target["subpart_shape"]["proof_obligation_count"] = 1
        self.expect("CORE2_ATOMIC_ASK_COVERAGE_GAP",
                    lambda: audit_source_completeness(manifest(), plan))

    # 4 — a lost parameter condition turns an underdetermined item into a unique one
    def test_CORE2_ATOMIC_ASK_COVERAGE_GAP_on_lost_parameter_condition(self):
        plan = authored()
        target = page(plan, "Q3")
        target["atomic_ask_refs"] = [r for r in target["atomic_ask_refs"] if r != "Q3#COND"]
        target["subpart_shape"]["parameter_condition_count"] = 0
        self.expect("CORE2_ATOMIC_ASK_COVERAGE_GAP",
                    lambda: audit_source_completeness(manifest(), plan))

    # 5
    def test_CORE2_SUBPART_SHAPE_DRIFT(self):
        plan = authored()
        page(plan, "Q1")["subpart_shape"]["option_count"] = 3
        self.expect("CORE2_SUBPART_SHAPE_DRIFT",
                    lambda: audit_source_completeness(manifest(), plan))

    # 6
    def test_SOURCE_CORPUS_NOT_FROZEN_BEFORE_AUTHORING(self):
        bad = manifest()
        bad["frozen_at_stage"] = "AFTER_AUTHORING"
        bad["manifest_digest"] = digest(bad, "manifest_digest")
        self.expect("SOURCE_CORPUS_NOT_FROZEN_BEFORE_AUTHORING",
                    lambda: audit_source_completeness(bad, authored()))

    # 7
    def test_SOURCE_CORPUS_MANIFEST_DIGEST_DRIFT(self):
        bad = manifest()
        bad["questions"][0]["stem"] = "A quietly edited stem."
        self.expect("SOURCE_CORPUS_MANIFEST_DIGEST_DRIFT",
                    lambda: audit_source_completeness(bad, authored()))

    # 8 — the Linear Equations failure, reproduced on a real rendered page
    def test_ASSESSMENT_OBJECT_OCCLUSION_covers_options_C_and_D(self):
        pdf, object_map = render(manifest(), TMP / "probe-occluded.pdf",
                                 occlude_after_option="(B)")
        texts = page_texts(pdf)
        # the options are all still present in the data and even in the page text ...
        blob = " ".join(texts)
        self.assertIn("(4, 0)", blob)
        self.assertIn("(1, 2)", blob)
        # ... and the learner still cannot read them
        with self.assertRaises(ValueError) as ctx:
            audit_source_completeness(manifest(), authored(), object_map=object_map,
                                      rendered_page_text=texts)
        message = str(ctx.exception)
        self.assertIn("ASSESSMENT_OBJECT_OCCLUSION:Q1#OPT-C", message)
        self.assertIn("ASSESSMENT_OBJECT_OCCLUSION:Q1#OPT-D", message)

    # 9
    def test_RENDERED_SOURCE_OPTION_COVERAGE_GAP(self):
        pdf, object_map = render(manifest(), TMP / "probe-dropped.pdf",
                                 drop_atomic_ask="Q1#OPT-D")
        self.expect("RENDERED_SOURCE_OPTION_COVERAGE_GAP",
                    lambda: audit_source_completeness(manifest(), authored(),
                                                      object_map=object_map,
                                                      rendered_page_text=page_texts(pdf)))

    # 10
    def test_ASSESSMENT_OBJECT_CLIPPED(self):
        pdf, object_map = render(manifest(), TMP / "probe-clipped.pdf",
                                 clip_atomic_ask="Q3#COND")
        self.expect("ASSESSMENT_OBJECT_CLIPPED",
                    lambda: audit_source_completeness(manifest(), authored(),
                                                      object_map=object_map,
                                                      rendered_page_text=page_texts(pdf)))

    # 11 — present in the object map but not readable on the page
    def test_RENDERED_SOURCE_OPTION_COVERAGE_GAP_when_text_is_not_extractable(self):
        _, object_map, _ = clean_render("text-missing")
        self.expect("RENDERED_SOURCE_OPTION_COVERAGE_GAP",
                    lambda: audit_source_completeness(
                        manifest(), authored(), object_map=object_map,
                        rendered_page_text=["a page with none of the source content on it"]))

    # 12
    def test_manifest_rejects_an_unknown_atomic_ask_kind(self):
        bad = manifest()
        bad["questions"][0]["atomic_asks"][0]["kind"] = "NOT_A_KIND"
        bad = freeze_manifest(bad)
        failures = validate_manifest(bad, kinds=KINDS)
        self.assertTrue(any(f.startswith("CORE2_ATOMIC_ASK_COVERAGE_GAP") for f in failures),
                        failures)

    # 13
    def test_manifest_shape_must_match_its_own_atomic_asks(self):
        bad = manifest()
        bad["questions"][0]["subpart_shape"]["option_count"] = 9
        bad["manifest_digest"] = digest(bad, "manifest_digest")
        failures = validate_manifest(bad, kinds=KINDS)
        self.assertTrue(any(f.startswith("CORE2_SUBPART_SHAPE_DRIFT") for f in failures),
                        failures)

    # 14
    def test_shape_of_counts_only_the_shape_bearing_kinds(self):
        asks = MANIFEST["questions"][0]["atomic_asks"]
        self.assertEqual(shape_of(asks),
                         {"subpart_count": 0, "option_count": 4,
                          "proof_obligation_count": 0, "parameter_condition_count": 0})

    # 15
    def test_policy_declares_every_falsifier_the_engine_raises(self):
        for code in ("CORE2_SOURCE_CORPUS_COVERAGE_GAP", "CORE2_ATOMIC_ASK_COVERAGE_GAP",
                     "CORE2_SUBPART_SHAPE_DRIFT", "SOURCE_CORPUS_NOT_FROZEN_BEFORE_AUTHORING",
                     "SOURCE_CORPUS_MANIFEST_DIGEST_DRIFT",
                     "RENDERED_SOURCE_OPTION_COVERAGE_GAP", "ASSESSMENT_OBJECT_OCCLUSION",
                     "ASSESSMENT_OBJECT_CLIPPED", "SOURCE_LEDGER_GATE_FAILED"):
            self.assertIn(code, POLICY["falsifiers"], code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
