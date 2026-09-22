from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
V25_SCRIPTS = ROOT.parent / "engineering-pr-delivery-v2.5" / "scripts"
for entry in (SCRIPTS, TESTS, V25_SCRIPTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from intelligence_projection import assess_continuity, build_improvement, build_task
from test_v25_migration import init_legacy_repo
from v25_migration import bootstrap, legacy_inventory
from v3lib import load_yaml


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def prepare_active_legacy(root: Path, *, files_changed: bool = True) -> None:
    init_legacy_repo(root)
    state_path = root / "agents/relay/REPO_STATE.yaml"
    roadmap_path = root / "agents/relay/roadmap/OVERALL_ROADMAP.yaml"
    progress_path = root / "agents/relay/roadmap/PROGRESS.yaml"
    state = load_yaml(state_path)
    roadmap = load_yaml(roadmap_path)
    progress = load_yaml(progress_path)

    objective = roadmap["objectives"][0]
    phase = objective["phases"][0]
    wp = phase["work_packages"][0]
    oid, pid, wid = objective["id"], phase["id"], wp["id"]
    phase.update({"state": "ACTIVE", "definition": "DETAILED"})
    wp.update({"state": "ACTIVE", "definition": "DETAILED", "execution_status": "ACTIVE"})
    dump(roadmap_path, roadmap)

    base = git(root, "rev-parse", "HEAD")
    ep = {
        "schema_version": "relay-v2.5",
        "identity": {
            "ep_id": "EP-CONT-001",
            "branch": "main",
            "base_ref": base,
            "execution_state": "EXECUTABLE",
            "previous_checkpoint": None,
            "previous_join": None,
            "previous_replan": None,
        },
        "git_basis": {
            "expected_branch": "main",
            "material_ref": base,
            "base_branch": "main",
            "base_observed_ref": base,
            "drift_policy": "RECHECK_BEFORE_WRITE",
            "drift_receipt": None,
        },
        "roadmap_source": {
            "roadmap_id": state["roadmap"]["id"],
            "roadmap_revision": state["roadmap"]["revision"],
            "objective": oid,
            "phase": pid,
            "work_package": wid,
            "generated_from_frontier": True,
            "task_admission": {
                "disposition": "MAPPED_EXISTING_WP",
                "searched_paths": ["agents/relay/roadmap/OVERALL_ROADMAP.yaml"],
                "basis": ["Existing WP owns the continuity task."],
            },
        },
        "outcome": {
            "user_visible": ["A successor can read one task-local snapshot."],
            "engineering": ["Preserve V2.5 intelligence as generated read models."],
        },
        "context_capsule": {
            "product_goal": "Preserve roadmap intelligence.",
            "roadmap_position": wid,
            "why_this_work_exists": "Cutover must not retire V2.5 roadmap/event/checkpoint intelligence.",
            "current_architecture": "V2.5 remains live while V3 is staged.",
        },
        "repository_discovery": [{
            "id": "DSTEP-CONT-001",
            "action": "VERIFY",
            "targets": ["agents/relay/REPO_STATE.yaml"],
            "question": "Which V2.5 objects own current task truth?",
            "expected_outputs": ["roadmap", "progress", "events", "checkpoint"],
            "receipt_required": True,
            "on_failure": "Stop migration.",
        }],
        "inputs": [{
            "id": "INPUT-CONT-001",
            "name": "Legacy authority",
            "description": "Current V2.5 state and roadmap.",
            "authority": "V2.5",
            "source": "agents/relay/REPO_STATE.yaml",
            "type": "AUTHORITY",
            "units": "NA",
            "editable": False,
            "applicability": "CURRENT_EP_REQUIRED",
            "resolution": "READY",
            "value": "current",
            "consumers": ["STEP-CONT-001"],
            "validation": ["State exists."],
            "stale_if": ["Roadmap changes."],
        }],
        "benchmarks": [{
            "id": "BENCH-CONT-001",
            "name": "Continuity witness",
            "purpose": "Prove accepted evidence remains visible.",
            "source": "synthetic fixture",
            "independence": "Fixture is independent from projection implementation.",
            "oracle_class": "FROZEN_GOLDEN",
            "applicability": "CURRENT_EP_REQUIRED",
            "resolution": "READY",
            "payload": {"case": "accepted evidence"},
            "expected": "visible",
            "tolerance": None,
            "verifies": ["AC-CONT-001"],
            "stale_if": ["Authority contract changes."],
        }],
        "scope": {
            "allowed": [{"path": "src/continuity.py", "reason": "Synthetic product path"}],
            "allowed_reads": [{"path": "agents/relay/", "reason": "Authority source"}],
            "protected": [{"invariant": "Legacy authority remains unchanged", "reason": "Migration safety"}],
            "prohibited": [{"domain": "duplicate authority", "reason": "Views must remain derived"}],
            "owner_reserved": [],
        },
        "anti_drift": {"do_not": [], "stale_if": []},
        "implementation_plan": [{
            "id": "STEP-CONT-001",
            "objective": "Generate continuity projections.",
            "targets": ["src/continuity.py"],
            "reads": ["agents/relay/"],
            "writes": ["src/continuity.py"],
            "inputs": ["INPUT-CONT-001"],
            "acceptance": ["AC-CONT-001"],
            "tests": ["TEST-CONT-001"],
            "expected_state": "Derived views expose current task truth.",
            "stop_conditions": ["Legacy authority mutates."],
        }],
        "next_work": {
            "phase_transition": False,
            "steps": [{
                "order": 1,
                "action": "Generate derived continuity views.",
                "targets": ["src/continuity.py"],
                "inputs": ["INPUT-CONT-001"],
                "tests": ["TEST-CONT-001"],
                "benchmarks": ["BENCH-CONT-001"],
                "acceptance": ["AC-CONT-001"],
                "expected_result": "Continuity views validate.",
                "stop_if": ["Legacy digest changes."],
            }],
        },
        "acceptance": [{
            "id": "AC-CONT-001",
            "weight": 100,
            "description": "Continuity projections remain derived and evidence-bound.",
            "verification": ["TEST-CONT-001", "BENCH-CONT-001"],
        }],
        "validation": [{
            "id": "TEST-CONT-001",
            "obligation_class": "MUST_PASS",
            "method": "Synthetic continuity scenario.",
            "proves": ["AC-CONT-001"],
            "class": "MUST_PASS",
        }],
        "qualification_boundary": {"required": False},
    }
    dump(root / "agents/relay/execution-packages/EP-CONT-001.yaml", ep)

    cp = {
        "schema_version": "relay-v2.5",
        "contract_version": 2,
        "checkpoint_id": "CP-CONT-001",
        "ep_id": "EP-CONT-001",
        "roadmap_basis": {"roadmap_id": state["roadmap"]["id"], "revision": state["roadmap"]["revision"]},
        "execution_basis": {"material_ref": base},
        "implementation_result": {
            "summary": "Continuity evidence accepted.",
            "completed_steps": ["STEP-CONT-001"],
            "files_changed": ["src/continuity.py"] if files_changed else [],
        },
        "acceptance_results": [{"id": "AC-CONT-001", "status": "PASS"}],
        "validation_results": [{"id": "TEST-CONT-001", "status": "PASS", "basis_ref": base}],
        "quality_findings": [],
        "known_limitations": [],
        "discoveries": ["Task-local projection preserves roadmap/event context."],
        "roadmap_reconciliation": {
            "result": "STATUS_UPDATE",
            "status_updates": [],
            "proposals": [],
            "owner_decisions_required": [],
        },
        "remaining_work": [],
        "successor": {
            "mode": "NONE",
            "frontier_work_package": None,
            "ep_id": None,
            "parallel_plan": None,
            "lane_id": None,
            "lanes": [],
        },
    }
    dump(root / "agents/relay/checkpoints/CP-CONT-001.yaml", cp)

    dump(root / "agents/relay/roadmap/ROADMAP_EVENTS.yaml", {
        "schema_version": "relay-v2.5-roadmap-events",
        "ledger_revision": 1,
        "events": [{
            "id": "EVT-CONT-001",
            "sequence": 1,
            "event_class": "ENGINEERING_DISCOVERY",
            "summary": "Rejected duplicate authoritative task ledger; keep projections derived.",
            "concept_refs": [oid, pid],
            "execution_refs": {
                "work_package": wid,
                "execution_package": "EP-CONT-001",
                "checkpoint": "CP-CONT-001",
                "issue": None,
                "pull_request": None,
            },
            "basis": ["CP-CONT-001"],
            "concept_change": "NO_CONCEPT_CHANGE",
            "roadmap_revision": {"id": state["roadmap"]["revision"], "path": None},
            "follow_up": "NONE",
        }],
    })

    state["relay_state"] = "ACTIVE"
    state["active_ep"] = {
        "id": "EP-CONT-001",
        "path": "agents/relay/execution-packages/EP-CONT-001.yaml",
        "state": "EXECUTABLE",
        "continuity_receipt": None,
    }
    state["last_checkpoint"] = {"id": "CP-CONT-001", "path": "agents/relay/checkpoints/CP-CONT-001.yaml"}
    state["current_position"] = {"objective": oid, "phase": pid, "work_package": wid, "work_packages": []}
    state["status_planes"]["execution"] = {
        "state": "READY",
        "can_continue": True,
        "material_authority": "WRITE",
        "next_action": "Generate continuity projections.",
    }
    state["progress"] = {
        "overall_percent": 100,
        "phase_percent": 100,
        "ep_percent": 100,
        "basis_revision": "PB-CONT",
    }
    dump(state_path, state)

    progress["progress_basis"] = {"id": "PB-CONT", "roadmap_revision": state["roadmap"]["revision"]}
    progress["overall"] = {"earned_weight": 1, "total_weight": 1, "percent": 100}
    for group in ("objectives", "phases", "work_packages"):
        progress[group][0].update({"earned_weight": 1, "total_weight": 1, "percent": 100})
    progress["execution_packages"] = [{"id": "EP-CONT-001", "earned_weight": 100, "total_weight": 100, "percent": 100}]
    progress["implementation_steps"] = [{"id": "STEP-CONT-001", "ep_id": "EP-CONT-001", "earned_weight": 100, "total_weight": 100, "percent": 100}]
    progress["acceptance_criteria"] = [{
        "id": "AC-CONT-001",
        "ep_id": "EP-CONT-001",
        "status": "COMPLETE",
        "basis": ["CP-CONT-001"],
        "earned_weight": 100,
        "total_weight": 100,
        "percent": 100,
    }]
    dump(progress_path, progress)

    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "continuity fixture"], check=True, stdout=subprocess.PIPE)


