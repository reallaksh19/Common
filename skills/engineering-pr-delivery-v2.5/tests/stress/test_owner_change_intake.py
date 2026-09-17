from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"))
from owner_change_projection import build
from render_owner_change import render
from validate_owner_change_intake import validate

def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def fixture(root:Path,*,status="APPLIED",with_intake=True,issue_reconciled=True,classify_active=True):
    state={"roadmap":{"path":"agents/relay/roadmap/OVERALL_ROADMAP.yaml"},"active_ep":{"id":"EP-2","path":"agents/relay/execution-packages/EP-2.yaml","state":"RECONCILING"},"current_position":{"work_package":"WP-2"}}
    roadmap={"schema_version":"relay-v2.5","roadmap":{"id":"RM-X","revision":"RM-2","title":"Synthetic roadmap","revision_record":"agents/relay/roadmap/revisions/RM-2.yaml"},"objectives":[{"id":"OBJ-1","state":"ACTIVE","definition":"DEFINED","phases":[{"id":"PHASE-1","state":"ACTIVE","definition":"DETAILED","work_packages":[{"id":"WP-1","state":"COMPLETE","definition":"DETAILED","execution_status":"TERMINAL","depends_on":[]},{"id":"WP-2","state":"ACTIVE","definition":"DETAILED","execution_status":"ACTIVE","depends_on":["WP-1"]}]}]}]}
    progress={"progress_basis":{"id":"PB-2","roadmap_revision":"RM-2"}}
    odr={"schema_version":"relay-v2.5","id":"ODR-1","decision":{"authority":"OWNER","kind":"INTENT_MUTATION","statement":"Expand the approved behavior while preserving the existing safety invariant.","source":"owner-message:synthetic"},"effects":{"requirement_disposition":"NOT_APPLICABLE","grants_material_write_authority":False,"pending_items":[]},"impact":{"class":["PHASE"]},"affected":{"objectives":[],"phases":["PHASE-1"],"work_packages":["WP-2"],"execution_packages":["EP-2"],"issues":["ISSUE-2"]},"required_reconciliation":["recompute frontier","reconcile progress basis","reconcile issue graph"],"status":status}
    if with_intake:odr["change_intake"]={"previous_concept":"Only the original behavior is authorized.","requested_concept":"Add the newly approved behavior while retaining the safety invariant.","retained_behavior":["Existing safety invariant remains unchanged."],"invalidated_behavior":["Prior no-expansion assumption is invalid."],"new_scope":["Implement the newly approved behavior."]}
    changed=["PHASE-1"] + (["WP-2"] if classify_active else [])
    unaffected=["WP-1"]
    revision={"schema_version":"relay-v2.5","revision":{"id":"RM-2","from_revision":"RM-1","to_revision":"RM-2","classification":"OWNER_INTENT_MUTATION","trigger":{"type":"OWNER_DECISION","path":"agents/relay/roadmap/owner-decisions/ODR-1.yaml"}},"changes":{"added":[],"removed":[],"changed":changed,"unaffected":unaffected},"invalidated_execution_packages":[],"issue_graph_reconciled":issue_reconciled,"progress_basis_change":{"old_basis":"PB-1","new_basis":"PB-2","old_total_weight":100,"new_total_weight":120},"frontier_after":["WP-2"],"notes":[]}
    issue={"nodes":[{"id":"ISSUE-2","state":"ACTIVE","github_state":"OPEN"}],"relationships":[]}
    dump(root/"agents/relay/REPO_STATE.yaml",state);dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress);dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",issue);dump(root/"agents/relay/roadmap/owner-decisions/ODR-1.yaml",odr);dump(root/"agents/relay/roadmap/revisions/RM-2.yaml",revision)
    return odr,revision,progress

class OwnerChangeIntakeStressTests(unittest.TestCase):
    def test_applied_owner_change_projects_semantic_and_structural_impact(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);fixture(root)
            self.assertEqual([],validate(root)[0]);p=build(root)
            self.assertTrue(p["decision"]["applied_to_current_roadmap"]);self.assertEqual("RECONCILE_REQUIRED",p["current_ep_disposition"]["disposition"]);self.assertEqual(["WP-2"],p["new_frontier"])
            text=render(root);self.assertIn("Existing safety invariant remains unchanged.",text);self.assertIn("PB-1 → PB-2",text);self.assertIn("ISSUE-2",text)

    def test_current_owner_mutation_requires_change_intake(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);fixture(root,with_intake=False)
            self.assertTrue(any("requires change_intake" in x for x in validate(root)[0]))

    def test_issue_impact_cannot_claim_reconciled_when_revision_did_not(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);fixture(root,issue_reconciled=False)
            self.assertTrue(any("affecting issues requires issue_graph_reconciled" in x for x in validate(root)[0]))

    def test_active_work_must_have_explicit_disposition(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);fixture(root,classify_active=False)
            self.assertTrue(any("explicitly classify the active EP" in x for x in validate(root)[0]))

    def test_progress_basis_and_frontier_are_source_bound(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,rev,progress=fixture(root)
            progress["progress_basis"]["id"]="PB-STALE";dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress)
            self.assertTrue(any("progress basis is stale" in x for x in validate(root)[0]))
            progress["progress_basis"]["id"]="PB-2";dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress);rev["frontier_after"]=["WP-1"];dump(root/"agents/relay/roadmap/revisions/RM-2.yaml",rev)
            self.assertTrue(any("new_frontier" in x for x in validate(root)[0]))

    def test_pending_change_is_visible_but_not_applied(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);odr,_,_=fixture(root,status="CAPTURED")
            # Remove the applied revision link and make current roadmap an execution-derived revision.
            roadmap=load_yaml(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml");roadmap["roadmap"]["revision_record"]=None;dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap)
            (root/"agents/relay/roadmap/revisions/RM-2.yaml").unlink()
            p=build(root,root/"agents/relay/roadmap/owner-decisions/ODR-1.yaml")
            self.assertFalse(p["decision"]["applied"]);self.assertIsNone(p["new_frontier"]);self.assertIn("Not yet applied",render(root,root/"agents/relay/roadmap/owner-decisions/ODR-1.yaml"))

# local import after helpers to keep fixture section compact
from relaylib import load_yaml
if __name__=="__main__":unittest.main()
