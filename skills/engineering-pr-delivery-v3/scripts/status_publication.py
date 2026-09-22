#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any

from intelligence_projection import build_task
from v3lib import canonical_digest, load_yaml, repo_path, validate_schema


DEFAULT_POLICY = Path(__file__).resolve().parents[1] / "config" / "status-publication.default.yaml"
REPO_POLICY = "relay/CONFIG/status-publication.yaml"
ACTION_TRIGGER = {
    "CHECKPOINT": "before_checkpoint",
    "HANDOVER": "before_handover",
    "PR_READY": "before_pr_ready",
    "CLOSE_TASK": "before_task_exit",
}


class StatusPublicationError(RuntimeError):
    pass


def _git(root: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode:
        raise StatusPublicationError(proc.stderr.strip() or "git command failed")
    return proc.stdout.strip()


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_policy(root: Path, policy_path: str | None = None) -> tuple[dict[str, Any], str]:
    path = Path(policy_path).resolve() if policy_path else root / REPO_POLICY
    if not path.exists():
        path = DEFAULT_POLICY
    policy = load_yaml(path)
    errors = validate_schema("status-publication-policy", policy, "STATUS_PUBLICATION_POLICY")
    if errors:
        raise StatusPublicationError("; ".join(errors))
    return policy, str(path)


def _matches(path: str, patterns: list[str]) -> bool:
    norm = path.replace("\\", "/").lstrip("./")
    for raw in patterns:
        pattern = str(raw).replace("\\", "/").lstrip("./")
        if fnmatch.fnmatchcase(norm, pattern):
            return True
        if pattern.startswith("**/") and fnmatch.fnmatchcase(norm, pattern[3:]):
            return True
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            if norm == prefix or norm.startswith(prefix + "/"):
                return True
    return False


def _sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _file_metrics(root: Path, material_base: str, exclusions: list[str]) -> list[dict[str, Any]]:
    numstat: dict[str, int] = {}
    raw = _git(root, "diff", "--numstat", material_base, "--", check=False)
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        add, delete, path = parts[0], parts[1], parts[-1]
        if _matches(path, exclusions):
            continue
        changed = 0 if add == "-" or delete == "-" else int(add) + int(delete)
        numstat[path] = changed

    statuses: dict[str, str] = {}
    raw = _git(root, "diff", "--name-status", material_base, "--", check=False)
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0], parts[-1]
        if not _matches(path, exclusions):
            statuses[path] = status

    untracked = _git(root, "ls-files", "--others", "--exclude-standard", check=False)
    for path in [x for x in untracked.splitlines() if x.strip()]:
        if _matches(path, exclusions):
            continue
        statuses[path] = "A?"
        target = root / path
        if target.is_file():
            try:
                numstat[path] = len(target.read_text(encoding="utf-8").splitlines())
            except UnicodeDecodeError:
                numstat[path] = 0

    result = []
    for path in sorted(set(numstat) | set(statuses)):
        status = statuses.get(path, "M")
        target = root / path
        if status == "A?" and target.is_file():
            payload = target.read_bytes()
        else:
            payload = _git(root, "diff", "--binary", material_base, "--", path, check=False).encode("utf-8")
        result.append({
            "path": path,
            "status": status,
            "changed_lines": int(numstat.get(path, 0)),
            "fingerprint": _sha256_bytes(payload),
        })
    return result


def _normalize_task(task: dict[str, Any]) -> dict[str, Any]:
    parent = task.get("parent_issue") or {}
    current = parent.get("current") or {}
    return {
        "acceptance": sorted(
            f"{row.get('id')}:{row.get('state')}"
            for row in task.get("acceptance") or []
            if isinstance(row, dict)
        ),
        "benchmarks": sorted(
            f"{row.get('id')}:{row.get('current_result')}"
            for row in task.get("benchmarks") or []
            if isinstance(row, dict)
        ),
        "pending": sorted(str(row.get("id")) for row in task.get("pending_items") or [] if isinstance(row, dict)),
        "known_issues": sorted(str(row.get("id")) for row in task.get("known_issues") or [] if isinstance(row, dict)),
        "offloads": sorted(
            f"{row.get('id')}:{row.get('status')}"
            for row in task.get("offloads") or []
            if isinstance(row, dict)
        ),
        "parent_contract_digest": current.get("body_digest") or ((parent.get("baseline") or {}).get("body_digest")),
        "parent_updates": sorted(str(row.get("ref")) for row in parent.get("updates") or [] if isinstance(row, dict)),
        "roadmap_revision": ((task.get("lineage") or {}).get("roadmap_admission") or {}).get("revision"),
    }


def _cursor_path(root: Path, ep_id: str) -> Path:
    return root / "relay" / "PUBLICATION" / f"{ep_id}.status.yaml"


def _load_cursor(root: Path, ep_id: str) -> dict[str, Any] | None:
    path = _cursor_path(root, ep_id)
    if not path.exists():
        return None
    cursor = load_yaml(path)
    errors = validate_schema("status-publication-cursor", cursor, "STATUS_PUBLICATION_CURSOR")
    if errors:
        raise StatusPublicationError("; ".join(errors))
    return cursor


