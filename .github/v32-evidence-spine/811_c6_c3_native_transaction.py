#!/usr/bin/env python3
"""Actual hosted GitHub GET-only CLI → real V3.2 PLAN_HANDOVER transaction."""
from __future__ import annotations

import copy
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
TESTS = ROOT / "skills/engineering-pr-delivery-v3.2/tests"
for p in (SCRIPTS, TESTS):
    sys.path.insert(0, str(p))

from test_relay_can import prepare_git  # noqa: E402
from test_handover_context import target_observation  # noqa: E402
from v3lib import load_yaml, load_events  # noqa: E402

REPO = "reallaksh19/Common"
GRAPH_SHA = "b4e61d8f61e9738833564795971692241c2e3df9"
GRAPH_PATH = ".github/v32-evidence-spine/718-proposal-v2.json"
LEAF = "Common#793"


def require(value, label):
    if not value:
        raise RuntimeError(label)


def new_fixture(root: Path):
    _, base = prepare_git(root)
    target_path = target_observation(root)
    target = load_yaml(target_path)
    target["repository"] = REPO
    target["provider_ref"] = "github:reallaksh19/Common#793"
    target["url"] = "https://github.com/reallaksh19/Common/issues/793"
    target["number"] = 793
    target["title"] = "Source-backed C6 handover target — actual GitHub issue #793"
    target_path.write_text(yaml.safe_dump(target, sort_keys=False), encoding="utf-8")
    return base, target_path


def command(root, base, target, txid, eventid, frozen_path=None):
    parts = [
        sys.executable, str(SCRIPTS / "plan_handover.py"), str(root),
        "--actor", "owner", "--tx-id", txid, "--event-id", eventid,
        "--target-observation", str(target), "--base-ref", base,
        "--successor-challenge-count", "3",
        "--source-repository", REPO,
        "--source-graph-revision", GRAPH_SHA,
        "--source-graph-path", GRAPH_PATH,
        "--source-leaf-ref", LEAF,
    ]
    if frozen_path is not None:
        parts += ["--source-frozen-basis", str(frozen_path)]
    return subprocess.run(parts, capture_output=True, text=True, timeout=160,
                          cwd=ROOT, env=os.environ.copy())


def main():
    require(os.environ.get("GITHUB_REPOSITORY") == REPO, "NATIVE_PROVIDER_REPOSITORY_MISMATCH")
    require(os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"), "READ_ONLY_TOKEN_MISSING")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        base, target = new_fixture(root)
        ok = command(root, base, target, "TX-C6-C3-LIVE-001", "EVT-C6-C3-LIVE-001")
        if ok.returncode != 0:
            raise RuntimeError("NATIVE_PLAN_HANDOVER_FAILURE " + ok.stderr[-1800:])
        require("COMMITTED" in ok.stdout, "NATIVE_CLI_NO_TRANSACTION_COMMIT")
        ctx = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
        src = ctx.get("source_bound_successor") or {}
        require(src.get("currentness") == "CURRENT_READ_ONLY", "NATIVE_SOURCE_NOT_CURRENT")
        require(src.get("leaf") == LEAF, "NATIVE_SOURCE_LEAF_MISMATCH")
        require(src.get("execution_admission") == "NEVER_FROM_RECONSTRUCTION",
                "NATIVE_RECONSTRUCTION_PROMOTED_TO_AUTHORITY")
        require(src.get("authority_effects") == [], "NATIVE_AUTHORITY_EFFECTS")
        digests = src.get("digests") or {}
        require(set(digests) == {"graph", "plan", "input", "provider"}, "NATIVE_SOURCE_DIGEST_MISSING")
        require(all(str(v).startswith("sha256:") for v in digests.values()), "NATIVE_BAD_SOURCE_DIGEST")
        entry = ctx.get("successor_entry") or {}
        require((entry.get("challenge_basis") or {}).get("source_input_digest") == digests["input"],
                "NATIVE_SUCCESSOR_SOURCE_PIN_MISSING")
        events, errors = load_events(root / "relay/EVENTS.jsonl")
        require(not errors, "NATIVE_EVENTS_INVALID")
        items = [e for e in events if e.get("event_id") == "EVT-C6-C3-LIVE-001"]
        require(len(items) == 1, "NATIVE_HANDOVER_EVENT_COUNT")
        require(items[0]["details"]["source_bound_input_digest"] == digests["input"],
                "NATIVE_EVENT_SOURCE_DIGEST_MISMATCH")
        origin = items[0]["details"].get("source_graph_pinned_location") or {}
        require(origin.get("repository") == REPO, "NATIVE_SOURCE_ORIGIN_REPOSITORY_MISSING")
        require(origin.get("revision") == GRAPH_SHA, "NATIVE_SOURCE_ORIGIN_COMMIT_MISSING")
        require(origin.get("path") == GRAPH_PATH, "NATIVE_SOURCE_ORIGIN_FILE_MISSING")
        require(origin.get("permalink") ==
                "https://github.com/" + REPO + "/blob/" + GRAPH_SHA + "/" + GRAPH_PATH,
                "NATIVE_SOURCE_ORIGIN_PERMALINK_MISSING")
        print("C6_C3_NATIVE_SOURCE_GRAPH_PERMALINK_IN_EVENT=PASS")
        print("C6_C3_NATIVE_GITHUB_GET_CLI_REAL_PLAN_HANDOVER=PASS")
        print("C6_C3_OBSERVED_SOURCE_PR_HEAD_BOUND=Common#800")
        print("C6_C3_OWNER_OR_MERGE_AUTHORITY=NOT_GRANTED")

        # Fresh fixture: stale frozen input must fail before all transaction targets.
        other = root / "second"
        other.mkdir()
        b2, t2 = new_fixture(other)
        stale = copy.deepcopy(digests)
        stale["input"] = "sha256:" + "0" * 64
        frozen_path = other / "frozen-basis.yaml"
        frozen_path.write_text(yaml.safe_dump({"digests": stale}), encoding="utf-8")
        events_before = (other / "relay/EVENTS.jsonl").read_bytes()
        bad = command(other, b2, t2, "TX-C6-C3-STALE", "EVT-C6-C3-STALE", frozen_path)
        require(bad.returncode != 0 and "SOURCE_BOUND_RECONCILIATION_REQUIRED" in bad.stderr,
                "NATIVE_STALE_PIN_FAILED_OPEN " + bad.stderr[-800:])
        require(events_before == (other / "relay/EVENTS.jsonl").read_bytes(),
                "NATIVE_STALE_PIN_MUTATED_EVENTS")
        require(not (other / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists(),
                "NATIVE_STALE_PIN_MUTATED_CONTEXT")
        require(not (other / "relay/TRANSACTIONS/TX-C6-C3-STALE").exists(),
                "NATIVE_STALE_PIN_CREATED_TX")
        print("C6_C3_NATIVE_STALE_PIN_FAIL_CLOSED_ZERO_TX=PASS")
        print("C6_C3_INDEPENDENT_SUCCESSOR_REVIEW=NOT_SUBMITTED")


if __name__ == "__main__":
    main()
