#!/usr/bin/env python3
"""Material-complete auto PublicationStructure projection.

Every RepresentationInstance selected by the PublicationPlan must travel through
an executable DEPICTION arc step. Every MATERIAL item emitted into a Study Guide
main section must also be selected by the executable structure; material may not
silently disappear between the semantic learner model and rendering.

This remains an engineering-replay projection. Mature learner products should
supply authored LearningDesignPlan and PublicationStructure rather than relying
on generic auto-generated pedagogy.
"""
from __future__ import annotations

import run_core2_patch3 as patch3

patch2 = patch3.patch2
impl = patch3.impl
_ORIG_AUTO = patch2._auto_structure


def _insert_step(unit: dict, role: str, refs: list[str], support_state: str) -> dict:
    existing = next((step for step in unit["arc_steps"] if step["role"] == role), None)
    if existing is not None:
        for ref in refs:
            if ref not in existing["content_refs"]:
                existing["content_refs"].append(ref)
        return existing

    order = {
        "PHYSICAL_SITUATION": 10,
        "DEPICTION": 20,
        "NOTICE": 30,
        "SAY_IN_WORDS": 40,
        "CONCEPT_INVARIANT": 45,
        "BUILD_RELATION": 50,
        "WHY_THIS_WORKS": 55,
        "MODEL_BOUNDARY": 60,
        "WORKED_EXAMPLE": 70,
        "GUIDED_1": 80,
        "GUIDED_2_FADED": 90,
        "INDEPENDENT_TRANSFER": 100,
        "RETRIEVAL_CHECK": 110,
    }
    target = order.get(role, 65)
    insert_at = len(unit["arc_steps"])
    for i, step in enumerate(unit["arc_steps"]):
        if order.get(step["role"], 65) > target:
            insert_at = i
            break
    step = {
        "step_id": f"{unit['unit_id']}-MAT-{role}-{len(unit['arc_steps']) + 1:02d}",
        "role": role,
        "content_refs": list(refs),
        "support_state": support_state,
    }
    unit["arc_steps"].insert(insert_at, step)
    return step


def _complete_material_selection(unit: dict, sec: dict) -> None:
    selected = {
        ref
        for step in unit.get("arc_steps", [])
        for ref in step.get("content_refs", [])
    }
    profile = unit.get("instructional_profile")
    state = "FULL" if profile in {"FOUNDATION", "BRIDGE"} else "REFERENCE"

    by_role: dict[str, list[str]] = {}
    for item in sec.get("items", []):
        if item.get("traceability_class") != "MATERIAL":
            continue
        ref = item.get("item_id")
        if not ref or ref in selected:
            continue
        item_type = item.get("type")
        if item_type == "REPRESENTATION":
            role = "DEPICTION"
        elif item_type == "CLAIM":
            role = "CONCEPT_INVARIANT"
        elif item_type == "CONDITION":
            role = "MODEL_BOUNDARY"
        elif item_type == "FORMAL_OBJECT":
            role = "BUILD_RELATION"
        elif item_type == "WORKED_REASONING":
            role = "WORKED_EXAMPLE" if profile in {"FOUNDATION", "BRIDGE"} else "WHY_THIS_WORKS"
        else:
            role = "CONCEPT_INVARIANT"
        by_role.setdefault(role, []).append(ref)

    for role, refs in by_role.items():
        _insert_step(unit, role, refs, state if role != "INDEPENDENT_TRANSFER" else "INDEPENDENT")


def _auto_structure(model: dict, plan: dict) -> dict:
    structure = _ORIG_AUTO(model, plan)
    sections = {sec["section_id"]: sec for sec in model.get("main_sections", [])}
    for unit in structure["study_guide"]["learning_units"]:
        sec = sections.get(unit["unit_id"])
        if not sec:
            continue

        rep_refs = [
            item["item_id"] for item in sec.get("items", [])
            if item.get("type") == "REPRESENTATION" and item.get("representation_instance_id")
        ]
        if rep_refs:
            _insert_step(
                unit,
                "DEPICTION",
                rep_refs,
                "FULL" if unit["instructional_profile"] in {"FOUNDATION", "BRIDGE"} else "REFERENCE",
            )

        _complete_material_selection(unit, sec)

    # PageIntent is the exact executable projection of each learning-unit arc.
    pages = []
    for unit in structure["study_guide"]["learning_units"]:
        refs = [ref for step in unit["arc_steps"] for ref in step["content_refs"]]
        pages.append({
            "page_intent_id": f"PI-{unit['unit_id']}",
            "cognitive_job": unit["cognitive_job"],
            "content_refs": refs,
            "layout_relation": "REPRESENTATION_VS_REASONING" if any(step["role"] == "DEPICTION" for step in unit["arc_steps"]) else "SINGLE_FLOW",
        })
    structure["study_guide"]["page_intents"] = pages
    return structure


def main() -> int:
    patch2._auto_structure = _auto_structure
    return patch3.main()


if __name__ == "__main__":
    raise SystemExit(main())
