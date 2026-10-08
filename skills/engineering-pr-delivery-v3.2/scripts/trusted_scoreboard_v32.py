#!/usr/bin/env python3
"""Trusted V3.2 C4-S5 event-to-DELP publisher; never execute PR-head code.

Runs ONLY from a trusted default-branch GitHub Actions checkout. An untrusted
event payload is a trigger, not source authority: compare its claimed candidate
with the provider's live PR identity/head before any writes. Live publication
requires the repository OWNER opt-in variable and existing guarded_publish().
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Mapping

import delp_projection_v32 as delp
import vertical_cycle_v32 as cycle

ROOT = Path(__file__).resolve().parents[3]
GRAPH = ROOT / ".github/v32-evidence-spine/718-proposal-v2.json"
MANIFEST = ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json"
SCHEMA = "relay-v32-trusted-live-scoreboard-gate-v1"
ACTIONS = frozenset({"opened", "reopened", "synchronize", "ready_for_review", "edited"})
SHA = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


def _identity(graph: Mapping[str, Any]) -> dict[str, Any]:
    """Root, selected child and bound product PR from actual released graph."""
    pair = delp._source_view_title_contract(graph)
    if pair is None:
        raise ValueError("RELEASED_R_PROJECTION_BINDING_MISSING")
    root, leaf = pair
    matching = [n for n in graph["nodes"] if n.get("ref") == leaf]
    if len(matching) != 1 or not matching[0].get("primary_pr"):
        raise ValueError("PRODUCT_PR_BINDING_MISSING")
    pr = matching[0]["primary_pr"]
    repo = graph["programme"]["repository"]
    if not all(isinstance(x, str) and x.startswith(repo.split("/")[1] + "#")
               for x in (root, leaf, pr)):
        raise ValueError("CURRENT_SOURCE_ADAPTER_REPO_BOUNDARY")
    if (root, leaf, pr) != ("Common#718", "Common#733", "Common#740"):
        # The R-PROJECTION and provider readback module remain one-programme
        # adapters; do not imply portability beyond the actual 718 source.
        raise ValueError("UNRELEASED_GENERIC_LIVE_ADAPTER")
    return {"repository": repo, "root": root, "leaf": leaf,
            "pr_number": int(pr.split("#")[-1]), "base": graph["programme"].get("base_ref", "main")}


def gate(event_name: str, event: Mapping[str, Any], graph: Mapping[str, Any],
         provider_pull: Mapping[str, Any], *, enabled: bool) -> dict[str, Any]:
    """Independent, deterministic negative authorization gate: NO writes."""
    target = _identity(graph)
    if event_name not in {"pull_request_target", "workflow_dispatch", "issue_comment"}:
        code = "DENY_EVENT_NAME"
    elif (event.get("repository") or {}).get("full_name") != target["repository"]:
        code = "DENY_REPOSITORY"
    elif event_name == "pull_request_target" and event.get("action") not in ACTIONS:
        code = "DENY_EVENT_ACTION"
    elif event_name == "issue_comment" and event.get("action") not in {"created", "edited", "deleted"}:
        code = "DENY_EVENT_ACTION"
    elif event_name == "issue_comment" and (
            not isinstance(event.get("issue"), Mapping) or
            str(event["issue"].get("number")) != target["leaf"].split("#")[-1]):
        code = "DENY_UNBOUND_ISSUE"
    elif event_name == "issue_comment" and (event.get("issue") or {}).get("pull_request"):
        code = "DENY_PR_COMMENT_SURFACE"
    elif event_name == "issue_comment" and (
            not isinstance(event.get("comment"), Mapping) or
            type(event["comment"].get("id")) is not int or
            event["comment"]["id"] <= 0 or
            not isinstance(event["comment"].get("body"), str)):
        code = "DENY_UNVERIFIABLE_COMMENT"
    elif event_name == "issue_comment" and event["comment"]["body"].lstrip().startswith(delp.STATUS_START):
        # DELP's managed LIVE_STATUS update emits issue_comment. Never loop.
        code = "DENY_MANAGED_STATUS_COMMENT"
    elif event_name == "pull_request_target" and not isinstance(event.get("pull_request"), Mapping):
        code = "DENY_MISSING_PR_EVENT"
    elif event_name == "workflow_dispatch" and not isinstance(event.get("inputs"), Mapping):
        code = "DENY_MISSING_DISPATCH_INPUTS"
    else:
        event_pr = event["pull_request"] if event_name == "pull_request_target" else None
        # A task-evidence comment is only an event signal. It cannot supply
        # candidate SHA or accepted facts; both come from fresh provider+DELP.
        pin = ((event_pr.get("head") or {}).get("sha") if event_pr is not None else
               event["inputs"].get("expected_head") if event_name == "workflow_dispatch" else
               (provider_pull.get("head") or {}).get("sha"))
        number = (event_pr.get("number") if event_pr is not None else
                  event["inputs"].get("pr_number") if event_name == "workflow_dispatch" else
                  target["pr_number"])
        if str(number) != str(target["pr_number"]):
            code = "DENY_UNBOUND_PR"
        elif event_pr and (event_pr.get("head", {}).get("repo") or {}).get("full_name") != target["repository"]:
            code = "DENY_FOREIGN_HEAD_REPOSITORY"
        elif event_pr and (event_pr.get("base") or {}).get("ref") != target["base"]:
            code = "DENY_WRONG_BASE"
        elif ((provider_pull.get("head") or {}).get("repo") or {}).get("full_name") != target["repository"]:
            code = "DENY_PROVIDER_HEAD_REPOSITORY"
        elif provider_pull.get("number") != target["pr_number"]:
            code = "DENY_PROVIDER_PR_IDENTITY"
        elif provider_pull.get("state") == "closed" and not provider_pull.get("merged"):
            code = "DENY_CLOSED_UNMERGED_PR"
        elif (provider_pull.get("base") or {}).get("ref", target["base"]) != target["base"]:
            code = "DENY_PROVIDER_BASE"
        elif ((provider_pull.get("base") or {}).get("repo") or {}).get("full_name") != target["repository"]:
            code = "DENY_PROVIDER_BASE_REPOSITORY"
        elif event_name == "pull_request_target" and provider_pull.get("merged"):
            # Historical/merged PRs can only be reconciled through deliberate
            # owner-pinned dispatch, not spurious automatic PR edit events.
            code = "DENY_MERGED_AUTO_EVENT"
        elif not isinstance(pin,str) or not SHA.fullmatch(pin) or pin != (provider_pull.get("head") or {}).get("sha"):
            code = "DENY_STALE_EVENT_HEAD"
        elif not enabled:
            code = "DISABLED_BY_OWNER_FLAG"
        else:
            code = "ALLOW"
    return {"schema": SCHEMA, "authority": "TRUSTED_EVENT_GATE_NOT_OWNER_ACCEPTANCE",
            "decision": code, "repository": target["repository"],
            "selected_leaf": target["leaf"], "bound_pr": target["pr_number"],
            "observed_head": (provider_pull.get("head") or {}).get("sha"),
            "writes": 0, "semantic_progress": "NEVER_ASSIGNED"}


def run(event_name: str, event: Mapping[str, Any], *, enabled: bool, apply: bool = False,
        transport: Any | None = None, graph: Any | None = None, manifest: Any | None = None) -> dict[str, Any]:
    """Explicit APPLY requires owner flag; fail closed on stale head/readback."""
    if graph is None:
        graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    if manifest is None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    target = _identity(graph)
    if transport is None:
        transport = delp.GhTransport(target["repository"])
    provider_pr = transport.get_pull(target["pr_number"])
    decision = gate(event_name, event, graph, provider_pr, enabled=enabled)
    if decision["decision"] != "ALLOW":
        decision["status"] = "SKIPPED_WITHOUT_MUTATION"
        return decision
    view = cycle.live_readback(manifest, graph, transport)
    if view["candidate_sha"] != decision["observed_head"] or view["pr_binding"] != "BOUND":
        raise cycle.ReplayError("GATE_PROVIDER_MOVED_BEFORE_PUBLICATION")
    decision["input_digest"] = view["source_input_digest"]
    if not apply:
        decision["status"] = "AUTHORIZED_DRY_RUN_NO_WRITE"
        decision["reconciliation"] = view["reconciliation"]
        return decision
    # A permitted trigger alone never becomes authority to accept evidence.
    report = cycle.guarded_publish(manifest, graph, transport,
        expected_head=decision["observed_head"],
        expected_input_digest=view["source_input_digest"], apply=True)
    decision["status"] = report["status"]
    decision["applied_surfaces"] = report["applied_surfaces"]
    decision["reconciliation"] = report["verified_readback"]
    decision["writes"] = len(report["applied_surfaces"])
    return decision


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        event = json.loads(args.event.read_text(encoding="utf-8"))
        enabled = os.environ.get("V32_718_LIVE_SCOREBOARD_ENABLED") == "true"
        report = run(args.event_name, event, enabled=enabled, apply=args.apply)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, sort_keys=True, indent=2))
        return 0 if report["decision"] in ("ALLOW","DISABLED_BY_OWNER_FLAG") or report["decision"].startswith("DENY_") else 2
    except cycle.PublicationIncomplete as exc:
        # GitHub has no cross-surface transaction: keep the partial write
        # report even when the job fails so the next agent can reconcile.
        failed = dict(exc.report)
        failed["source_event_name"] = args.event_name
        failed["exit_code"] = 3
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(failed, sort_keys=True, indent=2) + "\n",
                                   encoding="utf-8")
        print(json.dumps(failed, sort_keys=True, indent=2), file=sys.stderr)
        return 3
    except Exception as exc:
        # A pre-write failure is still not a successful live scoreboard sync.
        failed = {"schema": SCHEMA, "status": "FAILED_UNVERIFIED",
                  "error": type(exc).__name__ + ": " + str(exc), "exit_code": 3}
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(failed, sort_keys=True, indent=2) + "\n",
                                   encoding="utf-8")
        print("V32_744_TRUSTED_PUBLICATION_INCOMPLETE: "+failed["error"], file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
