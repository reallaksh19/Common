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
from pr_correlation import derive_current_correlations,render_markdown
from validate_pr_correlation import validate as correlation_check
from render_owner_status import render as owner_status
from report_projection import build as build_report


def issue_graph(root:Path,wp="WP-1"):
    graph={
        "schema_version":"relay-v2.5",
        "nodes":[{
            "id":"ISSUE-410",
            "state":"ACTIVE",
            "github_state":"OPEN",
            "github":{"issue_number":410,"issue_id":"gid-410","url":"https://github.com/owner/repo/issues/410"},
            "roadmap_node":wp,
        }],
        "relationships":[],
    }
    dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",graph)
    return graph


def observation(number:int=411,lifecycle:str="OPEN",ep_id:str="EP-1",ep_path:str="agents/relay/execution-packages/EP-1.yaml",wp:str="WP-1"):
    return {
        "schema_version":"relay-v2.5-delivery-observation",
        "id":f"DOBS-{number}",
        "provider":"GITHUB",
        "repository":"owner/repo",
        "vehicle":{
            "kind":"PULL_REQUEST","number":number,"url":f"https://github.com/owner/repo/pull/{number}",
            "lifecycle":lifecycle,"head":{"ref":f"agent/pr-{number}","sha":f"head-{number}"},"base":{"ref":"main","sha":"base-1"},
        },
        "mergeability":{"state":"MERGEABLE"},
        "checks":{"state":"PASS","head_sha":f"head-{number}","required":["ci"],"observations":[{"name":"ci","state":"PASS"}]},
        "review":{"state":"CLEAR","unresolved_threads":0,"change_requests":0},
        "description_contract":{
            "marker":"<!-- relay-pr-correlation:v1 -->","marker_present":True,"body_digest":f"sha256:body-{number}",
            "correlations":[{
                "issue_node":"ISSUE-410","issue_number":410,"ep_id":ep_id,"ep_path":ep_path,"work_package":wp,
                "relationship":"IMPLEMENTS","meaning":f"{ep_id} delivers {wp} for issue #410.",
            }],
        },
        "readback_basis":[f"provider-readback:pr-{number}"],
    }


def track(root:Path,state:dict,observations:list[dict],primary:int=0):
    pointers=[]
    for obs in observations:
        path=f"agents/relay/delivery/{obs['id']}.yaml";dump(root/path,obs);pointers.append({"id":obs["id"],"path":path})
    state["repository"]["remote"]="owner/repo"
    state["delivery"]={"required":True,"provider":"GITHUB","observation":pointers[primary],"observations":pointers}
    dump(root/"agents/relay/REPO_STATE.yaml",state)


class PrCorrelationStressTests(unittest.TestCase):
    def test_canonical_pr_block_contains_issue_ep_wp_and_meaning(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);issue_graph(root)
            rows,errors=derive_current_correlations(root)
            self.assertEqual([],errors)
            self.assertEqual(1,len(rows))
            text=render_markdown(rows)
            self.assertIn("<!-- relay-pr-correlation:v1 -->",text)
            self.assertIn("#410",text)
            self.assertIn("EP-1",text)
            self.assertIn("WP-1",text)
            self.assertIn("IMPLEMENTS",text)
            self.assertIn("Issue node",text)

    def test_meaningful_correlation_requires_issue_and_ep_same_work_package(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root);issue_graph(root,wp="WP-OTHER")
            track(root,state,[observation()])
            errors=correlation_check(root)[0]
            self.assertTrue(any("not meaningfully correlated to the same roadmap work package" in x for x in errors))

    def test_current_active_ep_must_exist_in_nonterminal_pr_description(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root);issue_graph(root)
            other=copy.deepcopy(observation());other["description_contract"]["correlations"][0]["ep_id"]="EP-OTHER"
            track(root,state,[other])
            errors=correlation_check(root)[0]
            self.assertTrue(any("active EP EP-1 is not declared" in x for x in errors))

    def test_task_close_checkpoint_ep_must_be_verified_in_tracked_pr_description(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root);issue_graph(root);track(root,state,[observation()])
            cp_path="agents/relay/checkpoints/CP-CLOSE.yaml"
            dump(root/cp_path,{"ep_id":"EP-CLOSED-TASK"})
            state=__import__("relaylib").load_yaml(root/"agents/relay/REPO_STATE.yaml")
            state["last_checkpoint"]={"id":"CP-CLOSE","path":cp_path};dump(root/"agents/relay/REPO_STATE.yaml",state)
            errors=correlation_check(root)[0]
            self.assertTrue(any("task-close checkpoint EP EP-CLOSED-TASK" in x for x in errors))

    def test_two_open_prs_are_both_carried_forward_in_every_owner_summary(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root);issue_graph(root)
            track(root,state,[observation(411),observation(412)])
            delivery=build_report(root)["delivery"]
            self.assertEqual([411,412],[x["vehicle"]["number"] for x in delivery["unmerged_prs"]])
            text=owner_status(root)
            self.assertIn("Unmerged PRs carried forward",text)
            self.assertIn("PR #411",text)
            self.assertIn("PR #412",text)
            self.assertGreaterEqual(text.count("Issue #410 ↔ EP-1 / WP-1"),2)

    def test_merged_pr_stays_in_evidence_but_leaves_unmerged_carry_forward(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root);issue_graph(root)
            track(root,state,[observation(411,"OPEN"),observation(412,"MERGED")])
            delivery=build_report(root)["delivery"]
            self.assertEqual([411],[x["vehicle"]["number"] for x in delivery["unmerged_prs"]])
            text=owner_status(root)
            carry=text.split("- Unmerged PRs carried forward:",1)[1].split("## Action required outside this environment",1)[0]
            self.assertIn("PR #411",carry)
            self.assertNotIn("PR #412",carry)

    def test_unknown_pr_is_carried_until_provider_state_is_resolved(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root);issue_graph(root)
            unknown=observation(413,"UNKNOWN");unknown["mergeability"]={"state":"UNKNOWN"};unknown["checks"]={"state":"UNKNOWN","head_sha":None,"required":[],"observations":[]};unknown["review"]={"state":"UNKNOWN","unresolved_threads":None,"change_requests":None}
            track(root,state,[unknown])
            delivery=build_report(root)["delivery"]
            self.assertEqual([413],[x["vehicle"]["number"] for x in delivery["unmerged_prs"]])
            self.assertIn("PR #413",owner_status(root))


if __name__=="__main__":
    unittest.main()
