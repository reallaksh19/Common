#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; PHYS=ROOT.parent

def load(path:Path):return json.loads(path.read_text(encoding="utf-8"))

def validate_ttu_v2_semantics(ttu:dict)->None:
    canonical=ttu["canonical_completed_state"]
    rep=canonical["representation"]
    element_ids={e["element_id"] for e in rep["elements"]}
    relation_ids={r["relation_id"] for r in canonical["governing_relations"]}
    step_ids={s["step_id"] for s in canonical["working_steps"]}

    if len(element_ids)!=len(rep["elements"]):raise AssertionError("TTU2_DUPLICATE_CANONICAL_ELEMENT_ID")
    for b in rep["bindings"]:
        if b["element_id"] not in element_ids:raise AssertionError("TTU2_BINDING_UNKNOWN_ELEMENT")
        if b["relation_or_step_id"] not in relation_ids|step_ids:raise AssertionError("TTU2_BINDING_UNKNOWN_RELATION_OR_STEP")
    for s in canonical["working_steps"]:
        if not set(s["uses_element_ids"]).issubset(element_ids):raise AssertionError("TTU2_WORKING_UNKNOWN_ELEMENT")
        if not set(s["uses_relation_ids"]).issubset(relation_ids):raise AssertionError("TTU2_WORKING_UNKNOWN_RELATION")

    rc=ttu["reconstruction_contract"]
    omitted_ids=[o["element_id"] for o in rc["omissions"]]
    if len(set(omitted_ids))!=len(omitted_ids):raise AssertionError("TTU2_DUPLICATE_OMISSION")
    if not set(omitted_ids).issubset(element_ids):raise AssertionError("TTU2_OMISSION_NOT_IN_CANONICAL_STATE")
    canonical_semantics={e["element_id"]:e["semantic_type"] for e in rep["elements"]}
    for o in rc["omissions"]:
        if canonical_semantics[o["element_id"]]!=o["semantic_type"]:raise AssertionError("TTU2_OMISSION_SEMANTIC_TYPE_DRIFT")

    help_steps=rc["fixed_help"]["steps"]
    help_ids=[h["help_id"] for h in help_steps]
    if len(set(help_ids))!=len(help_ids):raise AssertionError("TTU2_DUPLICATE_HELP_ID")
    for h in help_steps:
        if not set(h["addresses_element_ids"]).issubset(set(omitted_ids)):raise AssertionError("TTU2_HELP_NOT_BOUND_TO_OMISSION")

    if ttu["task_scale"]=="SUBSTANTIVE" and ttu["difficulty_badge"]=="HARD":
        if len(omitted_ids)<2:raise AssertionError("TTU2_HARD_SUBSTANTIVE_NEEDS_TWO_MEANINGFUL_OMISSIONS")
        funcs={h["function"] for h in help_steps}
        if funcs!={"NOTICE","REPRESENT","START"}:raise AssertionError("TTU2_HARD_SUBSTANTIVE_HELP_FUNCTION_DRIFT")
        structural={"FRAME_LABEL","AXIS_OR_SIGN","VECTOR","VECTOR_DIRECTION","COMPONENT","FORCE","EVENT_MARKER","GRAPH_AXIS","GRAPH_FEATURE","GEOMETRIC_CONSTRAINT","EQUATION_TERM","MODEL_CONDITION","BOUNDARY_CONDITION","INTERMEDIATE_STATE"}
        if not any(o["semantic_type"] in structural for o in rc["omissions"]):raise AssertionError("TTU2_NO_STRUCTURAL_OMISSION")

    for rule in ttu["verification_contract"]["independent_rules"]:
        if rule["uses_answer_key"] is not False or rule["applicable_before_reveal"] is not True:raise AssertionError("TTU2_VERIFICATION_NOT_INDEPENDENT")

    for lr in ttu["layer_realizations"]:
        if lr["layer"] in {"CORE1B","CORE2B"}:
            if not lr["uses_reconstruction_contract"]:raise AssertionError("TTU2_B_LAYER_WITHOUT_RECONSTRUCTION")
            if lr["mode"] not in {"RECONSTRUCTION","TRANSFER_RECONSTRUCTION"}:raise AssertionError("TTU2_B_LAYER_MODE_DRIFT")

