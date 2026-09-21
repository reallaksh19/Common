from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]))
from test_core import good,write_clear_quality_review,dump
from communication_projection import build as communication
from render_owner_status import render as owner_status
from render_technical_status import render as technical_status
from validate_human_communication import validate as communication_check
from validate_ep_semantics import validate as ep_semantics
from takeoverlib import digest_mapping,yaml_digest

class HumanCommunicationStressTests(unittest.TestCase):
    def test_owner_and_technical_views_share_one_report_projection(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);c=communication(root);report=c["technical"]["report"]
            self.assertEqual(digest_mapping(report),c["generated_from"]["report_projection_digest"])
            self.assertEqual([],communication_check(root)[0])
            owner=owner_status(root);technical=technical_status(root)
            self.assertIn("Implement the bounded synthetic result.",owner)
            self.assertIn("EP-1",technical)
            for token in ("BATON_READY","TAKEOVER_CERTIFIED","MATERIAL_WRITE_READY","REPO_STATE","QRV-"):self.assertNotIn(token,owner)


    def test_owner_view_projects_current_outcome_from_active_ep(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root)
            ep["outcome"]={
                "user_visible":["Owner can verify the bounded capability outcome."],
                "engineering":["The bounded capability invariant is preserved."],
            }
            dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            text=owner_status(root)
            self.assertIn("Owner can verify the bounded capability outcome.",text)
            self.assertIn("The bounded capability invariant is preserved.",text)
            self.assertEqual([],communication_check(root)[0])

    def test_owner_reserved_choice_is_not_invented_as_decision_required_now(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);c=communication(root)
            self.assertEqual([],c["owner"]["decisions"]["required_now"])
            self.assertTrue(c["owner"]["decisions"]["reserved"])
            self.assertIn("No Owner decision is currently required",owner_status(root))

    def test_owner_decision_hard_stop_is_visible_and_plain(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["status_planes"]["execution"]={"state":"WAITING","can_continue":False,"material_authority":"READ_ONLY","next_action":"Wait for product-direction decision."};s["status_planes"]["stop"]={"active":True,"category":"OWNER_DECISION_REQUIRED","reason":"Choose whether the accepted behavior should change before implementation continues.","basis":["owner-intent-boundary"]};dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertEqual([],communication_check(root)[0]);text=owner_status(root)
            self.assertIn("Choose whether the accepted behavior should change",text)
            self.assertIn("## Owner decisions",text)

    def test_missing_evidence_cannot_be_hidden(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["status_planes"]["evidence"]={"state":"NOT_RUN","summary":"A required environment check has not executed.","not_run":[{"id":"TEST-1","reason":"The external runner was unavailable.","cause":"UNAVAILABLE_TOOL"}]};dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertEqual([],communication_check(root)[0]);self.assertIn("The external runner was unavailable.",owner_status(root))

    def test_nonblocking_quality_risk_is_visible_without_fake_stop(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,s=good(root);ptr=write_clear_quality_review(root,ep);qpath=root/ptr["path"];q=yaml.safe_load(qpath.read_text())
            q["procedure_results"][0]["result"]="FINDINGS";q["findings"]=[{"id":"QF-1","blueprint":"coding","classification":"MAINTAINABILITY","severity":"HIGH","disposition":"DEFERRED","statement":"A bounded maintainability cleanup remains after this slice.","evidence":["review:module"],"blocks_execution":False,"hard_stop":None}];q["overall_state"]="NEEDS_ATTENTION";q["successor_handover"]={"unresolved_findings":["QF-1"],"follow_up":["Address the bounded cleanup in an authorized maintenance slice."]};dump(qpath,q);ptr["digest"]=yaml_digest(qpath)
            cp={"schema_version":"relay-v2.5","checkpoint_id":"CP-1","ep_id":"EP-1","roadmap_basis":{"roadmap_id":"RM-T","revision":"RM-0001"},"execution_basis":{"material_ref":"abc"},"implementation_result":{},"acceptance_results":[],"validation_results":[],"quality_review":ptr,"quality_findings":[{"id":"QF-1"}],"known_limitations":[],"discoveries":[],"roadmap_reconciliation":{"result":"NO_ROADMAP_CHANGE","status_updates":[],"proposals":[],"owner_decisions_required":[]},"remaining_work":[],"successor":{"mode":"SERIAL","frontier_work_package":"WP-1","ep_id":"EP-1","parallel_plan":None,"lane_id":None,"lanes":[]}};dump(root/"agents/relay/checkpoints/CP-1.yaml",cp);s["last_checkpoint"]={"id":"CP-1","path":"agents/relay/checkpoints/CP-1.yaml"};s["status_planes"]["quality"]={"state":"NEEDS_ATTENTION","findings":[{"statement":"A bounded maintainability cleanup remains after this slice.","severity":"HIGH","classification":"MAINTAINABILITY","disposition":"DEFERRED","blocks_execution":False}]};dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertEqual([],communication_check(root)[0]);text=owner_status(root)
            self.assertIn("A bounded maintainability cleanup remains after this slice.",text)
            self.assertNotIn("Engineering work is stopped",text)

    def test_owner_view_tracks_next_work_source_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["next_work"]["steps"][0]["action"]="Run the bounded migration rehearsal.";ep["next_work"]["steps"][0]["expected_result"]="The rehearsal proves the next implementation action is safe.";dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            text=owner_status(root);self.assertIn("Run the bounded migration rehearsal.",text);self.assertIn("The rehearsal proves the next implementation action is safe.",text);self.assertEqual([],communication_check(root)[0])



    def test_owner_view_shows_each_acceptance_status_percent_and_basis(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            text=owner_status(root)
            self.assertIn("AC-1",text)
            self.assertIn("In Progress",text)
            self.assertIn("50%",text)
            self.assertIn("basis: synthetic-progress",text)
            self.assertEqual([],communication_check(root)[0])

    def test_owner_view_projects_current_issue_identity_and_ep_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            graph={
                "schema_version":"relay-v2.5",
                "nodes":[{
                    "id":"ISSUE-1",
                    "state":"ACTIVE",
                    "github_state":"OPEN",
                    "github":{"issue_number":410,"issue_id":"gid-410","url":"https://github.com/owner/repo/issues/410"},
                    "roadmap_node":"WP-1",
                }],
                "relationships":[],
            }
            dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph)
            projection=communication(root);work=projection["owner"]["current_work"]
            self.assertEqual("ISSUE-1",work["issues"][0]["id"])
            self.assertEqual(410,work["issues"][0]["issue_number"])
            text=owner_status(root)
            self.assertIn("Issue #410",text)
            self.assertIn("https://github.com/owner/repo/issues/410",text)
            self.assertIn("active execution-package progress: **50%**",text)
            self.assertEqual([],communication_check(root)[0])


    def test_external_local_gate_is_actionable_in_owner_view(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root)
            ep["next_work"]["steps"][0]["execution_requirement"]={
                "id":"EXECREQ-1",
                "type":"LOCAL_ENVIRONMENT",
                "actor":"AUTHORIZED_OPERATOR",
                "environment":{"kind":"REAL_GIT_CHECKOUT","description":"A real Git checkout with a usable .git object database."},
                "command":"./tools/verify-admission --require-git",
                "instruction":None,
                "working_directory":"REPOSITORY_ROOT",
                "required_basis":["current EP material_ref"],
                "unavailable_here_reason":"The current environment has source files but no usable Git object database.",
                "expected_evidence":["TEST-1"],
                "blocks":["product implementation start"],
                "success_condition":"The command exits successfully against the admitted revision.",
                "clears":["repository-admission gate","product implementation may begin"],
                "delegation":{
                    "mode":"LOCAL_AGENT","control_obligation_id":"DLG-TEST-1","monitor_role":"READ_ONLY",
                    "prompt":"Open the repository at the admitted revision. Run the required local verification exactly as stated. Do not modify unrelated files. Post the command, exit status, key output and evidence result back to the same GitHub issue location.",
                    "publication":{"target":"CURRENT_WORK_ISSUE","method":"COMMENT","local_result_update":"SAME_LOCATION","readback_required":True},
                    "response_check":{"timer_required":True,"timer_title":"Local verification response","after_minutes":30,"selection_reason":"This is one bounded command expected to complete quickly.","terminate_when":"CONTROL_OBLIGATION_NOT_OPEN","on_due":"Read the current work issue for the local-agent result and reconcile the evidence.","on_no_response":"Report WAITING truthfully and schedule another check only if it remains useful."},
                },
            }
            dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertEqual([],ep_semantics(root)[0])
            self.assertEqual([],communication_check(root)[0])
            text=owner_status(root)
            for expected in (
                "./tools/verify-admission --require-git",
                "A real Git checkout with a usable .git object database.",
                "The current environment has source files but no usable Git object database.",
                "TEST-1",
                "product implementation start",
                "repository-admission gate",
                "product implementation may begin",
                "Local-agent handoff",
                "Local verification response",
                "30 minutes",
                "Copy-paste prompt for the local agent",
            ):self.assertIn(expected,text)

    def test_external_execution_requirement_needs_command_or_instruction(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root)
            ep["next_work"]["steps"][0]["execution_requirement"]={
                "id":"EXECREQ-1",
                "type":"EXTERNAL_ENVIRONMENT",
                "actor":"AUTHORIZED_OPERATOR",
                "environment":{"kind":"EXTERNAL_RUNNER","description":"The required external runner."},
                "command":None,
                "instruction":None,
                "working_directory":"REPOSITORY_ROOT",
                "required_basis":["current EP material_ref"],
                "unavailable_here_reason":"The runner is not accessible from this environment.",
                "expected_evidence":["TEST-1"],
                "blocks":["acceptance evidence"],
                "success_condition":"The required validation completes.",
                "clears":["acceptance evidence gap"],
                "delegation":{
                    "mode":"LOCAL_AGENT","control_obligation_id":"DLG-TEST-1","monitor_role":"READ_ONLY",
                    "prompt":"Open the repository at the admitted revision. Run the required local verification exactly as stated. Do not modify unrelated files. Post the command, exit status, key output and evidence result back to the same GitHub issue location.",
                    "publication":{"target":"CURRENT_WORK_ISSUE","method":"COMMENT","local_result_update":"SAME_LOCATION","readback_required":True},
                    "response_check":{"timer_required":True,"timer_title":"Local verification response","after_minutes":60,"selection_reason":"This is This external runner may require setup before the check completes.","terminate_when":"CONTROL_OBLIGATION_NOT_OPEN","on_due":"Read the current work issue for the local-agent result and reconcile the evidence.","on_no_response":"Report WAITING truthfully and schedule another check only if it remains useful."},
                },
            }
            dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("requires command or executable instruction" in x for x in ep_semantics(root)[0]))

    def test_owner_view_rejects_internal_jargon_in_user_facing_source_text(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["context_capsule"]["known_problems"]=["REPO_STATE contains a confusing internal-only status."];dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("relay-internal jargon" in x for x in communication_check(root)[0]))

    def test_external_execution_requirement_requires_local_agent_delegation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root)
            ep["next_work"]["steps"][0]["execution_requirement"]={
                "id":"EXECREQ-1","type":"LOCAL_ENVIRONMENT","actor":"AUTHORIZED_OPERATOR",
                "environment":{"kind":"BROWSER_UI","description":"A local browser session."},
                "instruction":"Open the UI and exercise the required workflow.",
                "working_directory":"REPOSITORY_ROOT","required_basis":["current EP material_ref"],
                "unavailable_here_reason":"No browser UI is available in this environment.",
                "expected_evidence":["TEST-1"],"blocks":["UI acceptance"],"success_condition":"The workflow is verified.",
                "clears":["UI acceptance gap"],
            }
            dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("delegation must be a mapping" in x for x in ep_semantics(root)[0]))

    def test_delegation_response_timer_is_bounded_to_30_or_60_minutes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root)
            req={
                "id":"EXECREQ-1","type":"LOCAL_ENVIRONMENT","actor":"AUTHORIZED_OPERATOR",
                "environment":{"kind":"BROWSER_UI","description":"A local browser session."},
                "instruction":"Open the UI and exercise the required workflow.",
                "working_directory":"REPOSITORY_ROOT","required_basis":["current EP material_ref"],
                "unavailable_here_reason":"No browser UI is available in this environment.",
                "expected_evidence":["TEST-1"],"blocks":["UI acceptance"],"success_condition":"The workflow is verified.",
                "clears":["UI acceptance gap"],
                "delegation":{
                    "mode":"LOCAL_AGENT","control_obligation_id":"DLG-TEST-1","monitor_role":"READ_ONLY","prompt":"Run the browser verification and post evidence to the same issue.",
                    "publication":{"target":"CURRENT_WORK_ISSUE","method":"COMMENT","local_result_update":"SAME_LOCATION","readback_required":True},
                    "response_check":{"timer_required":True,"timer_title":"Browser verification response","after_minutes":45,"selection_reason":"Invalid interval for regression.","terminate_when":"CONTROL_OBLIGATION_NOT_OPEN","on_due":"Check the issue.","on_no_response":"Report waiting."},
                },
            }
            ep["next_work"]["steps"][0]["execution_requirement"]=req
            dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("after_minutes must be 30 or 60" in x for x in ep_semantics(root)[0]))

    def test_owner_control_return_has_canonical_roadmap_macro(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            text=owner_status(root)
            for expected in (
                "# Owner Roadmap",
                "## Executive state",
                "Overall progress:",
                "Current phase:",
                "Current work:",
                "Current issue:",
                "Current PR:",
                "Roadmap disposition:",
                "## Phase status",
                "## Concept roadmap",
                "## Active work",
                "## Completed work log",
                "## Newly discovered work",
                "## Blocked / waiting",
                "## Recommended forward sequence",
                "## Roadmap revision history",
            ):
                self.assertIn(expected,text)

if __name__=="__main__":unittest.main()
