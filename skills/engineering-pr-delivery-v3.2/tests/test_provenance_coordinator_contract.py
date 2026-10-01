from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve()
V31 = HERE.parents[1]
SKILLS = V31.parent
COORDINATOR = SKILLS / "engineering-programme-coordinator"
ISSUE_AUTHORING = SKILLS / "engineering-github-issue-authoring"


class ProvenanceCoordinatorContractTests(unittest.TestCase):
    def test_coordinator_handover_schema_accepts_reference_only_provenance(self):
        schema = yaml.safe_load(
            (COORDINATOR / "schemas/relay-handover.schema.yaml").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        value = {
            "schema_version": "engineering-coordinator-relay-handover-v1",
            "authority": "DURABLE_OPERATIONAL_LEDGER",
            "programme_ref": "github:owner/repo#100",
            "observed_at": "2026-09-28T10:00:00Z",
            "basis_revision": "PB-0002",
            "observed_main": "a" * 40,
            "reconstruction": {
                "original_intent_ref": "github:owner/repo#101",
                "latest_programme_reconciliation_ref": "github:owner/repo#100/comment-9",
                "roadmap_refs": ["RM-100", "ROADMAP_RECONCILED:EVT-9"],
            },
            "workstreams": [
                {
                    "id": "A",
                    "issue_ref": "github:owner/repo#110",
                    "agent_ref": "agent-a",
                    "plan": {
                        "state": "PRESENT",
                        "ref": "github:owner/repo#110/comment-plan",
                        "revision": 2,
                        "responsibility_basis_ref": "github:owner/repo#110",
                        "responsibility_basis_digest": "sha256:" + ("b" * 64),
                    },
                    "provider_issue_state": "OPEN",
                    "branch": "issue-110",
                    "pr": "#120",
                    "base": "base-sha",
                    "exact_head": "head-sha",
                    "task_snapshot_ref": "relay/GENERATED/tasks/EP.110.1.snapshot.yaml",
                    "reconstruction": {
                        "latest_reconciliation_ref": "github:owner/repo#110/comment-reconcile",
                        "primary_conversation_refs": ["github:owner/repo#110/comment-context"],
                        "local_agent_refs": ["github:owner/repo#115"],
                        "rll_refs": ["github:owner/repo#110/comment-rll-state"],
                    },
                    "expected_next_observable": "Exact-head certification result.",
                    "latest_evidence": ["github:owner/repo#120"],
                    "next_consequence": "Route proven output to consumer B.",
                }
            ],
            "dependencies": [],
            "nonterminal_prs": [],
            "pending_items": [],
            "known_issues": [],
            "negative_knowledge": [],
            "recent_handoffs": [],
            "local_coordination": [],
            "owner_decisions_needed": [],
            "next_coordinator_action": "Observe exact-head certification.",
            "next_observation": {
                "reason": "Certification is the next meaningful observable.",
                "expected_evidence": ["test result", "exact head"],
            },
        }
        errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.path))
        self.assertEqual([], [error.message for error in errors])

    def test_issue_authoring_self_test_accepts_original_intent_role(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ISSUE_AUTHORING / "scripts/self_test_issue_workorder.py"),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: original intent source", result.stdout)


if __name__ == "__main__":
    unittest.main()
