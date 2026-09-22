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

from transactionlib import TransactionError, execute, incomplete_transactions, recover_all
from validate_foundation import validate_authority
from test_v3_foundation import materialize


class TransactionJournalTests(unittest.TestCase):
    def test_committed_transaction_applies_all_after_images(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            a = root / "alpha.txt"
            b = root / "beta.txt"
            a.write_text("before-a", encoding="utf-8")
            b.write_text("before-b", encoding="utf-8")
            result = execute(
                root,
                tx_id="TX-COMMIT-001",
                command="RESOLVE_CONTROL",
                actor="agent-x",
                replacements={
                    "alpha.txt": b"after-a",
                    "beta.txt": b"after-b",
                },
            )
            self.assertEqual("COMMITTED", result["status"])
            self.assertEqual("after-a", a.read_text(encoding="utf-8"))
            self.assertEqual("after-b", b.read_text(encoding="utf-8"))
            self.assertEqual([], incomplete_transactions(root))

    def test_interrupted_mixed_transaction_blocks_authority_then_rolls_back(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            before_state = (root / "relay/STATE.yaml").read_bytes()
            before_events = (root / "relay/EVENTS.jsonl").read_bytes()
            with self.assertRaisesRegex(TransactionError, "injected transaction interruption"):
                execute(
                    root,
                    tx_id="TX-ROLLBACK-001",
                    command="RELEASE_LEASE",
                    actor="agent-x",
                    replacements={
                        "relay/STATE.yaml": b"broken-state-after",
                        "relay/EVENTS.jsonl": b"broken-events-after",
                    },
                    fail_after=1,
                )
            errors = validate_authority(root)
            self.assertTrue(any("requires recovery" in item for item in errors), errors)

            results = recover_all(root)
            self.assertEqual("ROLLED_BACK", results[0]["status"])
            self.assertEqual(before_state, (root / "relay/STATE.yaml").read_bytes())
            self.assertEqual(before_events, (root / "relay/EVENTS.jsonl").read_bytes())
            self.assertEqual([], incomplete_transactions(root))
            self.assertEqual([], validate_authority(root))

    def test_interruption_after_every_after_image_confirms_commit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            with self.assertRaisesRegex(TransactionError, "injected transaction interruption"):
                execute(
                    root,
                    tx_id="TX-CONFIRM-001",
                    command="RESOLVE_CONTROL",
                    actor="agent-x",
                    replacements={
                        "one.txt": b"one-after",
                        "two.txt": b"two-after",
                    },
                    fail_after=2,
                )
            results = recover_all(root)
            self.assertEqual("COMMITTED", results[0]["status"])
            self.assertEqual("CONFIRM_COMMIT", results[0]["recovery"]["strategy"])
            self.assertEqual(b"one-after", (root / "one.txt").read_bytes())
            self.assertEqual(b"two-after", (root / "two.txt").read_bytes())

    def test_unknown_external_change_refuses_destructive_auto_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            target = root / "alpha.txt"
            target.write_text("before", encoding="utf-8")
            with self.assertRaises(TransactionError):
                execute(
                    root,
                    tx_id="TX-OTHER-001",
                    command="RESOLVE_CONTROL",
                    actor="agent-x",
                    replacements={
                        "alpha.txt": b"after",
                        "zeta.txt": b"after-z",
                    },
                    fail_after=1,
                )
            target.write_text("external-change", encoding="utf-8")
            with self.assertRaisesRegex(TransactionError, "manual reconciliation"):
                recover_all(root)
            self.assertEqual("external-change", target.read_text(encoding="utf-8"))
            self.assertTrue(incomplete_transactions(root))

    def test_orphan_staging_directory_is_detected_and_cleaned(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            orphan = root / "relay/TRANSACTIONS/TX-ORPHAN-001/staged"
            orphan.mkdir(parents=True)
            (orphan / "000.after").write_text("staged only", encoding="utf-8")
            errors = validate_authority(root)
            self.assertTrue(any("has no manifest" in item for item in errors), errors)
            results = recover_all(root)
            self.assertEqual("ROLLED_BACK", results[0]["status"])
            self.assertFalse((root / "relay/TRANSACTIONS/TX-ORPHAN-001").exists())
            self.assertEqual([], validate_authority(root))


if __name__ == "__main__":
    unittest.main()
