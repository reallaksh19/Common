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


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    p.add_argument("--graph", type=Path, default=GRAPH)
    p.add_argument("--report", type=Path)
    p.add_argument("--assert-all-consumers", action="store_true")
    args = p.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        graph = json.loads(args.graph.read_text(encoding="utf-8"))
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
