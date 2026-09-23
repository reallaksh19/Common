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

from transactionlib import (
    TransactionError,
    execute,
    incomplete_transactions,
    prune_terminal_payloads,
    recover_all,
)
from validate_foundation import validate_authority
from test_v3_foundation import materialize
from v3lib import load_yaml


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
            tx_dir = root / "relay/TRANSACTIONS/TX-COMMIT-001"
            manifest = load_yaml(tx_dir / "manifest.yaml")
            self.assertEqual("PRUNED", manifest["payload_state"])
            self.assertFalse((tx_dir / "staged").exists())
            self.assertFalse((tx_dir / "backups").exists())
            for operation in manifest["operations"]:
                self.assertNotIn("staged_path", operation)
                self.assertNotIn("backup_path", operation)
                self.assertIn("before_digest", operation)
                self.assertIn("after_digest", operation)


    def test_transaction_id_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            with self.assertRaisesRegex(TransactionError, "unsafe characters"):
                execute(
                    root,
                    tx_id="TX-../ESCAPE",
                    command="RESOLVE_CONTROL",
                    actor="agent-x",
                    replacements={"alpha.txt": b"after"},
                )
            self.assertFalse((root.parent / "ESCAPE").exists())

    def test_transaction_target_path_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            outside = root.parent / "relay-v3.1-outside.txt"
            if outside.exists():
                outside.unlink()
            with self.assertRaisesRegex((TransactionError, ValueError), "escapes repository root"):
                execute(
                    root,
                    tx_id="TX-SAFE-001",
                    command="RESOLVE_CONTROL",
                    actor="agent-x",
                    replacements={"../relay-v3.1-outside.txt": b"escape"},
                )
            self.assertFalse(outside.exists())

    def test_non_lease_command_cannot_use_liveness_carveout_to_rewrite_lease_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            lease_path = root / "relay/LEASES/LEASE-TA-011-01.yaml"
            lease = load_yaml(lease_path)
            mutated = dict(lease)
            mutated["state"] = "INVALIDATED"
            import yaml
            with self.assertRaisesRegex(
                TransactionError,
                "may only mutate lease custody liveness fields",
            ):
                execute(
                    root,
                    tx_id="TX-LIVENESS-ESCAPE-001",
                    command="RECORD_CHANGE_HYPOTHESIS",
                    actor="agent-x",
                    replacements={
                        "relay/LEASES/LEASE-TA-011-01.yaml": yaml.safe_dump(
                            mutated,
                            sort_keys=False,
                        ).encode("utf-8"),
                    },
                )

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
            tx_dir = root / "relay/TRANSACTIONS/TX-ROLLBACK-001"
            self.assertTrue((tx_dir / "staged").exists())
            self.assertTrue((tx_dir / "backups").exists())
            pending_manifest = load_yaml(tx_dir / "manifest.yaml")
            self.assertEqual("RECOVERY_PAYLOAD", pending_manifest["payload_state"])

            results = recover_all(root)
            self.assertEqual("ROLLED_BACK", results[0]["status"])
            self.assertEqual(before_state, (root / "relay/STATE.yaml").read_bytes())
            self.assertEqual(before_events, (root / "relay/EVENTS.jsonl").read_bytes())
            self.assertEqual([], incomplete_transactions(root))
            self.assertEqual([], validate_authority(root))
            terminal_manifest = load_yaml(tx_dir / "manifest.yaml")
            self.assertEqual("PRUNED", terminal_manifest["payload_state"])
            self.assertFalse((tx_dir / "staged").exists())
            self.assertFalse((tx_dir / "backups").exists())

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
            tx_dir = root / "relay/TRANSACTIONS/TX-CONFIRM-001"
            manifest = load_yaml(tx_dir / "manifest.yaml")
            self.assertEqual("PRUNED", manifest["payload_state"])
            self.assertFalse((tx_dir / "staged").exists())
            self.assertFalse((tx_dir / "backups").exists())

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

    def test_next_transaction_prunes_terminal_payload_left_after_commit_marking(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            execute(
                root,
                tx_id="TX-PRUNE-OLD-001",
                command="RESOLVE_CONTROL",
                actor="agent-x",
                replacements={"old.txt": b"old-after"},
            )
            tx_dir = root / "relay/TRANSACTIONS/TX-PRUNE-OLD-001"
            manifest_path = tx_dir / "manifest.yaml"
            manifest = load_yaml(manifest_path)
            terminal_updated_at = manifest["updated_at"]

            # Simulate residue from a process crash after terminal status was
            # durable but before physical payload cleanup.
            staged = tx_dir / "staged"
            backups = tx_dir / "backups"
            staged.mkdir(parents=True)
            backups.mkdir(parents=True)
            (staged / "residue.after").write_bytes(b"redundant")
            (backups / "residue.before").write_bytes(b"redundant")
            manifest["payload_state"] = "RECOVERY_PAYLOAD"
            manifest["operations"][0]["staged_path"] = (
                "relay/TRANSACTIONS/TX-PRUNE-OLD-001/staged/residue.after"
            )
            manifest["operations"][0]["backup_path"] = (
                "relay/TRANSACTIONS/TX-PRUNE-OLD-001/backups/residue.before"
            )
            import yaml
            manifest_path.write_text(
                yaml.safe_dump(manifest, sort_keys=False),
                encoding="utf-8",
            )

            self.assertEqual(["TX-PRUNE-OLD-001"], prune_terminal_payloads(root))
            compact = load_yaml(manifest_path)
            self.assertEqual("COMMITTED", compact["status"])
            self.assertEqual("PRUNED", compact["payload_state"])
            self.assertEqual(terminal_updated_at, compact["updated_at"])
            self.assertFalse(staged.exists())
            self.assertFalse(backups.exists())
            self.assertNotIn("staged_path", compact["operations"][0])
            self.assertNotIn("backup_path", compact["operations"][0])

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
