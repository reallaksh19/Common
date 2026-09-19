"""Cognition-before-manuscript validation with explicit semantic bridges."""

from __future__ import annotations

from .contracts import require, strings, text, unique, validate_dag


COMPONENTS = {"TRANSFORMATION", "ATOMS", "INFERENCE", "EQUATION", "REPRESENTATION", "MISCONCEPTION", "FADING"}


def validate_plan(plan: dict, join: dict, context: dict) -> dict:
    obligations = unique(join["obligations"], "obligation_id", "OBLIGATION_ID_DUPLICATE")
    treatments = unique(plan.get("treatments", []), "obligation_id", "TREATMENT_DUPLICATE")
    require(set(treatments) == set(obligations), "ASSIMILATION_OBLIGATION_COVERAGE")
    all_atoms = []
    for oid, treatment in treatments.items():
        _validate_treatment(treatment, obligations[oid], context)
        all_atoms.extend(treatment["atoms"])
    validate_dag(all_atoms, "atom_id", "prerequisite_atom_ids")
    text(plan.get("whole_concept_reconstruction"), "WHOLE_CONCEPT_RECONSTRUCTION_REQUIRED")
    require(plan.get("unresolved_required_jumps") == [], "UNRESOLVED_INFERENCE_JUMPS")
    require(plan.get("new_semantic_claims") == [], "NEW_SEMANTICS_REQUIRE_CORE_REVIEW")
    return plan


def _validate_treatment(treatment: dict, obligation: dict, context: dict) -> None:
    required = set(obligation["required_components"])
    require(required <= COMPONENTS, "UNKNOWN_ASSIMILATION_COMPONENT")
    require({"TRANSFORMATION", "ATOMS", "INFERENCE"} <= required,
            "CORE_ASSIMILATION_COMPONENTS_REQUIRED")
    change = treatment.get("transformation", {})
    for field in ("before", "difficult_connection", "after", "failure_probe"):
        text(change.get(field), "COGNITIVE_TRANSFORMATION_REQUIRED")
    atoms = treatment.get("atoms", [])
    require(bool(atoms), "TEACHING_ATOMS_REQUIRED")
    for atom in atoms:
        for field in ("atom_id", "entry_assumption", "learner_action", "justification", "meaning", "check", "split_rationale"):
            text(atom.get(field), "ATOM_INTELLECTUAL_CONTENT_REQUIRED")
    edges = treatment.get("inference_chain", [])
    require(bool(edges), "INFERENCE_CHAIN_REQUIRED")
    for edge in edges:
        for field in ("from_atom", "to_atom", "rule", "prerequisite_support", "why_permissible"):
            text(edge.get(field), "INFERENCE_EDGE_REQUIRED")
    atom_ids = {x["atom_id"] for x in atoms}
    require(all(x["from_atom"] in atom_ids and x["to_atom"] in atom_ids for x in edges),
            "INFERENCE_UNKNOWN_ATOM")
    if "EQUATION" in required:
        _validate_equation(treatment.get("equation", {}), context["subject_policy"])
    if "REPRESENTATION" in required:
        _validate_representation(treatment.get("representation", {}))
    if "MISCONCEPTION" in required:
        for field in ("wrong_chain", "contrast", "repair", "boundary"):
            text(treatment.get("misconception", {}).get(field), "MISCONCEPTION_REPAIR_REQUIRED")
    if "FADING" in required:
        _validate_fading(treatment.get("fading", {}), context["request"])


def _validate_equation(equation: dict, subject_policy: dict) -> None:
    for field in ("relation", "parent_basis", "meaning", "validity_limits", "failure_case"):
        text(equation.get(field), "EQUATION_ANATOMY_REQUIRED")
    strings(equation.get("conditions"), "EQUATION_CONDITIONS_REQUIRED")
    symbols = equation.get("symbols", [])
    require(bool(symbols), "SYMBOL_BRIDGE_REQUIRED")
    unique(symbols, "symbol", "SYMBOL_DUPLICATE")
    for symbol in symbols:
        text(symbol.get("meaning"), "SYMBOL_MEANING_REQUIRED")
        text(symbol.get("unit_or_domain"), "SYMBOL_UNIT_OR_DOMAIN_REQUIRED")
    steps = equation.get("steps", [])
    require(bool(steps), "EQUATION_DERIVATION_REQUIRED")
    for step in steps:
        for field in ("from", "to", "rule", "interpretation"):
            text(step.get(field), "EQUATION_STEP_JUSTIFICATION_REQUIRED")
    semantics = equation.get("subject_semantics", {})
    for field in subject_policy["equation_semantic_fields"]:
        text(semantics.get(field), "SUBJECT_EQUATION_SEMANTICS_REQUIRED")


def _validate_representation(rep: dict) -> None:
    for field in ("cognitive_need", "notice_before_math", "reading_conventions", "word_symbol_bridge"):
        text(rep.get(field), "REPRESENTATION_REASONING_REQUIRED")
    strings(rep.get("must_not_imply"), "REPRESENTATION_RISK_REQUIRED")
    candidates = unique(rep.get("candidates", []), "candidate_id", "REPRESENTATION_CANDIDATE_DUPLICATE")
    require(len(candidates) >= 2, "REPRESENTATION_ALTERNATIVE_REQUIRED")
    for row in candidates.values():
        for field in ("description", "affordance", "interpretation_cost", "limitation"):
            text(row.get(field), "REPRESENTATION_CANDIDATE_REASONING_REQUIRED")
        require(type(row.get("admissible")) is bool, "REPRESENTATION_ADMISSIBILITY_REQUIRED")
    selected = rep.get("selected_candidate_id")
    require(selected in candidates and candidates[selected]["admissible"], "INADMISSIBLE_REPRESENTATION")
    text(rep.get("selection_reason"), "REPRESENTATION_SELECTION_REASON_REQUIRED")
    rejected = unique(rep.get("rejections", []), "candidate_id", "REPRESENTATION_REJECTION_DUPLICATE")
    require(set(rejected) == set(candidates) - {selected}, "REPRESENTATION_REJECTION_COVERAGE")
    for row in rejected.values():
        text(row.get("reason"), "REPRESENTATION_REJECTION_REASON_REQUIRED")


def _validate_fading(fading: dict, request: dict) -> None:
    stages = fading.get("stages", [])
    order = [x.get("stage") for x in stages]
    full = ["MODELLED", "GUIDED", "FADED", "INDEPENDENT"]
    require(bool(order) and order == full[:len(order)], "FADING_ORDER_INVALID")
    for row in stages:
        for field in ("retained_support", "removed_support", "learner_responsibility", "check"):
            text(row.get(field), "FADING_DECISION_REQUIRED")
    if "INDEPENDENT" in request["practice"]["allowed_support"]:
        require(order == full, "INDEPENDENT_SUPPORT_PATH_INCOMPLETE")
    elif order != full:
        text(fading.get("bounded_support_reason"), "BOUNDED_FADING_REASON_REQUIRED")
