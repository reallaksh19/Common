#!/usr/bin/env python3
"""Compatibility patch for executable PublicationStructure auto-generation.

The initial executable layer correctly rejected ambiguous content ownership, but
legacy replay sections can legitimately reuse one verified claim in more than
one pedagogical role. For executable rendering, clone the material item with a
new publication-item ID so every arc role has a unique content_ref while the
same Core (1) research_refs are preserved.
"""
from __future__ import annotations

import copy

import run_core2_structured_impl as impl

_ORIG_AUTO = impl._auto_structure


def _find_item_container(model: dict, item_id: str):
    for sec in model.get("main_sections", []):
        for item in sec.get("items", []):
            if item.get("item_id") == item_id:
                return sec["items"], item
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        for item in model.get(key, {}).get("items", []):
            if item.get("item_id") == item_id:
                return model[key]["items"], item
    return None, None


def _auto_structure(model: dict, plan: dict) -> dict:
    structure = _ORIG_AUTO(model, plan)
    seen = set()
    for unit in structure["study_guide"]["learning_units"]:
        for step in unit["arc_steps"]:
            new_refs = []
            for ref in step["content_refs"]:
                if ref not in seen:
                    seen.add(ref)
                    new_refs.append(ref)
                    continue
                container, item = _find_item_container(model, ref)
                if container is None or item is None:
                    new_refs.append(ref)
                    continue
                clone = copy.deepcopy(item)
                clone_id = f"{ref}-ARC-{step['step_id']}"
                clone["item_id"] = clone_id
                container.append(clone)
                seen.add(clone_id)
                new_refs.append(clone_id)
            step["content_refs"] = new_refs

    # PageIntent is an executable projection of the arc. Keep exact order and
    # one cognitive job per learning unit for legacy auto-generated products.
    pages = []
    for unit in structure["study_guide"]["learning_units"]:
        refs = [ref for step in unit["arc_steps"] for ref in step["content_refs"]]
        has_rep = any(step["role"] == "DEPICTION" for step in unit["arc_steps"])
        pages.append({
            "page_intent_id": f"PI-{unit['unit_id']}",
            "cognitive_job": unit["cognitive_job"],
            "content_refs": refs,
            "layout_relation": "REPRESENTATION_VS_REASONING" if has_rep else "SINGLE_FLOW",
        })
    structure["study_guide"]["page_intents"] = pages
    return structure


def main() -> int:
    impl._auto_structure = _auto_structure
    return impl.main()


if __name__ == "__main__":
    raise SystemExit(main())
