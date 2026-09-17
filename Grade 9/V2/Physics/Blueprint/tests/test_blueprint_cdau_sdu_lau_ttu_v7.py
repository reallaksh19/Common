#!/usr/bin/env python3
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text())


CDAU = load("policy/core-governance-cdau.v1.json")
SDU = load("policy/study-differentiation-unit.v1.json")
LAU = load("policy/learner-adaptation-unit.v1.json")
TTU = load("policy/technical-teaching-unit.v3.json")

CDAU_FIX = load("fixtures/architecture-v7/m2d-sba23-cdau.json")
SDU_FIX = load("fixtures/architecture-v7/m2d-sba23-sdu.json")
LAU_FIX = load("fixtures/architecture-v7/m2d-sba23-lau-owner-guided.json")
CONCEPT_FIX = load("fixtures/architecture-v7/m2d-sba23-concept-ttu.json")
PROBLEM_FIX = load("fixtures/architecture-v7/m2d-sba23-problem-ttu.json")

# New architecture contracts must validate real process-golden objects, not merely parse.
schema_fixture_pairs = [
    ("contracts/core-differentiation-adaptation-unit.schema.json", CDAU_FIX),
    ("contracts/study-differentiation-unit.schema.json", SDU_FIX),
    ("contracts/learner-adaptation-unit.schema.json", LAU_FIX),
    ("contracts/technical-teaching-unit-v3.schema.json", CONCEPT_FIX),
    ("contracts/technical-teaching-unit-v3.schema.json", PROBLEM_FIX),
]
for schema_name, fixture in schema_fixture_pairs:
    schema = load(schema_name)
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["type"] == "object"
    Draft202012Validator(schema).validate(fixture)

# Upstream authority remains outside CDAU; product governance cannot rewrite truth.
assert CDAU["authority_order"][:5] == [
    "GROUND_TRUTH", "CORE0", "CORE1_CORE2_INDEPENDENT_VALIDATION", "JOIN", "CANONICAL_DOMAIN_REGISTRY"
]
owner = CDAU["owner_control"]
assert owner["may_override_product_routing"] is True
assert owner["may_choose_design_pilot_when_source_unresolved"] is True
for key in (
    "may_override_physics_or_math_correctness",
    "may_override_frozen_source_wording",
    "may_override_source_integrity_classification",
    "may_override_provenance",
    "may_override_observed_evidence",
    "may_expand_core2a_legal_pool",
    "may_bypass_authority_order",
):
    assert owner[key] is False
assert owner["global_decision_provenance_required"] == ["SYSTEM_FINDING", "OWNER_DECISION", "FINAL_ACTION"]

# Cross-Core differentiation treats semantic reuse differently from pedagogical duplication.
rels = CDAU["cross_core_relationships"]
assert "SEMANTIC_REUSE" in rels["release_allowed"]
assert "FADING_ANCHOR" in rels["release_allowed"]
assert "STRUCTURAL_SIBLING" in rels["release_allowed"]
assert "FAR_TRANSFER_SIBLING" in rels["release_allowed"]
assert rels["release_blocked"] == ["PEDAGOGICAL_DUPLICATION"]
assert set(CDAU["example_fingerprint_required_fields"]) == {
    "problem_family", "context", "givens", "numeric_values", "target_unknown",
    "representation", "model_sequence", "special_condition", "solution_path"
}

# SDU alone controls Core1A/Core1B; learner knowledge may not drive authored depth.
assert set(SDU["scope"]) == {"CORE1A", "CORE1B"}
assert SDU["student_knowledge_pct_may_drive_authored_depth"] is False
assert SDU["research_policy"] == {
    "EASY": "NONE_BY_DEFAULT",
    "MEDIUM": "TARGETED",
    "HARD": "DEEP",
    "research_must_produce_design_decisions": True,
}
env = SDU["shared_depth_envelope"]
assert env["EASY"] == 10 and env["MEDIUM"] == 20 and env["HARD"] == 30
assert env["applies_to_core1a"] is True and env["applies_to_core1b"] is True
assert env["page_count_is_quota"] is False
assert env["same_ceiling_implies_same_actual_length"] is False
assert env["same_ceiling_implies_same_content"] is False
assert env["actual_lengths_independently_derived"] is True
assert SDU_FIX["difficulty"]["student_knowledge_pct_used"] is False
assert SDU_FIX["core1a_realization"]["soft_page_ceiling"] == 30
assert SDU_FIX["core1b_realization"]["soft_page_ceiling"] == 30
assert SDU_FIX["core1a_realization"]["actual_length_independently_derived"] is True
assert SDU_FIX["core1b_realization"]["actual_length_independently_derived"] is True

