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
            "managed_block": view.inspect_managed_block(
                managed, expected["issue_read_views"][ref]),
            "body_digest": view.digest(managed),
        }
    pr_body = start_pull.get("body") or ""
    state["Common#740"] = {
        "observed": start_pull["title"],
        "expected": expected["draft_pr_title"],
        "title": "MATCH" if start_pull["title"] == expected["draft_pr_title"] else "DRIFT",
        "managed_block": view.inspect_managed_block(
            pr_body, expected["pr_managed_block"], pr=True),
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
                           s["managed_block"] == "MATCH" for s in state.values())
            else "DRIFT_OR_UNPUBLISHED"
        ),
        "full_ESC_6_gate": "FAIL_CLOSED_UNRELEASED_CONSUMERS",
        "authority_effects": [],
    }



class PublicationIncomplete(ReplayError):
    """A GitHub REST update may have partially succeeded; never assert atomicity."""

    def __init__(self, code: str, report: dict[str, Any]):
        self.report = report
        super().__init__(code)


def _provider_surface(transport: Any, ref: str) -> dict[str, Any]:
    number = int(ref.split("#")[-1])
    raw = transport.get_pull(number) if ref == "Common#740" else transport.get_issue(number)
    _require(isinstance(raw, dict) and isinstance(raw.get("title"), str) and
             isinstance(raw.get("body"), str), "PROVIDER_SURFACE_UNAVAILABLE:" + ref)
    _require(raw.get("number") == number, "PROVIDER_SURFACE_IDENTITY_MISMATCH:" + ref)
    return raw


def _apply_github_patch(transport: Any, ref: str, title: str, body: str) -> Any:
    """Field-separated GitHub transport: DELP owns issue titles, not this patch.

    The issue PATCH edits BODY ONLY, preserving the DELP-owned smart issue
    title and versioned LIVE_STATUS comment. PR metadata is disjoint.
    """
    _require(getattr(transport, "repository", None) == "reallaksh19/Common",
             "MUTATION_REPOSITORY_NOT_ALLOWED")
    number = int(ref.split("#")[-1])
    if ref == "Common#740":
        _require(callable(getattr(transport, "patch_pull_title_body", None)),
                 "PR_PATCH_ADAPTER_UNAVAILABLE")
        return transport.patch_pull_title_body(number, title, body)
    _require(ref in ("Common#718", "Common#733"),
             "ISSUE_PATCH_OUTSIDE_SELECTED_RESPONSIBILITY")
    _require(callable(getattr(transport, "patch_issue_body", None)),
             "ISSUE_BODY_PATCH_ADAPTER_UNAVAILABLE")
    return transport.patch_issue_body(number, body)


