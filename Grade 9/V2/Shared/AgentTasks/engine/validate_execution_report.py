#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema

from compile_execution_packet import AGENT_TASKS_ROOT, verify_packet_digest

CONTRACTS = AGENT_TASKS_ROOT / "contracts"


class ReportValidationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _binding_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (row["authority_class"], row["path"], row["sha256"])


def validate_report(packet: dict[str, Any], report: dict[str, Any]) -> None:
    verify_packet_digest(packet)
    try:
        jsonschema.validate(report, _load_json(CONTRACTS / "execution-report.schema.json"))
    except jsonschema.ValidationError as exc:
        raise ReportValidationError("E_AGENT_REPORT_SCHEMA", exc.message) from exc

    if report["task_id"] != packet["task"]["task_id"]:
        raise ReportValidationError("E_AGENT_REPORT_TASK_MISMATCH", "report belongs to another task")
    if report["packet_digest"] != packet["packet_digest"]:
        raise ReportValidationError("E_AGENT_REPORT_PACKET_MISMATCH", "report is not bound to this packet")

    expected_bindings = {_binding_key(row) for row in packet["authority_bindings"]}
    used_bindings = {_binding_key(row) for row in report["authority_bindings_used"]}
    if used_bindings != expected_bindings:
        missing = sorted(expected_bindings - used_bindings)
        extra = sorted(used_bindings - expected_bindings)
        raise ReportValidationError(
            "E_AGENT_REPORT_AUTHORITY_DRIFT",
            f"authority bindings differ; missing={missing}, extra={extra}",
        )

    packet_head = packet["repository_state"]["resolved_head"]
    if report["start_head"] != packet_head and report["execution_result"] != "STALE_PACKET":
        raise ReportValidationError(
            "E_AGENT_REPORT_STALE_PACKET_NOT_DECLARED",
            f"packet binds {packet_head} but execution started at {report['start_head']}",
        )

    allowed = set(packet["task_kind_contract"]["allowed_change_classes"])
    for row in report["changed_files"]:
        if row["change_class"] == "BLUEPRINT":
            raise ReportValidationError(
                "E_AGENT_BLUEPRINT_CHANGE_PROHIBITED",
                f"{row['path']} is a Blueprint change; open a separate new-invariant task instead",
            )
        if row["change_class"] not in allowed:
            raise ReportValidationError(
                "E_AGENT_CHANGE_CLASS_NOT_ALLOWED",
                f"{row['change_class']} is not allowed for {packet['task']['task_kind']}",
            )

    if report["publication_state"] not in {"NOT_IMPLIED", "INDEPENDENTLY_GOVERNED", "NOT_EVALUATED"}:
        raise ReportValidationError(
            "E_AGENT_PUBLICATION_ESCALATION",
            "delegation/Engineering state cannot authorize publication",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an execution report against its exact execution packet")
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    packet = _load_json(args.packet)
    report = _load_json(args.report)
    validate_report(packet, report)
    print("PASS: execution report is schema-valid and bound to the exact execution packet authority.")


if __name__ == "__main__":
    main()
