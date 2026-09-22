from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from v3lib import canonical_digest, validate_schema
from validate_foundation import validate


DIGEST = "sha256:" + ("a" * 64)


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def base_objects():
    roadmap = {
        "schema_version": "relay-v3.1-roadmap",
        "revision": "RM-0012",
        "title": "Synthetic V3 roadmap",
        "owner": {
            "outcome": "Simplify relay execution.",
            "current_goal": "Land V3 foundation.",
        },
        "work_packages": [
            {"id": "WP-TA-108", "title": "Accepted predecessor", "weight": 50, "state": "COMPLETE", "depends_on": []},
            {"id": "WP-TA-109", "title": "Current work", "weight": 50, "state": "ACTIVE", "depends_on": ["WP-TA-108"]},
        ],
    }
    state = {
        "schema_version": "relay-v3.1",
        "roadmap": {"revision": "RM-0012", "path": "relay/ROADMAP/ROADMAP.yaml"},
        "execution": {
            "lifecycle": "ACTIVE",
            "ep": "EP-TA-011",
            "lease": "LEASE-TA-011-01",
            "route": "SERIAL:EP-TA-011",
        },
        "accepted": {"checkpoint": "CP-TA-010"},
        "controls": {"path": "relay/CONTROLS/controls.yaml"},
        "delivery": {"required": False, "primary_vehicle": None},
        "generated": {"snapshot": "relay/GENERATED/CURRENT_SNAPSHOT.yaml"},
    }
    ep = {
        "schema_version": "relay-v3.1-ep",
        "id": "EP-TA-011",
        "work_package": "WP-TA-109",
        "outcome": {"statement": "Deliver one bounded V3 foundation slice."},
        "basis": {
            "predecessor_checkpoint": "CP-TA-010",
            "material_base": "85e59a93d469",
            "protocol_basis": "Common#418",
            "semantic_dependencies": [{"path": "skills/engineering-pr-delivery-v3.1", "reason": "Protocol source"}],
        },
        "scope": {
            "write": ["skills/engineering-pr-delivery-v3.1/**"],
            "read": ["skills/engineering-pr-delivery-v2.5/**"],
            "protect": ["skills/three-pass-prompt-generator/**"],
            "prohibit": ["Do not make V3 the default protocol in this slice."],
        },
        "acceptance": [
            {
                "id": "AC-1",
                "statement": "Foundation objects validate deterministically.",
                "evidence_requirements": [{"test": "test_v3_foundation.py"}],
            }
        ],
        "quality_policy": {"level": "STANDARD", "independent_review": "OPTIONAL"},
        "next": {"first_action": "Validate schemas.", "stop_conditions": ["Authority ambiguity"]},
    }
    lease = {
        "schema_version": "relay-v3.1-lease",
        "id": "LEASE-TA-011-01",
        "route": "SERIAL:EP-TA-011",
        "executor": {"id": "agent-x"},
        "basis": {
            "ep_id": "EP-TA-011",
            "ep_digest": DIGEST,
            "material_base": "85e59a93d469",
            "predecessor_checkpoint": "CP-TA-010",
            "protocol_basis": "Common#418",
        },
        "authority": {"actions": ["READ", "ANALYZE", "MATERIAL_WRITE", "TEST", "CHECKPOINT", "HANDOVER", "LOCAL_EXECUTION_EXPORT", "DRAFT_PR_UPDATE"]},
        "admission": {
            "method": "DETERMINISTIC",
            "result": "PASS",
            "repository_only": True,
            "qualification": {"required": False, "qset": None, "evaluator": None, "result": None, "evidence": []},
        },
        "state": "ACTIVE",
        "invalidation": {"reasons": []},
    }
    checkpoint = {
        "schema_version": "relay-v3.1-checkpoint",
        "id": "CP-TA-010",
        "ep": "EP-TA-010",
        "material_result": {
            "head": "1234567890abc",
            "relevant_paths_digest": DIGEST,
            "dependency_digest": DIGEST,
        },
        "acceptance": [{"id": "AC-1", "result": "PASS", "evidence": ["synthetic"]}],
        "validation": {"focused_tests": "PASS", "spec_delivery": "NOT_APPLICABLE", "full_guardrails": "PASS"},
        "quality": {"policy": "STANDARD", "result": "CLEAR"},
        "known_limitations": [],
        "discoveries": ["V3 foundation accepted."],
        "handoff": {
            "what_changed": ["Foundation schema established."],
            "what_is_true_now": ["V3 remains additive."],
            "what_remains_uncertain": [],
            "do_not_break": ["V2.5 remains live."],
            "attempted_and_rejected": [],
            "resume_from": ["Implement action authorization next."],
            "first_successor_action": "Read CURRENT_SNAPSHOT and EP.",
        },
    }
    controls = {"schema_version": "relay-v3.1-controls", "controls": []}
    snapshot = {
        "schema_version": "relay-v3.1-snapshot",
        "authority": "DERIVED_READ_MODEL",
        "generated_from": {
            "roadmap_revision": "RM-0012",
            "state_digest": canonical_digest(state),
            "material_basis": {
                "head": "1234567890abc",
                "tree_digest": DIGEST,
                "relevant_paths_digest": DIGEST,
                "dependency_digest": DIGEST,
            },
            "coordination_head": "fedcba0987654",
        },
        "owner": {"outcome": "Simplify relay execution.", "current_goal": "Land V3 foundation."},
        "programme": {
            "accepted_progress": 0,
            "completed_work": [],
            "remaining_work": ["WP-TA-109"],
        },
        "execution": {
            "lifecycle": "ACTIVE",
            "work_package": "WP-TA-109",
            "ep": "EP-TA-011",
            "lease": "LEASE-TA-011-01",
            "executor": "agent-x",
        },
        "scope": {
            "allowed_writes": ["skills/engineering-pr-delivery-v3.1/**"],
            "protected": ["skills/three-pass-prompt-generator/**"],
            "prohibited": ["Do not make V3 the default protocol in this slice."],
        },
        "material": {
            "base": "85e59a93d469",
            "head": "1234567890abc",
            "relevant_paths_digest": DIGEST,
            "dependency_digest": DIGEST,
        },
        "evidence": {"latest_checkpoint": "CP-TA-010", "latest_material_validation": {"focused": "PASS"}},
        "controls": {
            "execution_blockers": [],
            "handover_blockers": [],
            "delivery_blockers": [],
            "informational": [],
        },
        "delivery": {"issue": None, "pr": None, "lifecycle": "NOT_REQUIRED", "merge_authorized": False},
        "next": {
            "immediate_material_action": "Validate schemas.",
            "delivery_action": None,
            "stop_conditions": ["Authority ambiguity"],
        },
        "handoff": {
            "zero_context_takeover_possible": True,
            "reconstruction_sources": [
                "relay/ROADMAP/ROADMAP.yaml",
                "relay/STATE.yaml",
                "relay/CONTROLS/controls.yaml",
                "relay/WORK/EP-TA-011.yaml",
                "relay/LEASES/LEASE-TA-011-01.yaml",
                "relay/CHECKPOINTS/CP-TA-010.yaml",
            ],
        },
    }
    event = {
        "schema_version": "relay-v3.1-event",
        "event_id": "EVT-0001",
        "type": "EP_CREATED",
        "timestamp": "2026-09-22T03:20:57Z",
        "actor": "agent-x",
        "subject": "EP-TA-011",
        "basis": ["Common#418"],
        "details": {},
    }
    return roadmap, state, ep, lease, checkpoint, controls, snapshot, event


