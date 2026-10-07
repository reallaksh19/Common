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
import subprocess
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "delp_projection_v35.py"
spec = importlib.util.spec_from_file_location("delp_projection_v35", MODULE_PATH)
M = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(M)

DECOMPOSITION_MODULE_PATH = MODULE_PATH.parents[1] / "scripts" / "decomposition_classifier_v35.py"
decomposition_spec = importlib.util.spec_from_file_location("decomposition_classifier_v35", DECOMPOSITION_MODULE_PATH)
D = importlib.util.module_from_spec(decomposition_spec)
assert decomposition_spec.loader
decomposition_spec.loader.exec_module(D)

OBSERVER_MODULE_PATH = MODULE_PATH.parents[1] / "scripts" / "decomposition_observer_v35.py"
observer_spec = importlib.util.spec_from_file_location("decomposition_observer_v35", OBSERVER_MODULE_PATH)
O = importlib.util.module_from_spec(observer_spec)
assert observer_spec.loader
observer_spec.loader.exec_module(O)

ASSEMBLER_MODULE_PATH = MODULE_PATH.parents[1] / "scripts" / "decomposition_assembler_v35.py"
assembler_spec = importlib.util.spec_from_file_location("decomposition_assembler_v35", ASSEMBLER_MODULE_PATH)
A = importlib.util.module_from_spec(assembler_spec)
assert assembler_spec.loader
assembler_spec.loader.exec_module(A)

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
        if node["kind"] == "LEAF":
            if not node.get("responsibility_id"):
                node["responsibility_id"] = f"RESP-{M.ref_number(node['ref'])}"
            node["spec_generation"] = node.get("spec_generation", 1)
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


def bound_facts(g, **kwargs):
    return M.bind_facts_to_graph(g, facts(**kwargs))


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

    def test_execution_provenance_tuple_is_optional_but_strict_when_present(self):
        binding = {
            "ep": "EP-P3-B1",
            "lease": "LEASE-P3-B1",
            "executor": "agent-604-b1",
            "custody_epoch": 8,
        }
        self.assertEqual([], M.validate_facts(facts(units=[unit("U01")], execution=binding)))

        variants = []
        for key in binding:
            row = copy.deepcopy(binding)
            row.pop(key)
            variants.append(row)
        variants += [
            {**binding, "ep": "bad"},
            {**binding, "lease": "bad"},
            {**binding, "executor": "   "},
            {**binding, "custody_epoch": 0},
            {**binding, "custody_epoch": True},
            {**binding, "surprise": "x"},
        ]
        for row in variants:
            with self.subTest(row=row):
                self.assertTrue(M.validate_facts(facts(units=[unit("U01")], execution=row)))

    def test_execution_provenance_is_fact_metadata_not_progress_authority(self):
        base = M.project(graph(), [entry(facts(units=[unit("U01")]), 1)], OBS_A)
        bound = M.project(
            graph(),
            [
                entry(
                    facts(
                        units=[unit("U01")],
                        execution={
                            "ep": "EP-P3-B1",
                            "lease": "LEASE-P3-B1",
                            "executor": "agent-604-b1",
                            "custody_epoch": 8,
                        },
                    ),
                    1,
                )
            ],
            OBS_A,
        )
        self.assertEqual(
            base["nodes"]["Common#592"]["progress"],
            bound["nodes"]["Common#592"]["progress"],
        )
        self.assertEqual(
            base["nodes"]["Common#592"]["actual_next"],
            bound["nodes"]["Common#592"]["actual_next"],
        )

    def test_raw_epoch_remains_forbidden_projection_bookkeeping(self):
        self.assertTrue(M.validate_facts(facts(units=[unit("U01")], epoch=8)))


