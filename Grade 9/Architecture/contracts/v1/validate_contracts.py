#!/usr/bin/env python3
"""Validate the frozen two-core JSON Schema contracts and architecture invariants.

Requires jsonschema>=4.18 for Draft 2020-12 validation. The script is intentionally
small and local to the frozen contract directory so it can be run before any
subject/runtime implementation is accepted.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, RefResolver
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema>=4.18 is required to validate contract schemas") from exc

ROOT = Path(__file__).resolve().parent
SCHEMA_FILES = sorted(ROOT.glob("*.schema.json"))
EXAMPLE_DIR = ROOT / "examples"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def build_store(schemas: dict[str, dict]) -> tuple[str, dict[str, dict]]:
    base_uri = ROOT.as_uri().rstrip("/") + "/"
    store: dict[str, dict] = {}
    for filename, schema in schemas.items():
        schema_id = schema.get("$id", filename)
        store[base_uri + filename] = schema
        store[base_uri + schema_id] = schema
        store[schema_id] = schema
    return base_uri, store


def check_architecture_invariants(schemas: dict[str, dict]) -> list[str]:
    errors: list[str] = []

    rb = schemas["research-bundle.schema.json"]
    rb_props = rb.get("properties", {})
    if "baseline_profile" in rb_props or "learner_profile" in rb_props:
        errors.append("ResearchBundle must not own learner Bxx/baseline state")
    if any(key.endswith("sha256") for key in rb_props):
        errors.append("ResearchBundle must not contain a self hash")

    manifest = schemas["research-bundle-manifest.schema.json"]
    required = set(manifest.get("required", []))
    for key in {"semantic_digest", "package_digest", "change_class", "material_view_reconciliation"}:
        if key not in required:
            errors.append(f"ResearchBundleManifest must require {key}")

    common_defs = schemas["common.schema.json"].get("$defs", {})
    expected_change = {"EDITORIAL", "EVIDENCE", "SEMANTIC", "SCOPE", "EXAM_DEMAND", "ASSET"}
    actual_change = set(common_defs.get("change_class", {}).get("enum", []))
    if actual_change != expected_change:
        errors.append(f"change_class enum drift: {sorted(actual_change)}")

    expected_rights = {
        "REPRODUCTION_ALLOWED",
        "REFERENCE_ONLY",
        "USER_SUPPLIED_LIMITED",
        "DISCOVERY_ONLY",
        "UNKNOWN_REVIEW_REQUIRED",
    }
    actual_rights = set(common_defs.get("rights_status", {}).get("enum", []))
    if actual_rights != expected_rights:
        errors.append(f"rights_status enum drift: {sorted(actual_rights)}")

    expected_dispositions = {"REQUIRED", "DEFER", "EXCLUDE", "REVIEW", "DUPLICATE"}
    actual_dispositions = set(common_defs.get("question_disposition", {}).get("enum", []))
    if actual_dispositions != expected_dispositions:
        errors.append(f"question_disposition enum drift: {sorted(actual_dispositions)}")

    learner = schemas["learner-profile.schema.json"]
    if "baselines" not in set(learner.get("required", [])):
        errors.append("LearnerProfile must require per-subtopic baselines")

    gap = schemas["core1-research-gap.schema.json"]
    if gap.get("properties", {}).get("status", {}).get("const") != "CORE1_RESEARCH_GAP":
        errors.append("Core1ResearchGap status must be CORE1_RESEARCH_GAP")

    return errors


def validate_examples(schemas: dict[str, dict], base_uri: str, store: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    if not EXAMPLE_DIR.exists():
        return errors

    mapping = {
        "scope-graph.example.json": "scope-graph.schema.json",
        "learner-profile.example.json": "learner-profile.schema.json",
        "publication-target.example.json": "publication-target.schema.json",
        "source-ledger.example.json": "source-ledger.schema.json",
        "exam-demand-profile.example.json": "exam-demand-profile.schema.json",
        "question-evidence-ledger.example.json": "question-evidence-ledger.schema.json",
        "research-bundle.example.json": "research-bundle.schema.json",
        "research-bundle-manifest.example.json": "research-bundle-manifest.schema.json",
        "core1-research-gap.example.json": "core1-research-gap.schema.json",
    }

    for example_name, schema_name in mapping.items():
        path = EXAMPLE_DIR / example_name
        if not path.exists():
            continue
        instance = load_json(path)
        schema = schemas[schema_name]
        resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
        validator = Draft202012Validator(schema, resolver=resolver)
        for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
            where = ".".join(str(p) for p in err.absolute_path) or "<root>"
            errors.append(f"{example_name}:{where}: {err.message}")
    return errors


def main() -> int:
    if not SCHEMA_FILES:
        print("No schema files found", file=sys.stderr)
        return 2

    schemas: dict[str, dict] = {}
    errors: list[str] = []

    for path in SCHEMA_FILES:
        try:
            schema = load_json(path)
            Draft202012Validator.check_schema(schema)
            schemas[path.name] = schema
        except Exception as exc:  # schema/meta-schema error should be blocking
            errors.append(f"{path.name}: {exc}")

    required_names = {
        "common.schema.json",
        "scope-graph.schema.json",
        "learner-profile.schema.json",
        "publication-target.schema.json",
        "research-claim.schema.json",
        "representation-requirement.schema.json",
        "source-ledger.schema.json",
        "exam-demand-profile.schema.json",
        "question-evidence-ledger.schema.json",
        "research-bundle.schema.json",
        "research-bundle-manifest.schema.json",
        "core1-research-gap.schema.json",
    }
    missing = sorted(required_names - schemas.keys())
    if missing:
        errors.append(f"Missing frozen schemas: {', '.join(missing)}")

    if not errors:
        errors.extend(check_architecture_invariants(schemas))
        base_uri, store = build_store(schemas)
        errors.extend(validate_examples(schemas, base_uri, store))

    if errors:
        print("CONTRACT_SCHEMA_FREEZE_V1 = FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"CONTRACT_SCHEMA_FREEZE_V1 = PASS ({len(schemas)} schemas)")
    print("BXX_OUTSIDE_RESEARCH_BUNDLE = PASS")
    print("MANIFEST_NO_SELF_HASH = PASS")
    print("CHANGE_CLASS_ENUM = PASS")
    print("RIGHTS_USE_ENUM = PASS")
    print("QUESTION_DISPOSITION_ENUM = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
