from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]))
from test_core import good,dump
from validate_roadmap_continuity import validate as continuity
from validate_execution_frontier import validate as frontier
from validate_ep_staleness import validate as staleness


def revision(frm,to,unaffected=None,changed=None,removed=None):
    return {
        "schema_version":"relay-v2.5",
        "revision":{"id":to,"from_revision":frm,"to_revision":to,"classification":"EXECUTION_DERIVED_STATUS","trigger":{"type":"CHECKPOINT","ref":"CP-X"}},
        "changes":{"added":[],"removed":removed or [],"changed":changed or [],"unaffected":unaffected or []},
        "invalidated_execution_packages":[],"issue_graph_reconciled":False,
        "progress_basis_change":{"old_basis":"PB-1","new_basis":"PB-1","old_total_weight":100,"new_total_weight":100},
        "frontier_after":["WP-1"],"notes":[],
    }


def continuity_repo(root:Path,disposition="CONTINUE_UNCHANGED",changed=False):
    roadmap,ep,progress,state=good(root)
    roadmap["roadmap"]["revision"]="RM-0003"
    roadmap["roadmap"]["revision_record"]="agents/relay/roadmap/revisions/RM-0003.yaml"
    state["roadmap"]["revision"]="RM-0003"
    state["projection"]["roadmap_revision"]="RM-0003"
    progress["progress_basis"]["roadmap_revision"]="RM-0003"
    state["active_ep"]["continuity_receipt"]="agents/relay/roadmap/continuity/RC-1.yaml"
    if disposition=="RECONCILE_REQUIRED":
        state["active_ep"]["state"]="RECONCILING"
        state["status_planes"]["execution"].update({"state":"WAITING","can_continue":True,"material_authority":"READ_ONLY","next_action":"Regenerate the EP contract against RM-0003 before engineering writes."})
    r2=revision("RM-0001","RM-0002",unaffected=["WP-1"])
    r3=revision("RM-0002","RM-0003",unaffected=[] if changed else ["WP-1"],changed=["WP-1"] if changed else [])
    impact={"work_package_definition_changed":False,"dependencies_changed":False,"acceptance_changed":changed,"scope_authority_changed":False,"protected_invariants_changed":False}
    receipt={
        "schema_version":"relay-v2.5-roadmap-continuity","id":"RC-1","ep_id":"EP-1","work_package":"WP-1",
        "from_revision":"RM-0001","to_revision":"RM-0003",
        "revision_chain":[{"path":"agents/relay/roadmap/revisions/RM-0002.yaml"},{"path":"agents/relay/roadmap/revisions/RM-0003.yaml"}],
        "disposition":disposition,"impact_checks":impact,"basis":["RM-0002","RM-0003"],
    }
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress);dump(root/"agents/relay/REPO_STATE.yaml",state)
    dump(root/"agents/relay/roadmap/revisions/RM-0002.yaml",r2);dump(root/"agents/relay/roadmap/revisions/RM-0003.yaml",r3);dump(root/"agents/relay/roadmap/continuity/RC-1.yaml",receipt)
    return roadmap,ep,progress,state,receipt,r2,r3


class RoadmapContinuityStressTests(unittest.TestCase):
    def test_long_running_ep_can_continue_across_multiple_explicitly_unaffected_revisions(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);continuity_repo(root)
            self.assertEqual([],continuity(root)[0]);self.assertEqual([],frontier(root)[0]);self.assertEqual([],staleness(root)[0])

    def test_revision_mismatch_without_receipt_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state,_,_,_=continuity_repo(root);state["active_ep"].pop("continuity_receipt");dump(root/"agents/relay/REPO_STATE.yaml",state)
            self.assertTrue(any("continuity_receipt is required" in x for x in continuity(root)[0]))

    def test_false_unaffected_claim_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);continuity_repo(root,changed=True)
            self.assertTrue(any("explicitly unaffected" in x for x in continuity(root)[0]))

    def test_changed_active_contract_can_remain_recoverable_only_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);continuity_repo(root,disposition="RECONCILE_REQUIRED",changed=True)
            self.assertEqual([],continuity(root)[0]);self.assertEqual([],frontier(root)[0]);self.assertEqual([],staleness(root)[0])

    def test_reconcile_required_cannot_keep_write_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state,_,_,_=continuity_repo(root,disposition="RECONCILE_REQUIRED",changed=True);state["status_planes"]["execution"]["material_authority"]="WRITE";dump(root/"agents/relay/REPO_STATE.yaml",state)
            self.assertTrue(any("material_authority READ_ONLY" in x for x in continuity(root)[0]))

    def test_missing_middle_revision_breaks_continuity_chain(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,_,receipt,_,_=continuity_repo(root);receipt["revision_chain"]=receipt["revision_chain"][1:];dump(root/"agents/relay/roadmap/continuity/RC-1.yaml",receipt)
            self.assertTrue(any("does not continue expected" in x for x in continuity(root)[0]))

    def test_invalidated_ep_cannot_remain_active(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);continuity_repo(root,disposition="INVALIDATED",changed=True)
            self.assertTrue(any("cannot remain attached to an ACTIVE EP" in x for x in continuity(root)[0]))

if __name__=="__main__":unittest.main()
