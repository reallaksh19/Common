from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[2]/"scripts"))
sys.path.insert(0,str(HERE.parents[1]))
sys.path.insert(0,str(HERE.parent))

from test_core import good,dump
from test_takeover_certification import attach_takeover
from relaylib import load_yaml
from material_write_ready import evaluate as write_ready
from validate_repo_state import validate as repo_state
from validate_owner_decision import validate_file as owner_decision
from communication_projection import build as communication
from render_owner_status import render as owner_status


def git(root:Path,*args)->str:
    return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()


def init_git(root:Path,branch="fix/override")->str:
    subprocess.check_call(["git","-C",str(root),"init","-b","main"],stdout=subprocess.DEVNULL)
    git(root,"config","user.email","synthetic@example.test")
    git(root,"config","user.name","Synthetic Relay")
    git(root,"add",".")
    git(root,"commit","-m","base")
    base=git(root,"rev-parse","HEAD")
    ep_path=root/"agents/relay/execution-packages/EP-1.yaml"
    ep=load_yaml(ep_path)
    ep["identity"]["base_ref"]=base
    ep["git_basis"]["material_ref"]=base
    ep["git_basis"]["base_observed_ref"]=base
    dump(ep_path,ep)
    git(root,"add",str(ep_path.relative_to(root)))
    git(root,"commit","-m","bind material basis")
    git(root,"checkout","-b",branch)
    return base


def pending(id="PEND-1",branch="fix/override"):
    return {
        "id":id,
        "kind":"DEFERRED_VALIDATION",
        "state":"OPEN",
        "summary":"Reconcile route/custody before delivery readiness.",
        "source":"ODR-OVR-1",
        "scope":{"route_key":None,"ep_id":"EP-1","branch":branch,"issues":[162],"pull_requests":[180]},
        "evidence":["workflow:synthetic-route-failure"],
        "must_resolve_before":["PR_READY","MERGE"],
        "allowed_before_resolution":["BOUNDED_PRODUCT_WRITES","TESTS","DRAFT_PR_UPDATES"],
        "resolution_condition":"Current route/custody validates on the exact delivery head.",
    }


def write_override(root:Path,base:str,branch="fix/override",pending_id="PEND-1"):
    path=root/"agents/relay/roadmap/owner-decisions/ODR-OVR-1.yaml"
    odr={
        "schema_version":"relay-v2.5",
        "id":"ODR-OVR-1",
        "decision":{
            "authority":"OWNER",
            "kind":"AUTHORIZATION",
            "statement":"Start bounded corrective work while route reconciliation remains pending.",
            "source":"owner-message:synthetic",
        },
        "effects":{
            "requirement_disposition":"PENDING_NOT_SATISFIED",
            "grants_material_write_authority":True,
            "pending_items":[pending_id],
        },
        "delivery_authorization":None,
        "execution_override":{
            "disposition":"GRANTED",
            "scope":{
                "repository":"test",
                "branch":branch,
                "base_sha":base,
                "route_key":None,
                "issues":[162],
                "pull_requests":[180],
                "allowed_write_paths":["src/**","tests/**"],
            },
            "defers":["ROUTE_RECONCILIATION","CANDIDATE_ADMISSION"],
            "allows":["BOUNDED_PRODUCT_WRITES","TESTS","DRAFT_PR_UPDATES"],
            "blocks":["PR_READY","MERGE"],
            "pending_obligations":[pending_id],
        },
        "impact":{"class":["LOCAL"]},
        "affected":{"objectives":[],"phases":[],"work_packages":["WP-1"],"execution_packages":["EP-1"],"issues":[162]},
        "required_reconciliation":["Resolve route/custody before PR readiness or merge."],
        "status":"APPLIED",
    }
    dump(path,odr)
    return path


