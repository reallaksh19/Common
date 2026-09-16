from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[1]/"scripts"))
from validate_repo_state import validate as repo_state
from validate_roadmap import validate as roadmap
from validate_execution_frontier import validate as frontier
from validate_ep_self_contained import validate as ep_check
from validate_ep_acceptance_mapping import validate as acceptance
from validate_progress import validate as progress_check
from validate_serial_execution import validate as serial
from validate_state_planes import validate as state_planes
from validate_checkpoint_linkage import validate as checkpoint_linkage
from cold_start_check import validate as cold_start

REPORT_SECTIONS=[
    "Executive state",
    "Overall / phase / EP progress",
    "Work completed",
    "Files changed",
    "Acceptance matrix",
    "Tests and evidence",
    "Quality findings",
    "Known limitations",
    "Owner decisions required",
    "GitHub issue changes",
    "Roadmap changes",
    "Exact next actions",
    "Successor EP",
]

def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def good(root):
    r={"schema_version":"relay-v2.5","roadmap":{"id":"RM-T","revision":"RM-0001","title":"Test"},"objectives":[{"id":"OBJ-1","title":"Objective","state":"ACTIVE","definition":"DEFINED","phases":[{"id":"PHASE-1","title":"Phase","state":"ACTIVE","definition":"DETAILED","work_packages":[{"id":"WP-1","title":"Work","state":"ACTIVE","definition":"DETAILED","execution_status":"ACTIVE","depends_on":[]}]}]}]}
    ep={"schema_version":"relay-v2.5","identity":{"ep_id":"EP-1","branch":"agent/test","base_ref":"abc","execution_state":"ACTIVE","previous_checkpoint":"NONE"},"roadmap_source":{"roadmap_id":"RM-T","roadmap_revision":"RM-0001","objective":"OBJ-1","phase":"PHASE-1","work_package":"WP-1","generated_from_frontier":True},"outcome":{"user_visible":["User sees result"],"engineering":["Invariant preserved"]},"context_capsule":{"product_goal":"Deliver feature","roadmap_position":"Phase 1","why_this_work_exists":"Required by roadmap","current_architecture":"Single service","prior_owner_decisions":[],"current_implementation_state":"Baseline exists","known_problems":[],"deliberate_non_goals":[],"terminology":{}},"repository_discovery":[{"id":"DISC-1","action":"VERIFY","target":"agents/relay/REPO_STATE.yaml","purpose":"confirm"}],"inputs":[{"id":"INPUT-1","name":"policy","source":"roadmap","editable":False}],"benchmarks":[],"scope":{"allowed":[{"path":"src/a.py","reason":"implementation"}],"prohibited":[{"domain":"solver","reason":"outside EP"}]},"anti_drift":{"do_not":["change solver"],"stale_if":["roadmap changes"]},"implementation_plan":[{"id":"STEP-1","action":"Implement AC-1"}],"quality":{"blueprints":["coding","testing"]},"acceptance":[{"id":"AC-1","description":"Works","weight":100,"verification":["TEST-1"]}],"validation":[{"id":"TEST-1","class":"MUST_PASS","method":"pytest","proves":["AC-1"]}],"failure_and_stop_conditions":{"hard_stop_categories":["ROADMAP_CONFLICT"]},"report_contract":{"sections":REPORT_SECTIONS},"checkpoint_contract":{"required":True},"successor_relay":{"required":True,"duties":["compute next executable frontier","run cold-start check","update REPO_STATE"]}}
    p={"schema_version":"relay-v2.5","progress_basis":{"id":"PB-1","roadmap_revision":"RM-0001"},"overall":{"earned_weight":50,"total_weight":100,"percent":50},"objectives":[],"phases":[],"work_packages":[],"execution_packages":[]}
    s={"schema_version":"relay-v2.5","repository":{"name":"test"},"roadmap":{"id":"RM-T","revision":"RM-0001","path":"agents/relay/roadmap/OVERALL_ROADMAP.yaml"},"current_position":{"objective":"OBJ-1","phase":"PHASE-1","work_package":"WP-1"},"execution_policy":{"mode":"SERIAL"},"active_ep":{"id":"EP-1","path":"agents/relay/execution-packages/EP-1.yaml","state":"ACTIVE"},"last_checkpoint":{"id":"NONE","path":None},"progress":{"overall_percent":50,"phase_percent":50,"ep_percent":50,"basis_revision":"PB-1"},"status_planes":{"execution":{"state":"ACTIVE","can_continue":True,"next_action":"Implement AC-1"},"quality":{"state":"CLEAR","findings":[]},"evidence":{"state":"PARTIAL","summary":"One required check remains","not_run":[]},"stop":{"active":False,"category":"NONE","reason":"","basis":[]}},"chat_context_required":False}
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",r);dump(root/"agents/relay/roadmap/PROGRESS.yaml",p);dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",{"schema_version":"relay-v2.5","nodes":[],"relationships":[]});dump(root/"agents/relay/execution-packages/EP-1.yaml",ep);dump(root/"agents/relay/REPO_STATE.yaml",s);return r,ep,p,s

class CoreTests(unittest.TestCase):
    def test_good_repo(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            for check in (repo_state,roadmap,frontier,ep_check,acceptance,progress_check,serial,state_planes,checkpoint_linkage,cold_start):self.assertEqual([],check(root)[0],check.__module__)
    def test_context_phrase_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["implementation_plan"][0]["action"]="Continue previous work and run relevant tests";dump(root/"agents/relay/execution-packages/EP-1.yaml",ep);self.assertTrue(any("context-dependent phrase" in x for x in ep_check(root)[0]))
    def test_serial_multiple_frontier_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);r,_,_,_=good(root);r["objectives"][0]["phases"][0]["work_packages"].append({"id":"WP-2","title":"Second","state":"PLANNED","definition":"DETAILED","execution_status":"EXECUTABLE","depends_on":[]});dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",r);self.assertTrue(any("exactly one" in x for x in frontier(root)[0]))
    def test_progress_is_calculated(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,p,_=good(root);p["overall"]["percent"]=60;dump(root/"agents/relay/roadmap/PROGRESS.yaml",p);self.assertTrue(any("calculated" in x for x in progress_check(root)[0]))
    def test_not_run_infrastructure_is_not_a_hard_stop(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["status_planes"]["evidence"]={"state":"NOT_RUN","summary":"Required external runner did not execute","not_run":[{"id":"TEST-1","reason":"Runner produced no executable job","cause":"INFRASTRUCTURE"}]};s["status_planes"]["execution"]={"state":"WAITING","can_continue":False,"next_action":"Retry when the external runner can execute."};dump(root/"agents/relay/REPO_STATE.yaml",s);self.assertEqual([],state_planes(root)[0])
if __name__=="__main__":unittest.main()
