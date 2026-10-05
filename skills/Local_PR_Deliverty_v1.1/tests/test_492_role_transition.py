import importlib.util
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("role_transition", ROOT / "scripts" / "role_transition.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)

NOW = datetime(2026, 10, 5, 10, 0, tzinfo=timezone.utc)


def task(shared=True):
    reviewer = "principal:A"
    coordinator = reviewer if shared else "principal:B"
    return {
        "kind": "RESPONSIBILITY",
        "task_id": "PRD-492-X",
        "acceptance_epoch_id": "AE-2",
        "role_principals": {
            "CODER": ["principal:C"],
            "REVIEWER": [reviewer],
            "COORDINATOR": [coordinator],
        },
    }


def grant(principal="principal:A"):
    return {
        "grant_id": "AUTH-ROLE-1",
        "principal": principal,
        "capability": "ROLE_EXECUTION",
        "scope": {
            "parent_task_id": "PARENT-492",
            "responsibility_task_id": "PRD-492-X",
            "acceptance_epoch_id": "AE-2",
        },
        "issued_at": "2026-10-05T09:00:00Z",
        "expires_at": None,
        "revoked_at": None,
    }


def transition(**overrides):
    args = dict(
        parent_task_id="PARENT-492",
        task=task(True),
        previous_stage="REVIEWER",
        previous_executor="principal:A",
        next_stage="COORDINATOR",
        next_executor="principal:A",
        grants=[grant()],
        at=NOW,
        previous_end_published=True,
        previous_timer_stopped=True,
        fresh_start_published=True,
        fresh_timer_armed=True,
        fresh_reconstruction=True,
        fresh_role_replay=True,
    )
    args.update(overrides)
    return module.transition_contract(**args)


class RoleTransition492Tests(unittest.TestCase):
    def test_owner_authorized_reviewer_to_coordinator_collapse_preserves_stages(self):
        result = transition()
        self.assertEqual(result["mode"], "OWNER_AUTHORIZED_COLLAPSE")
        self.assertEqual(result["principal_independence"], "DEGRADED")
        self.assertTrue(result["stage_identity_preserved"])
        self.assertEqual(result["role_execution_grant_ref"], "AUTH-ROLE-1")
        self.assertEqual(result["oracle_independence_required"], "PINNED_ORACLE_INDEPENDENT")

    def test_same_principal_without_role_execution_grant_is_rejected(self):
        with self.assertRaisesRegex(module.RoleTransitionError, "ROLE_EXECUTION"):
            transition(grants=[])

    def test_same_principal_cannot_reuse_reviewer_verdict_as_coordinator_replay(self):
        with self.assertRaisesRegex(module.RoleTransitionError, "own role-required replay"):
            transition(fresh_role_replay=False)

    def test_same_principal_requires_fresh_reconstruction(self):
        with self.assertRaisesRegex(module.RoleTransitionError, "fresh reconstruction"):
            transition(fresh_reconstruction=False)

    def test_stage_boundary_requires_end_timer_stop_and_new_start_timer(self):
        checks = [
            ("previous_end_published", "END evidence"),
            ("previous_timer_stopped", "timer accounting"),
            ("fresh_start_published", "fresh START"),
            ("fresh_timer_armed", "fresh role timer"),
        ]
        for field, message in checks:
            with self.subTest(field=field):
                with self.assertRaisesRegex(module.RoleTransitionError, message):
                    transition(**{field: False})

    def test_distinct_principal_transition_does_not_need_collapse_grant(self):
        result = transition(
            task=task(False),
            next_executor="principal:B",
            grants=[],
        )
        self.assertEqual(result["mode"], "DISTINCT_PRINCIPAL")
        self.assertEqual(result["principal_independence"], "DISTINCT")
        self.assertIsNone(result["role_execution_grant_ref"])

    def test_role_collapse_cannot_skip_a_stage(self):
        with self.assertRaisesRegex(module.RoleTransitionError, "forward-only and adjacent"):
            transition(previous_stage="CODER", next_stage="COORDINATOR")

    def test_legacy_child_cannot_use_native_collapse_contract(self):
        legacy = task(True)
        legacy["kind"] = "CHILD"
        with self.assertRaisesRegex(module.RoleTransitionError, "native RESPONSIBILITY"):
            transition(task=legacy)


if __name__ == "__main__":
    unittest.main()
