#!/usr/bin/env python3
"""Actual-PDF visual preflight for Chemistry Core (1A)/(2A).

This stage validates the physical PDFs produced by C-LP-22. It combines
renderer-emitted physical rectangles with an independent PDF parser and raster
proof. It is intentionally a machine publication-engineering gate, not a human
subject/pedagogy/visual-quality approval.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF
from pypdf import PdfReader

HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]
CHEM_ROOT = LP_ROOT.parent
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))
import learner_surface_guard as GUARD  # noqa: E402

A4_W = 595.275590551
A4_H = 841.88976378


def load(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def sha_file(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def overlap_area(a: dict[str, Any], b: dict[str, Any]) -> float:
    x = max(0.0, min(a["x1"], b["x1"]) - max(a["x0"], b["x0"]))
    y = max(0.0, min(a["y1"], b["y1"]) - max(a["y0"], b["y0"]))
    return x * y


def physical_rect_checks(metrics: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    margin = float(policy["page"]["margin_pt"])
    threshold = float(policy["preflight"]["placement_overlap_fail_threshold_pt2"])
    clipping = []
    overlaps = []
    by_page: dict[int, list[dict[str, Any]]] = {}
    for op in metrics["draw_ops"]:
        page = int(op["page"])
        by_page.setdefault(page, []).append(op)
        if op["x0"] < -0.1 or op["y0"] < -0.1 or op["x1"] > A4_W + 0.1 or op["y1"] > A4_H + 0.1:
            clipping.append(op)
        if op["kind"] not in {"FOOTER", "RULE", "WORKSPACE_LINE"}:
            if op["x0"] < margin - 0.2 or op["x1"] > A4_W - margin + 0.2 or op["y0"] < margin - 0.2 or op["y1"] > A4_H - margin + 0.2:
                clipping.append(op)
    for page, ops in by_page.items():
        solids = [o for o in ops if o["kind"] in {"TEXT", "PRIMITIVE"}]
        for i, left in enumerate(solids):
            for right in solids[i + 1:]:
                area = overlap_area(left, right)
                if area > threshold:
                    overlaps.append({"page": page, "left": left.get("content_ref"), "right": right.get("content_ref"), "area_pt2": round(area, 3), "left_kind": left["kind"], "right_kind": right["kind"]})
    return {
        "clipping_count": len(clipping),
        "overlap_count": len(overlaps),
        "clipping_examples": clipping[:8],
        "overlap_examples": overlaps[:8],
        "status": "PASS" if not clipping and not overlaps else "FAIL",
    }


def raster_nonwhite_ratio(pix: fitz.Pixmap) -> float:
    channels = pix.n
    samples = memoryview(pix.samples)
    total = pix.width * pix.height
    if total <= 0:
        return 0.0
    # Sample every fourth pixel; sufficient to detect blank or near-blank pages.
    nonwhite = 0
    sampled = 0
    stride = max(channels * 4, channels)
    for offset in range(0, len(samples) - channels + 1, stride):
        pixel = samples[offset:offset + channels]
        rgb = pixel[:3] if channels >= 3 else pixel[:1]
        sampled += 1
        if any(v < 248 for v in rgb):
            nonwhite += 1
    return nonwhite / max(sampled, 1)


def sample_pages(page_count: int) -> list[int]:
    if page_count <= 0:
        return []
    values = [0, page_count // 2, page_count - 1]
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def pdf_checks(pdf_path: Path, metrics: dict[str, Any], policy: dict[str, Any], raster_dir: Path) -> dict[str, Any]:
    if sha_file(pdf_path) != metrics["pdf_sha256"]:
        raise ValueError("CHEM_LP_RENDER_ARTIFACT_HASH_MISMATCH:" + pdf_path.name)
    reader = PdfReader(str(pdf_path))
    page_count = len(reader.pages)
    if page_count != metrics["page_count"]:
        raise ValueError("CHEM_LP_RENDER_PAGE_COUNT_DRIFT:" + pdf_path.name)

    geometry_failures = []
    page_texts = []
    for index, page in enumerate(reader.pages, 1):
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        if abs(width - A4_W) > 0.75 or abs(height - A4_H) > 0.75:
            geometry_failures.append({"page": index, "width": width, "height": height})
        page_texts.append(page.extract_text() or "")
    leaks = GUARD.scan_pages(page_texts)

    raster_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    dpi = int(policy["preflight"]["raster_dpi"])
    scale = dpi / 72.0
    minimum_ratio = float(policy["preflight"]["minimum_nonwhite_pixel_ratio"])
    raster_proof = []
    blank = []
    for pageno in sample_pages(page_count):
        page = doc.load_page(pageno)
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        ratio = raster_nonwhite_ratio(pix)
        out = raster_dir / f"{pdf_path.stem}-p{pageno + 1:03d}.png"
        pix.save(str(out))
        row = {"page": pageno + 1, "width_px": pix.width, "height_px": pix.height, "nonwhite_pixel_ratio": round(ratio, 6), "raster": out.name}
        raster_proof.append(row)
        if ratio < minimum_ratio:
            blank.append(row)
    doc.close()

    return {
        "pdf_sha256": metrics["pdf_sha256"],
        "page_count": page_count,
        "geometry_failures": geometry_failures,
        "internal_identifier_leaks": leaks,
        "raster_proof": raster_proof,
        "blank_sample_pages": blank,
        "status": "PASS" if not geometry_failures and not leaks and not blank else "FAIL",
    }


def visual_closure(metrics: dict[str, Any]) -> dict[str, Any]:
    key = "section_visual_closure" if metrics["product"] == "CORE1A" else "item_visual_closure"
    rows = metrics.get(key) or []
    failed = [row for row in rows if row.get("status") != "PASS"]
    unavailable = sum(len(row.get("unavailable_secondary_refs") or []) for row in rows)
    return {
        "obligated_surfaces": len(rows),
        "closed_surfaces": len(rows) - len(failed),
        "failed_surfaces": len(failed),
        "unavailable_secondary_representations": unavailable,
        "status": "PASS" if not failed else "FAIL",
    }


def preflight_product(product_name: str, metrics: dict[str, Any], pdf_path: Path, policy: dict[str, Any], raster_dir: Path) -> dict[str, Any]:
    floor = float(policy["page"]["minimum_visible_font_pt"])
    font_ok = float(metrics["minimum_visible_font_pt"]) >= floor
    rectangles = physical_rect_checks(metrics, policy)
    parsed = pdf_checks(pdf_path, metrics, policy, raster_dir)
    visuals = visual_closure(metrics)
    status = "PASS" if font_ok and rectangles["status"] == "PASS" and parsed["status"] == "PASS" and visuals["status"] == "PASS" else "FAIL"
    report = {
        "product": product_name,
        "pdf": pdf_path.name,
        "minimum_visible_font_pt": metrics["minimum_visible_font_pt"],
        "required_minimum_visible_font_pt": floor,
        "font_floor_status": "PASS" if font_ok else "FAIL",
        "physical_rectangles": rectangles,
        "pdf_parse_and_raster": parsed,
        "visual_obligation_closure": visuals,
        "semantic_color_dependency": "NONE_BY_RENDERER_CONTRACT",
        "status": status,
    }
    if status != "PASS":
        if not font_ok:
            raise ValueError("CHEM_LP_RENDER_FONT_FLOOR_FAILURE:" + product_name)
        if rectangles["clipping_count"]:
            raise ValueError("CHEM_LP_RENDER_CLIPPING:" + product_name)
        if rectangles["overlap_count"]:
            raise ValueError("CHEM_LP_RENDER_OVERLAP:" + product_name)
        if parsed["internal_identifier_leaks"]:
            raise ValueError("CHEM_LP_RENDER_INTERNAL_ID_LEAK:" + product_name)
        if parsed["geometry_failures"]:
            raise ValueError("CHEM_LP_RENDER_PAGE_GEOMETRY_FAILURE:" + product_name)
        if parsed["blank_sample_pages"]:
            raise ValueError("CHEM_LP_RENDER_BLANK_PAGE:" + product_name)
        if visuals["status"] != "PASS":
            raise ValueError("CHEM_LP_RENDER_REQUIRED_VISUAL_MISSING:" + product_name)
    return report


def run_preflight(render_manifest: dict[str, Any], policy: dict[str, Any], render_dir: Path, out_dir: Path) -> dict[str, Any]:
    if policy.get("policy_id") != "CHEM-LEARNER-RENDER-v1" or render_manifest.get("render_policy_ref") != policy["policy_id"]:
        raise ValueError("CHEM_LP_RENDER_POLICY_MISMATCH")
    if render_manifest.get("status") != "RENDERED_NOT_PREFLIGHTED":
        raise ValueError("CHEM_LP_RENDER_MANIFEST_STATE_INVALID")
    out_dir.mkdir(parents=True, exist_ok=True)
    raster_dir = out_dir / "raster-proof"
    reports = {}
    for key in ("core1a", "core2a"):
        metrics = render_manifest[key]
        reports[key] = preflight_product(key.upper(), metrics, render_dir / metrics["pdf"], policy, raster_dir)
    report = {
        "preflight_id": "CHEM-LP-PREFLIGHT-" + render_manifest["manifest_id"].split("-")[-1],
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "render_manifest_ref": render_manifest["manifest_id"],
        "render_manifest_digest": render_manifest["manifest_digest"],
        "render_policy_ref": policy["policy_id"],
        "products": reports,
        "human_visual_review": "PENDING",
        "status": "PASS" if all(x["status"] == "PASS" for x in reports.values()) else "FAIL",
        "preflight_digest": "",
    }
    payload = copy.deepcopy(report)
    payload.pop("preflight_digest")
    report["preflight_digest"] = digest(payload)
    (out_dir / "visual_preflight.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-manifest", required=True)
    parser.add_argument("--render-policy", required=True)
    parser.add_argument("--render-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    run_preflight(load(args.render_manifest), load(args.render_policy), Path(args.render_dir), Path(args.out_dir))


if __name__ == "__main__":
    main()