def guarded_publish(
    manifest: dict,
    graph: dict,
    transport: Any,
    *,
    expected_head: str,
    expected_input_digest: str,
    apply: bool = False,
) -> dict[str, Any]:
    """Single DELP issue-title/status owner + disjoint body/PR write adapters.

    No atomic transaction or provider compare-and-swap exists across issues.
    Fail closed with INCOMPLETE_SYNC after *any* ambiguous/partial write.
    Human narrative is guarded by whole-body readback and digest, and is never
    silently rolled back. This owns no Owner approval or progress authority.
    """
    import delp_projection_v32 as delp

    _require(getattr(transport, "repository", None) == "reallaksh19/Common",
             "MUTATION_REPOSITORY_NOT_ALLOWED")
    _require(delp._source_view_title_contract(graph),
             "SINGLE_ISSUE_PUBLISHER_CONTRACT_NOT_RELEASED")
    _require(isinstance(expected_head, str) and len(expected_head) == 40 and
             all(c in "0123456789abcdefABCDEF" for c in expected_head),
             "PINNED_EXACT_HEAD_REQUIRED")
    _require(isinstance(expected_input_digest, str) and
             expected_input_digest.startswith("sha256:") and len(expected_input_digest) == 71,
             "PINNED_SOURCE_DIGEST_REQUIRED")
    before = live_readback(manifest, graph, transport)
    _require(before["candidate_sha"] == expected_head, "PINNED_HEAD_MOVED")
    _require(before["source_input_digest"] == expected_input_digest,
             "PINNED_INPUT_DIGEST_MOVED")
    _require(before["pr_binding"] == "BOUND", "PR_NOT_BOUND_TO_RELEASED_GRAPH")
    _require(before["qualifier"]["state"] != "PROVEN",
             "QUALIFICATION_NOT_PROVEN_BY_THIS_WRITER")
    refs = ("Common#718", "Common#733", "Common#740")
    planned = {}
    for ref in refs:
        surface = _provider_surface(transport, ref)
        observed = before["read_views"][ref]
        _require(surface["title"] == observed["observed"] and
                 view.digest(surface["body"]) == observed["body_digest"],
                 "PROVIDER_CHANGED_SINCE_READBACK:" + ref)
        replacement = before["expected_managed_blocks"][ref]
        proposed = view.reconcile_managed_block(
            surface["body"], replacement, observed_digest=observed["body_digest"],
            pr=ref == "Common#740",
        )
        planned[ref] = {
            "previous_title": surface["title"], "expected_title": observed["expected"],
            "previous_body_digest": observed["body_digest"], "expected_body_digest": view.digest(proposed),
            "expected_body": proposed,
            "write_required": surface["title"] != observed["expected"] or proposed != surface["body"],
            "body_write_required": proposed != surface["body"],
        }
    changes = [ref for ref in refs if planned[ref]["write_required"]]
    report = {
        "schema": "relay-v32-718-single-issue-publisher-v2",
        "authority": "DELP_ISSUE_TITLE_STATUS_AND_SEPARATE_PR_METADATA_NO_ACCEPTANCE",
        "requested_mode": "APPLY" if apply else "DRY_RUN",
        "candidate_sha": expected_head,
        "source_input_digest": expected_input_digest,
        "delp_input_digest": before["delp_input_digest"],
        "changed_surfaces": changes,
        "applied_surfaces": [],
        "delp_issue_status": "NOT_RUN",
        "status": "PLANNED" if not apply else "IN_PROGRESS",
        "full_ESC_6_gate": "FAIL_CLOSED_UNRELEASED_CONSUMERS",
        "authority_effects": [],
    }
    if not apply:
        return report

    try:
        fresh = live_readback(manifest, graph, transport)
        if fresh["candidate_sha"] != expected_head or fresh["source_input_digest"] != expected_input_digest:
            raise ReplayError("PROVIDER_MOVED_BEFORE_FIRST_WRITE")
        # Validate all three original observations before DELP performs any
        # non-atomic managed-comment/title writes.
        for ref in refs:
            surface = _provider_surface(transport, ref)
            if surface["title"] != planned[ref]["previous_title"] or \
                    view.digest(surface["body"]) != planned[ref]["previous_body_digest"]:
                raise ReplayError("PROVIDER_MOVED_BEFORE_FIRST_WRITE:" + ref)
        report["delp_issue_status"] = "IN_PROGRESS_POSSIBLY_PARTIAL"
        issue_results = delp.sync_projection(
            delp.GitHubStore(transport), graph,
            lambda: delp.ledger_from_github(transport, graph),
            lambda: delp.observe_github(transport, graph),
            {ref: planned[ref]["previous_title"] for ref in ("Common#718", "Common#733")},
            title_overrides={ref: planned[ref]["expected_title"]
                             for ref in ("Common#718", "Common#733")},
            selected_refs=("Common#718", "Common#733"),
            expected_input_digest=before["delp_input_digest"],
        )
        report["delp_issue_status"] = issue_results
        # DELP is the ONLY issue-title + LIVE_STATUS writer. We exclusively
        # patch issue read-view BODY after confirming its DELP title has landed.
        for ref in ("Common#733", "Common#718"):
            current = _provider_surface(transport, ref)
            if current["title"] != planned[ref]["expected_title"] or \
                    view.digest(current["body"]) != planned[ref]["previous_body_digest"]:
                raise ReplayError("PROVIDER_MOVED_AFTER_DELP_BEFORE_BODY:" + ref)
            if planned[ref]["body_write_required"]:
                _apply_github_patch(transport, ref, planned[ref]["expected_title"],
                                    planned[ref]["expected_body"])
            checked = _provider_surface(transport, ref)
            if checked["title"] != planned[ref]["expected_title"] or \
                    view.digest(checked["body"]) != planned[ref]["expected_body_digest"]:
                raise ReplayError("PROVIDER_FAILED_ISSUE_READBACK:" + ref)
            if planned[ref]["write_required"]:
                report["applied_surfaces"].append(ref)

        # Re-observe exact head and whole input before any PR metadata write.
        mid = live_readback(manifest, graph, transport)
        if mid["candidate_sha"] != expected_head or mid["source_input_digest"] != expected_input_digest:
            raise ReplayError("PROVIDER_MOVED_BEFORE_PR_WRITE")
        pr = planned["Common#740"]
        current = _provider_surface(transport, "Common#740")
        if current["title"] != pr["previous_title"] or \
                view.digest(current["body"]) != pr["previous_body_digest"]:
            raise ReplayError("PROVIDER_PR_MOVED_BEFORE_WRITE")
        if pr["write_required"]:
            _apply_github_patch(transport, "Common#740", pr["expected_title"], pr["expected_body"])
        checked = _provider_surface(transport, "Common#740")
        if checked["title"] != pr["expected_title"] or \
                view.digest(checked["body"]) != pr["expected_body_digest"]:
            raise ReplayError("PROVIDER_FAILED_PR_READBACK")
        if pr["write_required"]:
            report["applied_surfaces"].append("Common#740")

        after = live_readback(manifest, graph, transport)
        if after["candidate_sha"] != expected_head or \
                after["source_input_digest"] != expected_input_digest or \
                after["reconciliation"] != "MATCH":
            raise ReplayError("POST_PUBLISH_PARITY_OR_INPUT_CHANGED")
        store = delp.GitHubStore(transport)
        for ref in ("Common#718", "Common#733"):
            status = store.read(ref)
            if status["input_digest"] != before["delp_input_digest"] or not status["version"]:
                raise ReplayError("DELP_LIVE_STATUS_NOT_VERIFIED:" + ref)
        report["status"] = "VERIFIED_ALL_SURFACES"
        report["verified_readback"] = after["reconciliation"]
        return report
    except Exception as exc:
        report["status"] = "INCOMPLETE_SYNC"
        report["error"] = str(exc)
        raise PublicationIncomplete("INCOMPLETE_SYNC: " + str(exc), report) from exc



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
    p.add_argument("--plan-publication", action="store_true",
                   help="dry-run guarded source-bound publication; no mutations")
    p.add_argument("--apply-live", action="store_true",
                   help="explicitly mutate GitHub (opt-in, head+digest pinned)")
    p.add_argument("--expected-head", help="required exact candidate SHA for publication")
    p.add_argument("--expected-input-digest", help="required source input digest for publication")
    args = p.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        graph = json.loads(args.graph.read_text(encoding="utf-8"))
        if args.live_readback or args.plan_publication or args.apply_live:
            import delp_projection_v32 as delp
            _require(args.repository == graph["programme"]["repository"],
                     "REQUESTED_REPOSITORY_MISMATCH")
            adapter = delp.GhTransport(args.repository)
            if args.plan_publication or args.apply_live:
                report = guarded_publish(
                    manifest, graph, adapter,
                    expected_head=args.expected_head,
                    expected_input_digest=args.expected_input_digest,
                    apply=args.apply_live,
                )
                report["exit_code"] = 0
            else:
                report = live_readback(manifest, graph, adapter)
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
    except PublicationIncomplete as exc:
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(exc.report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        print("V32-718-INCOMPLETE-SYNC: " + str(exc), file=sys.stderr)
        return 3
    except (ReplayError, view.ViewError, KeyError, ValueError, OSError) as exc:
        print(f"V32-718-REPLAY-FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
