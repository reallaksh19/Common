#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = json.loads((ROOT / "policy" / "self-help-core-publication.v6.json").read_text())
BUCKET = json.loads((ROOT / "policy" / "core1ab-bucket-authoring.v2.json").read_text())
KNOW = json.loads((ROOT / "policy" / "core2ab-knowledge-routing.v1.json").read_text())
TTU = json.loads((ROOT / "policy" / "technical-teaching-unit.v2.json").read_text())
REP = json.loads((ROOT / "policy" / "physics-representation-semantic-quality.v1.json").read_text())
LAYOUT = json.loads((ROOT / "policy" / "pdf-layout-integrity.v2.json").read_text())
PILOT = json.loads((ROOT / "topics" / "self-help-three-topic-falsification-pilot.v3.json").read_text())

# Core1 stays bucket-wise and knowledge-independent; Core2 stays knowledge/owner-routed.
cp = PUB["control_planes"]
assert cp["CORE1_FAMILY"]["student_knowledge_pct_drives_authored_depth"] is False
assert cp["CORE1_FAMILY"]["always_subtopic_bucket_wise"] is True
assert cp["CORE1_FAMILY"]["shared_learning_model_required"] is True
assert cp["CORE2_FAMILY"]["student_knowledge_pct_required_unless_owner_override"] is True

# TTU v2 is stateful reconstruction architecture, not representation counting.
center = PUB["authoring_center"]
assert "RECONSTRUCTION_COMPLETE_TECHNICAL_TEACHING_UNIT" in center["primary_units_in_order"]
assert "cosmetic blanks" in center["anti_pattern"]
gate=PUB["technical_teaching_unit_gate"]
for key in (
    "canonical_completed_state_required",
    "reconstruction_contract_required",
    "semantic_omission_required",
    "learner_reconstruction_task_required",
    "fixed_help_required",
    "canonical_reveal_after_attempt_required",
    "independent_verification_required",
    "representation_must_bind_to_reasoning",
):
    assert gate[key] is True
assert gate["diagram_plus_equation_presence_alone_proves_ttu_complete"] is False
assert gate["generic_cards_count_as_physics_representation"] is False
assert gate["cosmetic_blank_counts_as_reconstruction"] is False
assert gate["compare_with_answer_counts_as_independent_verification"] is False

assert TTU["ttu_identity"]["canonical_state_required"] is True
assert TTU["ttu_identity"]["reconstruction_contract_required"] is True
assert TTU["ttu_identity"]["independent_verification_required"] is True
assert TTU["reconstruction_contract"]["omissions_must_reference_canonical_element_ids"] is True
assert TTU["reconstruction_contract"]["omissions_must_be_semantically_material"] is True
assert "COSMETIC_BLANK" in TTU["reconstruction_contract"]["prohibited_omissions"]
assert "ARBITRARY_NUMBER_BLANK_WITHOUT_REASONING_ROLE" in TTU["reconstruction_contract"]["prohibited_omissions"]
assert TTU["fixed_help"]["help_must_be_preauthored"] is True
assert TTU["fixed_help"]["help_must_bind_to_omitted_element_ids"] is True
assert TTU["fixed_help"]["dynamic_new_semantics_before_reveal_allowed"] is False
assert TTU["verification"]["must_be_independent_of_answer_key"] is True
assert TTU["verification"]["must_be_applicable_to_learner_state_before_reveal"] is True
assert TTU["verification"]["compare_with_answer_is_independent_verification"] is False
assert TTU["hard_bucket_rule"]["substantive_b_layer_ttu_minimum_semantic_omissions"] >= 2
assert TTU["hard_bucket_rule"]["prose_only_reconstruction_allowed"] is False

