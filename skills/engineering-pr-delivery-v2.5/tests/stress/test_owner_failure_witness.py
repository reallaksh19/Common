from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[2]/"scripts"))
sys.path.insert(0,str(HERE.parents[1]))

from test_core import good,dump
from relaylib import load_yaml
from publish_owner_progress import publish
from validate_human_communication import validate as communication_check
from validate_checkpoint import validate_file as checkpoint_check


class OwnerFailureWitnessStressTests(unittest.TestCase):
    def test_admission_only_local_git_gate_owner_control_picture(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,state=good(root)

            # Current work has a real issue and PR before the publication baseline.
            dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",{
                "schema_version":"relay-v2.5",
                "nodes":[{
                    "id":"ISSUE-410",
                    "state":"ACTIVE",
                    "github_state":"OPEN",
                    "github":{"issue_number":410,"issue_id":"gid-410","url":"https://github.com/owner/repo/issues/410"},
                    "roadmap_node":"WP-1",
                }],
                "relationships":[],
            })
            obs={
                "schema_version":"relay-v2.5-delivery-observation",
                "id":"DOBS-411",
                "provider":"GITHUB",
                "repository":"owner/repo",
                "vehicle":{
                    "kind":"PULL_REQUEST","number":411,"url":"https://github.com/owner/repo/pull/411",
                    "lifecycle":"OPEN",
                    "head":{"ref":"agent/work","sha":"head-411"},
                    "base":{"ref":"main","sha":"base-1"},
                },
                "mergeability":{"state":"MERGEABLE"},
                "checks":{"state":"PASS","head_sha":"head-411","required":["ci"],"observations":[{"name":"ci","state":"PASS"}]},
                "review":{"state":"CLEAR","unresolved_threads":0,"change_requests":0},
                "description_contract":{
                    "marker":"<!-- relay-pr-correlation:v1 -->",
                    "marker_present":True,
                    "body_digest":"sha256:witness-body",
                    "correlations":[{
                        "issue_node":"ISSUE-410","issue_number":410,"ep_id":"EP-1",
                        "ep_path":"agents/relay/execution-packages/EP-1.yaml","work_package":"WP-1",
                        "relationship":"IMPLEMENTS","meaning":"EP-1 delivers WP-1 for issue #410.",
                    }],
                },
                "readback_basis":["provider-readback:witness"],
            }
            dpath="agents/relay/delivery/DOBS-411.yaml";dump(root/dpath,obs)
            state["repository"]["remote"]="owner/repo"
            state["delivery"]={
                "required":True,"provider":"GITHUB",
                "observation":{"id":"DOBS-411","path":dpath},
                "observations":[{"id":"DOBS-411","path":dpath}],
            }

            # Baseline CP already says no product files changed and no roadmap structure change.
            cp_path=root/"agents/relay/checkpoints/CP-1.yaml"
            cp={
                "schema_version":"relay-v2.5",
                "contract_version":2,
                "checkpoint_id":"CP-1",
                "ep_id":"EP-1",
                "roadmap_basis":{"roadmap_id":"RM-T","revision":"RM-0001"},
                "execution_basis":{"material_ref":"abc"},
                "implementation_result":{
                    "summary":"Repository admission basis established; no product files changed.",
                    "completed_steps":["Admission basis established."],
                    "files_changed":[],
                },
                "acceptance_results":[],
                "validation_results":[],
                "quality_review":None,
                "quality_findings":[],
                "known_limitations":[],
                "discoveries":[],
                "roadmap_reconciliation":{
                    "result":"NO_ROADMAP_CHANGE",
                    "status_updates":[],
                    "proposals":[],
                    "owner_decisions_required":[],
                },
                "remaining_work":["Run the real local Git admission gate before product implementation."],
                "successor":{
                    "mode":"SERIAL","frontier_work_package":"WP-1","ep_id":"EP-1",
                    "parallel_plan":None,"lane_id":None,"lanes":[],
                },
            }
            dump(cp_path,cp)
            self.assertEqual([],checkpoint_check(cp_path)[0])

            state["last_checkpoint"]={"id":"CP-1","path":"agents/relay/checkpoints/CP-1.yaml"}
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            first=publish(root,apply=True)
            self.assertEqual("INITIAL_SNAPSHOT",first["event_class"])

            # Meaningful next event: custody/admission moved, but engineering acceptance/files did not.
            state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
            state["takeover_admissions"]=[{
                "candidate_id":"candidate-witness",
                "state":"ADMITTED",
                "basis":["admission:witness"],
            }]
            state["status_planes"]["execution"]={
                "state":"WAITING",
                "can_continue":False,
                "material_authority":"READ_ONLY",
                "next_action":"Run the real local Git admission gate in a usable checkout.",
            }
            state["status_planes"]["evidence"]={
                "state":"NOT_RUN",
                "summary":"The required real local Git gate has not run.",
                "not_run":[{
                    "id":"TEST-1",
                    "reason":"The current environment has source files but no usable Git object database.",
                    "cause":"UNAVAILABLE_TOOL",
                }],
            }
            dump(root/"agents/relay/REPO_STATE.yaml",state)

            ep=load_yaml(root/"agents/relay/execution-packages/EP-1.yaml")
            ep["outcome"]={
                "user_visible":["Owner retains control while repository admission is proven before implementation."],
                "engineering":["No product implementation begins until the real Git admission gate succeeds."],
            }
            ep["next_work"]["steps"][0]["execution_requirement"]={
                "id":"EXECREQ-LOCAL-GIT",
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
                    "prompt":"In a real Git checkout at the admitted revision, run ./tools/verify-admission --require-git. Do not change product files. Post the exact command, exit status and TEST-1 evidence back to this issue.",
                    "publication":{"target":"CURRENT_WORK_ISSUE","method":"COMMENT","local_result_update":"SAME_LOCATION","readback_required":True},
                    "response_check":{"timer_required":True,"timer_title":"Admission gate response","after_minutes":30,"selection_reason":"This is a single bounded local Git verification.","terminate_when":"CONTROL_OBLIGATION_NOT_OPEN","on_due":"Check the current work issue for TEST-1 evidence and reconcile.","on_no_response":"Report WAITING and recheck only if useful."},
                },
            }
            dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)

            result=publish(root,apply=False)
            text=result["owner_status"]

            self.assertEqual("EVIDENCE_PROGRESS",result["event_class"])
            self.assertIn("Acceptance/progress did not move.",text)
            self.assertIn("No newly recorded implementation/file change occurred",text)
            self.assertIn("Issue #410",text)
            self.assertIn("Owner retains control while repository admission is proven before implementation.",text)
            self.assertIn("Overall progress: **50%**",text)
            self.assertIn("active execution-package progress: **50%**",text)
            self.assertIn("The required real local Git gate has not run.",text)
            self.assertIn("./tools/verify-admission --require-git",text)
            self.assertIn("A real Git checkout with a usable .git object database.",text)
            self.assertIn("The current environment has source files but no usable Git object database.",text)
            self.assertIn("product implementation start",text)
            self.assertIn("product implementation may begin",text)
            self.assertIn("Last checkpoint roadmap reconciliation: **No Roadmap Change**",text)
            self.assertIn("PR #411",text)
            self.assertIn("Exact-head checks: **Pass**",text)
            self.assertIn("technically ready to merge: **NO**",text)
            self.assertIn("merge authorization: **Not Granted**",text)
            self.assertIn("No Owner decision is currently required",text)
            self.assertIn("Unmerged PRs carried forward",text)
            self.assertIn("Issue #410 ↔ EP-1 / WP-1",text)
            self.assertEqual([],communication_check(root)[0])


if __name__=="__main__":
    unittest.main()