def stage_v3(root: Path) -> None:
    result = bootstrap(
        root,
        tx_id="TX-MIGRATE-CONT-001",
        event_id="EVT-MIGRATE-CONT-001",
        actor="migration-agent",
        owner_outcome="Preserve engineering continuity.",
        current_goal="Project V2.5 task intelligence without duplicate authority.",
    )
    if result["status"] != "COMMITTED":
        raise AssertionError(result)


class IntelligenceProjectionTests(unittest.TestCase):
    def test_task_snapshot_is_scoped_derived_and_preserves_negative_knowledge(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_active_legacy(root)
            stage_v3(root)
            task = build_task(root)
            self.assertEqual("DERIVED_READ_MODEL", task["authority"])
            self.assertEqual("V2_5", task["source_protocol"])
            self.assertEqual("EP-CONT-001", task["identity"]["ep"])
            self.assertEqual("MAPPED_EXISTING_WP", task["lineage"]["roadmap_admission"]["disposition"])
            self.assertEqual(["src/continuity.py"], task["scope"]["write"])
            self.assertEqual("EVT-CONT-001", task["history"]["recent_events"][0]["id"])
            self.assertEqual("REJECTED", task["negative_knowledge"][0]["result"])

    def test_evidence_only_checkpoint_does_not_fake_capability_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_active_legacy(root, files_changed=False)
            stage_v3(root)
            view = build_improvement(root)
            self.assertEqual([], view["improvement"]["capability_added"])
            self.assertEqual([], view["improvement"]["capability_strengthened"])
            self.assertTrue(view["improvement"]["evidence_added"])
            self.assertTrue(view["not_improved"])

    def test_accepted_material_change_can_be_reported_as_strengthened_capability(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_active_legacy(root)
            stage_v3(root)
            view = build_improvement(root)
            self.assertEqual(["Continuity evidence accepted."], view["improvement"]["capability_strengthened"])
            self.assertIn("Task-local projection preserves roadmap/event context.", view["improvement"]["understanding_improved"])

    def test_continuity_assessment_passes_without_mutating_legacy_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_active_legacy(root)
            stage_v3(root)
            _, before = legacy_inventory(root)
            result = assess_continuity(root)
            _, after = legacy_inventory(root)
            self.assertTrue(result["ready"], result)
            self.assertEqual(before, after)
            self.assertTrue(all(value == "PASS" for value in result["checks"].values()))

    def test_prepared_selector_keeps_v25_as_projection_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_active_legacy(root)
            stage_v3(root)
            selection = load_yaml(root / "relay/PROTOCOL_SELECTION.yaml")
            self.assertEqual("V2_5", selection["selected_protocol"])
            self.assertEqual("V2_5", build_task(root)["source_protocol"])


if __name__ == "__main__":
    unittest.main()