class ExecutionBindingFromExistingCustody(unittest.TestCase):
    def state(self, **updates):
        execution = {
            "lifecycle": "ACTIVE",
            "ep": "EP-P3-B1",
            "lease": "LEASE-P3-B1",
            "route": "SERIAL:EP-P3-B1",
            "custody_epoch": 8,
        }
        execution.update(updates)
        return {"execution": execution}

    def lease(self, **updates):
        value = {
            "id": "LEASE-P3-B1",
            "state": "ACTIVE",
            "executor": {"id": "agent-604-b1"},
            "basis": {"ep_id": "EP-P3-B1"},
            "custody": {"epoch": 8},
        }
        value.update(updates)
        return value

    def test_current_state_and_lease_stamp_exact_execution_tuple(self):
        record = facts(units=[unit("U01")])
        bound = M.bind_facts_to_execution(record, self.state(), self.lease())
        self.assertEqual(
            {
                "ep": "EP-P3-B1",
                "lease": "LEASE-P3-B1",
                "executor": "agent-604-b1",
                "custody_epoch": 8,
            },
            bound["execution"],
        )
        self.assertNotIn("execution", record)
        self.assertEqual([], M.validate_facts(bound))

    def test_identical_existing_binding_is_idempotent(self):
        record = facts(
            units=[unit("U01")],
            execution={
                "ep": "EP-P3-B1",
                "lease": "LEASE-P3-B1",
                "executor": "agent-604-b1",
                "custody_epoch": 8,
            },
        )
        self.assertEqual(record, M.bind_facts_to_execution(record, self.state(), self.lease()))

    def test_conflicting_existing_binding_is_never_repaired_silently(self):
        record = facts(
            units=[unit("U01")],
            execution={
                "ep": "EP-P3-B1",
                "lease": "LEASE-P3-B1",
                "executor": "agent-old",
                "custody_epoch": 7,
            },
        )
        with self.assertRaises(M.DelpError):
            M.bind_facts_to_execution(record, self.state(), self.lease())

    def test_state_lease_disagreement_fails_closed(self):
        variants = [
            (self.state(lifecycle="IDLE"), self.lease()),
            (self.state(lease="LEASE-OTHER"), self.lease()),
            (self.state(ep="EP-OTHER"), self.lease()),
            (self.state(custody_epoch=9), self.lease()),
            (self.state(), self.lease(state="RELEASED")),
            (self.state(), self.lease(id="LEASE-OTHER")),
            (self.state(), self.lease(basis={"ep_id": "EP-OTHER"})),
            (self.state(), self.lease(custody={"epoch": 9})),
            (self.state(), self.lease(executor={"id": "   "})),
        ]
        for state, lease in variants:
            with self.subTest(state=state, lease=lease):
                with self.assertRaises(M.DelpError):
                    M.execution_binding_from_state_lease(state, lease)

    def test_stamping_does_not_create_a_currentness_or_progress_decision(self):
        record = facts(units=[unit("U01")])
        stamped = M.bind_facts_to_execution(record, self.state(), self.lease())
        node = M.project(graph(), [entry(stamped, 1)], OBS_A)["nodes"]["Common#592"]
        legacy = M.project(graph(), [entry(record, 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual(legacy["progress"], node["progress"])
        self.assertEqual(legacy["actual_next"], node["actual_next"])


class ExecutionProvenanceVisibility(unittest.TestCase):
    BINDING = {
        "ep": "EP-P3-B1",
        "lease": "LEASE-P3-B1",
        "executor": "agent-604-b1",
        "custody_epoch": 8,
    }

    def bound_fact(self, units, **updates):
        binding = dict(self.BINDING)
        binding.update(updates)
        return facts(units=units, execution=binding)

    def test_bound_facts_are_visible_and_identical_bindings_coalesce(self):
        ledger = [
            entry(self.bound_fact([unit("U01")]), 1, "fact-z"),
            entry(self.bound_fact([unit("U02")]), 2, "fact-a"),
        ]
        node = M.project(graph(), ledger, OBS_A)["nodes"]["Common#592"]
        self.assertEqual(
            {
                "bound_fact_count": 2,
                "unbound_fact_count": 0,
                "bindings": [
                    {
                        **self.BINDING,
                        "source_refs": ["fact-a", "fact-z"],
                    }
                ],
            },
            node["execution_provenance"],
        )

    def test_legacy_unbound_facts_remain_visible_not_rejected(self):
        ledger = [
            entry(facts(units=[unit("U01")]), 1, "legacy"),
            entry(self.bound_fact([unit("U02")]), 2, "bound"),
        ]
        projection = M.project(graph(), ledger, OBS_A)
        node = projection["nodes"]["Common#592"]
        self.assertEqual(1, node["execution_provenance"]["bound_fact_count"])
        self.assertEqual(1, node["execution_provenance"]["unbound_fact_count"])
        self.assertEqual([], projection["rejected_facts"])

    def test_provenance_order_is_deterministic_and_carries_no_currentness_verdict(self):
        older = self.bound_fact([unit("U01")], custody_epoch=7, executor="agent-old")
        newer = self.bound_fact([unit("U02")], custody_epoch=8, executor="agent-new")
        first = M.project(
            graph(),
            [entry(newer, 2, "new"), entry(older, 1, "old")],
            OBS_A,
        )["nodes"]["Common#592"]["execution_provenance"]
        second = M.project(
            graph(),
            [entry(older, 1, "old"), entry(newer, 2, "new")],
            OBS_A,
        )["nodes"]["Common#592"]["execution_provenance"]
        self.assertEqual(first, second)
        self.assertEqual([7, 8], [row["custody_epoch"] for row in first["bindings"]])
        self.assertTrue(
            all(
                "status" not in row and "current" not in row and "stale" not in row
                for row in first["bindings"]
            )
        )

    def test_execution_provenance_changes_no_semantic_or_decision_projection(self):
        raw = [entry(facts(units=[unit("U01"), unit("U02")]), 1, "fact")]
        bound = [entry(self.bound_fact([unit("U01"), unit("U02")]), 1, "fact")]
        legacy_node = M.project(graph(), raw, OBS_A)["nodes"]["Common#592"]
        bound_projection = M.project(graph(), bound, OBS_A)
        bound_node = bound_projection["nodes"]["Common#592"]
        for field in ("progress", "state", "lifecycle", "conditions", "actual_next", "title_prefix"):
            with self.subTest(field=field):
                self.assertEqual(legacy_node[field], bound_node[field])

        document = M.status_document(
            bound_node,
            version=1,
            digest=bound_projection["input_digest"],
            programme=bound_projection["programme"],
        )
        self.assertEqual(bound_node["execution_provenance"], document["node"]["execution_provenance"])
        self.assertNotIn(
            "execution_provenance",
            bound_projection["nodes"]["Common#588"],
        )



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
        self.assertEqual("🟡 [#527 › #588 › #592 → PR#593] R:P75/E50 · U04 · EVIDENCE_GAP · NEXT:RECOVER_EVIDENCE", node["title_prefix"])

    def test_recovery_evidence_restores_E(self):
        ledger = [
            entry(facts(units=[unit("U01"), unit("U02")]), 1),
            entry(facts(units=[unit("U03", refs=())]), 2),
            entry(facts(units=[unit("U03", refs=("Common#592#issuecomment-9",))]), 3),
        ]
        node = self.leaf(ledger)
        self.assertEqual((75, 75), (node["progress"]["P"], node["progress"]["E"]))
        self.assertEqual("ACTIVE", node["state"])
        self.assertEqual("🟢 [#527 › #588 › #592 → PR#593] R:P75/E75 · U04 · ACTIVE · NEXT:CONTINUE_UNIT", node["title_prefix"])

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
        self.assertEqual("⚪ [#527 › #588 › #592 → PR#593] R:P0/E0 · U01 · NOT_STARTED · NEXT:CONTINUE_UNIT", node["title_prefix"])


class CompletionAndDelivery(unittest.TestCase):
    ALL = [unit("U01"), unit("U02"), unit("U03"), unit("U04")]

    def test_complete_requires_result_units_current_evidence(self):
        done = entry(facts(units=self.ALL, result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 1)
        node = M.project(graph(), [done], OBS_A)["nodes"]["Common#592"]
        self.assertEqual("COMPLETE", node["lifecycle"])
        self.assertEqual("✅ [#527 › #588 › #592 → PR#593] R:P100/E100 · COMPLETE · NEXT:NONE", node["title_prefix"])

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
    def test_leaf_title_exposes_only_canonical_actual_next_action(self):
        first = M.project(
            graph(),
            [entry(facts(units=[unit("U01")], next={"unit": "U02", "action": "executor prose A"}), 1)],
            OBS_A,
        )["nodes"]["Common#592"]
        second = M.project(
            graph(),
            [entry(facts(units=[unit("U01")], next={"unit": "U02", "action": "executor prose B"}), 1)],
            OBS_A,
        )["nodes"]["Common#592"]
        self.assertEqual("CONTINUE_UNIT", first["actual_next"]["action"])
        self.assertIn("NEXT:CONTINUE_UNIT", first["title_prefix"])
        self.assertEqual(first["title_prefix"], second["title_prefix"])
        self.assertNotIn("executor prose", first["title_prefix"])

    def test_leaf_title_tracks_canonical_action_but_group_titles_do_not(self):
        g = broken(ref="Common#592")
        projection = M.project(g, [], OBS_A)
        leaf = projection["nodes"]["Common#592"]
        parent = projection["nodes"]["Common#588"]
        root = projection["nodes"]["Common#527"]
        self.assertEqual("FIX_PLAN", leaf["actual_next"]["action"])
        self.assertIn("NEXT:FIX_PLAN", leaf["title_prefix"])
        self.assertNotIn("NEXT:", parent["title_prefix"])
        self.assertNotIn("NEXT:", root["title_prefix"])

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
        self.assertEqual(proj["nodes"]["Common#592"]["actual_next"], report["actual_next"])
        self.assertEqual(report["actual_next"]["action"], report["action"])
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

    def test_matching_asserted_contract_digest_does_not_change_stable_graph_digest(self):
        without_assertion = stable_graph()
        derived = M.validate_graph(without_assertion)["nodes"]["Common#592"]["contract_digest"]
        with_assertion = copy.deepcopy(without_assertion)
        next(n for n in with_assertion["nodes"] if n["ref"] == "Common#592")["contract_digest"] = derived
        self.assertEqual(
            M.validate_graph(without_assertion)["digest"],
            M.validate_graph(with_assertion)["digest"],
        )

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


    def test_stable_identity_requires_positive_spec_generation(self):
        g = stable_graph()
        g["nodes"][4].pop("spec_generation")
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)
        for value in (0, True):
            g = stable_graph()
            g["nodes"][4]["spec_generation"] = value
            with self.assertRaises(M.GraphError):
                M.validate_graph(g)

    def test_contract_digest_is_derived_and_exposed(self):
        g = stable_graph()
        indexed = M.validate_graph(g)
        leaf = indexed["nodes"]["Common#592"]
        self.assertTrue(leaf["contract_digest"].startswith("sha256:"))
        public = M.project(g, [], OBS_A)["nodes"]["Common#592"]["identity"]
        self.assertEqual(1, public["spec_generation"])
        self.assertEqual(leaf["contract_digest"], public["contract_digest"])

    def test_spec_generation_itself_does_not_change_contract_digest(self):
        g1 = stable_graph()
        g2 = copy.deepcopy(g1)
        next(n for n in g2["nodes"] if n["ref"] == "Common#592")["spec_generation"] = 2
        d1 = M.validate_graph(g1)["nodes"]["Common#592"]["contract_digest"]
        d2 = M.validate_graph(g2)["nodes"]["Common#592"]["contract_digest"]
        self.assertEqual(d1, d2)

    def test_provider_topology_and_weights_do_not_change_contract_digest(self):
        g1 = stable_graph()
        g2 = copy.deepcopy(g1)
        leaf = next(n for n in g2["nodes"] if n["ref"] == "Common#592")
        leaf["parent"] = "Common#610"
        leaf["weight"] = 9
        leaf["primary_pr"] = "Common#999"
        d1 = M.validate_graph(g1)["nodes"]["Common#592"]["contract_digest"]
        d2 = M.validate_graph(g2)["nodes"]["Common#592"]["contract_digest"]
        self.assertEqual(d1, d2)

    def test_semantic_contract_fields_change_the_digest(self):
        base = stable_graph()
        original = M.validate_graph(base)["nodes"]["Common#592"]["contract_digest"]
        mutations = [
            lambda g: next(n for n in g["nodes"] if n["ref"] == "Common#592").__setitem__("outcome", "new observable outcome"),
            lambda g: next(n for n in g["nodes"] if n["ref"] == "Common#592")["units"][0].__setitem__("verify", "run exact replay"),
            lambda g: next(n for n in g["nodes"] if n["ref"] == "Common#592").__setitem__("write_surface", ["src/kernel.py"]),
            lambda g: next(n for n in g["nodes"] if n["ref"] == "Common#592").__setitem__(
                "size_budget", {"target_loc": 50, "hard_loc": 100, "target_minutes": 5, "hard_minutes": 10}
            ),
            lambda g: next(n for n in g["nodes"] if n["ref"] == "Common#592").__setitem__("work_class", "MECHANICAL"),
            lambda g: next(n for n in g["nodes"] if n["ref"] == "Common#592").__setitem__("verification", ["VERIFIED", "PARTIAL"]),
            lambda g: next(n for n in g["nodes"] if n["ref"] == "Common#592").__setitem__("depends_on", ["Common#594"]),
        ]
        for mutate in mutations:
            g = copy.deepcopy(base)
            mutate(g)
            with self.subTest(graph=g):
                current = M.validate_graph(g)["nodes"]["Common#592"]["contract_digest"]
                self.assertNotEqual(original, current)

    def test_asserted_contract_digest_cannot_override_derived_digest(self):
        g = stable_graph()
        next(n for n in g["nodes"] if n["ref"] == "Common#592")["contract_digest"] = DIGEST
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)

    def test_graph_diff_requires_generation_bump_for_semantic_contract_change(self):
        old = stable_graph()
        new = copy.deepcopy(old)
        next(n for n in new["nodes"] if n["ref"] == "Common#592")["outcome"] = "changed contract"
        blocked = M.graph_diff(old, new)
        self.assertFalse(blocked["conserved"])
        self.assertIn("SPEC_GENERATION_NOT_BUMPED", {f["code"] for f in blocked["findings"]})
        next(n for n in new["nodes"] if n["ref"] == "Common#592")["spec_generation"] = 2
        accepted = M.graph_diff(old, new)
        self.assertTrue(accepted["conserved"], accepted["findings"])

    def test_generation_bump_without_contract_change_is_advisory_only(self):
        old = stable_graph()
        new = copy.deepcopy(old)
        next(n for n in new["nodes"] if n["ref"] == "Common#592")["spec_generation"] = 2
        report = M.graph_diff(old, new)
        self.assertTrue(report["conserved"])
        finding = next(f for f in report["findings"] if f["code"] == "SPEC_GENERATION_BUMP_WITHOUT_CONTRACT_CHANGE")
        self.assertEqual("ADVISORY", finding["severity"])



class ResponsibilityContractBinding(unittest.TestCase):
    def test_stable_identity_facts_require_exact_binding(self):
        g = stable_graph()
        raw = facts(units=[unit("U01")])
        rejected = M.project(g, [entry(raw, 1)], OBS_A)
        self.assertEqual(0, rejected["nodes"]["Common#592"]["progress"]["P"])
        reasons = rejected["rejected_facts"][0]["reasons"]
        self.assertTrue(any("responsibility.id" in reason for reason in reasons))
        self.assertTrue(any("responsibility.spec_generation" in reason for reason in reasons))
        self.assertTrue(any("responsibility.contract_digest" in reason for reason in reasons))

        bound = bound_facts(g, units=[unit("U01")])
        accepted = M.project(g, [entry(bound, 1)], OBS_A)
        self.assertEqual((20, 20), (
            accepted["nodes"]["Common#592"]["progress"]["P"],
            accepted["nodes"]["Common#592"]["progress"]["E"],
        ))
        self.assertEqual([], accepted["rejected_facts"])

    def test_old_contract_fact_is_rejected_after_semantic_change(self):
        old = stable_graph()
        old_fact = bound_facts(old, units=[unit("U01")])
        new = copy.deepcopy(old)
        leaf = next(n for n in new["nodes"] if n["ref"] == "Common#592")
        leaf["outcome"] = "new contract"
        leaf["spec_generation"] = 2
        out = M.project(new, [entry(old_fact, 1)], OBS_A)
        self.assertEqual(0, out["nodes"]["Common#592"]["progress"]["P"])
        reasons = out["rejected_facts"][0]["reasons"]
        self.assertTrue(any("spec_generation" in reason for reason in reasons))
        self.assertTrue(any("contract_digest" in reason for reason in reasons))

    def test_bind_facts_refuses_conflicting_existing_binding(self):
        g = stable_graph()
        record = facts(units=[unit("U01")])
        record["responsibility"]["id"] = "WRONG"
        with self.assertRaises(M.DelpError):
            M.bind_facts_to_graph(g, record)

    def test_wrong_repository_same_issue_number_is_not_bound_or_admitted(self):
        g = stable_graph()
        raw = facts(units=[unit("U01")])
        raw["responsibility"]["issue"] = "other/repo#592"
        with self.assertRaises(M.DelpError):
            M.bind_facts_to_graph(g, raw)
        out = M.project(g, [entry(raw, 1)], OBS_A)
        self.assertEqual(0, out["nodes"]["Common#592"]["progress"]["P"])
        self.assertIn("not a declared LEAF", out["rejected_facts"][0]["reasons"][0])

    def test_legacy_locator_only_fact_remains_admissible(self):
        out = M.project(graph(), [entry(facts(units=[unit("U01")]), 1)], OBS_A)
        self.assertEqual(20, out["nodes"]["Common#592"]["progress"]["P"])
        self.assertEqual([], out["rejected_facts"])


class ResponsibilityCurrentnessProjection(unittest.TestCase):
    def test_stable_projection_exposes_currentness_on_every_node(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01")])
        out = M.project(g, [entry(record, 1)], OBS_A)
        self.assertEqual(out["graph_digest"], out["nodes"]["Common#527"]["currentness"]["graph_digest"])
        for ref, node in out["nodes"].items():
            with self.subTest(ref=ref):
                current = node["currentness"]
                self.assertEqual("STABLE", current["mode"])
                self.assertEqual(1, current["graph_generation"])
                self.assertEqual(out["graph_digest"], current["graph_digest"])
                if node["kind"] == "LEAF":
                    self.assertEqual(node["identity"]["spec_generation"], current["spec_generation"])
                    self.assertEqual(node["identity"]["contract_digest"], current["contract_digest"])
                    self.assertTrue(current["fact_binding_required"])
                else:
                    self.assertIsNone(current["spec_generation"])
                    self.assertIsNone(current["contract_digest"])
                    self.assertFalse(current["fact_binding_required"])

    def test_legacy_projection_exposes_legacy_currentness_without_changing_progress(self):
        ledger = [entry(facts(units=[unit("U01")]), 1)]
        out = M.project(graph(), ledger, OBS_A)
        leaf = out["nodes"]["Common#592"]
        self.assertEqual((20, 20), (leaf["progress"]["P"], leaf["progress"]["E"]))
        self.assertEqual(
            {
                "mode": "LEGACY",
                "graph_generation": 1,
                "graph_digest": out["graph_digest"],
                "spec_generation": None,
                "contract_digest": None,
                "fact_binding_required": False,
            },
            leaf["currentness"],
        )

    def test_old_generation_fact_on_new_semantic_contract_is_rejected_and_currentness_moves(self):
        old = stable_graph()
        record = bound_facts(old, units=[unit("U01")])
        old_digest = M.validate_graph(old)["nodes"]["Common#592"]["contract_digest"]
        new = copy.deepcopy(old)
        leaf = next(n for n in new["nodes"] if n["ref"] == "Common#592")
        leaf["outcome"] = "changed semantic contract"
        leaf["spec_generation"] = 2
        out = M.project(new, [entry(record, 1)], OBS_A)
        projected = out["nodes"]["Common#592"]
        self.assertEqual((0, 0), (projected["progress"]["P"], projected["progress"]["E"]))
        self.assertEqual(2, projected["currentness"]["spec_generation"])
        self.assertNotEqual(old_digest, projected["currentness"]["contract_digest"])
        reasons = out["rejected_facts"][0]["reasons"]
        self.assertTrue(any("spec_generation" in reason for reason in reasons))
        self.assertTrue(any("contract_digest" in reason for reason in reasons))

    def test_correct_candidate_with_wrong_contract_digest_is_rejected(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01")])
        planned = M.validate_graph(g)["nodes"]["Common#592"]["contract_digest"]
        wrong = "sha256:" + ("0" * 64 if planned != "sha256:" + "0" * 64 else "1" * 64)
        record["responsibility"]["contract_digest"] = wrong
        out = M.project(g, [entry(record, 1)], OBS_A)
        leaf = out["nodes"]["Common#592"]
        self.assertEqual((0, 0), (leaf["progress"]["P"], leaf["progress"]["E"]))
        self.assertEqual(planned, leaf["currentness"]["contract_digest"])
        self.assertTrue(any("contract_digest" in r for r in out["rejected_facts"][0]["reasons"]))

    def test_candidate_move_with_current_contract_keeps_P_and_drops_E(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01")])
        before = M.project(g, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]
        moved_obs = copy.deepcopy(OBS_A)
        moved_obs["Common#592"]["candidate_sha"] = SHA_B
        after = M.project(g, [entry(record, 1)], moved_obs)["nodes"]["Common#592"]
        self.assertEqual((20, 20), (before["progress"]["P"], before["progress"]["E"]))
        self.assertEqual((20, 0), (after["progress"]["P"], after["progress"]["E"]))
        self.assertEqual(before["currentness"], after["currentness"])
        self.assertEqual("CANDIDATE_MISMATCH", after["evidence"]["gaps"][0]["reason"])

    def test_reparent_and_reweight_preserve_leaf_contract_and_leaf_progress(self):
        old = stable_graph()
        record = bound_facts(old, units=[unit("U01")])
        before = M.project(old, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]
        moved = copy.deepcopy(old)
        leaf = next(n for n in moved["nodes"] if n["ref"] == "Common#592")
        leaf["parent"] = "Common#610"
        leaf["weight"] = 9
        after = M.project(moved, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual(before["identity"]["contract_digest"], after["identity"]["contract_digest"])
        self.assertEqual(before["currentness"]["contract_digest"], after["currentness"]["contract_digest"])
        self.assertEqual(before["progress"], after["progress"])
        self.assertNotEqual(before["currentness"]["graph_digest"], after["currentness"]["graph_digest"])

    def test_editorial_title_change_does_not_mutate_projection_or_currentness(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01")])
        out = M.project(g, [entry(record, 1)], OBS_A)
        snapshot = copy.deepcopy(out["nodes"]["Common#592"])
        before = M.expected_titles(out, {"Common#592": "Before editorial title"})["Common#592"]
        after = M.expected_titles(out, {"Common#592": "After editorial title"})["Common#592"]
        self.assertNotEqual(before, after)
        self.assertEqual(snapshot, out["nodes"]["Common#592"])

    def test_unknown_unit_moves_no_progress_and_currentness_stays_derived(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("NOPE")])
        out = M.project(g, [entry(record, 1)], OBS_A)
        leaf = out["nodes"]["Common#592"]
        self.assertEqual((0, 0), (leaf["progress"]["P"], leaf["progress"]["E"]))
        self.assertIn("UNKNOWN_UNIT:NOPE", leaf["warnings"])
        self.assertEqual("STABLE", leaf["currentness"]["mode"])
        self.assertTrue(leaf["currentness"]["fact_binding_required"])

    def test_agent_cannot_author_currentness_projection_fields(self):
        forbidden = [
            {"currentness": {"mode": "STABLE"}},
            {"graph_generation": 99},
            {"graph_digest": "sha256:" + "1" * 64},
            {"observed_generation": 99},
            {"contract_current": True},
            {"observation": {"visibility": "OBSERVED"}},
            {"observations": {"Common#592": {"candidate_sha": SHA_A}}},
            {"provider_observation": {"candidate_sha": SHA_A}},
            {"provider_visibility": "OBSERVED"},
        ]
        for extra in forbidden:
            with self.subTest(extra=extra):
                record = facts(units=[unit("U01")], **extra)
                self.assertTrue(M.validate_facts(record))
                with self.assertRaises(M.ForbiddenProjectionField):
                    M.require_facts(record)


    def test_claim_semantics_bind_the_existing_contract_currentness_chain(self):
        old = stable_claim_topology_graph()
        old_indexed = M.validate_graph(old)
        old_digest = old_indexed["nodes"]["Common#592"]["contract_digest"]
        record = bound_facts(old, units=[unit("U01")])

        changed = copy.deepcopy(old)
        changed["programme"]["acceptance_claims"][0]["claim"] = "the changed semantic product outcome exists"
        leaf = leaf_of(changed, "Common#592")
        leaf["spec_generation"] = 2

        changed_indexed = M.validate_graph(changed)
        self.assertNotEqual(old_digest, changed_indexed["nodes"]["Common#592"]["contract_digest"])

        projected = M.project(changed, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual((0, 0), (projected["progress"]["P"], projected["progress"]["E"]))
        self.assertNotEqual(old_digest, projected["currentness"]["contract_digest"])

    def test_unrelated_parent_claim_edit_does_not_stale_unrelated_leaf_contract(self):
        g = stable_claim_topology_graph()
        before = M.validate_graph(g)["nodes"]["Common#592"]["contract_digest"]

        changed = copy.deepcopy(g)
        gate_claim = next(c for c in changed["programme"]["acceptance_claims"] if c["id"] == "PC-GATE")
        gate_claim["claim"] = "the changed delivery gate passes"
        after = M.validate_graph(changed)["nodes"]["Common#592"]["contract_digest"]

        self.assertEqual(before, after)

    def test_changing_claim_relationship_changes_leaf_contract_digest(self):
        g = stable_claim_topology_graph()
        before = M.validate_graph(g)["nodes"]["Common#592"]["contract_digest"]

        changed = copy.deepcopy(g)
        relation = next(
            r for r in leaf_of(changed, "Common#592")["claim_relationships"]
            if r["claim_id"] == "PC-PRODUCT"
        )
        relation["relation"] = "ENABLES"
        after = M.validate_graph(changed)["nodes"]["Common#592"]["contract_digest"]

        self.assertNotEqual(before, after)

    def test_claim_topology_does_not_break_reparent_reweight_conservation(self):
        old = stable_claim_topology_graph()
        record = bound_facts(old, units=[unit("U01")])
        before = M.project(old, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]

        moved = copy.deepcopy(old)
        leaf = leaf_of(moved, "Common#592")
        leaf["parent"] = "Common#610"
        leaf["weight"] = 9
        after = M.project(moved, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]

        self.assertEqual(before["identity"]["contract_digest"], after["identity"]["contract_digest"])
        self.assertEqual(before["progress"], after["progress"])
        self.assertNotEqual(before["currentness"]["graph_digest"], after["currentness"]["graph_digest"])


class ProviderObservationNormalization(unittest.TestCase):
    def test_typed_and_legacy_equivalent_truth_project_the_same_nodes(self):
        legacy = {
            "candidate_sha": SHA_A,
            "base_sha": SHA_MAIN,
            "pr_state": "OPEN",
            "ahead_by": 2,
            "behind_by": 1,
            "interruptions": {"coverage_from": "2026-10-07T00:00:00Z", "losses": []},
            "liveness": "ACTIVE",
            "check": {"name": "optional", "result": "SUCCESS", "candidate_sha": SHA_A},
            "additions": 10,
            "deletions": 2,
            "since_checkpoint": {"additions": 3, "deletions": 1},
        }
        typed = {
            "schema": M.OBSERVATION_SCHEMA,
            "visibility": "OBSERVED",
            "material": {
                "candidate_sha": SHA_A,
                "base_sha": SHA_MAIN,
                "pr_state": "OPEN",
                "ahead_by": 2,
                "behind_by": 1,
            },
            "custody": {"interruptions": {"coverage_from": "2026-10-07T00:00:00Z", "losses": []}},
            "liveness": {"value": "ACTIVE"},
            "check": {"name": "optional", "result": "SUCCESS", "candidate_sha": SHA_A},
            "diff": {
                "additions": 10,
                "deletions": 2,
                "since_checkpoint": {"additions": 3, "deletions": 1},
            },
        }
        ledger = [entry(facts(units=[unit("U01")]), 1)]
        left = M.project(graph(), ledger, {"Common#592": legacy})["nodes"]
        right = M.project(graph(), ledger, {"Common#592": typed})["nodes"]
        self.assertEqual(left, right)

    def test_missing_optional_categories_are_unobserved_not_failures(self):
        typed = {
            "schema": M.OBSERVATION_SCHEMA,
            "visibility": "OBSERVED",
            "material": {"candidate_sha": SHA_A},
        }
        normalized = M.normalize_observation(typed)
        self.assertEqual(
            {
                "MATERIAL": "OBSERVED",
                "CUSTODY": "UNOBSERVED",
                "LIVENESS": "UNOBSERVED",
                "CHECK": "UNOBSERVED",
                "DIFF": "UNOBSERVED",
            },
            normalized["_observation"]["categories"],
        )
        leaf = M.project(
            graph(),
            [entry(facts(units=[unit("U01")]), 1)],
            {"Common#592": typed},
        )["nodes"]["Common#592"]
        self.assertEqual((20, 20), (leaf["progress"]["P"], leaf["progress"]["E"]))
        self.assertEqual("ACTIVE", leaf["state"])

    def test_provider_unavailable_preserves_P_and_fabricates_no_failure(self):
        unavailable = {"schema": M.OBSERVATION_SCHEMA, "visibility": "UNAVAILABLE"}
        normalized = M.normalize_observation(unavailable)
        self.assertTrue(all(v == "UNAVAILABLE" for v in normalized["_observation"]["categories"].values()))
        leaf = M.project(
            graph(),
            [entry(facts(units=[unit("U01")]), 1)],
            {"Common#592": unavailable},
        )["nodes"]["Common#592"]
        self.assertEqual(20, leaf["progress"]["P"])
        self.assertEqual(0, leaf["progress"]["E"])
        self.assertEqual("UNVERIFIABLE", leaf["evidence"]["health"])
        self.assertEqual("EVIDENCE_GAP", leaf["state"])

    def test_optional_failed_check_is_observed_but_not_a_universal_gate(self):
        base = {
            "schema": M.OBSERVATION_SCHEMA,
            "visibility": "OBSERVED",
            "material": {"candidate_sha": SHA_A},
        }
        failed = copy.deepcopy(base)
        failed["check"] = {"name": "optional", "result": "FAILURE", "candidate_sha": SHA_A}
        ledger = [entry(facts(units=[unit("U01")]), 1)]
        without = M.project(graph(), ledger, {"Common#592": base})["nodes"]["Common#592"]
        with_failed = M.project(graph(), ledger, {"Common#592": failed})["nodes"]["Common#592"]
        self.assertEqual(without, with_failed)
        self.assertEqual("OBSERVED", M.normalize_observation(failed)["_observation"]["categories"]["CHECK"])

    def test_legacy_flat_input_gets_category_currentness_without_semantic_change(self):
        normalized = M.normalize_observation({"candidate_sha": SHA_A, "liveness": "ACTIVE"})
        self.assertEqual("LEGACY_FLAT_OBSERVATION", normalized["_observation"]["schema"])
        self.assertEqual("OBSERVED", normalized["_observation"]["categories"]["MATERIAL"])
        self.assertEqual("OBSERVED", normalized["_observation"]["categories"]["LIVENESS"])
        self.assertEqual("UNOBSERVED", normalized["_observation"]["categories"]["CHECK"])
        self.assertEqual("UNOBSERVED", normalized["_observation"]["categories"]["DIFF"])

    def test_typed_shaped_observation_without_schema_fails_closed(self):
        for record in (
            {"visibility": "OBSERVED", "material": {"candidate_sha": SHA_A}},
            {"material": {"candidate_sha": SHA_A}},
            {"custody": {"interruptions": {}}},
            {"diff": {"additions": 1}},
            {"liveness": {"value": "ACTIVE"}},
            {"schema": None, "visibility": "OBSERVED"},
        ):
            with self.subTest(record=record), self.assertRaises(M.DelpError):
                M.project(graph(), [], {"Common#592": record})

    def test_wrong_repository_same_number_observation_fails_closed(self):
        with self.assertRaises(M.DelpError):
            M.project(graph(), [], {"other/repo#592": {"candidate_sha": SHA_A}})

    def test_declared_repository_rejects_same_repo_name_from_other_owner(self):
        g = graph()
        g["programme"]["repository"] = "reallaksh19/Common"
        with self.assertRaises(M.DelpError):
            M.project(g, [], {"other/Common#592": {"candidate_sha": SHA_A}})
        accepted = M.project(g, [], {"reallaksh19/Common#592": {"candidate_sha": SHA_A}})
        self.assertEqual(SHA_A, accepted["nodes"]["Common#592"]["material"]["candidate_sha"])

    def test_repo_name_only_locator_remains_graph_local_for_offline_examples(self):
        g = graph()
        g["programme"]["repository"] = "example/delp-demo"
        accepted = M.project(g, [], {"Common#592": {"candidate_sha": SHA_A}})
        self.assertEqual(SHA_A, accepted["nodes"]["Common#592"]["material"]["candidate_sha"])

    def test_unknown_observation_locator_fails_closed(self):
        with self.assertRaises(M.DelpError):
            M.project(graph(), [], {"Common#999": {"candidate_sha": SHA_A}})

    def test_duplicate_aliases_for_one_leaf_fail_closed(self):
        with self.assertRaises(M.DelpError):
            M.project(
                graph(),
                [],
                {
                    "Common#592": {"candidate_sha": SHA_A},
                    592: {"candidate_sha": SHA_A},
                },
            )


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
        rows = []
        for comment in self.comments.get(number, []):
            row = dict(comment)
            row.setdefault("created_at", "2026-10-07T00:00:00Z")
            row.setdefault("updated_at", row["created_at"])
            rows.append(row)
        return rows

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
        self.assertEqual(M.OBSERVATION_SCHEMA, observed["Common#612"]["schema"])
        self.assertEqual("OBSERVED", observed["Common#612"]["visibility"])
        self.assertEqual(
            {"candidate_sha": SHA_C, "ahead_by": 9, "behind_by": 4, "base_sha": SHA_MAIN},
            observed["Common#612"]["material"],
        )
        self.assertEqual({"schema", "visibility", "material"}, set(observed["Common#612"]))
        self.assertEqual(SHA_MAIN, observed["Common#594"]["material"]["base_sha"])  # every leaf is measured against the same base head
        self.assertIn(("COMPARE", "main", "investigate/592"), gh.calls)  # the base defaults to main
        gh.commits["release/2"] = SHA_B
        g["programme"]["base_ref"] = "release/2"
        self.assertEqual(SHA_B, M.observe_github(gh, g)["Common#612"]["material"]["base_sha"])
        self.assertIn(("COMPARE", "release/2", "investigate/592"), gh.calls)
        self.assertEqual(SHA_C, observed["Common#612"]["material"]["candidate_sha"])
        self.assertEqual(SHA_B, observed["Common#594"]["material"]["candidate_sha"])
        self.assertEqual("MERGED", observed["Common#592"]["material"]["pr_state"])

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_fact_ledger_retains_provider_created_and_updated_time(self):
        gh = FakeGitHub()
        body = ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A)
        gh.comments[592] = [
            {
                "id": 5,
                "body": body,
                "author_association": "OWNER",
                "user": {"login": "reallaksh19"},
                "created_at": "2026-10-07T10:00:00Z",
                "updated_at": "2026-10-07T11:30:00+00:00",
            }
        ]
        ledger = M.ledger_from_github(gh, graph())
        self.assertEqual(1, len(ledger))
        self.assertEqual(
            {
                "kind": "GITHUB_ISSUE_COMMENT",
                "created_at": "2026-10-07T10:00:00Z",
                "updated_at": "2026-10-07T11:30:00Z",
            },
            ledger[0]["provider"],
        )

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_provider_comment_timestamp_is_provider_metadata_not_semantic_authority(self):
        gh = FakeGitHub()
        body = ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A)
        gh.comments[592] = [
            {
                "id": 5,
                "body": body,
                "author_association": "OWNER",
                "user": {"login": "reallaksh19"},
                "created_at": "2026-10-07T10:00:00Z",
                "updated_at": "2026-10-07T11:30:00Z",
            }
        ]
        ledger = M.ledger_from_github(gh, graph())
        stripped = [{key: value for key, value in row.items() if key != "provider"} for row in ledger]
        with_provider = M.project(graph(), ledger, OBS_A)["nodes"]["Common#592"]
        without_provider = M.project(graph(), stripped, OBS_A)["nodes"]["Common#592"]
        for field in ("progress", "state", "lifecycle", "conditions", "actual_next", "title_prefix"):
            with self.subTest(field=field):
                self.assertEqual(without_provider[field], with_provider[field])

    @unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
    def test_malformed_or_naive_provider_timestamp_fails_closed_for_facts_comment(self):
        body = ExtractFactsBlocks.BODY.replace("__SHA__", SHA_A)
        for created_at, updated_at in (
            ("not-a-time", "2026-10-07T11:00:00Z"),
            ("2026-10-07T10:00:00", "2026-10-07T11:00:00Z"),
            ("2026-10-07T12:00:00Z", "2026-10-07T11:00:00Z"),
        ):
            with self.subTest(created_at=created_at, updated_at=updated_at):
                gh = FakeGitHub()
                gh.comments[592] = [
                    {
                        "id": 5,
                        "body": body,
                        "author_association": "OWNER",
                        "user": {"login": "reallaksh19"},
                        "created_at": created_at,
                        "updated_at": updated_at,
                    }
                ]
                with self.assertRaises(M.DelpError):
                    M.ledger_from_github(gh, graph())

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
            (f"⚪ {P} R:P0/E0 · U01 · NOT_STARTED · NEXT:CONTINUE_UNIT", "⚪ [#527 › #588] Φ:D0/E0 · F0 · IDLE", "⚪ [#527] Π:D0/E0 · F0 · IDLE"),
            self.titles(ledger, {}),
        )
        ledger.append(entry(facts(units=[unit("U01"), unit("U02")], next={"unit": "U03", "action": "build replay lane"}), 1))
        self.assertEqual(
            (f"🟢 {P} R:P50/E50 · U03 · ACTIVE · NEXT:CONTINUE_UNIT", f"🟢 {Q} Φ:D38/E38 · F1 · ACTIVE", "🟢 [#527] Π:D28/E28 · F1 · ACTIVE"),
            self.titles(ledger, obs_a),
        )
        ledger.append(entry(facts(units=[unit("U03", refs=())]), 2))
        self.assertEqual(
            (f"🟡 {P} R:P75/E50 · U04 · EVIDENCE_GAP · NEXT:RECOVER_EVIDENCE", f"🟡 {Q} Φ:D56/E38 · F1 · EVIDENCE_GAP", "🟡 [#527] Π:D42/E28 · F1 · EVIDENCE_GAP"),
            self.titles(ledger, obs_a),
        )
        ledger.append(entry(facts(units=[unit("U03", refs=("Common#592#issuecomment-9",))]), 3))
        self.assertEqual(
            (f"🟢 {P} R:P75/E75 · U04 · ACTIVE · NEXT:CONTINUE_UNIT", f"🟢 {Q} Φ:D56/E56 · F1 · ACTIVE", "🟢 [#527] Π:D42/E42 · F1 · ACTIVE"),
            self.titles(ledger, obs_a),
        )
        self.assertEqual(
            (f"🟡 {P} R:P75/E0 · U04 · EVIDENCE_STALE · NEXT:RECOVER_EVIDENCE", f"🟡 {Q} Φ:D56/E0 · F1 · EVIDENCE_GAP", "🟡 [#527] Π:D42/E0 · F1 · EVIDENCE_GAP"),
            self.titles(ledger, obs_b),
        )
        ledger.append(entry(facts(sha=SHA_B, units=[unit("U01"), unit("U02"), unit("U03")]), 4))
        replayed = self.titles(ledger, obs_b)
        self.assertEqual(
            (f"🟢 {P} R:P75/E75 · U04 · ACTIVE · NEXT:CONTINUE_UNIT", f"🟢 {Q} Φ:D56/E56 · F1 · ACTIVE", "🟢 [#527] Π:D42/E42 · F1 · ACTIVE"), replayed
        )
        ledger.append(entry(facts(sha=SHA_B, units=[unit("U04")], result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"}), 5))
        self.assertEqual(
            (f"✅ {P} R:P100/E100 · COMPLETE · NEXT:NONE", "⚪ [#527 › #588] Φ:D75/E75 · F0 · IDLE", "⚪ [#527] Π:D56/E56 · F0 · IDLE"),
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
        self.assertEqual("🟢 [#527 › #588 › #592 → PR#593] R:P50/E50 · U03 · ACTIVE · NEXT:CONTINUE_UNIT", out["nodes"]["Common#592"]["title_prefix"])
        self.assertEqual("🟢 [#527] Π:D28/E28 · F1 · ACTIVE", out["nodes"]["Common#527"]["title_prefix"])



class DecompositionRepositoryObserverTests(unittest.TestCase):
    def graph(self, *, surface=None, sibling_surface=None, boundaries=None):
        return {
            "nodes": [
                {
                    "ref": "Common#1",
                    "kind": "LEAF",
                    "write_surface": list(surface or ["pkg/"]),
                    "transformation_boundaries": list(boundaries or ["PRODUCT_IMPLEMENTATION"]),
                    "depends_on": [],
                },
                {
                    "ref": "Common#2",
                    "kind": "LEAF",
                    "write_surface": list(sibling_surface or ["other/"]),
                    "transformation_boundaries": ["PRODUCT_IMPLEMENTATION"],
                    "depends_on": [],
                },
            ]
        }

    def init_repo(self, root, files):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
        for name, content in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()

    def commit(self, root, files, message="candidate"):
        for name, content in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", message], check=True)
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()

    def test_large_surface_is_digest_count_and_bounded_sample(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            files = {f"pkg/f{i:02d}.py": str(i) for i in range(30)}
            files["other/x.py"] = "x"
            self.init_repo(root, files)
            out = O.observe_repository_basis(
                self.graph(), leaf_ref="Common#1", repo_root=root, sample_limit=3
            )
            entry = out["write_surface"]["entries"][0]
            self.assertEqual("COMPLETE", out["write_surface"]["status"])
            self.assertEqual(30, entry["matched_count"])
            self.assertEqual(3, len(entry["sample"]))
            self.assertEqual("LOCAL", out["path_impact"])
            self.assertEqual("UNKNOWN", out["change_impact"])
            self.assertEqual("UNAVAILABLE", out["static_dependency_visibility"])

    def test_observation_has_authority_and_plan_basis_digest_moves_with_plan(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root, {"pkg/a.py": "a", "other/x.py": "x"})
            first = O.observe_repository_basis(self.graph(), leaf_ref="Common#1", repo_root=root)
            repeat = O.observe_repository_basis(self.graph(), leaf_ref="Common#1", repo_root=root)
            moved = O.observe_repository_basis(
                self.graph(sibling_surface=["third/"]),
                leaf_ref="Common#1",
                repo_root=root,
            )
            self.assertEqual("OBSERVED_REPOSITORY_BASIS", first["authority"])
            self.assertEqual(first["plan_basis_digest"], repeat["plan_basis_digest"])
            self.assertNotEqual(first["plan_basis_digest"], moved["plan_basis_digest"])

    def test_unresolved_surface_stays_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root, {"pkg/a.py": "a"})
            out = O.observe_repository_basis(
                self.graph(surface=["missing/"]), leaf_ref="Common#1", repo_root=root
            )
            self.assertEqual("UNRESOLVED", out["write_surface"]["status"])
            self.assertEqual("UNKNOWN", out["path_impact"])
            self.assertEqual("UNKNOWN", out["change_impact"])

    def test_sibling_overlap_proves_cross_cutting(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root, {"pkg/a.py": "a", "other/x.py": "x"})
            out = O.observe_repository_basis(
                self.graph(sibling_surface=["pkg/a.py"]), leaf_ref="Common#1", repo_root=root
            )
            self.assertEqual([{"ref": "Common#2", "overlaps": ["pkg/a.py"]}], out["sibling_overlaps"])
            self.assertEqual("CROSS_CUTTING", out["path_impact"])
            self.assertEqual("CROSS_CUTTING", out["change_impact"])

    def test_multiple_boundaries_are_multistage_not_automatic_semantic_split(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root, {"pkg/a.py": "a", "other/x.py": "x"})
            out = O.observe_repository_basis(
                self.graph(boundaries=["WIRE_SCHEMA", "ENGINE_VALIDATION"]),
                leaf_ref="Common#1",
                repo_root=root,
            )
            self.assertEqual("BOUNDED_MULTI_STAGE", out["path_impact"])
            self.assertEqual("UNKNOWN", out["change_impact"])

    def test_candidate_diff_outside_surface_is_cross_cutting(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            base = self.init_repo(root, {"pkg/a.py": "a", "other/x.py": "x"})
            candidate = self.commit(root, {"pkg/a.py": "aa", "other/x.py": "xx"})
            out = O.observe_repository_basis(
                self.graph(),
                leaf_ref="Common#1",
                repo_root=root,
                base_ref=base,
                candidate_ref=candidate,
            )
            self.assertEqual("OBSERVED", out["candidate_diff"]["visibility"])
            self.assertEqual(2, out["candidate_diff"]["changed_count"])
            self.assertEqual(1, out["candidate_diff"]["outside_surface_count"])
            self.assertEqual(["other/x.py"], out["candidate_diff"]["outside_sample"])
            self.assertEqual("CROSS_CUTTING", out["change_impact"])

    def test_rename_observes_both_old_and_new_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            base = self.init_repo(root, {"outside/a.py": "a", "pkg/keep.py": "k"})
            (root / "pkg").mkdir(exist_ok=True)
            (root / "outside/a.py").rename(root / "pkg/a.py")
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "rename"], check=True)
            candidate = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
            ).strip()
            out = O.observe_repository_basis(
                self.graph(),
                leaf_ref="Common#1",
                repo_root=root,
                base_ref=base,
                candidate_ref=candidate,
            )
            self.assertEqual(2, out["candidate_diff"]["changed_count"])
            self.assertEqual(["outside/a.py"], out["candidate_diff"]["outside_sample"])
            self.assertEqual("CROSS_CUTTING", out["change_impact"])

    def test_invalid_git_ref_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            base = self.init_repo(root, {"pkg/a.py": "a"})
            with self.assertRaises(O.ObservationError):
                O.observe_repository_basis(
                    self.graph(),
                    leaf_ref="Common#1",
                    repo_root=root,
                    base_ref=base,
                    candidate_ref="does-not-exist",
                )

    def test_diff_is_not_requested_without_both_refs(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root, {"pkg/a.py": "a"})
            out = O.observe_repository_basis(self.graph(), leaf_ref="Common#1", repo_root=root)
            self.assertEqual("NOT_REQUESTED", out["candidate_diff"]["visibility"])
            with self.assertRaises(O.ObservationError):
                O.observe_repository_basis(
                    self.graph(), leaf_ref="Common#1", repo_root=root, base_ref="HEAD"
                )


class DecompositionRepositoryObservationCurrentness(unittest.TestCase):
    def graph(self):
        return DecompositionRepositoryObserverTests().graph()

    def init_repo(self, root):
        return DecompositionRepositoryObserverTests().init_repo(
            root, {"pkg/a.py": "a", "other/x.py": "x"}
        )

    def test_current_observation_matches_public_plan_basis_helper(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            graph_value = self.graph()
            observation = O.observe_repository_basis(
                graph_value, leaf_ref="Common#1", repo_root=root
            )
            basis = O.repository_plan_basis(graph_value, "Common#1")
            self.assertEqual(basis["digest"], observation["plan_basis_digest"])
            current = O.repository_observation_currentness(
                graph_value, "Common#1", observation
            )
            self.assertEqual("CURRENT", current["state"])
            self.assertEqual(basis["digest"], current["expected_plan_basis_digest"])

    def test_plan_basis_move_marks_existing_observation_moved(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            graph_value = self.graph()
            observation = O.observe_repository_basis(
                graph_value, leaf_ref="Common#1", repo_root=root
            )
            moved = copy.deepcopy(graph_value)
            moved["nodes"][0]["write_surface"] = ["pkg/a.py"]
            current = O.repository_observation_currentness(
                moved, "Common#1", observation
            )
            self.assertEqual("MOVED", current["state"])
            self.assertNotEqual(
                current["expected_plan_basis_digest"],
                current["observed_plan_basis_digest"],
            )

    def test_provider_locator_move_preserves_stable_repository_plan_basis(self):
        g = self.graph()
        g["nodes"][0]["responsibility_id"] = "RID-1"
        g["nodes"][1]["responsibility_id"] = "RID-2"
        first = O.repository_plan_basis(g, "Common#1")

        moved = copy.deepcopy(g)
        moved["nodes"][0]["ref"] = "Common#101"
        moved["nodes"][1]["ref"] = "Common#202"
        second = O.repository_plan_basis(moved, "Common#101")

        self.assertEqual("RID-1", first["value"]["subject"])
        self.assertEqual(
            [{"responsibility_id": "RID-2", "write_surface": ["other/"]}],
            first["value"]["siblings"],
        )
        self.assertEqual(first["digest"], second["digest"])

    def test_missing_observation_is_explicit_missing_not_clean(self):
        graph_value = self.graph()
        current = O.repository_observation_currentness(
            graph_value, "Common#1", None
        )
        self.assertEqual("MISSING", current["state"])
        self.assertIsNone(current["observed_plan_basis_digest"])

    def test_dependency_basis_uses_stable_responsibility_identity(self):
        g = self.graph()
        g["nodes"][0]["responsibility_id"] = "RID-1"
        g["nodes"][1]["responsibility_id"] = "RID-2"
        g["nodes"][0]["depends_on"] = ["Common#2"]
        first = O.repository_plan_basis(g, "Common#1")
        self.assertEqual(["RID-2"], first["value"]["declared_dependencies"])

        moved = copy.deepcopy(g)
        moved["nodes"][1]["ref"] = "Common#202"
        moved["nodes"][0]["depends_on"] = ["Common#202"]
        second = O.repository_plan_basis(moved, "Common#1")
        self.assertEqual(first["digest"], second["digest"])

    def test_wrong_authority_or_subject_fails_closed(self):
        graph_value = self.graph()
        basis = O.repository_plan_basis(graph_value, "Common#1")
        good = {
            "schema": O.SCHEMA,
            "authority": "OBSERVED_REPOSITORY_BASIS",
            "subject": "Common#1",
            "plan_basis_digest": basis["digest"],
        }
        bad_schema = dict(good, schema="relay-v0-observation")
        bad_authority = dict(good, authority="EXECUTOR")
        bad_subject = dict(good, subject="Common#2")
        for bad in (bad_schema, bad_authority, bad_subject):
            with self.subTest(bad=bad), self.assertRaises(O.ObservationError):
                O.repository_observation_currentness(graph_value, "Common#1", bad)


@unittest.skipUnless(HAVE_YAML and HAVE_JSONSCHEMA, "PyYAML/jsonschema unavailable")
class DecompositionRepositoryObservationSchemaContract(unittest.TestCase):
    def test_observer_output_matches_schema(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
            path = root / "pkg/a.py"
            path.parent.mkdir(parents=True)
            path.write_text("a", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)
            graph_value = {
                "nodes": [
                    {
                        "ref": "Common#1",
                        "kind": "LEAF",
                        "write_surface": ["pkg/"],
                        "transformation_boundaries": ["PRODUCT_IMPLEMENTATION"],
                    }
                ]
            }
            out = O.observe_repository_basis(graph_value, leaf_ref="Common#1", repo_root=root)
            schema = yaml.safe_load(
                (SCHEMAS / "delp-decomposition-repository-observation-v35.schema.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual([], [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(out)])

            impossible = copy.deepcopy(out)
            impossible["candidate_diff"]["visibility"] = "OBSERVED"
            self.assertTrue(
                [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(impossible)],
                "schema accepted OBSERVED diff with null observation fields",
            )


class BidirectionalDecompositionClassifier(unittest.TestCase):
    def assessment(self, subject="fixture", **overrides):
        value = {
            "schema": D.DECOMPOSITION_ASSESSMENT_SCHEMA,
            "subject": subject,
            "proposal_kind": "LEAF",
            "semantic_cohesion": "COHESIVE",
            "dependency_closure": "CLOSED",
            "verification_closure": "CLOSED",
            "uncertainty": "LOW",
            "change_impact": "LOCAL",
            "execution_horizon": "SHORT",
            "mutation_domains": ["LOCAL_FILES"],
            "recovery_radius": "SMALL",
            "handoff_cost": "LOW",
            "cross_child_cohesion": "LOW",
            "stable_cut": {
                "output_contract": False,
                "independent_oracle": False,
                "consumer_stable": False,
                "risk_reduction": False,
                "handoff_economy": False,
            },
            "basis_moved": False,
        }
        value.update(overrides)
        return value

    def verdict(self, subject="fixture", **overrides):
        return D.classify_decomposition_assessment(self.assessment(subject, **overrides))

    def test_617_original_phase_c_is_split_from_precode_shape(self):
        out = self.verdict(
            "#617-precode",
            semantic_cohesion="MIXED",
            dependency_closure="OPEN",
            verification_closure="DEFERRED",
            uncertainty="MATERIAL",
            change_impact="CROSS_CUTTING",
            execution_horizon="LONG_OR_AMBIGUOUS",
            mutation_domains=["LOCAL_FILES", "GIT_HISTORY", "GITHUB_PR", "CI"],
            recovery_radius="MULTI_SURFACE",
            handoff_cost="MATERIAL",
            stable_cut={
                "output_contract": True,
                "independent_oracle": True,
                "consumer_stable": True,
                "risk_reduction": True,
                "handoff_economy": True,
            },
        )
        self.assertEqual("SPLIT", out["decision"])
        self.assertEqual("ETX_SPLIT_REQUIRED", out["execution_boundary"])

    def test_624_observation_pipeline_is_split_despite_small_file_count(self):
        out = self.verdict(
            "#624-precode",
            semantic_cohesion="MIXED",
            dependency_closure="OPEN",
            verification_closure="DEFERRED",
            uncertainty="MATERIAL",
            change_impact="CROSS_CUTTING",
            execution_horizon="MULTI_STEP",
            mutation_domains=["LOCAL_FILES", "GIT_HISTORY"],
            recovery_radius="MULTI_SURFACE",
            stable_cut={
                "output_contract": True,
                "independent_oracle": True,
                "consumer_stable": True,
                "risk_reduction": True,
                "handoff_economy": True,
            },
        )
        self.assertEqual("SPLIT", out["decision"])

    def test_643_condition_contract_passes_and_bug_does_not_imply_split(self):
        out = self.verdict("#643-precode")
        self.assertEqual("PASS", out["decision"])
        self.assertEqual("INLINE_SAFE", out["execution_boundary"])

    def test_c2_c3_horizontal_split_is_merge_candidate(self):
        out = self.verdict(
            "#626+#629-precode",
            proposal_kind="ADJACENT_CHILDREN",
            execution_horizon="MULTI_STEP",
            mutation_domains=["LOCAL_FILES", "GIT_HISTORY"],
            recovery_radius="MULTI_SURFACE",
            handoff_cost="HIGH",
            cross_child_cohesion="HIGH",
        )
        self.assertEqual("MERGE", out["decision"])
        self.assertEqual("ETX_SPLIT_REQUIRED", out["execution_boundary"])

    def test_known_open_dependency_without_stable_cut_requires_discovery(self):
        out = self.verdict(
            "open-dependency",
            dependency_closure="OPEN",
            uncertainty="MATERIAL",
            change_impact="BOUNDED_MULTI_STAGE",
        )
        self.assertEqual("DISCOVER_FIRST", out["decision"])

    def test_merge_never_overrides_mixed_or_deferred_semantics(self):
        mixed = self.verdict(
            "mixed-adjacent",
            proposal_kind="ADJACENT_CHILDREN",
            semantic_cohesion="MIXED",
            handoff_cost="HIGH",
            cross_child_cohesion="HIGH",
        )
        self.assertEqual("SPLIT", mixed["decision"])
        deferred = self.verdict(
            "deferred-adjacent",
            proposal_kind="ADJACENT_CHILDREN",
            verification_closure="DEFERRED",
            handoff_cost="HIGH",
            cross_child_cohesion="HIGH",
        )
        self.assertEqual("SPLIT", deferred["decision"])

    def test_unknown_basis_requires_discovery_before_implementation(self):
        out = self.verdict(
            "unknown-owner",
            dependency_closure="UNKNOWN",
            verification_closure="UNKNOWN",
            uncertainty="BLOCKING",
            change_impact="UNKNOWN",
        )
        self.assertEqual("DISCOVER_FIRST", out["decision"])
        self.assertEqual("DISCOVERY_REQUIRED", out["execution_boundary"])

    def test_moved_basis_replans_before_all_other_decisions(self):
        out = self.verdict(
            "moved-contract",
            basis_moved=True,
            semantic_cohesion="UNKNOWN",
            dependency_closure="UNKNOWN",
            verification_closure="UNKNOWN",
            uncertainty="BLOCKING",
            change_impact="UNKNOWN",
        )
        self.assertEqual("REPLAN", out["decision"])

    def test_ambiguous_external_effect_requires_observe_before_retry(self):
        out = self.verdict(
            "external-effect",
            execution_horizon="MULTI_STEP",
            mutation_domains=["LOCAL_FILES", "GITHUB_ISSUE"],
            recovery_radius="AMBIGUOUS_EXTERNAL",
        )
        self.assertEqual("PASS", out["decision"])
        self.assertEqual("OBSERVE_BEFORE_RETRY_REQUIRED", out["execution_boundary"])

    def test_invalid_assessment_fails_closed(self):
        bad = self.assessment()
        bad["semantic_cohesion"] = "SORT_OF"
        self.assertTrue(D.validate_decomposition_assessment(bad))
        with self.assertRaises(D.DecompositionError):
            D.classify_decomposition_assessment(bad)


@unittest.skipUnless(HAVE_YAML and HAVE_JSONSCHEMA, "PyYAML/jsonschema unavailable")
class DecompositionAssessmentSchemaContract(unittest.TestCase):
    @classmethod
    def schema(cls):
        import yaml as _yaml

        return _yaml.safe_load((SCHEMAS / f"delp-decomposition-assessment-{TAG}.schema.yaml").read_text(encoding="utf-8"))

    def errors(self, value):
        return [e.message for e in jsonschema.Draft202012Validator(self.schema()).iter_errors(value)]

    def good(self):
        return BidirectionalDecompositionClassifier().assessment("schema-fixture")

    def test_schema_id_and_good_record(self):
        self.assertEqual(D.DECOMPOSITION_ASSESSMENT_SCHEMA, self.schema()["$id"])
        self.assertEqual([], self.errors(self.good()))
        self.assertEqual([], D.validate_decomposition_assessment(self.good()))

    def test_schema_and_engine_reject_malformed_records(self):
        variants = []
        good = self.good()
        for key, value in (
            ("proposal_kind", "EPIC"),
            ("semantic_cohesion", "KINDA"),
            ("dependency_closure", "PARTIAL"),
            ("verification_closure", "LATER"),
            ("uncertainty", "MAYBE"),
            ("change_impact", "HUGE"),
            ("execution_horizon", "FOREVER"),
            ("recovery_radius", "WIDE"),
            ("handoff_cost", "MEDIUM"),
            ("cross_child_cohesion", "MEDIUM"),
        ):
            row = copy.deepcopy(good)
            row[key] = value
            variants.append(row)
        row = copy.deepcopy(good)
        row["mutation_domains"] = ["LOCAL_FILES", "LOCAL_FILES"]
        variants.append(row)
        row = copy.deepcopy(good)
        row["mutation_domains"] = [["LOCAL_FILES"]]
        variants.append(row)
        row = copy.deepcopy(good)
        row["stable_cut"]["risk_reduction"] = "yes"
        variants.append(row)
        row = copy.deepcopy(good)
        row["basis_moved"] = "no"
        variants.append(row)
        for record in variants:
            with self.subTest(record=record):
                self.assertTrue(self.errors(record), "schema accepted malformed assessment")
                self.assertTrue(D.validate_decomposition_assessment(record), "engine accepted malformed assessment")


@unittest.skipUnless(HAVE_YAML and HAVE_JSONSCHEMA, "PyYAML/jsonschema unavailable")
class ResponsibilityConditionSchemaContract(unittest.TestCase):
    @classmethod
    def schema(cls):
        import yaml as _yaml

        return _yaml.safe_load((SCHEMAS / f"delp-responsibility-condition-{TAG}.schema.yaml").read_text(encoding="utf-8"))

    def errors(self, value):
        return [e.message for e in jsonschema.Draft202012Validator(self.schema()).iter_errors(value)]

    def good(self):
        return {
            "type": "EvidenceCurrent",
            "status": "TRUE",
            "reason": "CURRENT_EVIDENCE",
            "message": "Accepted evidence matches the observed candidate.",
            "observed_generation": 2,
            "candidate_sha": SHA_A,
            "source_refs": ["Common#592#issuecomment-1"],
        }

    def test_schema_id_and_vocabularies(self):
        schema = self.schema()
        self.assertEqual("relay-v3.5-delp-responsibility-condition", schema["$id"])
        self.assertEqual(
            {
                "PlanReady",
                "SpecCurrent",
                "MaterialObserved",
                "EvidenceCurrent",
                "DependenciesReady",
                "CustodySafe",
                "AssuranceSatisfied",
                "ProviderVisible",
            },
            set(schema["properties"]["type"]["enum"]),
        )
        self.assertEqual(
            {"TRUE", "FALSE", "UNKNOWN", "NOT_APPLICABLE"},
            set(schema["properties"]["status"]["enum"]),
        )

    def test_good_record_and_unknown_binding_shape(self):
        self.assertEqual([], self.errors(self.good()))
        unknown = self.good()
        unknown.update(
            {
                "type": "ProviderVisible",
                "status": "UNKNOWN",
                "observed_generation": None,
                "candidate_sha": None,
                "source_refs": [],
            }
        )
        self.assertEqual([], self.errors(unknown))

    def test_required_fields_and_additional_properties_are_closed(self):
        good = self.good()
        for key in good:
            with self.subTest(missing=key):
                row = copy.deepcopy(good)
                row.pop(key)
                self.assertTrue(self.errors(row))
        row = copy.deepcopy(good)
        row["surprise"] = True
        self.assertTrue(self.errors(row))

    def test_enum_text_generation_sha_and_source_ref_constraints(self):
        good = self.good()
        variants = []

        def changed(**updates):
            row = copy.deepcopy(good)
            row.update(updates)
            return row

        variants.extend(
            [
                changed(type="NoSuchCondition"),
                changed(type=[]),
                changed(status="PASS"),
                changed(status={}),
                changed(reason="   "),
                changed(message=""),
                changed(observed_generation=0),
                changed(observed_generation=True),
                changed(candidate_sha="abc123"),
                changed(source_refs="not-an-array"),
                changed(source_refs=[""]),
                changed(source_refs=["same", "same"]),
            ]
        )
        for row in variants:
            with self.subTest(row=row):
                self.assertTrue(self.errors(row), "schema accepted malformed condition")


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
        self.assertEqual(M.OBSERVATION_SCHEMA, self.schema("responsibility-observation")["$id"])
        self.assertEqual(M.CONDITION_SCHEMA, self.schema("responsibility-condition")["$id"])

    def test_execution_provenance_fact_passes_schema_and_engine(self):
        record = facts(
            units=[unit("U01")],
            execution={
                "ep": "EP-P3-B1",
                "lease": "LEASE-P3-B1",
                "executor": "agent-604-b1",
                "custody_epoch": 8,
            },
        )
        self.assertEqual([], self.schema_errors("checkpoint-facts", record))
        self.assertEqual([], M.validate_facts(record))

    def test_bad_execution_provenance_fails_schema_and_engine(self):
        good = {
            "ep": "EP-P3-B1",
            "lease": "LEASE-P3-B1",
            "executor": "agent-604-b1",
            "custody_epoch": 8,
        }
        variants = []
        for key in good:
            row = copy.deepcopy(good)
            row.pop(key)
            variants.append(row)
        variants += [
            {**good, "ep": "EP"},
            {**good, "lease": "LEASE"},
            {**good, "executor": "   "},
            {**good, "custody_epoch": 0},
            {**good, "custody_epoch": True},
            {**good, "unexpected": "x"},
        ]
        for execution in variants:
            record = facts(units=[unit("U01")], execution=execution)
            with self.subTest(execution=execution):
                self.assertTrue(self.schema_errors("checkpoint-facts", record), "schema accepted malformed execution binding")
                self.assertTrue(M.validate_facts(record), "engine accepted malformed execution binding")

    def test_good_observation_passes_schema_and_engine(self):
        record = {
            "schema": M.OBSERVATION_SCHEMA,
            "visibility": "OBSERVED",
            "material": {
                "candidate_sha": SHA_A,
                "base_sha": SHA_MAIN,
                "pr_state": "OPEN",
                "ahead_by": 2,
                "behind_by": 1,
            },
            "custody": {
                "interruptions": {
                    "coverage_from": "2026-10-07T00:00:00Z",
                    "losses": [{"kind": "STREAM"}],
                }
            },
            "liveness": {"value": "ACTIVE"},
            "check": {"name": "optional", "result": "SUCCESS", "candidate_sha": SHA_A},
            "diff": {
                "additions": 10,
                "deletions": 2,
                "since_checkpoint": {"additions": 3, "deletions": 1},
            },
        }
        self.assertEqual([], self.schema_errors("responsibility-observation", record))
        self.assertEqual([], M.validate_observation(record))

    def test_unavailable_observation_can_omit_all_optional_categories(self):
        record = {"schema": M.OBSERVATION_SCHEMA, "visibility": "UNAVAILABLE"}
        self.assertEqual([], self.schema_errors("responsibility-observation", record))
        self.assertEqual([], M.validate_observation(record))

    def test_bad_observations_fail_schema_and_engine(self):
        good = {
            "schema": M.OBSERVATION_SCHEMA,
            "visibility": "OBSERVED",
            "material": {"candidate_sha": SHA_A},
        }
        variants = []
        for mutate in (
            lambda x: x.__setitem__("visibility", "FAIL"),
            lambda x: x["material"].__setitem__("candidate_sha", "abc123"),
            lambda x: x.__setitem__("liveness", {"value": "DEAD"}),
            lambda x: x.__setitem__("diff", {"additions": -1}),
            lambda x: x.__setitem__("check", {"result": "GREEN"}),
            lambda x: x.__setitem__("surprise", True),
            lambda x: x["material"].__setitem__("pr_state", None),
            lambda x: x["material"].__setitem__("ahead_by", None),
            lambda x: x.__setitem__("check", {"result": None}),
            lambda x: x.__setitem__("check", {"name": None}),
            lambda x: x.__setitem__("diff", {"additions": None}),
            lambda x: x.__setitem__("custody", {"interruptions": {"losses": None}}),
            lambda x: x.__setitem__("material", None),
            lambda x: x.__setitem__("custody", None),
            lambda x: x.__setitem__("liveness", None),
            lambda x: x.__setitem__("check", None),
            lambda x: x.__setitem__("diff", None),
            lambda x: x.__setitem__("visibility", []),
            lambda x: x["material"].__setitem__("pr_state", {}),
            lambda x: x.__setitem__("liveness", {"value": []}),
            lambda x: x.__setitem__("check", {"result": {}}),
            lambda x: x.__setitem__("check", {"name": "   "}),
        ):
            row = copy.deepcopy(good)
            mutate(row)
            variants.append(row)
        for record in variants:
            with self.subTest(record=record):
                self.assertTrue(self.schema_errors("responsibility-observation", record), "schema accepted it")
                self.assertTrue(M.validate_observation(record), "engine accepted it")

    def test_good_condition_passes_schema_and_engine(self):
        record = {
            "type": "EvidenceCurrent",
            "status": "TRUE",
            "reason": "CURRENT_EVIDENCE",
            "message": "Accepted evidence matches the observed candidate.",
            "observed_generation": 2,
            "candidate_sha": SHA_A,
            "source_refs": ["Common#592#issuecomment-1"],
        }
        self.assertEqual([], self.schema_errors("responsibility-condition", record))
        self.assertEqual([], M.validate_condition(record))

    def test_integral_float_generation_matches_json_schema_integer_semantics(self):
        record = {
            "type": "PlanReady",
            "status": "TRUE",
            "reason": "PLAN_RELEASEABLE",
            "message": "The current plan is releaseable.",
            "observed_generation": 1.0,
            "candidate_sha": None,
            "source_refs": [],
        }
        self.assertEqual([], self.schema_errors("responsibility-condition", record))
        self.assertEqual([], M.validate_condition(record))

    def test_unknown_condition_binding_passes_schema_and_engine(self):
        record = {
            "type": "ProviderVisible",
            "status": "UNKNOWN",
            "reason": "PROVIDER_UNOBSERVED",
            "message": "Provider visibility was not observed.",
            "observed_generation": None,
            "candidate_sha": None,
            "source_refs": [],
        }
        self.assertEqual([], self.schema_errors("responsibility-condition", record))
        self.assertEqual([], M.validate_condition(record))

    def test_bad_conditions_fail_schema_and_engine_without_crashing(self):
        good = {
            "type": "PlanReady",
            "status": "TRUE",
            "reason": "PLAN_RELEASEABLE",
            "message": "The current plan is releaseable.",
            "observed_generation": 1,
            "candidate_sha": None,
            "source_refs": ["graph:sha256:" + "a" * 64],
        }
        variants = []

        def changed(**updates):
            row = copy.deepcopy(good)
            row.update(updates)
            return row

        variants.extend(
            [
                {k: v for k, v in good.items() if k != "reason"},
                changed(surprise=True),
                changed(type="NoSuchCondition"),
                changed(type=[]),
                changed(type={}),
                changed(status="PASS"),
                changed(status=[]),
                changed(status={}),
                changed(reason="   "),
                changed(message=""),
                changed(observed_generation=0),
                changed(observed_generation=True),
                changed(observed_generation="2"),
                changed(observed_generation=1.5),
                changed(candidate_sha="abc123"),
                changed(candidate_sha=[]),
                changed(source_refs="not-an-array"),
                changed(source_refs=[""]),
                changed(source_refs=["same", "same"]),
                changed(source_refs=[{}]),
            ]
        )
        for record in variants:
            with self.subTest(record=record):
                self.assertTrue(self.schema_errors("responsibility-condition", record), "schema accepted it")
                self.assertTrue(M.validate_condition(record), "engine accepted it")

    def test_condition_constructor_returns_a_valid_record(self):
        record = M.condition_record(
            "EvidenceCurrent",
            "TRUE",
            "CURRENT_EVIDENCE",
            "Accepted evidence matches the observed candidate.",
            observed_generation=2,
            candidate_sha=SHA_A,
            source_refs=["Common#592#issuecomment-1"],
        )
        self.assertEqual([], M.validate_condition(record))
        self.assertEqual([], self.schema_errors("responsibility-condition", record))

    def test_condition_constructor_accepts_a_non_text_iterable(self):
        record = M.condition_record(
            "ProviderVisible",
            "UNKNOWN",
            "PROVIDER_UNOBSERVED",
            "Provider visibility was not observed.",
            source_refs=(ref for ref in ["provider:github"]),
        )
        self.assertEqual(["provider:github"], record["source_refs"])
        self.assertEqual([], M.validate_condition(record))

    def test_condition_constructor_rejects_ambiguous_or_non_iterable_source_refs(self):
        for source_refs in (
            "abc",
            b"abc",
            bytearray(b"abc"),
            {"ref": "abc"},
            {"a", "b"},
            frozenset({"a", "b"}),
            None,
            7,
        ):
            with self.subTest(source_refs=source_refs):
                with self.assertRaises(M.DelpError):
                    M.condition_record(
                        "PlanReady",
                        "TRUE",
                        "PLAN_RELEASEABLE",
                        "The current plan is releaseable.",
                        source_refs=source_refs,
                    )

    def test_condition_constructor_fails_closed_on_invalid_record_fields(self):
        invalid = [
            {"condition_type": "NoSuchCondition"},
            {"status": "PASS"},
            {"reason": "   "},
            {"message": ""},
            {"observed_generation": 0},
            {"candidate_sha": "abc123"},
            {"source_refs": ["same", "same"]},
            {"source_refs": [""]},
        ]
        defaults = {
            "condition_type": "PlanReady",
            "status": "TRUE",
            "reason": "PLAN_RELEASEABLE",
            "message": "The current plan is releaseable.",
            "observed_generation": 1,
            "candidate_sha": None,
            "source_refs": [],
        }
        for updates in invalid:
            with self.subTest(updates=updates), self.assertRaises(M.DelpError):
                M.condition_record(**{**defaults, **updates})

    def test_good_facts_pass_both(self):
        record = facts(units=[unit("U01", candidate_sha=SHA_B, contract_digest=DIGEST)], activity="WAITING_CI",
                       next={"unit": "U02", "action": "run replay"}, blocker="NONE", owner_action="NONE",
                       gates=[{"id": "REVIEWER_ACCEPTANCE", "result": "PASSED", "evidence_refs": ["r"]}],
                       result={"scope": "STEP", "responsibility_complete": "NO"})
        self.assertEqual([], self.schema_errors("checkpoint-facts", record))
        self.assertEqual([], M.validate_facts(record))

    def test_responsibility_contract_binding_fields_pass_both(self):
        record = facts(units=[unit("U01")])
        record["responsibility"].update(
            {"id": "P3-I-R2", "spec_generation": 3, "contract_digest": DIGEST}
        )
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

    def test_stable_identity_graph_without_spec_generation_fails_both(self):
        g = stable_graph()
        g["nodes"][4].pop("spec_generation")
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


    def test_stable_currentness_projection_satisfies_live_status_schema(self):
        g = stable_graph()
        projection = M.project(g, [entry(bound_facts(g, units=[unit("U01")]), 1)], OBS_A)
        leaf = projection["nodes"]["Common#592"]
        document = M.status_document(
            leaf, version=1, digest=projection["input_digest"], programme=projection["programme"]
        )
        self.assertEqual([], self.schema_errors("live-status", json.loads(M.canonical_json(document))))
        self.assertEqual("STABLE", document["node"]["currentness"]["mode"])
        self.assertTrue(document["node"]["currentness"]["fact_binding_required"])


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = M.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_bind_facts_cli_stamps_current_contract(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            g = stable_graph()
            raw = facts(units=[unit("U01")])
            (root / "graph.json").write_text(json.dumps(g), encoding="utf-8")
            (root / "facts.json").write_text(json.dumps(raw), encoding="utf-8")
            code, out, err = self.run_cli(
                "bind-facts",
                "--graph", str(root / "graph.json"),
                "--facts", str(root / "facts.json"),
            )
            self.assertEqual(0, code, err)
            bound = json.loads(out)
            planned = M.validate_graph(g)["nodes"]["Common#592"]
            self.assertEqual(planned["responsibility_id"], bound["responsibility"]["id"])
            self.assertEqual(planned["spec_generation"], bound["responsibility"]["spec_generation"])
            self.assertEqual(planned["contract_digest"], bound["responsibility"]["contract_digest"])

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


def claim_topology_planned():
    """V3.5 claim topology fixture using explicit OWN / ENABLES / GATE relationships."""
    g = planned()
    g["programme"]["acceptance_claims"] = [
        {"id": "PC-PRODUCT", "claim": "the semantic product outcome exists", "kind": "SEMANTIC"},
        {"id": "PC-ENABLE", "claim": "a durable enabling contract exists", "kind": "SEMANTIC"},
        {"id": "PC-GATE", "claim": "the exact-head delivery gate passes", "kind": "DELIVERY_GATE"},
    ]
    leaf_of(g, "Common#592")["claim_relationships"] = [
        {"claim_id": "PC-PRODUCT", "relation": "OWN"},
        {"claim_id": "PC-ENABLE", "relation": "ENABLES"},
    ]
    leaf_of(g, "Common#594")["claim_relationships"] = [
        {"claim_id": "PC-GATE", "relation": "GATE"},
    ]
    return g


def stable_claim_topology_graph():
    g = stable_graph()
    g["programme"]["acceptance_claims"] = [
        {"id": "PC-PRODUCT", "claim": "the semantic product outcome exists", "kind": "SEMANTIC"},
        {"id": "PC-ENABLE", "claim": "a durable enabling contract exists", "kind": "SEMANTIC"},
        {"id": "PC-GATE", "claim": "the exact-head delivery gate passes", "kind": "DELIVERY_GATE"},
    ]
    leaf_of(g, "Common#592")["claim_relationships"] = [
        {"claim_id": "PC-PRODUCT", "relation": "OWN"},
        {"claim_id": "PC-ENABLE", "relation": "ENABLES"},
    ]
    leaf_of(g, "Common#594")["claim_relationships"] = [
        {"claim_id": "PC-GATE", "relation": "GATE"},
    ]
    return g


def topology_assessment_planned():
    g = stable_claim_topology_graph()
    leaf_of(g, "Common#612")["claim_relationships"] = [
        {"claim_id": "PC-ENABLE", "relation": "OWN"},
    ]
    g["programme"]["topology_assessments"] = [
        {
            "id": "TA-LEAF",
            "proposal_kind": "LEAF",
            "responsibility_ids": ["P3-I-R2"],
            "semantic_cohesion": "COHESIVE",
            "dependency_closure": "CLOSED",
            "verification_closure": "CLOSED",
            "uncertainty": "LOW",
            "change_impact": "LOCAL",
            "execution_horizon": "SHORT",
            "mutation_domains": ["LOCAL_FILES"],
            "recovery_radius": "SMALL",
            "handoff_cost": "LOW",
            "cross_child_cohesion": "LOW",
            "stable_cut": {
                "output_contract": False,
                "independent_oracle": False,
                "consumer_stable": False,
                "risk_reduction": False,
                "handoff_economy": False,
            },
            "source_refs": ["Common#648#topology-release"],
        },
        {
            "id": "TA-PAIR",
            "proposal_kind": "ADJACENT_CHILDREN",
            "responsibility_ids": ["RESP-594", "P3-I-R2"],
            "semantic_cohesion": "COHESIVE",
            "dependency_closure": "CLOSED",
            "verification_closure": "CLOSED",
            "uncertainty": "LOW",
            "change_impact": "LOCAL",
            "execution_horizon": "MULTI_STEP",
            "mutation_domains": ["LOCAL_FILES", "GIT_HISTORY"],
            "recovery_radius": "MULTI_SURFACE",
            "handoff_cost": "HIGH",
            "cross_child_cohesion": "HIGH",
            "stable_cut": {
                "output_contract": False,
                "independent_oracle": False,
                "consumer_stable": False,
                "risk_reduction": False,
                "handoff_economy": False,
            },
            "source_refs": ["Common#651#retained-replay"],
        },
    ]
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
        self.assertFalse(policy["require"]["transformation_boundaries"])

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
            "boundary list type": lambda g: leaf(g).__setitem__("transformation_boundaries", "WIRE_SCHEMA"),
            "unknown boundary": lambda g: leaf(g).__setitem__("transformation_boundaries", ["NOPE"]),
            "boundary whitespace": lambda g: leaf(g).__setitem__("transformation_boundaries", [" WIRE_SCHEMA "]),
            "duplicate boundary": lambda g: leaf(g).__setitem__("transformation_boundaries", ["WIRE_SCHEMA", "WIRE_SCHEMA"]),
            "integration basis type": lambda g: leaf(g).__setitem__("integration_basis", 3),
            "integration basis blank": lambda g: leaf(g).__setitem__("integration_basis", "   "),
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

    def test_transformation_boundary_metadata_is_normalised(self):
        g = planned(require={"transformation_boundaries": True})
        leaf = leaf_of(g, "Common#592")
        leaf["transformation_boundaries"] = ["WIRE_SCHEMA", "ENGINE_VALIDATION"]
        leaf["integration_basis"] = "  one atomic compatibility surface  "
        indexed = M.validate_graph(g)
        row = indexed["nodes"]["Common#592"]
        self.assertEqual(["ENGINE_VALIDATION", "WIRE_SCHEMA"], row["transformation_boundaries"])
        self.assertEqual("one atomic compatibility surface", row["integration_basis"])
        self.assertTrue(indexed["policy"]["require"]["transformation_boundaries"])

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


class ClaimTopologyContract(unittest.TestCase):
    def test_claim_topology_schema_and_engine_agree(self):
        g = claim_topology_planned()
        self.assertEqual([], SchemasAgreeWithTheEngine().schema_errors("execution-graph", g))
        indexed = M.validate_graph(g)
        self.assertEqual(
            ["PC-ENABLE", "PC-GATE", "PC-PRODUCT"],
            [row["id"] for row in indexed["acceptance_claims"]],
        )
        self.assertEqual(
            [
                {"claim_id": "PC-ENABLE", "relation": "ENABLES"},
                {"claim_id": "PC-PRODUCT", "relation": "OWN"},
            ],
            indexed["nodes"]["Common#592"]["claim_relationships"],
        )

    def test_claim_topology_shape_errors_fail_schema_and_engine(self):
        cases = []

        g = claim_topology_planned()
        g["programme"]["acceptance_claims"][0]["kind"] = "MECHANISM"
        cases.append(("claim kind", g))

        g = claim_topology_planned()
        g["programme"]["acceptance_claims"][0]["shared"] = "yes"
        cases.append(("shared type", g))

        g = claim_topology_planned()
        leaf_of(g, "Common#592")["claim_relationships"][0]["relation"] = "REVIEW"
        cases.append(("relation kind", g))

        for label, bad in cases:
            with self.subTest(label):
                self.assertTrue(SchemasAgreeWithTheEngine().schema_errors("execution-graph", bad))
                with self.assertRaises(M.GraphError):
                    M.validate_graph(bad)

    def test_claim_topology_relational_invariants_fail_closed_in_engine(self):
        cases = []

        g = claim_topology_planned()
        g["programme"]["acceptance_claims"].append(
            {"id": "PC-PRODUCT", "claim": "duplicate", "kind": "SEMANTIC"}
        )
        cases.append(("duplicate claim id", g))

        g = claim_topology_planned()
        leaf_of(g, "Common#592")["claim_relationships"][0]["claim_id"] = "PC-MISSING"
        cases.append(("unknown claim target", g))

        g = claim_topology_planned()
        leaf_of(g, "Common#592")["claim_relationships"].append(
            {"claim_id": "PC-PRODUCT", "relation": "ENABLES"}
        )
        cases.append(("duplicate relationship target", g))

        for label, bad in cases:
            with self.subTest(label), self.assertRaises(M.GraphError):
                M.validate_graph(bad)

    def test_legacy_graph_without_claim_topology_remains_readable(self):
        indexed = M.validate_graph(planned())
        self.assertEqual([], indexed["acceptance_claims"])
        self.assertEqual([], indexed["nodes"]["Common#592"]["claim_relationships"])


class TopologyAssessmentPlanContract(unittest.TestCase):
    def test_topology_assessment_schema_and_engine_agree(self):
        g = topology_assessment_planned()
        self.assertEqual([], SchemasAgreeWithTheEngine().schema_errors("execution-graph", g))
        indexed = M.validate_graph(g)
        self.assertEqual(["TA-LEAF", "TA-PAIR"], [row["id"] for row in indexed["topology_assessments"]])
        pair = indexed["topology_assessments_by_id"]["TA-PAIR"]
        self.assertEqual(["P3-I-R2", "RESP-594"], pair["responsibility_ids"])
        self.assertEqual(["GIT_HISTORY", "LOCAL_FILES"], pair["mutation_domains"])

    def test_topology_assessment_shape_errors_fail_schema_and_engine(self):
        cases = []

        g = topology_assessment_planned()
        g["programme"]["topology_assessments"][0]["proposal_kind"] = "PIPELINE"
        cases.append(("proposal kind", g))

        g = topology_assessment_planned()
        g["programme"]["topology_assessments"][0]["source_refs"] = []
        cases.append(("source refs", g))

        g = topology_assessment_planned()
        g["programme"]["topology_assessments"][0]["stable_cut"]["risk_reduction"] = "yes"
        cases.append(("stable cut bool", g))

        for label, bad in cases:
            with self.subTest(label):
                self.assertTrue(SchemasAgreeWithTheEngine().schema_errors("execution-graph", bad))
                with self.assertRaises(M.GraphError):
                    M.validate_graph(bad)

    def test_topology_assessment_relational_invariants_fail_closed(self):
        cases = []

        g = topology_assessment_planned()
        g["programme"]["topology_assessments"][0]["responsibility_ids"] = ["NO-SUCH-RID"]
        cases.append(("unknown stable id", g))

        g = topology_assessment_planned()
        g["programme"]["topology_assessments"][0]["responsibility_ids"] = ["P3-I-R2", "RESP-594"]
        cases.append(("leaf cardinality", g))

        g = topology_assessment_planned()
        g["programme"]["topology_assessments"][1]["responsibility_ids"] = ["P3-I-R2", "RESP-612"]
        cases.append(("non sibling pair", g))

        g = topology_assessment_planned()
        duplicate = copy.deepcopy(g["programme"]["topology_assessments"][0])
        duplicate["id"] = "TA-DUP"
        g["programme"]["topology_assessments"].append(duplicate)
        cases.append(("duplicate subject set", g))

        g = topology_assessment_planned()
        duplicate = copy.deepcopy(g["programme"]["topology_assessments"][0])
        duplicate["responsibility_ids"] = ["RESP-594"]
        g["programme"]["topology_assessments"].append(duplicate)
        cases.append(("duplicate assessment id", g))

        for label, bad in cases:
            with self.subTest(label), self.assertRaises(M.GraphError):
                M.validate_graph(bad)

    def test_topology_assessment_is_plan_metadata_not_product_contract(self):
        base = stable_claim_topology_graph()
        before = M.validate_graph(base)
        before_digest = before["nodes"]["Common#592"]["contract_digest"]

        planned = topology_assessment_planned()
        after = M.validate_graph(planned)
        self.assertEqual(before_digest, after["nodes"]["Common#592"]["contract_digest"])
        self.assertNotEqual(before["digest"], after["digest"])

        record = bound_facts(base, units=[unit("U01")])
        before_projection = M.project(base, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]
        after_projection = M.project(planned, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual(before_projection["progress"], after_projection["progress"])
        self.assertEqual(
            before_projection["identity"]["contract_digest"],
            after_projection["identity"]["contract_digest"],
        )

    def test_r2_plan_basis_does_not_change_the_mechanical_decomposition_layer(self):
        with_graph = topology_assessment_planned()
        without_graph = stable_claim_topology_graph()
        with_basis = M._decomposition(M.validate_graph(with_graph))
        without_basis = M._decomposition(M.validate_graph(without_graph))
        self.assertEqual(without_basis, with_basis)


class TopologyAdmissionAssembler(unittest.TestCase):
    def init_repo(self, root):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
        path = root / "placeholder.txt"
        path.write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)

    def observations(self, graph_value, root, refs):
        return {
            ref: O.observe_repository_basis(graph_value, leaf_ref=ref, repo_root=root)
            for ref in refs
        }

    def test_current_leaf_basis_classifies_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = topology_assessment_planned()
            observations = self.observations(g, root, ["Common#592"])
            out = A.assemble_topology_admission(
                g, assessment_id="TA-LEAF", observations=observations
            )
            self.assertEqual("DERIVED_TOPOLOGY_ADMISSION_ONLY", out["authority"])
            self.assertEqual([], out["claim_topology"]["blockers"])
            self.assertEqual("CURRENT", out["repository_currentness"][0]["state"])
            self.assertEqual("LOCAL", out["assessment"]["change_impact"])
            self.assertEqual("PASS", out["decision"]["decision"])
            self.assertEqual([], D.validate_decomposition_assessment(out["assessment"]))

    def test_current_adjacent_children_basis_classifies_merge(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = topology_assessment_planned()
            observations = self.observations(g, root, ["Common#592", "Common#594"])
            out = A.assemble_topology_admission(
                g, assessment_id="TA-PAIR", observations=observations
            )
            self.assertEqual(["P3-I-R2", "RESP-594"], out["responsibility_ids"])
            self.assertEqual("MERGE", out["decision"]["decision"])

    def test_missing_observation_derives_unknown_and_discover_first(self):
        g = topology_assessment_planned()
        out = A.assemble_topology_admission(
            g, assessment_id="TA-LEAF", observations={}
        )
        self.assertEqual("MISSING", out["repository_currentness"][0]["state"])
        self.assertEqual("UNKNOWN", out["assessment"]["change_impact"])
        self.assertEqual("DISCOVER_FIRST", out["decision"]["decision"])

    def test_moved_repository_basis_forces_replan(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            original = topology_assessment_planned()
            observations = self.observations(original, root, ["Common#592"])

            moved = copy.deepcopy(original)
            leaf_of(moved, "Common#592")["write_surface"] = ["pkg/"]
            out = A.assemble_topology_admission(
                moved, assessment_id="TA-LEAF", observations=observations
            )
            self.assertEqual("MOVED", out["repository_currentness"][0]["state"])
            self.assertTrue(out["assessment"]["basis_moved"])
            self.assertEqual("REPLAN", out["decision"]["decision"])

    def test_current_cross_cutting_observation_overrides_optimistic_plan_impact(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = topology_assessment_planned()
            leaf_of(g, "Common#592")["write_surface"] = ["placeholder.txt"]
            leaf_of(g, "Common#594")["write_surface"] = ["placeholder.txt"]
            observations = self.observations(g, root, ["Common#592"])
            self.assertEqual("CROSS_CUTTING", observations["Common#592"]["change_impact"])
            out = A.assemble_topology_admission(
                g, assessment_id="TA-LEAF", observations=observations
            )
            self.assertEqual("CROSS_CUTTING", out["assessment"]["change_impact"])

    def test_wrong_ontology_claim_topology_cannot_be_rescued_by_optimistic_boundary_basis(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = topology_assessment_planned()
            leaf_of(g, "Common#592")["claim_relationships"] = [
                {"claim_id": "PC-PRODUCT", "relation": "GATE"},
                {"claim_id": "PC-ENABLE", "relation": "ENABLES"},
            ]
            leaf_of(g, "Common#612")["claim_relationships"] = [
                {"claim_id": "PC-ENABLE", "relation": "GATE"},
            ]
            observations = self.observations(g, root, ["Common#592"])
            out = A.assemble_topology_admission(
                g, assessment_id="TA-LEAF", observations=observations
            )
            self.assertIn("UNCOVERED_CLAIMS", out["claim_topology"]["blockers"])
            self.assertEqual("BLOCKING", out["assessment"]["uncertainty"])
            self.assertEqual("DISCOVER_FIRST", out["decision"]["decision"])

    def test_assembly_is_deterministic_under_observation_map_order(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = topology_assessment_planned()
            obs = self.observations(g, root, ["Common#592", "Common#594"])
            forward = A.assemble_topology_admission(
                g, assessment_id="TA-PAIR", observations=obs
            )
            reverse = A.assemble_topology_admission(
                g,
                assessment_id="TA-PAIR",
                observations=dict(reversed(list(obs.items()))),
            )
            self.assertEqual(M.canonical_json(forward), M.canonical_json(reverse))

    def test_retained_precode_topology_replay(self):
        def cut(value):
            return {
                "output_contract": value,
                "independent_oracle": value,
                "consumer_stable": value,
                "risk_reduction": value,
                "handoff_economy": value,
            }

        fixtures = [
            {
                "name": "#617 original Phase C",
                "expected": "SPLIT",
                "refs": ["Common#592"],
                "basis": {
                    "id": "RET-617",
                    "proposal_kind": "LEAF",
                    "responsibility_ids": ["P3-I-R2"],
                    "semantic_cohesion": "MIXED",
                    "dependency_closure": "OPEN",
                    "verification_closure": "DEFERRED",
                    "uncertainty": "MATERIAL",
                    "change_impact": "CROSS_CUTTING",
                    "execution_horizon": "LONG_OR_AMBIGUOUS",
                    "mutation_domains": ["LOCAL_FILES", "GIT_HISTORY", "GITHUB_PR", "CI"],
                    "recovery_radius": "MULTI_SURFACE",
                    "handoff_cost": "MATERIAL",
                    "cross_child_cohesion": "LOW",
                    "stable_cut": cut(True),
                    "source_refs": ["Common#651:DECOMPOSITION_FAILURE_CORPUS_V1:CASE_A_PRECODE"],
                },
            },
            {
                "name": "PR #624 original observation integration",
                "expected": "SPLIT",
                "refs": ["Common#592"],
                "basis": {
                    "id": "RET-624",
                    "proposal_kind": "LEAF",
                    "responsibility_ids": ["P3-I-R2"],
                    "semantic_cohesion": "MIXED",
                    "dependency_closure": "OPEN",
                    "verification_closure": "DEFERRED",
                    "uncertainty": "MATERIAL",
                    "change_impact": "CROSS_CUTTING",
                    "execution_horizon": "MULTI_STEP",
                    "mutation_domains": ["LOCAL_FILES", "GIT_HISTORY", "GITHUB_PR"],
                    "recovery_radius": "MULTI_SURFACE",
                    "handoff_cost": "MATERIAL",
                    "cross_child_cohesion": "LOW",
                    "stable_cut": cut(True),
                    "source_refs": ["Common#651:DECOMPOSITION_FAILURE_CORPUS_V1:CASE_B_PRECODE"],
                },
            },
            {
                "name": "#638 / PR #643 canonical condition contract",
                "expected": "PASS",
                "refs": ["Common#592"],
                "basis": {
                    "id": "RET-643",
                    "proposal_kind": "LEAF",
                    "responsibility_ids": ["P3-I-R2"],
                    "semantic_cohesion": "COHESIVE",
                    "dependency_closure": "CLOSED",
                    "verification_closure": "CLOSED",
                    "uncertainty": "LOW",
                    "change_impact": "LOCAL",
                    "execution_horizon": "SHORT",
                    "mutation_domains": ["LOCAL_FILES"],
                    "recovery_radius": "SMALL",
                    "handoff_cost": "HIGH",
                    "cross_child_cohesion": "LOW",
                    "stable_cut": cut(False),
                    "source_refs": ["Common#651:DECOMPOSITION_FAILURE_CORPUS_V1:CASE_C_PRECODE"],
                },
            },
            {
                "name": "#626 + #629 proposed horizontal split",
                "expected": "MERGE",
                "refs": ["Common#592", "Common#594"],
                "basis": {
                    "id": "RET-626-629",
                    "proposal_kind": "ADJACENT_CHILDREN",
                    "responsibility_ids": ["P3-I-R2", "RESP-594"],
                    "semantic_cohesion": "COHESIVE",
                    "dependency_closure": "CLOSED",
                    "verification_closure": "CLOSED",
                    "uncertainty": "LOW",
                    "change_impact": "LOCAL",
                    "execution_horizon": "MULTI_STEP",
                    "mutation_domains": ["LOCAL_FILES", "GIT_HISTORY"],
                    "recovery_radius": "MULTI_SURFACE",
                    "handoff_cost": "HIGH",
                    "cross_child_cohesion": "HIGH",
                    "stable_cut": cut(False),
                    "source_refs": ["Common#651:DECOMPOSITION_FAILURE_CORPUS_V1:CASE_D_PRECODE"],
                },
            },
        ]

        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            for fixture in fixtures:
                with self.subTest(case=fixture["name"]):
                    g = topology_assessment_planned()
                    g["programme"]["topology_assessments"] = [fixture["basis"]]
                    observations = self.observations(g, root, fixture["refs"])
                    out = A.assemble_topology_admission(
                        g,
                        assessment_id=fixture["basis"]["id"],
                        observations=observations,
                    )
                    self.assertEqual([], out["claim_topology"]["blockers"])
                    self.assertEqual(fixture["expected"], out["decision"]["decision"])

    def test_wrong_current_observation_payload_fails_closed(self):
        g = topology_assessment_planned()
        basis = O.repository_plan_basis(g, "Common#592")
        malformed = {
            "schema": O.SCHEMA,
            "authority": "OBSERVED_REPOSITORY_BASIS",
            "subject": "Common#592",
            "plan_basis_digest": basis["digest"],
            "change_impact": "LOCAL",
        }
        with self.assertRaises(A.AssemblyError):
            A.assemble_topology_admission(
                g, assessment_id="TA-LEAF", observations={"Common#592": malformed}
            )


class TopologyReleaseFindings(unittest.TestCase):
    def init_repo(self, root):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
        path = root / "placeholder.txt"
        path.write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)

    def observations(self, graph_value, root, refs):
        return {
            ref: O.observe_repository_basis(graph_value, leaf_ref=ref, repo_root=root)
            for ref in refs
        }

    def test_legacy_graph_has_no_topology_release_findings(self):
        out = A.topology_release_findings(stable_graph(), observations={})
        self.assertFalse(out["active"])
        self.assertEqual({}, out["leaves"])
        self.assertEqual(0, out["summary"]["blocked"])

    def test_pass_adds_no_blocker_but_unassessed_leaf_is_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = topology_assessment_planned()
            g["programme"]["topology_assessments"] = [
                copy.deepcopy(g["programme"]["topology_assessments"][0])
            ]
            observations = self.observations(g, root, ["Common#592"])
            out = A.topology_release_findings(
                g,
                observations=observations,
                closed={"Common#594"},
            )
            self.assertEqual([], out["leaves"]["Common#592"]["blockers"])
            self.assertEqual(
                "PASS",
                out["leaves"]["Common#592"]["admissions"][0]["decision"],
            )
            self.assertEqual(
                ["TOPOLOGY_ADMISSION_MISSING"],
                [b["code"] for b in out["leaves"]["Common#612"]["blockers"]],
            )

    def test_existing_pair_merge_maps_to_both_subject_leaves(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = topology_assessment_planned()
            observations = self.observations(g, root, ["Common#592", "Common#594"])
            out = A.topology_release_findings(
                g,
                observations=observations,
                closed={"Common#612"},
            )
            for ref in ("Common#592", "Common#594"):
                self.assertIn(
                    "TOPOLOGY_MERGE_REQUIRED",
                    [b["code"] for b in out["leaves"][ref]["blockers"]],
                )
            self.assertEqual("MERGE", out["leaves"]["Common#594"]["admissions"][0]["decision"])

    def test_split_discover_and_replan_map_without_reinterpreting_r2(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)

            split = topology_assessment_planned()
            split["programme"]["topology_assessments"] = [
                copy.deepcopy(split["programme"]["topology_assessments"][0])
            ]
            split["programme"]["topology_assessments"][0]["semantic_cohesion"] = "MIXED"
            split_obs = self.observations(split, root, ["Common#592"])
            split_out = A.topology_release_findings(
                split, observations=split_obs, closed={"Common#594", "Common#612"}
            )
            self.assertEqual(
                ["TOPOLOGY_SPLIT_REQUIRED"],
                [b["code"] for b in split_out["leaves"]["Common#592"]["blockers"]],
            )

            missing = topology_assessment_planned()
            missing["programme"]["topology_assessments"] = [
                copy.deepcopy(missing["programme"]["topology_assessments"][0])
            ]
            missing_out = A.topology_release_findings(
                missing, observations={}, closed={"Common#594", "Common#612"}
            )
            self.assertEqual(
                ["TOPOLOGY_DISCOVERY_REQUIRED"],
                [b["code"] for b in missing_out["leaves"]["Common#592"]["blockers"]],
            )

            original = topology_assessment_planned()
            original["programme"]["topology_assessments"] = [
                copy.deepcopy(original["programme"]["topology_assessments"][0])
            ]
            stale_obs = self.observations(original, root, ["Common#592"])
            moved = copy.deepcopy(original)
            leaf_of(moved, "Common#592")["write_surface"] = ["pkg/"]
            moved_out = A.topology_release_findings(
                moved, observations=stale_obs, closed={"Common#594", "Common#612"}
            )
            self.assertEqual(
                ["TOPOLOGY_REPLAN_REQUIRED"],
                [b["code"] for b in moved_out["leaves"]["Common#592"]["blockers"]],
            )

    def test_findings_are_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = topology_assessment_planned()
            observations = self.observations(g, root, ["Common#592", "Common#594"])
            first = M.canonical_json(
                A.topology_release_findings(g, observations=observations, closed={"Common#612"})
            )
            g["programme"]["topology_assessments"].reverse()
            second = M.canonical_json(
                A.topology_release_findings(g, observations=observations, closed={"Common#612"})
            )
            self.assertEqual(first, second)


class ClaimTopologyReport(unittest.TestCase):
    def test_report_distinguishes_ownership_enabling_and_gate_coverage(self):
        report = M.claim_topology_report(claim_topology_planned())
        rows = {row["id"]: row for row in report["claims"]}
        self.assertEqual("OWNED", rows["PC-PRODUCT"]["coverage"])
        self.assertEqual(["Common#592"], rows["PC-PRODUCT"]["owners"])
        self.assertEqual("UNCOVERED", rows["PC-ENABLE"]["coverage"])
        self.assertEqual(["Common#592"], rows["PC-ENABLE"]["enablers"])
        self.assertEqual("COVERED", rows["PC-GATE"]["coverage"])
        self.assertEqual(["Common#594"], rows["PC-GATE"]["gates"])
        self.assertEqual(1, report["summary"]["uncovered_claims"])
        self.assertEqual(1, report["summary"]["orphan_responsibilities"])
        self.assertEqual("DERIVED_CLAIM_TOPOLOGY_ONLY", report["authority"])

    def test_enables_and_gate_do_not_masquerade_as_semantic_ownership(self):
        g = claim_topology_planned()
        leaf_of(g, "Common#592")["claim_relationships"] = [
            {"claim_id": "PC-PRODUCT", "relation": "GATE"},
            {"claim_id": "PC-ENABLE", "relation": "ENABLES"},
        ]
        report = M.claim_topology_report(g)
        rows = {row["id"]: row for row in report["claims"]}
        self.assertEqual("UNCOVERED", rows["PC-PRODUCT"]["coverage"])
        self.assertEqual([], rows["PC-PRODUCT"]["owners"])
        self.assertEqual(["Common#592"], rows["PC-PRODUCT"]["gates"])

    def test_duplicate_nonshared_ownership_is_observed_not_enforced(self):
        g = claim_topology_planned()
        leaf_of(g, "Common#594")["claim_relationships"] = [
            {"claim_id": "PC-PRODUCT", "relation": "OWN"},
            {"claim_id": "PC-GATE", "relation": "GATE"},
        ]
        report = M.claim_topology_report(g)
        product = next(row for row in report["claims"] if row["id"] == "PC-PRODUCT")
        self.assertEqual(["Common#592", "Common#594"], product["duplicate_owners"])
        self.assertEqual(1, report["summary"]["duplicate_nonshared_ownership"])
        # R1's report remains pure facts; R3 may later use those facts in the integrated release report.
        mechanical = M._decomposition(M.validate_graph(g))
        self.assertTrue(mechanical["leaves"]["Common#592"]["releasable"])

        for claim in g["programme"]["acceptance_claims"]:
            if claim["id"] == "PC-PRODUCT":
                claim["shared"] = True
        shared = M.claim_topology_report(g)
        product = next(row for row in shared["claims"] if row["id"] == "PC-PRODUCT")
        self.assertEqual([], product["duplicate_owners"])

    def test_report_is_deterministic_under_claim_and_relation_input_order(self):
        g = claim_topology_planned()
        first = M.canonical_json(M.claim_topology_report(g))
        g["programme"]["acceptance_claims"].reverse()
        leaf_of(g, "Common#592")["claim_relationships"].reverse()
        second = M.canonical_json(M.claim_topology_report(g))
        self.assertEqual(first, second)


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
        behavioral = lambda nodes: {  # noqa: E731
            ref: {key: value for key, value in node.items() if key != "currentness"}
            for ref, node in nodes.items()
        }
        self.assertEqual(behavioral(clean), behavioral(failing))
        self.assertNotEqual(
            clean["Common#592"]["currentness"]["graph_digest"],
            failing["Common#592"]["currentness"]["graph_digest"],
        )
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
        self.assertEqual("🟡 [#527 › #588 › #594 → PR#595] R:P0/E0 · V1 · NOT_RELEASEABLE · NEXT:FIX_PLAN", node["title_prefix"])
        for ref in clean:
            self.assertEqual(clean[ref]["progress"], enforced[ref]["progress"], ref)
        self.assertEqual("🟢 [#527 › #588 › #592 → PR#593] R:P50/E50 · U03 · ACTIVE · NEXT:CONTINUE_UNIT", enforced["Common#592"]["title_prefix"])

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


class CanonicalPlanSpecConditions(unittest.TestCase):
    @staticmethod
    def by_type(node):
        return {row["type"]: row for row in node["conditions"]}

    def test_off_plan_is_ready_without_fabricating_spec_currentness(self):
        g = stable_graph()
        g["programme"]["decomposition_policy"] = {"mode": "OFF"}
        node = M.project(g, [], OBS_A)["nodes"]["Common#592"]
        conditions = self.by_type(node)
        self.assertEqual("TRUE", conditions["PlanReady"]["status"])
        self.assertEqual("PLAN_GATE_OFF", conditions["PlanReady"]["reason"])
        self.assertEqual("UNKNOWN", conditions["SpecCurrent"]["status"])
        self.assertEqual("SPEC_BINDING_UNOBSERVED", conditions["SpecCurrent"]["reason"])

    def test_advisory_would_block_is_ready_but_exposes_the_blockers(self):
        g = broken("ADVISORY", "Common#592")
        node = M.project(g, [], OBS_A)["nodes"]["Common#592"]
        conditions = self.by_type(node)
        self.assertFalse(node["plan"]["releasable"])
        self.assertEqual("TRUE", conditions["PlanReady"]["status"])
        self.assertEqual("PLAN_ADVISORY_WOULD_BLOCK", conditions["PlanReady"]["reason"])
        self.assertIn("OUTCOME_MISSING", conditions["PlanReady"]["message"])

    def test_enforced_plan_ready_tracks_the_existing_releasability_only(self):
        good = M.project(planned(), [], OBS_A)["nodes"]["Common#592"]
        bad = M.project(broken(ref="Common#592"), [], OBS_A)["nodes"]["Common#592"]
        self.assertEqual("TRUE", self.by_type(good)["PlanReady"]["status"])
        self.assertEqual("FALSE", self.by_type(bad)["PlanReady"]["status"])
        self.assertEqual("PLAN_NOT_RELEASEABLE", self.by_type(bad)["PlanReady"]["reason"])

    def test_health_and_title_do_not_author_plan_ready(self):
        g = broken("ADVISORY", "Common#592")
        base = M.project(g, [], OBS_A)["nodes"]["Common#592"]
        observed = {
            **OBS_A,
            "Common#592": {
                **OBS_A["Common#592"],
                "liveness": "STALE",
                "additions": 9999,
                "deletions": 9999,
            },
        }
        changed = M.project(g, [], observed)["nodes"]["Common#592"]
        self.assertEqual(
            self.by_type(base)["PlanReady"],
            self.by_type(changed)["PlanReady"],
        )

    def test_current_bound_fact_makes_spec_current_true(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01")])
        node = M.project(g, [entry(record, 1, "current-fact")], OBS_A)["nodes"]["Common#592"]
        spec = self.by_type(node)["SpecCurrent"]
        self.assertEqual("TRUE", spec["status"])
        self.assertEqual("SPEC_BINDING_CURRENT", spec["reason"])
        self.assertEqual(1, spec["observed_generation"])
        self.assertEqual(["current-fact"], spec["source_refs"])

    def test_graph_only_reparent_reweight_preserves_spec_current(self):
        old = stable_graph()
        record = bound_facts(old, units=[unit("U01")])
        moved = copy.deepcopy(old)
        leaf = leaf_of(moved, "Common#592")
        leaf["parent"] = "Common#610"
        leaf["weight"] = 9
        node = M.project(moved, [entry(record, 1, "bound-before-move")], OBS_A)["nodes"]["Common#592"]
        spec = self.by_type(node)["SpecCurrent"]
        self.assertEqual("TRUE", spec["status"])
        self.assertEqual("SPEC_BINDING_CURRENT", spec["reason"])

    def test_stale_contract_fact_is_rejected_and_cannot_make_spec_current_true(self):
        old = stable_graph()
        stale = bound_facts(old, units=[unit("U01")])
        changed = copy.deepcopy(old)
        leaf = leaf_of(changed, "Common#592")
        leaf["outcome"] = "changed semantic contract"
        leaf["spec_generation"] = 2
        out = M.project(changed, [entry(stale, 1, "stale-contract")], OBS_A)
        spec = self.by_type(out["nodes"]["Common#592"])["SpecCurrent"]
        self.assertEqual("UNKNOWN", spec["status"])
        self.assertEqual("SPEC_BINDING_UNOBSERVED", spec["reason"])
        self.assertEqual(["stale-contract"], [row["source"] for row in out["rejected_facts"]])

    def test_terminal_leaf_plan_ready_is_not_applicable(self):
        g = stable_graph()
        done = bound_facts(
            g,
            leaf="Common#612",
            pr="Common#613",
            units=[unit("W1")],
            result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"},
        )
        node = M.project(g, [entry(done, 1)], OBS_A)["nodes"]["Common#612"]
        self.assertEqual("COMPLETE", node["lifecycle"])
        plan = self.by_type(node)["PlanReady"]
        self.assertEqual("NOT_APPLICABLE", plan["status"])
        self.assertEqual("PLAN_NOT_APPLICABLE_TERMINAL", plan["reason"])


class CanonicalProviderEvidenceConditions(unittest.TestCase):
    @staticmethod
    def by_type(node):
        return {row["type"]: row for row in node["conditions"]}

    def test_legacy_observed_candidate_makes_provider_and_material_true(self):
        node = M.project(stable_graph(), [], OBS_A)["nodes"]["Common#592"]
        conditions = self.by_type(node)
        self.assertEqual("TRUE", conditions["ProviderVisible"]["status"])
        self.assertEqual("TRUE", conditions["MaterialObserved"]["status"])
        self.assertEqual(SHA_A, conditions["MaterialObserved"]["candidate_sha"])
        self.assertEqual("UNKNOWN", conditions["EvidenceCurrent"]["status"])

    def test_explicit_provider_unavailable_is_unknown_not_failure(self):
        observations = {
            "Common#592": {
                "schema": M.OBSERVATION_SCHEMA,
                "visibility": "UNAVAILABLE",
            }
        }
        node = M.project(stable_graph(), [], observations)["nodes"]["Common#592"]
        conditions = self.by_type(node)
        self.assertEqual("UNKNOWN", conditions["ProviderVisible"]["status"])
        self.assertEqual("PROVIDER_UNAVAILABLE", conditions["ProviderVisible"]["reason"])
        self.assertEqual("UNKNOWN", conditions["MaterialObserved"]["status"])
        self.assertEqual("MATERIAL_UNAVAILABLE", conditions["MaterialObserved"]["reason"])
        self.assertEqual("UNKNOWN", conditions["EvidenceCurrent"]["status"])

    def test_observed_provider_with_no_material_signal_reports_material_false(self):
        observations = {
            "Common#592": {
                "schema": M.OBSERVATION_SCHEMA,
                "visibility": "OBSERVED",
                "material": {"ahead_by": 0, "behind_by": 0},
            }
        }
        node = M.project(stable_graph(), [], observations)["nodes"]["Common#592"]
        conditions = self.by_type(node)
        self.assertEqual("TRUE", conditions["ProviderVisible"]["status"])
        self.assertEqual("FALSE", conditions["MaterialObserved"]["status"])
        self.assertEqual("MATERIAL_NOT_PRESENT", conditions["MaterialObserved"]["reason"])

    def test_current_accepted_evidence_is_true(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01")])
        node = M.project(g, [entry(record, 1, "current-evidence")], OBS_A)["nodes"]["Common#592"]
        evidence = self.by_type(node)["EvidenceCurrent"]
        self.assertEqual("TRUE", evidence["status"])
        self.assertEqual("EVIDENCE_CURRENT", evidence["reason"])
        self.assertEqual(SHA_A, evidence["candidate_sha"])
        self.assertEqual(["current-evidence"], evidence["source_refs"])

    def test_stale_candidate_and_gap_are_false(self):
        g = stable_graph()
        current = bound_facts(g, units=[unit("U01")])
        stale = M.project(
            g,
            [entry(current, 1)],
            {**OBS_A, "Common#592": {"candidate_sha": SHA_B}},
        )["nodes"]["Common#592"]
        self.assertEqual("FALSE", self.by_type(stale)["EvidenceCurrent"]["status"])
        self.assertEqual(
            "EVIDENCE_STALE_CANDIDATE",
            self.by_type(stale)["EvidenceCurrent"]["reason"],
        )

        gap_record = bound_facts(g, units=[unit("U01", refs=())])
        gap = M.project(g, [entry(gap_record, 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual("FALSE", self.by_type(gap)["EvidenceCurrent"]["status"])
        self.assertEqual("EVIDENCE_GAP", self.by_type(gap)["EvidenceCurrent"]["reason"])

    def test_unobserved_candidate_makes_existing_evidence_unknown(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01")])
        node = M.project(g, [entry(record, 1)], {})["nodes"]["Common#592"]
        evidence = self.by_type(node)["EvidenceCurrent"]
        self.assertEqual("UNKNOWN", evidence["status"])
        self.assertEqual("EVIDENCE_UNVERIFIABLE", evidence["reason"])

    def test_optional_failed_check_does_not_change_provider_material_or_evidence_conditions(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01")])
        base_obs = {
            "Common#592": {
                "schema": M.OBSERVATION_SCHEMA,
                "visibility": "OBSERVED",
                "material": {"candidate_sha": SHA_A},
            }
        }
        check_obs = copy.deepcopy(base_obs)
        check_obs["Common#592"]["check"] = {
            "result": "FAILURE",
            "candidate_sha": SHA_A,
            "name": "optional-check",
        }
        before = self.by_type(M.project(g, [entry(record, 1)], base_obs)["nodes"]["Common#592"])
        after = self.by_type(M.project(g, [entry(record, 1)], check_obs)["nodes"]["Common#592"])
        for kind in ("ProviderVisible", "MaterialObserved", "EvidenceCurrent"):
            self.assertEqual(before[kind], after[kind], kind)


class CanonicalDependencyCondition(unittest.TestCase):
    @staticmethod
    def by_type(node):
        return {row["type"]: row for row in node["conditions"]}

    def test_no_declared_dependencies_is_not_applicable(self):
        node = M.project(stable_graph(), [], OBS_A)["nodes"]["Common#592"]
        condition = self.by_type(node)["DependenciesReady"]
        self.assertEqual("NOT_APPLICABLE", condition["status"])
        self.assertEqual("NO_DECLARED_DEPENDENCIES", condition["reason"])

    def test_all_declared_dependencies_complete_is_true(self):
        g = stable_graph()
        leaf_of(g, "Common#592")["depends_on"] = ["Common#612"]
        done = bound_facts(
            g,
            leaf="Common#612",
            pr="Common#613",
            units=[unit("W1")],
            result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"},
        )
        node = M.project(g, [entry(done, 1)], OBS_A)["nodes"]["Common#592"]
        condition = self.by_type(node)["DependenciesReady"]
        self.assertEqual("TRUE", condition["status"])
        self.assertEqual("DEPENDENCIES_COMPLETE", condition["reason"])
        self.assertEqual(["Common#612"], condition["source_refs"])

    def test_known_noncomplete_dependency_is_false(self):
        g = stable_graph()
        leaf_of(g, "Common#592")["depends_on"] = ["Common#612"]
        node = M.project(g, [], OBS_A)["nodes"]["Common#592"]
        condition = self.by_type(node)["DependenciesReady"]
        self.assertEqual("FALSE", condition["status"])
        self.assertEqual("DEPENDENCIES_INCOMPLETE", condition["reason"])
        self.assertIn("Common#612:NOT_STARTED", condition["message"])

    def test_provider_pr_merge_does_not_complete_a_dependency(self):
        g = stable_graph()
        leaf_of(g, "Common#592")["depends_on"] = ["Common#612"]
        observations = {
            **OBS_A,
            "Common#612": {
                "schema": M.OBSERVATION_SCHEMA,
                "visibility": "OBSERVED",
                "material": {
                    "candidate_sha": SHA_A,
                    "pr_state": "MERGED",
                },
            },
        }
        node = M.project(g, [], observations)["nodes"]["Common#592"]
        condition = self.by_type(node)["DependenciesReady"]
        self.assertEqual("FALSE", condition["status"])
        self.assertEqual("DEPENDENCIES_INCOMPLETE", condition["reason"])

    def test_undeclared_sibling_state_does_not_affect_dependency_condition(self):
        g = stable_graph()
        base = self.by_type(M.project(g, [], OBS_A)["nodes"]["Common#592"])["DependenciesReady"]
        active = bound_facts(g, leaf="Common#612", pr="Common#613", units=[unit("W1", state="IN_PROGRESS")])
        changed = self.by_type(
            M.project(g, [entry(active, 1)], OBS_A)["nodes"]["Common#592"]
        )["DependenciesReady"]
        self.assertEqual(base, changed)


class CanonicalConditionSetAssembly(unittest.TestCase):
    def test_every_leaf_has_exactly_eight_conditions_in_canonical_order(self):
        out = M.project(stable_graph(), [], OBS_A)
        for ref, node in out["nodes"].items():
            if node["kind"] != "LEAF":
                continue
            self.assertEqual(
                list(M.CONDITION_ORDER),
                [row["type"] for row in node["conditions"]],
                ref,
            )
            self.assertEqual(8, len(node["conditions"]))
            for row in node["conditions"]:
                self.assertEqual([], M.validate_condition(row), (ref, row))

    def test_custody_and_assurance_are_never_fabricated_true_before_p3_p4(self):
        node = M.project(stable_graph(), [], OBS_A)["nodes"]["Common#592"]
        rows = {row["type"]: row for row in node["conditions"]}
        self.assertEqual("NOT_APPLICABLE", rows["CustodySafe"]["status"])
        self.assertEqual("CUSTODY_POLICY_NOT_IMPLEMENTED", rows["CustodySafe"]["reason"])
        self.assertEqual("NOT_APPLICABLE", rows["AssuranceSatisfied"]["status"])
        self.assertEqual("ASSURANCE_POLICY_NOT_IMPLEMENTED", rows["AssuranceSatisfied"]["reason"])
        self.assertNotEqual("TRUE", rows["CustodySafe"]["status"])
        self.assertNotEqual("TRUE", rows["AssuranceSatisfied"]["status"])

    def test_condition_assembly_does_not_change_progress_math(self):
        g = stable_graph()
        record = bound_facts(g, units=[unit("U01"), unit("U02")])
        indexed = M.validate_graph(g)
        accepted, _ = M.partition_ledger(indexed, [entry(record, 1)])
        normalized = M.normalize_observations(indexed, OBS_A)
        raw_leaf = M.compute_leaf(
            indexed["nodes"]["Common#592"],
            accepted["Common#592"],
            normalized[592],
        )
        projected = M.project(g, [entry(record, 1)], OBS_A)["nodes"]["Common#592"]
        self.assertEqual(raw_leaf["progress"], projected["progress"])

    def test_advisory_health_changes_do_not_change_condition_set(self):
        g = stable_graph()
        g["programme"]["health_policy"] = {"mode": "ADVISORY"}
        base = M.project(g, [], OBS_A)["nodes"]["Common#592"]
        stressed_obs = {
            **OBS_A,
            "Common#592": {
                "candidate_sha": SHA_A,
                "liveness": "STALE",
                "additions": 5000,
                "deletions": 5000,
                "interruptions": {
                    "coverage_from": "start",
                    "losses": [{"kind": "stream"}, {"kind": "stream"}, {"kind": "stream"}],
                },
            },
        }
        stressed = M.project(g, [], stressed_obs)["nodes"]["Common#592"]
        self.assertIn("health", stressed)
        self.assertEqual(base["conditions"], stressed["conditions"])

    def test_leaf_projection_and_live_status_publish_same_conditions_and_actual_next(self):
        projection = M.project(stable_graph(), [], OBS_A)
        leaf = projection["nodes"]["Common#592"]
        self.assertEqual(8, len(leaf["conditions"]))
        self.assertEqual("DERIVED_ACTUAL_NEXT_ONLY", leaf["actual_next"]["authority"])
        self.assertEqual("CONTINUE_UNIT", leaf["actual_next"]["action"])

        status = M.status_document(
            leaf,
            version=0,
            digest=projection["input_digest"],
            programme=projection["programme"],
        )
        self.assertEqual(leaf["conditions"], status["node"]["conditions"])
        self.assertEqual(leaf["actual_next"], status["node"]["actual_next"])
        self.assertEqual(
            [],
            SchemasAgreeWithTheEngine().schema_errors(
                "live-status",
                json.loads(M.canonical_json(status)),
            ),
        )

    def test_non_leaf_projection_does_not_fabricate_conditions_or_actual_next(self):
        projection = M.project(stable_graph(), [], OBS_A)
        root = projection["nodes"]["Common#527"]
        self.assertNotIn("conditions", root)
        self.assertNotIn("actual_next", root)
        status = M.status_document(
            root,
            version=0,
            digest=projection["input_digest"],
            programme=projection["programme"],
        )
        self.assertNotIn("conditions", status["node"])
        self.assertNotIn("actual_next", status["node"])

    def test_actual_next_loader_binds_to_this_exact_delp_contract(self):
        module = M._actual_next_module()
        self.assertIs(M.DelpError, module.DelpError)
        self.assertIs(M.validate_condition, module.validate_condition)
        self.assertEqual(M.CONDITION_ORDER, module.CONDITION_ORDER)

    def test_finalizer_rejects_duplicate_or_incomplete_sets(self):
        node = M.project(stable_graph(), [], OBS_A)["nodes"]["Common#592"]
        complete = node["conditions"]
        with self.assertRaises(M.DelpError):
            M._finalize_condition_set([*complete, copy.deepcopy(complete[0])])
        with self.assertRaises(M.DelpError):
            M._finalize_condition_set(complete[:-1])


class SemanticTopologyPlanProjection(unittest.TestCase):
    def init_repo(self, root):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
        path = root / "placeholder.txt"
        path.write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)

    def observations(self, graph_value, root, refs):
        return {
            ref: O.observe_repository_basis(graph_value, leaf_ref=ref, repo_root=root)
            for ref in refs
        }

    def topology_graph(self, mode="ENFORCED"):
        g = topology_assessment_planned()
        g["programme"]["decomposition_policy"] = {"mode": mode}
        return g

    def test_off_mode_preserves_existing_no_plan_behavior(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.topology_graph("OFF")
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            out = M.project(g, [], OBS_A, topology_observations=topo)
            self.assertTrue(all("plan" not in node for node in out["nodes"].values()))

    def test_enforced_topology_blockers_merge_into_the_existing_plan(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.topology_graph("ENFORCED")
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            record = bound_facts(g, units=[unit("U01")])
            baseline = copy.deepcopy(g)
            baseline["programme"]["decomposition_policy"] = {"mode": "OFF"}
            before = M.project(baseline, [entry(record, 1)], OBS_A, topology_observations=topo)
            after = M.project(g, [entry(record, 1)], OBS_A, topology_observations=topo)

            leaf = after["nodes"]["Common#592"]
            codes = [b["code"] for b in leaf["plan"]["blockers"]]
            self.assertIn("TOPOLOGY_MERGE_REQUIRED", codes)
            self.assertFalse(leaf["plan"]["releasable"])
            self.assertEqual("NOT_RELEASEABLE", leaf["state"])
            self.assertEqual(
                before["nodes"]["Common#592"]["progress"],
                leaf["progress"],
            )
            self.assertEqual(
                before["nodes"]["Common#592"]["evidence"],
                leaf["evidence"],
            )
            self.assertIn("topology", leaf["plan"])
            self.assertEqual(
                "DERIVED_TOPOLOGY_RELEASE_FINDINGS",
                leaf["plan"]["topology"]["authority"],
            )

            missing = after["nodes"]["Common#612"]["plan"]
            self.assertIn(
                "TOPOLOGY_ADMISSION_MISSING",
                [b["code"] for b in missing["blockers"]],
            )

    def test_advisory_topology_blocker_does_not_overlay_leaf_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.topology_graph("ADVISORY")
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            out = M.project(g, [], OBS_A, topology_observations=topo)
            leaf = out["nodes"]["Common#592"]
            self.assertFalse(leaf["plan"]["releasable"])
            self.assertIn(
                "TOPOLOGY_MERGE_REQUIRED",
                [b["code"] for b in leaf["plan"]["blockers"]],
            )
            self.assertNotEqual("NOT_RELEASEABLE", leaf["state"])

    def test_pass_decisions_add_no_topology_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.topology_graph("ENFORCED")
            pair = next(a for a in g["programme"]["topology_assessments"] if a["id"] == "TA-PAIR")
            pair["handoff_cost"] = "LOW"
            pair["cross_child_cohesion"] = "LOW"
            g["programme"]["topology_assessments"].append(
                {
                    "id": "TA-CLOSEOUT",
                    "proposal_kind": "LEAF",
                    "responsibility_ids": ["RESP-612"],
                    "semantic_cohesion": "COHESIVE",
                    "dependency_closure": "CLOSED",
                    "verification_closure": "CLOSED",
                    "uncertainty": "LOW",
                    "change_impact": "LOCAL",
                    "execution_horizon": "SHORT",
                    "mutation_domains": ["LOCAL_FILES"],
                    "recovery_radius": "SMALL",
                    "handoff_cost": "LOW",
                    "cross_child_cohesion": "LOW",
                    "stable_cut": {
                        "output_contract": False,
                        "independent_oracle": False,
                        "consumer_stable": False,
                        "risk_reduction": False,
                        "handoff_economy": False,
                    },
                    "source_refs": ["Common#648#R3-pass-fixture"],
                }
            )
            topo = self.observations(g, root, ["Common#592", "Common#594", "Common#612"])
            out = M.project(g, [], OBS_A, topology_observations=topo)
            for ref in ("Common#592", "Common#594", "Common#612"):
                topology_codes = [
                    b["code"]
                    for b in out["nodes"][ref]["plan"]["blockers"]
                    if b["code"].startswith("TOPOLOGY_")
                ]
                self.assertEqual([], topology_codes, ref)

    def test_topology_observations_are_part_of_projection_input_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.topology_graph("ENFORCED")
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            current = M.project(g, [], OBS_A, topology_observations=topo)
            missing = M.project(g, [], OBS_A, topology_observations={})
            self.assertNotEqual(current["input_digest"], missing["input_digest"])
            self.assertNotEqual(
                current["nodes"]["Common#592"]["plan"]["topology"],
                missing["nodes"]["Common#592"]["plan"]["topology"],
            )


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


class LiveTopologyObservationPlumbing(unittest.TestCase):
    def init_repo(self, root):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
        for name in ("src/a.py", "src/b.py", "other/x.py"):
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name, encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)

    def set_origin(self, root, repository):
        subprocess.run(
            ["git", "-C", str(root), "remote", "add", "origin", f"https://github.com/{repository}.git"],
            check=True,
        )

    def graph(self):
        g = topology_assessment_planned()
        leaf_of(g, "Common#592")["write_surface"] = ["src/"]
        leaf_of(g, "Common#594")["write_surface"] = ["other/"]
        return g

    def test_live_topology_observer_is_empty_for_legacy_graph(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            self.assertEqual({}, M.observe_topology_repository(stable_graph(), root))

    def test_live_topology_observer_produces_current_r2_basis(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.graph()
            observed = M.observe_topology_repository(g, root)
            self.assertIn("Common#592", observed)
            current = O.repository_observation_currentness(
                g,
                "Common#592",
                observed["Common#592"],
            )
            self.assertEqual("CURRENT", current["state"])

    def test_live_repository_identity_binding_fails_closed_on_wrong_checkout(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            self.set_origin(root, "reallaksh19/Common")
            g = self.graph()
            observed = M.observe_topology_repository(
                g,
                root,
                expected_repository="reallaksh19/Common",
            )
            self.assertIn("Common#592", observed)
            with self.assertRaises(M.DelpError):
                M.observe_topology_repository(
                    g,
                    root,
                    expected_repository="reallaksh19/Other",
                )

    def test_input_cache_recomputes_topology_observations_after_conflict_invalidation(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.graph()
            calls = {"topology": 0}

            def topo():
                calls["topology"] += 1
                return M.observe_topology_repository(g, root)

            cache = M._InputCache(g, lambda: [], lambda: OBS_A, topo)
            first = cache.projection()
            second = cache.projection()
            self.assertEqual(1, calls["topology"])
            self.assertEqual(first["input_digest"], second["input_digest"])
            cache.invalidate()
            third = cache.projection()
            self.assertEqual(2, calls["topology"])
            self.assertEqual(first["input_digest"], third["input_digest"])


class IntegratedSemanticDecompositionReport(unittest.TestCase):
    def init_repo(self, root):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
        path = root / "placeholder.txt"
        path.write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)

    def observations(self, graph_value, root, refs):
        return {
            ref: O.observe_repository_basis(graph_value, leaf_ref=ref, repo_root=root)
            for ref in refs
        }

    def graph(self, mode="ENFORCED"):
        g = topology_assessment_planned()
        g["programme"]["decomposition_policy"] = {"mode": mode}
        return g

    def test_decomposition_report_and_project_use_the_same_semantic_blockers(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.graph()
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            report = M.decomposition_report(
                g,
                topology_observations=topo,
            )
            projection = M.project(
                g,
                [],
                OBS_A,
                topology_observations=topo,
            )
            for ref, row in report["leaves"].items():
                self.assertEqual(
                    [b["code"] for b in row["blockers"]],
                    [b["code"] for b in projection["nodes"][ref]["plan"]["blockers"]],
                    ref,
                )
                self.assertEqual(
                    row["releasable"],
                    projection["nodes"][ref]["plan"]["releasable"],
                    ref,
                )

    def test_legacy_report_is_unchanged_without_claim_first_authority(self):
        g = planned()
        self.assertEqual(
            M.canonical_json(M._decomposition(M.validate_graph(g))),
            M.canonical_json(M.decomposition_report(g)),
        )

    def test_decompose_check_cli_accepts_distinct_topology_observation_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.graph()
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            graph_path = root / "graph.json"
            topo_path = root / "topology.json"
            graph_path.write_text(json.dumps(g), encoding="utf-8")
            topo_path.write_text(json.dumps(topo), encoding="utf-8")
            code, out, err = cli(
                "decompose-check",
                "--graph", str(graph_path),
                "--topology-observations", str(topo_path),
                "--json",
            )
            self.assertEqual(1, code, err)
            payload = json.loads(out)
            self.assertIn(
                "TOPOLOGY_MERGE_REQUIRED",
                [b["code"] for b in payload["leaves"]["Common#592"]["blockers"]],
            )


class SemanticTopologyContinuationAndFrontier(unittest.TestCase):
    def init_repo(self, root):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
        path = root / "placeholder.txt"
        path.write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)

    def observations(self, graph_value, root, refs):
        return {
            ref: O.observe_repository_basis(graph_value, leaf_ref=ref, repo_root=root)
            for ref in refs
        }

    def graph(self, mode):
        g = topology_assessment_planned()
        g["programme"]["decomposition_policy"] = {"mode": mode}
        return g

    def ledger(self, graph_value):
        return [
            entry(
                bound_facts(
                    graph_value,
                    units=[unit("U01"), unit("U02")],
                    next={"unit": "U03", "action": "continue bounded unit"},
                ),
                1,
            )
        ]

    def test_enforced_topology_blocker_uses_existing_fix_plan_action(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.graph("ENFORCED")
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            projection = M.project(g, self.ledger(g), OBS_A, topology_observations=topo)
            report = M.admit(projection, "Common#592", "continue")
            self.assertEqual("FIX_PLAN", report["action"])
            self.assertTrue(report["plan_fix_required"])
            self.assertIn(
                "TOPOLOGY_MERGE_REQUIRED",
                [b["code"] for b in report["plan"]["blockers"]],
            )
            self.assertIn("PLAN: NOT_RELEASEABLE", M.render_checkpoint(report))

    def test_advisory_topology_blocker_does_not_stop_continuation(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.graph("ADVISORY")
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            projection = M.project(g, self.ledger(g), OBS_A, topology_observations=topo)
            report = M.admit(projection, "Common#592", "continue")
            self.assertEqual("CONTINUE_UNIT", report["action"])
            self.assertFalse(report["plan_fix_required"])
            self.assertIn("PLAN: WOULD_BLOCK (advisory)", M.render_checkpoint(report))

    def test_frontier_snapshots_topology_plan_and_topology_observation_input(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.init_repo(root)
            g = self.graph("ENFORCED")
            topo = self.observations(g, root, ["Common#592", "Common#594"])
            snap = M.frontier(
                g,
                self.ledger(g),
                OBS_A,
                "Common#592",
                topology_observations=topo,
            )
            self.assertIn("TOPOLOGY_MERGE_REQUIRED", snap["derived"]["plan"]["blockers"])
            self.assertIn("topology_observations", snap["inputs"])

            missing = M.frontier(
                g,
                self.ledger(g),
                OBS_A,
                "Common#592",
                topology_observations={},
            )
            drift = M.frontier_drift(snap, missing)
            self.assertEqual("MOVED", drift["status"])
            self.assertIn("TOPOLOGY_OBSERVATIONS", [row["what"] for row in drift["moved"]])
            self.assertIn("PLAN_RESULT", [row["what"] for row in drift["changed"]])

    def test_legacy_frontier_shape_does_not_gain_topology_input_when_omitted(self):
        snap = M.frontier(graph(), [], OBS_A, "Common#592")
        self.assertNotIn("topology_observations", snap["inputs"])


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
        self.assertTrue(gh.issues[594].startswith("🟡 [#527 › #588 › #594] R:P0/E0 · V1 · NOT_RELEASEABLE · NEXT:FIX_PLAN — Gate lane"), gh.issues[594])
        self.assertEqual("🟡 [#527] Π:D0/E0 · F0 · PLAN_GAP — Programme", gh.issues[527])
        self.assertEqual("🟡 [#527 › #588] Φ:D0/E0 · F0 · PLAN_GAP — Phase 3", gh.issues[588])
        self.assertIn('"releasable": false', gh.comments[594][0]["body"])
        self.assertIn("OUTCOME_MISSING", gh.comments[594][0]["body"])
        # the Coordinator states the outcome (a plan edit); nothing else changes and nobody edits a title
        self.sync(gh, not_started(planned()))
        self.assertTrue(gh.issues[594].startswith("⚪ [#527 › #588 › #594] R:P0/E0 · V1 · NOT_STARTED · NEXT:CONTINUE_UNIT — Gate lane"), gh.issues[594])
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
        g["programme"]["decomposition_policy"]["require"] = {"transformation_boundaries": True}
        leaf_of(g, "Common#592")["transformation_boundaries"] = ["WIRE_SCHEMA", "ENGINE_VALIDATION"]
        leaf_of(g, "Common#592")["integration_basis"] = "one atomic compatibility surface"
        self.assertEqual([], self.schema_errors("execution-graph", g))
        M.validate_graph(g)

    def test_malformed_decomposition_fields_fail_both(self):
        leaf = lambda g: leaf_of(g, "Common#592")  # noqa: E731
        for label, mutate in {
            "work_class": lambda g: leaf(g).__setitem__("work_class", "EPIC"),
            "size_budget key": lambda g: leaf(g).__setitem__("size_budget", {"loc": 5}),
            "write_surface glob": lambda g: leaf(g).__setitem__("write_surface", ["src/*.py"]),
            "boundary unknown": lambda g: leaf(g).__setitem__("transformation_boundaries", ["NOPE"]),
            "boundary whitespace": lambda g: leaf(g).__setitem__("transformation_boundaries", [" WIRE_SCHEMA "]),
            "boundary duplicate": lambda g: leaf(g).__setitem__("transformation_boundaries", ["WIRE_SCHEMA", "WIRE_SCHEMA"]),
            "integration blank": lambda g: leaf(g).__setitem__("integration_basis", "   "),
            "depends_on ref": lambda g: leaf(g).__setitem__("depends_on", ["x"]),
            "policy mode": lambda g: g["programme"]["decomposition_policy"].__setitem__("mode", "STRICT"),
            "policy key": lambda g: g["programme"]["decomposition_policy"].__setitem__("surprise", 1),
            "boundary require type": lambda g: g["programme"]["decomposition_policy"].__setitem__(
                "require", {"transformation_boundaries": "yes"}
            ),
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
                self.assertEqual("🟡 [#527 › #588 › #592 → PR#593] R:P0/E0 · NO_ACTIVE_UNIT · UNMATERIALIZED · NEXT:MATERIALIZE_FACTS", node["title_prefix"])
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

    def test_canonical_plan_failure_outranks_materialization(self):
        report = self.admit(g=broken(ref="Common#592"))
        self.assertEqual("FIX_PLAN", report["action"])
        self.assertTrue(report["plan_fix_required"])
        self.assertTrue(report["materialize_required"])
        self.assertIn("FIX_PLAN before coding", report["next"])
        self.assertEqual("FIX_PLAN", report["actual_next"]["action"])

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
        self.assertEqual("🟡 [#527 › #588] R:P0/E0 · NO_ACTIVE_UNIT · UNMATERIALIZED · NEXT:MATERIALIZE_FACTS — Title 588", gh.issues[588])
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
        projection = M.project(RealScenarioReplay.plan(), self.ledger(), self.observations())
        leaf = projection["nodes"][self.LEAF]
        self.assertEqual(leaf["conditions"], snapshot["derived"]["conditions"])
        self.assertEqual(leaf["actual_next"], snapshot["derived"]["actual_next"])
        self.assertNotIn("next", snapshot["derived"])
        self.assertEqual(["Common#527", "Common#588"], snapshot["lineage"])
        self.assertEqual(M.AUTHORITY, snapshot["authority"])
        self.assertEqual(snapshot, self.frontier())
        self.assertEqual(snapshot, json.loads(M.canonical_json(snapshot)))
        self.assertEqual([], M.forbidden_fields(snapshot["observed"]))  # nothing an agent could have authored is in what was observed

    def test_frontier_exposes_canonical_actual_next_not_executor_proposed_next(self):
        snapshot = self.frontier()
        self.assertNotIn("next", snapshot["derived"])
        self.assertEqual("DERIVED_ACTUAL_NEXT_ONLY", snapshot["derived"]["actual_next"]["authority"])
        self.assertEqual(
            M.project(RealScenarioReplay.plan(), self.ledger(), self.observations())["nodes"][self.LEAF]["actual_next"],
            snapshot["derived"]["actual_next"],
        )
        self.assertEqual(8, len(snapshot["derived"]["conditions"]))

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
        changed = {c["what"]: (c["was"], c["now"]) for c in drift["changed"]}
        self.assertEqual(
            {
                "STATE": ("ACTIVE", "EVIDENCE_STALE"),
                "EVIDENCE_HEALTH": ("CURRENT", "STALE_CANDIDATE"),
                "PROGRESS_E": ("1/5", "0/1"),
            },
            {key: value for key, value in changed.items() if key != "ACTUAL_NEXT"},
        )
        self.assertEqual(
            ("CONTINUE_UNIT", "RECOVER_EVIDENCE"),
            (
                changed["ACTUAL_NEXT"][0]["action"],
                changed["ACTUAL_NEXT"][1]["action"],
            ),
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
        strip = lambda nodes: {  # noqa: E731
            r: {k: v for k, v in n.items() if k not in {"health", "currentness"}}
            for r, n in nodes.items()
        }
        self.assertEqual(strip(off["nodes"]), strip(on["nodes"]))
        self.assertNotEqual(
            off["nodes"]["Common#592"]["currentness"]["graph_digest"],
            on["nodes"]["Common#592"]["currentness"]["graph_digest"],
        )
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



class SuccessorAwareHandover(unittest.TestCase):
    CHALLENGE_DIGEST = "sha256:" + "c" * 64

    @staticmethod
    def challenge_answers(ids=("Q1", "Q2", "Q3")):
        rows = []
        for qid in ids:
            row = {
                "question_id": qid,
                "evidence_refs": [f"Common#592#answer-{qid}"],
                "live_refs": [
                    {"kind": "REPOSITORY", "ref": f"path:skills/example/{qid}.py"},
                    {"kind": "PROVIDER", "ref": f"commit:{SHA_A}"},
                ],
                "evidence_summary": f"Current repository/provider evidence for {qid} establishes the requested engineering fact.",
            }
            if qid == "Q2":
                row["authority_classifications"] = ["PRODUCTION", "VALIDATION_BENCHMARK"]
            rows.append(row)
        return rows

    @staticmethod
    def root_classification():
        return {
            "classification": "EARLIEST_OWNING_LAYER",
            "owning_layer": "skills/example/runtime.py",
            "upstream_boundary": "Owner intent and plan authority",
            "downstream_boundary": "renderer / delivery consumers",
            "proof_required": "Focused exact-head regression proving the owning layer before coding",
            "evidence_refs": ["Common#592#root-evidence"],
        }

    @staticmethod
    def graph_with_policy(mode="INDEPENDENT_RECONSTRUCTION"):
        g = graph()
        leaf = next(n for n in g["nodes"] if n["ref"] == "Common#592")
        u04 = next(u for u in leaf["units"] if u["id"] == "U04")
        u04["successor_policy"] = {
            "mode": mode,
            "decision_at_risk": "ROOT_CAUSE_LAYER" if mode == "INDEPENDENT_RECONSTRUCTION" else "SAFE_CONTINUATION",
            "protected_invariants": ["P/E never moves from handover"],
        }
        return g

    @staticmethod
    def offer(mode="INDEPENDENT_RECONSTRUCTION", digest=DIGEST, decision=None, challenged=False):
        handover = {
            "event": "OFFERED",
            "mode": mode,
            "frontier_digest": digest,
            "decision_at_risk": decision or ("ROOT_CAUSE_LAYER" if mode == "INDEPENDENT_RECONSTRUCTION" else "SAFE_CONTINUATION"),
        }
        if challenged:
            handover.update({
                "challenge_digest": SuccessorAwareHandover.CHALLENGE_DIGEST,
                "question_ids": ["Q1", "Q2", "Q3"],
            })
        return facts(units=[], activity="PAUSED", handover=handover)

    @staticmethod
    def accept(
        mode="INDEPENDENT_RECONSTRUCTION",
        digest=DIGEST,
        decision=None,
        result=None,
        predecessor="offer",
        challenged=False,
        answer_ids=("Q1", "Q2", "Q3"),
        challenge_digest=None,
        include_root=True,
    ):
        h = {
            "event": "ACCEPTED",
            "mode": mode,
            "predecessor_ref": predecessor,
            "frontier_digest": digest,
            "decision_at_risk": decision or ("ROOT_CAUSE_LAYER" if mode == "INDEPENDENT_RECONSTRUCTION" else "SAFE_CONTINUATION"),
        }
        if challenged:
            h["challenge_digest"] = challenge_digest or SuccessorAwareHandover.CHALLENGE_DIGEST
            h["answer_evidence"] = SuccessorAwareHandover.challenge_answers(answer_ids)
            if include_root:
                h["root_classification"] = SuccessorAwareHandover.root_classification()
        if result is not None:
            h["result"] = result
        return facts(units=[], activity="ACTIVE", handover=h)

    def base_ledger(self):
        return [entry(facts(units=[unit("U01"), unit("U02"), unit("U03")], next={"unit": "U04", "action": "repair"}), 1)]

    def test_successor_policy_is_plan_authority_and_does_not_move_progress(self):
        base = M.project(graph(), self.base_ledger(), OBS_A)["nodes"]["Common#592"]
        planned = M.project(self.graph_with_policy(), self.base_ledger(), OBS_A)["nodes"]["Common#592"]
        self.assertEqual(base["progress"], planned["progress"])
        self.assertEqual(base["state"], planned["state"])
        self.assertEqual("INDEPENDENT_RECONSTRUCTION", planned["successor_policy"]["mode"])
        self.assertEqual("ROOT_CAUSE_LAYER", planned["successor_policy"]["decision_at_risk"])

    def test_independent_reconstruction_offer_derives_handoff_without_moving_pe(self):
        ledger = self.base_ledger() + [entry(self.offer(), 2, "offer")]
        node = M.project(self.graph_with_policy(), ledger, OBS_A)["nodes"]["Common#592"]
        self.assertEqual((75, 75), (node["progress"]["P"], node["progress"]["E"]))
        self.assertEqual("HANDOFF", node["state"])
        self.assertIn("R:P75/E75 · U04 · HANDOFF", node["title_prefix"])
        report = M.admit(M.project(self.graph_with_policy(), ledger, OBS_A), "Common#592")
        self.assertEqual("RECONCILE_HANDOFF", report["action"])
        self.assertEqual([], report["authority_effects"])

    def test_successor_acceptance_without_reconciliation_is_reconstructing(self):
        ledger = self.base_ledger() + [entry(self.offer(), 2, "offer"), entry(self.accept(), 3, "accept")]
        projection = M.project(self.graph_with_policy(), ledger, OBS_A)
        node = projection["nodes"]["Common#592"]
        self.assertEqual("RECONSTRUCTING", node["state"])
        self.assertTrue(node["handover"]["matched"])
        self.assertEqual("RECONCILE_HANDOFF", M.admit(projection, "Common#592")["action"])

    def test_matching_reconciled_acceptance_returns_to_active_and_continues_unit(self):
        ledger = self.base_ledger() + [
            entry(self.offer(), 2, "offer"),
            entry(self.accept(result="RECONCILED"), 3, "accept"),
        ]
        projection = M.project(self.graph_with_policy(), ledger, OBS_A)
        node = projection["nodes"]["Common#592"]
        self.assertEqual((75, 75), (node["progress"]["P"], node["progress"]["E"]))
        self.assertEqual("ACTIVE", node["state"])
        self.assertEqual("RECONCILED", node["handover"]["status"])
        self.assertEqual("CONTINUE_UNIT", M.admit(projection, "Common#592")["action"])

    def test_mismatched_frontier_digest_cannot_satisfy_acceptance(self):
        ledger = self.base_ledger() + [
            entry(self.offer(), 2, "offer"),
            entry(self.accept(digest="sha256:" + "e" * 64, result="RECONCILED"), 3, "accept"),
        ]
        projection = M.project(self.graph_with_policy(), ledger, OBS_A)
        node = projection["nodes"]["Common#592"]
        self.assertEqual("RECONSTRUCTING", node["state"])
        self.assertFalse(node["handover"]["matched"])
        self.assertIn("HANDOVER_ACCEPTANCE_MISMATCH", node["warnings"])
        self.assertEqual("RECONCILE_HANDOFF", M.admit(projection, "Common#592")["action"])

    def test_challenged_reconciliation_requires_exact_engineering_answer_evidence(self):
        ledger = self.base_ledger() + [
            entry(self.offer(challenged=True), 2, "offer"),
            entry(self.accept(result="RECONCILED", challenged=True), 3, "accept"),
        ]
        projection = M.project(self.graph_with_policy(), ledger, OBS_A)
        node = projection["nodes"]["Common#592"]
        self.assertEqual("RECONCILED", node["handover"]["status"])
        self.assertTrue(node["handover"]["challenge_evidence_complete"])
        self.assertEqual(["Q1", "Q2", "Q3"], node["handover"]["answered_question_ids"])
        self.assertEqual("EARLIEST_OWNING_LAYER", node["handover"]["root_classification"])
        self.assertEqual("CONTINUE_UNIT", M.admit(projection, "Common#592")["action"])

    def test_challenged_reconciliation_rejects_partial_or_stale_exam_evidence(self):
        cases = (
            (self.accept(result="RECONCILED", challenged=True, answer_ids=("Q1", "Q2")), "partial"),
            (
                self.accept(
                    result="RECONCILED",
                    challenged=True,
                    challenge_digest="sha256:" + "e" * 64,
                ),
                "wrong digest",
            ),
        )
        for accepted, label in cases:
            with self.subTest(label=label):
                ledger = self.base_ledger() + [entry(self.offer(challenged=True), 2, "offer"), entry(accepted, 3, "accept")]
                projection = M.project(self.graph_with_policy(), ledger, OBS_A)
                node = projection["nodes"]["Common#592"]
                self.assertEqual("RECONSTRUCTING", node["state"])
                self.assertFalse(node["handover"]["challenge_evidence_complete"])
                self.assertIn("HANDOVER_CHALLENGE_EVIDENCE_INCOMPLETE", node["warnings"])
                self.assertEqual("RECONCILE_HANDOFF", M.admit(projection, "Common#592")["action"])

    def test_challenged_reconciled_fact_requires_root_and_rejects_issue_prose_as_live_repo_evidence(self):
        missing_root = self.accept(result="RECONCILED", challenged=True, include_root=False)
        self.assertTrue(M.validate_facts(missing_root))
        issue_only = self.accept(result="RECONCILED", challenged=True)
        issue_only["handover"]["answer_evidence"][0]["live_refs"] = [{"kind": "REPOSITORY", "ref": "issue:Common#680"}]
        self.assertTrue(any("repository live ref" in error for error in M.validate_facts(issue_only)))

    def test_challenge_answer_cannot_author_progress_or_review_authority(self):
        base = M.project(self.graph_with_policy(), self.base_ledger(), OBS_A)["nodes"]["Common#592"]["progress"]
        ledger = self.base_ledger() + [
            entry(self.offer(challenged=True), 2, "offer"),
            entry(self.accept(result="RECONCILED", challenged=True), 3, "accept"),
        ]
        self.assertEqual(base, M.project(self.graph_with_policy(), ledger, OBS_A)["nodes"]["Common#592"]["progress"])
        bad = self.accept(result="RECONCILED", challenged=True)
        bad["handover"]["review_authority"] = "GRANTED"
        self.assertTrue(M.validate_facts(bad))

    def test_challenged_predecessor_answer_reuse_cannot_reconcile_new_offer(self):
        ledger = self.base_ledger() + [
            entry(self.offer(challenged=True), 2, "new-offer"),
            entry(self.accept(result="RECONCILED", challenged=True, predecessor="old-offer"), 3, "accept"),
        ]
        projection = M.project(self.graph_with_policy(), ledger, OBS_A)
        self.assertEqual("RECONSTRUCTING", projection["nodes"]["Common#592"]["state"])
        self.assertEqual("RECONCILE_HANDOFF", M.admit(projection, "Common#592")["action"])

    def test_continuity_offer_is_visible_but_never_becomes_a_new_gate(self):
        g = self.graph_with_policy("CONTINUITY")
        ledger = self.base_ledger() + [entry(self.offer(mode="CONTINUITY"), 2, "offer")]
        projection = M.project(g, ledger, OBS_A)
        node = projection["nodes"]["Common#592"]
        self.assertEqual("HANDOFF", node["state"])
        self.assertEqual((75, 75), (node["progress"]["P"], node["progress"]["E"]))
        self.assertEqual("CONTINUE_UNIT", M.admit(projection, "Common#592")["action"])

    def test_existing_evidence_recovery_precedes_handover_reconciliation(self):
        ledger = self.base_ledger() + [entry(self.offer(), 2, "offer")]
        projection = M.project(self.graph_with_policy(), ledger, {"Common#592": {"candidate_sha": SHA_B}})
        self.assertEqual("EVIDENCE_STALE", projection["nodes"]["Common#592"]["state"])
        self.assertEqual("RECOVER_EVIDENCE", M.admit(projection, "Common#592")["action"])

    def test_handover_facts_are_strict_and_cannot_author_progress(self):
        bad = self.offer()
        bad["handover"]["result"] = "RECONCILED"
        self.assertTrue(M.validate_facts(bad))
        bad = self.accept(result="RECONCILED")
        bad["handover"]["progress"] = 100
        self.assertTrue(M.validate_facts(bad))

    def test_independent_reconstruction_requires_decision_at_risk_in_plan(self):
        g = graph()
        leaf = next(n for n in g["nodes"] if n["ref"] == "Common#592")
        next(u for u in leaf["units"] if u["id"] == "U04")["successor_policy"] = {"mode": "INDEPENDENT_RECONSTRUCTION"}
        with self.assertRaises(M.GraphError):
            M.validate_graph(g)



class LowMemoryDecompositionRelay(unittest.TestCase):
    @staticmethod
    def serial_graph():
        g = graph()
        leaf = next(n for n in g["nodes"] if n["ref"] == "Common#594")
        leaf["depends_on"] = ["Common#592"]
        return g

    @staticmethod
    def complete_592(sha=SHA_A):
        return facts(
            sha=sha,
            units=[unit("U01"), unit("U02"), unit("U03"), unit("U04")],
            result={"scope": "RESPONSIBILITY", "responsibility_complete": "YES"},
        )

    def test_chat_memory_loss_after_checkpoint_reconstructs_the_same_exact_unit(self):
        ledger = [entry(facts(units=[unit("U01"), unit("U02")], next={"unit": "U03", "action": "continue bounded child"}), 1)]
        first = M.admit(M.project(graph(), ledger, OBS_A), "Common#592")
        second = M.admit(M.project(graph(), copy.deepcopy(ledger), copy.deepcopy(OBS_A)), "Common#592")
        self.assertEqual(("CONTINUE_UNIT", "U03"), (first["action"], first["child"]["unit"]))
        self.assertEqual(first["next"], second["next"])
        self.assertEqual(first["material"]["candidate_sha"], second["material"]["candidate_sha"])

    def test_moved_head_after_checkpoint_requires_recovery_before_new_coding(self):
        ledger = [entry(facts(units=[unit("U01"), unit("U02")]), 1)]
        report = M.admit(M.project(graph(), ledger, {"Common#592": {"candidate_sha": SHA_B}}), "Common#592")
        self.assertEqual("RECOVER_EVIDENCE", report["action"])
        self.assertTrue(report["recovery_required"])
        self.assertEqual(SHA_B, report["material"]["candidate_sha"])
        self.assertEqual(SHA_A, report["evidence_candidate"])

    def test_missing_provider_candidate_uses_canonical_wait_provider(self):
        ledger = [entry(facts(units=[unit("U01"), unit("U02")]), 1)]
        projection = M.project(graph(), ledger, {})
        report = M.admit(projection, "Common#592")
        self.assertEqual("WAIT_PROVIDER", report["action"])
        self.assertEqual("WAIT_PROVIDER", report["actual_next"]["action"])
        self.assertEqual("UNVERIFIABLE", report["evidence_health"])
        self.assertFalse(report["recovery_required"])

    def test_provider_work_without_any_facts_requires_materialization(self):
        observations = {"Common#592": {"candidate_sha": SHA_A, "pr_state": "OPEN"}}
        report = M.admit(M.project(graph(), [], observations), "Common#592")
        self.assertEqual("MATERIALIZE_FACTS", report["action"])
        self.assertTrue(report["materialize_required"])
        self.assertIsNone(report["child"]["unit"])

    def test_recovery_checkpoint_on_the_new_head_restores_the_exact_next_unit(self):
        ledger = [
            entry(facts(units=[unit("U01"), unit("U02")]), 1),
            entry(facts(sha=SHA_B, units=[unit("U01"), unit("U02")], next={"unit": "U03", "action": "resume after recovery"}), 2),
        ]
        report = M.admit(M.project(graph(), ledger, {"Common#592": {"candidate_sha": SHA_B}}), "Common#592")
        self.assertEqual(("CONTINUE_UNIT", "U03", "CURRENT"), (report["action"], report["child"]["unit"], report["evidence_health"]))

    def test_incomplete_serial_predecessor_blocks_downstream_child_without_moving_progress(self):
        g = self.serial_graph()
        before = M.project(g, [], {})["nodes"]["Common#594"]
        self.assertEqual((0, 0), (before["progress"]["P"], before["progress"]["E"]))
        self.assertEqual("WAITING_DEPENDENCY", before["state"])
        self.assertFalse(before["dependencies"]["ready"])
        self.assertEqual(["Common#592"], [row["ref"] for row in before["dependencies"]["blocking"]])
        report = M.admit(M.project(g, [], {}), "Common#594")
        self.assertEqual("WAIT_DEPENDENCY", report["action"])
        self.assertIn("Common#592:NOT_STARTED", report["next"])
        self.assertEqual((0, 0), (report["child"]["P"], report["child"]["E"]))

    def test_completed_predecessor_unblocks_downstream_child_and_keeps_its_progress_zero(self):
        g = self.serial_graph()
        ledger = [entry(self.complete_592(), 1)]
        projection = M.project(g, ledger, OBS_A)
        downstream = projection["nodes"]["Common#594"]
        self.assertTrue(downstream["dependencies"]["ready"])
        self.assertEqual((0, 0), (downstream["progress"]["P"], downstream["progress"]["E"]))
        report = M.admit(projection, "Common#594")
        self.assertEqual(("CONTINUE_UNIT", "V1"), (report["action"], report["child"]["unit"]))

    def test_superseded_predecessor_does_not_silently_satisfy_serial_order(self):
        g = self.serial_graph()
        superseded = facts(
            units=[],
            result={"scope": "RESPONSIBILITY", "responsibility_complete": "NO", "superseded_by": "Common#612"},
        )
        projection = M.project(g, [entry(superseded, 1)], OBS_A)
        self.assertEqual("SUPERSEDED", projection["nodes"]["Common#592"]["lifecycle"])
        self.assertEqual("WAITING_DEPENDENCY", projection["nodes"]["Common#594"]["state"])
        self.assertEqual("WAIT_DEPENDENCY", M.admit(projection, "Common#594")["action"])

    def test_dependency_completion_invalidates_a_handed_over_downstream_frontier(self):
        g = self.serial_graph()
        snapshot = M.frontier(g, [], {}, "Common#594")
        live = M.frontier(g, [entry(self.complete_592(), 1)], OBS_A, "Common#594")
        drift = M.frontier_drift(snapshot, live)
        self.assertEqual("MOVED", drift["status"])
        self.assertIn("DEPENDENCY_FACTS", [row["what"] for row in drift["moved"]])
        changed = {row["what"]: row for row in drift["changed"]}
        self.assertIn("DEPENDENCIES", changed)
        self.assertIn("ACTUAL_NEXT", changed)
        self.assertEqual("WAIT_DEPENDENCY", changed["ACTUAL_NEXT"]["was"]["action"])
        self.assertEqual("CONTINUE_UNIT", changed["ACTUAL_NEXT"]["now"]["action"])
        self.assertEqual("RECONCILE", drift["action"])

    def test_dependency_readiness_is_derived_and_cannot_be_authored_by_facts(self):
        bad = facts(units=[unit("U01")], dependencies={"ready": True})
        self.assertTrue(M.validate_facts(bad))



class ProjectionEndToEndAgreement(unittest.TestCase):
    def assert_four_surface_action(self, g, ledger, observations, ref, expected):
        projection = M.project(g, ledger, observations)
        node = projection["nodes"][ref]
        self.assertEqual(expected, node["actual_next"]["action"])

        status = M.status_document(
            node,
            version=1,
            digest=projection["input_digest"],
            programme=projection["programme"],
        )
        self.assertEqual(expected, status["node"]["actual_next"]["action"])

        snapshot = M.frontier(g, ledger, observations, ref)
        self.assertEqual(expected, snapshot["derived"]["actual_next"]["action"])

        report = M.admit(projection, ref)
        self.assertEqual(expected, report["actual_next"]["action"])
        self.assertEqual(expected, report["action"])

        self.assertIn(f"NEXT:{expected}", node["title_prefix"])
        return projection, node

    def test_four_surfaces_agree_for_core_replay_states(self):
        active_ledger = [
            entry(
                facts(
                    units=[unit("U01"), unit("U02"), unit("U03")],
                    next={"unit": "U04", "action": "executor prose must not become authority"},
                ),
                1,
            )
        ]
        self.assert_four_surface_action(graph(), active_ledger, OBS_A, "Common#592", "CONTINUE_UNIT")

        material_obs = {"Common#592": {"candidate_sha": SHA_A, "pr_state": "MERGED"}}
        self.assert_four_surface_action(graph(), [], material_obs, "Common#592", "MATERIALIZE_FACTS")

        stale_obs = {"Common#592": {"candidate_sha": SHA_B}}
        self.assert_four_surface_action(graph(), active_ledger, stale_obs, "Common#592", "RECOVER_EVIDENCE")

        serial = LowMemoryDecompositionRelay.serial_graph()
        self.assert_four_surface_action(serial, [], {}, "Common#594", "WAIT_DEPENDENCY")

        handover = SuccessorAwareHandover()
        handover_ledger = handover.base_ledger() + [entry(handover.offer(), 2, "offer")]
        self.assert_four_surface_action(
            handover.graph_with_policy(),
            handover_ledger,
            OBS_A,
            "Common#592",
            "RECONCILE_HANDOFF",
        )

    def test_executor_next_and_manual_title_cannot_move_decision_or_progress(self):
        first_ledger = [
            entry(
                facts(
                    units=[unit("U01"), unit("U02"), unit("U03")],
                    next={"unit": "U04", "action": "executor proposal A"},
                ),
                1,
            )
        ]
        second_ledger = [
            entry(
                facts(
                    units=[unit("U01"), unit("U02"), unit("U03")],
                    next={"unit": "U04", "action": "executor proposal B"},
                ),
                1,
            )
        ]
        first = M.project(graph(), first_ledger, OBS_A)
        second = M.project(graph(), second_ledger, OBS_A)
        a = first["nodes"]["Common#592"]
        b = second["nodes"]["Common#592"]
        self.assertEqual(a["progress"], b["progress"])
        self.assertEqual(a["actual_next"]["action"], b["actual_next"]["action"])
        self.assertEqual(a["title_prefix"], b["title_prefix"])

        forged_title = M.render_title(
            a["title_prefix"].replace("NEXT:CONTINUE_UNIT", "NEXT:PUBLISH_RESULT"),
            "manual edit",
        )
        drift = M.title_drift(forged_title, a["title_prefix"], "manual edit")
        self.assertEqual("STALE_OR_HAND_EDITED", drift["status"])
        self.assertEqual("CONTINUE_UNIT", a["actual_next"]["action"])


if __name__ == "__main__":
    unittest.main()
