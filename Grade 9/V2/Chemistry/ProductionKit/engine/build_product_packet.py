from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import ProductionKitError, digest, load_json, write_json


WORKSPACE_DEFAULT = "MEDIUM"


def _answer_map(answers: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(answer["question_id"]): answer for answer in answers}


def _representation_map(plan: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        item["question_id"]: list(item.get("requests") or [])
        for item in plan.get("question_plans") or []
    }


def _source_block(question: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "SOURCE",
        "label": "SOURCE / CONSTRUCTION REFERENCE",
        "text": question["source_display"],
        "source_refs": list(question.get("source_refs") or []),
    }


def _question_block(question: dict[str, Any]) -> dict[str, Any]:
    block = {
        "type": "QUESTION",
        "stem": question["stem"],
        "response_mode": question["response_mode"],
    }
    if question.get("options"):
        block["options"] = list(question["options"])
    if question.get("subparts"):
        block["subparts"] = list(question["subparts"])
    return block


def _clue_block(question: dict[str, Any], count: int) -> dict[str, Any] | None:
    if count <= 0:
        return None
    clues = list(question.get("technical_clues") or [])
    if len(clues) < count:
        raise ProductionKitError(
            "TECHNICAL_CLUES_MISSING",
            f"{question['question_id']}: profile requires {count}; authored {len(clues)}",
        )
    return {
        "type": "TECHNICAL_CLUES",
        "placement": "BOTTOM_OF_SHEET1",
        "clues": clues[:count],
    }


def build_product_packet(
    task: dict[str, Any],
    route_plan: dict[str, Any],
    questions: list[dict[str, Any]],
    answers: list[dict[str, Any]],
    representation_plan: dict[str, Any],
) -> dict[str, Any]:
    answer_by_id = _answer_map(answers)
    rep_by_id = _representation_map(representation_plan)
    profile = route_plan["profile"]
    workspace_table = profile["workspace_mm"]
    clue_count = int(profile.get("initial_clue_count", 0))
    source_on_sheet1 = bool(profile.get("source_on_sheet1"))
    max_pages = int(profile.get("max_pages_per_question", 2))
    if max_pages > 2:
        raise ProductionKitError("PRODUCTION_PAGE_BUDGET_INVALID", f"profile allows {max_pages} pages")

    packets: list[dict[str, Any]] = []
    for question in questions:
        qid = question["question_id"]
        answer = answer_by_id[qid]
        reps = rep_by_id.get(qid) or []
        if not reps:
            raise ProductionKitError("REPRESENTATION_PLAN_EMPTY", qid)

        demand = question.get("workspace_demand", WORKSPACE_DEFAULT)
        if demand not in workspace_table:
            raise ProductionKitError("WORKSPACE_DEMAND_UNKNOWN", f"{qid}: {demand}")
        workspace_mm = float(workspace_table[demand])

        sheet1_blocks: list[dict[str, Any]] = []
        if source_on_sheet1:
            if not str(question.get("source_display") or "").strip():
                raise ProductionKitError("CORE2A_SHEET1_SOURCE_MISSING", qid)
            sheet1_blocks.append(_source_block(question))
        sheet1_blocks.append(_question_block(question))
        sheet1_blocks.append(
            {
                "type": "REPRESENTATION_REQUESTS",
                "primitive_ids": [request["primitive_id"] for request in reps],
            }
        )
        sheet1_blocks.append(
            {
                "type": "WORKSPACE",
                "height_mm": workspace_mm,
                "demand": demand,
            }
        )
        clue_block = _clue_block(question, clue_count)
        if clue_block:
            sheet1_blocks.append(clue_block)

        sheet2_blocks: list[dict[str, Any]] = []
        if answer["response_mode"] == "OPEN_ENDED":
            sheet2_blocks.append(
                {
                    "type": "EXPECTED_RESPONSE",
                    "rubric": list(answer.get("expected_response_rubric") or []),
                }
            )
        else:
            sheet2_blocks.append(
                {
                    "type": "QUICK_CHECK",
                    "text": answer["quick_check"],
                    "final_unit_or_entity": answer.get("final_unit_or_entity"),
                }
            )
            sheet2_blocks.append(
                {
                    "type": "FULL_WORKING",
                    "steps": list(answer.get("full_working") or []),
                }
            )
        sheet2_blocks.append(
            {
                "type": "VERIFICATION",
                "checks": list(answer.get("verification") or []),
            }
        )

        sheets = [
            {"sheet_number": 1, "job": "ATTEMPT", "blocks": sheet1_blocks},
            {"sheet_number": 2, "job": "CHECK_AND_REPAIR", "blocks": sheet2_blocks},
        ]
        if len(sheets) > max_pages:
            raise ProductionKitError(
                "CORE2A_PAGE_BUDGET_EXCEPTION_UNJUSTIFIED" if task["product"] == "CORE2A" else "PRODUCTION_PAGE_BUDGET_EXCEEDED",
                qid,
            )

        packets.append(
            {
                "question_id": qid,
                "source_display": question["source_display"],
                "workspace_mm": workspace_mm,
                "representation_refs": [request["primitive_id"] for request in reps],
                "sheets": sheets,
            }
        )

    packet = {
        "task_id": task["task_id"],
        "product": task["product"],
        "purpose": task.get("purpose") if task["product"] == "CORE2A" else None,
        "profile_id": route_plan["profile_id"],
        "route": list(route_plan["stages"]),
        "questions": packets,
    }
    packet["packet_digest"] = digest(packet)
    return packet


def validate_product_packet(task: dict[str, Any], route_plan: dict[str, Any], packet: dict[str, Any]) -> None:
    expected = list(task["question_refs"])
    actual = [item["question_id"] for item in packet.get("questions") or []]
    if expected != actual:
        raise ProductionKitError("PRODUCT_PACKET_QUESTION_CUSTODY_MISMATCH", f"expected={expected}; actual={actual}")
    profile = route_plan["profile"]
    for item in packet["questions"]:
        sheets = item.get("sheets") or []
        if len(sheets) > int(profile.get("max_pages_per_question", 2)):
            raise ProductionKitError("PRODUCTION_PAGE_BUDGET_EXCEEDED", item["question_id"])
        if task["product"] == "CORE2A":
            sheet1 = sheets[0]
            source_blocks = [block for block in sheet1["blocks"] if block.get("type") == "SOURCE"]
            if len(source_blocks) != 1 or not source_blocks[0].get("text"):
                raise ProductionKitError("CORE2A_SHEET1_SOURCE_MISSING", item["question_id"])
            if sheet1["blocks"][-1].get("type") not in {"TECHNICAL_CLUES", "WORKSPACE"}:
                raise ProductionKitError("CORE2A_SHEET1_SUPPORT_ORDER_INVALID", item["question_id"])
        if not item.get("representation_refs"):
            raise ProductionKitError("PRODUCT_PACKET_REPRESENTATION_MISSING", item["question_id"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a render-ready Chemistry product packet")
    parser.add_argument("--task", required=True)
    parser.add_argument("--route-plan", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--answers", required=True)
    parser.add_argument("--representation-plan", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    task = load_json(args.task)
    route = load_json(args.route_plan)
    packet = build_product_packet(
        task,
        route,
        load_json(args.questions),
        load_json(args.answers),
        load_json(args.representation_plan),
    )
    validate_product_packet(task, route, packet)
    write_json(Path(args.out), packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
