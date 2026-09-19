from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[2]/"scripts"))
sys.path.insert(0,str(HERE.parents[1]))

from test_core import good,dump
from validate_handover_plan import validate as handover_check
from prepare_handover_projection import prepare as prepare_handover_projection
from handover_planning import (
    build_handover_plan,
    parse_handover_command,
    render_generator_request,
    render_issue_body,
)


class HandoverPlanningStressTests(unittest.TestCase):
    def test_verified_current_issue_wins_over_task_and_roadmap(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
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
            plan=build_handover_plan(root)
            self.assertEqual("READY",plan["status"])
            self.assertEqual("GITHUB_ISSUE",plan["work_contract"]["kind"])
            self.assertEqual(410,plan["work_contract"]["issue"]["issue_number"])
            self.assertEqual(410,plan["issue_strategy"]["parent_issue_number"])

    def test_active_task_is_fallback_when_no_verified_issue_exists(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            plan=build_handover_plan(root)
            self.assertEqual("ACTIVE_TASK",plan["work_contract"]["kind"])
            self.assertEqual("EP-1",plan["work_contract"]["id"])
            self.assertEqual([],handover_check(root)[0])

    def test_roadmap_work_package_is_fallback_when_no_issue_or_active_ep_exists(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root)
            state["relay_state"]="IDLE"
            state["active_ep"]={"id":None,"path":None,"state":"NONE"}
            state["status_planes"]["execution"]={"state":"WAITING","can_continue":False,"material_authority":"NONE","next_action":"No active EP."}
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            plan=build_handover_plan(root)
            self.assertEqual("ROADMAP_WORK_PACKAGE",plan["work_contract"]["kind"])
            self.assertEqual("WP-1",plan["work_contract"]["id"])

    def test_pending_intent_combines_acceptance_and_next_work_without_calling_activity_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            plan=build_handover_plan(root)
            kinds={x["kind"] for x in plan["intent"]}
            self.assertIn("ACCEPTANCE",kinds)
            self.assertIn("NEXT_WORK",kinds)
            self.assertTrue(any(x["id"]=="AC:AC-1" for x in plan["intent"]))
            self.assertTrue(any(x["id"]=="NEXT:EP-1:1" for x in plan["intent"]))

    def test_inputs_and_benchmarks_have_durable_full_definition_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            plan=build_handover_plan(root)
            self.assertEqual("agents/relay/execution-packages/EP-1.yaml#inputs/INPUT-1",plan["inputs"][0]["definition_path"])
            self.assertEqual("agents/relay/execution-packages/EP-1.yaml#benchmarks/BENCH-1",plan["benchmarks"][0]["definition_path"])

    def test_same_ownership_boundary_has_stable_handover_key_for_incremental_update(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            first=build_handover_plan(root,owner_requirements=["Preserve the current acceptance contract."])
            second=build_handover_plan(root,owner_requirements=["Preserve the current acceptance contract.","Keep GitHub linkage truthful."])
            self.assertEqual(first["issue_strategy"]["handover_key"],second["issue_strategy"]["handover_key"])
            self.assertEqual("UPDATE_MATCHING_OPEN_HANDOVER_ISSUE_FOR_SAME_KEY_ELSE_CREATE",second["issue_strategy"]["reuse_rule"])

    def test_owner_session_requirements_are_in_issue_body_but_sensitive_material_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            plan=build_handover_plan(root,owner_requirements=["Keep progress acceptance-derived."])
            self.assertIn("Keep progress acceptance-derived.",render_issue_body(plan))
            rejected=build_handover_plan(root,owner_requirements=["api_key=do-not-publish"])
            self.assertEqual("ERROR",rejected["status"])
            self.assertTrue(any("sensitive" in x.lower() for x in rejected["errors"]))

    def test_plain_handover_does_not_force_complex_q1_q5(self):
        mode=parse_handover_command("Plan for Handover")
        self.assertEqual("READY",mode["status"])
        self.assertFalse(mode["complex_project"])
        self.assertFalse(mode["visible_q1_q5"])

    def test_complex_project_command_enables_visible_q1_q5_but_stays_three_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            mode=parse_handover_command("Plan for Handover , complex project")
            self.assertTrue(mode["complex_project"])
            self.assertEqual([],handover_check(root,complex_project=True)[0])
            plan=build_handover_plan(
                root,
                complex_project=mode["complex_project"],
                handover_issue_url="https://github.com/owner/repo/issues/500",
            )
            self.assertEqual("THREE_PASS_ONLY",plan["generator"]["mode"])
            self.assertTrue(plan["generator"]["complex_mode"])
            self.assertTrue(plan["generator"]["visible_q1_q5"])
            request=render_generator_request(plan)
            self.assertIn("COMPLEX MODE: ON",request)
            self.assertIn("TARGET:\nhttps://github.com/owner/repo/issues/500",request)

    def test_generator_request_waits_for_verified_handover_issue_readback(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            plan=build_handover_plan(root)
            self.assertEqual("AWAITING_HANDOVER_ISSUE_READBACK",plan["generator"]["target_status"])
            with self.assertRaises(ValueError):
                render_generator_request(plan)


    def test_handover_projection_prepares_create_with_stable_marker(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            result=prepare_handover_projection(root)
            self.assertEqual("READY",result["status"])
            self.assertEqual("CREATE_HANDOVER_ISSUE",result["action"])
            self.assertEqual("CREATE",result["proposed_generation"]["operations"][0]["kind"])
            body=result["proposed_generation"]["operations"][0]["desired"]["body_projection"]
            self.assertIn(result["handover_key"],body)
            self.assertIn("relay-operation:",body)
            node=next(x for x in result["proposed_issue_graph"]["nodes"] if x.get("id")==result["issue_node"])
            self.assertEqual("HANDOVER",node["role"])
            self.assertEqual("ABSENT",node["github_state"])

    def test_handover_projection_relates_new_handover_node_to_verified_source_issue(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
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
            result=prepare_handover_projection(root)
            self.assertEqual("READY",result["status"])
            self.assertIn(
                {"from":result["issue_node"],"relation":"RELATES_TO","to":"ISSUE-410"},
                result["proposed_issue_graph"]["relationships"],
            )
            self.assertEqual(410,result["relationship"]["source_issue_number"])
            self.assertEqual("UNVERIFIED",result["relationship"]["native_parent_claim"])

    def test_existing_open_handover_node_is_updated_not_duplicated(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            plan=build_handover_plan(root)
            key=plan["issue_strategy"]["handover_key"]
            dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",{
                "schema_version":"relay-v2.5",
                "nodes":[{
                    "id":"HANDOVER-EXISTING",
                    "role":"HANDOVER",
                    "handover_key":key,
                    "state":"ACTIVE",
                    "github_state":"OPEN",
                    "github":{"issue_number":501,"issue_id":"gid-501","url":"https://github.com/owner/repo/issues/501"},
                    "source_contract":{"kind":"ACTIVE_TASK","id":"EP-1","work_package":"WP-1"},
                }],
                "relationships":[],
            })
            result=prepare_handover_projection(root)
            self.assertEqual("UPDATE_HANDOVER_ISSUE",result["action"])
            self.assertEqual("PUBLISH_HANDOVER",result["proposed_generation"]["operations"][0]["kind"])
            self.assertEqual("HANDOVER-EXISTING",result["issue_node"])
            handover_nodes=[x for x in result["proposed_issue_graph"]["nodes"] if x.get("role")=="HANDOVER"]
            self.assertEqual(1,len(handover_nodes))

    def test_multiple_equally_authoritative_current_issues_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",{
                "schema_version":"relay-v2.5",
                "nodes":[
                    {"id":"ISSUE-A","state":"ACTIVE","github_state":"OPEN","github":{"issue_number":1},"roadmap_node":"WP-1"},
                    {"id":"ISSUE-B","state":"ACTIVE","github_state":"OPEN","github":{"issue_number":2},"roadmap_node":"WP-1"},
                ],
                "relationships":[],
            })
            plan=build_handover_plan(root)
            self.assertEqual("ERROR",plan["status"])
            self.assertEqual("AMBIGUOUS",plan["work_contract"]["status"])


if __name__=="__main__":
    unittest.main()
