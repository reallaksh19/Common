from __future__ import annotations

import copy
import shutil
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

from handover_context import build_context, build_request, render_request, validate_visibility
from plan_handover import plan_handover
from relay_can import evaluate as can_action
from relay_tx import release_lease
from test_relay_can import WRITE_PATH, add_control, prepare_git
from test_v3_foundation import dump
from transactionlib import TransactionError
from v3lib import load_events, load_yaml
from validate_foundation import validate


STANDALONE = ROOT.parent / "three-pass-prompt-generator"


def install_standalone(root: Path) -> None:
    target = root / "skills/three-pass-prompt-generator"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("SKILL.md", "schema.md", "validate.py"):
        shutil.copyfile(STANDALONE / name, target / name)


def target_observation(root: Path, *, kind: str = "ISSUE", number: int = 418) -> Path:
    target = {
        "schema_version": "relay-v3-handover-target",
        "authority": "PROVIDER_READBACK",
        "provider": "GITHUB",
        "repository": "example/project",
        "kind": kind,
        "number": number,
        "title": "Synthetic provider-verified handover target",
        "url": f"https://github.com/example/project/{'issues' if kind == 'ISSUE' else 'pull'}/{number}",
        "state": "OPEN" if kind == "ISSUE" else "DRAFT",
        "observed_at": "2026-09-22T03:57:35Z",
        "provider_ref": f"github:example/project#{number}",
    }
    path = root / "provider-target.yaml"
    dump(path, target)
    return path


