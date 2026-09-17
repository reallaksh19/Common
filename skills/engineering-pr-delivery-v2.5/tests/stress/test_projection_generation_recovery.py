from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]))
from test_core import good
from validate_projection_convergence import validate as projection

def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def stale_projection():
    target="issue:synthetic-handover"
    return {
        "required":True,"state":"STALE","operation_id":"PROJ-3","target":target,
        "roadmap_revision":"RM-0003","execution_ref":"EP-1","receipt":None,"basis":[],
        "observed":{"operation_id":"PROJ-1","target":target,"roadmap_revision":"RM-0001","execution_ref":"EP-1","receipt":"receipt-1","basis":["observed:receipt-1"]},
        "superseded_operations":[{"operation_id":"PROJ-2","target":target,"roadmap_revision":"RM-0002","execution_ref":"EP-1","disposition":"SUPERSEDED_BEFORE_PUBLICATION","superseded_by":"PROJ-3","receipt":None,"basis":["repository advanced to RM-0003"]}],
    }

def readiness(projection_ready=False):return {"baton_ready":True,"projection_ready":projection_ready,"handover_ready":projection_ready,"reasons":[]}

class ProjectionGenerationRecoveryTests(unittest.TestCase):
    def test_multiple_repository_revisions_converge_to_newest_projection_only(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["roadmap"]["revision"]="RM-0003";s["projection"]=stale_projection();s["relay_readiness"]=readiness(False);s["relay_readiness"]["reasons"]=["External projection is stale"];dump(root/"agents/relay/REPO_STATE.yaml",s)
            errors,warnings=projection(root);self.assertEqual([],errors);self.assertTrue(any("newest desired operation" in x for x in warnings))

    def test_stale_projection_top_level_must_track_current_repository_truth(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["roadmap"]["revision"]="RM-0003";s["projection"]=stale_projection();s["projection"]["roadmap_revision"]="RM-0002";s["relay_readiness"]=readiness(False);dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertTrue(any("newest desired roadmap_revision" in x for x in projection(root)[0]))

    def test_superseded_projection_operation_has_no_retry_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["roadmap"]["revision"]="RM-0003";s["projection"]=stale_projection();s["projection"]["operation_id"]="PROJ-2";s["relay_readiness"]=readiness(False);dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertTrue(any("reuses current operation_id" in x for x in projection(root)[0]))

    def test_superseded_generation_chain_must_terminate_at_current_operation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["roadmap"]["revision"]="RM-0003";s["projection"]=stale_projection();s["projection"]["superseded_operations"][0]["superseded_by"]="PROJ-X";s["relay_readiness"]=readiness(False);dump(root/"agents/relay/REPO_STATE.yaml",s)
            errors=projection(root)[0];self.assertTrue(any("unknown superseded_by" in x for x in errors));self.assertTrue(any("does not terminate" in x for x in errors))

    def test_published_unconfirmed_old_generation_can_be_retired_with_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["roadmap"]["revision"]="RM-0003";p=stale_projection();p["superseded_operations"][0].update({"disposition":"SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED","receipt":"receipt-2"});s["projection"]=p;s["relay_readiness"]=readiness(False);dump(root/"agents/relay/REPO_STATE.yaml",s);self.assertEqual([],projection(root)[0])

    def test_latest_generation_can_publish_then_become_in_sync(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root);s["roadmap"]["revision"]="RM-0003";p=stale_projection();p.update({"state":"PUBLISHED_UNCONFIRMED","receipt":"receipt-3"});s["projection"]=p;s["relay_readiness"]=readiness(False);s["relay_readiness"]["reasons"]=["Latest publication awaits verification"];dump(root/"agents/relay/REPO_STATE.yaml",s);self.assertEqual([],projection(root)[0])
            p["state"]="IN_SYNC";p["basis"]=["verified:receipt-3"];p["observed"]={"operation_id":"PROJ-3","target":p["target"],"roadmap_revision":"RM-0003","execution_ref":"EP-1","receipt":"receipt-3","basis":["verified:receipt-3"]};s["relay_readiness"]=readiness(True);dump(root/"agents/relay/REPO_STATE.yaml",s);self.assertEqual([],projection(root)[0])

if __name__=="__main__":unittest.main()
