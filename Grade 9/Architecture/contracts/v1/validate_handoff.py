#!/usr/bin/env python3
"""Validate a Core (1) -> Core (2) package hand-off across v1 contracts.

JSON Schema validates shape. This script validates relationships that span
ResearchBundle, manifest, learner, publication target and optional exam/question
evidence artifacts. It performs no subject research.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parent
EXAMPLE_DIR = ROOT / "examples"


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_schemas():
    schemas = {p.name: load(p) for p in ROOT.glob("*.schema.json")}
    base_uri = ROOT.as_uri().rstrip("/") + "/"
    store = {}
    for filename, schema in schemas.items():
        sid = schema.get("$id", filename)
        store[base_uri + filename] = schema
        store[base_uri + sid] = schema
        store[sid] = schema
    return schemas, base_uri, store


def schema_validate(name: str, instance, schemas, base_uri, store, errors: list[str]):
    schema = schemas[name]
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    validator = Draft202012Validator(schema, resolver=resolver)
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
        loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"{name}:{loc}: {err.message}")


def artifact_by_role(manifest, role: str):
    return [a for a in manifest.get("artifacts", []) if a.get("role") == role]


def require_one_artifact(manifest, role: str, errors: list[str]):
    rows = artifact_by_role(manifest, role)
    if len(rows) != 1:
        errors.append(f"manifest must contain exactly one {role} artifact; found {len(rows)}")
        return None
    return rows[0]


def validate_refs(bundle, source_ledger, errors: list[str]):
    source_ids = {s["source_id"] for s in source_ledger.get("sources", [])}
    claim_ids = {c["claim_id"] for c in bundle.get("research_claims", [])}

    for claim in bundle.get("research_claims", []):
        for src in claim.get("source_refs", []):
            if src not in source_ids:
                errors.append(f"claim {claim['claim_id']} references unknown source {src}")

    for rep in bundle.get("representation_requirements", []):
        for ref in rep.get("research_refs", []):
            if ref not in claim_ids:
                errors.append(f"representation {rep['representation_requirement_id']} references unknown research claim {ref}")

    for obj in bundle.get("equation_or_reaction_objects", []):
        for ref in obj.get("research_refs", []):
            if ref not in claim_ids:
                errors.append(f"semantic object {obj['id']} references unknown research claim {ref}")

    for wr in bundle.get("worked_reasoning", []):
        for ref in wr.get("research_refs", []):
            if ref not in claim_ids:
                errors.append(f"worked reasoning {wr['worked_reasoning_id']} references unknown research claim {ref}")


def validate_manifest_binding(bundle, manifest, errors: list[str]):
    if manifest["research_bundle_id"] != bundle["research_bundle_id"]:
        errors.append("manifest research_bundle_id does not match ResearchBundle")
    if manifest["evidence_version"] != bundle["evidence_version"]:
        errors.append("manifest evidence_version does not match ResearchBundle")

    require_one_artifact(manifest, "RESEARCH_BUNDLE", errors)
    source_art = require_one_artifact(manifest, "SOURCE_LEDGER", errors)
    require_one_artifact(manifest, "RESEARCH_CORE_MD", errors)
    require_one_artifact(manifest, "RESEARCH_CORE_PDF", errors)

    if source_art:
        ref = bundle["source_ledger_ref"]
        if source_art["path"] != ref["path"] or source_art["sha256"] != ref["sha256"]:
            errors.append("ResearchBundle source_ledger_ref does not match manifest SOURCE_LEDGER artifact")

    if bundle.get("question_evidence_ledger_ref"):
        q_art = require_one_artifact(manifest, "QUESTION_EVIDENCE_LEDGER", errors)
        if q_art:
            ref = bundle["question_evidence_ledger_ref"]
            if q_art["path"] != ref["path"] or q_art["sha256"] != ref["sha256"]:
                errors.append("ResearchBundle question_evidence_ledger_ref does not match manifest QUESTION_EVIDENCE_LEDGER artifact")
    elif artifact_by_role(manifest, "QUESTION_EVIDENCE_LEDGER"):
        errors.append("manifest contains QUESTION_EVIDENCE_LEDGER but ResearchBundle has no question_evidence_ledger_ref")

    exam_refs = bundle.get("exam_demand_profile_refs", [])
    exam_arts = artifact_by_role(manifest, "EXAM_DEMAND_PROFILE")
    if len(exam_refs) != len(exam_arts):
        errors.append(f"ExamDemand artifact count mismatch: bundle={len(exam_refs)} manifest={len(exam_arts)}")
    else:
        wanted = {(x["path"], x["sha256"]) for x in exam_refs}
        actual = {(x["path"], x["sha256"]) for x in exam_arts}
        if wanted != actual:
            errors.append("ResearchBundle exam_demand_profile_refs do not match manifest EXAM_DEMAND_PROFILE artifacts")

    rec = manifest.get("material_view_reconciliation") or {}
    if bundle.get("status") == "READY_FOR_PUBLISH":
        if rec.get("bundle_to_md_coverage") != 1 or rec.get("bundle_to_pdf_coverage") != 1:
            errors.append("READY_FOR_PUBLISH requires 100% ResearchBundle -> MD/PDF material coverage")
        if rec.get("unmapped_md_material_claims") != 0 or rec.get("unmapped_pdf_material_claims") != 0:
            errors.append("READY_FOR_PUBLISH requires zero unmapped MD/PDF material claims")


def validate_publication_target(bundle, manifest, learner, target, exam_profiles, errors: list[str]):
    if target["research_bundle_id"] != bundle["research_bundle_id"]:
        errors.append("PublicationTarget research_bundle_id does not match ResearchBundle")
    if target["research_package_digest"] != manifest["package_digest"]:
        errors.append("PublicationTarget research_package_digest does not match ResearchBundleManifest.package_digest")
    if target["learner_profile_id"] != learner["learner_profile_id"]:
        errors.append("PublicationTarget learner_profile_id does not match LearnerProfile")

    blocking = [u for u in bundle.get("unresolved_items", []) if u.get("blocking")]
    if bundle.get("status") == "READY_FOR_PUBLISH" and blocking:
        errors.append(f"READY_FOR_PUBLISH bundle contains {len(blocking)} blocking unresolved items")

    purpose = target.get("purpose", {})
    if purpose.get("type") in {"COMPETITIVE_FOUNDATION", "COMPETITIVE_EXAM", "MOCK_EXAM_PREPARATION"}:
        exam_id = purpose.get("exam_profile_id")
        matched = [x for x in exam_profiles if x.get("exam_id") == exam_id]
        if not matched:
            errors.append(f"competitive PublicationTarget requires ExamDemandProfile for exam_id {exam_id}")


def validate_question_ledger(question_ledger, errors: list[str]):
    if not question_ledger:
        return
    rows = question_ledger.get("rows", [])
    if question_ledger.get("candidate_denominator") != len(rows):
        errors.append(
            f"QuestionEvidenceLedger candidate_denominator={question_ledger.get('candidate_denominator')} does not equal rows={len(rows)}"
        )
    reviews = [r for r in rows if r.get("disposition") == "REVIEW"]
    if reviews:
        errors.append(f"QuestionEvidenceLedger contains {len(reviews)} REVIEW rows; hand-off must remain blocked")

    summary = question_ledger.get("summary")
    if summary is not None:
        keys = {"REQUIRED": "required", "DEFER": "defer", "EXCLUDE": "exclude", "REVIEW": "review", "DUPLICATE": "duplicate"}
        counts = {v: 0 for v in keys.values()}
        for row in rows:
            counts[keys[row["disposition"]]] += 1
        for key, actual in counts.items():
            if summary.get(key, 0) != actual:
                errors.append(f"QuestionEvidenceLedger summary.{key}={summary.get(key)} but rows imply {actual}")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--bundle", type=Path, default=EXAMPLE_DIR / "research-bundle.example.json")
    p.add_argument("--manifest", type=Path, default=EXAMPLE_DIR / "research-bundle-manifest.example.json")
    p.add_argument("--learner", type=Path, default=EXAMPLE_DIR / "learner-profile.example.json")
    p.add_argument("--target", type=Path, default=EXAMPLE_DIR / "publication-target.example.json")
    p.add_argument("--source-ledger", type=Path, default=EXAMPLE_DIR / "source-ledger.example.json")
    p.add_argument("--exam-demand", type=Path, action="append", default=[])
    p.add_argument("--question-ledger", type=Path, default=None)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    schemas, base_uri, store = load_schemas()
    errors: list[str] = []

    bundle = load(args.bundle)
    manifest = load(args.manifest)
    learner = load(args.learner)
    target = load(args.target)
    source_ledger = load(args.source_ledger)
    question_ledger = load(args.question_ledger) if args.question_ledger and args.question_ledger.exists() else None
    exam_profiles = [load(p) for p in args.exam_demand if p.exists()]

    schema_validate("research-bundle.schema.json", bundle, schemas, base_uri, store, errors)
    schema_validate("research-bundle-manifest.schema.json", manifest, schemas, base_uri, store, errors)
    schema_validate("learner-profile.schema.json", learner, schemas, base_uri, store, errors)
    schema_validate("publication-target.schema.json", target, schemas, base_uri, store, errors)
    schema_validate("source-ledger.schema.json", source_ledger, schemas, base_uri, store, errors)
    if question_ledger is not None:
        schema_validate("question-evidence-ledger.schema.json", question_ledger, schemas, base_uri, store, errors)
    for exam in exam_profiles:
        schema_validate("exam-demand-profile.schema.json", exam, schemas, base_uri, store, errors)

    if not errors:
        validate_refs(bundle, source_ledger, errors)
        validate_manifest_binding(bundle, manifest, errors)
        validate_publication_target(bundle, manifest, learner, target, exam_profiles, errors)
        validate_question_ledger(question_ledger, errors)

    if errors:
        print("CORE1_CORE2_HANDOFF_V1 = FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("CORE1_CORE2_HANDOFF_V1 = PASS")
    print("BUNDLE_MANIFEST_BINDING = PASS")
    print("LEARNER_TARGET_BINDING = PASS")
    print("MATERIAL_VIEW_RECONCILIATION = PASS")
    print("RESEARCH_REFERENCE_CLOSURE = PASS")
    print(f"QUESTION_DENOMINATOR_CLOSURE = {'PASS' if question_ledger is not None else 'NOT_APPLICABLE'}")
    competitive = target.get('purpose', {}).get('type') in {"COMPETITIVE_FOUNDATION", "COMPETITIVE_EXAM", "MOCK_EXAM_PREPARATION"}
    print(f"COMPETITIVE_EXAM_DEMAND_BINDING = {'PASS' if competitive else 'NOT_APPLICABLE'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