# Shared Core1 model remains asymmetric in page realization.
shared = BUCKET["shared_bucket_learning_model"]
assert set(shared["required_fields"]) == {
    "HIDDEN_INVARIANTS", "PREREQUISITE_BRIDGES", "INFERENTIAL_JUMPS",
    "REPRESENTATIONS", "MISCONCEPTIONS", "PROBLEM_FAMILIES",
    "SOURCE_CORE2_LINKAGE", "FRAGILE_CHECKPOINTS"
}
pb = BUCKET["page_budget_rule"]
assert pb["applies_primarily_to"] == "CORE1A"
assert pb["core1b_inherits_core1a_page_budget"] is False
assert BUCKET["badges"]["EASY"]["core1a_soft_page_ceiling"] == 10
assert BUCKET["badges"]["MEDIUM"]["core1a_soft_page_ceiling"] == 20
assert BUCKET["badges"]["HARD"]["core1a_soft_page_ceiling"] == 30

# A renders canonical state; B reconstructs from semantically missing elements.
roles = PUB["learner_surface_roles"]
assert roles["CORE1A"]["major_jump_or_family_requires_complete_ttu"] is True
assert roles["CORE1A"]["ttu_must_already_define_downstream_reconstruction_contract"] is True
assert roles["CORE1B"]["fragile_technical_checkpoint_requires_reconstructable_ttu"] is True
assert roles["CORE1B"]["semantic_omissions_must_target_reasoning"] is True
assert roles["CORE1B"]["fixed_help_bound_to_omissions"] is True
assert roles["CORE1B"]["independent_verification_before_reveal"] is True
assert TTU["layer_realization"]["CORE1A"]["underlying_ttu_still_contains_reconstruction_contract"] is True
assert TTU["layer_realization"]["CORE1B"]["must_use_semantic_omissions"] is True
assert TTU["layer_realization"]["CORE1B"]["full_solution_exposure_is_mastery_evidence"] is False

# A visual counts only when it carries actual Physics structure and binds to reasoning.
assert PUB["representation_quality"]["eligible_representation_must_encode_physics_structure"] is True
assert PUB["representation_quality"]["figure_reasoning_binding_required"] is True
assert PUB["representation_quality"]["oversized_empty_plot_counts_as_representation"] is False
assert PUB["representation_quality"]["prose_cards_count_as_technical_diagram"] is False
assert "GENERIC_TEXT_CARD" in REP["non_counting_visuals"]
assert "OVERSIZED_EMPTY_COORDINATE_PLANE" in REP["non_counting_visuals"]
assert REP["binding_rule"]["figure_without_reasoning_binding_counts_as_technical_closure"] is False
assert REP["semantic_completeness"]["variables_used_in_working_must_be_identifiable"] is True
assert REP["semantic_completeness"]["frame_axis_direction_conventions_explicit_when_material"] is True

# Model discrimination must use Physics structure, not generic boxes.
md = REP["model_discrimination"]
assert md["generic_A_B_C_cards_count_as_physics_representation"] is False
assert set(md["minimum_comparison_fields"]) == {
    "PHYSICAL_TRIGGER", "RELEVANT_REPRESENTATION_OR_MODEL", "FIRST_MOVE", "WHY_COMPETING_MODEL_IS_REJECTED"
}
assert PUB["representation_quality"]["model_discrimination_requires_physical_trigger_model_first_move_and_rejection_reason"] is True

# Core2A/2B remain knowledge-routed and authority-safe, but TTU state semantics apply.
rir = KNOW["required_input_rule"]
assert rir["no_silent_default"] is True
assert set(rir["selection_basis_enum"]) == {"KNOWLEDGE_PERCENT", "OWNER_OVERRIDE"}
assert rir["KNOWLEDGE_PERCENT"]["range_inclusive"] == [0, 100]
assert set(rir["OWNER_OVERRIDE"]["required_fields"]) == {"owner_ref", "reason", "support_band"}
guards = KNOW["authority_guards"]
assert guards["knowledge_pct_may_expand_core2a_legal_pool"] is False
assert guards["owner_override_may_expand_core2a_legal_pool"] is False
assert guards["owner_override_waives_only_missing_knowledge_pct"] is True
assert roles["CORE2A"]["representative_worked_item_requires_complete_ttu"] is True
assert roles["CORE2B"]["learner_selects_or_constructs_representation_and_model_when_part_of_transfer_demand"] is True
assert roles["CORE2B"]["semantic_omission_or_model_selection_required_when_material"] is True
assert roles["CORE2B"]["independent_verification_before_reveal"] is True
assert TTU["layer_realization"]["CORE2B"]["full_solution_exposure_is_transfer_mastery"] is False

