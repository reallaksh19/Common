#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AGENT_TASKS = ROOT / "Grade 9" / "V2" / "Shared" / "AgentTasks"
ENGINE = AGENT_TASKS / "engine"
sys.path.insert(0, str(ENGINE))

from compile_execution_packet import (  # noqa: E402
    PacketCompilationError,
    compile_packet,
    validate_task,
    verify_packet_digest,
)
from resolve_execution_authority import AuthorityResolutionError  # noqa: E402
from validate_execution_report import ReportValidationError, validate_report  # noqa: E402

VALID_TASK = AGENT_TASKS / "fixtures" / "valid" / "physics-subtopic-engineering.task.json"
INVALID_MANUAL_READY = AGENT_TASKS / "fixtures" / "invalid" / "manual-readiness.task.json"
ROUTING_REL = Path("Grade 9/V2/Shared/AgentTasks/registry/authority-routing.v1.json")
ROADMAP_REL = Path("Grade 9/V2/Shared/LearningEngineering/registry/skp-schema-roadmap.v1.json")
FIXED_HEAD = "1" * 40


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def make_authority_copy(destination: Path, subject: str = "PHYSICS") -> None:
    copy_file(ROOT / ROUTING_REL, destination / ROUTING_REL)
    routing = load_json(ROOT / ROUTING_REL)
    for row in routing["authority_classes"]:
        rel = Path(row["path"])
        copy_file(ROOT / rel, destination / rel)

    roadmap = load_json(ROOT / ROADMAP_REL)
    adapters = [row for row in roadmap["subject_adapters"] if row["subject"] == subject]
    if len(adapters) != 1:
        raise AssertionError(f"expected one {subject} adapter in current roadmap")
    manifest_rel = Path(adapters[0]["current_authority_manifest_ref"])
    copy_file(ROOT / manifest_rel, destination / manifest_rel)


def base_report(packet: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "task_id": packet["task"]["task_id"],
        "packet_digest": packet["packet_digest"],
        "start_head": packet["repository_state"]["resolved_head"],
        "end_head": packet["repository_state"]["resolved_head"],
        "execution_result": "COMPLETE",
        "engineering_state": "NOT_EVALUATED",
        "research_state": "NOT_EVALUATED",
        "consumer_permissions": {},
        "publication_state": "NOT_IMPLIED",
        "authority_bindings_used": copy.deepcopy(packet["authority_bindings"]),
        "changed_files": [],
        "tests": [],
        "workflows": [],
        "blockers": [],
        "limitations": [],
        "unresolved": [],
        "architecture_findings": [],
        "memory_dependency_detected": False,
    }


