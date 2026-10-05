from __future__ import annotations

import importlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
V25_SCRIPTS = ROOT.parent / "engineering-pr-delivery-v2.5" / "scripts"
for entry in (SCRIPTS, V25_SCRIPTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

import bootstrap_relay as v25_bootstrap

from protocol_cutover import CutoverError, activate, assess, freeze_legacy, validate_selection
from protocol_default import resolve as resolve_default
from snapshot_projection import build as build_snapshot
from v25_migration import (
    INTELLIGENCE_CONTINUITY_CONTROL,
    MIGRATION_CONTROL,
    MigrationError,
    bootstrap,
    build_report,
    legacy_inventory,
)
from v3lib import load_yaml
from validate_foundation import validate


OWNER_DIGEST = "sha256:" + ("b" * 64)
OWNER_TIME = "2026-09-22T04:23:16Z"


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def init_legacy_repo(root: Path) -> None:
    manifest = {
        "schema_version": "relay-v2.5-bootstrap",
        "repository": {
            "name": "synthetic",
            "remote": "https://github.com/example/project",
            "repository_type": "application",
            "default_branch": "main",
        },
        "relay_protocol": {"basis_ref": "Common@85e59a93d469"},
        "roadmap": {
            "id": "RM-LEGACY",
            "revision": "RM-LEGACY-1",
            "title": "Synthetic legacy roadmap",
        },
        "initial_position": {
            "objective": {"id": "OBJ-1", "title": "Legacy objective"},
            "phase": {"id": "PH-1", "title": "Legacy phase"},
            "work_package": {"id": "WP-1", "title": "Legacy first work package"},
        },
        "initialization": {
            "next_action": "Reconcile the legacy roadmap.",
            "notes": [],
        },
    }
    v25_bootstrap.apply(root, v25_bootstrap.build(manifest))

    dump(root / "agents/relay/discovery/DISC-HISTORY.yaml", {
        "schema_version": "relay-v2.5-discovery",
        "id": "DISC-HISTORY",
        "result": "PASS",
    })
    dump(root / "agents/relay/qualification/QUAL-HISTORY.yaml", {
        "schema_version": "relay-v2.5-qualification",
        "id": "QUAL-HISTORY",
        "result": "PASS",
    })
    dump(root / "agents/relay/checkpoints/CP-HISTORY.yaml", {
        "schema_version": "relay-v2.5",
        "checkpoint_id": "CP-HISTORY",
    })

    subprocess.run(["git", "-C", str(root), "init", "-b", "main"], check=True, stdout=subprocess.PIPE)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Relay Test"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "relay@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-m", "legacy relay"],
        check=True,
        stdout=subprocess.PIPE,
    )


def bootstrap_v3(root: Path) -> str:
    result = bootstrap(
        root,
        tx_id="TX-MIGRATE-001",
        event_id="EVT-MIGRATE-001",
        actor="migration-agent",
        owner_outcome="Preserve engineering continuity while adopting the smaller V3 authority model.",
        current_goal="Reconcile the legacy frontier into native V3 authority.",
    )
    if result["status"] != "COMMITTED":
        raise AssertionError(result)
    return git(root, "rev-parse", "HEAD")


