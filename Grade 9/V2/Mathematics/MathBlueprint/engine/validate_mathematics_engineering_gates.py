#!/usr/bin/env python3
"""Deterministic validator for the Mathematics Technical Engineering Gate Registry.

Runtime logic is deliberately topic-agnostic. Mathematical requirements live in
Engineering data; this validator understands only generic invariant categories,
graph integrity, schema contracts, readiness rules and falsification mechanics.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as SchemaValidationError

from engineering_registry_composition import (
    BASE_REGISTRY_REL,
    load_canonical_engineering_registry,
)

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_REGISTRY_PATH = ROOT / BASE_REGISTRY_REL
INVARIANT_PROFILE_PATH = ROOT / "policies" / "mathematics-engineering-gate-invariants.v1.json"


class MathematicsEngineeringGateValidationError(Exception):
    """Structured validation error with stable machine-readable code."""

    def __init__(self, code: str, message: str, context: dict | None = None):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message
        self.context = context or {}


def load_json(path: Path) -> dict:
    path = Path(path)
    if path.resolve() == CANONICAL_REGISTRY_PATH.resolve():
        return load_canonical_engineering_registry(path)
    return json.loads(path.read_text(encoding="utf-8"))


def load_invariant_profile(path: Path = INVARIANT_PROFILE_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_gate_schema(registry: dict) -> None:
    schema_path = ROOT / "contracts" / "mathematics-technical-engineering-gate.schema.json"
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    try:
        validator.validate(registry)
    except SchemaValidationError as e:
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_SCHEMA_VIOLATION", str(e), {"path": list(e.path)}
        )


def validate_invariant_profile(profile: dict, registry: dict) -> dict[str, dict]:
    required_top = {"schema_version", "subject", "profile_id", "gate_invariants"}
    missing = sorted(required_top - set(profile))
    if missing or profile.get("schema_version") != "1.0.0" or profile.get("subject") != "MATHEMATICS":
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_INVARIANT_PROFILE_SCHEMA",
            f"missing={missing}",
        )

    rows = profile.get("gate_invariants")
    if not isinstance(rows, list):
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_INVARIANT_PROFILE_SCHEMA",
            "gate_invariants must be a list",
        )

    required_row = {
        "gate_id",
        "required_concept_ids",
        "required_equation_ids",
        "required_representation_ids",
        "required_misconception_ids",
        "required_prerequisite_ids",
    }
    registry_ids = {gate["subtopic_id"] for gate in registry.get("subtopic_gates", [])}
    out: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_INVARIANT_PROFILE_SCHEMA",
                f"row must be object: {row!r}",
            )
        missing_row = sorted(required_row - set(row))
        if missing_row:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_INVARIANT_PROFILE_SCHEMA",
                f"{row.get('gate_id')}: missing={missing_row}",
            )
        gate_id = row["gate_id"]
        if not isinstance(gate_id, str) or not gate_id.startswith("MATH-"):
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_INVARIANT_PROFILE_SCHEMA",
                f"invalid gate_id={gate_id!r}",
            )
        if gate_id in out:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_INVARIANT_PROFILE_DUPLICATE_GATE",
                gate_id,
            )
        if gate_id not in registry_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_INVARIANT_PROFILE_UNKNOWN_GATE",
                gate_id,
            )
        for key in required_row - {"gate_id"}:
            values = row[key]
            if not isinstance(values, list) or len(values) != len(set(values)) or any(
                not isinstance(value, str) or not value for value in values
            ):
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_INVARIANT_PROFILE_SCHEMA",
                    f"{gate_id}:{key}",
                )
        out[gate_id] = row
    return out


def _validate_dependency_cycles(registry: dict) -> None:
    gates = {gate["subtopic_id"]: gate for gate in registry["subtopic_gates"]}
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(gate_id: str) -> None:
        if gate_id in visited:
            return
        if gate_id in visiting:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_DEPENDENCY_CYCLE",
                gate_id,
            )
        visiting.add(gate_id)
        for prereq in gates[gate_id].get("prerequisite_ids", []):
            if isinstance(prereq, str) and prereq.startswith("MATH-"):
                walk(prereq)
        visiting.remove(gate_id)
        visited.add(gate_id)

    for gate_id in gates:
        walk(gate_id)


def validate_global_invariants(registry: dict) -> None:
    seen_subtopics: set[str] = set()
    seen_concepts: set[str] = set()
    seen_equations: set[str] = set()
    seen_reps: set[str] = set()
    seen_misconceptions: set[str] = set()

    for gate in registry["subtopic_gates"]:
        sub_id = gate["subtopic_id"]
        if sub_id in seen_subtopics:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_DUPLICATE_ID", f"Duplicate subtopic ID: {sub_id}"
            )
        seen_subtopics.add(sub_id)

        for collection, key, seen in (
            (gate["technical_core"], "concept_id", seen_concepts),
            (gate["mandatory_equations"], "equation_id", seen_equations),
            (gate["representations"], "representation_id", seen_reps),
            (gate["misconceptions"], "misconception_id", seen_misconceptions),
        ):
            for row in collection:
                item_id = row[key]
                if item_id in seen:
                    raise MathematicsEngineeringGateValidationError(
                        "MATH_GATE_DUPLICATE_ID", f"Duplicate {key}: {item_id}"
                    )
                seen.add(item_id)

    for gate in registry["subtopic_gates"]:
        for prereq in gate.get("prerequisite_ids", []):
            if prereq.startswith("MATH-") and prereq not in seen_subtopics:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_UNRESOLVED_PREREQUISITE",
                    f"Subtopic {gate['subtopic_id']} has unresolved prerequisite {prereq}",
                )
            if prereq == gate["subtopic_id"]:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_UNRESOLVED_PREREQUISITE",
                    f"Subtopic {gate['subtopic_id']} has self-dependency",
                )

    _validate_dependency_cycles(registry)


def _require_ids(
    gate_id: str,
    actual: set[str],
    required: list[str],
    code: str,
    category: str,
) -> None:
    missing = sorted(set(required) - actual)
    if missing:
        raise MathematicsEngineeringGateValidationError(
            code,
            f"{gate_id} missing required {category}: {missing}",
            {"gate_id": gate_id, "category": category, "missing": missing},
        )


def validate_subtopic_invariants(gate: dict, invariant: dict | None = None) -> None:
    sub_id = gate["subtopic_id"]

    if not sub_id.startswith("MATH-"):
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_INVALID_SUBTOPIC_ID", f"Invalid subtopic ID format: {sub_id}"
        )
    if gate.get("maturity") != "ENGINEERING":
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_MATURITY_OVERREACH",
            f"Maturity must be ENGINEERING, got {gate.get('maturity')}",
        )

    defined_fams = {f["family_id"] for f in gate.get("problem_families", [])}
    for linked_family_id in gate.get("linked_problem_family_ids", []):
        if linked_family_id not in defined_fams:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_CROSS_REFERENCE_INTEGRITY_FAIL",
                f"Linked problem family {linked_family_id} not defined in problem_families of {sub_id}",
            )

    concept_ids = {c["concept_id"] for c in gate.get("technical_core", [])}
    equation_ids = {e["equation_id"] for e in gate.get("mandatory_equations", [])}
    representation_ids = {r["representation_id"] for r in gate.get("representations", [])}
    misconception_ids = {m["misconception_id"] for m in gate.get("misconceptions", [])}
    prerequisite_ids = set(gate.get("prerequisite_ids", []))

    if invariant is not None:
        _require_ids(
            sub_id,
            concept_ids,
            invariant["required_concept_ids"],
            "MATH_GATE_MISSING_REQUIRED_CONCEPT",
            "concept IDs",
        )
        _require_ids(
            sub_id,
            equation_ids,
            invariant["required_equation_ids"],
            "MATH_GATE_MISSING_MANDATORY_EQUATION",
            "equation IDs",
        )
        _require_ids(
            sub_id,
            representation_ids,
            invariant["required_representation_ids"],
            "MATH_GATE_MISSING_MANDATORY_REPRESENTATION",
            "representation IDs",
        )
        _require_ids(
            sub_id,
            misconception_ids,
            invariant["required_misconception_ids"],
            "MATH_GATE_MISSING_MISCONCEPTION_TRAP",
            "misconception IDs",
        )
        _require_ids(
            sub_id,
            prerequisite_ids,
            invariant["required_prerequisite_ids"],
            "MATH_GATE_UNRESOLVED_PREREQUISITE",
            "prerequisite IDs",
        )

    dp = gate["difficulty_profile"]
    dims = [
        "prerequisite_depth",
        "element_interactivity",
        "inferential_jump_severity",
        "representation_translation",
        "model_discrimination",
        "sign_or_frame_sensitivity",
        "multi_step_dependency",
        "abstraction",
        "misconception_density",
        "synthesis",
    ]
    for dimension in dims:
        if not (0 <= dp.get(dimension, -1) <= 3):
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_INVALID_DIFFICULTY_PROFILE",
                f"Dimension {dimension} must be 0-3",
            )
    if dp.get("maturity") != "ENGINEERING":
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_INVALID_DIFFICULTY_PROFILE",
            "Difficulty profile maturity must be ENGINEERING",
        )

    checklist = gate["release_checklist"]
    if gate["technical_readiness"] == "ENGINEERING_GATE_READY":
        for field, status in checklist.items():
            if status is not True:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_RELEASE_CHECKLIST_INCOMPLETE",
                    f"Release checklist field {field} must be True for READY gate in {sub_id}",
                )


def validate(registry: dict) -> list[str]:
    validate_gate_schema(registry)
    validate_global_invariants(registry)
    invariant_by_gate = validate_invariant_profile(load_invariant_profile(), registry)
    validated_subtopics = []
    for gate in registry["subtopic_gates"]:
        validate_subtopic_invariants(gate, invariant_by_gate.get(gate["subtopic_id"]))
        validated_subtopics.append(gate["subtopic_id"])
    return validated_subtopics


def run_falsification_battery() -> None:
    """Generate mutation falsifiers from invariant data rather than topic names."""
    clean_registry = load_json(CANONICAL_REGISTRY_PATH)
    invariant_by_gate = validate_invariant_profile(load_invariant_profile(), clean_registry)
    falsifier_count = 0

    def expect_rejection(mutated: dict, expected_code: str) -> None:
        nonlocal falsifier_count
        try:
            validate(mutated)
        except MathematicsEngineeringGateValidationError as err:
            if err.code != expected_code:
                raise AssertionError(
                    f"Expected code {expected_code}, got {err.code}: {err.message}"
                )
            falsifier_count += 1
            return
        except Exception as err:
            raise AssertionError(
                f"Expected MathematicsEngineeringGateValidationError [{expected_code}], got {type(err).__name__}: {err}"
            )
        raise AssertionError(
            f"Expected validator rejection with code [{expected_code}], but validation passed!"
        )

    category_specs = (
        ("required_concept_ids", "technical_core", "concept_id", "MATH_GATE_MISSING_REQUIRED_CONCEPT"),
        ("required_equation_ids", "mandatory_equations", "equation_id", "MATH_GATE_MISSING_MANDATORY_EQUATION"),
        ("required_representation_ids", "representations", "representation_id", "MATH_GATE_MISSING_MANDATORY_REPRESENTATION"),
        ("required_misconception_ids", "misconceptions", "misconception_id", "MATH_GATE_MISSING_MISCONCEPTION_TRAP"),
        ("required_prerequisite_ids", "prerequisite_ids", None, "MATH_GATE_UNRESOLVED_PREREQUISITE"),
    )
    for gate_id, invariant in invariant_by_gate.items():
        for invariant_key, collection_key, item_key, error_code in category_specs:
            required = invariant[invariant_key]
            if not required:
                continue
            target = required[0]
            mutated = copy.deepcopy(clean_registry)
            gate = next(row for row in mutated["subtopic_gates"] if row["subtopic_id"] == gate_id)
            if item_key is None:
                gate[collection_key] = [value for value in gate[collection_key] if value != target]
            else:
                target_row = next(
                    (row for row in gate[collection_key] if row[item_key] == target),
                    None,
                )
                if target_row is None:
                    raise AssertionError(f"Invariant target absent before mutation: {gate_id}:{target}")
                target_row[item_key] = target + "-FALSIFIER-MISSING"
            expect_rejection(mutated, error_code)

    bad_cross_ref = copy.deepcopy(clean_registry)
    first_gate = bad_cross_ref["subtopic_gates"][0]
    first_gate["linked_problem_family_ids"].append("PF-MATH-ORPHAN-FAMILY-FALSIFIER")
    expect_rejection(bad_cross_ref, "MATH_GATE_CROSS_REFERENCE_INTEGRITY_FAIL")

    bad_duplicate = copy.deepcopy(clean_registry)
    bad_duplicate["subtopic_gates"][0]["technical_core"].append(
        copy.deepcopy(bad_duplicate["subtopic_gates"][1]["technical_core"][0])
    )
    expect_rejection(bad_duplicate, "MATH_GATE_DUPLICATE_ID")

    bad_checklist = copy.deepcopy(clean_registry)
    ready_gate = next(
        gate for gate in bad_checklist["subtopic_gates"]
        if gate["technical_readiness"] == "ENGINEERING_GATE_READY"
    )
    ready_gate["release_checklist"]["provenance_verified"] = False
    expect_rejection(bad_checklist, "MATH_GATE_RELEASE_CHECKLIST_INCOMPLETE")

    print(
        "Mathematics Technical Engineering Gate falsification battery: PASS "
        f"({falsifier_count} data-derived mutation falsifiers caught by production validator)"
    )


if __name__ == "__main__":
    registry = load_json(CANONICAL_REGISTRY_PATH)
    subtopics = validate(registry)
    print(f"Validated {len(subtopics)} Mathematics Technical Engineering subtopic gates: PASS")
    run_falsification_battery()
