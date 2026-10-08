#!/usr/bin/env python3
"""Read-only, self-running V3.2 #718 source→owner→OR→issue/PR replay.

The fixture EXPECTED values are committed independently before the renderer.
Phase gate can pass only R-PROJECTION's released consumer surfaces; a full
programme gate exits 2 while ESC-4/5 adapters are not implemented/released.
Never authors facts, progress, GitHub comments, titles or custody permission.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

import pr_responsibility_view_v32 as view

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json"
GRAPH = ROOT / ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json"
SCHEMA = "relay-v32-718-real-source-vertical-cycle-v1"
AUTHORITY = "READ_ONLY_SELF_REPLAY_NO_ACCEPTANCE"


class ReplayError(ValueError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ReplayError(code)


def _fixture(manifest: dict, key: str) -> dict:
    rows = [x for x in manifest["fixtures"] if x["id"] == key]
    _require(len(rows) == 1, "GOLDEN_FIXTURE_ID_MISSING:" + key)
    return rows[0]


def replay(manifest: dict, graph: dict) -> dict[str, Any]:
    """Run source modules; compare actual rendered outputs to precommitted oracles."""
    _require(manifest.get("schema") == "common-v32-718-precommitted-oracles-v1", "WRONG_ORACLE_VERSION")
    _require(manifest.get("released_proposal_digest") ==
             graph["programme"]["decomposition_proposal"].get("released_proposal_digest"),
             "FROZEN_PLAN_DIGEST_DRIFT")
    owner_history = {
        h["issue"]: {"pr_state": h["pr_state"], "candidate_sha": h["head_sha"]}
        for h in manifest["observed_historical_material"] if h.get("head_sha")
    }
    humans = {
        "Common#718": "V3.2 Evidence Spine",
        "Common#733": "Issue/PR Views",
        "PR": "Cross-Surface Views",
    }
    snapshot = view.build_views(
        graph, manifest, selected_leaf="Common#733", phase="C0",
        human_titles=humans, ledger=[], observations=owner_history,
    )
    gf = _fixture(manifest, "GF-SMART-SURFACES")["expected"]
    _require(snapshot["issue_titles"]["Common#718"] == gf["parent_title"],
             "GOLDEN_PARENT_TITLE_MISMATCH")
    _require(snapshot["issue_titles"]["Common#733"] == gf["child_title"],
             "GOLDEN_CHILD_TITLE_MISMATCH")
    _require(snapshot["draft_pr_title"] is None and gf["pr_title"] == "NOT_MATERIALIZED",
             "GOLDEN_NO_CURRENT_PRODUCT_PR_MISMATCH")
    _require(snapshot["historical_unreported"] == ["Common#720", "Common#724"],
             "LEGACY_UNREPORTED_GAP")
    _require(snapshot["claim_ids"] == ["ESC-3"] and snapshot["OR_ids"] == ["OR-718-04"],
             "OWNER_OR_CLAIM_MISMATCH")
    _require(snapshot["golden_fixture_ids"] == ["GF-PR-HEAD", "GF-PUBLISH-RACE", "GF-SMART-SURFACES"],
             "MISSING_R_PROJECTION_GOLDEN_CASE")
    _require(snapshot["leaf_semantic"]["P"] == 0 and snapshot["leaf_semantic"]["E"] == 0,
             "FAKE_PROGRESS")
    _require(snapshot["authority_effects"] == [], "UNAUTHORIZED_READ_VIEW_EFFECT")

    changed = _fixture(manifest, "GF-PR-HEAD")
    old = changed["input"]["candidate_before"]
    new = changed["input"]["candidate_after"]
    stale_qualifier = {
        "schema": "relay-v3.2-qualification-observation-v1",
        "repository": "reallaksh19/Common", "responsibility": "Common#733",
        "expected_candidate_sha": old, "observed_candidate_sha": old,
        "authority": "DERIVED_OBSERVATION_ONLY", "overall": "PROVEN",
    }
    draft = view.build_views(
        graph, manifest, selected_leaf="Common#733", phase="C0",
        human_titles=humans, ledger=[], observations=owner_history,
        draft_pr={"number": 740, "head_sha": new, "lifecycle": "DRAFT"},
        qualification=stale_qualifier,
    )
    oracle = changed["expected"]
    _require(draft["qualification"]["state"] == oracle["new_qualification"],
             "GOLDEN_STALE_QUALIFIER_MISMATCH")
    _require(draft["qualification"]["basis"] == "STALE_OR_UNBOUND_QUALIFICATION",
             "QUALIFIER_STALE_BASIS_UNREPORTED")
    _require("HEAD:" + oracle["smart_title_head"] in draft["draft_pr_title"],
             "SMART_PR_HEAD_NOT_UPDATED")
    _require(draft["pr"]["binding"] == "UNBOUND_ADVISORY" and draft["authority_effects"] == [],
             "UNBOUND_PR_GAINS_AUTHORITY")
    _require(draft["leaf_semantic"] == snapshot["leaf_semantic"],
             "CHANGED_HEAD_FABRICATED_SEMANTIC_PROGRESS")
    _require(draft["input_digest"] != snapshot["input_digest"], "CHANGED_HEAD_DIGEST_NOT_MOVED")

    human = "## Human change rationale\nPreserve exactly this line.\n"
    managed = view.reconcile_managed_block(
        human, draft["pr_managed_block"], observed_digest=view.digest(human))
    _require(managed.startswith(human), "OWNER_HUMAN_PR_TEXT_OVERWRITTEN")
    _require("Input basis: `" + draft["input_digest"] + "`" in managed,
             "PR_MANAGED_INPUT_NOT_BOUND")
    # Names are read-only preview surfaces; no provider mutation API exists.
    stages = {
        "OR_LEDGER": "PASS_SOURCE_TRACE",
        "DECOMPOSITION_BINDING": "PASS_RELEASE_DIGEST",
        "TASK_EVIDENCE_INPUT": "UNREPORTED_LEGACY_NOT_MANUFACTURED",
        "SOURCE_OBSERVATION": "PASS_REAL_V32_DELP_AND_STALE_QUALIFIER",
        "RESPONSIBILITY_SNAPSHOT": "PASS_BOUND_INPUT_DIGEST",
        "PARENT_TITLE": "PASS_GOLDEN_MATCH",
        "CHILD_TITLE": "PASS_GOLDEN_MATCH",
        "PR_TITLE": "PASS_GOLDEN_CHANGED_HEAD_PREVIEW",
        "PR_MANAGED_DESCRIPTION": "PASS_GUARDED_PURE_RECONCILE",
        "HANDOVER_PROMPT": "NOT_IMPLEMENTED_NOT_RELEASED",
        "AGENT_MATRIX": "NOT_IMPLEMENTED_NOT_RELEASED",
    }
    return {
        "schema": SCHEMA,
        "authority": AUTHORITY,
        "fixture_manifest_digest": view.digest(manifest),
        "released_proposal_digest": manifest["released_proposal_digest"],
        "source_input_digest": snapshot["input_digest"],
        "changed_head_input_digest": draft["input_digest"],
        "stage_results": stages,
        "parent_actual_title": snapshot["issue_titles"]["Common#718"],
        "child_actual_title": snapshot["issue_titles"]["Common#733"],
        "draft_changed_head_title": draft["draft_pr_title"],
        "draft_pr_managed_description": draft["pr_managed_block"],
        "material_vs_facts": {"merged_issues": snapshot["historical_unreported"],
                              "checkpoint_facts": "UNREPORTED"},
        "owner_origin_status": list({i["original_source_status"]
                                    for i in snapshot["owner_trace"]["owner_intents"]}),
        "R_PROJECTION_phase_gate": "PASS_PURE_READ_VIEWS",
        "full_ESC_6_gate": "FAIL_CLOSED_UNRELEASED_CONSUMERS",
        "next": "RECONCILE_LIVE_PUBLISHER_AND_RELEASE_SEPARATE_HANDOVER_AGENT_METRIC_CONSUMERS",
        "authority_effects": [],
    }


def live_readback(manifest: dict, graph: dict, transport: Any) -> dict[str, Any]:
    """Compare live GitHub readback to *independently generated* source views.

    No provider write methods are called. The caller authenticates its adapter;
    the pure function can only validate the observations it receives.
    GitHub's separate issue/title/body writes are NOT an atomic transaction.
    """
    import delp_projection_v32 as delp

    repository = graph["programme"]["repository"]
    delp.require_repository_match(graph, repository, live=False)
    root, child = "Common#718", "Common#733"
    root_issue = transport.get_issue(718)
    child_issue = transport.get_issue(733)
    start_pull = transport.get_pull(740)
    _require(all(isinstance(x, dict) for x in (root_issue, child_issue, start_pull)),
             "PROVIDER_READ_UNAVAILABLE")
    _require(start_pull.get("number") == 740, "PR_PROVIDER_IDENTITY_CHANGED")
    head = ((start_pull.get("head") or {}).get("sha"))
    _require(isinstance(head, str) and len(head) == 40 and
             all(x in "0123456789abcdefABCDEF" for x in head),
             "PROVIDER_HEAD_UNAVAILABLE")
    lifecycle = ("DRAFT" if start_pull.get("draft") else
                 "MERGED" if start_pull.get("merged") else
                 str(start_pull.get("state") or "").upper())
    _require(lifecycle in {"DRAFT", "OPEN", "CLOSED", "MERGED"}, "PR_LIFECYCLE_UNOBSERVED")
    observations = delp.observe_github(transport, graph)
    _require(observations.get(child, {}).get("candidate_sha") == head,
             "CANDIDATE_CHANGED_DURING_OBSERVATION")
    ledger = delp.ledger_from_github(transport, graph)
    titles = {}
    for ref, observed in ((root, root_issue), (child, child_issue), ("PR", start_pull)):
        original = observed.get("title")
        _require(isinstance(original, str) and " — " in original,
                 "HUMAN_TITLE_BASE_UNRESOLVED:" + ref)
        titles[ref] = original.rsplit(" — ", 1)[1]
    expected = view.build_views(
        graph, manifest, observations=observations, ledger=ledger,
        selected_leaf=child, phase="C4", human_titles=titles,
        draft_pr={"number": 740, "head_sha": head, "lifecycle": lifecycle},
        qualification=None,
    )
    # Double-read the *actual* live candidate. A concurrent force push must
    # fail closed rather than rendering a stale head as current.
    final_pull = transport.get_pull(740)
    _require(isinstance(final_pull, dict) and
             (final_pull.get("head") or {}).get("sha") == head and
             bool(final_pull.get("draft")) == bool(start_pull.get("draft")),
             "PROVIDER_MOVED_DURING_RECONCILIATION")
    # The provider can race us on issue titles/PR human descriptions without
    # changing PR head. Fail closed on *all* three read surfaces; this is an
    # observation guard, NOT proof of atomic GitHub REST publication.
    _require(all(final_pull.get(k) == start_pull.get(k) for k in ("title", "body", "state")),
             "PROVIDER_PR_METADATA_MOVED_DURING_RECONCILIATION")
    final_root = transport.get_issue(718)
    final_child = transport.get_issue(733)
    _require(isinstance(final_root, dict) and isinstance(final_child, dict) and
             all(final_root.get(k) == root_issue.get(k) for k in ("title", "body")) and
             all(final_child.get(k) == child_issue.get(k) for k in ("title", "body")),
             "PROVIDER_ISSUE_MOVED_DURING_RECONCILIATION")
    state = {}
    for ref, observed in ((root, root_issue), (child, child_issue)):
        target = expected["issue_titles"][ref]
        actual = observed["title"]
        managed = observed.get("body") or ""
        state[ref] = {
            "observed": actual, "expected": target,
            "title": "MATCH" if target == actual else "DRIFT",
            "managed_block": "PRESENT" if view.ISSUE_START in managed and
            view.ISSUE_END in managed else "MISSING",
            "body_digest": view.digest(managed),
        }
    pr_body = start_pull.get("body") or ""
    state["Common#740"] = {
        "observed": start_pull["title"],
        "expected": expected["draft_pr_title"],
        "title": "MATCH" if start_pull["title"] == expected["draft_pr_title"] else "DRIFT",
        "managed_block": "PRESENT" if view.START in pr_body and
        view.END in pr_body else "MISSING",
        "body_digest": view.digest(pr_body),
    }
    return {
        "schema": "relay-v32-718-live-provider-readback-v1",
        "authority": AUTHORITY,
        "candidate_sha": head,
        "source_input_digest": expected["input_digest"],
        "delp_input_digest": expected["delp_input_digest"],
        "source_provenance": "AUTHENTICATED_PROVIDER_IS_CALLER_RESPONSIBILITY",
        "pr_binding": expected["pr"]["binding"],
        "qualifier": expected["qualification"],
        "historical_unreported": expected["historical_unreported"],
        "semantic_progress": expected["leaf_semantic"],
        "read_views": state,
        "expected_managed_blocks": {
            root: expected["issue_read_views"][root],
            child: expected["issue_read_views"][child],
            "Common#740": expected["pr_managed_block"],
        },
        "reconciliation": (
            "MATCH" if all(s["title"] == "MATCH" and
                           s["managed_block"] == "PRESENT" for s in state.values())
            else "DRIFT_OR_UNPUBLISHED"
        ),
        "full_ESC_6_gate": "FAIL_CLOSED_UNRELEASED_CONSUMERS",
        "authority_effects": [],
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    p.add_argument("--graph", type=Path, default=GRAPH)
    p.add_argument("--report", type=Path)
    p.add_argument("--assert-all-consumers", action="store_true")
    p.add_argument("--live-readback", action="store_true",
                   help="GET-only source/provider projection parity (requires gh token)")
    p.add_argument("--repository", default="reallaksh19/Common")
    p.add_argument("--require-match", action="store_true",
                   help="fail if issue/PR titles or managed blocks are out of sync")
    args = p.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        graph = json.loads(args.graph.read_text(encoding="utf-8"))
        if args.live_readback:
            import delp_projection_v32 as delp
            _require(args.repository == graph["programme"]["repository"],
                     "REQUESTED_REPOSITORY_MISMATCH")
            report = live_readback(manifest, graph, delp.GhTransport(args.repository))
            report["exit_code"] = (2 if args.assert_all_consumers or
                                   (args.require_match and report["reconciliation"] != "MATCH")
                                   else 0)
        else:
            report = replay(manifest, graph)
            report["exit_code"] = 2 if args.assert_all_consumers else 0
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return report["exit_code"]
    except (ReplayError, view.ViewError, KeyError, ValueError, OSError) as exc:
        print(f"V32-718-REPLAY-FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
