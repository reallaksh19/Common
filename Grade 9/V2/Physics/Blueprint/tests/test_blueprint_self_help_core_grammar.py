#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = json.loads((ROOT / "policy" / "self-help-core-publication.v4.json").read_text())
BUCKET = json.loads((ROOT / "policy" / "core1ab-bucket-authoring.v2.json").read_text())
KNOW = json.loads((ROOT / "policy" / "core2ab-knowledge-routing.v1.json").read_text())
TECH = json.loads((ROOT / "policy" / "technical-density-and-figure-contract.v1.json").read_text())
LAYOUT = json.loads((ROOT / "policy" / "pdf-layout-integrity.v1.json").read_text())
PILOT = json.loads((ROOT / "topics" / "self-help-three-topic-falsification-pilot.v3.json").read_text())

# Core1 family stays bucket-wise and knowledge-percent independent.
cp = PUB["control_planes"]
assert cp["CORE1_FAMILY"]["student_knowledge_pct_drives_authored_depth"] is False
assert cp["CORE1_FAMILY"]["always_subtopic_bucket_wise"] is True
assert cp["CORE1_FAMILY"]["shared_learning_model_required"] is True
assert cp["CORE2_FAMILY"]["student_knowledge_pct_required_unless_owner_override"] is True

# Family-first / inference-first authoring.
center = PUB["authoring_center"]
assert center["primary_units_in_order"][:4] == [
    "SUBTOPIC_BUCKET", "HIDDEN_INVARIANT", "INFERENTIAL_JUMP", "PROBLEM_FAMILY"
]
assert "prose volume" in center["anti_pattern"]
assert "A/B symmetry" in center["anti_pattern"]

# Shared bucket model and asymmetric page budgets remain required.
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

# Hard means technical closure, not prose or visual inflation.
hard = PUB["hard_bucket_release"]
assert hard["prose_only_release_allowed"] is False
assert hard["core1a_requires_visible_technical_closure"] is True
assert hard["core1b_requires_technical_reconstruction_at_fragile_checkpoints"] is True
assert hard["long_prose_may_substitute_for_diagrams_equations_when_material"] is False

assert TECH["hard_bucket_contract"]["prose_only_release_allowed"] is False
assert "EQUATION_OR_SYMBOLIC_RELATION" in TECH["hard_bucket_contract"]["required_technical_forms_when_material"]
assert "DIAGRAM_OR_GRAPH" in TECH["hard_bucket_contract"]["required_technical_forms_when_material"]
assert "COMPONENT_OR_VECTOR_REPRESENTATION" in TECH["hard_bucket_contract"]["required_technical_forms_when_material"]
assert "WORKED_TRANSFORMATION_OR_DERIVATION" in TECH["hard_bucket_contract"]["required_technical_forms_when_material"]
assert "prose prompts" in TECH["core1b"]["prohibited_failure_mode"]

# A/B remain dominant modes, not duplicate books.
assert PUB["mode_rule"]["dominant_not_exclusive"] is True
assert PUB["mode_rule"]["parallel_duplicate_books_for_A_and_B"] is False
roles = PUB["learner_surface_roles"]
assert roles["CORE1A"]["mode"] == "DECLARATIVE_DOMINANT_DEEP_TEACHING"
assert roles["CORE1B"]["mode"] == "GENERATIVE_DOMINANT_TECHNICAL_RECONSTRUCTION"
assert roles["CORE1B"]["page_budget"] == "DERIVED_FROM_FRAGILE_CHECKPOINT_COVERAGE_NOT_BADGE_SYMMETRY"
assert "INCOMPLETE_OR_RECONSTRUCTABLE" in roles["CORE1B"]["technical_expectation"]

# Hint ladder remains conditional.
assert PUB["task_grammar_policy"]["MICRO_PROMPT"]["full_hint_ladder_required"] is False
assert PUB["task_grammar_policy"]["REPRESENTATION_TASK"]["technical_representation_must_be_visible"] is True
assert PUB["task_grammar_policy"]["SUBSTANTIVE_TASK"]["progressive_rescue_required_when_learner_can_be_stranded"] is True
assert PUB["task_grammar_policy"]["SUBSTANTIVE_TASK"]["full_technical_check_required"] is True

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

# Core2A/2B remain asymmetric and technically explicit.
assert roles["CORE2A"]["selection_rule"] == "REPRESENTATIVE_EXEMPLARS_BY_FAMILY_AND_DEMAND_NOT_AUTOMATIC_ALL_ITEM_SOLVING"
assert "EXPERT_REPRESENTATION" in roles["CORE2A"]["technical_expectation"]
assert "AVOID_ONE_FOR_ONE_MIRROR" in roles["CORE2B"]["selection_rule"]
assert "SELECTS_OR_CONSTRUCTS_TECHNICAL_REPRESENTATION" in roles["CORE2B"]["technical_expectation"]

# PDF layout is fail-closed: successful generation alone is not release.
assert PUB["layout_release"]["successful_pdf_generation_is_visual_preflight_pass"] is False
assert PUB["layout_release"]["render_every_page"] is True
assert PUB["layout_release"]["fail_on_text_figure_overlap"] is True
assert PUB["layout_release"]["fail_on_clipped_labels"] is True
assert PUB["layout_release"]["flow_layout_or_collision_validation_required"] is True
assert LAYOUT["preflight"]["render_every_page"] is True
assert LAYOUT["preflight"]["fail_closed"] is True
assert "TEXT_FIGURE_OVERLAP" in LAYOUT["preflight"]["must_check"]
assert "HEADER_FIGURE_COLLISION" in LAYOUT["preflight"]["must_check"]

# Three-topic pilot retains source holds and knowledge-routing rules.
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

print("Physics self-help core grammar v4: PASS")
