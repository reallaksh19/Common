"""#868 / WP0 native C6 -> fresh-process cold verification RED.

A genuinely executed local PLAN_HANDOVER transaction produces context + event,
from the existing repository's mock GitHub provider fixture. The synthetic
provider is intentionally NEVER represented as a live GitHub authentication.
"""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
SCRIPTS = HERE.parents[1] / "scripts"
for entry in (str(HERE.parent), str(SCRIPTS)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from test_handover_context import HandoverContextTests, target_observation
from test_relay_can import prepare_git
from plan_handover import plan_handover
from v3lib import canonical_digest, load_events, load_yaml

COLD = REPO / ".github/v32-evidence-spine/811_c6_c4_cold_successor.py"
GRAPH_PATH = ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json"
GRAPH_REVISION = "a" * 40
REPOSITORY = "reallaksh19/Common"


class ColdCoreLinkRed(unittest.TestCase):
    """D-06: event, challenge and nested core all bind the same producer truth."""

    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.workspace.cleanup)
        root = Path(cls.workspace.name) / "native"
        root.mkdir(parents=True)
        _, base = prepare_git(root)
        target = target_observation(root)
        graph, provider = HandoverContextTests._source_bound_fixture()
        origin = {
            "repository": REPOSITORY,
            "revision": GRAPH_REVISION,
            "path": GRAPH_PATH,
            "permalink": "https://github.com/" + REPOSITORY
                         + "/blob/" + GRAPH_REVISION + "/" + GRAPH_PATH,
        }
        native = plan_handover(
            root,
            tx_id="TX-865-NATIVE-001",
            event_id="EVT-865-NATIVE-001",
            actor="owner",
            target_path=target,
            base_ref=base,
            complex_mode=False,
            successor_challenge_count=3,
            delp_source={
                "graph": graph,
                "leaf_ref": "Common#720",
                "provider": provider,
                "__native_graph_source": origin,
            },
        )
        if native.get("status") != "COMMITTED":
            raise AssertionError("D06_NATIVE_PLAN_HANDOVER_DID_NOT_COMMIT")
        cls.real_context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
        events, errors = load_events(root / "relay/EVENTS.jsonl")
        if errors:
            raise AssertionError("D06_NATIVE_EVENT_PARSE_FAILED:" + str(errors))
        cls.real_events = events
        chosen = [
            idx for idx, event in enumerate(events)
            if event.get("type") == "HANDOVER_PLANNED"
            and (event.get("details") or {}).get("source_graph_pinned_location")
        ]
        if len(chosen) != 1:
            raise AssertionError("D06_NATIVE_GRAPH_LOCATOR_EVENT_REQUIRED")
        cls.chosen = chosen[0]
        core = cls.real_context["source_bound_successor"]["delp_responsibility_core"]
        if core["basis_digest"] != events[cls.chosen]["details"]["source_delp_responsibility_basis_digest"]:
            raise AssertionError("D06_NATIVE_EVENT_CORE_POSITIVE_BROKEN")
        if core["basis_digest"] != cls.real_context["successor_entry"]["challenge_basis"]["source_responsibility_basis_digest"]:
            raise AssertionError("D06_NATIVE_CHALLENGE_CORE_POSITIVE_BROKEN")

    def invoke_cold(self, context, events):
        with tempfile.TemporaryDirectory() as td:
            bundle = Path(td)
            (bundle / "HANDOVER_CONTEXT.yaml").write_text(
                yaml.safe_dump(context, sort_keys=False), encoding="utf-8")
            (bundle / "EVENTS.jsonl").write_text(
                "".join(json.dumps(e, sort_keys=True) + "\n" for e in events),
                encoding="utf-8",
            )
            # No GitHub tokens: a fresh real subprocess may verify offline
            # consistency, never report live provider currentness.
            env = os.environ.copy()
            env.pop("GH_TOKEN", None)
            env.pop("GITHUB_TOKEN", None)
            return subprocess.run(
                [sys.executable, str(COLD), "--bundle", str(bundle), "--local-only"],
                cwd=str(REPO), capture_output=True, text=True, timeout=50, env=env)

    def bundle(self):
        return copy.deepcopy(self.real_context), copy.deepcopy(self.real_events)

    def test_d06_positive_native_bundle_offline_only(self):
        ctx, events = self.bundle()
        result = self.invoke_cold(ctx, events)
        self.assertEqual(0, result.returncode, result.stderr[-1200:])
        self.assertIn("COLD_LOCAL_CONTEXT_EVENT_LINK=PASS_NOT_LIVE_CURRENT",
                      result.stdout)
        self.assertIn("COLD_OFFLINE_AUTHORITY=NO_SOURCE_CURRENTNESS_NO_EXECUTION",
                      result.stdout)
        self.assertNotIn("COLD_LIVE_GITHUB_SOURCE_REPLAY", result.stdout)

    def test_d06_positive_historical_v1_missing_new_core_is_explicitly_legacy(self):
        ctx, events = self.bundle()
        ctx["source_bound_successor"].pop("delp_responsibility_core")
        ctx["successor_entry"]["challenge_basis"].pop("source_responsibility_basis_digest")
        events[self.chosen]["details"].pop("source_delp_responsibility_basis_digest")
        events[self.chosen]["basis"][2] = canonical_digest(ctx)
        result = self.invoke_cold(ctx, events)
        self.assertEqual(0, result.returncode, result.stderr[-1200:])
        self.assertIn("NO_SOURCE_CURRENTNESS_NO_EXECUTION", result.stdout)

    def test_d06_red_event_only_core_digest_must_fail_closed(self):
        ctx, events = self.bundle()
        events[self.chosen]["details"]["source_delp_responsibility_basis_digest"] = (
            "sha256:" + "0" * 64)
        result = self.invoke_cold(ctx, events)
        self.assertNotEqual(
            0, result.returncode,
            "D06_EVENT_ONLY_CORE_DIGEST_MUTATION_ACCEPTED_BY_COLD")

    def test_d06_red_challenge_core_digest_must_fail_closed(self):
        ctx, events = self.bundle()
        ctx["successor_entry"]["challenge_basis"]["source_responsibility_basis_digest"] = (
            "sha256:" + "0" * 64)
        # Rebind the context hash so the legacy check cannot mask the gap.
        events[self.chosen]["basis"][2] = canonical_digest(ctx)
        result = self.invoke_cold(ctx, events)
        self.assertNotEqual(
            0, result.returncode,
            "D06_CHALLENGE_CORE_DIGEST_MUTATION_ACCEPTED_BY_COLD")

    def test_d06_red_tampered_nested_core_digest_must_fail_closed(self):
        ctx, events = self.bundle()
        core = ctx["source_bound_successor"]["delp_responsibility_core"]
        core["progress"]["leaf"]["P"] = 99
        # Keep the claimed basis_digest and 4 legacy axes unchanged, and
        # preserve the legacy event-to-context hash link after modification.
        events[self.chosen]["basis"][2] = canonical_digest(ctx)
        result = self.invoke_cold(ctx, events)
        self.assertNotEqual(
            0, result.returncode,
            "D06_FORGED_NESTED_CORE_WITH_REBOUND_CONTEXT_HASH_ACCEPTED")


if __name__ == "__main__":
    unittest.main()
