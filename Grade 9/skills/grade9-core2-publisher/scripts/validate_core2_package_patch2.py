#!/usr/bin/env python3
"""Independent structure and physical-page custody validation for Core (2).

Hard gates prove declared structure binding, main-section MATERIAL custody,
ReportLab-emitted page placement, exact PDF hash binding, and global reopened-PDF
ordering. Orphan/underfill morphology remains a separately reported release
finding until pagination policy is tuned against the cross-subject replays.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf as fitz

CORE2_ROOT = Path(__file__).resolve().parents[3] / "architecture" / "core2"
sys.path.insert(0, str(CORE2_ROOT))
from physical_page_custody import custody_errors, morphology_errors  # noqa: E402

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
    study_model_path = d / f"{prefix}_Core2_Study_Guide.json"
    sg_pdf = d / f"{prefix}_Core2_Study_Guide.pdf"
    page_map_path = d / f"{prefix}_Core2_Physical_Page_Map.json"
    errors: list[str] = []
    morphology_findings: list[str] = []
    contracts = Path(__file__).resolve().parents[3] / "architecture" / "core2" / "contracts" / "v1"

    if not structure_path.exists():
        errors.append("missing PUBLICATION_STRUCTURE artifact")
    else:
        structure = impl.load(structure_path)
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

        study = None
        if study_model_path.exists():
            study = impl.load(study_model_path)
            material_ids = _main_material_ids(study)
            missing_material = sorted(material_ids - set(arc_refs))
            for content_ref in missing_material:
                errors.append(f"{content_ref}: MATERIAL item disappears between StudyGuide model and PublicationStructure")

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

            if not page_map_path.exists():
                errors.append("missing PHYSICAL_PAGE_MAP for Study Guide PDF")
            else:
                page_map = impl.load(page_map_path)
                errors.extend("physical-page-map.schema.json:" + e for e in impl.schema_errors(page_map, contracts / "physical-page-map.schema.json"))
                if page_map.get("publication_structure_id") != structure.get("publication_structure_id"):
                    errors.append("PhysicalPageMap publication_structure_id binding drift")
                if study is not None and page_map.get("publication_id") != study.get("publication_id"):
                    errors.append("PhysicalPageMap publication_id binding drift")
                if page_map.get("pdf_sha256") != impl.legacy.sha256(sg_pdf):
                    errors.append("PhysicalPageMap pdf_sha256 does not bind exact Study Guide PDF")
                errors.extend("PhysicalPageMap: " + e for e in custody_errors(page_map))
                morphology_findings.extend(morphology_errors(page_map))

                map_roles = [x for x in manifest.get("artifacts", []) if x.get("role") == "PHYSICAL_PAGE_MAP"]
                if len(map_roles) != 1:
                    errors.append(f"manifest must contain exactly one PHYSICAL_PAGE_MAP; found {len(map_roles)}")
                elif map_roles[0].get("path") != page_map_path.name or map_roles[0].get("sha256") != impl.legacy.sha256(page_map_path):
                    errors.append("manifest hash/path mismatch for PHYSICAL_PAGE_MAP")

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
        errors.append("publication package_digest mismatch after PublicationStructure/PhysicalPageMap binding")

    if errors:
        print("CORE2_STRUCTURE_PACKAGE = FAIL")
        for err in errors:
            print("- " + err)
        return 1
    print("CORE2_STRUCTURE_PACKAGE = PASS")
    print("PUBLICATION_STRUCTURE_BINDING = PASS")
    print("MODEL_TO_STRUCTURE_MATERIAL_CUSTODY = PASS")
    print("PHYSICAL_PAGE_MAP_BINDING = PASS")
    print("STRUCTURE_TO_PHYSICAL_PAGE_CUSTODY = PASS")
    print("PDF_GLOBAL_STRUCTURE_ORDER = PASS")
    if morphology_findings:
        print(f"PHYSICAL_PAGE_MORPHOLOGY = PENDING ({len(morphology_findings)} findings)")
        for finding in morphology_findings:
            print("- " + finding)
    else:
        print("PHYSICAL_PAGE_MORPHOLOGY = PASS")
    return 0


def main() -> int:
    impl.validate_structure_package = validate_structure_package
    return impl.main()


if __name__ == "__main__":
    raise SystemExit(main())
