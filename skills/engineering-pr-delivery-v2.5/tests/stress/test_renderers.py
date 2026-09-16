from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parent))
from bootstrap_relay import build as bootstrap_build,apply as bootstrap_apply
from render_handover import render as render_handover
from render_status import render as render_status
from test_parallel_bootstrap import parallel_repo,dump
from test_parallel_convergence import converge

class RendererStressTests(unittest.TestCase):
    def test_parallel_renderers_show_lanes_integration_authority_and_readiness(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,state=parallel_repo(root);state["status_planes"]["execution"]["material_authority"]="READ_ONLY";state["status_planes"]["execution"]["next_action"]="Reconcile lane evidence without engineering writes.";dump(root/"agents/relay/REPO_STATE.yaml",state)
            status=render_status(root);handover=render_handover(root)
            self.assertIn("Parallel plan",status);self.assertIn("LANE-A",status);self.assertIn("Integration",status);self.assertIn("Material authority: **Read Only**",status);self.assertIn("Handover ready: **YES**",status)
            self.assertIn("Parallel plan PLAN-P1",handover);self.assertIn("EP-A",handover);self.assertIn("WP-I",handover);self.assertIn("material authority: **Read Only**",handover);self.assertIn("Full custody handover ready? **YES**",handover)

    def test_integration_renderer_shows_multi_parent_join_baton(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);converge(root)
            status=render_status(root);handover=render_handover(root)
            self.assertIn("Parallel join predecessor: `JOIN-P1`",status)
            self.assertIn("Parallel convergence JOIN-P1",handover);self.assertIn("checkpoint `CP-A`",handover);self.assertIn("checkpoint `CP-B`",handover)

    def test_initializing_renderers_do_not_require_an_ep_and_are_not_repository_ready(self):
        manifest={"schema_version":"relay-v2.5-bootstrap","repository":{"name":"synthetic","remote":"owner/synthetic","repository_type":"application","default_branch":"main"},"relay_protocol":{"basis_ref":"abc"},"roadmap":{"id":"RM-B","revision":"RM-0001","title":"Bootstrap"},"initial_position":{"objective":{"id":"OBJ-1","title":"Objective"},"phase":{"id":"PHASE-1","title":"Phase"},"work_package":{"id":"WP-1","title":"Discovery"}},"initialization":{"next_action":"Reconcile owner intent and define the first executable package.","notes":[]}}
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);bootstrap_apply(root,bootstrap_build(manifest))
            status=render_status(root);handover=render_handover(root)
            self.assertIn("Initializing",status);self.assertIn("NONE",status);self.assertIn("Repository recovery ready: **NO**",status);self.assertIn("Material authority: **None**",status)
            self.assertIn("Initializing",handover);self.assertIn("No active material EP",handover);self.assertIn("Repository recovery ready? **NO**",handover);self.assertIn("material authority: **None**",handover)

if __name__=="__main__":unittest.main()
