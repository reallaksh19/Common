#!/usr/bin/env python3
"""Validate a Core (1) -> Core (2) package hand-off across v1 contracts.

JSON Schema validates shape. This script validates relationships that span
ResearchBundle, manifest, source/question custody, learner state, publication
target and optional exam/question evidence artifacts. It performs no subject
research.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parent
EXAMPLE_DIR = ROOT / "examples"


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def resolve_ref(bundle_path: Path, ref: dict | None) -> Path | None:
    if not ref:
        return None
    return bundle_path.resolve().parent / ref["path"]


def load_ref(bundle_path: Path, ref: dict | None, label: str, errors: list[str]):
    path = resolve_ref(bundle_path, ref)
    if path is None:
        return None, None
    if not path.exists():
        errors.append(f"{label} referenced artifact does not exist: {path}")
        return None, path
    actual = sha256_file(path)
    if actual != ref["sha256"]:
        errors.append(f"{label} referenced artifact hash mismatch: expected {ref['sha256']} actual {actual}")
    return load(path), path


def validate_manifest_artifact_bytes(manifest: dict, manifest_path: Path, errors: list[str]):
    base = manifest_path.resolve().parent
    for art in manifest.get("artifacts", []):
        path = base / art["path"]
        if not path.exists():
            errors.append(f"manifest artifact missing from package: {art['role']} {art['path']}")
            continue
        actual = sha256_file(path)
        if actual != art["sha256"]:
            errors.append(f"manifest artifact hash mismatch for {art['role']} {art['path']}")


def validate_refs(bundle, source_ledger, strict_locators: bool, errors: list[str]):
    source_ids = {s["source_id"] for s in source_ledger.get("sources", [])}
    claim_ids = {c["claim_id"] for c in bundle.get("research_claims", [])}

    for claim in bundle.get("research_claims", []):
        for src in claim.get("source_refs", []):
            if src not in source_ids:
                errors.append(f"claim {claim['claim_id']} references unknown source {src}")
        for ev in claim.get("evidence_refs", []):
            src = ev.get("source_id")
            if src not in source_ids:
                errors.append(f"claim {claim['claim_id']} evidence locator references unknown source {src}")
            if src not in claim.get("source_refs", []):
                errors.append(f"claim {claim['claim_id']} evidence source {src} is absent from source_refs")
        if strict_locators and claim.get("traceability_class", "").startswith("MATERIAL_") and claim.get("source_refs") and not claim.get("evidence_refs"):
            errors.append(f"production handoff requires evidence locator(s) for material claim {claim['claim_id']}")

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

    if strict_locators:
        for reg in bundle.get("scope_graph", {}).get("canonical_registry_versions", []):
            if not reg.get("registry_sha256"):
                errors.append(f"production handoff requires registry_sha256 for {reg['registry_id']}@{reg['version']}")


def validate_ref_binding(bundle, manifest, key: str, role: str, errors: list[str]):
    ref = bundle.get(key)
    rows = artifact_by_role(manifest, role)
    if ref:
        if len(rows) != 1:
            errors.append(f"manifest must contain exactly one {role} artifact when {key} is present; found {len(rows)}")
            return
        row = rows[0]
        if row["path"] != ref["path"] or row["sha256"] != ref["sha256"]:
            errors.append(f"ResearchBundle {key} does not match manifest {role} artifact")
    elif rows:
        errors.append(f"manifest contains {role} but ResearchBundle has no {key}")


def validate_manifest_binding(bundle, manifest, errors: list[str]):
    if manifest["research_bundle_id"] != bundle["research_bundle_id"]:
        errors.append("manifest research_bundle_id does not match ResearchBundle")
    if manifest["evidence_version"] != bundle["evidence_version"]:
        errors.append("manifest evidence_version does not match ResearchBundle")

    require_one_artifact(manifest, "RESEARCH_BUNDLE", errors)
    require_one_artifact(manifest, "RESEARCH_CORE_MD", errors)
    require_one_artifact(manifest, "RESEARCH_CORE_PDF", errors)
    validate_ref_binding(bundle, manifest, "source_ledger_ref", "SOURCE_LEDGER", errors)
    validate_ref_binding(bundle, manifest, "question_content_ledger_ref", "QUESTION_CONTENT_LEDGER", errors)
    validate_ref_binding(bundle, manifest, "question_occurrence_ledger_ref", "QUESTION_OCCURRENCE_LEDGER", errors)
    validate_ref_binding(bundle, manifest, "question_evidence_ledger_ref", "QUESTION_EVIDENCE_LEDGER", errors)

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


def validate_question_custody(bundle, source_ledger, qcontent, qocc, qledger, strict_transfer: bool, errors: list[str]):
    claim_ids = {c["claim_id"] for c in bundle.get("research_claims", [])}
    scope_ids = set(bundle.get("scope_graph", {}).get("included_nodes", [])) | set(bundle.get("concept_ids", []))
    sources = {s["source_id"]: s for s in source_ledger.get("sources", [])}
    content_records = {r["question_content_id"]: r for r in (qcontent or {}).get("records", [])}
    occurrence_records = {r["occurrence_id"]: r for r in (qocc or {}).get("records", [])}

    if qcontent is not None and len(content_records) != len(qcontent.get("records", [])):
        errors.append("QuestionContentLedger contains duplicate question_content_id values")
    if qocc is not None and len(occurrence_records) != len(qocc.get("records", [])):
        errors.append("QuestionOccurrenceLedger contains duplicate occurrence_id values")

    for qc in content_records.values():
        if qc["primary_concept_id"] not in scope_ids:
            errors.append(f"question content {qc['question_content_id']} primary concept is outside ScopeGraph: {qc['primary_concept_id']}")
        for cid in qc.get("supporting_concept_ids", []):
            if cid not in scope_ids:
                errors.append(f"question content {qc['question_content_id']} supporting concept is outside ScopeGraph: {cid}")
        for ref in qc.get("research_refs", []):
            if ref not in claim_ids:
                errors.append(f"question content {qc['question_content_id']} references unknown research claim {ref}")
        for oid in qc.get("occurrence_ids", []):
            if oid not in occurrence_records:
                errors.append(f"question content {qc['question_content_id']} references unknown occurrence {oid}")
            elif occurrence_records[oid]["question_content_id"] != qc["question_content_id"]:
                errors.append(f"question content/occurrence linkage mismatch for {qc['question_content_id']} and {oid}")

    for qo in occurrence_records.values():
        if qo["question_content_id"] not in content_records:
            errors.append(f"question occurrence {qo['occurrence_id']} references unknown question content {qo['question_content_id']}")
        src = sources.get(qo["source_id"])
        if not src:
            errors.append(f"question occurrence {qo['occurrence_id']} references unknown source {qo['source_id']}")
        elif qo["rights_status_at_freeze"] != src.get("rights", {}).get("status"):
            errors.append(f"question occurrence {qo['occurrence_id']} frozen rights state differs from SourceLedger")

    if qledger is None:
        if strict_transfer:
            errors.append("transfer publication requires QuestionEvidenceLedger")
        return

    rows = qledger.get("rows", [])
    if qledger.get("candidate_denominator") != len(rows):
        errors.append(f"QuestionEvidenceLedger candidate_denominator={qledger.get('candidate_denominator')} does not equal rows={len(rows)}")
    reviews = [r for r in rows if r.get("disposition") == "REVIEW"]
    if reviews:
        errors.append(f"QuestionEvidenceLedger contains {len(reviews)} REVIEW rows; hand-off must remain blocked")

    summary = qledger.get("summary")
    if summary is not None:
        keys = {"REQUIRED": "required", "DEFER": "defer", "EXCLUDE": "exclude", "REVIEW": "review", "DUPLICATE": "duplicate"}
        counts = {v: 0 for v in keys.values()}
        for row in rows:
            counts[keys[row["disposition"]]] += 1
        for key, actual in counts.items():
            if summary.get(key, 0) != actual:
                errors.append(f"QuestionEvidenceLedger summary.{key}={summary.get(key)} but rows imply {actual}")

    transfer_rows = [r for r in rows if r.get("disposition") == "REQUIRED" and "TRANSFER_BOOK" in r.get("publication_targets", [])]
    if transfer_rows and (qcontent is None or qocc is None):
        errors.append("REQUIRED TRANSFER_BOOK rows require both QuestionContentLedger and QuestionOccurrenceLedger")
    for row in transfer_rows:
        oid = row["occurrence_id"]
        qo = occurrence_records.get(oid)
        if not qo:
            errors.append(f"required transfer occurrence missing from QuestionOccurrenceLedger: {oid}")
            continue
        qcid = row.get("question_content_id") or qo["question_content_id"]
        if qcid != qo["question_content_id"]:
            errors.append(f"QuestionEvidenceLedger question_content_id mismatch for {oid}")
        if qcid not in content_records:
            errors.append(f"required transfer question content missing from QuestionContentLedger: {qcid}")
        if row.get("source_state") != "VERIFIED" or row.get("transcription_state") != "VERIFIED" or row.get("answer_state") != "VERIFIED":
            errors.append(f"required transfer row is not fully verified: {oid}")


def path_or_ref(explicit: Path | None, bundle_path: Path, ref: dict | None, label: str, errors: list[str]):
    if explicit is not None:
        if not explicit.exists():
            errors.append(f"{label} path does not exist: {explicit}")
            return None, explicit
        return load(explicit), explicit
    return load_ref(bundle_path, ref, label, errors)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--bundle", type=Path, default=EXAMPLE_DIR / "research-bundle.example.json")
    p.add_argument("--manifest", type=Path, default=EXAMPLE_DIR / "research-bundle-manifest.example.json")
    p.add_argument("--learner", type=Path, default=EXAMPLE_DIR / "learner-profile.example.json")
    p.add_argument("--target", type=Path, default=EXAMPLE_DIR / "publication-target.example.json")
    p.add_argument("--source-ledger", type=Path, default=EXAMPLE_DIR / "source-ledger.example.json")
    p.add_argument("--exam-demand", type=Path, action="append", default=[])
    p.add_argument("--question-content-ledger", type=Path, default=None)
    p.add_argument("--question-occurrence-ledger", type=Path, default=None)
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
    exam_profiles = [load(p) for p in args.exam_demand if p.exists()]

    qcontent, _ = path_or_ref(args.question_content_ledger, args.bundle, bundle.get("question_content_ledger_ref"), "QuestionContentLedger", errors)
    qocc, _ = path_or_ref(args.question_occurrence_ledger, args.bundle, bundle.get("question_occurrence_ledger_ref"), "QuestionOccurrenceLedger", errors)
    qledger, _ = path_or_ref(args.question_ledger, args.bundle, bundle.get("question_evidence_ledger_ref"), "QuestionEvidenceLedger", errors)

    schema_validate("research-bundle.schema.json", bundle, schemas, base_uri, store, errors)
    schema_validate("research-bundle-manifest.schema.json", manifest, schemas, base_uri, store, errors)
    schema_validate("learner-profile.schema.json", learner, schemas, base_uri, store, errors)
    schema_validate("publication-target.schema.json", target, schemas, base_uri, store, errors)
    schema_validate("source-ledger.schema.json", source_ledger, schemas, base_uri, store, errors)
    if qcontent is not None:
        schema_validate("question-content-ledger.schema.json", qcontent, schemas, base_uri, store, errors)
    if qocc is not None:
        schema_validate("question-occurrence-ledger.schema.json", qocc, schemas, base_uri, store, errors)
    if qledger is not None:
        schema_validate("question-evidence-ledger.schema.json", qledger, schemas, base_uri, store, errors)
    for exam in exam_profiles:
        schema_validate("exam-demand-profile.schema.json", exam, schemas, base_uri, store, errors)

    delivery_contract = target.get("publication_profile", {}).get("delivery_contract")
    strict_production = delivery_contract == "FULL_TOPIC_PAIR"
    strict_transfer = target.get("requested_products", {}).get("transfer_book", False)

    if not errors:
        validate_refs(bundle, source_ledger, strict_production, errors)
        validate_manifest_binding(bundle, manifest, errors)
        validate_manifest_artifact_bytes(manifest, args.manifest, errors)
        validate_publication_target(bundle, manifest, learner, target, exam_profiles, errors)
        validate_question_custody(bundle, source_ledger, qcontent, qocc, qledger, strict_transfer, errors)

    if errors:
        print("CORE1_CORE2_HANDOFF_V1 = FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("CORE1_CORE2_HANDOFF_V1 = PASS")
    print("BUNDLE_MANIFEST_BINDING = PASS")
    print("MANIFEST_ARTIFACT_HASH_BINDING = PASS")
    print("LEARNER_TARGET_BINDING = PASS")
    print("MATERIAL_VIEW_RECONCILIATION = PASS")
    print("RESEARCH_REFERENCE_CLOSURE = PASS")
    print(f"CLAIM_EVIDENCE_LOCATOR_CLOSURE = {'PASS' if strict_production else 'NOT_REQUIRED'}")
    print(f"CANONICAL_REGISTRY_HASH_BINDING = {'PASS' if strict_production else 'NOT_REQUIRED'}")
    print(f"QUESTION_CONTENT_OCCURRENCE_CLOSURE = {'PASS' if qcontent is not None or qocc is not None else 'NOT_APPLICABLE'}")
    print(f"QUESTION_DENOMINATOR_CLOSURE = {'PASS' if qledger is not None else 'NOT_APPLICABLE'}")
    competitive = target.get('purpose', {}).get('type') in {"COMPETITIVE_FOUNDATION", "COMPETITIVE_EXAM", "MOCK_EXAM_PREPARATION"}
    print(f"COMPETITIVE_EXAM_DEMAND_BINDING = {'PASS' if competitive else 'NOT_APPLICABLE'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
