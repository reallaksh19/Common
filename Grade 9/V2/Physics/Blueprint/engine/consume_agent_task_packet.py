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
ROUTE_REGISTRY_SCHEMA = BLUEPRINT / "contracts" / "blueprint-execution-route-registry.schema.json"


class BlueprintAgentTaskIntakeError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str) -> None:
    raise BlueprintAgentTaskIntakeError(code, message)


def _git(repo_root: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise BlueprintAgentTaskIntakeError(
            "E_BLUEPRINT_REPOSITORY_STATE_UNRESOLVED",
            f"cannot resolve repository state for {' '.join(args)}",
        ) from exc
    return proc.stdout.strip()


def _git_head(repo_root: Path = REPO) -> str:
    return _git(repo_root, "rev-parse", "HEAD")


def _git_working_tree_state(repo_root: Path = REPO) -> str:
    return "CLEAN" if _git(repo_root, "status", "--porcelain") == "" else "DIRTY"


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


def _load_json(path: Path, *, code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BlueprintAgentTaskIntakeError(code, str(path)) from exc
    if not isinstance(value, dict):
        fail(code, f"expected JSON object: {path}")
    return value


def _verify_bound_authorities(packet: dict[str, Any], repo_root: Path) -> None:
    for binding in packet["authority_bindings"]:
        path = _safe_repo_file(repo_root, binding["path"])
        actual = _file_digest(path)
        if actual != binding["sha256"]:
            fail(
                "E_BLUEPRINT_BOUND_AUTHORITY_DRIFT",
                f"{binding['authority_class']} expected {binding['sha256']} but current file is {actual}",
            )


def _subject_generation_manifest(packet: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    rows = [
        row
        for row in packet["authority_bindings"]
        if row["authority_class"] == "SUBJECT_GENERATION_AUTHORITY"
    ]
    if len(rows) != 1:
        fail(
            "E_BLUEPRINT_SUBJECT_AUTHORITY_UNRESOLVED",
            f"expected one SUBJECT_GENERATION_AUTHORITY binding; found {len(rows)}",
        )
    manifest_path = _safe_repo_file(repo_root, rows[0]["path"])
    manifest = _load_json(manifest_path, code="E_BLUEPRINT_SUBJECT_MANIFEST_INVALID")
    expected = manifest.get("manifest_digest")
    actual = digest({k: v for k, v in manifest.items() if k != "manifest_digest"}).split(":", 1)[1]
    if expected != actual:
        fail(
            "E_BLUEPRINT_SUBJECT_MANIFEST_DIGEST",
            f"expected {expected}; recomputed {actual}",
        )
    if manifest.get("subject") != "PHYSICS":
        fail("E_BLUEPRINT_SUBJECT_MANIFEST_MISMATCH", str(manifest.get("subject")))
    return manifest


def _validate_route_registry(registry: dict[str, Any]) -> None:
    schema = _load_json(ROUTE_REGISTRY_SCHEMA, code="E_BLUEPRINT_ROUTE_SCHEMA_INVALID")
    try:
        jsonschema.validate(registry, schema)
    except jsonschema.ValidationError as exc:
        raise BlueprintAgentTaskIntakeError(
            "E_BLUEPRINT_ROUTE_REGISTRY_SCHEMA",
            exc.message,
        ) from exc

    actual = digest({k: v for k, v in registry.items() if k != "registry_digest"})
    if registry["registry_digest"] != actual:
        fail(
            "E_BLUEPRINT_ROUTE_REGISTRY_DIGEST",
            f"expected {registry['registry_digest']}; recomputed {actual}",
        )

    route_ids = [row["route_id"] for row in registry["routes"]]
    if len(route_ids) != len(set(route_ids)):
        fail("E_BLUEPRINT_ROUTE_ID_DUPLICATE", "route IDs must be unique")

    for route in registry["routes"]:
        roles = [row["role"] for row in route["inputs"]]
        paths = [row["path"] for row in route["inputs"]]
        if len(roles) != len(set(roles)):
            fail("E_BLUEPRINT_ROUTE_ROLE_DUPLICATE", route["route_id"])
        if len(paths) != len(set(paths)):
            fail("E_BLUEPRINT_ROUTE_PATH_DUPLICATE", route["route_id"])
        by_role = {row["role"]: row for row in route["inputs"]}
        for required_role in ("QUESTION_SET", "DECLARED_TOPIC_SCOPE"):
            if required_role not in by_role or by_role[required_role]["required"] is not True:
                fail(
                    "E_BLUEPRINT_ROUTE_REQUIRED_INPUT_MISSING",
                    f"{route['route_id']} requires {required_role}",
                )
        attempt = by_role.get("ATTEMPT_SET")
        if attempt is not None and attempt["required"] is not False:
            fail(
                "E_BLUEPRINT_ROUTE_ATTEMPT_MUST_BE_OPTIONAL",
                route["route_id"],
            )


def _route_registry_binding(
    manifest: dict[str, Any],
    repo_root: Path,
) -> tuple[dict[str, Any], dict[str, str]] | None:
    relative = manifest.get("authorities", {}).get("agent_task_execution_routes")
    if not relative:
        return None
    path = _safe_repo_file(repo_root, relative)
    registry = _load_json(path, code="E_BLUEPRINT_ROUTE_REGISTRY_INVALID")
    _validate_route_registry(registry)
    if registry["subject"] != "PHYSICS":
        fail("E_BLUEPRINT_ROUTE_REGISTRY_SUBJECT", str(registry["subject"]))
    return registry, {
        "registry_id": registry["registry_id"],
        "path": relative,
        "sha256": _file_digest(path),
    }


def _resolve_execution_route(
    task: dict[str, Any],
    manifest: dict[str, Any],
    repo_root: Path,
    packet_working_tree_state: str,
) -> dict[str, Any]:
    route_id = task.get("execution_route_id")
    registry_binding = _route_registry_binding(manifest, repo_root)

    if route_id is None:
        return {
            "status": "HELD_NO_ROUTE_REQUESTED",
            "execution_authorized": False,
            "authorization_scope": "P-A_INPUT_SELECTION_ONLY",
            "route_id": None,
            "route_registry": registry_binding[1] if registry_binding else None,
            "input_bindings": [],
            "label_inference": "PROHIBITED",
            "reason": (
                "No opaque execution_route_id was requested. Blueprint will not infer a route from grade, curriculum, topic, subtopic, learner state, or Engineering depth."
            ),
        }

    if registry_binding is None:
        return {
            "status": "HELD_ROUTE_UNRESOLVED",
            "execution_authorized": False,
            "authorization_scope": "P-A_INPUT_SELECTION_ONLY",
            "route_id": route_id,
            "route_registry": None,
            "input_bindings": [],
            "label_inference": "PROHIBITED",
            "reason": "The current Physics generation manifest declares no AgentTasks execution-route registry.",
        }

    registry, binding = registry_binding
    matches = [row for row in registry["routes"] if row["route_id"] == route_id]
    if len(matches) != 1:
        return {
            "status": "HELD_ROUTE_UNRESOLVED",
            "execution_authorized": False,
            "authorization_scope": "P-A_INPUT_SELECTION_ONLY",
            "route_id": route_id,
            "route_registry": binding,
            "input_bindings": [],
            "label_inference": "PROHIBITED",
            "reason": f"Exact route ID {route_id} is not ACTIVE in the repository-owned route registry.",
        }

    if packet_working_tree_state != "CLEAN" or _git_working_tree_state(repo_root) != "CLEAN":
        fail(
            "E_BLUEPRINT_ROUTE_DIRTY_CHECKOUT",
            "resolved P-A input custody requires a clean checkout at the packet HEAD",
        )

    route = matches[0]
    input_bindings: list[dict[str, Any]] = []
    for row in route["inputs"]:
        if not row["path"].startswith("Grade 9/V2/Physics/"):
            fail(
                "E_BLUEPRINT_ROUTE_INPUT_OUTSIDE_SUBJECT",
                row["path"],
            )
        path = _safe_repo_file(repo_root, row["path"])
        input_bindings.append(
            {
                "role": row["role"],
                "required": row["required"],
                "path": row["path"],
                "sha256": _file_digest(path),
            }
        )

    return {
        "status": "RESOLVED_REPOSITORY_ROUTE",
        "execution_authorized": True,
        "authorization_scope": "P-A_INPUT_SELECTION_ONLY",
        "route_id": route_id,
        "route_registry": binding,
        "input_bindings": sorted(input_bindings, key=lambda row: row["role"]),
        "label_inference": "PROHIBITED",
        "reason": (
            "Exact opaque route ID resolved through current Physics generation authority. Authorization is limited to selecting the bound P-A inputs; all downstream authority remains repository-governed."
        ),
    }


def _validate_receipt(receipt: dict[str, Any]) -> None:
    schema = _load_json(RECEIPT_SCHEMA, code="E_BLUEPRINT_TASK_INTAKE_SCHEMA_INVALID")
    try:
        jsonschema.validate(receipt, schema)
    except jsonschema.ValidationError as exc:
        raise BlueprintAgentTaskIntakeError(
            "E_BLUEPRINT_TASK_INTAKE_SCHEMA",
            exc.message,
        ) from exc

    route = receipt["execution_route"]
    resolved = route["status"] == "RESOLVED_REPOSITORY_ROUTE"
    if route["execution_authorized"] is not resolved:
        fail(
            "E_BLUEPRINT_ROUTE_AUTHORIZATION_STATE",
            "execution_authorized must be true exactly for RESOLVED_REPOSITORY_ROUTE",
        )
    if resolved:
        roles = {row["role"]: row for row in route["input_bindings"]}
        for required_role in ("QUESTION_SET", "DECLARED_TOPIC_SCOPE"):
            if required_role not in roles or roles[required_role]["required"] is not True:
                fail("E_BLUEPRINT_ROUTE_RECEIPT_INCOMPLETE", required_role)
        if route["route_registry"] is None or route["route_id"] is None:
            fail("E_BLUEPRINT_ROUTE_RECEIPT_INCOMPLETE", "registry/route identity")
    elif route["input_bindings"]:
        fail(
            "E_BLUEPRINT_HELD_ROUTE_HAS_INPUTS",
            "held routes may not bind P-A inputs",
        )


def consume_execution_packet(
    packet: dict[str, Any],
    *,
    current_head: str | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Accept delegation context and resolve only repository-owned P-A input routes."""
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
    manifest = _subject_generation_manifest(packet, repo_root)

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

    execution_route = _resolve_execution_route(
        task,
        manifest,
        repo_root,
        packet["repository_state"]["working_tree_state"],
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
        "execution_route": execution_route,
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
        description="Validate a Shared AgentTasks packet and resolve only repository-owned Physics P-A input routes"
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
