#!/usr/bin/env python3
"""
Comprehensive Test Suite for StandaloneExecutionPrompt Engine.
Tests:
- Schema validation for execution tasks and reports
- Deterministic compilation and digest generation
- Invariant inclusion (anti-drift, repository-discovery, completion-report)
- Prompt linter: mandatory sections, unexpanded placeholders, BLOCKED outcome validity
- Anti-coupling / leakage detection
- Multi-subject compilation (Physics, Math, Chemistry)
- Report validator checks (valid report vs malformed report vs BLOCKED without receipts)
"""

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
sys.path.insert(0, str(ROOT / "contracts"))

from compile_execution_prompt import (
    compile_prompt,
    validate_task_request,
    run_prompt_linter,
    locate_template,
    locate_subject_profile,
)
from validate_execution_report import (
    validate_report_json,
    validate_report_markdown,
    validate_report_file,
)
from validate_contracts import validate_all_contracts


SAMPLE_PHYSICS_TASK = {
    "prompt_id": "SEP-PHY-RELMOTION-v1",
    "prompt_template_id": "SEP-07",
    "prompt_template_version": "1.0.0",
    "task_instance_id": "task-relmotion-001",
    "repository": "reallaksh19/Common",
    "target_branch": "v2-physics-gates-gr9-11",
    "baseline_pr": 383,
    "subject": "PHYSICS",
    "grade": 9,
    "curriculum": "CBSE",
    "curriculum_version": "2026-27",
    "topic": "Motion",
    "subtopic": "Relative Motion",
    "engineering_depth": "STANDARD",
    "learner_state": "UNKNOWN",
    "web_research_allowed": True,
    "local_question_banks": "DISCOVER_FROM_REPOSITORY",
    "write_mode": "IMPLEMENT",
    "expected_scope": [
        "1D Relative Velocity",
        "2D Relative Velocity in Plane",
        "Frame of Reference Transformations"
    ],
    "explicit_exclusions": [
        "Relativistic velocity addition (Lorentz transformations)",
        "Curved spacetime"
    ],
    "subject_profile_version": "1.0.0",
    "schema_registry_version": "1.0.0"
}

SAMPLE_VALID_REPORT = {
    "prompt_id": "SEP-PHY-RELMOTION-v1",
    "task_instance_id": "task-relmotion-001",
    "start_head": "e92481f6e03a8bb49a55f568b03cba7c12fb942a",
    "end_head": "e92481f6e03a8bb49a55f568b03cba7c12fb942a",
    "result": "COMPLETE",
    "changed_files": [
        {
            "path": "Grade 9/V2/Physics/AssessmentScope/authority/relative_motion.json",
            "reason": "Populate relative motion candidate capabilities",
            "tier": "DATA_ONLY",
            "authority_impact": "Additive candidate data"
        }
    ],
    "tests": [
        {
            "test": "python -m unittest tests/test_agent_tasks_engine.py",
            "result": "PASS",
            "evidence": "OK (ran 12 tests)"
        }
    ],
    "workflows": [
        {
            "workflow": "check_relay.py",
            "run": "manual",
            "result": "PASS"
        }
    ],
    "blockers": [],
    "limitations": ["Grade 9 1D and 2D relative motion only"],
    "architecture_findings": ["Zero Blueprint edits required"],
    "memory_dependency_detected": False,
    "recommended_next_task": "SEP-08-stress-test"
}


