from __future__ import annotations

import argparse
from pathlib import Path

from build_product_packet import build_product_packet, validate_product_packet
from common import digest, load_json, write_json
from learning_representation import build_representation_plan, validate_representation_plan
from source_answer_validator import validate_source_answer
from task_router import route_task


def run(task_path: str, questions_path: str, answers_path: str, out_dir: str) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    task = load_json(task_path)
    questions = load_json(questions_path)
    answers = load_json(answers_path)

    route = route_task(task)
    write_json(out / "route_plan.json", route)

    audit = validate_source_answer(task, route, questions, answers)
    write_json(out / "source_answer_audit.json", audit)

    representations = build_representation_plan(task, route, questions)
    validate_representation_plan(representations, questions)
    write_json(out / "representation_plan.json", representations)

    packet = build_product_packet(task, route, questions, answers, representations)
    validate_product_packet(task, route, packet)
    write_json(out / "product_packet.json", packet)

    manifest = {
        "task_id": task["task_id"],
        "product": task["product"],
        "purpose": task.get("purpose") if task["product"] == "CORE2A" else None,
        "status": "PASS",
        "outputs": {
            "route_plan": "route_plan.json",
            "source_answer_audit": "source_answer_audit.json",
            "representation_plan": "representation_plan.json",
            "product_packet": "product_packet.json",
        },
        "digests": {
            "route": route["route_digest"],
            "audit": audit["audit_digest"],
            "representations": representations["representation_plan_digest"],
            "packet": packet["packet_digest"],
        },
    }
    manifest["manifest_digest"] = digest(manifest)
    write_json(out / "production_manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute the Chemistry Core1/Core2/Core1A/Core2A production kit")
    parser.add_argument("--task", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--answers", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    run(args.task, args.questions, args.answers, args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
