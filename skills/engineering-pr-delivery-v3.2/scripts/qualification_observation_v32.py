#!/usr/bin/env python3
"""Pure R-PROOF observer: exact source, named execution, immutable delivered blobs.

Inputs from a *separate read-only authenticated provider adapter* are necessary.
This function cannot authenticate a caller's fake adapter, and its outputs are
DERIVED_OBSERVATION_ONLY, never engineering acceptance or merge authority.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

INPUT_SCHEMA = "relay-v3.2-qualification-contract-v1"
RESULT_SCHEMA = "relay-v3.2-qualification-observation-v1"
AUTHORITY = "DERIVED_OBSERVATION_ONLY"
SHA = re.compile(r"[0-9a-f]{40}", re.I)
REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
CASE = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*){2,}")


def _contract(value: Any) -> dict:
    if not isinstance(value, dict) or set(value) != {
        "schema", "repository", "responsibility", "pull_number",
        "candidate_sha", "requirements",
    } or value.get("schema") != INPUT_SCHEMA:
        raise ValueError("unknown or missing contract fields; no agent-authored status/progress")
    if not isinstance(value["repository"], str) or not REPO.fullmatch(value["repository"]):
        raise ValueError("concrete repository required")
    if not isinstance(value["responsibility"], str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+#\d+", value["responsibility"]
    ):
        raise ValueError("exact responsibility reference required")
    if type(value["pull_number"]) is not int or value["pull_number"] < 1:
        raise ValueError("positive pull number required")
    if not isinstance(value["candidate_sha"], str) or not SHA.fullmatch(value["candidate_sha"]):
        raise ValueError("exact 40-character candidate SHA required")
    reqs = value["requirements"]
    if not isinstance(reqs, list) or not reqs:
        raise ValueError("nonempty obligation inventory required")
    ids = set()
    for row in reqs:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            raise ValueError("stable requirement id required")
        if row["id"] in ids:
            raise ValueError("duplicate requirement")
        ids.add(row["id"])
        if row.get("kind") == "UNITTEST":
            if set(row) != {"id", "kind", "case_id", "job_name", "step_name"}:
                raise ValueError("UNITTEST requires exact job, step, and dotted case")
            if not isinstance(row["case_id"], str) or not CASE.fullmatch(row["case_id"]):
                raise ValueError("dotted unittest ID required")
            if not row["case_id"].split(".")[-1].startswith("test_"):
                raise ValueError("case must be a test method")
            if not all(isinstance(row[k], str) and row[k].strip() for k in ("job_name", "step_name")):
                raise ValueError("job/step required")
        elif row.get("kind") == "BLOB":
            if set(row) != {"id", "kind", "path", "expected_blob_sha"}:
                raise ValueError("BLOB requires relative path and exact expected blob")
            path = row["path"]
            if not isinstance(path, str) or not path or path.startswith("/") or ".." in path.split("/") or "\\" in path:
                raise ValueError("safe relative path required")
            if not isinstance(row["expected_blob_sha"], str) or not SHA.fullmatch(row["expected_blob_sha"]):
                raise ValueError("expected blob SHA required")
        else:
            raise ValueError("unsupported obligation kind")
    return value


def _row(req: Mapping, status: str, reason: str, refs: list[str] | None = None) -> dict:
    return {"id": req["id"], "status": status, "reason": reason, "evidence_refs": refs or []}


def _named_successful_case(raw: str, case_id: str) -> bool:
    method = case_id.rsplit(".", 1)[-1]
    matcher = re.compile(rf"{re.escape(method)} \({re.escape(case_id)}\) \.\.\. ok")
    for line in raw.splitlines():
        line = re.sub(r"^\d{4}-\d\d-\d\dT[^ ]+Z\s+", "", line.strip())
        if matcher.fullmatch(line):
            return True
    return False


def _observed_execution(req: Mapping, provider: Any, repo: str, sha: str) -> dict:
    try:
        runs = provider.list_runs(repo, sha)
        if not isinstance(runs, list):
            return _row(req, "UNKNOWN", "PROVIDER_RUNS_UNAVAILABLE")
        if not runs:
            return _row(req, "UNKNOWN", "NO_RUNS_OBSERVED")
        uncertain = False
        for run in runs:
            if not isinstance(run, Mapping) or run.get("head_sha") != sha:
                continue
            if run.get("status") != "completed":
                uncertain = True
                continue
            run_id = run.get("id")
            if type(run_id) is not int or run_id < 1:
                uncertain = True
                continue
            jobs = provider.list_jobs(repo, run_id)
            if not isinstance(jobs, list):
                uncertain = True
                continue
            for job in jobs:
                if not isinstance(job, Mapping) or job.get("name") != req["job_name"]:
                    continue
                if job.get("status") != "completed":
                    uncertain = True
                    continue
                if job.get("conclusion") != "success" or run.get("conclusion") != "success":
                    return _row(req, "UNPROVEN", "NAMED_RUN_OR_JOB_FAILED")
                if not any(
                    isinstance(step, Mapping) and step.get("name") == req["step_name"]
                    and step.get("status") == "completed" and step.get("conclusion") == "success"
                    for step in job.get("steps") or []
                ):
                    return _row(req, "UNPROVEN", "REQUIRED_STEP_NOT_SUCCESSFUL")
                job_id = job.get("id")
                if type(job_id) is not int or job_id < 1:
                    uncertain = True
                    continue
                raw = provider.get_job_log(repo, job_id)
                if not isinstance(raw, str):
                    uncertain = True
                    continue
                if not _named_successful_case(raw, req["case_id"]):
                    return _row(req, "UNPROVEN", "NAMED_CASE_ABSENT_FROM_JOB_LOG")
                url = f"https://github.com/{repo}/actions/runs/{run_id}/job/{job_id}"
                return _row(req, "PROVEN", "CASE_OBSERVED_AT_EXACT_HEAD", [url])
        return _row(req, "UNKNOWN" if uncertain else "UNPROVEN",
                    "RUN_OR_LOG_INCOMPLETE" if uncertain else "REQUIRED_EXECUTION_NOT_OBSERVED")
    except (OSError, RuntimeError, ValueError):
        return _row(req, "UNKNOWN", "PROVIDER_RUN_READ_FAILED")


def _observed_blob(req: Mapping, tree: Any, repo: str, sha: str) -> dict:
    if not isinstance(tree, Mapping) or tree.get("truncated") is not False or not isinstance(tree.get("tree"), list):
        return _row(req, "UNKNOWN", "TREE_UNAVAILABLE_OR_TRUNCATED")
    for entry in tree["tree"]:
        if isinstance(entry, Mapping) and entry.get("path") == req["path"] and entry.get("type") == "blob":
            if str(entry.get("sha") or "").lower() != req["expected_blob_sha"].lower():
                return _row(req, "UNPROVEN", "SAME_PATH_WRONG_BLOB")
            return _row(req, "PROVEN", "EXPECTED_BLOB_AT_EXACT_HEAD",
                        [f"https://github.com/{repo}/blob/{sha}/{req['path']}"])
    return _row(req, "UNPROVEN", "EXPECTED_FILE_MISSING")


def assess(contract: dict, provider: object) -> dict:
    plan = _contract(contract)
    repo, sha = plan["repository"], plan["candidate_sha"].lower()
    result = {
        "schema": RESULT_SCHEMA, "authority": AUTHORITY, "repository": repo,
        "responsibility": plan["responsibility"], "expected_candidate_sha": sha,
        "observed_candidate_sha": None, "overall": "UNKNOWN", "requirements": [],
    }
    try:
        pull = provider.get_pull(repo, plan["pull_number"])
    except (OSError, RuntimeError, ValueError):
        pull = None
    if not isinstance(pull, Mapping) or not isinstance(pull.get("head"), Mapping):
        result["requirements"] = [_row(q, "UNKNOWN", "LIVE_PULL_UNAVAILABLE") for q in plan["requirements"]]
        return result
    actual = pull["head"].get("sha")
    if not isinstance(actual, str) or not SHA.fullmatch(actual):
        result["requirements"] = [_row(q, "UNKNOWN", "LIVE_HEAD_UNAVAILABLE") for q in plan["requirements"]]
        return result
    result["observed_candidate_sha"] = actual.lower()
    if actual.lower() != sha:
        result["requirements"] = [_row(q, "UNPROVEN", "LIVE_CANDIDATE_MOVED") for q in plan["requirements"]]
        result["overall"] = "UNPROVEN"
        return result

    tree = None
    for q in plan["requirements"]:
        if q["kind"] == "UNITTEST":
            row = _observed_execution(q, provider, repo, sha)
        else:
            if tree is None:
                try:
                    tree = provider.get_tree(repo, sha)
                except (OSError, RuntimeError, ValueError):
                    tree = {}
            row = _observed_blob(q, tree, repo, sha)
        result["requirements"].append(row)
    statuses = {x["status"] for x in result["requirements"]}
    result["overall"] = "UNPROVEN" if "UNPROVEN" in statuses else (
        "UNKNOWN" if "UNKNOWN" in statuses else "PROVEN"
    )
    return result
