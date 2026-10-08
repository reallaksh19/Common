"""Retained V3.2 Proposal-V2 progressive materialization / DELP plan-equivalence cases.

The project() status for a released, partially materialized programme must be
consistent with the same proposal's exact decompose-check authority. No title,
plan percentage, or agent conclusion can substitute for that calculation.
"""
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
MODULE = SCRIPTS / "delp_projection_v32.py"
SPEC = importlib.util.spec_from_file_location("v32_durable_plan_reconciliation", MODULE)
assert SPEC is not None and SPEC.loader is not None
DELP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DELP)


def product():
    return {
        "id": "R-PRODUCT",
        "work_class": "PRODUCT",
        "owns_claims": ["PA-PRODUCT"],
        "claim_allocations": [{"claim_id": "PA-PRODUCT", "weight": 80}],
        "outcome": "One bounded product behavior meets its independently verifiable contract.",
        "independence_basis": "The behavior can be judged before integrated delivery qualification.",
        "semantic_units": [
            {"id": "P1", "kind": "SEMANTIC", "weight": 34,
             "outcome": "The governing product identity is preserved.",
             "verify": "Exact identity comparison against approved contract"},
            {"id": "P2", "kind": "SEMANTIC", "weight": 33,
             "outcome": "The product behavior remains correct after revision.",
             "verify": "Retained functional oracle"},
            {"id": "P3", "kind": "SEMANTIC", "weight": 33,
             "outcome": "The product rejects conflicting prior state.",
             "verify": "Negative/recovery oracle"},
        ],
        "write_surface": ["src/product_component.py"],
        "size_budget": {"target_loc": 300, "hard_loc": 600, "target_minutes": 10, "hard_minutes": 20},
        "acceptance_methods": ["Functional outcome oracle", "Negative regression oracle"],
    }


def gate():
    return {
        "id": "G-QUAL",
        "work_class": "GATE",
        "owns_claims": ["PA-GATE"],
        "claim_allocations": [{"claim_id": "PA-GATE", "weight": 20}],
        "outcome": "Integrated qualification of the accepted product is independently established.",
        "independence_basis": "The integrated delivery result can be verified on an exact candidate.",
        "semantic_units": [
            {"id": "G1", "kind": "DELIVERY_GATE", "weight": 100,
             "outcome": "The required integrated verification is complete.",
             "verify": "Exact candidate integration run"},
        ],
        "write_surface": ["checks/integration.py"],
        "size_budget": {"target_loc": 80, "hard_loc": 150, "target_minutes": 5, "hard_minutes": 10},
        "acceptance_methods": ["Exact candidate integrated qualification"],
    }


def graph(*, materialize_gate=False, bind_product=True):
    proposals = [product(), gate()]
    graph = {
        "schema": DELP.GRAPH_SCHEMA,
        "programme": {
            "id": "V32-PROGRESSIVE-BINDING-REPLAY",
            "repository": "reallaksh19/Common",
            "root": "Common#718",
            "total_weight": 100,
            "acceptance_claims": [
                {"id": "PA-PRODUCT", "claim": "Provide the independently accepted product behavior.",
                 "kind": "SEMANTIC", "weight": 80},
                {"id": "PA-GATE", "claim": "Qualify integrated delivery of the accepted product.",
                 "kind": "DELIVERY_GATE", "weight": 20},
            ],
            "decomposition_policy": {
                "mode": "ENFORCED",
                "claim_first": {"mode": "ENFORCED", "require_independence_basis": True},
            },
            "decomposition_proposal": {"version": "V2", "responsibilities": proposals},
        },
        "nodes": [{"ref": "Common#718", "kind": "ROOT",
                   "reserve_weight": 0 if materialize_gate else 20}],
    }
    def leaf(p, number, weight):
        return {
            "ref": f"Common#{number}", "kind": "LEAF", "parent": "Common#718",
            "weight": weight, "responsibility_id": p["id"], "work_class": p["work_class"],
            "owns_claims": copy.deepcopy(p["owns_claims"]),
            "outcome": p["outcome"], "independence_basis": p["independence_basis"],
            "size_budget": copy.deepcopy(p["size_budget"]),
            "write_surface": copy.deepcopy(p["write_surface"]),
            "acceptance_methods": copy.deepcopy(p["acceptance_methods"]),
            "units": [{"id": u["id"], "weight": u["weight"], "outcome": u["outcome"],
                       "verify": u["verify"]} for u in p["semantic_units"]],
        }

    graph["nodes"].append(leaf(proposals[0], 720, 80))
    if materialize_gate:
        graph["nodes"].append(leaf(proposals[1], 722, 20))

    digest = DELP.decomposition_report(graph)["proposal_digest"]
    proposal = graph["programme"]["decomposition_proposal"]
    proposal["released_proposal_digest"] = digest
    proposal["bindings"] = ([{"responsibility_id": "R-PRODUCT", "ref": "Common#720"}]
                            if bind_product else [])
    if materialize_gate:
        proposal["bindings"].append({"responsibility_id": "G-QUAL", "ref": "Common#722"})
    return graph


