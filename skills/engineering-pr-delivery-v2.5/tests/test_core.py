from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[1]/"scripts"))
from validate_repo_state import validate as repo_state
from validate_repo_profile import validate as repo_profile
from validate_roadmap import validate as roadmap
from validate_execution_frontier import validate as frontier
from validate_ep_self_contained import validate as ep_check
from validate_ep_semantics import validate as ep_semantics
from validate_ep_acceptance_mapping import validate as acceptance
from validate_progress import validate as progress_check
from validate_serial_execution import validate as serial
from validate_state_planes import validate as state_planes
from validate_checkpoint_linkage import validate as checkpoint_linkage
from validate_projection_convergence import validate as projection
from validate_drift_receipt import validate as drift
from cold_start_check import validate as cold_start

REPORT_SECTIONS=[
    "Executive state","Overall / phase / EP progress","Work completed","Files changed","Acceptance matrix","Tests and evidence","Quality findings","Known limitations","Owner decisions required","GitHub issue changes","Roadmap changes","Exact next actions","Successor EP",
]

def report_payloads():
    return [{"id":f"RPT-{i:02d}","section":section,"sources":["synthetic-authority"],"required_fields":["reconciled_value"]} for i,section in enumerate(REPORT_SECTIONS,1)]

def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def semantic_ep(ep_id="EP-1",branch="agent/test",wp="WP-1",write_path="src/a.py"):
    return {
        "schema_version":"relay-v2.5",
        "identity":{"ep_id":ep_id,"branch":branch,"base_ref":"abc","execution_state":"ACTIVE","previous_checkpoint":"NONE"},
        "git_basis":{"expected_branch":branch,"material_ref":"abc","base_branch":"main","base_observed_ref":"base-1","drift_policy":"RECHECK_BEFORE_WRITE","drift_receipt":None},
        "roadmap_source":{"roadmap_id":"RM-T","roadmap_revision":"RM-0001","objective":"OBJ-1","phase":"PHASE-1","work_package":wp,"generated_from_frontier":True},
        "outcome":{"user_visible":["User sees result"],"engineering":["Invariant preserved"]},
        "context_capsule":{"product_goal":"Deliver feature","roadmap_position":f"Phase 1 / {wp}","why_this_work_exists":"Required by roadmap","current_architecture":"Single service","prior_owner_decisions":[],"current_implementation_state":"Baseline exists","known_problems":[],"deliberate_non_goals":[],"terminology":{}},
        "repository_discovery":[{"id":"DSTEP-1","action":"VERIFY","target":"agents/relay/REPO_STATE.yaml","question":"Does repository state still route to this EP?","expected_outputs":["active EP id","roadmap revision"],"receipt_required":True,"on_failure":"Reconcile repository custody before engineering writes."}],
        "inputs":[{"id":"INPUT-1","name":"policy","description":"Roadmap policy governing this slice","authority":"overall roadmap","source":"agents/relay/roadmap/OVERALL_ROADMAP.yaml","resolution_method":"Read the current WP contract from the pinned roadmap revision.","type":"mapping","units":"NA","editable":False,"applicability":"CURRENT_EP_REQUIRED","resolution":"READY","consumers":["STEP-1"],"validation":["Confirm roadmap revision and WP id match the EP."],"stale_if":["Roadmap revision changes this WP contract."]}],
        "benchmarks":[{"id":"BENCH-1","name":"synthetic oracle","purpose":"Independently verify the observable result","source":"synthetic fixture","oracle_class":"FROZEN_GOLDEN","payload":"expected synthetic result fixture","expected":"result matches frozen synthetic oracle","tolerance":None,"independence":"The oracle is fixed independently of the implementation step.","applicability":"CURRENT_EP_REQUIRED","resolution":"READY","verifies":["AC-1","TEST-1"],"stale_if":["Acceptance definition changes."]}],
        "scope":{"allowed":[{"path":write_path,"reason":"implementation"}],"allowed_reads":[{"path":"agents/relay","reason":"resolve current relay authority"}],"protected":[{"invariant":"roadmap authority remains unchanged","reason":"EP cannot rewrite Owner intent"}],"prohibited":[{"domain":"solver","reason":"outside EP"}],"owner_reserved":[{"decision":"Owner-intent mutation","reason":"requires ODR/roadmap transaction"}]},
        "anti_drift":{"do_not":[{"id":"ADR-1","restriction":"Do not change solver or future roadmap work.","reason":"Keep this EP within its one-WP authority."}],"stale_if":[{"id":"STALE-1","condition":"Roadmap changes this WP scope or acceptance.","effect":"STALE","rationale":"The forward contract no longer matches its governing basis."}]},
        "implementation_plan":[{"id":"STEP-1","objective":"Implement the bounded synthetic result","targets":[write_path],"reads":["agents/relay/roadmap/OVERALL_ROADMAP.yaml"],"writes":[write_path],"inputs":["INPUT-1"],"acceptance":["AC-1"],"tests":["TEST-1"],"expected_state":"AC-1 is satisfied on the exact material basis.","stop_conditions":["Stop if route, authority, protected invariant, input or benchmark becomes invalid."]}],
        "quality":{"blueprints":["coding","testing"]},
        "acceptance":[{"id":"AC-1","description":"Works","weight":100,"verification":["TEST-1","BENCH-1"]}],
        "validation":[{"id":"TEST-1","class":"MUST_PASS","method":"pytest synthetic test","proves":["AC-1"]}],
        "failure_and_stop_conditions":{"hard_stop_categories":["ROADMAP_CONFLICT"]},
        "report_contract":{"sections":REPORT_SECTIONS,"payloads":report_payloads()},
        "checkpoint_contract":{"required":True},
        "successor_relay":{"required":True,"duties":["compute next executable frontier","run cold-start check","update REPO_STATE"],"required_outputs":["checkpoint","progress_reconciliation","issue_projection_disposition","next_frontier","successor_ep_or_terminal_disposition"]},
    }

