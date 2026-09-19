from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[2]/"scripts"))
sys.path.insert(0,str(HERE.parents[1]))

from test_core import good,dump
from report_projection import build as build_report
from delivery_projection import snapshot as delivery_snapshot
from validate_delivery_observation import validate as delivery_check
from validate_report_projection import validate as report_check
from validate_human_communication import validate as communication_check
from render_owner_status import render as owner_status


def _complete_engineering(root:Path,progress:dict,state:dict):
    progress["acceptance_criteria"][0].update({"status":"COMPLETE","earned_weight":100,"percent":100})
    progress["implementation_steps"][0].update({"earned_weight":100,"percent":100})
    progress["execution_packages"][0].update({"earned_weight":100,"percent":100})
    progress["work_packages"][0].update({"earned_weight":100,"percent":100})
    progress["phases"][0].update({"earned_weight":100,"percent":100})
    progress["objectives"][0].update({"earned_weight":100,"percent":100})
    progress["overall"].update({"earned_weight":100,"percent":100})
    state["progress"].update({"overall_percent":100,"phase_percent":100,"ep_percent":100})
    state["status_planes"]["evidence"]={"state":"COMPLETE","summary":"Required engineering evidence is complete.","not_run":[]}
    dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress)
    dump(root/"agents/relay/REPO_STATE.yaml",state)


def _observe(root:Path,state:dict,*,head="head-1",checks="PASS",check_head=None,mergeability="MERGEABLE",review="CLEAR",lifecycle="OPEN"):
    obs={
        "schema_version":"relay-v2.5-delivery-observation",
        "id":"DOBS-1",
        "provider":"GITHUB",
        "repository":"owner/repo",
        "vehicle":{
            "kind":"PULL_REQUEST",
            "number":411,
            "url":"https://github.com/owner/repo/pull/411",
            "lifecycle":lifecycle,
            "head":{"ref":"agent/work","sha":head},
            "base":{"ref":"main","sha":"base-1"},
        },
        "mergeability":{"state":mergeability},
        "checks":{
            "state":checks,
            "head_sha":check_head if check_head is not None else (head if checks in {"PASS","FAIL","PENDING"} else None),
            "required":["engineering-pr-delivery-v2.5"],
            "observations":[{"name":"engineering-pr-delivery-v2.5","state":checks}],
        },
        "review":{"state":review,"unresolved_threads":0 if review=="CLEAR" else None,"change_requests":0 if review=="CLEAR" else None},
        "readback_basis":["provider-readback:synthetic"],
    }
    path="agents/relay/delivery/DOBS-1.yaml";dump(root/path,obs)
    state["repository"]["remote"]="owner/repo"
    state["delivery"]={"required":True,"provider":"GITHUB","observation":{"id":"DOBS-1","path":path}}
    dump(root/"agents/relay/REPO_STATE.yaml",state)
    return obs


def _owner_merge_authorization(root:Path,head="head-1",disposition="GRANTED"):
    odr={
        "schema_version":"relay-v2.5",
        "id":"ODR-MERGE-1",
        "decision":{"authority":"OWNER","kind":"AUTHORIZATION","statement":"Authorize merge of the exact reviewed PR head.","source":"owner:test"},
        "effects":{"requirement_disposition":"NOT_APPLICABLE","grants_material_write_authority":False,"pending_items":[]},
        "delivery_authorization":{
            "action":"MERGE","provider":"GITHUB","repository":"owner/repo","vehicle":"PULL_REQUEST",
            "number":411,"head_sha":head,"disposition":disposition,
        },
        "impact":{"class":["LOCAL"]},
        "affected":{"objectives":[],"phases":[],"work_packages":[],"execution_packages":[],"issues":[]},
        "required_reconciliation":[],
        "status":"APPLIED",
    }
    dump(root/"agents/relay/roadmap/owner-decisions/ODR-MERGE-1.yaml",odr)


