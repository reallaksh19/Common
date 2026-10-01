#!/usr/bin/env python3
"""Fail-closed product-completeness authority for Chemistry LearningBlueprint v5.

v4 decides depth/research and learner conditioning.
v5 decides whether the planned learner artifact is actually a study product rather
than an executive summary, padded booklet, repeated generic template, or a set of
fully-completed visuals that never asks the learner to reconstruct technical structure.
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


def _validate_ttu(
    ttu: dict[str, Any],
    *,
    owner_id: str,
    product_mode: str,
    policy: dict[str, Any],
) -> tuple[str, str]:
    tp = policy["ttu_policy"]
    _require_fields(ttu, set(tp["required_fields"]), "CHEM_V5_TTU_REQUIRED_FIELD_MISSING")

    tid = ttu.get("ttu_id")
    if not isinstance(tid, str) or not tid.strip():
        raise BlueprintV5Error("CHEM_V5_TTU_ID_INVALID")
    if ttu.get("owner_id") != owner_id:
        raise BlueprintV5Error("CHEM_V5_TTU_OWNER_MISMATCH")
    ttype = ttu.get("ttu_type")
    if ttype not in set(tp["allowed_types"]):
        raise BlueprintV5Error("CHEM_V5_TTU_TYPE_INVALID")
    if ttu.get("cognitive_job") not in set(tp["allowed_cognitive_jobs"]):
        raise BlueprintV5Error("CHEM_V5_TTU_COGNITIVE_JOB_INVALID")
    if not str(ttu.get("learner_action", "")).strip():
        raise BlueprintV5Error("CHEM_V5_TTU_LEARNER_ACTION_MISSING")

    initial = ttu.get("initial_state")
    canonical = ttu.get("canonical_complete_state")
    if not isinstance(initial, dict) or not initial:
        raise BlueprintV5Error("CHEM_V5_TTU_INITIAL_STATE_MISSING")
    if not isinstance(canonical, dict) or not canonical:
        raise BlueprintV5Error("CHEM_V5_TTU_CANONICAL_STATE_MISSING")
    if initial == canonical:
        raise BlueprintV5Error("CHEM_V5_TTU_NOT_RECONSTRUCTABLE_ALREADY_COMPLETE")

    missing = ttu.get("missing_elements")
    if not isinstance(missing, list) or len(missing) < int(tp["minimum_missing_elements"]):
        raise BlueprintV5Error("CHEM_V5_TTU_MISSING_STRUCTURE_ABSENT")
    missing_ids: list[str] = []
    for element in missing:
        eid = element.get("element_id") if isinstance(element, dict) else None
        role = element.get("semantic_role") if isinstance(element, dict) else None
        if not isinstance(eid, str) or not eid.strip() or not isinstance(role, str) or not role.strip():
            raise BlueprintV5Error("CHEM_V5_TTU_MISSING_ELEMENT_INVALID")
        missing_ids.append(eid)
    if len(set(missing_ids)) != len(missing_ids):
        raise BlueprintV5Error("CHEM_V5_TTU_DUPLICATE_MISSING_ELEMENT")

    hints = ttu.get("hint_ladder")
    if not isinstance(hints, list) or not hints:
        raise BlueprintV5Error("CHEM_V5_TTU_HINT_LADDER_MISSING")
    targeted: set[str] = set()
    missing_set = set(missing_ids)
    for hint in hints:
        if not isinstance(hint, dict):
            raise BlueprintV5Error("CHEM_V5_TTU_HINT_INVALID")
        targets = hint.get("targets_missing_element_ids")
        if not isinstance(targets, list) or not targets or set(targets) - missing_set:
            raise BlueprintV5Error("CHEM_V5_TTU_HINT_NOT_BOUND_TO_MISSING_STRUCTURE")
        if not str(hint.get("hint_text", "")).strip():
            raise BlueprintV5Error("CHEM_V5_TTU_HINT_TEXT_MISSING")
        targeted.update(targets)
    if targeted != missing_set:
        raise BlueprintV5Error("CHEM_V5_TTU_HINT_COVERAGE_INCOMPLETE")

    if not str(ttu.get("verification_rule", "")).strip():
        raise BlueprintV5Error("CHEM_V5_TTU_VERIFICATION_MISSING")
    refs = ttu.get("representation_authority_refs")
    if not isinstance(refs, list) or not refs or any(not str(x).strip() for x in refs):
        raise BlueprintV5Error("CHEM_V5_TTU_REPRESENTATION_AUTHORITY_MISSING")
    if ttu.get("new_chemistry_refs", []) != []:
        raise BlueprintV5Error("CHEM_V5_TTU_NEW_CHEMISTRY_FORBIDDEN")

    expected_exposure = tp["exposure_modes"][product_mode]
    if ttu.get("exposure_mode") != expected_exposure:
        raise BlueprintV5Error("CHEM_V5_TTU_EXPOSURE_MODE_INVALID")
    return tid, ttype


def _validate_page_plan(
    page_plan: list[dict[str, Any]],
    policy: dict[str, Any],
    known_technical_ids: set[str],
    technical_id_field: str,
    known_ttu_ids: set[str],
) -> tuple[set[str], set[str]]:
    if not page_plan:
        raise BlueprintV5Error("CHEM_V5_PAGE_PLAN_MISSING")
    ppolicy = policy["page_architecture"]
    allowed_roles = set(ppolicy["allowed_page_roles"])
    content_min = float(ppolicy["content_page_min_active_area_ratio"])
    workspace_min = float(ppolicy["workspace_page_min_active_area_ratio"])
    page_ids: set[str] = set()
    rendered_technical_ids: set[str] = set()
    rendered_ttu_ids: set[str] = set()
    substantive_pages = 0

    for page in page_plan:
        _require_fields(
            page,
            {"page_id", "page_role", "expected_active_area_ratio", technical_id_field, "ttu_ids", "learner_action_ids"},
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

        technical_ids = page.get(technical_id_field, [])
        ttu_ids = page.get("ttu_ids", [])
        action_ids = page.get("learner_action_ids", [])
        if role != "COVER" and not technical_ids and not ttu_ids and not action_ids:
            raise BlueprintV5Error("CHEM_V5_PAGE_WITHOUT_TECHNICAL_JOB")

        unknown_technical = sorted(set(technical_ids) - known_technical_ids)
        if unknown_technical:
            raise BlueprintV5Error(f"CHEM_V5_PAGE_UNKNOWN_TECHNICAL_ID:{','.join(unknown_technical)}")
        unknown_ttu = sorted(set(ttu_ids) - known_ttu_ids)
        if unknown_ttu:
            raise BlueprintV5Error(f"CHEM_V5_PAGE_UNKNOWN_TTU_ID:{','.join(unknown_ttu)}")
        rendered_technical_ids.update(technical_ids)
        rendered_ttu_ids.update(ttu_ids)

        if role in {"WORKSPACE", "TTU_RECONSTRUCTION"}:
            if ratio < workspace_min:
                raise BlueprintV5Error("CHEM_V5_WORKSPACE_PAGE_TOO_EMPTY")
            if not action_ids or not str(page.get("workspace_justification", "")).strip():
                raise BlueprintV5Error("CHEM_V5_WORKSPACE_NOT_JUSTIFIED")
            if role == "TTU_RECONSTRUCTION" and not ttu_ids:
                raise BlueprintV5Error("CHEM_V5_TTU_PAGE_WITHOUT_TTU")
            substantive_pages += 1
        elif role != "COVER":
            if ratio < content_min:
                raise BlueprintV5Error("CHEM_V5_UNJUSTIFIED_EMPTY_PAGE_AREA")
            if role not in {"ROUTE_OR_MAP", "SUMMARY_OR_HANDOUT"}:
                substantive_pages += 1

    if substantive_pages == 0:
        raise BlueprintV5Error("CHEM_V5_SUMMARY_ONLY_ARTIFACT")
    return rendered_technical_ids, rendered_ttu_ids


def validate_study_product(product: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require_fields(
        product,
        {
            "schema_version", "product_mode", "bucket_ref", "difficulty_badge",
            "learning_atoms", "technical_objects", "reconstructable_ttus", "practice_closure",
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

    ttus = product["reconstructable_ttus"]
    if not isinstance(ttus, list) or not ttus:
        raise BlueprintV5Error("CHEM_V5_TTU_REQUIRED_FOR_STUDY_PRODUCT")
    ttu_ids: set[str] = set()
    ttu_types: set[str] = set()
    ttus_by_atom: dict[str, int] = {aid: 0 for aid in atom_set}
    for ttu in ttus:
        owner = ttu.get("owner_id") if isinstance(ttu, dict) else None
        if owner not in atom_set:
            raise BlueprintV5Error("CHEM_V5_TTU_OWNER_MISMATCH")
        tid, ttype = _validate_ttu(ttu, owner_id=owner, product_mode=mode, policy=policy)
        if tid in ttu_ids:
            raise BlueprintV5Error("CHEM_V5_TTU_DUPLICATE_ID")
        ttu_ids.add(tid)
        ttu_types.add(ttype)
        ttus_by_atom[owner] += 1
    missing_atoms = sorted(aid for aid, count in ttus_by_atom.items() if count < 1)
    if missing_atoms:
        raise BlueprintV5Error(f"CHEM_V5_TTU_MISSING_FOR_LEARNING_ATOM:{','.join(missing_atoms)}")
    if badge == "HARD" and len(atom_set) > 1 and len(ttu_types) < 2:
        raise BlueprintV5Error("CHEM_V5_HARD_TTU_TYPE_DIVERSITY_MISSING")

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
    bound_ttu_ids: set[str] = set()
    for entry in translations:
        ids = set(entry.get("technical_object_ids", []))
        if not ids or ids - object_ids:
            raise BlueprintV5Error("CHEM_V5_RESEARCH_TRANSLATION_TECHNICAL_BINDING_INVALID")
        entry_ttu_ids = set(entry.get("ttu_ids", []))
        if entry_ttu_ids - ttu_ids:
            raise BlueprintV5Error("CHEM_V5_RESEARCH_TRANSLATION_TTU_BINDING_INVALID")
        bound_ttu_ids.update(entry_ttu_ids)
    if badge == "HARD" and not bound_ttu_ids:
        raise BlueprintV5Error("CHEM_V5_HARD_RESEARCH_NOT_TRANSLATED_TO_TTU")

    rendered_objects, rendered_ttus = _validate_page_plan(
        product["page_plan"], policy, object_ids, "technical_object_ids", ttu_ids
    )
    missing_from_pages = sorted(object_ids - rendered_objects)
    if missing_from_pages:
        raise BlueprintV5Error(f"CHEM_V5_TECHNICAL_OBJECT_NOT_REALIZED:{','.join(missing_from_pages)}")
    missing_ttu_pages = sorted(ttu_ids - rendered_ttus)
    if missing_ttu_pages:
        raise BlueprintV5Error(f"CHEM_V5_TTU_NOT_REALIZED:{','.join(missing_ttu_pages)}")

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
        "ttu_count": len(ttus),
        "obligations_closed": True,
        "ttu_reconstruction_closed": True,
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
    all_ttu_ids: set[str] = set()
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

        ep_ttus = ep.get("reconstructable_ttus", [])
        if not ep_ttus:
            raise BlueprintV5Error(f"CHEM_V5_TTU_MISSING_FOR_QUESTION:{qid}")
        for ttu in ep_ttus:
            tid, _ = _validate_ttu(ttu, owner_id=qid, product_mode=mode, policy=policy)
            if tid in all_ttu_ids:
                raise BlueprintV5Error("CHEM_V5_TTU_DUPLICATE_ID")
            all_ttu_ids.add(tid)

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
    for key in ("attempt_path_count", "check_path_count", "full_solution_path_count", "ttu_path_count"):
        if coverage.get(key) != selected:
            raise BlueprintV5Error(f"CHEM_V5_QUESTION_EPISODE_CLOSURE_MISSING:{key}")

    rendered_steps, rendered_ttus = _validate_page_plan(
        product["page_plan"], policy, all_step_ids, "technical_step_ids", all_ttu_ids
    )
    missing_from_pages = sorted(all_step_ids - rendered_steps)
    if missing_from_pages:
        raise BlueprintV5Error(f"CHEM_V5_QUESTION_STEP_NOT_REALIZED:{','.join(missing_from_pages)}")
    missing_ttu_pages = sorted(all_ttu_ids - rendered_ttus)
    if missing_ttu_pages:
        raise BlueprintV5Error(f"CHEM_V5_TTU_NOT_REALIZED:{','.join(missing_ttu_pages)}")

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
        "ttu_count": len(all_ttu_ids),
        "episode_closure": True,
        "ttu_reconstruction_closed": True,
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
