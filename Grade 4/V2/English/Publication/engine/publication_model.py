"""Deterministic English V2 publication models.

This module does not author pedagogy. It reshapes LearningRepresentationPlan into
page models for the renderer. Learner prompts, support, rubrics, misconceptions,
source boundaries and representation semantics must already exist upstream.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping


REPRESENTATION_LABELS = {
    "ADJECTIVE_FAMILY_CARDS": "Describing-word groups",
    "CATEGORY_SORT_TABLE": "Sort the words",
    "ADJECTIVE_ORDER_TRAIN": "Adjective train",
    "CONTRAST_PAIR": "Compare these two",
    "NOUN_PHRASE_BUILDER": "Build a noun phrase",
    "MYSTERY_OBJECT_PLANNER": "Mystery-object planner",
    "TRAVEL_BLOGGER_PLANNER": "Travel-blogger planner",
    "WRITING_CHECKLIST": "Writing checklist",
    "STANZA_MEANING_MAP": "Stanza meaning map",
    "ANSWER_CLUE_CONNECTION": "Answer + clue + connection",
    "CAUSE_EFFECT_CHAIN": "Cause and effect",
    "MULTI_CLUE_TABLE": "Clue collector",
    "TEXT_VS_MY_THINKING": "Text clue / my thinking",
    "CHOICE_REASON_FRAME": "Choice + reason",
    "TRANSFER_THREAT_ACTION_TABLE": "Species + threat + action",
}

TASK_TITLES = {
    "ADJECTIVE_CLASSIFICATION": "Sort describing words into the right groups",
    "CONTRAST_CLASSIFICATION": "Tell similar groups apart",
    "CONSTRUCT_NOUN_PHRASE": "Build a clear description",
    "MYSTERY_OBJECT_DESCRIPTION": "Describe a mystery object",
    "ADJECTIVE_ORDER_REPAIR": "Put adjectives in the right order",
    "SOURCE_BOUNDARY_HANDLING": "Know when the worksheet model does not decide",
    "EXTENDED_DESCRIPTIVE_WRITING": "Write like a travel blogger",
    "WRITING_REVISION": "Check and improve your writing",
    "CAUSE_EFFECT": "Explain cause and effect",
    "INFERENCE_WITH_EVIDENCE": "Use a clue to explain your thinking",
    "MULTI_CLUE_SYNTHESIS": "Bring more than one clue together",
    "TRANSFER": "Use the idea in a new situation",
    "JUSTIFY_CHOICE": "Make a choice and explain why",
}


def _title(plan: Mapping[str, Any]) -> str:
    for family in plan.get("task_family_refs") or []:
        if family in TASK_TITLES:
            return TASK_TITLES[family]
    return "English learning task"


def _rep_blocks(plan: Mapping[str, Any]) -> list[Dict[str, Any]]:
    blocks: list[Dict[str, Any]] = []
    for spec in plan.get("representation_specs") or []:
        rep_id = spec["representation_id"]
        blocks.append(
            {
                "representation_id": rep_id,
                "label": REPRESENTATION_LABELS.get(rep_id, rep_id.replace("_", " ").title()),
                "semantic_params": dict(spec.get("semantic_params") or {}),
            }
        )
    return blocks


def _source_model(handoff: Mapping[str, Any], ref: str | None) -> Mapping[str, Any] | None:
    if not ref:
        return None
    for model in handoff.get("source_models") or []:
        if model.get("source_model_id") == ref:
            return model
    return None


def _base_page(handoff: Mapping[str, Any], plan: Mapping[str, Any]) -> Dict[str, Any]:
    model = _source_model(handoff, plan.get("source_model_ref"))
    return {
        "question_ref": plan["question_ref"],
        "source_ref": plan.get("source_ref"),
        "section_ref": plan.get("section_ref"),
        "domain": plan.get("domain"),
        "title": _title(plan),
        "prompt": plan.get("learner_prompt") or "",
        "task_family_refs": list(plan.get("task_family_refs") or []),
        "capability_refs": list(plan.get("capability_refs") or []),
        "representations": _rep_blocks(plan),
        "response_demand": dict(plan.get("response_demand") or {}),
        "source_boundary_required": bool(plan.get("source_boundary_required", False)),
        "ambiguity": list(plan.get("ambiguity") or []),
        "source_issues": list(plan.get("source_issues") or []),
        "source_model": dict(model) if model else None,
        "misconception_watches": list(plan.get("misconception_watches") or []),
    }


def _cover(kind: str, source: Mapping[str, Any]) -> Dict[str, Any]:
    titles = {
        "STUDY_GUIDE": "Grade 4 English Study Guide",
        "WORKBOOK": "Grade 4 English Practice Workbook",
        "TEACHER_KEY": "Grade 4 English Teacher & Parent Diagnostic Key",
    }
    subtitles = {
        "STUDY_GUIDE": "Learn the idea, use a clue if needed, then try a fresh question.",
        "WORKBOOK": "Practice the same skills in fresh questions without copying the source worksheet.",
        "TEACHER_KEY": "Use observable work, response structure, and misconception probes — not labels about the child.",
    }
    return {
        "kind": "COVER",
        "title": titles[kind],
        "subtitle": subtitles[kind],
        "source_id": source.get("source_id", "SOURCE"),
        "grade": source.get("grade", 4),
    }


def build_study_guide_model(handoff: Mapping[str, Any]) -> Dict[str, Any]:
    pages: list[Dict[str, Any]] = [_cover("STUDY_GUIDE", handoff["source"])]
    for plan in handoff["learning_representation_plans"]:
        page = _base_page(handoff, plan)
        page.update(
            {
                "kind": "STUDY",
                "support": {
                    "H1": dict(plan["support"]["H1"]),
                    "H2": dict(plan["support"]["H2"]),
                    "H3": dict(plan["support"]["H3"]),
                },
                "fresh_retry": dict(plan["support"]["fresh_retry"]),
                "teaching_sequence": list(plan.get("teaching_sequence") or []),
            }
        )
        pages.append(page)
    return {"document_kind": "STUDY_GUIDE", "pages": pages}


def build_workbook_model(handoff: Mapping[str, Any]) -> Dict[str, Any]:
    pages: list[Dict[str, Any]] = [_cover("WORKBOOK", handoff["source"])]
    for plan in handoff["learning_representation_plans"]:
        page = _base_page(handoff, plan)
        page.update(
            {
                "kind": "WORKBOOK",
                "support": {
                    "H1": dict(plan["support"]["H1"]),
                    "H2": dict(plan["support"]["H2"]),
                    "H3": dict(plan["support"]["H3"]),
                },
                "fresh_retry": dict(plan["support"]["fresh_retry"]),
            }
        )
        pages.append(page)
    return {"document_kind": "WORKBOOK", "pages": pages}


def build_teacher_key_model(handoff: Mapping[str, Any]) -> Dict[str, Any]:
    pages: list[Dict[str, Any]] = [_cover("TEACHER_KEY", handoff["source"])]
    for plan in handoff["learning_representation_plans"]:
        page = _base_page(handoff, plan)
        response = page["response_demand"]
        page.update(
            {
                "kind": "TEACHER_KEY",
                "expected_evidence": list(response.get("evidence_parts") or []),
                "rubric_criteria": list(response.get("rubric_criteria") or []),
                "judgement_required": bool(response.get("teacher_or_source_judgement_required", False)),
                "support": {
                    "H1": dict(plan["support"]["H1"]),
                    "H2": dict(plan["support"]["H2"]),
                    "H3": dict(plan["support"]["H3"]),
                    "fresh_retry": dict(plan["support"]["fresh_retry"]),
                },
                "learner_evidence": list(plan.get("learner_evidence") or []),
            }
        )
        pages.append(page)
    return {"document_kind": "TEACHER_KEY", "pages": pages}


def assert_publication_model_safe(model: Mapping[str, Any]) -> None:
    """Fail closed on common publication-layer semantic leakage."""
    for page in model.get("pages") or []:
        if page.get("kind") == "COVER":
            continue
        response = page.get("response_demand") or {}
        if response.get("teacher_or_source_judgement_required"):
            forbidden = {"exact_answer", "model_answer", "correct_string"}
            if forbidden.intersection(page.keys()) or forbidden.intersection(response.keys()):
                raise ValueError(f"{page['question_ref']}: open response reduced to exact answer in publication")
        if page.get("source_boundary_required"):
            model_ref = page.get("source_model") or {}
            if not (model_ref.get("boundary_policy") or {}).get("no_force_fit"):
                raise ValueError(f"{page['question_ref']}: source boundary lost before publication")
        retry = (page.get("fresh_retry") or (page.get("support") or {}).get("fresh_retry") or {})
        if retry and retry.get("conceptual_support") != "H0":
            raise ValueError(f"{page['question_ref']}: fresh retry is not H0")