def _load_signals(path: str | None) -> dict[str, bool]:
    if not path:
        return {
            "public_contract_changed": False,
            "roadmap_reconciliation_requested": False,
        }
    value = load_yaml(Path(path))
    errors = validate_schema("status-publication-signals", value, "STATUS_PUBLICATION_SIGNALS")
    if errors:
        raise StatusPublicationError("; ".join(errors))
    return {
        "public_contract_changed": bool(value.get("public_contract_changed")),
        "roadmap_reconciliation_requested": bool(value.get("roadmap_reconciliation_requested")),
    }


def _diff_list(before: list[str], after: list[str]) -> int:
    return len(set(before) ^ set(after))


def evaluate(
    root: Path,
    *,
    policy_path: str | None = None,
    parent_issue_observation: dict[str, Any] | None = None,
    signals_path: str | None = None,
    action: str | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    policy, resolved_policy = load_policy(root, policy_path)
    if not policy.get("enabled"):
        return {
            "schema_version": "relay-v3-status-publication-result",
            "publication_due": False,
            "ep": None,
            "score": 0.0,
            "reasons": ["POLICY_DISABLED"],
            "metrics": {},
            "policy": resolved_policy,
            "cursor": None,
        }

    task = build_task(root, parent_issue_observation=parent_issue_observation)
    ep_id = str((task.get("identity") or {}).get("ep") or "")
    if not ep_id.startswith("EP-"):
        return {
            "schema_version": "relay-v3-status-publication-result",
            "publication_due": False,
            "ep": None,
            "score": 0.0,
            "reasons": ["NO_TASK_CONTEXT"],
            "metrics": {},
            "policy": resolved_policy,
            "cursor": None,
        }

    material_base = str((task.get("material") or {}).get("base") or "")
    if not material_base:
        raise StatusPublicationError("task snapshot has no material base")
    exclusions = list((policy.get("exclusions") or {}).get("paths") or [])
    current_files = _file_metrics(root, material_base, exclusions)
    cursor = _load_cursor(root, ep_id)
    before_files = {row["path"]: row for row in (cursor or {}).get("file_metrics") or []}
    current_map = {row["path"]: row for row in current_files}

    changed_files = [
        path for path, row in current_map.items()
        if path not in before_files or before_files[path].get("fingerprint") != row.get("fingerprint")
    ]
    created_files = [
        path for path in changed_files
        if current_map[path].get("status", "").startswith("A")
        and not str((before_files.get(path) or {}).get("status", "")).startswith("A")
    ]
    changed_lines = sum(
        max(0, int(current_map[path].get("changed_lines") or 0) - int((before_files.get(path) or {}).get("changed_lines") or 0))
        for path in changed_files
    )

    head = _git(root, "rev-parse", "HEAD")
    commit_base = str((cursor or {}).get("head") or material_base)
    commits = 0
    if _git(root, "merge-base", "--is-ancestor", commit_base, head, check=False) == "":
        proc = subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", commit_base, head])
        if proc.returncode == 0:
            commits = int(_git(root, "rev-list", "--count", f"{commit_base}..{head}") or "0")
    normalized = _normalize_task(task)
    before = (cursor or {}).get("normalized") or {
        "acceptance": [],
        "benchmarks": [],
        "pending": [],
        "known_issues": [],
        "offloads": [],
        "parent_contract_digest": None,
        "parent_updates": [],
        "roadmap_revision": None,
    }
    signals = _load_signals(signals_path)

    acceptance_changes = _diff_list(before.get("acceptance") or [], normalized["acceptance"])
    benchmark_changes = _diff_list(before.get("benchmarks") or [], normalized["benchmarks"])
    pending_known_changes = (
        _diff_list(before.get("pending") or [], normalized["pending"])
        + _diff_list(before.get("known_issues") or [], normalized["known_issues"])
    )
    offload_changes = _diff_list(before.get("offloads") or [], normalized["offloads"])
    parent_changed = (
        before.get("parent_contract_digest") != normalized["parent_contract_digest"]
        or set(before.get("parent_updates") or []) != set(normalized["parent_updates"])
    )

    weights = policy["weights"]
    score = (
        (changed_lines / 100.0) * float(weights["material_lines_per_100"])
        + len(changed_files) * float(weights["material_file_touched"])
        + len(created_files) * float(weights["material_file_created"])
        + acceptance_changes * float(weights["acceptance_state_change"])
        + benchmark_changes * float(weights["benchmark_state_change"])
        + (1 if signals["public_contract_changed"] else 0) * float(weights["public_contract_change"])
        + pending_known_changes * float(weights["pending_known_issue_change"])
        + (1 if parent_changed else 0) * float(weights["parent_issue_change"])
        + (1 if signals["roadmap_reconciliation_requested"] else 0) * float(weights["roadmap_reconciliation_request"])
        + offload_changes * float(weights["offload_change"])
    )
    score = round(score, 3)

    reasons: list[str] = []
    hard = policy["hard_triggers"]
    if cursor is None:
        reasons.append("INITIAL_STATUS")
    if acceptance_changes and hard["acceptance_state_changed"]:
        reasons.append("ACCEPTANCE_STATE_CHANGED")
    if benchmark_changes and hard["benchmark_state_changed"]:
        reasons.append("BENCHMARK_STATE_CHANGED")
    if pending_known_changes and hard["pending_known_issue_changed"]:
        reasons.append("PENDING_OR_KNOWN_ISSUE_CHANGED")
    if parent_changed and cursor is not None and hard["parent_issue_changed"]:
        reasons.append("PARENT_ISSUE_CHANGED")
    if signals["roadmap_reconciliation_requested"] and hard["roadmap_reconciliation_requested"]:
        reasons.append("ROADMAP_RECONCILIATION_REQUESTED")
    if signals["public_contract_changed"] and hard["public_contract_changed"]:
        reasons.append("PUBLIC_CONTRACT_CHANGED")
    if offload_changes and hard["offload_changed"]:
        reasons.append("OFFLOAD_CHANGED")

    volume = policy["volume_triggers"]
    for key, value, code in (
        ("material_lines_changed", changed_lines, "MATERIAL_LINES_THRESHOLD"),
        ("material_files_touched", len(changed_files), "MATERIAL_FILES_THRESHOLD"),
        ("material_files_created", len(created_files), "MATERIAL_FILES_CREATED_THRESHOLD"),
        ("material_commits", commits, "MATERIAL_COMMITS_THRESHOLD"),
    ):
        threshold = volume.get(key)
        if threshold is not None and value >= int(threshold):
            reasons.append(code)

    if score >= float(policy["score_threshold"]):
        reasons.append("STATUS_DEBT_THRESHOLD")

    action_name = str(action or "").upper()
    trigger = ACTION_TRIGGER.get(action_name)
    if trigger and hard.get(trigger):
        prepared = (cursor or {}).get("prepared_actions") or {}
        if prepared.get(action_name) != head:
            reasons.append(trigger.upper())

    return {
        "schema_version": "relay-v3-status-publication-result",
        "publication_due": bool(reasons),
        "ep": ep_id,
        "score": score,
        "reasons": list(dict.fromkeys(reasons)) or ["NO_PUBLICATION_DUE"],
        "metrics": {
            "material_lines_changed": changed_lines,
            "material_files_touched": len(changed_files),
            "material_files_created": len(created_files),
            "material_commits": commits,
            "acceptance_state_changes": acceptance_changes,
            "benchmark_state_changes": benchmark_changes,
            "pending_known_issue_changes": pending_known_changes,
            "parent_issue_changed": parent_changed,
            "offload_changes": offload_changes,
            "public_contract_changed": signals["public_contract_changed"],
            "roadmap_reconciliation_requested": signals["roadmap_reconciliation_requested"],
        },
        "policy": resolved_policy,
        "policy_digest": canonical_digest(policy),
        "cursor": str(_cursor_path(root, ep_id).relative_to(root)),
        "_cursor_payload": {
            "schema_version": "relay-v3-status-publication-cursor",
            "ep": ep_id,
            "published_at": _now(),
            "material_base": material_base,
            "head": head,
            "file_metrics": current_files,
            "normalized": normalized,
            "prepared_actions": {
                **((cursor or {}).get("prepared_actions") or {}),
                **({action_name: head} if trigger else {}),
            },
            "policy_digest": canonical_digest(policy),
            "note": None,
        },
    }


def apply(
    root: Path,
    *,
    policy_path: str | None = None,
    parent_issue_observation: dict[str, Any] | None = None,
    signals_path: str | None = None,
    action: str | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    result = evaluate(
        root,
        policy_path=policy_path,
        parent_issue_observation=parent_issue_observation,
        signals_path=signals_path,
        action=action,
    )
    payload = result.pop("_cursor_payload", None)
    if payload is None:
        return result
    payload["note"] = note
    errors = validate_schema("status-publication-cursor", payload, "STATUS_PUBLICATION_CURSOR")
    if errors:
        raise StatusPublicationError("; ".join(errors))
    path = _cursor_path(root.resolve(), payload["ep"])
    path.parent.mkdir(parents=True, exist_ok=True)
    import yaml
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    result["recorded"] = str(path.relative_to(root.resolve()))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate or record Engineering Relay V3 child-local status publication debt.")
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--policy")
    parser.add_argument("--parent-issue-observation")
    parser.add_argument("--signals")
    parser.add_argument("--action", choices=sorted(ACTION_TRIGGER))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--note")
    args = parser.parse_args()

    parent = load_yaml(Path(args.parent_issue_observation)) if args.parent_issue_observation else None
    fn = apply if args.apply else evaluate
    result = fn(
        Path(args.repo_root),
        policy_path=args.policy,
        parent_issue_observation=parent,
        signals_path=args.signals,
        action=args.action,
        **({"note": args.note} if args.apply else {}),
    )
    result.pop("_cursor_payload", None)
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if result.get("publication_due") and not args.apply else 0)


if __name__ == "__main__":
    main()
