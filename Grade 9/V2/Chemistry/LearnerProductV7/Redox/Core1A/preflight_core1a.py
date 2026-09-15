#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import pymupdf as fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
BP = ROOT / "Grade 9" / "V2" / "Chemistry" / "LearningBlueprint"

AUTHORITY_REL = "golden/v7/core1a-study-note-redox-authority.json"
CCBOM_REL = "golden/v7/ccbom-redox.json"
TTU_REL = "golden/v5/core1a-hard-study-product.json"
SCOPE_REL = "product_authority/redox/core1a/product-source-scope.v2.json"
EXTENSION_REL = "product_authority/redox/core1a/grade-extension-authorization.v1.json"
AUDIT_REL = "source_audits/redox/production-source-audit.v2.json"


def load(rel: str):
    return json.loads((BP / rel).read_text(encoding="utf-8"))


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text).strip().lower()


def coverage(page: fitz.Page) -> float:
    rects = []
    for block in page.get_text("blocks"):
        rect = fitz.Rect(block[:4])
        if rect.width > 1 and rect.height > 1:
            rects.append(rect)
    for drawing in page.get_drawings():
        rect = drawing.get("rect")
        if rect and rect.width > 1 and rect.height > 1:
            rects.append(rect)
    if not rects:
        return 0.0
    page_rect = page.rect
    cols, rows = 48, 68
    cell_w, cell_h = page_rect.width / cols, page_rect.height / rows
    used = 0
    for iy in range(rows):
        y0 = iy * cell_h
        for ix in range(cols):
            cell = fitz.Rect(ix * cell_w, y0, (ix + 1) * cell_w, y0 + cell_h)
            if any(cell.intersects(rect) for rect in rects):
                used += 1
    return used / (cols * rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("manifest")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    authority = load(AUTHORITY_REL)
    ccbom = load(CCBOM_REL)
    ttu_doc = load(TTU_REL)
    scope = load(SCOPE_REL)
    extension = load(EXTENSION_REL)
    audit = load(AUDIT_REL)

    assert manifest["product"] == "CORE1A"
    assert manifest["subtopic_id"] == authority["subtopic_id"] == ccbom["subtopic_id"]
    assert manifest["authority_id"] == authority["authority_id"]
    assert manifest["ccbom_id"] == ccbom["ccbom_id"]
    assert manifest["production_source_audit_id"] == audit["audit_id"]
    assert audit["audit_role"] == "PRODUCTION_SOURCE_AUDIT"
    assert manifest["grade_extension_authorization_id"] == extension["authorization_id"]
    assert extension["status"] == "AUTHORIZED"
    assert manifest["source_scope_contract_id"] == scope["scope_contract_id"]
    assert manifest["scope_validation"]["status"] == "PASS"
    assert manifest["scope_validation"]["source_audit_role"] == "PRODUCTION_SOURCE_AUDIT"
    assert manifest["engineering_custody"]["status"] == "ENGINEERING_CUSTODY_READY"
    assert manifest["pal_validation"]["status"] == "PASS"
    assert manifest["pagination_mode"] == "CONTENT_FIRST"

    required = {obj["object_id"] for obj in authority["content_objects"]}
    realized = set(manifest["realized_content_object_ids"])
    assert realized == required, f"content realization mismatch missing={sorted(required-realized)} extra={sorted(realized-required)}"
    required_ttus = set(authority["reconstructable_ttu_refs"])
    serialized_ttus = {row["ttu_id"] for row in ttu_doc.get("reconstructable_ttus", [])}
    assert required_ttus <= serialized_ttus
    assert set(manifest["realized_ttu_ids"]) == required_ttus

    doc = fitz.open(pdf_path)
    assert 1 <= doc.page_count <= 30, f"page count {doc.page_count} outside HARD ceiling"
    all_text = "\n".join(page.get_text("text") for page in doc)
    normalized = norm(all_text)
    assert len(normalized) > 1500, "learner product text is unexpectedly thin"

    forbidden = list(authority["learner_surface_policy"]["forbidden_internal_terms"])
    forbidden += list(audit["learner_surface_policy"]["forbidden_surface_labels"])
    leaks = [term for term in forbidden if norm(term) in normalized]
    assert not leaks, f"learner-surface internal/jargon leak: {leaks}"

    held_tokens = [token for guard in scope["held_transformation_guards"] for token in guard["detection_tokens"]]
    held_leaks = [token for token in held_tokens if norm(token) in normalized]
    assert not held_leaks, f"held source-scope content leaked: {held_leaks}"

    for source in manifest["practice_source_labels"]:
        assert norm(source) in normalized, f"practice source not learner-visible: {source}"
    assert normalized.count("answer check") >= 4, "answer closure not visibly realized for all practice items"
    assert normalized.count("reconstruct the model") >= 2, "both reconstructable TTUs are not learner-visible"
    assert "[blank]" in normalized or "____" in normalized, "serialized incomplete reconstruction state not visible"
    assert normalized.count("verification:") >= 2, "TTU verification rules not visible"
    assert "final consistency checks" in normalized

    ratios = []
    page_text_lengths = []
    for index, page in enumerate(doc, 1):
        text = norm(page.get_text("text"))
        page_text_lengths.append(len(text))
        assert len(text) > 80, f"page {index} is effectively blank"
        ratio = coverage(page)
        ratios.append(ratio)
        assert ratio >= 0.43, f"page {index} active technical area too low: {ratio:.3f}"
    mean_ratio = sum(ratios) / len(ratios)
    assert mean_ratio >= 0.54, f"mean active technical area too low: {mean_ratio:.3f}"

    result = {
        "status": "PASS",
        "pages": doc.page_count,
        "mean_active_area": round(mean_ratio, 3),
        "page_active_area": [round(x, 3) for x in ratios],
        "page_text_lengths": page_text_lengths,
        "content_objects": len(realized),
        "reconstructable_ttus": len(required_ttus),
        "practice_questions": len(manifest["practice_question_ids"]),
        "production_source_audit": audit["audit_id"],
        "authorized_scope_tiers": scope["authorized_scope_tiers"],
        "held_scope_tiers": scope["held_scope_tiers"],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
