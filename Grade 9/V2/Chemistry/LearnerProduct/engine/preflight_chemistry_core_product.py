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
BP_ROOT = CHEM_ROOT / "LearningBlueprint"
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

from chemistry_content_first_preflight import content_first_page_checks  # noqa: E402
from chemistry_review_candidate_preflight import review_candidate_checks  # noqa: E402
import learner_surface_guard as GUARD  # noqa: E402

A4_W = 595.28
A4_H = 841.89
POLICY_PATH = LP_ROOT / "policies" / "chemistry-learner-render-policy.json"
V5_POLICY_PATH = BP_ROOT / "policies" / "v5-study-product-quality-policy.json"
PRODUCT_CONTROL_PATH = BP_ROOT / "policies" / "product-control-consolidation.v1.json"
REVIEW_POLICY_PATH = BP_ROOT / "policies" / "review-candidate-realization.v1.json"


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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def representation_physical_closure(metrics: dict[str, Any], authority: dict[str, Any]) -> dict[str, Any]:
    """Bind Core authority representation use to actual primitive placements.

    A representation is not physically realized because it exists in a bundle or because
    a Core authority claims it was used. The renderer must emit a primitive placement
    carrying that exact representation reference. Conversely, a renderer may not draw a
    representation the Core payload did not declare as used.
    """
    closure = authority.get("representation_closure") or {}
    required = {str(value) for value in closure.get("used_representation_refs", []) if str(value).strip()}
    defined = {str(value) for value in closure.get("defined_representation_refs", []) if str(value).strip()}
    primitive_rows = metrics.get("primitives") or []
    if not isinstance(primitive_rows, list):
        return {
            "status": "FAIL",
            "required_representation_refs": sorted(required),
            "defined_representation_refs": sorted(defined),
            "physically_realized_representation_refs": [],
            "failures": ["CHEM_CORE_PREFLIGHT_REPRESENTATION_TRACE_INVALID"],
        }

    realized: set[str] = set()
    malformed = False
    for row in primitive_rows:
        if not isinstance(row, dict):
            malformed = True
            continue
        ref = str(row.get("representation_ref", "")).strip()
        if not ref:
            malformed = True
            continue
        realized.add(ref)

    failures: list[str] = []
    if malformed:
        failures.append("CHEM_CORE_PREFLIGHT_REPRESENTATION_TRACE_INVALID")
    missing = sorted(required - realized)
    if missing:
        failures.append("CHEM_CORE_PREFLIGHT_REPRESENTATION_NOT_PHYSICALLY_REALIZED:" + ",".join(missing))
    unexpected = sorted(realized - required)
    if unexpected:
        failures.append("CHEM_CORE_PREFLIGHT_REPRESENTATION_PHYSICAL_AUTHORITY_DRIFT:" + ",".join(unexpected))
    undefined = sorted(realized - defined) if defined else []
    if undefined:
        failures.append("CHEM_CORE_PREFLIGHT_REPRESENTATION_PHYSICAL_UNDEFINED:" + ",".join(undefined))

    return {
        "status": "PASS" if not failures else "FAIL",
        "required_representation_refs": sorted(required),
        "defined_representation_refs": sorted(defined),
        "physically_realized_representation_refs": sorted(realized),
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

    policy = load_json(POLICY_PATH)
    v5_policy = load_json(V5_POLICY_PATH)
    product_control = load_json(PRODUCT_CONTROL_PATH)
    review_policy = load_json(REVIEW_POLICY_PATH)
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
        page_rows.append({"page": page_no, "text_chars": len(text), "min_font_pt": round(page_min, 2)})
    doc.close()

    metrics = render_manifest.get("renderer_metrics") or {}
    content_first = content_first_page_checks(metrics, policy, render_manifest["product_mode"])
    failures.extend(content_first["failures"])
    content_by_page = {row["page"]: row for row in content_first["page_checks"]}
    for row in page_rows:
        if row["page"] in content_by_page:
            row.update({k: v for k, v in content_by_page[row["page"]].items() if k != "page"})

    physical_representation_closure = representation_physical_closure(metrics, authority)
    failures.extend(physical_representation_closure["failures"])

    review_candidate = review_candidate_checks(
        metrics,
        v5_policy,
        product_control,
        review_policy,
        render_manifest["product_mode"],
    )
    failures.extend(review_candidate["failures"])

    report = {
        "schema_version": "2.0.0",
        "preflight_id": render_manifest["render_id"].replace("CHEM-CORE-RENDER-", "CHEM-CORE-PREFLIGHT-", 1),
        "product_mode": render_manifest["product_mode"],
        "custody_id": custody["custody_id"],
        "custody_digest": custody["custody_digest"],
        "core_authority_id": authority["authority_id"],
        "core_authority_digest": authority["authority_digest"],
        "render_policy_ref": policy["policy_id"],
        "render_policy_digest": digest(policy),
        "review_policy_ref": review_policy["policy_id"],
        "review_policy_digest": digest(review_policy),
        "product_control_ref": product_control["policy_id"],
        "product_control_digest": digest(product_control),
        "artifact": copy.deepcopy(artifact),
        "page_checks": page_rows,
        "content_first_pagination": content_first,
        "physical_representation_closure": physical_representation_closure,
        "review_candidate": review_candidate,
        "minimum_font_pt": round(global_min_font, 2),
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
        "maturity_state": review_candidate["maturity_state"],
        "human_release_inferred": False,
        "preflight_digest": "",
    }
    report["preflight_digest"] = digest_without(report, "preflight_digest")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "core_product_preflight.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if failures:
        raise ValueError("CHEM_CORE_PREFLIGHT_FAILED:" + "|".join(failures[:8]))
    return report
