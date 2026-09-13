#!/usr/bin/env python3
"""Canonical Core1A entrypoint.

Core1A does not infer learner knowledge and does not equate a capability lesson with
a textbook bucket. It consumes the exact Core1 study plan plus the exact M-F
MathLearnerStudyModel, synthesizes governed teaching buckets, then realizes those
buckets as the learner textbook.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import build_math_core1a_textbook as base
import core1a_capability_authoring as capability
from core1a_bucket_synthesis import synthesize_bucket_plan
from core1a_bucket_realization import realize_bucket_manuscript, render_bucket_pdf

CONTRACTS = HERE.parent / "contracts"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--study-model", required=True)
    ap.add_argument("--pck-index", default=str(base.DEFAULT_PCK_INDEX))
    ap.add_argument("--problem-family-index", default=str(base.DEFAULT_FAMILY_INDEX))
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

    assets = base.load_pck_assets(Path(args.pck_index))
    families = base.load_problem_families(Path(args.problem_family_index))

    bucket_plan = synthesize_bucket_plan(core1, study_model, assets, families)
    bucket_schema = base.load(CONTRACTS / "math-core1a-bucket-plan.schema.json")
    jsonschema.validate(bucket_plan, bucket_schema)

    book = realize_bucket_manuscript(bucket_plan, core1, assets, families)
    manuscript_schema = base.load(CONTRACTS / "math-core1a-textbook-manuscript.schema.json")
    jsonschema.validate(book, manuscript_schema)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "core1a_bucket_plan.json").write_text(
        json.dumps(bucket_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "core1a_textbook_manuscript.json").write_text(
        json.dumps(book, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

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
        "artifact": {"path": pdf_path.name, **pdf_meta},
        "release_class": book["release_class"],
    }
    (out / "core1a_quality_audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