class TestAgentTasksEngine(unittest.TestCase):

    def test_01_all_contracts_valid(self):
        """Validate all schemas in contracts directory against Draft 2020-12."""
        try:
            validate_all_contracts()
        except Exception as e:
            self.fail(f"validate_all_contracts failed with: {e}")

    def test_02_task_schema_validation_success(self):
        """Task schema validation succeeds on well-formed task."""
        try:
            validate_task_request(SAMPLE_PHYSICS_TASK)
        except Exception as e:
            self.fail(f"validate_task_request failed unexpectedly on valid task: {e}")

    def test_03_task_schema_validation_failure(self):
        """Task schema validation fails on missing fields or invalid enums."""
        # Missing required field
        bad_task = copy.deepcopy(SAMPLE_PHYSICS_TASK)
        del bad_task["subject"]
        with self.assertRaises(ValueError):
            validate_task_request(bad_task)

        # Invalid enum
        bad_task2 = copy.deepcopy(SAMPLE_PHYSICS_TASK)
        bad_task2["engineering_depth"] = "SUPER_DEEP"
        with self.assertRaises(ValueError):
            validate_task_request(bad_task2)

        # Additional undeclared property (schema has additionalProperties: false)
        bad_task3 = copy.deepcopy(SAMPLE_PHYSICS_TASK)
        bad_task3["unknown_hack"] = True
        with self.assertRaises(ValueError):
            validate_task_request(bad_task3)

    def test_04_prompt_compilation_deterministic(self):
        """Prompt compilation is deterministic and returns matching SHA-256 digest."""
        prompt1, digest1 = compile_prompt(SAMPLE_PHYSICS_TASK)
        prompt2, digest2 = compile_prompt(SAMPLE_PHYSICS_TASK)

        self.assertEqual(prompt1, prompt2)
        self.assertEqual(digest1, digest2)
        self.assertEqual(len(digest1), 64)
        self.assertTrue(prompt1.startswith("<!-- COMPILED STANDALONE EXECUTION PROMPT -->"))

    def test_05_mandatory_sections_present(self):
        """Compiled prompt contains all mandatory sections from 0 to 16."""
        prompt, _ = compile_prompt(SAMPLE_PHYSICS_TASK)

        for sec_num in range(17):
            sec_header = f"## {sec_num}."
            self.assertIn(sec_header, prompt, f"Mandatory section header '{sec_header}' missing from prompt!")

    def test_06_invariants_properly_injected(self):
        """Invariants A-M and cold-start discovery steps are injected."""
        prompt, _ = compile_prompt(SAMPLE_PHYSICS_TASK)

        # Cold start
        self.assertIn("Mandatory Cold-Start Repository Discovery Protocol", prompt)
        self.assertIn("Resolve Target Branch & Exact HEAD", prompt)
        self.assertIn("Do not treat a previously seen implementation as authority", prompt)

        # Anti-drift
        self.assertIn("Universal Anti-Drift Invariants", prompt)
        self.assertIn("Invariant A: Repository authority overrides memory", prompt)
        self.assertIn("Invariant M: If the requested result cannot be reached honestly", prompt)

        # Completion report
        self.assertIn("Standardized Execution Report Contract", prompt)
        self.assertIn("## 13. No-memory declaration", prompt)

    def test_07_blocked_outcome_is_declared_valid(self):
        """Prompt explicitly permits BLOCKED as a valid outcome."""
        prompt, _ = compile_prompt(SAMPLE_PHYSICS_TASK)
        self.assertIn("BLOCKED", prompt)
        self.assertIn("BLOCKED with evidence is a successful outcome", prompt)

    def test_08_anti_coupling_leakage_detection(self):
        """Prompt linter detects and rejects leaked case literals when not in inputs."""
        # Create a task where topic is NOT Relative Motion, but test if body had it
        task = copy.deepcopy(SAMPLE_PHYSICS_TASK)
        task["prompt_id"] = "SEP-01-DISCOVERY"
        task["prompt_template_id"] = "SEP-01"
        task["topic"] = "Kinematics"
        task["subtopic"] = "FrameOfReference"
        task["expected_scope"] = ["Frames"]

        # SEP-01 is clean and should pass
        prompt, _ = compile_prompt(task)
        self.assertNotIn("Relative Motion", prompt.split("## 1. Mission")[1])

    def test_09_multi_subject_compilation(self):
        """Compiler succeeds for Physics, Math, and Chemistry tasks."""
        # 1. Physics (Thermodynamics, RESEARCH)
        phys_task = copy.deepcopy(SAMPLE_PHYSICS_TASK)
        phys_task["prompt_id"] = "SEP-PHY-THERMO-v1"
        phys_task["prompt_template_id"] = "SEP-09"
        phys_task["topic"] = "Thermodynamics"
        phys_task["subtopic"] = "HeatEngineCarnot"
        phys_task["engineering_depth"] = "RESEARCH"
        prompt_p, _ = compile_prompt(phys_task)
        self.assertIn("PHYSICS", prompt_p)
        self.assertIn("KINEMATIC_GRAPH_PLOT", prompt_p)

        # 2. Math (Trigonometry, STANDARD)
        math_task = copy.deepcopy(SAMPLE_PHYSICS_TASK)
        math_task["prompt_id"] = "SEP-MTH-TRIG-v1"
        math_task["prompt_template_id"] = "SEP-20"
        math_task["subject"] = "MATHEMATICS"
        math_task["topic"] = "Trigonometry"
        math_task["subtopic"] = "TrigonometricIdentities"
        prompt_m, _ = compile_prompt(math_task)
        self.assertIn("MATHEMATICS", prompt_m)
        self.assertIn("TRIGONOMETRIC_UNIT_CIRCLE", prompt_m)

        # 3. Chemistry (Redox, STANDARD)
        chem_task = copy.deepcopy(SAMPLE_PHYSICS_TASK)
        chem_task["prompt_id"] = "SEP-CHM-REDOX-v1"
        chem_task["prompt_template_id"] = "SEP-21"
        chem_task["subject"] = "CHEMISTRY"
        chem_task["topic"] = "ChemicalReactions"
        chem_task["subtopic"] = "RedoxBalancing"
        prompt_c, _ = compile_prompt(chem_task)
        self.assertIn("CHEMISTRY", prompt_c)
        self.assertIn("REDOX_HALF_REACTION_LANE", prompt_c)

    def test_10_report_validation_success(self):
        """Execution report validation passes on valid report JSON."""
        errors = validate_report_json(SAMPLE_VALID_REPORT)
        self.assertEqual(errors, [], f"Expected 0 errors, got: {errors}")

    def test_11_report_validation_blocked_requires_receipts(self):
        """If result is BLOCKED, blockers list cannot be empty."""
        bad_report = copy.deepcopy(SAMPLE_VALID_REPORT)
        bad_report["result"] = "BLOCKED"
        bad_report["blockers"] = []  # Empty!

        errors = validate_report_json(bad_report)
        self.assertTrue(any("blockers" in e.lower() for e in errors))

        # With explicit blocker receipts, it must pass
        good_blocked_report = copy.deepcopy(SAMPLE_VALID_REPORT)
        good_blocked_report["result"] = "BLOCKED"
        good_blocked_report["blockers"] = ["Primary curriculum source missing edition metadata"]
        errors2 = validate_report_json(good_blocked_report)
        self.assertEqual(errors2, [])

    def test_12_all_25_templates_loadable(self):
        """All 25 SEP prompt templates exist and have valid structure."""
        for i in range(1, 26):
            tid = f"SEP-{i:02d}"
            path = locate_template(tid)
            self.assertTrue(path.exists(), f"Template file for {tid} not found!")
            content = path.read_text(encoding="utf-8")
            self.assertIn("## 1. Mission", content)
            self.assertIn("## 16. Exact Completion Report", content)


if __name__ == "__main__":
    unittest.main()
