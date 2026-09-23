from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from material_basis import inspect as inspect_material_basis
from plan_handover import plan_handover
from relay_tx import (
    accept_checkpoint,
    activate_lease,
    admit_task,
    close_task,
    export_local_execution,
    publish_handover,
    release_lease,
    renew_lease,
    reconcile_roadmap,
    resolve_control,
    sync_delivery,
)
from snapshot_projection import build as build_snapshot
from test_handover_context import (
    install_parent_issue,
    install_standalone,
    parent_issue_observation,
    target_observation,
)
from test_relay_can import prepare_git
from test_v3_foundation import base_objects, dump
from transactionlib import TransactionError, execute, yaml_bytes
from v3lib import load_events, load_yaml
from validate_foundation import validate, validate_authority


def add_open_control(root: Path) -> None:
    path = root / "relay/CONTROLS/controls.yaml"
    controls = yaml.safe_load(path.read_text(encoding="utf-8"))
    controls["controls"].append({
        "id": "CTRL-TEST-001",
        "kind": "DELIVERY",
        "state": "OPEN",
        "source": {"type": "VALIDATOR", "ref": "synthetic"},
        "condition": "Synthetic delivery obligation.",
        "blocks": ["PR_READY"],
        "permits": ["MATERIAL_WRITE"],
        "resolution": {"condition": "Evidence supplied.", "evidence": []},
    })
    dump(path, controls)


def accept_current_checkpoint_and_reconcile(root: Path, base_ref: str) -> None:
    _, _, _, _, template, *_ = base_objects()
    checkpoint = copy.deepcopy(template)
    checkpoint["id"] = "CP-TA-011"
    checkpoint["ep"] = "EP-TA-011"
    ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
    current_material = inspect_material_basis(root, ep, base_ref)["material_basis"]
    checkpoint["material_result"] = {
        "head": current_material["head"],
        "relevant_paths_digest": current_material["relevant_paths_digest"],
        "dependency_digest": current_material["dependency_digest"],
    }
    incoming = root / "close-checkpoint.yaml"
    dump(incoming, checkpoint)
    accept_checkpoint(
        root,
        tx_id="TX-CLOSE-CP",
        event_id="EVT-CLOSE-CP",
        actor="agent-x",
        checkpoint_path=incoming,
        base_ref=base_ref,
    )

    state = load_yaml(root / "relay/STATE.yaml")
    roadmap_path = root / str((state.get("roadmap") or {}).get("path"))
    roadmap = load_yaml(roadmap_path)
    reconciliation = {
        "schema_version": "relay-v3.1-roadmap-reconciliation",
        "authority": "PROPOSED_RECONCILIATION",
        "expected_revision": roadmap["revision"],
        "disposition": "NO_CHANGE",
        "basis": ["Current EP acceptance is complete; no concept change is required."],
        "roadmap_after": roadmap,
    }
    reconciliation_path = root / "close-roadmap-reconciliation.yaml"
    dump(reconciliation_path, reconciliation)
    reconcile_roadmap(
        root,
        tx_id="TX-CLOSE-ROADMAP",
        event_id="EVT-CLOSE-ROADMAP",
        actor="agent-x",
        reconciliation_path=reconciliation_path,
        base_ref=base_ref,
    )


def configure_delivery(root: Path, base_ref: str, *, lifecycle: str = "MERGED") -> Path:
    state_path = root / "relay/STATE.yaml"
    state = load_yaml(state_path)
    state["delivery"] = {
        "required": True,
        "primary_vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
    }
    dump(state_path, state)
    dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", build_snapshot(root, base_ref))
    observation = {
        "schema_version": "relay-v3.1-delivery-status",
        "authority": "PROVIDER_READBACK",
        "vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
        "observed_at": "2026-09-22T03:57:35Z",
        "provider_ref": "github:reallaksh19/Common#419",
        "lifecycle": lifecycle,
        "checks": "PASS",
        "review": "APPROVED",
        "mergeability": "MERGEABLE",
    }
    path = root / "provider-observation.yaml"
    dump(path, observation)
    return path


