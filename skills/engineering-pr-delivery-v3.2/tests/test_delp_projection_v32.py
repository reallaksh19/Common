"""DELP (Durable Execution Lineage and Projection) regression and adversarial tests.

The central claim under test: agents publish facts only; every percentage, title,
frontier count and ancestor roll-up is recomputed, so an agent cannot move any of
them by writing a number, a title or a weight.
"""

from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import itertools
import json
import pathlib
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "delp_projection_v32.py"
spec = importlib.util.spec_from_file_location("delp_projection_v32", MODULE_PATH)
M = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(M)

try:  # PyYAML is only needed for the markdown-block and CLI-from-YAML paths
    import yaml  # noqa: F401

    HAVE_YAML = True
except ImportError:  # pragma: no cover
    HAVE_YAML = False

try:  # jsonschema is optional: the engine's own validators are authoritative and stdlib-only
    import jsonschema  # noqa: F401

    HAVE_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    HAVE_JSONSCHEMA = False

TAG = M.PROTOCOL_LINE.lower().replace(".", "")  # v35 / v32
SCHEMAS = MODULE_PATH.parents[1] / "schemas"

SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40
SHA_MAIN = "9" * 40  # the head of the base branch in the fake provider
DIGEST = "sha256:" + "d" * 64


def graph(**overrides):
    nodes = [
        {"ref": "Common#527", "kind": "ROOT"},
        {"ref": "Common#588", "kind": "INTERMEDIATE", "parent": "Common#527", "weight": 3},
        {"ref": "Common#610", "kind": "INTERMEDIATE", "parent": "Common#527", "weight": 1},
        {
            "ref": "Common#592",
            "kind": "LEAF",
            "parent": "Common#588",
            "weight": 3,
            "responsibility_id": "P3-I-R2",
            "primary_pr": "Common#593",
            "critical": True,
            "units": [
                {"id": "U01", "weight": 20},
                {"id": "U02", "weight": 30},
                {"id": "U03", "weight": 25},
                {"id": "U04", "weight": 25},
            ],
        },
        {
            "ref": "Common#594",
            "kind": "LEAF",
            "parent": "Common#588",
            "weight": 1,
            "primary_pr": "Common#595",
            "units": [{"id": "V1", "weight": 50}, {"id": "V2", "weight": 50}],
        },
        {
            "ref": "Common#612",
            "kind": "LEAF",
            "parent": "Common#610",
            "weight": 1,
            "primary_pr": "Common#613",
            "units": [{"id": "W1", "weight": 100}],
        },
    ]
    value = {"schema": M.GRAPH_SCHEMA, "programme": {"id": "COMMON-PROD-CONTROL-V1", "root": "Common#527"}, "nodes": nodes}
    value.update(overrides)
    return value


def stable_graph(**overrides):
    value = graph()
    value["programme"]["graph_generation"] = 1
    for node in value["nodes"]:
        if node["kind"] == "LEAF" and not node.get("responsibility_id"):
            node["responsibility_id"] = f"RESP-{M.ref_number(node['ref'])}"
    value.update(overrides)
    return value


def unit(uid, state="COMPLETE", result="VERIFIED", refs=("Common#592#issuecomment-1",), **extra):
    row = {"id": uid, "state": state, "result": result, "evidence_refs": list(refs)}
    row.update(extra)
    return row


def facts(leaf="Common#592", sha=SHA_A, units=(), pr="Common#593", **extra):
    record = {
        "schema": M.FACTS_SCHEMA,
        "responsibility": {"issue": leaf},
        "material": {"pr": pr, "candidate_sha": sha},
        "units": list(units),
    }
    record.update(extra)
    return record


def entry(record, order, source=None):
    return {"source": source or f"c{order}", "order": order, "facts": record}


OBS_A = {
    "Common#592": {"candidate_sha": SHA_A},
    "Common#594": {"candidate_sha": SHA_A},
    "Common#612": {"candidate_sha": SHA_A},
}


class FactsAreTheOnlyAgentInput(unittest.TestCase):
    def test_agent_authored_projection_fields_are_rejected(self):
        bad = [
            {"progress": 72},
            {"title": "🟢 R:P99/E99"},
            {"parent_progress": 72},
            {"programme_progress": {"D": 63}},
            {"activity_epoch": 7},
            {"frontier_count": 3},
            {"weight": 300},
            {"evidence_health": "CURRENT"},
        ]
        for extra in bad:
            with self.subTest(extra=extra):
                errors = M.validate_facts(facts(units=[unit("U01")], **extra))
                self.assertTrue(errors, extra)
                with self.assertRaises(M.ForbiddenProjectionField):
                    M.require_facts(facts(units=[unit("U01")], **extra))

    def test_legacy_agent_asserted_evidenced_flag_is_rejected(self):
        errors = M.validate_facts(facts(units=[unit("U01", evidenced=True)]))
        self.assertTrue(any("evidenced" in e for e in errors), errors)

    def test_nested_weight_or_percent_inside_units_is_rejected(self):
        self.assertTrue(M.validate_facts(facts(units=[unit("U01", weight=20)])))
        self.assertTrue(M.validate_facts(facts(units=[unit("U01", percent=100)])))

    def test_projection_notation_pasted_into_free_text_is_rejected(self):
        for text in ("now R:P80/E40", "phase Φ:D60/E58", "root Π:D72/E70", "{P50% · E50% · U1 · ACTIVE}"):
            with self.subTest(text=text):
                self.assertTrue(M.validate_facts(facts(units=[unit("U01")], next={"action": text})))

    def test_rejected_record_cannot_move_any_number(self):
        good = entry(facts(units=[unit("U01"), unit("U02")]), 1)
        bad = entry(facts(units=[unit("U03"), unit("U04")], progress=100, title="x"), 2, "forged")
        with_bad = M.project(graph(), [good, bad], OBS_A)
        without = M.project(graph(), [good], OBS_A)
        self.assertEqual(without["nodes"]["Common#592"]["progress"], with_bad["nodes"]["Common#592"]["progress"])
        self.assertEqual(without["nodes"]["Common#527"]["progress"], with_bad["nodes"]["Common#527"]["progress"])
        self.assertEqual(["forged"], [r["source"] for r in with_bad["rejected_facts"]])

    def test_facts_cannot_target_a_parent_issue_because_parents_are_not_workspaces(self):
        record = entry(facts(leaf="Common#588", units=[unit("U01")]), 1, "parent-work")
        out = M.project(graph(), [record], OBS_A)
        self.assertEqual(["parent-work"], [r["source"] for r in out["rejected_facts"]])
        self.assertIn("not a declared LEAF", out["rejected_facts"][0]["reasons"][0])

    def test_unknown_leaf_and_responsibility_id_mismatch_are_rejected(self):
        wrong_leaf = entry(facts(leaf="Common#9999", units=[unit("U01")]), 1, "ghost")
        wrong_id = entry(facts(units=[unit("U01")]), 2, "wrongid")
        wrong_id["facts"]["responsibility"]["id"] = "SOMETHING-ELSE"
        out = M.project(graph(), [wrong_leaf, wrong_id], OBS_A)
        self.assertEqual({"ghost", "wrongid"}, {r["source"] for r in out["rejected_facts"]})
        self.assertEqual(0, out["nodes"]["Common#592"]["progress"]["P"])

    def test_quiet_and_stale_are_observed_never_declared(self):
        self.assertTrue(M.validate_facts(facts(activity="QUIET")))
        self.assertTrue(M.validate_facts(facts(activity="STALE")))
        self.assertEqual([], M.validate_facts(facts(activity="WAITING_CI")))

    def test_complete_yes_requires_responsibility_scope(self):
        errors = M.validate_facts(facts(result={"scope": "STEP", "responsibility_complete": "YES"}))
        self.assertTrue(errors)

    def test_candidate_must_be_full_sha(self):
        self.assertTrue(M.validate_facts(facts(sha="abc123", units=[unit("U01")])))


