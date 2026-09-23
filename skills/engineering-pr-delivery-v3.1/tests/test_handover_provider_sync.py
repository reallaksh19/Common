from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from handover_provider_sync import END, START, sync_handover_provider
from test_relay_can import prepare_git
from test_v3_foundation import DIGEST, dump
from transactionlib import TransactionError
from v3lib import load_events, load_yaml


class FakeGitHub:
    def __init__(self, *, with_relay: bool = True, duplicate_relay: bool = False) -> None:
        self.next_number = 1900
        self.next_id = 9000
        self.issues: dict[str, dict] = {}
        self.subissues: dict[str, list[int]] = {}
        self._add_issue(1771, 7001, "Parent", "# Human parent\n\nDo not overwrite this.")
        if with_relay:
            self._add_issue(
                1870,
                7002,
                "[Relay] #1771 — Parent",
                "<!-- relay-v3.1:case parent=example/repo#1771 -->\n\n# Human handover notes\n\nKeep this too.",
            )
            self.subissues[self._sub_url(1771)] = [1870]
        else:
            self.subissues[self._sub_url(1771)] = []
        if duplicate_relay:
            self._add_issue(
                1871,
                7003,
                "[Relay] #1771 — duplicate",
                "<!-- relay-v3.1:case parent=example/repo#1771 -->",
            )
            self.subissues[self._sub_url(1771)].append(1871)

    def _url(self, number: int) -> str:
        return f"https://api.github.test/repos/example/repo/issues/{number}"

    def _sub_url(self, number: int) -> str:
        return self._url(number) + "/sub_issues"

    def _add_issue(self, number: int, provider_id: int, title: str, body: str) -> dict:
        issue = {
            "id": provider_id,
            "number": number,
            "title": title,
            "body": body,
            "html_url": f"https://github.com/example/repo/issues/{number}",
        }
        self.issues[self._url(number)] = issue
        return issue

    def __call__(self, method: str, url: str, token: str, payload):
        if token != "test-token":
            raise AssertionError("unexpected token")
        if method == "GET" and url.endswith("/sub_issues"):
            return [dict(self.issues[self._url(number)]) for number in self.subissues.get(url, [])]
        if method == "GET":
            return dict(self.issues[url])
        if method == "PATCH":
            self.issues[url]["body"] = payload["body"]
            return dict(self.issues[url])
        if method == "POST" and url == "https://api.github.test/repos/example/repo/issues":
            self.next_number += 1
            self.next_id += 1
            return dict(self._add_issue(self.next_number, self.next_id, payload["title"], payload["body"]))
        if method == "POST" and url.endswith("/sub_issues"):
            provider_id = payload["sub_issue_id"]
            match = next(issue for issue in self.issues.values() if issue["id"] == provider_id)
            self.subissues.setdefault(url, []).append(match["number"])
            return dict(match)
        raise AssertionError((method, url, payload))


def materialize_projection(root: Path, *, handover_number: int | None = 1870) -> None:
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
        "handover_issue": (
            {
                "repository": "example/repo",
                "number": handover_number,
                "url": f"https://github.com/example/repo/issues/{handover_number}",
            }
            if handover_number is not None
            else None
        ),
        "current_frontier": {
            "ep": "EP-TA-011",
            "work_package": "WP-TA-109",
            "lease": "LEASE-TA-011-01",
            "executor": "agent-x",
            "custody_epoch": 1,
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
        "accepted_truth": {"checkpoint": "CP-1", "accepted_head": "abc1234", "acceptance": []},
        "material": {"accepted_head": "abc1234", "working_head": "abc1234", "status": "AT_ACCEPTED_HEAD"},
        "negative_knowledge": {"rejected_approaches": [], "accepted_do_not_reopen": []},
        "accountability": {"scope_received": [], "completed": [], "partial": [], "remaining": [], "acceptance_movement": {}, "value_added": [], "continuation_reason": "NEW"},
        "active_change": None,
        "delivery": {},
        "records": [],
        "next": {"action": "Continue bounded work.", "stop_conditions": []},
    }
    dump(root / "relay/GENERATED/HANDOVER_LEDGER.yaml", ledger)
    (root / "relay/GENERATED/HANDOVER_LEDGER.md").write_text("# stale generated body\n", encoding="utf-8")
    (root / "relay/GENERATED/PARENT_RELAY_SUMMARY.md").write_text("## stale parent summary\n", encoding="utf-8")


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

            parent_body = client.issues[client._url(1771)]["body"]
            handover_body = client.issues[client._url(1870)]["body"]
            self.assertIn("# Human parent", parent_body)
            self.assertIn("# Human handover notes", handover_body)
            self.assertIn(START, parent_body)
            self.assertIn(END, parent_body)
            self.assertIn("Handover ledger: example/repo#1870", parent_body)
            self.assertIn("Custody epoch: 1", handover_body)

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

    def test_provider_sync_allocates_bookkeeping_ids_from_parent_issue(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            materialize_projection(root)
            client = FakeGitHub()

            result = sync_handover_provider(
                root,
                tx_id=None,
                event_id=None,
                actor="relay",
                token="test-token",
                api_base="https://api.github.test",
                client=client,
            )

            self.assertEqual("COMMITTED", result["status"])
            self.assertEqual("TX.1771.1", result["id"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            synced = [row for row in events if row["type"] == "HANDOVER_LEDGER_SYNCED"][-1]
            self.assertEqual("EVT.1771.1", synced["event_id"])

    def test_missing_relay_issue_is_created_attached_and_persisted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            materialize_projection(root, handover_number=None)
            client = FakeGitHub(with_relay=False)

            result = sync_handover_provider(
                root,
                tx_id="TX-HANDOVER-CREATE",
                event_id="EVT-HANDOVER-CREATE",
                actor="relay",
                token="test-token",
                api_base="https://api.github.test",
                client=client,
            )
            self.assertEqual("COMMITTED", result["status"])
            ledger = load_yaml(root / "relay/GENERATED/HANDOVER_LEDGER.yaml")
            created_number = ledger["handover_issue"]["number"]
            self.assertIn(created_number, client.subissues[client._sub_url(1771)])
            self.assertIn("[Relay] #1771", client.issues[client._url(created_number)]["title"])
            status = load_yaml(root / "relay/GENERATED/HANDOVER_PROVIDER_STATUS.yaml")
            self.assertEqual(created_number, status["handover"]["issue_number"])

    def test_duplicate_relay_issues_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            materialize_projection(root, handover_number=None)
            client = FakeGitHub(with_relay=True, duplicate_relay=True)
            with self.assertRaisesRegex(TransactionError, "MULTIPLE_RELAY_ISSUES"):
                sync_handover_provider(
                    root,
                    tx_id="TX-HANDOVER-DUP",
                    event_id="EVT-HANDOVER-DUP",
                    actor="relay",
                    token="test-token",
                    api_base="https://api.github.test",
                    client=client,
                )


if __name__ == "__main__":
    unittest.main()
