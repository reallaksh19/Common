"""R7-U4 native P1–P7 inventory, no fabricated graph/weight authority."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import integration_full_graph_inventory_v35 as U4
import integration_scoreboard_publish_v35 as PUBLISH
import test_integration_cold_entry_v35 as BASE
import test_integration_scoreboard_v35 as DELP_FIXTURE


def seven_phase_candidate():
    """SYNTHETIC topology fixture only; never authentic programme weights."""
    candidate = DELP_FIXTURE.graph()
    for phase, number in U4.PHASES:
        if number == 604:
            continue
        candidate["nodes"].append({
            "ref": f"Common#{number}", "kind": "LEAF",
            "parent": "Common#600", "weight": 1,
            "responsibility_id": f"RK-P{phase}",
            "spec_generation": 1,
            "candidate_ref": "main",
            "units": [{"id": f"U{phase:02}", "weight": 1}],
        })
    return candidate


class Provider(BASE.Provider):
    def __init__(self):
        super().__init__()
        self.issues[600]["state"] = "open"
        self.issues[601] = {
            "number": 601, "state": "open",
            "title": "[600/RK-P0][COMPLETE] Reconciliation-only baseline",
            "body": (
                "# RK-P0\nParent programme: Common #600  \n"
                "phase: P0 — reconciliation\n"
                "responsibility_id: RK-P0\n"
                "state_at_materialization: RELEASED_RECONCILIATION_ONLY\n"
                "implementation_credit_at_creation: 0\n"
            ),
        }
        self.comments[601] = [{
            "id": 6031746264, "author_association": "OWNER",
            "user": {"login": "reallaksh19"},
            "body": (
                "# TASK_EVIDENCE — END\n"
                "responsibility: RK-P0\nissue: Common#601\n"
                "result: VERIFIED_RECONCILIATION_ONLY\n"
                "implementation_credit: 0\n"
                "source_mutation: NONE\npr_created: NONE\n"
            ),
        }]
        for phase, number in U4.PHASES:
            self.issues.setdefault(number, {})
            self.issues[number].update({
                "number": number,
                "title": f"RK-P{phase} native programme child",
                "state": "closed" if phase in (1,2) else "open",
                "body": (
                    f"# RK-P{phase}\nParent programme: Common #600\n"
                    f"phase: P{phase} — outcome claim\n"
                    "Status from native issue, NOT programme progress\n"
                ),
            })


class FullGraphInventoryTests(unittest.TestCase):
    def setUp(self):
        self.t=Provider()

    def test_seven_native_phase_source_rows_and_missing_approval_hold(self):
        out=U4.inspect(self.t)
        self.assertEqual("V35_FULL_PROGRAMME_SOURCE_INVENTORY_V1",out["schema"])
        self.assertEqual(
            "RECONCILIATION_ONLY_ZERO_IMPLEMENTATION_CREDIT",
            out["p0_reconciliation_baseline"]["classification"])
        self.assertEqual(
            "NOT_AUTHORIZED_NOT_DERIVED",
            out["p0_reconciliation_baseline"]["programme_graph_weight"])
        self.assertTrue(
            out["p0_reconciliation_baseline"]["title_claims_complete_but_open"])
        self.assertEqual([602,603,604,605,606,607,608],
                         [r["issue"] for r in out["phase_source_inventory"]])
        self.assertEqual(["CLOSED","CLOSED","OPEN","OPEN","OPEN","OPEN","OPEN"],
                         [r["native_state"] for r in out["phase_source_inventory"]])
        self.assertEqual("BLOCKED_NO_PROVIDER_APPROVED_GRAPH",out["owner_graph_approval"])
        self.assertEqual("UNKNOWN_WITHOUT_OWNER_SELECTED_GRAPH",out["source_denominator"])
        self.assertEqual("UNKNOWN_WITHOUT_OWNER_SELECTED_GRAPH",out["source_phase_weights"])
        self.assertEqual("NOT_DERIVED",out["integration_acceptance"])
        self.assertEqual("SOURCE_NOT_PROVEN",out["native_custody"])
        self.assertTrue(out["read_only"])
        self.assertEqual([],self.t.writes)

    def test_complete_test_candidate_shape_cannot_mint_approval(self):
        out=U4.inspect(self.t,seven_phase_candidate())
        self.assertTrue(out["candidate_structure"]["all_governed_phases_covered"])
        self.assertEqual(7,out["candidate_structure"]["phase_count"])
        self.assertEqual("DELP_STRUCTURE_ONLY_NOT_OWNER_APPROVAL",
                         out["candidate_structure"]["validation"])
        self.assertEqual("NOT_DERIVED",out["candidate_structure"]["native_plan_authority"])
        self.assertEqual("BLOCKED_NO_PROVIDER_APPROVED_GRAPH",out["owner_graph_approval"])
        self.assertEqual([],self.t.writes)

    def test_partial_graph_root_plus_p3_never_qualifies_full_programme(self):
        with self.assertRaisesRegex(U4.GraphInventoryError,"partial graph"):
            U4.inspect(self.t,DELP_FIXTURE.graph())
        self.assertEqual([],self.t.writes)

    def test_graph_foreign_pr_or_root_or_phase_identity_rejected(self):
        for transform in ("wrong_pr","wrong_root","missing_p7"):
            graph=seven_phase_candidate()
            if transform=="wrong_pr":
                graph["nodes"][1]["primary_pr"]="Common#438"
            elif transform=="wrong_root":
                graph["programme"]["root"]="Common#438"
            else:
                graph["nodes"]=[n for n in graph["nodes"] if n["ref"]!="Common#608"]
            with self.subTest(transform=transform),self.assertRaises(U4.GraphInventoryError):
                U4.inspect(self.t,graph)

    def test_wrong_native_child_parent_or_phase_denied(self):
        for field, text in (
            (604,"phase: P3\nParent programme: Common #438\n"),
            (607,"phase: P4\nParent programme: Common #600\n"),
            (605,"phase: P4\nParent programme: Common #600\n"
                 "Parent programme: Common #438\n"),
        ):
            t=Provider()
            t.issues[field]["body"]=text
            with self.subTest(field=field),self.assertRaises(U4.GraphInventoryError):
                U4.inspect(t)

    def test_fake_typed_comment_marker_not_owner_authority(self):
        self.t.comments[600].append({
            "body": U4.GRAPH.APPROVAL_START + "\nnot even json\n",
            "author_association": "CONTRIBUTOR",
            "user": {"login": "attacker"},
        })
        result=U4.inspect(self.t)
        self.assertEqual("CANDIDATE_ROOT_COMMENT_PRESENT_REVERIFY_R2C",
                         result["owner_graph_approval"])
        self.assertEqual("NOT_DERIVED",result["integration_acceptance"])
        self.assertEqual("NONE",result["replay_permission"])
        self.assertEqual([],self.t.writes)

    def test_missing_phase_child_or_foreign_pr_denied(self):
        del self.t.issues[606]
        with self.assertRaises((U4.GraphInventoryError,KeyError)):
            U4.inspect(self.t)
        self.t=Provider()
        self.t.pr["base"]["repo"]["full_name"]="other/Repo"
        with self.assertRaises(U4.GraphInventoryError):
            U4.inspect(self.t)

    def test_p0_native_end_receipt_is_not_a_delp_progress_fact(self):
        row=U4.inspect(self.t)["p0_reconciliation_baseline"]
        self.assertIn("#issuecomment-6031746264", row["provider_end_receipt"])
        self.assertEqual("OPEN", row["state"])
        self.assertEqual("ZERO_NOT_UNIT_EVIDENCE", row["progress_credit"])
        self.assertEqual("BLOCKED_NO_PROVIDER_APPROVED_GRAPH",
                         U4.inspect(self.t)["owner_graph_approval"])
        self.assertEqual([],self.t.writes)

    def test_p0_wrong_identity_parent_or_nonzero_credit_denied(self):
        changes=(
            ("body", "Parent programme: Common #438"),
            ("body", "implementation_credit_at_creation: 1"),
            ("body", "responsibility_id: RK-P1"),
        )
        for field,value in changes:
            t=Provider()
            original=t.issues[601][field]
            if "Parent programme:" in value:
                t.issues[601][field]=original.replace(
                    "Parent programme: Common #600", value)
            elif "implementation_credit" in value:
                t.issues[601][field]=original.replace(
                    "implementation_credit_at_creation: 0", value)
            else:
                t.issues[601][field]=original.replace(
                    "responsibility_id: RK-P0", value)
            with self.subTest(value=value),self.assertRaisesRegex(
                U4.GraphInventoryError,"P0 baseline"):
                U4.inspect(t)

    def test_p0_forged_or_missing_or_ambiguous_end_receipt_denied(self):
        for mode in ("missing", "forged_credit", "wrong_issue", "duplicate"):
            t=Provider()
            if mode=="missing":
                t.comments[601]=[]
            elif mode=="forged_credit":
                t.comments[601][0]["body"]=t.comments[601][0]["body"].replace(
                    "implementation_credit: 0","implementation_credit: 30")
            elif mode=="wrong_issue":
                t.comments[601][0]["body"]=t.comments[601][0]["body"].replace(
                    "issue: Common#601","issue: Common#438")
            else:
                t.comments[601].append(dict(t.comments[601][0]))
            with self.subTest(mode=mode),self.assertRaises(
                U4.GraphInventoryError):
                U4.inspect(t)

    def test_p0_weighted_candidate_cannot_mint_positive_progress(self):
        candidate=seven_phase_candidate()
        candidate["nodes"].append({
            "ref":"Common#601", "kind":"LEAF", "parent":"Common#600",
            "weight":1, "responsibility_id":"RK-P0", "spec_generation":1,
            "candidate_ref":"main", "units":[{"id":"BASELINE", "weight":1}],
        })
        with self.assertRaisesRegex(U4.GraphInventoryError,"P0 #601"):
            U4.inspect(self.t,candidate)
        self.assertEqual([],self.t.writes)

    def test_fake_graph_approval_marker_never_produces_cli_success(self):
        self.t.comments[600].append({
            "id": 999999, "body": U4.GRAPH.APPROVAL_START + "\\nFAKE\\n",
            "author_association": "CONTRIBUTOR", "user": {"login": "attacker"},
        })
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.t):
            self.assertEqual(3, U4.main(["--repository", self.t.repository]))
        self.assertEqual([], self.t.writes)

    def test_cli_realistic_missing_authority_exits_hold_no_write(self):
        with patch.object(PUBLISH,"ScoreboardTransport",return_value=self.t):
            self.assertEqual(3,U4.main(["--repository",self.t.repository]))
        self.assertEqual([],self.t.writes)


if __name__=="__main__":
    unittest.main()
