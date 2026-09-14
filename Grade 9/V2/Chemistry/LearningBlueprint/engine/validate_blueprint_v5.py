#!/usr/bin/env python3
"""Fail-closed product-completeness authority for Chemistry LearningBlueprint v5.

v4 decides depth/research and learner conditioning.
v5 decides whether the planned learner artifact is actually a study product rather
than an executive summary, padded booklet, or repeated generic template.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class BlueprintV5Error(ValueError):
    pass


def _require_fields(payload: dict[str, Any], fields: set[str], code: str) -> None:
    missing = sorted(fields - set(payload))
    if missing:
        raise BlueprintV5Error(f"{code}:{','.join(missing)}")


def _walk_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def _validate_page_plan(
    page_plan: list[dict[str, Any]],
    policy: dict[str, Any],
    known_ids: set[str],
    id_field: str,
) -> set[str]:
    if not page_plan:
        raise BlueprintV5Error("CHEM_V5_PAGE_PLAN_MISSING")
    ppolicy = policy["page_architecture"]
    allowed_roles = set(ppolicy["allowed_page_roles"])
    content_min = float(ppolicy["content_page_min_active_area_ratio"])
    workspace_min = float(ppolicy["workspace_page_min_active_area_ratio"])
    page_ids: set[str] = set()
    rendered_ids: set[str] = set()
    substantive_pages = 0

    for page in page_plan:
        _require_fields(
            page,
            {"page_id", "page_role", "expected_active_area_ratio", id_field, "learner_action_ids"},
            "CHEM_V5_PAGE_REQUIRED_FIELD_MISSING",
        )
        pid = page["page_id"]
        if pid in page_ids:
            raise BlueprintV5Error("CHEM_V5_DUPLICATE_PAGE_ID")
        page_ids.add(pid)
        role = page["page_role"]
        if role not in allowed_roles:
            raise BlueprintV5Error("CHEM_V5_PAGE_ROLE_INVALID")
        ratio = page["expected_active_area_ratio"]
        if not isinstance(ratio, (int, float)) or isinstance(ratio, bool) or ratio < 0 or ratio > 1:
            raise BlueprintV5Error("CHEM_V5_PAGE_ACTIVE_AREA_INVALID")

        technical_ids = page.get(id_field, [])
        action_ids = page.get("learner_action_ids", [])
        if role != "COVER" and not technical_ids and not action_ids:
            raise BlueprintV5Error("CHEM_V5_PAGE_WITHOUT_TECHNICAL_JOB")

        unknown = sorted(set(technical_ids) - known_ids)
        if unknown:
            raise BlueprintV5Error(f"CHEM_V5_PAGE_UNKNOWN_TECHNICAL_ID:{','.join(unknown)}")
        rendered_ids.update(technical_ids)

        if role == "WORKSPACE":
            if ratio < workspace_min:
                raise BlueprintV5Error("CHEM_V5_WORKSPACE_PAGE_TOO_EMPTY")
            if not action_ids or not str(page.get("workspace_justification", "")).strip():
                raise BlueprintV5Error("CHEM_V5_WORKSPACE_NOT_JUSTIFIED")
            substantive_pages += 1
        elif role != "COVER":
            if ratio < content_min:
                raise BlueprintV5Error("CHEM_V5_UNJUSTIFIED_EMPTY_PAGE_AREA")
            if role not in {"ROUTE_OR_MAP", "SUMMARY_OR_HANDOUT"}:
                substantive_pages += 1

    if substantive_pages == 0:
        raise BlueprintV5Error("CHEM_V5_SUMMARY_ONLY_ARTIFACT")
    return rendered_ids


def validate_study_product(product: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require_fields(
        product,
        {
            "schema_version", "product_mode", "bucket_ref", "difficulty_badge",
            "learning_atoms", "technical_objects", "practice_closure",
            "research_translation", "page_plan", "cross_core_reuse_audit",
        },
        "CHEM_V5_STUDY_REQUIRED_FIELD_MISSING",
    )
    if product["schema_version"] != "5.0.0":
        raise BlueprintV5Error("CHEM_V5_STUDY_SCHEMA_INVALID")
    mode = product["product_mode"]
    if mode not in {"CORE1A", "CORE1B"}:
        raise BlueprintV5Error("CHEM_V5_STUDY_MODE_INVALID")
    badge = product["difficulty_badge"]
    if badge not in {"EASY", "MEDIUM", "HARD"}:
        raise BlueprintV5Error("CHEM_V5_STUDY_DIFFICULTY_INVALID")

    forbidden_page_target_keys = {"target_pages", "minimum_pages", "page_count_target", "pad_to_pages"}
    leaked = sorted(forbidden_page_target_keys & set(_walk_keys(product)))
    if leaked:
        raise BlueprintV5Error(f"CHEM_V5_PAGE_COUNT_TARGETING_FORBIDDEN:{','.join(leaked)}")

    atoms = product["learning_atoms"]
    if not isinstance(atoms, list) or not atoms:
        raise BlueprintV5Error("CHEM_V5_STUDY_LEARNING_ATOMS_MISSING")
    atom_ids = [a.get("atom_id") for a in atoms]
    if len(set(atom_ids)) != len(atom_ids) or any(not x for x in atom_ids):
        raise BlueprintV5Error("CHEM_V5_STUDY_ATOM_ID_INVALID")
    atom_set = set(atom_ids)

    spolicy = policy["study_side"]
    mandatory_jobs = set(spolicy["core1a_required_jobs_per_learning_atom"] if mode == "CORE1A" else spolicy["core1b_required_jobs_per_learning_atom"])
    required_by_atom: dict[str, set[str]] = {}
    for atom in atoms:
        declared = set(atom.get("required_jobs", []))
        missing = sorted(mandatory_jobs - declared)
        if missing:
            raise BlueprintV5Error(f"CHEM_V5_STUDY_MANDATORY_JOB_OMITTED:{atom['atom_id']}:{','.join(missing)}")
        required_by_atom[atom["atom_id"]] = declared

    objects = product["technical_objects"]
    if not isinstance(objects, list) or not objects:
        raise BlueprintV5Error("CHEM_V5_STUDY_TECHNICAL_OBJECTS_MISSING")
    object_ids: set[str] = set()
    jobs_by_atom: dict[str, set[str]] = {aid: set() for aid in atom_set}
    for obj in objects:
        oid = obj.get("object_id")
        aid = obj.get("atom_id")
        job = obj.get("job")
        if not oid or oid in object_ids:
            raise BlueprintV5Error("CHEM_V5_STUDY_TECHNICAL_OBJECT_ID_INVALID")
        object_ids.add(oid)
        if aid not in atom_set:
            raise BlueprintV5Error("CHEM_V5_STUDY_TECHNICAL_OBJECT_ATOM_INVALID")
        if not job:
            raise BlueprintV5Error("CHEM_V5_STUDY_TECHNICAL_OBJECT_JOB_MISSING")
        jobs_by_atom[aid].add(job)

    for aid, required in required_by_atom.items():
        unclosed = sorted(required - jobs_by_atom[aid])
        if unclosed:
            raise BlueprintV5Error(f"CHEM_V5_STUDY_OBLIGATION_UNCLOSED:{aid}:{','.join(unclosed)}")

    if badge == "HARD":
        product_jobs = set().union(*jobs_by_atom.values())
        extras = set(spolicy["hard_bucket_additional_product_jobs"][mode])
        missing = sorted(extras - product_jobs)
        if missing:
            raise BlueprintV5Error(f"CHEM_V5_HARD_TECHNICAL_DEPTH_MISSING:{','.join(missing)}")

    closure = product["practice_closure"]
    if mode == "CORE1A":
        req = spolicy["practice_closure"]["CORE1A"]
        mapping = {
            "worked_count": req["worked_min"],
            "completion_count": req["completion_min"],
            "independent_count": req["independent_min"],
            "full_solution_count": req["full_solution_min"],
        }
        for key, minimum in mapping.items():
            value = closure.get(key)
            if not isinstance(value, int) or value < minimum:
                raise BlueprintV5Error(f"CHEM_V5_CORE1A_PRACTICE_CLOSURE_MISSING:{key}")
    else:
        atom_count = len(atoms)
        for key in (
            "constructive_task_count", "self_help_ladder_count",
            "canonical_response_count", "verification_check_count",
        ):
            value = closure.get(key)
            if not isinstance(value, int) or value < atom_count:
                raise BlueprintV5Error(f"CHEM_V5_CORE1B_CONSTRUCTIVE_CLOSURE_MISSING:{key}")

    translations = product["research_translation"]
    min_translations = 0 if badge == "EASY" else (1 if badge == "MEDIUM" else 2)
    if len(translations) < min_translations:
        raise BlueprintV5Error("CHEM_V5_RESEARCH_TO_CONTENT_TRANSLATION_MISSING")
    for entry in translations:
        ids = set(entry.get("technical_object_ids", []))
        if not ids or ids - object_ids:
            raise BlueprintV5Error("CHEM_V5_RESEARCH_TRANSLATION_TECHNICAL_BINDING_INVALID")

    rendered = _validate_page_plan(product["page_plan"], policy, object_ids, "technical_object_ids")
    missing_from_pages = sorted(object_ids - rendered)
    if missing_from_pages:
        raise BlueprintV5Error(f"CHEM_V5_TECHNICAL_OBJECT_NOT_REALIZED:{','.join(missing_from_pages)}")

    audit = product["cross_core_reuse_audit"]
    if audit.get("shared_expository_block_count") != 0:
        raise BlueprintV5Error("CHEM_V5_CROSS_CORE_EXPOSITORY_DUPLICATION")
    fraction = audit.get("repeated_generic_template_fraction")
    max_fraction = policy["anti_padding"]["repeated_generic_template_fraction_max"]
    if not isinstance(fraction, (int, float)) or fraction > max_fraction:
        raise BlueprintV5Error("CHEM_V5_GENERIC_TEMPLATE_REPETITION_EXCESSIVE")

    return {
        "status": "PASS",
        "product_mode": mode,
        "learning_atom_count": len(atoms),
        "technical_object_count": len(objects),
        "obligations_closed": True,
        "page_count_used_as_quality_metric": False,
        "summary_only": False,
    }


def validate_question_product(product: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require_fields(
        product,
        {
            "schema_version", "product_mode", "conditioning_ref", "question_ids",
            "episodes", "coverage_closure", "page_plan", "cross_core_reuse_audit",
        },
        "CHEM_V5_QUESTION_REQUIRED_FIELD_MISSING",
    )
    if product["schema_version"] != "5.0.0":
        raise BlueprintV5Error("CHEM_V5_QUESTION_SCHEMA_INVALID")
    mode = product["product_mode"]
    if mode not in {"CORE2A", "CORE2B"}:
        raise BlueprintV5Error("CHEM_V5_QUESTION_MODE_INVALID")
    if not str(product.get("conditioning_ref", "")).strip():
        raise BlueprintV5Error("CHEM_V5_QUESTION_CONDITIONING_REF_MISSING")

    qids = product["question_ids"]
    if not isinstance(qids, list) or not qids or len(set(qids)) != len(qids):
        raise BlueprintV5Error("CHEM_V5_QUESTION_IDS_INVALID")
    qset = set(qids)
    episodes = product["episodes"]
    if len(episodes) != len(qids):
        raise BlueprintV5Error("CHEM_V5_QUESTION_EPISODE_COUNT_MISMATCH")

    qpolicy = policy["question_side"]
    mandatory = set(qpolicy["core2a_required_jobs_per_question"] if mode == "CORE2A" else qpolicy["core2b_required_jobs_per_question"])
    all_step_ids: set[str] = set()
    episode_qids: set[str] = set()
    for ep in episodes:
        qid = ep.get("question_id")
        if qid not in qset or qid in episode_qids:
            raise BlueprintV5Error("CHEM_V5_QUESTION_EPISODE_ID_INVALID")
        episode_qids.add(qid)
        declared = set(ep.get("required_jobs", []))
        missing = sorted(mandatory - declared)
        if missing:
            raise BlueprintV5Error(f"CHEM_V5_QUESTION_MANDATORY_JOB_OMITTED:{qid}:{','.join(missing)}")

        if ep.get("source_class") == "SOURCE_CORE2":
            if ep.get("stem_custody") != "PRESERVED" or ep.get("provenance_custody") != "PRESERVED" or ep.get("answer_custody") != "PRESERVED":
                raise BlueprintV5Error("CHEM_V5_SOURCE_QUESTION_CUSTODY_DRIFT")

        steps = ep.get("technical_steps", [])
        if not steps:
            raise BlueprintV5Error("CHEM_V5_QUESTION_TECHNICAL_STEPS_MISSING")
        step_jobs: set[str] = set()
        local_ids: set[str] = set()
        for step in steps:
            sid = step.get("step_id")
            job = step.get("job")
            if not sid or sid in all_step_ids or sid in local_ids:
                raise BlueprintV5Error("CHEM_V5_QUESTION_STEP_ID_INVALID")
            local_ids.add(sid)
            all_step_ids.add(sid)
            if not job:
                raise BlueprintV5Error("CHEM_V5_QUESTION_STEP_JOB_MISSING")
            step_jobs.add(job)
        unclosed = sorted(declared - step_jobs)
        if unclosed:
            raise BlueprintV5Error(f"CHEM_V5_QUESTION_OBLIGATION_UNCLOSED:{qid}:{','.join(unclosed)}")

        hints = ep.get("hint_bindings", [])
        if "PROGRESSIVE_HINTS" in declared and not hints:
            raise BlueprintV5Error("CHEM_V5_CORE2B_PROGRESSIVE_HINTS_MISSING")
        for hint in hints:
            if hint.get("binds_to_step_id") not in local_ids:
                raise BlueprintV5Error("CHEM_V5_HINT_NOT_BOUND_TO_REASONING_STEP")

    coverage = product["coverage_closure"]
    selected = len(qids)
    if coverage.get("selected_question_count") != selected:
        raise BlueprintV5Error("CHEM_V5_QUESTION_COVERAGE_COUNT_INVALID")
    for key in ("attempt_path_count", "check_path_count", "full_solution_path_count"):
        if coverage.get(key) != selected:
            raise BlueprintV5Error(f"CHEM_V5_QUESTION_EPISODE_CLOSURE_MISSING:{key}")

    rendered = _validate_page_plan(product["page_plan"], policy, all_step_ids, "technical_step_ids")
    missing_from_pages = sorted(all_step_ids - rendered)
    if missing_from_pages:
        raise BlueprintV5Error(f"CHEM_V5_QUESTION_STEP_NOT_REALIZED:{','.join(missing_from_pages)}")

    audit = product["cross_core_reuse_audit"]
    if audit.get("shared_helper_prose_count") != 0:
        raise BlueprintV5Error("CHEM_V5_CROSS_CORE_HELPER_PROSE_DUPLICATION")
    fraction = audit.get("repeated_generic_template_fraction")
    max_fraction = policy["anti_padding"]["repeated_generic_template_fraction_max"]
    if not isinstance(fraction, (int, float)) or fraction > max_fraction:
        raise BlueprintV5Error("CHEM_V5_GENERIC_TEMPLATE_REPETITION_EXCESSIVE")

    return {
        "status": "PASS",
        "product_mode": mode,
        "question_count": selected,
        "episode_closure": True,
        "question_custody_closed": True,
        "page_count_used_as_quality_metric": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", required=True)
    parser.add_argument("--study-product")
    parser.add_argument("--question-product")
    args = parser.parse_args()
    if bool(args.study_product) == bool(args.question_product):
        raise SystemExit("supply exactly one of --study-product or --question-product")
    policy = json.loads(Path(args.policy).read_text(encoding="utf-8"))
    if args.study_product:
        payload = json.loads(Path(args.study_product).read_text(encoding="utf-8"))
        result = validate_study_product(payload, policy)
    else:
        payload = json.loads(Path(args.question_product).read_text(encoding="utf-8"))
        result = validate_question_product(payload, policy)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
