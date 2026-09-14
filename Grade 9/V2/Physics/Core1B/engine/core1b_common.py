from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence, Set

FORBIDDEN_LEARNER_TOKENS = (
    "ATOM_",
    "DIAGNOSTIC_BRANCH",
    "STATE_FRAGILE",
    "REPAIR_",
    "TRANSFER_READY",
)

REQUIRED_READINESS = ("recognise", "represent", "first_move", "finish", "check")


class Core1BValidationError(ValueError):
    pass


def _atom_map(registry: Mapping) -> Dict[str, Mapping]:
    atoms = registry.get("atoms", [])
    result = {}
    for atom in atoms:
        atom_id = atom.get("atom_id")
        if not atom_id or atom_id in result:
            raise Core1BValidationError(f"invalid or duplicate atom_id: {atom_id!r}")
        result[atom_id] = atom
    if not result:
        raise Core1BValidationError("atom registry must not be empty")
    return result


def validate_atom_registry(registry: Mapping) -> None:
    atoms = _atom_map(registry)
    for atom_id, atom in atoms.items():
        for key in ("proposition", "representation", "micro_check", "merge_target"):
            if not atom.get(key):
                raise Core1BValidationError(f"{atom_id} missing {key}")
        for ref in atom.get("prerequisites", []):
            if ref not in atoms:
                raise Core1BValidationError(f"{atom_id} has unknown prerequisite {ref}")
        for ref in atom.get("repair_routes", []):
            if ref not in atoms:
                raise Core1BValidationError(f"{atom_id} has unknown repair route {ref}")

    visiting: Set[str] = set()
    visited: Set[str] = set()

    def visit(atom_id: str) -> None:
        if atom_id in visited:
            return
        if atom_id in visiting:
            raise Core1BValidationError(f"prerequisite cycle detected at {atom_id}")
        visiting.add(atom_id)
        for prereq in atoms[atom_id].get("prerequisites", []):
            visit(prereq)
        visiting.remove(atom_id)
        visited.add(atom_id)

    for atom_id in atoms:
        visit(atom_id)


def validate_unit(unit: Mapping, registry: Mapping) -> None:
    atoms = _atom_map(registry)
    if unit.get("subject") != "PHYSICS":
        raise Core1BValidationError("unit subject must be PHYSICS")
    if not unit.get("authority_refs"):
        raise Core1BValidationError("unit requires authority_refs")
    if not unit.get("atom_refs"):
        raise Core1BValidationError("unit requires atom_refs")
    unknown = [ref for ref in unit["atom_refs"] if ref not in atoms]
    if unknown:
        raise Core1BValidationError(f"unit references unknown atoms: {unknown}")

    included = set(unit["atom_refs"])
    for ref in unit["atom_refs"]:
        missing = [p for p in atoms[ref].get("prerequisites", []) if p not in included]
        if missing:
            raise Core1BValidationError(f"unit atom {ref} omits prerequisites {missing}")

    surface = unit.get("learner_surface", {})
    surface_text = "\n".join(
        [*surface.get("teacher_moves", []), surface.get("worked_example", ""), surface.get("independent_task", "")]
    )
    upper_surface = surface_text.upper()
    leaked = [token for token in FORBIDDEN_LEARNER_TOKENS if token in upper_surface]
    if leaked:
        raise Core1BValidationError(f"internal runtime labels leaked to learner surface: {leaked}")

    readiness = unit.get("readiness", {})
    missing_readiness = [name for name in REQUIRED_READINESS if readiness.get(name) is not True]
    if missing_readiness:
        raise Core1BValidationError(f"release readiness incomplete: {missing_readiness}")


def build_independent_evidence(unit: Mapping, learner_profile_ref: str, problem_family_ref: str) -> dict:
    readiness = unit["readiness"]
    return {
        "schema_version": "0.1.0",
        "learner_profile_ref": learner_profile_ref,
        "capability_id": unit["capability_id"],
        "problem_family_ref": problem_family_ref,
        "state": "INDEPENDENT",
        "evidence": {
            "recognise": "PASS" if readiness["recognise"] else "FAIL",
            "represent": "PASS" if readiness["represent"] else "FAIL",
            "explain": "PASS" if readiness.get("explain") else "UNTESTED",
            "model_select": "PASS",
            "first_move": "PASS" if readiness["first_move"] else "FAIL",
            "finish": "PASS" if readiness["finish"] else "FAIL",
            "check": "PASS" if readiness["check"] else "FAIL",
            "delayed_retrieval": "UNTESTED",
        },
        "hint_history": [],
        "error_history": [],
        "representation_coverage": ["EVENT_TIMELINE", "SIGNED_VERTICAL_VELOCITY", "VY_T_GRAPH"],
        "evidence_refs": [f"{unit['unit_id']}:INDEPENDENT_TASK"],
    }


def build_release_receipt(unit: Mapping, evidence_ref: str, teaching_receipt_ref: str, problem_family_ref: str) -> dict:
    return {
        "schema_version": "0.1.0",
        "receipt_id": f"C1B-REL-{unit['unit_id']}",
        "capability_id": unit["capability_id"],
        "teaching_receipt_ref": teaching_receipt_ref,
        "learner_evidence_ref": evidence_ref,
        "minimum_state": "INDEPENDENT",
        "released_problem_family_refs": [problem_family_ref],
        "representation_evidence": ["EVENT_TIMELINE", "SIGNED_VERTICAL_VELOCITY", "VY_T_GRAPH"],
        "unresolved_required_atoms": [],
    }
