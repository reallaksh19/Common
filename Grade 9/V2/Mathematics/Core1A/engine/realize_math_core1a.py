#!/usr/bin/env python3
"""Canonical Core1A entrypoint.

Core1A does not infer learner knowledge and does not equate a capability lesson with
a textbook bucket. It consumes the exact Core1 study plan plus the exact M-F
MathLearnerStudyModel, synthesizes governed teaching buckets, then realizes those
buckets as the learner textbook.

Every run also emits a producer governance receipt. A legacy run without a
Canonical Domain Registry, generation/difficulty spec, and Engineering-domain
admission is explicitly marked UNBOUND_PRE_RELEASE; it can never be mistaken for
a fully governed release.

Bound runs additionally admit candidate examples into a governed example catalog
before learner authoring. Medium/Hard runs must also bind their pedagogy-research
references to a typed research manifest; those sources may justify pedagogy and
representation decisions but never become curriculum authority.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
MATH = HERE.parents[1]
MB_ENGINE = MATH / "MathBlueprint" / "engine"
for p in (HERE, MB_ENGINE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import build_math_core1a_textbook as base
import core1a_capability_authoring as capability
import core1a_governed_example_authoring as governed_examples
from core1a_bucket_synthesis import synthesize_bucket_plan
from core1a_bucket_realization import realize_bucket_manuscript, render_bucket_pdf
from producer_governance import core1a_receipt
from emit_stage_governance import write_receipt, digest as governance_digest
from engineering_product_custody import load_custody, stamp_receipt, custody_summary
from validate_canonical_domain_registry import validate_registry
from validate_self_teaching_generation_spec import validate_generation_spec
from validate_pedagogy_research_manifest import validate_generation_research_bindings

CONTRACTS = HERE.parent / "contracts"


def _restore_subtopic_identity(receipt: dict, bucket_plan: dict, generation_spec: dict | None) -> None:
    if not generation_spec or not receipt["difficulty_evidence"]:
        return
    by_id = {row["bucket_id"]: row for row in generation_spec["core1_buckets"]}
    by_title = {row["subtopic_title"].strip().lower(): row for row in generation_spec["core1_buckets"]}
    actual_to_subtopic = {}
    for bucket in bucket_plan["buckets"]:
        row = by_id.get(bucket["bucket_id"]) or by_title.get(bucket["title"].strip().lower())
        if row:
            actual_to_subtopic[bucket["bucket_id"]] = row["subtopic_id"]
    for row in receipt["difficulty_evidence"]:
        row["subtopic_ref"] = actual_to_subtopic.get(row["subtopic_ref"], row["subtopic_ref"])
    receipt["receipt_id"] = ""
    receipt["receipt_id"] = "MATH-STAGE-GOV-CORE1A-" + governance_digest(receipt)[:16]


def _refresh_governed_example_audit(book: dict, registry_bound: bool) -> None:
    if not registry_bound:
        return
    practice_count = 0
    worked_count = 0
    missing = []
    for bucket in book.get("buckets", []):
        for unit in bucket.get("capability_units", []):
            for ex in unit.get("worked_examples", []):
                worked_count += 1
                if not ex.get("governed_example_asset_ref") or not ex.get("content_digest"):
                    missing.append(unit["capability_ref"] + ":WORKED")
            for role, item in (unit.get("practice") or {}).items():
                practice_count += 1
                if item.get("source_class") != "GOVERNED_CORE1A_EXAMPLE" or not item.get("governed_example_asset_ref") or not item.get("content_digest"):
                    missing.append(unit["capability_ref"] + ":" + role)
    if missing:
        base.fail("CORE1A_GOVERNED_EXAMPLE_PROVENANCE_INCOMPLETE", ",".join(sorted(set(missing))))
    book["quality_audit"]["actual_problem_instances"] = practice_count
    book["quality_audit"]["governed_worked_examples"] = worked_count
    checks = list(book["quality_audit"].get("checks", []))
    if "GOVERNED_EXAMPLE_ADMISSION_BOUND" not in checks:
        checks.append("GOVERNED_EXAMPLE_ADMISSION_BOUND")
    book["quality_audit"]["checks"] = checks
    book["book_digest"] = base.digest(book, "book_digest")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--study-model", required=True)
    ap.add_argument("--pck-index", default=str(base.DEFAULT_PCK_INDEX))
    ap.add_argument("--problem-family-index", default=str(base.DEFAULT_FAMILY_INDEX))
    ap.add_argument("--generation-spec")
    ap.add_argument("--pedagogy-research-manifest")
    ap.add_argument("--domain-registry")
    ap.add_argument("--engineering-admission")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    capability.install()
    core1 = base.load(args.core1_plan)
    study_model = base.load(args.study_model)
    if core1.get("subject") != "MATHEMATICS" or study_model.get("subject") != "MATHEMATICS":
        base.fail("CORE1A_NON_MATH_INPUT")
    if core1.get("plan_digest") != base.digest(core1, "plan_digest"):
        base.fail("CORE1A_CORE1_PLAN_DIGEST_MISMATCH")
    if study_model.get("study_model_digest") != base.digest(study_model, "study_model_digest"):
        base.fail("CORE1A_STUDY_MODEL_DIGEST_INVALID")

    generation_spec = base.load(args.generation_spec) if args.generation_spec else None
    research_manifest = base.load(args.pedagogy_research_manifest) if args.pedagogy_research_manifest else None
    if generation_spec is not None:
        validate_generation_spec(generation_spec)
        validate_generation_research_bindings(generation_spec, research_manifest)
    elif research_manifest is not None:
        base.fail("CORE1A_RESEARCH_MANIFEST_WITHOUT_GENERATION_SPEC")

    registry = base.load(args.domain_registry) if args.domain_registry else None
    if registry is not None:
        validate_registry(registry)
        governed_examples.install(registry)
    engineering_custody = load_custody(args.engineering_admission, registry)

    assets = base.load_pck_assets(Path(args.pck_index))
    families = base.load_problem_families(Path(args.problem_family_index))

    bucket_plan = synthesize_bucket_plan(core1, study_model, assets, families)
    bucket_schema = base.load(CONTRACTS / "math-core1a-bucket-plan.schema.json")
    jsonschema.validate(bucket_plan, bucket_schema)

    book = realize_bucket_manuscript(bucket_plan, core1, assets, families)
    _refresh_governed_example_audit(book, registry is not None)
    manuscript_schema = base.load(CONTRACTS / "math-core1a-textbook-manuscript.schema.json")
    jsonschema.validate(book, manuscript_schema)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "core1a_bucket_plan.json").write_text(json.dumps(bucket_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "core1a_textbook_manuscript.json").write_text(json.dumps(book, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if registry is not None:
        catalog = governed_examples.catalog_document()
        if not catalog["examples"]:
            base.fail("CORE1A_GOVERNED_EXAMPLE_CATALOG_EMPTY")
        (out / "core1a_governed_example_catalog.json").write_text(
            json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    receipt = core1a_receipt(bucket_plan, book, registry=registry, generation_spec=generation_spec)
    _restore_subtopic_identity(receipt, bucket_plan, generation_spec)
    receipt = stamp_receipt(receipt, engineering_custody)
    write_receipt(receipt, out / "core1a_governance_receipt.json")

    pdf_path = out / "core1a_student_textbook.pdf"
    pdf_meta = render_bucket_pdf(book, pdf_path)
    audit = {
        "core1a_book_id": book["core1a_book_id"],
        "source_core1_plan_ref": core1["core1_study_plan_id"],
        "source_core1_plan_digest": core1["plan_digest"],
        "source_study_model_ref": study_model["study_model_id"],
        "source_study_model_digest": study_model["study_model_digest"],
        "bucket_plan_id": bucket_plan["bucket_plan_id"],
        "bucket_plan_digest": bucket_plan["plan_digest"],
        "book_digest": book["book_digest"],
        "quality_audit": book["quality_audit"],
        "governance_receipt_ref": receipt["receipt_id"],
        "governance_release_state": receipt["release_state"],
        "engineering_custody": custody_summary(engineering_custody),
        "governed_example_catalog_ref": "core1a_governed_example_catalog.json" if registry is not None else None,
        "pedagogy_research_manifest_ref": args.pedagogy_research_manifest,
        "pedagogy_research_manifest_digest": governance_digest(research_manifest) if research_manifest is not None else None,
        "artifact": {"path": pdf_path.name, **pdf_meta},
        "release_class": book["release_class"],
    }
    (out / "core1a_quality_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
