#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    import pymupdf as fitz
except ImportError:  # pragma: no cover
    import fitz  # type: ignore

HERE = Path(__file__).resolve()
CHEM_ROOT = HERE.parents[2]
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

import learner_surface_guard as GUARD  # noqa: E402

A4_W = 595.28
A4_H = 841.89


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def digest_without(obj: dict[str, Any], field: str) -> str:
    payload = copy.deepcopy(obj)
    payload.pop(field, None)
    return digest(payload)


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def run_core_product_preflight(
    render_manifest: dict[str, Any],
    custody: dict[str, Any],
    authority: dict[str, Any],
    out_dir: Path,
) -> dict[str, Any]:
    if custody.get("status") != "CORE_PRODUCT_CUSTODY_READY":
        raise ValueError("CHEM_CORE_PREFLIGHT_CUSTODY_NOT_READY")
    if authority.get("status") != "CORE_AUTHORITY_READY":
        raise ValueError("CHEM_CORE_PREFLIGHT_AUTHORITY_NOT_READY")
    if render_manifest.get("custody_id") != custody["custody_id"] or render_manifest.get("custody_digest") != custody["custody_digest"]:
        raise ValueError("CHEM_CORE_PREFLIGHT_CUSTODY_DRIFT")
    if render_manifest.get("core_authority_id") != authority["authority_id"] or render_manifest.get("core_authority_digest") != authority["authority_digest"]:
        raise ValueError("CHEM_CORE_PREFLIGHT_AUTHORITY_DRIFT")

    artifact = render_manifest["artifact"]
    pdf_path = out_dir / artifact["path"]
    if not pdf_path.exists():
        raise ValueError("CHEM_CORE_PREFLIGHT_PDF_MISSING")
    if file_digest(pdf_path) != artifact["pdf_sha256"]:
        raise ValueError("CHEM_CORE_PREFLIGHT_PDF_DIGEST_MISMATCH")

    doc = fitz.open(pdf_path)
    if doc.page_count != artifact["page_count"] or doc.page_count < 1:
        raise ValueError("CHEM_CORE_PREFLIGHT_PAGE_COUNT_MISMATCH")

    page_rows: list[dict[str, Any]] = []
    global_min_font = 999.0
    for index, page in enumerate(doc):
        rect = page.rect
        if abs(rect.width - A4_W) > 2.0 or abs(rect.height - A4_H) > 2.0:
            raise ValueError(f"CHEM_CORE_PREFLIGHT_PAGE_SIZE:{index + 1}")
        text = " ".join(page.get_text("text").split())
        if len(text) < 30:
            raise ValueError(f"CHEM_CORE_PREFLIGHT_EFFECTIVELY_BLANK:{index + 1}")
        leaks = GUARD.find_internal_identifiers(text)
        if leaks:
            raise ValueError(f"CHEM_CORE_PREFLIGHT_INTERNAL_ID_LEAK:{index + 1}:{','.join(leaks[:5])}")
        spans = []
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                spans.extend(line.get("spans", []))
        sizes = [float(span.get("size", 0)) for span in spans if str(span.get("text", "")).strip()]
        page_min = min(sizes) if sizes else 999.0
        global_min_font = min(global_min_font, page_min)
        if page_min < 8.5:
            raise ValueError(f"CHEM_CORE_PREFLIGHT_FONT_FLOOR:{index + 1}:{page_min:.2f}")
        page_rows.append({"page": index + 1, "text_chars": len(text), "min_font_pt": round(page_min, 2)})
    doc.close()

    report = {
        "schema_version": "1.0.0",
        "preflight_id": render_manifest["render_id"].replace("CHEM-CORE-RENDER-", "CHEM-CORE-PREFLIGHT-", 1),
        "product_mode": render_manifest["product_mode"],
        "custody_id": custody["custody_id"],
        "custody_digest": custody["custody_digest"],
        "core_authority_id": authority["authority_id"],
        "core_authority_digest": authority["authority_digest"],
        "artifact": copy.deepcopy(artifact),
        "page_checks": page_rows,
        "minimum_font_pt": round(global_min_font, 2),
        "status": "PASS",
        "preflight_digest": "",
    }
    report["preflight_digest"] = digest_without(report, "preflight_digest")
    return report
