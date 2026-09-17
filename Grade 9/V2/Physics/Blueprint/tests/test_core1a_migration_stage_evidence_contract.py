#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contracts" / "core1a-migration-stage-evidence.schema.json").read_text(encoding="utf-8"))


def receipt(stage: str, evidence_kind: str, proof: dict) -> dict:
    return {
        "schema_version": "2.0.0",
        "receipt_id": f"SYNTH-{stage}",
        "bucket_id": "SYNTH-BUCKET",
        "stage": stage,
        "evidence_kind": evidence_kind,
        "evidence_state": "PRESENT",
        "source_refs": ["fixtures/core1a-migration-stage-evidence/synthetic-source.json"],
        "artifact_refs": ["SYNTH-ARTIFACT"],
        "evidence_refs": ["SYNTH-EVIDENCE"],
        "proof": proof,
        "unresolved_requirements": [],
    }


def must_schema_fail(doc: dict) -> None:
    try:
        jsonschema.validate(doc, SCHEMA)
    except jsonschema.ValidationError:
        return
    raise AssertionError("expected stage-evidence schema rejection")


jump = receipt(
    "1A2_INFERENTIAL_JUMPS",
    "INFERENTIAL_JUMP_CLOSURE",
    {
        "jump_rows": [
            {
                "jump_ref": "J1",
                "learning_atom_refs": ["A1"],
                "novice_obligation": "Notice that horizontal and vertical velocity evolve independently.",
                "closure_move_refs": ["MOVE-1"],
                "evidence_refs": ["EV-1"],
            }
        ],
        "uncovered_jump_refs": [],
    },
)
jsonschema.validate(jump, SCHEMA)
bad = copy.deepcopy(jump)
bad["proof"]["uncovered_jump_refs"] = ["J-X"]
must_schema_fail(bad)

transformation = receipt(
    "1A3_COGNITIVE_TRANSFORMATION",
    "COGNITIVE_TRANSFORMATION",
    {
        "transformations": [
            {
                "jump_ref": "J1",
                "novice_state": "Treats speed as a signed scalar.",
                "target_expert_state": "Separates velocity magnitude from direction.",
                "teaching_move_refs": ["MOVE-1"],
                "verification_ref": "CHECK-1",
            }
        ],
        "unmapped_jump_refs": [],
    },
)
jsonschema.validate(transformation, SCHEMA)
bad = copy.deepcopy(transformation)
bad["proof"]["unmapped_jump_refs"] = ["J-X"]
must_schema_fail(bad)

requirements = receipt(
    "1A4_REPRESENTATION_REQUIREMENTS",
    "REPRESENTATION_REQUIREMENTS",
    {
        "requirement_rows": [
            {
                "scope_ref": "A1",
                "representation_requirement_ref": "REP-REQ-1",
                "noticing_target": "Vertical velocity changes while the shared clock advances.",
                "instructional_purpose": "Make component evolution visible before equations.",
                "translation_obligation": "Translate picture to words to component symbols.",
            }
        ],
        "unbound_requirement_refs": [],
    },
)
jsonschema.validate(requirements, SCHEMA)
bad = copy.deepcopy(requirements)
bad["proof"]["unbound_requirement_refs"] = ["REP-REQ-X"]
must_schema_fail(bad)

bridge = receipt(
    "1A7_PICTURE_WORD_SYMBOL_EQUATION_BRIDGE",
    "PICTURE_WORD_SYMBOL_EQUATION_BRIDGE",
    {
        "bridge_rows": [
            {
                "learning_atom_ref": "A1",
                "picture_ref": "PIC-1",
                "word_ref": "WORD-1",
                "symbol_ref": "SYM-1",
                "equation_ref": "EQ-1",
                "translation_check_refs": ["CHECK-1"],
            }
        ],
        "unbridged_atom_refs": [],
    },
)
jsonschema.validate(bridge, SCHEMA)
bad = copy.deepcopy(bridge)
bad["proof"]["unbridged_atom_refs"] = ["A-X"]
must_schema_fail(bad)

closure = receipt(
    "1A11_UNRESOLVED_JUMP_AUDIT",
    "UNRESOLVED_JUMP_CLOSURE",
    {
        "required_jump_refs": ["J1"],
        "closure_receipt_refs": ["CLOSE-1"],
        "unresolved_jump_refs": [],
        "unresolved_required_jump_count": 0,
    },
)
jsonschema.validate(closure, SCHEMA)
bad = copy.deepcopy(closure)
bad["proof"]["unresolved_required_jump_count"] = 1
must_schema_fail(bad)
bad = copy.deepcopy(closure)
bad["proof"]["unresolved_jump_refs"] = ["J-X"]
must_schema_fail(bad)

print("Core1A migration stage-evidence contract: PASS (typed closure proofs for all promotable partial stages)")
