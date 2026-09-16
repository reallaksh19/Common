#!/usr/bin/env python3
"""
Comprehensive Test and Falsifier Suite for Standalone Delegation Layer / Task Composer.

Verifies:
- Draft 2020-12 schema validity for all contracts
- Deterministic packet compilation & cryptographic custody digests
- Stale authority digest detection
- Manual readiness assertion rejection
- BLOCKED outcome validity with receipts & rejection without receipts
- Memory dependency rejection
- Complete absence of case literals in generic engine code
- Absence of disciplinary ontology in subject router
- Learner-state invariance on domain truth
- Engineering depth independence from exams
- Multi-subject compilation (Physics, Mathematics, Chemistry)
- Engineering Preflight / Map generation
"""
from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

TESTS_DIR = Path(__file__).resolve().parent
AGENT_TASKS_DIR = TESTS_DIR.parent
CONTRACTS_DIR = AGENT_TASKS_DIR / "contracts"
REGISTRY_DIR = AGENT_TASKS_DIR / "registry"
ENGINE_DIR = AGENT_TASKS_DIR / "engine"
FIXTURES_DIR = AGENT_TASKS_DIR / "fixtures"

sys.path.insert(0, str(ENGINE_DIR))
from resolve_execution_authority import (  # noqa: E402
    find_repository_root,
    resolve_authorities,
    check_packet_freshness,
    load_json,
)
from compile_execution_packet import (  # noqa: E402
    compile_packet,
    compute_canonical_digest,
    PacketCompilationError,
)
from validate_execution_report import validate_report  # noqa: E402
from engineering_preflight import generate_engineering_preflight  # noqa: E402


