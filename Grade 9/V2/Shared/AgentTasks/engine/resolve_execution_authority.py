#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
AGENT_TASKS_ROOT = HERE.parent.parent
AUTHORITY_ROUTING = AGENT_TASKS_ROOT / "registry" / "authority-routing.v1.json"


class AuthorityResolutionError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _repo_root(start: Path | None = None) -> Path:
    start = (start or HERE).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    # Repository archive/tests may not carry .git; preserve the known relative V2 layout.
    return HERE.parents[5]


def _git(repo_root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout.strip()


def git_head(repo_root: Path) -> str:
    try:
        value = _git(repo_root, "rev-parse", "HEAD")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise AuthorityResolutionError("E_AGENT_HEAD_UNRESOLVED", "cannot resolve repository HEAD") from exc
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise AuthorityResolutionError("E_AGENT_HEAD_INVALID", value)
    return value


def git_working_tree_state(repo_root: Path) -> str:
    try:
        return "CLEAN" if _git(repo_root, "status", "--porcelain") == "" else "DIRTY"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNKNOWN"


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _bind_file(repo_root: Path, authority_class: str, relative_path: str) -> dict[str, str]:
    path = repo_root / relative_path
    if not path.is_file():
        raise AuthorityResolutionError(
            "E_AGENT_AUTHORITY_MISSING",
            f"{authority_class} does not resolve to a file: {relative_path}",
        )
    return {
        "authority_class": authority_class,
        "path": relative_path,
        "sha256": file_digest(path),
    }


def _subject_adapter(roadmap: dict[str, Any], subject: str) -> dict[str, Any]:
    matches = [
        row for row in roadmap.get("subject_adapters", [])
        if str(row.get("subject", "")).casefold() == subject.casefold()
    ]
    if len(matches) != 1:
        raise AuthorityResolutionError(
            "E_AGENT_SUBJECT_ADAPTER_UNRESOLVED",
            f"expected exactly one current subject adapter routing row for {subject}; found {len(matches)}",
        )
    return matches[0]


def _declared_grades(manifest: dict[str, Any]) -> list[int]:
    """Read only explicit manifest grade declarations; never infer grade from paths or labels."""
    values: list[Any]
    if "grades" in manifest:
        raw = manifest["grades"]
        values = raw if isinstance(raw, list) else []
    elif "grade" in manifest:
        values = [manifest["grade"]]
    else:
        values = []

    declared: list[int] = []
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            declared.append(value)
        elif isinstance(value, str) and re.fullmatch(r"[0-9]+", value):
            declared.append(int(value))
    return sorted(set(declared))


def _generation_authority_scope(task: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    task_grade = int(task["grade"])
    declared = _declared_grades(manifest)
    state = "UNDECLARED" if not declared else ("MATCH" if task_grade in declared else "MISMATCH")
    return {
        "task_grade": task_grade,
        "declared_grades": declared,
        "grade_state": state,
    }


def resolve_authority(
    task: dict[str, Any],
    *,
    repo_root: Path | None = None,
    head_sha: str | None = None,
    working_tree_state: str | None = None,
) -> dict[str, Any]:
    repo_root = (repo_root or _repo_root()).resolve()
    routing = _load_json(repo_root / AUTHORITY_ROUTING.relative_to(_repo_root())) if repo_root != _repo_root() else _load_json(AUTHORITY_ROUTING)

    head = head_sha or git_head(repo_root)
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise AuthorityResolutionError("E_AGENT_HEAD_INVALID", head)

    target_ref = task["target_ref"]
    if re.fullmatch(r"[0-9a-fA-F]{40}", target_ref) and target_ref.lower() != head:
        raise AuthorityResolutionError(
            "E_AGENT_STALE_TARGET",
            f"task binds {target_ref.lower()} but checkout is {head}",
        )

    bindings = [
        _bind_file(repo_root, row["authority_class"], row["path"])
        for row in routing["authority_classes"]
    ]
    by_class = {row["authority_class"]: row for row in bindings}
    roadmap_binding = by_class.get("SKP_SCHEMA_REGISTRY")
    if roadmap_binding is None:
        raise AuthorityResolutionError("E_AGENT_ROUTING_INVALID", "SKP_SCHEMA_REGISTRY routing is required")
    roadmap = _load_json(repo_root / roadmap_binding["path"])

    adapter = _subject_adapter(roadmap, task["subject"])
    subject_manifest_binding = _bind_file(
        repo_root,
        "SUBJECT_GENERATION_AUTHORITY",
        adapter["current_authority_manifest_ref"],
    )
    bindings.append(subject_manifest_binding)
    subject_manifest = _load_json(repo_root / subject_manifest_binding["path"])
    generation_scope = _generation_authority_scope(task, subject_manifest)

    counts = Counter(str(row.get("status", "UNKNOWN")) for row in roadmap.get("modules", []))
    learning_state = {
        "roadmap_id": roadmap["roadmap_id"],
        "authority_state": roadmap["authority_state"],
        "bulk_population_allowed": bool(roadmap["bulk_population_allowed"]),
        "module_status_counts": dict(sorted(counts.items())),
        "subject_adapter": {
            "subject": adapter["subject"],
            "status": adapter["status"],
            "runtime_authority": bool(adapter["runtime_authority"]),
            "current_authority_manifest_ref": adapter["current_authority_manifest_ref"],
            "generation_authority_scope": generation_scope,
        },
    }

    reason = "Shared AgentTasks has not invoked the governed Engineering Gate evaluator."
    consumers = {
        consumer: {"status": "NOT_EVALUATED", "reason": reason}
        for consumer in task.get("target_consumers", [])
    }
    blockers: list[str] = []
    if not adapter.get("runtime_authority", False):
        blockers.append(
            f"LearningEngineering subject adapter {adapter['subject']} is {adapter['status']} with runtime_authority=false; "
            "use the bound current subject authority and do not fabricate SKP-to-Engineering promotion."
        )
    if not roadmap.get("bulk_population_allowed", False):
        blockers.append(f"SKP bulk population is blocked by roadmap {roadmap['roadmap_id']}.")
    if generation_scope["grade_state"] == "MISMATCH":
        blockers.append(
            f"Bound {adapter['subject']} generation authority explicitly declares grade(s) "
            f"{generation_scope['declared_grades']} but task grade is {generation_scope['task_grade']}; "
            "discovery/reconciliation may proceed, but this manifest cannot authorize subject production or Engineering consumption for the task grade."
        )
    elif generation_scope["grade_state"] == "UNDECLARED":
        blockers.append(
            f"Bound {adapter['subject']} generation authority declares no machine-readable grade scope; "
            "discovery/reconciliation may proceed, but subject production or Engineering consumption must remain held until grade authority is explicit."
        )

    preflight = {
        "engineering_state": "NOT_EVALUATED",
        "research_state": "NOT_EVALUATED",
        "consumer_permissions": consumers,
        "publication_authorization": "NOT_IMPLIED",
        "blockers": blockers,
        "next_action": (
            "Read the exact bound authorities and perform only the delegated task. Discovery/reconciliation may preserve explicit holds. "
            "Use a current subject Engineering path only when its declared scope covers the task; only a governed downstream evaluator may produce Engineering readiness or consumer authorization."
        ),
    }

    return {
        "repository_state": {
            "repository": task["repository"],
            "resolved_head": head,
            "target_ref": target_ref,
            "working_tree_state": working_tree_state or (git_working_tree_state(repo_root) if head_sha is None else "UNKNOWN"),
        },
        "authority_bindings": sorted(bindings, key=lambda row: row["authority_class"]),
        "learning_engineering_state": learning_state,
        "engineering_preflight": preflight,
    }


def render_preflight(resolved: dict[str, Any], task: dict[str, Any]) -> str:
    le = resolved["learning_engineering_state"]
    preflight = resolved["engineering_preflight"]
    grade_scope = le["subject_adapter"].get("generation_authority_scope")
    lines = [
        "# Engineering Preflight",
        "",
        f"- **Task:** {task['subject']} / {task['topic']} / {task['subtopic']}",
        f"- **Engineering depth:** {task['engineering_depth']}",
        f"- **Repository HEAD:** `{resolved['repository_state']['resolved_head']}`",
        f"- **LearningEngineering:** `{le['authority_state']}`",
        f"- **SKP bulk population allowed:** `{str(le['bulk_population_allowed']).lower()}`",
        f"- **Subject adapter:** `{le['subject_adapter']['status']}` / runtime authority `{str(le['subject_adapter']['runtime_authority']).lower()}`",
    ]
    if grade_scope is not None:
        lines.append(
            f"- **Generation-authority grade scope:** task `{grade_scope['task_grade']}` / "
            f"declared `{grade_scope['declared_grades']}` / `{grade_scope['grade_state']}`"
        )
    lines.extend([
        f"- **Engineering state:** `{preflight['engineering_state']}`",
        f"- **Research state:** `{preflight['research_state']}`",
        f"- **Publication:** `{preflight['publication_authorization']}`",
        "",
        "## Bound authority",
        "",
    ])
    for row in resolved["authority_bindings"]:
        lines.append(f"- **{row['authority_class']}:** `{row['path']}` — `{row['sha256']}`")
    lines.extend(["", "## Consumer permissions", ""])
    if preflight["consumer_permissions"]:
        for consumer, row in preflight["consumer_permissions"].items():
            lines.append(f"- **{consumer}:** `{row['status']}` — {row['reason']}")
    else:
        lines.append("- None requested.")
    lines.extend(["", "## Holds / limitations", ""])
    if preflight["blockers"]:
        lines.extend(f"- {value}" for value in preflight["blockers"])
    else:
        lines.append("- None discovered by the delegation layer.")
    lines.extend(["", "## Next action", "", preflight["next_action"], ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve exact repository authority for an execution task")
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preflight-output", type=Path)
    args = parser.parse_args()

    task = _load_json(args.task)
    resolved = resolve_authority(task)
    text = json.dumps(resolved, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.preflight_output:
        args.preflight_output.write_text(render_preflight(resolved, task), encoding="utf-8")


if __name__ == "__main__":
    main()
