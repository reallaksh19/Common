#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

BP = Path(__file__).resolve().parents[1]


def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compiler = mod("bp_m2d_composition", BP / "engine" / "compile_m2d_composition_plan.py")
POLICY = json.loads((BP / "policy" / "m2d-composition-release.v1.json").read_text())
STAGES = json.loads((BP / "policy" / "core1a-stage-machine.v1.json").read_text())["pre_manuscript_stages"]
CHAPTER, READINESS = compiler.current_real_inputs()


def repository_stage_run(*, run_id="C1A-RUN-PHY-M2D-REPOSITORY-TEST"):
    rows = []
    for i, stage in enumerate(STAGES):
        rows.append({
            "stage":stage,
            "status":"PASS",
            "artifact_refs":[f"repo:Grade 9/V2/Physics/Core1A/registry/real-stage-artifacts.json#{i}"],
            "evidence_refs":[f"repo:Grade 9/V2/Physics/Core1A/registry/real-stage-evidence.json#{i}"],
            "notes":[],
        })
    out = {
        "schema_version":"1.0.0",
        "run_id":run_id,
        "topic_id":"PHY-M2D",
        "join_ref":"J-PHY-M2D-REPOSITORY-TEST",
        "join_digest":"1"*64,
        "control_state_ref":"CTRL-PHY-M2D-P20-REPOSITORY-TEST",
        "control_digest":"2"*64,
        "stage_results":rows,
        "unresolved_required_jump_count":0,
        "manuscript_gate":"RELEASED",
        "next_stage":"1A12_MANUSCRIPT",
        "block_reasons":[],
    }
    out["stage_run_digest"] = compiler.digest(out)
    return out


def binding(stage_run, *, chapter_digest=None):
    artifacts = sorted({ref for row in stage_run["stage_results"] for ref in row["artifact_refs"] if ref.startswith("repo:")})
    evidence = sorted({ref for row in stage_run["stage_results"] for ref in row["evidence_refs"] if ref.startswith("repo:")})
    out = {
        "schema_version":"1.0.0",
        "binding_id":"M2D-MANUSCRIPT-RELEASE-REPOSITORY-TEST",
        "topic_id":"PHY-M2D",
        "provenance_class":"REPOSITORY_PRODUCTION",
        "stage_run_ref":stage_run["run_id"],
        "stage_run_digest":stage_run["stage_run_digest"],
        "chapter_plan_digest":chapter_digest or CHAPTER["plan_digest"],
        "repository_artifact_refs":artifacts,
        "repository_evidence_refs":evidence,
    }
    out["binding_digest"] = compiler.digest(out)
    return out


class M2DCompositionGateTests(unittest.TestCase):
    def test_current_real_chapter_maps_all_concepts_but_blocks_without_real_stage_release(self):
        plan = compiler.compile_composition_plan(CHAPTER, READINESS, POLICY)
        self.assertEqual(len(plan["sections"]), 10)
        self.assertEqual(plan["summary"]["mapped_concept_count"], 10)
        self.assertEqual(plan["summary"]["representation_status"], "READY_FOR_RENDER_ADAPTER")
        self.assertEqual(plan["summary"]["composition_status"], "BLOCKED_UPSTREAM_MANUSCRIPT_RELEASE")
        self.assertEqual(plan["summary"]["publication_ir_gate"], "BLOCKED")
        self.assertFalse(plan["summary"]["renderer_invocation_allowed"])
        self.assertFalse(plan["summary"]["release_authorized"])

    def test_process_golden_can_never_authorize_real_publication(self):
        stage = repository_stage_run(run_id="C1A-RUN-PHY-M2D-GOLDEN-001")
        b = binding(stage)
        with self.assertRaisesRegex(AssertionError, "M2D_MANUSCRIPT_PROCESS_FIXTURE_FORBIDDEN"):
            compiler.compile_composition_plan(CHAPTER, READINESS, POLICY, stage_run=stage, release_binding=b)

    def test_chapter_digest_mismatch_fails_closed(self):
        stage = repository_stage_run()
        b = binding(stage, chapter_digest="0"*64)
        with self.assertRaisesRegex(AssertionError, "M2D_MANUSCRIPT_CHAPTER_DIGEST_DRIFT"):
            compiler.compile_composition_plan(CHAPTER, READINESS, POLICY, stage_run=stage, release_binding=b)

    def test_release_without_repository_backed_stage_evidence_fails_closed(self):
        stage = repository_stage_run()
        stage["stage_results"][3]["evidence_refs"] = ["A-NOT-REPOSITORY-EVIDENCE"]
        stage["stage_run_digest"] = compiler.digest_without_field(stage, "stage_run_digest")
        b = binding(stage)
        with self.assertRaisesRegex(AssertionError, "M2D_MANUSCRIPT_STAGE_REPOSITORY_EVIDENCE_REQUIRED"):
            compiler.compile_composition_plan(CHAPTER, READINESS, POLICY, stage_run=stage, release_binding=b)

    def test_representation_gap_still_blocks_even_with_valid_repository_stage_release(self):
        stage = repository_stage_run(); b = binding(stage)
        readiness = copy.deepcopy(READINESS)
        readiness["concepts"][0]["state"] = "BLOCKED_NEEDS_PRIMITIVE"
        readiness["concepts"][0]["missing_primitive_capabilities"] = ["TEST_GAP"]
        readiness["summary"]["ready_count"] -= 1
        readiness["summary"]["blocked_count"] += 1
        readiness["summary"]["blocked_concept_ids"] = [readiness["concepts"][0]["concept_id"]]
        readiness["summary"]["status"] = "BLOCKED_REPRESENTATION_GAP"
        readiness["readiness_digest"] = compiler.digest_without_field(readiness, "readiness_digest")
        plan = compiler.compile_composition_plan(CHAPTER, readiness, POLICY, stage_run=stage, release_binding=b)
        self.assertEqual(plan["summary"]["composition_status"], "BLOCKED_REPRESENTATION_GAP")
        self.assertEqual(plan["summary"]["publication_ir_gate"], "BLOCKED")

    def test_valid_repository_backed_release_opens_only_publication_ir_gate(self):
        stage = repository_stage_run(); b = binding(stage)
        plan = compiler.compile_composition_plan(CHAPTER, READINESS, POLICY, stage_run=stage, release_binding=b)
        self.assertEqual(plan["summary"]["composition_status"], "READY_FOR_PUBLICATION_IR")
        self.assertEqual(plan["summary"]["publication_ir_gate"], "OPEN")
        self.assertEqual(plan["summary"]["next_action"], "COMPILE_PUBLICATION_IR")
        self.assertFalse(plan["summary"]["renderer_invocation_allowed"])
        self.assertFalse(plan["summary"]["release_authorized"])

    def test_semantic_digest_and_representation_refs_are_bound_per_real_concept(self):
        plan = compiler.compile_composition_plan(CHAPTER, READINESS, POLICY)
        chapter_by_id = {row["concept_id"]:row for row in CHAPTER["concepts"]}
        for section in plan["sections"]:
            self.assertEqual(section["semantic_digest"], compiler.digest(chapter_by_id[section["concept_id"]]))
            self.assertTrue(section["authorized_representation_refs"])


if __name__ == "__main__":
    unittest.main()