def good(root):
    r={"schema_version":"relay-v2.5","roadmap":{"id":"RM-T","revision":"RM-0001","title":"Test"},"objectives":[{"id":"OBJ-1","title":"Objective","state":"ACTIVE","definition":"DEFINED","phases":[{"id":"PHASE-1","title":"Phase","state":"ACTIVE","definition":"DETAILED","work_packages":[{"id":"WP-1","title":"Work","state":"ACTIVE","definition":"DETAILED","execution_status":"ACTIVE","depends_on":[]}]}]}]}
    ep=semantic_ep()
    p={"schema_version":"relay-v2.5","progress_basis":{"id":"PB-1","roadmap_revision":"RM-0001"},"overall":{"earned_weight":50,"total_weight":100,"percent":50},"objectives":[],"phases":[],"work_packages":[],"execution_packages":[]}
    s={"schema_version":"relay-v2.5","relay_state":"ACTIVE","repository":{"name":"test"},"relay_protocol":{"version":"2.5","basis_ref":"common-test-ref"},"roadmap":{"id":"RM-T","revision":"RM-0001","path":"agents/relay/roadmap/OVERALL_ROADMAP.yaml"},"current_position":{"objective":"OBJ-1","phase":"PHASE-1","work_package":"WP-1","work_packages":[]},"execution_policy":{"mode":"SERIAL"},"active_ep":{"id":"EP-1","path":"agents/relay/execution-packages/EP-1.yaml","state":"ACTIVE"},"last_checkpoint":{"id":"NONE","path":None},"predecessor_join":{"id":None,"path":None},"progress":{"overall_percent":50,"phase_percent":50,"ep_percent":50,"basis_revision":"PB-1"},"status_planes":{"execution":{"state":"ACTIVE","can_continue":True,"material_authority":"WRITE","next_action":"Implement AC-1"},"quality":{"state":"CLEAR","findings":[]},"evidence":{"state":"PARTIAL","summary":"One required check remains","not_run":[]},"stop":{"active":False,"category":"NONE","reason":"","basis":[]}},"projection":{"required":False,"state":"NOT_REQUIRED","operation_id":None,"target":None,"roadmap_revision":"RM-0001","execution_ref":"EP-1","receipt":None,"basis":[]},"relay_readiness":{"repository_ready":True,"projection_ready":True,"handover_ready":True,"reasons":[]},"chat_context_required":False}
    profile={"schema_version":"relay-v2.5","repository_type":"application","default_branch":"main","important_paths":{"source":["src"],"tests":["tests"]},"commands":{"unit_test":"python -m unittest"},"protected_domains":[],"generated_paths":[],"repository_rules":[]}
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",r);dump(root/"agents/relay/roadmap/PROGRESS.yaml",p);dump(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml",{"schema_version":"relay-v2.5","nodes":[],"relationships":[]});dump(root/"agents/relay/execution-packages/EP-1.yaml",ep);dump(root/"agents/relay/REPO_STATE.yaml",s);dump(root/"agents/relay/REPO_PROFILE.yaml",profile);return r,ep,p,s

