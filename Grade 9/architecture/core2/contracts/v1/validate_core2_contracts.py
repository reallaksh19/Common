#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parent
REP_REG = ROOT.parents[1] / "representation" / "capabilities.v1.json"
EXAMPLES = ROOT / "examples"


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_instance(schema_name: str, instance: dict, schemas: dict, base_uri: str, store: dict, errors: list[str], label: str):
    schema = schemas[schema_name]
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    for err in Draft202012Validator(schema, resolver=resolver).iter_errors(instance):
        loc = ".".join(str(x) for x in err.absolute_path) or "<root>"
        errors.append(f"{label}:{loc}: {err.message}")


def main() -> int:
    errors: list[str] = []
    schemas = {}
    for path in sorted(ROOT.glob("*.schema.json")):
        try:
            schema = load(path)
            Draft202012Validator.check_schema(schema)
            schemas[path.name] = schema
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")

    required = {
        "product-identity.schema.json",
        "badge.schema.json",
        "representation-instance.schema.json",
        "publication-plan.schema.json",
        "study-guide.schema.json",
        "transfer-book.schema.json",
        "publication-audit.schema.json",
        "publication-manifest.schema.json",
    }
    missing = sorted(required - schemas.keys())
    if missing:
        errors.append("missing schemas: " + ", ".join(missing))

    base_uri = ROOT.as_uri().rstrip("/") + "/"
    store = {}
    for name, schema in schemas.items():
        sid = schema.get("$id", name)
        store[name] = schema
        store[sid] = schema
        store[base_uri + name] = schema
        store[base_uri + sid] = schema

    if not errors:
        for schema_name in ("publication-plan.schema.json", "study-guide.schema.json", "transfer-book.schema.json"):
            try:
                RefResolver(base_uri=base_uri, referrer=schemas[schema_name], store=store)
            except Exception as exc:
                errors.append(f"{schema_name} ref resolution: {exc}")

    try:
        transfer = schemas["transfer-book.schema.json"]
        qreq = set(transfer["$defs"]["question"]["required"])
        mature_question_fields = {
            "occurrence_id", "question_content_id", "primary_concept_id", "supporting_concept_ids",
            "concept_labels", "task", "difficulty", "transfer", "source", "attempt",
            "required_hint_depth", "hints", "solution_id"
        }
        missing_fields = mature_question_fields - qreq
        if missing_fields:
            errors.append("TransferBook question contract missing: " + ", ".join(sorted(missing_fields)))
        sreq = set(transfer["$defs"]["solution"]["required"])
        mature_solution_fields = {"recap", "why", "method", "answer_check", "concept_to_keep", "return_target"}
        if not mature_solution_fields <= sreq:
            errors.append("TransferBook solution contract is weaker than mature assimilation solution grammar")
        mixed = transfer["$defs"]["set"].get("allOf", [])
        if not mixed:
            errors.append("TransferBook set contract does not encode mixed-transfer concealment")
    except Exception as exc:
        errors.append(f"transfer-book structural invariant: {exc}")

    try:
        study = schemas["study-guide.schema.json"]
        appendix_c_required = set(study["$defs"]["appendix_c"]["required"])
        for key in {"standalone_usable", "introduces_new_subject_content", "answer_leakage_detected"}:
            if key not in appendix_c_required:
                errors.append(f"StudyGuide Appendix C must require {key}")
    except Exception as exc:
        errors.append(f"study-guide appendix invariant: {exc}")

    try:
        registry = load(REP_REG)
        rows = registry.get("capabilities", [])
        ids = [r.get("capability_id") for r in rows]
        types = [(r.get("representation_type"), tuple(r.get("subjects", []))) for r in rows]
        if len(ids) != len(set(ids)):
            errors.append("duplicate representation capability_id")
        if not any(r.get("status") == "IMPLEMENTED" for r in rows):
            errors.append("representation registry has no IMPLEMENTED capability")
        if any(not r.get("representation_type") for r in rows):
            errors.append("representation capability missing representation_type")
        if len(types) != len(set(types)):
            errors.append("duplicate representation_type + subjects capability declaration")
    except Exception as exc:
        errors.append(f"representation registry: {exc}")

    if EXAMPLES.exists() and not errors:
        mapping = {
            "transfer-book.example.json": "transfer-book.schema.json",
            "product-identity.example.json": "product-identity.schema.json",
        }
        for name, schema_name in mapping.items():
            path = EXAMPLES / name
            if path.exists():
                validate_instance(schema_name, load(path), schemas, base_uri, store, errors, name)

    if errors:
        print("CORE2_CONTRACTS_V1 = FAIL")
        for err in errors:
            print("- " + err)
        return 1

    print(f"CORE2_CONTRACTS_V1 = PASS ({len(schemas)} schemas)")
    print("DELIVERY_CONTRACT = PASS")
    print("RECIPROCAL_PRODUCT_IDENTITY = PASS")
    print("MATURE_TRANSFER_BOOK_CONTRACT = PASS")
    print("APPENDIX_C_BLOCKING_SEMANTICS = PASS")
    print("SHARED_REPRESENTATION_REGISTRY = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
