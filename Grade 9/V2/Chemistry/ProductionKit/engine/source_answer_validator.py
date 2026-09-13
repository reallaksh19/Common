from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import ProductionKitError, digest, load_json, write_json


CLOSED_MODES = {"MCQ", "CONSTRUCTED_RESPONSE"}
VALID_RESPONSE_MODES = CLOSED_MODES | {"OPEN_ENDED"}


def validate_source_answer(
    task: dict[str, Any],
    route_plan: dict[str, Any],
    questions: list[dict[str, Any]],
    answers: list[dict[str, Any]],
) -> dict[str, Any]:
    expected_refs = list(task.get("question_refs") or [])
    q_by_id: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    for question in questions:
        qid = question.get("question_id")
        if qid in q_by_id:
            duplicates.append(str(qid))
        q_by_id[str(qid)] = question
    if duplicates:
        raise ProductionKitError("SOURCE_QUESTION_DUPLICATED", ", ".join(sorted(set(duplicates))))

    missing = [qid for qid in expected_refs if qid not in q_by_id]
    extra = [qid for qid in q_by_id if qid not in expected_refs]
    if missing or extra:
        raise ProductionKitError(
            "SOURCE_DENOMINATOR_MISMATCH",
            f"missing={missing}; extra={extra}",
        )

    a_by_id: dict[str, dict[str, Any]] = {}
    answer_duplicates: list[str] = []
    for answer in answers:
        qid = str(answer.get("question_id"))
        if qid in a_by_id:
            answer_duplicates.append(qid)
        a_by_id[qid] = answer
    if answer_duplicates:
        raise ProductionKitError("ANSWER_RECORD_DUPLICATED", ", ".join(sorted(set(answer_duplicates))))

    missing_answers = [qid for qid in expected_refs if qid not in a_by_id]
    extra_answers = [qid for qid in a_by_id if qid not in expected_refs]
    if missing_answers or extra_answers:
        raise ProductionKitError(
            "ANSWER_DENOMINATOR_MISMATCH",
            f"missing={missing_answers}; extra={extra_answers}",
        )

    profile = route_plan["profile"]
    source_on_sheet1 = bool(profile.get("source_on_sheet1"))
    closed_count = 0
    open_count = 0
    quick_checks = 0
    full_workings = 0
    rubrics = 0

    for qid in expected_refs:
        question = q_by_id[qid]
        answer = a_by_id[qid]
        stem = str(question.get("stem") or "").strip()
        if len(stem) < 5:
            raise ProductionKitError("SOURCE_STEM_MISSING", qid)

        mode = question.get("response_mode")
        if mode not in VALID_RESPONSE_MODES:
            raise ProductionKitError("SOURCE_RESPONSE_MODE_INVALID", f"{qid}: {mode}")
        if answer.get("response_mode") != mode:
            raise ProductionKitError("ANSWER_RESPONSE_MODE_MISMATCH", qid)

        integrity = question.get("source_integrity")
        if integrity != "CLEAN":
            raise ProductionKitError(
                "SOURCE_INTEGRITY_UNRESOLVED",
                f"{qid}: {integrity}; production requires an explicit clean/resolved source item",
            )

        source_display = str(question.get("source_display") or "").strip()
        source_refs = question.get("source_refs") or []
        if source_on_sheet1 and not source_display:
            raise ProductionKitError("CORE2A_SHEET1_SOURCE_MISSING", qid)
        if not source_display or not source_refs:
            raise ProductionKitError("SOURCE_TRACEABILITY_MISSING", qid)

        origin = question.get("origin")
        if origin == "GENERATED_ORIGINAL":
            if not any(ref.get("role") == "CONSTRUCTION_REFERENCE" for ref in source_refs):
                raise ProductionKitError(
                    "GENERATED_QUESTION_CONSTRUCTION_SOURCE_MISSING",
                    qid,
                )
            lowered = source_display.lower()
            if "official past question" in lowered and "not" not in lowered:
                raise ProductionKitError("GENERATED_QUESTION_FALSE_OFFICIAL_ATTRIBUTION", qid)

        capabilities = question.get("capability_refs") or []
        if not capabilities:
            raise ProductionKitError("QUESTION_CAPABILITY_BINDING_MISSING", qid)

        if mode == "MCQ" and len(question.get("options") or []) < 2:
            raise ProductionKitError("MCQ_OPTIONS_MISSING", qid)

        verification = answer.get("verification") or []
        if not verification:
            raise ProductionKitError("ANSWER_VERIFICATION_MISSING", qid)

        if mode in CLOSED_MODES:
            closed_count += 1
            quick = str(answer.get("quick_check") or "").strip()
            working = answer.get("full_working") or []
            if not quick:
                raise ProductionKitError("QUESTION_WITHOUT_ANSWER_CHECK", qid)
            if not working:
                raise ProductionKitError("QUESTION_WITHOUT_FULL_SOLUTION", qid)
            quick_checks += 1
            full_workings += 1
        else:
            open_count += 1
            rubric = answer.get("expected_response_rubric") or []
            if not rubric:
                raise ProductionKitError("OPEN_ENDED_ITEM_WITHOUT_RUBRIC", qid)
            rubrics += 1

    audit = {
        "task_id": task["task_id"],
        "question_total": len(expected_refs),
        "closed_question_total": closed_count,
        "open_question_total": open_count,
        "quick_checks_total": quick_checks,
        "full_workings_total": full_workings,
        "open_rubrics_total": rubrics,
        "missing_questions": [],
        "duplicate_questions": [],
        "missing_answers": [],
        "duplicate_answers": [],
        "source_on_sheet1_required": source_on_sheet1,
        "status": "PASS",
    }
    audit["audit_digest"] = digest(audit)
    return audit


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Chemistry source-question and answer closure")
    parser.add_argument("--task", required=True)
    parser.add_argument("--route-plan", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--answers", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    audit = validate_source_answer(
        load_json(args.task),
        load_json(args.route_plan),
        load_json(args.questions),
        load_json(args.answers),
    )
    write_json(Path(args.out), audit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
