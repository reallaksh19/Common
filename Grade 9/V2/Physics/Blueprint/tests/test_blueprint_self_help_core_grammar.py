#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = json.loads((ROOT / "policy" / "self-help-core-publication.v3.json").read_text())
BUCKET = json.loads((ROOT / "policy" / "core1ab-bucket-authoring.v2.json").read_text())
KNOW = json.loads((ROOT / "policy" / "core2ab-knowledge-routing.v1.json").read_text())
PILOT = json.loads((ROOT / "topics" / "self-help-three-topic-falsification-pilot.v3.json").read_text())

# Core1 family stays bucket-wise and knowledge-percent independent.
cp = PUB["control_planes"]
assert cp["CORE1_FAMILY"]["student_knowledge_pct_drives_authored_depth"] is False
assert cp["CORE1_FAMILY"]["always_subtopic_bucket_wise"] is True
assert cp["CORE1_FAMILY"]["shared_learning_model_required"] is True
assert cp["CORE2_FAMILY"]["student_knowledge_pct_required_unless_owner_override"] is True

# Authoring must be centered on invariant/jump/family, not page symmetry.
center = PUB["authoring_center"]
assert center["primary_units_in_order"][:4] == [
    "SUBTOPIC_BUCKET",
    "HIDDEN_INVARIANT",
    "INFERENTIAL_JUMP",
    "PROBLEM_FAMILY",
]
assert "A/B symmetry" in center["anti_pattern"]

# Shared bucket model must be explicit.
shared = BUCKET["shared_bucket_learning_model"]
assert set(shared["required_fields"]) == {
    "HIDDEN_INVARIANTS",
    "PREREQUISITE_BRIDGES",
    "INFERENTIAL_JUMPS",
    "REPRESENTATIONS",
    "MISCONCEPTIONS",
    "PROBLEM_FAMILIES",
    "SOURCE_CORE2_LINKAGE",
    "FRAGILE_CHECKPOINTS",
}

# Page-budget asymmetry: 10/20/30 belong to Core1A, not automatically Core1B.
pb = BUCKET["page_budget_rule"]
assert pb["applies_primarily_to"] == "CORE1A"
assert pb["anti_padding"] is True
assert pb["core1b_inherits_core1a_page_budget"] is False
assert BUCKET["badges"]["EASY"]["core1a_soft_page_ceiling"] == 10
assert BUCKET["badges"]["MEDIUM"]["core1a_soft_page_ceiling"] == 20
assert BUCKET["badges"]["HARD"]["core1a_soft_page_ceiling"] == 30

# Difficulty controls inferential closure rather than visual quantity.
ds = BUCKET["difficulty_semantics"]
assert ds["normative_definition"] == "Difficulty controls inferential closure, not visual quantity."
assert ds["visual_quantity_is_quality_proxy"] is False
assert BUCKET["badges"]["MEDIUM"]["web_research_required_for_visual_and_pedagogy_design"] is True
assert BUCKET["badges"]["HARD"]["web_research_required_for_visual_and_pedagogy_design"] is True

# A/B are dominant modes, not exclusive content types.
mode = BUCKET["mode_rule"]
assert mode["A_B_ARE_DOMINANT_MODES_NOT_EXCLUSIVE_CONTENT_TYPES"] is True
assert "PREDICTION" in mode["CORE1A"]["may_include"]
assert "POST_ATTEMPT_EXPLANATION" in mode["CORE1B"]["may_include"]

# Core1B coverage is fragile-checkpoint/family driven, not badge page driven.
c1b = BUCKET["core1b_realization"]
assert c1b["page_budget_derivation"] == "CHECKPOINT_COVERAGE_NOT_DIFFICULTY_SYMMETRY"
assert c1b["fixed_badge_page_ceiling"] is False
assert "EVERY_FRAGILE_INFERENTIAL_JUMP_AT_LEAST_ONCE" in c1b["required_coverage"]
assert "EVERY_DISTINCT_PROBLEM_FAMILY_RECOGNITION_AT_LEAST_ONCE" in c1b["required_coverage"]

# Full H1/H2/H3 ladder is conditional, not mandatory for every micro-prompt.
hints = BUCKET["hint_ladder_rule"]
assert hints["mandatory_for_every_prompt"] is False
assert hints["every_open_prompt_requires_local_resolution"] is True
assert PUB["hint_ladder"]["mandatory_for_every_prompt"] is False
assert PUB["task_grammar_policy"]["MICRO_PROMPT"]["full_hint_ladder_required"] is False
assert PUB["task_grammar_policy"]["SUBSTANTIVE_TASK"]["progressive_rescue_required_when_learner_can_be_stranded"] is True

# Core2 knowledge/owner input remains mandatory and authority-safe.
rir = KNOW["required_input_rule"]
assert rir["no_silent_default"] is True
assert set(rir["selection_basis_enum"]) == {"KNOWLEDGE_PERCENT", "OWNER_OVERRIDE"}
assert rir["KNOWLEDGE_PERCENT"]["range_inclusive"] == [0, 100]
assert set(rir["OWNER_OVERRIDE"]["required_fields"]) == {"owner_ref", "reason", "support_band"}

guards = KNOW["authority_guards"]
assert guards["knowledge_pct_may_expand_core2a_legal_pool"] is False
assert guards["owner_override_may_expand_core2a_legal_pool"] is False
assert guards["owner_override_waives_only_missing_knowledge_pct"] is True

# Core2A is representative by family; Core2B is not a one-for-one mirror.
c2 = PUB["core2_family_realization"]
assert c2["core2a_should_solve_every_legal_item_by_default"] is False
assert c2["core2b_should_mirror_core2a_item_for_item"] is False
assert c2["prefer_different_transfer_items_after_worked_exemplars_when_legal_pool_allows"] is True
assert "MODEL_DISCRIMINATION" in c2["transfer_dimensions"]
assert "MULTI_STEP_BRIDGE" in c2["transfer_dimensions"]

roles = PUB["learner_surface_roles"]
assert roles["CORE1A"]["mode"] == "DECLARATIVE_DOMINANT_DEEP_TEACHING"
assert roles["CORE1B"]["mode"] == "GENERATIVE_DOMINANT_CONCEPT_RECONSTRUCTION"
assert roles["CORE1B"]["page_budget"] == "DERIVED_FROM_FRAGILE_CHECKPOINT_COVERAGE_NOT_BADGE_SYMMETRY"
assert roles["CORE2A"]["selection_rule"] == "REPRESENTATIVE_EXEMPLARS_BY_FAMILY_AND_DEMAND_NOT_AUTOMATIC_ALL_ITEM_SOLVING"
assert "AVOID_ONE_FOR_ONE_MIRROR" in roles["CORE2B"]["selection_rule"]

# Three-topic falsification pilot keeps source holds and new anti-symmetry criteria.
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

pc = PILOT["pass_criteria"]
assert pc["shared_bucket_learning_model_precedes_layer_realization"] is True
assert pc["core1a_page_ceiling_not_inherited_by_core1b"] is True
assert pc["difficulty_controls_inferential_closure_not_visual_quantity"] is True
assert pc["a_b_are_dominant_modes_not_exclusive_content_types"] is True
assert pc["full_hint_ladder_not_required_for_every_prompt"] is True
assert pc["core2a_representative_problem_family_selection"] is True
assert pc["core2b_not_one_for_one_core2a_mirror"] is True
assert pc["owner_override_does_not_expand_legality"] is True

print("Physics self-help core grammar v3: PASS")
