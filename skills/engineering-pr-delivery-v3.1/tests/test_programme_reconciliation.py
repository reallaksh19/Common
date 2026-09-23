from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from programme_reconciliation import assess_boundary, build, require_boundary_ready
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

    def test_canonical_boundary_switches_handover_to_first_still_real_parent(self):
        parent = {"repository": "example/project", "number": 118}
        result = require_boundary_ready(
            assess_boundary(
                parent,
                [
                    observation(118, state="CLOSED", disposition="SUPERSEDE", acceptance_state="COMPLETE"),
                    observation(19, acceptance_state="DEFERRED"),
                    observation(174, acceptance_state="PENDING"),
                ],
                boundary="HANDOVER",
            )
        )
        self.assertEqual("READY", result["status"])
        self.assertEqual("SUPERSEDED", result["selected_ownership"])
        self.assertEqual("SWITCH_FRONTIER", result["continuation"])
        self.assertEqual("example/project#174", result["next_frontier"])

    def test_next_work_uses_same_ordered_frontier_decision_as_handover(self):
        parent = {"repository": "example/project", "number": 118}
        observations = [
            observation(118, state="CLOSED", disposition="CLOSE", acceptance_state="COMPLETE"),
            observation(174, acceptance_state="PENDING"),
            observation(175, acceptance_state="PENDING"),
        ]
        handover = require_boundary_ready(
            assess_boundary(parent, observations, boundary="HANDOVER")
        )
        next_work = require_boundary_ready(
            assess_boundary(parent, observations, boundary="NEXT_WORK")
        )
        self.assertEqual(handover["reconciliation"], next_work["reconciliation"])
        self.assertEqual("example/project#174", next_work["next_frontier"])
        self.assertEqual("SWITCH_FRONTIER", next_work["continuation"])

    def test_recovery_and_admission_require_selected_parent_itself_to_be_frontier(self):
        parent = {"repository": "example/project", "number": 118}
        observations = [
            observation(118, state="CLOSED", disposition="CLOSE", acceptance_state="COMPLETE"),
            observation(174, acceptance_state="PENDING"),
        ]
        for boundary in ("RECOVERY_TAKEOVER", "ADMIT_TASK"):
            result = assess_boundary(parent, observations, boundary=boundary)
            self.assertEqual("PROGRAMME_FRONTIER_MISMATCH", result["status"])
            self.assertEqual("example/project#174", result["next_frontier"])
            with self.assertRaisesRegex(RuntimeError, "PROGRAMME_FRONTIER_MISMATCH"):
                require_boundary_ready(result)

    def test_single_parent_handover_requires_current_provider_truth(self):
        parent = {"repository": "example/project", "number": 118}
        missing = assess_boundary(parent, None, boundary="HANDOVER")
        self.assertEqual("PROGRAMME_CURRENTNESS_REQUIRED", missing["status"])

        unknown = observation(118)
        unknown["disposition"] = "UNKNOWN"
        result = assess_boundary(
            parent,
            None,
            boundary="HANDOVER",
            current_observation=unknown,
        )
        self.assertEqual("PROGRAMME_CURRENTNESS_REQUIRED", result["status"])
        self.assertIn("PARENT_DISPOSITION_REQUIRED", result["reason_codes"])

    def test_single_parent_terminal_handover_requires_programme_reconciliation(self):
        parent = {"repository": "example/project", "number": 118}
        completed = observation(
            118,
            state="CLOSED",
            disposition="CLOSE",
            acceptance_state="COMPLETE",
        )

        result = assess_boundary(
            parent,
            None,
            boundary="HANDOVER",
            current_observation=completed,
        )
        self.assertEqual("PROGRAMME_RECONCILIATION_REQUIRED", result["status"])
        self.assertEqual("LANDED", result["selected_ownership"])
        with self.assertRaisesRegex(RuntimeError, "PROGRAMME_RECONCILIATION_REQUIRED"):
            require_boundary_ready(result)

    def test_wrc_style_owner_selection_displaces_unfinished_stale_current_programme(self):
        current_parent = {"repository": "example/project", "number": 1771}
        observations = [
            observation(1771, acceptance_state="PENDING"),
            observation(1775, acceptance_state="PENDING"),
        ]

        result = require_boundary_ready(
            assess_boundary(
                current_parent,
                observations,
                boundary="NEXT_WORK",
                selected_frontier_ref="example/project#1775",
            )
        )

        self.assertEqual("STILL_REAL", result["selected_ownership"])
        self.assertEqual("example/project#1775", result["selected_programme_frontier"])
        self.assertEqual("example/project#1775", result["executable_frontier"])
        self.assertEqual("SWITCH_FRONTIER", result["continuation"])
        self.assertIn(
            "example/project#1771",
            result["reconciliation"]["alternate_live_frontiers"],
        )

    def test_pdfhub_style_blocked_selected_frontier_does_not_laterally_jump(self):
        current_parent = {"repository": "example/project", "number": 288}
        observations = [
            observation(284, acceptance_state="PENDING"),
            observation(286, acceptance_state="DEFERRED"),
            observation(288, acceptance_state="BLOCKED"),
        ]

        result = require_boundary_ready(
            assess_boundary(
                current_parent,
                observations,
                boundary="NEXT_WORK",
                selected_frontier_ref="example/project#288",
            )
        )

        self.assertEqual("READY", result["status"])
        self.assertEqual("BLOCKED", result["selected_programme_ownership"])
        self.assertEqual("BLOCKED_SELECTED_FRONTIER", result["continuation"])
        self.assertEqual("example/project#288", result["next_frontier"])
        self.assertIsNone(result["executable_frontier"])
        self.assertIn(
            "example/project#284",
            result["reconciliation"]["alternate_live_frontiers"],
        )

    def test_blocked_current_frontier_is_implicitly_sticky_without_owner_reselection(self):
        current_parent = {"repository": "example/project", "number": 288}
        observations = [
            observation(284, acceptance_state="PENDING"),
            observation(288, acceptance_state="BLOCKED"),
        ]

        result = require_boundary_ready(
            assess_boundary(
                current_parent,
                observations,
                boundary="NEXT_WORK",
            )
        )

        self.assertEqual("example/project#288", result["selected_programme_frontier"])
        self.assertEqual("BLOCKED_SELECTED_FRONTIER", result["continuation"])
        self.assertIsNone(result["executable_frontier"])

    def test_ambiguous_idle_admission_requires_explicit_programme_selection(self):
        proposed_parent = {"repository": "example/project", "number": 1775}
        observations = [
            observation(1771, acceptance_state="PENDING"),
            observation(1775, acceptance_state="PENDING"),
        ]

        result = assess_boundary(
            proposed_parent,
            observations,
            boundary="ADMIT_TASK",
        )
        self.assertEqual("PROGRAMME_SELECTION_REQUIRED", result["status"])
        with self.assertRaisesRegex(RuntimeError, "PROGRAMME_SELECTION_REQUIRED"):
            require_boundary_ready(result)

        selected = require_boundary_ready(
            assess_boundary(
                proposed_parent,
                observations,
                boundary="ADMIT_TASK",
                selected_frontier_ref="example/project#1775",
            )
        )
        self.assertEqual("example/project#1775", selected["executable_frontier"])
        self.assertEqual("CONTINUE_CURRENT", selected["continuation"])

    def test_recovery_cannot_resurrect_old_programme_after_owner_selection_moves(self):
        old_parent = {"repository": "example/project", "number": 1771}
        observations = [
            observation(1771, acceptance_state="PENDING"),
            observation(1775, acceptance_state="PENDING"),
        ]

        result = assess_boundary(
            old_parent,
            observations,
            boundary="RECOVERY_TAKEOVER",
            selected_frontier_ref="example/project#1775",
        )
        self.assertEqual("PROGRAMME_FRONTIER_MISMATCH", result["status"])
        self.assertEqual("example/project#1775", result["executable_frontier"])

    def test_blocked_parent_is_not_promoted_to_programme_frontier(self):
        result = build([
            observation(200, acceptance_state="BLOCKED"),
            observation(201, acceptance_state="PENDING"),
        ])
        self.assertEqual(["example/project#200"], result["execution_blocked"])
        self.assertEqual(["example/project#201"], result["programme_frontier"])


if __name__ == "__main__":
    unittest.main()
