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
        self.assertEqual("RELEASEABLE", delp.decompose_check(g)["release_state"])
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
        self.assertNotIn("primary_pr", row)

    def test_03_missing_binding_rejected(self):
        bad = copy.deepcopy(self.graph)
        bad["programme"]["decomposition_proposal"]["bindings"] = [
            b for b in bad["programme"]["decomposition_proposal"]["bindings"]
            if b["responsibility_id"] != "R-RECONSTRUCTION"
        ]
        with self.assertRaises(Exception):
            delp.validate_graph(bad)

    def test_04_wrong_claim_ownership_rejected(self):
        bad = copy.deepcopy(self.graph)
        target = next(n for n in bad["nodes"] if n.get("responsibility_id") == "R-RECONSTRUCTION")
        target["owns_claims"] = ["ESC-5"]
        with self.assertRaises(Exception):
            delp.validate_graph(bad)

    def test_05_reserve_and_denominator_inflation_rejected(self):
        bad = copy.deepcopy(self.graph)
        bad["nodes"][0]["reserve_weight"] = self.oracle["old_reserve_weight"]
        with self.assertRaises(Exception):
            delp.validate_graph(bad)

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


if __name__ == "__main__":
    unittest.main()
