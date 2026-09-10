#!/usr/bin/env python3
"""Independently validate a materialized Core (2) publication package.

The validator re-opens the final PDF bytes and does not trust audit booleans as
proof. It also validates product-pair identity, Transfer Book semantic closure,
artifact hashes, package digest and hash-bound human-review state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

import pymupdf as fitz
from jsonschema import Draft202012Validator, RefResolver


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def package_digest(arts: list[dict]) -> str:
    payload = "\n".join("|".join(x) for x in sorted((a["role"], a["path"], a["sha256"]) for a in arts)).encode()
    return hashlib.sha256(payload).hexdigest()


def schema_context(root: Path):
    schemas = {p.name: load(p) for p in root.glob("*.schema.json")}
    base_uri = root.as_uri().rstrip("/") + "/"
    store = {}
    for name, obj in schemas.items():
        sid = obj.get("$id", name)
        for key in (name, sid, base_uri + name, base_uri + sid):
            store[key] = obj
    return schemas, base_uri, store


def validate_schema(name: str, instance: dict, root: Path, errors: list[str]):
    schemas, base_uri, store = schema_context(root)
    schema = schemas[name]
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    validator = Draft202012Validator(schema, resolver=resolver)
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
        loc = ".".join(str(x) for x in err.absolute_path) or "<root>"
        errors.append(f"{name}:{loc}: {err.message}")


def inspect_pdf(path: Path) -> dict:
    doc = fitz.open(path)
    min_font = None
    bounds = internal = broken = external = invalid_external = nongray = 0
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
        rect = page.rect
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = float(span.get("size", 0))
                    if size > 0:
                        min_font = size if min_font is None else min(min_font, size)
                    x0, y0, x1, y1 = span.get("bbox", (0, 0, 0, 0))
                    if x0 < -0.5 or y0 < -0.5 or x1 > rect.width + 0.5 or y1 > rect.height + 0.5:
                        bounds += 1
        for link in page.get_links():
            if link.get("kind") == fitz.LINK_GOTO:
                internal += 1
                if not (0 <= link.get("page", -1) < len(doc)):
                    broken += 1
            elif link.get("kind") == fitz.LINK_URI:
                external += 1
                parsed = urlparse(link.get("uri", ""))
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    invalid_external += 1
        for drawing in page.get_drawings():
            for key in ("color", "fill"):
                col = drawing.get(key)
                if isinstance(col, (tuple, list)) and len(col) >= 3 and max(col[:3]) - min(col[:3]) > 1e-6:
                    nongray += 1
    result = {
        "pages": len(doc), "min_font_pt": round(min_font or 0, 2),
        "text_bounds_violations": bounds, "internal_links_checked": internal,
        "broken_internal_links": broken, "external_links_checked": external,
        "invalid_external_links": invalid_external, "grayscale_nonneutral_drawings": nongray,
        "text": "\n".join(text_parts),
    }
    doc.close()
    return result


def validate_transfer(model: dict, errors: list[str]):
    qids = [q["question_id"] for q in model.get("questions", [])]
    qset = set(qids)
    if len(qids) != len(qset):
        errors.append("duplicate Transfer Book question IDs")
    solutions = {s["question_id"]: s for s in model.get("solutions", [])}
    if set(solutions) != qset:
        errors.append("Transfer Book questions/solutions are not one-to-one")
    set_coverage = set()
    for group in model.get("sets", []):
        gids = group.get("question_ids", [])
        if set(gids) - qset:
            errors.append(f"{group.get('set_id')}: contains unknown question IDs")
        set_coverage.update(gids)
        if group.get("mode") == "MIXED_TRANSFER":
            if not (group.get("concept_hidden_on_attempt") and group.get("task_hidden_on_attempt") and group.get("difficulty_hidden_on_attempt")):
                errors.append(f"{group.get('set_id')}: mixed-transfer metadata leaks on attempt")
            rows = group.get("diagnosis", {}).get("rows", [])
            diagnosed = [r.get("question_id") for r in rows]
            if set(diagnosed) != set(gids) or len(diagnosed) != len(set(diagnosed)):
                errors.append(f"{group.get('set_id')}: diagnosis does not cover mixed questions exactly once")
    if set_coverage != qset:
        errors.append("not every Transfer Book question belongs to a set")
    for q in model.get("questions", []):
        qid = q["question_id"]
        tiers = [h.get("tier") for h in q.get("hints", [])]
        if tiers != ["H1", "H2", "H3"][:len(tiers)]:
            errors.append(f"{qid}: hint tiers are not ordered H1→H2→H3")
        needed = {"H0": 0, "H1": 1, "H2": 2, "H3": 3}.get(q.get("required_hint_depth"), 99)
        if len(tiers) < needed:
            errors.append(f"{qid}: required hint depth is not met")
        if not q.get("source", {}).get("source_link"):
            errors.append(f"{qid}: source link missing")
        if not q.get("concept_labels", {}).get("primary", "").startswith("PRIMARY"):
            errors.append(f"{qid}: primary concept hierarchy label missing")
        for label in q.get("concept_labels", {}).get("supports", []):
            if not label.startswith("SUPPORTS"):
                errors.append(f"{qid}: supporting concept label lacks SUPPORTS hierarchy")
        sol = solutions.get(qid, {})
        for key in ("recap", "why", "method", "answer_check", "concept_to_keep", "return_target"):
            if not sol.get(key):
                errors.append(f"{qid}: solution missing {key}")
        if len(sol.get("method", "").split()) < 8:
            errors.append(f"{qid}: solution method is too terse")
        if set(q.get("research_refs", [])) - set(sol.get("research_refs", [])):
            errors.append(f"{qid}: solution loses research lineage")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, required=True)
    ap.add_argument("--prefix", required=True)
    args = ap.parse_args()
    d, p = args.dir, args.prefix
    grade9 = Path(__file__).resolve().parents[3]
    contracts = grade9 / "architecture" / "core2" / "contracts" / "v1"

    base_files = {
        "plan": d / f"{p}_Core2_Publication_Plan.json",
        "audit": d / f"{p}_Core2_Publication_Audit.json",
        "manifest": d / f"{p}_Core2_Publication_Manifest.json",
    }
    errors: list[str] = []
    for name, path in base_files.items():
        if not path.exists():
            errors.append(f"missing {name}: {path.name}")
    if errors:
        print("CORE2_PACKAGE = FAIL")
        for e in errors:
            print("- " + e)
        return 1

    plan, audit, manifest = (load(base_files[k]) for k in ("plan", "audit", "manifest"))
    validate_schema("publication-plan.schema.json", plan, contracts, errors)
    validate_schema("publication-audit.schema.json", audit, contracts, errors)
    validate_schema("publication-manifest.schema.json", manifest, contracts, errors)

    delivery = plan.get("delivery_contract")
    want_study = plan.get("requested_products", {}).get("study_guide", False)
    want_transfer = plan.get("requested_products", {}).get("transfer_book", False)
    study_files = {
        "model": d / f"{p}_Core2_Study_Guide.json",
        "md": d / f"{p}_Core2_Study_Guide.md",
        "pdf": d / f"{p}_Core2_Study_Guide.pdf",
    }
    transfer_files = {
        "model": d / f"{p}_Core2_Transfer_Book.json",
        "md": d / f"{p}_Core2_Transfer_Book.md",
        "pdf": d / f"{p}_Core2_Transfer_Book.pdf",
    }
    for label, group, wanted in (("study", study_files, want_study), ("transfer", transfer_files, want_transfer)):
        for kind, path in group.items():
            if wanted and not path.exists():
                errors.append(f"missing requested {label} {kind}: {path.name}")
            if not wanted and path.exists():
                errors.append(f"unexpected {label} artifact for delivery contract: {path.name}")

    study = transfer = None
    if want_study and all(x.exists() for x in study_files.values()):
        study = load(study_files["model"])
        validate_schema("study-guide.schema.json", study, contracts, errors)
        if study["publication_plan_id"] != plan["publication_plan_id"]:
            errors.append("Study Guide publication_plan_id mismatch")
        c = study.get("appendix_C", {})
        if not c.get("standalone_usable") or c.get("introduces_new_subject_content") or c.get("answer_leakage_detected"):
            errors.append("Appendix C blocking semantics failed")
        md = study_files["md"].read_text(encoding="utf-8")
        for title in ("Appendix A — Core Practice", "Appendix B — Core Solutions", "Appendix C — Printable Handout"):
            if title not in md:
                errors.append(f"Study Guide MD missing {title}")
        for sec in study.get("main_sections", []):
            for item in sec.get("items", []):
                if item.get("traceability_class") == "MATERIAL" and not item.get("research_refs"):
                    errors.append(f"material Study Guide item lacks research refs: {item.get('item_id')}")
        for key in ("appendix_A", "appendix_B", "appendix_C"):
            for item in study.get(key, {}).get("items", []):
                if item.get("traceability_class") == "MATERIAL" and not item.get("research_refs"):
                    errors.append(f"appendix material item lacks research refs: {item.get('item_id')}")
        for rep in plan.get("representation_instances", []):
            if rep.get("status") != "RENDERED":
                errors.append(f"representation not rendered: {rep.get('representation_instance_id')}")
            if not set(rep.get("required_labels", [])) <= set(rep.get("rendered_labels", [])):
                errors.append(f"representation label closure failed: {rep.get('representation_instance_id')}")
            if rep.get("requirement_id") not in md:
                errors.append(f"Study Guide MD missing representation requirement id: {rep.get('requirement_id')}")

    if want_transfer and all(x.exists() for x in transfer_files.values()):
        transfer = load(transfer_files["model"])
        validate_schema("transfer-book.schema.json", transfer, contracts, errors)
        validate_transfer(transfer, errors)
        if transfer["publication_plan_id"] != plan["publication_plan_id"]:
            errors.append("Transfer Book publication_plan_id mismatch")
        tmd = transfer_files["md"].read_text(encoding="utf-8")
        for marker in ("STOP · Try independently", "Complete Solutions"):
            if marker not in tmd:
                errors.append(f"Transfer Book MD missing {marker}")

    if delivery == "FULL_TOPIC_PAIR":
        if not (study and transfer):
            errors.append("FULL_TOPIC_PAIR requires both learner products")
        else:
            sid, tid = study["product_identity"], transfer["product_identity"]
            if not (sid.get("pair_id") == tid.get("pair_id") == plan.get("pair_id")):
                errors.append("reciprocal pair_id mismatch")
            if sid.get("companion_product_id") != transfer["publication_id"] or tid.get("companion_product_id") != study["publication_id"]:
                errors.append("reciprocal companion_product_id mismatch")

    if manifest.get("research_package_digest") != plan.get("research_package_digest"):
        errors.append("research package digest drift between plan and manifest")
    if manifest.get("learner_profile_id") != plan.get("learner_profile_id"):
        errors.append("learner profile drift between plan and manifest")
    if manifest.get("publication_target_id") != plan.get("publication_target_id"):
        errors.append("publication target drift between plan and manifest")
    if manifest.get("delivery_contract") != delivery:
        errors.append("delivery contract drift between plan and manifest")

    expected_roles = {"PUBLICATION_PLAN": base_files["plan"], "PUBLICATION_AUDIT": base_files["audit"]}
    if want_study:
        expected_roles.update({"STUDY_GUIDE_MODEL": study_files["model"], "STUDY_GUIDE_MD": study_files["md"], "STUDY_GUIDE_PDF": study_files["pdf"]})
    if want_transfer:
        expected_roles.update({"TRANSFER_BOOK_MODEL": transfer_files["model"], "TRANSFER_BOOK_MD": transfer_files["md"], "TRANSFER_BOOK_PDF": transfer_files["pdf"]})
    by_role: dict[str, list[dict]] = {}
    for row in manifest.get("artifacts", []):
        by_role.setdefault(row.get("role"), []).append(row)
    for role, path in expected_roles.items():
        rows = by_role.get(role, [])
        if len(rows) != 1:
            errors.append(f"manifest must contain exactly one {role}; found {len(rows)}")
        elif rows[0].get("path") != path.name or rows[0].get("sha256") != sha256(path):
            errors.append(f"manifest hash/path mismatch for {role}")
    if manifest.get("package_digest") != package_digest(manifest.get("artifacts", [])):
        errors.append("publication package_digest mismatch")

    if audit.get("status") in {"FAIL", "BLOCKED"}:
        errors.append(f"publication audit status is {audit.get('status')}")
    for key, value in audit.get("gates", {}).items():
        if value is not True:
            errors.append(f"audit gate failed: {key}")

    measured_by_role = {}
    for role, pdf_path in (("STUDY_GUIDE_PDF", study_files["pdf"]), ("TRANSFER_BOOK_PDF", transfer_files["pdf"])):
        if pdf_path.exists():
            measured_by_role[role] = inspect_pdf(pdf_path)
    evidence_by_role = {x["role"]: x for x in audit.get("pdf_evidence", [])}
    for role, measured in measured_by_role.items():
        ev = evidence_by_role.get(role)
        if not ev:
            errors.append(f"audit missing PDF evidence for {role}")
            continue
        path = expected_roles[role]
        if ev.get("sha256") != sha256(path) or ev.get("path") != path.name:
            errors.append(f"audit PDF identity mismatch for {role}")
        for key in ("pages", "text_bounds_violations", "internal_links_checked", "broken_internal_links", "external_links_checked", "invalid_external_links", "grayscale_nonneutral_drawings"):
            if ev.get(key) != measured.get(key):
                errors.append(f"audit evidence drift for {role}.{key}")
        if abs(float(ev.get("min_font_pt", -1)) - float(measured["min_font_pt"])) > 0.05:
            errors.append(f"audit evidence drift for {role}.min_font_pt")
        if measured["min_font_pt"] < 7.5:
            errors.append(f"minimum font below 7.5 pt in {role}: {measured['min_font_pt']}")
        if measured["text_bounds_violations"] or measured["broken_internal_links"] or measured["invalid_external_links"] or measured["grayscale_nonneutral_drawings"]:
            errors.append(f"measured PDF QA failed for {role}")
        for marker in ev.get("missing_required_text", []):
            errors.append(f"PDF missing required text in {role}: {marker}")
        for probe in ev.get("notation_probes_missing", []):
            errors.append(f"PDF missing notation probe in {role}: {probe}")
        if ev.get("answer_leakage_detected"):
            errors.append(f"answer leakage detected in {role}")
    if transfer:
        measured = measured_by_role.get("TRANSFER_BOOK_PDF", {})
        if measured.get("external_links_checked", 0) < len(transfer.get("questions", [])):
            errors.append("Transfer Book does not expose one clickable source link per question occurrence")
        text = measured.get("text", "")
        pos = text.find("Complete Solutions")
        if pos < 0 or "ANSWER / CHECK" in text[:pos] or "QUESTION RECAP" in text[:pos]:
            errors.append("Transfer Book answer separation failed on final PDF")

    review = audit.get("human_visual_review", {})
    current_pdf_hashes = {sha256(path) for path in (study_files["pdf"], transfer_files["pdf"]) if path.exists()}
    if set(review.get("pdf_sha256s", [])) != current_pdf_hashes:
        errors.append("human visual review hash set is stale relative to final PDFs")
    if review.get("minimum_render_dpi", 0) < 200:
        errors.append("human visual review contract requires at least 200 DPI")
    if review.get("status") == "PASS":
        total_pages = sum(x["pages"] for x in measured_by_role.values())
        if not review.get("all_pages_reviewed") or review.get("pages_reviewed", 0) < total_pages:
            errors.append("human visual PASS does not cover every final PDF page")
        if not review.get("reviewer") or not review.get("reviewed_at"):
            errors.append("human visual PASS lacks reviewer/timestamp")
    elif audit.get("release_state") == "HUMAN_REVIEW_PASS":
        errors.append("release state claims human PASS without human visual PASS")

    if errors:
        print("CORE2_PACKAGE = FAIL")
        for e in errors:
            print("- " + e)
        return 1

    total_pages = sum(x["pages"] for x in measured_by_role.values())
    print("CORE2_PACKAGE = PASS")
    print(f"DELIVERY_CONTRACT = {delivery}")
    print(f"LEARNER_PDFS = {len(measured_by_role)}")
    print(f"PDF_PAGES = {total_pages}")
    print("MATERIAL_TRACEABILITY = PASS")
    print("REPRESENTATION_CLOSURE = PASS")
    print("PRODUCT_PAIR_IDENTITY = PASS")
    print("APPENDIX_A_B_C = PASS" if want_study else "APPENDIX_A_B_C = NOT_APPLICABLE")
    print("TRANSFER_BOOK_SEMANTICS = PASS" if want_transfer else "TRANSFER_BOOK_SEMANTICS = NOT_APPLICABLE")
    print("MEASURED_PDF_QA = PASS")
    print("PUBLICATION_MANIFEST_HASH_BINDING = PASS")
    print(f"HUMAN_VISUAL_REVIEW = {review.get('status', 'MISSING')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
