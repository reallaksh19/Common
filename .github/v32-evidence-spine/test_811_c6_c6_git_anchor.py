#!/usr/bin/env python3
"""Seven actual adversarial verifications against already committed Git anchor."""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
sys.path.insert(0, str(SCRIPTS))
from v3lib import canonical_digest  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "git_anchor_v32", Path(__file__).with_name("811_c6_c6_verify_git_anchor.py"))
assert spec and spec.loader
anchor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(anchor)

ARCHIVE: Path | None = None
COLD_VERIFIER = Path(__file__).with_name("811_c6_c4_cold_successor.py")


def repack(items: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, raw in items.items():
            z.writestr(name, raw)
    return buffer.getvalue()


class GitAnchorAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if ARCHIVE is None or not ARCHIVE.is_file():
            raise RuntimeError("GIT_ANCHOR_VERIFIED_ARCHIVE_FILE_REQUIRED")
        cls.original = ARCHIVE.read_bytes()
        cls.anchor = anchor.committed_anchor()
        cls.files = anchor.verify_archive_bytes(cls.original, cls.anchor)

    def test_a01_real_archive_and_both_files_equal_immutable_git_anchor(self):
        self.assertEqual(
            "de3cac5d2c19b4301500fede250f4c56c226fda1", anchor.ANCHOR_SHA)
        self.assertEqual({"EVENTS.jsonl", "HANDOVER_CONTEXT.yaml"}, set(self.files))
        self.assertEqual(2, len(self.anchor["files"]))
        self.assertEqual(
            "UNKNOWN", self.anchor["owner_original_message_permalink"])
        self.assertEqual("AGENT_RECORDED_PROVIDER_EVIDENCE_NOT_OWNER_SIGNATURE",
                         self.anchor["authority"])

    def test_a02_one_bit_changed_zip_must_fail_before_extraction(self):
        b = bytearray(self.original)
        b[len(b) // 2] ^= 1
        with self.assertRaisesRegex(RuntimeError, "GIT_ANCHOR_ARCHIVE_BYTES_MISMATCH"):
            anchor.verify_archive_bytes(bytes(b), self.anchor)

    def test_a03_coherent_two_file_forgery_passes_old_but_not_git_anchor(self):
        ctx = yaml.safe_load(self.files["HANDOVER_CONTEXT.yaml"])
        events = [json.loads(s) for s in
                  self.files["EVENTS.jsonl"].decode("utf-8").splitlines() if s.strip()]
        ctx["accumulated_learning"]["what_changed"].append(
            "COHERENT_TWO_FILE_REWRITE_AFTER_EXPORT")
        actual = [e for e in events if e.get("type") == "HANDOVER_PLANNED"]
        self.assertEqual(1, len(actual))
        actual[0]["basis"][2] = canonical_digest(ctx)
        altered = {
            "HANDOVER_CONTEXT.yaml": yaml.safe_dump(ctx, sort_keys=False).encode("utf-8"),
            "EVENTS.jsonl": "".join(json.dumps(e, sort_keys=True) + "\n"
                                   for e in events).encode("utf-8")
        }
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)
            for name, raw in altered.items():
                (dest / name).write_bytes(raw)
            env = dict(os.environ)
            env.pop("GH_TOKEN", None)
            env.pop("GITHUB_TOKEN", None)
            old = subprocess.run(
                [sys.executable, str(COLD_VERIFIER), "--bundle", str(dest), "--local-only"],
                capture_output=True, text=True, timeout=40, env=env,
            )
            self.assertEqual(0, old.returncode, old.stderr[-1000:])
            self.assertIn("COLD_OFFLINE_AUTHORITY=NO_SOURCE_CURRENTNESS_NO_EXECUTION", old.stdout)
        with self.assertRaisesRegex(RuntimeError, "GIT_ANCHOR_ARCHIVE_BYTES_MISMATCH"):
            anchor.verify_archive_bytes(repack(altered), self.anchor)

    def test_a04_invalid_zip_members_or_duplicate_rejected_after_digest(self):
        for unsafe in ("../EVENTS.jsonl", "EXTRA.jsonl", "HANDOVER_CONTEXT.yaml/"):
            with self.subTest(unsafe=unsafe):
                changed = dict(self.files)
                changed[unsafe] = changed.pop("EVENTS.jsonl")
                blob = repack(changed)
                modified_manifest = copy.deepcopy(self.anchor)
                modified_manifest["source"]["artifact_zip_sha256"] = anchor.sha256(blob)
                modified_manifest["source"]["artifact_zip_bytes"] = len(blob)
                with self.assertRaisesRegex(RuntimeError, "GIT_ANCHOR_ARCHIVE_FILE_INVENTORY_MISMATCH"):
                    anchor.verify_archive_bytes(blob, modified_manifest)

    def test_a05_forged_member_digest_rejected(self):
        changed = copy.deepcopy(self.anchor)
        changed["files"][0]["sha256"] = "f" * 64
        with self.assertRaisesRegex(RuntimeError, "GIT_ANCHOR_FILE_HASH_MISMATCH"):
            anchor.verify_archive_bytes(self.original, changed)

    @staticmethod
    def _git(root, *args):
        return subprocess.run(["git", "-C", str(root), *args],
                              capture_output=True, check=True, timeout=30).stdout

    @classmethod
    def _create_squash_simulation(cls, root, tamper=False, retain_anchor_objects=True):
        """Actually make an orphan HEAD with a real tracked anchor file."""
        if retain_anchor_objects:
            subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout",
                            str(ROOT), str(root)], check=True, timeout=55)
            cls._git(root, "checkout", "--orphan", "synthetic-squash")
            cls._git(root, "read-tree", "--empty")
        else:
            subprocess.run(["git", "init", "--quiet", str(root)], check=True, timeout=20)
        raw = cls._git(ROOT, "show", anchor.ANCHOR_SHA + ":" + anchor.ANCHOR_PATH)
        if tamper:
            obj = json.loads(raw)
            obj["authority"] = "FAKE_OWNER_SIGNED"
            raw = (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode()
        output = root / anchor.ANCHOR_PATH
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(raw)
        cls._git(root, "add", "--", anchor.ANCHOR_PATH)
        cls._git(root, "-c", "user.name=CustodyTest",
                 "-c", "user.email=custody-test@example.invalid", "commit",
                 "--quiet", "-m", "Simulated squashed anchor manifest, independent HEAD")
        return output

    def test_a06_worktree_manifest_replacement_cannot_change_exact_commit_blob(self):
        # Earlier test was only writing a fake file in an unrelated directory.
        # Now mutate the ACTUAL tracked checkout path after a true checkout.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "real-worktree"
            subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout",
                            str(ROOT), str(root)], check=True, timeout=55)
            self._git(root, "checkout", "--detach", anchor.ANCHOR_SHA)
            original = anchor.committed_anchor(root)
            modified = root / anchor.ANCHOR_PATH
            self.assertTrue(modified.is_file())
            modified.write_text(json.dumps({"authority": "FAKE_OWNER_SIGNED"}))
            self.assertNotEqual(original, json.loads(modified.read_text()))
            self.assertEqual(original, anchor.committed_anchor(root))
        self.assertEqual("AGENT_RECORDED_PROVIDER_EVIDENCE_NOT_OWNER_SIGNATURE",
                         original["authority"])

    def test_a08_valid_anchor_blob_survives_synthetic_squash_head(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "squashed"
            self._create_squash_simulation(root)
            ancestor = subprocess.run(
                ["git", "-C", str(root), "merge-base", "--is-ancestor",
                 anchor.ANCHOR_SHA, "HEAD"], capture_output=True)
            self.assertEqual(1, ancestor.returncode, "must simulate a real non-ancestor squash")
            actual_blob = self._git(root, "rev-parse", "HEAD:" + anchor.ANCHOR_PATH)
            self.assertEqual(anchor.ANCHOR_BLOB_SHA, actual_blob.decode().strip())
            self.assertEqual(self.anchor, anchor.committed_anchor(root))

    def test_a09_squash_with_forged_manifest_blob_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "forged-squash"
            self._create_squash_simulation(root, tamper=True)
            with self.assertRaisesRegex(RuntimeError, "GIT_ANCHOR_BLOB_IDENTITY_MISMATCH"):
                anchor.committed_anchor(root)

    def test_a10_squash_blob_verifies_even_when_original_commit_not_in_clone(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "new-isolated-history"
            self._create_squash_simulation(root, retain_anchor_objects=False)
            original_missing = subprocess.run(
                ["git", "-C", str(root), "cat-file", "-e",
                 anchor.ANCHOR_SHA + "^{commit}"], capture_output=True)
            self.assertNotEqual(0, original_missing.returncode)
            self.assertEqual(self.anchor, anchor.committed_anchor(root))

    def test_a07_offline_replay_needs_no_live_provider_or_token(self):
        with patch.dict(os.environ, {"GH_TOKEN": "", "GITHUB_TOKEN": ""}):
            output = anchor.run_offline(ARCHIVE)
        self.assertEqual(self.files, output)
        self.assertEqual(
            "NOT_INDEPENDENT_NEW_AGENT_APPROVAL", self.anchor["cold_acceptance"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--archive", required=True)
    opts, remaining = parser.parse_known_args()
    ARCHIVE = Path(opts.archive).resolve()
    unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
