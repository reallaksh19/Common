#!/usr/bin/env python3
"""Realize a Core1A bucket plan into a learner-facing semantic manuscript.

This module intentionally stops before page composition. It reorganizes only
existing C-G teaching authority and the governed Core1A bucket plan. It does not
invent new chemistry examples. Existing C-G practice prompts are treated as
open-response tasks and receive an explicit expected-response rubric derived
from their bound Appendix B solution/verification authority.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, field=None):
    value = copy.deepcopy(obj)
    if field:
        value.pop(field, None)
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def uniq(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def validate_upstream(bucket_plan, core1):
    if bucket_plan.get("core1_plan_ref") != core1.get("plan_id"):
        fail("CORE1A_MANUSCRIPT_UPSTREAM_MISMATCH", "Core1 ref")
    if bucket_plan.get("core1_plan_digest") != core1.get("plan_digest"):
        fail("CORE1A_MANUSCRIPT_UPSTREAM_MISMATCH", "Core1 digest")
    required = [l["capability_ref"] for l in core1["lessons"]]
    placed = []
    for bucket in bucket_plan["buckets"]:
        placed.extend(bucket["primary_capability_refs"] + bucket["supporting_capability_refs"])
    if Counter(required) != Counter(placed):
        fail("CORE1A_MANUSCRIPT_CAPABILITY_DRIFT")


def solution_tables(core1):
    appendix_a = core1["appendices"]["appendix_a"]["items"]
    appendix_b = core1["appendices"]["appendix_b"]["solutions"]
    by_solution = {row["solution_id"]: row for row in appendix_b}
    by_item = {row["item_ref"]: row for row in appendix_b}
    if len(by_solution) != len(appendix_b) or len(by_item) != len(appendix_b):
        fail("CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING", "duplicate Appendix B solution")
    return appendix_a, by_solution, by_item


def open_rubric(item, solution):
    criteria = uniq(
        list(solution.get("reasoning_steps", []))
        + list(solution.get("verification_steps", []))
        + ([solution["final_response"]] if solution.get("final_response") else [])
        + ([solution["condition_exception_note"]] if solution.get("condition_exception_note") else [])
    )
    if not criteria:
        fail("CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING", item["item_id"])
    return {
        "question_ref": item["item_id"],
        "answer_path_kind": "OPEN_RUBRIC",
        "learner_question_present": True,
        "answer_path_complete": True,
        "quick_check": None,
        "full_working": None,
        "expected_response_rubric": {
            "learner_label": "EXPECTED RESPONSE",
            "criteria": criteria,
        },
    }


def teaching_section(lesson, bucket):
    cap = lesson["capability_ref"]
    atoms = [a for a in bucket["learning_atoms"] if a["capability_ref"] == cap]
    reps = [r for r in bucket["representation_obligations"] if r["capability_ref"] == cap]
    if not atoms or not reps:
        fail("CORE1A_MANUSCRIPT_TEACHING_INCOMPLETE", cap)
    misconception = lesson.get("misconception_repair")
    worked = lesson.get("worked_example")
    return {
        "lesson_ref": lesson["lesson_id"],
        "capability_ref": cap,
        "lesson_mode": lesson["lesson_mode"],
        "activation": lesson.get("activation", ""),
        "see": lesson.get("familiar_macro_anchor", "") or lesson.get("activation", ""),
        "explain": [a["text"] for a in atoms if a["atom_kind"] in {"MEANING", "RULE_MODEL_CONDITION", "RECONSTRUCTION_STEP"}],
        "representation_refs": [r["representation_ref"] for r in reps],
        "watch_one": misconception.get("minimal_contrast") if misconception else None,
        "worked_example": copy.deepcopy(worked),
        "verification_steps": copy.deepcopy(lesson.get("verification_steps", [])),
        "transfer_bridge": lesson.get("transfer_bridge", ""),
    }


def practice_for_bucket(bucket, appendix_a, by_solution, by_item):
    caps = set(bucket["primary_capability_refs"] + bucket["supporting_capability_refs"])
    out = []
    for item in appendix_a:
        if item["primary_capability_ref"] not in caps:
            continue
        sol = None
        if item.get("solution_ref"):
            sol = by_solution.get(item["solution_ref"])
        if sol is None:
            sol = by_item.get(item["item_id"])
        if sol is None:
            fail("CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING", item["item_id"])
        out.append(
            {
                "item_ref": item["item_id"],
                "capability_ref": item["primary_capability_ref"],
                "support_stage": item["support_stage"],
                "prompt": item["prompt"],
                "answer_path": open_rubric(item, sol),
            }
        )
    return out


def build_manuscript(
    bucket_plan,
    core1,
    language_policy,
    answer_policy,
    manuscript_id="CHEM-C1A-MANUSCRIPT-PILOT-v1",
):
    validate_upstream(bucket_plan, core1)
    if language_policy.get("policy_id") != "CHEM-LEARNER-LANGUAGE-v1":
        fail("CORE1A_MANUSCRIPT_POLICY_MISMATCH", "learner language")
    if answer_policy.get("policy_id") != "CHEM-ANSWER-PATH-v1":
        fail("CORE1A_MANUSCRIPT_POLICY_MISMATCH", "answer path")
    if answer_policy.get("governing_rule") != "NO_LEARNER_FACING_QUESTION_WITHOUT_A_CHECKABLE_ANSWER_PATH":
        fail("CORE1A_MANUSCRIPT_POLICY_MISMATCH", "governing answer rule")

    lesson_by_cap = {l["capability_ref"]: l for l in core1["lessons"]}
    appendix_a, by_solution, by_item = solution_tables(core1)
    buckets = []
    for bucket in bucket_plan["buckets"]:
        caps = bucket["primary_capability_refs"] + bucket["supporting_capability_refs"]
        sections = []
        for cap in caps:
            if cap not in lesson_by_cap:
                fail("CORE1A_MANUSCRIPT_CAPABILITY_DRIFT", cap)
            sections.append(teaching_section(lesson_by_cap[cap], bucket))
        practice = practice_for_bucket(bucket, appendix_a, by_solution, by_item)
        buckets.append(
            {
                "bucket_id": bucket["bucket_id"],
                "learner_title": bucket["learner_title"],
                "bucket_invariant": bucket["bucket_invariant"],
                "teaching_sections": sections,
                "problem_family_routines": copy.deepcopy(bucket["problem_families"]),
                "practice_items": practice,
                "readiness_gate": copy.deepcopy(bucket["readiness_gate"]),
            }
        )

    practice_count = sum(len(b["practice_items"]) for b in buckets)
    open_count = sum(
        item["answer_path"]["answer_path_kind"] == "OPEN_RUBRIC"
        for bucket in buckets for item in bucket["practice_items"]
    )
    if practice_count != len(appendix_a):
        fail("CORE1A_MANUSCRIPT_PRACTICE_COVERAGE_DRIFT", f"required={len(appendix_a)} realized={practice_count}")
    if open_count != practice_count:
        fail("CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING", "practice closure")

    manuscript = {
        "manuscript_id": manuscript_id,
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "bucket_plan_ref": bucket_plan["plan_id"],
        "bucket_plan_digest": bucket_plan["plan_digest"],
        "core1_plan_ref": core1["plan_id"],
        "core1_plan_digest": core1["plan_digest"],
        "learner_language_policy_ref": language_policy["policy_id"],
        "answer_path_policy_ref": answer_policy["policy_id"],
        "buckets": buckets,
        "summary": {
            "bucket_count": len(buckets),
            "teaching_section_count": sum(len(b["teaching_sections"]) for b in buckets),
            "practice_question_count": practice_count,
            "open_rubric_count": open_count,
            "objective_question_count": 0,
            "answer_path_failures": 0,
            "status": "PASS",
        },
        "manuscript_digest": "",
    }
    manuscript["manuscript_digest"] = digest(manuscript, "manuscript_digest")
    validate_manuscript(manuscript, bucket_plan, core1, language_policy, answer_policy)
    return manuscript


def validate_manuscript(manuscript, bucket_plan, core1, language_policy, answer_policy):
    validate_upstream(bucket_plan, core1)
    if manuscript.get("manuscript_digest") != digest(manuscript, "manuscript_digest"):
        fail("CORE1A_MANUSCRIPT_DIGEST_MISMATCH")
    expected = {
        "bucket_plan_ref": bucket_plan["plan_id"],
        "bucket_plan_digest": bucket_plan["plan_digest"],
        "core1_plan_ref": core1["plan_id"],
        "core1_plan_digest": core1["plan_digest"],
        "learner_language_policy_ref": language_policy["policy_id"],
        "answer_path_policy_ref": answer_policy["policy_id"],
    }
    for key, value in expected.items():
        if manuscript.get(key) != value:
            fail("CORE1A_MANUSCRIPT_UPSTREAM_MISMATCH", key)
    if [b["bucket_id"] for b in manuscript["buckets"]] != [b["bucket_id"] for b in bucket_plan["buckets"]]:
        fail("CORE1A_MANUSCRIPT_BUCKET_ORDER_DRIFT")
    appendix_a, _, _ = solution_tables(core1)
    practice = [item for b in manuscript["buckets"] for item in b["practice_items"]]
    if Counter(i["item_ref"] for i in practice) != Counter(i["item_id"] for i in appendix_a):
        fail("CORE1A_MANUSCRIPT_PRACTICE_COVERAGE_DRIFT")
    for item in practice:
        ap = item["answer_path"]
        if ap.get("answer_path_kind") != "OPEN_RUBRIC" or not ap.get("answer_path_complete"):
            fail("CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING", item["item_ref"])
        rubric = ap.get("expected_response_rubric") or {}
        if rubric.get("learner_label") != "EXPECTED RESPONSE" or not rubric.get("criteria"):
            fail("CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING", item["item_ref"])
    summary = manuscript["summary"]
    if summary["practice_question_count"] != len(practice) or summary["open_rubric_count"] != len(practice):
        fail("CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING", "summary")
    if summary["answer_path_failures"] != 0 or summary["status"] != "PASS":
        fail("CORE1A_MANUSCRIPT_ANSWER_PATH_MISSING", "status")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket-plan", required=True)
    parser.add_argument("--core1-plan", required=True)
    parser.add_argument("--learner-language-policy", required=True)
    parser.add_argument("--answer-path-policy", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--manuscript-id", default="CHEM-C1A-MANUSCRIPT-PILOT-v1")
    args = parser.parse_args()
    out = build_manuscript(
        load(args.bucket_plan), load(args.core1_plan), load(args.learner_language_policy),
        load(args.answer_path_policy), args.manuscript_id,
    )
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