class DeliveryReadinessStressTests(unittest.TestCase):
    def test_no_delivery_vehicle_is_not_applicable(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            delivery=build_report(root)["delivery"]
            self.assertEqual("NOT_APPLICABLE",delivery["applicability"])
            self.assertEqual("NOT_APPLICABLE",delivery["technical_ready_to_merge"]["state"])
            self.assertIn("No pull-request delivery vehicle",owner_status(root))

    def test_mergeable_pr_with_pending_exact_head_checks_is_not_technically_ready(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,progress,state=good(root);_complete_engineering(root,progress,state);_observe(root,state,checks="PENDING")
            self.assertEqual([],delivery_check(root)[0])
            delivery=build_report(root)["delivery"]
            self.assertEqual("MERGEABLE",delivery["mergeability"]["state"])
            self.assertEqual("PENDING",delivery["checks"]["state"])
            self.assertEqual("NO",delivery["technical_ready_to_merge"]["state"])
            self.assertEqual("NOT_GRANTED",delivery["merge_authorization"]["state"])
            self.assertEqual([],report_check(root)[0])
            self.assertEqual([],communication_check(root)[0])

    def test_stale_checks_are_explicit_and_cannot_count_as_exact_head_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,progress,state=good(root);_complete_engineering(root,progress,state);_observe(root,state,head="head-2",checks="STALE",check_head="head-1")
            self.assertEqual([],delivery_check(root)[0])
            delivery=build_report(root)["delivery"]
            self.assertEqual("STALE",delivery["checks"]["state"])
            self.assertEqual("NO",delivery["technical_ready_to_merge"]["state"])

    def test_pass_claim_on_wrong_head_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,progress,state=good(root);_complete_engineering(root,progress,state);_observe(root,state,head="head-2",checks="PASS",check_head="head-1")
            self.assertTrue(any("must bind to current PR head" in x for x in delivery_check(root)[0]))

    def test_unknown_review_yields_unknown_when_every_known_gate_is_clear(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,progress,state=good(root);_complete_engineering(root,progress,state);_observe(root,state,review="UNKNOWN")
            delivery=build_report(root)["delivery"]
            self.assertEqual("UNKNOWN",delivery["technical_ready_to_merge"]["state"])
            self.assertTrue(any("review" in x for x in delivery["technical_ready_to_merge"]["reasons"]))

    def test_technical_ready_does_not_imply_merge_authorized(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,progress,state=good(root);_complete_engineering(root,progress,state);_observe(root,state)
            delivery=build_report(root)["delivery"]
            self.assertEqual("YES",delivery["technical_ready_to_merge"]["state"])
            self.assertEqual("NOT_GRANTED",delivery["merge_authorization"]["state"])
            text=owner_status(root)
            self.assertIn("technically ready to merge: **YES**",text)
            self.assertIn("merge authorization: **Not Granted**",text)

    def test_applied_owner_authorization_is_exact_pr_head_bound(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,progress,state=good(root);_complete_engineering(root,progress,state);_observe(root,state);_owner_merge_authorization(root,"head-1")
            delivery=build_report(root)["delivery"]
            self.assertEqual("YES",delivery["technical_ready_to_merge"]["state"])
            self.assertEqual("GRANTED",delivery["merge_authorization"]["state"])
            self.assertEqual(["ODR-MERGE-1"],delivery["merge_authorization"]["basis"])
            self.assertEqual([],communication_check(root)[0])

    def test_head_change_stales_prior_merge_authorization_without_changing_technical_readiness(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,progress,state=good(root);_complete_engineering(root,progress,state);_observe(root,state,head="head-2");_owner_merge_authorization(root,"head-1")
            delivery=build_report(root)["delivery"]
            self.assertEqual("YES",delivery["technical_ready_to_merge"]["state"])
            self.assertEqual("STALE",delivery["merge_authorization"]["state"])

    def test_draft_pr_is_not_ready_for_review(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,progress,state=good(root);_complete_engineering(root,progress,state);_observe(root,state,lifecycle="DRAFT")
            delivery=build_report(root)["delivery"]
            self.assertEqual("NO",delivery["ready_for_review"]["state"])
            self.assertEqual("NO",delivery["technical_ready_to_merge"]["state"])


if __name__=="__main__":
    unittest.main()
