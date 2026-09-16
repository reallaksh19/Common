from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"))
from validate_checkpoint_linkage import validate as checkpoint_linkage
from validate_issue_closure import validate as issue_closure
from validate_phase_transition_questions import validate as phase_questions
from validate_roadmap_transaction import validate as roadmap_transaction
from validate_state_planes import validate as state_planes
from validate_supersession import validate as supersession

def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

class LifecycleTransactionStressTests(unittest.TestCase):
    def test_checkpoint_baton_must_route_to_active_ep(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            state={"active_ep":{"id":"EP-2","path":"agents/relay/execution-packages/EP-2.yaml"},"last_checkpoint":{"id":"CP-1","path":"agents/relay/checkpoints/CP-1.yaml"},"current_position":{"work_package":"WP-2"}}
            ep={"identity":{"previous_checkpoint":"CP-1"}}
            cp={"schema_version":"relay-v2.5","checkpoint_id":"CP-1","ep_id":"EP-1","roadmap_basis":{"roadmap_id":"RM-X","revision":"RM-1"},"implementation_result":{},"acceptance_results":[],"validation_results":[],"quality_findings":[],"discoveries":[],"roadmap_reconciliation":{"result":"STATUS_UPDATE"},"successor":{"frontier_work_package":"WP-2","ep_id":"EP-2"}}
            dump(root/"agents/relay/REPO_STATE.yaml",state);dump(root/"agents/relay/execution-packages/EP-2.yaml",ep);dump(root/"agents/relay/checkpoints/CP-1.yaml",cp)
            self.assertEqual([],checkpoint_linkage(root)[0])
            cp["successor"]["ep_id"]="EP-WRONG";dump(root/"agents/relay/checkpoints/CP-1.yaml",cp)
            self.assertTrue(any("successor.ep_id" in x for x in checkpoint_linkage(root)[0]))

    def test_active_hard_stop_cannot_claim_execution_can_continue(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            state={"status_planes":{"execution":{"state":"WAITING","can_continue":True,"next_action":"Wait for owner decision."},"quality":{"state":"CLEAR","findings":[]},"evidence":{"state":"PARTIAL","summary":"Evidence retained","not_run":[]},"stop":{"active":True,"category":"OWNER_DECISION_REQUIRED","reason":"Owner intent must be resolved.","basis":["ODR-PROPOSAL-1"]}}}
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            self.assertTrue(any("can_continue=false" in x for x in state_planes(root)[0]))

    def test_owner_mutation_revision_must_match_frontier_and_new_progress_basis(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            roadmap={"schema_version":"relay-v2.5","roadmap":{"id":"RM-X","revision":"RM-2","title":"Synthetic roadmap","revision_record":"agents/relay/roadmap/revisions/RM-2.yaml"},"objectives":[{"id":"OBJ-1","state":"ACTIVE","definition":"DEFINED","phases":[{"id":"PHASE-1","state":"ACTIVE","definition":"DETAILED","work_packages":[{"id":"WP-1","state":"COMPLETE","definition":"DETAILED","execution_status":"TERMINAL","depends_on":[]},{"id":"WP-2","state":"ACTIVE","definition":"DETAILED","execution_status":"ACTIVE","depends_on":["WP-1"]}]}]}]}
            state={"roadmap":{"path":"agents/relay/roadmap/OVERALL_ROADMAP.yaml"}}
            progress={"progress_basis":{"id":"PB-2","roadmap_revision":"RM-2"}}
            odr={"status":"APPLIED"}
            revision={"revision":{"from_revision":"RM-1","to_revision":"RM-2","classification":"OWNER_INTENT_MUTATION","trigger":{"type":"OWNER_DECISION","path":"agents/relay/roadmap/owner-decisions/ODR-1.yaml"}},"changes":{"added":["WP-2"],"removed":[],"changed":["PHASE-1"],"unaffected":["WP-1"]},"progress_basis_change":{"old_basis":"PB-1","new_basis":"PB-2","old_total_weight":100,"new_total_weight":140},"frontier_after":["WP-2"]}
            dump(root/"agents/relay/REPO_STATE.yaml",state);dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress);dump(root/"agents/relay/roadmap/owner-decisions/ODR-1.yaml",odr);dump(root/"agents/relay/roadmap/revisions/RM-2.yaml",revision)
            self.assertEqual([],roadmap_transaction(root)[0])
            revision["frontier_after"]=["WP-1"];dump(root/"agents/relay/roadmap/revisions/RM-2.yaml",revision)
            self.assertTrue(any("frontier_after" in x for x in roadmap_transaction(root)[0]))

    def test_phase_transition_questions_must_be_structurally_grounded_in_incoming_ep(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            state={"active_ep":{"path":"agents/relay/execution-packages/EP-2.yaml"}}
            ep={"roadmap_source":{"phase":"PHASE-2","work_package":"WP-2"},"inputs":[{"id":"INPUT-1"}],"acceptance":[{"id":"AC-1"}],"validation":[{"id":"TEST-1"}],"implementation_plan":[{"id":"STEP-1"}],"phase_transition":{"required":True,"from_phase":"PHASE-1","to_phase":"PHASE-2","questions":[
                {"id":"Q1","focus":"PRODUCTION_PATH","anchors":["PHASE-2","WP-2"],"question":"Trace the incoming production path."},
                {"id":"Q2","focus":"ENGINEERING_PROBLEM","anchors":["WP-2","INPUT-1"],"question":"Explain the incoming engineering problem."},
                {"id":"Q3","focus":"BOUNDARIES_INVARIANTS","anchors":["WP-2","AC-1"],"question":"State the incoming boundaries and invariants."},
                {"id":"Q4","focus":"VERIFICATION","anchors":["AC-1","TEST-1"],"question":"Explain how the incoming result is independently verified."},
                {"id":"Q5","focus":"FIRST_SAFE_SLICE","anchors":["STEP-1","AC-1"],"question":"Identify the first safe bounded contribution."},
            ]}}
            dump(root/"agents/relay/REPO_STATE.yaml",state);dump(root/"agents/relay/execution-packages/EP-2.yaml",ep)
            self.assertEqual([],phase_questions(root)[0])
            ep["phase_transition"]["questions"][1]["anchors"]=["OLD-PHASE-ANCHOR"];dump(root/"agents/relay/execution-packages/EP-2.yaml",ep)
            self.assertTrue(any("not present in incoming EP" in x for x in phase_questions(root)[0]))

    def test_supersession_requires_successor_to_receive_exact_transfer(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            transfer={"unresolved_acceptance":["AC-9"],"inputs":["INPUT-3"],"risks":["RISK-2"],"decisions":["DEC-4"],"evidence":["EV-7"]}
            graph={"nodes":[
                {"id":"ISSUE-OLD","state":"SUPERSEDED","supersession_receipt":{"successor":"ISSUE-NEW",**transfer}},
                {"id":"ISSUE-NEW","state":"OPEN","supersession_inheritance":{"predecessor":"ISSUE-OLD",**transfer}},
            ],"relationships":[{"from":"ISSUE-NEW","relation":"SUPERSEDES","to":"ISSUE-OLD"}]}
            dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph)
            self.assertEqual([],supersession(root)[0])
            graph["nodes"][1]["supersession_inheritance"]["unresolved_acceptance"]=[];dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph)
            self.assertTrue(any("transfer mismatch" in x for x in supersession(root)[0]))

    def test_issue_cannot_close_before_terminal_roadmap_and_receipts(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            state={"roadmap":{"path":"agents/relay/roadmap/OVERALL_ROADMAP.yaml"}}
            roadmap={"objectives":[{"id":"OBJ","phases":[{"id":"PHASE","work_packages":[{"id":"WP-1","state":"ACTIVE"}]}]}]}
            graph={"nodes":[{"id":"ISSUE-1","state":"CLOSED","roadmap_node":"WP-1","closure_receipt":{"acceptance_terminal":False,"evidence_terminal":True,"pr_disposition":"MERGED","remaining_work_disposition":"NONE","checkpoint":"CP-1"}}],"relationships":[]}
            dump(root/"agents/relay/REPO_STATE.yaml",state);dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph)
            errors=issue_closure(root)[0]
            self.assertTrue(any("non-terminal roadmap node" in x for x in errors))
            self.assertTrue(any("acceptance is not terminal" in x for x in errors))

if __name__=="__main__":unittest.main()