# LAU alone controls Core2 adaptation; no silent default and no authority leakage.
assert set(LAU["scope"]) == {"CORE2A", "CORE2B"}
assert set(LAU["required_selection_basis"]) == {"KNOWLEDGE_PERCENT", "OWNER_OVERRIDE"}
assert LAU["no_silent_default"] is True
assert LAU["owner_override"]["may_rewrite_frozen_source"] is False
assert LAU["owner_override"]["may_expand_legal_pool"] is False
assert LAU["owner_override"]["may_manufacture_mastery"] is False
assert LAU["core2b"]["lineage_modes"]["FADING_ANCHOR"]["may_count_as_transfer_evidence"] is False
assert LAU["core2b"]["lineage_modes"]["STRUCTURAL_SIBLING"]["may_count_as_transfer_evidence"] is True
assert LAU["core2b"]["lineage_modes"]["FAR_TRANSFER_SIBLING"]["may_count_as_transfer_evidence"] is True
assert LAU_FIX["selection_basis"]["type"] == "OWNER_OVERRIDE"
assert LAU_FIX["support_decision"]["prediction_is_psychometric_claim"] is False
for guard, value in LAU_FIX["authority_guards"].items():
    if guard == "no_silent_default":
        assert value is True
    else:
        assert value is False

# TTU is now a family: concept vs problem, with broader learner transformations than omissions.
assert set(TTU["ttu_families"]) == {"CONCEPT_TTU", "PROBLEM_TTU"}
expected_modes = {
    "PREDICTION", "COMPLETION", "GENERATION", "SELECTION", "DISCRIMINATION",
    "DIAGNOSIS", "DERIVATION_CONNECTION", "VERIFICATION", "TRANSFER"
}
assert set(TTU["learner_transformation_modes"]) == expected_modes
tr = TTU["transformation_rules"]
assert tr["must_change_reasoning_state"] is True
assert tr["must_produce_observable_learner_product"] is True
assert tr["blank_or_omission_required_for_all_modes"] is False
assert tr["cosmetic_blank_allowed"] is False
assert tr["arbitrary_number_blank_without_reasoning_role_allowed"] is False
assert TTU["tutor_dialogue"]["all_functions_required_for_every_task"] is False
assert TTU["tutor_dialogue"]["prompt_sequence_must_be_target_driven"] is True
assert TTU["canonical_reveal"]["full_solution_exposure_is_mastery_evidence"] is False
assert TTU["canonical_reveal"]["full_solution_exposure_is_transfer_evidence"] is False
assert TTU["verification"]["answer_key_only_counts_as_independent_verification"] is False

# Concept TTU golden proves a B-layer can be generation/selection/derivation without arbitrary blanks.
assert CONCEPT_FIX["ttu_family"] == "CONCEPT_TTU"
assert "GENERATION" in CONCEPT_FIX["learner_transformation"]["modes"]
assert "SELECTION" in CONCEPT_FIX["learner_transformation"]["modes"]
assert "DERIVATION_CONNECTION" in CONCEPT_FIX["learner_transformation"]["modes"]
assert CONCEPT_FIX["learner_transformation"]["semantic_omissions"] == []
assert CONCEPT_FIX["learner_transformation"]["changes_reasoning_state"] is True
assert len(CONCEPT_FIX["verification_contract"]["independent_rules"]) >= 1

# Problem TTU golden proves changed-sign transfer with independent verification and bounded repair.
assert PROBLEM_FIX["ttu_family"] == "PROBLEM_TTU"
assert "TRANSFER" in PROBLEM_FIX["learner_transformation"]["modes"]
assert "SELECTION" in PROBLEM_FIX["learner_transformation"]["modes"]
assert PROBLEM_FIX["learner_transformation"]["anti_triviality"]["answer_copy_task_allowed"] is False
assert len(PROBLEM_FIX["verification_contract"]["independent_rules"]) >= 1
assert PROBLEM_FIX["repair_contract"]["smallest_repair_route"]

# SBA23 source hold remains visible through owner decision provenance; architecture cannot legalize it.
assert "Q15 exact prompt" in CDAU_FIX["owner_control"]["system_finding"]
assert CDAU_FIX["owner_control"]["bounded_authority"]["may_change_source_truth"] is False
assert CDAU_FIX["owner_control"]["bounded_authority"]["may_expand_legal_pool"] is False

print("Physics CDAU/SDU/LAU + TTU v3 architecture: PASS")
