#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]


class ChemistryEngineeringRegistryError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryEngineeringRegistryError(code, message)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def validate(registry: dict) -> dict:
    schema = load("contracts/chemistry-technical-engineering-gate.schema.json")
    Draft202012Validator.check_schema(schema)
    try:
        Draft202012Validator(schema).validate(registry)
    except ValidationError as exc:
        fail("CHEM_RUNTIME_GATE_SCHEMA", f"{exc.message} at {list(exc.path)}")

    gates = registry["subtopic_gates"]
    gate_ids = [g["subtopic_id"] for g in gates]
    if len(gate_ids) != len(set(gate_ids)):
        fail("CHEM_RUNTIME_GATE_DUPLICATE", "subtopic gate IDs must be unique")
    gate_map = {g["subtopic_id"]: g for g in gates}

    global_ids = {
        "concept": set(),
        "equation": set(),
        "representation": set(),
        "misconception": set(),
    }
    for gate in gates:
        if gate["maturity"] != "ENGINEERING":
            fail("CHEM_RUNTIME_GATE_MATURITY", f"{gate['subtopic_id']} maturity must be ENGINEERING")
        local_families = {f["family_id"] for f in gate["problem_families"]}
        missing_families = sorted(set(gate["linked_problem_family_ids"]) - local_families)
        if missing_families:
            fail("CHEM_RUNTIME_GATE_FAMILY_REF", f"{gate['subtopic_id']} missing problem families {missing_families}")

        groups = {
            "concept": [x["concept_id"] for x in gate["technical_core"]],
            "equation": [x["equation_id"] for x in gate["mandatory_equations"]],
            "representation": [x["representation_id"] for x in gate["representations"]],
            "misconception": [x["misconception_id"] for x in gate["misconceptions"]],
        }
        for kind, values in groups.items():
            if len(values) != len(set(values)):
                fail("CHEM_RUNTIME_GATE_DUPLICATE_ASSET", f"{gate['subtopic_id']} duplicates {kind} IDs")
            overlap = global_ids[kind] & set(values)
            if overlap:
                fail("CHEM_RUNTIME_GATE_DUPLICATE_ASSET", f"global duplicate {kind} IDs {sorted(overlap)}")
            global_ids[kind].update(values)

        if gate["technical_readiness"] == "ENGINEERING_GATE_READY":
            false_checks = sorted(k for k, v in gate["release_checklist"].items() if v is not True)
            if false_checks:
                fail("CHEM_RUNTIME_GATE_RELEASE_CHECKLIST", f"{gate['subtopic_id']} READY but false checks={false_checks}")

    for gate in gates:
        for prereq in gate.get("prerequisite_ids", []):
            if prereq.startswith("CHEM-") and prereq not in gate_map:
                fail("CHEM_RUNTIME_GATE_PREREQ_MISSING", f"{gate['subtopic_id']} -> {prereq}")

    visiting: list[str] = []
    done: set[str] = set()
    def walk(gid: str):
        if gid in done:
            return
        if gid in visiting:
            i = visiting.index(gid)
            fail("CHEM_RUNTIME_GATE_CYCLE", " -> ".join(visiting[i:] + [gid]))
        visiting.append(gid)
        for prereq in gate_map[gid].get("prerequisite_ids", []):
            if prereq in gate_map:
                walk(prereq)
        visiting.pop()
        done.add(gid)
    for gid in gate_ids:
        walk(gid)

    return {"status":"PASS","gate_count":len(gates),"gate_ids":gate_ids}
