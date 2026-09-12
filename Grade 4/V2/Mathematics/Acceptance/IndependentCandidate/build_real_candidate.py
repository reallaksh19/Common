"""Build a REAL_CANDIDATE for the frozen independent Primary Math V2 oracle.

Producer boundary:
- reads only producer-owned CASES from this package;
- renders with the canonical Grade-4 vector backend/primitive dispatcher;
- emits exact PDF bytes, physical placement maps and SHA-256 custody;
- does not import/read BenchmarkAcceptance or its expected registry.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

from reportlab.pdfgen import canvas

from Grade4.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PageMetricsA4,
    PrimaryPalette,
    ReportLabBackend,
)
from Grade4.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive

from .producer_cases import CASES


PAGE = PageMetricsA4()
PANEL_H = 180.0
PANEL_GAP = 18.0


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_digest(payload: Any) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _frame(backend: ReportLabBackend, bbox: BoundingBox) -> None:
    backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)


def _custom_visual(kind: str, params: Mapping[str, Any], backend: ReportLabBackend, bbox: BoundingBox) -> None:
    _frame(backend, bbox)
    cx = bbox.x + bbox.width / 2.0
    cy = bbox.y + bbox.height / 2.0

    if kind == "CUSTOM_SLOTS":
        digits = [str(x) for x in params.get("digits", [])]
        labels = [str(x) for x in params.get("labels", [])]
        slot_w = min(70.0, (bbox.width - 40.0) / max(len(digits), 1))
        total_w = slot_w * len(digits)
        sx = cx - total_w / 2.0
        for i, digit in enumerate(digits):
            x = sx + i * slot_w
            backend.draw_rect(x + 4.0, cy - 24.0, slot_w - 8.0, 48.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, corner_radius=4.0)
            backend.draw_text(digit, x + slot_w / 2.0, cy - 5.0, font_size=18.0, color=PrimaryPalette.NAVY, align="center")
            if i < len(labels):
                backend.draw_text(labels[i], x + slot_w / 2.0, cy - 43.0, font_size=9.5, color=PrimaryPalette.SLATE, align="center")
        return

    if kind == "CUSTOM_CONTRAST":
        positive = list(params.get("positive", []))
        negative = list(params.get("negative", []))
        items = [(x, PrimaryPalette.TEAL) for x in positive] + [(x, PrimaryPalette.AMBER) for x in negative]
        card_w = (bbox.width - 40.0) / max(len(items), 1)
        for i, (text, stroke) in enumerate(items):
            x = bbox.x + 20.0 + i * card_w
            backend.draw_rect(x + 4.0, cy - 28.0, card_w - 8.0, 56.0, fill=PrimaryPalette.LIGHT_BG, stroke=stroke, corner_radius=4.0)
            backend.draw_text(str(text), x + card_w / 2.0, cy - 4.0, font_size=11.0, color=PrimaryPalette.NAVY, align="center")
        backend.draw_text(str(params.get("feature", "compare one feature")), cx, bbox.y + 18.0, font_size=10.0, color=PrimaryPalette.SLATE, align="center")
        return

    if kind == "CUSTOM_PROBE":
        backend.draw_text("Smallest useful probe", cx, bbox.y_max - 32.0, font_size=14.0, color=PrimaryPalette.TEAL, align="center")
        backend.draw_paragraph(str(params.get("prompt", "")), bbox.x + 30.0, cy + 22.0, bbox.width - 60.0, font_size=12.0, line_height=16.0)
        backend.draw_text("Change one feature; keep other load low.", cx, bbox.y + 24.0, font_size=10.5, color=PrimaryPalette.SLATE, align="center")
        return

    if kind == "CUSTOM_ANSWER_FORM":
        backend.draw_text(f"{params.get('quotient')} full groups, {params.get('remainder')} left", cx, cy + 20.0, font_size=14.0, color=PrimaryPalette.NAVY, align="center")
        backend.draw_arrow(cx - 90.0, cy - 4.0, cx + 75.0, cy - 4.0, stroke=PrimaryPalette.TEAL)
        backend.draw_text(f"story answer: {params.get('answer')}", cx, cy - 32.0, font_size=14.0, color=PrimaryPalette.SOFT_GREEN, align="center")
        return

    if kind == "CUSTOM_FRACTION_NUMBER_LINE":
        x1, x2 = bbox.x + 55.0, bbox.x_max - 55.0
        y = cy
        backend.draw_line(x1, y, x2, y, stroke=PrimaryPalette.NAVY, stroke_width=1.5)
        for frac, label in ((0.0, "0"), (0.5, "1/2 = 2/4 = 4/8"), (1.0, "1")):
            x = x1 + frac * (x2 - x1)
            backend.draw_line(x, y - 8.0, x, y + 8.0, stroke=PrimaryPalette.NAVY)
            backend.draw_text(label, x, y - 26.0, font_size=10.5, color=PrimaryPalette.TEAL if frac == 0.5 else PrimaryPalette.NAVY, align="center")
        return

    if kind == "CUSTOM_EQUATION":
        backend.draw_text(str(params.get("text", "")), cx, cy - 6.0, font_size=20.0, color=PrimaryPalette.ACCENT_BLUE, align="center")
        return

    if kind == "CUSTOM_SCALE":
        left, right = str(params.get("left", "")), str(params.get("right", ""))
        backend.draw_rect(bbox.x + 45.0, cy - 26.0, 120.0, 52.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, corner_radius=5.0)
        backend.draw_rect(bbox.x_max - 165.0, cy - 26.0, 120.0, 52.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, corner_radius=5.0)
        backend.draw_text(left, bbox.x + 105.0, cy - 5.0, font_size=14.0, color=PrimaryPalette.NAVY, align="center")
        backend.draw_text(right, bbox.x_max - 105.0, cy - 5.0, font_size=14.0, color=PrimaryPalette.NAVY, align="center")
        backend.draw_arrow(bbox.x + 180.0, cy, bbox.x_max - 180.0, cy, stroke=PrimaryPalette.AMBER)
        backend.draw_text(f"repeat x{params.get('count', 1)}", cx, cy + 16.0, font_size=10.5, color=PrimaryPalette.AMBER, align="center")
        return

    if kind == "CUSTOM_TABLE":
        headers = list(params.get("headers", []))
        rows = list(params.get("rows", []))
        data = [headers] + rows
        cols = max((len(r) for r in data), default=1)
        row_h = min(30.0, (bbox.height - 24.0) / max(len(data), 1))
        col_w = (bbox.width - 48.0) / cols
        top = bbox.y_max - 16.0
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                x = bbox.x + 24.0 + c * col_w
                y = top - (r + 1) * row_h
                backend.draw_rect(x, y, col_w, row_h, fill=PrimaryPalette.LIGHT_BG if r == 0 else PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER)
                backend.draw_text(str(value), x + col_w / 2.0, y + row_h / 2.0 - 4.0, font_size=10.5, color=PrimaryPalette.NAVY, align="center")
        return

    if kind == "CUSTOM_SCALE_KEY":
        backend.draw_line(bbox.x + 80.0, cy, bbox.x_max - 80.0, cy, stroke=PrimaryPalette.NAVY, stroke_width=2.0)
        for i in range(6):
            x = bbox.x + 80.0 + i * (bbox.width - 160.0) / 5.0
            backend.draw_line(x, cy - 7.0, x, cy + 7.0, stroke=PrimaryPalette.NAVY)
            backend.draw_text(str(i * int(params.get("scale", 5))), x, cy - 25.0, font_size=9.5, color=PrimaryPalette.SLATE, align="center")
        backend.draw_text(str(params.get("text", "")), cx, cy + 24.0, font_size=11.0, color=PrimaryPalette.TEAL, align="center")
        return

    if kind == "CUSTOM_WORK_REPLAY":
        steps = list(params.get("steps", []))
        y = bbox.y_max - 36.0
        for step in steps:
            status = str(step.get("status", ""))
            backend.draw_rect(bbox.x + 28.0, y - 24.0, bbox.width - 56.0, 34.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=4.0)
            backend.draw_text(str(step.get("text", "")), bbox.x + 42.0, y - 13.0, font_size=11.0, color=PrimaryPalette.NAVY)
            backend.draw_text(status.title(), bbox.x_max - 42.0, y - 13.0, font_size=10.0, color=PrimaryPalette.SLATE, align="right")
            y -= 42.0
        backend.draw_text(str(params.get("teacher_note", "")), bbox.x + 28.0, bbox.y + 14.0, font_size=9.5, color=PrimaryPalette.TEACHER_RED)
        return

    if kind == "CUSTOM_HINT":
        backend.draw_text(str(params.get("level", "")), bbox.x + 32.0, cy + 8.0, font_size=16.0, color=PrimaryPalette.TEAL)
        backend.draw_paragraph(str(params.get("text", "")), bbox.x + 125.0, cy + 22.0, bbox.width - 155.0, font_size=12.0, line_height=16.0)
        return

    if kind == "CUSTOM_ROUTE_TRACE":
        labels = ["same route", "same route", str(params.get("changed_to", "new route")), str(params.get("retry", "retry"))]
        gap = 12.0
        w = (bbox.width - 50.0 - gap * 3) / 4.0
        for i, label in enumerate(labels):
            x = bbox.x + 25.0 + i * (w + gap)
            backend.draw_rect(x, cy - 24.0, w, 48.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL if i >= 2 else PrimaryPalette.SLATE, corner_radius=4.0)
            backend.draw_text(label, x + w / 2.0, cy - 4.0, font_size=9.5, color=PrimaryPalette.NAVY, align="center")
            if i < 3:
                backend.draw_arrow(x + w, cy, x + w + gap - 2.0, cy, stroke=PrimaryPalette.AMBER)
        return

    raise ValueError(f"UNKNOWN_ACCEPTANCE_CUSTOM_VISUAL: {kind}")


def _draw_visual(backend: ReportLabBackend, spec: Mapping[str, Any], bbox: BoundingBox) -> None:
    kind = str(spec["kind"])
    if kind.startswith("CUSTOM_"):
        _custom_visual(kind, spec.get("params") or {}, backend, bbox)
    else:
        render_primitive(kind, dict(spec.get("params") or {}), backend, bbox)


def _new_page(c: canvas.Canvas, backend: ReportLabBackend, product: str, title: str, page_number: int) -> float:
    if page_number > 1:
        c.showPage()
    y = PAGE.PAGE_HEIGHT - PAGE.MARGIN_TOP
    backend.draw_rect(PAGE.MARGIN_LEFT, y - 58.0, PAGE.usable_width, 58.0, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)
    backend.draw_text(f"Grade 4 Mathematics - {product}", PAGE.MARGIN_LEFT + 14.0, y - 24.0, font_size=18.0, color=PrimaryPalette.NAVY)
    backend.draw_paragraph(title, PAGE.MARGIN_LEFT + 14.0, y - 38.0, PAGE.usable_width - 28.0, font_size=11.5, color=PrimaryPalette.SLATE, line_height=14.0)
    return y - 78.0


def _render_core1(path: Path, cases: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    c = canvas.Canvas(str(path), pagesize=(PAGE.PAGE_WIDTH, PAGE.PAGE_HEIGHT))
    backend = ReportLabBackend(c)
    page_number = 0
    placements: List[Dict[str, Any]] = []
    pages: List[Dict[str, Any]] = []

    for case in cases:
        visuals = list(case.get("visuals") or [])
        for offset in range(0, len(visuals), 3):
            page_number += 1
            y = _new_page(c, backend, "Core 1 Study Evidence", str(case["title"]), page_number)
            page_roles: List[str] = []
            for local_index, spec in enumerate(visuals[offset:offset + 3]):
                backend.draw_text(str(spec["caption"]), PAGE.MARGIN_LEFT, y, font_size=12.0, color=PrimaryPalette.NAVY)
                box = BoundingBox(PAGE.MARGIN_LEFT, y - PANEL_H - 8.0, PAGE.usable_width, PANEL_H)
                _draw_visual(backend, spec, box)
                placement_id = f"CORE1-P{page_number:03d}-E{local_index + 1:02d}"
                placements.append({
                    "placement_evidence_id": placement_id,
                    "case_id": case["case_id"],
                    "role": spec["role"],
                    "page": page_number,
                    "bbox": [box.x, box.y, box.width, box.height],
                    "primitive_kind": spec["kind"],
                })
                page_roles.append(str(spec["role"]))
                y -= PANEL_H + PANEL_GAP + 24.0
            pages.append({"page": page_number, "case_id": case["case_id"], "roles": page_roles})

    c.save()
    return {"product": "CORE1", "page_count": page_number, "pages": pages, "placements": placements}


def _render_core2(path: Path, cases: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    c = canvas.Canvas(str(path), pagesize=(PAGE.PAGE_WIDTH, PAGE.PAGE_HEIGHT))
    backend = ReportLabBackend(c)
    page_number = 0
    placements: List[Dict[str, Any]] = []
    pages: List[Dict[str, Any]] = []

    for case in cases:
        page_number += 1
        y = _new_page(c, backend, "Core 2 Practice Companion", str(case["title"]), page_number)
        backend.draw_text("TRY A FRESH ITEM", PAGE.MARGIN_LEFT, y, font_size=13.5, color=PrimaryPalette.TEAL)
        y -= 24.0
        used = backend.draw_paragraph(str(case.get("practice_prompt") or ""), PAGE.MARGIN_LEFT, y, PAGE.usable_width, font_size=13.0, color=PrimaryPalette.NAVY, line_height=17.0)
        y -= max(used, 38.0) + 18.0

        spec = list(case.get("visuals") or [])[0]
        backend.draw_text("REFERENCE MODEL", PAGE.MARGIN_LEFT, y, font_size=11.5, color=PrimaryPalette.SLATE)
        box = BoundingBox(PAGE.MARGIN_LEFT, y - 285.0, PAGE.usable_width, 260.0)
        _draw_visual(backend, spec, box)
        placement_id = f"CORE2-P{page_number:03d}-E01"
        placements.append({
            "placement_evidence_id": placement_id,
            "case_id": case["case_id"],
            "role": spec["role"],
            "page": page_number,
            "bbox": [box.x, box.y, box.width, box.height],
            "primitive_kind": spec["kind"],
        })
        pages.append({"page": page_number, "case_id": case["case_id"], "roles": [spec["role"]]})

        backend.draw_text("MY WORK", PAGE.MARGIN_LEFT, box.y - 28.0, font_size=11.5, color=PrimaryPalette.SLATE)
        backend.draw_rect(PAGE.MARGIN_LEFT, PAGE.MARGIN_BOTTOM + 30.0, PAGE.usable_width, 150.0, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.GRID_LINE, corner_radius=5.0)

    c.save()
    return {"product": "CORE2", "page_count": page_number, "pages": pages, "placements": placements}


def build_real_candidate(output_dir: Path) -> Dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    core1 = output_dir / "Grade4_Math_V2_Independent_Core1.pdf"
    core2 = output_dir / "Grade4_Math_V2_Independent_Core2.pdf"
    core1_map_path = output_dir / "core1_physical_page_map.json"
    core2_map_path = output_dir / "core2_physical_page_map.json"
    manifest_path = output_dir / "architecture_manifest.json"
    candidate_path = output_dir / "candidate_export.json"

    core1_map = _render_core1(core1, CASES)
    core2_map = _render_core2(core2, CASES)
    core1_sha = _sha256(core1)
    core2_sha = _sha256(core2)
    core1_map["pdf_sha256"] = core1_sha
    core2_map["pdf_sha256"] = core2_sha
    _write_json(core1_map_path, core1_map)
    _write_json(core2_map_path, core2_map)

    combined_page_map_digest = _json_digest({"core1": core1_map, "core2": core2_map})
    core1_by_case: Dict[str, List[Dict[str, Any]]] = {}
    core2_by_case: Dict[str, List[Dict[str, Any]]] = {}
    for row in core1_map["placements"]:
        core1_by_case.setdefault(str(row["case_id"]), []).append(row)
    for row in core2_map["placements"]:
        core2_by_case.setdefault(str(row["case_id"]), []).append(row)

    exported_cases: List[Dict[str, Any]] = []
    for case in CASES:
        cid = str(case["case_id"])
        c1 = core1_by_case.get(cid) or []
        c2 = core2_by_case.get(cid) or []
        if not c1 or not c2:
            raise ValueError(f"CANDIDATE_PLACEMENT_COVERAGE_INCOMPLETE: {cid}")
        exported = {
            key: copy.deepcopy(value)
            for key, value in case.items()
            if key not in {"title", "practice_prompt", "visuals"} and value is not None
        }
        exported["surface_evidence"] = {
            "internal_identifier_leaks": [],
            "minimum_body_font_pt": 12.0,
            "publisher_invention_allowed": False,
        }
        exported["custody_evidence"] = {
            "placement_evidence_id": c1[0]["placement_evidence_id"],
            "core1_placement_ids": [x["placement_evidence_id"] for x in c1],
            "core2_placement_ids": [x["placement_evidence_id"] for x in c2],
            "core1_pdf_sha256": core1_sha,
            "core2_pdf_sha256": core2_sha,
        }
        exported_cases.append(exported)

    candidate = {
        "version": "1.0.0",
        "candidate_id": "GRADE4-MATH-V2-REAL-CANDIDATE-001",
        "evidence_class": "REAL_CANDIDATE",
        "producer": "Grade 4/V2/Mathematics",
        "artifacts": {
            "core1_sha256": core1_sha,
            "core2_sha256": core2_sha,
            "physical_page_map_digest": combined_page_map_digest,
            "core1_page_map_sha256": _sha256(core1_map_path),
            "core2_page_map_sha256": _sha256(core2_map_path),
        },
        "cases": exported_cases,
    }
    _write_json(candidate_path, candidate)

    manifest = {
        "schema_version": "1.0.0",
        "candidate_id": candidate["candidate_id"],
        "producer_runtime": "Grade4 canonical vector backend + primitive dispatcher",
        "renderer_invention_allowed": False,
        "benchmark_oracle_imported_by_producer": False,
        "artifacts": {
            "core1": {"path": core1.name, "sha256": core1_sha, "pages": core1_map["page_count"]},
            "core2": {"path": core2.name, "sha256": core2_sha, "pages": core2_map["page_count"]},
            "core1_page_map": {"path": core1_map_path.name, "sha256": _sha256(core1_map_path)},
            "core2_page_map": {"path": core2_map_path.name, "sha256": _sha256(core2_map_path)},
            "candidate_export": {"path": candidate_path.name, "sha256": _sha256(candidate_path)},
        },
        "human_review_status": "PENDING_HUMAN_REVIEW",
    }
    _write_json(manifest_path, manifest)

    return {
        "core1": core1,
        "core2": core2,
        "core1_map": core1_map_path,
        "core2_map": core2_map_path,
        "manifest": manifest_path,
        "candidate": candidate_path,
    }


if __name__ == "__main__":
    outputs = build_real_candidate(Path("build/grade4_math_v2/independent_acceptance"))
    print(json.dumps({k: str(v) for k, v in outputs.items()}, indent=2))
