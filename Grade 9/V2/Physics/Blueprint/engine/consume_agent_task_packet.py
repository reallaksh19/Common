#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema

HERE = Path(__file__).resolve()
BLUEPRINT = HERE.parents[1]
REPO = HERE.parents[5]
AGENT_ENGINE = REPO / "Grade 9" / "V2" / "Shared" / "AgentTasks" / "engine"
sys.path.insert(0, str(AGENT_ENGINE))

from compile_execution_packet import PacketCompilationError, digest, validate_packet  # noqa: E402

RECEIPT_SCHEMA = BLUEPRINT / "contracts" / "blueprint-agent-task-intake.schema.json"


class BlueprintAgentTaskIntakeError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str) -> None:
    raise BlueprintAgentTaskIntakeError(code, message)


def _git_head(repo_root: Path = REPO) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise BlueprintAgentTaskIntakeError(
            "E_BLUEPRINT_REPOSITORY_HEAD_UNRESOLVED",
            "cannot resolve current repository HEAD",
        ) from exc
    return proc.stdout.strip()


def _safe_repo_file(repo_root: Path, relative_path: str) -> Path:
    rel = Path(relative_path)
    if rel.is_absolute() or ".." in rel.parts:
        fail("E_BLUEPRINT_BOUND_AUTHORITY_PATH_INVALID", relative_path)
    path = repo_root / rel
    if not path.is_file():
        fail("E_BLUEPRINT_BOUND_AUTHORITY_MISSING", relative_path)
    return path


def _file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _verify_bound_authorities(packet: dict[str, Any], repo_root: Path) -> None:
    for binding in packet["authority_bindings"]:
        path = _safe_repo_file(repo_root, binding["path"])
        actual = _file_digest(path)
        if actual != binding["sha256"]:
            fail(
                "E_BLUEPRINT_BOUND_AUTHORITY_DRIFT",
                f"{binding['authority_class']} expected {binding['sha256']} but current file is {actual}",
            )


def _validate_receipt(receipt: dict[str, Any]) -> None:
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(receipt, schema)
    except jsonschema.ValidationError as exc:
        raise BlueprintAgentTaskIntakeError(
            "E_BLUEPRINT_TASK_INTAKE_SCHEMA",
            exc.message,
        ) from exc


def consume_execution_packet(
    packet: dict[str, Any],
    *,
    current_head: str | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Accept delegation context without accepting scope, truth, readiness, or release authority."""
    try:
        validate_packet(packet)
    except PacketCompilationError as exc:
        raise BlueprintAgentTaskIntakeError(
            "E_BLUEPRINT_EXECUTION_PACKET_INVALID",
            f"{exc.code}: {exc.message}",
        ) from exc

    task = packet["task"]
    if str(task["subject"]).casefold() != "physics":
        fail(
            "E_BLUEPRINT_TASK_SUBJECT_MISMATCH",
            f"Physics Blueprint cannot consume subject {task['subject']}",
        )

    repo_root = (repo_root or REPO).resolve()
    actual_head = current_head or _git_head(repo_root)
    packet_head = packet["repository_state"]["resolved_head"]
    if packet_head != actual_head:
        fail(
            "E_BLUEPRINT_EXECUTION_PACKET_STALE",
            f"packet binds {packet_head} but Blueprint checkout is {actual_head}",
        )
    _verify_bound_authorities(packet, repo_root)

    # These assertions are deliberately redundant with the Shared packet schema.
    # They make the Blueprint consumer boundary explicit and fail closed if that
    # upstream contract ever changes without coordinated review.
    preflight = packet["engineering_preflight"]
    if preflight["engineering_state"] != "NOT_EVALUATED":
        fail(
            "E_BLUEPRINT_PACKET_READINESS_NOT_CONSUMABLE",
            "Blueprint must recompute Engineering readiness from governed scope",
        )
    if preflight["publication_authorization"] != "NOT_IMPLIED":
        fail(
            "E_BLUEPRINT_PACKET_PUBLICATION_NOT_CONSUMABLE",
            "delegation packet cannot authorize publication",
        )
    if any(
        row["status"] != "NOT_EVALUATED"
        for row in preflight["consumer_permissions"].values()
    ):
        fail(
            "E_BLUEPRINT_PACKET_CONSUMER_PERMISSION_NOT_CONSUMABLE",
            "delegation packet cannot authorize Blueprint consumers",
        )

    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "receipt_id": "PHY-BLUEPRINT-TASK-INTAKE-" + packet["packet_digest"].split(":", 1)[1][:16],
        "status": "ACCEPTED_AS_DELEGATION_CONTEXT",
        "packet_digest": packet["packet_digest"],
        "repository_head": actual_head,
        "task_id": task["task_id"],
        "task_kind": task["task_kind"],
        "execution_intent": {
            "engineering_depth": task["engineering_depth"],
            "learner_state": task["learner_state"],
            "web_research_allowed": task["web_research_allowed"],
            "target_consumers": list(task["target_consumers"]),
            "write_mode": task["write_mode"],
        },
        "non_authoritative_labels": {
            "grade": task["grade"],
            "curriculum": dict(task["curriculum"]),
            "topic": task["topic"],
            "subtopic": task["subtopic"],
        },
        "authority_boundary": {
            "packet_authority_use": "DELEGATION_CONTEXT_ONLY",
            "scope_selection": "REPOSITORY_GOVERNED_NOT_PACKET",
            "domain_truth": "REPOSITORY_GOVERNED_NOT_PACKET",
            "engineering_readiness": "RECOMPUTE_FROM_GOVERNED_SCOPE",
            "learner_state_effect": "TREATMENT_CONTEXT_ONLY_NOT_DOMAIN_TRUTH",
            "consumer_permissions": "NOT_AUTHORIZED_BY_PACKET",
            "publication": "NOT_AUTHORIZED_BY_PACKET",
        },
        "receipt_digest": "",
    }
    receipt["receipt_digest"] = digest({k: v for k, v in receipt.items() if k != "receipt_digest"})
    _validate_receipt(receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a Shared AgentTasks packet as non-authoritative Physics Blueprint delegation context"
    )
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    receipt = consume_execution_packet(packet)
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
