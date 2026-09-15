import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))
SPEC = importlib.util.spec_from_file_location("static_b", ENGINE / "validate_static_b_layer_boundary.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(mod)


def easy_bucket():
    return {
        "schema_version": "4.0.0",
        "bucket_id": "CHEM-BUCKET-TEST-ONLY",
        "subject": "CHEMISTRY",
        "subtopic_id": "CHEM-TEST-ONLY",
        "title": "Synthetic boundary test",
        "difficulty_badge": "EASY",
        "page_envelope": {"max_pages": 4, "is_ceiling_not_quota": True},
        "research": {"mode": "OPTIONAL", "research_refs": [], "research_questions": []},
        "visual_plan": {"visual_jobs": ["TEST_REASONING_VIEW"]},
        "decomposition": {"decision": "NOT_NEEDED", "sub_subtopic_ids": []},
        "realization_modes": ["CORE1A", "CORE1B"],
    }


def core1b_payload():
    return {
        "subject": "CHEMISTRY",
        "delivery_mode": "STATIC",
        "source_core1a_ref": "TEST_ONLY_CORE1A_AUTHORITY",
        "instruction_bucket": easy_bucket(),
        "capability_ref": "CAP-GENERIC-TEST",
        "approved_capability_refs": ["CAP-GENERIC-TEST"],
        "problem_family_ref": "PF-GENERIC-TEST",
        "approved_problem_family_refs": ["PF-GENERIC-TEST"],
        "new_chemistry_refs": [],
        "task_prompt": "Use the supplied synthetic evidence to construct a response.",
        "help_mode": "PROGRESSIVE_FIXED",
        "help": [
            {"level": "H1_ORIENT", "text": "Identify the requested evidence."},
            {"level": "H2_REPRESENT", "text": "Place the evidence in a simple structure."},
            {"level": "H4_FIRST_MOVE", "text": "Write the first justified statement."},
        ],
        "canonical_answer": "A synthetic canonical response for contract testing.",
        "check": "Check that every claim is supported by the supplied synthetic evidence.",
    }


def source_item():
    return {
        "item_id": "TEST-Q-01",
        "source_locator": "TEST_ONLY:synthetic",
        "stem": "Synthetic source item used only to test static product custody.",
        "canonical_answer": "TEST-ANSWER",
        "problem_family_ref": "PF-GENERIC-TEST",
        "provenance_class": "TEST_ONLY",
    }


def full_help():
    policy = json.loads((ROOT / "policies" / "static-b-layer-boundary.v1.json").read_text(encoding="utf-8"))
    return [{"level": level, "text": f"Synthetic {level} support."} for level in policy["core2b"]["help_order"]]


def core2b_payload(percent=50):
    return {
        "subject": "CHEMISTRY",
        "delivery_mode": "STATIC",
        "source_core2a_ref": "TEST_ONLY_CORE2A_AUTHORITY",
        "learner_conditioning": {
            "schema_version": "4.0.0",
            "mode": "KNOWLEDGE_PERCENT",
            "knowledge_percent": percent,
        },
        "selected_item_id": "TEST-Q-01",
        "legal_core2a_item_ids": ["TEST-Q-01", "TEST-Q-02"],
        "source_item": source_item(),
        "question_mode": "FROZEN_SOURCE_ITEM",
        "new_chemistry_refs": [],
        "help_mode": "PROGRESSIVE_FIXED",
        "help": full_help(),
        "full_solution": "Synthetic complete solution for contract testing.",
        "verify_reflect": "Verify against the synthetic canonical answer.",
    }


class StaticBLayerBoundaryTests(unittest.TestCase):
    def test_core1b_passes_without_learner_knowledge(self):
        result = mod.validate_core1b(core1b_payload())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["product_mode"], "CORE1B")
        self.assertFalse(result["learner_knowledge_used_for_depth"])
        self.assertEqual(result["difficulty_badge"], "EASY")

    def test_core1b_rejects_live_runtime_fields(self):
        payload = core1b_payload()
        payload["attempt_history"] = []
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core1b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_B_LIVE_RUNTIME_FIELD_PRESENT")

    def test_core1b_rejects_knowledge_contamination(self):
        payload = core1b_payload()
        payload["knowledge_percent"] = 50
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core1b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE1B_KNOWLEDGE_CONTAMINATION")

    def test_core1b_rejects_new_chemistry_and_scope_drift(self):
        payload = core1b_payload()
        payload["new_chemistry_refs"] = ["UNAUTHORIZED-CHEMISTRY"]
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core1b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_B_NEW_CHEMISTRY_INTRODUCED")

        payload = core1b_payload()
        payload["capability_ref"] = "CAP-NOT-AUTHORIZED"
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core1b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE1B_AUTHORITY_SCOPE_VIOLATION")

    def test_core1b_rejects_bad_help_order_and_missing_answer(self):
        payload = core1b_payload()
        payload["help"][0], payload["help"][1] = payload["help"][1], payload["help"][0]
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core1b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE1B_HELP_ORDER_INVALID")

        payload = core1b_payload()
        payload["canonical_answer"] = ""
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core1b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE1B_ANSWER_CLOSURE_MISSING")

    def test_core2b_knowledge_changes_support_not_item_identity(self):
        medium = mod.validate_core2b(core2b_payload(50))
        minimal = mod.validate_core2b(core2b_payload(90))
        self.assertEqual(medium["selected_item_id"], "TEST-Q-01")
        self.assertEqual(minimal["selected_item_id"], "TEST-Q-01")
        self.assertEqual(medium["resolved_support_profile"]["support_density"], "MEDIUM")
        self.assertEqual(minimal["resolved_support_profile"]["support_density"], "MINIMAL")
        self.assertFalse(medium["question_identity_mutable_by_conditioning"])
        self.assertEqual(medium["knowledge_interpretation"], "SUPPORT_PRIOR_NOT_MASTERY_MEASUREMENT")

    def test_core2b_owner_override_does_not_fabricate_percent(self):
        payload = core2b_payload()
        payload["learner_conditioning"] = {
            "schema_version": "4.0.0",
            "mode": "OWNER_OVERRIDE",
            "owner_override": {
                "reason": "Synthetic owner-controlled contract path.",
                "support_profile": {
                    "support_density": "LOW",
                    "hint_entry_level": "H3_REPRESENTATION",
                    "representation_support": "AVAILABLE_ON_REQUEST",
                    "first_move_support": "DEFERRED",
                    "solution_delay": "AFTER_FULL_ATTEMPT"
                },
                "demand_profile": {"test_only": True}
            }
        }
        result = mod.validate_core2b(payload)
        self.assertEqual(result["conditioning_mode"], "OWNER_OVERRIDE")
        self.assertTrue(result["owner_override_auditable"])
        self.assertFalse(result["fabricated_knowledge_percent"])
        self.assertNotIn("knowledge_percent", result)

    def test_core2b_rejects_unresolved_dual_or_illegal_conditioning(self):
        payload = core2b_payload()
        payload.pop("learner_conditioning")
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core2b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE2_LEARNER_CONDITION_UNRESOLVED")

        payload = core2b_payload()
        payload["learner_conditioning"]["owner_override"] = {
            "reason": "invalid dual authority",
            "support_profile": {},
            "demand_profile": {},
        }
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core2b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_V4_CONDITIONING_DUAL_AUTHORITY")

        payload = core2b_payload()
        payload["learner_conditioning"]["knowledge_percent"] = 101
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core2b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_V4_KNOWLEDGE_PERCENT_INVALID")

    def test_core2b_rejects_item_source_help_and_answer_drift(self):
        payload = core2b_payload()
        payload["legal_core2a_item_ids"] = []
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core2b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE2B_ITEM_NOT_CORE2A_LEGAL")

        payload = core2b_payload()
        payload["source_item"]["item_id"] = "OTHER"
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core2b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE2B_SOURCE_IDENTITY_DRIFT")

        payload = core2b_payload()
        payload["help"] = payload["help"][:-1]
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core2b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE2B_HELP_ORDER_INVALID")

        payload = core2b_payload()
        payload["full_solution"] = ""
        with self.assertRaises(mod.StaticBLayerBoundaryError) as ctx:
            mod.validate_core2b(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE2B_ANSWER_CLOSURE_MISSING")

    def test_generic_boundary_contains_no_stress_topic_branching(self):
        engine = (ENGINE / "validate_static_b_layer_boundary.py").read_text(encoding="utf-8").lower()
        policy = (ROOT / "policies" / "static-b-layer-boundary.v1.json").read_text(encoding="utf-8").lower()
        for token in ("redox", "mno4", "permanganate"):
            self.assertNotIn(token, engine)
            self.assertNotIn(token, policy)


if __name__ == "__main__":
    unittest.main()
