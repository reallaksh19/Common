from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[2]/"scripts"))
sys.path.insert(0,str(HERE.parents[1]))

from test_core import good,dump
from append_roadmap_event import append_event
from handover_planning import build_handover_plan,render_issue_body
from render_roadmap import render as render_roadmap
from validate_roadmap_events import validate as roadmap_events_check


def event(event_id="EVT-1",concept_change="NO_CONCEPT_CHANGE",follow_up="NEW_EXECUTION_WORK"):
    return {
        "id":event_id,
        "sequence":999,
        "event_class":"ENGINEERING_DISCOVERY",
        "summary":"A material engineering discovery changed the execution work needed under the existing concept.",
        "concept_refs":["OBJ-1","PHASE-1"],
        "execution_refs":{
            "work_package":"WP-1",
            "execution_package":"EP-1",
            "checkpoint":None,
            "issue":410,
            "pull_request":411,
        },
        "basis":["agents/relay/execution-packages/EP-1.yaml"],
        "concept_change":concept_change,
        "roadmap_revision":{"id":None,"path":None},
        "follow_up":follow_up,
    }


class RoadmapEventStressTests(unittest.TestCase):
    def test_missing_event_ledger_is_backward_compatible(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            self.assertEqual([],roadmap_events_check(root)[0])
            self.assertIn("No roadmap events have been recorded.",render_roadmap(root))

    def test_append_event_links_concept_and_execution_without_mutating_roadmap(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);roadmap,_,_,_=good(root)
            proposal=root/"event.yaml";dump(proposal,event())
            before=copy.deepcopy(roadmap)
            result=append_event(root,proposal,apply=True)
            self.assertEqual("OK",result["status"])
            self.assertEqual(1,result["event"]["sequence"])
            self.assertEqual([],roadmap_events_check(root)[0])
            self.assertEqual(before, __import__("relaylib").load_yaml(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml"))
            text=render_roadmap(root)
            self.assertIn("## Concept roadmap",text)
            self.assertIn("## Execution under the concepts",text)
            self.assertIn("EVT-1 / ENGINEERING_DISCOVERY",text)
            self.assertIn("OBJ-1, PHASE-1",text)
            self.assertIn("WP WP-1",text)

    def test_work_package_cannot_masquerade_as_concept_ref(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            bad=event();bad["concept_refs"]=["WP-1"]
            dump(root/"event.yaml",bad)
            result=append_event(root,root/"event.yaml")
            self.assertEqual("ERROR",result["status"])
            self.assertTrue(any("is a work package" in x for x in result["errors"]))

    def test_proposed_concept_change_routes_to_roadmap_proposal_or_owner_decision(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            bad=event(concept_change="CONCEPT_CHANGE_PROPOSED",follow_up="NEW_EXECUTION_WORK")
            dump(root/"event.yaml",bad)
            result=append_event(root,root/"event.yaml")
            self.assertEqual("ERROR",result["status"])
            self.assertTrue(any("proposed concept change" in x for x in result["errors"]))

    def test_applied_concept_change_requires_real_roadmap_revision_record(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            bad=event(concept_change="CONCEPT_CHANGE_APPLIED",follow_up="NONE")
            bad["event_class"]="ROADMAP_REVISION"
            bad["roadmap_revision"]={"id":"RM-0002","path":"agents/relay/roadmap/revisions/RM-0002.yaml"}
            dump(root/"event.yaml",bad)
            result=append_event(root,root/"event.yaml")
            self.assertEqual("ERROR",result["status"])
            self.assertTrue(any("roadmap revision path missing" in x for x in result["errors"]))

            dump(root/"agents/relay/roadmap/revisions/RM-0002.yaml",{
                "schema_version":"relay-v2.5",
                "revision":{"id":"RM-0002","from_revision":"RM-0001","to_revision":"RM-0002","classification":"OWNER_INTENT_MUTATION","trigger":{"type":"OWNER_DECISION","ref":"ODR-1"}},
                "changes":{"added":[],"removed":[],"changed":[],"unaffected":[]},
                "invalidated_execution_packages":[],
                "issue_graph_reconciled":False,
                "progress_basis_change":{"old_basis":"PB-1","new_basis":"PB-1","old_total_weight":100,"new_total_weight":100},
                "frontier_after":["WP-1"],
            })
            result=append_event(root,root/"event.yaml",apply=True)
            self.assertEqual("OK",result["status"])
            self.assertEqual([],roadmap_events_check(root)[0])

    def test_ledger_is_append_only_through_producer(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            first=root/"first.yaml";second=root/"second.yaml"
            dump(first,event("EVT-1"));dump(second,event("EVT-2"))
            append_event(root,first,apply=True)
            first_snapshot=__import__("relaylib").load_yaml(root/"agents/relay/roadmap/ROADMAP_EVENTS.yaml")["events"][0]
            result=append_event(root,second,apply=True)
            self.assertEqual(2,result["event"]["sequence"])
            ledger=__import__("relaylib").load_yaml(root/"agents/relay/roadmap/ROADMAP_EVENTS.yaml")
            self.assertEqual(first_snapshot,ledger["events"][0])
            self.assertEqual(["EVT-1","EVT-2"],[x["id"] for x in ledger["events"]])

    def test_handover_receives_recent_concept_events_as_context_not_intent(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            dump(root/"event.yaml",event())
            append_event(root,root/"event.yaml",apply=True)
            plan=build_handover_plan(root)
            self.assertEqual("EVT-1",plan["recent_concept_events"][0]["id"])
            self.assertFalse(any(x.get("id")=="EVT-1" for x in plan["intent"]))
            text=render_issue_body(plan)
            self.assertIn("## Recent concept-linked material events",text)
            self.assertIn("EVT-1 / ENGINEERING_DISCOVERY",text)


if __name__=="__main__":
    unittest.main()
