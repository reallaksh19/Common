"""Learner-facing publication refinements for Worksheet 09.

This file records visual-QA / child-language decisions upstream of Publication.
It may select/reorder already-typed representations and provide a clearer child
prompt, but it may not change source truth, capability meaning, rubrics, hints,
source boundaries, or response judgement rules.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from build_fixture import build_handoff


CHILD_PROMPTS = {
    "ENG-G4-WS09-I": "Put each describing word into the group where it belongs.",
    "ENG-G4-WS09-II": "Imagine you found a mysterious object. Describe it. Tell what it is made of, where it came from, and what it might be used for.",
    "ENG-G4-WS09-III": "The describing words are mixed up. Put them in the worksheet's order and rewrite the description.",
    "ENG-G4-WS09-IV": "Choose a place and write a short travel-blogger description. Use at least six adjectives, then check your work.",
    "ENG-G4-WS09-V-Q1": "Why did clearing the forests hurt the Dodo? Use a clue from the poem and explain the connection.",
    "ENG-G4-WS09-V-Q2": "Was hunting the only problem for the Dodo? Find other human actions in the poem and explain how they mattered.",
    "ENG-G4-WS09-V-Q3": "Name a living species that people can harm. What can people do to protect it?",
    "ENG-G4-WS09-V-Q4": "Choose one event in the Dodo's story that you would change. Explain why your change would matter.",
}

REPRESENTATION_ORDER = {
    "ENG-G4-WS09-I": ["CATEGORY_SORT_TABLE", "ADJECTIVE_FAMILY_CARDS", "CONTRAST_PAIR"],
    "ENG-G4-WS09-II": ["MYSTERY_OBJECT_PLANNER", "NOUN_PHRASE_BUILDER"],
    "ENG-G4-WS09-III": ["ADJECTIVE_ORDER_TRAIN", "CONTRAST_PAIR"],
    "ENG-G4-WS09-IV": ["TRAVEL_BLOGGER_PLANNER", "WRITING_CHECKLIST", "ADJECTIVE_ORDER_TRAIN"],
    "ENG-G4-WS09-V-Q1": ["ANSWER_CLUE_CONNECTION", "CAUSE_EFFECT_CHAIN", "STANZA_MEANING_MAP"],
    "ENG-G4-WS09-V-Q2": ["MULTI_CLUE_TABLE", "CAUSE_EFFECT_CHAIN", "STANZA_MEANING_MAP"],
    "ENG-G4-WS09-V-Q3": ["TRANSFER_THREAT_ACTION_TABLE", "TEXT_VS_MY_THINKING"],
    "ENG-G4-WS09-V-Q4": ["CHOICE_REASON_FRAME", "STANZA_MEANING_MAP"],
}


def build_production_handoff() -> Dict[str, Any]:
    handoff = deepcopy(build_handoff())
    for plan in handoff["learning_representation_plans"]:
        qref = plan["question_ref"]
        plan["source_prompt"] = plan.get("learner_prompt")
        plan["learner_prompt"] = CHILD_PROMPTS[qref]
        by_id = {spec["representation_id"]: spec for spec in plan["representation_specs"]}
        ordered = [by_id[rep_id] for rep_id in REPRESENTATION_ORDER[qref] if rep_id in by_id]
        if not ordered:
            raise AssertionError(f"{qref}: production representation selection is empty")
        plan["representation_specs"] = ordered
        plan["representations"] = [spec["representation_id"] for spec in ordered]
        plan["publication_provenance"] = "VISUAL_QA_REFINEMENT_WITHOUT_SEMANTIC_CHANGE"
    return handoff


if __name__ == "__main__":
    result = build_production_handoff()
    print({
        plan["question_ref"]: {
            "prompt": plan["learner_prompt"],
            "representations": plan["representations"],
        }
        for plan in result["learning_representation_plans"]
    })
