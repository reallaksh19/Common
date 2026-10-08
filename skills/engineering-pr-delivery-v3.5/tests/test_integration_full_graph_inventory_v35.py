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

    def test_cli_realistic_missing_authority_exits_hold_no_write(self):
        with patch.object(PUBLISH,"ScoreboardTransport",return_value=self.t):
            self.assertEqual(3,U4.main(["--repository",self.t.repository]))
        self.assertEqual([],self.t.writes)


if __name__=="__main__":
    unittest.main()
