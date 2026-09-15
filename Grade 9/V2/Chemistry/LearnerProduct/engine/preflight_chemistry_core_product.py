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
LP_ROOT = HERE.parents[1]
CHEM_ROOT = HERE.parents[2]
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

import learner_surface_guard as GUARD  # noqa: E402

A4_W = 595.28
A4_H = 841.89
POLICY_PATH = LP_ROOT / "policies" / "chemistry-learner-render-policy.json"


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


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


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
        clipped = []
        for row in ops:
            y0 = max(margin, float(row.get("y0", margin)))
            y1 = min(A4_H - margin, float(row.get("y1", A4_H - margin)))
            if y1 > y0:
                clipped.append((y0, y1))
        active_height = max((row[1] for row in clipped), default=margin) - min((row[0] for row in clipped), default=margin)
        ratio = max(0.0, active_height / usable_height)
        semantic_refs = sorted({str(row.get("content_ref")) for row in ops if row.get("content_ref")})
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

    policy = load_policy()
    if render_manifest.get("render_policy_ref") != policy.get("policy_id"):
        raise ValueError("CHEM_CORE_PREFLIGHT_RENDER_POLICY_REF_DRIFT")
    if render_manifest.get("render_policy_digest") != digest(policy):
        raise ValueError("CHEM_CORE_PREFLIGHT_RENDER_POLICY_DIGEST_DRIFT")

    artifact = render_manifest["artifact"]
    pdf_path = out_dir / artifact["path"]
    if not pdf_path.exists():
        raise ValueError("CHEM_CORE_PREFLIGHT_PDF_MISSING")
    if file_digest(pdf_path) != artifact["pdf_sha256"]:
        raise ValueError("CHEM_CORE_PREFLIGHT_PDF_DIGEST_MISMATCH")

    doc = fitz.open(pdf_path)
    if doc.page_count < 1:
        doc.close()
        raise ValueError("CHEM_CORE_PREFLIGHT_PAGE_COUNT_INVALID")

    failures: list[str] = []
    if doc.page_count != artifact["page_count"]:
        failures.append(f"CHEM_CORE_PREFLIGHT_PAGE_COUNT_MISMATCH:{doc.page_count}!={artifact['page_count']}")

    page_rows: list[dict[str, Any]] = []
    global_min_font = 999.0
    font_floor = float(policy["page"]["minimum_visible_font_pt"])
    for index, page in enumerate(doc):
        page_no = index + 1
        rect = page.rect
        if abs(rect.width - A4_W) > 2.0 or abs(rect.height - A4_H) > 2.0:
            failures.append(f"CHEM_CORE_PREFLIGHT_PAGE_SIZE:{page_no}")
        text = " ".join(page.get_text("text").split())
        if len(text) < 30:
            failures.append(f"CHEM_CORE_PREFLIGHT_EFFECTIVELY_BLANK:{page_no}")
        leaks = GUARD.find_internal_identifiers(text)
        if leaks:
            failures.append(f"CHEM_CORE_PREFLIGHT_INTERNAL_ID_LEAK:{page_no}:{','.join(leaks[:5])}")
        spans = []
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                spans.extend(line.get("spans", []))
        sizes = [float(span.get("size", 0)) for span in spans if str(span.get("text", "")).strip()]
        page_min = min(sizes) if sizes else 999.0
        global_min_font = min(global_min_font, page_min)
        if page_min < font_floor:
            failures.append(f"CHEM_CORE_PREFLIGHT_FONT_FLOOR:{page_no}:{page_min:.2f}<{font_floor:.2f}")
        page_rows.append({
            "page": page_no,
            "text_chars": len(text),
            "min_font_pt": round(page_min, 2),
        })
    doc.close()

    content_first = content_first_page_checks(
        render_manifest.get("renderer_metrics") or {},
        policy,
        render_manifest["product_mode"],
    )
    failures.extend(content_first["failures"])
    content_by_page = {row["page"]: row for row in content_first["page_checks"]}
    for row in page_rows:
        if row["page"] in content_by_page:
            row.update({k: v for k, v in content_by_page[row["page"]].items() if k != "page"})

    report = {
        "schema_version": "1.0.0",
        "preflight_id": render_manifest["render_id"].replace("CHEM-CORE-RENDER-", "CHEM-CORE-PREFLIGHT-", 1),
        "product_mode": render_manifest["product_mode"],
        "custody_id": custody["custody_id"],
        "custody_digest": custody["custody_digest"],
        "core_authority_id": authority["authority_id"],
        "core_authority_digest": authority["authority_digest"],
        "render_policy_ref": policy["policy_id"],
        "render_policy_digest": digest(policy),
        "artifact": copy.deepcopy(artifact),
        "page_checks": page_rows,
        "content_first_pagination": content_first,
        "minimum_font_pt": round(global_min_font, 2),
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
        "preflight_digest": "",
    }
    report["preflight_digest"] = digest_without(report, "preflight_digest")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "core_product_preflight.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if failures:
        raise ValueError("CHEM_CORE_PREFLIGHT_FAILED:" + "|".join(failures[:8]))
    return report