def validate():
    names=["architecture-blueprint.schema.json","packet-envelope.schema.json","evidence-state.schema.json","routing-decision.schema.json","independent-validation-session.schema.json","join-packet.schema.json","role-bindings.schema.json","learner-purpose-control-state.schema.json","core1a-stage-run.schema.json","topic-blueprint.schema.json","publication-ir.schema.json","render-custody.schema.json","render-preflight-report.schema.json","m2d-render-readiness.schema.json","m2d-manuscript-release-binding.schema.json","m2d-composition-plan.schema.json","b-layer-runtime-boundary.schema.json","technical-teaching-unit.schema.json","technical-teaching-unit-v2.schema.json","blueprint-agent-task-intake.schema.json","blueprint-execution-route-registry.schema.json","physics-curriculum-scope-binding-registry.schema.json","physics-blueprint-authority-projection.schema.json","scoped-evidence-receipt.schema.json","seven-core-stress-test-receipt.schema.json"]
    schemas={n:load(ROOT/"contracts"/n) for n in names}
    for s in schemas.values():Draft202012Validator.check_schema(s)
    architecture=load(ROOT/"policy"/"architecture.v1.json");Draft202012Validator(schemas["architecture-blueprint.schema.json"]).validate(architecture)
    bindings=load(ROOT/"policy"/"role-bindings.v1.json");Draft202012Validator(schemas["role-bindings.schema.json"]).validate(bindings)
    b_policy=load(ROOT/"policy"/"b-layer-runtime-boundary.v1.json");Draft202012Validator(schemas["b-layer-runtime-boundary.schema.json"]).validate(b_policy)
    route_registry=load(ROOT/"registry"/"physics-agent-task-execution-routes.v1.json");Draft202012Validator(schemas["blueprint-execution-route-registry.schema.json"]).validate(route_registry)
    curriculum_registry=load(ROOT/"registry"/"physics-curriculum-scope-bindings.v1.json");Draft202012Validator(schemas["physics-curriculum-scope-binding-registry.schema.json"]).validate(curriculum_registry)
    ids=[row["binding_id"] for row in curriculum_registry["bindings"]]
    if len(ids)!=len(set(ids)):raise AssertionError("PHYSICS_CURRICULUM_BINDING_ID_DUPLICATE")
    ev=Draft202012Validator(schemas["evidence-state.schema.json"])
    for f in sorted((ROOT/"fixtures"/"golden").glob("*.json")):ev.validate(load(f)["evidence"])

    # Legacy TTU v1 stays readable, but new architecture requires a TTU v2 process golden.
    ttu1_validator=Draft202012Validator(schemas["technical-teaching-unit.schema.json"])
    for f in sorted((ROOT/"fixtures"/"technical-ttu").glob("*.json")):ttu1_validator.validate(load(f))
    ttu2_validator=Draft202012Validator(schemas["technical-teaching-unit-v2.schema.json"])
    ttu2_files=sorted((ROOT/"fixtures"/"technical-ttu-v2").glob("*.json"))
    if not ttu2_files:raise AssertionError("TECHNICAL_TTU_V2_PROCESS_GOLDEN_MISSING")
    for f in ttu2_files:
        obj=load(f);ttu2_validator.validate(obj);validate_ttu_v2_semantics(obj)

    if any(architecture["role_lifecycle"].get(r)!="ACTIVE" for r in ("CORE2A","CORE1B","CORE2B")):raise AssertionError("BLUEPRINT_ACTIVE_ROLE_LIFECYCLE_DRIFT")
    if b_policy.get("status")!="ACTIVE":raise AssertionError("B_LAYER_GOVERNANCE_NOT_ACTIVE")
    if architecture["invariants"]["max_subtopics_per_handoff"]!=3 or not architecture["invariants"]["learning_atoms_unbounded"]:raise AssertionError("TRANSPORT_PEDAGOGY_BOUND_DRIFT")
    if set(architecture["roles"])!={"CORE0","CORE1","CORE2","JOIN","CORE1A","CORE1B","CORE2A","CORE2B"}:raise AssertionError("BLUEPRINT_ROLE_SET_DRIFT")
    if architecture["planes"]["RUNTIME"]["authority"]!="AUTHORIZED_EXPERIENCE_EXECUTION":raise AssertionError("B_LAYER_RUNTIME_PLANE_DRIFT")
    for key in ("core2a_requires_taught_state_receipts","core2a_may_not_infer_learner_mastery","b_layers_have_no_semantic_or_legality_authority","core1b_requires_released_core1a_authority","teaching_configuration_cannot_prove_learner_state","core2b_requires_digest_bound_core2a_legal_pool","core2b_escalation_requires_per_capability_evidence","runtime_evidence_is_append_only","repair_routing_cannot_rewrite_a_layer_authority"):
        if not architecture["invariants"][key]:raise AssertionError("BLUEPRINT_INVARIANT_DISABLED:"+key)
    if bindings["canonical_root"]!="Grade 9/V2/Physics/Blueprint" or bindings["roles"]["JOIN"]["ownership"]!="BLUEPRINT_NATIVE":raise AssertionError("PHYSICS_BLUEPRINT_ROLE_BINDING_DRIFT")
    if bindings["roles"]["CORE1B"]["implementation_root"]!="Grade 9/V2/Physics/Core1B" or bindings["roles"]["CORE2B"]["implementation_root"]!="Grade 9/V2/Physics/Core2B":raise AssertionError("B_LAYER_IMPLEMENTATION_ROOT_DRIFT")
    required_runtime_files=[PHYS/"Core1B"/"engine"/"core1b_runtime.py",PHYS/"Core1B"/"tests"/"test_core1b_runtime.py",PHYS/"Core2B"/"engine"/"core2b_runtime.py",PHYS/"Core2B"/"tests"/"test_core2b_runtime.py"]
    if not all(p.exists() for p in required_runtime_files):raise AssertionError("ACTIVE_B_LAYER_RUNTIME_MISSING")
    independent=load(ROOT/"policy"/"independent-validation.v1.json");join=load(ROOT/"policy"/"join-policy.v1.json");purpose=load(ROOT/"policy"/"purpose-contracts.v1.json");c1a=load(ROOT/"policy"/"core1a-stage-machine.v1.json");pub=load(ROOT/"policy"/"publication-boundary.v1.json");render=load(ROOT/"policy"/"render-preflight.v1.json");m2d_rep=load(ROOT/"policy"/"m2d-representation-requirements.v1.json");m2d_comp=load(ROOT/"policy"/"m2d-composition-release.v1.json")
    if not independent["self_validation_forbidden"] or not independent["fresh_validator_instance_required"]:raise AssertionError("INDEPENDENT_VALIDATION_POLICY_DISABLED")
    if join["coverage_rule"]!="EVERY_CORE2_DEMAND_CLAIM_EXACTLY_ONCE" or not join["critical_conflict_blocks_core1a"]:raise AssertionError("JOIN_POLICY_DRIFT")
    if purpose["invariant"]!="PURPOSE_CANNOT_BYPASS_REQUIRED_PREREQUISITES" or set(purpose["purposes"])!={"FIRST_STUDY","PRACTICE","REVISION","COMPETITIVE_EXAM"}:raise AssertionError("PURPOSE_POLICY_DRIFT")
    if len(c1a["pre_manuscript_stages"])!=12 or c1a["manuscript_stage"]!="1A12_MANUSCRIPT" or c1a["rules"]["unresolved_required_jump_count_must_equal"]!=0:raise AssertionError("CORE1A_STAGE_MACHINE_DRIFT")
    if pub["semantic_authority"]!="UPSTREAM_ONLY" or pub["renderer_authority"]!="COMPOSITION_ONLY" or not pub["renderer_semantic_generation_forbidden"]:raise AssertionError("PUBLICATION_AUTHORITY_BOUNDARY_DRIFT")
    if render["release_rule"]["machine_preflight_can_authorize_release"] or not render["release_rule"]["human_visual_review_required"]:raise AssertionError("RENDER_RELEASE_GATE_DRIFT")
    if render["page_geometry"]["format"]!="A4_PORTRAIT" or render["sample_raster_dpi"]<144:raise AssertionError("RENDER_PHYSICAL_QA_POLICY_DRIFT")
    if m2d_rep.get("topic_id")!="PHY-M2D" or not all((m2d_rep.get("rules") or {}).values()):raise AssertionError("M2D_REPRESENTATION_GAP_POLICY_DRIFT")
    if m2d_comp.get("topic_id")!="PHY-M2D" or not all((m2d_comp.get("rules") or {}).values()):raise AssertionError("M2D_COMPOSITION_RELEASE_POLICY_DRIFT")

    self_help=load(ROOT/"policy"/"self-help-core-publication.v6.json");ttu_policy=load(ROOT/"policy"/"technical-teaching-unit.v2.json");rep_quality=load(ROOT/"policy"/"physics-representation-semantic-quality.v1.json");layout=load(ROOT/"policy"/"pdf-layout-integrity.v2.json")
    gate=self_help["technical_teaching_unit_gate"]
    for k in ("canonical_completed_state_required","reconstruction_contract_required","semantic_omission_required","learner_reconstruction_task_required","fixed_help_required","canonical_reveal_after_attempt_required","independent_verification_required","representation_must_bind_to_reasoning"):
        if not gate[k]:raise AssertionError("TTU_V2_GATE_DISABLED:"+k)
    if gate["cosmetic_blank_counts_as_reconstruction"]:raise AssertionError("TTU_V2_COSMETIC_BLANK_ALLOWED")
    if gate["compare_with_answer_counts_as_independent_verification"]:raise AssertionError("TTU_V2_ANSWER_COMPARISON_FALSE_VERIFICATION")
    if not ttu_policy["reconstruction_contract"]["omissions_must_be_semantically_material"]:raise AssertionError("TTU_V2_SEMANTIC_OMISSION_GATE_DISABLED")
    if ttu_policy["verification"]["compare_with_answer_is_independent_verification"]:raise AssertionError("TTU_V2_VERIFY_GATE_DISABLED")
    if rep_quality["binding_rule"]["figure_without_reasoning_binding_counts_as_technical_closure"]:raise AssertionError("FIGURE_BINDING_GATE_DISABLED")
    if layout["composition"]["oversized_figure_displacing_required_working_allowed"]:raise AssertionError("OVERSIZED_FIGURE_GATE_DISABLED")
    sys.path.insert(0,str(ROOT/"engine"));from validate_b_layer_boundary import validate_boundary;validate_boundary(b_policy,architecture,bindings)
    print("Blueprint contracts: PASS")
if __name__=="__main__":validate()
