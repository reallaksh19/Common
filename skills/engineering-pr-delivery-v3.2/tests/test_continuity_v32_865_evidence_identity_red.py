"""#868 / WP0 native source-level RED: decision-input identity and projection custody.

Intentional RED is a test outcome, not a product fix. Only test files belong on
this stacked branch. An old V1 input digest is not a complete trusted V2 basis.
"""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
TESTS = HERE.parent
SCRIPTS = HERE.parents[1] / "scripts"
for path in (str(TESTS), str(SCRIPTS)):
    if path not in sys.path:
        sys.path.insert(0, path)

import delp_projection_v32 as delp
from test_delp_projection_v32 import OBS_A, entry, facts, graph, unit


class SourceIdentityRed(unittest.TestCase):
    """D-01: an input that changes accepted facts must change trusted identity."""

    def test_d01_positive_identical_facts_replay(self):
        row = entry(facts(units=[unit("U01")]), 42, "Common#592#issuecomment-42")
        first = delp.project(graph(), [row], OBS_A)
        second = delp.project(graph(), [copy.deepcopy(row)], copy.deepcopy(OBS_A))
        self.assertEqual(first["input_digest"], second["input_digest"])
        self.assertEqual(first["nodes"]["Common#592"]["progress"],
                         second["nodes"]["Common#592"]["progress"])
        self.assertEqual([], first["rejected_facts"])

    def test_d01_red_trust_marker_changes_complete_decision_identity(self):
        accepted = entry(facts(units=[unit("U01")]), 42,
                         "Common#592#issuecomment-42")
        untrusted = copy.deepcopy(accepted)
        untrusted["untrusted_author"] = "drive-by"
        yes = delp.project(graph(), [accepted], OBS_A)
        no = delp.project(graph(), [untrusted], OBS_A)

        self.assertEqual([], yes["rejected_facts"])
        self.assertEqual(1, len(no["rejected_facts"]))
        self.assertIn("not a trusted fact author", no["rejected_facts"][0]["reasons"][0])
        self.assertNotEqual(yes["nodes"]["Common#592"]["progress"],
                            no["nodes"]["Common#592"]["progress"])

        # Current source omits untrusted_author from project().input_digest.
        # The V2 decision-input identity must not collide for these distinct
        # acceptance decisions. Intentionally fails until the source contract
        # is repaired/versioned, never by rewriting the golden expectation.
        self.assertNotEqual(
            yes["input_digest"], no["input_digest"],
            "D01_TRUST_CHANGED_FACT_ACCEPTANCE_WITH_IDENTICAL_INPUT_DIGEST",
        )


class DerivedCoreRed(unittest.TestCase):
    """D-03: syntactically plausible projections do not prove source derivation."""

    def test_d03_positive_same_source_same_core(self):
        row = entry(facts(units=[unit("U01")]), 43,
                    "Common#592#issuecomment-43")
        source = graph()
        # The generic DELP legacy test fixture omits programme.repository;
        # the real core has always required an explicit repository identity.
        source["programme"]["repository"] = "reallaksh19/Common"
        projected = delp.project(source, [row], OBS_A)
        first = delp.source_bound_responsibility_core(
            source, projected, "Common#592")
        second = delp.source_bound_responsibility_core(
            copy.deepcopy(source), copy.deepcopy(projected), "Common#592")
        self.assertEqual(first["basis_digest"], second["basis_digest"])
        self.assertEqual([], first["authority_effects"])

    def test_d03_red_correct_schema_forged_leaf_progress_is_not_derived(self):
        source = graph()
        source["programme"]["repository"] = "reallaksh19/Common"
        row = entry(facts(units=[unit("U01")]), 43,
                    "Common#592#issuecomment-43")
        projection = delp.project(source, [row], OBS_A)
        forged = copy.deepcopy(projection)
        genuine_value = projection["nodes"]["Common#592"]["progress"]["P"]
        self.assertNotEqual(99, genuine_value)
        forged["nodes"]["Common#592"]["progress"]["P"] = 99

        # Preserve the real schema, labels, plan and claimed input digest.
        self.assertEqual(projection["schema"], forged["schema"])
        self.assertEqual(projection["authority"], forged["authority"])
        self.assertEqual(projection["plan_digest"], forged["plan_digest"])
        self.assertEqual(projection["input_digest"], forged["input_digest"])

        try:
            core = delp.source_bound_responsibility_core(
                source, forged, "Common#592")
        except delp.DelpError:
            return  # valid alternative: reject untrusted input
        # If a low-level helper still permits arbitrary read models, it MUST
        # explicitly quarantine their provenance instead of claiming DELP
        # source derivation on a caller-fabricated P value.
        self.assertNotEqual(
            "DELP_SOURCE_DERIVED_NO_PROVIDER_AUTHENTICATION",
            core["authority"],
            "D03_FORGED_CORRECT_SCHEMA_PROJECTION_STAMPED_AS_SOURCE_DERIVED",
        )


if __name__ == "__main__":
    unittest.main()
