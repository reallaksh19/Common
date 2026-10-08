"""C6 legacy compatibility and explicit source transition over actual PLAN_HANDOVER.

Tests verify source is optional; passing never constitutes independent C6 approval.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
TESTS = ROOT / "skills/engineering-pr-delivery-v3.2/tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from handover_context import build_context, build_delp_source_bound_successor  # noqa: E402
from plan_handover import plan_handover  # noqa: E402
from test_handover_context import target_observation  # noqa: E402
from test_relay_can import prepare_git  # noqa: E402
from v3lib import load_yaml, load_events  # noqa: E402

ORACLE = json.loads(
    (Path(__file__).with_name("811-c6-runtime-red-golden-v1.json")).read_text(encoding="utf-8")
)


class RealC6RuntimeRedPrecommit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert ORACLE["schema"] == "common-v32-811-c6-runtime-red-golden-v1"
        assert ORACLE["release"] == "LEGACY_BASELINE_TRANSITION_TO_SOURCE_BOUND_CANDIDATE"
        assert [x["id"] for x in ORACLE["scenarios"]] == [f"R{i:02d}" for i in range(1, 6)]
        assert ORACLE["expected_release_state"] == "C6_PRODUCT_CANDIDATE_NOT_INDEPENDENT_ACCEPTANCE"

    @staticmethod
    def _run(root, base, *, count=None):
        return plan_handover(
            root, tx_id="TX-C6-RED-001", event_id="EVT-C6-RED-001",
            actor="owner", target_path=target_observation(root), base_ref=base,
            complex_mode=False, successor_challenge_count=count,
        )

    def test_r01_real_plan_handover_commits_without_delp_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            result = self._run(root, base)
            self.assertEqual("COMMITTED", result["status"])
            ctx = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            self.assertNotIn("source_bound_successor", ctx)
            self.assertNotIn("source_input_digest", ctx["successor_entry"]["challenge_basis"])
            self.assertEqual("RECONSTRUCT_PLAN_ONLY", ctx["successor_entry"]["mode"])
            self.assertEqual("OWNER_EXPLICIT_EXECUTION_ADMISSION",
                             ctx["successor_entry"]["execution_admission"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertEqual(1, len([e for e in events if e["type"] == "HANDOVER_PLANNED"]))

    def test_r02_real_transaction_rejects_existing_missing_source_input(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            from handover_context import HandoverContextError
            with self.assertRaises(HandoverContextError):
                plan_handover(
                    root, tx_id="TX-C6-RED-002", event_id="EVT-C6-RED-002",
                    actor="owner", target_path=target_observation(root),
                    base_ref=base, complex_mode=False,
                    delp_source={"graph": {}, "leaf_ref": "Common#793", "provider": None},
                )
            self.assertFalse((root / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists())

    def test_r03_actual_legacy_transaction_does_not_call_source_adapter(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            with patch("handover_context.build_delp_source_bound_successor",
                       side_effect=AssertionError("SOURCE_ADAPTER_SHOULD_NOT_RUN")) as source:
                result = self._run(root, base)
                self.assertEqual("COMMITTED", result["status"])
                source.assert_not_called()

    def test_r04_real_source_supports_opt_in_but_runtime_does_not(self):
        self.assertTrue(callable(build_delp_source_bound_successor))
        self.assertIn("delp_source", inspect.signature(build_context).parameters)
        self.assertIn("delp_source", inspect.signature(plan_handover).parameters)
        self.assertEqual("LEGACY_HANDOVER_UNBOUND_UNLESS_EXPLICIT_OPT_IN",
                         ORACLE["expected_currentness"])

    def test_r05_requested_real_successor_challenge_still_isnt_source_bound(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base = prepare_git(root)
            self.assertEqual("COMMITTED", self._run(root, base, count=3)["status"])
            ctx = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            entry = ctx["successor_entry"]
            self.assertEqual(3, len(entry["successor_reconstruction_challenge"]))
            self.assertNotIn("source_bound_successor", ctx)
            self.assertNotIn("source_plan_digest", entry["challenge_basis"])
            self.assertIn("TASK_EXECUTION", entry["forbidden_actions"])
            self.assertNotIn("owner_merge_authority", ctx)
            self.assertEqual("UNKNOWN", ORACLE["original_chat_message_permalink"])


if __name__ == "__main__":
    unittest.main()