class OwnerOverrideControlStressTests(unittest.TestCase):
    def test_pending_known_issue_and_delegation_survive_cold_start_projection(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root)
            state["control_obligations"]=[
                pending(),
                {
                    "id":"KI-1","kind":"KNOWN_ISSUE","state":"OPEN",
                    "summary":"A bounded non-blocking limitation remains.",
                    "source":"issue:synthetic","scope":{},"evidence":["test:known"],
                    "revisit_when":"The next consumer reaches this boundary.",
                },
                {
                    "id":"DLG-1","kind":"DELEGATION","state":"OPEN",
                    "summary":"External browser verification is waiting.",
                    "source":"EP-1 next_work","scope":{},"evidence":[],
                    "success_condition":"Browser evidence is posted and validated.",
                    "monitor_role":"READ_ONLY",
                },
            ]
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            self.assertEqual([],repo_state(root)[0])
            projection=communication(root)
            control=projection["owner"]["control"]
            self.assertEqual(["PEND-1"],[x["id"] for x in control["pending_validations"]])
            self.assertEqual(["KI-1"],[x["id"] for x in control["known_issues"]])
            self.assertEqual(["DLG-1"],[x["id"] for x in control["delegations"]])
            text=owner_status(root)
            self.assertIn("Pending control PEND-1",text)
            self.assertIn("Known issue KI-1",text)
            self.assertIn("read-only",text)
            self.assertIn("PR Ready",text)
            self.assertIn("Merge",text)

    def test_satisfied_pending_requires_resolution_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root)
            item=pending();item["state"]="SATISFIED";item["evidence"]=[]
            state["control_obligations"]=[item]
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            self.assertTrue(any("SATISFIED requires resolution evidence" in x for x in repo_state(root)[0]))

    def test_multiple_active_execution_custody_leases_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
            state["execution_custody"]={
                "enforced":True,
                "leases":[
                    {"route_key":"SERIAL:EP-1","candidate":{"agent_instance_id":"agent-A"},"state":"ACTIVE","branch":"agent/test","source":"ODR-A","basis":[]},
                    {"route_key":"SERIAL:EP-1","candidate":{"agent_instance_id":"agent-B"},"state":"ACTIVE","branch":"agent/test","source":"ODR-B","basis":[]},
                ],
            }
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            self.assertTrue(any("multiple ACTIVE executors" in x for x in repo_state(root)[0]))

    def test_owner_override_allows_bounded_route_mismatch_without_claiming_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);base=init_git(root)
            state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
            state["control_obligations"]=[pending()]
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            odr_path=write_override(root,base)
            self.assertEqual([],owner_decision(odr_path)[0])
            git(root,"add",".");git(root,"commit","-m","record bounded override")
            out=write_ready(root,"fresh-agent",branch="fix/override",worktree=str(root))
            self.assertTrue(out["material_write_ready"],out)
            self.assertEqual("PASS_WITH_OWNER_OVERRIDE",out["status"])
            self.assertFalse(out["candidate_certified"])
            self.assertEqual(["CANDIDATE_ADMISSION","ROUTE_RECONCILIATION"],out["deferred_controls"])
            self.assertEqual(["PEND-1"],out["pending_obligations"])
            self.assertIn("PR_READY",out["owner_override"]["blocks"])
            self.assertIn("MERGE",out["owner_override"]["blocks"])
            self.assertTrue(any("remain OPEN" in x for x in out["claim_limitations"]))

    def test_resolved_pending_invalidates_owner_override(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);base=init_git(root)
            item=pending();item["state"]="SATISFIED";item["evidence"].append("route:reconciled")
            state=load_yaml(root/"agents/relay/REPO_STATE.yaml");state["control_obligations"]=[item];dump(root/"agents/relay/REPO_STATE.yaml",state)
            write_override(root,base);git(root,"add",".");git(root,"commit","-m","record resolved override basis")
            out=write_ready(root,"fresh-agent",branch="fix/override",worktree=str(root))
            self.assertFalse(out["material_write_ready"])
            self.assertEqual("FAIL",out["status"])

    def test_owner_override_cannot_bypass_hard_stop(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);base=init_git(root)
            state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
            state["control_obligations"]=[pending()]
            state["status_planes"]["stop"]={
                "active":True,"category":"PROTECTED_INVARIANT_FAILURE",
                "reason":"Synthetic protected invariant failed.","basis":["test:protected"],
            }
            state["status_planes"]["execution"]["can_continue"]=False
            state["status_planes"]["execution"]["material_authority"]="READ_ONLY"
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            write_override(root,base);git(root,"add",".");git(root,"commit","-m","record blocked override")
            out=write_ready(root,"fresh-agent",branch="fix/override",worktree=str(root))
            self.assertFalse(out["material_write_ready"])
            self.assertTrue(any("hard stop is active and non-overridable" in x for x in out["errors"]))

    def test_certified_candidate_still_needs_active_execution_custody(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            subprocess.check_call(["git","-C",str(root),"init","-b","main"],stdout=subprocess.DEVNULL)
            git(root,"config","user.email","synthetic@example.test");git(root,"config","user.name","Synthetic Relay")
            git(root,"add",".");git(root,"commit","-m","base")
            base=git(root,"rev-parse","HEAD");git(root,"checkout","-b","agent/test")
            ep_path=root/"agents/relay/execution-packages/EP-1.yaml";ep=load_yaml(ep_path)
            ep["identity"]["base_ref"]=base;ep["git_basis"]["material_ref"]=base;ep["git_basis"]["base_observed_ref"]=base
            dump(ep_path,ep);git(root,"add",str(ep_path.relative_to(root)));git(root,"commit","-m","bind material basis")
            attach_takeover(root,candidate="agent-B",preparer="agent-B",disc_id="DISC-B",tc_id="TC-B")
            attach_takeover(root,candidate="agent-C",preparer="agent-C",disc_id="DISC-C",tc_id="TC-C")
            state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
            state["execution_custody"]={
                "enforced":True,
                "leases":[{"route_key":"SERIAL:EP-1","candidate":{"agent_instance_id":"agent-B"},"state":"ACTIVE","branch":"agent/test","source":"takeover:agent-B","basis":["TC-B"]}],
            }
            dump(root/"agents/relay/REPO_STATE.yaml",state)
            owner=write_ready(root,"agent-B",branch="agent/test",worktree=str(root))
            self.assertTrue(owner["material_write_ready"],owner)
            other=write_ready(root,"agent-C",branch="agent/test",worktree=str(root))
            self.assertFalse(other["material_write_ready"])
            self.assertTrue(other["candidate_certified"])
            self.assertTrue(any("execution custody belongs to agent-B" in x for x in other["errors"]))


if __name__=="__main__":
    unittest.main()
