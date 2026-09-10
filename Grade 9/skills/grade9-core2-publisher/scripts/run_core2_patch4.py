#!/usr/bin/env python3
"""Representation-complete auto PublicationStructure projection.

Every RepresentationInstance selected by the PublicationPlan must travel through
an executable DEPICTION arc step. This preserves legacy replay coverage while
keeping the structure renderer authoritative for ordering.
"""
from __future__ import annotations

import run_core2_patch3 as patch3

patch2 = patch3.patch2
impl = patch3.impl
_ORIG_AUTO = patch2._auto_structure


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
        if not rep_refs:
            continue
        depiction = next((step for step in unit["arc_steps"] if step["role"] == "DEPICTION"), None)
        if depiction is None:
            insert_at = next((i for i, step in enumerate(unit["arc_steps"]) if step["role"] in {"NOTICE", "SAY_IN_WORDS", "BUILD_RELATION"}), 0)
            depiction = {
                "step_id": f"{unit['unit_id']}-REP",
                "role": "DEPICTION",
                "content_refs": [],
                "support_state": "FULL" if unit["instructional_profile"] in {"FOUNDATION", "BRIDGE"} else "REFERENCE",
            }
            unit["arc_steps"].insert(insert_at, depiction)
        for ref in rep_refs:
            if ref not in depiction["content_refs"]:
                depiction["content_refs"].append(ref)

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