def make_cutover_ready(root: Path) -> None:
    state_path = root / "relay/STATE.yaml"
    state = load_yaml(state_path)
    state["execution"] = {"lifecycle": "IDLE", "ep": None, "lease": None, "route": None}
    dump(state_path, state)

    controls_path = root / "relay/CONTROLS/controls.yaml"
    controls = load_yaml(controls_path)
    migration = [x for x in controls["controls"] if x["id"] == MIGRATION_CONTROL][0]
    migration["state"] = "RESOLVED"
    migration["resolution"]["evidence"] = [
        "Synthetic reconciliation established native V3 present authority without importing legacy receipts."
    ]
    continuity = [x for x in controls["controls"] if x["id"] == INTELLIGENCE_CONTINUITY_CONTROL][0]
    continuity["state"] = "RESOLVED"
    continuity["resolution"]["evidence"] = [
        "relay/GENERATED/INTELLIGENCE_CONTINUITY.yaml: ready=true; Common#421 continuity proof."
    ]
    dump(controls_path, controls)

    freeze_result = freeze_legacy(
        root,
        tx_id="TX-FREEZE-001",
        event_id="EVT-FREEZE-001",
        actor="migration-agent",
    )
    if freeze_result["status"] != "COMMITTED":
        raise AssertionError(freeze_result)

    # Generate the continuity proof from live preserved V2.5 authority instead of
    # manufacturing a schema-valid PASS document. This mirrors the real cutover path.
    from intelligence_projection import assess_continuity
    continuity_report = assess_continuity(root)
    if continuity_report.get("ready") is not True:
        raise AssertionError(continuity_report)
    dump(root / "relay/GENERATED/INTELLIGENCE_CONTINUITY.yaml", continuity_report)

    dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", build_snapshot(root))