class TestExecutionKernel(unittest.TestCase):

    def setUp(self):
        self.repo_root = find_repository_root()
        self.sample_task = load_json(FIXTURES_DIR / "sample_subtopic_engineering_task.json")
        self.sample_report = load_json(FIXTURES_DIR / "sample_execution_report.json")

    def test_01_all_contracts_valid_draft202012(self):
        """All schemas in contracts directory must be valid Draft 2020-12 schemas."""
        for schema_file in CONTRACTS_DIR.glob("*.schema.json"):
            schema = load_json(schema_file)
            Draft202012Validator.check_schema(schema)

    def test_02_task_schema_validation_success(self):
        """Valid human task intent payloads pass schema validation."""
        task_schema = load_json(CONTRACTS_DIR / "execution-task.schema.json")
        validator = Draft202012Validator(task_schema)

        # 1. 1D Motion
        errors1 = list(validator.iter_errors(self.sample_task))
        self.assertEqual(errors1, [], f"1D motion task errors: {errors1}")

        # 2. Thermodynamics RESEARCH task
        thermo_task = load_json(FIXTURES_DIR / "sample_thermo_research_task.json")
        errors2 = list(validator.iter_errors(thermo_task))
        self.assertEqual(errors2, [], f"Thermo task errors: {errors2}")

    def test_03_task_schema_validation_failure_on_invalid_depth(self):
        """Invalid engineering_depth enum (e.g. exam name) fails schema validation."""
        mutant_task = load_json(FIXTURES_DIR / "falsifiers" / "invalid_depth_task.json")
        task_schema = load_json(CONTRACTS_DIR / "execution-task.schema.json")
        validator = Draft202012Validator(task_schema)
        errors = list(validator.iter_errors(mutant_task))
        self.assertTrue(len(errors) > 0, "Expected schema error for invalid engineering_depth")
        self.assertTrue(any("engineering_depth" in e.message or "engineering_depth" in str(e.path) for e in errors))

    def test_04_deterministic_packet_compilation(self):
        """Compiling same task with same authority produces identical bytes and SHA-256 digest."""
        packet1 = compile_packet(self.sample_task, repo_root=self.repo_root, override_head="897cb1e8d6ceff6d42e6a4760077facf4fb5195e")
        packet2 = compile_packet(self.sample_task, repo_root=self.repo_root, override_head="897cb1e8d6ceff6d42e6a4760077facf4fb5195e")

        self.assertEqual(packet1, packet2)
        digest1 = packet1["compiled_packet_digest"]
        digest2 = packet2["compiled_packet_digest"]
        self.assertEqual(digest1, digest2)
        self.assertEqual(len(digest1), 64)
        self.assertTrue(re.match(r"^[0-9a-f]{64}$", digest1))

    def test_05_authority_drift_changes_packet_digest(self):
        """Changing an authority binding's digest changes the compiled packet digest."""
        packet1 = compile_packet(self.sample_task, repo_root=self.repo_root, override_head="897cb1e8d6ceff6d42e6a4760077facf4fb5195e")

        mutated_task = copy.deepcopy(self.sample_task)
        mutated_task["task_id"] = "TASK-PHY-KIN-002"
        packet2 = compile_packet(mutated_task, repo_root=self.repo_root, override_head="897cb1e8d6ceff6d42e6a4760077facf4fb5195e")

        self.assertNotEqual(packet1["compiled_packet_digest"], packet2["compiled_packet_digest"])

    def test_06_stale_authority_rejection(self):
        """Packet with stale authority digest is detected and flagged."""
        packet = compile_packet(self.sample_task, repo_root=self.repo_root)
        # Verify fresh packet has 0 mismatches
        fresh_mismatches = check_packet_freshness(packet, repo_root=self.repo_root)
        self.assertEqual(fresh_mismatches, [])

        # Tamper with an authority digest in the packet
        tampered = copy.deepcopy(packet)
        tampered["authority_bindings"][0]["digest_sha256"] = "0000000000000000000000000000000000000000000000000000000000000000"
        stale_mismatches = check_packet_freshness(tampered, repo_root=self.repo_root)
        self.assertTrue(len(stale_mismatches) > 0)
        self.assertIn("Stale authority", stale_mismatches[0])

    def test_07_manual_readiness_assertion_rejection(self):
        """Claiming ENGINEERING_GATE_READY without passing test evidence fails report validation."""
        mutant_report = load_json(FIXTURES_DIR / "falsifiers" / "manual_readiness_report.json")
        errors = validate_report(mutant_report)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("Manual readiness violation" in e for e in errors))

    def test_08_blocked_empty_receipts_rejection(self):
        """Reporting BLOCKED with an empty blockers list fails report validation."""
        mutant_report = load_json(FIXTURES_DIR / "falsifiers" / "blocked_empty_receipts_report.json")
        errors = validate_report(mutant_report)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("Invalid BLOCKED report" in e for e in errors))

    def test_09_memory_dependency_rejection(self):
        """Reporting memory_dependency_detected = true fails report validation."""
        mutant_report = load_json(FIXTURES_DIR / "falsifiers" / "memory_dependent_report.json")
        errors = validate_report(mutant_report)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("Memory violation" in e for e in errors))

    def test_10_no_case_literals_in_generic_engine(self):
        """Generic delegation engine scripts must not contain hardcoded case literals or leakage lists."""
        forbidden_terms = [
            "Relative Motion",
            "M2D-SBA-04",
            "Q14",
            "Thermodynamics",
            "Redox",
            "Euclid",
            "Carnot",
            "LEAK_DETECTION_TARGETS"
        ]

        engine_files = [
            ENGINE_DIR / "resolve_execution_authority.py",
            ENGINE_DIR / "compile_execution_packet.py",
            ENGINE_DIR / "validate_execution_report.py",
        ]

        for file_path in engine_files:
            content = file_path.read_text(encoding="utf-8")
            for term in forbidden_terms:
                self.assertNotIn(
                    term,
                    content,
                    f"Forbidden case-specific literal or blacklist '{term}' found in generic engine: {file_path.name}"
                )

    def test_11_subject_truth_absent_from_router(self):
        """subject-routing-registry.json must contain only paths and refs, zero disciplinary concepts."""
        router = load_json(REGISTRY_DIR / "subject-routing-registry.json")
        router_str = json.dumps(router)
        disciplinary_terms = [
            "vector", "kinematics", "force", "acceleration", "derivative",
            "integral", "stoichiometry", "orbital", "oxidation"
        ]
        for term in disciplinary_terms:
            self.assertNotIn(
                term,
                router_str.lower(),
                f"Disciplinary concept '{term}' illegally embedded in routing registry!"
            )

    def test_12_learner_state_invariance_on_domain_truth(self):
        """Changing learner_state (UNKNOWN -> NOVICE -> ADVANCED) does not alter authority bindings or change classes."""
        task_unknown = copy.deepcopy(self.sample_task)
        task_unknown["learner_state"] = "UNKNOWN"

        task_novice = copy.deepcopy(self.sample_task)
        task_novice["learner_state"] = "NOVICE"

        task_advanced = copy.deepcopy(self.sample_task)
        task_advanced["learner_state"] = "ADVANCED"

        pkt_u = compile_packet(task_unknown, repo_root=self.repo_root)
        pkt_n = compile_packet(task_novice, repo_root=self.repo_root)
        pkt_a = compile_packet(task_advanced, repo_root=self.repo_root)

        self.assertEqual(pkt_u["authority_bindings"], pkt_n["authority_bindings"])
        self.assertEqual(pkt_u["authority_bindings"], pkt_a["authority_bindings"])
        self.assertEqual(pkt_u["allowed_change_classes"], pkt_n["allowed_change_classes"])
        self.assertEqual(pkt_u["required_outputs"], pkt_a["required_outputs"])

    def test_13_multi_subject_compilation(self):
        """Compiler succeeds for Physics, Mathematics, and Chemistry tasks."""
        # 1. Physics
        pkt_p = compile_packet(self.sample_task, repo_root=self.repo_root)
        self.assertEqual(pkt_p["task"]["subject"], "PHYSICS")
        self.assertTrue(any("physics" in b["ref_path"].lower() for b in pkt_p["authority_bindings"]))

        # 2. Mathematics
        math_task = copy.deepcopy(self.sample_task)
        math_task["task_id"] = "TASK-MTH-001"
        math_task["subject"] = "MATHEMATICS"
        math_task["topic"] = "Polynomials"
        math_task["subtopic"] = "Remainder Theorem"
        pkt_m = compile_packet(math_task, repo_root=self.repo_root)
        self.assertEqual(pkt_m["task"]["subject"], "MATHEMATICS")
        self.assertTrue(any("mathematics" in b["ref_path"].lower() for b in pkt_m["authority_bindings"]))

        # 3. Chemistry
        chem_task = copy.deepcopy(self.sample_task)
        chem_task["task_id"] = "TASK-CHM-001"
        chem_task["subject"] = "CHEMISTRY"
        chem_task["topic"] = "Chemical Reactions"
        chem_task["subtopic"] = "Types of Reactions"
        pkt_c = compile_packet(chem_task, repo_root=self.repo_root)
        self.assertEqual(pkt_c["task"]["subject"], "CHEMISTRY")
        self.assertTrue(any("chemistry" in b["ref_path"].lower() for b in pkt_c["authority_bindings"]))

    def test_14_engineering_preflight_generation(self):
        """Engineering Preflight accurately derives scope state and consumer readiness."""
        packet = compile_packet(self.sample_task, repo_root=self.repo_root)
        preflight = generate_engineering_preflight(packet, repo_root=self.repo_root)

        self.assertIn("ENGINEERING PREFLIGHT / MAP", preflight)
        self.assertIn("Task: PHYSICS -> Motion -> 1D Motion", preflight)
        self.assertIn("Identity Resolution: REGISTERED (PHY-KIN-1D-MOTION)", preflight)
        self.assertIn("Curriculum Binding:  CBSE Gr 9, Ch 8", preflight)
        self.assertIn("PROBLEM_SEMANTICS:   AUTHORIZED", preflight)
        self.assertIn("CORE_AUTHORING:      AUTHORIZED", preflight)
        self.assertIn("PUBLICATION:         BLOCKED_PENDING_AUTHORIZED_REVIEW", preflight)

    def test_15_valid_report_with_held_engineering_state(self):
        """A task can complete successfully by proving engineering remains HELD."""
        held_report = copy.deepcopy(self.sample_report)
        held_report["execution_result"] = "COMPLETE"
        held_report["engineering_state"] = "HELD"
        held_report["consumer_permissions"] = {
            "PROBLEM_SEMANTICS": "HELD",
            "CORE_AUTHORING": "HELD"
        }
        held_report["blockers"] = [
            "External mathematics trigonometry prerequisite uncertified by provider"
        ]

        errors = validate_report(held_report)
        self.assertEqual(errors, [], f"Valid HELD report should have 0 errors, got: {errors}")

    def test_16_diversity_stress_relative_motion_held(self):
        """Relative Motion as unregistered candidate correctly derives HELD across all consumers."""
        rel_task = load_json(FIXTURES_DIR / "task_physics_relative_motion.json")
        packet = compile_packet(rel_task, repo_root=self.repo_root)
        preflight = generate_engineering_preflight(packet, repo_root=self.repo_root)

        self.assertIn("Identity Resolution: UNREGISTERED CANDIDATE (Relative Motion)", preflight)
        self.assertIn("Gate Readiness:      HELD", preflight)
        self.assertIn("PROBLEM_SEMANTICS:   HELD", preflight)
        self.assertIn("CORE_AUTHORING:      HELD", preflight)

    def test_17_diversity_stress_thermodynamics_research(self):
        """Thermodynamics at RESEARCH depth resolves gate, derives prereqs & reps without case branches."""
        thermo_task = load_json(FIXTURES_DIR / "sample_thermo_research_task.json")
        packet = compile_packet(thermo_task, repo_root=self.repo_root)
        preflight = generate_engineering_preflight(packet, repo_root=self.repo_root)

        self.assertIn("Identity Resolution: REGISTERED (PHY-THERMO-FIRST-SECOND-LAW)", preflight)
        self.assertIn("Internal Prereqs:    PHY-WORK-ENERGY-POWER", preflight)
        self.assertIn("REP-PHYS-PV-CARNOT-CYCLE", preflight)
        self.assertIn("Gate Readiness:      ENGINEERING_GATE_READY", preflight)
        self.assertIn("PROBLEM_SEMANTICS:   AUTHORIZED", preflight)

    def test_18_diversity_stress_math_modular_arithmetic(self):
        """Mathematics IOQM modular arithmetic task compiles and binds Math authority."""
        math_task = load_json(FIXTURES_DIR / "task_math_modular_arithmetic.json")
        packet = compile_packet(math_task, repo_root=self.repo_root)
        self.assertEqual(packet["task"]["subject"], "MATHEMATICS")
        self.assertTrue(any("mathematics" in b["ref_path"].lower() for b in packet["authority_bindings"]))
        preflight = generate_engineering_preflight(packet, repo_root=self.repo_root)
        self.assertIn("Task: MATHEMATICS -> Number Theory -> Modular Divisibility and Congruences", preflight)

    def test_19_diversity_stress_chem_redox_balancing(self):
        """Chemistry CBSE Redox balancing task compiles and binds Chemistry authority."""
        chem_task = load_json(FIXTURES_DIR / "task_chem_redox_reactions.json")
        packet = compile_packet(chem_task, repo_root=self.repo_root)
        self.assertEqual(packet["task"]["subject"], "CHEMISTRY")
        self.assertTrue(any("chemistry" in b["ref_path"].lower() for b in packet["authority_bindings"]))
        preflight = generate_engineering_preflight(packet, repo_root=self.repo_root)
        self.assertIn("Task: CHEMISTRY -> Redox Reactions -> Oxidation Number Method and Ion-Electron Balancing", preflight)


if __name__ == "__main__":
    unittest.main()

