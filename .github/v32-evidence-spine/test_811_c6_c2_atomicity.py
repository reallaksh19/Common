"""C6 read-only RED-first contract: execute REAL legacy PLAN_HANDOVER atomicity.

Precommitted expected behavior lives in 811-c6-c2-atomicity-golden-v1.json.
A legacy transaction recovery PASS is not source-bound C6 product delivery.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
TESTS = ROOT / "skills/engineering-pr-delivery-v3.2/tests"
for path in (SCRIPTS, TESTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from plan_handover import plan_handover  # noqa: E402
from test_handover_context import target_observation  # noqa: E402
from test_relay_can import prepare_git  # noqa: E402
from transactionlib import (  # noqa: E402
    TransactionError, recover_all, incomplete_transactions,
)
from v3lib import load_yaml, load_events  # noqa: E402

ORACLE = json.loads(
    Path(__file__).with_name("811-c6-c2-atomicity-golden-v1.json").read_text(encoding="utf-8")
)


class ActualC6TransactionAtomicityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert ORACLE["schema"] == "common-v32-811-c6-atomicity-oracle-v1"
        assert ORACLE["production_status"] == "DELP_SOURCE_NOT_WIRED"
        assert [row["id"] for row in ORACLE["scenarios"]] == [
            f"A{i:02d}" for i in range(1, 6)
        ]

    @staticmethod
    def _handover(root, base, suffix, *, fail_after=None):
        return plan_handover(
            root,
            tx_id=f"TX-C6-ATOM-{suffix}",
            event_id=f"EVT-C6-ATOM-{suffix}",
            actor="owner",
            target_path=target_observation(root),
            base_ref=base,
            complex_mode=False,
            fail_after=fail_after,
        )

    @staticmethod
    def _tracked(root):
        state = load_yaml(root / "relay/STATE.yaml")
        paths = [
            "relay/EVENTS.jsonl",
            "relay/GENERATED/HANDOVER_CONTEXT.yaml",
            str((state.get("generated") or {}).get("snapshot")),
        ]
        paths.extend(
            str(p.relative_to(root))
            for p in sorted((root / "relay/LEASES").glob("LEASE-*.yaml"))
        )
        return {
            relative: (root / relative).read_bytes() if (root / relative).exists() else None
            for relative in paths
        }

    def test_a01_first_operation_interruption_requires_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            before = self._tracked(root)
            with self.assertRaisesRegex(TransactionError, "injected transaction interruption"):
                self._handover(root, base, "001", fail_after=1)
            self.assertTrue(incomplete_transactions(root))
            manifest = load_yaml(root / "relay/TRANSACTIONS/TX-C6-ATOM-001/manifest.yaml")
            self.assertEqual("RECOVERY_REQUIRED", manifest["status"])
            self.assertEqual(1, len(manifest["applied"]))
            self.assertEqual(["ROLLED_BACK"], [r["status"] for r in recover_all(root)])
            self.assertEqual(before, self._tracked(root))
            self.assertEqual([], incomplete_transactions(root))

    def test_a02_two_operation_partial_handover_rolls_back_exact_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            before = self._tracked(root)
            with self.assertRaisesRegex(TransactionError, "injected transaction interruption"):
                self._handover(root, base, "002", fail_after=2)
            manifest = load_yaml(root / "relay/TRANSACTIONS/TX-C6-ATOM-002/manifest.yaml")
            self.assertEqual("RECOVERY_REQUIRED", manifest["status"])
            self.assertEqual(2, len(manifest["applied"]))
            self.assertEqual(["ROLLED_BACK"], [r["status"] for r in recover_all(root)])
            self.assertEqual(before, self._tracked(root))
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertFalse(any(row.get("event_id") == "EVT-C6-ATOM-002" for row in events))

    def test_a03_second_plan_handover_cannot_skip_incomplete_transaction(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            with self.assertRaises(TransactionError):
                self._handover(root, base, "003", fail_after=1)
            # Authority projection refuses the incomplete transaction even before
            # transactionlib can prepare the attempted next handover.
            with self.assertRaisesRegex(RuntimeError, "requires recovery before authority can be used"):
                self._handover(root, base, "NEXT")
            self.assertFalse((root / "relay/TRANSACTIONS/TX-C6-ATOM-NEXT").exists())
            self.assertEqual(["ROLLED_BACK"], [r["status"] for r in recover_all(root)])

    def test_a04_external_target_change_refuses_blind_rollback(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            with self.assertRaises(TransactionError):
                self._handover(root, base, "004", fail_after=1)
            manifest_path = root / "relay/TRANSACTIONS/TX-C6-ATOM-004/manifest.yaml"
            manifest = load_yaml(manifest_path)
            self.assertTrue(manifest["applied"])
            damaged_path = root / manifest["applied"][0]
            damaged = b"EXTERNAL_UNKNOWN_TARGET_CHANGE\\n"
            damaged_path.write_bytes(damaged)
            with self.assertRaisesRegex(TransactionError, "external/unknown target changes"):
                recover_all(root)
            self.assertEqual(damaged, damaged_path.read_bytes())
            self.assertEqual("RECOVERY_REQUIRED", load_yaml(manifest_path)["status"])
            self.assertTrue(incomplete_transactions(root))

    def test_a05_legacy_handover_commits_once_without_source_or_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            self.assertEqual("COMMITTED", self._handover(root, base, "005")["status"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertEqual(1, len([
                row for row in events if row.get("event_id") == "EVT-C6-ATOM-005"
            ]))
            context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            self.assertNotIn("source_bound_successor", context)
            self.assertEqual([], incomplete_transactions(root))
            self.assertEqual([], recover_all(root))
            with self.assertRaises(TransactionError):
                self._handover(root, base, "005")


if __name__ == "__main__":
    unittest.main()
