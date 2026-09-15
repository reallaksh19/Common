#!/usr/bin/env python3
"""Dependency-free content-first pagination checks for unified Chemistry A products."""
from __future__ import annotations

from typing import Any

A4_H = 841.89


def content_first_page_checks(
    metrics: dict[str, Any],
    policy: dict[str, Any],
    product_mode: str,
) -> dict[str, Any]:
    cfg = policy.get("preflight", {}).get("content_first_pagination", {})
    products = set(cfg.get("products") or [])
    if product_mode not in products:
        return {"status": "NOT_APPLICABLE", "page_checks": [], "failures": []}

    failures: list[str] = []
    if metrics.get("pagination_mode") != "CONTENT_FIRST":
        failures.append("CHEM_CORE_PREFLIGHT_CONTENT_FIRST_MODE_MISSING")

    draw_ops = metrics.get("draw_ops")
    page_labels = metrics.get("page_labels")
    if not isinstance(draw_ops, list) or not isinstance(page_labels, list):
        failures.append("CHEM_CORE_PREFLIGHT_CONTENT_TRACE_MISSING")
        return {"status": "FAIL", "page_checks": [], "failures": failures}

    margin = float(policy["page"]["margin_pt"])
    usable_height = A4_H - 2.0 * margin
    threshold = float(cfg["minimum_noncover_active_height_ratio"])
    cover_exempt = bool(cfg.get("cover_page_exempt", True))
    labels = {int(row["page"]): str(row.get("label", "")) for row in page_labels}
    by_page: dict[int, list[dict[str, Any]]] = {}
    for op in draw_ops:
        by_page.setdefault(int(op["page"]), []).append(op)

    rows: list[dict[str, Any]] = []
    for page_no in range(1, int(metrics.get("page_count", 0)) + 1):
        ops = [row for row in by_page.get(page_no, []) if row.get("kind") != "FOOTER"]
        clipped: list[tuple[float, float]] = []
        for op in ops:
            y0 = max(margin, float(op.get("y0", margin)))
            y1 = min(A4_H - margin, float(op.get("y1", A4_H - margin)))
            if y1 > y0:
                clipped.append((y0, y1))
        active_height = max((span[1] for span in clipped), default=margin) - min((span[0] for span in clipped), default=margin)
        ratio = max(0.0, active_height / usable_height)
        semantic_refs = sorted({str(op.get("content_ref")) for op in ops if op.get("content_ref")})
        row = {
            "page": page_no,
            "label": labels.get(page_no, ""),
            "active_height_ratio": round(ratio, 4),
            "semantic_ref_count": len(semantic_refs),
            "has_workspace": any(op.get("kind") == "WORKSPACE_LINE" for op in ops),
            "has_primitive": any(op.get("kind") == "PRIMITIVE" for op in ops),
        }
        sparse = ratio < threshold and not (cover_exempt and page_no == 1)
        row["content_first_status"] = "FAIL" if sparse else "PASS"
        rows.append(row)
        if sparse:
            failures.append(
                f"CHEM_LP_RENDER_SPARSE_SEMANTIC_FRAGMENT:{page_no}:{ratio:.4f}<{threshold:.4f}:{row['label']}"
            )

    return {
        "status": "PASS" if not failures else "FAIL",
        "minimum_noncover_active_height_ratio": threshold,
        "page_checks": rows,
        "failures": failures,
    }
