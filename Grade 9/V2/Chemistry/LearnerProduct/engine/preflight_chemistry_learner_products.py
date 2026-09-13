#!/usr/bin/env python3
"""Actual-PDF visual preflight for Chemistry Core (1A)/(2A).

C-LP-23 checks physical page bounds, unintended placement overlaps, font floor,
A4 geometry, extracted learner text, reasoning-visual closure and raster proof.
The machine gate does not substitute for human actual-size visual review.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pymupdf
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
    width = max(0.0, min(a["x1"], b["x1"]) - max(a["x0"], b["x0"]))
    height = max(0.0, min(a["y1"], b["y1"]) - max(a["y0"], b["y0"]))
    return width * height


def physical_rect_checks(metrics: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Check physical page clipping and unintended solid-object overlap.

    `margin_pt` is a composition baseline/inset used by the renderer; clipping is
    defined against the physical page box. A baseline sitting on the composition
    inset is therefore not falsely labelled as clipping because a glyph ascender
    extends above that baseline. The independent raster proof remains the second
    renderer check.
    """
    threshold = float(policy["preflight"]["placement_overlap_fail_threshold_pt2"])
    clipping, overlaps = [], []
    by_page: dict[int, list[dict[str, Any]]] = {}
    for op in metrics["draw_ops"]:
        by_page.setdefault(int(op["page"]), []).append(op)
        if op["x0"] < -0.1 or op["y0"] < -0.1 or op["x1"] > A4_W + 0.1 or op["y1"] > A4_H + 0.1:
            clipping.append(op)
    for page, ops in by_page.items():
        solids = [row for row in ops if row["kind"] in {"TEXT", "PRIMITIVE"}]
        for index, left in enumerate(solids):
            for right in solids[index + 1:]:
                area = overlap_area(left, right)
                if area > threshold:
                    overlaps.append({
                        "page": page,
                        "left": left.get("content_ref"),
                        "right": right.get("content_ref"),
                        "left_kind": left["kind"],
                        "right_kind": right["kind"],
                        "area_pt2": round(area, 3),
                    })
    return {
        "clipping_count": len(clipping),
        "overlap_count": len(overlaps),
        "clipping_examples": clipping[:8],
        "overlap_examples": overlaps[:8],
        "status": "PASS" if not clipping and not overlaps else "FAIL",
    }


def raster_nonwhite_ratio(pix: pymupdf.Pixmap) -> float:
    channels = pix.n
    data = memoryview(pix.samples)
    nonwhite = sampled = 0
    stride = max(channels * 4, channels)
    for offset in range(0, len(data) - channels + 1, stride):
        sample = data[offset:offset + channels]
        rgb = sample[:3] if channels >= 3 else sample[:1]
        sampled += 1
        if any(value < 248 for value in rgb):
            nonwhite += 1
    return nonwhite / max(sampled, 1)


def sample_pages(page_count: int) -> list[int]:
    values = [0, page_count // 2, page_count - 1] if page_count else []
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

    geometry_failures, page_texts = [], []
    for number, page in enumerate(reader.pages, 1):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        if abs(width - A4_W) > 0.75 or abs(height - A4_H) > 0.75:
            geometry_failures.append({"page": number, "width": width, "height": height})
        page_texts.append(page.extract_text() or "")
    leaks = GUARD.scan_pages(page_texts)

    raster_dir.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open(str(pdf_path))
    scale = int(policy["preflight"]["raster_dpi"]) / 72.0
    minimum_ratio = float(policy["preflight"]["minimum_nonwhite_pixel_ratio"])
    raster_proof, blank = [], []
    for pageno in sample_pages(page_count):
        page = document.load_page(pageno)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
        ratio = raster_nonwhite_ratio(pix)
        out = raster_dir / f"{pdf_path.stem}-p{pageno + 1:03d}.png"
        pix.save(str(out))
        row = {
            "page": pageno + 1,
            "width_px": pix.width,
            "height_px": pix.height,
            "nonwhite_pixel_ratio": round(ratio, 6),
            "raster": out.name,
        }
        raster_proof.append(row)
        if ratio < minimum_ratio:
            blank.append(row)
    document.close()
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
    return {
        "obligated_surfaces": len(rows),
        "closed_surfaces": len(rows) - len(failed),
        "failed_surfaces": len(failed),
        "unavailable_secondary_representations": sum(len(row.get("unavailable_secondary_refs") or []) for row in rows),
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
    if not font_ok:
        raise ValueError("CHEM_LP_RENDER_FONT_FLOOR_FAILURE:" + product_name)
    if rectangles["clipping_count"]:
        raise ValueError("CHEM_LP_RENDER_CLIPPING:" + product_name)
    if rectangles["overlap_count"]:
        raise ValueError("CHEM_LP_RENDER_OVERLAP:" + product_name + ":" + canonical(rectangles["overlap_examples"][:2]))
    if parsed["internal_identifier_leaks"]:
        raise ValueError("CHEM_LP_RENDER_INTERNAL_ID_LEAK:" + product_name + ":" + canonical(parsed["internal_identifier_leaks"]))
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
    reports = {
        key: preflight_product(key.upper(), render_manifest[key], render_dir / render_manifest[key]["pdf"], policy, raster_dir)
        for key in ("core1a", "core2a")
    }
    report = {
        "preflight_id": "CHEM-LP-PREFLIGHT-" + render_manifest["manifest_id"].split("-")[-1],
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "render_manifest_ref": render_manifest["manifest_id"],
        "render_manifest_digest": render_manifest["manifest_digest"],
        "render_policy_ref": policy["policy_id"],
        "products": reports,
        "human_visual_review": "PENDING",
        "status": "PASS" if all(row["status"] == "PASS" for row in reports.values()) else "FAIL",
        "preflight_digest": "",
    }
    payload = copy.deepcopy(report); payload.pop("preflight_digest"); report["preflight_digest"] = digest(payload)
    (out_dir / "visual_preflight.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--render-manifest", required=True); parser.add_argument("--render-policy", required=True)
    parser.add_argument("--render-dir", required=True); parser.add_argument("--out-dir", required=True); args = parser.parse_args()
    run_preflight(load(args.render_manifest), load(args.render_policy), Path(args.render_dir), Path(args.out_dir))


if __name__ == "__main__":
    main()
