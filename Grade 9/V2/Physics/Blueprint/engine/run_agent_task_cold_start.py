#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

HERE = Path(__file__).resolve()
BLUEPRINT = HERE.parents[1]
PHYS = HERE.parents[2]
REPO = HERE.parents[5]
AGENT_ENGINE = REPO / "Grade 9" / "V2" / "Shared" / "AgentTasks" / "engine"
COLD_ENGINE = PHYS / "ColdStart" / "engine"
sys.path.insert(0, str(AGENT_ENGINE))
sys.path.insert(0, str(COLD_ENGINE))

from compile_execution_packet import digest as packet_digest  # noqa: E402
from consume_agent_task_packet import consume_execution_packet  # noqa: E402
from physics_cold_start_runner import compare_runs, load, run_cold_start  # noqa: E402

RECEIPT_SCHEMA = BLUEPRINT / "contracts" / "blueprint-agent-task-cold-start.schema.json"


class BlueprintAgentTaskColdStartError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str) -> None:
    raise BlueprintAgentTaskColdStartError(code, message)


def _validate_receipt(receipt: dict[str, Any]) -> None:
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(receipt, schema)
    except jsonschema.ValidationError as exc:
        raise BlueprintAgentTaskColdStartError(
            "E_BLUEPRINT_AGENT_COLDSTART_SCHEMA",
            exc.message,
        ) from exc


def _subject_manifest(packet: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    rows = [
        row
        for row in packet["authority_bindings"]
        if row["authority_class"] == "SUBJECT_GENERATION_AUTHORITY"
    ]
    if len(rows) != 1:
        fail(
            "E_BLUEPRINT_AGENT_COLDSTART_SUBJECT_AUTHORITY",
            f"expected one SUBJECT_GENERATION_AUTHORITY binding; found {len(rows)}",
        )
    path = repo_root / rows[0]["path"]
    if not path.is_file():
        fail("E_BLUEPRINT_AGENT_COLDSTART_MANIFEST_MISSING", rows[0]["path"])
    return load(path)


def run_packet_cold_start(
    packet: dict[str, Any],
    out_dir: Path | str,
    *,
    repo_root: Path | str = REPO,
) -> dict[str, Any]:
    """Traverse the existing Physics cold-start chain from an exact governed route receipt."""
    repo_root = Path(repo_root).resolve()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    intake_receipt = consume_execution_packet(packet, repo_root=repo_root)
    route = intake_receipt["execution_route"]
    if route["status"] != "RESOLVED_REPOSITORY_ROUTE" or not route["execution_authorized"]:
        fail(
            "E_BLUEPRINT_AGENT_COLDSTART_ROUTE_HELD",
            f"route state is {route['status']}",
        )
    if route["authorization_scope"] != "P-A_INPUT_SELECTION_ONLY":
        fail(
            "E_BLUEPRINT_AGENT_COLDSTART_ROUTE_SCOPE",
            route["authorization_scope"],
        )

    manifest = _subject_manifest(packet, repo_root)
    bindings = route["input_bindings"]
    no_attempt, _ = run_cold_start(
        manifest,
        out / "no-attempt",
        False,
        repo_root,
        run_id="PHY-AGENT-P-K-NO-ATTEMPT",
        assessment_input_bindings=bindings,
    )
    with_attempts, _ = run_cold_start(
        manifest,
        out / "with-attempts",
        True,
        repo_root,
        run_id="PHY-AGENT-P-K-WITH-ATTEMPTS",
        assessment_input_bindings=bindings,
    )
    comparison = compare_runs(
        no_attempt,
        with_attempts,
        comparison_id="PHY-AGENT-P-K-COMPARISON-v1",
    )
    failed = sorted(key for key, value in comparison["invariants"].items() if not value)
    if failed:
        fail(
            "E_BLUEPRINT_AGENT_COLDSTART_INVARIANT",
            ",".join(failed),
        )

    requirement_identical = (
        no_attempt["assessment_truth"]["engineering_gate_requirement_state"]
        == with_attempts["assessment_truth"]["engineering_gate_requirement_state"]
    )
    if not requirement_identical:
        fail(
            "E_BLUEPRINT_AGENT_COLDSTART_ENGINEERING_DRIFT",
            "learner evidence changed Engineering gate requirement state",
        )

    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "receipt_id": "PHY-BLUEPRINT-COLDSTART-" + packet["packet_digest"].split(":", 1)[1][:16],
        "packet_digest": packet["packet_digest"],
        "intake_receipt_digest": intake_receipt["receipt_digest"],
        "route_id": route["route_id"],
        "route_registry": route["route_registry"],
        "assessment_input_bindings": bindings,
        "no_attempt_report_digest": no_attempt["report_digest"],
        "with_attempts_report_digest": with_attempts["report_digest"],
        "comparison_digest": comparison["comparison_digest"],
        "comparison_invariants_all_true": True,
        "engineering": {
            "no_attempt_consumer_status": no_attempt["assessment_truth"]["engineering_consumer_status"],
            "with_attempts_consumer_status": with_attempts["assessment_truth"]["engineering_consumer_status"],
            "requirement_state_identical": True,
        },
        "publication_authorization": "NOT_IMPLIED",
        "human_review_authorization": "NOT_IMPLIED",
        "receipt_digest": "",
    }
    receipt["receipt_digest"] = packet_digest(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )
    _validate_receipt(receipt)

    (out / "comparison.json").write_text(
        json.dumps(comparison, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "agent-task-cold-start-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Physics P-A through P-K from a resolved repository-owned AgentTasks route"
    )
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=REPO)
    args = parser.parse_args()

    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    receipt = run_packet_cold_start(packet, args.out_dir, repo_root=args.repo_root)
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
