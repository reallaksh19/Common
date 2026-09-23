from __future__ import annotations

import shutil
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

from intelligence_projection import build_improvement, build_task
from relay_can import evaluate
from snapshot_projection import build as build_snapshot
from test_relay_can import WRITE_PATH, prepare_git
from v3lib import load_yaml
from validate_foundation import validate, validate_authority


class ArchitecturePreservationTests(unittest.TestCase):
    def test_generated_state_can_be_destroyed_and_reconstructed_from_durable_truth(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            before_snapshot = build_snapshot(root, base_ref)
            before_task = build_task(root, base_ref)
            before_improvement = build_improvement(root)
            before_write = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertTrue(before_write["allowed"], before_write)

            generated = root / "relay/GENERATED"
            shutil.rmtree(generated)

            # Generated read models are disposable. Their loss may make the full
            # repository projection incomplete, but durable authority remains valid
            # and synchronous authorization must not depend on them.
            self.assertEqual([], validate_authority(root))
            conformance_errors = validate(root)
            self.assertTrue(
                any("SNAPSHOT: cannot load" in item for item in conformance_errors),
                conformance_errors,
            )

            after_write = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertEqual(before_write["allowed"], after_write["allowed"])
            self.assertEqual(before_write["reason_codes"], after_write["reason_codes"])

            after_snapshot = build_snapshot(root, base_ref)
            after_task = build_task(root, base_ref)
            after_improvement = build_improvement(root)

            # Reconstructed programme, custody, evidence and task truth are stable.
            for key in ("owner", "programme", "execution", "scope", "evidence", "controls", "delivery", "next"):
                self.assertEqual(before_snapshot[key], after_snapshot[key], key)
            for key in ("identity", "purpose", "lineage", "scope", "execution", "acceptance", "knowledge_state", "preserve", "next"):
                self.assertEqual(before_task[key], after_task[key], key)
            for key in ("task", "checkpoint", "from", "to", "improvement", "roadmap_effect", "still_not_proved"):
                self.assertEqual(before_improvement[key], after_improvement[key], key)

            state = load_yaml(root / "relay/STATE.yaml")
            snapshot_path = root / str((state.get("generated") or {}).get("snapshot"))
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            import yaml
            snapshot_path.write_text(
                yaml.safe_dump(after_snapshot, sort_keys=False),
                encoding="utf-8",
            )
            self.assertEqual([], validate(root))

    def test_generated_snapshot_cannot_grant_authority_missing_from_durable_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            state_path = root / "relay/STATE.yaml"
            state = load_yaml(state_path)
            state["execution"] = {
                "lifecycle": "IDLE",
                "ep": None,
                "lease": None,
                "route": None,
            }
            import yaml
            state_path.write_text(yaml.safe_dump(state, sort_keys=False), encoding="utf-8")

            # Leave the generated snapshot untouched: it still claims ACTIVE.
            denied = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertFalse(denied["allowed"], denied)
            self.assertIn("NO_ACTIVE_EXECUTION", denied["reason_codes"])
            self.assertIn("NO_ACTIVE_LEASE", denied["reason_codes"])

    def test_preservation_contract_keeps_execution_safety_outside_provider_projection(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            # Provider/read-model absence is coordination quality, not execution
            # authority. Product writes remain governed by durable custody, scope
            # and material drift only.
            for name in (
                "HANDOVER_CONTEXT.yaml",
                "HANDOVER_LEDGER.yaml",
                "HANDOVER_PROVIDER_STATUS.yaml",
                "PARENT_RELAY_SUMMARY.md",
                "TASK_SNAPSHOT.yaml",
                "IMPROVEMENT_VIEW.yaml",
            ):
                path = root / "relay/GENERATED" / name
                if path.exists():
                    path.unlink()

            allowed = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertTrue(allowed["allowed"], allowed)


if __name__ == "__main__":
    unittest.main()
