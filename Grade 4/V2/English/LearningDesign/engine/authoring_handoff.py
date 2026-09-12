"""Grade-4 English V2 CoreSkills -> LearningDesign handoff.

Publication consumes this handoff. Therefore every learner-facing semantic needed
later (prompt, response demand, representation specification, source ambiguity,
and support) is carried forward explicitly rather than reconstructed in layout.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Mapping

CORE_ENGINE = Path(__file__).resolve().parents[2] / "CoreSkills" / "engine"
if str(CORE_ENGINE) not in sys.path:
    sys.path.insert(0, str(CORE_ENGINE))

from author import author_core_skills  # type: ignore  # noqa: E402


def _sequence_for(row: Mapping[str, Any]) -> list[str]:
    sequence = ["TEACH", "MODEL", "GUIDED_PRACTICE", "HINT_LADDER", "INDEPENDENT_RETRY"]
    watches = (row.get("learning_support_blueprint") or {}).get("misconception_watches") or []
    if watches:
        sequence.insert(3, "DIAGNOSTIC_CONTRAST")
    response = row.get("response_demand") or {}
    if response.get("rubric_criteria"):
        sequence.append("RUBRIC_REVIEW")
    if any(family in {"TRANSFER", "JUSTIFY_CHOICE"} for family in row.get("task_family_refs", [])):
        sequence.append("TRANSFER")
    return sequence


def build_english_authoring_handoff(primary_input: Mapping[str, Any]) -> Dict[str, Any]:
    core = author_core_skills(primary_input)
    learner_by_question: dict[str, list[dict[str, Any]]] = {}
    for row in core["learner_evidence"]:
        learner_by_question.setdefault(row["question_ref"], []).append(dict(row))

    plans: list[dict[str, Any]] = []
    for row in core["question_evidence"]:
        blueprint = row["learning_support_blueprint"]
        representation_specs = [dict(rep) for rep in row["representation_requirements"]]
        plans.append(
            {
                "schema_version": "1.0.0",
                "question_ref": row["question_ref"],
                "source_ref": row.get("source_ref"),
                "section_ref": row.get("section_ref"),
                "learner_prompt": row.get("raw_text"),
                "domain": row["domain"],
                "capability_refs": list(row["capability_refs"]),
                "task_family_refs": list(row["task_family_refs"]),
                "teaching_sequence": _sequence_for(row),
                "representations": [rep["representation_id"] for rep in representation_specs],
                "representation_specs": representation_specs,
                "response_demand": dict(row["response_demand"]),
                "support": {
                    "H1": dict(blueprint["H1"]),
                    "H2": dict(blueprint["H2"]),
                    "H3": dict(blueprint["H3"]),
                    "fresh_retry": dict(blueprint["fresh_retry"]),
                },
                "misconception_watches": list(blueprint.get("misconception_watches") or []),
                "source_model_ref": row.get("source_model_ref"),
                "source_boundary_required": bool(row.get("source_boundary_required", False)),
                "ambiguity": list(row.get("ambiguity") or []),
                "source_issues": list(row.get("source_issues") or []),
                "coverage_obligations": dict(blueprint["coverage_obligations"]),
                "learner_evidence": learner_by_question.get(row["question_ref"], []),
            }
        )

    return {
        "schema_version": "1.0.0",
        "subject": "ENGLISH",
        "grade": 4,
        "source": core["source"],
        "source_models": core["source_models"],
        "learning_representation_plans": plans,
        "authoring_invariants": core["authoring_invariants"],
    }
