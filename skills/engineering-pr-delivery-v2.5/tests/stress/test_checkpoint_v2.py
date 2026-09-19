from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[2]/"scripts"))
sys.path.insert(0,str(HERE.parents[1]))

from test_core import good,dump
from relaylib import load_yaml
from validate_checkpoint import validate_file
from render_owner_status import render as owner_status
from validate_human_communication import validate as communication_check


def legacy_cp()->dict:
    return {
        "schema_version":"relay-v2.5",
        "checkpoint_id":"CP-1",
        "ep_id":"EP-1",
        "roadmap_basis":{"roadmap_id":"RM-T","revision":"RM-0001"},
        "execution_basis":{"material_ref":"abc"},
        "implementation_result":{},
        "acceptance_results":[],
        "validation_results":[],
        "quality_review":None,
        "quality_findings":[],
        "discoveries":[],
        "roadmap_reconciliation":{"result":"NO_ROADMAP_CHANGE"},
        "successor":{
            "mode":"SERIAL","frontier_work_package":"WP-1","ep_id":"EP-1",
            "parallel_plan":None,"lane_id":None,"lanes":[],
        },
    }


def write_cp(root:Path,cp:dict,point_state:bool=False)->Path:
    path=root/"agents/relay/checkpoints/CP-1.yaml";dump(path,cp)
    if point_state:
        state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
        state["last_checkpoint"]={"id":"CP-1","path":"agents/relay/checkpoints/CP-1.yaml"}
        dump(root/"agents/relay/REPO_STATE.yaml",state)
    return path


def make_v2(cp:dict)->dict:
    cp=copy.deepcopy(cp)
    cp["contract_version"]=2
    cp["implementation_result"]={
        "summary":"Completed the bounded synthetic implementation result.",
        "completed_steps":["STEP-1"],
        "files_changed":["src/example.py","tests/test_example.py"],
    }
    cp["known_limitations"]=["External qualification remains outside this synthetic fixture."]
    cp["remaining_work"]=["Run the next authorized execution-package step."]
    cp["roadmap_reconciliation"]={
        "result":"STATUS_UPDATE",
        "status_updates":["WP-1 checkpoint result recorded."],
        "proposals":[],
        "owner_decisions_required":[],
    }
    return cp


class CheckpointV2StressTests(unittest.TestCase):
    def test_legacy_checkpoint_remains_valid_with_migration_warning(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            path=write_cp(root,legacy_cp())
            errors,warnings=validate_file(path)
            self.assertEqual([],errors)
            self.assertTrue(any("legacy checkpoint contract" in x for x in warnings))

    def test_valid_v2_checkpoint_enforces_publication_fields(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            path=write_cp(root,make_v2(legacy_cp()))
            errors,warnings=validate_file(path)
            self.assertEqual([],errors)
            self.assertFalse(any("legacy checkpoint" in x for x in warnings))

    def test_v2_checkpoint_requires_implementation_summary_steps_and_files(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);base=make_v2(legacy_cp())
            for missing in ("summary","completed_steps","files_changed"):
                cp=copy.deepcopy(base);cp["implementation_result"].pop(missing)
                path=write_cp(root,cp)
                errors=validate_file(path)[0]
                self.assertTrue(any(f"implementation_result.{missing}" in x or missing in x for x in errors),missing)

    def test_v2_checkpoint_requires_limitations_remaining_work_and_reconciliation_arrays(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);base=make_v2(legacy_cp())
            for missing in ("known_limitations","remaining_work"):
                cp=copy.deepcopy(base);cp.pop(missing)
                path=write_cp(root,cp)
                self.assertTrue(any(missing in x for x in validate_file(path)[0]),missing)
            for missing in ("status_updates","proposals","owner_decisions_required"):
                cp=copy.deepcopy(base);cp["roadmap_reconciliation"].pop(missing)
                path=write_cp(root,cp)
                self.assertTrue(any(missing in x for x in validate_file(path)[0]),missing)

    def test_v2_checkpoint_allows_explicit_no_file_change(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            cp=make_v2(legacy_cp())
            cp["implementation_result"]={
                "summary":"Admission completed; no product files changed.",
                "completed_steps":["Repository admission completed."],
                "files_changed":[],
            }
            path=write_cp(root,cp)
            self.assertEqual([],validate_file(path)[0])

    def test_v2_checkpoint_files_and_completed_steps_reach_owner_publication(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            path=write_cp(root,make_v2(legacy_cp()),point_state=True)
            self.assertEqual([],validate_file(path)[0])
            text=owner_status(root)
            self.assertIn("Completed steps recorded now: STEP-1.",text)
            self.assertIn("Files changed in the current checkpoint result: src/example.py, tests/test_example.py.",text)
            self.assertEqual([],communication_check(root)[0])

    def test_v2_checkpoint_rejects_empty_publication_items(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            cp=make_v2(legacy_cp())
            cp["implementation_result"]["completed_steps"]=[""]
            cp["known_limitations"]=[""]
            cp["remaining_work"]=[{}]
            path=write_cp(root,cp)
            errors=validate_file(path)[0]
            self.assertTrue(any("completed_steps[0]" in x for x in errors))
            self.assertTrue(any("known_limitations[0]" in x for x in errors))
            self.assertTrue(any("remaining_work[0]" in x for x in errors))


if __name__=="__main__":
    unittest.main()
