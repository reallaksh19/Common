#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "topics" / "m2d-sba23-v7-realization-plan.json").read_text())

assert PLAN["architecture_version"] == "SELF_HELP_V7"
assert PLAN["bucket_id"] == "M2D-SBA-23"
assert PLAN["intrinsic_difficulty_badge"] == "HARD"

src = PLAN["source_boundary"]
assert src["primary_core2_item_id"] == "Q15"
assert src["exact_prompt"] == "HELD"
assert src["source_solution"] == "HELD"
assert src["source_h1_h2_h3"] == "HELD"
assert src["production_core2a_legal_item_count"] == 0
assert src["author_created_items_may_substitute_for_q15"] is False
assert src["owner_may_release_q15_without_source_resolution"] is False

# Canonical laws/checks may repeat semantically; examples/visual states may not silently mirror.
assets = {a["asset_id"]: a for a in PLAN["canonical_assets"]}
assert assets["EQ-ML-GALILEAN-ADD-01"]["cross_core_reuse"] == "SEMANTIC_REUSE_ALLOWED"
assert assets["REP-ML-VELOCITY-TRIANGLE-01"]["cross_core_reuse"] == "TRANSFORM_OR_RECONSTRUCT_NOT_SILENT_COPY"

sdu = PLAN["sdu_realization"]
assert sdu["student_knowledge_pct_used"] is False
assert sdu["shared_soft_maximum_page_envelope"] == 30
assert sdu["core1a_actual_length_derived_independently"] is True
assert sdu["core1b_actual_length_derived_independently"] is True

c1a = sdu["core1a"]
c1b = sdu["core1b"]
assert c1a["ttu_family"] == "CONCEPT_TTU"
assert c1b["ttu_family"] == "CONCEPT_TTU"
assert c1a["worked_example_fingerprint"]["fingerprint_id"] != c1b["practice_example_fingerprint"]["fingerprint_id"]
assert c1a["worked_example_fingerprint"]["numeric_values"] != c1b["practice_example_fingerprint"]["numeric_values"]
assert c1b["relationship_to_core1a_example"] == "PEDAGOGICAL_TRANSFORMATION"
assert c1b["same_numeric_dataset_as_core1a"] is False
assert c1b["same_solution_surface_as_core1a"] is False
assert c1b["observed_evidence_required_for_mastery"] is True

# Hard B-layer reconstruction must be richer than completion blanks.
required_modes = {"GENERATION", "SELECTION", "DISCRIMINATION", "DIAGNOSIS", "DERIVATION_CONNECTION", "VERIFICATION"}
assert required_modes.issubset(set(c1b["high_value_transformation_modes"]))

lau = PLAN["lau_realization"]
assert lau["production_selection_basis"] == "UNRESOLVED_BECAUSE_LEGAL_POOL_EMPTY"
pilot = lau["design_pilot_selection_basis"]
assert pilot["type"] == "OWNER_OVERRIDE"
assert pilot["support_band"] == "GUIDED"

c2a = lau["core2a"]
c2b = lau["core2b"]
assert c2a["status"] == "BLOCKED_SOURCE_CUSTODY"
assert c2a["production_legal_items"] == []
assert c2a["generated_design_items_are_legal_pool"] is False
assert c2a["design_pilot_must_be_marked_nonproduction"] is True
assert c2b["status"] == "BLOCKED_CORE2A_LEGAL_POOL"
assert c2b["production_transfer_items"] == []
assert c2b["fading_anchor_counts_as_independent_transfer_evidence"] is False
assert c2b["structural_sibling_may_count_as_transfer_evidence"] is True
assert c2b["far_transfer_sibling_may_count_as_transfer_evidence"] is True

anti = PLAN["cross_core_duplication_controls"]
assert anti["fundamental_equation_repetition_allowed"] is True
assert anti["exact_explanatory_paragraph_repetition_allowed"] is False
assert anti["exact_numeric_example_reuse_across_adjacent_ab_layers_default"] == "PROHIBITED"
assert anti["example_fingerprint_comparison_required"] is True
assert anti["pedagogical_duplication_release_allowed"] is False
assert anti["core2_source_question_may_be_rewritten_to_create_freshness"] is False

# The plan must fail closed on production publication while source/manuscript authority is unresolved.
gates = PLAN["release_gates"]
assert gates["G_FIT"] == "DESIGN_PILOT_OWNER_OVERRIDE_ONLY"
assert gates["G_PUBLICATION"] == "BLOCKED_UPSTREAM_SOURCE_AND_MANUSCRIPT_RELEASE"

print("SBA23 V7 CDAU/SDU/LAU realization: PASS")
