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

from handover_context import (
    HandoverContextError,
    _protocol_checkout_root,
    _standalone_contract,
    build_context,
    build_request,
    render_request,
    validate_visibility,
)
from plan_handover import plan_handover
from relay_can import evaluate as can_action
from relay_tx import release_lease
from test_relay_can import WRITE_PATH, add_control, prepare_git
from test_v3_foundation import DIGEST, dump
from transactionlib import TransactionError
from v3lib import canonical_digest, load_events, load_yaml, validate_schema
from validate_foundation import validate


STANDALONE = ROOT.parent / "two-pass-prompt-generator"


def install_standalone(root: Path) -> None:
    target = root / "skills/two-pass-prompt-generator"
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
            self.assertNotIn("work_package", blind_text.lower())
            self.assertNotIn("selected_frontier", blind_text.lower())
            self.assertNotIn("acceptance_statements", blind_text.lower())
            self.assertNotIn("Do not make V3 the default protocol in this slice.", blind_text)
            self.assertEqual(
                {"outcome", "roadmap_title"},
                set(context["blind_context"]["programme"]),
            )
            self.assertNotIn("generator_contract", context)

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
            self.assertEqual("WP-TA-109", context["reality_context"]["local_responsibility"]["work_package"])
            self.assertIn(
                "Foundation objects validate deterministically.",
                context["reality_context"]["local_responsibility"]["acceptance_statements"],
            )
            self.assertIn(
                "Do not make V3 the default protocol in this slice.",
                context["reality_context"]["task_constraints"],
            )
            self.assertEqual([], context["blind_context"]["stable_constraints"])


    def test_complex_request_preserves_exact_two_pass_contract_and_approval_boundary(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target = load_yaml(target_observation(root))
            context, _ = build_context(root, base_ref=base_ref, target=target, complex_mode=True)
            self.assertNotIn("generator_contract", context)
            request = build_request(context, complex_mode=True)
            self.assertEqual(
                ["PASS_1_SYSTEM_BASELINE", "PASS_2_IMPROVE_RECONCILE_PLAN"],
                request["generator"]["prompt_sequence"],
            )
            self.assertTrue(request["generator"]["live_main_fetch_required"])
            self.assertTrue(request["generator"]["complex_mode"])
            self.assertTrue(request["generator"]["approval_boundary_required"])
            rendered = render_request(request)
            self.assertIn("Fetch skills/two-pass-prompt-generator/schema.md from current main", rendered)
            self.assertIn("DEEP MODE: ON", rendered)
            self.assertIn("grant no production authority", rendered)


    def test_non_complex_request_still_has_two_passes_and_approval_boundary(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target = load_yaml(target_observation(root))
            context, _ = build_context(root, base_ref=base_ref, target=target, complex_mode=False)
            self.assertNotIn("generator_contract", context)
            request = build_request(context, complex_mode=False)
            self.assertEqual(2, len(request["generator"]["prompt_sequence"]))
            self.assertFalse(request["generator"]["complex_mode"])
            self.assertTrue(request["generator"]["approval_boundary_required"])
            self.assertIn("DEEP MODE: OFF", render_request(request))

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
            self.assertEqual(
                {
                    "original_intent": None,
                    "latest_reconciliation": None,
                    "primary_conversation_refs": [],
                    "roadmap_refs": [],
                    "local_agent_refs": [],
                    "rll_refs": [],
                },
                learning["reconstruction_context"],
            )

    def test_reconstruction_context_is_explicit_for_pass2_and_absent_from_blind_context(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            target = load_yaml(target_observation(root))

            initial, _ = build_context(
                root,
                base_ref=base_ref,
                target=target,
                complex_mode=False,
            )
            task_snapshot = copy.deepcopy(initial["accumulated_learning"]["task_snapshot"]["value"])
            task_snapshot["reconstruction_context"] = {
                "original_intent": {
                    "repository": "example/project",
                    "issue_number": 1700,
                    "url": "https://github.com/example/project/issues/1700",
                    "source_ref": "github:example/project#1700/body",
                    "digest": "sha256:" + ("a" * 64),
                },
                "latest_reconciliation": {
                    "ref": "github:example/project#1771/comment-reconcile",
                    "observed_at": "2026-09-28T10:00:00Z",
                    "summary": "Current responsibility remains aligned with effective Owner intent.",
                },
                "primary_conversation_refs": ["github:example/project#1771/comment-context"],
                "roadmap_refs": ["RM-1771"],
                "local_agent_refs": ["github:example/project#1780"],
                "rll_refs": ["github:example/project#1771/comment-rll-state"],
            }
            task_snapshot["continuity"] = {
                "current": {
                    "ref": "github:example/project#1771/comment-status",
                    "custody_epoch": 4,
                    "executor": "agent-successor",
                    "status": "ACTIVE",
                    "continuation": "RECOVERY",
                    "exact_head": "material-head",
                    "updated_at": "2026-09-28T10:05:00Z",
                },
                "further_tasks": [
                    {
                        "id": "FT-1771-1",
                        "state": "PENDING",
                        "statement": "Revalidate exact-head evidence.",
                        "reason_class": "CURRENT_TASK",
                        "dependency": None,
                        "expected_next_observable": "Exact-head evidence result.",
                    }
                ],
                "predecessor_ref": "github:example/project#1771/comment-old-status",
            }

            context, _ = build_context(
                root,
                base_ref=base_ref,
                target=target,
                complex_mode=False,
                task_snapshot_override=task_snapshot,
                improvement_view_override=initial["accumulated_learning"]["improvement_view"]["value"],
            )

            reconstruction = context["accumulated_learning"]["reconstruction_context"]
            self.assertEqual(1700, reconstruction["original_intent"]["issue_number"])
            self.assertEqual(
                "github:example/project#1771/comment-reconcile",
                reconstruction["latest_reconciliation"]["ref"],
            )
            self.assertEqual(["github:example/project#1780"], reconstruction["local_agent_refs"])
            self.assertEqual(["github:example/project#1771/comment-rll-state"], reconstruction["rll_refs"])
            continuity = context["accumulated_learning"]["continuity"]
            self.assertEqual(4, continuity["current"]["custody_epoch"])
            self.assertEqual("RECOVERY", continuity["current"]["continuation"])
            self.assertEqual("FT-1771-1", continuity["further_tasks"][0]["id"])

            blind_text = yaml.safe_dump(context["blind_context"], sort_keys=True)
            self.assertNotIn("1700", blind_text)
            self.assertNotIn("comment-reconcile", blind_text)
            self.assertNotIn("comment-context", blind_text)
            self.assertNotIn("comment-rll-state", blind_text)
            self.assertNotIn("comment-status", blind_text)
            self.assertNotIn("FT-1771-1", blind_text)
            self.assertEqual([], validate_visibility(context))

            request = build_request(context)
            rendered = render_request(request)
            self.assertIn("STEP-BACK RECONCILIATION", rendered)
            self.assertIn("Original Intent", rendered)
            self.assertIn("Local Agent/OFFLOAD", rendered)
            self.assertIn("RLL transport", rendered)
            self.assertIn("AGENT_STATUS_V1", rendered)
            self.assertIn("Further task", rendered)



    def test_default_handover_entry_is_conservative_even_without_a_requested_challenge(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            context, _ = build_context(
                root,
                base_ref=base_ref,
                target=load_yaml(target_observation(root)),
                complex_mode=False,
            )
            entry = context["successor_entry"]
            self.assertEqual("RECONSTRUCT_PLAN_ONLY", entry["mode"])
            self.assertEqual([], entry["successor_reconstruction_challenge"])
            self.assertEqual("OWNER_EXPLICIT_EXECUTION_ADMISSION", entry["execution_admission"])
            for forbidden in ("QUALIFICATION", "RETAINED_VALIDATION", "PRODUCTION_MUTATION", "PR_CREATION", "TASK_EXECUTION"):
                self.assertIn(forbidden, entry["forbidden_actions"])

    def test_plan_handover_materializes_exactly_three_repo_grounded_entry_exam_questions(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-CHALLENGE-001",
                event_id="EVT-HANDOVER-CHALLENGE-001",
                actor="owner",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
                successor_challenge_count=3,
            )
            self.assertEqual("COMMITTED", result["status"])
            context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            entry = context["successor_entry"]
            challenge = entry["successor_reconstruction_challenge"]
            self.assertEqual(3, len(challenge))
            self.assertEqual(["Q1", "Q2", "Q3"], [q["id"] for q in challenge])
            self.assertIn("files/functions", challenge[0]["question"])
            self.assertIn("authority", challenge[1]["question"].lower())
            self.assertIn("upstream and downstream", challenge[2]["question"].lower())
            for q in challenge:
                self.assertTrue(q["decision_at_risk"])
                self.assertIn("github:example/project#418", q["repository_anchors"])
                self.assertTrue(any(str(a).startswith("material_head:") for a in q["repository_anchors"]))
                self.assertTrue(q["required_evidence"])
                self.assertTrue(q["authority_distinctions"])
                self.assertTrue(q["falsifier"])
                self.assertTrue(q["pass_condition"])
                self.assertTrue(q["fail_condition"])
                self.assertTrue(q["forbidden_shortcuts"])
                self.assertTrue(q["downstream_consequence"])
            self.assertEqual("DERIVED_HANDOVER_INPUT", context["authority"])
            self.assertFalse((root / "relay/GENERATED/TWO_PASS_REQUEST.yaml").exists())
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            planned = [row for row in events if row["event_id"] == "EVT-HANDOVER-CHALLENGE-001"][0]
            self.assertEqual("RECONSTRUCT_PLAN_ONLY", planned["details"]["successor_entry_mode"])
            self.assertEqual(3, planned["details"]["successor_challenge_count"])
            self.assertFalse(planned["details"]["reasoning_request_generated"])
            self.assertEqual([], validate(root))

    def test_successor_challenge_count_is_bounded_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            target = load_yaml(target_observation(root))
            for bad in (-1, 11, True):
                with self.subTest(bad=bad), self.assertRaises(HandoverContextError):
                    build_context(
                        root,
                        base_ref=base_ref,
                        target=target,
                        complex_mode=False,
                        successor_challenge_count=bad,
                    )

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


    def test_plan_handover_transaction_publishes_custody_context_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
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
            self.assertNotIn("generator_contract", context)
            self.assertFalse((root / "relay/GENERATED/TWO_PASS_REQUEST.yaml").exists())
            self.assertFalse((root / "relay/GENERATED/TWO_PASS_REQUEST.md").exists())
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            planned = [item for item in events if item["event_id"] == "EVT-HANDOVER-PLAN-001"][0]
            self.assertFalse(planned["details"]["reasoning_request_generated"])
            self.assertNotIn("complex_mode", planned["details"])
            self.assertNotIn("prompt_count", planned["details"])
            self.assertNotIn("generator_mode", planned["details"])
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
                context["reality_context"]["programme_reconciliation"]["status"],
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
            reconciliation = context["reality_context"]["programme_reconciliation"]
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


    def test_handover_context_does_not_resolve_generator_assets(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as bad_proto:
            root = Path(td)
            _, base_ref = prepare_git(root)
            self.assertFalse((root / "skills/two-pass-prompt-generator").exists())
            target = load_yaml(target_observation(root, kind="PULL_REQUEST", number=420))
            context, _ = build_context(
                root,
                base_ref=base_ref,
                target=target,
                complex_mode=True,
                protocol_root=Path(bad_proto),
            )
            self.assertFalse((root / "skills/two-pass-prompt-generator").exists())
            self.assertNotIn("generator_contract", context)
            self.assertEqual([], validate_visibility(context))


    def test_plan_handover_succeeds_without_two_pass_assets_and_emits_no_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            self.assertFalse((root / "skills/two-pass-prompt-generator").exists())
            target_path = target_observation(root)
            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-UNVENDORED-001",
                event_id="EVT-HANDOVER-UNVENDORED-001",
                actor="owner",
                target_path=target_path,
                base_ref=base_ref,
                complex_mode=True,
            )
            self.assertEqual("COMMITTED", result["status"])
            self.assertTrue((root / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists())
            self.assertFalse((root / "relay/GENERATED/TWO_PASS_REQUEST.yaml").exists())
            self.assertFalse((root / "relay/GENERATED/TWO_PASS_REQUEST.md").exists())
            self.assertFalse((root / "skills/two-pass-prompt-generator").exists())
            context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            self.assertNotIn("generator_contract", context)
            self.assertEqual([], validate(root))


    def test_legacy_generator_contract_remains_readable_but_not_authoritative(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            target = load_yaml(target_observation(root))
            context, _ = build_context(
                root,
                base_ref=base_ref,
                target=target,
                complex_mode=False,
            )
            legacy = copy.deepcopy(context)
            legacy["generator_contract"] = {
                "canonical_launcher": "skills/two-pass-prompt-generator/SKILL.md",
                "canonical_schema": "skills/two-pass-prompt-generator/schema.md",
                "canonical_validator": "skills/two-pass-prompt-generator/validate.py",
                "protocol_revision_at_freeze": _standalone_contract(),
                "generator_mode": "TWO_PASS_ONLY",
                "live_main_fetch_required": True,
                "prompt_sequence": [
                    "PASS_1_SYSTEM_BASELINE",
                    "PASS_2_IMPROVE_RECONCILE_PLAN",
                ],
                "complex_mode": True,
                "approval_boundary_required": True,
            }
            self.assertEqual(
                [],
                validate_schema("handover-context", legacy, "LEGACY_HANDOVER_CONTEXT"),
            )
            request = build_request(legacy)
            self.assertTrue(request["generator"]["complex_mode"])
            self.assertEqual(
                ["PASS_1_SYSTEM_BASELINE", "PASS_2_IMPROVE_RECONCILE_PLAN"],
                request["generator"]["prompt_sequence"],
            )

    def test_only_explicit_reasoning_request_depends_on_two_pass_assets(self):
        with tempfile.TemporaryDirectory() as bad_proto:
            with self.assertRaises(HandoverContextError) as cm:
                _standalone_contract(Path(bad_proto))
            self.assertIn("standalone two-pass component missing", str(cm.exception))

        with tempfile.TemporaryDirectory() as bad_proto:
            proto_path = Path(bad_proto)
            proto_skills = proto_path / "skills/two-pass-prompt-generator"
            proto_skills.mkdir(parents=True)
            for name in ("SKILL.md", "schema.md", "validate.py"):
                shutil.copyfile(STANDALONE / name, proto_skills / name)
            schema_file = proto_skills / "schema.md"
            schema_file.write_text(
                schema_file.read_text(encoding="utf-8").replace(
                    "TPG-2P-2026-09-28-R3", "TPG-WRONG-REV"
                ),
                encoding="utf-8",
            )
            with self.assertRaises(HandoverContextError) as cm:
                _standalone_contract(proto_path)
            self.assertIn("revision mismatch", str(cm.exception))

        with tempfile.TemporaryDirectory() as bad_proto:
            proto_path = Path(bad_proto)
            proto_skills = proto_path / "skills/two-pass-prompt-generator"
            proto_skills.mkdir(parents=True)
            for name in ("SKILL.md", "schema.md", "validate.py"):
                shutil.copyfile(STANDALONE / name, proto_skills / name)
            schema_file = proto_skills / "schema.md"
            schema_file.write_text(
                schema_file.read_text(encoding="utf-8").replace(
                    "TWO_PASS_ONLY", "MISSING_TOKEN"
                ),
                encoding="utf-8",
            )
            with self.assertRaises(HandoverContextError) as cm:
                _standalone_contract(proto_path)
            self.assertIn("missing required surface", str(cm.exception))

        with tempfile.TemporaryDirectory() as bad_proto:
            proto_path = Path(bad_proto)
            proto_skills = proto_path / "skills/two-pass-prompt-generator"
            proto_skills.mkdir(parents=True)
            for name in ("SKILL.md", "schema.md", "validate.py"):
                shutil.copyfile(STANDALONE / name, proto_skills / name)
            launcher_file = proto_skills / "SKILL.md"
            launcher_file.write_text("No fetch required", encoding="utf-8")
            with self.assertRaises(HandoverContextError) as cm:
                _standalone_contract(proto_path)
            self.assertIn(
                "launcher no longer requires a current-main schema fetch",
                str(cm.exception),
            )

        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as bad_proto:
            root = Path(td)
            _, base_ref = prepare_git(root)
            target = load_yaml(target_observation(root))
            context, _ = build_context(
                root,
                base_ref=base_ref,
                target=target,
                complex_mode=False,
                protocol_root=Path(bad_proto),
            )
            self.assertNotIn("generator_contract", context)
            with self.assertRaises(HandoverContextError):
                build_request(
                    context,
                    complex_mode=False,
                    protocol_root=Path(bad_proto),
                )

