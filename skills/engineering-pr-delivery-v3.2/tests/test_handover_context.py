from __future__ import annotations

import copy
import json
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
    build_delp_source_bound_successor,
    build_request,
    _successor_entry,
    render_request,
    validate_visibility,
)
from plan_handover import plan_handover
from owner_commands import parse_owner_command
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





    def test_benchmark_owner_instruction_drives_handover_runtime_end_to_end(self):
        owner = parse_owner_command(
            "prepare for handover and create exactly 3 questions; no qualification; "
            "do not run retained validation; do not modify production code; do not create a PR; "
            "do not start C1 execution"
        )
        self.assertEqual("PLAN_HANDOVER", owner["intent"])
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            result = plan_handover(
                root,
                tx_id="TX-HANDOVER-OWNER-001",
                event_id="EVT-HANDOVER-OWNER-001",
                actor="owner",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
                owner_intent=owner,
            )
            self.assertEqual("COMMITTED", result["status"])
            context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            entry = context["successor_entry"]
            self.assertEqual("RECONSTRUCT_PLAN_ONLY", entry["mode"])
            self.assertEqual(3, len(entry["successor_reconstruction_challenge"]))
            expected = {
                "EXACT_SUCCESSOR_CHALLENGE_COUNT:3",
                "NO_QUALIFICATION",
                "NO_RETAINED_VALIDATION",
                "NO_PRODUCTION_MUTATION",
                "NO_PR_CREATION",
                "NO_TASK_EXECUTION",
            }
            self.assertTrue(expected.issubset(set(entry["owner_boundary_constraints"])))
            self.assertEqual("OWNER_EXPLICIT_EXECUTION_ADMISSION", entry["execution_admission"])
            self.assertFalse((root / "relay/GENERATED/TWO_PASS_REQUEST.yaml").exists())
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            planned = [row for row in events if row["event_id"] == "EVT-HANDOVER-OWNER-001"][0]
            self.assertTrue(planned["details"]["owner_intent_bound"])
            self.assertEqual(3, planned["details"]["successor_challenge_count"])
            self.assertGreaterEqual(planned["details"]["owner_boundary_constraint_count"], 6)

    def test_owner_intent_count_conflict_fails_closed_before_handover_write(self):
        owner = parse_owner_command("prepare for handover and create exactly 3 questions")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            with self.assertRaisesRegex(TransactionError, "conflicts with Owner intent"):
                plan_handover(
                    root,
                    tx_id="TX-HANDOVER-CONFLICT-001",
                    event_id="EVT-HANDOVER-CONFLICT-001",
                    actor="owner",
                    target_path=target_observation(root),
                    base_ref=base_ref,
                    complex_mode=False,
                    owner_intent=owner,
                    successor_challenge_count=2,
                )
            self.assertFalse((root / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists())

    def test_owner_intent_challenge_without_count_fails_closed_instead_of_dropping_deliverable(self):
        owner = parse_owner_command("prepare for handover and create successor questions for the next agent")
        self.assertIn(
            {"type": "SUCCESSOR_RECONSTRUCTION_CHALLENGE"},
            owner["owner_intent"]["requested_deliverables"],
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            with self.assertRaisesRegex(TransactionError, "without a concrete count"):
                plan_handover(
                    root,
                    tx_id="TX-HANDOVER-NOCOUNT-001",
                    event_id="EVT-HANDOVER-NOCOUNT-001",
                    actor="owner",
                    target_path=target_observation(root),
                    base_ref=base_ref,
                    complex_mode=False,
                    owner_intent=owner,
                )

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
            self.assertIsNone(entry["challenge_digest"])
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
            self.assertRegex(entry["challenge_digest"], r"^sha256:[0-9a-f]{64}$")
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

    def test_successor_challenge_digest_is_deterministic_and_material_bound(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            context, _ = build_context(
                root,
                base_ref=base_ref,
                target=load_yaml(target_observation(root)),
                complex_mode=False,
                successor_challenge_count=0,
            )
            self.assertIsNone(context["successor_entry"]["challenge_digest"])
            first = _successor_entry(context, 3)
            second = _successor_entry(copy.deepcopy(context), 3)
            self.assertEqual(first["challenge_digest"], second["challenge_digest"])
            moved = copy.deepcopy(context)
            moved["reality_context"]["material"]["head"] = "f" * 40
            self.assertNotEqual(
                first["challenge_digest"],
                _successor_entry(moved, 3)["challenge_digest"],
            )

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



    def test_retained_1256_frontier_advance_supersedes_the_historical_c1_entry_exam(self):
        context = {
            "target": {
                "provider_ref": "github:reallaksh19/XML_Compare_Utilities#1256",
                "state": "CLOSED",
            },
            "reality_context": {
                "material": {
                    "head": "c1998df47e4183e6d54c30555cbc022742ffebc5",
                },
                "execution": {"branch": "main"},
                "task_constraints": [
                    "TEXPECTED is validation-only and cannot select correspondence.",
                    "Manual reviewed seeds remain diagnostic/manual authority only.",
                ],
            },
            "accumulated_learning": {
                "first_successor_action": "Run C1 retained S1 candidate funnel before any production repair.",
                "what_remains_uncertain": [
                    "ROOT_CLASSIFICATION = UNKNOWN; candidate generation vs Method-A qualification vs fusion vs propagation.",
                ],
                "attempted_and_rejected": [
                    "Blind budget escalation: budget 11 READY was not semantic acceptance.",
                    "Manual-anchor cardinality expansion as the general solution.",
                ],
                "do_not_break": [
                    "TEXPECTED is validation-only; benchmark identities must not enter matching.",
                    "Manual seeds are diagnostic only and must not become automatic authority.",
                ],
                "reconstruction_context": {
                    "original_intent": {
                        "source_ref": "github:reallaksh19/XML_Compare_Utilities#1256",
                        "url": "https://github.com/reallaksh19/XML_Compare_Utilities/issues/1256",
                    },
                    "latest_reconciliation": {
                        "ref": "issuecomment-6026782962",
                        "summary": (
                            "RESPONSIBILITY_COMPLETE=YES; PRODUCT_LANDED=YES; POST_MERGE_QUALIFICATION=PASS; "
                            "retained S1 mandatory correspondence 12/12 and mutation 12/12 at budget 10."
                        ),
                    },
                    "primary_conversation_refs": [],
                    "roadmap_refs": ["#1257", "#1258", "#1259"],
                    "local_agent_refs": [],
                    "rll_refs": [],
                },
                "task_snapshot": {
                    "value": {
                        "next": {
                            "immediate_action": "Reconcile downstream consumers; no further S1 product coding."
                        }
                    }
                },
            },
        }

        entry = _successor_entry(context, 3)
        basis = entry["challenge_basis"]
        self.assertEqual("CURRENT_RECONCILIATION_SUPERSEDES_HANDOFF", basis["freshness"])
        self.assertEqual("CLOSED", basis["target_state"])
        self.assertEqual("issuecomment-6026782962", basis["latest_reconciliation_ref"])
        self.assertIn("12/12", basis["latest_reconciliation_summary"])
        self.assertIn("Run C1", basis["inherited_first_successor_action"])
        self.assertTrue(any("ROOT_CLASSIFICATION = UNKNOWN" in item for item in basis["inherited_uncertainties"]))
        self.assertTrue(any("budget 11 READY" in item for item in basis["inherited_negative_knowledge"]))
        self.assertTrue(any("TEXPECTED is validation-only" in item for item in basis["protected_invariants"]))

        challenge = entry["successor_reconstruction_challenge"]
        self.assertEqual(3, len(challenge))
        self.assertEqual(
            {"Reconcile downstream consumers; no further S1 product coding."},
            {q["decision_at_risk"] for q in challenge},
        )
        joined = "\n".join(q["question"] for q in challenge)
        self.assertIn("current frontier", joined.lower())
        self.assertIn("historical handover uncertainty", joined.lower())
        self.assertIn("12/12", joined)
        self.assertIn("TEXPECTED is validation-only", joined)
        self.assertIn("budget 11 READY", joined)
        self.assertNotIn("Resolve this current uncertainty: ROOT_CLASSIFICATION = UNKNOWN", joined)
        self.assertNotIn("Before Run C1 retained S1 candidate funnel", joined)
        self.assertEqual("RECONSTRUCT_PLAN_ONLY", entry["mode"])
        self.assertIn("TASK_EXECUTION", entry["forbidden_actions"])
        self.assertIn("PR_CREATION", entry["forbidden_actions"])

    def test_terminal_target_without_reconciliation_does_not_reactivate_inherited_execution(self):
        context = {
            "target": {"provider_ref": "github:example/project#1", "state": "CLOSED"},
            "reality_context": {"material": {}, "execution": {}, "task_constraints": []},
            "accumulated_learning": {
                "first_successor_action": "Implement the old patch.",
                "what_remains_uncertain": ["Old uncertainty."],
                "attempted_and_rejected": [],
                "do_not_break": [],
                "reconstruction_context": {
                    "original_intent": None,
                    "latest_reconciliation": None,
                    "primary_conversation_refs": [],
                    "roadmap_refs": [],
                    "local_agent_refs": [],
                    "rll_refs": [],
                },
                "task_snapshot": {"value": {"next": {}}},
            },
        }
        entry = _successor_entry(context, 1)
        self.assertEqual("TERMINAL_TARGET_REQUIRES_RECONCILIATION", entry["challenge_basis"]["freshness"])
        self.assertEqual("VERIFY_CURRENT_DISPOSITION_AND_NEXT_CONSUMER", entry["successor_reconstruction_challenge"][0]["decision_at_risk"])
        self.assertNotIn("Before Implement the old patch", entry["successor_reconstruction_challenge"][0]["question"])

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


    @staticmethod
    def _source_bound_fixture():
        repo = ROOT.parents[1]
        graph = json.loads(
            (repo / ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json").read_text(encoding="utf-8")
        )
        class ReadOnlyProvider:
            def __init__(self):
                self.sha = "a" * 40
                self.issue_title = "Source issue"
                self.read_number = 0
                self.move_during_read = False
            def get_commit_sha(self, ref):
                return "b" * 40
            def get_issue(self, n):
                self.read_number += 1
                if self.move_during_read and self.read_number >= 3:
                    self.issue_title = "Changed while reading"
                return {"number": n, "title": self.issue_title, "body": "human source",
                        "state": "open"}
            def get_pull(self, n):
                return {"head": {"sha": self.sha}, "merged": False, "state": "open"}
            def list_comments(self, n):
                return []
        return graph, ReadOnlyProvider()

    def test_delp_source_successor_is_real_read_model_not_authority(self):
        graph, provider = self._source_bound_fixture()
        result = build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)
        self.assertEqual("DERIVED_RECONSTRUCTION_READ_ONLY", result["authority"])
        self.assertEqual("CURRENT_READ_ONLY", result["currentness"])
        self.assertEqual("UNRESOLVED_CHAT_MESSAGE_LINK", result["owner_source_status"])
        self.assertEqual("Common#720", result["leaf"])
        self.assertEqual([], result["authority_effects"])
        self.assertEqual(0, result["progress"]["P"])
        self.assertEqual("NEVER_FROM_RECONSTRUCTION", result["execution_admission"])
        self.assertIn(result["source_action"], ("MATERIALIZE_FACTS", "RECOVER_EVIDENCE",
                                               "WAIT_DEPENDENCY", "AWAIT_RESULT", "FIX_PLAN"))

    def test_delp_successor_changed_candidate_requires_reconciliation(self):
        graph, provider = self._source_bound_fixture()
        first = build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)
        provider.sha = "c" * 40
        moved = build_delp_source_bound_successor(
            graph, leaf_ref="Common#720", provider=provider, frozen_basis=first["digests"])
        self.assertEqual("RECONCILE_REQUIRED", moved["currentness"])
        self.assertIn("input", moved["moved_axes"])
        self.assertEqual([], moved["authority_effects"])

    def test_delp_successor_same_frozen_provider_facts_unchanged(self):
        graph, provider = self._source_bound_fixture()
        first = build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)
        second = build_delp_source_bound_successor(
            graph, leaf_ref="Common#720", provider=provider, frozen_basis=first["digests"])
        self.assertEqual("CURRENT_READ_ONLY", second["currentness"])
        self.assertEqual([], second["moved_axes"])
        provider.issue_title = "Human title changed"
        third = build_delp_source_bound_successor(
            graph, leaf_ref="Common#720", provider=provider, frozen_basis=first["digests"])
        self.assertEqual("RECONCILE_REQUIRED", third["currentness"])
        self.assertIn("provider", third["moved_axes"])

    def test_delp_successor_provider_race_or_wrong_issue_fails_closed(self):
        graph, provider = self._source_bound_fixture()
        provider.move_during_read = True
        with self.assertRaisesRegex(HandoverContextError, "SOURCE_PROVIDER_CHANGED_DURING_READ"):
            build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)
        graph, provider = self._source_bound_fixture()
        provider.get_issue = lambda n: {"number": 999, "state": "open"}
        with self.assertRaisesRegex(HandoverContextError, "SOURCE_ISSUE_PROVIDER_IDENTITY_MISMATCH"):
            build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)

    def test_delp_successor_rejects_moved_plan_and_missing_frozen_keys(self):
        graph, provider = self._source_bound_fixture()
        first = build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)
        with self.assertRaisesRegex(HandoverContextError, "FROZEN_SOURCE_BASIS_INCOMPLETE"):
            build_delp_source_bound_successor(
                graph, leaf_ref="Common#720", provider=provider,
                frozen_basis={"input": first["digests"]["input"]})
        graph["programme"]["decomposition_proposal"]["released_proposal_digest"] = "sha256:" + "0"*64
        with self.assertRaisesRegex(HandoverContextError, "SOURCE_PROPOSAL_NOT_RELEASEABLE"):
            build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)

    def test_build_context_opt_in_carries_source_anchor_to_actual_successor_question(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            target = load_yaml(target_observation(root))
            graph, provider = self._source_bound_fixture()
            context, _ = build_context(
                root, base_ref=base_ref, target=target, complex_mode=False,
                successor_challenge_count=1,
                delp_source={"graph": graph, "leaf_ref": "Common#720", "provider": provider},
            )
            source = context["source_bound_successor"]
            self.assertEqual("CURRENT_READ_ONLY", source["currentness"])
            self.assertEqual(source["digests"]["input"],
                             context["successor_entry"]["challenge_basis"]["source_input_digest"])
            self.assertEqual("RECONSTRUCT_PLAN_ONLY", context["successor_entry"]["mode"])
            self.assertNotIn("source_bound_successor", context["blind_context"])
            self.assertEqual([], validate_visibility(context))


    def test_delp_successor_racing_checkpoint_facts_fail_closed(self):
        graph, provider = self._source_bound_fixture()
        provider.fact_reads = 0
        def comments(n):
            if n != 720:
                return []
            provider.fact_reads += 1
            if provider.fact_reads == 1:
                return []
            return [{
                "id": 8121, "author_association": "OWNER",
                "user": {"login": "authorized"},
                "body": (
                    "```yaml\nCHECKPOINT_FACTS_V1:\n"
                    "  responsibility: {issue: Common#720}\n"
                    "  material: {candidate_sha: " + "a"*40 + "}\n"
                    "  units: []\n```"
                ),
            }]
        provider.list_comments = comments
        with self.assertRaisesRegex(HandoverContextError, "SOURCE_PROVIDER_CHANGED_DURING_READ"):
            build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)

    def test_delp_successor_cannot_mint_owner_original_link(self):
        graph, provider = self._source_bound_fixture()
        with self.assertRaisesRegex(HandoverContextError, "OWNER_ORIGIN_STATUS_UNVERIFIED"):
            build_delp_source_bound_successor(
                graph, leaf_ref="Common#720", provider=provider,
                owner_source_status="LINKED_ORIGINAL_SOURCE")

    def test_delp_successor_refuses_missing_or_malformed_live_material(self):
        # A named PR is not proof of the actual commit. An unavailable provider
        # must not mint CURRENT_READ_ONLY simply because no frozen basis exists.
        for missing in (None, "", "short", "z" * 40):
            with self.subTest(candidate_sha=missing):
                graph, provider = self._source_bound_fixture()
                provider.sha = missing
                with self.assertRaisesRegex(HandoverContextError, "SOURCE_CANDIDATE_SHA_UNVERIFIED"):
                    build_delp_source_bound_successor(
                        graph, leaf_ref="Common#720", provider=provider)
        graph, provider = self._source_bound_fixture()
        provider.get_commit_sha = lambda ref: None
        with self.assertRaisesRegex(HandoverContextError, "SOURCE_BASE_SHA_UNVERIFIED"):
            build_delp_source_bound_successor(
                graph, leaf_ref="Common#720", provider=provider)

    def test_delp_successor_refuses_unknown_provider_pr_state(self):
        graph, provider = self._source_bound_fixture()
        provider.get_pull = lambda n: {
            "head": {"sha": "a" * 40}, "state": None, "merged": False,
        }
        with self.assertRaisesRegex(HandoverContextError, "SOURCE_PR_STATE_UNVERIFIED"):
            build_delp_source_bound_successor(
                graph, leaf_ref="Common#720", provider=provider)

    def test_delp_successor_refuses_unbound_esc4_like_leaf(self):
        # The real C1 graph originally had no primary_pr or candidate_ref for
        # Common#793. Its live SHA was invisible to observe_github. A leaf
        # without either binding is never CURRENT, even if other leaves are.
        graph, provider = self._source_bound_fixture()
        target = next(n for n in graph["nodes"] if n["ref"] == "Common#733")
        target.pop("primary_pr", None)
        target.pop("candidate_ref", None)
        with self.assertRaisesRegex(HandoverContextError, "SOURCE_CANDIDATE_NOT_BOUND"):
            build_delp_source_bound_successor(graph, leaf_ref="Common#733", provider=provider)


    def test_c6_p01_real_transaction_source_bound_context_and_event(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            graph, provider = self._source_bound_fixture()
            result = plan_handover(
                root, tx_id="TX-C6-P01", event_id="EVT-C6-P01",
                actor="owner", target_path=target_observation(root),
                base_ref=base_ref, complex_mode=False, successor_challenge_count=3,
                delp_source={"graph": graph, "leaf_ref": "Common#720", "provider": provider},
            )
            self.assertEqual("COMMITTED", result["status"])
            context = load_yaml(root / "relay/GENERATED/HANDOVER_CONTEXT.yaml")
            bound = context["source_bound_successor"]
            self.assertEqual("CURRENT_READ_ONLY", bound["currentness"])
            self.assertEqual("NEVER_FROM_RECONSTRUCTION", bound["execution_admission"])
            self.assertEqual([], bound["authority_effects"])
            self.assertEqual(bound["digests"]["input"],
                             context["successor_entry"]["challenge_basis"]["source_input_digest"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            matches = [e for e in events if e["event_id"] == "EVT-C6-P01"]
            self.assertEqual(1, len(matches))
            self.assertEqual(bound["digests"]["input"], matches[0]["details"]["source_bound_input_digest"])

    def test_c6_p02_stale_frozen_provider_denied_before_writes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            graph, provider = self._source_bound_fixture()
            before = build_delp_source_bound_successor(graph, leaf_ref="Common#720", provider=provider)
            provider.sha = "c" * 40
            events_before = (root / "relay/EVENTS.jsonl").read_bytes()
            with self.assertRaisesRegex(TransactionError, "SOURCE_BOUND_RECONCILIATION_REQUIRED"):
                plan_handover(
                    root, tx_id="TX-C6-P02", event_id="EVT-C6-P02", actor="owner",
                    target_path=target_observation(root), base_ref=base_ref, complex_mode=False,
                    delp_source={"graph": graph, "leaf_ref": "Common#720",
                                 "provider": provider, "frozen_basis": before["digests"]},
                )
            self.assertEqual(events_before, (root / "relay/EVENTS.jsonl").read_bytes())
            self.assertFalse((root / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists())
            self.assertFalse((root / "relay/TRANSACTIONS/TX-C6-P02").exists())

    def test_c6_p03_p04_invalid_or_racing_provider_cannot_start_transaction(self):
        for mode in ("missing_head", "moving_issue"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _, base_ref = prepare_git(root)
                graph, provider = self._source_bound_fixture()
                if mode == "missing_head":
                    provider.sha = None
                    expected = "SOURCE_CANDIDATE_SHA_UNVERIFIED"
                else:
                    provider.move_during_read = True
                    expected = "SOURCE_PROVIDER_CHANGED_DURING_READ"
                before = (root / "relay/EVENTS.jsonl").read_bytes()
                with self.assertRaisesRegex(HandoverContextError, expected):
                    plan_handover(
                        root, tx_id="TX-C6-P03", event_id="EVT-C6-P03", actor="owner",
                        target_path=target_observation(root), base_ref=base_ref, complex_mode=False,
                        delp_source={"graph": graph, "leaf_ref": "Common#720", "provider": provider},
                    )
                self.assertEqual(before, (root / "relay/EVENTS.jsonl").read_bytes())
                self.assertFalse((root / "relay/TRANSACTIONS/TX-C6-P03").exists())

    def test_c6_p08_opted_in_interruption_recovers_before_images(self):
        from transactionlib import recover_all, incomplete_transactions
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            graph, provider = self._source_bound_fixture()
            before = (root / "relay/EVENTS.jsonl").read_bytes()
            with self.assertRaisesRegex(TransactionError, "injected transaction interruption"):
                plan_handover(
                    root, tx_id="TX-C6-P08", event_id="EVT-C6-P08", actor="owner",
                    target_path=target_observation(root), base_ref=base_ref, complex_mode=False,
                    delp_source={"graph": graph, "leaf_ref": "Common#720", "provider": provider},
                    fail_after=1,
                )
            self.assertTrue(incomplete_transactions(root))
            self.assertEqual(["ROLLED_BACK"], [v["status"] for v in recover_all(root)])
            self.assertEqual(before, (root / "relay/EVENTS.jsonl").read_bytes())
            self.assertFalse((root / "relay/GENERATED/HANDOVER_CONTEXT.yaml").exists())
