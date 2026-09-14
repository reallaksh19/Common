from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "core2b_common.py"
SPEC = importlib.util.spec_from_file_location("core2b_common", ENGINE)
core2b = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(core2b)


class Core2BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = json.loads((ROOT / "golden" / "projectile-vertical-event" / "core2b-session.json").read_text())
        cls.escalation = json.loads((ROOT / "policies" / "physics-core2b-escalation-policy.json").read_text())
        cls.hint_policy = json.loads((ROOT / "policies" / "physics-core2b-hint-policy.json").read_text())
        cls.taxonomy = json.loads((ROOT / "policies" / "physics-core2b-error-taxonomy.json").read_text())

    def test_golden_session_selects_reversed_target(self):
        core2b.validate_session(self.session, self.escalation, self.hint_policy)
        selected = core2b.choose_next_item(self.session, self.escalation)
        self.assertEqual("T3_REVERSED_TARGET", selected["transfer_level"])

    def test_core2b_rejects_non_core2a_legal_item(self):
        broken = json.loads(json.dumps(self.session))
        broken["legal_items"][0]["core2a_legal"] = False
        with self.assertRaises(core2b.Core2BValidationError):
            core2b.validate_session(broken, self.escalation, self.hint_policy)

    def test_independent_cannot_jump_to_reversed_target(self):
        restricted = json.loads(json.dumps(self.session))
        restricted["learner_state"] = "INDEPENDENT"
        selected = core2b.choose_next_item(restricted, self.escalation)
        self.assertEqual("T1_NEAR_TRANSFER", selected["transfer_level"])

    def test_internal_hint_labels_must_not_leak(self):
        broken = json.loads(json.dumps(self.session))
        broken["legal_items"][0]["hint_texts"][0] = "Use MODEL_CUE now."
        with self.assertRaises(core2b.Core2BValidationError):
            core2b.validate_session(broken, self.escalation, self.hint_policy)

    def test_error_routes_to_small_core1b_repair(self):
        attempt = {
            "outcome": "INCORRECT",
            "error_classes": ["SIGN_CONVENTION"],
            "response_evidence": {
                "model_selected": "VERTICAL_CONSTANT_ACCELERATION",
                "first_move": "12 = u + 10(1)",
                "final_answer": "2 m/s",
            },
        }
        errors = core2b.classify_attempt(attempt, self.taxonomy)
        repair = core2b.build_core1b_repair_request(
            "PHY-LS-P20",
            "PHY-CAP-PROJECTILE-VERTICAL-EVENT",
            errors,
            self.taxonomy,
        )
        self.assertIsNotNone(repair)
        self.assertEqual(["PHY-A-SIGN-01"], repair["repair_atom_refs"])

    def test_retrieval_failure_shortens_due_bucket(self):
        current = {
            "schema_version": "0.1.0",
            "capability_id": "PHY-CAP-PROJECTILE-VERTICAL-EVENT",
            "retrieval_count": 2,
            "success_streak": 2,
            "hint_dependence": "NONE",
            "representation_coverage": ["EVENT_TIMELINE"],
            "next_due_bucket": "MEDIUM",
        }
        updated = core2b.update_retrieval_state(current, "INCORRECT", "MODEL_CUE", "SIGNED_VERTICAL_VELOCITY")
        self.assertEqual("SHORT", updated["next_due_bucket"])
        self.assertEqual("MEDIUM", updated["hint_dependence"])
        self.assertIn("SIGNED_VERTICAL_VELOCITY", updated["representation_coverage"])


if __name__ == "__main__":
    unittest.main()
