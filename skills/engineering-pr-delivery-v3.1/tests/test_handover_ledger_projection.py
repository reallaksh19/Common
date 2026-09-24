from __future__ import annotations

import copy
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

from handover_ledger_projection import build, render_ledger, render_parent_summary
from test_relay_can import prepare_git
from test_v3_foundation import DIGEST, dump
from v3lib import load_yaml, validate_schema


def parent_observation() -> dict:
    return {
        "schema_version": "relay-v3.1-parent-issue-observation",
        "authority": "DERIVED_PROVIDER_OBSERVATION",
        "provider": "GITHUB",
        "repository": "example/repo",
        "issue_number": 1771,
        "title": "C3-D baseline",
        "url": "https://github.com/example/repo/issues/1771",
        "state": "OPEN",
        "observed_at": "2026-09-22T14:00:00Z",
        "baseline": {
            "observed_at": "2026-09-20T00:00:00Z",
            "body_digest": DIGEST,
            "acceptance_items": [
                {"id": "PI-1", "statement": "Baseline is proven."},
                {"id": "PI-2", "statement": "Follow-up is classified."},
            ],
        },
        "current_contract": {
            "body_digest": DIGEST,
            "acceptance_items": [
                {"id": "PI-1", "statement": "Baseline is proven.", "state": "COMPLETE", "evidence": ["CP-TA-008"], "provider_refs": ["issue-1771"]},
                {"id": "PI-2", "statement": "Follow-up is classified.", "state": "PENDING", "evidence": [], "provider_refs": ["issue-1771"]},
            ],
        },
        "updates": [],
        "disposition": "NO_CHANGE",
        "relationships": [],
        "handover_ledger": {
            "repository": "example/repo",
            "issue_number": 1870,
            "url": "https://github.com/example/repo/issues/1870",
        },
        "implementation_plan": {
            "state": "PRESENT",
            "provider_ref": "github:example/repo#1771/comment-10",
            "revision": 2,
            "digest": DIGEST,
            "observed_at": "2026-09-22T13:55:00Z",
        },
        "expected_next_observable": {
            "statement": "Focused validation result on the exact head.",
            "evidence": ["test result", "exact head"],
        },
        "task_publications": [
            {
                "type": "IMPLEMENTATION_PLAN",
                "ref": "github:example/repo#1771/comment-9",
                "observed_at": "2026-09-22T13:00:00Z",
                "summary": "Initial implementation plan.",
                "exact_head": None,
            },
            {
                "type": "PLAN_UPDATE",
                "ref": "github:example/repo#1771/comment-10",
                "observed_at": "2026-09-22T13:55:00Z",
                "summary": "Plan revised after source inspection.",
                "exact_head": None,
            },
        ],
    }


