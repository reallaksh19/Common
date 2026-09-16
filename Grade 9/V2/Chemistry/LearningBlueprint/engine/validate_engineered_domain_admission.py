#!/usr/bin/env python3
"""Validation for Chemistry Engineered Domain Admission."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class ChemistryEngineeredDomainAdmissionError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def canonical(val: Any) -> str:
    return json.dumps(val, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(val: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(val).encode("utf-8")).hexdigest()


def load_json(rel_or_path: str | Path) -> dict:
    p = Path(rel_or_path) if Path(rel_or_path).is_absolute() else ROOT / rel_or_path
    return json.loads(p.read_text(encoding="utf-8"))


def validate(admission: dict, registry: dict | None = None) -> dict:
    schema = load_json("contracts/chemistry-engineered-domain-admission.schema.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(admission), key=lambda e: list(e.path))
    if errors:
        raise ChemistryEngineeredDomainAdmissionError("CHEM_ENG_ADM_SCHEMA", errors[0].message)

    if admission["subject"] != "CHEMISTRY":
        raise ChemistryEngineeredDomainAdmissionError("CHEM_ENG_ADM_SUBJECT_MISMATCH", "Subject must be CHEMISTRY")

    registry = registry or load_json("policies/chemistry-technical-engineering-gates.v1.json")
    known_gates = {g["subtopic_id"] for g in registry.get("subtopic_gates", [])}

    for gid in admission["evaluated_gate_ids"]:
        if gid not in known_gates:
            raise ChemistryEngineeredDomainAdmissionError("CHEM_ENG_ADM_GATE_UNKNOWN", f"Unknown gate: {gid}")

    if admission["held_gate_ids"] and admission["admission_status"] == "ADMITTED":
        raise ChemistryEngineeredDomainAdmissionError("CHEM_ENG_ADM_HELD_GATES_PRESENT", "Cannot be ADMITTED with held gates")

    return {
        "status": "PASS",
        "admission_receipt_id": admission["admission_receipt_id"],
        "admission_status": admission["admission_status"],
        "evaluated_count": len(admission["evaluated_gate_ids"]),
        "admitted_count": len(admission["admitted_gate_ids"]),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate Chemistry Engineered Domain Admission")
    ap.add_argument("--admission", required=True)
    args = ap.parse_args()
    print(json.dumps(validate(load_json(args.admission)), indent=2))


if __name__ == "__main__":
    main()
