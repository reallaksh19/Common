#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import fitz


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, required=True)
    ap.add_argument("--prefix", required=True)
    args = ap.parse_args()

    d, p = args.dir, args.prefix
    files = {
        "plan": d / f"{p}_Core2_Publication_Plan.json",
        "model": d / f"{p}_Core2_Study_Guide.json",
        "md": d / f"{p}_Core2_Study_Guide.md",
        "pdf": d / f"{p}_Core2_Study_Guide.pdf",
        "audit": d / f"{p}_Core2_Publication_Audit.json",
        "manifest": d / f"{p}_Core2_Publication_Manifest.json",
    }
    errors: list[str] = []
    for name, path in files.items():
        if not path.exists():
            errors.append(f"missing {name}: {path.name}")
    if errors:
        print("CORE2_PACKAGE = FAIL")
        for e in errors:
            print("- " + e)
        return 1

    plan, model, audit, manifest = (load(files[k]) for k in ("plan", "model", "audit", "manifest"))
    if audit.get("status") == "FAIL":
        errors.append("publication audit status is FAIL")
    for key, value in audit.get("gates", {}).items():
        if value is not True:
            errors.append(f"audit gate failed: {key}")

    expected_roles = {
        "PUBLICATION_PLAN": files["plan"],
        "STUDY_GUIDE_MODEL": files["model"],
        "STUDY_GUIDE_MD": files["md"],
        "STUDY_GUIDE_PDF": files["pdf"],
        "PUBLICATION_AUDIT": files["audit"],
    }
    by_role = {x.get("role"): x for x in manifest.get("artifacts", [])}
    for role, path in expected_roles.items():
        row = by_role.get(role)
        if not row:
            errors.append(f"manifest missing {role}")
        elif row.get("path") != path.name or row.get("sha256") != sha256(path):
            errors.append(f"manifest hash/path mismatch for {role}")

    if manifest.get("research_package_digest") != plan.get("research_package_digest"):
        errors.append("research package digest drift between plan and manifest")
    if manifest.get("learner_profile_id") != plan.get("learner_profile_id"):
        errors.append("learner profile drift between plan and manifest")
    if manifest.get("publication_target_id") != plan.get("publication_target_id"):
        errors.append("publication target drift between plan and manifest")

    claim_refs = set()
    for sec in model.get("main_sections", []):
        for item in sec.get("items", []):
            if item.get("traceability_class") == "MATERIAL":
                refs = item.get("research_refs", [])
                if not refs:
                    errors.append(f"material item has no research refs: {item.get('item_id')}")
                claim_refs.update(refs)
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        if key not in model:
            errors.append(f"missing {key}")
        else:
            for item in model[key].get("items", []):
                if item.get("traceability_class") == "MATERIAL" and not item.get("research_refs"):
                    errors.append(f"appendix material item has no research refs: {item.get('item_id')}")

    md = files["md"].read_text(encoding="utf-8")
    for title in ("Appendix A — Core Practice", "Appendix B — Core Solutions", "Appendix C — Printable Handout"):
        if title not in md:
            errors.append(f"MD missing {title}")

    doc = fitz.open(files["pdf"])
    pdf_text = "\n".join(page.get_text() for page in doc)
    page_count = len(doc)
    doc.close()
    for marker in ("Appendix A", "Appendix B", "Appendix C", plan["research_bundle_id"]):
        if marker not in pdf_text:
            errors.append(f"PDF missing marker: {marker}")
    for rep in plan.get("representation_instances", []):
        if rep.get("status") != "RENDERED":
            errors.append(f"representation not rendered: {rep.get('representation_instance_id')}")
        if not set(rep.get("required_labels", [])) <= set(rep.get("rendered_labels", [])):
            errors.append(f"representation label closure failed: {rep.get('representation_instance_id')}")
        if rep.get("requirement_id") not in md:
            errors.append(f"MD missing representation requirement id: {rep.get('requirement_id')}")

    if errors:
        print("CORE2_PACKAGE = FAIL")
        for e in errors:
            print("- " + e)
        return 1

    print("CORE2_PACKAGE = PASS")
    print(f"PDF_PAGES = {page_count}")
    print("MATERIAL_TRACEABILITY = PASS")
    print("REPRESENTATION_CLOSURE = PASS")
    print("APPENDIX_A_B_C = PASS")
    print("PUBLICATION_MANIFEST_HASH_BINDING = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
