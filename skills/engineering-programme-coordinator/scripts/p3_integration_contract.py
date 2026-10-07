#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from coordlib import validate as schema_validate
from project_outcome_falsification import validate_project_protocol


AUTHORITY_BOUNDARIES = {
    "emits_engineering_pass": False,
    "emits_project_acceptance_pass": False,
    "emits_independent_review_verdict": False,
    "performs_lifecycle_advance": False,
    "grants_merge_authority": False,
    "grants_production_cutover": False,
}

CHECK_IDS = tuple(f"P3I-{index:02d}" for index in range(1, 21))
ACTION_UNIVERSE = {
    "WRITE_CANDIDATE",
    "RUN_VERIFICATION",
    "REPAIR_CANDIDATE",
    "PUBLISH_EVIDENCE",
    "REQUEST_STAGE_ADVANCE",
    "ESCALATE",
}


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


def object_digest(value: dict[str, Any], field: str) -> str:
    payload = copy.deepcopy(value)
    payload.pop(field, None)
    return canonical_digest(payload)


def _git(repo_root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise ValueError(proc.stderr.strip() or proc.stdout.strip() or "git failed")
    return proc.stdout.strip()


def _assert_exact_commit(repo_root: Path, sha: str, label: str) -> None:
    resolved = _git(repo_root, "rev-parse", f"{sha}^{{commit}}")
    if resolved != sha:
        raise ValueError(f"{label} resolved to {resolved}, expected {sha}")


def _safe_path(repo_root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe repository path: {relative}")
    result = (repo_root / path).resolve()
    try:
        result.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository root: {relative}") from exc
    return result


def _source_semantic_errors(source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    ids = [row["id"] for row in source["expected_checks"]]
    if tuple(ids) != CHECK_IDS:
        errors.append("expected_checks must equal P3I-01..P3I-20 in order")

    components = [row["component"] for row in source["runtime_basis"]]
    paths = [row["path"] for row in source["runtime_basis"]]
    if len(components) != len(set(components)):
        errors.append("runtime_basis component ids must be unique")
    if len(paths) != len(set(paths)):
        errors.append("runtime_basis paths must be unique")

    obligation_ids = [row["id"] for row in source["contract_obligations"]]
    if len(obligation_ids) != len(set(obligation_ids)):
        errors.append("contract_obligations ids must be unique")

    selector_ids = [row["id"] for row in source["baseline_selectors"]]
    if len(selector_ids) != len(set(selector_ids)):
        errors.append("baseline_selectors ids must be unique")

    rule_ids = [row["id"] for row in source["impact_rules"]]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("impact_rules ids must be unique")

    if source["authority_boundaries"] != AUTHORITY_BOUNDARIES:
        errors.append("qualification source authority boundaries do not match fixed contract")
    return errors


def validate_source(
    source: Any,
    label: str = "p3-integration-qualification-source",
) -> list[str]:
    errors = schema_validate("p3-integration-qualification-source", source, label)
    if errors:
        return errors
    return [f"{label}: {row}" for row in _source_semantic_errors(source)]


def _validate_runtime_basis(
    source: dict[str, Any],
    candidate_sha: str,
    repo_root: Path,
) -> None:
    base_sha = source["base"]["sha"]
    _assert_exact_commit(repo_root, base_sha, "P3-I base")
    _assert_exact_commit(repo_root, candidate_sha, "P3-I candidate")

    for item in source["runtime_basis"]:
        path = item["path"]
        expected = item["blob_sha"]
        base_blob = _git(repo_root, "rev-parse", f"{base_sha}:{path}")
        candidate_blob = _git(repo_root, "rev-parse", f"{candidate_sha}:{path}")
        if base_blob != expected:
            raise ValueError(
                f"{item['component']}: base blob {base_blob} != frozen {expected}"
            )
        if candidate_blob != expected:
            raise ValueError(
                f"{item['component']}: candidate changed reused runtime "
                f"({candidate_blob} != {expected})"
            )


def _load_project_protocol(
    source: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    spec = source["local_project_protocol"]
    path = _safe_path(repo_root, spec["path"])
    bundle = json.loads(path.read_text(encoding="utf-8"))
    protocols = bundle["support"]["project_protocols"]
    protocol = copy.deepcopy(protocols[spec["index"]])
    errors = validate_project_protocol(protocol)
    if errors:
        raise ValueError("; ".join(errors))
    available = {row["id"] for row in protocol["verification_methods"]}
    missing = sorted(set(spec["method_ids"]) - available)
    if missing:
        raise ValueError(
            "P3-I project method ids absent from Local protocol: " + ", ".join(missing)
        )
    return protocol
