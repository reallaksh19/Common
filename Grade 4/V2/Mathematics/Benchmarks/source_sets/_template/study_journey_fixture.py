"""Document-level StudyJourney template for a copied scanned source set.

Do not turn source order into lesson order mechanically.  Group source evidence
into teaching concepts, then choose teach/worked/guided/independent/transfer
blocks deliberately.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source.json"


def B(
    block_id: str,
    block_type: str,
    title: str,
    body: str,
    *,
    visibility: str = "HIDDEN",
    refs: Iterable[str] = (),
    learner_prompt: str = "",
    solution_text: str = "",
    representation: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "block_id": block_id,
        "block_type": block_type,
        "title": title,
        "body": body,
        "answer_visibility": visibility,
        "source_refs": list(refs),
    }
    if learner_prompt:
        out["learner_prompt"] = learner_prompt
    if solution_text:
        out["solution_text"] = solution_text
    if representation is not None:
        out["representation"] = representation
    return out


# Replace with explicit concept-level modules after semantic extraction.
#
# A useful module shape is:
#
# {
#   "module_id": "M1-...",
#   "title": "...",
#   "learning_goal": "...",
#   "source_refs": ["Q1", "Q2"],
#   "concept_refs": ["..."],
#   "prerequisite_bridges": [
#       {
#           "bridge_id": "BR-M1-...",
#           "statement": "instructionally necessary bridge",
#           "provenance": "PEDAGOGICAL_BRIDGE"
#       }
#   ],
#   "misconception_targets": ["bounded mechanism, not learner trait"],
#   "blocks": [
#       B("M1-SEE", "SEE_DISCOVER", "...", "...", refs=["Q1"]),
#       B(
#           "M1-WORKED", "WORKED_EXAMPLE", "...", "...",
#           visibility="WORKED_EXAMPLE", refs=["Q1"],
#           solution_text="complete authored worked example"
#       ),
#       B(
#           "M1-INDEPENDENT", "INDEPENDENT_TRY", "...", "...",
#           refs=["Q2"], learner_prompt="fresh answer-free attempt"
#       ),
#   ],
#   "mastery_evidence": ["observable evidence statement"]
# }
#
# Do not reuse p97-p99 module content unless the new source independently
# supports the same mathematics and sequence.
MODULES: list[Dict[str, Any]] = []


def _source_refs() -> list[str]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    if payload.get("template_only") is True:
        raise ValueError("TEMPLATE_NOT_FILLED: source.json")
    refs = [str(row.get("question_ref") or "") for row in payload.get("questions") or []]
    if not refs or any(not ref for ref in refs):
        raise ValueError("SOURCE_QUESTION_REFS_REQUIRED")
    if len(refs) != len(set(refs)):
        raise ValueError("DUPLICATE_SOURCE_QUESTION_REF")
    return refs


def build_study_journey() -> Dict[str, Any]:
    required = _source_refs()
    if not MODULES:
        raise ValueError(
            "TEMPLATE_REQUIRES_STUDY_JOURNEY: synthesize source questions into explicit teaching modules"
        )

    covered = sorted({
        str(ref)
        for module in MODULES
        for ref in (module.get("source_refs") or [])
    })

    plan = {
        "schema_version": "1.0.0",
        "journey_id": "REPLACE_WITH_STUDY_JOURNEY_ID",
        "grade_level": 4,
        "title": "REPLACE_WITH_LEARNER_FACING_STUDY_GUIDE_TITLE",
        "modules": MODULES,
        "source_coverage": {
            "required_source_refs": required,
            "covered_source_refs": covered,
        },
    }

    if "REPLACE_" in plan["journey_id"] or "REPLACE_" in plan["title"]:
        raise ValueError("TEMPLATE_NOT_FILLED: StudyJourney identity/title")
    return plan


if __name__ == "__main__":
    print(json.dumps(build_study_journey(), indent=2))
