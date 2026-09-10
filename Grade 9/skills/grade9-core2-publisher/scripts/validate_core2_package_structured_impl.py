#!/usr/bin/env python3
"""Independent Core (2) package validator with publication-morphology closure."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pymupdf as fitz
from jsonschema import Draft202012Validator, RefResolver

import validate_core2_package_legacy as legacy


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _arg_value(argv: list[str], name: str) -> str:
    i = argv.index(name)
    return argv[i + 1]


def schema_errors(instance: dict, schema_path: Path) -> list[str]:
    root = schema_path.parent
    schemas = {p.name: load(p) for p in root.glob("*.schema.json")}
    base_uri = root.as_uri().rstrip("/") + "/"
    store = {}
    for name, obj in schemas.items():
        sid = obj.get("$id", name)
        for key in (name, sid, base_uri + name, base_uri + sid):
            store[key] = obj
    schema = load(schema_path)
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    return [f"{'.'.join(str(x) for x in e.absolute_path) or '<root>'}: {e.message}" for e in Draft202012Validator(schema, resolver=resolver).iter_errors(instance)]


def _ordered(text: str, markers: list[str]) -> bool:
    pos = -1
    for marker in markers:
        pos = text.find(marker, pos + 1)
        if pos < 0:
            return False
    return True


def validate_structure_package(argv: list[str]) -> int:
    d = Path(_arg_value(argv, "--dir"))
    prefix = _arg_value(argv, "--prefix")
    plan = load(d / f"{prefix}_Core2_Publication_Plan.json")
    audit = load(d / f"{prefix}_Core2_Publication_Audit.json")
    manifest = load(d / f"{prefix}_Core2_Publication_Manifest.json")
    if not plan.get("requested_products", {}).get("study_guide", False):
        print("CORE2_STRUCTURE_PACKAGE = NOT_APPLICABLE")
        return 0
    structure_path = d / f"{prefix}_Core2_Publication_Structure.json"
    errors = []
    if not structure_path.exists():
        errors.append("missing PUBLICATION_STRUCTURE artifact")
    else:
        structure = load(structure_path)
        contracts = Path(__file__).resolve().parents[3] / "architecture" / "core2" / "contracts" / "v1"
        errors.extend("publication-structure.schema.json:" + e for e in schema_errors(structure, contracts / "publication-structure.schema.json"))
        for key in ("publication_plan_id", "research_bundle_id", "research_package_digest", "learner_profile_id"):
            if structure.get(key) != plan.get(key):
                errors.append(f"PublicationStructure binding drift: {key}")
        roles = [x for x in manifest.get("artifacts", []) if x.get("role") == "PUBLICATION_STRUCTURE"]
        if len(roles) != 1:
            errors.append(f"manifest must contain exactly one PUBLICATION_STRUCTURE; found {len(roles)}")
        elif roles[0].get("path") != structure_path.name or roles[0].get("sha256") != legacy.sha256(structure_path):
            errors.append("manifest hash/path mismatch for PUBLICATION_STRUCTURE")
        sg_pdf = d / f"{prefix}_Core2_Study_Guide.pdf"
        if sg_pdf.exists():
            doc = fitz.open(sg_pdf)
            text = "\n".join(p.get_text() for p in doc)
            doc.close()
            arc_refs = []
            ref_role = {}
            for unit in structure["study_guide"]["learning_units"]:
                for step in unit["arc_steps"]:
                    for ref in step["content_refs"]:
                        arc_refs.append(ref)
                        ref_role[ref] = step["role"].replace("_", " ")
            page_refs = [ref for page in structure["study_guide"]["page_intents"] for ref in page["content_refs"]]
            if page_refs != arc_refs:
                errors.append("PublicationStructure page intents do not reconcile exactly to arc-step content order")
            role_markers = [ref_role[ref] for ref in page_refs]
            if not _ordered(text, role_markers):
                errors.append("Study Guide PDF arc-step order does not reconcile")
            for page in structure["study_guide"]["page_intents"]:
                if page["cognitive_job"] not in text:
                    errors.append(f"{page['page_intent_id']}: cognitive job missing from PDF")
            if not _ordered(text, ["Appendix A", "Appendix B", "Appendix C"]):
                errors.append("Study Guide PDF appendix order does not reconcile")
        tb_pdf = d / f"{prefix}_Core2_Transfer_Book.pdf"
        if tb_pdf.exists() and structure.get("transfer_book"):
            doc = fitz.open(tb_pdf)
            text = "\n".join(p.get_text() for p in doc)
            internal = sum(1 for p in doc for link in p.get_links() if link.get("kind") == fitz.LINK_GOTO)
            doc.close()
            markers = [x.replace("_", " ") for x in structure["transfer_book"]["section_order"]]
            if not _ordered(text, markers):
                errors.append("Transfer Book PDF section topology does not reconcile")
            min_links = max(1, len(structure["transfer_book"]["question_navigation"]) * 3)
            if internal < min_links:
                errors.append(f"Transfer Book internal navigation too weak: {internal} < {min_links}")
    required_gates = {"product_structure", "arc_step_order_reconciliation", "page_intent_reconciliation", "support_progression_reconciliation", "attempt_help_solution_order", "appendix_order_reconciliation", "navigation_topology"}
    for gate in required_gates:
        if audit.get("gates", {}).get(gate) is not True:
            errors.append(f"missing/failed morphology audit gate: {gate}")
    if manifest.get("package_digest") != legacy.package_digest(manifest.get("artifacts", [])):
        errors.append("publication package_digest mismatch after PublicationStructure binding")
    if errors:
        print("CORE2_STRUCTURE_PACKAGE = FAIL")
        for err in errors:
            print("- " + err)
        return 1
    print("CORE2_STRUCTURE_PACKAGE = PASS")
    print("PUBLICATION_STRUCTURE_BINDING = PASS")
    print("EXACT_PDF_MORPHOLOGY = PASS")
    return 0


def main() -> int:
    rc = legacy.main()
    if rc != 0:
        return rc
    return validate_structure_package(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
