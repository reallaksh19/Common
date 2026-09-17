#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from build_physics_engineering_gate_registry_v3 import build_registry, digest  # noqa: E402


class PhysicsEngineeringGateV3Error(Exception):
    def __init__(self, code: str, message: str, context: dict | None = None):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message
        self.context = context or {}


def fail(code: str, message: str, context: dict | None = None) -> None:
    raise PhysicsEngineeringGateV3Error(code, message, context)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _ids(rows: list[dict], key: str) -> set[str]:
    return {row[key] for row in rows}


def _require_subset(gate_id: str, category: str, actual: set[str], required: set[str], code: str) -> None:
    missing = sorted(required - actual)
    if missing:
        fail(code, f"{gate_id} missing {category}: {missing}", {"gate_id": gate_id, "missing": missing})


def validate_schema(registry: dict) -> None:
    schema = load("contracts/physics-technical-engineering-gate-v3.schema.json")
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(registry), key=lambda e: list(e.path))
    if errors:
        err = errors[0]
        fail("PHY_GATE_SCHEMA_VIOLATION", err.message, {"path": list(err.path)})


def validate(registry: dict | None = None, invariant_profile: dict | None = None) -> dict:
    registry = registry if registry is not None else build_registry()
    profile = invariant_profile if invariant_profile is not None else load("policy/physics-engineering-gate-invariants.v3.json")
    validate_schema(registry)

    gates = registry["gates"]
    gate_map = {g["subtopic_id"]: g for g in gates}
    if len(gate_map) != len(gates):
        fail("PHY_GATE_DUPLICATE_ID", "duplicate subtopic_id")

    required_gate_ids = set(profile["required_gates"])
    if set(gate_map) != required_gate_ids:
        fail("PHY_GATE_CANONICAL_SET_MISMATCH", f"expected={sorted(required_gate_ids)} actual={sorted(gate_map)}")

    # Canonical semantic assets are globally unique. Problem-family IDs are intentionally
    # reusable across gates (e.g. incline or Atwood) because each gate contributes a
    # gate-specific engineering view of the same family; family uniqueness is local below.
    global_ids: dict[str, str] = {}
    categories = [
        ("concepts", "concept_id"), ("relations", "relation_id"),
        ("representations", "representation_id"), ("misconceptions", "misconception_id"),
        ("required_transformations", "transformation_id"),
    ]
    for gate in gates:
        gid = gate["subtopic_id"]
        for collection, key in categories:
            for row in gate[collection]:
                value = row[key]
                if value in global_ids:
                    fail("PHY_GATE_DUPLICATE_ASSET_ID", f"{value} appears in {global_ids[value]} and {gid}")
                global_ids[value] = gid

    # Physics prerequisite graph must resolve and be acyclic. External Mathematics prerequisites remain visible but are not walked here.
    visiting: list[str] = []
    seen: set[str] = set()
    def walk(gid: str) -> None:
        if gid in seen:
            return
        if gid in visiting:
            cycle = visiting[visiting.index(gid):] + [gid]
            fail("PHY_GATE_DEPENDENCY_CYCLE", " -> ".join(cycle))
        visiting.append(gid)
        for prereq in gate_map[gid]["prerequisites"]:
            if prereq.startswith("PHY-"):
                if prereq not in gate_map:
                    fail("PHY_GATE_PREREQUISITE_UNKNOWN", f"{gid} references unknown Physics prerequisite {prereq}")
                walk(prereq)
        visiting.pop()
        seen.add(gid)
    for gid in gate_map:
        walk(gid)

    derived_states: list[dict] = []
    for gate in gates:
        gid = gate["subtopic_id"]
        spec = profile["required_gates"][gid]
        authority = gate["authority_basis"]
        if gate["scope_state"] == "ACTIVE" and any(a["claim_class"] == "SOURCE_SCOPE_HELD" for a in authority):
            fail("PHY_GATE_SOURCE_SCOPE_HELD", f"{gid} cannot be ACTIVE while authority is source-scope held")

        for concept in gate["concepts"]:
            if concept["authority_ref"] >= len(authority):
                fail("PHY_GATE_AUTHORITY_REF_INVALID", f"{gid}:{concept['concept_id']} authority_ref is out of range")

        concept_ids = _ids(gate["concepts"], "concept_id")
        relation_ids = _ids(gate["relations"], "relation_id")
        representation_ids = _ids(gate["representations"], "representation_id")
        invariant_ids = set(gate["required_invariants"])
        verification_ids = set(gate["verifications"])
        prereq_ids = set(gate["prerequisites"])

        _require_subset(gid, "invariants", invariant_ids, set(spec.get("required_invariants", [])), "PHY_GATE_REQUIRED_INVARIANT_MISSING")
        _require_subset(gid, "concepts", concept_ids, set(spec.get("required_concepts", [])), "PHY_GATE_REQUIRED_CONCEPT_MISSING")
        _require_subset(gid, "relations", relation_ids, set(spec.get("required_relations", [])), "PHY_GATE_REQUIRED_RELATION_MISSING")
        _require_subset(gid, "representations", representation_ids, set(spec.get("required_representations", [])), "PHY_GATE_REQUIRED_REPRESENTATION_MISSING")
        _require_subset(gid, "prerequisites", prereq_ids, set(spec.get("required_prerequisites", [])), "PHY_GATE_REQUIRED_PREREQUISITE_MISSING")
        _require_subset(gid, "verifications", verification_ids, set(spec.get("required_verifications", [])), "PHY_GATE_REQUIRED_VERIFICATION_MISSING")
        _require_subset(gid, "linked buckets", set(gate["linked_buckets"]), set(spec.get("required_linked_buckets", [])), "PHY_GATE_REQUIRED_BUCKET_BINDING_MISSING")

        for relation in gate["relations"]:
            symbols = relation["symbols"]
            if len({s["symbol"] for s in symbols}) != len(symbols):
                fail("PHY_GATE_SYMBOL_BINDING_INVALID", f"{gid}:{relation['relation_id']} duplicates a symbol binding")
            for symbol in symbols:
                if not symbol["unit_dimension"].strip() or not symbol["reference_frame_role"].strip() or not symbol["sign_role"].strip():
                    fail("PHY_GATE_SYMBOL_BINDING_INVALID", f"{gid}:{relation['relation_id']} has incomplete physical symbol metadata")

        for condition in gate["model_conditions"]:
            unknown = set(condition["required_for_relations"]) - relation_ids
            if unknown:
                fail("PHY_GATE_MODEL_CONDITION_BINDING_INVALID", f"{gid}:{condition['condition_id']} references unknown relations {sorted(unknown)}")

        for rep in gate["representations"]:
            unknown_rel = set(rep["relation_bindings"]) - relation_ids
            unknown_con = set(rep["concept_bindings"]) - concept_ids
            if unknown_rel or unknown_con:
                fail("PHY_GATE_REPRESENTATION_BINDING_INVALID", f"{gid}:{rep['representation_id']} unknown_rel={sorted(unknown_rel)} unknown_con={sorted(unknown_con)}")
            if not rep["must_not_imply"]:
                fail("PHY_GATE_REPRESENTATION_SEMANTICS_INCOMPLETE", f"{gid}:{rep['representation_id']} has no must_not_imply guard")

        reasoning = sorted(gate["reasoning_sequence"], key=lambda x: x["sequence"])
        if [r["sequence"] for r in reasoning] != list(range(1, len(reasoning) + 1)):
            fail("PHY_GATE_REASONING_SEQUENCE_INVALID", f"{gid} reasoning sequence must be contiguous from 1")
        step_ids = {r["step_id"] for r in reasoning}
        if len(step_ids) != len(reasoning):
            fail("PHY_GATE_REASONING_SEQUENCE_INVALID", f"{gid} has duplicate reasoning step IDs")
        index = {r["step_id"]: r["sequence"] for r in reasoning}
        for step in reasoning:
            unknown_dep = set(step["depends_on"]) - step_ids
            if unknown_dep:
                fail("PHY_GATE_REASONING_DEPENDENCY_INVALID", f"{gid}:{step['step_id']} unknown dependencies {sorted(unknown_dep)}")
            if any(index[d] >= step["sequence"] for d in step["depends_on"]):
                fail("PHY_GATE_REASONING_ORDER_INVALID", f"{gid}:{step['step_id']} depends on a non-earlier step")
            if set(step["required_concepts"]) - concept_ids or set(step["required_relations"]) - relation_ids:
                fail("PHY_GATE_REASONING_BINDING_INVALID", f"{gid}:{step['step_id']} binds unknown concept/relation")

        if gid == "PHY-M2D-MOVING-LAUNCHER":
            required_order = [
                "RS-M2D-ML-FRAME-NAMING",
                "RS-M2D-ML-FRAME-CONVERSION",
                "RS-M2D-ML-PROJECTILE-EVOLUTION",
                "RS-M2D-ML-INVERSE-LIMIT",
            ]
            actual = [r["step_id"] for r in reasoning]
            positions = [actual.index(x) if x in actual else -1 for x in required_order]
            if -1 in positions or positions != sorted(positions):
                fail("PHY_GATE_REASONING_ORDER_INVALID", f"{gid} must preserve frame naming -> conversion -> projectile evolution -> inverse/limit verification")

        family_ids = set()
        for family in gate["problem_families"]:
            fid = family["family_id"]
            if fid in family_ids:
                fail("PHY_GATE_PROBLEM_FAMILY_INVALID", f"{gid} duplicates family {fid}")
            family_ids.add(fid)
            if set(family["hidden_invariants"]) - invariant_ids:
                fail("PHY_GATE_PROBLEM_FAMILY_INVALID", f"{gid}:{fid} references undeclared invariants")
            rep = family["required_representation"]
            if rep is not None and rep not in representation_ids:
                fail("PHY_GATE_PROBLEM_FAMILY_INVALID", f"{gid}:{fid} references unknown representation {rep}")

        if not gate["required_transformations"]:
            fail("PHY_GATE_TRANSFORMATION_REQUIRED", gid)
        if not gate["misconceptions"]:
            fail("PHY_GATE_MISCONCEPTION_REQUIRED", gid)
        for misconception in gate["misconceptions"]:
            if not misconception["required_counterexample"].strip() or not misconception["required_technical_repair"].strip():
                fail("PHY_GATE_COUNTEREXAMPLE_REQUIRED", f"{gid}:{misconception['misconception_id']}")

        dp = gate["difficulty_engineering"]
        if dp["maturity"] != "ENGINEERING":
            fail("PHY_GATE_DIFFICULTY_INVALID", f"{gid} difficulty maturity may not claim empirical validation")

        derived_status = "ENGINEERING_GATE_READY" if gate["scope_state"] == "ACTIVE" else "BLOCKED"
        derived_states.append({"gate_id": gid, "scope_state": gate["scope_state"], "derived_status": derived_status})

    return {
        "status": "PASS",
        "registry_id": registry["registry_id"],
        "registry_digest": digest(registry),
        "gate_count": len(gates),
        "gate_states": derived_states,
        "all_engineering_ready": all(x["derived_status"] == "ENGINEERING_GATE_READY" for x in derived_states),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate canonical Physics Technical Engineering Gate v3 registry")
    ap.add_argument("--registry")
    ap.add_argument("--report-out")
    args = ap.parse_args()
    registry = json.loads(Path(args.registry).read_text(encoding="utf-8")) if args.registry else build_registry()
    result = validate(registry)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.report_out:
        Path(args.report_out).write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
