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

from render_owner_status import render as render_owner
from render_technical_status import render as render_technical
from snapshot_projection import build
from v3lib import canonical_digest, load_yaml
from test_relay_can import prepare_git
from test_v3_foundation import dump


def install_accepted_predecessor(root: Path) -> None:
    current = yaml.safe_load((root / "relay/WORK/EP-TA-011.yaml").read_text(encoding="utf-8"))
    predecessor = copy.deepcopy(current)
    predecessor["id"] = "EP-TA-010"
    predecessor["work_package"] = "WP-TA-108"
    predecessor["basis"]["predecessor_checkpoint"] = None
    predecessor["outcome"]["statement"] = "Accepted predecessor outcome."
    dump(root / "relay/WORK/EP-TA-010.yaml", predecessor)


class SnapshotProjectionTests(unittest.TestCase):
    def test_snapshot_is_derived_first_read_model(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            install_accepted_predecessor(root)
            snapshot = build(root, "base")

            self.assertEqual("DERIVED_READ_MODEL", snapshot["authority"])
            self.assertEqual("RM-0012", snapshot["generated_from"]["roadmap_revision"])
            self.assertEqual("EP-TA-011", snapshot["execution"]["ep"])
            self.assertEqual("LEASE-TA-011-01", snapshot["execution"]["lease"])
            self.assertEqual("agent-x", snapshot["execution"]["executor"])
            self.assertEqual("WP-TA-109", snapshot["execution"]["work_package"])
            self.assertEqual(50.0, snapshot["programme"]["programme_progress"])
            self.assertEqual(50.0, snapshot["programme"]["accepted_progress"])
            self.assertEqual(["WP-TA-108"], snapshot["programme"]["evidence_backed_work"])
            self.assertEqual(["WP-TA-108"], snapshot["programme"]["completed_work"])
            self.assertEqual(["WP-TA-109"], snapshot["programme"]["remaining_work"])
            self.assertTrue(snapshot["handoff"]["zero_context_takeover_possible"])
            sources = set(snapshot["handoff"]["reconstruction_sources"])
            self.assertIn("relay/ROADMAP/ROADMAP.yaml", sources)
            self.assertIn("relay/STATE.yaml", sources)
            self.assertIn("relay/WORK/EP-TA-011.yaml", sources)
            self.assertIn("relay/LEASES/LEASE-TA-011-01.yaml", sources)
            self.assertIn("relay/CHECKPOINTS/CP-TA-010.yaml", sources)
            self.assertEqual("Validate schemas.", snapshot["next"]["immediate_material_action"])

    def test_canonical_work_package_and_checkpoint_ids_project_normally(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            roadmap = load_yaml(root / "relay/ROADMAP/ROADMAP.yaml")
            roadmap["revision"] = "RM-CANONICAL"
            roadmap["work_packages"] = [
                {
                    "id": "WP.438",
                    "title": "Canonical programme work",
                    "weight": 100,
                    "state": "COMPLETE",
                    "depends_on": [],
                }
            ]
            dump(root / "relay/ROADMAP/ROADMAP.yaml", roadmap)

            state = load_yaml(root / "relay/STATE.yaml")
            state["roadmap"]["revision"] = "RM-CANONICAL"
            state["execution"]["ep"] = "EP.438.1"
            state["execution"]["lease"] = "LEASE.438.1"
            state["execution"]["route"] = "SERIAL:EP.438.1"
            state["accepted"]["checkpoint"] = "CP.438.1"
            dump(root / "relay/STATE.yaml", state)

            legacy_ep = root / "relay/WORK/EP-TA-011.yaml"
            ep = load_yaml(legacy_ep)
            ep["id"] = "EP.438.1"
            ep["work_package"] = "WP.438"
            dump(root / "relay/WORK/EP.438.1.yaml", ep)
            legacy_ep.unlink()

            legacy_lease = root / "relay/LEASES/LEASE-TA-011-01.yaml"
            lease = load_yaml(legacy_lease)
            lease["id"] = "LEASE.438.1"
            lease["route"] = "SERIAL:EP.438.1"
            lease["basis"]["ep_id"] = "EP.438.1"
            lease["basis"]["ep_digest"] = canonical_digest(ep)
            dump(root / "relay/LEASES/LEASE.438.1.yaml", lease)
            legacy_lease.unlink()

            legacy_cp = root / "relay/CHECKPOINTS/CP-TA-010.yaml"
            cp = load_yaml(legacy_cp)
            cp["id"] = "CP.438.1"
            cp["ep"] = "EP.438.1"
            dump(root / "relay/CHECKPOINTS/CP.438.1.yaml", cp)
            legacy_cp.unlink()

            snapshot = build(root, base_ref)
            self.assertEqual(["WP.438"], snapshot["programme"]["completed_work"])
            self.assertEqual(["WP.438"], snapshot["programme"]["evidence_backed_work"])
            self.assertEqual(100.0, snapshot["programme"]["accepted_progress"])

    def test_roadmap_complete_work_stays_complete_without_recreated_native_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)

            # The roadmap already says WP-TA-108 is COMPLETE, while its historical
            # checkpoint points to an EP that is intentionally absent. This models
            # migrated/history-backed work where native evidence was not replayed.
            snapshot = build(root, "base")

            self.assertEqual(50.0, snapshot["programme"]["programme_progress"])
            self.assertEqual(["WP-TA-108"], snapshot["programme"]["completed_work"])
            self.assertEqual(["WP-TA-109"], snapshot["programme"]["remaining_work"])
            self.assertEqual(0.0, snapshot["programme"]["accepted_progress"])
            self.assertEqual([], snapshot["programme"]["evidence_backed_work"])

    def test_coordination_head_can_advance_without_material_head(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_sha, _ = prepare_git(root)
            snapshot = build(root, "base")
            self.assertEqual(base_sha, snapshot["material"]["head"])
            self.assertNotEqual(
                snapshot["material"]["head"],
                snapshot["generated_from"]["coordination_head"],
            )

    def test_controls_are_grouped_by_consequence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            controls_path = root / "relay/CONTROLS/controls.yaml"
            controls = yaml.safe_load(controls_path.read_text(encoding="utf-8"))
            controls["controls"] = [
                {
                    "id": "CTRL-EXEC",
                    "kind": "COLLISION",
                    "state": "OPEN",
                    "source": {"type": "VALIDATOR", "ref": "collision"},
                    "condition": "writer collision",
                    "blocks": ["MATERIAL_WRITE"],
                    "permits": ["READ"],
                    "resolution": {"condition": "exclusive writer restored", "evidence": []},
                },
                {
                    "id": "CTRL-HANDOVER",
                    "kind": "PROTOCOL",
                    "state": "OPEN",
                    "source": {"type": "VALIDATOR", "ref": "capsule"},
                    "condition": "handover capsule stale",
                    "blocks": ["HANDOVER"],
                    "permits": ["MATERIAL_WRITE"],
                    "resolution": {"condition": "capsule regenerated", "evidence": []},
                },
                {
                    "id": "CTRL-DELIVERY",
                    "kind": "DELIVERY",
                    "state": "OPEN",
                    "source": {"type": "PROVIDER", "ref": "github"},
                    "condition": "projection stale",
                    "blocks": ["PR_READY"],
                    "permits": ["MATERIAL_WRITE"],
                    "resolution": {"condition": "provider synchronized", "evidence": []},
                },
                {
                    "id": "CTRL-INFO",
                    "kind": "PROTOCOL",
                    "state": "OPEN",
                    "source": {"type": "REPOSITORY", "ref": "note"},
                    "condition": "informational debt",
                    "blocks": [],
                    "permits": ["READ"],
                    "resolution": {"condition": "reviewed", "evidence": []},
                },
            ]
            dump(controls_path, controls)
            snapshot = build(root, "base")
            grouped = snapshot["controls"]
            self.assertEqual(["CTRL-EXEC"], grouped["execution_blockers"])
            self.assertEqual(["CTRL-HANDOVER"], grouped["handover_blockers"])
            self.assertEqual(["CTRL-DELIVERY"], grouped["delivery_blockers"])
            self.assertEqual(["CTRL-INFO"], grouped["informational"])

    def test_new_scope_rebases_progress_without_losing_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            install_accepted_predecessor(root)
            before = build(root, "base")
            self.assertEqual(50.0, before["programme"]["accepted_progress"])

            roadmap_path = root / "relay/ROADMAP/ROADMAP.yaml"
            roadmap = yaml.safe_load(roadmap_path.read_text(encoding="utf-8"))
            roadmap["revision"] = "RM-0013"
            roadmap["work_packages"].append(
                {
                    "id": "WP-TA-110",
                    "title": "Newly discovered legitimate scope",
                    "weight": 50,
                    "state": "PLANNED",
                    "depends_on": ["WP-TA-109"],
                }
            )
            dump(roadmap_path, roadmap)
            state_path = root / "relay/STATE.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["roadmap"]["revision"] = "RM-0013"
            dump(state_path, state)

            after = build(root, "base")
            self.assertEqual(33.33, after["programme"]["accepted_progress"])
            self.assertEqual(["WP-TA-108"], after["programme"]["completed_work"])
            self.assertIn("WP-TA-110", after["programme"]["remaining_work"])
            self.assertEqual("CP-TA-010", after["evidence"]["latest_checkpoint"])

    def test_owner_and_technical_views_derive_from_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            install_accepted_predecessor(root)
            snapshot = build(root, "base")
            owner = render_owner(snapshot)
            technical = render_technical(snapshot)
            self.assertIn("Programme progress: **50.0%**", owner)
            self.assertIn("Accepted evidence coverage: **50.0%**", owner)
            self.assertIn("EP-TA-011", owner)
            self.assertIn("Authority: **DERIVED_READ_MODEL**", technical)
            self.assertIn("Material head:", technical)
            self.assertIn("Execution blockers:", technical)


if __name__ == "__main__":
    unittest.main()
