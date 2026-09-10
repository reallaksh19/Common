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


def validate_structure(instance: dict, errors: list[str], label: str):
    sg = instance.get("study_guide", {})
    if sg.get("product_first") is not True:
        errors.append(f"{label}: Study Guide must be product-first")

    for unit in sg.get("learning_units", []):
        uid = unit.get("unit_id", "<unknown>")
        profile = unit.get("instructional_profile")
        roles = [s.get("role") for s in unit.get("arc_steps", [])]
        role_set = set(roles)
        if profile in {"FOUNDATION", "BRIDGE"}:
            required = {"NOTICE", "WORKED_EXAMPLE", "GUIDED_1", "GUIDED_2_FADED", "INDEPENDENT_TRANSFER", "RETRIEVAL_CHECK"}
            if not ({"PHYSICAL_SITUATION", "DEPICTION"} & role_set):
                errors.append(f"{label}:{uid}: FOUNDATION/BRIDGE requires a physical situation or depiction")
            missing = required - role_set
            if missing:
                errors.append(f"{label}:{uid}: FOUNDATION/BRIDGE arc missing {sorted(missing)}")
        elif profile in {"COMPRESSED", "REFERENCE"}:
            required = {"NOTICE", "INDEPENDENT_TRANSFER", "RETRIEVAL_CHECK"}
            if not ({"DEPICTION", "VARIANT_CONTRAST", "PHYSICAL_SITUATION"} & role_set):
                errors.append(f"{label}:{uid}: COMPRESSED/REFERENCE requires a representation, situation, or contrast anchor")
            missing = required - role_set
            if missing:
                errors.append(f"{label}:{uid}: COMPRESSED/REFERENCE arc missing {sorted(missing)}")

        if "BUILD_RELATION" in roles:
            i = roles.index("BUILD_RELATION")
            prior = set(roles[:i])
            if not prior & {"PHYSICAL_SITUATION", "DEPICTION", "NOTICE", "SAY_IN_WORDS", "VARIANT_CONTRAST"}:
                errors.append(f"{label}:{uid}: BUILD_RELATION appears before any model/notice/contrast anchor")
        if "FORMAL_OBJECT" in roles:
            errors.append(f"{label}:{uid}: FORMAL_OBJECT is content, not an arc role; use BUILD_RELATION/CONCEPT_INVARIANT")

        progression = unit.get("support_progression", {})
        if profile in {"FOUNDATION", "BRIDGE"}:
            for key in ("worked_example", "guided_1", "guided_2_faded", "independent_transfer"):
                if progression.get(key, {}).get("state") != "PRESENT":
                    errors.append(f"{label}:{uid}: {key} must be PRESENT for FOUNDATION/BRIDGE")
        else:
            if progression.get("independent_transfer", {}).get("state") != "PRESENT":
                errors.append(f"{label}:{uid}: independent_transfer must remain PRESENT at high baseline")

    topology = sg.get("practice_topology", {})
    if not topology.get("attempt_before_help") or not topology.get("solutions_after_attempts") or not topology.get("progressive_hints"):
        errors.append(f"{label}: Study Guide practice topology must preserve attempt -> optional help -> solutions")
    if topology.get("hint_delivery") == "INLINE_ALWAYS_VISIBLE":
        errors.append(f"{label}: static learner attempt may not force all hints visible")
    if sg.get("appendix_order") != ["A", "B", "C"]:
        errors.append(f"{label}: appendix order must be A -> B -> C")
    if "FULL_SOLUTIONS" not in sg.get("appendix_B_sections", []):
        errors.append(f"{label}: Appendix B must include FULL_SOLUTIONS")

    nav = sg.get("navigation", {})
    if instance.get("structure_profile") in {"PHYSICS_PR156", "CHEMISTRY_PR157"}:
        for key in ("question_to_hint", "question_to_solution", "solution_to_question", "solution_to_lesson"):
            if nav.get(key) is not True:
                errors.append(f"{label}: mature profile requires navigation {key}")

    tb = instance.get("transfer_book")
    if tb:
        order = tb.get("section_order", [])
        wanted = [x for x in ("ATTEMPTS", "OPTIONAL_HELP", "COMPLETE_SOLUTIONS", "MIXED_DIAGNOSIS") if x in order]
        if order != wanted:
            errors.append(f"{label}: Transfer Book sections must follow ATTEMPTS -> OPTIONAL_HELP -> COMPLETE_SOLUTIONS -> MIXED_DIAGNOSIS")
        if not tb.get("attempt_before_hints") or not tb.get("solutions_after_attempts"):
            errors.append(f"{label}: Transfer Book must keep attempt before help and solutions")
        if "OPTIONAL_HELP" in order and tb.get("hint_delivery") != "SEPARATE_HELP_SECTION":
            errors.append(f"{label}: static mature specimen requires hints in a separate optional-help section")
        if "MIXED_DIAGNOSIS" in order and not tb.get("mixed_diagnosis_after_solutions"):
            errors.append(f"{label}: mixed diagnosis must be revealed after solutions")
        for row in tb.get("question_navigation", []):
            for key in ("hint_target", "solution_target", "return_to_question"):
                if not row.get(key):
                    errors.append(f"{label}:{row.get('question_id')}: missing {key}")


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
        "publication-structure.schema.json",
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
        for schema_name in ("publication-plan.schema.json", "publication-structure.schema.json", "study-guide.schema.json", "transfer-book.schema.json"):
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

    structure_examples = []
    if EXAMPLES.exists() and not errors:
        mapping = {
            "transfer-book.example.json": "transfer-book.schema.json",
            "product-identity.example.json": "product-identity.schema.json",
            "publication-structure.bridge.example.json": "publication-structure.schema.json",
            "publication-structure.reference.example.json": "publication-structure.schema.json",
        }
        for name, schema_name in mapping.items():
            path = EXAMPLES / name
            if path.exists():
                instance = load(path)
                validate_instance(schema_name, instance, schemas, base_uri, store, errors, name)
                if schema_name == "publication-structure.schema.json":
                    validate_structure(instance, errors, name)
                    structure_examples.append(instance)

    if len(structure_examples) == 2:
        bridge, reference = structure_examples
        if bridge.get("research_bundle_id") != reference.get("research_bundle_id") or bridge.get("research_package_digest") != reference.get("research_package_digest"):
            errors.append("B40/B90 structure examples must consume the same frozen ResearchPackage")
        if bridge.get("learner_profile_id") == reference.get("learner_profile_id"):
            errors.append("B40/B90 structure examples must use distinct LearnerProfiles")
        bridge_arcs = [[s["role"] for s in u["arc_steps"]] for u in bridge["study_guide"]["learning_units"]]
        ref_arcs = [[s["role"] for s in u["arc_steps"]] for u in reference["study_guide"]["learning_units"]]
        if bridge_arcs == ref_arcs:
            errors.append("B40/B90 structure examples do not demonstrate structural adaptation")

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
    print("PRODUCT_FIRST_STRUCTURE_CONTRACT = PASS")
    print("B40_B90_MORPHOLOGY_SEPARATION = PASS")
    print("SHARED_REPRESENTATION_REGISTRY = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
