#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import fitz

ROOT = Path(__file__).resolve().parents[1]


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def digest_without_field(value: dict[str, Any], field: str) -> str:
    clone = dict(value)
    clone.pop(field, None)
    return digest(clone)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text_spans(page: fitz.Page):
    for block in page.get_text("dict").get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                yield span


def _bbox_inside(bbox, rect: fitz.Rect, tol: float = 0.5) -> bool:
    x0, y0, x1, y1 = bbox
    return (
        x0 >= rect.x0 - tol
        and y0 >= rect.y0 - tol
        and x1 <= rect.x1 + tol
        and y1 <= rect.y1 + tol
        and x1 >= x0
        and y1 >= y0
    )


def _sample_nonwhite_fraction(page: fitz.Page, dpi: int, out_path: Path | None = None) -> float:
    zoom = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        pix.save(str(out_path))
    samples = memoryview(pix.samples)
    channels = pix.n
    pixels = pix.width * pix.height
    nonwhite = 0
    for i in range(0, len(samples), channels):
        if min(samples[i:i + min(3, channels)]) < 245:
            nonwhite += 1
    return nonwhite / pixels if pixels else 0.0


def preflight_rendered_pdf(
    *,
    pdf_path: Path,
    publication_ir: dict[str, Any],
    renderer_report: dict[str, Any],
    custody: dict[str, Any],
    policy: dict[str, Any],
    raster_dir: Path | None = None,
) -> dict[str, Any]:
    if publication_ir.get("publication_ir_digest") != digest_without_field(publication_ir, "publication_ir_digest"):
        raise AssertionError("RENDER_PUBLICATION_IR_DIGEST_DRIFT")
    boundary = publication_ir.get("authority_boundary") or {}
    if (
        boundary.get("semantic_authority") != "UPSTREAM_ONLY"
        or boundary.get("renderer_authority") != "COMPOSITION_ONLY"
        or boundary.get("renderer_may_introduce_semantic_claims") is not False
        or boundary.get("renderer_may_substitute_representation") is not False
        or (publication_ir.get("lossless_audit") or {}).get("status") != "PASS"
    ):
        raise AssertionError("RENDER_PUBLICATION_AUTHORITY_NOT_CLOSED")

    pdf_sha = sha256_file(pdf_path)
    renderer_report_digest = digest(renderer_report)
    if custody.get("publication_ir_digest") != publication_ir["publication_ir_digest"]:
        raise AssertionError("RENDER_CUSTODY_PUBLICATION_IR_MISMATCH")
    if custody.get("renderer_report_digest") != renderer_report_digest:
        raise AssertionError("RENDER_CUSTODY_REPORT_DIGEST_MISMATCH")
    if custody.get("expected_pdf_sha256") != pdf_sha:
        raise AssertionError("RENDER_CUSTODY_PDF_DIGEST_MISMATCH")
    if renderer_report.get("artifact_sha256") != pdf_sha:
        raise AssertionError("RENDER_REPORT_PDF_DIGEST_MISMATCH")
    if custody.get("renderer_authority") != "COMPOSITION_ONLY":
        raise AssertionError("RENDERER_AUTHORITY_ESCALATION")

    findings: list[str] = []
    page_audit: list[dict[str, Any]] = []
    actual_font_sizes: list[float] = []
    internal_patterns = [re.compile(p) for p in policy["internal_identifier_patterns"]]
    expected_w = float(policy["page_geometry"]["width_pt"])
    expected_h = float(policy["page_geometry"]["height_pt"])
    geom_tol = float(policy["page_geometry"]["tolerance_pt"])
    bbox_tol = float(policy["page_bounds_tolerance_pt"])

    doc = fitz.open(pdf_path)
    if len(doc) == 0:
        findings.append("RENDER_PDF_HAS_NO_PAGES")

    for index, page in enumerate(doc):
        rect = page.rect
        page_findings: list[str] = []
        if abs(rect.width - expected_w) > geom_tol or abs(rect.height - expected_h) > geom_tol:
            page_findings.append("PAGE_GEOMETRY_NOT_A4")

        text = page.get_text("text")
        internal_hits = sorted({m.group(0) for rx in internal_patterns for m in rx.finditer(text)})
        if internal_hits:
            page_findings.append("INTERNAL_IDENTIFIER_LEAK")

        span_count = 0
        bounds_violations = 0
        page_font_sizes: list[float] = []
        for span in _text_spans(page):
            span_count += 1
            size = float(span.get("size") or 0)
            if size > 0:
                page_font_sizes.append(size)
                actual_font_sizes.append(size)
            if not _bbox_inside(span.get("bbox", (0, 0, 0, 0)), rect, bbox_tol):
                bounds_violations += 1
        if bounds_violations:
            page_findings.append("TEXT_OUTSIDE_PAGE_BOUNDS")

        drawing_count = len(page.get_drawings())
        image_count = len(page.get_images(full=True))
        page_audit.append(
            {
                "page": index + 1,
                "width_pt": round(rect.width, 3),
                "height_pt": round(rect.height, 3),
                "text_char_count": len(text.strip()),
                "text_span_count": span_count,
                "minimum_text_font_pt": round(min(page_font_sizes), 3) if page_font_sizes else None,
                "drawing_count": drawing_count,
                "image_count": image_count,
                "internal_identifier_hits": internal_hits,
                "bounds_violation_count": bounds_violations,
                "findings": sorted(set(page_findings)),
            }
        )
        findings.extend(f"PAGE_{index + 1}:{f}" for f in page_findings)

    actual_floor = min(actual_font_sizes) if actual_font_sizes else None
    if actual_floor is None:
        findings.append("RENDER_NO_EXTRACTABLE_TEXT")
    elif actual_floor < float(policy["minimum_actual_text_font_pt"]):
        findings.append("RENDER_ACTUAL_FONT_FLOOR_VIOLATION")

    sample_pages: list[dict[str, Any]] = []
    if len(doc):
        sample_indexes = sorted(set([0, len(doc) // 2, len(doc) - 1]))
        for idx in sample_indexes:
            png = None
            if raster_dir is not None:
                png = raster_dir / f"page-{idx + 1:03d}.png"
            fraction = _sample_nonwhite_fraction(doc[idx], int(policy["sample_raster_dpi"]), png)
            sample_pages.append(
                {
                    "page": idx + 1,
                    "nonwhite_fraction": round(fraction, 6),
                    "raster_path": png.name if png else None,
                }
            )
            if fraction < float(policy["minimum_sample_nonwhite_fraction"]):
                findings.append(f"PAGE_{idx + 1}:RASTER_EFFECTIVELY_BLANK")

    if renderer_report.get("page_count") != len(doc):
        findings.append("RENDERER_REPORT_PAGE_COUNT_MISMATCH")

    findings = sorted(set(findings))
    machine_pass = not findings
    report = {
        "schema_version": "1.0.0",
        "preflight_id": custody["custody_id"].replace("RENDER-CUSTODY-", "RENDER-PREFLIGHT-"),
        "publication_ir_id": publication_ir["publication_ir_id"],
        "publication_ir_digest": publication_ir["publication_ir_digest"],
        "renderer_name": custody["renderer_name"],
        "renderer_report_digest": renderer_report_digest,
        "pdf_sha256": pdf_sha,
        "page_count": len(doc),
        "minimum_actual_text_font_pt": round(actual_floor, 3) if actual_floor is not None else None,
        "page_audit": page_audit,
        "sample_pages": sample_pages,
        "machine_findings": findings,
        "machine_preflight_pass": machine_pass,
        "machine_release_state": (
            "MACHINE_PREFLIGHT_PASS_HUMAN_VISUAL_REVIEW_PENDING"
            if machine_pass
            else "MACHINE_PREFLIGHT_BLOCKED"
        ),
        "human_visual_review_state": "PENDING",
        "release_authorized": False,
    }
    doc.close()
    return report


def main() -> None:
    import argparse
    from jsonschema import Draft202012Validator

    ap = argparse.ArgumentParser(description="Inspect a finished Physics PDF behind the Blueprint publication boundary.")
    ap.add_argument("--pdf", type=Path, required=True)
    ap.add_argument("--publication-ir", type=Path, required=True)
    ap.add_argument("--renderer-report", type=Path, required=True)
    ap.add_argument("--custody", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--raster-dir", type=Path)
    args = ap.parse_args()

    load = lambda p: json.loads(p.read_text(encoding="utf-8"))
    policy = load(ROOT / "policy" / "render-preflight.v1.json")
    publication_ir = load(args.publication_ir)
    renderer_report = load(args.renderer_report)
    custody = load(args.custody)
    Draft202012Validator(load(ROOT / "contracts" / "render-custody.schema.json")).validate(custody)
    report = preflight_rendered_pdf(
        pdf_path=args.pdf,
        publication_ir=publication_ir,
        renderer_report=renderer_report,
        custody=custody,
        policy=policy,
        raster_dir=args.raster_dir,
    )
    schema = load(ROOT / "contracts" / "render-preflight-report.schema.json")
    Draft202012Validator(schema).validate(report)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not report["machine_preflight_pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
