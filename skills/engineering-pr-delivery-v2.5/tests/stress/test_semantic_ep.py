from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]))
from test_core import good,dump
from validate_ep_semantics import validate as semantic_ep
from validate_repo_profile import validate as repo_profile
from validate_repo_state import validate as repo_state


class SemanticExecutionPackageStressTests(unittest.TestCase):
    def test_rich_semantic_ep_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);self.assertEqual([],semantic_ep(root)[0])

    def test_semantically_empty_current_input_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);item=ep["inputs"][0];item["description"]="";item["consumers"]=[];dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            errors=semantic_ep(root)[0];self.assertTrue(any("description" in x for x in errors));self.assertTrue(any("consumers" in x for x in errors))

    def test_unresolved_current_required_input_cannot_claim_executable(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["inputs"][0]["resolution"]="MISSING_BLOCKING";dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("executable EP cannot carry unresolved current-required input" in x for x in semantic_ep(root)[0]))

    def test_semantically_empty_required_benchmark_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["benchmarks"][0]["payload"]="";ep["benchmarks"][0]["expected"]="";dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            errors=semantic_ep(root)[0];self.assertTrue(any("payload" in x for x in errors));self.assertTrue(any("expected" in x for x in errors))

    def test_vague_discovery_step_and_receipt_namespace_collision_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["repository_discovery"]=[{"id":"DISC-1","action":"VERIFY","target":"agents/relay/REPO_STATE.yaml","purpose":"confirm"}];dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            errors=semantic_ep(root)[0];self.assertTrue(any("DSTEP" in x for x in errors));self.assertTrue(any("expected_outputs" in x for x in errors));self.assertTrue(any("question" in x for x in errors))

    def test_empty_write_scope_cannot_claim_executable(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["scope"]["allowed"]=[];dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("scope.allowed must not be empty" in x for x in semantic_ep(root)[0]))

    def test_unstructured_or_empty_anti_drift_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["anti_drift"]={"do_not":["do not drift"],"stale_if":[]};dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            errors=semantic_ep(root)[0];self.assertTrue(any("do_not[0] must be a mapping" in x for x in errors));self.assertTrue(any("stale_if must contain structured" in x for x in errors))

    def test_vague_implementation_step_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["implementation_plan"]=[{"id":"STEP-1","action":"Implement required changes"}];dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            errors=semantic_ep(root)[0];self.assertTrue(any("objective" in x for x in errors));self.assertTrue(any("targets" in x for x in errors));self.assertTrue(any("expected_state" in x for x in errors))

    def test_report_headings_without_reconciliation_payload_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ep["report_contract"].pop("payloads");dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("payloads must be a list" in x for x in semantic_ep(root)[0]))

    def test_repository_profile_is_required_for_conformance(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);(root/"agents/relay/REPO_PROFILE.yaml").unlink();self.assertTrue(any("required" in x for x in repo_profile(root)[0]))

    def test_protocol_binding_cannot_be_placeholder(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,state=good(root);state["relay_protocol"]["basis_ref"]="<pinned Common SHA>";dump(root/"agents/relay/REPO_STATE.yaml",state)
            self.assertTrue(any("basis_ref" in x for x in repo_state(root)[0]))

    def test_missing_task_roadmap_admission_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root)
            ep["roadmap_source"].pop("task_admission")
            dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("task_admission is required" in x for x in semantic_ep(root)[0]))

    def test_added_execution_wp_requires_revision_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root)
            ep["roadmap_source"]["task_admission"]["disposition"]="ADDED_EXECUTION_WP"
            ep["roadmap_source"]["task_admission"]["basis"]=["Engineering discovery required a new execution WP."]
            dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("requires current roadmap revision_record" in x for x in semantic_ep(root)[0]))

if __name__=="__main__":unittest.main()
