#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
LE = HERE.parents[1]
REPO = HERE.parents[5]
AGENT_TASKS = REPO / "Grade 9" / "V2" / "Shared" / "AgentTasks"
sys.path.insert(0, str(AGENT_TASKS / "engine"))

from compile_execution_packet import compile_packet  # noqa: E402

PILOT_PATH = LE / "pilots" / "physics-thermodynamics.research.prototype.json"
TASK_PATH = AGENT_TASKS / "fixtures" / "valid" / "physics-thermodynamics-research.task.json"
CROSSDOMAIN_PATH = REPO / "Grade 9" / "V2" / "Shared" / "CrossDomain" / "registry" / "domain-provider-registry.v1.json"

SCHEMAS = {
    "identity": LE / "contracts" / "skp-identity.schema.json",
    "scope": LE / "contracts" / "skp-scope.schema.json",
    "curriculum": LE / "contracts" / "skp-curriculum-binding.schema.json",
    "capability": LE / "contracts" / "skp-capability.schema.json",
    "prerequisite": LE / "contracts" / "skp-prerequisite-edge.schema.json",
    "source_plan": LE / "contracts" / "skp-source-plan.schema.json",
    "source_record": LE / "contracts" / "skp-source-record.schema.json",
    "concept": LE / "prototypes" / "contracts" / "skp-concept.prototype.schema.json",
    "relation": LE / "prototypes" / "contracts" / "skp-relation.prototype.schema.json",
    "reasoning": LE / "prototypes" / "contracts" / "skp-reasoning-sequence.prototype.schema.json",
    "representation": LE / "prototypes" / "contracts" / "skp-representation.prototype.schema.json",
    "verification": LE / "prototypes" / "contracts" / "skp-verification-route.prototype.schema.json",
    "family": LE / "prototypes" / "contracts" / "skp-problem-family.prototype.schema.json",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


VALIDATORS = {name: Draft202012Validator(load(path)) for name, path in SCHEMAS.items()}


def validate(kind: str, value: dict) -> None:
    VALIDATORS[kind].validate(value)


def source_refs_from(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"source_refs", "evidence_refs"} and isinstance(item, list):
                for ref in item:
                    if isinstance(ref, str) and ref.startswith("SRC-"):
                        yield ref
            yield from source_refs_from(item)
    elif isinstance(value, list):
        for item in value:
            yield from source_refs_from(item)


class ThermodynamicsResearchPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = load(PILOT_PATH)
        cls.task = load(TASK_PATH)

    def test_declared_module_shapes_are_valid_but_non_runtime(self):
        p = self.pilot
        self.assertTrue(p["prototype_only"])
        self.assertFalse(p["runtime_authority"])
        self.assertEqual(p["promotion_state"], "HELD")
        self.assertEqual(p["engineering_depth"], "RESEARCH")
        self.assertFalse(p["learner_state_authority"])
        self.assertIn("SKP_TO_ENGINEERING_PROMOTION_PATH_INACTIVE", p["hold_reasons"])
        self.assertIn("RESEARCH_OVERLAY_SCHEMA_PLANNED", p["hold_reasons"])

        validate("identity", p["identity"])
        validate("scope", p["scope"])
        for row in p["curriculum_bindings"]:
            validate("curriculum", row)
        for row in p["capabilities"]:
            validate("capability", row)
        for row in p["prerequisite_edges"]:
            validate("prerequisite", row)
        validate("source_plan", p["source_plan"])
        for row in p["source_ledger"]:
            validate("source_record", row)
        for row in p["concepts"]:
            validate("concept", row)
        for row in p["relations"]:
            validate("relation", row)
        for row in p["representations"]:
            validate("representation", row)
        for row in p["reasoning_sequences"]:
            validate("reasoning", row)
        for row in p["verification_routes"]:
            validate("verification", row)
        for row in p["problem_families"]:
            validate("family", row)

    def test_all_evidence_refs_resolve_and_source_reasons_are_auditable(self):
        p = self.pilot
        source_ids = {row["source_id"] for row in p["source_ledger"]}
        self.assertEqual(len(source_ids), len(p["source_ledger"]))
        unresolved = sorted(set(source_refs_from(p)) - source_ids)
        self.assertEqual(unresolved, [])
        for source in p["source_ledger"]:
            for assessment in source["intent_assessments"]:
                self.assertGreaterEqual(len(assessment["selection_reason"]), 10)

    def test_current_cbse_is_curriculum_authority_and_external_exam_is_not(self):
        p = self.pilot
        binding = p["curriculum_bindings"][0]
        self.assertEqual(binding["grade"], "11")
        self.assertEqual(binding["curriculum_version"], "2026-27")
        self.assertEqual(binding["classification"], "CURRICULUM_REQUIRED")
        self.assertEqual(binding["explicitness"], "EXPLICIT")
        self.assertEqual(binding["binding_state"], "CONFIRMED")
        self.assertEqual(binding["evidence_refs"], ["SRC-CBSE-PHYSICS-2026-27"])

        curriculum_promotions = []
        for source in p["source_ledger"]:
            for assessment in source["intent_assessments"]:
                if assessment["source_intent"] == "CURRICULUM_AUTHORITY" and assessment["authority_disposition"] == "PROMOTED_FOR_INTENT":
                    curriculum_promotions.append(source["source_id"])
        self.assertEqual(curriculum_promotions, ["SRC-CBSE-PHYSICS-2026-27"])

        nta = next(row for row in p["source_ledger"] if row["source_id"] == "SRC-NTA-JEE-MAIN-2026")
        self.assertEqual({a["source_intent"] for a in nta["intent_assessments"]}, {"EXTERNAL_ASSESSMENT"})
        assessment_discovery = next(row for row in p["discovery_reconciliation"] if row["record_id"] == "DISCOVERY-PHY-THERMO-JEE-MAIN-2026")
        self.assertEqual(assessment_discovery["promotion_effect"], "DOES_NOT_MUTATE_CURRICULUM")

    def test_research_claims_are_additive_and_cannot_silently_mutate_standard_truth(self):
        p = self.pilot
        base_ids = {row["claim_id"] for row in p["base_claim_snapshot"]}
        research_ids = {row["claim_id"] for row in p["research_extension_claims"]}
        self.assertTrue(base_ids)
        self.assertTrue(research_ids)
        self.assertTrue(base_ids.isdisjoint(research_ids))
        self.assertTrue(all(row["depth"] == "STANDARD" for row in p["base_claim_snapshot"]))
        self.assertTrue(all(row["depth"] == "RESEARCH" for row in p["research_extension_claims"]))
        self.assertTrue(all(row["mutates_base_claims"] is False for row in p["research_extension_claims"]))
        self.assertTrue(all(row["source_refs"] for row in p["base_claim_snapshot"] + p["research_extension_claims"]))

        exclusions = " ".join(row["statement"] for row in p["scope"]["excludes"]).lower()
        self.assertIn("entropy", exclusions)
        self.assertIn("carnot", exclusions)

    def test_population_limited_research_does_not_create_grade11_misconception_authority(self):
        p = self.pilot
        candidates = p["learner_conception_candidates"]
        self.assertTrue(candidates)
        self.assertTrue(all(row["canonical_grade11_authorized"] is False for row in candidates))
        self.assertTrue(all(row["population_transfer_state"] == "TRANSFER_LIMITED" for row in candidates))

        research_sources = []
        for source in p["source_ledger"]:
            for assessment in source["intent_assessments"]:
                if assessment["source_intent"] == "MISCONCEPTION_EVIDENCE":
                    research_sources.append(assessment)
        self.assertTrue(research_sources)
        self.assertTrue(all(row.get("population_context") for row in research_sources))
        self.assertTrue(any("not cbse grade xi" in " ".join(row["limitations"]).lower() for row in research_sources))

    def test_external_math_prerequisite_is_provider_owned_but_not_self_certified(self):
        p = self.pilot
        edge = next(row for row in p["prerequisite_edges"] if row["edge_type"] == "EXTERNAL_DOMAIN_PREREQUISITE")
        self.assertEqual(edge["provider_owner"]["subject"], "MATHEMATICS")
        self.assertEqual(edge["missing_behavior"], "UNRESOLVED")
        self.assertNotIn("provider_receipt", edge)
        self.assertIn("CROSS_DOMAIN_IDENTIFIER_ROUTING_UNRESOLVED", p["hold_reasons"])

        registry = load(CROSSDOMAIN_PATH)
        math_provider = next(row for row in registry["providers"] if row["provider_subject"] == "MATHEMATICS")
        self.assertTrue(math_provider["provider_root"].startswith("Grade 9/"))
        self.assertTrue(edge["prerequisite_ref"].startswith("CAP-MATH-"))
        self.assertFalse(edge["prerequisite_ref"].startswith(math_provider["prerequisite_prefix"]))

    def test_agent_task_exposes_grade_mismatch_without_granting_readiness(self):
        packet = compile_packet(self.task)
        scope = packet["learning_engineering_state"]["subject_adapter"]["generation_authority_scope"]
        self.assertEqual(scope["task_grade"], 11)
        self.assertEqual(scope["declared_grades"], [9])
        self.assertEqual(scope["grade_state"], "MISMATCH")
        self.assertEqual(packet["engineering_preflight"]["engineering_state"], "NOT_EVALUATED")
        self.assertEqual(packet["engineering_preflight"]["research_state"], "NOT_EVALUATED")
        self.assertEqual(packet["engineering_preflight"]["publication_authorization"], "NOT_IMPLIED")
        self.assertTrue(any("task grade" in blocker.lower() for blocker in packet["engineering_preflight"]["blockers"]))

    def test_learner_state_and_depth_do_not_change_bound_authority(self):
        research_task = copy.deepcopy(self.task)
        other_learner = copy.deepcopy(self.task)
        other_learner["task_id"] = "TASK-PHY-THERMO-LEARNER-METAMORPHIC"
        other_learner["learner_state"] = "SYNTHETIC_DIFFERENT_LEARNER_STATE"
        standard_depth = copy.deepcopy(self.task)
        standard_depth["task_id"] = "TASK-PHY-THERMO-DEPTH-METAMORPHIC"
        standard_depth["engineering_depth"] = "STANDARD"

        packet_research = compile_packet(research_task)
        packet_learner = compile_packet(other_learner)
        packet_standard = compile_packet(standard_depth)

        self.assertNotEqual(packet_research["packet_digest"], packet_learner["packet_digest"])
        self.assertNotEqual(packet_research["packet_digest"], packet_standard["packet_digest"])
        self.assertEqual(packet_research["authority_bindings"], packet_learner["authority_bindings"])
        self.assertEqual(packet_research["authority_bindings"], packet_standard["authority_bindings"])
        self.assertEqual(
            packet_research["learning_engineering_state"]["subject_adapter"]["generation_authority_scope"],
            packet_learner["learning_engineering_state"]["subject_adapter"]["generation_authority_scope"],
        )
        self.assertEqual(
            packet_research["learning_engineering_state"]["subject_adapter"]["generation_authority_scope"],
            packet_standard["learning_engineering_state"]["subject_adapter"]["generation_authority_scope"],
        )
        frozen_base = json.dumps(self.pilot["base_claim_snapshot"], sort_keys=True)
        self.assertEqual(frozen_base, json.dumps(self.pilot["base_claim_snapshot"], sort_keys=True))

    def test_pilot_does_not_claim_runtime_engineering_or_release_authority(self):
        p = self.pilot
        forbidden_keys = {"engineering_ready", "technical_readiness", "publication_authorized", "consumer_permissions", "provider_receipt"}
        self.assertTrue(forbidden_keys.isdisjoint(p.keys()))
        self.assertFalse(p["runtime_authority"])
        self.assertEqual(p["promotion_state"], "HELD")
        finding_states = {row["finding_id"]: row["state"] for row in p["architecture_findings"]}
        self.assertEqual(finding_states["ARCH-PHY-THERMO-GRADE-SCOPE"], "CONFIRMED_GAP")
        self.assertEqual(finding_states["ARCH-PHY-THERMO-RESEARCH-OVERLAY"], "EXPECTED_HOLD")


if __name__ == "__main__":
    unittest.main(verbosity=2)
