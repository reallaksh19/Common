from __future__ import annotations

import json
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

from protocol_default import resolve as resolve_protocol
from relay_can import evaluate
from relay_tx import activate_lease
from test_relay_can import WRITE_PATH, git, prepare_git
from test_v3_foundation import DIGEST, dump
from v25_migration import legacy_inventory
from v3lib import canonical_digest, load_yaml
from validate_foundation import validate


def _to_v3_schema(value):
    if not isinstance(value, dict):
        return value
    version = str(value.get("schema_version") or "")
    if version == "relay-v3.1":
        value["schema_version"] = "relay-v3"
    elif version.startswith("relay-v3.1-"):
        value["schema_version"] = "relay-v3-" + version[len("relay-v3.1-"):]
    return value


def make_native_v3_active(root: Path) -> None:
    for path in [
        root / "relay/ROADMAP/ROADMAP.yaml",
        root / "relay/STATE.yaml",
        root / "relay/WORK/EP-TA-011.yaml",
        root / "relay/LEASES/LEASE-TA-011-01.yaml",
        root / "relay/CHECKPOINTS/CP-TA-010.yaml",
        root / "relay/CONTROLS/controls.yaml",
        root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml",
    ]:
        value = load_yaml(path)
        _to_v3_schema(value)
        dump(path, value)

    state = load_yaml(root / "relay/STATE.yaml")
    snapshot_path = root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml"
    snapshot = load_yaml(snapshot_path)
    snapshot["generated_from"]["state_digest"] = canonical_digest(state)
    dump(snapshot_path, snapshot)

    event_path = root / "relay/EVENTS.jsonl"
    rows = []
    for raw in event_path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        row = json.loads(raw)
        _to_v3_schema(row)
        rows.append(row)
    event_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")

    legacy_file = root / "agents/relay/HISTORY.txt"
    legacy_file.parent.mkdir(parents=True, exist_ok=True)
    legacy_file.write_text("frozen V2.5 history\n", encoding="utf-8")
    _, legacy_digest = legacy_inventory(root)

    selection = {
        "schema_version": "relay-v3-protocol-selection",
        "selected_protocol": "V3",
        "status": "ACTIVE",
        "legacy": {
            "root": "agents/relay",
            "tree_digest": legacy_digest,
            "policy": "READ_ONLY_HISTORY",
        },
        "v3": {
            "state_path": "relay/STATE.yaml",
            "validation": "PASS",
        },
        "cutover": {
            "owner_authorized": True,
            "owner_basis": {
                "direct_utterance_digest": DIGEST,
                "session_timestamp": "2026-09-22T20:00:00Z",
            },
            "legacy_freeze_digest": legacy_digest,
            "readiness_digest": DIGEST,
            "activated_at": "2026-09-22T20:00:00Z",
        },
    }
    dump(root / "relay/PROTOCOL_SELECTION.yaml", selection)
    notice = root / "relay/MIGRATION/V25_DEPRECATION.md"
    notice.parent.mkdir(parents=True, exist_ok=True)
    notice.write_text("# V2.5 read-only history\n", encoding="utf-8")

    git(root, "add", ".")
    git(root, "commit", "-m", "represent existing native V3 authority")


class NativeV3CompatibilityTests(unittest.TestCase):
    def test_active_v3_uses_current_v31_tooling_without_protocol_migration(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            make_native_v3_active(root)

            self.assertEqual([], validate(root))
            resolved = resolve_protocol(root)
            self.assertEqual("V3_1", resolved["selected_protocol"])
            self.assertEqual("V3", resolved["repository_protocol"])
            self.assertEqual("ACTIVE", resolved["status"])
            self.assertEqual("skills/engineering-pr-delivery-v3.1/SKILL.md", resolved["skill"])
            self.assertIn("without rewriting accepted history", resolved["warning"])

            allowed = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertTrue(allowed["allowed"], allowed)
            self.assertTrue(
                any(item == "protocol:V3:ACTIVE:COMPATIBLE_NATIVE_CORE" for item in allowed["basis"]),
                allowed,
            )

            before_selector = (root / "relay/PROTOCOL_SELECTION.yaml").read_bytes()
            before_checkpoint = (root / "relay/CHECKPOINTS/CP-TA-010.yaml").read_bytes()
            result = activate_lease(
                root,
                tx_id="TX-COMPAT-NEXT-LEASE",
                event_id="EVT-COMPAT-NEXT-LEASE",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-x",
                actor="agent-x",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref="base",
            )
            self.assertEqual("COMMITTED", result["status"])

            self.assertEqual(before_selector, (root / "relay/PROTOCOL_SELECTION.yaml").read_bytes())
            self.assertEqual(before_checkpoint, (root / "relay/CHECKPOINTS/CP-TA-010.yaml").read_bytes())
            state = load_yaml(root / "relay/STATE.yaml")
            lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-02.yaml")
            self.assertEqual("relay-v3", state["schema_version"])
            self.assertEqual(1, state["execution"]["custody_epoch"])
            self.assertEqual("relay-v3.1-lease", lease["schema_version"])
            self.assertEqual(1, lease["custody"]["epoch"])
            self.assertEqual([], validate(root))

    def test_invalid_native_v3_still_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            make_native_v3_active(root)
            state_path = root / "relay/STATE.yaml"
            state = load_yaml(state_path)
            state["roadmap"]["revision"] = "WRONG"
            dump(state_path, state)

            resolved = resolve_protocol(root)
            self.assertEqual("INVALID", resolved["status"])
            denied = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertFalse(denied["allowed"], denied)
            self.assertIn("INVALID_FOUNDATION", denied["reason_codes"])


if __name__ == "__main__":
    unittest.main()
