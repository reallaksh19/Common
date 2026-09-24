from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from v25_migration import legacy_inventory
from v3lib import validate_schema


class PortableLegacyInventoryTests(unittest.TestCase):
    def test_crlf_and_lf_produce_identical_digest(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            relay = root / "agents" / "relay"
            relay.mkdir(parents=True)

            yaml_file = relay / "sample.yaml"
            json_file = relay / "nested" / "sample.json"
            md_file = relay / "DOC.md"
            txt_file = relay / "NOTES.txt"

            json_file.parent.mkdir(parents=True)

            # Write LF
            yaml_file.write_bytes(b"key: value\nlist:\n  - item1\n  - item2\n")
            json_file.write_bytes(b'{\n  "name": "test",\n  "ok": true\n}\n')
            md_file.write_bytes(b"# Title\n\nSome documentation.\n")
            txt_file.write_bytes(b"line 1\nline 2\n")

            entries_lf, digest_lf = legacy_inventory(root)

            # Rewrite all text files with CRLF
            yaml_file.write_bytes(b"key: value\r\nlist:\r\n  - item1\r\n  - item2\r\n")
            json_file.write_bytes(b'{\r\n  "name": "test",\r\n  "ok": true\r\n}\r\n')
            md_file.write_bytes(b"# Title\r\n\r\nSome documentation.\r\n")
            txt_file.write_bytes(b"line 1\r\nline 2\r\n")

            entries_crlf, digest_crlf = legacy_inventory(root)

            self.assertEqual(digest_lf, digest_crlf)
            self.assertEqual(
                [x["digest"] for x in entries_lf],
                [x["digest"] for x in entries_crlf],
            )

    def test_posix_path_sorting_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            relay = root / "agents" / "relay"

            # Create paths where directory names and file names test sorting order
            (relay / "certifications" / "discovery").mkdir(parents=True)
            (relay / "certifications" / "discovery" / "DISC-001.yaml").write_text("id: DISC-001\n", encoding="utf-8")
            (relay / "REPO_PROFILE.yaml").write_text("id: REPO_PROFILE\n", encoding="utf-8")
            (relay / "REPO_STATE.yaml").write_text("id: REPO_STATE\n", encoding="utf-8")
            (relay / "roadmap").mkdir(parents=True)
            (relay / "roadmap" / "PROGRESS.yaml").write_text("id: PROGRESS\n", encoding="utf-8")

            entries, _ = legacy_inventory(root)
            paths = [e["path"] for e in entries]

            # In POSIX string sort, REPO_PROFILE.yaml and REPO_STATE.yaml (uppercase 'R') come before certifications ('c')
            expected_order = [
                "agents/relay/REPO_PROFILE.yaml",
                "agents/relay/REPO_STATE.yaml",
                "agents/relay/certifications/discovery/DISC-001.yaml",
                "agents/relay/roadmap/PROGRESS.yaml",
            ]
            self.assertEqual(paths, expected_order)

    def test_content_change_changes_digest(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            relay = root / "agents" / "relay"
            relay.mkdir(parents=True)

            target = relay / "file.yaml"
            target.write_text("value: 1\n", encoding="utf-8")
            _, digest_1 = legacy_inventory(root)

            target.write_text("value: 2\n", encoding="utf-8")
            _, digest_2 = legacy_inventory(root)

            self.assertNotEqual(digest_1, digest_2)


class SchemaRepositoryRegexTests(unittest.TestCase):
    def test_ep_schema_accepts_valid_repositories(self) -> None:
        valid_repos = [
            "reallaksh19/Advanced_Analysis",
            "owner/repo",
            "org-1.name/repo_2-name",
            "A/B",
        ]
        for repo in valid_repos:
            ep = {
                "schema_version": "relay-v3.1-ep",
                "id": "EP-TEST-001",
                "work_package": "WP-001",
                "outcome": {"statement": "test"},
                "basis": {
                    "predecessor_checkpoint": "CP-001",
                    "material_base": "85e59a93d469",
                    "protocol_basis": "Common#457",
                    "semantic_dependencies": [],
                },
                "scope": {"write": ["a/**"], "read": [], "protect": [], "prohibit": []},
                "acceptance": [{"id": "AC-1", "statement": "test", "evidence_requirements": [{"test": "t.py"}]}],
                "quality_policy": {"level": "STANDARD", "independent_review": "OPTIONAL"},
                "parent_issue": {
                    "provider": "GITHUB",
                    "repository": repo,
                    "number": 1771,
                    "title": "Parent",
                    "url": "https://github.com/test",
                    "baseline": {
                        "observed_at": "2026-09-24T00:00:00Z",
                        "body_digest": "sha256:" + ("a" * 64),
                        "acceptance_items": [{"id": "A1", "statement": "test"}],
                    },
                },
                "next": {"first_action": "test", "stop_conditions": ["stop"]},
            }
            errors = validate_schema("ep", ep, "EP")
            self.assertEqual([], errors, f"Expected valid repository {repo} to pass, got: {errors}")

    def test_ep_schema_rejects_invalid_repositories(self) -> None:
        invalid_repos = [
            "",
            "no-slash",
            "owner/",
            "/repo",
            "/",
            "owner/repo with spaces",
            "owner /repo",
            "owner/repo/extra",
        ]
        for repo in invalid_repos:
            ep = {
                "schema_version": "relay-v3.1-ep",
                "id": "EP-TEST-001",
                "work_package": "WP-001",
                "outcome": {"statement": "test"},
                "basis": {
                    "predecessor_checkpoint": "CP-001",
                    "material_base": "85e59a93d469",
                    "protocol_basis": "Common#457",
                    "semantic_dependencies": [],
                },
                "scope": {"write": ["a/**"], "read": [], "protect": [], "prohibit": []},
                "acceptance": [{"id": "AC-1", "statement": "test", "evidence_requirements": [{"test": "t.py"}]}],
                "quality_policy": {"level": "STANDARD", "independent_review": "OPTIONAL"},
                "parent_issue": {
                    "provider": "GITHUB",
                    "repository": repo,
                    "number": 1771,
                    "title": "Parent",
                    "url": "https://github.com/test",
                    "baseline": {
                        "observed_at": "2026-09-24T00:00:00Z",
                        "body_digest": "sha256:" + ("a" * 64),
                        "acceptance_items": [{"id": "A1", "statement": "test"}],
                    },
                },
                "next": {"first_action": "test", "stop_conditions": ["stop"]},
            }
            errors = validate_schema("ep", ep, "EP")
            self.assertTrue(bool(errors), f"Expected invalid repository {repo!r} to fail validation")

    def test_parent_issue_observation_repository_validation(self) -> None:
        obs = {
            "schema_version": "relay-v3.1-parent-issue-observation",
            "authority": "DERIVED_PROVIDER_OBSERVATION",
            "provider": "GITHUB",
            "repository": "reallaksh19/Advanced_Analysis",
            "issue_number": 1771,
            "title": "C3-D",
            "url": "https://github.com/reallaksh19/Advanced_Analysis/issues/1771",
            "state": "OPEN",
            "observed_at": "2026-09-24T00:00:00Z",
            "baseline": None,
            "current_contract": {
                "body_digest": "sha256:" + ("a" * 64),
                "acceptance_items": [],
            },
            "disposition": "NO_CHANGE",
            "relationships": [
                {
                    "type": "RELATED_TO",
                    "target": {
                        "repository": "reallaksh19/Advanced_Analysis",
                        "issue_number": 1862,
                        "url": "https://github.com/reallaksh19/Advanced_Analysis/issues/1862",
                    },
                    "scope": ["s"],
                    "acceptance_items": ["a"],
                    "provider_refs": ["p"],
                }
            ],
            "handover_ledger": {
                "repository": "reallaksh19/Advanced_Analysis",
                "issue_number": 1882,
                "url": "https://github.com/reallaksh19/Advanced_Analysis/issues/1882",
            },
            "updates": [],
        }
        errors = validate_schema("parent-issue-observation", obs, "OBSERVATION")
        self.assertEqual([], errors)

        # Invalid repository
        obs["repository"] = "invalid repo with spaces"
        errors = validate_schema("parent-issue-observation", obs, "OBSERVATION")
        self.assertTrue(bool(errors))

    def test_handover_ledger_repository_validation(self) -> None:
        ledger = {
            "schema_version": "relay-v3.1-handover-ledger",
            "authority": "DERIVED_PROVIDER_PROJECTION",
            "generated_from": {
                "state_digest": "sha256:" + ("a" * 64),
                "task_snapshot_digest": "sha256:" + ("b" * 64),
                "roadmap_revision": "RM-0012",
            },
            "parent_issue": {
                "repository": "reallaksh19/Advanced_Analysis",
                "number": 1771,
                "title": "Parent",
                "url": "https://github.com/reallaksh19/Advanced_Analysis/issues/1771",
                "state": "OPEN",
                "disposition": "NO_CHANGE",
                "relationships": [],
            },
            "handover_issue": {
                "repository": "reallaksh19/Advanced_Analysis",
                "number": 1882,
                "url": "https://github.com/reallaksh19/Advanced_Analysis/issues/1882",
            },
            "current_frontier": {
                "ep": "EP-01",
                "work_package": "WP-01",
                "lease": "LEASE-01",
                "executor": "agent",
                "status": "ACTIVE",
                "continuation": "NEW",
            },
            "parent_progress": {
                "complete": 0,
                "partial": 0,
                "pending": 1,
                "blocked": 0,
                "deferred": 0,
                "not_applicable": 0,
                "unknown": 0,
                "total": 1,
            },
            "ep_index": [],
            "pending_items": [],
            "known_issues": [],
            "offloads": [],
            "accepted_truth": {},
            "material": {},
            "negative_knowledge": {},
            "accountability": {},
            "active_change": None,
            "delivery": {
                "issue": 1882,
                "pr": None,
                "lifecycle": "LOCAL_PROJECTION",
                "merge_authorized": False,
            },
            "records": [],
            "next": {
                "action": "action",
                "stop_conditions": [],
            },
        }
        errors = validate_schema("handover-ledger", ledger, "LEDGER")
        self.assertEqual([], errors)

        # Invalid parent_issue.repository
        ledger["parent_issue"]["repository"] = "invalid"
        errors = validate_schema("handover-ledger", ledger, "LEDGER")
        self.assertTrue(bool(errors))

    def test_handover_provider_status_repository_validation(self) -> None:
        status = {
            "schema_version": "relay-v3.1-handover-provider-status",
            "authority": "PROVIDER_READBACK",
            "observed_at": "2026-09-24T00:00:00Z",
            "marker": "relay-v3.1",
            "parent": {
                "repository": "reallaksh19/Advanced_Analysis",
                "issue_number": 1771,
                "url": "https://github.com/reallaksh19/Advanced_Analysis/issues/1771",
                "body_digest": "sha256:" + ("a" * 64),
                "updated": True,
            },
            "handover": {
                "repository": "reallaksh19/Advanced_Analysis",
                "issue_number": 1882,
                "url": "https://github.com/reallaksh19/Advanced_Analysis/issues/1882",
                "body_digest": "sha256:" + ("b" * 64),
                "updated": True,
            },
        }
        errors = validate_schema("handover-provider-status", status, "STATUS")
        self.assertEqual([], errors)

        status["parent"]["repository"] = "bad repo name"
        errors = validate_schema("handover-provider-status", status, "STATUS")
        self.assertTrue(bool(errors))


if __name__ == "__main__":
    unittest.main()