class RelayTransactionalCommandTests(unittest.TestCase):
    def test_different_executor_is_recorded_as_recovery_without_gate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            result = activate_lease(
                root,
                tx_id="TX-TAKEOVER-RECORDER",
                event_id="EVT-TAKEOVER-RECORDER",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            old = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            self.assertEqual("INVALIDATED", old["state"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            started = [row for row in events if row["type"] == "RECOVERY_STARTED"][-1]
            self.assertEqual("RECORDER_EXPLICIT_TAKEOVER", started["details"]["recovery_reason"])

    def test_explicit_recovery_takeover_invalidates_abandoned_lease_and_keeps_same_ep(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            result = activate_lease(
                root,
                tx_id="TX-TAKEOVER-RECOVERY",
                event_id="EVT-TAKEOVER-RECOVERY",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
            )
            self.assertEqual("COMMITTED", result["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            old_lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            new_lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-02.yaml")
            self.assertEqual("EP-TA-011", state["execution"]["ep"])
            self.assertEqual("LEASE-TA-011-02", state["execution"]["lease"])
            self.assertEqual("INVALIDATED", old_lease["state"])
            self.assertIn("RECOVERY_TAKEOVER_BY:LEASE-TA-011-02", old_lease["invalidation"]["reasons"])
            self.assertEqual("ACTIVE", new_lease["state"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            revoked = [item for item in events if item["event_id"] == "EVT-TAKEOVER-RECOVERY-REL"][0]
            granted = [item for item in events if item["event_id"] == "EVT-TAKEOVER-RECOVERY"][0]
            self.assertEqual("LEASE_REVOKED", revoked["type"])
            self.assertEqual("RECOVERY", revoked["details"]["continuation"])
            self.assertEqual("RECOVERY", granted["details"]["continuation"])

    def test_recovery_records_completed_parent_context_without_blocking_takeover(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            baseline = install_parent_issue(root, number=1771)
            closed = parent_issue_observation(
                baseline=baseline,
                number=1771,
                state="CLOSED",
                disposition="CLOSE",
                acceptance_state="COMPLETE",
            )

            result = activate_lease(
                root,
                tx_id="TX-RECOVERY-STALE-PARENT",
                event_id="EVT-RECOVERY-STALE-PARENT",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
                programme_issue_observations=[closed],
            )
            self.assertEqual("COMMITTED", result["status"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            started = [row for row in events if row["type"] == "RECOVERY_STARTED"][-1]
            self.assertEqual("RECORDER_EXPLICIT_TAKEOVER", started["details"]["recovery_reason"])

    def test_recovery_can_resume_only_when_parent_remains_in_programme_frontier(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            baseline = install_parent_issue(root, number=1771)
            live = parent_issue_observation(
                baseline=baseline,
                number=1771,
                state="OPEN",
                disposition="NO_CHANGE",
                acceptance_state="PENDING",
            )

            result = activate_lease(
                root,
                tx_id="TX-RECOVERY-LIVE-PARENT",
                event_id="EVT-RECOVERY-LIVE-PARENT",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
                programme_issue_observations=[live],
            )
            self.assertEqual("COMMITTED", result["status"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            started = [row for row in events if row["type"] == "RECOVERY_STARTED"][-1]
            self.assertEqual(
                ["example/project#1771"],
                started["details"]["programme_frontier"],
            )

    def test_handoff_release_records_missing_handover_as_advisory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            result = release_lease(
                root,
                tx_id="TX-RELEASE-NO-HANDOVER",
                event_id="EVT-RELEASE-NO-HANDOVER",
                actor="agent-x",
                reason="HANDOFF",
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            released = [row for row in events if row["type"] == "LEASE_RELEASED"][-1]
            self.assertIn("RECORDER_ADVISORY:NO_FRESH_HANDOVER", released["basis"])

    def test_admit_task_atomically_moves_idle_repository_to_active_execution(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            release_lease(
                root,
                tx_id="TX-RELEASE-BEFORE-ADMIT",
                event_id="EVT-RELEASE-BEFORE-ADMIT",
                actor="agent-x",
                reason="ADMINISTRATIVE",
            )

            roadmap_path = root / "relay/ROADMAP/ROADMAP.yaml"
            roadmap = load_yaml(roadmap_path)
            roadmap["work_packages"].append({
                "id": "WP-OTHER-ACTIVE",
                "title": "Separate unfinished programme obligation",
                "weight": 10,
                "state": "ACTIVE",
                "depends_on": [],
            })
            dump(roadmap_path, roadmap)

            source_ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
            new_ep = copy.deepcopy(source_ep)
            new_ep["id"] = "EP-TA-012"
            request = {
                "schema_version": "relay-v3.1-task-admission",
                "roadmap": {
                    "disposition": "MAPPED_EXISTING_WP",
                    "new_revision": "RM-0013",
                    "basis": ["Owner selected the next bounded task."],
                    "work_package": {
                        "id": "WP-TA-109",
                        "title": "Current work",
                        "weight": 50,
                        "state": "ACTIVE",
                        "depends_on": ["WP-TA-108"],
                    },
                },
                "ep": new_ep,
                "lease": {
                    "id": "LEASE-TA-012-01",
                    "executor_id": "agent-z",
                    "method": "DETERMINISTIC",
                },
                "delivery": {"required": False, "primary_vehicle": None},
            }
            request_path = root / "task-admission.yaml"
            dump(request_path, request)
            result = admit_task(
                root,
                tx_id="TX-ADMIT-001",
                event_id="EVT-ADMIT-001",
                actor="owner",
                admission_path=request_path,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual("ACTIVE", state["execution"]["lifecycle"])
            self.assertEqual("EP-TA-012", state["execution"]["ep"])
            self.assertEqual("LEASE-TA-012-01", state["execution"]["lease"])
            self.assertEqual("RM-0013", state["roadmap"]["revision"])
            admitted_roadmap = load_yaml(root / "relay/ROADMAP/ROADMAP.yaml")
            self.assertEqual(
                {"WP-TA-109", "WP-OTHER-ACTIVE"},
                {
                    item["id"]
                    for item in admitted_roadmap["work_packages"]
                    if item["state"] == "ACTIVE"
                },
            )
            self.assertTrue((root / "relay/WORK/EP-TA-012.yaml").exists())
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            ids = {row["event_id"] for row in events}
            self.assertTrue({"EVT-ADMIT-001-OWNER", "EVT-ADMIT-001-EP", "EVT-ADMIT-001-LEASE"}.issubset(ids))
            self.assertEqual([], validate(root))

    def test_provider_backed_admission_can_allocate_execution_identities(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            baseline = install_parent_issue(root, number=1771)
            release_lease(
                root,
                tx_id="TX-RELEASE-BEFORE-CANONICAL-ADMIT",
                event_id="EVT-RELEASE-BEFORE-CANONICAL-ADMIT",
                actor="agent-x",
                reason="ADMINISTRATIVE",
            )

            source_ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
            new_ep = copy.deepcopy(source_ep)
            new_ep.pop("id", None)
            request = {
                "schema_version": "relay-v3.1-task-admission",
                "roadmap": {
                    "disposition": "MAPPED_EXISTING_WP",
                    "new_revision": "RM-0013",
                    "basis": ["Owner selected the provider-backed task."],
                    "work_package": {
                        "id": "WP-TA-109",
                        "title": "Current work",
                        "weight": 50,
                        "state": "ACTIVE",
                        "depends_on": ["WP-TA-108"],
                    },
                },
                "ep": new_ep,
                "lease": {
                    "executor_id": "agent-z",
                    "method": "DETERMINISTIC",
                },
                "delivery": {"required": False, "primary_vehicle": None},
            }
            request_path = root / "canonical-task-admission.yaml"
            dump(request_path, request)
            live = parent_issue_observation(
                baseline=baseline,
                number=1771,
                state="OPEN",
                disposition="NO_CHANGE",
                acceptance_state="PENDING",
            )

            result = admit_task(
                root,
                tx_id=None,
                event_id=None,
                actor="owner",
                admission_path=request_path,
                base_ref=base_ref,
                programme_issue_observations=[live],
                selected_programme_ref="example/project#1771",
            )

            self.assertEqual("COMMITTED", result["status"])
            self.assertEqual("TX.1771.1", result["id"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual("EP.1771.1", state["execution"]["ep"])
            self.assertEqual("LEASE.1771.1", state["execution"]["lease"])
            self.assertTrue((root / "relay/WORK/EP.1771.1.yaml").exists())
            self.assertTrue((root / "relay/LEASES/LEASE.1771.1.yaml").exists())
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            canonical = [
                row["event_id"]
                for row in events
                if str(row["event_id"]).startswith("EVT.1771.")
            ]
            self.assertEqual(["EVT.1771.1", "EVT.1771.2", "EVT.1771.3"], canonical)

    def test_provider_backed_admission_records_programme_uncertainty_without_blocking(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_parent_issue(root, number=1771)
            release_lease(
                root,
                tx_id="TX-RELEASE-BEFORE-PARENT-ADMIT",
                event_id="EVT-RELEASE-BEFORE-PARENT-ADMIT",
                actor="agent-x",
                reason="ADMINISTRATIVE",
            )

            source_ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
            new_ep = copy.deepcopy(source_ep)
            new_ep["id"] = "EP-TA-012"
            request = {
                "schema_version": "relay-v3.1-task-admission",
                "roadmap": {
                    "disposition": "MAPPED_EXISTING_WP",
                    "new_revision": "RM-0013",
                    "basis": ["Recorder-first admission preserves programme uncertainty as context."],
                    "work_package": {
                        "id": "WP-TA-109",
                        "title": "Current work",
                        "weight": 50,
                        "state": "ACTIVE",
                        "depends_on": ["WP-TA-108"],
                    },
                },
                "ep": new_ep,
                "lease": {
                    "id": "LEASE-TA-012-01",
                    "executor_id": "agent-z",
                    "method": "DETERMINISTIC",
                },
                "delivery": {"required": False, "primary_vehicle": None},
            }
            request_path = root / "parent-task-admission.yaml"
            dump(request_path, request)

            result = admit_task(
                root,
                tx_id="TX-PARENT-ADMIT-MISSING",
                event_id="EVT-PARENT-ADMIT-MISSING",
                actor="owner",
                admission_path=request_path,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual("EP-TA-012", state["execution"]["ep"])

    def test_critical_transaction_command_cannot_mutate_unowned_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            roadmap = load_yaml(root / "relay/ROADMAP/ROADMAP.yaml")
            roadmap["revision"] = "RM-ILLEGAL"
            with self.assertRaisesRegex(TransactionError, "ACTIVATE_LEASE cannot mutate"):
                execute(
                    root,
                    tx_id="TX-ILLEGAL-TARGET",
                    command="ACTIVATE_LEASE",
                    actor="agent-x",
                    replacements={"relay/ROADMAP/ROADMAP.yaml": yaml_bytes(roadmap)},
                )

    def test_explicit_recovery_takeover_transfers_exclusive_custody_and_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            result = activate_lease(
                root,
                tx_id="TX-ACTIVATE-001",
                event_id="EVT-ACTIVATE-001",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="owner",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
            )
            self.assertEqual("COMMITTED", result["status"])
            old = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            new = load_yaml(root / "relay/LEASES/LEASE-TA-011-02.yaml")
            state = load_yaml(root / "relay/STATE.yaml")
            snapshot = load_yaml(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml")
            self.assertEqual("INVALIDATED", old["state"])
            self.assertEqual("ACTIVE", new["state"])
            self.assertEqual("agent-y", new["executor"]["id"])
            self.assertEqual("LEASE-TA-011-02", state["execution"]["lease"])
            self.assertEqual("LEASE-TA-011-02", snapshot["execution"]["lease"])
            self.assertEqual("agent-y", snapshot["execution"]["executor"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            ids = [item["event_id"] for item in events]
            self.assertIn("EVT-ACTIVATE-001-REL", ids)
            self.assertIn("EVT-ACTIVATE-001", ids)
            self.assertEqual([], validate(root))

    def test_provider_backed_custody_maintenance_can_allocate_transition_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_parent_issue(root, number=1771)

            activated = activate_lease(
                root,
                tx_id="TX-CUSTODY-SETUP",
                event_id="EVT-CUSTODY-SETUP",
                lease_id="LEASE-CUSTODY-SETUP",
                executor_id="agent-x",
                actor="agent-x",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", activated["status"])

            renewed = renew_lease(
                root,
                tx_id=None,
                event_id=None,
                actor="agent-x",
                expected_custody_epoch=1,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", renewed["status"])
            self.assertEqual("TX.1771.1", renewed["id"])

            released = release_lease(
                root,
                tx_id=None,
                event_id=None,
                actor="agent-x",
                reason="ADMINISTRATIVE",
                expected_custody_epoch=1,
            )
            self.assertEqual("COMMITTED", released["status"])
            self.assertEqual("TX.1771.2", released["id"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual("IDLE", state["execution"]["lifecycle"])

            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            canonical = [
                (row["event_id"], row["type"])
                for row in events
                if str(row["event_id"]).startswith("EVT.1771.")
            ]
            self.assertEqual(
                [("EVT.1771.1", "LEASE_RENEWED"), ("EVT.1771.2", "LEASE_RELEASED")],
                canonical,
            )

    def test_release_lease_atomically_enters_idle_state_and_refreshes_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            result = release_lease(
                root,
                tx_id="TX-RELEASE-001",
                event_id="EVT-RELEASE-001",
                actor="agent-x",
                reason="ADMINISTRATIVE",
            )
            self.assertEqual("COMMITTED", result["status"])
            lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            state = load_yaml(root / "relay/STATE.yaml")
            snapshot = load_yaml(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml")
            self.assertEqual("RELEASED", lease["state"])
            self.assertEqual(
                {"lifecycle": "IDLE", "ep": None, "lease": None, "route": None},
                state["execution"],
            )
            self.assertEqual("IDLE", snapshot["execution"]["lifecycle"])
            self.assertIsNone(snapshot["execution"]["lease"])
            self.assertEqual([], validate(root))

    def test_accept_checkpoint_publishes_immutable_checkpoint_state_and_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            _, _, _, _, template, *_ = base_objects()
            checkpoint = copy.deepcopy(template)
            checkpoint["id"] = "CP-TA-011"
            checkpoint["ep"] = "EP-TA-011"
            ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
            current_material = inspect_material_basis(root, ep, base_ref)["material_basis"]
            checkpoint["material_result"] = {
                "head": current_material["head"],
                "relevant_paths_digest": current_material["relevant_paths_digest"],
                "dependency_digest": current_material["dependency_digest"],
            }
            incoming = root / "incoming-checkpoint.yaml"
            dump(incoming, checkpoint)

            result = accept_checkpoint(
                root,
                tx_id="TX-CP-001",
                event_id="EVT-CP-001",
                actor="agent-x",
                checkpoint_path=incoming,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            self.assertTrue((root / "relay/CHECKPOINTS/CP-TA-011.yaml").exists())
            state = load_yaml(root / "relay/STATE.yaml")
            snapshot = load_yaml(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml")
            self.assertEqual("CP-TA-011", state["accepted"]["checkpoint"])
            self.assertEqual("CP-TA-011", snapshot["evidence"]["latest_checkpoint"])
            self.assertEqual([], validate(root))

            with self.assertRaisesRegex(TransactionError, "immutable"):
                accept_checkpoint(
                    root,
                    tx_id="TX-CP-002",
                    event_id="EVT-CP-002",
                    actor="agent-x",
                    checkpoint_path=incoming,
                    base_ref=base_ref,
                )

    def test_checkpoint_records_control_and_material_debt_without_blocking(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            _, _, _, _, template, *_ = base_objects()
            checkpoint = copy.deepcopy(template)
            checkpoint["id"] = "CP-TA-011"
            checkpoint["ep"] = "EP-TA-011"
            checkpoint["material_result"]["head"] = "deadbeef"
            incoming = root / "incoming-checkpoint.yaml"
            dump(incoming, checkpoint)

            controls_path = root / "relay/CONTROLS/controls.yaml"
            controls = load_yaml(controls_path)
            controls["controls"].append({
                "id": "CTRL-BLOCK-CP",
                "kind": "QUALITY",
                "state": "OPEN",
                "source": {"type": "VALIDATOR", "ref": "synthetic"},
                "condition": "Synthetic checkpoint warning.",
                "blocks": ["CHECKPOINT"],
                "permits": ["TEST"],
                "resolution": {"condition": "Synthetic blocker clears.", "evidence": []},
            })
            dump(controls_path, controls)

            result = accept_checkpoint(
                root,
                tx_id="TX-CP-RECORDER",
                event_id="EVT-CP-RECORDER",
                actor="agent-x",
                checkpoint_path=incoming,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            stored = load_yaml(root / "relay/CHECKPOINTS/CP-TA-011.yaml")
            self.assertEqual("deadbeef", stored["material_result"]["head"])

    def test_checkpoint_acceptance_id_mismatch_is_recorded_not_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            _, _, _, _, template, *_ = base_objects()
            checkpoint = copy.deepcopy(template)
            checkpoint["id"] = "CP-TA-011"
            checkpoint["ep"] = "EP-TA-011"
            checkpoint["acceptance"][0]["id"] = "AC-WRONG"
            incoming = root / "incoming-checkpoint.yaml"
            dump(incoming, checkpoint)

            result = accept_checkpoint(
                root,
                tx_id="TX-CP-AC-MISMATCH",
                event_id="EVT-CP-AC-MISMATCH",
                actor="agent-x",
                checkpoint_path=incoming,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            stored = load_yaml(root / "relay/CHECKPOINTS/CP-TA-011.yaml")
            self.assertEqual("AC-WRONG", stored["acceptance"][0]["id"])

    def test_provider_backed_checkpoint_can_allocate_acceptance_identities(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_parent_issue(root, number=1771)

            _, _, _, _, template, *_ = base_objects()
            checkpoint = copy.deepcopy(template)
            checkpoint.pop("id", None)
            ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
            material = inspect_material_basis(root, ep, base_ref)["material_basis"]
            checkpoint["ep"] = "EP-TA-011"
            checkpoint["material_result"] = {
                "head": material["head"],
                "relevant_paths_digest": material["relevant_paths_digest"],
                "dependency_digest": material["dependency_digest"],
            }
            incoming = root / "canonical-checkpoint.yaml"
            dump(incoming, checkpoint)

            result = accept_checkpoint(
                root,
                tx_id=None,
                event_id=None,
                actor="agent-x",
                checkpoint_path=incoming,
                base_ref=base_ref,
            )

            self.assertEqual("COMMITTED", result["status"])
            self.assertEqual("TX.1771.1", result["id"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual("CP.1771.1", state["accepted"]["checkpoint"])
            self.assertTrue((root / "relay/CHECKPOINTS/CP.1771.1.yaml").exists())
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            accepted = [row for row in events if row["type"] == "CHECKPOINT_ACCEPTED"][-1]
            self.assertEqual("EVT.1771.1", accepted["event_id"])
            self.assertEqual("CP.1771.1", accepted["subject"])

    def test_failed_checkpoint_is_recorded_without_claiming_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            _, _, _, _, template, *_ = base_objects()
            checkpoint = copy.deepcopy(template)
            checkpoint["id"] = "CP-TA-011"
            checkpoint["ep"] = "EP-TA-011"
            checkpoint["acceptance"][0]["result"] = "FAIL"
            incoming = root / "incoming-checkpoint.yaml"
            dump(incoming, checkpoint)

            result = accept_checkpoint(
                root,
                tx_id="TX-CP-FAIL",
                event_id="EVT-CP-FAIL",
                actor="agent-x",
                checkpoint_path=incoming,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            stored = load_yaml(root / "relay/CHECKPOINTS/CP-TA-011.yaml")
            self.assertEqual("FAIL", stored["acceptance"][0]["result"])

    def test_local_execution_after_lease_release_uses_checkpoint_ep_context(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            historical_ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
            historical_ep["id"] = "EP-TA-010"
            dump(root / "relay/WORK/EP-TA-010.yaml", historical_ep)
            release_lease(
                root,
                tx_id="TX-RELEASE-LOCAL",
                event_id="EVT-RELEASE-LOCAL",
                actor="agent-x",
                reason="ADMINISTRATIVE",
            )
            result = export_local_execution(
                root,
                tx_id="TX-LOCAL-IDLE",
                event_id="EVT-LOCAL-IDLE",
                actor="agent-x",
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            package = load_yaml(root / "relay/GENERATED/LOCAL_EXECUTION.yaml")
            self.assertEqual("EP-TA-010", package["execution"]["ep"])
            self.assertTrue(package["checkpoint"]["handoff"])
            self.assertEqual(
                "Read CURRENT_SNAPSHOT and EP.",
                package["next"]["first_action"],
            )

    def test_control_resolution_changes_control_event_and_snapshot_together(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            add_open_control(root)
            install_parent_issue(root, number=1771)
            result = resolve_control(
                root,
                tx_id=None,
                event_id=None,
                actor="agent-x",
                control_id="CTRL-TEST-001",
                evidence=["provider readback PASS"],
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            controls = load_yaml(root / "relay/CONTROLS/controls.yaml")
            row = [item for item in controls["controls"] if item["id"] == "CTRL-TEST-001"][0]
            self.assertEqual("RESOLVED", row["state"])
            self.assertEqual(["provider readback PASS"], row["resolution"]["evidence"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertIn("EVT.1771.1", [item["event_id"] for item in events])
            self.assertEqual("TX.1771.1", result["id"])
            self.assertEqual([], validate(root))

    def test_handover_and_local_execution_are_generated_downstream_views(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            accept_current_checkpoint_and_reconcile(root, base_ref)
            planned = plan_handover(
                root,
                tx_id="TX-HANDOVER-PLAN-001",
                event_id="EVT-HANDOVER-PLAN-001",
                actor="agent-x",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
            )
            self.assertEqual("COMMITTED", planned["status"])
            handover = publish_handover(
                root,
                tx_id="TX-HANDOVER-001",
                event_id="EVT-HANDOVER-001",
                actor="agent-x",
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", handover["status"])
            text = (root / "relay/GENERATED/HANDOVER.md").read_text(encoding="utf-8")
            self.assertIn("Engineering Relay V3.1 Handover", text)
            self.assertIn("Reconstruction sources", text)

            local = export_local_execution(
                root,
                tx_id="TX-LOCAL-001",
                event_id="EVT-LOCAL-001",
                actor="agent-x",
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", local["status"])
            package = load_yaml(root / "relay/GENERATED/LOCAL_EXECUTION.yaml")
            self.assertEqual("DERIVED_EXECUTION_PACKAGE", package["authority"])
            self.assertEqual("EP-TA-011", package["execution"]["ep"])
            self.assertEqual("Validate schemas.", package["next"]["first_action"])
            self.assertEqual([], validate(root))

    def test_sync_delivery_requires_provider_vehicle_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            observation = configure_delivery(root, base_ref)
            install_parent_issue(root, number=1771)
            result = sync_delivery(
                root,
                tx_id=None,
                event_id=None,
                actor="provider-sync",
                observation_path=observation,
            )
            self.assertEqual("COMMITTED", result["status"])
            self.assertEqual("TX.1771.1", result["id"])
            events, event_errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], event_errors)
            self.assertIn("EVT.1771.1", [item["event_id"] for item in events])
            persisted = load_yaml(root / "relay/GENERATED/DELIVERY_STATUS.yaml")
            self.assertEqual("PROVIDER_READBACK", persisted["authority"])
            self.assertEqual("MERGED", persisted["lifecycle"])

            wrong = load_yaml(observation)
            wrong["vehicle"]["number"] = 999
            wrong_path = root / "wrong-provider-observation.yaml"
            dump(wrong_path, wrong)
            with self.assertRaisesRegex(TransactionError, "does not match"):
                sync_delivery(
                    root,
                    tx_id="TX-DELIVERY-002",
                    event_id="EVT-DELIVERY-002",
                    actor="provider-sync",
                    observation_path=wrong_path,
                )

    def test_close_records_terminal_state_without_checkpoint_or_delivery_gate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            observation = configure_delivery(root, base_ref, lifecycle="OPEN")
            sync_delivery(
                root,
                tx_id="TX-DELIVERY-OPEN",
                event_id="EVT-DELIVERY-OPEN",
                actor="provider-sync",
                observation_path=observation,
            )

            result = close_task(
                root,
                tx_id="TX-CLOSE-RECORDER",
                event_id="EVT-CLOSE-RECORDER",
                actor="owner",
            )
            self.assertEqual("COMMITTED", result["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            self.assertEqual("TERMINAL", state["execution"]["lifecycle"])
            self.assertEqual("RELEASED", lease["state"])

    def test_incomplete_transaction_blocks_all_authority_until_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            with self.assertRaises(TransactionError):
                activate_lease(
                    root,
                    tx_id="TX-ACTIVATE-FAIL",
                    event_id="EVT-ACTIVATE-FAIL",
                    lease_id="LEASE-TA-011-02",
                    executor_id="agent-y",
                    actor="owner",
                    method="DETERMINISTIC",
                    qualification=None,
                    owner_basis=None,
                    branch=None,
                    base_ref=base_ref,
                    recovery_takeover=True,
                    fail_after=1,
                )
            errors = validate_authority(root)
            self.assertTrue(any("requires recovery" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()
