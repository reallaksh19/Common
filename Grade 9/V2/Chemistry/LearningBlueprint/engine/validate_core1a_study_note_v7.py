#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


class Core1AStudyNoteError(ValueError):
    pass


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise Core1AStudyNoteError(f"{code}:{detail}" if detail else code)


def payload_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(payload_text(x) for x in value)
    if isinstance(value, dict):
        return " ".join(payload_text(v) for v in value.values())
    return str(value)


def nonempty_payload(value: Any) -> bool:
    if isinstance(value, str):
        return len(value.strip()) >= 3
    if isinstance(value, list):
        return bool(value) and all(nonempty_payload(x) for x in value)
    if isinstance(value, dict):
        return bool(value) and all(str(k).strip() and nonempty_payload(v) for k, v in value.items())
    return value is not None


def validate(authority: dict[str, Any], ccbom: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version", "authority_id", "subtopic_id", "subtopic_title", "difficulty_badge",
        "source_refs", "scope_statement", "learning_atoms", "content_objects",
        "reconstructable_ttu_refs", "practice_progression", "learner_surface_policy",
        "pagination_policy", "ccbom_ref", "completeness_summary"
    }
    missing = sorted(required - set(authority))
    if missing:
        fail("CHEM_V7_CORE1A_STUDY_AUTHORITY_REQUIRED_FIELD_MISSING", ",".join(missing))
    if authority["schema_version"] != "7.0.0":
        fail("CHEM_V7_CORE1A_STUDY_AUTHORITY_SCHEMA_INVALID")
    if authority["ccbom_ref"] != ccbom.get("ccbom_id"):
        fail("CHEM_V7_CORE1A_STUDY_CCBOM_REF_MISMATCH")
    if authority["subtopic_id"] != ccbom.get("subtopic_id"):
        fail("CHEM_V7_CORE1A_STUDY_SUBTOPIC_MISMATCH")

    source_refs = {x.get("ref") for x in authority["source_refs"] if isinstance(x, dict)}
    if len(source_refs) < 2 or None in source_refs or "" in source_refs:
        fail("CHEM_V7_CORE1A_STUDY_SOURCE_AUTHORITY_INCOMPLETE")
    source_roles = {x.get("role") for x in authority["source_refs"] if isinstance(x, dict)}
    if "SEMANTIC_AUTHORITY" not in source_roles or "PEDAGOGY_AUTHORITY" not in source_roles:
        fail("CHEM_V7_CORE1A_STUDY_SOURCE_ROLE_INCOMPLETE")

    ccbom_assets = {x.get("asset_id"): x for x in ccbom.get("assets", []) if isinstance(x, dict)}
    objects = authority["content_objects"]
    if not isinstance(objects, list) or not objects:
        fail("CHEM_V7_CORE1A_STUDY_CONTENT_OBJECTS_MISSING")
    by_id: dict[str, dict[str, Any]] = {}
    reps: set[str] = set()
    practice_levels: set[str] = set()
    class_counts: dict[str, int] = {}
    banned = [str(x).casefold() for x in authority["learner_surface_policy"].get("forbidden_internal_terms", [])]
    banned += [str(x).casefold() for x in policy["learner_surface"]["forbidden_internal_terms_default"]]

    for obj in objects:
        oid = str(obj.get("object_id", "")).strip()
        if not oid or oid in by_id:
            fail("CHEM_V7_CORE1A_STUDY_OBJECT_ID_INVALID", oid)
        by_id[oid] = obj
        if obj.get("source_ref") not in source_refs:
            fail("CHEM_V7_CORE1A_STUDY_OBJECT_SOURCE_UNRESOLVED", oid)
        if not nonempty_payload(obj.get("learner_payload")):
            fail("CHEM_V7_CORE1A_STUDY_OBJECT_PAYLOAD_EMPTY", oid)
        asset_id = obj.get("ccbom_asset_id")
        asset = ccbom_assets.get(asset_id)
        if not asset:
            fail("CHEM_V7_CORE1A_STUDY_OBJECT_CCBOM_UNRESOLVED", oid)
        core1a = (asset.get("core_dispositions") or {}).get("CORE1A", {})
        if core1a.get("disposition") not in {"MUST_REALIZE", "MUST_REFERENCE", "MUST_RECONSTRUCT"}:
            fail("CHEM_V7_CORE1A_STUDY_OBJECT_NOT_REQUIRED_BY_CCBOM", oid)
        if not str(core1a.get("realization_ref", "")).strip():
            fail("CHEM_V7_CORE1A_STUDY_OBJECT_REALIZATION_REF_MISSING", oid)
        cls = str(obj.get("object_class", ""))
        class_counts[cls] = class_counts.get(cls, 0) + 1
        if obj.get("representation_type"):
            reps.add(str(obj["representation_type"]))
        if obj.get("practice_level"):
            practice_levels.add(str(obj["practice_level"]))
        learner = payload_text(obj.get("learner_payload")).casefold()
        for term in banned:
            if term and re.search(r"(?<![a-z0-9_])" + re.escape(term) + r"(?![a-z0-9_])", learner):
                fail("CHEM_V7_CORE1A_STUDY_INTERNAL_JARGON_LEAK", f"{oid}:{term}")
        ascii_leaks = ["e-", "cu2+", "zn2+"]
        for token in ascii_leaks:
            if token in learner:
                fail("CHEM_V7_CORE1A_STUDY_ASCII_CHEMISTRY_LEAK", f"{oid}:{token}")

    expected_jobs = set(policy["required_jobs_per_learning_atom"])
    job_class = {
        "MEANING": {"MEANING", "PREREQUISITE_RECAP"},
        "RULE_OR_DECISION": {"RULE"},
        "REPRESENTATION_OR_EQUATION": {"REPRESENTATION", "EQUATION"},
        "REASONING_CHAIN": {"REASONING_CHAIN", "DERIVATION"},
        "BOUNDARY_OR_MISCONCEPTION": {"MISCONCEPTION_REPAIR", "BOUNDARY", "VERIFICATION"},
        "WORKED_OR_MODELED_EXAMPLE": {"WORKED_EXAMPLE"},
        "PRACTICE": {"GUIDED_PRACTICE", "INDEPENDENT_PRACTICE"},
        "ANSWER_CLOSURE": {"ANSWER"}
    }
    atom_ids: set[str] = set()
    for atom in authority["learning_atoms"]:
        aid = str(atom.get("atom_id", "")).strip()
        if not aid or aid in atom_ids:
            fail("CHEM_V7_CORE1A_STUDY_ATOM_ID_INVALID", aid)
        atom_ids.add(aid)
        jobs = atom.get("required_job_object_ids", {})
        if set(jobs) != expected_jobs:
            fail("CHEM_V7_CORE1A_STUDY_ATOM_JOB_SET_INCOMPLETE", aid)
        for job, oid in jobs.items():
            obj = by_id.get(oid)
            if not obj:
                fail("CHEM_V7_CORE1A_STUDY_ATOM_JOB_OBJECT_UNRESOLVED", f"{aid}:{job}:{oid}")
            if obj.get("learning_atom_id") != aid:
                fail("CHEM_V7_CORE1A_STUDY_ATOM_JOB_CROSS_BOUND", f"{aid}:{oid}")
            if obj.get("object_class") not in job_class[job]:
                fail("CHEM_V7_CORE1A_STUDY_ATOM_JOB_CLASS_INVALID", f"{aid}:{job}:{obj.get('object_class')}")

    orphan_atoms = sorted({str(o.get("learning_atom_id")) for o in objects} - atom_ids)
    if orphan_atoms:
        fail("CHEM_V7_CORE1A_STUDY_OBJECT_ATOM_UNRESOLVED", ",".join(orphan_atoms))

    prog = authority["practice_progression"]
    for field in ("worked_object_ids", "guided_object_ids", "independent_object_ids", "answer_object_ids"):
        if not prog.get(field):
            fail("CHEM_V7_CORE1A_STUDY_PRACTICE_PROGRESSION_INCOMPLETE", field)
        for oid in prog[field]:
            if oid not in by_id:
                fail("CHEM_V7_CORE1A_STUDY_PRACTICE_REF_UNRESOLVED", oid)
    if len(prog["answer_object_ids"]) < len(prog["guided_object_ids"]) + len(prog["independent_object_ids"]):
        fail("CHEM_V7_CORE1A_STUDY_PRACTICE_ANSWER_CLOSURE_INCOMPLETE")

    if authority["difficulty_badge"] == "HARD":
        minimums = policy["hard_minimums"]
        if len(reps) < int(minimums["representation_types"]):
            fail("CHEM_V7_CORE1A_STUDY_HARD_REPRESENTATION_DEPTH_LOW")
        if class_counts.get("MISCONCEPTION_REPAIR", 0) < int(minimums["misconception_repairs"]):
            fail("CHEM_V7_CORE1A_STUDY_HARD_MISCONCEPTION_DEPTH_LOW")
        if len(authority["reconstructable_ttu_refs"]) < int(minimums["reconstructable_ttu_refs"]):
            fail("CHEM_V7_CORE1A_STUDY_HARD_TTU_DEPTH_LOW")
        if not set(minimums["practice_levels"]) <= practice_levels:
            fail("CHEM_V7_CORE1A_STUDY_HARD_PRACTICE_LEVELS_INCOMPLETE")
        if class_counts.get("VERIFICATION", 0) < int(minimums["verification_objects"]):
            fail("CHEM_V7_CORE1A_STUDY_HARD_VERIFICATION_DEPTH_LOW")

    surface = authority["learner_surface_policy"]
    if surface.get("subject_language_only") is not True or surface.get("example_before_abstraction_when_helpful") is not True:
        fail("CHEM_V7_CORE1A_STUDY_LEARNER_SURFACE_POLICY_INVALID")
    pagination = authority["pagination_policy"]
    if pagination.get("mode") != "CONTENT_FIRST" or pagination.get("page_count_is_target") is not False or pagination.get("content_closure_precedes_pagination") is not True:
        fail("CHEM_V7_CORE1A_STUDY_PAGINATION_POLICY_INVALID")

    summary = authority["completeness_summary"]
    recomputed = {
        "learning_atom_count": len(atom_ids),
        "content_object_count": len(by_id),
        "equation_count": class_counts.get("EQUATION", 0),
        "representation_count": class_counts.get("REPRESENTATION", 0),
        "worked_example_count": class_counts.get("WORKED_EXAMPLE", 0),
        "misconception_repair_count": class_counts.get("MISCONCEPTION_REPAIR", 0),
        "practice_count": class_counts.get("GUIDED_PRACTICE", 0) + class_counts.get("INDEPENDENT_PRACTICE", 0),
        "answer_count": class_counts.get("ANSWER", 0)
    }
    for key, value in recomputed.items():
        if summary.get(key) != value:
            fail("CHEM_V7_CORE1A_STUDY_SUMMARY_DRIFT", f"{key}:{summary.get(key)}!={value}")
    if summary.get("unresolved_object_ids") != []:
        fail("CHEM_V7_CORE1A_STUDY_UNRESOLVED_OBJECTS")

    return {
        "status": "PASS",
        "subtopic_id": authority["subtopic_id"],
        "difficulty_badge": authority["difficulty_badge"],
        "learning_atom_count": len(atom_ids),
        "content_object_count": len(by_id),
        "ccbom_asset_count": len(ccbom_assets),
        "representation_types": sorted(reps),
        "practice_levels": sorted(practice_levels),
        "learner_surface_internal_jargon_leaks": 0,
        "pagination_mode": "CONTENT_FIRST"
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--authority", required=True)
    ap.add_argument("--ccbom", required=True)
    ap.add_argument("--policy", required=True)
    args = ap.parse_args()
    try:
        out = validate(load(args.authority), load(args.ccbom), load(args.policy))
    except Core1AStudyNoteError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
