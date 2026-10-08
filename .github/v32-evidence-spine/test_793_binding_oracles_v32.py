"""#793 precommitted ESC-4 binding acceptance; actual V3.2 DELP, no GitHub writes.

The historical #718 C0 golden is evaluated from its frozen baseline, not
silently rewritten to match a newly materialized responsibility.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "skills/engineering-pr-delivery-v3.2/scripts"))
import delp_projection_v32 as delp  # noqa: E402
import vertical_cycle_preflight_v32 as historical  # noqa: E402

GRAPH = HERE / "718-proposal-v2.json"
ORACLE = HERE / "793-binding-oracles-v1.json"


class SourceBoundReconstructionAdmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = json.loads(GRAPH.read_text(encoding="utf-8"))
        cls.oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        cls.released = cls.graph["programme"]["decomposition_proposal"]

    def test_01_clean_bound_release_and_reserve(self):
        g, o = self.graph, self.oracle
        self.assertEqual(o["released_proposal_digest"], self.released["released_proposal_digest"])
        self.assertEqual("RELEASEABLE", delp.decomposition_report(g)["release_state"])
        self.assertEqual(o["expected_reserve_weight"], g["nodes"][0]["reserve_weight"])
        bindings = {b["responsibility_id"]: b["ref"] for b in self.released["bindings"]}
        self.assertEqual({x["responsibility_id"]: x["ref"] for x in o["expected_bindings"]}, bindings)
        nodes = {n["responsibility_id"]: n for n in g["nodes"] if n["kind"] == "LEAF"}
        self.assertEqual(100, sum(n["weight"] for n in nodes.values()) + g["nodes"][0]["reserve_weight"])
        self.assertEqual(set(bindings), set(nodes))

    def test_02_released_source_units_exact(self):
        row = next(n for n in self.graph["nodes"] if n.get("responsibility_id") == "R-RECONSTRUCTION")
        spec = next(n for n in self.released["responsibilities"] if n["id"] == "R-RECONSTRUCTION")
        self.assertEqual(self.oracle["expected_new_node"]["ref"], row["ref"])
        for key in ("outcome", "independence_basis", "write_surface", "acceptance_methods", "size_budget"):
            self.assertEqual(spec[key], row[key])
        for left, right in zip(spec["semantic_units"], row["units"], strict=True):
            for key in ("id", "weight", "outcome", "verify"):
                self.assertEqual(left[key], right[key])
        registration = json.loads((HERE / "793-c4-material-binding-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(registration["proposed_acceptance"]["graph_primary_pr"], row["primary_pr"])
        self.assertEqual("Common#800", row["primary_pr"])
        self.assertNotEqual("Common#794", row["primary_pr"], "planning PR is not the product candidate")

    def test_03_missing_binding_rejected(self):
        bad = copy.deepcopy(self.graph)
        bad["programme"]["decomposition_proposal"]["bindings"] = [
            b for b in bad["programme"]["decomposition_proposal"]["bindings"]
            if b["responsibility_id"] != "R-RECONSTRUCTION"
        ]
        # Structural parse may succeed; the RELEASE gate must reject semantic drift.
        verdict = delp.decomposition_report(bad)
        self.assertEqual("NOT_RELEASEABLE", verdict["release_state"])
        self.assertGreater(verdict["summary"]["not_releasable"], 0)

    def test_04_wrong_claim_ownership_rejected(self):
        bad = copy.deepcopy(self.graph)
        target = next(n for n in bad["nodes"] if n.get("responsibility_id") == "R-RECONSTRUCTION")
        target["owns_claims"] = ["ESC-5"]
        # Structural parse may succeed; the RELEASE gate must reject semantic drift.
        verdict = delp.decomposition_report(bad)
        self.assertEqual("NOT_RELEASEABLE", verdict["release_state"])
        self.assertGreater(verdict["summary"]["not_releasable"], 0)

    def test_05_reserve_and_denominator_inflation_rejected(self):
        bad = copy.deepcopy(self.graph)
        bad["nodes"][0]["reserve_weight"] = self.oracle["old_reserve_weight"]
        # Structural parse may succeed; the RELEASE gate must reject semantic drift.
        verdict = delp.decomposition_report(bad)
        self.assertEqual("NOT_RELEASEABLE", verdict["release_state"])
        self.assertGreater(verdict["summary"]["not_releasable"], 0)

    def test_06_no_facts_no_acceptance_or_progress(self):
        view = delp.project(self.graph, [], {})
        leaf = view["nodes"]["Common#793"]
        self.assertEqual(self.oracle["expected"]["new_leaf_P"], leaf["progress"]["P"])
        self.assertEqual(self.oracle["expected"]["new_leaf_E"], leaf["progress"]["E"])
        self.assertNotEqual("COMPLETE", leaf["state"])
        self.assertNotEqual("COMPLETE", view["nodes"]["Common#718"]["state"])

    def test_07_retained_historic_c0_oracle_not_rewritten(self):
        manifest, frozen = historical.load()
        report = historical.validate_contract(manifest, frozen)
        self.assertEqual(self.oracle["old_reserve_weight"], report["root_reserve"])
        self.assertEqual(12, report["fixture_count"])
        self.assertEqual("Common#718", manifest["programme"])
        self.assertNotIn("Common#793", {n["ref"] for n in frozen["nodes"]})


    def test_08_actual_esc4_candidate_sha_is_in_delp_material_basis(self):
        registration = json.loads((HERE / "793-c4-material-binding-v1.json").read_text(encoding="utf-8"))
        graph = self.graph
        sha = "a" * 40

        class ReadOnlyMaterial:
            def __init__(self):
                self.product_sha = sha

            def get_commit_sha(self, ref):
                return "b" * 40

            def get_pull(self, number):
                return {
                    "head": {"sha": self.product_sha if number == 800 else "c" * 40},
                    "merged": False,
                    "state": "open",
                }

        provider = ReadOnlyMaterial()
        before = delp.observe_github(provider, graph)
        self.assertEqual(sha, before["Common#793"]["candidate_sha"])
        self.assertEqual("OPEN", before["Common#793"]["pr_state"])
        self.assertEqual(registration["proposed_acceptance"]["graph_primary_pr"],
                         next(n for n in graph["nodes"] if n["ref"] == "Common#793")["primary_pr"])
        first = delp.project(graph, [], before)
        provider.product_sha = "d" * 40
        after = delp.observe_github(provider, graph)
        self.assertEqual("d" * 40, after["Common#793"]["candidate_sha"])
        second = delp.project(graph, [], after)
        self.assertNotEqual(first["input_digest"], second["input_digest"])
        self.assertEqual(0, second["nodes"]["Common#793"]["progress"]["P"])
        self.assertEqual(0, second["nodes"]["Common#793"]["progress"]["E"])



if __name__ == "__main__":
    unittest.main()