def projection(g):
    return DELP.project(g, [], {})


def blockers(g, ref="Common#720"):
    return {f["code"] for f in projection(g)["nodes"][ref].get("plan", {}).get("blockers", [])}


class ProgressiveClaimFirstBinding(unittest.TestCase):
    def test_partial_releaseable_proposal_keeps_the_first_leaf_releasable(self):
        g = graph()
        self.assertEqual("RELEASEABLE", DELP.decomposition_report(g)["release_state"])
        output = projection(g)
        leaf = output["nodes"]["Common#720"]
        root = output["nodes"]["Common#718"]
        self.assertTrue(leaf["plan"]["releasable"], leaf["plan"])
        self.assertNotEqual("NOT_RELEASEABLE", leaf["state"])
        self.assertNotEqual("PLAN_GAP", root["state"])
        self.assertNotEqual("COMPLETE", root["state"])
        self.assertIn("UNDECOMPOSED_RESERVE:20", root["warnings"])
        self.assertEqual(0, leaf["progress"]["P"])
        self.assertEqual(0, leaf["progress"]["E"])

    def test_exact_release_digest_drift_fails_closed_in_projection(self):
        g = graph()
        g["programme"]["decomposition_proposal"]["released_proposal_digest"] = "sha256:" + "0" * 64
        self.assertEqual("NOT_RELEASEABLE", projection(g)["nodes"]["Common#720"]["state"])
        self.assertIn("PROPOSAL_RELEASE_DIGEST_MISMATCH", blockers(g))

    def test_changed_released_product_outcome_fails_closed(self):
        g = graph()
        g["nodes"][1]["outcome"] = "Different undelivered product"
        self.assertEqual("NOT_RELEASEABLE", projection(g)["nodes"]["Common#720"]["state"])
        self.assertIn("BINDING_OUTCOME_MISMATCH", blockers(g))

    def test_changed_claim_ownership_fails_closed(self):
        g = graph()
        g["nodes"][1]["owns_claims"] = ["PA-GATE"]
        self.assertIn("BINDING_CLAIM_MISMATCH", blockers(g))
        self.assertEqual("NOT_RELEASEABLE", projection(g)["nodes"]["Common#720"]["state"])

    def test_wrong_bound_weight_fails_closed(self):
        g = graph()
        g["nodes"][1]["weight"] = 79
        self.assertIn("BINDING_WEIGHT_MISMATCH", blockers(g))

    def test_unbound_materialized_leaf_fails_closed(self):
        g = graph(bind_product=False)
        self.assertEqual("RELEASEABLE", DELP.decomposition_report(g)["release_state"])
        leaf = projection(g)["nodes"]["Common#720"]
        self.assertEqual("NOT_RELEASEABLE", leaf["state"])
        self.assertIn("PROPOSAL_BINDING_UNRESOLVED", blockers(g))

    def test_binding_to_nonexistent_provider_fails_closed(self):
        g = graph()
        g["programme"]["decomposition_proposal"]["bindings"][0]["ref"] = "Common#999999"
        self.assertEqual("NOT_RELEASEABLE", projection(g)["nodes"]["Common#720"]["state"])

    def test_complete_materialization_has_no_extra_blockers(self):
        g = graph(materialize_gate=True)
        self.assertEqual("RELEASEABLE", DELP.decomposition_report(g)["release_state"])
        output = projection(g)
        for ref in ("Common#720", "Common#722"):
            self.assertTrue(output["nodes"][ref]["plan"]["releasable"])

    def test_legacy_graph_keeps_existing_materialized_leaf_claim_gate(self):
        g = graph()
        del g["programme"]["decomposition_proposal"]
        self.assertIn("PARENT_CLAIM_UNCOVERED", blockers(g))
        self.assertEqual("NOT_RELEASEABLE", projection(g)["nodes"]["Common#720"]["state"])

    def test_invalid_progress_fact_still_cannot_change_numbers(self):
        g = graph()
        fake = {
            "schema": DELP.FACTS_SCHEMA,
            "responsibility": {"issue": "Common#720"},
            "material": {"candidate_sha": "a" * 40},
            "progress": {"P": 100, "E": 100},
        }
        output = DELP.project(g, [{"source": "test", "order": 1, "facts": fake}], {})
        self.assertTrue(output["rejected_facts"])
        self.assertEqual(0, output["nodes"]["Common#720"]["progress"]["P"])
        self.assertEqual(0, output["nodes"]["Common#720"]["progress"]["E"])


if __name__ == "__main__":
    unittest.main()
