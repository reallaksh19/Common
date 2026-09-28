#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from v3lib import validate_schema


def load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("agent status must be a mapping")
    return value


def _value(v: Any) -> str:
    if v is None:
        return "NONE"
    return str(v)


def render(value: dict[str, Any]) -> str:
    errors = validate_schema("agent-status", value, "AGENT_STATUS_V1")
    if errors:
        raise ValueError("; ".join(errors))

    agent = value["agent"]
    protocol = value["protocol_basis"]
    responsibility = value["responsibility"]
    plan = value["plan"]
    material = value["material"]
    rll = value["rll"]
    delivery = value["delivery"]
    handover = value["handover"]

    lines = [
        "AGENT_STATUS_V1",
        "",
        "AUTHORITY: DERIVED_EXECUTION_CONTINUITY",
        "",
        "## Agent",
        f"- executor: {agent['executor']}",
        f"- custody_epoch: {agent['custody_epoch']}",
        f"- continuation: {agent['continuation']}",
        f"- status: {agent['status']}",
        "",
        "## Protocol basis",
        f"- V3.1",
        f"- Common@{protocol['common_sha']}",
        f"- {protocol['two_pass_revision']}",
        "",
        "## Responsibility",
        f"- issue: #{responsibility['issue']}",
        f"- ep: {_value(responsibility['ep'])}",
        f"- work_package: {_value(responsibility['work_package'])}",
        "",
        "## Plan",
        f"- implementation_plan: {_value(plan['implementation_plan'])}",
        f"- plan_revision: {_value(plan['plan_revision'])}",
        f"- latest_plan_update: {_value(plan['latest_plan_update'])}",
        f"- latest_task_evidence: {_value(plan['latest_task_evidence'])}",
        f"- latest_task_result: {_value(plan['latest_task_result'])}",
        "",
        "## Material",
        f"- branch: {_value(material['branch'])}",
        f"- primary_pr: {_value(material['primary_pr'])}",
        f"- base: {_value(material['base'])}",
        f"- head: {_value(material['head'])}",
        "",
        "## Current",
        value["current"],
        "",
        "## Completed",
    ]

    if value["completed"]:
        for item in value["completed"]:
            evidence = ", ".join(item["evidence"]) if item["evidence"] else "NONE"
            lines.append(f"- {item['id']}: {item['statement']} — evidence: {evidence}")
    else:
        lines.append("- NONE")

    lines += ["", "## Further task"]
    if value["further_tasks"]:
        for item in value["further_tasks"]:
            lines += [
                "",
                item["id"],
                f"- state: {item['state']}",
                f"- statement: {item['statement']}",
                f"- depends_on: {_value(item['depends_on'])}",
                f"- unblock_condition: {_value(item['unblock_condition'])}",
                f"- expected_evidence: {_value(item['expected_evidence'])}",
                f"- target: {_value(item['target'])}",
                f"- evidence: {item['evidence'] if item['evidence'] else 'NONE'}",
            ]
            if item.get("reason_class"):
                lines.append(f"- reason_class: {item['reason_class']}")
    else:
        lines.append("- None within this responsibility.")

    lines += ["", "## Pending / blocked"]
    if value["pending_items"]:
        for item in value["pending_items"]:
            lines += [
                f"- {item['id']} — {item['state']} / {item['reason_class']}: {item['statement']}",
                f"  - owner: {_value(item['owner'])}",
                f"  - dependency: {_value(item['dependency'])}",
                f"  - unblock_condition: {_value(item['unblock_condition'])}",
                f"  - expected_next_observable: {_value(item['expected_next_observable'])}",
                f"  - evidence_refs: {item['evidence_refs'] if item['evidence_refs'] else 'NONE'}",
            ]
    else:
        lines.append("- NONE")

    lines += ["", "## Reasoning refs"]
    lines += [f"- {ref}" for ref in value["reasoning_refs"]] or ["- NONE"]

    lines += ["", "## Local Agent / OFFLOAD"]
    if value["offloads"]:
        for row in value["offloads"]:
            lines.append(
                f"- {row['id']}: {row['state']} / {row['engineering_result']} — "
                f"provider_issue={_value(row['provider_issue'])} — "
                f"latest_result_ref={_value(row['latest_result_ref'])} — "
                f"consumer_consequence={_value(row['consumer_consequence'])}"
            )
    else:
        lines.append("- NONE")

    lines += [
        "",
        "## RLL",
        f"- transport: {rll['transport']}",
        f"- state: {rll['state']}",
        f"- execution_ref: {_value(rll['execution_ref'])}",
        f"- worker_state_ref: {_value(rll['worker_state_ref'])}",
        f"- engineering_result: {rll['engineering_result']}",
        "",
        "## Delivery",
        f"- lifecycle: {delivery['lifecycle']}",
        f"- relationship: {delivery['relationship']}",
    ]
    if delivery["related_prs"]:
        for row in delivery["related_prs"]:
            lines.append(
                f"- PR #{row['pr']}: {row['relationship']} / {row['lifecycle']} / head={_value(row['head'])}"
            )
    else:
        lines.append("- related_prs: NONE")

    lines += ["", "## Negative knowledge"]
    lines += [f"- {row}" for row in value["negative_knowledge"]] or ["- NONE"]

    lines += [
        "",
        "## Handover",
        f"- predecessor_status_ref: {_value(handover['predecessor_status_ref'])}",
        "- successor_first_action:",
    ]
    if handover["successor_first_action"]:
        lines += [f"  {i}. {row}" for i, row in enumerate(handover["successor_first_action"], 1)]
    else:
        lines.append("  1. NONE")

    lines += ["", f"updated_at: {value['updated_at']}"]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate/render AGENT_STATUS_V1 normalized YAML.")
    parser.add_argument("artifact")
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    value = load(Path(args.artifact))
    errors = validate_schema("agent-status", value, "AGENT_STATUS_V1")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    if args.render:
        print(render(value), end="")
    else:
        print("PASS")


if __name__ == "__main__":
    main()