def materialize(root: Path):
    roadmap, state, ep, lease, checkpoint, controls, snapshot, event = base_objects()
    dump(root / "relay/ROADMAP/ROADMAP.yaml", roadmap)
    dump(root / "relay/STATE.yaml", state)
    dump(root / "relay/WORK/EP-TA-011.yaml", ep)
    dump(root / "relay/LEASES/LEASE-TA-011-01.yaml", lease)
    dump(root / "relay/CHECKPOINTS/CP-TA-010.yaml", checkpoint)
    dump(root / "relay/CONTROLS/controls.yaml", controls)
    dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", snapshot)
    (root / "relay/EVENTS.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
    return roadmap, state, ep, lease, checkpoint, controls, snapshot, event


class V3FoundationTests(unittest.TestCase):
    def test_valid_foundation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            self.assertEqual([], validate(root))

    def test_missing_roadmap_is_authority_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            (root / "relay/ROADMAP/ROADMAP.yaml").unlink()
            errors = validate(root)
            self.assertTrue(any("ROADMAP: cannot load" in item for item in errors), errors)


    def test_state_object_id_path_traversal_is_rejected_before_lookup(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, state, *_ = materialize(root)
            state["execution"]["ep"] = "EP-../../outside"
            dump(root / "relay/STATE.yaml", state)
            errors = validate(root)
            self.assertTrue(any("unsafe characters" in item or "does not match" in item for item in errors), errors)

    def test_state_authority_path_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, state, *_ = materialize(root)
            state["roadmap"]["path"] = "../outside-roadmap.yaml"
            dump(root / "relay/STATE.yaml", state)
            errors = validate(root)
            self.assertTrue(any("escapes repository root" in item for item in errors), errors)

    def test_snapshot_disagreement_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            *_, snapshot, _ = materialize(root)
            snapshot["execution"]["ep"] = "EP-WRONG"
            dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", snapshot)
            errors = validate(root)
            self.assertTrue(any("SNAPSHOT.execution.ep disagrees" in item for item in errors), errors)

    def test_snapshot_state_digest_disagreement_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            *_, snapshot, _ = materialize(root)
            snapshot["generated_from"]["state_digest"] = DIGEST
            dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", snapshot)
            errors = validate(root)
            self.assertTrue(any("state digest disagrees" in item for item in errors), errors)

    def test_control_cannot_block_and_permit_same_action(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            *_, controls, _, _ = materialize(root)
            controls["controls"] = [{
                "id": "CTRL-001",
                "kind": "COLLISION",
                "state": "OPEN",
                "source": {"type": "VALIDATOR", "ref": "synthetic"},
                "condition": "collision",
                "blocks": ["MATERIAL_WRITE"],
                "permits": ["MATERIAL_WRITE"],
                "resolution": {"condition": "collision cleared", "evidence": []},
            }]
            dump(root / "relay/CONTROLS/controls.yaml", controls)
            errors = validate(root)
            self.assertTrue(any("both blocked and permitted" in item for item in errors), errors)

    def test_owner_override_cannot_grant_merge(self):
        _, _, _, lease, *_ = base_objects()
        lease = copy.deepcopy(lease)
        lease["admission"] = {
            "method": "OWNER_OVERRIDE",
            "result": "PASS",
            "repository_only": False,
            "qualification": {"required": False, "qset": None, "evaluator": None, "result": None, "evidence": []},
            "owner_basis": {
                "direct_utterance_digest": DIGEST,
                "session_timestamp": "2026-09-22T03:20:57Z",
            },
        }
        lease["scope"] = {
            "ep_or_task": "EP-TA-011",
            "branch": "v3/test",
            "allowed_writes": ["skills/engineering-pr-delivery-v3.1/**"],
            "prohibited": ["MERGE", "RELEASE"],
        }
        lease["authority"]["actions"].append("MERGE")
        errors = validate_schema("lease", lease, "LEASE")
        self.assertTrue(errors)

    def test_high_risk_ep_requires_independent_review(self):
        _, _, ep, *_ = base_objects()
        ep = copy.deepcopy(ep)
        ep["quality_policy"] = {"level": "HIGH_RISK", "independent_review": "OPTIONAL"}
        errors = validate_schema("ep", ep, "EP")
        self.assertTrue(errors)

    def test_idle_state_rejects_active_execution_pointers(self):
        _, state, *_ = base_objects()
        state = copy.deepcopy(state)
        state["execution"]["lifecycle"] = "IDLE"
        errors = validate_schema("state", state, "STATE")
        self.assertTrue(errors)

    def test_duplicate_event_ids_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            *_, event = materialize(root)
            path = root / "relay/EVENTS.jsonl"
            path.write_text(json.dumps(event) + "\n" + json.dumps(event) + "\n", encoding="utf-8")
            errors = validate(root)
            self.assertTrue(any("duplicate event_id" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()
