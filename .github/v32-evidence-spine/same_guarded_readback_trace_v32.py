#!/usr/bin/env python3
"""GET-only, same-invocation V3.2 live-readback transport trace.

This runs a NEW guarded source replay after the original failed audit. All
reads within THIS diagnostic replay are recorded on one transport instance.
Never claim these observations came from the earlier failed invocation.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
sys.path.insert(0, str(SOURCE_DIR))
import delp_projection_v32 as delp
import vertical_cycle_v32 as cycle

SHA = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)
CODE = re.compile(r"^[A-Z][A-Z0-9_]{2,100}$")
GRAPH = ROOT / ".github/v32-evidence-spine/718-proposal-v2.json"
MANIFEST = ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json"


def _sha(value: Any) -> str | None:
    return value if isinstance(value, str) and SHA.fullmatch(value) else None


def classify_calls(calls: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Pure classifier against precommitted source-head ordering oracle."""
    heads = [_sha(c.get("sha")) for c in calls]
    stages = ("direct_initial", "delp_observer", "direct_final")
    serial = [{"phase": stages[i] if i < 3 else "extra_bound_read",
               "sha": head} for i, head in enumerate(heads)]
    if not heads:
        verdict = "NO_BOUND_PULL_OBSERVATION"
    elif heads[0] is None:
        verdict = "HEAD_UNAVAILABLE"
    elif len(heads) == 1:
        verdict = "UNOBSERVED_SECOND_CALL"
    elif heads[1] is None or heads[1] != heads[0]:
        verdict = "DELP_OBSERVER_MISMATCH"
    elif len(heads) == 2:
        verdict = "UNOBSERVED_FINAL_CALL"
    elif heads[2] is None:
        verdict = "HEAD_UNAVAILABLE"
    elif heads[2] != heads[0]:
        verdict = "PROVIDER_HEAD_MOVED"
    else:
        verdict = "MATCH"
    return {"verdict": verdict, "ordered_bound_pull_reads": serial,
            "read_count": len(heads)}


class ReadOnlyTraceTransport:
    """Expose only GET APIs; do not offer DELP GitHubStore mutation methods."""

    def __init__(self, provider: Any) -> None:
        self._provider = provider
        self.repository = "reallaksh19/Common"
        self.bound_calls: list[dict[str, Any]] = []

    def get_issue(self, number: int) -> dict[str, Any]:
        return self._provider.get_issue(number)

    def get_pull(self, number: int) -> dict[str, Any]:
        data = self._provider.get_pull(number)
        if number == 740:
            self.bound_calls.append({"sha": (data.get("head") or {}).get("sha")})
        return data

    def get_commit_sha(self, ref: str) -> str:
        return self._provider.get_commit_sha(ref)

    def compare(self, base: str, head: str) -> dict[str, Any]:
        return self._provider.compare(base, head)

    def list_comments(self, number: int) -> list[dict[str, Any]]:
        return self._provider.list_comments(number)


def run_guarded_trace(*, provider: Any | None = None,
                      graph: Mapping[str, Any] | None = None,
                      manifest: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Call unmodified cycle.live_readback ONCE, with one recording adapter."""
    if graph is None:
        graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    if manifest is None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    nodes = [n for n in graph.get("nodes", []) if n.get("ref") == "Common#733"]
    if (graph.get("programme") or {}).get("repository") != "reallaksh19/Common" or \
            len(nodes) != 1 or nodes[0].get("primary_pr") != "Common#740":
        raise ValueError("UNRELEASED_PROBE_BINDING")
    transport = ReadOnlyTraceTransport(provider or delp.GhTransport("reallaksh19/Common"))
    outcome, code = "SOURCE_REPLAY_SUCCEEDED_NO_ACCEPTANCE", "NONE"
    try:
        view = cycle.live_readback(dict(manifest), dict(graph), transport)
        # A successful source readback is an observation, NOT a grant of authority.
        if view.get("authority_effects") != [] or view.get("full_ESC_6_gate") != "FAIL_CLOSED_UNRELEASED_CONSUMERS":
            raise ValueError("SOURCE_AUTHORITY_BOUNDARY_CHANGED")
    except Exception as exc:
        outcome = "SOURCE_REPLAY_FAILED_UNVERIFIED"
        msg = str(exc)
        code = msg if CODE.fullmatch(msg) else "UNCLASSIFIED_SOURCE_FAILURE"
    classification = classify_calls(transport.bound_calls)
    return {"schema": "relay-v32-780-same-guarded-invocation-trace-v1",
            "authority": "GET_ONLY_REPLAY_DIAGNOSTIC_NO_ACCEPTANCE",
            "invocation_scope": "NEW_GUARDED_REPLAY_AFTER_ORIGINAL_FAILURE",
            "within_one_source_live_readback_call": True,
            "source_outcome": outcome, "source_error_code": code,
            **classification,
            "write_count": 0, "authority_effects": [],
            "full_ESC_6_gate": "FAIL_CLOSED_UNRELEASED_CONSUMERS"}