class V25MigrationTests(unittest.TestCase):
    def test_report_validates_and_inventories_legacy_history_without_writes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            entries_before, digest_before = legacy_inventory(root)
            report = build_report(root)
            entries_after, digest_after = legacy_inventory(root)

            self.assertEqual("PASS", report["validation"]["repo_state"])
            self.assertEqual(digest_before, digest_after)
            self.assertEqual(entries_before, entries_after)
            counts = report["legacy_inventory"]["category_counts"]
            self.assertGreaterEqual(counts.get("DISCOVERY", 0), 1)
            self.assertGreaterEqual(counts.get("QUALIFICATION", 0), 1)
            self.assertGreaterEqual(counts.get("CHECKPOINT", 0), 1)
            self.assertTrue(report["bootstrap"]["preserves_legacy_tree"])
            self.assertFalse(report["bootstrap"]["creates_native_history"])
            self.assertFalse((root / "relay").exists())

    def test_bootstrap_is_non_destructive_and_keeps_v25_selected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            _, legacy_before = legacy_inventory(root)
            bootstrap_v3(root)
            _, legacy_after = legacy_inventory(root)

            self.assertEqual(legacy_before, legacy_after)
            state = load_yaml(root / "relay/STATE.yaml")
            selection = load_yaml(root / "relay/PROTOCOL_SELECTION.yaml")
            controls = load_yaml(root / "relay/CONTROLS/controls.yaml")
            self.assertEqual("INITIALIZING", state["execution"]["lifecycle"])
            self.assertIsNone(state["execution"]["ep"])
            self.assertIsNone(state["accepted"]["checkpoint"])
            self.assertFalse((root / "relay/WORK").exists())
            self.assertFalse((root / "relay/CHECKPOINTS").exists())
            self.assertEqual("V2_5", selection["selected_protocol"])
            self.assertEqual("PREPARED", selection["status"])
            self.assertEqual("LIVE_COMPATIBILITY", selection["legacy"]["policy"])
            migration = [x for x in controls["controls"] if x["id"] == MIGRATION_CONTROL][0]
            self.assertEqual("OPEN", migration["state"])
            self.assertEqual([], validate(root))
            default = resolve_default(root)
            self.assertEqual("V2_5", default["selected_protocol"])
            self.assertEqual("PREPARED", default["status"])

    def test_bootstrap_refuses_to_invent_owner_intent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            with self.assertRaisesRegex(MigrationError, "owner_outcome"):
                bootstrap(
                    root,
                    tx_id="TX-MIGRATE-BAD",
                    event_id="EVT-MIGRATE-BAD",
                    actor="migration-agent",
                    owner_outcome="",
                    current_goal="Goal",
                )
            self.assertFalse((root / "relay/STATE.yaml").exists())

    def test_cutover_is_denied_while_initializing_or_migration_control_open(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            bootstrap_v3(root)
            readiness = assess(root)
            self.assertFalse(readiness["ready"])
            self.assertEqual("FAIL", readiness["checks"]["migration_control_resolved"])
            self.assertEqual("FAIL", readiness["checks"]["native_lifecycle_ready"])
            with self.assertRaisesRegex(CutoverError, "not ready"):
                activate(
                    root,
                    tx_id="TX-CUTOVER-BLOCKED",
                    event_id="EVT-CUTOVER-BLOCKED",
                    actor="owner",
                    owner_utterance_digest=OWNER_DIGEST,
                    owner_session_timestamp=OWNER_TIME,
                )


    def test_cutover_remains_blocked_without_421_intelligence_continuity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            bootstrap_v3(root)

            state_path = root / "relay/STATE.yaml"
            state = load_yaml(state_path)
            state["execution"] = {"lifecycle": "IDLE", "ep": None, "lease": None, "route": None}
            dump(state_path, state)

            controls_path = root / "relay/CONTROLS/controls.yaml"
            controls = load_yaml(controls_path)
            migration = [x for x in controls["controls"] if x["id"] == MIGRATION_CONTROL][0]
            migration["state"] = "RESOLVED"
            migration["resolution"]["evidence"] = ["Native V3 present authority reconciled."]
            dump(controls_path, controls)
            dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", build_snapshot(root))

            readiness = assess(root)
            self.assertFalse(readiness["ready"], readiness)
            self.assertEqual("FAIL", readiness["checks"]["roadmap_intelligence_continuity"])
            with self.assertRaisesRegex(CutoverError, "roadmap_intelligence_continuity"):
                activate(
                    root,
                    tx_id="TX-CUTOVER-NO-421",
                    event_id="EVT-CUTOVER-NO-421",
                    actor="owner",
                    owner_utterance_digest=OWNER_DIGEST,
                    owner_session_timestamp=OWNER_TIME,
                )

    def test_resolved_continuity_control_without_report_still_blocks_cutover(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            bootstrap_v3(root)
            make_cutover_ready(root)
            (root / "relay/GENERATED/INTELLIGENCE_CONTINUITY.yaml").unlink()

            readiness = assess(root)
            self.assertFalse(readiness["ready"], readiness)
            self.assertEqual("FAIL", readiness["checks"]["roadmap_intelligence_continuity"])
            self.assertTrue(any("intelligence_continuity_report=FAIL" in item for item in readiness["basis"]))

    def test_continuity_report_must_bind_exact_preserved_legacy_digest(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            bootstrap_v3(root)
            make_cutover_ready(root)
            path = root / "relay/GENERATED/INTELLIGENCE_CONTINUITY.yaml"
            report = load_yaml(path)
            report["source"]["legacy_tree_digest"] = "sha256:" + ("0" * 64)
            dump(path, report)

            readiness = assess(root)
            self.assertFalse(readiness["ready"], readiness)
            self.assertEqual("FAIL", readiness["checks"]["roadmap_intelligence_continuity"])

    def test_forged_ready_continuity_report_cannot_clear_cutover(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            bootstrap_v3(root)
            make_cutover_ready(root)
            path = root / "relay/GENERATED/INTELLIGENCE_CONTINUITY.yaml"
            report = load_yaml(path)
            report["projections"]["task_snapshot_digest"] = "sha256:" + ("c" * 64)
            report["evidence"] = ["Forged but schema-valid continuity report."]
            dump(path, report)

            readiness = assess(root)
            self.assertFalse(readiness["ready"], readiness)
            self.assertEqual("FAIL", readiness["checks"]["roadmap_intelligence_continuity"])
            self.assertTrue(any("intelligence_continuity_recomputed=PASS" in item for item in readiness["basis"]))
            self.assertTrue(any("intelligence_continuity_report=FAIL" in item for item in readiness["basis"]))

    def test_cutover_freeze_preserves_bootstrap_digest_and_binds_latest_live_legacy(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            bootstrap_v3(root)
            selection_before = load_yaml(root / "relay/PROTOCOL_SELECTION.yaml")
            bootstrap_digest = selection_before["legacy"]["tree_digest"]

            profile = root / "agents/relay/REPO_PROFILE.yaml"
            profile.write_text(profile.read_text(encoding="utf-8") + "\n# legitimate pre-cutover V2.5 evolution\n", encoding="utf-8")
            _, live_digest = legacy_inventory(root)
            self.assertNotEqual(bootstrap_digest, live_digest)

            result = freeze_legacy(
                root,
                tx_id="TX-FREEZE-CHANGED",
                event_id="EVT-FREEZE-CHANGED",
                actor="migration-agent",
            )
            self.assertEqual("COMMITTED", result["status"])
            selection_after = load_yaml(root / "relay/PROTOCOL_SELECTION.yaml")
            self.assertEqual(bootstrap_digest, selection_after["legacy"]["tree_digest"])
            self.assertEqual(live_digest, selection_after["cutover"]["legacy_freeze_digest"])

    def test_ready_cutover_requires_owner_basis_and_activates_v3(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            bootstrap_v3(root)
            make_cutover_ready(root)
            readiness = assess(root)
            self.assertTrue(readiness["ready"], readiness)

            with self.assertRaises(CutoverError):
                activate(
                    root,
                    tx_id="TX-CUTOVER-BAD-AUTH",
                    event_id="EVT-CUTOVER-BAD-AUTH",
                    actor="owner",
                    owner_utterance_digest="not-a-digest",
                    owner_session_timestamp=OWNER_TIME,
                )

            result = activate(
                root,
                tx_id="TX-CUTOVER-001",
                event_id="EVT-CUTOVER-001",
                actor="owner",
                owner_utterance_digest=OWNER_DIGEST,
                owner_session_timestamp=OWNER_TIME,
            )
            self.assertEqual("COMMITTED", result["status"])
            selection = load_yaml(root / "relay/PROTOCOL_SELECTION.yaml")
            self.assertEqual("V3_1", selection["selected_protocol"])
            self.assertEqual("ACTIVE", selection["status"])
            self.assertEqual("READ_ONLY_HISTORY", selection["legacy"]["policy"])
            self.assertTrue(selection["cutover"]["owner_authorized"])
            self.assertEqual([], validate_selection(root))
            default = resolve_default(root)
            self.assertEqual("V3_1", default["selected_protocol"])
            self.assertEqual("skills/engineering-pr-delivery-v3.1/SKILL.md", default["skill"])
            self.assertTrue((root / "relay/MIGRATION/V25_DEPRECATION.md").exists())

    def test_post_cutover_legacy_mutation_invalidates_selection(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            bootstrap_v3(root)
            make_cutover_ready(root)
            activate(
                root,
                tx_id="TX-CUTOVER-001",
                event_id="EVT-CUTOVER-001",
                actor="owner",
                owner_utterance_digest=OWNER_DIGEST,
                owner_session_timestamp=OWNER_TIME,
            )
            path = root / "agents/relay/discovery/DISC-HISTORY.yaml"
            value = load_yaml(path)
            value["post_cutover_mutation"] = True
            dump(path, value)

            errors = validate_selection(root)
            self.assertTrue(any("changed after V3.1 cutover" in item for item in errors), errors)
            default = resolve_default(root)
            self.assertEqual("INVALID", default["status"])
            self.assertIsNone(default["skill"])

    def test_no_selector_preserves_legacy_default(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_repo(root)
            default = resolve_default(root)
            self.assertEqual("V2_5", default["selected_protocol"])
            self.assertEqual("LEGACY_DEFAULT", default["status"])
            self.assertIn("must not be inferred", default["warning"])


if __name__ == "__main__":
    unittest.main()
