#!/usr/bin/env python3
"""Machine review-candidate gate for all four Chemistry Core product modes.

The thresholds come from current Blueprint product-quality authority. This layer does
not infer human approval; it only prevents a structurally valid engineering PDF from
being mislabeled review-ready when page architecture or semantic composition is weak.
"""
from __future__ import annotations

from typing import Any

A4_H = 841.89

# Must remain physically consistent with the shared ReviewWriter navigation contract.
# A dedicated renderer-level falsifier compares this map with ReviewWriter.ROLE_LABELS so
# drift between preflight and composition fails in CI rather than silently passing.
ROLE_NAV_LABELS = {
    "COVER": "START HERE",
    "ROUTE_OR_MAP": "ROUTE",
    "CONCEPT_EXPLANATION": "LEARN",
    "RULE_OR_DERIVATION": "BUILD THE RULE",
    "REPRESENTATION": "REPRESENT",
    "TTU_RECONSTRUCTION": "RECONSTRUCT",
    "WORKED_EXAMPLE": "WATCH ONE",
    "MISCONCEPTION_OR_BOUNDARY": "CHECK THE BOUNDARY",
    "PRACTICE": "PRACTISE",
    "QUESTION_EPISODE": "ATTEMPT",
    "WORKSPACE": "WORKSPACE",
    "SOLUTION": "CHECK",
    "SUMMARY_OR_HANDOUT": "REVIEW",
}