class HandoverContextTests(unittest.TestCase):
    def test_rich_reality_is_structurally_quarantined_from_blind_context(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target = load_yaml(target_observation(root, kind="PULL_REQUEST", number=419))
            context, _ = build_context(
                root,
                base_ref=base_ref,
                target=target,
                complex_mode=True,
            )

            blind_text = yaml.safe_dump(context["blind_context"], sort_keys=True)
            reality = context["reality_context"]
            self.assertEqual([], validate_visibility(context))
            self.assertEqual("LEASE-TA-011-01", reality["execution"]["lease"])
            self.assertEqual("agent-x", reality["execution"]["executor"])
            self.assertEqual("exec", reality["execution"]["branch"])
            self.assertNotIn("LEASE-TA-011-01", blind_text)
            self.assertNotIn("agent-x", blind_text)
            self.assertNotIn("branch:", blind_text.lower())
            self.assertNotIn("pull request", blind_text.lower())
            self.assertNotIn("419", blind_text)
            self.assertEqual("TPG-3P-2026-09-22-R10", context["generator_contract"]["protocol_revision_at_freeze"])

    def test_post_release_handover_keeps_checkpoint_task_context_while_reality_is_idle(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            historical_ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
            historical_ep["id"] = "EP-TA-010"
            dump(root / "relay/WORK/EP-TA-010.yaml", historical_ep)
            release_lease(
                root,
                tx_id="TX-RELEASE-HANDOVER",
                event_id="EVT-RELEASE-HANDOVER",
                actor="agent-x",
            )

            target = load_yaml(target_observation(root))
            context, _ = build_context(
                root,
                base_ref=base_ref,
                target=target,
                complex_mode=True,
            )
            self.assertEqual("IDLE", context["reality_context"]["execution"]["lifecycle"])
            self.assertIsNone(context["reality_context"]["execution"]["ep"])
            self.assertEqual("WP-TA-109", context["blind_context"]["local_responsibility"]["work_package"])
            self.assertIn(
                "Foundation objects validate deterministically.",
                context["blind_context"]["local_responsibility"]["acceptance_statements"],
            )
            self.assertIn(
                "Do not make V3 the default protocol in this slice.",
                context["blind_context"]["stable_constraints"],
            )

    def test_complex_request_preserves_exact_five_prompt_contract_and_q1_q5(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target = load_yaml(target_observation(root))
            context, _ = build_context(root, base_ref=base_ref, target=target, complex_mode=True)
            request = build_request(context)
            self.assertEqual(
                ["PROMPT_0_5", "PROMPT_1", "PROMPT_2", "PROMPT_2_5", "PROMPT_3"],
                request["generator"]["prompt_sequence"],
            )
            self.assertTrue(request["generator"]["live_main_fetch_required"])
            self.assertTrue(request["generator"]["complex_mode"])
            self.assertTrue(request["generator"]["prompt1_q1_q5_required"])
            rendered = render_request(request)
            self.assertIn("Fetch skills/three-pass-prompt-generator/schema.md from current main", rendered)
            self.assertIn("COMPLEX MODE: ON", rendered)
            self.assertIn("grants no new action authority", rendered)

    def test_non_complex_request_still_has_five_prompts_without_forcing_q1_q5(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target = load_yaml(target_observation(root))
            context, _ = build_context(root, base_ref=base_ref, target=target, complex_mode=False)
            request = build_request(context)
            self.assertEqual(5, len(request["generator"]["prompt_sequence"]))
            self.assertFalse(request["generator"]["complex_mode"])
            self.assertFalse(request["generator"]["prompt1_q1_q5_required"])
            self.assertIn("COMPLEX MODE: OFF", render_request(request))

    def test_checkpoint_learning_is_carried_as_history_not_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target = load_yaml(target_observation(root))
            context, _ = build_context(root, base_ref=base_ref, target=target, complex_mode=False)
            learning = context["accumulated_learning"]
            self.assertEqual("CP-TA-010", learning["checkpoint"])
            self.assertIn("V3 foundation accepted.", learning["discoveries"])
            self.assertIn("Foundation schema established.", learning["what_changed"])
            self.assertIn("V2.5 remains live.", learning["do_not_break"])
            self.assertEqual("Read CURRENT_SNAPSHOT and EP.", learning["first_successor_action"])

    def test_visibility_validator_rejects_reality_leak_into_blind_context(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target = load_yaml(target_observation(root))
            context, _ = build_context(root, base_ref=base_ref, target=target, complex_mode=False)
            bad = copy.deepcopy(context)
            bad["blind_context"]["stable_constraints"].append(
                f"Continue on branch {context['reality_context']['execution']['branch']} under lease {context['reality_context']['execution']['lease']}."
            )
            errors = validate_visibility(bad)
            self.assertTrue(any("reality-only token" in item or "leaks current" in item for item in errors), errors)

    def test_plan_handover_transaction_publishes_context_and_generator_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target_path = target_observation(root)
            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-PLAN-001",
                event_id="EVT-HANDOVER-PLAN-001",
                actor="owner",
                target_path=target_path,
                base_ref=base_ref,
                complex_mode=True,
            )
            self.assertEqual("COMMITTED", result["status"])
            context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            request = load_yaml(root / "relay/GENERATED/THREE_PASS_REQUEST.yaml")
            request_text = (root / "relay/GENERATED/THREE_PASS_REQUEST.md").read_text(encoding="utf-8")
            self.assertEqual("DERIVED_HANDOVER_INPUT", context["authority"])
            self.assertEqual("PROVIDER_READBACK", context["target"]["authority"])
            self.assertEqual("DERIVED_GENERATOR_REQUEST", request["authority"])
            self.assertEqual(5, len(request["generator"]["prompt_sequence"]))
            self.assertTrue(request["generator"]["prompt1_q1_q5_required"])
            self.assertIn("current main", request_text)
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertIn("EVT-HANDOVER-PLAN-001", [item["event_id"] for item in events])
            self.assertEqual([], validate(root))

    def test_unverified_target_fails_without_changing_execution_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target_path = target_observation(root)
            target = load_yaml(target_path)
            target["authority"] = "DERIVED_READ_MODEL"
            dump(target_path, target)

            before = can_action(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertTrue(before["allowed"], before)
            with self.assertRaises(TransactionError):
                plan_handover(
                    root,
                    tx_id="TX-HANDOVER-BADTARGET",
                    event_id="EVT-HANDOVER-BADTARGET",
                    actor="owner",
                    target_path=target_path,
                    base_ref=base_ref,
                    complex_mode=True,
                )
            after = can_action(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertTrue(after["allowed"], after)
            self.assertFalse((root / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists())

    def test_handover_only_control_blocks_plan_but_not_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            add_control(root, {
                "id": "CTRL-HANDOVER-ONLY",
                "kind": "DELIVERY",
                "state": "OPEN",
                "source": {"type": "VALIDATOR", "ref": "handover-target"},
                "condition": "Handover publication is not ready.",
                "blocks": ["HANDOVER"],
                "permits": ["MATERIAL_WRITE", "TEST"],
                "resolution": {"condition": "Handover target is ready.", "evidence": []},
            })
            write = can_action(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertTrue(write["allowed"], write)
            with self.assertRaisesRegex(TransactionError, "HANDOVER denied"):
                plan_handover(
                    root,
                    tx_id="TX-HANDOVER-BLOCKED",
                    event_id="EVT-HANDOVER-BLOCKED",
                    actor="owner",
                    target_path=target_observation(root),
                    base_ref=base_ref,
                    complex_mode=False,
                )
            write_after = can_action(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertTrue(write_after["allowed"], write_after)


if __name__ == "__main__":
    unittest.main()
