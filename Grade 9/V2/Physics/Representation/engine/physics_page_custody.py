#!/usr/bin/env python3
"""Physical-page custody and morphology checks for Physics learner PDFs.

Ported from the `PhysicalPageMap` custody mechanism proved in draft PR #161 /
PR #196 and adapted to the P-H representation bundle. The governing rule is
unchanged: **planned page numbers are not physical evidence**. A placement is
only admissible if the renderer emitted it while it was actually drawing, and
every declared page-intent content ref must reconcile to such a placement.
"""


def custody_errors(page_map):
    """Hard reconciliation failures: logical content cannot be lost or mis-bound."""
    errors = []
    count = page_map.get("physical_page_count", 0)
    intents = page_map.get("page_intents", [])
    intent_by_id = {row.get("page_intent_id"): row for row in intents}

    if len(intent_by_id) != len(intents):
        errors.append("duplicate page_intent_id in PhysicalPageMap")
    if page_map.get("actual_placement_evidence") is not True:
        errors.append("planned placement is not physical evidence")

    for iid, row in intent_by_id.items():
        pages = row.get("physical_pages", [])
        if any(p < 1 or p > count for p in pages):
            errors.append(f"{iid}: physical page outside declared page count")
        continuations = set(row.get("continuation_pages", []))
        if continuations - set(pages):
            errors.append(f"{iid}: continuation page is not part of physical_pages")
        if row.get("split") is False and len(pages) > 1:
            errors.append(f"{iid}: multiple physical pages but split=false")

    placements = page_map.get("content_placements", [])
    placed = set()
    for placement in placements:
        iid = placement.get("page_intent_id")
        ref = placement.get("content_ref")
        key = (iid, ref)
        if key in placed:
            errors.append(f"{iid}:{ref}: duplicate content placement")
        placed.add(key)
        intent = intent_by_id.get(iid)
        if not intent:
            errors.append(f"{ref}: content placement references unknown page intent {iid}")
            continue
        if ref not in intent.get("content_refs", []):
            errors.append(f"{iid}:{ref}: placement is not declared by page intent")
        if placement.get("page") not in intent.get("physical_pages", []):
            errors.append(f"{iid}:{ref}: content placement escapes page-intent physical range")
        if placement.get("fragment_kind") == "CONTINUATION":
            if placement.get("page") not in intent.get("continuation_pages", []) or not intent.get("split"):
                errors.append(f"{iid}:{ref}: orphan continuation")

    for iid, intent in intent_by_id.items():
        for ref in intent.get("content_refs", []):
            if (iid, ref) not in placed:
                errors.append(f"{iid}:{ref}: declared page-intent content has no physical placement")

    metrics = page_map.get("page_metrics", [])
    if [m.get("page") for m in metrics] != list(range(1, count + 1)):
        errors.append("page_metrics must cover physical pages exactly once in order")
    return errors


def bounds_errors(page_map, page_width, page_height, tolerance=0.0):
    """Every placement and its measured ink must sit inside the physical page."""
    errors = []
    for p in page_map.get("content_placements", []):
        ref = p.get("content_ref")
        if not (0 <= p["x0"] < p["x1"] <= page_width and 0 <= p["y0"] < p["y1"] <= page_height):
            errors.append(f"{ref}: allocated box outside physical page")
        ink = p.get("ink_bbox")
        if not ink:
            errors.append(f"{ref}: no measured ink box")
            continue
        if not (0 <= ink["x0"] and ink["x1"] <= page_width and 0 <= ink["y0"] and ink["y1"] <= page_height):
            errors.append(f"{ref}: measured ink escapes the physical page")
        if not (p["x0"] - tolerance <= ink["x0"] and ink["x1"] <= p["x1"] + tolerance
                and p["y0"] - tolerance <= ink["y0"] and ink["y1"] <= p["y1"] + tolerance):
            errors.append(f"{ref}: measured ink escapes its allocated box")
    return errors


def realization_errors(page_map, minimum_by_primitive):
    """The label-only defect: a primitive that drew no real vector graphics."""
    errors = []
    for p in page_map.get("content_placements", []):
        ref = p.get("content_ref")
        pid = p.get("primitive")
        floor = minimum_by_primitive.get(pid)
        if floor is None:
            errors.append(f"{ref}: primitive {pid} has no declared vector floor")
            continue
        if p.get("vector_ops", 0) < floor:
            errors.append(
                f"{ref}: {pid} drew {p.get('vector_ops', 0)} vector operations, below its floor of {floor}"
            )
        if p.get("vector_ops", 0) <= 0:
            errors.append(f"{ref}: {pid} is label-only, no vector graphics were emitted")
    return errors


def morphology_errors(page_map):
    """Layout-quality findings; independently promotable release gates."""
    errors = []
    for metric in page_map.get("page_metrics", []):
        page = metric.get("page")
        if metric.get("orphan_continuation") is True:
            errors.append(f"page {page}: orphan continuation")
        if metric.get("underfill_disposition") == "PATHOLOGICAL":
            errors.append(f"page {page}: pathological underfill")
        if metric.get("bounds_violations", 0):
            errors.append(f"page {page}: {metric['bounds_violations']} bounds violations")
    return errors


def reconciliation_errors(page_map, page_width, page_height, minimum_by_primitive, tolerance=0.0):
    return (
        custody_errors(page_map)
        + bounds_errors(page_map, page_width, page_height, tolerance)
        + realization_errors(page_map, minimum_by_primitive)
        + morphology_errors(page_map)
    )
