#!/usr/bin/env python3
"""C4 S5-D1: hosted read-only provider/DELP audit, never a GitHub writer.

This wrapper calls the exact default-branch source readback in GET-only mode,
checks its three-surface parity independently, and saves a failure artifact
even when provider reads fail. Do not use a passing audit as Owner acceptance.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "skills/engineering-pr-delivery-v3.2/scripts/vertical_cycle_v32.py"
SCHEMA = "relay-v32-760-provider-audit-v1"
VALID_SHA = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
SURFACES = frozenset({"Common#718", "Common#733", "Common#740"})


class AuditError(ValueError):
    pass


def require(value: bool, reason: str) -> None:
    if not value:
        raise AuditError(reason)


def summary(view: Mapping[str, Any], *, checkout_sha: str, event_name: str,
            enabled_flag: str, writer_job_result: str) -> dict[str, Any]:
    """Source-independent parity check; no accepted facts or provider writes."""
    require(view.get("authority") == "READ_ONLY_SELF_REPLAY_NO_ACCEPTANCE",
            "UNTRUSTED_SOURCE_VIEW")
    require(view.get("full_ESC_6_gate") == "FAIL_CLOSED_UNRELEASED_CONSUMERS",
            "FULL_GATE_MUST_REMAIN_RED")
    require(view.get("authority_effects") == [], "UNEXPECTED_SEMANTIC_AUTHORITY")
    require(view.get("pr_binding") == "BOUND", "UNBOUND_SOURCE_PRODUCT")
    require(isinstance(view.get("candidate_sha"), str)
            and bool(VALID_SHA.fullmatch(view["candidate_sha"])),
            "CANDIDATE_IDENTITY_NOT_EXACT_HEAD")
    require(bool(VALID_SHA.fullmatch(checkout_sha)), "UNTRUSTED_CHECKOUT_SHA")
    require(all(isinstance(view.get(k), str) and bool(DIGEST.fullmatch(view[k]))
                for k in ("source_input_digest", "delp_input_digest")),
            "SOURCE_DELP_DIGEST_MISSING")
    states = view.get("read_views")
    require(isinstance(states, Mapping) and set(states) == SURFACES,
            "THREE_SURFACE_READBACK_MISSING")
    require(all(isinstance(s, Mapping)
                and s.get("title") in ("MATCH", "DRIFT")
                and s.get("managed_block") in ("MATCH", "DRIFT", "MISSING", "CORRUPT_MARKERS")
                for s in states.values()), "INVALID_READBACK_PARITY")
    expected = ("MATCH" if all(
        s["title"] == "MATCH" and s["managed_block"] == "MATCH"
        for s in states.values()) else "DRIFT_OR_UNPUBLISHED")
    require(view.get("reconciliation") == expected,
            "READBACK_FALSE_SUCCESS_OR_INCONSISTENT_DRIFT")
    progress = view.get("semantic_progress")
    require(isinstance(progress, Mapping) and
            all(type(progress.get(k)) is int and 0 <= progress[k] <= 100
                for k in ("P", "E", "D", "DE")),
            "NOT_DELP_DERIVED_PROGRESS")
    require(event_name in ("issue_comment", "pull_request_target", "workflow_dispatch"),
            "UNAUTHORIZED_AUDIT_EVENT")
    require(writer_job_result in ("success", "failure", "cancelled", "skipped"),
            "UNKNOWN_WRITER_RUN_STATE")
    flag = ("ENABLED" if enabled_flag == "true" else
            "DISABLED" if enabled_flag == "false" else "NOT_OBSERVED_ENABLED")
    status = ("FAILED_WRITER_REVIEW_PROVIDER_STATE" if writer_job_result in ("failure", "cancelled")
              else "OBSERVED_MATCH_NO_ACCEPTANCE" if expected == "MATCH"
              else "OBSERVED_DRIFT_OR_UNPUBLISHED")
    return {
        "schema": SCHEMA,
        "authority": "GET_ONLY_DELP_PROVIDER_AUDIT_NO_ACCEPTANCE",
        "status": status,
        "source_checkout_sha": checkout_sha,
        "event_name": event_name,
        "repository_flag_state": flag,
        "writer_job_result": writer_job_result,
        "candidate_sha": view["candidate_sha"],
        "source_input_digest": view["source_input_digest"],
        "delp_input_digest": view["delp_input_digest"],
        "read_views": dict(states),
        "observed_reconciliation": expected,
        "semantic_progress": {k: progress[k] for k in ("P", "E", "D", "DE")},
        "full_ESC_6_gate": "FAIL_CLOSED_UNRELEASED_CONSUMERS",
        "write_count": 0,
        "authority_effects": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--writer-job-result", required=True)
    args = parser.parse_args()
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True,
            cwd=ROOT).stdout.strip()
        with TemporaryDirectory(prefix="v32-760-audit-") as temp:
            report_path = Path(temp) / "readback.json"
            # Deliberately omit --apply, --plan-publication, or any write mode.
            result = subprocess.run([
                sys.executable, str(SOURCE), "--live-readback",
                "--report", str(report_path),
            ], cwd=ROOT, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                raise AuditError("READ_ONLY_PROVIDER_REPLAY_FAILED_EXIT_" + str(result.returncode))
            observed = json.loads(report_path.read_text(encoding="utf-8"))
        report = summary(
            observed, checkout_sha=sha, event_name=args.event_name,
            enabled_flag=os.environ.get("V32_718_LIVE_SCOREBOARD_ENABLED", ""),
            writer_job_result=args.writer_job_result,
        )
        code = 0
    except Exception as exc:
        report = {
            "schema": SCHEMA, "authority": "GET_ONLY_DELP_PROVIDER_AUDIT_NO_ACCEPTANCE",
            "status": "FAILED_UNVERIFIED", "write_count": 0,
            "error": type(exc).__name__ + ": " + str(exc),
            "authority_effects": [], "full_ESC_6_gate": "FAIL_CLOSED_UNRELEASED_CONSUMERS",
        }
        code = 3
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