# Hints remain bounded and local; arbitrary prompt volume is not quality.
assert PUB["task_grammar_policy"]["MICRO_PROMPT"]["full_hint_ladder_required"] is False
assert PUB["task_grammar_policy"]["REPRESENTATION_TASK"]["reconstructable_ttu_required_when_technical"] is True
assert PUB["task_grammar_policy"]["REPRESENTATION_TASK"]["semantic_omission_required"] is True
assert PUB["task_grammar_policy"]["SUBSTANTIVE_TASK"]["progressive_rescue_required_when_learner_can_be_stranded"] is True
assert PUB["task_grammar_policy"]["SUBSTANTIVE_TASK"]["full_technical_check_required"] is True
assert PUB["task_grammar_policy"]["SUBSTANTIVE_TASK"]["fixed_help_bound_to_omissions"] is True
assert PUB["task_grammar_policy"]["MIXED_RETRIEVAL"]["answer_key_may_not_be_the_only_verification"] is True

# Layout release preserves visible reconstruction and answer separation.
assert PUB["layout_release"]["successful_pdf_generation_is_visual_preflight_pass"] is False
assert PUB["layout_release"]["render_every_page"] is True
assert PUB["layout_release"]["learner_state_and_canonical_state_visually_distinct"] is True
assert PUB["layout_release"]["omitted_elements_must_have_visible_targets"] is True
assert PUB["layout_release"]["help_must_be_visually_separate_from_canonical_reveal"] is True
assert PUB["layout_release"]["fail_on_label_vector_overlap"] is True
assert PUB["layout_release"]["fail_on_microscopic_figure_labels"] is True
assert PUB["layout_release"]["fail_on_oversized_low_information_figure"] is True
assert PUB["layout_release"]["fail_on_orphaned_figure_from_working"] is True
assert PUB["layout_release"]["thumbnail_review_required_for_new_figure_grammar"] is True
assert LAYOUT["preflight"]["render_every_page"] is True
assert LAYOUT["preflight"]["fail_closed"] is True
assert LAYOUT["legibility"]["figure_label_min_pt_at_final_size"] >= 8.0
assert LAYOUT["legibility"]["main_equation_min_pt_at_final_size"] >= 9.5
assert LAYOUT["composition"]["oversized_figure_displacing_required_working_allowed"] is False
assert LAYOUT["composition"]["large_empty_plot_region_allowed_without_pedagogical_reason"] is False

# Three-topic pilot retains source holds and adaptation-input rules.
topics = PILOT["topics"]
assert len(topics) == 3
for t in topics:
    assert t["core1_bucket_difficulty_badge"] in {"EASY", "MEDIUM", "HARD"}
    inp = t["core2_adaptation_input"]
    assert inp["selection_basis"] in {"KNOWLEDGE_PERCENT", "OWNER_OVERRIDE"}
    if inp["selection_basis"] == "KNOWLEDGE_PERCENT":
        assert 0 <= inp["student_knowledge_pct"] <= 100
    else:
        assert inp["student_knowledge_pct"] is None
        ov = inp["owner_override"]
        assert ov["owner_ref"] and ov["reason"]
        assert ov["support_band"] in rir["OWNER_OVERRIDE"]["support_band_enum"]

moving = next(x for x in topics if x["topic_id"] == "MOVING_LAUNCHER_RELATIVE_VELOCITY")
assert "EXACT_Q15_HELD" in moving["source_status"]
assert moving["core2_adaptation_input"]["selection_basis"] == "OWNER_OVERRIDE"

print("Physics self-help core grammar v6: PASS")
