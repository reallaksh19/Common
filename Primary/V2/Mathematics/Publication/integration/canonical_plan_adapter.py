"""Adapter from canonical PR #336 plans into the ready PR #327 page composer.

This module owns projection only. It does not infer scope, diagnose learners, or
invent practice content. Learner-facing prompts/hints must be supplied through an
explicit content-realization payload.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable, Mapping, Tuple


class ProjectionError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _index_by(items: Iterable[Mapping[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if not value or value in out:
            raise ProjectionError("PROJECTION_ID_INVALID", f"missing/duplicate {key}: {value}")
        out[str(value)] = dict(item)
    return out


def _concept_rep_context(reps: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    context: Dict[str, Any] = {}
    for rep in reps:
        kind = str(rep.get("primitive_kind", "")).upper()
        params = dict(rep.get("semantic_params") or {})
        if kind == "AREA_DISTRIBUTIVE":
            context["a"] = params.get("a")
            context["b"] = params.get("b")
            context["split"] = params.get("split")
            context["partial_products"] = params.get("partial_products")
            context["product"] = params.get("product")
        elif kind == "EQUAL_GROUPS":
            context.setdefault("a", params.get("items_per_group"))
            context.setdefault("b", params.get("group_count"))
        elif kind == "ARRAY":
            context.setdefault("a", params.get("columns", params.get("cols")))
            context.setdefault("b", params.get("rows"))
    return context


def _project_primitive(rep: Mapping[str, Any], context: Mapping[str, Any]) -> Dict[str, Any] | None:
    kind = str(rep.get("primitive_kind", "")).upper()
    params = dict(rep.get("semantic_params") or {})

    if kind == "EQUAL_GROUPS":
        return {"kind": "EQUAL_GROUPS", "params": params}
    if kind == "ARRAY":
        if "columns" in params and "cols" not in params:
            params["cols"] = params.pop("columns")
        return {"kind": "ARRAY", "params": params}
    if kind == "AREA_DISTRIBUTIVE":
        a, b = params.get("a"), params.get("b")
        split = list(params.get("split") or [])
        partials = list(params.get("partial_products") or [])
        if a is None or b is None or not split or len(split) != len(partials):
            raise ProjectionError("AREA_DISTRIBUTIVE_PROJECTION_INCOMPLETE", rep.get("representation_id", kind))
        partitions = [
            {"length": length, "height": b, "area": area}
            for length, area in zip(split, partials)
        ]
        return {"kind": "AREA_MODEL", "params": {"factors": [a, b], "partitions": partitions}}
    if kind == "PARTIAL_PRODUCTS":
        factors = params.get("factors")
        if not factors:
            a, b = context.get("a"), context.get("b")
            if a is None or b is None:
                raise ProjectionError("PARTIAL_PRODUCTS_FACTORS_UNGROUNDED", rep.get("representation_id", kind))
            factors = [a, b]
        return {"kind": "PARTIAL_PRODUCTS", "params": {
            "factors": factors,
            "partial_products": list(params.get("partial_products") or context.get("partial_products") or []),
            "product": params.get("product", context.get("product")),
        }}
    if kind == "VERTICAL_MULTIPLICATION":
        multiplicand = params.get("multiplicand", context.get("a"))
        multiplier = params.get("multiplier", context.get("b"))
        product = params.get("product", context.get("product"))
        partials = list(params.get("partial_products") or context.get("partial_products") or [])
        if multiplicand is None or multiplier is None or product is None or not partials:
            raise ProjectionError("WRITTEN_MULTIPLICATION_PROJECTION_INCOMPLETE", rep.get("representation_id", kind))
        return {"kind": "VERTICAL_MULTIPLICATION", "params": {
            "factors": [multiplicand, multiplier],
            "partial_products": partials,
            "total_product": product,
            "tier": "AUTHORED_NOTEBOOK_EXAMPLE",
        }}
    if kind in {"WRITTEN_DIVISION", "LONG_DIVISION_WORKOUT"}:
        quotient = params.get("quotient")
        if quotient is None:
            raise ProjectionError("WRITTEN_DIVISION_PROJECTION_INCOMPLETE", rep.get("representation_id", kind))
        projected = dict(params)
        projected.setdefault("quotient_digits", [int(ch) for ch in str(quotient)])
        projected.setdefault("provenance_tier", "AUTHORED_NOTEBOOK_EXAMPLE")
        projected.setdefault("actor", "SYSTEM")
        return {"kind": "LONG_DIVISION_WORKOUT", "params": projected}
    if kind == "FRACTION_STRIP":
        return {"kind": "FRACTION_STRIP", "params": params}
    if kind == "DECIMAL_HUNDRED_GRID":
        return {"kind": "DECIMAL_HUNDRED_GRID", "params": params}
    if kind == "DECIMAL_NUMBER_LINE":
        return {"kind": "DECIMAL_NUMBER_LINE", "params": params}
    if kind in {"PLACE_VALUE_BLOCKS", "MEASUREMENT_CONVERSION", "RECTILINEAR_PERIMETER_AREA", "VOLUME_CUBE_LAYERS", "GEOMETRIC_ANGLE", "DATA_BAR_CHART", "BAR_CHART", "DIVISION_SHARING_VS_GROUPING", "DIVISION_REMAINDER_CONTEXT", "UNIT_CHAIN"}:
        return {"kind": kind, "params": params}
    if kind in {"INVERSE_CHECK", "MULTIPLICATION_CHECK", "DIVISION_EQUATION", "QUANTITY_STRUCTURE_MAP", "EQUATION"}:
        return None

    raise ProjectionError("CANONICAL_PRIMITIVE_NOT_SUPPORTED_BY_PUBLISHER", f"{rep.get('representation_id')}: {kind}")


def adapt_authoring_result(
    authoring_result: Mapping[str, Any],
    content_realization: Mapping[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    skill_model = authoring_result.get("skill_model") or {}
    core1 = authoring_result.get("core1_plan") or {}
    core2 = authoring_result.get("core2_plan") or {}
    rep_plan = authoring_result.get("representation_plan") or {}
    concepts = _index_by(skill_model.get("concepts") or [], "concept_id")
    reps = _index_by(rep_plan.get("representations") or [], "representation_id")

    reps_by_concept: Dict[str, list[Dict[str, Any]]] = defaultdict(list)
    for rep in reps.values():
        reps_by_concept[str(rep.get("concept_ref"))].append(rep)

    pub = content_realization.get("publication_context") or {}
    if not pub.get("title") or not pub.get("topic") or not pub.get("grade_label"):
        raise ProjectionError("PUBLICATION_CONTEXT_REQUIRED", "title/topic/grade_label are required")

    core1_modules = []
    projection_trace = {"representation_projection": {}, "content_realization_refs": []}
    for module in core1.get("modules") or []:
        concept_ref = module.get("concept_ref")
        concept = concepts.get(str(concept_ref))
        if not concept:
            raise ProjectionError("CORE1_CONCEPT_REF_UNRESOLVED", str(concept_ref))
        concept_reps = reps_by_concept.get(str(concept_ref), [])
        context = _concept_rep_context(concept_reps)
        sections = [{
            "section_type": "NOTICE",
            "title": "Notice the relationship",
            "content": module.get("objective") or concept.get("title"),
        }]
        for rep in concept_reps:
            projected = _project_primitive(rep, context)
            rid = rep["representation_id"]
            if projected is None:
                expression = (rep.get("semantic_params") or {}).get("expression")
                sections.append({
                    "section_type": "CHECK",
                    "title": "Check",
                    "content": expression or "Check the result using the stated mathematical relationship.",
                })
                projection_trace["representation_projection"][rid] = "TEXT_CHECK_SECTION"
            else:
                sections.append({
                    "section_type": "MAKE_DRAW_REPRESENT",
                    "title": concept.get("title", "Representation"),
                    "content": "Use the model to connect the quantities and the calculation.",
                    "primitive_call": projected,
                })
                projection_trace["representation_projection"][rid] = projected["kind"]
        core1_modules.append({
            "module_id": module["module_id"],
            "title": concept.get("title", module["module_id"]),
            "sections": sections,
        })

    content_modules = dict(content_realization.get("core2_modules") or {})
    batches: Dict[str, Dict[str, Any]] = {}
    ladders = []
    for module in core2.get("modules") or []:
        mid = module["module_id"]
        content = content_modules.get(mid)
        if content is None:
            if module.get("concept_mode") == "PROBE":
                continue
            raise ProjectionError("CORE2_CONTENT_REALIZATION_MISSING", mid)
        projection_trace["content_realization_refs"].append(mid)
        role = module.get("practice_batch_type") or "BUILD"
        batch = batches.setdefault(role, {
            "batch_id": f"BATCH-{role}",
            "title": content.get("batch_title", role.title()),
            "practice_role": role,
            "items": [],
        })
        batch["items"].append({"item_id": content["item_id"], "prompt": content["prompt"]})
        ladder = content.get("hint_ladder")
        if ladder:
            ladders.append({"item_id": content["item_id"], **ladder})

    appendix_c = content_realization.get("appendix_c") or {}
    appendix_rep_id = appendix_c.get("representation_id")
    appendix_primitive = None
    if appendix_rep_id:
        rep = reps.get(appendix_rep_id)
        if not rep:
            raise ProjectionError("APPENDIX_C_REPRESENTATION_UNRESOLVED", appendix_rep_id)
        appendix_primitive = _project_primitive(rep, _concept_rep_context(reps_by_concept.get(str(rep.get("concept_ref")), [])))
        if appendix_primitive is None:
            raise ProjectionError("APPENDIX_C_REQUIRES_VISUAL_PRIMITIVE", appendix_rep_id)

    core1_render_plan = {
        "title": pub["title"],
        "topic": pub["topic"],
        "grade_level": pub["grade_label"],
        "modules": core1_modules,
    }
    core2_render_plan = {
        "companion_id": core2.get("plan_id", "PrimaryMathCore2Companion"),
        "linked_core1_id": core1.get("plan_id", "PrimaryMathCore1StudyPlan"),
        "appendix_a": {"batches": list(batches.values())},
        "appendix_b": {"ladders": ladders},
        "appendix_c": {
            "title": appendix_c.get("title", "Appendix C — Visual Quick Reference"),
            "decision_aid_name": appendix_c.get("decision_aid_name", "Visual decision aid"),
            "primitive_call": appendix_primitive,
        },
    }
    return core1_render_plan, core2_render_plan, projection_trace
