#!/usr/bin/env python3
"""Physical page custody and morphology checks for Core (2) learner PDFs."""
from __future__ import annotations


def custody_errors(page_map: dict) -> list[str]:
    """Hard reconciliation failures: logical content cannot be lost or mis-bound."""
    errors: list[str] = []
    count = page_map.get("physical_page_count", 0)
    intents = page_map.get("page_intents", [])
    intent_by_id = {row.get("page_intent_id"): row for row in intents}

    if len(intent_by_id) != len(intents):
        errors.append("duplicate page_intent_id in PhysicalPageMap")

    for iid, row in intent_by_id.items():
        pages = row.get("physical_pages", [])
        if any(p < 1 or p > count for p in pages):
            errors.append(f"{iid}: physical page outside declared page count")
        continuations = set(row.get("continuation_pages", []))
        if continuations - set(pages):
            errors.append(f"{iid}: continuation page is not part of physical_pages")
        if row.get("pagination_policy") == "FORCE_SINGLE_PAGE" and len(pages) != 1:
            errors.append(f"{iid}: FORCE_SINGLE_PAGE mapped to {len(pages)} pages")
        max_pages = row.get("max_physical_pages")
        if max_pages is not None and len(pages) > max_pages:
            errors.append(f"{iid}: exceeds max_physical_pages={max_pages}")
        if row.get("split") is False and len(pages) > 1:
            errors.append(f"{iid}: multiple physical pages but split=false")

    placements = page_map.get("content_placements", [])
    placed_refs: set[tuple[str, str]] = set()
    for placement in placements:
        iid = placement.get("page_intent_id")
        ref = placement.get("content_ref")
        key = (iid, ref)
        if key in placed_refs:
            errors.append(f"{iid}:{ref}: duplicate content placement")
        placed_refs.add(key)
        intent = intent_by_id.get(iid)
        if not intent:
            errors.append(f"{ref}: content placement references unknown page intent {iid}")
            continue
        if ref not in intent.get("content_refs", []):
            errors.append(f"{iid}:{ref}: placement is not declared by page intent")
        if set(placement.get("physical_pages", [])) - set(intent.get("physical_pages", [])):
            errors.append(f"{iid}:{ref}: content placement escapes page-intent physical range")
        fragment_pages = {f.get("page") for f in placement.get("fragments", [])}
        if fragment_pages != set(placement.get("physical_pages", [])):
            errors.append(f"{iid}:{ref}: fragment pages do not reconcile to content physical_pages")

    for iid, intent in intent_by_id.items():
        for ref in intent.get("content_refs", []):
            if (iid, ref) not in placed_refs:
                errors.append(f"{iid}:{ref}: declared page-intent content has no physical placement")

    metrics = page_map.get("page_metrics", [])
    metric_pages = [m.get("page") for m in metrics]
    if metric_pages != list(range(1, count + 1)):
        errors.append("page_metrics must cover physical pages exactly once in order")
    return errors


def morphology_errors(page_map: dict) -> list[str]:
    """Layout-quality findings. These are independently promotable release gates."""
    errors: list[str] = []
    for metric in page_map.get("page_metrics", []):
        page = metric.get("page")
        if metric.get("orphan_continuation") is True:
            errors.append(f"page {page}: orphan continuation")
        if metric.get("underfill_disposition") == "PATHOLOGICAL":
            errors.append(f"page {page}: pathological underfill")
    return errors


def reconciliation_errors(page_map: dict) -> list[str]:
    return custody_errors(page_map) + morphology_errors(page_map)
