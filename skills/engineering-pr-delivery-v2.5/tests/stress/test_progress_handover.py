from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]))
from test_core import good,dump
from relaylib import load_yaml
from validate_progress import validate as validate_progress
from validate_ep_semantics import validate as validate_ep
from render_handover import render as render_handover
from report_projection import build as build_report

class ProgressHandoverStressTests(unittest.TestCase):
    def test_phase_and_ep_mirrors_must_match_authoritative_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);s=load_yaml(root/"agents/relay/REPO_STATE.yaml");s["progress"]["phase_percent"]=99;s["progress"]["ep_percent"]=88;dump(root/"agents/relay/REPO_STATE.yaml",s)
            errors=validate_progress(root)[0];self.assertTrue(any("phase_percent mirror" in x for x in errors));self.assertTrue(any("ep_percent mirror" in x for x in errors))
            text=render_handover(root);self.assertIn("PHASE-1 — 50%",text);self.assertIn("EP-1 — 50%",text);self.assertNotIn("99%",text);self.assertNotIn("88%",text)
    def test_missing_roadmap_progress_row_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);p=load_yaml(root/"agents/relay/roadmap/PROGRESS.yaml");p["work_packages"]=[];dump(root/"agents/relay/roadmap/PROGRESS.yaml",p);self.assertTrue(any("missing roadmap ids" in x for x in validate_progress(root)[0]))
    def test_handover_renders_objective_phase_wp_step_acceptance_and_next_work(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);text=render_handover(root)
            for expected in ("OBJ-1","PHASE-1","WP-1","STEP-1","AC-1","Implement the bounded synthetic result.","BENCH-1","synthetic-progress"):self.assertIn(expected,text)
    def test_next_work_references_must_be_current_ep_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);ep=load_yaml(root/"agents/relay/execution-packages/EP-1.yaml");ep["next_work"]["steps"][0]["tests"]=["OLD-TEST"];dump(root/"agents/relay/execution-packages/EP-1.yaml",ep);self.assertTrue(any("references unknown validation id OLD-TEST" in x for x in validate_ep(root)[0]))
    def test_next_work_order_must_be_contiguous(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);ep=load_yaml(root/"agents/relay/execution-packages/EP-1.yaml");copy=dict(ep["next_work"]["steps"][0]);copy["order"]=3;ep["next_work"]["steps"].append(copy);dump(root/"agents/relay/execution-packages/EP-1.yaml",ep);self.assertTrue(any("order must be contiguous" in x for x in validate_ep(root)[0]))
    def test_report_projection_is_derived_and_source_bound(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);before=build_report(root);p=load_yaml(root/"agents/relay/roadmap/PROGRESS.yaml");p["acceptance_criteria"][0].update({"status":"COMPLETE","earned_weight":100,"percent":100});p["implementation_steps"][0].update({"earned_weight":100,"percent":100});p["execution_packages"][0].update({"earned_weight":100,"percent":100});p["work_packages"][0].update({"earned_weight":100,"percent":100});p["phases"][0].update({"earned_weight":100,"percent":100});p["objectives"][0].update({"earned_weight":100,"percent":100});p["overall"].update({"earned_weight":100,"percent":100});dump(root/"agents/relay/roadmap/PROGRESS.yaml",p);after=build_report(root);self.assertNotEqual(before["generated_from"]["progress_digest"],after["generated_from"]["progress_digest"]);self.assertEqual(50,before["progress"]["overall_percent"]);self.assertEqual(100,after["progress"]["overall_percent"]);self.assertEqual("COMPLETE",after["acceptance"][0]["status"])
if __name__=="__main__":unittest.main()
