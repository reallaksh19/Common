"""Production visual selections for The Pupil pages 97-99.

The base source fixture preserves the original semantic extraction.  This module
applies the learner-facing production selections discovered during visual QA:
P97-Q9 needs a five-angle classification set, and P99-Q2 needs the linked
count-and-money scale model with the target count hidden.

These are LearningDesign/source-fixture choices, never renderer-local patches.
"""
from __future__ import annotations

import copy
from typing import Any, Dict

from .build_fixture import build_primary_input as _build_base_primary_input


def _question(primary_input: Dict[str, Any], qref: str) -> Dict[str, Any]:
    matches = [
        question
        for question in primary_input["question_set"]["questions"]
        if question.get("question_ref") == qref
    ]
    if len(matches) != 1:
        raise ValueError(f"{qref}: expected exactly one source question, found {len(matches)}")
    return matches[0]


def _append_representation(evidence: Dict[str, Any], representation: Dict[str, Any]) -> None:
    rows = evidence["representation_requirements"]
    rid = representation["representation_id"]
    if any(row.get("representation_id") == rid for row in rows):
        raise ValueError(f"duplicate representation id: {rid}")
    rows.append(representation)


def build_primary_input() -> Dict[str, Any]:
    primary_input = copy.deepcopy(_build_base_primary_input())

    # P97-Q9: the learner must classify five distinct angle types.  A single
    # obtuse-vs-right benchmark is not sufficient evidence for that task.
    q9 = _question(primary_input, "P97-Q9")
    q9_evidence = q9["evidence"]
    q9_rep = {
        "representation_id": "REP-P97-Q9-CLASSIFICATION-SET",
        "role": "PICTORIAL",
        "primitive_kind": "ANGLE_CLASSIFICATION_SET",
        "semantic_params": {"degrees": [45, 90, 120, 180, 240]},
        "validator_refs": ["ANGLE_GEOMETRY", "FIVE_ANGLE_CLASSIFICATION_COVERAGE"],
        "fade_modes": ["FULL", "PARTIAL", "NONE"],
        "provenance": "ENGINE_AUTHORED_VISUAL",
    }
    _append_representation(q9_evidence, q9_rep)
    q9_evidence["learning_support_blueprint"]["primary"] = {
        "representation_ref": q9_rep["representation_id"],
        "fidelity": "SCHEMATIC",
        "fade_mode": "FULL",
    }

    # P99-Q2: show the linked scale relationship instead of only 120 -> 240.
    # The target count is deliberately absent, so the learner sees 3 objects on
    # the left and '?' on the right while the x2 money relationship stays visible.
    hats = _question(primary_input, "P99-Q2")
    hats_evidence = hats["evidence"]
    hats_rep = {
        "representation_id": "REP-P99-Q2-RATE-UNKNOWN",
        "role": "STRUCTURAL",
        "primitive_kind": "RATE_SCALE_MODEL",
        "semantic_params": {
            "base_amount": 120,
            "target_amount": 240,
            "base_count": 3,
            "target_count": None,
            "scale_factor": 2,
        },
        "validator_refs": ["SAME_RATE_STRUCTURE", "TARGET_COUNT_HIDDEN"],
        "fade_modes": ["FULL", "PARTIAL", "NONE"],
        "provenance": "ENGINE_AUTHORED_VISUAL",
    }
    _append_representation(hats_evidence, hats_rep)
    hats_evidence["learning_support_blueprint"]["primary"] = {
        "representation_ref": hats_rep["representation_id"],
        "fidelity": "SCHEMATIC",
        "fade_mode": "FULL",
    }

    return primary_input