def review_candidate_checks(
    metrics: dict[str, Any],
    v5_policy: dict[str, Any],
    product_control: dict[str, Any],
    review_policy: dict[str, Any],
    product_mode: str,
) -> dict[str, Any]:
    failures: list[str] = []
    rows: list[dict[str, Any]] = []

    if metrics.get("composition_system") != "CHEMISTRY_REVIEW_GRADE_V1":
        failures.append("CHEM_REVIEW_PLAIN_DOCUMENT_LAYOUT")

    draw_ops = metrics.get("draw_ops")
    page_labels = metrics.get("page_labels")
    if not isinstance(draw_ops, list) or not isinstance(page_labels, list):
        return {
            "status": "FAIL",
            "maturity_state": review_policy["failure_status"],
            "page_checks": [],
            "failures": failures + ["CHEM_REVIEW_RENDER_TRACE_MISSING"],
        }

    architecture = v5_policy["page_architecture"]
    content_min = float(architecture["content_page_min_active_area_ratio"])
    workspace_min = float(architecture["workspace_page_min_active_area_ratio"])
    standard_roles = set(review_policy["standard_page_roles"])
    major_kinds = set(review_policy["major_semantic_surface_kinds"])
    minimum_major = int(review_policy["review_candidate_requirements"]["noncover_major_semantic_surface_min"])
    max_text_coverage = float(product_control["legibility_assurance"]["maximum_text_coverage_ratio"])

    margin = 42.0
    usable_height = A4_H - 2 * margin
    labels = {int(row["page"]): row for row in page_labels}
    by_page: dict[int, list[dict[str, Any]]] = {}
    for op in draw_ops:
        by_page.setdefault(int(op["page"]), []).append(op)

    document_kinds: set[str] = set()
    for page_no in range(1, int(metrics.get("page_count", 0)) + 1):
        label_row = labels.get(page_no, {})
        role = str(label_row.get("role") or "")
        if role not in standard_roles:
            failures.append(f"CHEM_REVIEW_PAGE_ROLE_INVALID:{page_no}:{role or 'MISSING'}")

        page_ops = by_page.get(page_no, [])
        nav_headers = [op for op in page_ops if op.get("kind") == "NAV_HEADER"]
        ops = [op for op in page_ops if op.get("kind") not in {"FOOTER", "NAV_HEADER"}]
        spans: list[tuple[float, float]] = []
        text_area = 0.0
        major = []
        for op in ops:
            x0, y0 = float(op.get("x0", 0)), float(op.get("y0", 0))
            x1, y1 = float(op.get("x1", 0)), float(op.get("y1", 0))
            cy0, cy1 = max(margin, y0), min(A4_H - margin, y1)
            if cy1 > cy0:
                spans.append((cy0, cy1))
            kind = str(op.get("kind") or "")
            document_kinds.add(kind)
            if kind == "TEXT":
                text_area += max(0.0, x1 - x0) * max(0.0, y1 - y0)
            if kind in major_kinds:
                major.append(kind)

        active_height = max((b for _, b in spans), default=margin) - min((a for a, _ in spans), default=margin)
        active_ratio = max(0.0, active_height / usable_height)
        # COVER is a physical first-page exemption, not a role that may be
        # inherited by continuations. Otherwise a sparse overflow page could
        # accidentally bypass the current Blueprint density authority.
        is_cover = page_no == 1
        is_workspace = role == "WORKSPACE"
        threshold = workspace_min if is_workspace else content_min
        page_failures: list[str] = []

        if len(nav_headers) != 1:
            page_failures.append("CHEM_REVIEW_NAV_HEADER_TRACE_INVALID")
        elif role in ROLE_NAV_LABELS:
            rendered_nav = str(nav_headers[0].get("text") or "")
            expected_nav = ROLE_NAV_LABELS[role]
            if rendered_nav != expected_nav:
                page_failures.append(
                    f"CHEM_REVIEW_PAGE_ROLE_NAV_MISMATCH:{rendered_nav or 'MISSING'}!={expected_nav}"
                )

        if page_no > 1 and role == "COVER":
            page_failures.append("CHEM_REVIEW_COVER_ROLE_AFTER_FIRST_PAGE")
        if not is_cover and active_ratio < threshold:
            page_failures.append(f"CHEM_REVIEW_UNJUSTIFIED_EMPTY_PAGE_AREA:{active_ratio:.4f}<{threshold:.4f}")
        if not is_cover and len(major) < minimum_major:
            page_failures.append("CHEM_REVIEW_MAJOR_SEMANTIC_SURFACE_MISSING")

        has_workspace = "WORKSPACE_PANEL" in major
        has_task_binding = "QUESTION_PANEL" in major or "ACTION_PANEL" in major
        if has_workspace and not has_task_binding:
            page_failures.append("CHEM_REVIEW_WORKSPACE_NOT_TASK_BOUND")

        usable_width = 595.276 - 2 * margin
        text_coverage = text_area / max(1.0, usable_width * usable_height)
        if text_coverage > max_text_coverage:
            page_failures.append(f"CHEM_REVIEW_TEXT_COVERAGE_EXCESSIVE:{text_coverage:.4f}>{max_text_coverage:.4f}")

        rows.append({
            "page": page_no,
            "label": str(label_row.get("label") or ""),
            "role": role,
            "active_height_ratio": round(active_ratio, 4),
            "minimum_active_height_ratio": 0.0 if is_cover else threshold,
            "major_surface_kinds": sorted(set(major)),
            "major_surface_count": len(major),
            "text_coverage_ratio": round(text_coverage, 4),
            "status": "PASS" if not page_failures else "FAIL",
            "failures": page_failures,
        })
        failures.extend(f"{item}:page={page_no}" for item in page_failures)

    required = set(review_policy["mode_required_surface_jobs"][product_mode])
    missing = sorted(required - document_kinds)
    if missing:
        failures.append("CHEM_REVIEW_MODE_SURFACE_JOBS_MISSING:" + ",".join(missing))

    return {
        "status": "PASS" if not failures else "FAIL",
        "maturity_state": review_policy["review_candidate_status"] if not failures else review_policy["failure_status"],
        "product_mode": product_mode,
        "content_page_min_active_area_ratio": content_min,
        "workspace_page_min_active_area_ratio": workspace_min,
        "required_surface_jobs": sorted(required),
        "realized_surface_jobs": sorted(document_kinds & major_kinds),
        "page_checks": rows,
        "failures": failures,
        "human_release_inferred": False,
    }