class CoreTests(unittest.TestCase):
    def test_good_repo(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            for check in (repo_state,repo_profile,roadmap,frontier,ep_check,ep_semantics,acceptance,progress_check,serial,state_planes,projection,drift,checkpoint_linkage,cold_start):self.assertEqual([],check(root)[0],check.__module__)
    def test_context_phrase_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["implementation_plan"][0]["objective"]="Continue previous work and run relevant tests";dump(root/"agents/relay/execution-packages/EP-1.yaml",ep);self.assertTrue(any("context-dependent phrase" in x for x in ep_check(root)[0]))
    def test_serial_multiple_frontier_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);r,_,_,_=good(root);r["objectives"][0]["phases"][0]["work_packages"].append({"id":"WP-2","title":"Second","state":"PLANNED","definition":"DETAILED","execution_status":"EXECUTABLE","depends_on":[]});dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",r);self.assertTrue(any("exactly one" in x for x in frontier(root)[0]))
    def test_progress_is_calculated(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,p,_=good(root);p["overall"]["percent"]=60;dump(root/"agents/relay/roadmap/PROGRESS.yaml",p);self.assertTrue(any("calculated" in x for x in progress_check(root)[0]))
    def test_not_run_infrastructure_is_not_a_hard_stop(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["status_planes"]["evidence"]={"state":"NOT_RUN","summary":"Required external runner did not execute","not_run":[{"id":"TEST-1","reason":"Runner produced no executable job","cause":"INFRASTRUCTURE"}]};s["status_planes"]["execution"]={"state":"WAITING","can_continue":False,"material_authority":"READ_ONLY","next_action":"Retry when the external runner can execute."};dump(root/"agents/relay/REPO_STATE.yaml",s);self.assertEqual([],state_planes(root)[0])
    def test_read_only_progress_can_continue_without_write_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["status_planes"]["execution"]={"state":"ACTIVE","can_continue":True,"material_authority":"READ_ONLY","next_action":"Reconcile pending evidence without changing engineering state."};dump(root/"agents/relay/REPO_STATE.yaml",s);self.assertEqual([],state_planes(root)[0])
    def test_terminal_repo_has_empty_frontier_and_no_active_ep(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);r,_,p,s=good(root)
            obj=r["objectives"][0];phase=obj["phases"][0];wp=phase["work_packages"][0];obj["state"]="COMPLETE";phase["state"]="COMPLETE";wp["state"]="COMPLETE";wp["execution_status"]="TERMINAL"
            p["overall"]={"earned_weight":100,"total_weight":100,"percent":100}
            s["relay_state"]="TERMINAL";s["active_ep"]={"id":None,"path":None,"state":"NONE"};s["last_checkpoint"]={"id":"CP-1","path":"agents/relay/checkpoints/CP-1.yaml"};s["progress"].update({"overall_percent":100,"phase_percent":100,"ep_percent":100});s["projection"].update({"execution_ref":"NONE"});s["relay_readiness"].update({"repository_ready":True,"projection_ready":True,"handover_ready":True});s["status_planes"]={"execution":{"state":"COMPLETE","can_continue":False,"material_authority":"NONE","next_action":"No material work remains."},"quality":{"state":"CLEAR","findings":[]},"evidence":{"state":"COMPLETE","summary":"Required evidence is terminal.","not_run":[]},"stop":{"active":False,"category":"NONE","reason":"","basis":[]}}
            cp={"schema_version":"relay-v2.5","checkpoint_id":"CP-1","ep_id":"EP-1","roadmap_basis":{"roadmap_id":"RM-T","revision":"RM-0001"},"execution_basis":{"material_ref":"abc"},"implementation_result":{},"acceptance_results":[],"validation_results":[],"quality_findings":[],"discoveries":[],"roadmap_reconciliation":{"result":"STATUS_UPDATE"},"successor":{"mode":"NONE","frontier_work_package":None,"ep_id":None,"parallel_plan":None,"lanes":[]}}
            dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",r);dump(root/"agents/relay/roadmap/PROGRESS.yaml",p);dump(root/"agents/relay/REPO_STATE.yaml",s);dump(root/"agents/relay/checkpoints/CP-1.yaml",cp)
            self.assertEqual([],frontier(root)[0]);self.assertEqual([],projection(root)[0]);self.assertEqual([],checkpoint_linkage(root)[0]);self.assertEqual([],cold_start(root)[0])
if __name__=="__main__":unittest.main()
