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

from relay_can import evaluate
from validate_foundation import validate
from test_v3_foundation import DIGEST, dump, materialize


WRITE_PATH = "skills/engineering-pr-delivery-v3/scripts/new_feature.py"


def add_control(root: Path, control: dict) -> None:
    path = root / "relay/CONTROLS/controls.yaml"
    import yaml
    controls = yaml.safe_load(path.read_text(encoding="utf-8"))
    controls["controls"].append(control)
    dump(path, controls)


def owner_authority(action: str) -> dict:
    return {
        "id": f"CTRL-OWNER-{action}",
        "kind": "OWNER",
        "state": "OPEN",
        "source": {"type": "OWNER", "ref": f"direct-owner:{action.lower()}"},
        "condition": f"Owner explicitly authorizes {action}.",
        "blocks": [],
        "permits": [action],
        "resolution": {"condition": "Action completed or authority revoked.", "evidence": []},
    }


class RelayCanTests(unittest.TestCase):
    def test_material_write_allows_disjoint_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, drift="DISJOINT")
            self.assertTrue(result["allowed"], result)
            self.assertEqual(["ALLOW"], result["reason_codes"])

    def test_stale_generated_snapshot_does_not_block_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            *_, snapshot, _ = materialize(root)
            snapshot["execution"]["ep"] = "EP-STALE"
            dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", snapshot)
            self.assertTrue(validate(root))
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, drift="NONE")
            self.assertTrue(result["allowed"], result)

    def test_delivery_only_control_does_not_block_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            add_control(root, {
                "id": "CTRL-PROJECTION",
                "kind": "DELIVERY",
                "state": "OPEN",
                "source": {"type": "PROVIDER", "ref": "github:stale-projection"},
                "condition": "External projection is stale.",
                "blocks": ["HANDOVER", "PR_READY"],
                "permits": ["MATERIAL_WRITE", "TEST"],
                "resolution": {"condition": "Projection converges.", "evidence": []},
            })
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, drift="DISJOINT")
            self.assertTrue(result["allowed"], result)

    def test_write_collision_blocks_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            add_control(root, {
                "id": "CTRL-COLLISION",
                "kind": "COLLISION",
                "state": "OPEN",
                "source": {"type": "VALIDATOR", "ref": "exclusive-lease-check"},
                "condition": "Competing writer overlaps this serial route.",
                "blocks": ["MATERIAL_WRITE"],
                "permits": ["READ", "ANALYZE"],
                "resolution": {"condition": "Exclusive ownership restored.", "evidence": []},
            })
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, drift="DISJOINT")
            self.assertFalse(result["allowed"], result)
            self.assertIn("CONTROL_BLOCKS_ACTION", result["reason_codes"])
            self.assertEqual(["CTRL-COLLISION"], result["blocking_controls"])

    def test_relevant_and_unknown_drift_block_material_write(self):
        for drift, expected in (("RELEVANT", "DRIFT_RELEVANT"), ("UNKNOWN", "DRIFT_UNKNOWN")):
            with self.subTest(drift=drift), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                materialize(root)
                result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, drift=drift)
                self.assertFalse(result["allowed"], result)
                self.assertIn(expected, result["reason_codes"])

    def test_protected_or_out_of_scope_path_is_denied(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            result = evaluate(
                root,
                "MATERIAL_WRITE",
                path="skills/three-pass-prompt-generator/schema.md",
                drift="NONE",
            )
            self.assertFalse(result["allowed"], result)
            self.assertIn("PATH_OUTSIDE_EP_WRITE_SCOPE", result["reason_codes"])
            self.assertIn("PATH_PROTECTED", result["reason_codes"])

    def test_owner_override_allows_bounded_write_but_not_merge(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            import yaml
            lease_path = root / "relay/LEASES/LEASE-TA-011-01.yaml"
            lease = yaml.safe_load(lease_path.read_text(encoding="utf-8"))
            lease["admission"] = {
                "method": "OWNER_OVERRIDE",
                "result": "PASS",
                "repository_only": False,
                "qualification": {"required": False, "qset": None, "evaluator": None, "result": None},
                "owner_basis": {
                    "direct_utterance_digest": DIGEST,
                    "session_timestamp": "2026-09-22T03:29:06Z",
                },
            }
            lease["scope"] = {
                "ep_or_task": "EP-TA-011",
                "branch": "v3/issue-418-foundation",
                "allowed_writes": ["skills/engineering-pr-delivery-v3/**"],
                "prohibited": ["MERGE", "RELEASE"],
            }
            dump(lease_path, lease)

            write = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, drift="NONE")
            self.assertTrue(write["allowed"], write)

            state_path = root / "relay/STATE.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["delivery"] = {
                "required": True,
                "primary_vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
            }
            dump(state_path, state)
            add_control(root, owner_authority("MERGE"))
            merge = evaluate(root, "MERGE")
            self.assertFalse(merge["allowed"], merge)
            self.assertIn("OWNER_OVERRIDE_DELIVERY_FORBIDDEN", merge["reason_codes"])

    def test_merge_requires_explicit_owner_delivery_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            import yaml
            state_path = root / "relay/STATE.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["delivery"] = {
                "required": True,
                "primary_vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
            }
            dump(state_path, state)

            denied = evaluate(root, "MERGE")
            self.assertFalse(denied["allowed"], denied)
            self.assertEqual(["OWNER_DELIVERY_AUTHORITY_REQUIRED"], denied["reason_codes"])

            add_control(root, owner_authority("MERGE"))
            allowed = evaluate(root, "MERGE")
            self.assertTrue(allowed["allowed"], allowed)
            self.assertEqual(["ALLOW"], allowed["reason_codes"])

    def test_merge_requires_delivery_vehicle(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            add_control(root, owner_authority("MERGE"))
            result = evaluate(root, "MERGE")
            self.assertFalse(result["allowed"], result)
            self.assertIn("DELIVERY_VEHICLE_REQUIRED", result["reason_codes"])


if __name__ == "__main__":
    unittest.main()