class HandoverLedgerProjectionTests(unittest.TestCase):
    def test_parent_ledger_indexes_ep_history_and_reuses_existing_tracking(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            current_path = root / "relay/WORK/EP-TA-011.yaml"
            current = load_yaml(current_path)
            current["parent_issue"] = {
                "provider": "GITHUB",
                "repository": "example/repo",
                "number": 1771,
                "title": "C3-D baseline",
                "url": "https://github.com/example/repo/issues/1771",
                "baseline": parent_observation()["baseline"],
            }
            current["offloads"] = [{
                "id": "OFFLOAD-LOCAL-001",
                "status": "RETURNED",
                "agent_type": "LOCAL_AGENT",
                "task": "Run exact-head baseline validation.",
                "allowed_writes": [],
                "expected_return": ["command results"],
                "trace_refs": ["LOCAL-EP-TA-011"],
            }]
            dump(current_path, current)

            abandoned = copy.deepcopy(current)
            abandoned["id"] = "EP-TA-009"
            abandoned["outcome"]["statement"] = "Unfinished predecessor work."
            dump(root / "relay/WORK/EP-TA-009.yaml", abandoned)
            old_lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            old_lease["id"] = "LEASE-TA-009-01"
            old_lease["basis"]["ep_id"] = "EP-TA-009"
            old_lease["state"] = "RELEASED"
            dump(root / "relay/LEASES/LEASE-TA-009-01.yaml", old_lease)

            complete = copy.deepcopy(current)
            complete["id"] = "EP-TA-008"
            complete["outcome"]["statement"] = "Completed predecessor work."
            dump(root / "relay/WORK/EP-TA-008.yaml", complete)
            cp = load_yaml(root / "relay/CHECKPOINTS/CP-TA-010.yaml")
            cp["id"] = "CP-TA-008"
            cp["ep"] = "EP-TA-008"
            dump(root / "relay/CHECKPOINTS/CP-TA-008.yaml", cp)

            controls_path = root / "relay/CONTROLS/controls.yaml"
            controls = load_yaml(controls_path)
            controls["controls"] = [
                {
                    "id": "CTRL.1771.1",
                    "kind": "DEPENDENCY",
                    "state": "OPEN",
                    "source": {"type": "REPOSITORY", "ref": "baseline"},
                    "condition": "Local baseline result must be consumed.",
                    "blocks": ["CHECKPOINT"],
                    "permits": ["READ"],
                    "tracking": {"kind": "PENDING", "id": "PEND.1771.1"},
                    "resolution": {"condition": "Result consumed.", "evidence": []},
                },
                {
                    "id": "CTRL.1771.2",
                    "kind": "DELIVERY",
                    "state": "OPEN",
                    "source": {"type": "PROVIDER", "ref": "actions-zero-steps"},
                    "condition": "Hosted Actions executes zero steps.",
                    "blocks": ["PR_READY"],
                    "permits": ["MATERIAL_WRITE"],
                    "tracking": {"kind": "KNOWN_ISSUE", "id": "KI.1771.1"},
                    "resolution": {"condition": "Hosted execution restored.", "evidence": []},
                },
            ]
            dump(controls_path, controls)

            ledger = build(root, parent_observation(), base_ref=base_ref)
            self.assertEqual("DERIVED_PROVIDER_PROJECTION", ledger["authority"])
            canonical_ledger = copy.deepcopy(ledger)
            canonical_ledger["parent_issue"]["repository"] = "reallaksh19/Common"
            canonical_ledger["handover_issue"]["repository"] = "reallaksh19/Common"
            canonical_ledger["ep_index"][0]["ep"] = "EP.1771.1"
            canonical_ledger["ep_index"][0]["work_package"] = "WP.1771"
            self.assertEqual(
                [],
                validate_schema("handover-ledger", canonical_ledger, "CANONICAL_HANDOVER_LEDGER"),
            )
            self.assertEqual(1870, ledger["handover_issue"]["number"])

            by_ep = {row["ep"]: row for row in ledger["ep_index"]}
            self.assertEqual("ACTIVE", by_ep["EP-TA-011"]["status"])
            self.assertEqual("RECOVERY_REQUIRED", by_ep["EP-TA-009"]["status"])
            self.assertEqual("COMPLETE", by_ep["EP-TA-008"]["status"])
            self.assertEqual("RECOVERY", by_ep["EP-TA-009"]["continuation"])
            self.assertEqual("NEW", by_ep["EP-TA-011"]["continuation"])
            self.assertEqual("PRESENT", by_ep["EP-TA-011"]["implementation_plan"]["state"])
            self.assertEqual(2, by_ep["EP-TA-011"]["implementation_plan"]["revision"])
            self.assertEqual(
                "Focused validation result on the exact head.",
                by_ep["EP-TA-011"]["expected_next_observable"]["statement"],
            )
            self.assertEqual(2, len(by_ep["EP-TA-011"]["latest_publications"]))

            self.assertEqual(["PEND.1771.1"], [row["id"] for row in ledger["pending_items"]])
            self.assertEqual(["KI.1771.1"], [row["id"] for row in ledger["known_issues"]])
            self.assertEqual("EP-TA-011", ledger["offloads"][0]["origin_ep"])

            body = render_ledger(ledger)
            parent = render_parent_summary(ledger)
            self.assertIn("## EP index", body)
            self.assertIn("EP-TA-009", body)
            self.assertIn("RECOVERY_REQUIRED", body)
            self.assertIn("PEND.1771.1", body)
            self.assertIn("KI.1771.1", body)
            self.assertIn("Handover ledger: example/repo#1870", parent)
            self.assertIn("Recovery-required EPs: 1", parent)

    def test_programme_ledger_can_root_at_parent_while_task_plan_lives_on_child_issue(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            current_path = root / "relay/WORK/EP-TA-011.yaml"
            current = load_yaml(current_path)
            current["programme_parent"] = {
                "provider": "GITHUB",
                "repository": "example/repo",
                "number": 1771,
                "title": "Programme root",
                "url": "https://github.com/example/repo/issues/1771",
            }
            current["parent_issue"] = {
                "provider": "GITHUB",
                "repository": "example/repo",
                "number": 1772,
                "title": "Focused child",
                "url": "https://github.com/example/repo/issues/1772",
                "baseline": {
                    "observed_at": "2026-09-20T00:00:00Z",
                    "body_digest": DIGEST,
                    "acceptance_items": [{"id": "CHILD-1", "statement": "Focused result is proved."}],
                },
            }
            dump(current_path, current)

            work = copy.deepcopy(parent_observation())
            work["issue_number"] = 1772
            work["title"] = "Focused child"
            work["url"] = "https://github.com/example/repo/issues/1772"
            work["handover_ledger"] = None
            work["baseline"] = current["parent_issue"]["baseline"]
            work["current_contract"] = {
                "body_digest": DIGEST,
                "acceptance_items": [
                    {
                        "id": "CHILD-1",
                        "statement": "Focused result is proved.",
                        "state": "PENDING",
                        "evidence": [],
                        "provider_refs": ["issue-1772"],
                    }
                ],
            }
            work["implementation_plan"]["provider_ref"] = "github:example/repo#1772/comment-20"
            work["implementation_plan"]["revision"] = 1
            work["task_publications"] = [
                {
                    "type": "IMPLEMENTATION_PLAN",
                    "ref": "github:example/repo#1772/comment-20",
                    "observed_at": "2026-09-22T13:55:00Z",
                    "summary": "Child implementation plan.",
                    "exact_head": None,
                }
            ]

            ledger = build(
                root,
                parent_observation(),
                base_ref=base_ref,
                work_issue_observation=work,
            )

            self.assertEqual(1771, ledger["parent_issue"]["number"])
            self.assertEqual(2, ledger["parent_progress"]["total"])
            row = next(item for item in ledger["ep_index"] if item["ep"] == "EP-TA-011")
            self.assertEqual(1772, row["work_issue"]["number"])
            self.assertEqual("PRESENT", row["implementation_plan"]["state"])
            self.assertEqual(1, row["implementation_plan"]["revision"])
            self.assertEqual(
                "github:example/repo#1772/comment-20",
                row["implementation_plan"]["provider_ref"],
            )


if __name__ == "__main__":
    unittest.main()
