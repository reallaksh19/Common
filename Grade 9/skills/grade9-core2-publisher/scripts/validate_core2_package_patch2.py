#!/usr/bin/env python3
"""Whitespace-stable independent structure-order validation for Core (2).

This validator proves declared structure binding, main-section MATERIAL custody,
and global reopened-PDF ordering. It deliberately does not call that result
exact physical-page morphology: page-intent -> physical-page custody is a
separate contract still to be implemented.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf as fitz

import validate_core2_package_structured_impl as impl


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text)).strip()


def _main_material_ids(study: dict) -> set[str]:
    return {
        item["item_id"]
        for section in study.get("main_sections", [])
        for item in section.get("items", [])
        if item.get("traceability_class") == "MATERIAL"
    }


def validate_structure_package(argv: list[str]) -> int:
    d = Path(impl._arg_value(argv, "--dir"))
    prefix = impl._arg_value(argv, "--prefix")
    plan = impl.load(d / f"{prefix}_Core2_Publication_Plan.json")
    audit = impl.load(d / f"{prefix}_Core2_Publication_Audit.json")
    manifest = impl.load(d / f"{prefix}_Core2_Publication_Manifest.json")
    if not plan.get("requested_products", {}).get("study_guide", False):
        print("CORE2_STRUCTURE_PACKAGE = NOT_APPLICABLE")
        return 0

    structure_path = d / f"{prefix}_Core2_Publication_Structure.json"
    errors: list[str] = []
    if not structure_path.exists():
        errors.append("missing PUBLICATION_STRUCTURE artifact")
    else:
        structure = impl.load(structure_path)
        contracts = Path(__file__).resolve().parents[3] / "architecture" / "core2" / "contracts" / "v1"
        errors.extend("publication-structure.schema.json:" + e for e in impl.schema_errors(structure, contracts / "publication-structure.schema.json"))
        for key in ("publication_plan_id", "research_bundle_id", "research_package_digest", "learner_profile_id"):
            if structure.get(key) != plan.get(key):
                errors.append(f"PublicationStructure binding drift: {key}")

        roles = [x for x in manifest.get("artifacts", []) if x.get("role") == "PUBLICATION_STRUCTURE"]
        if len(roles) != 1:
            errors.append(f"manifest must contain exactly one PUBLICATION_STRUCTURE; found {len(roles)}")
        elif roles[0].get("path") != structure_path.name or roles[0].get("sha256") != impl.legacy.sha256(structure_path):
            errors.append("manifest hash/path mismatch for PUBLICATION_STRUCTURE")

        arc_refs: list[str] = []
        ref_role: dict[str, str] = {}
        for unit in structure["study_guide"]["learning_units"]:
            for step in unit["arc_steps"]:
                for ref in step["content_refs"]:
                    arc_refs.append(ref)
                    ref_role[ref] = step["role"].replace("_", " ")
        page_refs = [ref for page in structure["study_guide"]["page_intents"] for ref in page["content_refs"]]
        if page_refs != arc_refs:
            errors.append("PublicationStructure page intents do not reconcile exactly to arc-step content order")

        study_model_path = d / f"{prefix}_Core2_Study_Guide.json"
        if study_model_path.exists():
            study = impl.load(study_model_path)
            material_ids = _main_material_ids(study)
            missing_material = sorted(material_ids - set(arc_refs))
            for content_ref in missing_material:
                errors.append(f"{content_ref}: MATERIAL item disappears between StudyGuide model and PublicationStructure")

        sg_pdf = d / f"{prefix}_Core2_Study_Guide.pdf"
        if sg_pdf.exists():
            doc = fitz.open(sg_pdf)
            raw_text = "\n".join(p.get_text() for p in doc)
            doc.close()
            text = _norm(raw_text)
            role_markers = [ref_role[ref] for ref in page_refs]
            if not impl._ordered(text, role_markers):
                errors.append("Study Guide PDF arc-step order does not reconcile")
            for page in structure["study_guide"]["page_intents"]:
                if _norm(page["cognitive_job"]) not in text:
                    errors.append(f"{page['page_intent_id']}: cognitive job missing from PDF")
            if not impl._ordered(text, ["Appendix A", "Appendix B", "Appendix C"]):
                errors.append("Study Guide PDF appendix order does not reconcile")

        tb_pdf = d / f"{prefix}_Core2_Transfer_Book.pdf"
        if tb_pdf.exists() and structure.get("transfer_book"):
            doc = fitz.open(tb_pdf)
            text = _norm("\n".join(p.get_text() for p in doc))
            internal = sum(1 for p in doc for link in p.get_links() if link.get("kind") == fitz.LINK_GOTO)
            doc.close()
            markers = [x.replace("_", " ") for x in structure["transfer_book"]["section_order"]]
            if not impl._ordered(text, markers):
                errors.append("Transfer Book PDF section topology does not reconcile")
            min_links = max(1, len(structure["transfer_book"]["question_navigation"]) * 3)
            if internal < min_links:
                errors.append(f"Transfer Book internal navigation too weak: {internal} < {min_links}")

    required_gates = {
        "product_structure", "arc_step_order_reconciliation", "page_intent_reconciliation",
        "support_progression_reconciliation", "attempt_help_solution_order",
        "appendix_order_reconciliation", "navigation_topology"
    }
    for gate in required_gates:
        if audit.get("gates", {}).get(gate) is not True:
            errors.append(f"missing/failed morphology audit gate: {gate}")
    if manifest.get("package_digest") != impl.legacy.package_digest(manifest.get("artifacts", [])):
        errors.append("publication package_digest mismatch after PublicationStructure binding")

    if errors:
        print("CORE2_STRUCTURE_PACKAGE = FAIL")
        for err in errors:
            print("- " + err)
        return 1
    print("CORE2_STRUCTURE_PACKAGE = PASS")
    print("PUBLICATION_STRUCTURE_BINDING = PASS")
    print("MODEL_TO_STRUCTURE_MATERIAL_CUSTODY = PASS")
    print("PDF_GLOBAL_STRUCTURE_ORDER = PASS")
    print("PHYSICAL_PAGE_MORPHOLOGY = PENDING")
    return 0


def main() -> int:
    impl.validate_structure_package = validate_structure_package
    return impl.main()


if __name__ == "__main__":
    raise SystemExit(main())
