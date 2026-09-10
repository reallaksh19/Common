#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "learning-design.schema.json"
EXAMPLE = ROOT / "examples" / "learning-design.permutations-bridge.example.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(instance: dict) -> list[str]:
    schema = load(SCHEMA)
    base_uri = ROOT.as_uri().rstrip("/") + "/"
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store={
        SCHEMA.name: schema,
        schema.get("$id", SCHEMA.name): schema,
        base_uri + SCHEMA.name: schema,
        base_uri + schema.get("$id", SCHEMA.name): schema,
    })
    out = []
    for err in Draft202012Validator(schema, resolver=resolver).iter_errors(instance):
        loc = ".".join(str(x) for x in err.absolute_path) or "<root>"
        out.append(f"{loc}: {err.message}")
    return out


def validate_semantics(instance: dict) -> list[str]:
    errors: list[str] = []
    unit_ids = {u.get("unit_id") for u in instance.get("learning_units", [])}

    for unit in instance.get("learning_units", []):
        uid = unit.get("unit_id", "<unknown>")
        capabilities = unit.get("learner_capabilities", [])
        cap_ids = {c.get("capability_id") for c in capabilities}
        required = {c.get("capability_id") for c in capabilities if c.get("required") is True}
        covered = {r for p in unit.get("completion_probes", []) for r in p.get("capability_refs", [])}
        if required - covered:
            errors.append(f"{uid}: required capabilities missing completion probes: {sorted(required - covered)}")
        if covered - cap_ids:
            errors.append(f"{uid}: completion probes reference unknown capabilities: {sorted(covered - cap_ids)}")

        progression = unit.get("support_progression", {})
        if unit.get("instructional_profile") in {"FOUNDATION", "BRIDGE"}:
            previous = None
            for name in ("worked", "guided_1", "guided_2", "independent"):
                stage = progression.get(name, {})
                if stage.get("state") != "PRESENT":
                    errors.append(f"{uid}: {name} must be PRESENT for FOUNDATION/BRIDGE")
                    continue
                features = set(stage.get("support_features", []))
                if previous is not None:
                    removed = previous - features
                    declared = set(stage.get("removed_since_previous", []))
                    if not removed:
                        errors.append(f"{uid}: {name} removes no support; fading is only nominal")
                    if declared != removed:
                        errors.append(f"{uid}: {name} declared support removal does not match actual removal")
                    if features - previous:
                        errors.append(f"{uid}: {name} adds support during a fading sequence")
                previous = features

        transfer = unit.get("transfer_design", {})
        if transfer.get("required") is True:
            dims = set(transfer.get("changed_dimensions", []))
            if not dims or dims <= {"NUMBER_CHANGE"}:
                errors.append(f"{uid}: number change alone cannot satisfy transfer")
            required_types = {c.get("type") for c in capabilities if c.get("required") is True}
            if "TRANSFER" not in required_types:
                errors.append(f"{uid}: required transfer has no required TRANSFER capability")

    bridge = instance.get("exam_bridge")
    if bridge:
        for family in bridge.get("question_families", []):
            unknown = set(family.get("learning_unit_refs", [])) - unit_ids
            if unknown:
                errors.append(f"{family.get('question_family_id')}: unknown learning unit refs {sorted(unknown)}")
            if not family.get("recognition_requirements"):
                errors.append(f"{family.get('question_family_id')}: missing recognition requirements")
            if not family.get("failure_models"):
                errors.append(f"{family.get('question_family_id')}: missing failure models")

    if instance.get("mode") == "MATURE_LEARNER_PRODUCT":
        review = instance.get("review_requirements", {})
        for key in ("pedagogy_review_required", "subject_review_required", "exact_artifact_binding_required"):
            if review.get(key) is not True:
                errors.append(f"mature learner product must require {key}")
    return errors


def main() -> int:
    errors: list[str] = []
    schema = load(SCHEMA)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        errors.append(f"schema: {exc}")

    example = load(EXAMPLE)
    errors.extend("schema: " + e for e in validate_schema(example))
    errors.extend("semantic: " + e for e in validate_semantics(example))

    if errors:
        print("CORE2_LEARNING_DESIGN_V1 = FAIL")
        for error in errors:
            print("- " + error)
        return 1

    print("CORE2_LEARNING_DESIGN_SCHEMA = PASS")
    print("LEARNER_CAPABILITY_COVERAGE = PASS")
    print("SUPPORT_FADING_SEMANTICS = PASS")
    print("TRANSFER_DIFFERENTIATION = PASS")
    print("EXAM_BRIDGE_STRUCTURE = PASS")
    print("CORE2_LEARNING_DESIGN_V1 = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
