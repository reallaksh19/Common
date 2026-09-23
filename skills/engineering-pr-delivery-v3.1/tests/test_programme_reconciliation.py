from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from programme_reconciliation import build
from test_v3_foundation import DIGEST


def observation(
    number: int,
    *,
    state: str = "OPEN",
    disposition: str = "NO_CHANGE",
    acceptance_state: str = "PENDING",
    relationships: list[dict] | None = None,
) -> dict:
    return {
        "schema_version": "relay-v3.1-parent-issue-observation",
        "authority": "DERIVED_PROVIDER_OBSERVATION",
        "provider": "GITHUB",
        "repository": "example/project",
        "issue_number": number,
        "title": f"Programme parent {number}",
        "url": f"https://github.com/example/project/issues/{number}",
        "state": state,
        "observed_at": "2026-09-23T00:30:00Z",
        "baseline": {
            "observed_at": "2026-09-22T00:00:00Z",
            "body_digest": DIGEST,
            "acceptance_items": [{"id": f"PI-{number}", "statement": f"Parent {number} outcome"}],
        },
        "current_contract": {
            "body_digest": DIGEST,
            "acceptance_items": [{
                "id": f"PI-{number}",
                "statement": f"Parent {number} outcome",
                "state": acceptance_state,
                "evidence": ["provider-readback"] if acceptance_state == "COMPLETE" else [],
                "provider_refs": [f"issue-{number}"],
            }],
        },
        "updates": [],
        "disposition": disposition,
        "relationships": list(relationships or []),
        "handover_ledger": None,
    }


class ProgrammeReconciliationTests(unittest.TestCase):
    def test_parent_set_separates_terminal_deferred_and_real_frontier(self):
        result = build([
            observation(118, state="CLOSED", disposition="SUPERSEDE", acceptance_state="COMPLETE"),
            observation(19, state="OPEN", disposition="NO_CHANGE", acceptance_state="DEFERRED"),
            observation(174, state="OPEN", disposition="NO_CHANGE", acceptance_state="PENDING"),
        ])

        self.assertEqual("READY", result["status"])
        self.assertEqual(
            [
                {"order": 1, "ref": "example/project#118", "ownership": "SUPERSEDED"},
                {"order": 2, "ref": "example/project#19", "ownership": "DEFERRED"},
                {"order": 3, "ref": "example/project#174", "ownership": "STILL_REAL"},
            ],
            result["ordered_roadmap"],
        )
        self.assertEqual(["example/project#174"], result["programme_frontier"])
        self.assertEqual(["example/project#19"], result["deferred_or_future"])
        self.assertEqual([], result["execution_blocked"])

    def test_current_parent_must_be_present_in_reconciled_parent_set(self):
        result = build(
            [observation(174)],
            current_parent_ref="example/project#118",
        )
        self.assertEqual("RECONCILIATION_REQUIRED", result["status"])
        self.assertIn("CURRENT_PARENT_MISSING:example/project#118", result["reason_codes"])

    def test_lineage_target_must_be_observed(self):
        relationship = {
            "type": "TRANSFERS_TO",
            "target": {
                "repository": "example/project",
                "issue_number": 175,
                "url": "https://github.com/example/project/issues/175",
            },
            "scope": ["unfinished obligation"],
            "acceptance_items": ["PI-174"],
            "provider_refs": ["issue-175"],
        }
        result = build([
            observation(
                174,
                state="OPEN",
                disposition="TRANSFER",
                acceptance_state="PENDING",
                relationships=[relationship],
            )
        ])
        self.assertEqual("RECONCILIATION_REQUIRED", result["status"])
        self.assertIn("LINEAGE_TARGET_UNOBSERVED:example/project#175", result["reason_codes"])

    def test_blocked_parent_is_not_promoted_to_programme_frontier(self):
        result = build([
            observation(200, acceptance_state="BLOCKED"),
            observation(201, acceptance_state="PENDING"),
        ])
        self.assertEqual(["example/project#200"], result["execution_blocked"])
        self.assertEqual(["example/project#201"], result["programme_frontier"])


if __name__ == "__main__":
    unittest.main()
