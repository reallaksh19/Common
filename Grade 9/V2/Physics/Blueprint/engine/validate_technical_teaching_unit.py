#!/usr/bin/env python3
from __future__ import annotations


def validate_ttu_v2_semantics(ttu: dict) -> None:
    canonical = ttu["canonical_completed_state"]
    rep = canonical["representation"]
    element_ids = {e["element_id"] for e in rep["elements"]}
    relation_ids = {r["relation_id"] for r in canonical["governing_relations"]}
    step_ids = {s["step_id"] for s in canonical["working_steps"]}

    if len(element_ids) != len(rep["elements"]):
        raise AssertionError("TTU2_DUPLICATE_CANONICAL_ELEMENT_ID")

    for b in rep["bindings"]:
        if b["element_id"] not in element_ids:
            raise AssertionError("TTU2_BINDING_UNKNOWN_ELEMENT")
        if b["relation_or_step_id"] not in relation_ids | step_ids:
            raise AssertionError("TTU2_BINDING_UNKNOWN_RELATION_OR_STEP")

    for s in canonical["working_steps"]:
        if not set(s["uses_element_ids"]).issubset(element_ids):
            raise AssertionError("TTU2_WORKING_UNKNOWN_ELEMENT")
        if not set(s["uses_relation_ids"]).issubset(relation_ids):
            raise AssertionError("TTU2_WORKING_UNKNOWN_RELATION")

    rc = ttu["reconstruction_contract"]
    omitted_ids = [o["element_id"] for o in rc["omissions"]]
    if len(set(omitted_ids)) != len(omitted_ids):
        raise AssertionError("TTU2_DUPLICATE_OMISSION")
    if not set(omitted_ids).issubset(element_ids):
        raise AssertionError("TTU2_OMISSION_NOT_IN_CANONICAL_STATE")

    canonical_semantics = {e["element_id"]: e["semantic_type"] for e in rep["elements"]}
    for o in rc["omissions"]:
        if canonical_semantics[o["element_id"]] != o["semantic_type"]:
            raise AssertionError("TTU2_OMISSION_SEMANTIC_TYPE_DRIFT")

    help_steps = rc["fixed_help"]["steps"]
    help_ids = [h["help_id"] for h in help_steps]
    if len(set(help_ids)) != len(help_ids):
        raise AssertionError("TTU2_DUPLICATE_HELP_ID")
    for h in help_steps:
        addressed = set(h["addresses_element_ids"])
        if not addressed.issubset(set(omitted_ids)):
            raise AssertionError("TTU2_HELP_NOT_BOUND_TO_OMISSION")

    if ttu["task_scale"] == "SUBSTANTIVE" and ttu["difficulty_badge"] == "HARD":
        if len(omitted_ids) < 2:
            raise AssertionError("TTU2_HARD_SUBSTANTIVE_NEEDS_TWO_MEANINGFUL_OMISSIONS")
        functions = {h["function"] for h in help_steps}
        if functions != {"NOTICE", "REPRESENT", "START"}:
            raise AssertionError("TTU2_HARD_SUBSTANTIVE_HELP_FUNCTION_DRIFT")
        structural = {
            "FRAME_LABEL", "AXIS_OR_SIGN", "VECTOR", "VECTOR_DIRECTION", "COMPONENT",
            "FORCE", "EVENT_MARKER", "GRAPH_AXIS", "GRAPH_FEATURE", "GEOMETRIC_CONSTRAINT",
            "EQUATION_TERM", "MODEL_CONDITION", "BOUNDARY_CONDITION", "INTERMEDIATE_STATE"
        }
        if not any(o["semantic_type"] in structural for o in rc["omissions"]):
            raise AssertionError("TTU2_NO_STRUCTURAL_OMISSION")

    for rule in ttu["verification_contract"]["independent_rules"]:
        if rule["uses_answer_key"] is not False or rule["applicable_before_reveal"] is not True:
            raise AssertionError("TTU2_VERIFICATION_NOT_INDEPENDENT")

    for realization in ttu["layer_realizations"]:
        if realization["layer"] in {"CORE1B", "CORE2B"}:
            if not realization["uses_reconstruction_contract"]:
                raise AssertionError("TTU2_B_LAYER_WITHOUT_RECONSTRUCTION")
            if realization["mode"] not in {"RECONSTRUCTION", "TRANSFER_RECONSTRUCTION"}:
                raise AssertionError("TTU2_B_LAYER_MODE_DRIFT")


def validate_ttu_v2(ttu: dict) -> dict:
    validate_ttu_v2_semantics(ttu)
    return ttu
