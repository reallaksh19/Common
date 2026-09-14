from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "policies" / "v8-blueprint-only-execution-policy.json").read_text())
GOLDEN = json.loads((ROOT / "golden" / "v8" / "core1a-ready-execution.json").read_text())

spec = importlib.util.spec_from_file_location("v8", ROOT / "engine" / "validate_blueprint_v8.py")
v8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v8)


class BlueprintV8ExecutionTests(unittest.TestCase):
    def test_ready_packet_passes(self):
        out = v8.validate(copy.deepcopy(GOLDEN), POLICY)
        self.assertEqual(out["status"], "READY")
        self.assertFalse(out["memory_authority_used"])

    def test_model_memory_is_forbidden(self):
        p = copy.deepcopy(GOLDEN)
        p["authority_sources_used"].append("MODEL_MEMORY")
        with self.assertRaisesRegex(v8.BlueprintV8Error, "MEMORY_OR_UNTRACED_AUTHORITY_FORBIDDEN"):
            v8.validate(p, POLICY)

    def test_conversation_memory_is_forbidden_as_fact_authority(self):
        p = copy.deepcopy(GOLDEN)
        p["authority_sources_used"].append("CONVERSATION_MEMORY_AS_FACT_SOURCE")
        with self.assertRaisesRegex(v8.BlueprintV8Error, "MEMORY_OR_UNTRACED_AUTHORITY_FORBIDDEN"):
            v8.validate(p, POLICY)

    def test_missing_required_blueprint_authority_blocks_ready_execution(self):
        p = copy.deepcopy(GOLDEN)
        p["authority_refs"] = [x for x in p["authority_refs"] if x["authority_type"] != "CONCEPT_TTU"]
        with self.assertRaisesRegex(v8.BlueprintV8Error, "REQUIRED_BLUEPRINT_AUTHORITY_MISSING"):
            v8.validate(p, POLICY)

    def test_missing_authority_can_only_return_blocked(self):
        p = copy.deepcopy(GOLDEN)
        p["authority_refs"] = [x for x in p["authority_refs"] if x["authority_type"] != "CONCEPT_TTU"]
        p["execution_status"] = "BLOCKED"
        p["blocked_reasons"] = ["CONCEPT_TTU authority is absent"]
        out = v8.validate(p, POLICY)
        self.assertEqual(out["status"], "BLOCKED")
        self.assertIn("CONCEPT_TTU", out["missing_authority_types"])

    def test_unbound_technical_object_fails(self):
        p = copy.deepcopy(GOLDEN)
        p["output_bindings"].append({
            "output_id": "EX-UNTRACED-01",
            "object_class": "EXAMPLE",
            "authority_ref": "memory://example"
        })
        with self.assertRaisesRegex(v8.BlueprintV8Error, "OUTPUT_AUTHORITY_REF_UNRESOLVED"):
            v8.validate(p, POLICY)

    def test_core2b_requires_lau_problem_ttu_dialogue_and_question_custody(self):
        p = copy.deepcopy(GOLDEN)
        p["execution_id"] = "CHEM-V8-GOLDEN-CORE2B-001"
        p["product_mode"] = "CORE2B"
        p["authority_refs"] = [
            {"authority_type": "CANONICAL_DOMAIN_REGISTRY", "ref": "registry://chem/redox"},
            {"authority_type": "CDAU", "ref": "cdau://chem/redox"},
            {"authority_type": "LAU", "ref": "lau://chem/redox/q1"},
            {"authority_type": "PROBLEM_TTU", "ref": "problem-ttu://chem/redox/q1"},
            {"authority_type": "TUTOR_DIALOGUE", "ref": "dialogue://chem/redox/q1"},
            {"authority_type": "QUESTION_CUSTODY", "ref": "question://chem/redox/q1"},
            {"authority_type": "CCBOM", "ref": "ccbom://chem/redox"},
            {"authority_type": "PRODUCT_ASSURANCE", "ref": "pal://chem/redox"}
        ]
        p["output_bindings"] = [
            {"output_id": "Q1", "object_class": "QUESTION", "authority_ref": "question://chem/redox/q1"},
            {"output_id": "TTU-Q1", "object_class": "TTU", "authority_ref": "problem-ttu://chem/redox/q1"},
            {"output_id": "SUPPORT-Q1", "object_class": "SUPPORT_DECISION", "authority_ref": "lau://chem/redox/q1"}
        ]
        out = v8.validate(p, POLICY)
        self.assertEqual(out["status"], "READY")


if __name__ == "__main__":
    unittest.main()
