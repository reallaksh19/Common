#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

from resolve_execution_authority import AGENT_TASKS_ROOT, render_preflight, resolve_authority

CONTRACTS = AGENT_TASKS_ROOT / "contracts"
TASK_KIND_REGISTRY = AGENT_TASKS_ROOT / "registry" / "task-kind-registry.v1.json"


class PacketCompilationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def _task_schema() -> dict[str, Any]:
    return _load_json(CONTRACTS / "execution-task.schema.json")


def _packet_schema() -> dict[str, Any]:
    schema = copy.deepcopy(_load_json(CONTRACTS / "execution-packet.schema.json"))
    schema["properties"]["task"] = _task_schema()
    return schema


def validate_task(task: dict[str, Any]) -> None:
    forbidden = {
        "engineering_ready",
        "technical_readiness",
        "publication_authorized",
        "consumer_permissions",
        "authority_bindings",
    }
    leaked = sorted(forbidden.intersection(task))
    if leaked:
        raise PacketCompilationError(
            "E_AGENT_MANUAL_AUTHORITY_ASSERTION",
            f"task contains derived/authoritative fields: {', '.join(leaked)}",
        )
    try:
        jsonschema.validate(task, _task_schema())
    except jsonschema.ValidationError as exc:
        raise PacketCompilationError("E_AGENT_TASK_SCHEMA", exc.message) from exc


def _task_kind(task_kind: str) -> dict[str, Any]:
    registry = _load_json(TASK_KIND_REGISTRY)
    matches = [row for row in registry["task_kinds"] if row["task_kind"] == task_kind]
    if len(matches) != 1:
        raise PacketCompilationError(
            "E_AGENT_TASK_KIND_UNRESOLVED",
            f"expected exactly one task-kind contract for {task_kind}; found {len(matches)}",
        )
    return matches[0]


def verify_packet_digest(packet: dict[str, Any]) -> None:
    expected = packet.get("packet_digest")
    if not isinstance(expected, str):
        raise PacketCompilationError("E_AGENT_PACKET_DIGEST_MISSING", "packet_digest missing")
    payload = {key: value for key, value in packet.items() if key != "packet_digest"}
    actual = digest(payload)
    if actual != expected:
        raise PacketCompilationError(
            "E_AGENT_PACKET_DIGEST_MISMATCH",
            f"expected {expected}; recomputed {actual}",
        )


def validate_packet(packet: dict[str, Any]) -> None:
    """Validate a compiled packet as custody infrastructure, never as domain/readiness authority."""
    try:
        jsonschema.validate(packet, _packet_schema())
    except jsonschema.ValidationError as exc:
        raise PacketCompilationError("E_AGENT_PACKET_SCHEMA", exc.message) from exc

    verify_packet_digest(packet)

    task = packet["task"]
    repository_state = packet["repository_state"]
    task_kind_contract = packet["task_kind_contract"]
    subject_adapter = packet["learning_engineering_state"]["subject_adapter"]

    if repository_state["repository"] != task["repository"]:
        raise PacketCompilationError(
            "E_AGENT_PACKET_REPOSITORY_MISMATCH",
            "repository_state.repository does not match task.repository",
        )
    if task_kind_contract["task_kind"] != task["task_kind"]:
        raise PacketCompilationError(
            "E_AGENT_PACKET_TASK_KIND_MISMATCH",
            "task-kind contract does not match task intent",
        )
    if str(subject_adapter["subject"]).casefold() != str(task["subject"]).casefold():
        raise PacketCompilationError(
            "E_AGENT_PACKET_SUBJECT_BINDING_MISMATCH",
            "bound subject adapter does not match task subject",
        )

    classes = [row["authority_class"] for row in packet["authority_bindings"]]
    if len(classes) != len(set(classes)):
        raise PacketCompilationError(
            "E_AGENT_PACKET_AUTHORITY_DUPLICATE",
            "authority classes must be unique",
        )
    missing = sorted(set(task_kind_contract["required_authority_classes"]) - set(classes))
    if missing:
        raise PacketCompilationError(
            "E_AGENT_REQUIRED_AUTHORITY_UNBOUND",
            f"missing authority bindings: {', '.join(missing)}",
        )

    subject_authority = [
        row for row in packet["authority_bindings"]
        if row["authority_class"] == "SUBJECT_GENERATION_AUTHORITY"
    ]
    if len(subject_authority) != 1:
        raise PacketCompilationError(
            "E_AGENT_PACKET_SUBJECT_AUTHORITY_UNRESOLVED",
            f"expected one SUBJECT_GENERATION_AUTHORITY binding; found {len(subject_authority)}",
        )
    if subject_authority[0]["path"] != subject_adapter["current_authority_manifest_ref"]:
        raise PacketCompilationError(
            "E_AGENT_PACKET_SUBJECT_AUTHORITY_MISMATCH",
            "subject authority binding does not match current subject-adapter authority ref",
        )

    preflight = packet["engineering_preflight"]
    if preflight["engineering_state"] != "NOT_EVALUATED":
        raise PacketCompilationError(
            "E_AGENT_PACKET_READINESS_ASSERTION",
            "delegation packet may not assert Engineering readiness",
        )
    if preflight["publication_authorization"] != "NOT_IMPLIED":
        raise PacketCompilationError(
            "E_AGENT_PACKET_PUBLICATION_ASSERTION",
            "delegation packet may not authorize publication",
        )


def compile_packet(
    task: dict[str, Any],
    *,
    repo_root: Path | None = None,
    head_sha: str | None = None,
    working_tree_state: str | None = None,
) -> dict[str, Any]:
    validate_task(task)
    kind = _task_kind(task["task_kind"])
    resolved = resolve_authority(
        task,
        repo_root=repo_root,
        head_sha=head_sha,
        working_tree_state=working_tree_state,
    )

    bound_classes = {row["authority_class"] for row in resolved["authority_bindings"]}
    missing = sorted(set(kind["required_authority_classes"]) - bound_classes)
    if missing:
        raise PacketCompilationError(
            "E_AGENT_REQUIRED_AUTHORITY_UNBOUND",
            f"missing authority bindings: {', '.join(missing)}",
        )

    packet: dict[str, Any] = {
        "schema_version": "1.0.0",
        "task": task,
        "repository_state": resolved["repository_state"],
        "task_kind_contract": {
            "task_kind": kind["task_kind"],
            "promotion_policy": kind["promotion_policy"],
            "allowed_change_classes": kind["allowed_change_classes"],
            "required_authority_classes": kind["required_authority_classes"],
            "required_outputs": kind["required_outputs"],
            "blueprint_change_policy": kind["blueprint_change_policy"],
        },
        "authority_bindings": resolved["authority_bindings"],
        "learning_engineering_state": resolved["learning_engineering_state"],
        "engineering_preflight": resolved["engineering_preflight"],
    }
    packet["packet_digest"] = digest(packet)
    validate_packet(packet)
    return packet


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile a deterministic, authority-bound execution packet")
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preflight-output", type=Path)
    args = parser.parse_args()

    task = _load_json(args.task)
    packet = compile_packet(task)
    text = json.dumps(packet, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")

    if args.preflight_output:
        resolved_view = {
            "repository_state": packet["repository_state"],
            "authority_bindings": packet["authority_bindings"],
            "learning_engineering_state": packet["learning_engineering_state"],
            "engineering_preflight": packet["engineering_preflight"],
        }
        args.preflight_output.parent.mkdir(parents=True, exist_ok=True)
        args.preflight_output.write_text(render_preflight(resolved_view, task), encoding="utf-8")


if __name__ == "__main__":
    main()
