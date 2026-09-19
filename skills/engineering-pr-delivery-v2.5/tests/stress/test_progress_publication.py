from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
sys.path.insert(0, str(HERE.parents[1]))

from test_core import good, dump
from report_projection import build as build_report
from owner_publication import classify_change


class ProgressPublicationStressTests(unittest.TestCase):
    def test_unchanged_report_is_no_material_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            good(root)
            before = build_report(root)
            after = build_report(root)
            result = classify_change(before, after)
            self.assertEqual("NO_MATERIAL_PROGRESS", result["event_class"])
            self.assertFalse(result["publication_due"])

    def test_takeover_only_change_is_not_task_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, _, _, state = good(root)
            before = build_report(root)
            state["takeover_admissions"] = [
                {
                    "route_key": "SERIAL:EP-1",
                    "candidate": {"agent_instance_id": "agent-B"},
                    "discovery_receipt": {"id": "DISC-1", "path": "agents/relay/discovery/DISC-1.yaml"},
                    "certification": {"id": "TC-1", "path": "agents/relay/takeover/TC-1.yaml"},
                }
            ]
            dump(root / "agents/relay/REPO_STATE.yaml", state)
            result = classify_change(before, build_report(root))
            self.assertEqual("DELIVERY_OR_CUSTODY_PROGRESS", result["event_class"])
            self.assertNotIn("task", result["changed_dimensions"])

    def test_not_run_evidence_change_is_evidence_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, _, _, state = good(root)
            before = build_report(root)
            state["status_planes"]["evidence"] = {
                "state": "NOT_RUN",
                "summary": "A required repository check cannot execute here.",
                "not_run": [
                    {
                        "id": "TEST-1",
                        "reason": "The current environment has no usable Git object database.",
                        "cause": "UNAVAILABLE_TOOL",
                    }
                ],
            }
            dump(root / "agents/relay/REPO_STATE.yaml", state)
            result = classify_change(before, build_report(root))
            self.assertEqual("EVIDENCE_PROGRESS", result["event_class"])
            self.assertIn("evidence", result["changed_dimensions"])

    def test_accepted_progress_has_priority_over_other_activity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, _, progress, _ = good(root)
            before = build_report(root)
            progress["acceptance_criteria"][0].update(
                {"status": "COMPLETE", "earned_weight": 100, "percent": 100}
            )
            progress["implementation_steps"][0].update({"earned_weight": 100, "percent": 100})
            progress["execution_packages"][0].update({"earned_weight": 100, "percent": 100})
            progress["work_packages"][0].update({"earned_weight": 100, "percent": 100})
            progress["phases"][0].update({"earned_weight": 100, "percent": 100})
            progress["objectives"][0].update({"earned_weight": 100, "percent": 100})
            progress["overall"].update({"earned_weight": 100, "percent": 100})
            dump(root / "agents/relay/roadmap/PROGRESS.yaml", progress)
            result = classify_change(before, build_report(root))
            self.assertEqual("TASK_PROGRESS", result["event_class"])
            self.assertIn("task", result["changed_dimensions"])

    def test_files_changed_without_acceptance_is_implementation_change(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, _, _, state = good(root)
            before = build_report(root)
            cp = {
                "schema_version": "relay-v2.5",
                "checkpoint_id": "CP-1",
                "ep_id": "EP-1",
                "roadmap_basis": {"roadmap_id": "RM-T", "revision": "RM-0001"},
                "execution_basis": {"material_ref": "abc"},
                "implementation_result": {
                    "summary": "Implementation changed but acceptance has not advanced.",
                    "completed_steps": [],
                    "files_changed": ["src/a.py"],
                },
                "acceptance_results": [],
                "validation_results": [],
                "quality_findings": [],
                "known_limitations": [],
                "discoveries": [],
                "roadmap_reconciliation": {
                    "result": "NO_ROADMAP_CHANGE",
                    "status_updates": [],
                    "proposals": [],
                    "owner_decisions_required": [],
                },
                "remaining_work": [],
                "successor": {
                    "mode": "SERIAL",
                    "frontier_work_package": "WP-1",
                    "ep_id": "EP-1",
                    "parallel_plan": None,
                    "lane_id": None,
                    "lanes": [],
                },
            }
            dump(root / "agents/relay/checkpoints/CP-1.yaml", cp)
            state["last_checkpoint"] = {"id": "CP-1", "path": "agents/relay/checkpoints/CP-1.yaml"}
            dump(root / "agents/relay/REPO_STATE.yaml", state)
            result = classify_change(before, build_report(root))
            self.assertEqual("IMPLEMENTATION_CHANGE", result["event_class"])
            self.assertNotIn("task", result["changed_dimensions"])

    def test_transition_to_waiting_is_not_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, _, _, state = good(root)
            before = build_report(root)
            state["status_planes"]["execution"] = {
                "state": "WAITING",
                "can_continue": False,
                "material_authority": "READ_ONLY",
                "next_action": "Wait for the required external repository check.",
            }
            dump(root / "agents/relay/REPO_STATE.yaml", state)
            result = classify_change(before, build_report(root))
            self.assertEqual("WAITING_OR_MONITORING", result["event_class"])
            self.assertIn("waiting_or_monitoring", result["changed_dimensions"])


if __name__ == "__main__":
    unittest.main()
