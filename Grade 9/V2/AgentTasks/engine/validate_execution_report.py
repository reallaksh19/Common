#!/usr/bin/env python3
"""
Execution Report Validator.

Validates machine execution reports against execution-report.schema.json,
enforces separation between execution completion and engineering readiness,
and verifies fail-closed evidence rules for BLOCKED, HELD, and ready states.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from jsonschema import Draft202012Validator

SCRIPT_DIR = Path(__file__).resolve().parent
CONTRACTS_DIR = SCRIPT_DIR.parent / "contracts"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_report(
    report: Dict[str, Any],
    packet: Optional[Dict[str, Any]] = None
) -> List[str]:
    """Validate report dictionary and return list of failure messages."""
    errors: List[str] = []

    # 1. JSON Schema validation
    schema_path = CONTRACTS_DIR / "execution-report.schema.json"
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    for err in validator.iter_errors(report):
        errors.append(f"Schema violation at {err.json_path}: {err.message}")

    if errors:
        return errors

    # 2. BLOCKED / HELD require explicit blocker receipts
    exec_result = report.get("execution_result")
    eng_state = report.get("engineering_state")
    blockers = report.get("blockers", [])

    if exec_result == "BLOCKED" and len(blockers) == 0:
        errors.append("Invalid BLOCKED report: execution_result is BLOCKED but 'blockers' list is empty.")

    if eng_state == "HELD" and len(blockers) == 0:
        errors.append("Invalid HELD report: engineering_state is HELD but 'blockers' list is empty.")

    # 3. Engineering readiness must be backed by test evidence
    if eng_state == "ENGINEERING_GATE_READY":
        tests = report.get("tests", [])
        passing_tests = [t for t in tests if t.get("result") == "PASS"]
        if not passing_tests:
            errors.append(
                "Manual readiness violation: engineering_state is 'ENGINEERING_GATE_READY' "
                "but no test with result 'PASS' was recorded in 'tests'."
            )

    # 4. Memory dependency violation
    if report.get("memory_dependency_detected") is True:
        errors.append("Memory violation: memory_dependency_detected is true. Agent execution must be zero-memory reproducible.")

    # 5. Optional packet reconciliation
    if packet is not None:
        pkt_digest = packet.get("compiled_packet_digest")
        rep_pkt_digest = report.get("packet_identity", {}).get("compiled_packet_digest")
        if pkt_digest and rep_pkt_digest and pkt_digest != rep_pkt_digest:
            errors.append(f"Packet digest mismatch: report references {rep_pkt_digest[:12]}..., packet has {pkt_digest[:12]}...")

        pkt_head = packet.get("resolved_repository", {}).get("resolved_head")
        rep_head = report.get("start_head")
        if pkt_head and rep_head and rep_head != "UNKNOWN" and pkt_head != rep_head:
            errors.append(f"Starting HEAD mismatch: packet compiled at {pkt_head[:12]}..., execution started at {rep_head[:12]}...")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate execution report")
    parser.add_argument("report_file", type=Path, help="Path to report JSON")
    parser.add_argument("--packet", type=Path, default=None, help="Optional path to execution packet for reconciliation")

    args = parser.parse_args()
    report = load_json(args.report_file)
    packet = load_json(args.packet) if args.packet else None

    errors = validate_report(report, packet=packet)
    if errors:
        print(f"Report validation FAILED ({len(errors)} errors):")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    else:
        print("Report validation PASS: perfectly conformant.")


if __name__ == "__main__":
    main()