class ExecutionKernelTests(unittest.TestCase):
    def setUp(self):
        self.task = load_json(VALID_TASK)

    def compile_in_copy(self, root: Path, task: dict | None = None) -> dict:
        make_authority_copy(root)
        return compile_packet(
            task or self.task,
            repo_root=root,
            head_sha=FIXED_HEAD,
            working_tree_state="CLEAN",
        )

    def test_same_task_same_authority_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_a = self.compile_in_copy(root)
            packet_b = compile_packet(
                self.task,
                repo_root=root,
                head_sha=FIXED_HEAD,
                working_tree_state="CLEAN",
            )
            self.assertEqual(packet_a, packet_b)
            verify_packet_digest(packet_a)

    def test_authority_change_changes_packet_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_a = self.compile_in_copy(root)
            source_governance = root / "Grade 9/V2/Shared/LearningEngineering/SOURCE_GOVERNANCE.md"
            source_governance.write_text(
                source_governance.read_text(encoding="utf-8") + "\n<!-- authority mutation falsifier -->\n",
                encoding="utf-8",
            )
            packet_b = compile_packet(
                self.task,
                repo_root=root,
                head_sha=FIXED_HEAD,
                working_tree_state="CLEAN",
            )
            self.assertNotEqual(packet_a["packet_digest"], packet_b["packet_digest"])
            digest_a = {row["authority_class"]: row["sha256"] for row in packet_a["authority_bindings"]}
            digest_b = {row["authority_class"]: row["sha256"] for row in packet_b["authority_bindings"]}
            self.assertNotEqual(digest_a["SOURCE_GOVERNANCE"], digest_b["SOURCE_GOVERNANCE"])

    def test_manual_readiness_is_rejected(self):
        with self.assertRaises(PacketCompilationError) as ctx:
            validate_task(load_json(INVALID_MANUAL_READY))
        self.assertEqual(ctx.exception.code, "E_AGENT_MANUAL_AUTHORITY_ASSERTION")

    def test_explicit_stale_sha_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_authority_copy(root)
            task = copy.deepcopy(self.task)
            task["target_ref"] = "2" * 40
            with self.assertRaises(AuthorityResolutionError) as ctx:
                compile_packet(task, repo_root=root, head_sha=FIXED_HEAD, working_tree_state="CLEAN")
            self.assertEqual(ctx.exception.code, "E_AGENT_STALE_TARGET")

    def test_preflight_never_grants_readiness_or_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = self.compile_in_copy(Path(tmp))
        self.assertEqual(packet["engineering_preflight"]["engineering_state"], "NOT_EVALUATED")
        self.assertEqual(packet["engineering_preflight"]["publication_authorization"], "NOT_IMPLIED")
        self.assertTrue(
            all(row["status"] == "NOT_EVALUATED" for row in packet["engineering_preflight"]["consumer_permissions"].values())
        )

    def test_subject_generation_authority_is_derived_from_current_roadmap(self):
        roadmap = load_json(ROOT / ROADMAP_REL)
        adapter = next(row for row in roadmap["subject_adapters"] if row["subject"] == self.task["subject"])
        with tempfile.TemporaryDirectory() as tmp:
            packet = self.compile_in_copy(Path(tmp))
        binding = next(row for row in packet["authority_bindings"] if row["authority_class"] == "SUBJECT_GENERATION_AUTHORITY")
        self.assertEqual(binding["path"], adapter["current_authority_manifest_ref"])
        self.assertEqual(packet["learning_engineering_state"]["subject_adapter"]["status"], adapter["status"])
        self.assertEqual(
            packet["learning_engineering_state"]["subject_adapter"]["runtime_authority"],
            adapter["runtime_authority"],
        )

    def test_generation_authority_grade_scope_matches_or_holds_generically(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_match = self.compile_in_copy(root)
            grade_scope = packet_match["learning_engineering_state"]["subject_adapter"]["generation_authority_scope"]
            self.assertEqual(grade_scope["task_grade"], self.task["grade"])
            self.assertIn(self.task["grade"], grade_scope["declared_grades"])
            self.assertEqual(grade_scope["grade_state"], "MATCH")

            mismatched = copy.deepcopy(self.task)
            mismatched["task_id"] = "TASK-GENERIC-GRADE-MISMATCH"
            mismatched["grade"] = self.task["grade"] + 2
            packet_mismatch = compile_packet(
                mismatched,
                repo_root=root,
                head_sha=FIXED_HEAD,
                working_tree_state="CLEAN",
            )
            mismatch_scope = packet_mismatch["learning_engineering_state"]["subject_adapter"]["generation_authority_scope"]
            self.assertEqual(mismatch_scope["grade_state"], "MISMATCH")
            self.assertEqual(packet_mismatch["engineering_preflight"]["engineering_state"], "NOT_EVALUATED")
            self.assertEqual(packet_mismatch["engineering_preflight"]["publication_authorization"], "NOT_IMPLIED")
            self.assertTrue(any("task grade" in blocker.lower() for blocker in packet_mismatch["engineering_preflight"]["blockers"]))

    def test_task_registry_contains_no_subject_ontology(self):
        text = (AGENT_TASKS / "registry" / "task-kind-registry.v1.json").read_text(encoding="utf-8").lower()
        banned = [
            "allowed_representations",
            "mandatory_falsifiers",
            "epistemological_rules",
            "curriculum_tiers",
            "free_body_diagram",
            "thermodynamic_pv_cycle",
        ]
        for token in banned:
            self.assertNotIn(token, text)

    def test_kernel_contains_no_exam_to_depth_mapping(self):
        targets = [*ENGINE.glob("*.py"), *AGENT_TASKS.joinpath("registry").glob("*.json"), *AGENT_TASKS.joinpath("contracts").glob("*.json")]
        text = "\n".join(path.read_text(encoding="utf-8") for path in targets).upper()
        for token in ["JEE MAIN", "JEE_MAINS", "JEE ADVANCED", "JEE_ADVANCED", "OLYMPIAD"]:
            self.assertNotIn(token, text)

    def test_engine_contains_no_current_pilot_case_literals(self):
        roadmap = load_json(ROOT / ROADMAP_REL)
        engine_text = "\n".join(path.read_text(encoding="utf-8") for path in ENGINE.glob("*.py"))
        for pilot in roadmap.get("pilots", []):
            self.assertNotIn(pilot["pilot_id"], engine_text)
            self.assertNotIn(pilot["target"], engine_text)

    def test_blueprint_change_is_not_an_allowed_task_change_class(self):
        registry = load_json(AGENT_TASKS / "registry" / "task-kind-registry.v1.json")
        for row in registry["task_kinds"]:
            self.assertNotIn("BLUEPRINT", row["allowed_change_classes"])
            self.assertEqual(row["blueprint_change_policy"], "PROHIBITED_REQUIRES_NEW_INVARIANT_TASK")

    def test_report_rejects_blueprint_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = self.compile_in_copy(Path(tmp))
        report = base_report(packet)
        report["changed_files"] = [{
            "path": "Grade 9/V2/Physics/Blueprint/example.py",
            "change_class": "BLUEPRINT",
            "reason": "case patch",
            "authority_impact": "would bypass upstream Engineering",
        }]
        with self.assertRaises(ReportValidationError) as ctx:
            validate_report(packet, report)
        self.assertEqual(ctx.exception.code, "E_AGENT_BLUEPRINT_CHANGE_PROHIBITED")

    def test_report_must_declare_stale_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = self.compile_in_copy(Path(tmp))
        report = base_report(packet)
        report["start_head"] = "2" * 40
        report["end_head"] = "2" * 40
        with self.assertRaises(ReportValidationError) as ctx:
            validate_report(packet, report)
        self.assertEqual(ctx.exception.code, "E_AGENT_REPORT_STALE_PACKET_NOT_DECLARED")
        report["execution_result"] = "STALE_PACKET"
        validate_report(packet, report)

    def test_packet_digest_detects_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = self.compile_in_copy(Path(tmp))
        packet["task"]["topic"] = "mutated"
        with self.assertRaises(PacketCompilationError) as ctx:
            verify_packet_digest(packet)
        self.assertEqual(ctx.exception.code, "E_AGENT_PACKET_DIGEST_MISMATCH")


if __name__ == "__main__":
    unittest.main()
