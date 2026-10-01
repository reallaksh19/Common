import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "validate_blueprint_v4.py"
POLICY_PATH = ROOT / "policies" / "v4-bucket-and-conditioning-policy.json"

spec = importlib.util.spec_from_file_location("validate_blueprint_v4", ENGINE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def bucket(badge="EASY"):
    rules = {
        "EASY": (10, "OPTIONAL", ["PHENOMENON_VISUAL"], []),
        "MEDIUM": (20, "REQUIRED", ["PHENOMENON_VISUAL"], ["R1"]),
        "HARD": (30, "DEEP_REQUIRED", ["PHENOMENON_VISUAL", "REPRESENTATION_BRIDGE"], ["R1", "R2"]),
    }
    pages, mode, visuals, refs = rules[badge]
    out = {
        "schema_version": "4.0.0",
        "bucket_id": f"B-{badge}",
        "subject": "CHEMISTRY",
        "subtopic_id": "SUB-1",
        "title": "Sample",
        "difficulty_badge": badge,
        "page_envelope": {"max_pages": pages, "is_ceiling_not_quota": True},
        "research": {"mode": mode, "research_refs": refs},
        "visual_plan": {"visual_jobs": visuals},
        "decomposition": {"decision": "NOT_NEEDED", "sub_subtopic_ids": []},
        "realization_modes": ["CORE1A", "CORE1B"],
    }
    if badge == "HARD":
        out["research"]["research_questions"] = ["How is this best represented?", "What misconceptions recur?"]
    return out


class BlueprintV4Tests(unittest.TestCase):
    def test_easy_medium_hard_buckets_pass(self):
        for badge in ("EASY", "MEDIUM", "HARD"):
            result = mod.validate_instruction_bucket(bucket(badge))
            self.assertEqual(result["status"], "PASS")
            self.assertFalse(result["learner_knowledge_used"])

    def test_core1_rejects_learner_knowledge(self):
        data = bucket("EASY")
        data["knowledge_percent"] = 50
        with self.assertRaisesRegex(mod.BlueprintV4Error, "CORE1_KNOWLEDGE_CONTAMINATION"):
            mod.validate_instruction_bucket(data)

    def test_page_envelopes_are_ceilinged(self):
        data = bucket("MEDIUM")
        data["page_envelope"]["max_pages"] = 21
        with self.assertRaisesRegex(mod.BlueprintV4Error, "PAGE_ENVELOPE_INVALID"):
            mod.validate_instruction_bucket(data)

    def test_medium_requires_research(self):
        data = bucket("MEDIUM")
        data["research"]["research_refs"] = []
        with self.assertRaisesRegex(mod.BlueprintV4Error, "MEDIUM_RESEARCH_MISSING"):
            mod.validate_instruction_bucket(data)

    def test_hard_requires_deep_research_and_multiple_visual_jobs(self):
        data = bucket("HARD")
        data["research"]["research_refs"] = ["R1"]
        with self.assertRaisesRegex(mod.BlueprintV4Error, "HARD_DEEP_RESEARCH_MISSING"):
            mod.validate_instruction_bucket(data)

    def test_knowledge_percent_resolves_support_only(self):
        result = mod.validate_core2_conditioning({
            "schema_version": "4.0.0",
            "mode": "KNOWLEDGE_PERCENT",
            "knowledge_percent": 50,
        }, POLICY)
        self.assertEqual(result["resolved_support_profile"]["support_density"], "MEDIUM")
        self.assertEqual(result["knowledge_interpretation"], "SUPPORT_PRIOR_NOT_MASTERY_MEASUREMENT")

    def test_owner_override_waives_unknown_knowledge(self):
        result = mod.validate_core2_conditioning({
            "schema_version": "4.0.0",
            "mode": "OWNER_OVERRIDE",
            "owner_override": {
                "reason": "knowledge percentage unavailable",
                "support_profile": {
                    "support_density": "HIGH",
                    "hint_entry_level": "H1_ORIENT",
                    "representation_support": "SUPPLIED",
                    "first_move_support": "EXPLICIT",
                    "solution_delay": "AFTER_HINT_LADDER"
                },
                "demand_profile": {
                    "transfer_distance": "NEAR_TRANSFER",
                    "interleaving": False,
                    "synthesis_width": 1,
                    "time_pressure": "PRACTICE"
                }
            }
        }, POLICY)
        self.assertTrue(result["owner_override_auditable"])

    def test_core2_blocks_when_conditioning_unresolved(self):
        with self.assertRaisesRegex(mod.BlueprintV4Error, "CHEM_CORE2_LEARNER_CONDITION_UNRESOLVED"):
            mod.validate_core2_conditioning({"schema_version": "4.0.0"}, POLICY)

    def test_core2_rejects_dual_authority(self):
        payload = {
            "schema_version": "4.0.0",
            "mode": "KNOWLEDGE_PERCENT",
            "knowledge_percent": 50,
            "owner_override": {"reason": "invalid"},
        }
        with self.assertRaisesRegex(mod.BlueprintV4Error, "DUAL_AUTHORITY"):
            mod.validate_core2_conditioning(payload, POLICY)


if __name__ == "__main__":
    unittest.main()
