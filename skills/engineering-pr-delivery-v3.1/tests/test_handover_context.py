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
from test_v3_foundation import DIGEST, dump
from transactionlib import TransactionError
from v3lib import canonical_digest, load_events, load_yaml
from validate_foundation import validate


STANDALONE = ROOT.parent / "three-pass-prompt-generator"


def install_standalone(root: Path) -> None:
    target = root / "skills/three-pass-prompt-generator"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("SKILL.md", "schema.md", "validate.py"):
        shutil.copyfile(STANDALONE / name, target / name)


def target_observation(root: Path, *, kind: str = "ISSUE", number: int = 418) -> Path:
    target = {
        "schema_version": "relay-v3.1-handover-target",
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


def install_parent_issue(root: Path, *, number: int = 1771) -> dict:
    baseline = {
        "observed_at": "2026-09-22T00:00:00Z",
        "body_digest": DIGEST,
        "acceptance_items": [
            {"id": "PI-1", "statement": "Deliver the bounded provider-backed task."},
        ],
    }
    ep_path = root / "relay/WORK/EP-TA-011.yaml"
    ep = load_yaml(ep_path)
    ep["parent_issue"] = {
        "provider": "GITHUB",
        "repository": "example/project",
        "number": number,
        "title": "Provider-backed programme task",
        "url": f"https://github.com/example/project/issues/{number}",
        "baseline": baseline,
    }
    dump(ep_path, ep)
    return baseline


def parent_issue_observation(
    *,
    baseline: dict,
    number: int = 1771,
    state: str = "OPEN",
    disposition: str = "NO_CHANGE",
    acceptance_state: str | None = None,
) -> dict:
    acceptance_state = acceptance_state or ("COMPLETE" if state == "CLOSED" else "PENDING")
    return {
        "schema_version": "relay-v3.1-parent-issue-observation",
        "authority": "DERIVED_PROVIDER_OBSERVATION",
        "provider": "GITHUB",
        "repository": "example/project",
        "issue_number": number,
        "title": "Provider-backed programme task",
        "url": f"https://github.com/example/project/issues/{number}",
        "state": state,
        "observed_at": "2026-09-23T00:30:00Z",
        "baseline": baseline,
        "current_contract": {
            "body_digest": DIGEST,
            "acceptance_items": [{
                "id": "PI-1",
                "statement": "Deliver the bounded provider-backed task.",
                "state": acceptance_state,
                "evidence": ["provider-readback"] if acceptance_state == "COMPLETE" else [],
                "provider_refs": [f"issue-{number}"],
            }],
        },
        "updates": [],
        "disposition": disposition,
        "relationships": [],
        "handover_ledger": None,
    }


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
                reason="ADMINISTRATIVE",
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
            self.assertEqual("V3_1", learning["task_snapshot"]["source_protocol"])
            self.assertEqual("EP-TA-011", learning["task_snapshot"]["ep"])
            self.assertEqual("WP-TA-109", learning["task_snapshot"]["work_package"])
            self.assertTrue(learning["task_snapshot"]["digest"].startswith("sha256:"))
            self.assertEqual("V3_1", learning["improvement_view"]["source_protocol"])
            self.assertEqual("CP-TA-010", learning["improvement_view"]["checkpoint"])
            self.assertTrue(learning["improvement_view"]["digest"].startswith("sha256:"))

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
            task_meta = context["accumulated_learning"]["task_snapshot"]
            improvement_meta = context["accumulated_learning"]["improvement_view"]
            task_snapshot = task_meta["value"]
            improvement_view = improvement_meta["value"]
            self.assertEqual("DERIVED_READ_MODEL", task_snapshot["authority"])
            self.assertEqual("DERIVED_READ_MODEL", improvement_view["authority"])
            self.assertEqual(task_meta["ep"], task_snapshot["identity"]["ep"])
            self.assertEqual(improvement_meta["checkpoint"], improvement_view["checkpoint"])
            self.assertEqual(task_meta["digest"], canonical_digest(task_snapshot))
            self.assertEqual(improvement_meta["digest"], canonical_digest(improvement_view))
            self.assertFalse((root / "relay/GENERATED/tasks").exists())
            self.assertFalse((root / "relay/GENERATED/improvements").exists())
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

    def test_parent_backed_handover_allocates_bookkeeping_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            baseline = install_parent_issue(root)
            observation = parent_issue_observation(
                baseline=baseline,
                state="OPEN",
                disposition="NO_CHANGE",
            )

            result = plan_handover(
                root,
                tx_id=None,
                event_id=None,
                actor="agent-x",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
                parent_issue_observation=observation,
            )

            self.assertEqual("COMMITTED", result["status"])
            self.assertEqual("TX.1771.1", result["id"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            planned = [row for row in events if row["type"] == "HANDOVER_PLANNED"][-1]
            self.assertEqual("EVT.1771.1", planned["event_id"])

    def test_parent_backed_handover_records_missing_programme_observation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            install_parent_issue(root)

            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-CURRENTNESS-MISSING",
                event_id="EVT-HANDOVER-CURRENTNESS-MISSING",
                actor="agent-x",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
            )
            self.assertEqual("COMMITTED", result["status"])
            context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            self.assertEqual(
                "NOT_REQUIRED",
                context["blind_context"]["programme"]["reconciliation"]["status"],
            )

    def test_closed_parent_reconciliation_debt_does_not_block_handover_recording(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            baseline = install_parent_issue(root)
            observation = parent_issue_observation(
                baseline=baseline,
                state="CLOSED",
                disposition="CLOSE",
            )

            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-STALE-PARENT",
                event_id="EVT-HANDOVER-STALE-PARENT",
                actor="agent-x",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
                parent_issue_observation=observation,
            )
            self.assertEqual("COMMITTED", result["status"])
            self.assertTrue((root / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists())

    def test_stale_current_parent_can_handover_after_explicit_programme_reconciliation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            baseline = install_parent_issue(root, number=1771)
            completed = parent_issue_observation(
                baseline=baseline,
                number=1771,
                state="CLOSED",
                disposition="CLOSE",
                acceptance_state="COMPLETE",
            )
            next_parent = parent_issue_observation(
                baseline=baseline,
                number=1772,
                state="OPEN",
                disposition="NO_CHANGE",
                acceptance_state="PENDING",
            )

            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-PROGRAMME-RECONCILED",
                event_id="EVT-HANDOVER-PROGRAMME-RECONCILED",
                actor="agent-x",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=True,
                programme_issue_observations=[completed, next_parent],
            )
            self.assertEqual("COMMITTED", result["status"])

            context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            reconciliation = context["blind_context"]["programme"]["reconciliation"]
            self.assertEqual("READY", reconciliation["status"])
            self.assertEqual(
                ["example/project#1772"],
                reconciliation["programme_frontier"],
            )
            self.assertEqual(
                "LANDED",
                reconciliation["ordered_roadmap"][0]["ownership"],
            )
            self.assertEqual(
                "STILL_REAL",
                reconciliation["ordered_roadmap"][1]["ownership"],
            )

    def test_open_unchanged_parent_can_plan_handover(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            baseline = install_parent_issue(root)
            observation = parent_issue_observation(
                baseline=baseline,
                state="OPEN",
                disposition="NO_CHANGE",
            )

            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-CURRENT-PARENT",
                event_id="EVT-HANDOVER-CURRENT-PARENT",
                actor="agent-x",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
                parent_issue_observation=observation,
            )
            self.assertEqual("COMMITTED", result["status"])
            self.assertTrue((root / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists())


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

    def test_handover_control_is_advisory_and_plan_still_records(self):
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
            handover_diag = can_action(root, "HANDOVER")
            self.assertTrue(handover_diag["allowed"], handover_diag)
            self.assertIn("CONTROL_BLOCKS_ACTION", handover_diag["reason_codes"])

            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-BLOCKED",
                event_id="EVT-HANDOVER-BLOCKED",
                actor="owner",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
            )
            self.assertEqual("COMMITTED", result["status"])

