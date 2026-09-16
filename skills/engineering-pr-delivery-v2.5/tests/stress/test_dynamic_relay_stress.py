from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"))
from relaylib import compute_frontier,pct,scan_context_phrases
from validate_state_planes import validate as state_planes

def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def repo_state(evidence_state="PARTIAL",not_run=None,execution_state="ACTIVE",stop=None,material_authority="WRITE"):
    return {"schema_version":"relay-v2.5","relay_state":"ACTIVE","status_planes":{"execution":{"state":execution_state,"can_continue":True,"material_authority":material_authority,"next_action":"Execute the current bounded validation step."},"quality":{"state":"CLEAR","findings":[]},"evidence":{"state":evidence_state,"summary":"Synthetic evidence state","not_run":not_run or []},"stop":stop or {"active":False,"category":"NONE","reason":"","basis":[]}}}

class DynamicRelayStressTests(unittest.TestCase):
    def test_infrastructure_not_run_is_evidence_not_hard_stop(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);dump(root/"agents/relay/REPO_STATE.yaml",repo_state("NOT_RUN",[{"id":"TEST-EXT","reason":"External runner created no executable job","cause":"INFRASTRUCTURE"}],material_authority="READ_ONLY"))
            self.assertEqual([],state_planes(root)[0])

    def test_overloaded_blocked_execution_state_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);dump(root/"agents/relay/REPO_STATE.yaml",repo_state(execution_state="BLOCKED"))
            self.assertTrue(any("execution.state invalid" in x for x in state_planes(root)[0]))

    def test_active_hard_stop_cannot_keep_write_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);state=repo_state(stop={"active":True,"category":"OWNER_DECISION_REQUIRED","reason":"Owner decision required.","basis":["ODR-1"]});state["status_planes"]["execution"]["can_continue"]=False;dump(root/"agents/relay/REPO_STATE.yaml",state)
            self.assertTrue(any("cannot retain material_authority WRITE" in x for x in state_planes(root)[0]))

    def test_frontier_is_derived_from_dependencies(self):
        roadmap={"objectives":[{"id":"OBJ","phases":[{"id":"P1","work_packages":[{"id":"W1","state":"COMPLETE","definition":"DETAILED","execution_status":"TERMINAL","depends_on":[]},{"id":"W2","state":"ACTIVE","definition":"DETAILED","execution_status":"ACTIVE","depends_on":["W1"]},{"id":"W3","state":"PLANNED","definition":"DETAILED","execution_status":"WAITING","depends_on":["W2"]}]}]}]}
        self.assertEqual(["W2"],compute_frontier(roadmap))

    def test_scope_growth_changes_denominator_without_losing_earned_work(self):
        earned=60
        self.assertEqual(60.0,pct(earned,100))
        self.assertEqual(50.0,pct(earned,120))

    def test_chat_dependent_instruction_is_detected(self):
        found=scan_context_phrases({"step":"Continue previous work and run relevant tests"})
        self.assertGreaterEqual(len(found),2)

if __name__=="__main__":unittest.main()