class LeafProgressAndEvidence(unittest.TestCase):
    def leaf(self, ledger, observations=OBS_A):
        return M.project(graph(), ledger, observations)["nodes"]["Common#592"]

    def test_p_and_e_from_declared_unit_weights(self):
        node = self.leaf([entry(facts(units=[unit("U01"), unit("U02")]), 1)])
        self.assertEqual((50, 50), (node["progress"]["P"], node["progress"]["E"]))
        self.assertEqual("CURRENT", node["evidence"]["health"])
        self.assertEqual("U03", node["active_unit"])

    def test_missing_evidence_is_a_visible_gap_not_progress_for_E(self):
        ledger = [
            entry(facts(units=[unit("U01"), unit("U02")]), 1),
            entry(facts(units=[unit("U03", refs=())]), 2),
        ]
        node = self.leaf(ledger)
        self.assertEqual((75, 50), (node["progress"]["P"], node["progress"]["E"]))
        self.assertEqual("EVIDENCE_GAP", node["state"])
        self.assertEqual("GAP", node["evidence"]["health"])
        self.assertEqual([{"unit": "U03", "reason": "NO_EVIDENCE_REFS"}], node["evidence"]["gaps"])
        self.assertEqual("🟡 [#527 › #588 › #592 → PR#593] R:P75/E50 · U04 · EVIDENCE_GAP", node["title_prefix"])

    def test_recovery_evidence_restores_E(self):
        ledger = [
            entry(facts(units=[unit("U01"), unit("U02")]), 1),
            entry(facts(units=[unit("U03", refs=())]), 2),
            entry(facts(units=[unit("U03", refs=("Common#592#issuecomment-9",))]), 3),
        ]
        node = self.leaf(ledger)
        self.assertEqual((75, 75), (node["progress"]["P"], node["progress"]["E"]))
        self.assertEqual("ACTIVE", node["state"])
        self.assertEqual("🟢 [#527 › #588 › #592 → PR#593] R:P75/E75 · U04 · ACTIVE", node["title_prefix"])

    def test_candidate_move_keeps_P_and_drops_E_until_replay(self):
        ledger = [entry(facts(units=[unit("U01"), unit("U02"), unit("U03")]), 1)]
        before = self.leaf(ledger)
        moved = self.leaf(ledger, {"Common#592": {"candidate_sha": SHA_B}})
        self.assertEqual(before["progress"]["P"], moved["progress"]["P"])
        self.assertEqual(75, before["progress"]["E"])
        self.assertEqual(0, moved["progress"]["E"])
        self.assertEqual("EVIDENCE_STALE", moved["state"])
        self.assertEqual("CANDIDATE_MOVED", moved["frontier"]["relation"])
        replay = [entry(facts(sha=SHA_B, units=[unit("U01"), unit("U02"), unit("U03")]), 2)] + ledger
        replayed = self.leaf(replay, {"Common#592": {"candidate_sha": SHA_B}})
        self.assertEqual((75, 75), (replayed["progress"]["P"], replayed["progress"]["E"]))

    def test_partial_replay_counts_only_units_replayed_on_the_new_head(self):
        ledger = [
            entry(facts(units=[unit("U01"), unit("U02")]), 1),
            entry(facts(sha=SHA_B, units=[unit("U01")]), 2),
        ]
        node = self.leaf(ledger, {"Common#592": {"candidate_sha": SHA_B}})
        self.assertEqual(50, node["progress"]["P"])
        self.assertEqual(20, node["progress"]["E"])

    def test_unverified_result_does_not_count_as_evidence(self):
        node = self.leaf([entry(facts(units=[unit("U01", result="PARTIAL")]), 1)])
        self.assertEqual((20, 0), (node["progress"]["P"], node["progress"]["E"]))
        self.assertEqual("RESULT_NOT_ACCEPTED(PARTIAL)", node["evidence"]["gaps"][0]["reason"])

    def test_unobserved_candidate_is_conservative(self):
        node = self.leaf([entry(facts(units=[unit("U01")]), 1)], observations={})
        self.assertEqual(0, node["progress"]["E"])
        self.assertEqual("UNVERIFIABLE", node["evidence"]["health"])
        self.assertEqual("EVIDENCE_GAP", node["state"])

    def test_contract_digest_binding(self):
        g = graph()
        next(n for n in g["nodes"] if n["ref"] == "Common#592")["contract_digest"] = DIGEST
        ok = M.project(g, [entry(facts(units=[unit("U01", contract_digest=DIGEST)]), 1)], OBS_A)["nodes"]["Common#592"]
        bad = M.project(g, [entry(facts(units=[unit("U01")]), 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual(20, ok["progress"]["E"])
        self.assertEqual(0, bad["progress"]["E"])
        self.assertEqual("CONTRACT_DIGEST_MISMATCH", bad["evidence"]["gaps"][0]["reason"])

    def test_evidence_bound_to_another_pr_is_not_current(self):
        node = self.leaf([entry(facts(pr="Common#700", units=[unit("U01")]), 1)])
        self.assertEqual(0, node["progress"]["E"])
        self.assertEqual("PR_MISMATCH", node["evidence"]["gaps"][0]["reason"])

    def test_later_claim_for_a_unit_supersedes_the_earlier_one(self):
        ledger = [
            entry(facts(units=[unit("U01")]), 1),
            entry(facts(units=[unit("U01", state="IN_PROGRESS", result="NOT_RUN", refs=())]), 2),
        ]
        self.assertEqual(0, self.leaf(ledger)["progress"]["P"])

    def test_unknown_unit_is_ignored_with_warning(self):
        node = self.leaf([entry(facts(units=[unit("NOPE")]), 1)])
        self.assertEqual(0, node["progress"]["P"])
        self.assertIn("UNKNOWN_UNIT:NOPE", node["warnings"])

    def test_evidence_never_exceeds_progress_and_roll_up_is_bounded(self):
        states = ["COMPLETE", "IN_PROGRESS"]
        results = ["VERIFIED", "PARTIAL"]
        refs = [("r",), ()]
        shas = [SHA_A, SHA_B]
        for combo in itertools.product(states, results, refs, shas):
            state, result, rf, sha = combo
            ledger = [entry(facts(sha=sha, units=[unit("U01", state, result, rf), unit("U02", state, result, rf)]), 1)]
            out = M.project(graph(), ledger, OBS_A)
            for node in out["nodes"].values():
                p = node["progress"]
                self.assertLessEqual(p.get("E", 0), p.get("P", p.get("D", 100)), combo)
                if "D" in p:
                    self.assertLessEqual(p["E"], 100)
                    self.assertGreaterEqual(p["D"], p["E"], combo)

    def test_activity_and_blockers_never_change_progress(self):
        base = self.leaf([entry(facts(units=[unit("U01")]), 1)])
        noisy = self.leaf(
            [entry(facts(units=[unit("U01")], activity="WAITING_CI", blocker="CI queue", owner_action="NONE"), 1)]
        )
        self.assertEqual(base["progress"], noisy["progress"])
        self.assertEqual("WAITING_CI", noisy["state"])

    def test_a_gates_only_record_does_not_reset_blocker_next_unit_or_activity(self):
        ledger = [
            entry(
                facts(units=[unit("U01")], activity="WAITING_EXTERNAL", blocker="runner unavailable",
                      owner_action="REQUIRED — approve runner", next={"unit": "U03", "action": "resume when runner returns"}),
                1,
            ),
            entry(facts(units=[], gates=[{"id": "REVIEWER_ACCEPTANCE", "result": "NOT_RUN"}]), 2),
        ]
        g = graph()
        next(n for n in g["nodes"] if n["ref"] == "Common#592")["delivery_gates"] = [{"id": "REVIEWER_ACCEPTANCE", "weight": 10}]
        node = M.project(g, ledger, OBS_A)["nodes"]["Common#592"]
        self.assertEqual("WAITING_EXTERNAL", node["state"])
        self.assertEqual("runner unavailable", node["blocker"])
        self.assertEqual("REQUIRED — approve runner", node["owner_action"])
        self.assertEqual("U03", node["active_unit"])

    def test_evidence_frontier_is_the_candidate_of_the_latest_evidence_record(self):
        ledger = [entry(facts(units=[unit("U01")]), 1), entry(facts(sha=SHA_B, units=[unit("U02")]), 2)]
        node = self.leaf(ledger, {"Common#592": {"candidate_sha": SHA_B}})
        self.assertEqual(SHA_B, node["frontier"]["evidence_candidate"])
        self.assertEqual("ALIGNED", node["frontier"]["relation"])

    def test_activity_epoch_counts_accepted_checkpoints_only(self):
        ledger = [entry(facts(units=[unit("U01")]), 1), entry(facts(units=[unit("U02")], progress=1), 2)]
        self.assertEqual(1, self.leaf(ledger)["activity_epoch"])

    def test_duplicate_publication_is_idempotent_for_numbers(self):
        once = [entry(facts(units=[unit("U01"), unit("U02")]), 1)]
        twice = once + [entry(facts(units=[unit("U01"), unit("U02")]), 2)]
        self.assertEqual(self.leaf(once)["progress"], self.leaf(twice)["progress"])

    def test_ledger_order_uses_order_field_not_list_position(self):
        a = entry(facts(units=[unit("U01")]), 2)
        b = entry(facts(units=[unit("U01", state="IN_PROGRESS", result="NOT_RUN", refs=())]), 1)
        self.assertEqual(20, self.leaf([a, b])["progress"]["P"])
        self.assertEqual(20, self.leaf([b, a])["progress"]["P"])

    def test_not_started_leaf_is_idle_white(self):
        node = self.leaf([], observations={})
        self.assertEqual("NOT_STARTED", node["state"])
        self.assertEqual("⚪ [#527 › #588 › #592 → PR#593] R:P0/E0 · U01 · NOT_STARTED", node["title_prefix"])


class CompletionAndDelivery(unittest.TestCase):
    ALL = [unit("U01"), unit("U02"), unit("U03"), unit("U04")]

    def test_complete_requires_result_units_current_evidence(self):
        done = entry(facts(units=self.ALL, result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1)
        node = M.project(graph(), [done], OBS_A)["nodes"]["Common#592"]
        self.assertEqual("COMPLETE", node["lifecycle"])
        self.assertEqual("✅ [#527 › #588 › #592 → PR#593] R:P100/E100 · COMPLETE", node["title_prefix"])

    def test_complete_claim_with_open_units_does_not_complete(self):
        claim = entry(
            facts(units=[unit("U01")], result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1
        )
        node = M.project(graph(), [claim], OBS_A)["nodes"]["Common#592"]
        self.assertNotEqual("COMPLETE", node["lifecycle"])
        self.assertIn("RESULT_CLAIMS_COMPLETE_BUT_UNITS_OPEN", node["warnings"])

    def test_complete_claim_without_current_evidence_does_not_complete(self):
        claim = entry(
            facts(sha=SHA_B, units=self.ALL, result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1
        )
        node = M.project(graph(), [claim], OBS_A)["nodes"]["Common#592"]
        self.assertNotEqual("COMPLETE", node["lifecycle"])
        self.assertIn("COMPLETE_CLAIM_WITHOUT_CURRENT_EVIDENCE", node["warnings"])

    def test_superseded_leaf_keeps_its_planned_weight(self):
        rec = entry(facts(units=[unit("U01")], result={"scope": "STEP", "responsibility_complete": "NO", "superseded_by": "Common#700"}), 1)
        out = M.project(graph(), [rec], OBS_A)
        self.assertEqual("SUPERSEDED", out["nodes"]["Common#592"]["state"])
        self.assertEqual(3, out["nodes"]["Common#592"]["weight"])

    def gated_graph(self):
        g = graph()
        leaf = next(n for n in g["nodes"] if n["ref"] == "Common#592")
        leaf["delivery_gates"] = [
            {"id": "REVIEWER_ACCEPTANCE", "weight": 20},
            {"id": "SUPER_REVIEW", "weight": 15},
            {"id": "HANDOFF", "weight": 5},
        ]
        leaf["coder_weight"] = 60
        return g

    def test_coder_p100_never_means_delivery_100(self):
        node = M.project(self.gated_graph(), [entry(facts(units=self.ALL), 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual((100, 100, 60, 60), tuple(node["progress"][k] for k in ("P", "E", "D", "DE")))

    def test_delivery_gates_add_only_with_current_evidence(self):
        gates = [
            {"id": "REVIEWER_ACCEPTANCE", "result": "PASSED", "evidence_refs": ["r"]},
            {"id": "SUPER_REVIEW", "result": "PASSED", "evidence_refs": []},
        ]
        node = M.project(self.gated_graph(), [entry(facts(units=self.ALL, gates=gates), 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual(95, node["progress"]["D"])
        self.assertEqual(80, node["progress"]["DE"])

    def test_gates_passed_without_current_evidence_do_not_complete_the_leaf(self):
        gates = [{"id": g_id, "result": "PASSED", "evidence_refs": []} for g_id in ("REVIEWER_ACCEPTANCE", "SUPER_REVIEW", "HANDOFF")]
        done = entry(
            facts(units=self.ALL, gates=gates, result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1
        )
        node = M.project(self.gated_graph(), [done], OBS_A)["nodes"]["Common#592"]
        self.assertEqual((100, 60), (node["progress"]["D"], node["progress"]["DE"]))  # passed gates add D but not DE
        self.assertNotEqual("COMPLETE", node["lifecycle"])
        self.assertIn("COMPLETE_CLAIM_WITH_UNEVIDENCED_DELIVERY_GATES", node["warnings"])
        evidenced = [{**g_row, "evidence_refs": ["r"]} for g_row in gates]
        done = entry(
            facts(units=self.ALL, gates=evidenced, result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1
        )
        node = M.project(self.gated_graph(), [done], OBS_A)["nodes"]["Common#592"]
        self.assertEqual("COMPLETE", node["lifecycle"])

    def test_leaf_with_open_gates_does_not_complete(self):
        done = entry(facts(units=self.ALL, result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1)
        node = M.project(self.gated_graph(), [done], OBS_A)["nodes"]["Common#592"]
        self.assertNotEqual("COMPLETE", node["lifecycle"])
        self.assertIn("COMPLETE_CLAIM_WITH_OPEN_DELIVERY_GATES", node["warnings"])


class RollUpIsRecomputedNeverIncremented(unittest.TestCase):
    LEDGER = [
        entry(facts(units=[unit("U01"), unit("U02"), unit("U03")]), 1),
        entry(facts(leaf="Common#612", pr="Common#613", units=[unit("W1", refs=("r",))]), 2),
    ]

    def test_weighted_roll_up_matches_hand_computation(self):
        out = M.project(graph(), self.LEDGER, OBS_A)["nodes"]
        # #588 = (3*0.75 + 1*0) / 4 = 56.25 -> 56 ; #610 = 100 ; root = (3*0.5625 + 1*1) / 4 = 67.1875 -> 67
        self.assertEqual((56, 56), (out["Common#588"]["progress"]["D"], out["Common#588"]["progress"]["E"]))
        self.assertEqual((100, 100), (out["Common#610"]["progress"]["D"], out["Common#610"]["progress"]["E"]))
        self.assertEqual((67, 67), (out["Common#527"]["progress"]["D"], out["Common#527"]["progress"]["E"]))
        self.assertEqual("9/16", out["Common#588"]["progress"]["ratio"]["D"])
        self.assertEqual("43/64", out["Common#527"]["progress"]["ratio"]["D"])

    def test_projection_is_pure_and_idempotent(self):
        first = M.project(graph(), self.LEDGER, OBS_A)
        second = M.project(copy.deepcopy(graph()), copy.deepcopy(self.LEDGER), copy.deepcopy(OBS_A))
        self.assertEqual(first, second)

    def test_parent_numbers_cannot_be_authored_through_a_child_record(self):
        forged = entry(facts(units=[unit("U01")], parent_progress=100, programme_progress=100), 9, "forged")
        out = M.project(graph(), self.LEDGER + [forged], OBS_A)
        self.assertEqual(67, out["nodes"]["Common#527"]["progress"]["D"])

    def test_undecomposed_reserve_counts_as_zero_and_blocks_complete(self):
        g = graph()
        next(n for n in g["nodes"] if n["ref"] == "Common#610")["reserve_weight"] = 1
        done = [
            entry(facts(units=[unit(u) for u in ("U01", "U02", "U03", "U04")]), 1),
            entry(facts(leaf="Common#594", pr="Common#595", units=[unit("V1"), unit("V2")]), 2),
            entry(facts(leaf="Common#612", pr="Common#613", units=[unit("W1")]), 3),
        ]
        out = M.project(g, done, OBS_A)["nodes"]
        self.assertEqual(50, out["Common#610"]["progress"]["D"])
        self.assertNotEqual("COMPLETE", out["Common#610"]["state"])
        self.assertIn("UNDECOMPOSED_RESERVE:1", out["Common#610"]["warnings"])

    def test_programme_completes_only_when_every_leaf_is_complete(self):
        res = {"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}
        done = [
            entry(facts(units=[unit(u) for u in ("U01", "U02", "U03", "U04")], result=res), 1),
            entry(facts(leaf="Common#594", pr="Common#595", units=[unit("V1"), unit("V2")], result=res), 2),
            entry(facts(leaf="Common#612", pr="Common#613", units=[unit("W1")], result=res), 3),
        ]
        out = M.project(graph(), done, OBS_A)["nodes"]
        self.assertEqual("COMPLETE", out["Common#527"]["state"])
        self.assertEqual("✅ [#527] Π:D100/E100 · F0 · COMPLETE", out["Common#527"]["title_prefix"])

    def test_frontier_count_and_titles(self):
        out = M.project(graph(), self.LEDGER, OBS_A)["nodes"]
        self.assertEqual(2, out["Common#527"]["frontier"]["count"])
        self.assertEqual("🟢 [#527] Π:D67/E67 · F2 · ACTIVE", out["Common#527"]["title_prefix"])
        self.assertEqual("🟢 [#527 › #588 → #592/PR#593] Φ:D56/E56 · F1 · ACTIVE", out["Common#588"]["title_prefix"])

    def test_evidence_gap_in_a_leaf_surfaces_on_every_ancestor_without_averaging_colours(self):
        stale = {**OBS_A, "Common#592": {"candidate_sha": SHA_B}}
        out = M.project(graph(), self.LEDGER, stale)["nodes"]
        self.assertEqual("EVIDENCE_GAP", out["Common#588"]["state"])
        self.assertEqual("EVIDENCE_GAP", out["Common#527"]["state"])
        self.assertTrue(out["Common#527"]["title_prefix"].startswith("🟡"))
        # D is unaffected by evidence; E drops
        self.assertEqual(67, out["Common#527"]["progress"]["D"])
        self.assertLess(out["Common#527"]["progress"]["E"], out["Common#527"]["progress"]["D"])

    def test_critical_stale_leaf_turns_ancestors_red_and_noncritical_does_not(self):
        crit = {**OBS_A, "Common#592": {"candidate_sha": SHA_A, "liveness": "STALE"}}
        out = M.project(graph(), self.LEDGER, crit)["nodes"]
        self.assertEqual("STALE", out["Common#527"]["state"])
        self.assertTrue(out["Common#527"]["title_prefix"].startswith("🔴"))
        noncrit_ledger = [entry(facts(leaf="Common#594", pr="Common#595", units=[unit("V1")]), 1)]
        noncrit = {**OBS_A, "Common#594": {"candidate_sha": SHA_A, "liveness": "STALE"}}
        out2 = M.project(graph(), noncrit_ledger, noncrit)["nodes"]
        self.assertNotEqual("STALE", out2["Common#527"]["state"])

    def test_critical_waiting_leaf_turns_ancestors_blue(self):
        ledger = [entry(facts(units=[unit("U01")], activity="WAITING_CI"), 1)]
        out = M.project(graph(), ledger, OBS_A)["nodes"]
        self.assertEqual("WAITING", out["Common#588"]["state"])
        self.assertTrue(out["Common#588"]["title_prefix"].startswith("🔵"))

    def test_multi_leaf_frontier_summary_is_capped(self):
        g = graph()
        extra = [
            {
                "ref": f"Common#{800 + i}",
                "kind": "LEAF",
                "parent": "Common#588",
                "weight": 1,
                "primary_pr": f"Common#{900 + i}",
                "units": [{"id": "X1", "weight": 1}],
            }
            for i in range(3)
        ]
        g["nodes"].extend(extra)
        ledger = [
            entry(facts(leaf="Common#592", units=[unit("U01")]), 1),
            entry(facts(leaf="Common#594", pr="Common#595", units=[unit("V1")]), 2),
        ] + [entry(facts(leaf=e["ref"], pr=e["primary_pr"], units=[unit("X1")]), 3 + i) for i, e in enumerate(extra)]
        out = M.project(g, ledger, {})["nodes"]["Common#588"]
        self.assertIn("[#527 › #588 → #592/PR#593, #594/PR#595, +3] Φ:D", out["title_prefix"])


class TitleGrammar(unittest.TestCase):
    def test_round_trip_and_base_recovery(self):
        node = M.project(graph(), [entry(facts(units=[unit("U01")]), 1)], OBS_A)["nodes"]["Common#592"]
        title = M.render_title(node["title_prefix"], "Add replay lane")
        info, base = M.split_title(title)
        self.assertEqual("Add replay lane", base)
        self.assertEqual("R", info["scope"])
        self.assertEqual(title, M.render_title(node["title_prefix"], base))

    def test_legacy_formats_are_recognised_and_stripped(self):
        self.assertEqual(({"legacy": "SUFFIX"}, "Task"), M.split_title("Task {P50% · E50% · UNIT-02 · IMPLEMENTING}"))
        self.assertEqual(({"legacy": "PREFIX"}, "Task"), M.split_title("🟢 {P42% · E31% · A07 · U03 · ACTIVE} Task"))
        self.assertEqual((None, "Plain title"), M.split_title("Plain title"))

    def test_base_title_containing_an_em_dash_survives(self):
        title = M.render_title("🟢 [#527] Π:D1/E1 · F0 · ACTIVE", "A — B")
        self.assertEqual("A — B", M.split_title(title)[1])

    def test_title_drift_classification(self):
        prefix = "🟢 [#527] Π:D67/E67 · F2 · ACTIVE"
        good = M.render_title(prefix, "Programme")
        self.assertEqual("OK", M.title_drift(good, prefix)["status"])
        self.assertEqual("STALE_OR_HAND_EDITED", M.title_drift("🟢 [#527] Π:D99/E99 · F2 · ACTIVE — Programme", prefix)["status"])
        self.assertEqual("MISSING_PROJECTION", M.title_drift("Programme", prefix)["status"])
        self.assertEqual("LEGACY_FORMAT", M.title_drift("Programme {P1% · E1% · U · ACTIVE}", prefix)["status"])

    def test_long_titles_truncate_the_human_base_not_the_projection(self):
        prefix = "🟢 [#527] Π:D67/E67 · F2 · ACTIVE"
        title = M.render_title(prefix, "x" * 400)
        self.assertLessEqual(len(title), M.TITLE_LIMIT)
        self.assertTrue(title.startswith(prefix))

    def test_percent_rounding_never_shows_100_or_0_falsely(self):
        F = M.Fraction
        self.assertEqual(100, M.percent(F(1)))
        self.assertEqual(99, M.percent(F(996, 1000)))
        self.assertEqual(0, M.percent(F(0)))
        self.assertEqual(1, M.percent(F(1, 1000)))
        self.assertEqual(13, M.percent(F(125, 1000)))  # half-up, not banker's


class ContinuationAdmission(unittest.TestCase):
    LEDGER = [
        entry(facts(units=[unit("U01"), unit("U02"), unit("U03")], next={"unit": "U04", "action": "negative replay"}), 1),
        entry(facts(leaf="Common#612", pr="Common#613", units=[unit("W1", refs=("r",))]), 2),
    ]

    def test_commands_that_must_pass_the_admission_barrier(self):
        for text in ("continue", "Proceed", "next", "resume", "reconcile", "take over", "keep going", "continue please!"):
            self.assertTrue(M.classify_continuation(text), text)
        for text in ("continue with the refactor", "please add tests", "what next"):
            self.assertFalse(M.classify_continuation(text), text)

    def test_current_evidence_continues_the_exact_unit_with_scoped_checkpoint(self):
        proj = M.project(graph(), self.LEDGER, OBS_A)
        report = M.admit(proj, "Common#592", "continue")
        self.assertEqual("CONTINUE_UNIT", report["action"])
        self.assertFalse(report["recovery_required"])
        self.assertEqual([], report["authority_effects"])
        self.assertEqual(
            "\n".join(
                [
                    "CONTINUE CHECKPOINT",
                    "",
                    "PATH: #527 → #588 → #592 → PR#593",
                    "CHILD: R:P75/E75 · U04 · ACTIVE",
                    "EVIDENCE: CURRENT @ aaaaaaa",
                    "PARENT: #588 Φ:D56/E56",
                    "ROOT: #527 Π:D67/E67",
                    "BLOCKER: NONE",
                    "OWNER_ACTION: NONE",
                    "NEXT: U04 — negative replay",
                ]
            ),
            M.render_checkpoint(report),
        )

    def test_evidence_gap_forces_recovery_before_new_coding(self):
        moved = {**OBS_A, "Common#592": {"candidate_sha": SHA_B}}
        report = M.admit(M.project(graph(), self.LEDGER, moved), "Common#592", "proceed")
        self.assertEqual("RECOVER_EVIDENCE", report["action"])
        self.assertTrue(report["recovery_required"])
        text = M.render_checkpoint(report)
        self.assertIn("NEXT: RECOVER_EVIDENCE before new coding", text)
        self.assertIn("EVIDENCE: STALE_CANDIDATE (evidence @ aaaaaaa, live @ bbbbbbb)", text)

    def test_admission_is_pure_and_never_changes_graph_or_projection(self):
        proj = M.project(graph(), self.LEDGER, OBS_A)
        before = copy.deepcopy(proj)
        M.admit(proj, "Common#592", "continue")
        self.assertEqual(before, proj)

    def test_admission_requires_a_leaf(self):
        proj = M.project(graph(), self.LEDGER, OBS_A)
        with self.assertRaises(M.DelpError):
            M.admit(proj, "Common#588")


class GraphValidation(unittest.TestCase):
    def bad(self, mutate):
        g = copy.deepcopy(graph())
        mutate(g)
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)

    def test_structural_errors(self):
        self.bad(lambda g: g["nodes"].append(dict(g["nodes"][1])))  # duplicate
        self.bad(lambda g: g["nodes"][1].__setitem__("parent", "Common#99999"))  # missing parent
        self.bad(lambda g: g["nodes"].append({"ref": "Common#2", "kind": "ROOT"}))  # two roots
        self.bad(lambda g: g["nodes"][3]["units"][0].__setitem__("weight", 0))  # non-positive weight
        self.bad(lambda g: g["nodes"][3].__setitem__("units", []))  # leaf without units
        self.bad(lambda g: g["nodes"][3].__setitem__("reserve_weight", 2))  # reserve on a leaf
        self.bad(lambda g: g["nodes"].append({"ref": "Common#700", "kind": "INTERMEDIATE", "parent": "Common#527", "weight": 1}))  # childless
        self.bad(lambda g: g["nodes"].append({"ref": "Common#701", "kind": "LEAF", "parent": "Common#592", "weight": 1, "units": [{"id": "A", "weight": 1}]}))  # child of a leaf

    def test_cycle_is_rejected(self):
        def mutate(g):
            g["nodes"][1]["parent"] = "Common#610"
            g["nodes"][2]["parent"] = "Common#588"

        self.bad(mutate)

    def test_agent_cannot_change_the_plan_through_facts(self):
        # weights live only in the graph: a facts record that carries one is rejected outright
        self.assertTrue(M.validate_facts(facts(units=[unit("U01", weight=999)])))

    def test_graph_generation_and_stable_responsibility_identity(self):
        g = stable_graph()
        indexed = M.validate_graph(g)
        self.assertEqual(1, indexed["programme"]["graph_generation"])
        self.assertEqual("P3-I-R2", indexed["nodes"]["Common#592"]["responsibility_id"])
        self.assertEqual(indexed["digest"], M.project(g, [], OBS_A)["graph_digest"])

    def test_declared_graph_generation_requires_every_leaf_identity(self):
        g = stable_graph()
        g["nodes"][4].pop("responsibility_id")
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)

    def test_responsibility_identity_must_be_unique(self):
        g = stable_graph()
        g["nodes"][4]["responsibility_id"] = "P3-I-R2"
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)

    def test_graph_generation_must_be_positive_integer(self):
        for value in (0, True):
            g = stable_graph()
            g["programme"]["graph_generation"] = value
            with self.assertRaises(M.GraphError):
                M.validate_graph(g)

    def test_legacy_graph_without_generation_remains_readable_and_normalizes_to_one(self):
        indexed = M.validate_graph(graph())
        self.assertEqual(1, indexed["programme"]["graph_generation"])

    def test_explicit_default_generation_does_not_change_graph_digest(self):
        explicit = stable_graph()
        legacy = copy.deepcopy(explicit)
        legacy["programme"].pop("graph_generation")
        self.assertEqual(M.validate_graph(explicit)["digest"], M.validate_graph(legacy)["digest"])

    def test_responsibility_id_is_not_synthesized_from_issue_locator(self):
        g = stable_graph()
        leaf = next(n for n in g["nodes"] if n["ref"] == "Common#592")
        stable_id = leaf["responsibility_id"]
        leaf["ref"] = "Common#999"
        # Repair references that identify the provider locator; the semantic Responsibility id is unchanged.
        for node in g["nodes"]:
            if node.get("parent") == "Common#592":
                node["parent"] = "Common#999"
        indexed = M.validate_graph(g)
        self.assertEqual(stable_id, indexed["nodes"]["Common#999"]["responsibility_id"])



class ExtractFactsBlocks(unittest.TestCase):
    BODY = """TASK_EVIDENCE — CHECKPOINT

Narrative prose is for humans. Coverage was 100% on the suite.

```yaml
CHECKPOINT_FACTS_V1:
  responsibility: {issue: Common#592, id: P3-I-R2}
  material: {pr: Common#593, candidate_sha: __SHA__}
  units:
    - id: U04
      state: COMPLETE
      result: VERIFIED
      evidence_refs: [Common#592#issuecomment-12]
  next: {unit: U05, action: negative replay}
  blocker: NONE
  owner_action: NONE
```
"""

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_block_is_parsed_and_prose_is_ignored(self):
        blocks = M.extract_facts_blocks(self.BODY.replace("__SHA__", SHA_A))
        self.assertEqual(1, len(blocks))
        self.assertEqual([], M.validate_facts(blocks[0]))
        self.assertEqual("U04", blocks[0]["units"][0]["id"])

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_prose_percentages_outside_a_block_are_not_facts(self):
        self.assertEqual([], M.extract_facts_blocks("Phase is at R:P80/E40 apparently"))

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_forged_block_with_progress_is_rejected_by_the_ledger(self):
        body = self.BODY.replace("__SHA__", SHA_A).replace("blocker: NONE", "progress: 99")
        record = M.extract_facts_blocks(body)[0]
        out = M.project(graph(), [entry(record, 1, "forged")], OBS_A)
        self.assertEqual("forged", out["rejected_facts"][0]["source"])
        self.assertEqual(0, out["nodes"]["Common#592"]["progress"]["P"])


class CompareAndSwap(unittest.TestCase):
    def doc(self, digest, ref="Common#592"):
        return {"schema": M.STATUS_SCHEMA, "authority": M.AUTHORITY, "node": {"ref": ref}, "projection": {"version": 0, "input_digest": digest}}

    def test_first_write_then_unchanged_is_idempotent(self):
        store = M.InMemoryStore({"Common#592": "Human title"})
        compute = lambda: (self.doc("sha256:" + "1" * 64), "T")  # noqa: E731
        first = M.apply_projection(store, "Common#592", compute)
        second = M.apply_projection(store, "Common#592", compute)
        self.assertEqual(("WRITTEN", 1), (first["status"], first["version"]))
        self.assertEqual(("UNCHANGED", 1), (second["status"], second["version"]))
        self.assertEqual(1, len(store.writes))

    def test_stale_expected_version_is_rejected(self):
        store = M.InMemoryStore()
        store.write("Common#592", None, self.doc("sha256:" + "1" * 64), "T")
        with self.assertRaises(M.ProjectionConflict):
            store.write("Common#592", None, self.doc("sha256:" + "2" * 64), "T")

    def test_lost_race_recomputes_from_fresh_inputs_instead_of_overwriting(self):
        store = M.InMemoryStore()
        truth = {"digest": "sha256:" + "1" * 64}
        calls = {"n": 0}

        class Racy(M.InMemoryStore):
            def write(self, ref, expected, document, title):
                if calls["n"] == 1:  # a competing writer lands between our read and our write
                    truth["digest"] = "sha256:" + "2" * 64
                    super().write(ref, expected, self_doc(truth["digest"]), "competitor")
                return super().write(ref, expected, document, title)

        def self_doc(digest):
            return {"schema": M.STATUS_SCHEMA, "authority": M.AUTHORITY, "node": {}, "projection": {"version": 0, "input_digest": digest}}

        store = Racy()

        def compute():
            calls["n"] += 1
            return self_doc(truth["digest"]), f"title-{truth['digest'][7:9]}"

        result = M.apply_projection(store, "Common#592", compute)
        self.assertEqual("WRITTEN", result["status"])
        self.assertEqual(2, result["attempts"])
        self.assertEqual(2, store.read("Common#592")["version"] - 0)  # competitor v1, ours v2
        self.assertEqual(truth["digest"], store.status["Common#592"]["digest"])
        self.assertEqual("title-22", store.titles["Common#592"])

    def test_hand_edited_title_is_corrected_and_flagged(self):
        store = M.InMemoryStore({"Common#592": "🟢 [#527] Π:D99/E99 · F9 · ACTIVE — hand edit"})
        store.write("Common#592", None, self.doc("sha256:" + "1" * 64), "🟢 [#527] Π:D99/E99 · F9 · ACTIVE — hand edit")
        store.titles["Common#592"] = "totally different"
        result = M.apply_projection(store, "Common#592", lambda: (self.doc("sha256:" + "1" * 64), "derived title"))
        self.assertEqual("WRITTEN", result["status"])
        self.assertTrue(result["title_corrected"])
        self.assertEqual("derived title", store.titles["Common#592"])

    def test_persistent_conflict_surfaces_rather_than_looping(self):
        class Always(M.InMemoryStore):
            def write(self, ref, expected, document, title):
                raise M.ProjectionConflict("always")

        with self.assertRaises(M.ProjectionConflict):
            M.apply_projection(Always(), "Common#592", lambda: (self.doc("sha256:" + "1" * 64), "t"), max_attempts=3)


class FakeGitHub:
    """Minimal GitHub transport with issues, comments and pulls for GitHubStore tests."""

    def __init__(self):
        self.issues = {}
        self.comments = {}
        self.pulls = {}
        self.commits = {"main": SHA_MAIN}
        self.compares = {}
        self.next_id = 100
        self.on_patch_comment = None
        self.calls = []

    def get_issue(self, number):
        self.calls.append(("GET_ISSUE", number))
        return {"number": number, "title": self.issues.get(number, "")}

    def get_pull(self, number):
        return self.pulls[number]

    def get_commit_sha(self, ref):
        return self.commits[ref]

    def compare(self, base, head):
        self.calls.append(("COMPARE", base, head))
        return dict(self.compares.get(head, {"ahead_by": 0, "behind_by": 0}))

    def list_comments(self, number):
        return [dict(c) for c in self.comments.get(number, [])]

    def post_comment(self, number, body):
        self.next_id += 1
        row = {"id": self.next_id, "body": body}
        self.comments.setdefault(number, []).append(row)
        self.calls.append(("POST", number))
        return dict(row)

    def patch_comment(self, comment_id, body):
        self.calls.append(("PATCH_COMMENT", comment_id))
        for rows in self.comments.values():
            for row in rows:
                if row["id"] == comment_id:
                    row["body"] = body
        if self.on_patch_comment:
            self.on_patch_comment(comment_id)
        return {"id": comment_id}

    def patch_title(self, number, title):
        self.calls.append(("PATCH_TITLE", number))
        self.issues[number] = title
        return {"number": number}


def doc_for(ref, digest):
    return {"schema": M.STATUS_SCHEMA, "authority": M.AUTHORITY, "node": {"ref": ref}, "projection": {"version": 0, "input_digest": digest}}


class GitHubStoreTests(unittest.TestCase):
    D1 = "sha256:" + "1" * 64
    D2 = "sha256:" + "2" * 64

    def test_write_creates_then_updates_one_managed_comment_and_title(self):
        gh = FakeGitHub()
        gh.issues[592] = "Add replay lane"
        store = M.GitHubStore(gh)
        self.assertEqual(1, store.write("Common#592", None, doc_for("Common#592", self.D1), "T1 — Add replay lane"))
        self.assertEqual(2, store.write("Common#592", 1, doc_for("Common#592", self.D2), "T2 — Add replay lane"))
        self.assertEqual(1, len(gh.comments[592]))
        self.assertEqual("T2 — Add replay lane", gh.issues[592])
        marker = M.read_status_marker(gh.comments[592][0]["body"])
        self.assertEqual({"version": 2, "input_digest": self.D2}, marker)

    def test_stale_expected_version_is_rejected_before_writing(self):
        gh = FakeGitHub()
        store = M.GitHubStore(gh)
        store.write("Common#592", None, doc_for("Common#592", self.D1), "T")
        with self.assertRaises(M.ProjectionConflict):
            store.write("Common#592", None, doc_for("Common#592", self.D2), "T")
        self.assertEqual(1, len([c for c in gh.calls if c[0] == "POST"]))

    def test_readback_detects_a_competing_write_that_landed_after_ours(self):
        gh = FakeGitHub()
        store = M.GitHubStore(gh)
        store.write("Common#592", None, doc_for("Common#592", self.D1), "T")

        def competitor(comment_id):
            gh.comments[592][0]["body"] = M.render_status_comment(
                {"schema": M.STATUS_SCHEMA, "projection": {"version": 9, "input_digest": self.D2}}
            )

        gh.on_patch_comment = competitor
        with self.assertRaises(M.ProjectionConflict):
            store.write("Common#592", 1, doc_for("Common#592", self.D2), "T")

    def test_leaf_without_a_pr_observes_its_candidate_ref_head(self):
        gh = FakeGitHub()
        gh.pulls[595] = {"head": {"sha": SHA_B}, "state": "open", "merged": False}
        gh.pulls[593] = {"head": {"sha": SHA_A}, "state": "closed", "merged": True}
        gh.commits["investigate/592"] = SHA_C
        gh.compares["investigate/592"] = {"ahead_by": 9, "behind_by": 4}
        g = graph()
        leaf = next(n for n in g["nodes"] if n["ref"] == "Common#612")
        leaf.pop("primary_pr")
        leaf["candidate_ref"] = "investigate/592"
        observed = M.observe_github(gh, g)
        self.assertEqual({"candidate_sha": SHA_C, "ahead_by": 9, "behind_by": 4, "base_sha": SHA_MAIN}, observed["Common#612"])
        self.assertEqual(SHA_MAIN, observed["Common#594"]["base_sha"])  # every leaf is measured against the same base head
        self.assertIn(("COMPARE", "main", "investigate/592"), gh.calls)  # the base defaults to main
        gh.commits["release/2"] = SHA_B
        g["programme"]["base_ref"] = "release/2"
        self.assertEqual(SHA_B, M.observe_github(gh, g)["Common#612"]["base_sha"])
        self.assertIn(("COMPARE", "release/2", "investigate/592"), gh.calls)
        self.assertEqual(SHA_C, observed["Common#612"]["candidate_sha"])
        self.assertEqual(SHA_B, observed["Common#594"]["candidate_sha"])
        self.assertEqual("MERGED", observed["Common#592"]["pr_state"])

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_facts_from_untrusted_authors_are_rejected_not_believed(self):
        gh = FakeGitHub()
        body = ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A)
        gh.comments[592] = [
            {"id": 5, "body": body, "author_association": "NONE", "user": {"login": "drive-by"}},
            {"id": 6, "body": body, "author_association": "COLLABORATOR", "user": {"login": "teammate"}},
        ]
        g = graph()
        ledger = M.ledger_from_github(gh, g)
        self.assertEqual(["drive-by"], [r["untrusted_author"] for r in ledger if "untrusted_author" in r])
        out = M.project(g, ledger, OBS_A)
        self.assertEqual(["Common#592#issuecomment-5"], [r["source"] for r in out["rejected_facts"]])
        self.assertIn("not a trusted fact author", out["rejected_facts"][0]["reasons"][0])
        self.assertEqual(25, out["nodes"]["Common#592"]["progress"]["P"])  # only the trusted record counted
        self.assertEqual(1, out["nodes"]["Common#592"]["activity_epoch"])

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_explicit_fact_author_allowlist_overrides_association(self):
        gh = FakeGitHub()
        body = ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A)
        gh.comments[592] = [
            {"id": 5, "body": body, "author_association": "OWNER", "user": {"login": "someone-else"}},
            {"id": 6, "body": body, "author_association": "NONE", "user": {"login": "coder-bot"}},
        ]
        g = graph()
        g["programme"]["fact_authors"] = ["coder-bot"]
        untrusted = [r["source"] for r in M.ledger_from_github(gh, g) if "untrusted_author" in r]
        self.assertEqual(["Common#592#issuecomment-5"], untrusted)

    def test_multiple_managed_comments_fail_closed(self):
        gh = FakeGitHub()
        body = M.render_status_comment({"schema": M.STATUS_SCHEMA, "projection": {"version": 1, "input_digest": self.D1}})
        gh.comments[592] = [{"id": 1, "body": body}, {"id": 2, "body": body}]
        with self.assertRaises(M.DelpError):
            M.GitHubStore(gh).read("Common#592")

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_end_to_end_observe_project_and_write_every_node_then_noop(self):
        gh = FakeGitHub()
        for number, title in {527: "Programme", 588: "Phase 3", 610: "Phase 4", 592: "Replay lane", 594: "Gate lane", 612: "Closeout"}.items():
            gh.issues[number] = title
        for number, sha in {593: SHA_A, 595: SHA_A, 613: SHA_A}.items():
            gh.pulls[number] = {"head": {"sha": sha}, "state": "open", "merged": False}
        body = ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A)
        gh.comments[592] = [{"id": 5, "body": body, "author_association": "OWNER", "user": {"login": "reallaksh19"}}]
        g = graph()
        report = M.sync_projection(
            M.GitHubStore(gh),
            g,
            lambda: M.ledger_from_github(gh, g),
            lambda: M.observe_github(gh, g),
            {f"Common#{n}": t for n, t in gh.issues.items()},
        )
        self.assertTrue(all(r["status"] == "WRITTEN" for r in report.values()), report)
        self.assertTrue(gh.issues[592].startswith("🟢 [#527 › #588 › #592 → PR#593] R:P25/E25 · U01 · ACTIVE"))
        self.assertTrue(gh.issues[592].endswith("— Replay lane"))
        self.assertTrue(gh.issues[527].endswith("— Programme"))
        # a second pass with unchanged truth writes nothing
        before = [c for c in gh.calls if c[0] in {"POST", "PATCH_COMMENT", "PATCH_TITLE"}]
        titles = {f"Common#{n}": t for n, t in gh.issues.items()}
        again = M.sync_projection(M.GitHubStore(gh), g, lambda: M.ledger_from_github(gh, g), lambda: M.observe_github(gh, g), titles)
        self.assertTrue(all(r["status"] == "UNCHANGED" for r in again.values()), again)
        self.assertEqual(before, [c for c in gh.calls if c[0] in {"POST", "PATCH_COMMENT", "PATCH_TITLE"}])

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_dry_run_plan_reads_only_and_reports_drift_and_rejections(self):
        gh = FakeGitHub()
        for number, title in {527: "Programme", 588: "Phase", 610: "Phase 4", 592: "Hand-edited R:P99/E99", 594: "Gate", 612: "Close"}.items():
            gh.issues[number] = title
        for number in (593, 595, 613):
            gh.pulls[number] = {"head": {"sha": SHA_A}, "state": "open", "merged": False}
        body = ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A)
        gh.comments[592] = [
            {"id": 5, "body": body, "author_association": "OWNER", "user": {"login": "o"}},
            {"id": 6, "body": body, "author_association": "NONE", "user": {"login": "drive-by"}},
        ]
        plan = M.plan_github(gh, graph())
        self.assertEqual(6, plan["would_write_titles"])
        self.assertEqual("STALE_OR_HAND_EDITED", plan["drift"]["Common#592"]["status"])
        self.assertEqual("MISSING_PROJECTION", plan["drift"]["Common#527"]["status"])
        self.assertEqual(["Common#592#issuecomment-6"], [r["source"] for r in plan["rejected_facts"]])
        self.assertTrue(plan["expected_titles"]["Common#527"].endswith("— Programme"))
        self.assertEqual([], [c for c in gh.calls if c[0] in {"POST", "PATCH_COMMENT", "PATCH_TITLE"}])

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_head_moved_between_passes_flips_evidence_without_agent_action(self):
        gh = FakeGitHub()
        for number in (527, 588, 610, 592, 594, 612):
            gh.issues[number] = f"T{number}"
        for number in (593, 595, 613):
            gh.pulls[number] = {"head": {"sha": SHA_A}, "state": "open", "merged": False}
        gh.comments[592] = [{"id": 5, "body": ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A), "author_association": "OWNER", "user": {"login": "reallaksh19"}}]
        g = graph()
        run = lambda: M.sync_projection(  # noqa: E731
            M.GitHubStore(gh), g, lambda: M.ledger_from_github(gh, g), lambda: M.observe_github(gh, g),
            {f"Common#{n}": t for n, t in gh.issues.items()},
        )
        run()
        self.assertIn("· ACTIVE", gh.issues[592])
        gh.pulls[593]["head"]["sha"] = SHA_C  # a push happens; no agent edits anything
        run()
        self.assertIn("EVIDENCE_STALE", gh.issues[592])
        self.assertTrue(gh.issues[592].startswith("🟡"))


class DocumentedBehaviour(unittest.TestCase):
    """The worked lifecycle in operating-model/durable-execution-lineage-projection-*.md, replayed exactly."""

    def titles(self, ledger, obs):
        nodes = M.project(graph(), ledger, obs)["nodes"]
        return nodes["Common#592"]["title_prefix"], nodes["Common#588"]["title_prefix"], nodes["Common#527"]["title_prefix"]

    def test_documented_lifecycle_walkthrough(self):
        obs_a, obs_b = {"Common#592": {"candidate_sha": SHA_A}}, {"Common#592": {"candidate_sha": SHA_B}}
        P = "[#527 › #588 › #592 → PR#593]"
        Q = "[#527 › #588 → #592/PR#593]"
        ledger = []
        self.assertEqual(
            (f"⚪ {P} R:P0/E0 · U01 · NOT_STARTED", "⚪ [#527 › #588] Φ:D0/E0 · F0 · IDLE", "⚪ [#527] Π:D0/E0 · F0 · IDLE"),
            self.titles(ledger, {}),
        )
        ledger.append(entry(facts(units=[unit("U01"), unit("U02")], next={"unit": "U03", "action": "build replay lane"}), 1))
        self.assertEqual(
            (f"🟢 {P} R:P50/E50 · U03 · ACTIVE", f"🟢 {Q} Φ:D38/E38 · F1 · ACTIVE", "🟢 [#527] Π:D28/E28 · F1 · ACTIVE"),
            self.titles(ledger, obs_a),
        )
        ledger.append(entry(facts(units=[unit("U03", refs=())]), 2))
        self.assertEqual(
            (f"🟡 {P} R:P75/E50 · U04 · EVIDENCE_GAP", f"🟡 {Q} Φ:D56/E38 · F1 · EVIDENCE_GAP", "🟡 [#527] Π:D42/E28 · F1 · EVIDENCE_GAP"),
            self.titles(ledger, obs_a),
        )
        ledger.append(entry(facts(units=[unit("U03", refs=("Common#592#issuecomment-9",))]), 3))
        self.assertEqual(
            (f"🟢 {P} R:P75/E75 · U04 · ACTIVE", f"🟢 {Q} Φ:D56/E56 · F1 · ACTIVE", "🟢 [#527] Π:D42/E42 · F1 · ACTIVE"),
            self.titles(ledger, obs_a),
        )
        self.assertEqual(
            (f"🟡 {P} R:P75/E0 · U04 · EVIDENCE_STALE", f"🟡 {Q} Φ:D56/E0 · F1 · EVIDENCE_GAP", "🟡 [#527] Π:D42/E0 · F1 · EVIDENCE_GAP"),
            self.titles(ledger, obs_b),
        )
        ledger.append(entry(facts(sha=SHA_B, units=[unit("U01"), unit("U02"), unit("U03")]), 4))
        replayed = self.titles(ledger, obs_b)
        self.assertEqual(
            (f"🟢 {P} R:P75/E75 · U04 · ACTIVE", f"🟢 {Q} Φ:D56/E56 · F1 · ACTIVE", "🟢 [#527] Π:D42/E42 · F1 · ACTIVE"), replayed
        )
        ledger.append(entry(facts(sha=SHA_B, units=[unit("U04")], result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 5))
        self.assertEqual(
            (f"✅ {P} R:P100/E100 · COMPLETE", "⚪ [#527 › #588] Φ:D75/E75 · F0 · IDLE", "⚪ [#527] Π:D56/E56 · F0 · IDLE"),
            self.titles(ledger, obs_b),
        )
        # a rerun with nothing new is a no-op: identical digest
        again = M.project(graph(), ledger, obs_b)["input_digest"]
        self.assertEqual(again, M.project(graph(), list(ledger), dict(obs_b))["input_digest"])

    def test_shipped_examples_validate_and_project(self):
        examples = MODULE_PATH.parents[1] / "examples" / "delp"
        loaded = M._load_structured(examples / "execution-graph.yaml") if HAVE_YAML else None
        if loaded is None:
            self.skipTest("PyYAML unavailable")
        M.validate_graph(loaded)
        ledger = M._load_ledger([examples / "checkpoint-facts.md"])
        self.assertEqual([], M.validate_facts(ledger[0]["facts"]))
        out = M.project(loaded, ledger, M._load_structured(examples / "observations.json"))
        self.assertEqual([], out["rejected_facts"])
        self.assertEqual("🟢 [#527 › #588 › #592 → PR#593] R:P50/E50 · U03 · ACTIVE", out["nodes"]["Common#592"]["title_prefix"])
        self.assertEqual("🟢 [#527] Π:D28/E28 · F1 · ACTIVE", out["nodes"]["Common#527"]["title_prefix"])


@unittest.skipUnless(HAVE_YAML and HAVE_JSONSCHEMA, "PyYAML/jsonschema unavailable")
class SchemasAgreeWithTheEngine(unittest.TestCase):
    """The YAML schemas are the published contract; the engine validators must say the same thing."""

    @classmethod
    def schema(cls, name):
        import yaml as _yaml

        return _yaml.safe_load((SCHEMAS / f"delp-{name}-{TAG}.schema.yaml").read_text(encoding="utf-8"))

    def schema_errors(self, name, value):
        validator = jsonschema.Draft202012Validator(self.schema(name))
        return [e.message for e in validator.iter_errors(value)]

    def test_schema_ids_match_the_engine_constants(self):
        self.assertEqual(M.FACTS_SCHEMA, self.schema("checkpoint-facts")["$id"])
        self.assertEqual(M.GRAPH_SCHEMA, self.schema("execution-graph")["$id"])
        self.assertEqual(M.STATUS_SCHEMA, self.schema("live-status")["$id"])

    def test_good_facts_pass_both(self):
        record = facts(units=[unit("U01", candidate_sha=SHA_B, contract_digest=DIGEST)], activity="WAITING_CI",
                       next={"unit": "U02", "action": "run replay"}, blocker="NONE", owner_action="NONE",
                       gates=[{"id": "REVIEWER_ACCEPTANCE", "result": "PASSED", "evidence_refs": ["r"]}],
                       result={"scope": "STEP", "responsibility_complete": "NO"})
        self.assertEqual([], self.schema_errors("checkpoint-facts", record))
        self.assertEqual([], M.validate_facts(record))

    def test_every_forbidden_or_malformed_facts_variant_fails_both(self):
        bad = [
            facts(units=[unit("U01")], progress=72),
            facts(units=[unit("U01")], title="x"),
            facts(units=[unit("U01")], parent_progress=1),
            facts(units=[unit("U01")], activity_epoch=3),
            facts(units=[unit("U01", weight=20)]),
            facts(units=[unit("U01", evidenced=True)]),
            facts(units=[unit("U01")], activity="QUIET"),
            facts(units=[unit("U01")], activity="STALE"),
            facts(sha="abc123", units=[unit("U01")]),
            facts(units=[unit("U01", state="DONE")]),
            facts(units=[unit("U01", result="GREEN")]),
            facts(units=[unit("U01", refs=[""])]),
            facts(units=[unit("U01")], next={"unit": "U02", "extra": 1}),
            facts(units=[unit("U01")], result={"scope": "NOPE"}),
            {"schema": M.FACTS_SCHEMA, "material": {"candidate_sha": SHA_A}},
        ]
        for record in bad:
            with self.subTest(record=record):
                self.assertTrue(self.schema_errors("checkpoint-facts", record), "schema accepted it")
                self.assertTrue(M.validate_facts(record), "engine accepted it")

    def test_graph_sample_passes_both(self):
        self.assertEqual([], self.schema_errors("execution-graph", graph()))
        M.validate_graph(graph())

    def test_stable_identity_graph_passes_both(self):
        g = stable_graph()
        self.assertEqual([], self.schema_errors("execution-graph", g))
        M.validate_graph(g)

    def test_stable_identity_graph_without_leaf_id_fails_both(self):
        g = stable_graph()
        g["nodes"][4].pop("responsibility_id")
        self.assertTrue(self.schema_errors("execution-graph", g))
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)

    def test_graph_without_units_or_parent_fails_both(self):
        g = copy.deepcopy(graph())
        g["nodes"][3].pop("units")
        self.assertTrue(self.schema_errors("execution-graph", g))
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)
        g = copy.deepcopy(graph())
        g["nodes"][3].pop("parent")
        self.assertTrue(self.schema_errors("execution-graph", g))
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)

    def test_real_projection_output_satisfies_the_live_status_schema(self):
        ledger = [
            entry(facts(units=[unit("U01"), unit("U02", refs=())], next={"unit": "U03", "action": "replay"}), 1),
            entry(facts(leaf="Common#612", pr="Common#613", units=[unit("W1")]), 2),
        ]
        projection = M.project(graph(), ledger, OBS_A)
        for ref, node in projection["nodes"].items():
            document = M.status_document(node, version=1, digest=projection["input_digest"], programme=projection["programme"])
            with self.subTest(ref=ref):
                self.assertEqual([], self.schema_errors("live-status", json.loads(M.canonical_json(document))))


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = M.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_project_admit_validate_and_verify_titles(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "graph.json").write_text(json.dumps(graph()), encoding="utf-8")
            good = [entry(facts(units=[unit("U01"), unit("U02"), unit("U03")], next={"unit": "U04", "action": "negative replay"}), 1)]
            (root / "facts.json").write_text(json.dumps(good), encoding="utf-8")
            (root / "obs.json").write_text(json.dumps(OBS_A), encoding="utf-8")
            code, out, _ = self.run_cli("project", "--graph", str(root / "graph.json"), "--facts", str(root / "facts.json"), "--observations", str(root / "obs.json"))
            self.assertEqual(0, code)
            self.assertEqual(75, json.loads(out)["nodes"]["Common#592"]["progress"]["P"])
            code, out, _ = self.run_cli("admit", "--graph", str(root / "graph.json"), "--facts", str(root / "facts.json"), "--observations", str(root / "obs.json"), "--leaf", "Common#592")
            self.assertEqual(0, code)
            self.assertIn("NEXT: U04 — negative replay", out)
            code, _, err = self.run_cli("validate-facts", str(root / "facts.json"))
            self.assertEqual(0, code)
            bad = [entry(facts(units=[unit("U01")], progress=5), 1)]
            (root / "bad.json").write_text(json.dumps(bad), encoding="utf-8")
            code, _, err = self.run_cli("validate-facts", str(root / "bad.json"))
            self.assertEqual(1, code)
            self.assertIn("agents publish facts only", err)
            projection = M.project(graph(), good, OBS_A)
            (root / "titles.json").write_text(
                json.dumps({"Common#592": "hand-written R:P99/E99", "Common#527": M.render_title(projection["nodes"]["Common#527"]["title_prefix"], "Programme")}),
                encoding="utf-8",
            )
            code, out, _ = self.run_cli("verify-titles", "--graph", str(root / "graph.json"), "--facts", str(root / "facts.json"), "--observations", str(root / "obs.json"), "--actual-titles", str(root / "titles.json"))
            self.assertEqual(2, code)
            drift = json.loads(out)["drift"]
            self.assertEqual("STALE_OR_HAND_EDITED", drift["Common#592"]["status"])
            self.assertNotIn("Common#527", drift)

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_validate_facts_fails_when_a_comment_has_no_facts_block(self):
        with tempfile.TemporaryDirectory() as td:
            comment = pathlib.Path(td) / "comment.md"
            comment.write_text("TASK_EVIDENCE — CHECKPOINT\n\nProse only, the facts block is missing.\n", encoding="utf-8")
            code, _, err = self.run_cli("validate-facts", str(comment))
            self.assertEqual(1, code)
            self.assertIn("no CHECKPOINT_FACTS_V1 block found", err)
            good = pathlib.Path(td) / "good.md"
            good.write_text(ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A), encoding="utf-8")
            self.assertEqual(0, self.run_cli("validate-facts", str(good))[0])

    def test_invalid_graph_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "g.json"
            path.write_text(json.dumps({"programme": {"root": "Common#1"}, "nodes": []}), encoding="utf-8")
            code, _, err = self.run_cli("validate-graph", "--graph", str(path))
            self.assertEqual(1, code)
            self.assertIn("DELP error", err)


# --------------------------------------------------------------------------
# decomposition gate: is the plan small, verifiable and collision-free enough to hand to an agent?
# --------------------------------------------------------------------------


def leaf_of(g, ref):
    return next(n for n in g["nodes"] if n["ref"] == ref)


def planned(mode="ENFORCED", **policy):
    """The shared plan, fully decomposed: every leaf is small, verifiable and has its own write surface."""
    g = copy.deepcopy(graph())
    g["programme"]["decomposition_policy"] = {"mode": mode, **policy}
    for node in g["nodes"]:
        if node["kind"] != "LEAF":
            continue
        number = node["ref"].split("#")[1]
        node["outcome"] = f"slice {number} is observably done"
        node["size_budget"] = {"target_loc": 600, "hard_loc": 1200, "target_minutes": 15, "hard_minutes": 20}
        node["write_surface"] = [f"src/{number}/"]
    leaf_of(g, "Common#594")["units"] = [{"id": "V1", "weight": 40}, {"id": "V2", "weight": 30}, {"id": "V3", "weight": 30}]
    leaf_of(g, "Common#612")["units"] = [{"id": "W1", "weight": 40}, {"id": "W2", "weight": 30}, {"id": "W3", "weight": 30}]
    for node in g["nodes"]:
        for u in node.get("units", []):
            u["verify"] = f"{u['id']} check passes"
    return g


def with_weights(g, ref, weights):
    leaf_of(g, ref)["units"] = [{"id": f"U{i}", "weight": w, "verify": "check passes"} for i, w in enumerate(weights, 1)]
    return g


def broken(mode="ENFORCED", ref="Common#594"):
    """A plan that fails the gate on exactly one rule (the leaf states no outcome)."""
    g = planned(mode)
    leaf_of(g, ref).pop("outcome")
    return g


def cli(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = M.main(list(args))
    return code, out.getvalue(), err.getvalue()


class DecompositionPolicyValidation(unittest.TestCase):
    def bad(self, mutate, label=""):
        g = planned()
        mutate(g)
        with self.subTest(label), self.assertRaises(M.GraphError):
            M.validate_graph(g)

    def test_a_graph_without_a_policy_is_mode_off_and_nothing_changes(self):
        self.assertEqual("OFF", M.validate_graph(graph())["policy"]["mode"])
        for node in M.project(graph(), [], {})["nodes"].values():
            self.assertNotIn("plan", node)

    def test_policy_overrides_merge_over_the_defaults(self):
        policy = M.validate_graph(planned(units={"max": 6}))["policy"]
        self.assertEqual({"min": 3, "max": 6, "max_share_percent": 40}, policy["units"])
        self.assertEqual({"target_loc": 700, "hard_loc": 1500, "target_minutes": 15, "hard_minutes": 20}, policy["leaf_budget"])

    def test_malformed_policy_is_rejected(self):
        for label, policy in {
            "mode": {"mode": "STRICT"},
            "min above max": {"units": {"min": 5, "max": 4}},
            "share above 100": {"units": {"max_share_percent": 101}},
            "zero floor": {"units": {"min": 0}},
            "target above hard": {"leaf_budget": {"target_loc": 900, "hard_loc": 800}},
            "target minutes above hard": {"leaf_budget": {"target_minutes": 30}},
            "unknown budget key": {"leaf_budget": {"extra": 5}},
            "non-boolean require": {"require": {"verify": "yes"}},
            "negative nano floor": {"min_leaf_target_loc": -1},
            "unknown key": {"surprise": 1},
        }.items():
            self.bad(lambda g, p=policy: g["programme"].__setitem__("decomposition_policy", p), label)
        self.bad(lambda g: g["programme"].__setitem__("decomposition_policy", "ENFORCED"), "not a mapping")
        self.bad(lambda g: g["programme"].__setitem__("total_weight", 0), "total weight")

    def test_leaf_decomposition_fields_are_validated(self):
        leaf = lambda g: leaf_of(g, "Common#592")  # noqa: E731
        for label, mutate in {
            "work_class": lambda g: leaf(g).__setitem__("work_class", "EPIC"),
            "outcome type": lambda g: leaf(g).__setitem__("outcome", 5),
            "size_budget key": lambda g: leaf(g).__setitem__("size_budget", {"loc": 5}),
            "size_budget zero": lambda g: leaf(g).__setitem__("size_budget", {"target_loc": 0}),
            "surface glob": lambda g: leaf(g).__setitem__("write_surface", ["src/*.py"]),
            "surface absolute": lambda g: leaf(g).__setitem__("write_surface", ["/etc/passwd"]),
            "surface traversal": lambda g: leaf(g).__setitem__("write_surface", ["../x"]),
            "surface empty segment": lambda g: leaf(g).__setitem__("write_surface", ["src//x"]),
            "surface root": lambda g: leaf(g).__setitem__("write_surface", ["."]),
            "surface backslash": lambda g: leaf(g).__setitem__("write_surface", ["src\\x"]),
            "unknown dependency": lambda g: leaf(g).__setitem__("depends_on", ["Common#9999"]),
            "self dependency": lambda g: leaf(g).__setitem__("depends_on", ["Common#592"]),
            "dependency on a parent": lambda g: leaf(g).__setitem__("depends_on", ["Common#588"]),
            "unknown parallel": lambda g: leaf(g).__setitem__("parallel_ok", ["Common#9999"]),
            "basis type": lambda g: leaf(g).__setitem__("parallel_ok_basis", 3),
            "unit verify type": lambda g: leaf(g)["units"][0].__setitem__("verify", 5),
            "unit moved_from": lambda g: leaf(g)["units"][0].__setitem__("moved_from", "not a ref"),
            "unit not a mapping": lambda g: leaf(g).__setitem__("units", ["U01"]),
        }.items():
            self.bad(mutate, label)

    def test_dependency_cycles_are_rejected(self):
        def cycle(g):
            leaf_of(g, "Common#592")["depends_on"] = ["Common#594"]
            leaf_of(g, "Common#594")["depends_on"] = ["Common#612"]
            leaf_of(g, "Common#612")["depends_on"] = ["Common#592"]

        self.bad(cycle, "cycle")

    def test_write_surfaces_are_normalised(self):
        g = planned()
        leaf_of(g, "Common#592")["write_surface"] = ["./src/b/", "src/a.py", "src/b/", "src/a.py"]
        self.assertEqual(["src/a.py", "src/b/"], M.validate_graph(g)["nodes"]["Common#592"]["write_surface"])

    def test_plan_updates_are_validated(self):
        update = {"id": "PU-1", "kind": "SCOPE_EXPANSION", "nodes": ["Common#588"], "reason": "r", "owner_authorized": True, "owner_basis": "b"}
        g = planned()
        g["plan_updates"] = [update]
        self.assertEqual(["PU-1"], [u["id"] for u in M.validate_graph(g)["plan_updates"]])
        for label, change in {
            "no id": {"id": ""},
            "kind": {"kind": "WIDEN"},
            "reason": {"reason": ""},
            "authorised type": {"owner_authorized": "yes"},
            "no scope": {"nodes": []},
            "unit key": {"units": ["Common#592"]},
            "node ref": {"nodes": ["x"]},
        }.items():
            self.bad(lambda g, c=change: g.__setitem__("plan_updates", [{**update, **c}]), label)
        self.bad(lambda g: g.__setitem__("plan_updates", [update, dict(update)]), "duplicate id")
        policy_only = {"id": "PU-2", "kind": "POLICY_CHANGE", "reason": "r"}
        g["plan_updates"] = [policy_only]
        M.validate_graph(g)  # a policy change names no units or nodes


class DecompositionRules(unittest.TestCase):
    def codes(self, g, ref="Common#592", kind="blockers"):
        return [f["code"] for f in M.decomposition_report(g)["leaves"][ref][kind]]

    def test_a_fully_decomposed_plan_is_releasable_with_no_findings(self):
        report = M.decomposition_report(planned())
        self.assertTrue(all(row["releasable"] for row in report["leaves"].values()))
        self.assertEqual(
            {"evaluated": 3, "skipped_closed": 0, "releasable": 3, "not_releasable": 0, "advisories": 0, "by_class": {"PRODUCT": 3}},
            report["summary"],
        )

    def test_unit_count_bounds(self):
        self.assertIn("UNITS_BELOW_MIN", self.codes(with_weights(planned(), "Common#592", [50, 50])))
        self.assertEqual(["UNITS_ABOVE_MAX"], self.codes(with_weights(planned(), "Common#592", [10] * 9)))
        self.assertEqual([], self.codes(with_weights(planned(), "Common#592", [10] * 8)))
        self.assertEqual([], self.codes(with_weights(planned(), "Common#592", [34, 33, 33])))

    def test_unit_share_cap_is_exact_at_the_boundary(self):
        self.assertEqual([], self.codes(with_weights(planned(), "Common#592", [40, 30, 30])))
        row = M.decomposition_report(with_weights(planned(), "Common#592", [41, 30, 29]))["leaves"]["Common#592"]
        self.assertEqual(["UNIT_SHARE_OVER"], [f["code"] for f in row["blockers"]])
        self.assertIn("U1 carries 41% of the leaf (max 40%)", row["blockers"][0]["detail"])
        self.assertEqual([], self.codes(with_weights(planned(units={"max_share_percent": 50}), "Common#592", [41, 30, 29])))

    def test_mechanical_and_gate_leaves_are_exempt_from_the_floor_and_the_cap_only(self):
        g = with_weights(planned(), "Common#592", [100])
        self.assertEqual({"UNITS_BELOW_MIN", "UNIT_SHARE_OVER"}, set(self.codes(g)))
        for klass in ("MECHANICAL", "GATE"):
            leaf_of(g, "Common#592")["work_class"] = klass
            self.assertEqual([], self.codes(g), klass)
        leaf_of(g, "Common#592").pop("write_surface")
        self.assertEqual(["WRITE_SURFACE_MISSING"], self.codes(g))  # every other rule still applies
        g = with_weights(planned(), "Common#592", [10] * 9)
        leaf_of(g, "Common#592")["work_class"] = "MECHANICAL"
        self.assertEqual(["UNITS_ABOVE_MAX"], self.codes(g))
        self.assertEqual({"MECHANICAL": 1, "PRODUCT": 2}, M.decomposition_report(g)["summary"]["by_class"])

    def test_each_required_field_is_enforced_and_can_be_switched_off(self):
        for code, key, mutate in (
            ("OUTCOME_MISSING", "outcome", lambda leaf: leaf.pop("outcome")),
            ("WRITE_SURFACE_MISSING", "write_surface", lambda leaf: leaf.pop("write_surface")),
            ("SIZE_BUDGET_MISSING", "size_budget", lambda leaf: leaf.pop("size_budget")),
            ("UNIT_VERIFY_MISSING", "verify", lambda leaf: leaf["units"][0].pop("verify")),
        ):
            with self.subTest(code):
                g = planned()
                mutate(leaf_of(g, "Common#592"))
                self.assertEqual([code], self.codes(g))
                relaxed = planned(require={key: False})
                mutate(leaf_of(relaxed, "Common#592"))
                self.assertEqual([], self.codes(relaxed))

    def test_a_partial_size_budget_names_what_is_missing(self):
        g = planned()
        leaf_of(g, "Common#592")["size_budget"] = {"target_loc": 600}
        row = M.decomposition_report(g)["leaves"]["Common#592"]
        self.assertEqual(["SIZE_BUDGET_MISSING"], [f["code"] for f in row["blockers"]])
        self.assertIn("hard_loc, target_minutes, hard_minutes", row["blockers"][0]["detail"])

    def test_size_budget_is_judged_against_the_policy(self):
        def sized(**override):
            g = planned()
            leaf_of(g, "Common#592")["size_budget"] = {"target_loc": 600, "hard_loc": 1200, "target_minutes": 15, "hard_minutes": 20, **override}
            return M.decomposition_report(g)["leaves"]["Common#592"]

        row = sized(target_loc=1800, hard_loc=2200)
        self.assertEqual(["SIZE_OVER_HARD"], [f["code"] for f in row["blockers"]])
        self.assertEqual("hard_loc 2200 > 1500: split into at least 3 leaves", row["blockers"][0]["detail"])
        self.assertEqual("hard_loc 2200 > 1500: lower the cap or split the leaf", sized(hard_loc=2200)["blockers"][0]["detail"])
        self.assertEqual("hard_minutes 40 > 20: split into at least 2 leaves", sized(target_minutes=30, hard_minutes=40)["blockers"][0]["detail"])
        row = sized(target_loc=900, hard_loc=1400)
        self.assertTrue(row["releasable"])
        self.assertEqual(["SIZE_OVER_TARGET"], [f["code"] for f in row["advisories"]])
        row = sized(target_loc=900, hard_loc=800)
        self.assertEqual(["SIZE_BUDGET_INCONSISTENT"], [f["code"] for f in row["blockers"]])
        row = sized(target_loc=20, hard_loc=100)
        self.assertTrue(row["releasable"])
        self.assertEqual(["LEAF_TOO_SMALL"], [f["code"] for f in row["advisories"]])

    def test_a_tiny_mechanical_leaf_is_not_called_too_small(self):
        g = planned()
        leaf_of(g, "Common#592")["size_budget"] = {"target_loc": 20, "hard_loc": 100, "target_minutes": 5, "hard_minutes": 10}
        leaf_of(g, "Common#592")["work_class"] = "MECHANICAL"
        self.assertEqual([], self.codes(g, kind="advisories"))

    def test_overlapping_write_surfaces_collide_unless_ordered_or_declared_parallel(self):
        g = planned()
        leaf_of(g, "Common#594")["write_surface"] = ["src/592/sub/file.py"]
        report = M.decomposition_report(g)["leaves"]
        for ref, other in (("Common#592", "#594"), ("Common#594", "#592")):
            self.assertEqual(["WRITE_SURFACE_COLLISION"], [f["code"] for f in report[ref]["blockers"]], ref)
            self.assertIn(other, report[ref]["blockers"][0]["detail"])
            self.assertIn("src/592/sub/file.py", report[ref]["blockers"][0]["detail"])  # the more specific side is reported
        for owner, dependency in (("Common#594", "Common#592"), ("Common#592", "Common#594")):
            ordered = copy.deepcopy(g)
            leaf_of(ordered, owner)["depends_on"] = [dependency]
            self.assertEqual([], self.codes(ordered), f"{owner} after {dependency}")
        chained = copy.deepcopy(g)
        leaf_of(chained, "Common#612")["depends_on"] = ["Common#592"]
        leaf_of(chained, "Common#594")["depends_on"] = ["Common#612"]
        self.assertEqual([], self.codes(chained))  # ordered transitively
        self.assertEqual([], self.codes(chained, "Common#594"))

    def test_declared_parallelism_needs_a_basis_from_the_side_that_declares_it(self):
        g = planned()
        leaf_of(g, "Common#594")["write_surface"] = ["src/592/sub/file.py"]
        leaf_of(g, "Common#594")["parallel_ok"] = ["Common#592"]
        self.assertEqual(["PARALLEL_BASIS_MISSING"], self.codes(g, "Common#594"))
        self.assertEqual([], self.codes(g, "Common#592"))  # the collision is acknowledged from either side
        leaf_of(g, "Common#594")["parallel_ok_basis"] = "disjoint hunks of one file"
        self.assertEqual([], self.codes(g, "Common#594"))

    def test_sibling_directories_that_share_a_name_prefix_do_not_collide(self):
        g = planned()
        leaf_of(g, "Common#592")["write_surface"] = ["src/59/", "src/592"]  # a directory and a file named alike
        leaf_of(g, "Common#594")["write_surface"] = ["src/594/", "src/592/"]
        self.assertEqual([], self.codes(g))
        self.assertEqual([], self.codes(g, "Common#594"))

    def test_closed_leaves_are_not_judged_and_do_not_collide(self):
        g = planned()
        leaf_of(g, "Common#594")["write_surface"] = ["src/592/"]
        self.assertEqual(["WRITE_SURFACE_COLLISION"], self.codes(g, "Common#594"))
        report = M.decomposition_report(g, closed=["Common#592"])
        self.assertNotIn("Common#592", report["leaves"])
        self.assertEqual([], report["leaves"]["Common#594"]["blockers"])
        self.assertEqual(1, report["summary"]["skipped_closed"])

    def test_the_mode_can_be_overridden_per_run_and_is_validated(self):
        self.assertEqual("OFF", M.decomposition_report(planned("ENFORCED"), mode="OFF")["mode"])
        self.assertEqual("ENFORCED", M.decomposition_report(graph(), mode="ENFORCED")["mode"])
        with self.assertRaises(M.GraphError):
            M.decomposition_report(planned(), mode="STRICT")

    def test_the_report_is_pure_deterministic_and_serialisable(self):
        g = broken()
        before = copy.deepcopy(g)
        first = M.decomposition_report(g)
        self.assertEqual(first, M.decomposition_report(g))
        self.assertEqual(before, g)
        self.assertEqual(first, json.loads(M.canonical_json(first)))


class DecompositionInProjection(unittest.TestCase):
    LEDGER = [entry(facts(units=[unit("U01"), unit("U02")], next={"unit": "U03", "action": "build replay lane"}), 1)]

    def nodes(self, g, ledger=None, obs=OBS_A):
        return M.project(g, self.LEDGER if ledger is None else ledger, obs)["nodes"]

    def test_off_ignores_a_plan_that_fails_the_gate(self):
        failing, clean = self.nodes(broken("OFF")), self.nodes(planned("OFF"))
        self.assertEqual(clean, failing)
        self.assertTrue(all("plan" not in n for n in failing.values()))

    def test_advisory_reports_but_never_changes_a_state_or_a_title(self):
        advisory, clean = self.nodes(broken("ADVISORY")), self.nodes(planned("OFF"))
        self.assertEqual({r: (n["title_prefix"], n["state"]) for r, n in clean.items()}, {r: (n["title_prefix"], n["state"]) for r, n in advisory.items()})
        node = advisory["Common#594"]
        self.assertEqual("ADVISORY", node["plan"]["mode"])
        self.assertFalse(node["plan"]["releasable"])
        self.assertEqual(["OUTCOME_MISSING"], [b["code"] for b in node["plan"]["blockers"]])
        self.assertIn("DECOMPOSITION_BLOCKERS:OUTCOME_MISSING", node["warnings"])
        self.assertEqual({"mode": "ADVISORY", "not_releasable": 1, "leaves": ["Common#594"]}, advisory["Common#588"]["plan"])

    def test_enforced_marks_the_unreleasable_leaf_without_moving_any_number(self):
        enforced, clean = self.nodes(broken()), self.nodes(planned("OFF"))
        node = enforced["Common#594"]
        self.assertEqual("NOT_RELEASEABLE", node["state"])
        self.assertEqual("🟡", node["light"])
        self.assertEqual("🟡 [#527 › #588 › #594 → PR#595] R:P0/E0 · V1 · NOT_RELEASEABLE", node["title_prefix"])
        for ref in clean:
            self.assertEqual(clean[ref]["progress"], enforced[ref]["progress"], ref)
        self.assertEqual("🟢 [#527 › #588 › #592 → PR#593] R:P50/E50 · U03 · ACTIVE", enforced["Common#592"]["title_prefix"])

    def test_ancestors_stay_active_while_something_moves_and_report_the_gap_in_warnings(self):
        enforced = self.nodes(broken())
        self.assertEqual("ACTIVE", enforced["Common#588"]["state"])
        self.assertEqual("ACTIVE", enforced["Common#527"]["state"])
        self.assertIn("DECOMPOSITION_BLOCKED_LEAVES:1", enforced["Common#588"]["warnings"])
        self.assertEqual({"mode": "ENFORCED", "not_releasable": 1, "leaves": ["Common#594"]}, enforced["Common#527"]["plan"])

    def test_plan_gap_appears_only_when_nothing_is_moving(self):
        idle = self.nodes(broken(), ledger=[])
        self.assertEqual("🟡 [#527 › #588] Φ:D0/E0 · F0 · PLAN_GAP", idle["Common#588"]["title_prefix"])
        self.assertEqual("🟡 [#527] Π:D0/E0 · F0 · PLAN_GAP", idle["Common#527"]["title_prefix"])
        self.assertEqual("IDLE", idle["Common#588"]["lifecycle"])
        self.assertEqual("⚪ [#527 › #610] Φ:D0/E0 · F0 · IDLE", idle["Common#610"]["title_prefix"])  # nothing blocked below it

    def test_an_active_leaf_that_fails_the_gate_still_counts_on_the_frontier(self):
        g = broken(ref="Common#592")
        out = self.nodes(g)
        self.assertEqual("NOT_RELEASEABLE", out["Common#592"]["state"])
        self.assertEqual("ACTIVE", out["Common#592"]["lifecycle"])
        self.assertEqual(1, out["Common#527"]["frontier"]["count"])
        self.assertEqual("🟢 [#527] Π:D28/E28 · F1 · ACTIVE", out["Common#527"]["title_prefix"])

    def test_only_not_started_and_active_leaves_are_overlaid(self):
        g = broken(ref="Common#592")

        def state(ledger, obs=OBS_A):
            return self.nodes(g, ledger, obs)["Common#592"]["state"]

        self.assertEqual("WAITING_CI", state([entry(facts(units=[unit("U01")], activity="WAITING_CI"), 1)]))
        self.assertEqual("PAUSED", state([entry(facts(units=[unit("U01")], activity="PAUSED"), 1)]))
        self.assertEqual("STALE", state(self.LEDGER, {**OBS_A, "Common#592": {"candidate_sha": SHA_A, "liveness": "STALE"}}))
        self.assertEqual("EVIDENCE_STALE", state(self.LEDGER, {**OBS_A, "Common#592": {"candidate_sha": SHA_B}}))
        self.assertEqual("NOT_RELEASEABLE", state([]))

    def test_completed_and_superseded_leaves_are_history_and_skip_the_gate(self):
        done = [
            entry(
                facts(leaf="Common#612", pr="Common#613", units=[unit("W1"), unit("W2"), unit("W3")], result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}),
                1,
            )
        ]
        out = self.nodes(broken(ref="Common#612"), done)["Common#612"]
        self.assertEqual("COMPLETE", out["state"])
        self.assertNotIn("plan", out)
        replaced = [
            entry(
                facts(leaf="Common#612", pr="Common#613", units=[unit("W1")], result={"scope": "STEP", "responsibility_complete": "NO", "superseded_by": "Common#700"}),
                1,
            )
        ]
        out = self.nodes(broken(ref="Common#612"), replaced)["Common#612"]
        self.assertEqual("SUPERSEDED", out["state"])
        self.assertNotIn("plan", out)

    def test_generated_titles_with_the_new_states_round_trip_through_the_title_grammar(self):
        for ref, node in self.nodes(broken(), ledger=[]).items():
            expected = M.render_title(node["title_prefix"], "Human title")
            self.assertEqual("OK", M.title_drift(expected, node["title_prefix"])["status"], ref)
            self.assertEqual("Human title", M.split_title(expected)[1])

    def test_a_projection_with_the_gate_on_is_idempotent_and_agent_facts_cannot_move_it(self):
        g = broken()
        self.assertEqual(M.project(g, self.LEDGER, OBS_A)["input_digest"], M.project(copy.deepcopy(g), list(self.LEDGER), dict(OBS_A))["input_digest"])
        forged = [entry(facts(leaf="Common#594", pr="Common#595", units=[unit("V1")], plan={"releasable": True}), 2)]
        self.assertEqual(1, len(M.project(g, forged, OBS_A)["rejected_facts"]))
        self.assertEqual("NOT_RELEASEABLE", M.project(g, forged, OBS_A)["nodes"]["Common#594"]["state"])


class DecompositionAdmission(unittest.TestCase):
    LEDGER = [entry(facts(units=[unit("U01"), unit("U02")], next={"unit": "U03", "action": "build replay lane"}), 1)]

    def admit(self, g, obs=OBS_A, ref="Common#592"):
        return M.admit(M.project(g, self.LEDGER, obs), ref, "continue")

    def test_an_unreleasable_leaf_is_told_to_fix_the_plan_before_coding(self):
        report = self.admit(broken(ref="Common#592"))
        self.assertEqual("FIX_PLAN", report["action"])
        self.assertTrue(report["plan_fix_required"])
        self.assertFalse(report["recovery_required"])
        self.assertEqual([], report["authority_effects"])
        text = M.render_checkpoint(report)
        self.assertIn("CHILD: R:P50/E50 · U03 · NOT_RELEASEABLE", text)
        self.assertIn("PLAN: NOT_RELEASEABLE — OUTCOME_MISSING", text)
        self.assertIn(
            "NEXT: FIX_PLAN before coding — OUTCOME_MISSING (state the observable outcome of the leaf in one sentence)"
            " — request a plan update (split or reweight) from the Coordinator; do not start or continue units",
            text,
        )

    def test_plan_comes_before_evidence_but_the_evidence_gap_is_still_reported(self):
        report = self.admit(broken(ref="Common#592"), {**OBS_A, "Common#592": {"candidate_sha": SHA_B}})
        self.assertEqual("FIX_PLAN", report["action"])
        self.assertIn("evidence is also STALE_CANDIDATE", report["next"])
        self.assertFalse(report["recovery_required"])

    def test_many_blockers_are_summarised(self):
        g = planned()
        leaf = leaf_of(g, "Common#592")
        for key in ("outcome", "write_surface", "size_budget"):
            leaf.pop(key)
        leaf["units"] = [{"id": "U01", "weight": 50}, {"id": "U02", "weight": 50}]
        report = self.admit(g)
        self.assertGreater(len(report["plan"]["blockers"]), 3)
        self.assertRegex(report["next"], r"; \+\d+ more")

    def test_a_releasable_leaf_continues_and_says_so(self):
        report = self.admit(planned())
        self.assertEqual("CONTINUE_UNIT", report["action"])
        self.assertFalse(report["plan_fix_required"])
        self.assertIn("PLAN: RELEASABLE\n", M.render_checkpoint(report) + "\n")

    def test_advisories_are_shown_without_blocking(self):
        g = planned()
        leaf_of(g, "Common#592")["size_budget"] = {"target_loc": 900, "hard_loc": 1400, "target_minutes": 15, "hard_minutes": 20}
        report = self.admit(g)
        self.assertEqual("CONTINUE_UNIT", report["action"])
        self.assertIn("PLAN: RELEASABLE — ADVISORY: SIZE_OVER_TARGET", M.render_checkpoint(report))

    def test_advisory_mode_names_the_blocker_but_does_not_stop_work(self):
        report = self.admit(broken("ADVISORY", "Common#592"))
        self.assertEqual("CONTINUE_UNIT", report["action"])
        self.assertIn("PLAN: WOULD_BLOCK (advisory) — OUTCOME_MISSING", M.render_checkpoint(report))

    def test_off_adds_nothing_to_the_report(self):
        report = self.admit(broken("OFF", "Common#592"))
        self.assertNotIn("plan", report)
        self.assertNotIn("plan_fix_required", report)
        self.assertNotIn("PLAN:", M.render_checkpoint(report))

    def test_a_completed_leaf_is_never_told_to_fix_its_plan(self):
        done = [entry(facts(leaf="Common#612", pr="Common#613", units=[unit("W1"), unit("W2"), unit("W3")], result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1)]
        report = M.admit(M.project(broken(ref="Common#612"), done, OBS_A), "Common#612", "continue")
        self.assertEqual("NONE", report["action"])


class DecompositionGitHubSync(unittest.TestCase):
    def sync(self, gh, g):
        titles = {f"Common#{n}": t for n, t in gh.issues.items()}
        return M.sync_projection(M.GitHubStore(gh), g, lambda: M.ledger_from_github(gh, g), lambda: M.observe_github(gh, g), titles)

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")  # the second pass re-reads the managed comment's fenced block
    def test_fixing_the_plan_flips_the_titles_with_no_agent_action(self):
        gh = FakeGitHub()
        for number, title in {527: "Programme", 588: "Phase 3", 610: "Phase 4", 592: "Replay lane", 594: "Gate lane", 612: "Closeout"}.items():
            gh.issues[number] = title

        def not_started(g):  # no PR and no branch yet: the provider shows no work, so the leaves really are not started
            for node in g["nodes"]:
                node.pop("primary_pr", None)
            return g

        self.sync(gh, not_started(broken()))
        self.assertTrue(gh.issues[594].startswith("🟡 [#527 › #588 › #594] R:P0/E0 · V1 · NOT_RELEASEABLE — Gate lane"), gh.issues[594])
        self.assertEqual("🟡 [#527] Π:D0/E0 · F0 · PLAN_GAP — Programme", gh.issues[527])
        self.assertEqual("🟡 [#527 › #588] Φ:D0/E0 · F0 · PLAN_GAP — Phase 3", gh.issues[588])
        self.assertIn('"releasable": false', gh.comments[594][0]["body"])
        self.assertIn("OUTCOME_MISSING", gh.comments[594][0]["body"])
        # the Coordinator states the outcome (a plan edit); nothing else changes and nobody edits a title
        self.sync(gh, not_started(planned()))
        self.assertTrue(gh.issues[594].startswith("⚪ [#527 › #588 › #594] R:P0/E0 · V1 · NOT_STARTED — Gate lane"), gh.issues[594])
        self.assertEqual("⚪ [#527] Π:D0/E0 · F0 · IDLE — Programme", gh.issues[527])
        self.assertIn('"releasable": true', gh.comments[594][0]["body"])
        self.assertEqual(1, len(gh.comments[594]))  # still one managed comment per node


class PlanConservation(unittest.TestCase):
    UPDATE = {"id": "PU-1", "kind": "UNIT_REWEIGHT", "nodes": ["Common#592"], "reason": "descoped U02", "owner_authorized": True, "owner_basis": "Owner chat 2026-10-07"}

    @staticmethod
    def split(new_leaf_weight=3):
        """Move U03/U04 out of #592 into a new sibling #620, rescaling siblings so every share is conserved."""
        g = copy.deepcopy(graph())
        leaf_of(g, "Common#592")["units"] = [{"id": "U01", "weight": 20}, {"id": "U02", "weight": 30}]
        leaf_of(g, "Common#594")["weight"] = 2
        g["nodes"].append(
            {
                "ref": "Common#620",
                "kind": "LEAF",
                "parent": "Common#588",
                "weight": new_leaf_weight,
                "primary_pr": "Common#621",
                "units": [{"id": "U03", "weight": 25, "moved_from": "Common#592"}, {"id": "U04", "weight": 25, "moved_from": "Common#592"}],
            }
        )
        return g

    def codes(self, report, severity="BLOCKER"):
        return sorted(f["code"] for f in report["findings"] if f["severity"] == severity)

    def test_identical_plans_conserve(self):
        report = M.graph_diff(graph(), graph())
        self.assertTrue(report["conserved"])
        self.assertEqual([], report["findings"])
        self.assertEqual({"items_before": 7, "items_after": 7, "moved": 0, "added": 0, "dropped": 0, "new_plan_updates": 0}, report["summary"])

    def test_a_split_that_conserves_every_share_needs_no_plan_update(self):
        report = M.graph_diff(graph(), self.split())
        self.assertTrue(report["conserved"], report["findings"])
        self.assertEqual({"items_before": 7, "items_after": 7, "moved": 2, "added": 0, "dropped": 0, "new_plan_updates": 0}, report["summary"])
        self.assertEqual([], report["drift"])

    def test_a_split_that_misweights_the_new_leaf_is_caught_item_by_item(self):
        report = M.graph_diff(graph(), self.split(new_leaf_weight=1))
        self.assertFalse(report["conserved"])
        self.assertEqual(["POINTS_DRIFT"], sorted(set(self.codes(report))))
        self.assertIn("Common#620:U03", {row["item"] for row in report["drift"]})
        self.assertIn("Common#592:U01", {row["item"] for row in report["drift"]})  # the siblings' shares moved too

    def test_dropping_a_unit_needs_a_covering_authorised_update(self):
        g = copy.deepcopy(graph())
        leaf_of(g, "Common#592")["units"] = [u for u in leaf_of(g, "Common#592")["units"] if u["id"] != "U04"]
        report = M.graph_diff(graph(), g)
        self.assertFalse(report["conserved"])
        self.assertIn("UNIT_LOST", self.codes(report))
        self.assertIn("POINTS_DRIFT", self.codes(report))  # the survivors' shares rose
        update = {"id": "PU-1", "kind": "UNIT_DROPPED", "units": ["Common#592:U04"], "reason": "descoped", "owner_authorized": True, "owner_basis": "Owner chat 2026-10-07"}
        g["plan_updates"] = [update]
        covered = M.graph_diff(graph(), g)
        self.assertTrue(covered["conserved"], covered["findings"])
        self.assertEqual(1, covered["summary"]["dropped"])
        g["plan_updates"] = [{**update, "owner_authorized": False}]
        self.assertEqual(["PLAN_UPDATE_UNAUTHORISED"], self.codes(M.graph_diff(graph(), g)))
        g["plan_updates"] = [{**update, "owner_basis": ""}]
        self.assertEqual(["PLAN_UPDATE_UNAUTHORISED"], self.codes(M.graph_diff(graph(), g)))
        g["plan_updates"] = [{**update, "kind": "SCOPE_EXPANSION"}]  # right words, wrong kind
        self.assertEqual(["POINTS_DRIFT", "UNIT_LOST"], sorted(set(self.codes(M.graph_diff(graph(), g)))))

    def test_reweighting_is_a_scope_change_unless_declared(self):
        g = copy.deepcopy(graph())
        leaf_of(g, "Common#592")["units"][1]["weight"] = 10
        self.assertEqual(["POINTS_DRIFT"], sorted(set(self.codes(M.graph_diff(graph(), g)))))
        g["plan_updates"] = [self.UPDATE]
        self.assertTrue(M.graph_diff(graph(), g)["conserved"])

    def test_adding_scope_dilutes_everyone_so_it_must_be_declared(self):
        g = copy.deepcopy(graph())
        g["nodes"].append({"ref": "Common#630", "kind": "LEAF", "parent": "Common#588", "weight": 1, "units": [{"id": "X1", "weight": 1}]})
        report = M.graph_diff(graph(), g)
        self.assertEqual(["POINTS_DRIFT"], sorted(set(self.codes(report))))
        self.assertEqual({"Common#592:U01", "Common#592:U02", "Common#592:U03", "Common#592:U04", "Common#594:V1", "Common#594:V2"}, {r["item"] for r in report["drift"]})
        g["plan_updates"] = [{"id": "PU-2", "kind": "SCOPE_EXPANSION", "nodes": ["Common#588"], "reason": "new lane", "owner_authorized": True, "owner_basis": "Owner chat"}]
        declared = M.graph_diff(graph(), g)
        self.assertTrue(declared["conserved"], declared["findings"])
        self.assertEqual(1, declared["summary"]["added"])

    def test_removing_scope_raises_everyone_so_it_must_be_declared_as_a_reduction(self):
        new = copy.deepcopy(graph())
        new["nodes"] = [n for n in new["nodes"] if n["ref"] != "Common#594"]
        report = M.graph_diff(graph(), new)
        self.assertEqual({"UNIT_LOST", "POINTS_DRIFT"}, set(self.codes(report)))
        new["plan_updates"] = [
            {"id": "PU-3", "kind": "SCOPE_REDUCTION", "nodes": ["Common#594", "Common#588"], "reason": "lane cancelled", "owner_authorized": True, "owner_basis": "Owner chat"}
        ]
        self.assertTrue(M.graph_diff(graph(), new)["conserved"])

    def test_the_wrong_kind_of_update_does_not_cover_a_change(self):
        g = copy.deepcopy(graph())
        g["nodes"].append({"ref": "Common#630", "kind": "LEAF", "parent": "Common#588", "weight": 1, "units": [{"id": "X1", "weight": 1}]})
        g["plan_updates"] = [{"id": "PU-5", "kind": "SCOPE_REDUCTION", "nodes": ["Common#588"], "reason": "mislabelled", "owner_authorized": True, "owner_basis": "Owner chat"}]
        report = M.graph_diff(graph(), g)
        self.assertFalse(report["conserved"])  # added scope dilutes everyone; only an expansion or a reweight covers that
        self.assertIn("POINTS_DRIFT", self.codes(report))
        self.assertEqual(["PLAN_UPDATE_UNUSED"], self.codes(report, "ADVISORY"))

    def test_moving_a_leaf_to_another_phase_changes_shares_and_is_caught(self):
        g = copy.deepcopy(graph())
        leaf_of(g, "Common#594")["parent"] = "Common#610"  # a heavier slice of the programme than #588 gave it
        report = M.graph_diff(graph(), g)
        self.assertFalse(report["conserved"])
        self.assertIn("Common#594:V1", {row["item"] for row in report["drift"]})
        self.assertIn("Common#612:W1", {row["item"] for row in report["drift"]})  # the new siblings are diluted

    def test_decomposing_reserve_into_leaves_conserves_the_existing_shares(self):
        old = copy.deepcopy(graph())
        leaf_of(old, "Common#610")["reserve_weight"] = 2
        new = copy.deepcopy(old)
        leaf_of(new, "Common#610")["reserve_weight"] = 1
        new["nodes"].append({"ref": "Common#640", "kind": "LEAF", "parent": "Common#610", "weight": 1, "units": [{"id": "Y1", "weight": 1}]})
        report = M.graph_diff(old, new)
        self.assertTrue(report["conserved"], report["findings"])
        self.assertEqual(1, report["summary"]["added"])

    def test_a_move_must_name_a_real_origin_and_be_claimed_once(self):
        g = self.split()
        leaf_of(g, "Common#620")["units"][0]["moved_from"] = "Common#594"  # #594 never had U03
        self.assertIn("MOVE_ORIGIN_UNKNOWN", self.codes(M.graph_diff(graph(), g)))
        g = self.split()
        leaf_of(g, "Common#592")["units"].append({"id": "U03", "weight": 25})  # still in #592 and also claimed by #620
        self.assertIn("MOVE_DUPLICATE", self.codes(M.graph_diff(graph(), g)))

    def test_a_stale_moved_from_note_from_an_earlier_split_is_harmless(self):
        already_split = self.split()
        again = copy.deepcopy(already_split)
        report = M.graph_diff(already_split, again)  # #620:U03 still carries moved_from, but it already lived there
        self.assertTrue(report["conserved"], report["findings"])
        self.assertEqual(0, report["summary"]["moved"])

    def test_plan_updates_are_append_only_history(self):
        old = copy.deepcopy(graph())
        old["plan_updates"] = [self.UPDATE]
        same = M.graph_diff(old, copy.deepcopy(old))
        self.assertTrue(same["conserved"])
        self.assertEqual([], same["findings"])  # history is not "fresh" and so is not reported as unused
        edited = copy.deepcopy(old)
        edited["plan_updates"][0]["reason"] = "rewritten"
        self.assertEqual(["PLAN_HISTORY_CHANGED"], self.codes(M.graph_diff(old, edited)))
        removed = copy.deepcopy(old)
        removed["plan_updates"] = []
        self.assertEqual(["PLAN_HISTORY_CHANGED"], self.codes(M.graph_diff(old, removed)))

    def test_an_update_that_covers_nothing_is_an_advisory(self):
        new = copy.deepcopy(graph())
        new["plan_updates"] = [self.UPDATE]
        report = M.graph_diff(graph(), new)
        self.assertTrue(report["conserved"])
        self.assertEqual(["PLAN_UPDATE_UNUSED"], self.codes(report, "ADVISORY"))

    def test_weakening_the_gate_needs_a_policy_change_update(self):
        change = {"id": "PU-9", "kind": "POLICY_CHANGE", "reason": "relax for the migration", "owner_authorized": True, "owner_basis": "Owner chat 2026-10-07"}
        for label, new in {
            "mode to advisory": planned("ADVISORY"),
            "mode off": planned("OFF"),
            "more units": planned(units={"max": 12}),
            "fewer units required": planned(units={"min": 1}),
            "bigger share": planned(units={"max_share_percent": 60}),
            "bigger budget": planned(leaf_budget={"hard_loc": 3000}),
            "no nano floor": planned(min_leaf_target_loc=0),
            "dropped requirement": planned(require={"verify": False}),
        }.items():
            with self.subTest(label):
                self.assertEqual(["POLICY_WEAKENED"], self.codes(M.graph_diff(planned(), new)))
                new["plan_updates"] = [change]
                report = M.graph_diff(planned(), new)
                self.assertTrue(report["conserved"], report["findings"])
                self.assertEqual([], report["findings"])  # the update is used, not reported as idle

    def test_tightening_the_gate_needs_no_update(self):
        for old, new in (
            (planned("ADVISORY"), planned("ENFORCED")),
            (planned(), planned(units={"max": 6})),
            (planned(), planned(leaf_budget={"hard_loc": 1000})),
            (planned(require={"verify": False}), planned()),
        ):
            report = M.graph_diff(old, new)
            self.assertTrue(report["conserved"])
            self.assertEqual([], report["findings"])

    def test_dropping_a_delivery_gate_is_lost_progress_bar(self):
        old = copy.deepcopy(graph())
        leaf_of(old, "Common#592")["delivery_gates"] = [{"id": "REVIEWER_ACCEPTANCE", "weight": 40}]
        report = M.graph_diff(old, graph())
        self.assertIn("UNIT_LOST", self.codes(report))
        self.assertIn("Common#592:gate:REVIEWER_ACCEPTANCE", " ".join(f["detail"] for f in report["findings"]))
        new = copy.deepcopy(graph())
        new["plan_updates"] = [
            {"id": "PU-4", "kind": "UNIT_DROPPED", "units": ["Common#592:gate:REVIEWER_ACCEPTANCE"], "nodes": ["Common#592"], "reason": "gate retired", "owner_authorized": True, "owner_basis": "Owner chat"}
        ]
        self.assertTrue(M.graph_diff(old, new)["conserved"])

    def test_the_total_weight_scale_never_registers_as_drift(self):
        new = copy.deepcopy(graph())
        new["programme"]["total_weight"] = 777
        self.assertEqual([], M.graph_diff(graph(), new)["findings"])

    def test_points_are_exact_and_the_diff_is_pure(self):
        old, new = graph(), self.split(new_leaf_weight=1)
        before = copy.deepcopy((old, new))
        report = M.graph_diff(old, new)
        self.assertEqual(report, M.graph_diff(old, new))
        self.assertEqual(before, (old, new))
        u03 = next(r for r in report["drift"] if r["item"] == "Common#620:U03")
        self.assertEqual("1406.25", u03["points_before"])  # 9/64 of the programme on a 10000 scale
        self.assertEqual("625", u03["points_after"])  # 1/16: the new leaf is under-weighted


class DecompositionCommandLine(unittest.TestCase):
    def write(self, root, name, value):
        path = root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return str(path)

    def test_decompose_check_exit_codes_follow_the_effective_mode(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            bad, good = self.write(root, "bad.json", broken()), self.write(root, "good.json", planned())
            code, out, _ = cli("decompose-check", "--graph", bad)
            self.assertEqual(1, code)
            self.assertIn("DECOMPOSITION GATE — ENFORCED", out)
            self.assertIn("Common#594 [PRODUCT] NOT_RELEASEABLE", out)
            self.assertIn("BLOCKER  OUTCOME_MISSING", out)
            self.assertEqual(0, cli("decompose-check", "--graph", good)[0])
            self.assertEqual(0, cli("decompose-check", "--graph", bad, "--mode", "ADVISORY")[0])
            code, out, _ = cli("decompose-check", "--graph", bad, "--mode", "OFF")
            self.assertEqual(0, code)
            self.assertIn("informational: nothing is enforced", out)
            plain = self.write(root, "plain.json", graph())
            self.assertEqual(1, cli("decompose-check", "--graph", plain, "--mode", "ENFORCED")[0])  # a CI can force the gate on

    def test_decompose_check_json_and_closed_leaves(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            bad = self.write(root, "bad.json", broken(ref="Common#612"))
            code, out, _ = cli("decompose-check", "--graph", bad, "--json")
            self.assertEqual(1, code)
            report = json.loads(out)
            self.assertEqual(M.DECOMPOSITION_SCHEMA, report["schema"])
            self.assertEqual(["OUTCOME_MISSING"], [b["code"] for b in report["leaves"]["Common#612"]["blockers"]])
            done = [entry(facts(leaf="Common#612", pr="Common#613", units=[unit("W1"), unit("W2"), unit("W3")], result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1)]
            code, out, _ = cli("decompose-check", "--graph", bad, "--facts", self.write(root, "f.json", done), "--observations", self.write(root, "o.json", OBS_A))
            self.assertEqual(0, code)
            self.assertIn("1 closed (skipped)", out)

    def test_graph_diff_exit_codes_and_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            old = self.write(root, "old.json", graph())
            good = self.write(root, "good.json", PlanConservation.split())
            bad = self.write(root, "bad.json", PlanConservation.split(new_leaf_weight=1))
            code, out, _ = cli("graph-diff", "--old", old, "--new", good)
            self.assertEqual(0, code)
            self.assertIn("PLAN CONSERVATION — CONSERVED", out)
            self.assertIn("moved 2", out)
            code, out, _ = cli("graph-diff", "--old", old, "--new", bad)
            self.assertEqual(1, code)
            self.assertIn("NOT_CONSERVED", out)
            self.assertIn("POINTS_DRIFT", out)
            code, out, _ = cli("graph-diff", "--old", old, "--new", bad, "--json")
            self.assertEqual(1, code)
            self.assertEqual(M.DIFF_SCHEMA, json.loads(out)["schema"])

    def test_admit_cli_shows_the_plan_line_and_the_fix_plan_action(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            graph_path = self.write(root, "g.json", broken(ref="Common#592"))
            facts_path = self.write(root, "f.json", DecompositionAdmission.LEDGER)
            obs_path = self.write(root, "o.json", OBS_A)
            code, out, _ = cli("admit", "--graph", graph_path, "--facts", facts_path, "--observations", obs_path, "--leaf", "Common#592")
            self.assertEqual(0, code)
            self.assertIn("PLAN: NOT_RELEASEABLE — OUTCOME_MISSING", out)
            code, out, _ = cli("admit", "--graph", graph_path, "--facts", facts_path, "--observations", obs_path, "--leaf", "Common#592", "--json")
            self.assertEqual("FIX_PLAN", json.loads(out)["action"])

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_the_shipped_example_plan_passes_its_own_enforced_gate(self):
        example = MODULE_PATH.parents[1] / "examples" / "delp" / "execution-graph.yaml"
        code, out, _ = cli("decompose-check", "--graph", str(example))
        self.assertEqual(0, code, out)
        self.assertIn("DECOMPOSITION GATE — ENFORCED", out)
        self.assertIn("3 leaves · 3 releasable · 0 not releasable", out)


@unittest.skipUnless(HAVE_YAML and HAVE_JSONSCHEMA, "PyYAML/jsonschema unavailable")
class DecompositionSchemasAgreeWithTheEngine(unittest.TestCase):
    schema = SchemasAgreeWithTheEngine.schema
    schema_errors = SchemasAgreeWithTheEngine.schema_errors

    def test_a_fully_decomposed_plan_passes_both(self):
        g = planned()
        g["plan_updates"] = [
            {"id": "PU-1", "kind": "SCOPE_EXPANSION", "nodes": ["Common#588"], "reason": "r", "owner_authorized": True, "owner_basis": "b"},
            {"id": "PU-2", "kind": "UNIT_DROPPED", "units": ["Common#592:gate:REVIEWER_ACCEPTANCE", "Common#592:U04"], "reason": "r"},
            {"id": "PU-3", "kind": "POLICY_CHANGE", "reason": "r"},
        ]
        leaf_of(g, "Common#594")["depends_on"] = ["Common#592"]
        leaf_of(g, "Common#594")["parallel_ok"] = ["Common#612"]
        leaf_of(g, "Common#594")["parallel_ok_basis"] = "disjoint files"
        leaf_of(g, "Common#612")["work_class"] = "MECHANICAL"
        self.assertEqual([], self.schema_errors("execution-graph", g))
        M.validate_graph(g)

    def test_malformed_decomposition_fields_fail_both(self):
        leaf = lambda g: leaf_of(g, "Common#592")  # noqa: E731
        for label, mutate in {
            "work_class": lambda g: leaf(g).__setitem__("work_class", "EPIC"),
            "size_budget key": lambda g: leaf(g).__setitem__("size_budget", {"loc": 5}),
            "write_surface glob": lambda g: leaf(g).__setitem__("write_surface", ["src/*.py"]),
            "depends_on ref": lambda g: leaf(g).__setitem__("depends_on", ["x"]),
            "policy mode": lambda g: g["programme"]["decomposition_policy"].__setitem__("mode", "STRICT"),
            "policy key": lambda g: g["programme"]["decomposition_policy"].__setitem__("surprise", 1),
            "total_weight": lambda g: g["programme"].__setitem__("total_weight", 0),
            "update kind": lambda g: g.__setitem__("plan_updates", [{"id": "P", "kind": "WIDEN", "reason": "r", "nodes": ["Common#588"]}]),
            "update without scope": lambda g: g.__setitem__("plan_updates", [{"id": "P", "kind": "UNIT_REWEIGHT", "reason": "r"}]),
            "update item key": lambda g: g.__setitem__("plan_updates", [{"id": "P", "kind": "UNIT_DROPPED", "reason": "r", "units": ["Common#592"]}]),
        }.items():
            with self.subTest(label):
                g = planned()
                mutate(g)
                self.assertTrue(self.schema_errors("execution-graph", g), "schema accepted it")
                with self.assertRaises(M.GraphError):
                    M.validate_graph(g)

    def test_projection_with_the_gate_on_satisfies_the_live_status_schema(self):
        for ledger in ([], DecompositionInProjection.LEDGER):
            for mode in ("ADVISORY", "ENFORCED"):
                projection = M.project(broken(mode), ledger, OBS_A)
                for ref, node in projection["nodes"].items():
                    document = M.status_document(node, version=1, digest=projection["input_digest"], programme=projection["programme"])
                    with self.subTest(mode=mode, ref=ref, facts=bool(ledger)):
                        self.assertEqual([], self.schema_errors("live-status", json.loads(M.canonical_json(document))))


# --------------------------------------------------------------------------
# materialization: provider truth the ledger lacks reads as unknown, never as zero
# --------------------------------------------------------------------------


class MaterializationUnknownIsNotZero(unittest.TestCase):
    def leaf(self, obs, ledger=(), g=None, ref="Common#592"):
        return M.project(g or graph(), list(ledger), obs)["nodes"][ref]

    def test_work_the_provider_shows_but_the_ledger_lacks_is_unmaterialized_never_zero(self):
        for pr_state in ("OPEN", "MERGED", "CLOSED", "merged"):
            with self.subTest(pr_state):
                node = self.leaf({"Common#592": {"candidate_sha": SHA_A, "pr_state": pr_state}})
                signal = f"PR_{pr_state.upper()}"
                self.assertEqual("UNMATERIALIZED", node["state"])
                self.assertEqual("UNMATERIALIZED", node["lifecycle"])
                self.assertEqual("🟡", node["light"])
                self.assertEqual("🟡 [#527 › #588 › #592 → PR#593] R:P0/E0 · NO_ACTIVE_UNIT · UNMATERIALIZED", node["title_prefix"])
                self.assertEqual({"status": "UNMATERIALIZED", "provider_signal": signal}, node["materialization"])
                self.assertIn(f"UNMATERIALIZED:{signal}", node["warnings"])

    def test_a_branch_ahead_of_its_base_is_work_and_anything_else_is_not(self):
        node = self.leaf({"Common#592": {"candidate_sha": SHA_A, "ahead_by": 9}})
        self.assertEqual("BRANCH_AHEAD_9", node["materialization"]["provider_signal"])
        for nothing in (
            {"candidate_sha": SHA_A},  # an observed head alone proves nothing: a fresh branch points at its base
            {"candidate_sha": SHA_A, "ahead_by": 0},
            {"candidate_sha": SHA_A, "ahead_by": -1},
            {"candidate_sha": SHA_A, "ahead_by": True},
            {"candidate_sha": SHA_A, "ahead_by": "9"},
            {"candidate_sha": SHA_A, "pr_state": "UNKNOWN"},
        ):
            with self.subTest(nothing):
                node = self.leaf({"Common#592": nothing})
                self.assertEqual("NOT_STARTED", node["state"])
                self.assertNotIn("materialization", node)
        self.assertEqual("NOT_STARTED", self.leaf({})["state"])

    def test_any_accepted_fact_materializes_the_leaf_and_a_rejected_one_does_not(self):
        obs = {"Common#592": {"candidate_sha": SHA_A, "pr_state": "OPEN"}}
        reported = [entry(facts(units=[unit("U01")], next={"unit": "U02", "action": "next"}), 1)]
        node = self.leaf(obs, reported)
        self.assertEqual("ACTIVE", node["state"])
        self.assertNotIn("materialization", node)
        forged = M.project(graph(), [entry(facts(units=[unit("U01")], progress=50), 1)], obs)
        self.assertEqual("UNMATERIALIZED", forged["nodes"]["Common#592"]["state"])
        self.assertEqual(1, len(forged["rejected_facts"]))

    def test_an_unmaterialized_leaf_moves_no_number_and_every_ancestor_says_the_numbers_are_a_lower_bound(self):
        obs = {"Common#592": {"candidate_sha": SHA_A, "pr_state": "MERGED"}}
        silent, loud = M.project(graph(), [], {})["nodes"], M.project(graph(), [], obs)["nodes"]
        for ref in silent:
            self.assertEqual(silent[ref]["progress"], loud[ref]["progress"], ref)  # nothing is invented
        self.assertEqual("🟡 [#527 › #588] Φ:D0/E0 · F0 · UNMATERIALIZED", loud["Common#588"]["title_prefix"])
        self.assertEqual("🟡 [#527] Π:D0/E0 · F0 · UNMATERIALIZED", loud["Common#527"]["title_prefix"])
        self.assertEqual("⚪ [#527 › #610] Φ:D0/E0 · F0 · IDLE", loud["Common#610"]["title_prefix"])  # nothing unreported below it
        self.assertEqual({"status": "UNMATERIALIZED", "leaves": ["Common#592"]}, loud["Common#527"]["materialization"])
        self.assertIn("UNMATERIALIZED_LEAVES:1", loud["Common#527"]["warnings"])
        self.assertEqual("UNMATERIALIZED", loud["Common#527"]["lifecycle"])
        self.assertEqual(0, loud["Common#527"]["frontier"]["count"])  # an unreported leaf is not active frontier

    def test_unmaterialized_outranks_benign_and_evidence_states_but_not_a_critical_dead_executor(self):
        obs = {**OBS_A, "Common#594": {"candidate_sha": SHA_A, "pr_state": "OPEN"}}
        active = [entry(facts(units=[unit("U01")], next={"unit": "U02", "action": "x"}), 1)]
        nodes = M.project(graph(), active, obs)["nodes"]
        self.assertEqual(("ACTIVE", "UNMATERIALIZED"), (nodes["Common#592"]["state"], nodes["Common#594"]["state"]))
        self.assertEqual("UNMATERIALIZED", nodes["Common#588"]["state"])  # one active leaf does not hide an unreported sibling
        self.assertEqual(1, nodes["Common#588"]["frontier"]["count"])
        gap = [entry(facts(units=[unit("U01", refs=())]), 1)]
        self.assertEqual("UNMATERIALIZED", M.project(graph(), gap, obs)["nodes"]["Common#588"]["state"])
        dead = {**obs, "Common#592": {"candidate_sha": SHA_A, "liveness": "STALE"}}  # #592 is critical in graph()
        self.assertEqual("STALE", M.project(graph(), active, dead)["nodes"]["Common#588"]["state"])

    def test_a_dead_executor_outranks_an_unreported_leaf_on_the_leaf_itself(self):
        node = self.leaf({"Common#592": {"candidate_sha": SHA_A, "pr_state": "OPEN", "liveness": "STALE"}})
        self.assertEqual(("STALE", "UNMATERIALIZED"), (node["state"], node["lifecycle"]))

    def test_the_decomposition_gate_does_not_overlay_an_unmaterialized_leaf(self):
        node = self.leaf({"Common#594": {"candidate_sha": SHA_A, "pr_state": "OPEN"}}, g=broken(), ref="Common#594")
        self.assertEqual("UNMATERIALIZED", node["state"])
        self.assertFalse(node["plan"]["releasable"])  # still reported, and still blocks new units at admission

    def test_generated_titles_with_the_new_state_round_trip_through_the_title_grammar(self):
        obs = {"Common#592": {"candidate_sha": SHA_A, "pr_state": "MERGED"}}
        for ref, node in M.project(graph(), [], obs)["nodes"].items():
            title = M.render_title(node["title_prefix"], "Human title")
            self.assertEqual("OK", M.title_drift(title, node["title_prefix"])["status"], ref)
            self.assertEqual("Human title", M.split_title(title)[1])


class MaterializationAdmission(unittest.TestCase):
    OBS = {"Common#592": {"candidate_sha": SHA_A, "pr_state": "MERGED"}}

    def admit(self, ledger=(), g=None, obs=None):
        return M.admit(M.project(g or graph(), list(ledger), obs or self.OBS), "Common#592", "continue")

    def test_an_unreported_leaf_is_told_to_publish_facts_before_any_new_work(self):
        report = self.admit()
        self.assertEqual("MATERIALIZE_FACTS", report["action"])
        self.assertTrue(report["materialize_required"])
        self.assertFalse(report["recovery_required"])
        self.assertEqual("NONE", report["evidence_health"])
        self.assertEqual([], report["authority_effects"])
        text = M.render_checkpoint(report)
        self.assertIn("CHILD: R:P0/E0 · NO_ACTIVE_UNIT · UNMATERIALIZED", text)
        self.assertIn("EVIDENCE: NONE — no accepted facts; provider shows PR_MERGED (live @ aaaaaaa)", text)
        self.assertIn(
            "NEXT: MATERIALIZE_FACTS before any new work — the provider shows PR_MERGED but the ledger has no accepted "
            "CHECKPOINT_FACTS_V1 for this leaf; publish facts for exactly what current evidence supports (completion is never inferred)",
            text,
        )

    def test_a_failing_plan_is_reported_alongside_but_does_not_come_first(self):
        report = self.admit(g=broken(ref="Common#592"))
        self.assertEqual("MATERIALIZE_FACTS", report["action"])
        self.assertIn("the plan also fails the decomposition gate (OUTCOME_MISSING)", report["next"])
        self.assertFalse(report["plan_fix_required"])

    def test_publishing_facts_ends_it_and_the_ordinary_barrier_takes_over(self):
        ledger = [entry(facts(units=[unit("U01"), unit("U02")], next={"unit": "U03", "action": "continue the replay lane"}), 1)]
        report = self.admit(ledger)
        self.assertEqual("CONTINUE_UNIT", report["action"])
        self.assertNotIn("materialize_required", report)
        self.assertIn("EVIDENCE: CURRENT @ aaaaaaa", M.render_checkpoint(report))

    def test_a_completed_leaf_never_asks_for_materialization(self):
        done = [entry(facts(units=[unit("U01"), unit("U02"), unit("U03"), unit("U04")], result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1)]
        self.assertEqual("NONE", self.admit(done)["action"])

    def test_without_provider_signals_nothing_changes(self):
        report = self.admit(obs={"Common#592": {"candidate_sha": SHA_A}})  # an observed head alone proves no work
        self.assertEqual("CONTINUE_UNIT", report["action"])
        self.assertEqual("NOT_STARTED", report["state"])
        self.assertNotIn("materialize_required", report)
        self.assertNotIn("materialization", report)


class RepositoryGuard(unittest.TestCase):
    """A plan may only be applied to the repository it declares: example plans reuse real issue numbers."""

    def run_sync(self, programme, *extra, repository="reallaksh19/Common"):
        import unittest.mock as mock

        g = copy.deepcopy(graph())
        g["programme"].update(programme)
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "g.json"
            path.write_text(json.dumps(g), encoding="utf-8")
            with mock.patch.object(M, "GhTransport") as transport, mock.patch.object(
                M, "plan_github", return_value={"ok": True}
            ) as plan, mock.patch.object(M, "sync_projection", return_value={}) as sync:
                code, _, err = cli("sync-github", "--graph", str(path), "--repository", repository, *extra)
        return code, err, transport, plan, sync

    def test_a_declared_repository_that_differs_is_refused_before_anything_is_read_or_written(self):
        for extra in ((), ("--dry-run",)):
            with self.subTest(extra):
                code, err, transport, plan, sync = self.run_sync({"repository": "example/delp-demo"}, *extra)
                self.assertEqual(1, code)
                self.assertIn("does not match --repository", err)
                self.assertIn("example/delp-demo", err)
                transport.assert_not_called()
                plan.assert_not_called()
                sync.assert_not_called()

    def test_a_live_sync_requires_the_plan_to_name_its_repository(self):
        code, err, transport, _, sync = self.run_sync({})
        self.assertEqual(1, code)
        self.assertIn("programme.repository is required for a live sync-github", err)
        transport.assert_not_called()
        sync.assert_not_called()
        code, err, transport, plan, _ = self.run_sync({}, "--dry-run")  # read-only, so it may omit it
        self.assertEqual(0, code)
        plan.assert_called_once()

    def test_a_matching_repository_passes_regardless_of_case(self):
        code, _, _, _, sync = self.run_sync({"repository": "ReallaKSH19/common"})
        self.assertEqual(0, code)
        sync.assert_called_once()

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_the_shipped_example_cannot_be_applied_to_a_real_repository(self):
        example = M._load_structured(MODULE_PATH.parents[1] / "examples" / "delp" / "execution-graph.yaml")
        self.assertEqual("example/delp-demo", example["programme"]["repository"])
        for live in (False, True):
            with self.assertRaises(M.DelpError):
                M.require_repository_match(example, "reallaksh19/Common", live=live)
        M.require_repository_match(example, "example/delp-demo", live=True)


class RealScenarioReplay(unittest.TestCase):
    """The #527 / P3-I situation as handed over on 2026-10-07, replayed through the projector.

    Real (from the handover and the provider): issue and PR numbers, the merge commits, the P3-I branch head and its
    divergence from main (ahead 9, behind 4), the programme denominator 10000 and Phase 3's closed weight 1650.
    Assumed, because the handover does not give them: each closed P3-SOLO leaf weighs 275 (only their sum is real),
    each has one unit, and P3-I's three units. The 8100 of the programme that is not in any graph yet is an explicit
    reserve, so every number below is a lower bound over what the graph can see - which is exactly the point.
    """

    SOLO = [  # (leaf issue, primary PR, commit standing in as the candidate)
        ("Common#574", "Common#575", "aeb855919d9866972248d811c75962dcb8fed861"),
        ("Common#576", "Common#577", "39cca232b9a4cbdc3643f763af682c4aa3830828"),
        ("Common#578", "Common#579", "8041f6ab4959a9aac4fbd1450e7e4523b18d8ce1"),
        ("Common#580", "Common#581", "3157ddbfb6a47ba397480d4771ef3c906e03a4c9"),
        ("Common#582", "Common#583", "a05db7c57fdacc2f5fcb0e55e300d6d76f70e4cd"),
        ("Common#584", "Common#587", "797acb30a6bc7942104423f426dfd25758e4f655"),
    ]
    BRANCH = "prod/527-p3-i-full-solo-role-replay"
    OLD_HEAD = "ff7c3b7678a77ff943bb7314cd5a01f5fd9e99b6"
    REBASED_HEAD = "e" * 40

    @classmethod
    def plan(cls):
        nodes = [{"ref": "Common#527", "kind": "ROOT", "reserve_weight": 8100}]
        for ref, pr, _ in cls.SOLO:
            nodes.append({"ref": ref, "kind": "LEAF", "parent": "Common#527", "weight": 275, "primary_pr": pr, "units": [{"id": "U1", "weight": 1}]})
        nodes.append(
            {
                "ref": "Common#588",
                "kind": "LEAF",
                "parent": "Common#527",
                "weight": 250,
                "candidate_ref": cls.BRANCH,
                "units": [{"id": "A", "weight": 20}, {"id": "B", "weight": 50}, {"id": "C", "weight": 30}],
            }
        )
        return {"schema": M.GRAPH_SCHEMA, "programme": {"id": "COMMON-PROD-CONTROL-V1", "root": "Common#527", "repository": "reallaksh19/Common"}, "nodes": nodes}

    @classmethod
    def observations(cls, head=None):
        obs = {ref: {"candidate_sha": sha, "pr_state": "MERGED"} for ref, _, sha in cls.SOLO}
        obs["Common#588"] = {"candidate_sha": head or cls.OLD_HEAD, "ahead_by": 9, "behind_by": 4}
        return obs

    @classmethod
    def closed_ledger(cls):
        return [
            entry(
                facts(
                    leaf=ref,
                    pr=pr,
                    sha=sha,
                    units=[unit("U1", refs=(f"{ref}#issuecomment-1",))],
                    result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"},
                ),
                index,
            )
            for index, (ref, pr, sha) in enumerate(cls.SOLO, 1)
        ]

    @classmethod
    def p3i_facts(cls, sha, order):
        record = {
            "schema": M.FACTS_SCHEMA,
            "responsibility": {"issue": "Common#588"},
            "material": {"candidate_sha": sha},
            "units": [unit("A", refs=("Common#588#issuecomment-1",))],
            "next": {"unit": "B", "action": "rebase the integration runtime onto main"},
        }
        return entry(record, order)

    def test_wiring_delp_onto_history_with_an_empty_ledger_reads_unknown_not_zero(self):
        nodes = M.project(self.plan(), [], self.observations())["nodes"]
        self.assertEqual("🟡 [#527] Π:D0/E0 · F0 · UNMATERIALIZED", nodes["Common#527"]["title_prefix"])
        for ref, *_ in self.SOLO:
            self.assertEqual(("UNMATERIALIZED", "PR_MERGED"), (nodes[ref]["state"], nodes[ref]["materialization"]["provider_signal"]), ref)
        self.assertEqual("BRANCH_AHEAD_9", nodes["Common#588"]["materialization"]["provider_signal"])
        self.assertIn("UNMATERIALIZED_LEAVES:7", nodes["Common#527"]["warnings"])
        self.assertIn("UNDECOMPOSED_RESERVE:8100", nodes["Common#527"]["warnings"])

    def test_the_successors_first_continue_is_to_materialize_not_to_code(self):
        projection = M.project(self.plan(), [], self.observations())
        text = M.render_checkpoint(M.admit(projection, "Common#588", "continue"))
        self.assertIn("EVIDENCE: NONE — no accepted facts; provider shows BRANCH_AHEAD_9 (live @ ff7c3b7)", text)
        self.assertIn("NEXT: MATERIALIZE_FACTS before any new work", text)

    def test_materializing_the_six_closed_leaves_gives_an_honest_lower_bound_and_still_flags_p3_i(self):
        nodes = M.project(self.plan(), self.closed_ledger(), self.observations())["nodes"]
        for ref, *_ in self.SOLO:
            self.assertEqual("COMPLETE", nodes[ref]["state"], ref)
        root = nodes["Common#527"]
        self.assertEqual("33/200", root["progress"]["ratio"]["D"])  # 1650 / 10000, not a hand-computed 72.5%
        self.assertEqual("33/200", root["progress"]["ratio"]["E"])
        self.assertEqual("🟡 [#527] Π:D17/E17 · F0 · UNMATERIALIZED", root["title_prefix"])  # P3-I is still unreported
        self.assertEqual({"status": "UNMATERIALIZED", "leaves": ["Common#588"]}, root["materialization"])

    def test_a_rebase_lowers_E_and_not_P_until_the_evidence_is_replayed_on_the_new_head(self):
        ledger = self.closed_ledger() + [self.p3i_facts(self.OLD_HEAD, 10)]
        before = M.project(self.plan(), ledger, self.observations())["nodes"]
        self.assertEqual("ACTIVE", before["Common#588"]["state"])
        self.assertEqual(("1/5", "1/5"), (before["Common#588"]["progress"]["ratio"]["P"], before["Common#588"]["progress"]["ratio"]["E"]))
        self.assertEqual("17/100", before["Common#527"]["progress"]["ratio"]["E"])  # (1650 + 250 * 1/5) / 10000
        moved = M.project(self.plan(), ledger, self.observations(head=self.REBASED_HEAD))["nodes"]
        self.assertEqual("EVIDENCE_STALE", moved["Common#588"]["state"])
        self.assertEqual(("1/5", "0/1"), (moved["Common#588"]["progress"]["ratio"]["P"], moved["Common#588"]["progress"]["ratio"]["E"]))
        self.assertEqual("17/100", moved["Common#527"]["progress"]["ratio"]["D"])  # semantic progress is untouched
        self.assertEqual("33/200", moved["Common#527"]["progress"]["ratio"]["E"])  # evidenced progress drops
        report = M.admit(M.project(self.plan(), ledger, self.observations(head=self.REBASED_HEAD)), "Common#588", "continue")
        self.assertEqual("RECOVER_EVIDENCE", report["action"])
        replayed = ledger + [self.p3i_facts(self.REBASED_HEAD, 11)]
        after = M.project(self.plan(), replayed, self.observations(head=self.REBASED_HEAD))["nodes"]
        self.assertEqual("17/100", after["Common#527"]["progress"]["ratio"]["E"])

    def test_the_provider_pass_observes_the_branch_and_publishes_unknown_not_zero(self):
        gh = FakeGitHub()
        for number in [527, 588] + [int(ref.split("#")[1]) for ref, *_ in self.SOLO]:
            gh.issues[number] = f"Title {number}"
        for _, pr, sha in self.SOLO:
            gh.pulls[int(pr.split("#")[1])] = {"head": {"sha": sha}, "state": "closed", "merged": True}
        gh.commits[self.BRANCH] = self.OLD_HEAD
        gh.compares[self.BRANCH] = {"ahead_by": 9, "behind_by": 4}
        g = self.plan()
        titles = {f"Common#{n}": t for n, t in gh.issues.items()}
        M.sync_projection(M.GitHubStore(gh), g, lambda: M.ledger_from_github(gh, g), lambda: M.observe_github(gh, g), titles)
        self.assertEqual("🟡 [#527] Π:D0/E0 · F0 · UNMATERIALIZED — Title 527", gh.issues[527])
        self.assertEqual("🟡 [#527 › #588] R:P0/E0 · NO_ACTIVE_UNIT · UNMATERIALIZED — Title 588", gh.issues[588])
        self.assertIn(("COMPARE", "main", self.BRANCH), gh.calls)


class FrontierSnapshotAndDrift(unittest.TestCase):
    """A handover carries the predecessor's frontier at one instant. DELP derives it and checks it is still true.

    The replay is the real event: the P3-I handover pinned `main` at 4acc5704; the next merge (#591) moved it to
    46916f48. The handover itself says to stop and recompute when main moves; this makes that rule mechanical.
    """

    MAIN_AT_HANDOVER = "4acc570495c96653366ef4cd7d5801a5cf747399"
    MAIN_NOW = "46916f4828090c1f32cf2856186b0b00defdbea3"
    LEAF = "Common#588"

    def observations(self, main=None, head=None, behind=4):
        obs = RealScenarioReplay.observations(head)
        for row in obs.values():
            row["base_sha"] = main or self.MAIN_AT_HANDOVER
        obs[self.LEAF]["behind_by"] = behind
        return obs

    def ledger(self):
        return RealScenarioReplay.closed_ledger() + [RealScenarioReplay.p3i_facts(RealScenarioReplay.OLD_HEAD, 10)]

    def frontier(self, ledger=None, obs=None, graph_value=None):
        return M.frontier(graph_value or RealScenarioReplay.plan(), self.ledger() if ledger is None else ledger, obs or self.observations(), self.LEAF)

    def test_the_frontier_holds_only_observed_and_derived_values_and_is_reproducible(self):
        snapshot = self.frontier()
        self.assertEqual(
            {"base_sha": self.MAIN_AT_HANDOVER, "candidate_sha": RealScenarioReplay.OLD_HEAD, "ahead_by": 9, "behind_by": 4},
            snapshot["observed"],
        )
        self.assertEqual(("ACTIVE", "1/5", "1/5", "B"), (snapshot["derived"]["state"], snapshot["derived"]["progress"]["P"], snapshot["derived"]["progress"]["E"], snapshot["derived"]["active_unit"]))
        self.assertEqual("CURRENT", snapshot["derived"]["evidence"]["health"])
        self.assertEqual(["Common#527", "Common#588"], snapshot["lineage"])
        self.assertEqual(M.AUTHORITY, snapshot["authority"])
        self.assertEqual(snapshot, self.frontier())
        self.assertEqual(snapshot, json.loads(M.canonical_json(snapshot)))
        self.assertEqual([], M.forbidden_fields(snapshot["observed"]))  # nothing an agent could have authored is in what was observed

    def test_main_moving_after_the_handover_makes_every_pinned_value_stale(self):
        snapshot = self.frontier()
        drift = M.frontier_drift(snapshot, self.frontier(obs=self.observations(main=self.MAIN_NOW)))
        self.assertEqual(("MOVED", "RECONCILE"), (drift["status"], drift["action"]))
        self.assertEqual([{"what": "BASE", "was": self.MAIN_AT_HANDOVER, "now": self.MAIN_NOW}], drift["moved"])
        self.assertEqual([], drift["changed"])  # nothing derived moved: the evidence is still on the same candidate
        self.assertIn("recompute from live truth", M.render_frontier_drift(drift))

    def test_unchanged_inputs_are_current(self):
        snapshot = self.frontier()
        drift = M.frontier_drift(snapshot, self.frontier())
        self.assertEqual(("CURRENT", "NONE", []), (drift["status"], drift["action"], drift["moved"]))
        self.assertEqual(snapshot["frontier_digest"], drift["live_digest"])

    def test_every_kind_of_movement_is_named(self):
        snapshot = self.frontier()
        replay_head = self.frontier(obs=self.observations(head=RealScenarioReplay.REBASED_HEAD))
        drift = M.frontier_drift(snapshot, replay_head)
        self.assertEqual({"CANDIDATE_HEAD"}, {m["what"] for m in drift["moved"]})
        self.assertEqual(
            {"STATE": ("ACTIVE", "EVIDENCE_STALE"), "EVIDENCE_HEALTH": ("CURRENT", "STALE_CANDIDATE"), "PROGRESS_E": ("1/5", "0/1")},
            {c["what"]: (c["was"], c["now"]) for c in drift["changed"]},
        )
        more = self.ledger() + [RealScenarioReplay.p3i_facts(RealScenarioReplay.OLD_HEAD, 11)]
        facts = M.frontier_drift(snapshot, self.frontier(ledger=more))
        self.assertEqual([{"what": "FACTS", "was": 1, "now": 2, "detail": "accepted facts records"}], facts["moved"])
        edited = RealScenarioReplay.plan()
        leaf_of(edited, self.LEAF)["units"][0]["weight"] = 30
        self.assertEqual({"PLAN"}, {m["what"] for m in M.frontier_drift(snapshot, self.frontier(graph_value=edited))["moved"]})
        dead = self.observations()
        dead[self.LEAF]["liveness"] = "STALE"
        stale = M.frontier_drift(snapshot, self.frontier(obs=dead))
        self.assertEqual({"LIVENESS"}, {m["what"] for m in stale["moved"]})
        self.assertEqual("STALE", next(c["now"] for c in stale["changed"] if c["what"] == "STATE"))

    def test_a_pull_request_leaf_reports_its_state_moving(self):
        leaf = "Common#584"
        was = M.frontier(RealScenarioReplay.plan(), RealScenarioReplay.closed_ledger(), self.observations(), leaf)
        reopened = self.observations()
        reopened[leaf]["pr_state"] = "OPEN"
        now = M.frontier(RealScenarioReplay.plan(), RealScenarioReplay.closed_ledger(), reopened, leaf)
        self.assertEqual([{"what": "PR_STATE", "was": "MERGED", "now": "OPEN"}], M.frontier_drift(was, now)["moved"])

    def test_an_input_the_predecessor_never_observed_is_not_treated_as_unchanged(self):
        blind = self.observations()
        for row in blind.values():
            row.pop("base_sha")
        drift = M.frontier_drift(self.frontier(obs=blind), self.frontier())
        self.assertEqual([{"what": "BASE", "was": None, "now": self.MAIN_AT_HANDOVER}], drift["moved"])
        self.assertEqual("MOVED", drift["status"])

    def test_a_snapshot_for_another_leaf_or_a_non_leaf_is_refused(self):
        with self.assertRaises(M.DelpError):
            M.frontier_drift(self.frontier(), M.frontier(RealScenarioReplay.plan(), self.ledger(), self.observations(), "Common#584"))
        with self.assertRaises(M.DelpError):
            M.frontier(RealScenarioReplay.plan(), [], {}, "Common#527")
        with self.assertRaises(M.DelpError):
            M.frontier(RealScenarioReplay.plan(), [], {}, "Common#99999")

    def test_the_continue_checkpoint_carries_the_material_frontier_instead_of_prose(self):
        projection = M.project(RealScenarioReplay.plan(), self.ledger(), self.observations())
        text = M.render_checkpoint(M.admit(projection, self.LEAF, "continue"))
        self.assertIn("FRONTIER: base 4acc570 · candidate ff7c3b7 · ahead 9 · behind 4", text)
        merged = M.render_checkpoint(M.admit(projection, "Common#584", "continue"))
        self.assertIn("FRONTIER: base 4acc570 · candidate 797acb3 · PR MERGED", merged)
        quiet = M.render_checkpoint(M.admit(M.project(graph(), [], OBS_A), "Common#592", "continue"))
        self.assertNotIn("FRONTIER:", quiet)  # observations without provider fields change nothing

    def test_command_line_snapshot_then_verify_exit_codes(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)

            def write(name, value):
                path = root / name
                path.write_text(json.dumps(value), encoding="utf-8")
                return str(path)

            graph_path, facts_path = write("g.json", RealScenarioReplay.plan()), write("f.json", self.ledger())
            then, now = write("then.json", self.observations()), write("now.json", self.observations(main=self.MAIN_NOW))
            snapshot = str(root / "snapshot.json")
            self.assertEqual(0, cli("frontier", "--graph", graph_path, "--facts", facts_path, "--observations", then, "--leaf", self.LEAF, "--output", snapshot)[0])
            code, out, _ = cli("frontier", "--graph", graph_path, "--facts", facts_path, "--observations", then, "--leaf", self.LEAF, "--text")
            self.assertEqual(0, code)
            self.assertIn("MATERIAL: base 4acc570 · candidate ff7c3b7 · ahead 9 · behind 4", out)
            self.assertIn("not current truth", out)
            code, out, _ = cli("frontier-verify", "--snapshot", snapshot, "--graph", graph_path, "--facts", facts_path, "--observations", then, "--leaf", self.LEAF)
            self.assertEqual(0, code)
            self.assertIn("FRONTIER DRIFT — CURRENT", out)
            code, out, _ = cli("frontier-verify", "--snapshot", snapshot, "--graph", graph_path, "--facts", facts_path, "--observations", now, "--leaf", self.LEAF)
            self.assertEqual(2, code)
            self.assertIn("MOVED   BASE: 4acc570 -> 46916f4", out)
            self.assertIn("ACTION: RECONCILE", out)
            code, out, _ = cli("frontier-verify", "--snapshot", snapshot, "--graph", graph_path, "--facts", facts_path, "--observations", now, "--leaf", self.LEAF, "--json")
            self.assertEqual(2, code)
            self.assertEqual(M.FRONTIER_DRIFT_SCHEMA, json.loads(out)["schema"])

    def test_live_mode_observes_read_only_and_honours_the_repository_guard(self):
        import unittest.mock as mock

        gh = FakeGitHub()
        gh.commits.update({"main": self.MAIN_NOW, RealScenarioReplay.BRANCH: RealScenarioReplay.OLD_HEAD})
        gh.compares[RealScenarioReplay.BRANCH] = {"ahead_by": 9, "behind_by": 4}
        for _, pr, sha in RealScenarioReplay.SOLO:
            gh.pulls[int(pr.split("#")[1])] = {"head": {"sha": sha}, "state": "closed", "merged": True}
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "g.json"
            path.write_text(json.dumps(RealScenarioReplay.plan()), encoding="utf-8")
            with mock.patch.object(M, "GhTransport", return_value=gh):
                code, out, _ = cli("frontier", "--graph", str(path), "--repository", "reallaksh19/Common", "--leaf", self.LEAF)
                self.assertEqual(0, code)
                self.assertEqual(self.MAIN_NOW, json.loads(out)["observed"]["base_sha"])
                self.assertEqual("UNMATERIALIZED", json.loads(out)["derived"]["state"])  # the ledger really is empty
                code, _, err = cli("frontier", "--graph", str(path), "--repository", "someone/else", "--leaf", self.LEAF)
                self.assertEqual(1, code)
                self.assertIn("does not match --repository", err)
        self.assertEqual([], [c for c in gh.calls if c[0] in {"POST", "PATCH_COMMENT", "PATCH_TITLE"}])  # nothing was written


# --------------------------------------------------------------------------
# agent health: observed or derived, never declared; advisory
# --------------------------------------------------------------------------


def with_health(mode="ADVISORY", g=None, **policy):
    g = copy.deepcopy(g or graph())
    g["programme"]["health_policy"] = {"mode": mode, **policy}
    return g


FULL_OBS = {  # every health input observed, all inside the written limits
    "candidate_sha": SHA_A,
    "pr_state": "OPEN",
    "base_sha": SHA_MAIN,
    "behind_by": 0,
    "additions": 120,
    "deletions": 30,
    "since_checkpoint": {"additions": 40, "deletions": 5, "commits": 1},
    "liveness": "ACTIVE",
    "interruptions": {"coverage_from": "2026-10-07T00:00:00Z", "losses": []},
}
STARTED = [entry(facts(units=[unit("U01"), unit("U02")], next={"unit": "U03", "action": "continue"}), 1)]


class AgentHealth(unittest.TestCase):
    def health(self, over=None, drop=(), ledger=None, g=None, ref="Common#592"):
        obs = {**FULL_OBS, **(over or {})}
        for key in drop:
            obs.pop(key, None)
        node = M.project(g or with_health(), STARTED if ledger is None else ledger, {ref: obs})["nodes"][ref]
        return node.get("health")

    @staticmethod
    def statuses(h):
        return {name: c["status"] for name, c in h["components"].items()}

    def test_off_is_the_default_and_adds_nothing_anywhere(self):
        for g in (graph(), with_health("OFF")):
            projection = M.project(g, STARTED, {"Common#592": FULL_OBS})
            self.assertTrue(all("health" not in n for n in projection["nodes"].values()))
            report = M.admit(projection, "Common#592")
            self.assertNotIn("health", report)
            self.assertNotIn("HEALTH:", M.render_checkpoint(report))

    def test_a_fully_observed_leaf_inside_every_limit_is_healthy_and_each_component_says_why(self):
        h = self.health()
        self.assertEqual(("HEALTHY", "🟢", True, []), (h["verdict"], h["light"], h["advisory"], h["reasons"]))
        self.assertEqual(
            {"materialization", "evidence", "checkpoint_distance", "size", "base_drift", "interruptions", "liveness"}, set(h["components"])
        )
        self.assertEqual({"OK"}, set(self.statuses(h).values()))
        self.assertTrue(all(c["detail"] for c in h["components"].values()))

    def test_unobserved_is_never_healthy(self):
        for component, key in {
            "checkpoint_distance": "since_checkpoint",
            "size": "additions",
            "base_drift": "behind_by",
            "interruptions": "interruptions",
            "liveness": "liveness",
        }.items():
            with self.subTest(component):
                h = self.health(drop=(key,))
                self.assertEqual("UNOBSERVED", h["components"][component]["status"])
                self.assertEqual(("UNOBSERVED", "⚪"), (h["verdict"], h["light"]))  # six other OK components do not make it healthy
        bare = M.project(with_health(), STARTED, {})["nodes"]["Common#592"]["health"]
        self.assertEqual("UNOBSERVED", bare["verdict"])
        self.assertEqual("OK", bare["components"]["materialization"]["status"])  # derived from the ledger, so it needs no observer
        self.assertEqual({"UNOBSERVED"}, {s for n, s in self.statuses(bare).items() if n != "materialization"})

    def test_the_verdict_is_the_worst_component_never_an_average(self):
        h = self.health({"behind_by": 25})
        self.assertEqual(("AT_RISK", "🔴", ["base_drift (25 commit(s) behind the base)"]), (h["verdict"], h["light"], h["reasons"]))
        self.assertEqual(("WATCH", "🟡"), (self.health({"liveness": "QUIET"})["verdict"], self.health({"liveness": "QUIET"})["light"]))
        self.assertEqual("WATCH", self.health({"liveness": "QUIET"}, drop=("behind_by",))["verdict"])  # a known concern outranks an unknown
        h = self.health({"liveness": "STALE", "behind_by": 1}, drop=("additions",))
        self.assertEqual("AT_RISK", h["verdict"])
        self.assertEqual(["liveness", "base_drift", "size"], [r.split(" (")[0] for r in h["reasons"]])  # AT_RISK, then WATCH, then UNOBSERVED

    def test_checkpoint_distance_follows_the_written_thresholds_exactly(self):
        for added, deleted, expected in (
            (249, 0, "OK"),
            (250, 0, "WATCH"),
            (499, 0, "WATCH"),
            (500, 0, "AT_RISK"),
            (100, 299, "OK"),  # 399 changed
            (100, 300, "WATCH"),  # 400 changed: the materially-modified trigger
            (100, 599, "WATCH"),  # 699 changed
            (100, 600, "AT_RISK"),  # 700 changed: the hard ceiling
        ):
            with self.subTest(added=added, deleted=deleted):
                h = self.health({"since_checkpoint": {"additions": added, "deletions": deleted}})
                self.assertEqual(expected, h["components"]["checkpoint_distance"]["status"])
        relaxed = with_health(checkpoint={"watch_added_loc": 300, "at_risk_added_loc": 600})
        self.assertEqual("OK", self.health({"since_checkpoint": {"additions": 290, "deletions": 0}}, g=relaxed)["components"]["checkpoint_distance"]["status"])

    def test_size_is_judged_against_the_declared_budget_else_the_policy_default(self):
        for total, expected in ((700, "OK"), (701, "WATCH"), (1500, "WATCH"), (1501, "AT_RISK")):
            with self.subTest(default=total):
                c = self.health({"additions": total - 10, "deletions": 10})["components"]["size"]
                self.assertEqual(expected, c["status"])
                self.assertIn("policy default", c["detail"])
        g = with_health()
        leaf_of(g, "Common#592")["size_budget"] = {"target_loc": 100, "hard_loc": 200, "target_minutes": 15, "hard_minutes": 20}
        for total, expected in ((100, "OK"), (101, "WATCH"), (200, "WATCH"), (201, "AT_RISK")):
            with self.subTest(declared=total):
                c = self.health({"additions": total, "deletions": 0}, g=g)["components"]["size"]
                self.assertEqual(expected, c["status"])
                self.assertIn("declared budget", c["detail"])

    def test_base_drift_interruptions_and_liveness_thresholds(self):
        for behind, expected in ((0, "OK"), (1, "WATCH"), (19, "WATCH"), (20, "AT_RISK")):
            self.assertEqual(expected, self.health({"behind_by": behind})["components"]["base_drift"]["status"], behind)
        tight = with_health(drift={"watch_behind": 5, "at_risk_behind": 10})
        self.assertEqual("OK", self.health({"behind_by": 4}, g=tight)["components"]["base_drift"]["status"])
        self.assertEqual("AT_RISK", self.health({"behind_by": 10}, g=tight)["components"]["base_drift"]["status"])
        watched = "2026-10-07T00:00:00Z"
        for losses, expected in ((0, "OK"), (1, "WATCH"), (2, "WATCH"), (3, "AT_RISK"), (4, "AT_RISK")):
            c = self.health({"interruptions": {"coverage_from": watched, "losses": [{"kind": "STREAM"}] * losses}})["components"]["interruptions"]
            self.assertEqual(expected, c["status"], losses)
        self.assertIn("plans a handover at the third", c["detail"])
        self.assertEqual("WATCH", self.health({"interruptions": {"losses": [{"kind": "STREAM"}]}})["components"]["interruptions"]["status"])  # a recorded loss counts without a coverage start
        self.assertEqual("UNOBSERVED", self.health({"interruptions": {"losses": []}})["components"]["interruptions"]["status"])  # zero needs an observer
        for liveness, expected in (("ACTIVE", "OK"), ("QUIET", "WATCH"), ("STALE", "AT_RISK"), (None, "UNOBSERVED")):
            self.assertEqual(expected, self.health({"liveness": liveness})["components"]["liveness"]["status"], liveness)

    def test_evidence_and_materialization_are_derived_from_the_ledger_not_declared(self):
        self.assertEqual("OK", self.health()["components"]["evidence"]["status"])
        gap = [entry(facts(units=[unit("U01", refs=())]), 1)]
        c = self.health(ledger=gap)["components"]["evidence"]
        self.assertEqual("WATCH", c["status"])
        self.assertIn("U01:NO_EVIDENCE_REFS", c["detail"])
        self.assertEqual("AT_RISK", self.health({"candidate_sha": SHA_B})["components"]["evidence"]["status"])  # the head moved
        self.assertEqual("UNOBSERVED", self.health(drop=("candidate_sha",))["components"]["evidence"]["status"])
        h = self.health(ledger=[], over={"pr_state": "MERGED"})  # work the ledger lacks
        self.assertEqual(("AT_RISK", "UNOBSERVED"), (h["components"]["materialization"]["status"], h["components"]["evidence"]["status"]))

    def test_with_nothing_ever_checkpointed_the_whole_branch_is_the_distance(self):
        h = self.health({"additions": 2422, "deletions": 0}, drop=("since_checkpoint",), ledger=[])
        self.assertEqual("AT_RISK", h["components"]["checkpoint_distance"]["status"])
        self.assertIn("2422 lines authored", h["components"]["checkpoint_distance"]["detail"])
        h = self.health({"additions": 2422, "deletions": 0}, drop=("since_checkpoint",))  # facts exist, so the distance is unknown, not the total
        self.assertEqual("UNOBSERVED", h["components"]["checkpoint_distance"]["status"])

    def test_only_started_unfinished_leaves_are_assessed(self):
        done = [entry(facts(leaf="Common#612", pr="Common#613", units=[unit("W1")], result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 2)]
        nodes = M.project(with_health(), STARTED + done, {"Common#592": FULL_OBS, "Common#612": {"candidate_sha": SHA_A}})["nodes"]
        self.assertIn("health", nodes["Common#592"])
        self.assertNotIn("health", nodes["Common#594"])  # not started
        self.assertNotIn("health", nodes["Common#612"])  # complete
        self.assertNotIn("health", nodes["Common#610"])  # nothing started below it

    def test_ancestors_roll_up_the_worst_leaf_and_name_the_at_risk_ones(self):
        obs = {
            "Common#592": FULL_OBS,
            "Common#594": {"candidate_sha": SHA_A, "pr_state": "OPEN", "additions": 5000, "deletions": 0},  # unreported and far over budget
        }
        nodes = M.project(with_health(), STARTED, obs)["nodes"]
        phase = nodes["Common#588"]["health"]
        self.assertEqual(("AT_RISK", 2, {"HEALTHY": 1, "AT_RISK": 1}, ["Common#594"]), (phase["verdict"], phase["leaves"], phase["counts"], phase["at_risk"]))
        self.assertEqual(phase, nodes["Common#527"]["health"])

    def test_health_never_moves_a_number_a_state_a_title_or_an_admission_answer(self):
        bad = {**FULL_OBS, "behind_by": 99, "additions": 5000, "liveness": "STALE"}
        off, on = M.project(graph(), STARTED, {"Common#592": bad}), M.project(with_health(), STARTED, {"Common#592": bad})
        strip = lambda nodes: {r: {k: v for k, v in n.items() if k != "health"} for r, n in nodes.items()}  # noqa: E731
        self.assertEqual(strip(off["nodes"]), strip(on["nodes"]))
        self.assertEqual("AT_RISK", on["nodes"]["Common#592"]["health"]["verdict"])
        self.assertEqual(M.admit(off, "Common#592")["action"], M.admit(on, "Common#592")["action"])
        title = on["nodes"]["Common#592"]["title_prefix"]
        self.assertNotIn("AT_RISK", title)
        self.assertNotIn("HEALTH", title)

    def test_the_policy_is_validated_and_merged_over_the_written_defaults(self):
        for label, policy in {
            "mode": {"mode": "ENFORCED"},
            "mode case": {"mode": "advisory"},
            "unknown key": {"surprise": 1},
            "watch above at-risk": {"checkpoint": {"watch_added_loc": 600}},
            "changed watch above at-risk": {"checkpoint": {"watch_changed_loc": 800}},
            "drift": {"drift": {"watch_behind": 30}},
            "interruptions": {"interruptions": {"watch": 4}},
            "unknown section key": {"checkpoint": {"extra": 1}},
            "section not a mapping": {"checkpoint": 5},
            "zero": {"drift": {"watch_behind": 0}},
        }.items():
            g = graph()
            g["programme"]["health_policy"] = policy
            with self.subTest(label), self.assertRaises(M.GraphError):
                M.validate_graph(g)
        g = graph()
        g["programme"]["health_policy"] = "ADVISORY"
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)
        merged = M.validate_graph(with_health(checkpoint={"at_risk_added_loc": 800}))["health_policy"]
        self.assertEqual({"watch_added_loc": 250, "at_risk_added_loc": 800, "watch_changed_loc": 400, "at_risk_changed_loc": 700}, merged["checkpoint"])
        self.assertEqual({"watch_behind": 1, "at_risk_behind": 20}, merged["drift"])

    def test_the_continue_checkpoint_carries_one_advisory_health_line(self):
        ok = M.render_checkpoint(M.admit(M.project(with_health(), STARTED, {"Common#592": FULL_OBS}), "Common#592"))
        self.assertIn("HEALTH: 🟢 HEALTHY (advisory)\n", ok + "\n")
        bad = M.render_checkpoint(M.admit(M.project(with_health(), STARTED, {"Common#592": {**FULL_OBS, "behind_by": 25, "liveness": "QUIET"}}), "Common#592"))
        self.assertIn("HEALTH: 🔴 AT_RISK (advisory) — base_drift (25 commit(s) behind the base); liveness (observed QUIET)", bad)

    def test_the_real_p3_i_timeline_crosses_the_written_ceilings_long_before_its_first_checkpoint(self):
        """Cumulative lines added by the nine real P3-I commits (provider log, 2026-10-06 UTC) against its first checkpoint comment."""
        from datetime import datetime, timedelta

        timeline = [
            ("23:01:10", 190),
            ("23:01:15", 282),
            ("23:01:19", 290),
            ("23:01:23", 504),
            ("23:05:00", 2232),
            ("23:08:53", 2233),
            ("23:09:24", 2330),
            ("23:09:44", 2357),
            ("23:10:21", 2424),
        ]
        g = with_health(g=RealScenarioReplay.plan())
        seen = []
        for _, added in timeline:
            obs = RealScenarioReplay.observations()
            obs["Common#588"].update({"additions": added, "deletions": 0})
            seen.append(M.project(g, [], obs)["nodes"]["Common#588"]["health"]["components"]["checkpoint_distance"]["status"])
        self.assertEqual(["OK", "WATCH", "WATCH", "AT_RISK"] + ["AT_RISK"] * 5, seen)
        first_at_risk = timeline[seen.index("AT_RISK")][0]
        wait = datetime.strptime("23:12:49", "%H:%M:%S") - datetime.strptime(first_at_risk, "%H:%M:%S")  # the first #588 checkpoint comment
        self.assertEqual(timedelta(minutes=11, seconds=26), wait)

    def test_the_p3_i_handover_state_reads_at_risk_and_names_every_unobserved_input(self):
        g = with_health(g=RealScenarioReplay.plan())
        obs = RealScenarioReplay.observations()
        obs["Common#588"].update({"additions": 2422, "deletions": 0})
        projection = M.project(g, RealScenarioReplay.closed_ledger(), obs)
        leaf = projection["nodes"]["Common#588"]["health"]
        self.assertEqual(
            {
                "materialization": "AT_RISK",
                "size": "AT_RISK",
                "checkpoint_distance": "AT_RISK",
                "base_drift": "WATCH",
                "evidence": "UNOBSERVED",
                "interruptions": "UNOBSERVED",
                "liveness": "UNOBSERVED",
            },
            self.statuses(leaf),
        )
        root = projection["nodes"]["Common#527"]["health"]
        self.assertEqual(("AT_RISK", 1, ["Common#588"]), (root["verdict"], root["leaves"], root["at_risk"]))
        for ref, *_ in RealScenarioReplay.SOLO:
            self.assertNotIn("health", projection["nodes"][ref])  # finished leaves are not assessed

    def test_command_line_health_is_advisory_and_always_exits_zero(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)

            def write(name, value):
                path = root / name
                path.write_text(json.dumps(value), encoding="utf-8")
                return str(path)

            obs = RealScenarioReplay.observations()
            obs["Common#588"].update({"additions": 2422, "deletions": 0})
            args = ("--graph", write("g.json", RealScenarioReplay.plan()), "--facts", write("f.json", RealScenarioReplay.closed_ledger()), "--observations", write("o.json", obs))
            code, out, _ = cli("health", *args)  # the plan sets no health policy: the command is explicit intent
            self.assertEqual(0, code)
            self.assertIn("AGENT HEALTH (advisory; observed or derived, never declared", out)
            self.assertIn("PROGRAMME: 🔴 AT_RISK — 1 started leaves (AT_RISK 1)", out)
            self.assertIn("🔴 AT_RISK    Common#588  checkpoint_distance (", out)
            code, out, _ = cli("health", *args, "--mode", "OFF")
            self.assertEqual(0, code)
            self.assertIn("(no started leaf to assess, or the health policy is OFF)", out)
            code, out, _ = cli("health", *args, "--json")
            self.assertEqual(0, code)
            report = json.loads(out)
            self.assertEqual(("AT_RISK", ["Common#588"]), (report["programme"]["verdict"], list(report["leaves"])))
            code, out, _ = cli("health", *args, "--leaf", "Common#584")  # a completed leaf has nothing to assess
            self.assertEqual(0, code)
            self.assertIn("(no started leaf to assess", out)


@unittest.skipUnless(HAVE_YAML and HAVE_JSONSCHEMA, "PyYAML/jsonschema unavailable")
class HealthSchemasAgreeWithTheEngine(unittest.TestCase):
    schema = SchemasAgreeWithTheEngine.schema
    schema_errors = SchemasAgreeWithTheEngine.schema_errors

    def test_the_health_policy_is_validated_by_both(self):
        g = with_health(checkpoint={"at_risk_added_loc": 800}, drift={"watch_behind": 2}, interruptions={"at_risk": 5})
        self.assertEqual([], self.schema_errors("execution-graph", g))
        M.validate_graph(g)
        for label, policy in {
            "mode": {"mode": "ENFORCED"},
            "unknown key": {"surprise": 1},
            "unknown section key": {"checkpoint": {"extra": 1}},
            "zero": {"drift": {"watch_behind": 0}},
        }.items():
            bad = graph()
            bad["programme"]["health_policy"] = policy
            with self.subTest(label):
                self.assertTrue(self.schema_errors("execution-graph", bad), "schema accepted it")
                with self.assertRaises(M.GraphError):
                    M.validate_graph(bad)

    def test_a_projection_with_health_satisfies_the_live_status_schema(self):
        obs = RealScenarioReplay.observations()
        obs["Common#588"].update({"additions": 2422, "deletions": 0, "interruptions": {"coverage_from": "2026-10-06T22:51:06Z", "losses": [{"kind": "STREAM"}] * 3}})
        projection = M.project(with_health(g=RealScenarioReplay.plan()), RealScenarioReplay.closed_ledger(), obs)
        for ref, node in projection["nodes"].items():
            document = M.status_document(node, version=1, digest=projection["input_digest"], programme=projection["programme"])
            with self.subTest(ref=ref):
                self.assertEqual([], self.schema_errors("live-status", json.loads(M.canonical_json(document))))
        self.assertIn("health", projection["nodes"]["Common#588"])


@unittest.skipUnless(HAVE_YAML and HAVE_JSONSCHEMA, "PyYAML/jsonschema unavailable")
class MaterializationSchemasAgreeWithTheEngine(unittest.TestCase):
    schema = SchemasAgreeWithTheEngine.schema
    schema_errors = SchemasAgreeWithTheEngine.schema_errors

    def test_an_unmaterialized_projection_satisfies_the_live_status_schema(self):
        projection = M.project(RealScenarioReplay.plan(), [], RealScenarioReplay.observations())
        for ref, node in projection["nodes"].items():
            document = M.status_document(node, version=1, digest=projection["input_digest"], programme=projection["programme"])
            with self.subTest(ref=ref):
                self.assertEqual([], self.schema_errors("live-status", json.loads(M.canonical_json(document))))

    def test_the_base_ref_is_validated_by_both(self):
        for good in ("main", "release/2"):
            g = planned()
            g["programme"]["base_ref"] = good
            self.assertEqual([], self.schema_errors("execution-graph", g))
            M.validate_graph(g)
        for bad in (5, "", "  "):
            g = planned()
            g["programme"]["base_ref"] = bad
            with self.subTest(bad=bad), self.assertRaises(M.GraphError):
                M.validate_graph(g)
        g = planned()
        g["programme"]["base_ref"] = 5
        self.assertTrue(self.schema_errors("execution-graph", g))


if __name__ == "__main__":
    unittest.main()
