from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from v3lib import load_yaml, validate_schema


def render(package: dict[str, Any]) -> str:
    errors = validate_schema("local-execution", package, "LOCAL_EXECUTION")
    if errors:
        raise RuntimeError("; ".join(errors))

    request = package["request"]
    basis = request["exact_basis"]
    contract = package["return_contract"]
    lines = [
        "# Engineering Relay V3.1 — Local Execution Request",
        "",
        "## Purpose",
        request["purpose"],
        "",
        "## Exact basis",
        f"- Request: {request['id']}",
        f"- Mode: {request['mode']}",
        f"- EP: {basis.get('ep') or 'NONE'}",
        f"- Work package: {basis.get('work_package') or 'NONE'}",
        f"- Branch: {basis['branch']}",
        f"- Required HEAD: {basis['material_head']}",
        "",
        "## Repository / checkout",
        f"- Clone URL: {(package.get('repository') or {}).get('clone_url') or 'DISPATCHER MUST SUPPLY'}",
        f"- Branch: {(package.get('repository') or {}).get('branch')}",
        f"- Required HEAD: {(package.get('repository') or {}).get('required_head')}",
    ]
    lines.extend(f"{i}. {item}" for i, item in enumerate((package.get("repository") or {}).get("checkout_instructions") or [], 1))
    lines += [
        "",
        "## Preflight",
    ]
    lines.extend(f"{i}. {item}" for i, item in enumerate(request["preflight"], 1))
    lines += ["", "## Run"]
    for step in request["steps"]:
        lines.append(f"- **{step['id']}** — {step['instruction']}")
        if step.get("command"):
            lines.append(f"  - Command: {step['command']}")
        lines.append(f"  - Working directory: {step['working_directory']}")
        lines.append(f"  - Expected: {step['expected_result']}")

    lines += ["", "## Stop conditions"]
    lines.extend(f"- {item}" for item in request["stop_conditions"])
    lines += ["", "## Do not"]
    lines.extend(f"- {item}" for item in request["prohibited_actions"])
    provider_return = package.get("provider_return") or {}
    lines += [
        "",
        "## Provider sub-issue update",
        f"- Target: {provider_return.get('target_sub_issue') or 'MUST BE SET BEFORE DISPATCH'}",
        f"- Required: {'YES' if provider_return.get('update_required') else 'NO'}",
        f"- {provider_return.get('instruction')}",
    ]
    for item in provider_return.get("required_content") or []:
        lines.append(f"- Include: {item}")

    lines += [
        "",
        "## Return exactly this contract",
        f"- REQUEST_ID: {contract['request_id']}",
        "- RESULT: PASS | FAIL | BLOCKED | NOT_RUN_ENVIRONMENT | NOT_RUN_INFRASTRUCTURE | HEAD_MISMATCH",
        "- OBSERVED_HEAD:",
        "- ENVIRONMENT:",
        "- COMMAND_RESULTS:",
        "- FAILURES:",
        "- ARTIFACTS:",
        "",
        "## Continuation",
        f"- {contract['resume_owner']['responsibility']}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a recipient-ready V3.1 local execution request.")
    parser.add_argument("package", help="Path to relay-v3.1-local-execution YAML.")
    args = parser.parse_args()
    print(render(load_yaml(Path(args.package))), end="")


if __name__ == "__main__":
    main()
