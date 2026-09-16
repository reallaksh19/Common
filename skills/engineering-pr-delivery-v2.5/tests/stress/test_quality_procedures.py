from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]))
from test_core import good,semantic_ep,write_clear_quality_review,dump
from validate_blueprints import validate as blueprints
from validate_quality_router import validate_ep as quality_route
from validate_quality_review import validate as quality_reviews,validate_file as quality_review_file

class QualityProcedureStressTests(unittest.TestCase):
    def test_blueprint_library_is_procedural(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual([],blueprints(Path(td))[0])

    def test_router_is_complete_partition_and_only_applicable_requires_focus(self):
        ep=semantic_ep();self.assertEqual([],quality_route(ep,"EP")[0])
        ep["quality"]["not_applicable"][0].pop("reason")
        self.assertTrue(any("reason" in x for x in quality_route(ep,"EP")[0]))
        ep=semantic_ep();ep["quality"]["not_applicable"].pop()
        self.assertTrue(any("classify every built-in blueprint" in x for x in quality_route(ep,"EP")[0]))
        ep=semantic_ep();ep["quality"]["applicable"][0]["review_focus"]=[]
        self.assertTrue(any("review_focus" in x for x in quality_route(ep,"EP")[0]))

    def test_clear_qrv_exactly_covers_applicable_procedures(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);write_clear_quality_review(root,ep)
            self.assertEqual([],quality_reviews(root)[0])

    def test_not_run_is_quality_attention_not_execution_block(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ptr=write_clear_quality_review(root,ep);p=root/ptr["path"];q=yaml.safe_load(p.read_text())
            q["procedure_results"][0]={"blueprint":"coding","result":"NOT_RUN","evidence":[],"reason":"Independent review tool unavailable.","cause":"UNAVAILABLE_TOOL"};q["overall_state"]="NEEDS_ATTENTION";dump(p,q)
            self.assertEqual([],quality_review_file(root,p)[0]);self.assertFalse(q["execution_effect"]["blocks_execution"])

    def test_high_severity_ordinary_finding_does_not_become_fake_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ptr=write_clear_quality_review(root,ep);p=root/ptr["path"];q=yaml.safe_load(p.read_text())
            q["procedure_results"][0]["result"]="FINDINGS";q["findings"]=[{"id":"QF-1","blueprint":"coding","classification":"MAINTAINABILITY","severity":"HIGH","disposition":"DEFERRED","statement":"A bounded maintainability cleanup remains after the accepted slice.","evidence":["review:path/to/module"],"blocks_execution":False,"hard_stop":None}];q["overall_state"]="NEEDS_ATTENTION";q["successor_handover"]={"unresolved_findings":["QF-1"],"follow_up":["Address QF-1 in the next authorized maintenance slice."]};dump(p,q)
            self.assertEqual([],quality_review_file(root,p)[0]);self.assertFalse(q["execution_effect"]["blocks_execution"])

    def test_blocking_finding_requires_real_hard_stop_mapping(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ptr=write_clear_quality_review(root,ep);p=root/ptr["path"];q=yaml.safe_load(p.read_text())
            finding={"id":"QF-1","blueprint":"coding","classification":"SAFETY","severity":"CRITICAL","disposition":"UNRESOLVED","statement":"Protected safety invariant is violated.","evidence":["test:protected-invariant"],"blocks_execution":True,"hard_stop":{"category":"PROTECTED_INVARIANT_FAILURE","trigger":"AUTHORITY","basis":["test:protected-invariant"]}}
            q["procedure_results"][0]["result"]="FINDINGS";q["findings"]=[finding];q["overall_state"]="NEEDS_ATTENTION";q["execution_effect"]={"blocks_execution":True,"blocking_findings":["QF-1"]};q["successor_handover"]={"unresolved_findings":["QF-1"],"follow_up":["Restore the protected invariant before material execution."]};dump(p,q)
            self.assertTrue(any("does not match trigger" in x for x in quality_review_file(root,p)[0]))
            q["findings"][0]["hard_stop"]["trigger"]="PROTECTED_INVARIANT";dump(p,q)
            self.assertEqual([],quality_review_file(root,p)[0])

    def test_unresolved_findings_cannot_disappear_from_handover(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root);ptr=write_clear_quality_review(root,ep);p=root/ptr["path"];q=yaml.safe_load(p.read_text())
            q["procedure_results"][1]["result"]="FINDINGS";q["findings"]=[{"id":"QF-2","blueprint":"testing","classification":"TEST_GAP","severity":"MEDIUM","disposition":"DEFERRED","statement":"A non-blocking edge-case test remains.","evidence":["review:test-gap"],"blocks_execution":False,"hard_stop":None}];q["overall_state"]="NEEDS_ATTENTION";q["successor_handover"]={"unresolved_findings":[],"follow_up":[]};dump(p,q)
            self.assertTrue(any("exactly transfer" in x for x in quality_review_file(root,p)[0]))

if __name__=="__main__":unittest.main()
