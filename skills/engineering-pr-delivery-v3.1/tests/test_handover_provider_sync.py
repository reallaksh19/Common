from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from handover_provider_sync import END, START, sync_handover_provider
from test_relay_can import prepare_git
from test_v3_foundation import DIGEST, dump
from v3lib import load_events, load_yaml


class FakeGitHub:
    def __init__(self) -> None:
        self.issues = {
            "https://api.github.test/repos/example/repo/issues/1771": {
                "body": "# Human parent\n\nDo not overwrite this.",
                "html_url": "https://github.com/example/repo/issues/1771",
            },
            "https://api.github.test/repos/example/repo/issues/1870": {
                "body": "# Human handover notes\n\nKeep this too.",
                "html_url": "https://github.com/example/repo/issues/1870",
            },
        }

    def __call__(self, method: str, url: str, token: str, payload):
        if token != "test-token":
            raise AssertionError("unexpected token")
        if method == "GET":
            return dict(self.issues[url])
        if method == "PATCH":
            self.issues[url]["body"] = payload["body"]
            return dict(self.issues[url])
        raise AssertionError(method)


def materialize_projection(root: Path) -> None:
    ledger = {
        "schema_version": "relay-v3.1-handover-ledger",
        "authority": "DERIVED_PROVIDER_PROJECTION",
        "generated_from": {
            "state_digest": DIGEST,
            "task_snapshot_digest": DIGEST,
            "roadmap_revision": "RM-0012",
        },
        "parent_issue": {
            "repository": "example/repo",
            "number": 1771,
            "title": "Parent",
            "url": "https://github.com/example/repo/issues/1771",
            "state": "OPEN",
            "disposition": "NO_CHANGE",
            "relationships": [],
        },
        "handover_issue": {
            "repository": "example/repo",
            "number": 1870,
            "url": "https://github.com/example/repo/issues/1870",
        },
        "current_frontier": {
            "ep": "EP-TA-011",
            "work_package": "WP-TA-109",
            "lease": "LEASE-TA-011-01",
            "executor": "agent-x",
            "status": "ACTIVE",
            "continuation": "NEW",
        },
        "parent_progress": {
            "complete": 1,
            "partial": 0,
            "pending": 1,
            "blocked": 0,
            "deferred": 0,
            "not_applicable": 0,
            "unknown": 0,
            "total": 2,
        },
        "ep_index": [],
        "pending_items": [],
        "known_issues": [],
        "offloads": [],
        "delivery": {},
        "records": [],
        "next": {"action": "Continue bounded work.", "stop_conditions": []},
    }
    dump(root / "relay/GENERATED/HANDOVER_LEDGER.yaml", ledger)
    (root / "relay/GENERATED/HANDOVER_LEDGER.md").write_text(
        "# Relay Handover\n\nEP-TA-011 ACTIVE / NEW\n",
        encoding="utf-8",
    )
    (root / "relay/GENERATED/PARENT_RELAY_SUMMARY.md").write_text(
        "## Relay\n\nHandover ledger: #1870\n",
        encoding="utf-8",
    )


class HandoverProviderSyncTests(unittest.TestCase):
    def test_sync_updates_only_relay_blocks_and_verifies_readback(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            materialize_projection(root)
            client = FakeGitHub()

            result = sync_handover_provider(
                root,
                tx_id="TX-HANDOVER-SYNC-001",
                event_id="EVT-HANDOVER-SYNC-001",
                actor="relay",
                token="test-token",
                api_base="https://api.github.test",
                client=client,
            )
            self.assertEqual("COMMITTED", result["status"])

            parent_body = client.issues["https://api.github.test/repos/example/repo/issues/1771"]["body"]
            handover_body = client.issues["https://api.github.test/repos/example/repo/issues/1870"]["body"]
            self.assertIn("# Human parent", parent_body)
            self.assertIn("# Human handover notes", handover_body)
            self.assertIn(START, parent_body)
            self.assertIn(END, parent_body)
            self.assertIn("Handover ledger: #1870", parent_body)
            self.assertIn("EP-TA-011 ACTIVE / NEW", handover_body)

            status = load_yaml(root / "relay/GENERATED/HANDOVER_PROVIDER_STATUS.yaml")
            self.assertTrue(status["parent"]["updated"])
            self.assertTrue(status["handover"]["updated"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertEqual(
                "HANDOVER_LEDGER_SYNCED",
                [row for row in events if row["event_id"] == "EVT-HANDOVER-SYNC-001"][0]["type"],
            )

            second = sync_handover_provider(
                root,
                tx_id="TX-HANDOVER-SYNC-002",
                event_id="EVT-HANDOVER-SYNC-002",
                actor="relay",
                token="test-token",
                api_base="https://api.github.test",
                client=client,
            )
            self.assertEqual("COMMITTED", second["status"])
            status = load_yaml(root / "relay/GENERATED/HANDOVER_PROVIDER_STATUS.yaml")
            self.assertFalse(status["parent"]["updated"])
            self.assertFalse(status["handover"]["updated"])


if __name__ == "__main__":
    unittest.main()
