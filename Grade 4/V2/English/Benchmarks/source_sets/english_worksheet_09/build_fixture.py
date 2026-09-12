"""Curated semantic extraction fixture for Grade-4 English Worksheet 09.

This benchmark is deliberately explicit. It does not infer English semantics from
keywords. Each visible source obligation is mapped to registry capabilities,
task families, response structures, representations, source boundaries and a
progressive support blueprint.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source.json"
ENGLISH_ROOT = ROOT.parents[2]
HANDOFF_ENGINE = ENGLISH_ROOT / "LearningDesign" / "engine"
if str(HANDOFF_ENGINE) not in sys.path:
    sys.path.insert(0, str(HANDOFF_ENGINE))

from authoring_handoff import build_english_authoring_handoff  # type: ignore  # noqa: E402

SOURCE_MODEL_ID = "ENG-G4-WS09-ADJ-ORDER"
FADES = ["FULL", "PARTIAL", "NONE"]


def _rep(rep_id: str, *, params: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    return {
        "representation_id": rep_id,
        "primitive_kind": rep_id,
        "semantic_params": dict(params or {}),
        "validator_refs": ["SOURCE_GROUNDED"],
        "fade_modes": list(FADES),
        "provenance": "ENGINE_AUTHORED_VISUAL",
    }


def _coverage() -> Dict[str, bool]:
    return {
        "teach": True,
        "model": True,
        "practice": True,
        "hints": True,
        "verify": True,
        "answer_or_rubric": True,
    }


def _blueprint(
    *,
    h1: str,
    h2: str,
    h3_representation: str,
    fresh_retry: str,
    watches: Iterable[str] = (),
) -> Dict[str, Any]:
    return {
        "H1": {
            "semantic_role": "NOTICE",
            "child_label": "SPOT IT",
            "prompt": h1,
            "conceptual_support": "H1",
        },
        "H2": {
            "semantic_role": "REMEMBER",
            "child_label": "REMEMBER",
            "prompt": h2,
            "conceptual_support": "H2",
        },
        "H3": {
            "semantic_role": "REPRESENT",
            "child_label": "PICTURE IT",
            "representation_ref": h3_representation,
            "conceptual_support": "H3",
        },
        "fresh_retry": {
            "required": True,
            "conceptual_support": "H0",
            "prompt": fresh_retry,
            "must_be_new_item": True,
        },
        "misconception_watches": list(watches),
        "coverage_obligations": _coverage(),
    }


def _source_model() -> Dict[str, Any]:
    categories = ["OPINION", "SIZE", "AGE", "SHAPE", "COLOUR", "ORIGIN", "MATERIAL"]
    return {
        "source_model_id": SOURCE_MODEL_ID,
        "model_type": "ORDERED_TAXONOMY",
        "assessment_authority": "SOURCE_WORKSHEET",
        "categories": categories,
        "ordering": categories,
        "classification_questions": {
            "OPINION": "What do I think or feel about it?",
            "SIZE": "How big, small or wide?",
            "AGE": "How old or new?",
            "SHAPE": "What shape?",
            "COLOUR": "What colour?",
            "ORIGIN": "Where is it from?",
            "MATERIAL": "What is it made of?",
        },
        "clean_examples": {
            "OPINION": ["tasty", "fascinating", "sad", "fantastic"],
            "SIZE": ["huge", "tiny", "wide", "small"],
            "AGE": ["new", "old"],
            "SHAPE": ["round", "square"],
            "COLOUR": ["pink", "grey", "yellow"],
            "ORIGIN": ["Japanese", "Spanish", "Swedish", "Indian"],
            "MATERIAL": ["leather", "plastic", "wooden", "wool", "metal", "stone"],
        },
        "boundary_examples": ["traditional"],
        "forbidden_invented_categories": ["QUALITY", "PHYSICAL_QUALITY", "QUALITY_TYPE", "CONDITION"],
        "boundary_policy": {
            "no_force_fit": True,
            "allowed_statuses": ["SOURCE_MODEL_BOUNDARY", "AMBIGUOUS", "TEACHER_JUDGMENT"],
        },
        "source_refs": ["ENG-G4-WS09:I", "ENG-G4-WS09:III", "ENG-G4-WS09:IV"],
    }


def _question_evidence(source: Mapping[str, Any]) -> list[Dict[str, Any]]:
    section_by_ref = {section["section_ref"]: section for section in source["sections"]}
    poem_q = {q["question_ref"]: q for q in section_by_ref["V"]["questions"]}

    evidence: list[Dict[str, Any]] = []

    evidence.append({
        "question_ref": "ENG-G4-WS09-I",
        "source_ref": "ENG-G4-WS09:I",
        "section_ref": "I",
        "raw_text": section_by_ref["I"]["instruction"],
        "domain": "GRAMMAR",
        "scope_basis": "QUESTION_SET_OBSERVED",
        "source_model_ref": SOURCE_MODEL_ID,
        "source_boundary_required": False,
        "capability_refs": ["ENG-ADJ-IDENTIFY", "ENG-ADJ-CLASSIFY-SOURCE-MODEL"],
        "task_family_refs": ["ADJECTIVE_CLASSIFICATION", "CONTRAST_CLASSIFICATION"],
        "response_demand": {
            "response_structure_ref": "CLASSIFICATION_TABLE",
            "response_modes": ["WRITTEN", "SORTED"],
            "teacher_or_source_judgement_required": False,
        },
        "representation_requirements": [
            _rep("ADJECTIVE_FAMILY_CARDS", params={"source_categories": section_by_ref["I"]["printed_categories"]}),
            _rep("CATEGORY_SORT_TABLE", params={"source_words": section_by_ref["I"]["printed_words"]}),
            _rep("CONTRAST_PAIR", params={"contrasts": [["Swedish", "wooden"], ["wide", "round"]]}),
        ],
        "learning_support_blueprint": _blueprint(
            h1="Ask what the word tells you: feeling, size, age, shape, colour, where from, or made of?",
            h2="Use the worksheet's family question instead of guessing the category name.",
            h3_representation="CATEGORY_SORT_TABLE",
            fresh_retry="Classify four new words that are not in the source list: enormous, ancient, oval, Brazilian.",
            watches=["ORIGIN_MATERIAL_CONFUSION", "SIZE_SHAPE_CONFUSION"],
        ),
    })

    evidence.append({
        "question_ref": "ENG-G4-WS09-II",
        "source_ref": "ENG-G4-WS09:II",
        "section_ref": "II",
        "raw_text": section_by_ref["II"]["instruction"],
        "domain": "WRITING",
        "scope_basis": "QUESTION_SET_OBSERVED",
        "source_model_ref": SOURCE_MODEL_ID,
        "source_boundary_required": False,
        "capability_refs": ["ENG-DESC-NOUN-PHRASE", "ENG-DESC-MATERIAL-ORIGIN", "ENG-DESC-PURPOSE-INFERENCE"],
        "task_family_refs": ["CONSTRUCT_NOUN_PHRASE", "MYSTERY_OBJECT_DESCRIPTION"],
        "response_demand": {
            "response_structure_ref": "MYSTERY_OBJECT_FRAME",
            "response_modes": ["WRITTEN", "DRAWN"],
            "teacher_or_source_judgement_required": True,
            "rubric_criteria": ["SUITABLE_ADJECTIVES", "MATERIAL", "ORIGIN", "PLAUSIBLE_PURPOSE"],
        },
        "representation_requirements": [
            _rep("NOUN_PHRASE_BUILDER"),
            _rep("MYSTERY_OBJECT_PLANNER", params={"source_frame": section_by_ref["II"]["response_frame"]}),
        ],
        "learning_support_blueprint": _blueprint(
            h1="Choose the noun first. What kind of object did you find?",
            h2="Add only details that answer a useful question: what is it like, made of, from, or used for?",
            h3_representation="MYSTERY_OBJECT_PLANNER",
            fresh_retry="Describe a different mystery object in two sentences with no sentence frame.",
            watches=["ADJECTIVE_LIST_WITHOUT_CLEAR_NOUN", "PURPOSE_STATED_WITHOUT_REASON"],
        ),
    })

    evidence.append({
        "question_ref": "ENG-G4-WS09-III",
        "source_ref": "ENG-G4-WS09:III",
        "section_ref": "III",
        "raw_text": section_by_ref["III"]["printed_text"],
        "domain": "GRAMMAR",
        "scope_basis": "QUESTION_SET_OBSERVED",
        "source_model_ref": SOURCE_MODEL_ID,
        "source_boundary_required": True,
        "capability_refs": ["ENG-ADJ-CLASSIFY-SOURCE-MODEL", "ENG-ADJ-ORDER", "ENG-ADJ-SOURCE-BOUNDARY"],
        "task_family_refs": ["ADJECTIVE_ORDER_REPAIR", "SOURCE_BOUNDARY_HANDLING"],
        "response_demand": {
            "response_structure_ref": "ORDERED_REWRITE",
            "response_modes": ["WRITTEN"],
            "teacher_or_source_judgement_required": True,
        },
        "representation_requirements": [
            _rep("ADJECTIVE_ORDER_TRAIN", params={"ordering": _source_model()["ordering"]}),
            _rep("CATEGORY_SORT_TABLE"),
            _rep("CONTRAST_PAIR", params={"contrasts": [["huge", "ancient"], ["Indian", "stone"]]}),
        ],
        "learning_support_blueprint": _blueprint(
            h1="Find the noun, then ask which family each describing word belongs to.",
            h2="Read the worksheet order from left to right: opinion, size, age, shape, colour, origin, material.",
            h3_representation="ADJECTIVE_ORDER_TRAIN",
            fresh_retry="Rewrite a new phrase: old / tiny / Brazilian / wooden / house.",
            watches=["ADJECTIVE_ORDER_SEQUENCE_ERROR", "SOURCE_MODEL_FORCE_FIT"],
        ),
        "ambiguity": [
            "traditional does not have a clean category in the seven-category printed classification table"
        ],
        "source_issues": [
            "traditional must remain SOURCE_MODEL_BOUNDARY unless teacher/source authority supplies a classification"
        ],
    })

    evidence.append({
        "question_ref": "ENG-G4-WS09-IV",
        "source_ref": "ENG-G4-WS09:IV",
        "section_ref": "IV",
        "raw_text": section_by_ref["IV"]["instruction"],
        "domain": "WRITING",
        "scope_basis": "QUESTION_SET_OBSERVED",
        "source_model_ref": SOURCE_MODEL_ID,
        "source_boundary_required": False,
        "capability_refs": ["ENG-DESC-OPENING", "ENG-DESC-VISUAL-DETAIL", "ENG-DESC-REVISION", "ENG-ADJ-ORDER"],
        "task_family_refs": ["EXTENDED_DESCRIPTIVE_WRITING", "WRITING_REVISION"],
        "response_demand": {
            "response_structure_ref": "TRAVEL_BLOGGER_RUBRIC",
            "response_modes": ["WRITTEN", "UNDERLINED"],
            "teacher_or_source_judgement_required": True,
            "rubric_criteria": section_by_ref["IV"]["printed_checklist"],
        },
        "representation_requirements": [
            _rep("TRAVEL_BLOGGER_PLANNER", params={"destinations": section_by_ref["IV"]["destinations"]}),
            _rep("WRITING_CHECKLIST", params={"criteria": section_by_ref["IV"]["printed_checklist"]}),
            _rep("ADJECTIVE_ORDER_TRAIN"),
        ],
        "learning_support_blueprint": _blueprint(
            h1="Before writing, choose one thing you can see and one detail about it.",
            h2="Build the paragraph in four moves: opening, what I see, zoom in, how I feel.",
            h3_representation="TRAVEL_BLOGGER_PLANNER",
            fresh_retry="Write two new sentences about a mountain village using your own details and no model sentence.",
            watches=["ADJECTIVE_DUMP_WITHOUT_DESCRIPTION", "CHECKLIST_REQUIREMENT_OMITTED"],
        ),
    })

    evidence.append({
        "question_ref": "ENG-G4-WS09-V-Q1",
        "source_ref": "ENG-G4-WS09:V:Q1",
        "section_ref": "V",
        "raw_text": poem_q["ENG-G4-WS09-V-Q1"]["prompt"],
        "domain": "POETRY",
        "scope_basis": "QUESTION_SET_OBSERVED",
        "source_model_ref": None,
        "source_boundary_required": False,
        "capability_refs": ["ENG-POEM-READ-FOR-MEANING", "ENG-TEXT-EVIDENCE", "ENG-CAUSE-EFFECT", "ENG-INFERENCE"],
        "task_family_refs": ["CAUSE_EFFECT", "INFERENCE_WITH_EVIDENCE"],
        "response_demand": {
            "response_structure_ref": "ANSWER_TEXT_CLUE_CONNECTION",
            "response_modes": ["WRITTEN", "ORAL"],
            "teacher_or_source_judgement_required": True,
            "evidence_parts": ["ANSWER", "TEXT_CLUE", "CONNECTION"],
        },
        "representation_requirements": [
            _rep("STANZA_MEANING_MAP"),
            _rep("ANSWER_CLUE_CONNECTION"),
            _rep("CAUSE_EFFECT_CHAIN"),
        ],
        "learning_support_blueprint": _blueprint(
            h1="Which line tells you what the Dodo got from the trees?",
            h2="A strong answer says what happened, gives a poem clue, and explains the link.",
            h3_representation="ANSWER_CLUE_CONNECTION",
            fresh_retry="Use a different short text to explain one cause-and-effect answer with a clue and connection.",
            watches=["TEXT_EVIDENCE_NOT_PROVIDED", "CAUSE_NAMED_WITHOUT_CONNECTION"],
        ),
    })

    evidence.append({
        "question_ref": "ENG-G4-WS09-V-Q2",
        "source_ref": "ENG-G4-WS09:V:Q2",
        "section_ref": "V",
        "raw_text": poem_q["ENG-G4-WS09-V-Q2"]["prompt"],
        "domain": "POETRY",
        "scope_basis": "QUESTION_SET_OBSERVED",
        "source_model_ref": None,
        "source_boundary_required": False,
        "capability_refs": ["ENG-POEM-READ-FOR-MEANING", "ENG-TEXT-EVIDENCE", "ENG-CAUSE-EFFECT", "ENG-MULTI-CLUE-SYNTHESIS"],
        "task_family_refs": ["CAUSE_EFFECT", "MULTI_CLUE_SYNTHESIS"],
        "response_demand": {
            "response_structure_ref": "MULTI_CLUE_EXPLANATION",
            "response_modes": ["WRITTEN", "ORAL"],
            "teacher_or_source_judgement_required": True,
            "evidence_parts": ["ANSWER", "TEXT_CLUES", "SYNTHESIS"],
        },
        "representation_requirements": [
            _rep("STANZA_MEANING_MAP"),
            _rep("MULTI_CLUE_TABLE"),
            _rep("CAUSE_EFFECT_CHAIN"),
        ],
        "learning_support_blueprint": _blueprint(
            h1="Look for more than one human-linked action in the danger stanza.",
            h2="Collect the clues first; then explain how they worked together rather than naming only hunting.",
            h3_representation="MULTI_CLUE_TABLE",
            fresh_retry="From a fresh paragraph with three causes, explain why one cause alone is not the whole answer.",
            watches=["SINGLE_CAUSE_WHEN_MULTI_CAUSE_REQUIRED", "CLUE_LIST_WITHOUT_SYNTHESIS"],
        ),
    })

    evidence.append({
        "question_ref": "ENG-G4-WS09-V-Q3",
        "source_ref": "ENG-G4-WS09:V:Q3",
        "section_ref": "V",
        "raw_text": poem_q["ENG-G4-WS09-V-Q3"]["prompt"],
        "domain": "READING",
        "scope_basis": "QUESTION_SET_OBSERVED",
        "source_model_ref": None,
        "source_boundary_required": False,
        "capability_refs": ["ENG-TRANSFER", "ENG-JUSTIFICATION"],
        "task_family_refs": ["TRANSFER"],
        "response_demand": {
            "response_structure_ref": "TRANSFER_REASON",
            "response_modes": ["WRITTEN", "ORAL"],
            "teacher_or_source_judgement_required": True,
            "evidence_parts": ["TRANSFER_EXAMPLE", "THREAT_OR_PARALLEL", "REASON_OR_ACTION"],
        },
        "representation_requirements": [
            _rep("TRANSFER_THREAT_ACTION_TABLE"),
            _rep("TEXT_VS_MY_THINKING"),
        ],
        "learning_support_blueprint": _blueprint(
            h1="Choose one living species, then name one human-linked threat.",
            h2="Your answer needs three parts: species, threat, and one sensible protective action.",
            h3_representation="TRANSFER_THREAT_ACTION_TABLE",
            fresh_retry="Use a different species and give a new threat-action pair without the frame.",
            watches=["TRANSFER_EXAMPLE_WITHOUT_PARALLEL", "PROTECTION_ACTION_NOT_LINKED_TO_THREAT"],
        ),
    })

    evidence.append({
        "question_ref": "ENG-G4-WS09-V-Q4",
        "source_ref": "ENG-G4-WS09:V:Q4",
        "section_ref": "V",
        "raw_text": poem_q["ENG-G4-WS09-V-Q4"]["prompt"],
        "domain": "READING",
        "scope_basis": "QUESTION_SET_OBSERVED",
        "source_model_ref": None,
        "source_boundary_required": False,
        "capability_refs": ["ENG-POEM-READ-FOR-MEANING", "ENG-JUSTIFICATION"],
        "task_family_refs": ["JUSTIFY_CHOICE"],
        "response_demand": {
            "response_structure_ref": "CHOICE_JUSTIFICATION",
            "response_modes": ["WRITTEN", "ORAL"],
            "teacher_or_source_judgement_required": True,
            "evidence_parts": ["CHOICE", "JUSTIFICATION"],
        },
        "representation_requirements": [
            _rep("CHOICE_REASON_FRAME"),
            _rep("STANZA_MEANING_MAP"),
        ],
        "learning_support_blueprint": _blueprint(
            h1="Choose one event from the poem that you would change.",
            h2="There can be more than one good choice, but your reason must explain why the change matters.",
            h3_representation="CHOICE_REASON_FRAME",
            fresh_retry="Choose a different event from a fresh story and justify the change in one complete sentence.",
            watches=["CHOICE_WITHOUT_JUSTIFICATION", "REASON_NOT_CONNECTED_TO_CHOICE"],
        ),
    })

    return evidence


def build_primary_input() -> Dict[str, Any]:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    return {
        "source": {
            "source_id": source["source_id"],
            "source_type": source["source_type"],
            "grade": source["grade"],
            "source_issues": list(source.get("source_issues") or []),
        },
        "source_models": [_source_model()],
        "question_evidence": _question_evidence(source),
        "learner_evidence": [],
    }


def build_handoff() -> Dict[str, Any]:
    return build_english_authoring_handoff(build_primary_input())


def main() -> None:
    handoff = build_handoff()
    print(json.dumps({
        "source": handoff["source"],
        "plan_count": len(handoff["learning_representation_plans"]),
        "question_refs": [row["question_ref"] for row in handoff["learning_representation_plans"]],
        "invariants": handoff["authoring_invariants"],
    }, indent=2))


if __name__ == "__main__":
    main()
